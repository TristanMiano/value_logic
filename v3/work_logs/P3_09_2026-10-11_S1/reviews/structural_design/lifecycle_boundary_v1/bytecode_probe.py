"""Explicit DEVELOPMENT bytecode/source toy; no experiment imports or cases.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11. Zero research-clock credit.
The retained output directory is single-use and never overwritten.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import py_compile
import subprocess
import sys
import traceback


HERE = Path(__file__).resolve().parent
OUT = HERE / "bytecode_probe_run"
PREFIX = "/dev/null/value_logic_p309"


def written(path, data):
    with path.open("xb") as stream:
        stream.write(data)


def record(path):
    data = path.read_bytes()
    return {"path": path.relative_to(HERE).as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def main():
    OUT.mkdir(exist_ok=False)
    result = {"schema": "value_logic.p309.development_bytecode_probe.v1",
              "stage": "DEVELOPMENT", "principal_credit_seconds": 0,
              "final_population_generated": False, "experiment_modules_imported": False,
              "interpreter": {"path": sys.executable, "version": sys.version,
                              "sha256": hashlib.sha256(Path(sys.executable).resolve().read_bytes()).hexdigest()},
              "child_processes": []}
    try:
        module_root = OUT / "toy_module"
        module_root.mkdir()
        source = module_root / "_p309_cached_toy.py"
        cache_root = module_root / "__pycache__"
        cache_root.mkdir()
        cache = cache_root / ("_p309_cached_toy." + sys.implementation.cache_tag + ".pyc")
        old = b"VALUE = 17\n"
        new = b"VALUE = 99\n"
        assert len(old) == len(new)
        written(OUT / "original_source_17.py", old)
        written(OUT / "replacement_source_99.py", new)
        written(source, old)
        timestamp = 1700000000
        os.utime(source, (timestamp, timestamp))
        py_compile.compile(str(source), cfile=str(cache), doraise=True,
                           invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
        source.write_bytes(new)
        os.utime(source, (timestamp, timestamp))
        before = [record(source), record(cache)]
        child = (
            "import sys,json;sys.path.insert(0,sys.argv[1]);import _p309_cached_toy as toy;"
            "print(json.dumps({'value':toy.VALUE,'source_path':toy.__file__,"
            "'derived_cache_path':toy.__cached__,'cache_prefix':sys.pycache_prefix,"
            "'dont_write_bytecode':sys.flags.dont_write_bytecode,"
            "'ignore_environment':sys.flags.ignore_environment,'no_site':sys.flags.no_site,"
            "'xoptions':dict(sys._xoptions)},sort_keys=True))"
        )
        for label, extra in (("B_alone_reads_adjacent_cache", []),
                             ("required_prefix_compiles_source", ["-X", "pycache_prefix=" + PREFIX])):
            command = [sys.executable, "-E", "-S", "-B", *extra, "-c", child, str(module_root)]
            completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=20)
            written(OUT / (label + ".stdout.txt"), completed.stdout.encode())
            written(OUT / (label + ".stderr.txt"), completed.stderr.encode())
            row = {"label": label, "command": command, "returncode": completed.returncode}
            result["child_processes"].append(row)
            if completed.returncode != 0:
                raise AssertionError("Development child failed: " + label)
            row["observed"] = json.loads(completed.stdout)
        after = [record(source), record(cache)]
        result["before"] = before
        result["after"] = after
        result["unchanged_source_and_cache"] = before == after
        assert result["child_processes"][0]["observed"]["value"] == 17
        assert result["child_processes"][1]["observed"]["value"] == 99
        assert before == after
        assert result["child_processes"][0]["observed"]["source_path"] == str(source)
        assert result["child_processes"][1]["observed"]["source_path"] == str(source)
        result["status"] = "PASS"
    except BaseException as error:
        result["status"] = "FAIL"
        result["error_type"] = type(error).__name__
        result["error"] = str(error)
        result["traceback"] = traceback.format_exc()
        raise
    finally:
        result["probe_source"] = record(Path(__file__).resolve())
        written(OUT / "results.json", (json.dumps(result, sort_keys=True, indent=2) + "\n").encode())
    print(json.dumps({"status": result["status"], "results": str(OUT / "results.json"),
                      "values": [row["observed"]["value"] for row in result["child_processes"]],
                      "unchanged_source_and_cache": result["unchanged_source_and_cache"]}, sort_keys=True))


if __name__ == "__main__":
    main()
