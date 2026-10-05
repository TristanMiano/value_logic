"""F14 pre-exposure integrity and recovery contracts, using development or mocks.

No prospective neural or retention generator is invoked by these tests.
The mocked orchestration seeds are deliberately outside the F15 registry.
Contributor: ChatGPT (GPT-6 Astra Pro), F14.
"""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from v2.experiments import freeze as F
from v2.experiments import neural as N
from v2.experiments import runner as R


class FreezeContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = F.load_json(F.DEFAULT_CONFIG)
        cls.prepared = N.prepare_neural(cls.config, cls.config["neural"]["development_seed"])

    def rehash(self, artifact):
        artifact["artifact_hash"] = N.canonical_hash({k: v for k, v in artifact.items() if k != "artifact_hash"})
        return artifact

    def test_current_configuration_and_development_discovery(self):
        F.validate_config(self.config)
        self.assertTrue(F.validate_prepared(self.prepared, self.config, self.config["neural"]["development_seed"]))
        self.assertFalse(self.prepared["evaluation_generated"])

    def test_json_rejects_duplicates_nonfinite_and_overflow(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"value.json"
            for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":1e309}'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    F.load_json(path)

    def test_changed_budget_or_labels_rejected_even_with_valid_hash(self):
        for key, value in (("steps", 128), ("batch_size", 1), ("stochastic_outcome_labels", 17),
                           ("expected_cost_training_labels", 1)):
            with self.subTest(key=key):
                mutant = copy.deepcopy(self.prepared)
                mutant["training"][key] = value
                with self.assertRaises(ValueError):
                    F.validate_prepared(self.rehash(mutant), self.config, mutant["discovery_seed"])

    def test_saved_network_and_decoder_dimensions_preflighted(self):
        mutants = []
        bad = copy.deepcopy(self.prepared); bad["network"]["w"].pop(); mutants.append(bad)
        bad = copy.deepcopy(self.prepared); bad["untrained_network"]["v"].pop(); mutants.append(bad)
        bad = copy.deepcopy(self.prepared)
        bad["alignments"]["identity/aligned"]["roles"][0]["decoder"]["coefficient"].pop()
        mutants.append(bad)
        for mutant in mutants:
            with self.assertRaises(ValueError):
                F.validate_prepared(self.rehash(mutant), self.config, mutant["discovery_seed"])

    def test_missing_control_or_per_role_budget_cannot_hide_in_aggregate(self):
        for mutation in ("missing", "budget", "candidate"):
            bad = copy.deepcopy(self.prepared)
            if mutation == "missing":
                del bad["alignments"]["identity/random"]
            elif mutation == "budget":
                bad["alignments"]["identity/random"]["roles"][0]["decoder_fits"] = 1
            else:
                bad["alignments"]["identity/random"]["roles"][0]["candidate_scores"].pop()
            with self.assertRaises(ValueError):
                F.validate_prepared(self.rehash(bad), self.config, bad["discovery_seed"])

    def test_configuration_binding_rejects_alternate_valid_object(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            F.write_json(root/"config.json", self.config)
            F.write_json(root/"manifest.json", {"config_path": "config.json"})
            changed = copy.deepcopy(self.config); changed["neural"]["training_steps"] += 1
            with patch.object(F, "ROOT", root), patch.object(F, "verify_manifest", return_value={"verified": True}):
                self.assertEqual(F.bound_configuration(self.config, root/"manifest.json"), {"verified": True})
                with self.assertRaises(ValueError):
                    F.bound_configuration(changed, root/"manifest.json")

    def test_dependency_closure_includes_parent_initializers_and_relative_imports(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/"pkg/sub").mkdir(parents=True)
            files = {"pkg/__init__.py": "from . import helper\n", "pkg/helper.py": "VALUE = 1\n",
                     "pkg/sub/__init__.py": "", "pkg/sub/main.py": "from ..helper import VALUE\n"}
            for name, content in files.items():
                (root/name).write_text(content)
            with patch.object(F, "ROOT", root):
                actual = {str(p.relative_to(root)) for p in F.local_dependencies([root/"pkg/sub/main.py"])}
            self.assertEqual(actual, set(files))

    def test_manifest_cannot_be_overwritten_and_detects_changed_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); config_path = root/"config.json"; manifest_path = root/"manifest.json"
            F.write_json(config_path, self.config); (root/"core.py").write_text("x = 1\n")
            paths = [config_path, root/"core.py"]
            with patch.object(F, "ROOT", root), patch.object(F, "manifest_paths", return_value=paths):
                F.create_manifest(config_path, manifest_path)
                self.assertTrue(F.verify_manifest(manifest_path)["verified"])
                with self.assertRaises(FileExistsError):
                    F.create_manifest(config_path, manifest_path)
                (root/"core.py").write_text("x = 2\n")
                with self.assertRaises(ValueError):
                    F.verify_manifest(manifest_path)


class RunnerContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)/"run"
        self.config = F.load_json(F.DEFAULT_CONFIG)
        self.config["neural"]["model_seeds"] = [101, 102]
        self.config["neural"]["evaluation_seeds"] = [201, 202]
        self.config["retention"]["evaluation_seeds"] = [301]
        self.config["retention"]["variants"] = ["unchanged", "small_price"]
        self.freeze = {"verified": True, "manifest_sha256": "synthetic-development-test"}
        self.mocks = []
        for owner, name, kwargs in (
            (F, "bound_configuration", {"return_value": self.freeze}),
            (F, "verify_environment", {"return_value": {"test_only": True}}),
            (F, "validate_prepared", {"return_value": True}),
            (N, "prepare_neural", {"side_effect": lambda c, s: {"artifact_hash": f"test-{s}", "discovery_seed": s}}),
            (N, "evaluate_neural", {"side_effect": lambda p, c, s: {"discovery_artifact_hash": p["artifact_hash"], "evaluation_seed": s}}),
            (R.R, "run_generated_case", {"side_effect": lambda s, v, c: {"seed": s, "variant": v}}),
            (R.A, "retention_assessment", {"return_value": {"bounded_application_criterion_met": False}}),
            (R.A, "neural_assessment", {"return_value": {"pilot_support_criterion_met": False}}),
        ):
            patcher = patch.object(owner, name, **kwargs)
            mock = patcher.start(); self.addCleanup(patcher.stop)
            self.mocks.append((name, mock))
        self.by_name = dict(self.mocks)

    def prepare(self):
        return R.prepare(self.config, self.output, Path("unused-manifest"))

    def evaluate(self, **kwargs):
        return R.evaluate(self.config, self.output, Path("unused-manifest"), **kwargs)

    def test_all_discovery_files_durable_before_any_evaluation(self):
        self.prepare()
        self.by_name["evaluate_neural"].assert_not_called()
        self.by_name["run_generated_case"].assert_not_called()
        def check(s, v, c):
            for i in range(2):
                self.assertTrue((self.output/f"preparation_attempt_1/model_{i}_prepared.json.sha256").is_file())
            start = R._read_artifact(self.output/"evaluation_start.json")
            self.assertEqual(start["preparation_manifest_sha256"], F.file_digest(self.output/"preparation_complete.json"))
            return {"seed": s, "variant": v}
        self.by_name["run_generated_case"].side_effect = check
        result = self.evaluate()
        self.assertEqual(result["neural_models"], 2)
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_late_invalid_model_blocks_all_retention_exposure(self):
        self.prepare()
        self.by_name["validate_prepared"].side_effect = [True, ValueError("malformed second saved network")]
        with self.assertRaises(ValueError):
            self.evaluate()
        self.by_name["run_generated_case"].assert_not_called()
        self.assertFalse((self.output/"evaluation_start.json").exists())

    def test_preparation_retry_reuses_completed_model_and_is_bounded(self):
        self.by_name["prepare_neural"].side_effect = [{"artifact_hash": "test-101", "discovery_seed": 101}, RuntimeError("controlled interruption")]
        with self.assertRaises(RuntimeError):
            self.prepare()
        first = self.output/"preparation_attempt_1/model_0_prepared.json"
        digest = F.file_digest(first)
        self.by_name["prepare_neural"].side_effect = lambda c, s: {"artifact_hash": f"test-{s}", "discovery_seed": s}
        result = R.prepare(self.config, self.output, Path("unused"), retry=True, failure_note="Synthetic interruption; unchanged retry")
        self.assertEqual(result["attempt"], 2)
        self.assertEqual(F.file_digest(first), digest)
        complete = R._read_artifact(self.output/"preparation_complete.json")
        self.assertEqual(len(complete["reused_units"]), 1)
        self.assertTrue((self.output/"preparation_attempt_1/failure.json").exists())
        with self.assertRaises(ValueError):
            R.prepare(self.config, self.output, Path("unused"), retry=True, failure_note="No third attempt allowed")

    def test_evaluation_retry_reuses_cases_and_never_refits(self):
        self.prepare()
        self.by_name["run_generated_case"].side_effect = [{"seed": 301, "variant": "unchanged"}, RuntimeError("controlled interruption")]
        with self.assertRaises(RuntimeError):
            self.evaluate()
        self.by_name["run_generated_case"].reset_mock()
        self.by_name["run_generated_case"].side_effect = lambda s, v, c: {"seed": s, "variant": v}
        result = self.evaluate(retry=True, failure_note="Synthetic interruption; unchanged models")
        self.assertEqual(self.by_name["run_generated_case"].call_count, 1)
        self.assertEqual(len(result["reused_units"]), 1)
        self.assertEqual(self.by_name["prepare_neural"].call_count, 2)
        self.assertTrue((self.output/"evaluation_attempt_1/failure.json").exists())

    def test_retry_requires_reason_and_original_preparation_digest(self):
        self.prepare()
        self.by_name["run_generated_case"].side_effect = RuntimeError("controlled interruption")
        with self.assertRaises(RuntimeError):
            self.evaluate()
        with self.assertRaises(ValueError):
            self.evaluate(retry=True)
        path = self.output/"preparation_complete.json"
        data = F.load_json(path); data["tampered_after_exposure"] = True
        F.write_json(path, data)
        Path(str(path)+".sha256").write_text(F.file_digest(path)+"\n")
        with self.assertRaises(ValueError):
            self.evaluate(retry=True, failure_note="Unchanged retry cannot use a changed manifest")
        self.assertFalse((self.output/"evaluation_attempt_2").exists())


if __name__ == "__main__":
    unittest.main()
