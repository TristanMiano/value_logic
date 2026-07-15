"""Focused regressions for the frozen Task 20 implementation."""

from __future__ import annotations

from dataclasses import replace
import inspect
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from experiments import learner
from experiments.implementation import (
    FEATURE_NAMES,
    NORMALIZATION_ID,
    CalibrationBundle,
    CalibrationGroup,
    calibrate_structured,
    decode_cross_entropy,
    decode_request,
    decode_structured,
    encode_probe,
    f18_implementation_witness,
    frozen_prediction_trace,
    implementation_preflight,
    join_evaluation_namespace,
    prediction_hash,
    probe_payload,
    request_atom_payload,
    route_with_exact_mask,
    self_confidence_ablation,
    tolerance_transfer_cases,
    world_panel,
    write_trace_jsonl,
)
from experiments.protocol import (
    AtomStratum,
    Plan,
    Role,
    Schema,
    generate_world,
    validate_scorer_payload,
)
from experiments.system_witness import (
    AuditRecord,
    LearnedGradeEnvelope,
    checked_grade_adapter,
    deterministic_system_witness,
)
from experiments.run_experiment import run_preflight, run_task21_final
from verification.kernel import AtomValue, Outcome
from verification.proof_plans import PlanContractError


ROOT = Path(__file__).resolve().parents[1]


def calibration(eta_j: float = 0.0, eta_t: float = 0.0, variant: str = "structured") -> CalibrationBundle:
    return CalibrationBundle(
        "scorer-hash",
        variant,
        "train-manifest",
        "cal-manifest",
        {
            Schema.LOSS: CalibrationGroup(Schema.LOSS, eta_j, 5000, 10000, 9000),
            Schema.LATENCY: CalibrationGroup(Schema.LATENCY, eta_t, 5000, 10000, 9000),
        },
        f"calibration:{variant}",
    )


