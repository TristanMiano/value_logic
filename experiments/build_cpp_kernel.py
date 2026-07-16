"""Build the small data-oriented C++ decoder used by the repaired runner.

The compiled library is a disposable local artifact under ``.cache``.  The
repository stores and hashes the C++ source, not a machine-specific binary.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
import shutil
import subprocess
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = ROOT / "experiments" / "cpp"
BUILD_DIRECTORY = ROOT / ".cache" / "value_logic_cpp_v1_1"
DEBUG_BUILD_DIRECTORY = ROOT / ".cache" / "value_logic_cpp_v1_1_debug"
BUILD_MARKER = BUILD_DIRECTORY / "build_record.json"


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def source_sha256() -> str:
    digest = sha256()
    for path in sorted(SOURCE_DIRECTORY.glob("*")):
        if path.is_file():
            digest.update(path.name.encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _library_candidates() -> tuple[Path, ...]:
    names = (
        "value_logic_kernel.dll",
        "libvalue_logic_kernel.so",
        "libvalue_logic_kernel.dylib",
    )
    return tuple(
        path
        for name in names
        for path in BUILD_DIRECTORY.rglob(name)
        if path.is_file()
    )


def library_path() -> Path:
    candidates = _library_candidates()
    if not candidates:
        raise FileNotFoundError(
            "the C++ value-logic kernel is not built; run "
            "`python -m experiments.build_cpp_kernel`"
        )
    return max(candidates, key=lambda path: path.stat().st_mtime_ns)


def _read_marker() -> Mapping[str, Any] | None:
    if not BUILD_MARKER.exists():
        return None
    return json.loads(BUILD_MARKER.read_text(encoding="utf-8"))


def _configure_build(
    cmake: str,
    directory: Path,
    configuration: str,
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    configure: list[str] = [
        cmake,
        "-S",
        str(SOURCE_DIRECTORY),
        "-B",
        str(directory),
        f"-DCMAKE_BUILD_TYPE={configuration}",
    ]
    if platform.system() == "Windows":
        configure.extend(("-A", "x64"))
    subprocess.run(configure, check=True)
    subprocess.run(
        [cmake, "--build", str(directory), "--config", configuration],
        check=True,
    )
    subprocess.run(
        [
            "ctest",
            "--test-dir",
            str(directory),
            "-C",
            configuration,
            "--output-on-failure",
        ],
        check=True,
    )


def build_cpp_kernel(
    *,
    force: bool = False,
    verify_debug: bool = False,
) -> Mapping[str, Any]:
    cmake = shutil.which("cmake")
    if cmake is None:
        raise RuntimeError("CMake is required to build the C++ value-logic kernel")
    source_hash = source_sha256()
    marker = _read_marker()
    if (
        not force
        and marker is not None
        and marker.get("source_sha256") == source_hash
        and (not verify_debug or marker.get("debug_self_test") == "pass")
    ):
        try:
            library = library_path()
        except FileNotFoundError:
            pass
        else:
            if marker.get("library_sha256") == _sha256(library):
                return marker

    _configure_build(cmake, BUILD_DIRECTORY, "Release")
    library = library_path()
    debug_self_test = "not_requested"
    if verify_debug:
        _configure_build(cmake, DEBUG_BUILD_DIRECTORY, "Debug")
        debug_self_test = "pass"
    cmake_version = subprocess.run(
        [cmake, "--version"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()[0]
    record = {
        "status": "pass",
        "interface": "vl_decode_block_v1",
        "source_sha256": source_hash,
        "library_path": str(library),
        "library_sha256": _sha256(library),
        "cmake": cmake_version,
        "platform": platform.platform(),
        "build_type": "Release",
        "release_self_test": "pass",
        "debug_self_test": debug_self_test,
    }
    BUILD_MARKER.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return record


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="discard the source-hash cache")
    parser.add_argument(
        "--verify-debug",
        action="store_true",
        help="also compile and run the native self-test without optimization",
    )
    args = parser.parse_args(argv)
    print(
        json.dumps(
            build_cpp_kernel(force=args.force, verify_debug=args.verify_debug),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
