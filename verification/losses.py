"""Executable witnesses for the Task 18 learning-objective contract.

The functions here are deliberately smaller than a training framework.  They
make the chosen structured loss, calibration proposal, symbolic decoder,
classification baseline, router ranking loss, and selective-risk accounting
executable with only the standard library.  None of these functions accepts a
calibration proposal as a proof or certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import ceil, exp, inf, isfinite, log, log1p
from typing import Iterable, Mapping, Sequence

from verification.kernel import AtomValue, Outcome, meet


@dataclass(frozen=True)
class StatisticExample:
    """One externally sourced atom-statistic target and one model proposal.

    ``target=None`` is explicit missingness.  Such an example is excluded from
    the statistic loss rather than silently imputed as zero.
    """

    atom_id: str
    schema_id: str
    source_id: str
    target: float | None
    center: float
    radius: float
    scale: float
    weight: float = 1.0

    def __post_init__(self) -> None:
        if not self.atom_id or not self.schema_id or not self.source_id:
            raise ValueError("statistic examples require atom, schema, and source identities")
        if not isfinite(self.center):
            raise ValueError("predicted center must be finite")
        if self.radius < 0 or not isfinite(self.radius):
            raise ValueError("predicted radius must be finite and nonnegative")
        if self.scale <= 0 or not isfinite(self.scale):
            raise ValueError("normalization scale must be finite and positive")
        if self.weight <= 0 or not isfinite(self.weight):
            raise ValueError("example weight must be finite and positive")
        if self.target is not None and not isfinite(self.target):
            raise ValueError("observed statistic target must be finite")

    @property
    def lower(self) -> float:
        return self.center - self.radius

    @property
    def upper(self) -> float:
        return self.center + self.radius


@dataclass(frozen=True)
class StructuredLoss:
    total: float
    center: float
    interval: float
    included_examples: int
    included_schemas: int


def interval_score(
    target: float,
    lower: float,
    upper: float,
    miscoverage: float,
) -> float:
    """Central interval score; smaller is better."""

    if lower > upper:
        raise ValueError("interval lower bound exceeds upper bound")
    if not 0 < miscoverage < 1:
        raise ValueError("miscoverage must lie strictly between zero and one")
    score = upper - lower
    if target < lower:
        score += (2.0 / miscoverage) * (lower - target)
    elif target > upper:
        score += (2.0 / miscoverage) * (target - upper)
    return score


def structured_statistic_loss(
    examples: Iterable[StatisticExample],
    *,
    miscoverage: float,
    center_weight: float = 1.0,
    interval_weight: float = 1.0,
) -> StructuredLoss:
    """Schema-balanced standardized center plus interval loss.

    Each schema contributes one mean, so a frequently instantiated atom family
    does not dominate solely by cardinality.  Targets that are explicitly
    missing contribute nothing and are counted separately by callers.  This
    computes the objective value only; the reference optimizer freezes or
    stop-gradients the center while fitting the radius.
    """

    if center_weight < 0 or interval_weight < 0:
        raise ValueError("loss weights must be nonnegative")
    if center_weight == 0 and interval_weight == 0:
        raise ValueError("at least one statistic-loss component must be active")

    grouped: dict[str, list[tuple[float, float, float]]] = {}
    included = 0
    for example in examples:
        if example.target is None:
            continue
        target = example.target / example.scale
        center = example.center / example.scale
        lower = example.lower / example.scale
        upper = example.upper / example.scale
        center_term = (center - target) ** 2
        interval_term = interval_score(target, lower, upper, miscoverage)
        grouped.setdefault(example.schema_id, []).append(
            (center_term, interval_term, example.weight)
        )
        included += 1

    if not grouped:
        raise ValueError("structured statistic loss has no observed targets")

    schema_centers: list[float] = []
    schema_intervals: list[float] = []
    for records in grouped.values():
        total_weight = sum(weight for _, _, weight in records)
        schema_centers.append(
            sum(center * weight for center, _, weight in records) / total_weight
        )
        schema_intervals.append(
            sum(interval * weight for _, interval, weight in records) / total_weight
        )
    center_mean = sum(schema_centers) / len(schema_centers)
    interval_mean = sum(schema_intervals) / len(schema_intervals)
    return StructuredLoss(
        center_weight * center_mean + interval_weight * interval_mean,
        center_mean,
        interval_mean,
        included,
        len(grouped),
    )


def residual_nonconformity(target: float, lower: float, upper: float) -> float:
    """Additive expansion needed for an interval proposal to include a target."""

    if lower > upper:
        raise ValueError("interval lower bound exceeds upper bound")
    return max(lower - target, target - upper, 0.0)


@dataclass(frozen=True)
class CalibrationProposal:
    """A held-out finite-sample radius proposal, not an accepted certificate."""

    radius: float
    miscoverage: float
    calibration_count: int
    rank: int


def proposed_calibration_radius(
    residual_scores: Sequence[float], miscoverage: float
) -> CalibrationProposal:
    """Split-conformal-style finite quantile, including the infinity sentinel.

    The rank is ``ceil((n+1)(1-alpha))``.  When that rank exceeds the number of
    finite calibration scores, the valid finite-sample proposal is unbounded.
    Exchangeability, split integrity, scope, and downstream-risk translation
    are external certificate-mode obligations.
    """

    if not residual_scores:
        raise ValueError("calibration requires at least one residual score")
    if not 0 < miscoverage < 1:
        raise ValueError("miscoverage must lie strictly between zero and one")
    if any(score < 0 or not isfinite(score) for score in residual_scores):
        raise ValueError("calibration residuals must be finite and nonnegative")
    count = len(residual_scores)
    rank = ceil((count + 1) * (1.0 - miscoverage))
    radius = inf if rank > count else sorted(residual_scores)[rank - 1]
    return CalibrationProposal(radius, miscoverage, count, rank)


def expand_interval(lower: float, upper: float, radius: float) -> tuple[float, float]:
    if lower > upper:
        raise ValueError("interval lower bound exceeds upper bound")
    if radius < 0:
        raise ValueError("calibration radius must be nonnegative")
    return lower - radius, upper + radius


def decode_upper_region(
    lower: float,
    upper: float,
    threshold: float,
    *,
    evidence_usable: bool,
    can_support: bool = True,
    can_refute: bool = True,
) -> AtomValue:
    """Exact scalar ``K_3`` decoder with inclusive support and strict refutation."""

    if lower > upper:
        raise ValueError("interval lower bound exceeds upper bound")
    if not evidence_usable:
        return AtomValue.OPEN
    if upper <= threshold and can_support:
        return AtomValue.SUPPORTED
    if lower > threshold and can_refute:
        return AtomValue.REFUTED
    return AtomValue.OPEN


def derive_public_outcome(
    *, well_formed: bool, required_atom_values: Iterable[AtomValue]
) -> Outcome:
    """Derive the public outcome symbolically; there is no status logit here."""

    if not well_formed:
        return Outcome.UNDEFINED
    aggregate = meet(required_atom_values)
    if aggregate is AtomValue.SUPPORTED:
        return Outcome.GRANTED
    if aggregate is AtomValue.REFUTED:
        return Outcome.REFUSED
    return Outcome.WITHHELD


def weighted_binary_cross_entropy(
    target: bool,
    reject_probability: float,
    *,
    reject_weight: float = 1.0,
    accept_weight: float = 1.0,
) -> float:
    """Asymmetric auxiliary loss for an externally labeled reject proposal."""

    if not 0 < reject_probability < 1:
        raise ValueError("probability must lie strictly between zero and one")
    if reject_weight <= 0 or accept_weight <= 0:
        raise ValueError("binary-loss weights must be positive")
    if target:
        return -reject_weight * log(reject_probability)
    return -accept_weight * log(1.0 - reject_probability)


def atom_cross_entropy(
    logits: Mapping[AtomValue, float], target: AtomValue
) -> float:
    """Independent three-way atom-state baseline loss."""

    if set(logits) != set(AtomValue):
        raise ValueError("atom baseline requires one logit for every K_3 value")
    maximum = max(logits.values())
    log_normalizer = maximum + log(sum(exp(value - maximum) for value in logits.values()))
    return log_normalizer - logits[target]


@dataclass(frozen=True)
class RouterPair:
    left_score: float
    right_score: float
    left_cost: float
    right_cost: float
    left_active: bool = True
    right_active: bool = True
    comparison_resolved: bool = True


@dataclass(frozen=True)
class MaskedLoss:
    value: float | None
    included: int


def _softplus(value: float) -> float:
    if value > 0:
        return value + log1p(exp(-value))
    return log1p(exp(value))


def pairwise_router_loss(pairs: Iterable[RouterPair]) -> MaskedLoss:
    """Pairwise logistic ranking over resolved pairs in the exact active set."""

    terms: list[float] = []
    for pair in pairs:
        if not (pair.left_active and pair.right_active and pair.comparison_resolved):
            continue
        if pair.left_cost == pair.right_cost:
            continue
        direction = 1.0 if pair.left_cost < pair.right_cost else -1.0
        terms.append(_softplus(-direction * (pair.left_score - pair.right_score)))
    if not terms:
        return MaskedLoss(None, 0)
    return MaskedLoss(sum(terms) / len(terms), len(terms))


@dataclass(frozen=True)
class SelectiveMetrics:
    coverage: float
    selective_risk: float | None
    deployed_risk: float
    selected_count: int


def selective_metrics(
    selected_losses: Sequence[float],
    accepted: Sequence[bool],
    fallback_losses: Sequence[float],
) -> SelectiveMetrics:
    """Joint coverage, conditional selected risk, and fallback-inclusive risk."""

    if not selected_losses:
        raise ValueError("selective metrics require at least one case")
    if len(selected_losses) != len(accepted) or len(accepted) != len(fallback_losses):
        raise ValueError("loss, acceptance, and fallback vectors must align")
    selected = [loss for loss, use in zip(selected_losses, accepted) if use]
    deployed = [
        loss if use else fallback
        for loss, use, fallback in zip(selected_losses, accepted, fallback_losses)
    ]
    count = len(selected)
    return SelectiveMetrics(
        count / len(accepted),
        None if not selected else sum(selected) / count,
        sum(deployed) / len(deployed),
        count,
    )


def normalized_positive_surplus(
    margin: float, scale: float, *, supported: bool
) -> float:
    """Dual-use feature with a fixed unit registry and symbolic support gate."""

    if scale <= 0:
        raise ValueError("normalization scale must be positive")
    return max(0.0, margin / scale) if supported else 0.0


def validate_disjoint_splits(
    train_ids: Iterable[str], calibration_ids: Iterable[str], test_ids: Iterable[str]
) -> None:
    """Reject train/calibration/test leakage in the reference protocol."""

    named = {
        "train": set(train_ids),
        "calibration": set(calibration_ids),
        "test": set(test_ids),
    }
    for (left_name, left), (right_name, right) in combinations(named.items(), 2):
        overlap = left & right
        if overlap:
            raise ValueError(
                f"{left_name}/{right_name} split overlap: {sorted(overlap)!r}"
            )
