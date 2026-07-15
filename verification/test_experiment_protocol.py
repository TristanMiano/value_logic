"""Task 19A regressions for the frozen synthetic experiment protocol."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import replace
from hashlib import sha256
import json
from math import inf
from pathlib import Path
import unittest

from experiments.protocol import (
    ALPHA_CAL,
    CELL_DESIGN_COUNTS,
    FINAL_WORLD_CAP,
    K_90,
    OUTCOME_DESIGN_COUNTS,
    PROTOCOL_VERSION,
    REQUIRED_BINDING_FIELDS,
    STRATUM_DESIGN_COUNTS,
    AtomStratum,
    ContextCell,
    EvidenceMode,
    EvidenceSnapshot,
    FinalEmbargoError,
    Plan,
    PredictionRow,
    Proposal,
    Role,
    Schema,
    TaintedValue,
    UpdateEvent,
    apply_evidence_update,
    audit_manifest_disjointness,
    check_proposal_binding,
    decode_evidence,
    exact_active_set,
    f18_witness,
    fidelity_metrics,
    generate_world,
    latency_mean,
    loss_mean,
    manifest_summary,
    marginal_coverage,
    outcome_scale,
    paired_sample_size,
    reference_binding_record,
    round_world_count,
    select_or_fallback,
    succession_fixture,
    update_is_relevant,
    validate_scorer_payload,
    world_identity,
    worst_case_paired_sd,
)
from verification.kernel import AtomValue, Interval, Outcome


ROOT = Path(__file__).resolve().parents[1]


class GeneratorFormulaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.world = generate_world(Role.PILOT, 0)

    def test_latent_formulas_and_reference_regions_are_exact(self) -> None:
        zeros = {Plan.OLD: 0.0, Plan.SUCCESSOR: 0.0, Plan.NEW: 0.0}
        self.assertAlmostEqual(loss_mean(Plan.FALLBACK, 0.5, 0.2, zeros), 0.34)
        self.assertAlmostEqual(
            loss_mean(Plan.OLD, 0.0, 0.0, zeros), 0.122
        )
        self.assertAlmostEqual(
            latency_mean(Plan.SUCCESSOR, 0.5, 0.5, zeros), 47.0
        )
        self.assertAlmostEqual(outcome_scale(Schema.LOSS, 0.5, 0.5), 0.010)
        for probe in self.world.probes:
            self.assertAlmostEqual(
                probe.reference_region.lower,
                probe.oracle_mean - K_90 * probe.oracle_scale,
            )
            self.assertAlmostEqual(
                probe.reference_region.upper,
                probe.oracle_mean + K_90 * probe.oracle_scale,
            )

    def test_atom_and_context_quotas_are_exact_per_schema(self) -> None:
        self.assertEqual(len(self.world.probes), 80)
        for schema in Schema:
            probes = [probe for probe in self.world.probes if probe.schema is schema]
            self.assertEqual(Counter(p.stratum for p in probes), Counter(STRATUM_DESIGN_COUNTS))
            self.assertEqual(Counter(p.cell for p in probes), Counter(CELL_DESIGN_COUNTS))
        self.assertEqual(
            Counter(probe.value for probe in self.world.probes),
            Counter(
                {
                    AtomValue.SUPPORTED: 36,
                    AtomValue.OPEN: 32,
                    AtomValue.REFUTED: 12,
                }
            ),
        )
        self.assertEqual(sum(probe.boundary for probe in self.world.probes), 16)

    def test_missing_invalid_and_polarity_are_open_without_zero_semantics(self) -> None:
        missing = next(
            probe
            for probe in self.world.probes
            if probe.stratum is AtomStratum.MISSING_OPEN
        )
        invalid = next(
            probe
            for probe in self.world.probes
            if probe.stratum is AtomStratum.INVALID_OPEN
        )
        self.assertIs(missing.value, AtomValue.OPEN)
        self.assertFalse(missing.evidence_present)
        self.assertIsNone(missing.learning_target)
        self.assertIs(invalid.value, AtomValue.OPEN)
        self.assertTrue(invalid.evidence_present)
        self.assertFalse(invalid.evidence_valid)
        region = Interval(1.1, 1.2)
        self.assertIs(
            decode_evidence(
                region,
                1.0,
                evidence_present=True,
                evidence_valid=True,
                can_support=True,
                can_refute=False,
            ),
            AtomValue.OPEN,
        )

    def test_request_panel_has_all_outcomes_shared_loss_and_boundaries(self) -> None:
        self.assertEqual(Counter(r.outcome for r in self.world.requests), Counter(OUTCOME_DESIGN_COUNTS))
        self.assertEqual(Counter(r.cell for r in self.world.requests), Counter(CELL_DESIGN_COUNTS))
        self.assertEqual(sum(r.boundary_case for r in self.world.requests), 8)
        focal: dict[Outcome, Counter[str]] = defaultdict(Counter)
        for request in self.world.requests:
            focal[request.outcome][request.focal_atom] += 1
            atoms = {atom.name: atom for atom in request.atoms}
            self.assertEqual(atoms["A"].region, atoms["I"].region)
            self.assertGreater(request.delta, 0.0)
            if request.boundary_case:
                boundaries = [atom for atom in request.atoms if atom.boundary]
                self.assertEqual(len(boundaries), 1)
                self.assertIs(boundaries[0].value, AtomValue.SUPPORTED)
                self.assertEqual(boundaries[0].threshold, boundaries[0].region.upper)
        for outcome in (Outcome.GRANTED, Outcome.WITHHELD, Outcome.REFUSED):
            self.assertEqual(focal[outcome], Counter({"A": 4, "I": 4, "C": 4}))

    def test_generation_is_reproducible_and_roles_are_distinct(self) -> None:
        repeated = generate_world(Role.PILOT, 0)
        self.assertEqual(self.world, repeated)
        self.assertNotEqual(
            world_identity(Role.PILOT, 0).world_root,
            world_identity(Role.TRAIN, 0).world_root,
        )


class SuccessionAndUpdateTests(unittest.TestCase):
    def test_fixture_covers_overlap_gap_lapse_rebuttal_tolerance_and_dominator(self) -> None:
        fixture = succession_fixture()
        self.assertEqual(
            fixture.stage0_outcomes,
            {Plan.OLD: Outcome.GRANTED, Plan.SUCCESSOR: Outcome.GRANTED},
        )
        self.assertEqual(fixture.simultaneous_active, (Plan.OLD, Plan.SUCCESSOR))
        self.assertEqual(fixture.gap_active, ())
        self.assertTrue(fixture.gap_uses_fallback)
        self.assertIs(fixture.lapse_value, AtomValue.OPEN)
        self.assertIs(fixture.lapse_outcome, Outcome.WITHHELD)
        self.assertIs(fixture.rebuttal_value, AtomValue.REFUTED)
        self.assertIs(fixture.rebuttal_outcome, Outcome.REFUSED)
        self.assertIs(fixture.tolerance_old, AtomValue.OPEN)
        self.assertIs(fixture.tolerance_successor, AtomValue.SUPPORTED)
        self.assertEqual(fixture.later_dominates, (Plan.OLD, Plan.SUCCESSOR))
        self.assertTrue(
            all(
                interval.upper < 0
                for interval in fixture.paired_dominance_certificates.values()
            )
        )

    def test_active_set_preserves_overlap_and_mask_forces_gap_fallback(self) -> None:
        outcomes = {
            Plan.OLD: Outcome.GRANTED,
            Plan.SUCCESSOR: Outcome.GRANTED,
            Plan.NEW: Outcome.WITHHELD,
        }
        self.assertEqual(exact_active_set(outcomes), (Plan.OLD, Plan.SUCCESSOR))
        # The inactive new plan has the highest score but cannot be selected.
        self.assertIs(
            select_or_fallback(
                outcomes,
                {Plan.OLD: 1.0, Plan.SUCCESSOR: 2.0, Plan.NEW: 1000.0},
            ),
            Plan.SUCCESSOR,
        )
        self.assertIs(
            select_or_fallback(
                {Plan.OLD: Outcome.REFUSED, Plan.SUCCESSOR: Outcome.WITHHELD},
                {Plan.OLD: 1000.0, Plan.SUCCESSOR: 900.0},
            ),
            Plan.FALLBACK,
        )

    def test_irrelevant_write_is_exactly_invariant_and_relevant_write_changes(self) -> None:
        reads = frozenset({"region:O:J", "current:O:J"})
        before = EvidenceSnapshot(Interval(0.14, 0.18), True, "v0")
        irrelevant = UpdateEvent("archive:N", frozenset({"archive:N"}))
        self.assertFalse(update_is_relevant(reads, irrelevant))
        self.assertIs(apply_evidence_update(before, reads, irrelevant), before)
        relevant = UpdateEvent(
            "counter:O:J",
            frozenset({"region:O:J"}),
            replacement_region=Interval(0.23, 0.25),
            replacement_version="v1",
        )
        self.assertTrue(update_is_relevant(reads, relevant))
        self.assertEqual(
            apply_evidence_update(before, reads, relevant),
            EvidenceSnapshot(Interval(0.23, 0.25), True, "v1"),
        )


class FirewallAndBindingTests(unittest.TestCase):
    def test_whitelisted_preoutcome_payload_passes(self) -> None:
        validate_scorer_payload(
            {
                "x": TaintedValue(0.1, ("x",)),
                "complexity": 0.3,
                "atom_address": {"slot": "A", "plan": "O"},
                "candidate_library_id": TaintedValue(
                    "abc", ("candidate_library_id",), transform="sha256"
                ),
            }
        )

    def test_direct_aliased_nested_and_hashed_leakage_are_rejected(self) -> None:
        bad_payloads = (
            {"oracle_upper": 1.0},
            {"x": TaintedValue(0.1, ("oracle_upper",))},
            {"atom_address": {"oracle_state": "Supported"}},
            {
                "candidate_library_id": TaintedValue(
                    "hash", ("public_outcome",), transform="sha256"
                )
            },
        )
        for payload in bad_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    validate_scorer_payload(payload)

    def test_complete_matching_binding_is_accepted(self) -> None:
        record = reference_binding_record()
        proposal = Proposal(
            0.10,
            0.20,
            "scorer-hash",
            "normalization-v1",
            "J",
            "O",
            "core-target-law",
        )
        decision = check_proposal_binding(record, proposal, current_stage=1)
        self.assertTrue(decision.accepted, decision.reasons)
        self.assertEqual(set(record), set(REQUIRED_BINDING_FIELDS))
        self.assertEqual(record["alpha_cal"], ALPHA_CAL)

    def test_missing_mismatch_unbounded_expired_and_bad_polarity_reject(self) -> None:
        proposal = Proposal(
            0.10,
            0.20,
            "scorer-hash",
            "normalization-v1",
            "J",
            "O",
            "core-target-law",
        )
        variants = []
        missing = reference_binding_record()
        missing.pop("checker_version")
        variants.append(missing)
        variants.append(reference_binding_record(scorer_parameter_hash="other"))
        variants.append(reference_binding_record(eta_cal_or_infinity=inf))
        variants.append(reference_binding_record(valid_through_stage=0))
        variants.append(
            reference_binding_record(
                certificate_mode=EvidenceMode.UPPER_ONLY.value,
                can_support=True,
                can_refute=True,
            )
        )
        for record in variants:
            with self.subTest(record=record):
                self.assertFalse(
                    check_proposal_binding(record, proposal, current_stage=1).accepted
                )


class ManifestMetricAndPowerTests(unittest.TestCase):
    def test_final_worlds_are_embargoed_but_ids_can_be_frozen(self) -> None:
        summary = manifest_summary(Role.FINAL_CONFIRMATION, 3)
        self.assertTrue(summary.embargoed)
        self.assertFalse(summary.payloads_generated)
        with self.assertRaises(FinalEmbargoError):
            generate_world(Role.FINAL_CONFIRMATION, 0)

    def test_manifests_are_lineage_disjoint(self) -> None:
        manifests = (
            manifest_summary(Role.PILOT, 3, payloads_generated=True),
            manifest_summary(Role.TRAIN, 4),
            manifest_summary(Role.CALIBRATION, 3),
            manifest_summary(Role.VALIDATION, 3),
            manifest_summary(Role.SYSTEM_AUDIT, 3),
            manifest_summary(Role.FINAL_CONFIRMATION, 3),
        )
        audit_manifest_disjointness(manifests)
        with self.assertRaises(ValueError):
            audit_manifest_disjointness((manifests[0], replace(manifests[0])))

    def test_metric_skeleton_preserves_false_support_and_refutation(self) -> None:
        rows = (
            PredictionRow("w1", AtomValue.SUPPORTED, AtomValue.SUPPORTED, 2.0),
            PredictionRow("w1", AtomValue.OPEN, AtomValue.SUPPORTED, 1.0),
            PredictionRow("w2", AtomValue.REFUTED, AtomValue.REFUTED, 1.0),
            PredictionRow("w2", AtomValue.OPEN, AtomValue.REFUTED, 1.0),
        )
        metrics = fidelity_metrics(rows)
        self.assertAlmostEqual(metrics.accuracy, 0.6)
        self.assertAlmostEqual(metrics.false_support_rate or 0.0, 1.0 / 3.0)
        self.assertAlmostEqual(metrics.false_refutation_rate or 0.0, 0.5)
        self.assertEqual(marginal_coverage(((1.0, (-inf, inf)),)), 1.0)

    def test_power_rule_freezes_at_cap_without_exceeding_it(self) -> None:
        superiority_sd = worst_case_paired_sd(0.90, 0.80)
        in_regime_sd = worst_case_paired_sd(0.90, 0.90)
        self.assertEqual(paired_sample_size(superiority_sd, 0.05, alpha=0.025), 1402)
        self.assertEqual(paired_sample_size(in_regime_sd, 0.02, alpha=0.05), 4925)
        self.assertEqual(round_world_count(4925), FINAL_WORLD_CAP)

    def test_f18_sign_boundary_and_masking_witness_is_frozen(self) -> None:
        witness = f18_witness()
        self.assertEqual(witness["support_surplus"], (2.0, 12.0, 3.0))
        self.assertEqual(witness["grant"], 1.0)
        self.assertEqual(witness["boundary_surplus"], 0.0)
        self.assertEqual(witness["open_pair"], (0.0, 0.0))
        self.assertEqual(witness["bias_bypass"], 7.0)
        self.assertGreater(witness["raw_rank_with_missing_constraint"], 0.0)
        self.assertEqual(witness["masked_rank_with_missing_constraint"], 0.0)


class FrozenArtifactTests(unittest.TestCase):
    def test_protocol_hashes_and_embargo_are_self_consistent(self) -> None:
        protocol_path = ROOT / "experiments" / "protocol_v1.json"
        manifests_path = ROOT / "experiments" / "manifests_v1.json"
        results_path = ROOT / "experiments" / "pilot_results_v1.json"
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        manifests = json.loads(manifests_path.read_text(encoding="utf-8"))
        results = json.loads(results_path.read_text(encoding="utf-8"))
        digest = lambda path: sha256(path.read_bytes()).hexdigest()
        self.assertEqual(protocol["protocol_version"], PROTOCOL_VERSION)
        self.assertEqual(protocol["pilot_results_sha256"], digest(results_path))
        self.assertEqual(protocol["manifests_sha256"], digest(manifests_path))
        self.assertEqual(
            protocol["design_sha256"],
            digest(ROOT / "experiments" / "01_design.md"),
        )
        self.assertEqual(
            protocol["generator_source_sha256"],
            digest(ROOT / "experiments" / "protocol.py"),
        )
        self.assertEqual(
            protocol["pilot_runner_sha256"],
            digest(ROOT / "experiments" / "run_pilot.py"),
        )
        self.assertFalse(protocol["embargo"]["final_payloads_generated"])
        self.assertFalse(results["production_world_payloads_generated"])
        final = next(
            item
            for item in manifests["manifests"]
            if item["role"] == Role.FINAL_CONFIRMATION.value
        )
        self.assertTrue(final["embargoed"])
        self.assertFalse(final["payloads_generated"])


if __name__ == "__main__":
    unittest.main()
