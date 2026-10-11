"""Focused local-reference checks for exact historical snapshot relocations."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.evidence_paths import MANIFEST
from verification.check_links import check_links


class RelocatedLinkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        data = b"# Archived title\n\nPreserved historical content.\n"
        digest = hashlib.sha256(data).hexdigest()
        stored = "v3/evidence/objects/" + digest
        self.object = self.root / stored
        self.object.parent.mkdir(parents=True)
        self.object.write_bytes(data)
        (self.root / MANIFEST).write_text(json.dumps({
            "schema": "value_logic.evidence_relocations.v1",
            "relocated_paths": 1,
            "entries": [{
                "original_path": "history/report.md",
                "stored_path": stored,
                "sha256": digest,
                "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
                "mode": "100644",
                "bytes": len(data),
            }],
        }), encoding="utf-8")

    def source(self, text):
        (self.root / "source.md").write_text(text, encoding="utf-8")

    def test_relocated_file_and_original_markdown_anchor_resolve(self):
        self.source("[file](history/report.md) [heading](history/report.md#archived-title)\n")
        self.assertEqual(check_links(self.root), [])
        self.assertFalse((self.root / "history/report.md").exists())

    def test_bad_anchor_is_still_rejected_for_extensionless_object(self):
        self.source("[wrong](history/report.md#absent-heading)\n")
        broken = check_links(self.root)
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0].detail, "heading anchor does not exist")

    def test_unmapped_missing_target_is_still_rejected(self):
        self.source("[missing](history/other.md)\n")
        broken = check_links(self.root)
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0].detail, "target does not exist")

    def test_tampered_object_is_rejected(self):
        self.source("[file](history/report.md)\n")
        self.object.write_bytes(b"altered")
        broken = check_links(self.root)
        self.assertEqual(len(broken), 1)
        self.assertIn("relocated target cannot be verified", broken[0].detail)
        self.assertIn("does not match its identity", broken[0].detail)

    def test_missing_object_is_rejected(self):
        self.source("[file](history/report.md)\n")
        self.object.unlink()
        broken = check_links(self.root)
        self.assertEqual(len(broken), 1)
        self.assertIn("relocated target cannot be verified", broken[0].detail)

    def test_root_without_manifest_keeps_physical_link_behavior(self):
        (self.root / MANIFEST).unlink()
        (self.root / "live.md").write_text("# Current title\n", encoding="utf-8")
        self.source("[live](live.md#current-title) [missing](history/report.md)\n")
        broken = check_links(self.root)
        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0].target, "history/report.md")
        self.assertEqual(broken[0].detail, "target does not exist")

    def test_direct_script_invocation_from_another_directory(self):
        self.source("[heading](history/report.md#archived-title)\n")
        script = Path(__file__).resolve().parent / "check_links.py"
        result = subprocess.run([sys.executable, str(script), str(self.root)],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