class FeatureAndArchitectureTests(unittest.TestCase):
    def test_learner_module_has_no_generator_or_oracle_import(self) -> None:
        source = inspect.getsource(learner)
        self.assertNotIn("experiments.protocol", source)
        self.assertNotIn("oracle_", source)

    def test_feature_payload_is_closed_audited_and_25_dimensional(self) -> None:
        world = generate_world(Role.PILOT, 0)
        probe = world.probes[0]
        payload = probe_payload(probe)
        validate_scorer_payload(payload)
        vector = encode_probe(probe)
        self.assertEqual(vector.shape, (25,))
        self.assertEqual(len(FEATURE_NAMES), 25)
        self.assertNotIn("threshold", payload)
        self.assertFalse(any("oracle" in name for name in payload))

    def test_matched_capacity_rule_is_within_two_percent(self) -> None:
        for budget in (12000, 20000):
            structured, ce = learner.matched_architectures(len(FEATURE_NAMES), budget)
            mismatch = abs(structured.parameter_count - ce.parameter_count) / max(
                structured.parameter_count, ce.parameter_count
            )
            self.assertLessEqual(mismatch, 0.02)
            self.assertGreaterEqual(structured.parameter_count, budget)
            self.assertGreaterEqual(ce.parameter_count, budget)

    def test_paired_initialization_shares_trunk_prefix_and_isolates_heads(self) -> None:
        structured_spec, ce_spec = learner.matched_architectures(len(FEATURE_NAMES), 20000)
        structured = learner.ReluMLP(
            structured_spec.input_dim,
            structured_spec.hidden_width,
            structured_spec.output_dim,
        )
        ce = learner.ReluMLP(ce_spec.input_dim, ce_spec.hidden_width, ce_spec.output_dim)
        learner.initialize_paired(structured, structured_spec, 101)
        learner.initialize_paired(ce, ce_spec, 101)
        width = structured_spec.hidden_width
        self.assertTrue(
            np.array_equal(
                structured.trunk[0].weight.detach().numpy(),
                ce.trunk[0].weight[:width].detach().numpy(),
            )
        )
        self.assertTrue(
            np.array_equal(
                structured.trunk[2].weight.detach().numpy(),
                ce.trunk[2].weight[:width, :width].detach().numpy(),
            )
        )
        self.assertFalse(
            np.array_equal(
                structured.vector_head.weight[:3].detach().numpy(),
                ce.vector_head.weight[:, :width].detach().numpy(),
            )
        )

    def test_joint_selection_keeps_one_shared_budget(self) -> None:
        configs = (
            learner.FitConfig(0.001, 0.0, 12000),
            learner.FitConfig(0.001, 0.0, 20000),
        )
        trials = (
            learner.TrialScore("structured", configs[0], 1.01),
            learner.TrialScore("structured", configs[1], 1.00),
            learner.TrialScore("cross_entropy", configs[0], 0.50),
            learner.TrialScore("cross_entropy", configs[1], 0.51),
        )
        selected = learner.choose_joint_capacity(trials)
        self.assertIn(selected.parameter_budget, (12000, 20000))
        self.assertEqual(selected.structured.config.parameter_budget, selected.parameter_budget)
        self.assertEqual(selected.cross_entropy.config.parameter_budget, selected.parameter_budget)

    def test_world_panel_masks_missing_regression_targets_without_hiding_K3(self) -> None:
        panel = world_panel(generate_world(Role.PILOT, 1))
        self.assertEqual(panel.features.shape, (1, 80, 25))
        self.assertEqual(np.isnan(panel.statistic_targets).sum(), 8)
        self.assertTrue(np.isin(panel.state_targets, (0, 1, 2)).all())

    def test_calibration_uses_one_independent_score_per_schema_world(self) -> None:
        panels = [world_panel(generate_world(Role.PILOT, index)) for index in range(4)]
        data = learner.WorldPanelData(
            np.concatenate([panel.features for panel in panels]),
            np.concatenate([panel.statistic_targets for panel in panels]),
            np.concatenate([panel.schemas for panel in panels]),
            np.concatenate([panel.state_targets for panel in panels]),
            np.concatenate([panel.weights for panel in panels]),
        )
        spec, _ = learner.matched_architectures(len(FEATURE_NAMES), 12000)
        model = learner.ReluMLP(spec.input_dim, spec.hidden_width, spec.output_dim)
        learner.initialize_paired(model, spec, 101)
        bundle = calibrate_structured(
            model,
            data,
            scorer_parameter_hash="hash",
            training_manifest_hash="train",
            calibration_manifest_hash="calibration",
        )
        self.assertEqual(bundle.groups[Schema.LOSS].score_count, 4)
        self.assertEqual(bundle.groups[Schema.LATENCY].score_count, 4)
        self.assertEqual(bundle.groups[Schema.LOSS].calibration_worlds, 4)


