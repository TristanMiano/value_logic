"""Focused integrity checks for source-bound portable mathematical views.

All fixtures are temporary documents and provenance records. These checks
exercise publication admission; they execute no scientific source or solver.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from v3.checks.math_markdown import analyze_documents
from verification.math_views import MANIFEST, SCHEMA, generate, verify_views, view_text


SOURCE = "v3/work_logs/demo/report.md"
VIEW = "docs/math/fixture.md"
RECEIPT = "v3/work_logs/demo/receipt.json"


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class PortableMathViewIntegrityTests(unittest.TestCase):
    def fixture(self, root: Path) -> dict:
        source = root / SOURCE
        source.parent.mkdir(parents=True)
        source.write_text(
            "# Preserved report\n\n"
            "Signed by reviewer.  \nUTC date.  \n\n"
            "The retained bound is \\(x+1\\).\n\n"
            "\\[\\operatorname{rank}(A)\\]\n\n"
            "See [checked evidence](../../../evidence.md#checked-evidence).\n"
            "The literal `[example](missing.md)` is not a prose link.\n",
            encoding="utf-8",
        )
        (root / "evidence.md").write_text("# Checked evidence\n", encoding="utf-8")
        (root / "docs/math").mkdir(parents=True)
        (root / "docs/math_markdown.md").write_text(
            "# Formatting and provenance\n", encoding="utf-8"
        )
        _write_json(root / RECEIPT, {"files": [{"path": SOURCE, "sha256": _hash(source)}]})
        view = root / VIEW
        view.write_text(view_text(root, SOURCE, VIEW, {}), encoding="utf-8")
        document = {
            "schema": SCHEMA,
            "entries": [{
                "source_path": SOURCE,
                "source_sha256": _hash(source),
                "view_path": VIEW,
                "view_sha256": _hash(view),
                "preservation": {
                    "kind": "scientific-record",
                    "path": RECEIPT,
                    "sha256": _hash(root / RECEIPT),
                    "pointer": ["files", 0],
                    "path_pointer": ["path"],
                    "sha256_pointer": ["sha256"],
                    "path_base": "",
                },
            }],
        }
        _write_json(root / MANIFEST, document)
        return document

    def test_bound_view_preserves_source_and_rebases_actual_links(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            document = self.fixture(root)
            before = (root / SOURCE).read_bytes()
            self.assertEqual(verify_views(root, {}), {SOURCE: document["entries"][0]})
            self.assertEqual((root / SOURCE).read_bytes(), before)
            derived = (root / VIEW).read_text(encoding="utf-8")
            self.assertIn("[checked evidence](../../evidence.md#checked-evidence)", derived)
            self.assertIn("`[example](missing.md)`", derived)
            self.assertIn("Signed by reviewer.\\\nUTC date.\\\n", derived)
            # Formatting whitespace must preserve a prose hard break and leave
            # trailing spaces inside code/math literals byte-for-byte intact.
            from verification.math_views import portable_hard_breaks
            prose = "Signed by reviewer.  \nUTC date.  \n"
            literals = ("\n```text\nliteral  \n```\n"
                        "\n```math\nx = 1  \n```\n"
                        "\nInline `literal  \ncode` stays literal.\n")
            self.assertEqual(portable_hard_breaks(prose + literals),
                             "Signed by reviewer.\\\nUTC date.\\\n" + literals)

    def test_source_tampering_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            source = root / SOURCE
            source.write_bytes(source.read_bytes() + b"\nAn unrecorded revision.\n")
            with self.assertRaises(ValueError):
                verify_views(root, {})

    def test_view_tampering_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            view = root / VIEW
            view.write_text(view.read_text(encoding="utf-8").replace("x+1", "x+2"),
                            encoding="utf-8")
            with self.assertRaises(ValueError):
                verify_views(root, {})

    def test_rehashing_a_changed_view_cannot_replace_exact_derivation(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            document = self.fixture(root)
            view = root / VIEW
            view.write_text(view.read_text(encoding="utf-8").replace("x+1", "x+2"),
                            encoding="utf-8")
            document["entries"][0]["view_sha256"] = _hash(view)
            _write_json(root / MANIFEST, document)
            with self.assertRaises(ValueError):
                verify_views(root, {})

    def test_provenance_content_tampering_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            receipt = root / RECEIPT
            receipt.write_bytes(receipt.read_bytes() + b"\n")
            with self.assertRaises(ValueError):
                verify_views(root, {})

    def test_rehashed_source_and_new_exact_view_still_need_original_receipt(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            document = self.fixture(root)
            source = root / SOURCE
            source.write_text(source.read_text(encoding="utf-8").replace("x+1", "x+2"),
                              encoding="utf-8")
            view = root / VIEW
            view.write_text(view_text(root, SOURCE, VIEW, {}), encoding="utf-8")
            entry = document["entries"][0]
            entry["source_sha256"] = _hash(source)
            entry["view_sha256"] = _hash(view)
            _write_json(root / MANIFEST, document)
            with self.assertRaises(ValueError):
                verify_views(root, {})

    def test_missing_preservation_provenance_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            document = self.fixture(root)
            del document["entries"][0]["preservation"]
            _write_json(root / MANIFEST, document)
            with self.assertRaises(ValueError):
                verify_views(root, {})

    def test_rehashed_receipt_for_another_source_is_not_a_binding(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            document = self.fixture(root)
            _write_json(root / RECEIPT, {"files": [{
                "path": "v3/work_logs/demo/another.md", "sha256": _hash(root / SOURCE),
            }]})
            document["entries"][0]["preservation"]["sha256"] = _hash(root / RECEIPT)
            _write_json(root / MANIFEST, document)
            with self.assertRaises(ValueError):
                verify_views(root, {})

    def test_supplied_origin_map_cannot_invent_archive_authority(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            document = self.fixture(root)
            document["entries"][0]["preservation"] = {
                "kind": "archive-origin", "origin_path": "docs/original.md",
            }
            _write_json(root / MANIFEST, document)
            for origins in ({}, {SOURCE: "docs/original.md"}):
                with self.subTest(origins=origins), self.assertRaises(ValueError):
                    verify_views(root, origins)

    def test_verified_archive_does_not_hide_an_unbound_active_violation(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            active = root / "v3/live.md"
            active.write_text("# Live manuscript\n\\(x+2\\) needs normalization.\n",
                              encoding="utf-8")
            before = {name: (root / name).read_bytes() for name in (SOURCE, VIEW, "v3/live.md")}
            result = analyze_documents(root, [Path(SOURCE), Path(VIEW), Path("v3/live.md")])
            self.assertEqual(result["verified_portable_views"], 1)
            self.assertTrue(result["issues_before"])
            self.assertEqual({issue["path"] for issue in result["issues_before"]}, {"v3/live.md"})
            self.assertTrue(result["preserved_source_issues"])
            self.assertEqual({issue["path"] for issue in result["preserved_source_issues"]}, {SOURCE})
            self.assertEqual({entry["path"] for entry in result["changed_files"]}, {"v3/live.md"})
            self.assertEqual({name: (root / name).read_bytes() for name in before}, before)

    def test_generation_keeps_registered_sources_and_ignores_unregistered_files(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            unregistered = root / "active.md"
            unregistered.write_text("# Active draft\n\\(needs formatting\\)\n", encoding="utf-8")
            before = {SOURCE: (root / SOURCE).read_bytes(),
                      "active.md": unregistered.read_bytes()}
            generate(root)
            self.assertEqual(set(verify_views(root, {})), {SOURCE})
            self.assertEqual({name: (root / name).read_bytes() for name in before}, before)

    def test_generation_reconstructs_only_the_missing_registered_view(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            expected = (root / VIEW).read_bytes()
            (root / VIEW).unlink()
            before = {name: (root / name).read_bytes() for name in (SOURCE, MANIFEST, RECEIPT)}
            generate(root)
            self.assertEqual((root / VIEW).read_bytes(), expected)
            self.assertEqual({name: (root / name).read_bytes() for name in before}, before)

    def test_generation_cannot_launder_rehashed_view_tampering(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            document = self.fixture(root)
            view = root / VIEW
            view.write_text(view.read_text(encoding="utf-8").replace("x+1", "x+2"),
                            encoding="utf-8")
            document["entries"][0]["view_sha256"] = _hash(view)
            _write_json(root / MANIFEST, document)
            before = {name: (root / name).read_bytes() for name in (SOURCE, VIEW, MANIFEST, RECEIPT)}
            with self.assertRaises(ValueError):
                generate(root)
            self.assertEqual({name: (root / name).read_bytes() for name in before}, before)


if __name__ == "__main__":
    unittest.main()
