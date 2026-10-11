"""Regression checks for portable Git checkout paths."""

import contextlib
import io
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tools.check_repo_paths import attribute_probes, audit_paths, main, tracked_paths, utf16_units


class PathBudgetTests(unittest.TestCase):
    def test_reported_windows_failure(self):
        path = (
            "v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/"
            "forecast_action_price_review_v1/readable_figure_review_v1/source_and_data/"
            "v3/work_logs/P3_10_2026-10-11_S1/forecast_action_price_figure_A1_v2/"
            "forecast_action_price_regions.png"
        )
        audit = audit_paths([path], checkout_root=r"C:\Users\trist\projects\value_logic")
        issue = next(item for item in audit.issues if item.path == path)
        self.assertEqual(issue.relative_units, 243)
        self.assertEqual(issue.full_units, 279)
        self.assertTrue(issue.relative_overflow)
        self.assertTrue(issue.full_overflow)

    def test_attribute_probe_can_overflow_when_file_fits(self):
        directory = "d" * (201 - len("/.gitattributes"))
        path = directory + "/x"
        self.assertLessEqual(len(path), 200)
        audit = audit_paths([path])
        self.assertEqual(len(audit.issues), 1)
        self.assertEqual(audit.issues[0].kind, "attributes probe")
        self.assertEqual(audit.issues[0].relative_units, 201)

    def test_both_limit_equalities_pass(self):
        path = "f" * 200
        root = "C:\\" + "r" * 55
        audit = audit_paths([path], checkout_root=root)
        self.assertEqual(audit.max_relative_units, 200)
        self.assertEqual(audit.max_full_units, 259)
        self.assertEqual(audit.issues, ())

    def test_full_path_can_fail_while_relative_path_fits(self):
        audit = audit_paths(["f" * 200], checkout_root="C:\\" + "r" * 56)
        self.assertEqual(len(audit.issues), 1)
        self.assertFalse(audit.issues[0].relative_overflow)
        self.assertTrue(audit.issues[0].full_overflow)
        self.assertEqual(audit.issues[0].full_units, 260)

    def test_astral_unicode_uses_two_utf16_units(self):
        self.assertEqual(utf16_units("a\U0001F680b"), 4)
        self.assertEqual(audit_paths(["\U0001F680" * 100]).issues, ())
        issue = audit_paths(["\U0001F680" * 101]).issues[0]
        self.assertEqual(issue.relative_units, 202)

    def test_all_ancestor_probes_are_included(self):
        self.assertEqual(attribute_probes(["a/b/c.txt"]),
                         {".gitattributes", "a/.gitattributes", "a/b/.gitattributes"})


@unittest.skipUnless(shutil.which("git"), "Git is required for the index/ref integration check")
class GitPathSelectionTests(unittest.TestCase):
    def test_index_ref_and_untracked_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)

            def git(*args):
                return subprocess.check_output(["git", "-C", directory, *args],
                                               stderr=subprocess.PIPE).decode().strip()

            git("init", "-q")
            (repo / "tracked.txt").write_text("content\n", encoding="utf-8")
            git("add", "tracked.txt")
            tree = git("write-tree")
            blob = git("rev-parse", ":tracked.txt")
            # Index-only insertion also runs on Windows without creating a long file.
            long_path = "n" * 201
            git("update-index", "--add", "--cacheinfo", "100644", blob, long_path)
            (repo / "untracked.txt").write_text("untracked\n", encoding="utf-8")

            self.assertEqual(tracked_paths(repo, tree), ["tracked.txt"])
            self.assertEqual(set(tracked_paths(repo)), {"tracked.txt", long_path})
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["--repo", directory, "--ref", tree]), 0)
                self.assertEqual(main(["--repo", directory]), 1)


if __name__ == "__main__":
    unittest.main()
