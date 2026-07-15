"""Deterministic certificate/system integration witness for Task 20.

This is intentionally not a powered empirical arm.  It demonstrates the
typed boundary from a learned grade *proposal* to independently checked local
evidence, finite composite-certificate construction, grounded provenance, and
strictly lower-ranked audit records.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Mapping

from verification.proof_plans import (
    EvidenceRecord,
    EvaluationNode,
    PlanContractError,
    PlanDAG,
    PlanNode,
    ResourceBound,
    SupportNode,
    evaluate_stratified,
    execute_annotated,
    execute_plain,
    grounded_sources,
    verify_proof_term,
)


@dataclass(frozen=True)
class LearnedGradeEnvelope:
    """A fitted system's bounded grade proposal, not a certificate."""

    scorer_parameter_hash: str
    calibration_id: str
    metric: str
    proposed_error_bound: float
    payload: float

    def __post_init__(self) -> None:
        if not self.scorer_parameter_hash or not self.calibration_id or not self.metric:
            raise ValueError("learned envelopes require exact scorer/calibration identity")
        if self.proposed_error_bound < 0:
            raise ValueError("learned grade bounds must be nonnegative")


@dataclass(frozen=True)
class AuditRecord:
    """Externally checked, lower-ranked evidence about a frozen envelope."""

    record_id: str
    role: str
    rank: int
    world_root: str
    provenance_root: str
    scorer_parameter_hash: str
    calibration_id: str
    checker: str
    accepted: bool
    checked_error_bound: float

    def __post_init__(self) -> None:
        exact = (
            self.record_id,
            self.role,
            self.world_root,
            self.provenance_root,
            self.scorer_parameter_hash,
            self.calibration_id,
            self.checker,
        )
        if not all(exact) or self.rank < 0 or self.checked_error_bound < 0:
            raise ValueError("audit record is incomplete or invalid")


@dataclass(frozen=True)
class CheckedGrade:
    envelope: LearnedGradeEnvelope
    audit: AuditRecord
    certificate_id: str


def checked_grade_adapter(
    envelope: LearnedGradeEnvelope,
    audit: AuditRecord,
) -> CheckedGrade:
    """Bind an envelope to independent evidence without treating it as proof."""

    if audit.role != "system_audit" or audit.rank != 0:
        raise PlanContractError("grade evidence must come from the lower-ranked system-audit role")
    if not audit.accepted:
        raise PlanContractError("the external grade checker rejected the proposal")
    if audit.scorer_parameter_hash != envelope.scorer_parameter_hash:
        raise PlanContractError("audit/scorer binding mismatch")
    if audit.calibration_id != envelope.calibration_id:
        raise PlanContractError("audit/calibration binding mismatch")
    if audit.checked_error_bound < envelope.proposed_error_bound:
        raise PlanContractError("audit record understates the learned proposal")
    return CheckedGrade(envelope, audit, f"checked:{audit.record_id}")


def _resource(dimension: str, unit: str, amount: float) -> ResourceBound:
    return ResourceBound(dimension, unit, amount)


def _plan(checked: CheckedGrade) -> tuple[PlanDAG, Mapping[str, EvidenceRecord]]:
    primitive_error = checked.audit.checked_error_bound
    nodes = (
        PlanNode(
            name="learned-predictor",
            predecessors=(),
            input_types=(),
            input_frames=(),
            input_metrics=(),
            output_type="scalar",
            output_frame="model",
            output_metric=checked.envelope.metric,
            transform=lambda external, _: checked.envelope.payload * float(external),
            sensitivities=(),
            local_error_bound=primitive_error,
            local_resources=(
                _resource("latency", "ms", 2.0),
                _resource("energy", "J", 0.4),
            ),
            resource_operators=(("latency", "ms", "sum"), ("energy", "J", "sum")),
            certificate_id=checked.certificate_id,
        ),
        PlanNode(
            name="checked-postprocess",
            predecessors=("learned-predictor",),
            input_types=("scalar",),
            input_frames=("model",),
            input_metrics=(checked.envelope.metric,),
            output_type="scalar",
            output_frame="world",
            output_metric=checked.envelope.metric,
            transform=lambda _, inputs: float(inputs[0]) + 1.0,
            sensitivities=(1.5,),
            local_error_bound=0.01,
            local_resources=(
                _resource("latency", "ms", 0.5),
                _resource("energy", "J", 0.1),
            ),
            resource_operators=(("latency", "ms", "sum"), ("energy", "J", "sum")),
            certificate_id="checked:postprocess",
        ),
    )
    registry = {
        checked.certificate_id: EvidenceRecord(
            certificate_id=checked.certificate_id,
            node="learned-predictor",
            checker=checked.audit.checker,
            accepted=True,
            metric=checked.envelope.metric,
            local_error_bound=primitive_error,
            local_resources=nodes[0].local_resources,
            sources=(f"empirical:{checked.audit.provenance_root}",),
        ),
        "checked:postprocess": EvidenceRecord(
            certificate_id="checked:postprocess",
            node="checked-postprocess",
            checker="formal-transformer:v1",
            accepted=True,
            metric=checked.envelope.metric,
            local_error_bound=0.01,
            local_resources=nodes[1].local_resources,
            sources=("formal:composite-rule-v1",),
        ),
    }
    return PlanDAG(nodes, "checked-postprocess"), registry


