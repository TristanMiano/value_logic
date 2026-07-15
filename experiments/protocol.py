"""Task 19A synthetic generator and frozen-protocol primitives.

This module is deliberately standard-library only.  It implements the
independent world generator, exact oracle semantics, scorer-input firewall,
proposal binding checker, implicit role manifests, metric skeleton, power
arithmetic, succession fixture, and final-role embargo.  It does not implement
either learned arm and it never treats a prediction as evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from math import ceil, cos, inf, isfinite, log, pi, sqrt
import random
from statistics import mean, stdev
from typing import Any, Iterable, Mapping, Sequence

from verification.kernel import AtomValue, Interval, Outcome
from verification.losses import decode_upper_region, derive_public_outcome


PROTOCOL_VERSION = "value-logic-experiment-v1.0.0"
GENERATOR_VERSION = "synthetic-succession-v1"
ORACLE_VERSION = "conditional-normal-region-v1"
K_90 = 1.6448536269514722
ALPHA_CAL = 0.10
PILOT_WORLD_COUNT = 256
FINAL_WORLD_FLOOR = 400
FINAL_WORLD_CAP = 5000
WORLD_BLOCK_SIZE = 100
FIT_SEEDS = (101, 211, 307, 401, 503, 601, 701, 809)
BOOTSTRAP_SEED = 19012026


class Role(str, Enum):
    PILOT = "pilot"
    TRAIN = "train"
    CALIBRATION = "envelope_calibration"
    VALIDATION = "reject_router_validation"
    SYSTEM_AUDIT = "system_audit"
    FINAL_CONFIRMATION = "final_confirmation"


PRODUCTION_ROLES = (
    Role.TRAIN,
    Role.CALIBRATION,
    Role.VALIDATION,
    Role.SYSTEM_AUDIT,
    Role.FINAL_CONFIRMATION,
)

ROLE_SEEDS: Mapping[Role, str] = {
    Role.PILOT: "pilot-7b9d41c6",
    Role.TRAIN: "train-1e824bd9",
    Role.CALIBRATION: "cal-5739ad20",
    Role.VALIDATION: "validation-8fa301bc",
    Role.SYSTEM_AUDIT: "audit-294c0de7",
    Role.FINAL_CONFIRMATION: "confirmation-6d17f4a2",
}


class FinalEmbargoError(RuntimeError):
    """Raised when code tries to materialize a final world before Task 21."""


class Schema(str, Enum):
    LOSS = "J"
    LATENCY = "T"


class Plan(str, Enum):
    OLD = "O"
    SUCCESSOR = "S"
    NEW = "N"
    FALLBACK = "F"


class ContextCell(str, Enum):
    OLD_ONLY = "old_only"
    OVERLAP = "old_successor_overlap"
    SUCCESSOR_ONLY = "successor_only"
    GAP = "stage0_gap"


CELL_BOUNDS: Mapping[ContextCell, tuple[float, float]] = {
    ContextCell.OLD_ONLY: (-1.0, -0.35),
    ContextCell.OVERLAP: (-0.35, 0.35),
    ContextCell.SUCCESSOR_ONLY: (0.35, 0.85),
    ContextCell.GAP: (0.85, 1.0),
}

CELL_DESIGN_COUNTS: Mapping[ContextCell, int] = {
    ContextCell.OLD_ONLY: 8,
    ContextCell.OVERLAP: 12,
    ContextCell.SUCCESSOR_ONLY: 10,
    ContextCell.GAP: 10,
}

CELL_TARGET_MASS: Mapping[ContextCell, float] = {
    ContextCell.OLD_ONLY: 0.325,
    ContextCell.OVERLAP: 0.35,
    ContextCell.SUCCESSOR_ONLY: 0.25,
    ContextCell.GAP: 0.075,
}

CELL_DESIGN_MASS: Mapping[ContextCell, float] = {
    cell: count / 40.0 for cell, count in CELL_DESIGN_COUNTS.items()
}


class AtomStratum(str, Enum):
    STRICT_SUPPORTED = "strict_supported"
    BOUNDARY_SUPPORTED = "boundary_supported"
    CROSSING_OPEN = "crossing_or_polarity_open"
    MISSING_OPEN = "missing_open"
    INVALID_OPEN = "invalid_open"
    REFUTED = "refuted"


STRATUM_DESIGN_COUNTS: Mapping[AtomStratum, int] = {
    AtomStratum.STRICT_SUPPORTED: 10,
    AtomStratum.BOUNDARY_SUPPORTED: 8,
    AtomStratum.CROSSING_OPEN: 8,
    AtomStratum.MISSING_OPEN: 4,
    AtomStratum.INVALID_OPEN: 4,
    AtomStratum.REFUTED: 6,
}

STRATUM_TARGET_MASS: Mapping[AtomStratum, float] = {
    AtomStratum.STRICT_SUPPORTED: 0.40,
    AtomStratum.BOUNDARY_SUPPORTED: 0.05,
    AtomStratum.CROSSING_OPEN: 0.20,
    AtomStratum.MISSING_OPEN: 0.05,
    AtomStratum.INVALID_OPEN: 0.05,
    AtomStratum.REFUTED: 0.25,
}

STRATUM_DESIGN_MASS: Mapping[AtomStratum, float] = {
    stratum: count / 40.0 for stratum, count in STRATUM_DESIGN_COUNTS.items()
}


class EvidenceMode(str, Enum):
    TWO_SIDED = "checked_two_sided"
    UPPER_ONLY = "checked_upper_bound"
    LOWER_ONLY = "checked_lower_bound"
    EMPIRICAL_ONLY = "empirical_proposal_only"


MODE_POLARITY: Mapping[EvidenceMode, tuple[bool, bool]] = {
    EvidenceMode.TWO_SIDED: (True, True),
    EvidenceMode.UPPER_ONLY: (True, False),
    EvidenceMode.LOWER_ONLY: (False, True),
    EvidenceMode.EMPIRICAL_ONLY: (False, False),
}


@dataclass(frozen=True)
class WorldIdentity:
    role: Role
    index: int
    world_root: str
    trajectory_root: str
    provenance_root: str
    plan_family_root: str


@dataclass(frozen=True)
class AtomRecord:
    atom_id: str
    world_root: str
    schema: Schema
    plan: Plan
    stage: int
    cell: ContextCell
    x: float
    complexity: float
    difficulty: float
    oracle_mean: float
    oracle_scale: float
    oracle_target: float
    learning_target: float | None
    reference_region: Interval
    threshold: float
    stratum: AtomStratum
    mode: EvidenceMode
    evidence_present: bool
    evidence_valid: bool
    can_support: bool
    can_refute: bool
    value: AtomValue
    diagnostic: str
    target_weight: float
    design_weight: float

    @property
    def importance_weight(self) -> float:
        return self.target_weight / self.design_weight

    @property
    def boundary(self) -> bool:
        return self.stratum is AtomStratum.BOUNDARY_SUPPORTED


@dataclass(frozen=True)
class RequestAtom:
    name: str
    schema: Schema
    region: Interval
    threshold: float
    value: AtomValue
    diagnostic: str
    evidence_present: bool
    evidence_valid: bool
    can_support: bool
    can_refute: bool
    boundary: bool = False


@dataclass(frozen=True)
class RequestRecord:
    request_id: str
    world_root: str
    stage: int
    cell: ContextCell
    plan: Plan
    x: float
    complexity: float
    difficulty: float
    well_formed: bool
    wf_diagnostic: str | None
    focal_atom: str
    atoms: tuple[RequestAtom, ...]
    outcome: Outcome
    boundary_case: bool
    fallback_loss: float
    delta: float
    target_weight: float
    design_weight: float

    @property
    def importance_weight(self) -> float:
        return self.target_weight / self.design_weight


@dataclass(frozen=True)
class GeneratedWorld:
    identity: WorldIdentity
    hidden_loss_intercepts: Mapping[Plan, float]
    hidden_latency_intercepts: Mapping[Plan, float]
    probes: tuple[AtomRecord, ...]
    requests: tuple[RequestRecord, ...]


@dataclass(frozen=True)
class EvidenceSnapshot:
    region: Interval
    valid: bool
    version: str


@dataclass(frozen=True)
class UpdateEvent:
    event_id: str
    writes: frozenset[str]
    replacement_region: Interval | None = None
    replacement_validity: bool | None = None
    replacement_version: str | None = None


def update_is_relevant(
    read_footprint: frozenset[str], event: UpdateEvent
) -> bool:
    return bool(read_footprint & event.writes)


def apply_evidence_update(
    snapshot: EvidenceSnapshot,
    read_footprint: frozenset[str],
    event: UpdateEvent,
) -> EvidenceSnapshot:
    """Apply only writes intersecting the frozen request footprint."""

    if not update_is_relevant(read_footprint, event):
        return snapshot
    return EvidenceSnapshot(
        event.replacement_region or snapshot.region,
        snapshot.valid
        if event.replacement_validity is None
        else event.replacement_validity,
        event.replacement_version or snapshot.version,
    )


def _digest(*parts: object) -> str:
    payload = "|".join(str(part) for part in parts).encode("utf-8")
    return sha256(payload).hexdigest()


def _seed_int(*parts: object) -> int:
    return int(_digest(*parts)[:16], 16)


def _standard_normal(rng: random.Random) -> float:
    """Version-stable Box--Muller draw using Random.random only."""

    u1 = max(rng.random(), 2.0**-53)
    u2 = rng.random()
    return sqrt(-2.0 * log(u1)) * cos(2.0 * pi * u2)


def world_identity(role: Role, index: int) -> WorldIdentity:
    if index < 0:
        raise ValueError("world index must be nonnegative")
    seed = ROLE_SEEDS[role]
    return WorldIdentity(
        role=role,
        index=index,
        world_root=f"world:{_digest(PROTOCOL_VERSION, seed, 'world', index)}",
        trajectory_root=f"trajectory:{_digest(PROTOCOL_VERSION, seed, 'trajectory', index)}",
        provenance_root=f"provenance:{_digest(PROTOCOL_VERSION, seed, 'provenance', index)}",
        plan_family_root=f"family:{_digest(PROTOCOL_VERSION, seed, 'family', index)}",
    )


def plan_for_cell(cell: ContextCell, index: int) -> tuple[Plan, int]:
    if cell is ContextCell.OLD_ONLY:
        return Plan.OLD, 0
    if cell is ContextCell.OVERLAP:
        return (Plan.OLD if index % 2 == 0 else Plan.SUCCESSOR), 0
    if cell is ContextCell.SUCCESSOR_ONLY:
        return Plan.SUCCESSOR, 0
    return Plan.NEW, 3


def loss_mean(
    plan: Plan,
    x: float,
    complexity: float,
    intercepts: Mapping[Plan, float],
) -> float:
    relu = lambda value: max(0.0, value)
    if plan is Plan.FALLBACK:
        return 0.32 + 0.05 * complexity + 0.02 * abs(x)
    if plan is Plan.OLD:
        return (
            0.10
            + 0.03 * complexity
            + 0.04 * abs(x + 0.55)
            + 0.22 * relu(x - 0.20)
            + intercepts[plan]
        )
    if plan is Plan.SUCCESSOR:
        return (
            0.12
            + 0.05 * complexity
            + 0.035 * abs(x)
            + 0.08 * relu(x - 0.75)
            + intercepts[plan]
        )
    if plan is Plan.NEW:
        return (
            0.09
            + 0.04 * complexity
            + 0.025 * abs(x - 0.55)
            + 0.06 * relu(0.10 - x)
            + intercepts[plan]
        )
    raise ValueError(f"unsupported plan {plan!r}")


def latency_mean(
    plan: Plan,
    x: float,
    complexity: float,
    intercepts: Mapping[Plan, float],
) -> float:
    if plan is Plan.OLD:
        return 35.0 + 8.0 * complexity + 5.0 * abs(x + 0.50) + intercepts[plan]
    if plan is Plan.SUCCESSOR:
        return 42.0 + 6.0 * complexity + 4.0 * abs(x) + intercepts[plan]
    if plan is Plan.NEW:
        return 38.0 + 7.0 * complexity + 3.0 * abs(x - 0.50) + intercepts[plan]
    raise ValueError("fallback latency is not a registered target schema")


def outcome_scale(schema: Schema, complexity: float, difficulty: float) -> float:
    if schema is Schema.LOSS:
        return 0.006 + 0.006 * difficulty + 0.002 * complexity
    return 0.60 + 1.00 * difficulty + 0.40 * complexity


def _mode_for_stratum(stratum: AtomStratum, index: int) -> EvidenceMode:
    if stratum in {AtomStratum.STRICT_SUPPORTED, AtomStratum.BOUNDARY_SUPPORTED}:
        return EvidenceMode.TWO_SIDED if index % 2 == 0 else EvidenceMode.UPPER_ONLY
    if stratum is AtomStratum.REFUTED:
        return EvidenceMode.TWO_SIDED if index % 2 == 0 else EvidenceMode.LOWER_ONLY
    if stratum is AtomStratum.CROSSING_OPEN:
        modes = (
            EvidenceMode.TWO_SIDED,
            EvidenceMode.EMPIRICAL_ONLY,
            EvidenceMode.UPPER_ONLY,
            EvidenceMode.LOWER_ONLY,
        )
        return modes[index % len(modes)]
    return EvidenceMode.TWO_SIDED


def decode_evidence(
    region: Interval,
    threshold: float,
    *,
    evidence_present: bool,
    evidence_valid: bool,
    can_support: bool,
    can_refute: bool,
) -> AtomValue:
    return decode_upper_region(
        region.lower,
        region.upper,
        threshold,
        evidence_usable=evidence_present and evidence_valid,
        can_support=can_support,
        can_refute=can_refute,
    )


def exact_active_set(outcomes: Mapping[Plan, Outcome]) -> tuple[Plan, ...]:
    """Return every and only Granted plan, preserving simultaneous licenses."""

    return tuple(
        plan
        for plan in (Plan.OLD, Plan.SUCCESSOR, Plan.NEW)
        if outcomes.get(plan) is Outcome.GRANTED
    )


def select_or_fallback(
    outcomes: Mapping[Plan, Outcome],
    scores: Mapping[Plan, float],
    *,
    tie_order: Sequence[Plan] = (Plan.NEW, Plan.SUCCESSOR, Plan.OLD),
) -> Plan:
    """Post-license deterministic selection; scores cannot reactivate plans."""

    active = exact_active_set(outcomes)
    if not active:
        return Plan.FALLBACK
    missing = [plan for plan in active if plan not in scores]
    if missing:
        raise ValueError(f"active plans lack router scores: {missing!r}")
    best_score = max(scores[plan] for plan in active)
    tied = {plan for plan in active if scores[plan] == best_score}
    for plan in tie_order:
        if plan in tied:
            return plan
    raise ValueError("tie order does not cover every active plan")


def _threshold_for_stratum(
    stratum: AtomStratum,
    region: Interval,
    scale: float,
    rng: random.Random,
) -> float:
    if stratum is AtomStratum.STRICT_SUPPORTED:
        return region.upper + rng.uniform(0.25, 1.50) * scale
    if stratum is AtomStratum.BOUNDARY_SUPPORTED:
        return region.upper
    if stratum is AtomStratum.CROSSING_OPEN:
        return rng.uniform(
            region.lower + 0.10 * (region.upper - region.lower),
            region.upper - 0.10 * (region.upper - region.lower),
        )
    if stratum is AtomStratum.REFUTED:
        return region.lower - rng.uniform(0.25, 1.50) * scale
    return region.upper + 0.50 * scale


def _diagnostic(
    stratum: AtomStratum,
    value: AtomValue,
    mode: EvidenceMode,
) -> str:
    if stratum is AtomStratum.MISSING_OPEN:
        return "missing_evidence"
    if stratum is AtomStratum.INVALID_OPEN:
        return "invalid_evidence"
    if mode is EvidenceMode.EMPIRICAL_ONLY:
        return "proposal_has_no_evidential_polarity"
    if value is AtomValue.SUPPORTED:
        return "accepted_support_region"
    if value is AtomValue.REFUTED:
        return "accepted_counter_region"
    return "boundary_crossing_or_polarity_block"


def _cell_schedule(rng: random.Random) -> list[ContextCell]:
    cells = [cell for cell, count in CELL_DESIGN_COUNTS.items() for _ in range(count)]
    rng.shuffle(cells)
    return cells


def _stratum_schedule(rng: random.Random) -> list[AtomStratum]:
    strata = [
        stratum
        for stratum, count in STRATUM_DESIGN_COUNTS.items()
        for _ in range(count)
    ]
    rng.shuffle(strata)
    return strata


def _make_probe(
    identity: WorldIdentity,
    schema: Schema,
    index: int,
    stratum: AtomStratum,
    cell: ContextCell,
    rng: random.Random,
    loss_intercepts: Mapping[Plan, float],
    latency_intercepts: Mapping[Plan, float],
) -> AtomRecord:
    low, high = CELL_BOUNDS[cell]
    x = rng.uniform(low, high)
    complexity = rng.random()
    difficulty = rng.random()
    plan, stage = plan_for_cell(cell, index)
    scale = outcome_scale(schema, complexity, difficulty)
    oracle_mean = (
        loss_mean(plan, x, complexity, loss_intercepts)
        if schema is Schema.LOSS
        else latency_mean(plan, x, complexity, latency_intercepts)
    )
    target = oracle_mean + scale * _standard_normal(rng)
    region = Interval(oracle_mean - K_90 * scale, oracle_mean + K_90 * scale)
    mode = _mode_for_stratum(stratum, index)
    can_support, can_refute = MODE_POLARITY[mode]
    evidence_present = stratum is not AtomStratum.MISSING_OPEN
    evidence_valid = stratum is not AtomStratum.INVALID_OPEN
    threshold = _threshold_for_stratum(stratum, region, scale, rng)
    value = decode_evidence(
        region,
        threshold,
        evidence_present=evidence_present,
        evidence_valid=evidence_valid,
        can_support=can_support,
        can_refute=can_refute,
    )
    learning_target = None if stratum is AtomStratum.MISSING_OPEN else target
    return AtomRecord(
        atom_id=f"{identity.world_root}:{schema.value}:probe:{index}",
        world_root=identity.world_root,
        schema=schema,
        plan=plan,
        stage=stage,
        cell=cell,
        x=x,
        complexity=complexity,
        difficulty=difficulty,
        oracle_mean=oracle_mean,
        oracle_scale=scale,
        oracle_target=target,
        learning_target=learning_target,
        reference_region=region,
        threshold=threshold,
        stratum=stratum,
        mode=mode,
        evidence_present=evidence_present,
        evidence_valid=evidence_valid,
        can_support=can_support,
        can_refute=can_refute,
        value=value,
        diagnostic=_diagnostic(stratum, value, mode),
        target_weight=STRATUM_TARGET_MASS[stratum],
        design_weight=STRATUM_DESIGN_MASS[stratum],
    )


OUTCOME_DESIGN_COUNTS: Mapping[Outcome, int] = {
    Outcome.GRANTED: 12,
    Outcome.WITHHELD: 12,
    Outcome.REFUSED: 12,
    Outcome.UNDEFINED: 4,
}

OUTCOME_TARGET_MASS: Mapping[Outcome, float] = {
    Outcome.GRANTED: 0.35,
    Outcome.WITHHELD: 0.30,
    Outcome.REFUSED: 0.30,
    Outcome.UNDEFINED: 0.05,
}

OUTCOME_DESIGN_MASS: Mapping[Outcome, float] = {
    outcome: count / 40.0 for outcome, count in OUTCOME_DESIGN_COUNTS.items()
}


def _request_atom(
    name: str,
    schema: Schema,
    region: Interval,
    threshold: float,
    *,
    evidence_present: bool = True,
    evidence_valid: bool = True,
    mode: EvidenceMode = EvidenceMode.TWO_SIDED,
    diagnostic_override: str | None = None,
    boundary: bool = False,
) -> RequestAtom:
    can_support, can_refute = MODE_POLARITY[mode]
    value = decode_evidence(
        region,
        threshold,
        evidence_present=evidence_present,
        evidence_valid=evidence_valid,
        can_support=can_support,
        can_refute=can_refute,
    )
    diagnostic = diagnostic_override or (
        "accepted_support_region"
        if value is AtomValue.SUPPORTED
        else "accepted_counter_region"
        if value is AtomValue.REFUTED
        else "boundary_crossing_or_polarity_block"
    )
    return RequestAtom(
        name,
        schema,
        region,
        threshold,
        value,
        diagnostic,
        evidence_present,
        evidence_valid,
        can_support,
        can_refute,
        boundary,
    )


def _make_request(
    identity: WorldIdentity,
    index: int,
    outcome_local_index: int,
    desired: Outcome,
    cell: ContextCell,
    rng: random.Random,
    loss_intercepts: Mapping[Plan, float],
    latency_intercepts: Mapping[Plan, float],
    boundary_case: bool,
) -> RequestRecord:
    low, high = CELL_BOUNDS[cell]
    x = rng.uniform(low, high)
    complexity = rng.random()
    difficulty = rng.random()
    plan, stage = plan_for_cell(cell, index)
    mu_j = loss_mean(plan, x, complexity, loss_intercepts)
    mu_t = latency_mean(plan, x, complexity, latency_intercepts)
    sigma_j = outcome_scale(Schema.LOSS, complexity, difficulty)
    sigma_t = outcome_scale(Schema.LATENCY, complexity, difficulty)
    region_j = Interval(mu_j - K_90 * sigma_j, mu_j + K_90 * sigma_j)
    region_t = Interval(mu_t - K_90 * sigma_t, mu_t + K_90 * sigma_t)
    fallback_loss = loss_mean(Plan.FALLBACK, x, complexity, loss_intercepts)

    focal = ("A", "I", "C")[outcome_local_index % 3]
    support_j = region_j.upper + 0.50 * sigma_j
    support_t = region_t.upper + 0.50 * sigma_t
    eps_a = support_j
    eps_i = support_j
    eps_c = support_t
    evidence_j = (True, True, EvidenceMode.TWO_SIDED, None)
    evidence_t = (True, True, EvidenceMode.TWO_SIDED, None)

    if desired is Outcome.WITHHELD:
        open_kind = ("crossing", "polarity", "missing", "invalid")[(outcome_local_index // 3) % 4]
        if focal in {"A", "I"}:
            if open_kind == "crossing":
                threshold = (region_j.lower + region_j.upper) / 2.0
            elif open_kind == "polarity":
                threshold = region_j.lower - 0.50 * sigma_j
                evidence_j = (True, True, EvidenceMode.UPPER_ONLY, "polarity_blocked")
            elif open_kind == "missing":
                threshold = support_j
                evidence_j = (False, False, EvidenceMode.TWO_SIDED, "missing_evidence")
            else:
                threshold = support_j
                evidence_j = (True, False, EvidenceMode.TWO_SIDED, "invalid_evidence")
            if focal == "A":
                eps_a = threshold
            else:
                eps_i = threshold
        else:
            if open_kind == "crossing":
                eps_c = (region_t.lower + region_t.upper) / 2.0
            elif open_kind == "polarity":
                eps_c = region_t.lower - 0.50 * sigma_t
                evidence_t = (True, True, EvidenceMode.UPPER_ONLY, "polarity_blocked")
            elif open_kind == "missing":
                evidence_t = (False, False, EvidenceMode.TWO_SIDED, "missing_evidence")
            else:
                evidence_t = (True, False, EvidenceMode.TWO_SIDED, "invalid_evidence")
    elif desired is Outcome.REFUSED:
        if focal == "A":
            eps_a = region_j.lower - 0.50 * sigma_j
        elif focal == "I":
            eps_i = region_j.lower - 0.50 * sigma_j
        else:
            eps_c = region_t.lower - 0.50 * sigma_t

    # Exactly eight of the 36 well-formed requests carry a supported equality.
    boundary_name: str | None = None
    if boundary_case and desired is not Outcome.UNDEFINED:
        if focal in {"A", "I"} and desired is not Outcome.GRANTED:
            eps_c = region_t.upper
            boundary_name = "C"
        else:
            eps_a = region_j.upper
            boundary_name = "A"

    a = _request_atom(
        "A",
        Schema.LOSS,
        region_j,
        eps_a,
        evidence_present=evidence_j[0],
        evidence_valid=evidence_j[1],
        mode=evidence_j[2],
        diagnostic_override=evidence_j[3],
        boundary=boundary_name == "A",
    )
    i = _request_atom(
        "I",
        Schema.LOSS,
        region_j,
        eps_i,
        evidence_present=evidence_j[0],
        evidence_valid=evidence_j[1],
        mode=evidence_j[2],
        diagnostic_override=evidence_j[3],
        boundary=boundary_name == "I",
    )
    c_atom = _request_atom(
        "C",
        Schema.LATENCY,
        region_t,
        eps_c,
        evidence_present=evidence_t[0],
        evidence_valid=evidence_t[1],
        mode=evidence_t[2],
        diagnostic_override=evidence_t[3],
        boundary=boundary_name == "C",
    )
    well_formed = desired is not Outcome.UNDEFINED
    wf_reasons = ("wrong_units", "unbound_plan_domain", "malformed_profile")
    wf_diagnostic = (
        None
        if well_formed
        else wf_reasons[outcome_local_index % len(wf_reasons)]
    )
    atoms = (a, i, c_atom)
    outcome = derive_public_outcome(
        well_formed=well_formed,
        required_atom_values=(atom.value for atom in atoms),
    )
    if outcome is not desired:
        raise AssertionError(
            f"request constructor produced {outcome.value}, expected {desired.value}"
        )
    delta = fallback_loss - eps_i
    return RequestRecord(
        request_id=f"{identity.world_root}:request:{index}",
        world_root=identity.world_root,
        stage=stage,
        cell=cell,
        plan=plan,
        x=x,
        complexity=complexity,
        difficulty=difficulty,
        well_formed=well_formed,
        wf_diagnostic=wf_diagnostic,
        focal_atom=focal,
        atoms=atoms,
        outcome=outcome,
        boundary_case=boundary_name is not None,
        fallback_loss=fallback_loss,
        delta=delta,
        target_weight=OUTCOME_TARGET_MASS[outcome],
        design_weight=OUTCOME_DESIGN_MASS[outcome],
    )


def generate_world(
    role: Role,
    index: int,
    *,
    allow_final: bool = False,
) -> GeneratedWorld:
    if role is Role.FINAL_CONFIRMATION and not allow_final:
        raise FinalEmbargoError(
            "final-confirmation world materialization is embargoed until Task 21"
        )
    identity = world_identity(role, index)
    rng = random.Random(_seed_int(PROTOCOL_VERSION, ROLE_SEEDS[role], index))
    loss_intercepts = {
        plan: 0.006 * _standard_normal(rng)
        for plan in (Plan.OLD, Plan.SUCCESSOR, Plan.NEW)
    }
    latency_intercepts = {
        plan: 0.8 * _standard_normal(rng)
        for plan in (Plan.OLD, Plan.SUCCESSOR, Plan.NEW)
    }

    probes: list[AtomRecord] = []
    for schema in Schema:
        strata = _stratum_schedule(rng)
        cells = _cell_schedule(rng)
        probes.extend(
            _make_probe(
                identity,
                schema,
                probe_index,
                stratum,
                cell,
                rng,
                loss_intercepts,
                latency_intercepts,
            )
            for probe_index, (stratum, cell) in enumerate(zip(strata, cells))
        )

    request_schedule = [
        (outcome, local_index)
        for outcome, count in OUTCOME_DESIGN_COUNTS.items()
        for local_index in range(count)
    ]
    cells = _cell_schedule(rng)
    # Keep exact quotas while breaking the construction-order association.
    rng.shuffle(request_schedule)
    requests = tuple(
        _make_request(
            identity,
            request_index,
            outcome_local_index,
            desired,
            cell,
            rng,
            loss_intercepts,
            latency_intercepts,
            boundary_case=request_index < 8 and desired is not Outcome.UNDEFINED,
        )
        for request_index, ((desired, outcome_local_index), cell) in enumerate(
            zip(request_schedule, cells)
        )
    )
    # If an Undefined request occupied one of the first eight positions, promote
    # later meaningful requests until the exact boundary quota is reached.
    boundary_count = sum(request.boundary_case for request in requests)
    if boundary_count < 8:
        repaired: list[RequestRecord] = []
        needed = 8 - boundary_count
        for request_index, ((desired, outcome_local_index), cell) in enumerate(
            zip(request_schedule, cells)
        ):
            make_boundary = request_index < 8 and desired is not Outcome.UNDEFINED
            if not make_boundary and needed and desired is not Outcome.UNDEFINED:
                make_boundary = True
                needed -= 1
            repaired.append(
                _make_request(
                    identity,
                    request_index,
                    outcome_local_index,
                    desired,
                    cell,
                    random.Random(
                        _seed_int(identity.world_root, "request-repair", request_index)
                    ),
                    loss_intercepts,
                    latency_intercepts,
                    boundary_case=make_boundary,
                )
            )
        requests = tuple(repaired)
    if sum(request.boundary_case for request in requests) != 8:
        raise AssertionError("request boundary quota is not exactly eight")
    return GeneratedWorld(
        identity,
        loss_intercepts,
        latency_intercepts,
        tuple(probes),
        requests,
    )


@dataclass(frozen=True)
class FixtureSummary:
    stage0_outcomes: Mapping[Plan, Outcome]
    simultaneous_active: tuple[Plan, ...]
    gap_active: tuple[Plan, ...]
    gap_uses_fallback: bool
    lapse_outcome: Outcome
    lapse_value: AtomValue
    rebuttal_outcome: Outcome
    rebuttal_value: AtomValue
    irrelevant_before: tuple[AtomValue, ...]
    irrelevant_after: tuple[AtomValue, ...]
    tolerance_old: AtomValue
    tolerance_successor: AtomValue
    paired_dominance_certificates: Mapping[str, Interval]
    later_dominates: tuple[Plan, ...]


def _assess_fixture(
    loss_region: Interval,
    latency_region: Interval,
    *,
    epsilon_a: float = 0.20,
    loss_usable: bool = True,
) -> tuple[tuple[AtomValue, ...], Outcome]:
    values = (
        decode_upper_region(
            loss_region.lower,
            loss_region.upper,
            epsilon_a,
            evidence_usable=loss_usable,
        ),
        decode_upper_region(
            loss_region.lower,
            loss_region.upper,
            0.30,
            evidence_usable=loss_usable,
        ),
        decode_upper_region(
            latency_region.lower,
            latency_region.upper,
            50.0,
            evidence_usable=True,
        ),
    )
    return values, derive_public_outcome(well_formed=True, required_atom_values=values)


def succession_fixture() -> FixtureSummary:
    old_loss = Interval(0.14, 0.18)
    old_time = Interval(43.0, 47.0)
    successor_loss = Interval(0.11, 0.16)
    successor_time = Interval(45.0, 49.0)
    old_values, old_outcome = _assess_fixture(old_loss, old_time)
    _, successor_outcome = _assess_fixture(successor_loss, successor_time)
    loss_reads = frozenset({"certificate:O:J", "region:O:J", "current:O:J"})
    original = EvidenceSnapshot(old_loss, True, "stage0")
    irrelevant = apply_evidence_update(
        original,
        loss_reads,
        UpdateEvent("archive:N", frozenset({"archive:N"}), replacement_version="ignored"),
    )
    expired = apply_evidence_update(
        original,
        loss_reads,
        UpdateEvent(
            "expire:O:J",
            frozenset({"current:O:J"}),
            replacement_validity=False,
            replacement_version="stage1-expired",
        ),
    )
    rebutted = apply_evidence_update(
        original,
        loss_reads,
        UpdateEvent(
            "counter:O:J",
            frozenset({"certificate:O:J", "region:O:J"}),
            replacement_region=Interval(0.23, 0.25),
            replacement_validity=True,
            replacement_version="stage2-counter",
        ),
    )
    lapse_values, lapse_outcome = _assess_fixture(
        expired.region, old_time, loss_usable=expired.valid
    )
    rebuttal_values, rebuttal_outcome = _assess_fixture(
        rebutted.region, old_time, loss_usable=rebutted.valid
    )
    tolerance_old = _assess_fixture(old_loss, old_time, epsilon_a=0.16)[0][0]
    tolerance_successor = _assess_fixture(
        successor_loss, successor_time, epsilon_a=0.16
    )[0][0]

    # Paired differences can be strictly negative even when marginal intervals
    # overlap because the measurements may be correlated.  These registered
    # certificates, not the marginal table alone, establish finite dominance.
    paired = {
        "N_minus_O_loss": Interval(-0.10, -0.02),
        "N_minus_O_latency": Interval(-7.0, -0.5),
        "N_minus_S_loss": Interval(-0.08, -0.005),
        "N_minus_S_latency": Interval(-8.0, -0.5),
    }
    later_dominates = (
        Plan.OLD,
        Plan.SUCCESSOR,
    ) if all(interval.upper < 0 for interval in paired.values()) else ()
    return FixtureSummary(
        stage0_outcomes={Plan.OLD: old_outcome, Plan.SUCCESSOR: successor_outcome},
        simultaneous_active=(Plan.OLD, Plan.SUCCESSOR),
        gap_active=(),
        gap_uses_fallback=True,
        lapse_outcome=lapse_outcome,
        lapse_value=lapse_values[0],
        rebuttal_outcome=rebuttal_outcome,
        rebuttal_value=rebuttal_values[0],
        irrelevant_before=old_values,
        irrelevant_after=_assess_fixture(
            irrelevant.region, old_time, loss_usable=irrelevant.valid
        )[0],
        tolerance_old=tolerance_old,
        tolerance_successor=tolerance_successor,
        paired_dominance_certificates=paired,
        later_dominates=later_dominates,
    )


@dataclass(frozen=True)
class TaintedValue:
    value: Any
    source_fields: tuple[str, ...]
    transform: str = "identity"


SCORER_INPUT_WHITELIST = frozenset(
    {
        "atom_address",
        "dependency_projection",
        "plan_template",
        "plan_features",
        "x",
        "complexity",
        "difficulty",
        "scope",
        "stage_prefix",
        "statistic_schema",
        "units",
        "normalization_id",
        "evidence_mode",
        "can_support",
        "can_refute",
        "profile_slot",
        "profile_role",
        "epsilon_a",
        "delta",
        "fallback_threshold_inputs",
        "epsilon_c",
        "candidate_library_id",
        "evaluated_set_id",
        "evidence_design",
        "well_formed",
        "missingness",
        "validity",
        "expiry",
        "checker_status",
    }
)

FORBIDDEN_TOKENS = frozenset(
    {
        "target",
        "oracle",
        "latent",
        "noise",
        "reference_region",
        "reference_state",
        "label",
        "public_outcome",
        "grant_bit",
        "active_mask",
        "selected_route",
        "seam_label",
        "dominator_label",
        "future_event",
        "audit_result",
        "confirmation_result",
        "plan_family_root",
        "provenance_root",
    }
)


def _contains_forbidden_token(name: str) -> bool:
    normalized = name.lower().replace("-", "_")
    return any(token in normalized for token in FORBIDDEN_TOKENS)


def _audit_nested(value: Any, path: str) -> None:
    if isinstance(value, TaintedValue):
        if not value.source_fields:
            raise ValueError(f"taint record at {path} omits source fields")
        for source in value.source_fields:
            if _contains_forbidden_token(source) or source not in SCORER_INPUT_WHITELIST:
                raise ValueError(
                    f"scorer field {path} is derived via {value.transform} from forbidden {source}"
                )
        _audit_nested(value.value, path)
        return
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key)
            if _contains_forbidden_token(key_text):
                raise ValueError(f"nested forbidden scorer field {path}.{key_text}")
            _audit_nested(nested, f"{path}.{key_text}")
        return
    if isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _audit_nested(nested, f"{path}[{index}]")


def validate_scorer_payload(payload: Mapping[str, Any]) -> None:
    if not payload:
        raise ValueError("scorer payload must not be empty")
    for field_name, value in payload.items():
        if field_name not in SCORER_INPUT_WHITELIST:
            raise ValueError(f"scorer input field {field_name!r} is not whitelisted")
        if _contains_forbidden_token(field_name):
            raise ValueError(f"scorer input field {field_name!r} is forbidden")
        _audit_nested(value, field_name)


REQUIRED_BINDING_FIELDS = (
    "record_id",
    "atom_address",
    "statistic_schema",
    "target_constructor_version",
    "plan_template",
    "plan_family_scope",
    "candidate_registry_version",
    "units",
    "normalization_id",
    "scorer_architecture_id",
    "scorer_parameter_hash",
    "learned_head_factorization_id",
    "training_manifest_hash",
    "calibration_procedure_id",
    "calibration_manifest_hash",
    "calibration_group",
    "alpha_cal",
    "finite_quantile_rule",
    "eta_cal_or_infinity",
    "calibration_count",
    "certificate_mode",
    "can_support",
    "can_refute",
    "scope",
    "valid_from_stage",
    "valid_through_stage",
    "checker_id",
    "checker_version",
    "checker_result",
    "provenance_root",
    "created_stage",
)


@dataclass(frozen=True)
class Proposal:
    lower: float
    upper: float
    scorer_parameter_hash: str
    normalization_id: str
    statistic_schema: str
    plan_template: str
    scope: str


@dataclass(frozen=True)
class BindingDecision:
    accepted: bool
    reasons: tuple[str, ...]


def check_proposal_binding(
    record: Mapping[str, Any],
    proposal: Proposal,
    *,
    current_stage: int,
    expected: Mapping[str, Any] | None = None,
) -> BindingDecision:
    reasons: list[str] = []
    missing = [field for field in REQUIRED_BINDING_FIELDS if field not in record]
    if missing:
        reasons.append("missing_fields:" + ",".join(missing))
        return BindingDecision(False, tuple(reasons))
    for key, value in (expected or {}).items():
        if record.get(key) != value:
            reasons.append(f"expected_mismatch:{key}")
    for key in (
        "scorer_parameter_hash",
        "normalization_id",
        "statistic_schema",
        "plan_template",
        "scope",
    ):
        if record[key] != getattr(proposal, key):
            reasons.append(f"proposal_mismatch:{key}")
    if not isfinite(proposal.lower) or not isfinite(proposal.upper):
        reasons.append("nonfinite_endpoint")
    elif proposal.lower > proposal.upper:
        reasons.append("reversed_interval")
    eta = record["eta_cal_or_infinity"]
    if not isinstance(eta, (int, float)) or eta < 0:
        reasons.append("invalid_eta")
    elif not isfinite(float(eta)):
        reasons.append("unbounded_proposal")
    if record["alpha_cal"] != ALPHA_CAL:
        reasons.append("wrong_alpha_cal")
    if record["calibration_count"] < 200:
        reasons.append("undersized_calibration_group")
    mode = record["certificate_mode"]
    try:
        allowed = MODE_POLARITY[EvidenceMode(mode)]
    except (KeyError, ValueError):
        reasons.append("unknown_certificate_mode")
    else:
        if (bool(record["can_support"]), bool(record["can_refute"])) != allowed:
            reasons.append("invalid_polarity")
    if not record["valid_from_stage"] <= current_stage <= record["valid_through_stage"]:
        reasons.append("expired_or_not_yet_valid")
    if record["checker_result"] != "accepted":
        reasons.append("checker_rejected")
    for field in REQUIRED_BINDING_FIELDS:
        value = record[field]
        if value is None or value == "":
            reasons.append(f"empty_field:{field}")
    return BindingDecision(not reasons, tuple(reasons))


def reference_binding_record(**overrides: Any) -> dict[str, Any]:
    record: dict[str, Any] = {
        "record_id": "binding:reference",
        "atom_address": "atom:A",
        "statistic_schema": Schema.LOSS.value,
        "target_constructor_version": ORACLE_VERSION,
        "plan_template": Plan.OLD.value,
        "plan_family_scope": "registered-family-law-v1",
        "candidate_registry_version": "candidate-registry-v1",
        "units": "loss",
        "normalization_id": "normalization-v1",
        "scorer_architecture_id": "structured-reference-v1",
        "scorer_parameter_hash": "scorer-hash",
        "learned_head_factorization_id": "single-vector-head-v1",
        "training_manifest_hash": "train-manifest-hash",
        "calibration_procedure_id": "additive-residual-expansion-v1",
        "calibration_manifest_hash": "calibration-manifest-hash",
        "calibration_group": Schema.LOSS.value,
        "alpha_cal": ALPHA_CAL,
        "finite_quantile_rule": "ceil((n+1)*(1-alpha)); infinity-if-rank>n",
        "eta_cal_or_infinity": 0.01,
        "calibration_count": 200,
        "certificate_mode": EvidenceMode.TWO_SIDED.value,
        "can_support": True,
        "can_refute": True,
        "scope": "core-target-law",
        "valid_from_stage": 0,
        "valid_through_stage": 3,
        "checker_id": "envelope-checker-v1",
        "checker_version": "1.0.0",
        "checker_result": "accepted",
        "provenance_root": "provenance:binding",
        "created_stage": 0,
    }
    record.update(overrides)
    return record


@dataclass(frozen=True)
class ManifestSummary:
    role: Role
    count: int
    seed_label: str
    first_world_root: str
    last_world_root: str
    world_roots_digest: str
    trajectory_roots_digest: str
    provenance_roots_digest: str
    plan_family_roots_digest: str
    manifest_hash: str
    payloads_generated: bool
    embargoed: bool


def _sequence_digest(values: Iterable[str]) -> str:
    hasher = sha256()
    for value in values:
        hasher.update(value.encode("utf-8"))
        hasher.update(b"\n")
    return hasher.hexdigest()


def manifest_summary(
    role: Role,
    count: int,
    *,
    payloads_generated: bool = False,
) -> ManifestSummary:
    if count <= 0:
        raise ValueError("manifest count must be positive")
    identities = [world_identity(role, index) for index in range(count)]
    digests = {
        "world": _sequence_digest(identity.world_root for identity in identities),
        "trajectory": _sequence_digest(
            identity.trajectory_root for identity in identities
        ),
        "provenance": _sequence_digest(
            identity.provenance_root for identity in identities
        ),
        "family": _sequence_digest(
            identity.plan_family_root for identity in identities
        ),
    }
    manifest_hash = _digest(
        PROTOCOL_VERSION,
        role.value,
        count,
        ROLE_SEEDS[role],
        *(digests[key] for key in ("world", "trajectory", "provenance", "family")),
        payloads_generated,
    )
    return ManifestSummary(
        role,
        count,
        ROLE_SEEDS[role],
        identities[0].world_root,
        identities[-1].world_root,
        digests["world"],
        digests["trajectory"],
        digests["provenance"],
        digests["family"],
        manifest_hash,
        payloads_generated,
        role is Role.FINAL_CONFIRMATION,
    )


def audit_manifest_disjointness(manifests: Sequence[ManifestSummary]) -> None:
    if len({manifest.role for manifest in manifests}) != len(manifests):
        raise ValueError("duplicate role manifest")
    seen: dict[str, set[str]] = {
        "world": set(),
        "trajectory": set(),
        "provenance": set(),
        "family": set(),
    }
    for manifest in manifests:
        for index in range(manifest.count):
            identity = world_identity(manifest.role, index)
            values = {
                "world": identity.world_root,
                "trajectory": identity.trajectory_root,
                "provenance": identity.provenance_root,
                "family": identity.plan_family_root,
            }
            for kind, value in values.items():
                if value in seen[kind]:
                    raise ValueError(f"{kind} lineage overlaps across manifests")
                seen[kind].add(value)


@dataclass(frozen=True)
class PredictionRow:
    world_root: str
    reference: AtomValue
    predicted: AtomValue
    weight: float = 1.0


@dataclass(frozen=True)
class FidelityMetrics:
    accuracy: float
    false_support_rate: float | None
    false_refutation_rate: float | None
    weight_sum: float


def fidelity_metrics(rows: Iterable[PredictionRow]) -> FidelityMetrics:
    records = tuple(rows)
    if not records:
        raise ValueError("fidelity metric requires at least one row")
    if any(row.weight <= 0 or not isfinite(row.weight) for row in records):
        raise ValueError("metric weights must be finite and positive")
    total = sum(row.weight for row in records)
    accuracy = sum(
        row.weight for row in records if row.predicted is row.reference
    ) / total
    predicted_support = [
        row for row in records if row.predicted is AtomValue.SUPPORTED
    ]
    predicted_refute = [
        row for row in records if row.predicted is AtomValue.REFUTED
    ]
    false_support = (
        sum(
            row.weight
            for row in predicted_support
            if row.reference is not AtomValue.SUPPORTED
        )
        / sum(row.weight for row in predicted_support)
        if predicted_support
        else None
    )
    false_refute = (
        sum(
            row.weight
            for row in predicted_refute
            if row.reference is not AtomValue.REFUTED
        )
        / sum(row.weight for row in predicted_refute)
        if predicted_refute
        else None
    )
    return FidelityMetrics(accuracy, false_support, false_refute, total)


def marginal_coverage(
    targets_and_regions: Iterable[tuple[float, tuple[float, float]]]
) -> float:
    records = tuple(targets_and_regions)
    if not records:
        raise ValueError("coverage requires at least one eligible target")
    covered = 0
    for target, (lower, upper) in records:
        if lower > upper:
            raise ValueError("coverage interval is reversed")
        if lower <= target <= upper:
            covered += 1
    return covered / len(records)


def paired_sample_size(
    sd_upper: float,
    null_to_design_distance: float,
    *,
    alpha: float,
    inflation: float = 1.15,
) -> int:
    if sd_upper <= 0 or null_to_design_distance <= 0:
        raise ValueError("power inputs must be positive")
    z_alpha = {
        0.025: 1.959963984540054,
        0.05: 1.6448536269514722,
    }.get(alpha)
    if z_alpha is None:
        raise ValueError("only the frozen one-sided alpha values are supported")
    z_power = 1.2815515655446004
    return ceil(
        inflation
        * (z_alpha + z_power) ** 2
        * sd_upper**2
        / null_to_design_distance**2
    )


def bootstrap_sd_upper(
    values: Sequence[float],
    *,
    seed: int = BOOTSTRAP_SEED,
    replicates: int = 2000,
    quantile: float = 0.95,
) -> float:
    if len(values) < 2:
        raise ValueError("SD bootstrap requires at least two worlds")
    if replicates < 100:
        raise ValueError("SD bootstrap requires at least 100 replicates")
    if not 0 < quantile < 1:
        raise ValueError("bootstrap quantile must lie in (0,1)")
    rng = random.Random(seed)
    estimates: list[float] = []
    for _ in range(replicates):
        sample = [values[rng.randrange(len(values))] for _ in values]
        estimates.append(stdev(sample))
    estimates.sort()
    index = min(len(estimates) - 1, ceil(quantile * len(estimates)) - 1)
    return estimates[index]


def worst_case_paired_sd(
    structured_accuracy: float,
    ce_accuracy: float,
) -> float:
    """Largest Bernoulli-pair SD consistent with two design accuracies."""

    if not 0 <= structured_accuracy <= 1 or not 0 <= ce_accuracy <= 1:
        raise ValueError("design accuracies must be probabilities")
    mean_difference = structured_accuracy - ce_accuracy
    max_discordance = min(
        structured_accuracy + ce_accuracy,
        2.0 - structured_accuracy - ce_accuracy,
    )
    variance = max_discordance - mean_difference**2
    return sqrt(max(0.0, variance))


def round_world_count(value: int) -> int:
    return int(ceil(value / WORLD_BLOCK_SIZE) * WORLD_BLOCK_SIZE)


def f18_witness() -> Mapping[str, Any]:
    support_surplus = (2.0, 12.0, 3.0)
    grant = max(0.0, 1.0 + 1.0 + 1.0 + 1.0 - 3.0)
    boundary_surplus = max(0.0, (0.20 - 0.20) / 0.01)
    open_support = max(0.0, (0.20 - 0.22) / 0.01)
    open_refute = max(0.0, (0.18 - 0.20) / 0.01)
    bypass = 3.0 * max(0.0, -10.0) + 2.0 + 5.0
    raw_rank_with_missing_constraint = max(
        0.0, 0.5 * support_surplus[0] + 0.1 * support_surplus[1] - 1.0
    )
    return {
        "support_surplus": support_surplus,
        "grant": grant,
        "boundary_surplus": boundary_surplus,
        "open_pair": (open_support, open_refute),
        "bias_bypass": bypass,
        "raw_rank_with_missing_constraint": raw_rank_with_missing_constraint,
        "masked_rank_with_missing_constraint": 0.0,
    }


def mean_or_none(values: Sequence[float]) -> float | None:
    return mean(values) if values else None