class ExactSemanticBoundaryTests(unittest.TestCase):
    def test_boundary_zero_and_crossing_zero_have_distinct_exact_states(self) -> None:
        boundary = decode_structured(
            atom_address="atom:A",
            schema=Schema.LOSS,
            plan=Plan.OLD,
            stage=0,
            threshold=0.20,
            evidence_present=True,
            evidence_valid=True,
            can_support=True,
            can_refute=True,
            raw=(1.9, 0.1, 0.0, 0.0),
            scorer_parameter_hash="scorer-hash",
            calibration=calibration(),
        )
        crossing = decode_structured(
            atom_address="atom:A",
            schema=Schema.LOSS,
            plan=Plan.OLD,
            stage=0,
            threshold=0.20,
            evidence_present=True,
            evidence_valid=True,
            can_support=True,
            can_refute=True,
            raw=(2.0, 0.2, 0.0, 0.0),
            scorer_parameter_hash="scorer-hash",
            calibration=calibration(),
        )
        self.assertIs(boundary.value, AtomValue.SUPPORTED)
        self.assertEqual(boundary.support_relu, 0.0)
        self.assertIs(crossing.value, AtomValue.OPEN)
        self.assertEqual((crossing.support_relu, crossing.refutation_relu), (0.0, 0.0))

    def test_missing_invalid_and_unaccepted_proposals_are_open(self) -> None:
        common = dict(
            atom_address="atom:A",
            schema=Schema.LOSS,
            plan=Plan.OLD,
            stage=0,
            threshold=0.30,
            can_support=True,
            can_refute=True,
            raw=(1.0, 0.1, 0.0, 0.0),
            scorer_parameter_hash="scorer-hash",
            calibration=calibration(),
        )
        self.assertIs(
            decode_structured(**common, evidence_present=False, evidence_valid=True).value,
            AtomValue.OPEN,
        )
        self.assertIs(
            decode_structured(**common, evidence_present=True, evidence_valid=False).value,
            AtomValue.OPEN,
        )
        shadow = decode_structured(
            **common,
            evidence_present=True,
            evidence_valid=True,
            variant="unaccepted_radius",
        )
        self.assertIs(shadow.value, AtomValue.OPEN)
        self.assertIs(shadow.shadow_value, AtomValue.SUPPORTED)
        self.assertFalse(shadow.production_active)

    def test_ce_logits_cannot_override_exact_usability_or_polarity(self) -> None:
        support_logits = (-5.0, -2.0, 5.0)
        missing = decode_cross_entropy(
            atom_address="atom:A",
            logits=support_logits,
            evidence_present=False,
            evidence_valid=True,
            can_support=True,
            can_refute=True,
        )
        blocked = decode_cross_entropy(
            atom_address="atom:A",
            logits=support_logits,
            evidence_present=True,
            evidence_valid=True,
            can_support=False,
            can_refute=True,
        )
        self.assertIs(missing.value, AtomValue.OPEN)
        self.assertIs(blocked.value, AtomValue.OPEN)

    def test_self_confidence_is_never_a_production_active_mask(self) -> None:
        invalid = self_confidence_ablation("atom:A", (-10.0, -10.0, 10.0))
        self.assertIs(invalid.value, AtomValue.SUPPORTED)
        self.assertFalse(invalid.production_active)
        self.assertFalse(invalid.binding_accepted)

    def test_symbolic_WF_K3_diagnostics_and_public_outcome(self) -> None:
        world = generate_world(Role.PILOT, 2)
        request = next(record for record in world.requests if record.outcome is Outcome.GRANTED)
        decisions = [
            decode_cross_entropy(
                atom_address=f"{request.request_id}:{atom.name}",
                logits=(-5.0, -2.0, 5.0),
                evidence_present=atom.evidence_present,
                evidence_valid=atom.evidence_valid,
                can_support=atom.can_support,
                can_refute=atom.can_refute,
            )
            for atom in request.atoms
        ]
        result = decode_request(request, decisions)
        self.assertEqual(set(result.atoms), {"A", "I", "C"})
        self.assertIs(result.outcome, Outcome.GRANTED)
        self.assertEqual(result.active_mask, 1)

    def test_exact_mask_handles_simultaneous_and_empty_sets(self) -> None:
        simultaneous = route_with_exact_mask(
            {Plan.OLD: Outcome.GRANTED, Plan.SUCCESSOR: Outcome.GRANTED},
            {Plan.OLD: 1.0, Plan.SUCCESSOR: 2.0, Plan.NEW: 1e9},
        )
        self.assertEqual(simultaneous.active, (Plan.OLD, Plan.SUCCESSOR))
        self.assertIs(simultaneous.selected, Plan.SUCCESSOR)
        self.assertEqual(simultaneous.inactive_selection_probability, 0.0)
        empty = route_with_exact_mask(
            {Plan.OLD: Outcome.WITHHELD, Plan.SUCCESSOR: Outcome.REFUSED},
            {Plan.OLD: 1e9, Plan.SUCCESSOR: 2e9},
        )
        self.assertIs(empty.selected, Plan.FALLBACK)

    def test_f18_prevents_positive_as_grant_and_zero_as_quarantine(self) -> None:
        witness = f18_implementation_witness()
        self.assertEqual(witness["grant"], 1.0)
        self.assertEqual(witness["boundary_surplus"], 0.0)
        self.assertEqual(witness["open_pair"], (0.0, 0.0))
        self.assertEqual(witness["bias_bypass"], 7.0)
        self.assertEqual(witness["selected_with_inactive_high_score"], "O")
        self.assertEqual(witness["empty_selected"], "F")