def deterministic_system_witness() -> Mapping[str, object]:
    envelope = LearnedGradeEnvelope(
        "scorer:fixed-hash",
        "calibration:fixed-hash",
        "absolute-error",
        0.08,
        2.0,
    )
    audit = AuditRecord(
        "audit:grade-1",
        "system_audit",
        0,
        "world:audit-root",
        "provenance:audit-root",
        envelope.scorer_parameter_hash,
        envelope.calibration_id,
        "external-grade-checker:v1",
        True,
        0.10,
    )
    confirmation = AuditRecord(
        "confirmation:run-1",
        "final_confirmation",
        2,
        "world:confirmation-root",
        "provenance:confirmation-root",
        envelope.scorer_parameter_hash,
        envelope.calibration_id,
        "confirmation-assessor:v1",
        True,
        0.12,
    )
    if audit.world_root == confirmation.world_root or audit.provenance_root == confirmation.provenance_root:
        raise AssertionError("audit and confirmation evidence are not lineage-disjoint")

    learned_alone_rejected = False
    try:
        checked_grade_adapter(envelope, replace(audit, accepted=False))
    except PlanContractError:
        learned_alone_rejected = True
    checked = checked_grade_adapter(envelope, audit)
    plan, registry = _plan(checked)
    annotated = execute_annotated(plan, 3.0, registry)
    plain = execute_plain(plan, 3.0)
    proof_valid = verify_proof_term(plan, annotated.certificate, registry)

    invalid_local_rejected = False
    invalid_registry = dict(registry)
    invalid_registry["checked:postprocess"] = replace(
        invalid_registry["checked:postprocess"], accepted=False
    )
    try:
        execute_annotated(plan, 3.0, invalid_registry)
    except PlanContractError:
        invalid_local_rejected = True

    cycle_rejected = False
    cycle_nodes = list(plan.nodes)
    cycle_nodes[0] = replace(
        cycle_nodes[0],
        predecessors=("checked-postprocess",),
        input_types=("scalar",),
        input_frames=("world",),
        input_metrics=(envelope.metric,),
        sensitivities=(1.0,),
    )
    try:
        execute_plain(PlanDAG(tuple(cycle_nodes), plan.root), 3.0)
    except PlanContractError:
        cycle_rejected = True

    support_graph = (
        SupportNode("audit-data", base_kind="empirical"),
        SupportNode("composite-checker", base_kind="formal"),
        SupportNode("learned-grade", ("audit-data",)),
        SupportNode("system-license", ("learned-grade", "composite-checker")),
    )
    sources = grounded_sources(support_graph, "system-license")
    ranked = evaluate_stratified(
        (
            EvaluationNode("audit-evidence", 0, ("audit-record",), lambda xs: xs[0].accepted),
            EvaluationNode("checked-grade", 1, ("audit-evidence",), lambda xs: bool(xs[0])),
            EvaluationNode("confirmation-status", 2, ("checked-grade",), lambda xs: "assess" if xs[0] else "open"),
        ),
        {"audit-record": audit},
    )
    return {
        "evidence_grade": "deterministic_integration_witness_only",
        "learned_envelope_is_certificate": False,
        "learned_alone_rejected": learned_alone_rejected,
        "proof_erasure": annotated.payload == plain,
        "payload": annotated.payload,
        "grade_error_bound": annotated.grade.error_bound,
        "proof_valid": proof_valid,
        "invalid_local_certificate_rejected": invalid_local_rejected,
        "cycle_rejected": cycle_rejected,
        "grounded_sources": sources,
        "audit_confirmation_lineage_disjoint": True,
        "ranks": {"system_audit": audit.rank, "checked_adapter": 1, "final_confirmation": confirmation.rank},
        "stratified_status": ranked["confirmation-status"],
        "powered_empirical_claim": False,
    }
