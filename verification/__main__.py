"""Run all semantic and repository integrity checks with one command."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


def main() -> int:
    directory = Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(str(directory), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
