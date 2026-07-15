"""Matched ReLU learners for the frozen value-logic experiment.

This module deliberately knows nothing about the synthetic oracle or its
records.  It accepts already-separated numeric feature panels and training
targets.  The adapter in :mod:`experiments.implementation` is the only layer
allowed to turn generator records into these arrays.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import isfinite, sqrt
import random
import time
from typing import Iterable, Mapping, Sequence

import numpy as np
import torch
from torch import Tensor, nn
from torch.nn import functional as F


STRUCTURED_OUTPUTS = 4
CE_OUTPUTS = 3
CENTER_ROWS = (0, 2)
RADIUS_ROWS = (1, 3)


@dataclass(frozen=True)
class WorldPanelData:
    """Numeric arrays grouped by independent world.

    Panels have shape ``(world, atom, feature)``.  Probe positions ``0..39``
    are loss atoms and ``40..79`` are latency atoms under the frozen
    generator.  Missing regression targets are represented by ``NaN`` and
    are masked, never imputed.
    """

    features: np.ndarray
    statistic_targets: np.ndarray
    schemas: np.ndarray
    state_targets: np.ndarray
    weights: np.ndarray

    def __post_init__(self) -> None:
        if self.features.ndim != 3:
            raise ValueError("features must have shape (world, atom, feature)")
        shape = self.features.shape[:2]
        arrays = (
            self.statistic_targets,
            self.schemas,
            self.state_targets,
            self.weights,
        )
        if any(array.shape != shape for array in arrays):
            raise ValueError("all panel arrays must share world/atom dimensions")
        if shape[1] != 80:
            raise ValueError("the frozen panel has exactly 80 atom probes per world")
        if not np.isfinite(self.features).all():
            raise ValueError("learner features must be finite")
        observed = ~np.isnan(self.statistic_targets)
        if not np.isfinite(self.statistic_targets[observed]).all():
            raise ValueError("observed statistic targets must be finite")
        if not np.isin(self.schemas, (0, 1)).all():
            raise ValueError("schema indices must be 0 (J) or 1 (T)")
        if not np.isin(self.state_targets, (0, 1, 2)).all():
            raise ValueError("state targets must be K3 class indices 0, 1, or 2")
        if not (np.isfinite(self.weights).all() and (self.weights > 0).all()):
            raise ValueError("training weights must be finite and positive")

    @property
    def world_count(self) -> int:
        return int(self.features.shape[0])

    @property
    def feature_count(self) -> int:
        return int(self.features.shape[2])


@dataclass(frozen=True)
class ArchitectureSpec:
    arm: str
    input_dim: int
    hidden_width: int
    output_dim: int
    parameter_budget: int
    parameter_count: int
    inference_flops: int


@dataclass(frozen=True)
class FitConfig:
    learning_rate: float
    weight_decay: float
    parameter_budget: int
    batch_worlds: int = 512
    max_epochs: int = 200
    patience_epochs: int = 20
    minimum_improvement: float = 1e-5
    gradient_norm_clip: float = 1.0
    validation_cadence: int = 5
    center_epochs: int = 100
    radius_epochs: int = 100

    def __post_init__(self) -> None:
        if self.learning_rate <= 0 or self.weight_decay < 0:
            raise ValueError("optimizer constants are invalid")
        if self.parameter_budget <= 0 or self.batch_worlds <= 0:
            raise ValueError("budget and world-batch size must be positive")
        if self.max_epochs <= 0 or self.patience_epochs <= 0:
            raise ValueError("epoch constants must be positive")
        if self.center_epochs + self.radius_epochs != self.max_epochs:
            raise ValueError("structured phases must exactly exhaust max_epochs")
        if self.validation_cadence <= 0:
            raise ValueError("validation cadence must be positive")


@dataclass(frozen=True)
class PhaseHistory:
    phase: str
    epochs_run: int
    best_epoch: int
    best_validation_loss: float
    optimizer_steps: int


@dataclass(frozen=True)
class FitSummary:
    arm: str
    seed: int
    architecture: ArchitectureSpec
    config: FitConfig
    phases: tuple[PhaseHistory, ...]
    parameter_hash: str
    wall_seconds: float

    @property
    def selection_loss(self) -> float:
        return self.phases[-1].best_validation_loss


@dataclass(frozen=True)
class TrialScore:
    arm: str
    config: FitConfig
    validation_loss: float


@dataclass(frozen=True)
class JointSelection:
    parameter_budget: int
    structured: TrialScore
    cross_entropy: TrialScore
    normalized_joint_regret: float


class ReluMLP(nn.Module):
    """Two-hidden-layer ReLU MLP with one vector-valued affine head."""

    def __init__(self, input_dim: int, hidden_width: int, output_dim: int) -> None:
        super().__init__()
        self.trunk = nn.Sequential(
            nn.Linear(input_dim, hidden_width),
            nn.ReLU(),
            nn.Linear(hidden_width, hidden_width),
            nn.ReLU(),
        )
        self.vector_head = nn.Linear(hidden_width, output_dim)
        if output_dim == STRUCTURED_OUTPUTS:
            with torch.no_grad():
                # ReLU radii start in their live region.  This is initialization,
                # not a logical state or grant convention.
                self.vector_head.bias[list(RADIUS_ROWS)] = 0.25

    def forward(self, features: Tensor) -> Tensor:
        return self.vector_head(self.trunk(features))


def parameter_count(input_dim: int, width: int, output_dim: int) -> int:
    return (input_dim + 1) * width + (width + 1) * width + (width + 1) * output_dim


def width_for_budget(input_dim: int, output_dim: int, budget: int) -> int:
    """Smallest equal hidden width whose parameter count meets ``budget``."""

    if input_dim <= 0 or output_dim <= 0 or budget <= 0:
        raise ValueError("architecture dimensions and budget must be positive")
    width = 1
    while parameter_count(input_dim, width, output_dim) < budget:
        width += 1
    return width


def architecture_spec(arm: str, input_dim: int, output_dim: int, budget: int) -> ArchitectureSpec:
    width = width_for_budget(input_dim, output_dim, budget)
    count = parameter_count(input_dim, width, output_dim)
    # Multiply-adds are counted as two FLOPs. ReLU comparisons are one FLOP.
    flops = 2 * (input_dim * width + width * width + width * output_dim) + 2 * width
    return ArchitectureSpec(arm, input_dim, width, output_dim, budget, count, flops)


def matched_architectures(input_dim: int, budget: int) -> tuple[ArchitectureSpec, ArchitectureSpec]:
    structured = architecture_spec("structured", input_dim, STRUCTURED_OUTPUTS, budget)
    ce = architecture_spec("cross_entropy", input_dim, CE_OUTPUTS, budget)
    mismatch = abs(structured.parameter_count - ce.parameter_count) / max(
        structured.parameter_count, ce.parameter_count
    )
    if mismatch > 0.02:
        raise ValueError("matched arms exceed the frozen two-percent parameter tolerance")
    return structured, ce


def initialize_paired(model: ReluMLP, spec: ArchitectureSpec, seed: int) -> None:
    """Initialize shared trunk coordinates identically across matched arms.

    When the 20k-budget arms differ by one hidden unit, both draw a common
    128-wide parent trunk and slice their declared width.  Head draws use an
    arm-specific stream, so changing head factorization cannot perturb the
    shared prefix.
    """

    reference_width = max(
        width_for_budget(spec.input_dim, STRUCTURED_OUTPUTS, spec.parameter_budget),
        width_for_budget(spec.input_dim, CE_OUTPUTS, spec.parameter_budget),
    )

    def generator(label: str) -> torch.Generator:
        token = sha256(f"paired-init-v1|{seed}|{label}".encode("utf-8")).digest()
        return torch.Generator(device="cpu").manual_seed(int.from_bytes(token[:8], "big"))

    def uniform(shape: tuple[int, ...], bound: float, label: str) -> Tensor:
        return torch.empty(shape).uniform_(-bound, bound, generator=generator(label))

    first: nn.Linear = model.trunk[0]  # type: ignore[assignment]
    second: nn.Linear = model.trunk[2]  # type: ignore[assignment]
    with torch.no_grad():
        first_parent = uniform(
            (reference_width, spec.input_dim),
            sqrt(6.0 / (spec.input_dim + reference_width)),
            "trunk:first:weight",
        )
        first.weight.copy_(first_parent[: spec.hidden_width])
        first.bias.copy_(
            uniform((reference_width,), 1.0 / sqrt(spec.input_dim), "trunk:first:bias")[
                : spec.hidden_width
            ]
        )
        second_parent = uniform(
            (reference_width, reference_width),
            sqrt(3.0 / reference_width),
            "trunk:second:weight",
        )
        second.weight.copy_(
            second_parent[: spec.hidden_width, : spec.hidden_width]
        )
        second.bias.copy_(
            uniform(
                (reference_width,),
                1.0 / sqrt(reference_width),
                "trunk:second:bias",
            )[: spec.hidden_width]
        )
        head_bound = sqrt(6.0 / (reference_width + spec.output_dim))
        head_parent = uniform(
            (spec.output_dim, reference_width),
            head_bound,
            f"head:{spec.arm}:weight",
        )
        model.vector_head.weight.copy_(head_parent[:, : spec.hidden_width])
        model.vector_head.bias.copy_(
            uniform(
                (spec.output_dim,),
                1.0 / sqrt(reference_width),
                f"head:{spec.arm}:bias",
            )
        )
        if spec.output_dim == STRUCTURED_OUTPUTS:
            model.vector_head.bias[list(RADIUS_ROWS)] += 0.25


def _seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)


def model_parameter_hash(model: nn.Module) -> str:
    digest = sha256()
    for name, value in sorted(model.state_dict().items()):
        digest.update(name.encode("utf-8"))
        digest.update(str(tuple(value.shape)).encode("ascii"))
        digest.update(value.detach().cpu().contiguous().numpy().tobytes())
    return digest.hexdigest()


def _panel_positions(epoch: int) -> tuple[int, int]:
    """One deterministic J/T probe per world, cycling through all 80 rows."""

    return epoch % 40, 40 + ((17 * epoch) % 40)


def _world_order(world_count: int, seed: int, epoch: int) -> np.ndarray:
    rng = np.random.default_rng(seed * 1_000_003 + epoch)
    return rng.permutation(world_count)


def _selected_batch(data: WorldPanelData, worlds: np.ndarray, epoch: int) -> tuple[Tensor, ...]:
    positions = np.asarray(_panel_positions(epoch), dtype=np.int64)
    features = data.features[worlds[:, None], positions[None, :], :].reshape(
        -1, data.feature_count
    )
    statistic = data.statistic_targets[worlds[:, None], positions[None, :]].reshape(-1)
    schemas = data.schemas[worlds[:, None], positions[None, :]].reshape(-1)
    states = data.state_targets[worlds[:, None], positions[None, :]].reshape(-1)
    weights = data.weights[worlds[:, None], positions[None, :]].reshape(-1)
    return (
        torch.from_numpy(features.astype(np.float32, copy=False)),
        torch.from_numpy(statistic.astype(np.float32, copy=False)),
        torch.from_numpy(schemas.astype(np.int64, copy=False)),
        torch.from_numpy(states.astype(np.int64, copy=False)),
        torch.from_numpy(weights.astype(np.float32, copy=False)),
    )


def _weighted_schema_mean(values: Tensor, schemas: Tensor, weights: Tensor, mask: Tensor) -> Tensor:
    terms: list[Tensor] = []
    for schema in (0, 1):
        selected = mask & (schemas == schema)
        if torch.any(selected):
            local_weights = weights[selected]
            terms.append(torch.sum(values[selected] * local_weights) / torch.sum(local_weights))
    if not terms:
        raise ValueError("a training batch contains no eligible targets")
    return torch.stack(terms).mean()


def _structured_loss(outputs: Tensor, targets: Tensor, schemas: Tensor, weights: Tensor, phase: str) -> Tensor:
    centers = torch.where(schemas == 0, outputs[:, 0], outputs[:, 2])
    radii = torch.where(schemas == 0, F.relu(outputs[:, 1]), F.relu(outputs[:, 3]))
    observed = ~torch.isnan(targets)
    if phase == "center":
        values = (centers - torch.nan_to_num(targets)) ** 2
    elif phase == "radius":
        clean = torch.nan_to_num(targets)
        lower = centers.detach() - radii
        upper = centers.detach() + radii
        values = (upper - lower) + 20.0 * F.relu(lower - clean) + 20.0 * F.relu(clean - upper)
    else:
        raise ValueError(f"unknown structured phase {phase!r}")
    return _weighted_schema_mean(values, schemas, weights, observed)


def _ce_loss(outputs: Tensor, states: Tensor, schemas: Tensor, weights: Tensor) -> Tensor:
    per_row = F.cross_entropy(outputs, states, reduction="none")
    return _weighted_schema_mean(per_row, schemas, weights, torch.ones_like(states, dtype=torch.bool))


@torch.no_grad()
def _validation_loss(model: ReluMLP, data: WorldPanelData, arm: str, phase: str, chunk_rows: int = 32768) -> float:
    model.eval()
    features = data.features.reshape(-1, data.feature_count)
    statistic = data.statistic_targets.reshape(-1)
    schemas = data.schemas.reshape(-1)
    states = data.state_targets.reshape(-1)
    weights = data.weights.reshape(-1)
    totals = {0: 0.0, 1: 0.0}
    weight_totals = {0: 0.0, 1: 0.0}
    for start in range(0, len(features), chunk_rows):
        stop = min(len(features), start + chunk_rows)
        x = torch.from_numpy(features[start:stop].astype(np.float32, copy=False))
        out = model(x)
        local_schema = torch.from_numpy(schemas[start:stop].astype(np.int64, copy=False))
        local_weight = torch.from_numpy(weights[start:stop].astype(np.float32, copy=False))
        if arm == "structured":
            local_target = torch.from_numpy(statistic[start:stop].astype(np.float32, copy=False))
            centers = torch.where(local_schema == 0, out[:, 0], out[:, 2])
            radii = torch.where(local_schema == 0, F.relu(out[:, 1]), F.relu(out[:, 3]))
            mask = ~torch.isnan(local_target)
            clean = torch.nan_to_num(local_target)
            if phase == "center":
                per_row = (centers - clean) ** 2
            else:
                lower = centers - radii
                upper = centers + radii
                per_row = (upper - lower) + 20.0 * F.relu(lower - clean) + 20.0 * F.relu(clean - upper)
        else:
            local_state = torch.from_numpy(states[start:stop].astype(np.int64, copy=False))
            per_row = F.cross_entropy(out, local_state, reduction="none")
            mask = torch.ones_like(local_state, dtype=torch.bool)
        for schema in (0, 1):
            selected = mask & (local_schema == schema)
            if torch.any(selected):
                totals[schema] += float(torch.sum(per_row[selected] * local_weight[selected]))
                weight_totals[schema] += float(torch.sum(local_weight[selected]))
    included = [totals[schema] / weight_totals[schema] for schema in (0, 1) if weight_totals[schema] > 0]
    if not included:
        raise ValueError("validation contains no eligible rows")
    return sum(included) / len(included)


def _run_phase(
    model: ReluMLP,
    train: WorldPanelData,
    validation: WorldPanelData,
    config: FitConfig,
    seed: int,
    *,
    arm: str,
    phase: str,
    max_epochs: int,
    epoch_offset: int,
) -> PhaseHistory:
    if arm == "structured" and phase == "radius":
        for parameter in model.trunk.parameters():
            parameter.requires_grad_(False)
        preserved_weight = model.vector_head.weight[list(CENTER_ROWS)].detach().clone()
        preserved_bias = model.vector_head.bias[list(CENTER_ROWS)].detach().clone()
    else:
        preserved_weight = preserved_bias = None

    optimizer = torch.optim.AdamW(
        (parameter for parameter in model.parameters() if parameter.requires_grad),
        lr=config.learning_rate,
        weight_decay=config.weight_decay,
    )
    best_state: dict[str, Tensor] | None = None
    best_loss = float("inf")
    best_epoch = -1
    stale_epochs = 0
    steps = 0
    epochs_run = 0
    for local_epoch in range(max_epochs):
        epoch = epoch_offset + local_epoch
        model.train()
        order = _world_order(train.world_count, seed, epoch)
        for start in range(0, train.world_count, config.batch_worlds):
            worlds = order[start : start + config.batch_worlds]
            features, statistic, schemas, states, weights = _selected_batch(train, worlds, epoch)
            optimizer.zero_grad(set_to_none=True)
            outputs = model(features)
            loss = (
                _structured_loss(outputs, statistic, schemas, weights, phase)
                if arm == "structured"
                else _ce_loss(outputs, states, schemas, weights)
            )
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.gradient_norm_clip)
            optimizer.step()
            if preserved_weight is not None and preserved_bias is not None:
                with torch.no_grad():
                    model.vector_head.weight[list(CENTER_ROWS)] = preserved_weight
                    model.vector_head.bias[list(CENTER_ROWS)] = preserved_bias
            steps += 1
        epochs_run = local_epoch + 1
        if epochs_run % config.validation_cadence != 0 and epochs_run != max_epochs:
            continue
        score = _validation_loss(model, validation, arm, phase)
        if best_loss - score >= config.minimum_improvement:
            best_loss = score
            best_epoch = epochs_run
            best_state = {name: value.detach().clone() for name, value in model.state_dict().items()}
            stale_epochs = 0
        else:
            stale_epochs += config.validation_cadence
        if stale_epochs >= config.patience_epochs:
            break
    if best_state is None:
        raise RuntimeError("training phase never produced a finite validation checkpoint")
    model.load_state_dict(best_state)
    return PhaseHistory(phase, epochs_run, best_epoch, best_loss, steps)


def fit_structured(
    train: WorldPanelData,
    validation: WorldPanelData,
    spec: ArchitectureSpec,
    config: FitConfig,
    seed: int,
) -> tuple[ReluMLP, FitSummary]:
    if spec.arm != "structured" or spec.output_dim != STRUCTURED_OUTPUTS:
        raise ValueError("structured fitting requires the structured architecture")
    if train.feature_count != spec.input_dim or validation.feature_count != spec.input_dim:
        raise ValueError("feature dimension does not match architecture")
    _seed_everything(seed)
    started = time.perf_counter()
    model = ReluMLP(spec.input_dim, spec.hidden_width, spec.output_dim)
    initialize_paired(model, spec, seed)
    center = _run_phase(
        model,
        train,
        validation,
        config,
        seed,
        arm="structured",
        phase="center",
        max_epochs=config.center_epochs,
        epoch_offset=0,
    )
    radius = _run_phase(
        model,
        train,
        validation,
        config,
        seed,
        arm="structured",
        phase="radius",
        max_epochs=config.radius_epochs,
        epoch_offset=config.center_epochs,
    )
    elapsed = time.perf_counter() - started
    summary = FitSummary(
        "structured", seed, spec, config, (center, radius), model_parameter_hash(model), elapsed
    )
    return model, summary


def fit_cross_entropy(
    train: WorldPanelData,
    validation: WorldPanelData,
    spec: ArchitectureSpec,
    config: FitConfig,
    seed: int,
) -> tuple[ReluMLP, FitSummary]:
    if spec.arm != "cross_entropy" or spec.output_dim != CE_OUTPUTS:
        raise ValueError("CE fitting requires the cross-entropy architecture")
    if train.feature_count != spec.input_dim or validation.feature_count != spec.input_dim:
        raise ValueError("feature dimension does not match architecture")
    _seed_everything(seed)
    started = time.perf_counter()
    model = ReluMLP(spec.input_dim, spec.hidden_width, spec.output_dim)
    initialize_paired(model, spec, seed)
    phase = _run_phase(
        model,
        train,
        validation,
        config,
        seed,
        arm="cross_entropy",
        phase="cross_entropy",
        max_epochs=config.max_epochs,
        epoch_offset=0,
    )
    elapsed = time.perf_counter() - started
    summary = FitSummary(
        "cross_entropy", seed, spec, config, (phase,), model_parameter_hash(model), elapsed
    )
    return model, summary


@torch.no_grad()
def predict(model: ReluMLP, features: np.ndarray, chunk_rows: int = 65536) -> np.ndarray:
    if features.ndim != 2:
        raise ValueError("prediction features must be a two-dimensional matrix")
    model.eval()
    chunks: list[np.ndarray] = []
    for start in range(0, len(features), chunk_rows):
        x = torch.from_numpy(features[start : start + chunk_rows].astype(np.float32, copy=False))
        chunks.append(model(x).cpu().numpy())
    if not chunks:
        return np.empty((0, model.vector_head.out_features), dtype=np.float32)
    return np.concatenate(chunks, axis=0)


def choose_joint_capacity(trials: Iterable[TrialScore]) -> JointSelection:
    """Select one shared budget while allowing arm-specific optimizer constants.

    Loss units differ across arms, so the shared budget minimizes the sum of
    each arm's relative regret from its own best internal-selection loss.  A
    tie selects the smaller budget.  This keeps the final arms capacity
    matched without comparing raw MSE/interval units to cross entropy.
    """

    records = tuple(trials)
    arms = {record.arm for record in records}
    if arms != {"structured", "cross_entropy"}:
        raise ValueError("joint selection requires trials for both learned arms")
    if any(record.validation_loss <= 0 or not isfinite(record.validation_loss) for record in records):
        raise ValueError("trial validation losses must be finite and positive")
    budgets = sorted({record.config.parameter_budget for record in records})
    global_best = {
        arm: min(record.validation_loss for record in records if record.arm == arm)
        for arm in arms
    }
    candidates: list[JointSelection] = []
    for budget in budgets:
        best: dict[str, TrialScore] = {}
        for arm in arms:
            local = [
                record
                for record in records
                if record.arm == arm and record.config.parameter_budget == budget
            ]
            if not local:
                raise ValueError(f"budget {budget} is missing trials for arm {arm}")
            best[arm] = min(
                local,
                key=lambda record: (
                    record.validation_loss,
                    record.config.learning_rate,
                    record.config.weight_decay,
                ),
            )
        regret = sum(best[arm].validation_loss / global_best[arm] - 1.0 for arm in arms)
        candidates.append(
            JointSelection(budget, best["structured"], best["cross_entropy"], regret)
        )
    return min(candidates, key=lambda candidate: (candidate.normalized_joint_regret, candidate.parameter_budget))


def frozen_grid(
    learning_rates: Sequence[float],
    weight_decays: Sequence[float],
    budgets: Sequence[int],
) -> tuple[FitConfig, ...]:
    configs = tuple(
        FitConfig(learning_rate, weight_decay, budget)
        for learning_rate in learning_rates
        for weight_decay in weight_decays
        for budget in budgets
    )
    if len(configs) != 18:
        raise ValueError("the frozen optimizer grid must contain exactly 18 trials")
    return configs


def state_dict_arrays(model: ReluMLP) -> Mapping[str, np.ndarray]:
    """Portable array form used by the Task 21 artifact writer."""

    return {
        name: value.detach().cpu().numpy().copy()
        for name, value in model.state_dict().items()
    }
