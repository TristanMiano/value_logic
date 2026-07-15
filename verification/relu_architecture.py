"""Semantic wrapper witnesses for the Task 16 hybrid ReLU architecture.

The learned scorer itself is intentionally absent.  These helpers make the
architecture's exact boundary executable: a neural statistic proposal is
attached to an externally certified envelope, decoded with inclusive boundary
rules, and admitted to downstream selection only through a symbolic license
mask.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from verification.kernel import (
    AtomValue,
    Diagnostic,
    Interval,
    assess_improvement,
    assess_upper_bound,
    open_atom,
)


def relu(value: float) -> float:
    return max(0.0, float(value))


def signed_relu(value: float) -> tuple[float, float]:
    """Positive and negative channels that reconstruct one signed scalar."""

    return relu(value), relu(-value)


@dataclass(frozen=True)
class StatisticProposal:
    """A learned region proposal before external calibration."""

    center: float
    predicted_half_width: float
    uncertainty_score: float

    def __post_init__(self) -> None:
        if self.predicted_half_width < 0:
            raise ValueError("predicted half-width must be nonnegative")


@dataclass(frozen=True)
class CertifiedEnvelope:
    """A proposal plus an error radius supplied by a named calibration path."""

    proposal: StatisticProposal
    certified_error_radius: float

    def __post_init__(self) -> None:
        if self.certified_error_radius < 0:
            raise ValueError("certified error radius must be nonnegative")

    @property
    def region(self) -> Interval:
        radius = self.proposal.predicted_half_width + self.certified_error_radius
        return Interval(self.proposal.center - radius, self.proposal.center + radius)


@dataclass(frozen=True)
class EvidenceGate:
    """Exact evidence state; the learned reject flag can only make it stricter."""

    certificate_id: str
    checker_id: str
    checker_version: str
    calibration_id: str
    calibration_version: str
    provenance: tuple[str, ...]
    present: bool = True
    current: bool = True
    conflict: bool = False
    checker_accepted: bool = True
    calibration_accepted: bool = True
    learned_reject: bool = False
    can_support: bool = True
    can_refute: bool = True

    def __post_init__(self) -> None:
        exact_fields = (
            self.certificate_id,
            self.checker_id,
            self.checker_version,
            self.calibration_id,
            self.calibration_version,
        )
        if not all(exact_fields) or not self.provenance:
            raise ValueError("evidence gates require exact identities and provenance")

    @property
    def witness(self) -> str:
        return (
            f"{self.certificate_id}|{self.checker_id}@{self.checker_version}"
            f"|{self.calibration_id}@{self.calibration_version}"
        )

    def obstacle(self) -> str | None:
        if not self.present:
            return "MissingStatisticEvidence"
        if not self.current:
            return "ExpiredStatisticEvidence"
        if self.conflict:
            return "EvidenceConflict"
        if not self.checker_accepted:
            return "EnvelopeCheckerRejected"
        if not self.calibration_accepted:
            return "UncalibratedStatistic"
        if self.learned_reject:
            return "LearnedValidityReject"
        return None


@dataclass(frozen=True)
class AtomChannels:
    """Audit-visible signed statistics plus a symbolically gated ReLU feature."""

    region: Interval | None
    support_margin: float | None
    refutation_margin: float | None
    positive_surplus: float
    support_deficit: float
    normalization_scale: float
    diagnostic: Diagnostic

    @property
    def supported_bit(self) -> bool:
        return self.diagnostic.value is AtomValue.SUPPORTED


def _polarity_checked(diagnostic: Diagnostic, gate: EvidenceGate) -> Diagnostic:
    if diagnostic.value is AtomValue.SUPPORTED and not gate.can_support:
        return open_atom(
            diagnostic.atom,
            "CertificateModeCannotSupport",
            gate.provenance,
            safety=diagnostic.safety,
        )
    if diagnostic.value is AtomValue.REFUTED and not gate.can_refute:
        return open_atom(
            diagnostic.atom,
            "CertificateModeCannotRefute",
            gate.provenance,
            safety=diagnostic.safety,
        )
    return diagnostic


def decode_upper_risk(
    atom: str,
    envelope: CertifiedEnvelope | None,
    threshold: float,
    gate: EvidenceGate,
    *,
    normalization_scale: float,
    safety: bool = False,
) -> AtomChannels:
    """Decode a smaller-is-better region with inclusive support at equality."""

    if normalization_scale <= 0:
        raise ValueError("normalization scale must be positive")
    region = envelope.region if envelope is not None else None
    support_margin = None if region is None else threshold - region.upper
    refutation_margin = None if region is None else region.lower - threshold
    deficit = 0.0 if support_margin is None else relu(-support_margin / normalization_scale)

    obstacle = gate.obstacle()
    if envelope is None:
        obstacle = obstacle or "MissingCertifiedEnvelope"
    if obstacle is not None:
        diagnostic = open_atom(atom, obstacle, gate.provenance, safety=safety)
        return AtomChannels(
            region,
            support_margin,
            refutation_margin,
            0.0,
            deficit,
            normalization_scale,
            diagnostic,
        )

    diagnostic = assess_upper_bound(
        atom,
        region,
        threshold,
        gate.witness,
        gate.provenance,
        safety=safety,
    )
    diagnostic = _polarity_checked(diagnostic, gate)
    surplus = (
        relu(support_margin / normalization_scale)
        if diagnostic.value is AtomValue.SUPPORTED and support_margin is not None
        else 0.0
    )
    return AtomChannels(
        region,
        support_margin,
        refutation_margin,
        surplus,
        deficit,
        normalization_scale,
        diagnostic,
    )


def decode_improvement_margin(
    atom: str,
    candidate: CertifiedEnvelope | None,
    fallback: CertifiedEnvelope | None,
    required_advantage: float,
    candidate_gate: EvidenceGate,
    fallback_gate: EvidenceGate,
    *,
    normalization_scale: float,
) -> AtomChannels:
    """Decode a candidate-versus-fallback improvement atom."""

    if normalization_scale <= 0:
        raise ValueError("normalization scale must be positive")
    candidate_region = candidate.region if candidate is not None else None
    fallback_region = fallback.region if fallback is not None else None
    support_margin = (
        None
        if candidate_region is None or fallback_region is None
        else fallback_region.lower - (candidate_region.upper + required_advantage)
    )
    refutation_margin = (
        None
        if candidate_region is None or fallback_region is None
        else (candidate_region.lower + required_advantage) - fallback_region.upper
    )
    deficit = 0.0 if support_margin is None else relu(-support_margin / normalization_scale)

    obstacle = candidate_gate.obstacle()
    if obstacle is not None:
        obstacle = f"Candidate:{obstacle}"
    if obstacle is None:
        obstacle = fallback_gate.obstacle()
        if obstacle is not None:
            obstacle = f"Fallback:{obstacle}"
    if candidate is None:
        obstacle = obstacle or "MissingCandidateEnvelope"
    if fallback is None:
        obstacle = obstacle or "MissingFallbackEnvelope"
    provenance = tuple(dict.fromkeys(candidate_gate.provenance + fallback_gate.provenance))
    if obstacle is not None:
        diagnostic = open_atom(atom, obstacle, provenance)
        return AtomChannels(
            None,
            support_margin,
            refutation_margin,
            0.0,
            deficit,
            normalization_scale,
            diagnostic,
        )

    diagnostic = assess_improvement(
        atom,
        candidate_region,
        fallback_region,
        required_advantage,
        f"candidate:{candidate_gate.witness}|fallback:{fallback_gate.witness}",
        provenance,
    )
    if diagnostic.value is AtomValue.SUPPORTED and not (
        candidate_gate.can_support and fallback_gate.can_support
    ):
        diagnostic = open_atom(atom, "CertificateModeCannotSupport", provenance)
    if diagnostic.value is AtomValue.REFUTED and not (
        candidate_gate.can_refute and fallback_gate.can_refute
    ):
        diagnostic = open_atom(atom, "CertificateModeCannotRefute", provenance)
    surplus = (
        relu(support_margin / normalization_scale)
        if diagnostic.value is AtomValue.SUPPORTED and support_margin is not None
        else 0.0
    )
    return AtomChannels(
        None,
        support_margin,
        refutation_margin,
        surplus,
        deficit,
        normalization_scale,
        diagnostic,
    )


@dataclass(frozen=True)
class HypothesisChannelSpec:
    hypothesis: str
    atom_address: str
    domain: str
    normalization_id: str
    normalization_scale: float
    calibration_ref: str
    consumer_context: str
    downstream_consumers: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.normalization_scale <= 0:
            raise ValueError("hypothesis normalization scale must be positive")
        exact = (
            self.hypothesis,
            self.atom_address,
            self.domain,
            self.normalization_id,
            self.calibration_ref,
            self.consumer_context,
        )
        if not all(exact) or not self.downstream_consumers:
            raise ValueError("hypothesis channels require exact semantics and consumers")


def validate_hypothesis_registry(specs: Sequence[HypothesisChannelSpec]) -> None:
    """Require one declared comparable normalization and consumer context."""

    if not specs:
        raise ValueError("hypothesis registry cannot be empty")
    if len({spec.hypothesis for spec in specs}) != len(specs):
        raise ValueError("hypothesis identifiers must be unique")
    if len({spec.normalization_id for spec in specs}) != 1:
        raise ValueError("dual-use channels do not share a normalization semantics")
    if len({spec.consumer_context for spec in specs}) != 1:
        raise ValueError("dual-use channels do not share a consumer context")


@dataclass(frozen=True)
class DualUseFeature:
    hypothesis: str
    positive_surplus: float
    supported_bit: bool
    atom_value: AtomValue


def dual_use_feature(
    spec: HypothesisChannelSpec,
    channels: AtomChannels,
) -> DualUseFeature:
    """Expose positive surplus only when the external decoder supports the atom."""

    if abs(spec.normalization_scale - channels.normalization_scale) > 1e-12:
        raise ValueError("channel and registry normalization scales disagree")
    return DualUseFeature(
        spec.hypothesis,
        channels.positive_surplus if channels.supported_bit else 0.0,
        channels.supported_bit,
        channels.diagnostic.value,
    )


@dataclass(frozen=True)
class CandidateRoute:
    candidate_id: str
    active: bool
    selection_score: float
    payload: Any


@dataclass(frozen=True)
class SelectionResult:
    selected_id: str
    payload: Any
    used_fallback: bool


def select_from_active(
    candidates: Iterable[CandidateRoute],
    *,
    fallback_id: str,
    fallback_payload: Any,
    tie_priority: Mapping[str, int] | None = None,
) -> SelectionResult:
    """Select only from the symbolic active set, or return the exact fallback."""

    candidates = tuple(candidates)
    if len({candidate.candidate_id for candidate in candidates}) != len(candidates):
        raise ValueError("candidate route identities must be unique")
    active = tuple(candidate for candidate in candidates if candidate.active)
    if not active:
        return SelectionResult(fallback_id, fallback_payload, True)
    best_score = max(candidate.selection_score for candidate in active)
    tied = tuple(candidate for candidate in active if candidate.selection_score == best_score)
    if len(tied) == 1:
        selected = tied[0]
    else:
        if tie_priority is None or any(candidate.candidate_id not in tie_priority for candidate in tied):
            raise ValueError("selection ties require an explicit complete priority rule")
        selected = min(tied, key=lambda candidate: tie_priority[candidate.candidate_id])
    return SelectionResult(selected.candidate_id, selected.payload, False)


def naive_relu_path(
    margin: float,
    *,
    outgoing_weight: float,
    downstream_bias: float,
    bypass: float = 0.0,
) -> float:
    """Counterexample helper: a zeroed unit does not silence other paths/biases."""

    return outgoing_weight * relu(margin) + downstream_bias + bypass
