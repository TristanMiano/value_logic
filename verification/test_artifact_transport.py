"""Regression checks for platform-invariant future JSON artifacts."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from experiments.artifact_io import write_json_lf


class ArtifactTransportTests(unittest.TestCase):
    def test_future_json_writer_emits_exact_lf_bytes(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.json"
            write_json_lf(path, {"second": 2, "first": [1, 3]})

            self.assertEqual(
                path.read_bytes(),
                b'{\n  "first": [\n    1,\n    3\n  ],\n  "second": 2\n}\n',
            )
            self.assertFalse(path.with_name(path.name + ".tmp").exists())


if __name__ == "__main__":
    unittest.main()
