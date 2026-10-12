"""Content and destination checks for preserved archive source namespaces."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from verification.archive_origins import MANIFEST, SCHEMA, load_origins
from verification.check_links import check_links


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


class ArchiveNamespaceTests(unittest.TestCase):
    def fixture(self, root: Path) -> dict:
        (root / "docs").mkdir()
        (root / "archive").mkdir()
        (root / "docs/chapter.md").write_text("# Current chapter\n", encoding="utf-8")
        (root / "docs/evidence.md").write_text("# Checked evidence\n", encoding="utf-8")
        source = root / "archive/chapter.md"
        source.write_text(
            "# Original chapter\n[proof](evidence.md#checked-evidence) "
            "[self](#original-chapter)\n", encoding="utf-8"
        )
        record = {"path": "docs/chapter.md", "sha256": _hash(source)}
        _write_json(root / "archive/receipt.json", {"sources": [record]})
        registry = {"schema": SCHEMA, "entries": [{
            "stored_path": "archive/chapter.md", "sha256": _hash(source),
            "origin_path": "docs/chapter.md", "provenance": [{
                "path": "archive/receipt.json", "sha256": _hash(root / "archive/receipt.json"),
                "pointer": ["sources", 0], "kind": "record:path:sha256",
            }],
        }]}
        _write_json(root / MANIFEST, registry)
        return registry

    def test_verified_copy_retains_original_relative_context_and_own_anchors(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.assertEqual(load_origins(root), {"archive/chapter.md": "docs/chapter.md"})
            self.assertEqual(check_links(root), [])

    def test_missing_targets_and_wrong_anchors_remain_failures(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "docs/evidence.md").write_text("# Different heading\n", encoding="utf-8")
            self.assertEqual([x.detail for x in check_links(root)], ["heading anchor does not exist"])
            (root / "docs/evidence.md").unlink()
            self.assertEqual([x.detail for x in check_links(root)], ["target does not exist"])

    def test_source_or_provenance_tamper_fails_closed(self) -> None:
        for relative in ("archive/chapter.md", "archive/receipt.json"):
            with self.subTest(relative=relative), TemporaryDirectory() as directory:
                root = Path(directory)
                self.fixture(root)
                path = root / relative
                path.write_bytes(path.read_bytes() + b"\n")
                with self.assertRaisesRegex(ValueError, "content identity mismatch"):
                    load_origins(root)
                self.assertIn("invalid document origin manifest", check_links(root)[0].detail)

    def test_rehashed_but_unrelated_provenance_is_not_a_binding(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            registry = self.fixture(root)
            _write_json(root / "archive/receipt.json", {"sources": [{
                "path": "docs/evidence.md", "sha256": _hash(root / "archive/chapter.md")
            }]})
            registry["entries"][0]["provenance"][0]["sha256"] = _hash(root / "archive/receipt.json")
            _write_json(root / MANIFEST, registry)
            with self.assertRaisesRegex(ValueError, "does not bind"):
                load_origins(root)

    def test_unregistered_copies_get_no_filename_heuristic(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / MANIFEST).unlink()
            self.assertEqual([x.detail for x in check_links(root)], ["target does not exist"])

    def test_unsafe_or_duplicate_registry_paths_are_rejected(self) -> None:
        for kind in ("traversal", "duplicate"):
            with self.subTest(kind=kind), TemporaryDirectory() as directory:
                root = Path(directory)
                registry = self.fixture(root)
                if kind == "traversal":
                    registry["entries"][0]["origin_path"] = "../outside.md"
                else:
                    registry["entries"].append(registry["entries"][0].copy())
                _write_json(root / MANIFEST, registry)
                with self.assertRaises(ValueError):
                    load_origins(root)

    def test_historical_checkout_prefix_is_source_bound_and_checks_destination(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            registry = self.fixture(root)
            source = root / "archive/review.md"
            source.write_text("[proof](sandbox:/old/checkout/docs/evidence.md#checked-evidence)\n", encoding="utf-8")
            _write_json(root / "archive/start.json", {"cwd": "/old/checkout"})
            registry["checkout_roots"] = [{
                "prefix": "sandbox:/old/checkout/", "sources": [{
                    "path": "archive/review.md", "sha256": _hash(source),
                }], "provenance": {
                    "path": "archive/start.json", "sha256": _hash(root / "archive/start.json"),
                    "pointer": ["cwd"],
                },
            }]
            _write_json(root / MANIFEST, registry)
            self.assertEqual(check_links(root), [])
            (root / "unregistered.md").write_bytes(source.read_bytes())
            self.assertEqual([x.source.name for x in check_links(root)], ["unregistered.md"])
            (root / "unregistered.md").unlink()
            (root / "docs/evidence.md").unlink()
            self.assertEqual(len(check_links(root)), 2)

    def test_complete_historical_transform_chain_is_required(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            registry = self.fixture(root)
            entry = registry["entries"][0]
            old_digest = entry["sha256"]
            source = root / entry["stored_path"]
            source.write_bytes(source.read_bytes() + b"\nPreserved presentation change.\n")
            entry["origin_sha256"] = old_digest
            entry["sha256"] = _hash(source)
            record = {"path": entry["stored_path"], "before_sha256": old_digest,
                      "after_sha256": entry["sha256"]}
            _write_json(root / "archive/transform.json", record)
            entry["transforms"] = [{"path": "archive/transform.json",
                                    "sha256": _hash(root / "archive/transform.json"), "pointer": []}]
            _write_json(root / MANIFEST, registry)
            self.assertEqual(check_links(root), [])
            entry["transforms"] = []
            _write_json(root / MANIFEST, registry)
            with self.assertRaisesRegex(ValueError, "does not reach current bytes"):
                load_origins(root)

    def test_excerpt_context_and_assembled_fragment_still_check_actual_anchor(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            registry = self.fixture(root)
            entry = registry["entries"][0]
            passage = "This archived chapter is the reviewed chapter of docs/chapter.md."
            (root / "archive/review.txt").write_text(passage, encoding="utf-8")
            proof = entry["provenance"][0]
            entry["provenance"] = [{**proof, "kind": "source-context", "origin_pointer": ["path"],
                "identity": {"path": proof["path"], "sha256": proof["sha256"],
                             "pointer": ["sources", 0, "sha256"]},
                "context": {"path": "archive/review.txt", "sha256": _hash(root / "archive/review.txt"),
                            "passage": passage}}]
            entry["assembled_fragments"] = ["original-chapter"]
            _write_json(root / MANIFEST, registry)
            self.assertEqual([x.detail for x in check_links(root)], ["heading anchor does not exist"])
            (root / "docs/chapter.md").write_text("# Original chapter\n", encoding="utf-8")
            self.assertEqual(check_links(root), [])
            entry["provenance"][0]["context"]["passage"] = "Unrecorded context."
            _write_json(root / MANIFEST, registry)
            with self.assertRaisesRegex(ValueError, "passage is unavailable"):
                load_origins(root)

    def test_recorded_anchor_correction_cannot_redirect_other_paths_or_bypass_anchor(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            registry = self.fixture(root)
            entry = registry["entries"][0]
            source = root / entry["stored_path"]
            source.write_text("[old](evidence.md#old-heading)\n", encoding="utf-8")
            entry["sha256"] = _hash(source)
            _write_json(root / "archive/receipt.json", {"sources": [{
                "path": "docs/chapter.md", "sha256": entry["sha256"]}]})
            entry["provenance"][0]["sha256"] = _hash(root / "archive/receipt.json")
            _write_json(root / "archive/correction.json", {
                "path": "docs/chapter.md", "before_sha256": entry["sha256"],
                "substitutions": {"#old-heading": "#checked-evidence"}})
            correction = {"source": entry["stored_path"], "sha256": entry["sha256"],
                "target": "evidence.md#old-heading", "replacement": "evidence.md#checked-evidence",
                "provenance": {"path": "archive/correction.json",
                    "sha256": _hash(root / "archive/correction.json"), "pointer": []}}
            registry["link_corrections"] = [correction]
            _write_json(root / MANIFEST, registry)
            self.assertEqual(check_links(root), [])
            (root / "docs/evidence.md").write_text("# Missing replacement\n", encoding="utf-8")
            self.assertEqual([x.detail for x in check_links(root)], ["heading anchor does not exist"])
            correction["replacement"] = "chapter.md#checked-evidence"
            _write_json(root / MANIFEST, registry)
            with self.assertRaisesRegex(ValueError, "mismatched recorded link correction"):
                load_origins(root)


if __name__ == "__main__":
    unittest.main()