class TransferTraceAndSystemTests(unittest.TestCase):
    def test_transfer_changes_declared_threshold_without_exposing_reference(self) -> None:
        probe = generate_world(Role.PILOT, 3).probes[0]
        cases = tolerance_transfer_cases(probe)
        self.assertEqual(tuple(case.offset for case in cases), (-2.0, -1.5, 1.5, 2.0))
        self.assertTrue(all(case.feature.shape == (25,) for case in cases))
        self.assertTrue(all("oracle" not in case.atom_address for case in cases))

    def test_prediction_is_hashed_before_evaluation_namespace_join(self) -> None:
        world = generate_world(Role.PILOT, 4)
        probe = world.probes[0]
        decision = decode_cross_entropy(
            atom_address=probe.atom_id,
            logits=(1.0, 2.0, 3.0),
            evidence_present=probe.evidence_present,
            evidence_valid=probe.evidence_valid,
            can_support=probe.can_support,
            can_refute=probe.can_refute,
        )
        trace = frozen_prediction_trace(
            world=world,
            atom_address=probe.atom_id,
            role=Role.PILOT,
            allowed_payload=probe_payload(probe),
            arm="cross_entropy",
            fit_seed=101,
            parameter_hash="hash",
            raw_output=(1.0, 2.0, 3.0),
            decision=decision,
            manifest_hashes={"pilot": "manifest"},
            request_context={"threshold": probe.threshold, "stage": probe.stage},
        )
        frozen_hash = prediction_hash(trace)
        joined = join_evaluation_namespace(
            trace,
            reference=probe.value,
            target_weight=probe.target_weight,
            design_weight=probe.design_weight,
            stratum=probe.stratum.value,
        )
        self.assertFalse(trace["access_control_separated_oracle_namespace"]["joined"])
        self.assertTrue(joined["access_control_separated_oracle_namespace"]["joined"])
        self.assertEqual(joined["access_control_separated_oracle_namespace"]["prediction_hash"], frozen_hash)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.jsonl"
            digest = write_trace_jsonl(path, (joined,))
            self.assertEqual(len(digest), 64)
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), 1)

    def test_system_witness_separates_grade_proposal_and_certificate(self) -> None:
        result = deterministic_system_witness()
        self.assertFalse(result["learned_envelope_is_certificate"])
        self.assertTrue(result["learned_alone_rejected"])
        self.assertTrue(result["proof_erasure"])
        self.assertTrue(result["proof_valid"])
        self.assertTrue(result["invalid_local_certificate_rejected"])
        self.assertTrue(result["cycle_rejected"])
        self.assertTrue(result["audit_confirmation_lineage_disjoint"])
        self.assertFalse(result["powered_empirical_claim"])

    def test_adapter_rejects_wrong_role_or_self_asserted_audit(self) -> None:
        envelope = LearnedGradeEnvelope("s", "c", "error", 0.1, 1.0)
        audit = AuditRecord("a", "final_confirmation", 0, "w", "p", "s", "c", "checker", True, 0.1)
        with self.assertRaises(PlanContractError):
            checked_grade_adapter(envelope, audit)

    def test_preflight_preserves_final_embargo_and_moe_omission(self) -> None:
        result = implementation_preflight(
            ROOT / "experiments" / "protocol_v1.json",
            ROOT / "experiments" / "manifests_v1.json",
        )
        self.assertEqual(result["status"], "pass")
        self.assertFalse(result["final_payloads_generated"])
        self.assertEqual(result["hard_moe"], "omitted")

    def test_frozen_entry_point_verifies_hashes_and_requires_task21_token(self) -> None:
        result = run_preflight()
        self.assertTrue(result["source_hashes_verified"])
        self.assertFalse(result["final_payloads_generated"])
        with self.assertRaises(PermissionError):
            run_task21_final("not-the-task21-token")


if __name__ == "__main__":
    unittest.main()
