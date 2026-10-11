"""Preservation and safe export checks for relocated historical evidence."""

import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest

from tools.evidence_paths import MANIFEST, REPO, load_entries, materialize, resolve, verify


class RecordedEvidenceTests(unittest.TestCase):
    def test_real_manifest_verifies_every_original_identity(self):
        result = verify(REPO)
        self.assertEqual(result, {
            "status": "verified",
            "relocated_paths": 32,
            "unique_objects": 30,
            "original_bytes": 5_350_075,
        })
        entries = load_entries(REPO)
        self.assertEqual(len(entries), 32)
        self.assertEqual(len({entry["stored_path"] for entry in entries}), 30)


class EvidenceExportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.destination = self.root / "export"
        self.entries = []
        self.payloads = {}
        samples = [
            ("a.txt", b"alpha\n", "100644"),
            ("nested/b.bin", b"\x00binary\xff\n", "100755"),
            ("copies/a.txt", b"alpha\n", "100644"),
        ]
        for original, data, mode in samples:
            digest = hashlib.sha256(data).hexdigest()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            stored = "v3/evidence/objects/" + digest
            path = self.repo / stored
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            self.entries.append({
                "original_path": original,
                "stored_path": stored,
                "sha256": digest,
                "git_blob": blob,
                "mode": mode,
                "bytes": len(data),
            })
            self.payloads[original] = data
        self.write_manifest()

    def write_manifest(self):
        (self.repo / MANIFEST).write_text(json.dumps({
            "schema": "value_logic.evidence_relocations.v1",
            "relocated_paths": len(self.entries),
            "unique_objects": len({entry["stored_path"] for entry in self.entries}),
            "original_bytes": sum(entry["bytes"] for entry in self.entries),
            "entries": self.entries,
        }), encoding="utf-8")

    def test_short_fixture_roundtrip_and_idempotence(self):
        self.assertEqual(verify(self.repo)["unique_objects"], 2)
        first = materialize(self.destination, self.repo)
        self.assertEqual((first["created"], first["already_identical"]), (3, 0))
        times = {}
        for entry in self.entries:
            path = self.destination / entry["original_path"]
            self.assertEqual(path.read_bytes(), self.payloads[entry["original_path"]])
            self.assertEqual(resolve(entry["original_path"], self.repo),
                             self.repo / entry["stored_path"])
            times[path] = path.stat().st_mtime_ns
            if os.name != "nt":
                expected_mode = 0o755 if entry["mode"] == "100755" else 0o644
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), expected_mode)
        second = materialize(self.destination, self.repo)
        self.assertEqual((second["created"], second["already_identical"]), (0, 3))
        self.assertEqual({path: path.stat().st_mtime_ns for path in times}, times)

    def test_later_tampered_object_prevents_all_export_writes(self):
        # The first entry is sound; detecting a later problem must precede all writes.
        (self.repo / self.entries[1]["stored_path"]).write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "does not match its identity"):
            materialize(self.destination, self.repo)
        self.assertFalse(self.destination.exists())
        with self.assertRaisesRegex(ValueError, "does not match its identity"):
            resolve(self.entries[1]["original_path"], self.repo)

    def test_each_identity_component_is_verified(self):
        cases = {"bytes": 999, "sha256": "0" * 64, "git_blob": "0" * 40}
        for field, changed in cases.items():
            with self.subTest(field=field):
                original = self.entries[1][field]
                original_stored = self.entries[1]["stored_path"]
                self.entries[1][field] = changed
                if field == "sha256":
                    # Keep the manifest structurally valid so content hashing is tested.
                    relocated = "v3/evidence/objects/" + changed
                    (self.repo / relocated).write_bytes(self.payloads["nested/b.bin"])
                    self.entries[1]["stored_path"] = relocated
                self.write_manifest()
                with self.assertRaisesRegex(ValueError, "does not match its identity"):
                    materialize(self.destination, self.repo)
                self.assertFalse(self.destination.exists())
                self.entries[1][field] = original
                self.entries[1]["stored_path"] = original_stored
        self.write_manifest()

    def test_later_existing_mismatch_prevents_earlier_writes(self):
        conflict = self.destination / self.entries[2]["original_path"]
        conflict.parent.mkdir(parents=True)
        conflict.write_bytes(b"existing user data")
        with self.assertRaisesRegex(ValueError, "Existing destination differs"):
            materialize(self.destination, self.repo)
        self.assertEqual(conflict.read_bytes(), b"existing user data")
        self.assertFalse((self.destination / "a.txt").exists())
        self.assertFalse((self.destination / "nested").exists())

    def test_blocked_parent_preflight_prevents_earlier_writes(self):
        self.destination.mkdir()
        blocker = self.destination / "nested"
        blocker.write_bytes(b"existing user file")
        with self.assertRaises((ValueError, OSError)):
            materialize(self.destination, self.repo)
        self.assertEqual(blocker.read_bytes(), b"existing user file")
        self.assertFalse((self.destination / "a.txt").exists())
        self.assertFalse((self.destination / "copies").exists())

    def test_manifest_file_and_descendant_conflict_prevents_all_writes(self):
        self.entries[0]["original_path"] = "clash"
        self.entries[1]["original_path"] = "clash/child"
        self.write_manifest()
        with self.assertRaises((ValueError, OSError)):
            materialize(self.destination, self.repo)
        self.assertFalse(self.destination.exists())

    def test_invalid_original_paths_refused_before_writes(self):
        invalid = ["../escape", "snap/../../escape", "/absolute", "C:/absolute",
                   "snap\\outside", "snap//file", "snap/./file", ".", ""]
        for original in invalid:
            with self.subTest(path=original):
                self.entries[2]["original_path"] = original
                self.write_manifest()
                with self.assertRaisesRegex(ValueError, "Invalid relative path"):
                    materialize(self.destination, self.repo)
                self.assertFalse(self.destination.exists())

    def test_live_repository_destinations_are_refused(self):
        for destination in (self.repo, self.repo / "export"):
            with self.subTest(destination=destination):
                with self.assertRaisesRegex(ValueError, "outside the working repository"):
                    materialize(destination, self.repo)
        self.assertFalse((self.repo / "a.txt").exists())
        self.assertFalse((self.repo / "export").exists())
        self.assertEqual(verify(self.repo)["relocated_paths"], 3)

    def test_parent_export_cannot_write_back_into_live_repository(self):
        self.entries[2]["original_path"] = "repo/injected.txt"
        self.write_manifest()
        with self.assertRaisesRegex(ValueError, "enter the working repository"):
            materialize(self.root, self.repo)
        self.assertFalse((self.root / "a.txt").exists())
        self.assertFalse((self.root / "nested").exists())
        self.assertFalse((self.repo / "injected.txt").exists())


if __name__ == "__main__":
    unittest.main()
