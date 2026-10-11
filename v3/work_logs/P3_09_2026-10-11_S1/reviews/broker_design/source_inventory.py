"""Read-only P3-09 current-source inventory; never imports research modules.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11. PREPARATION observer.
Writes only its explicitly supplied new output path. No queries/randomness,
providers, private truth, preparation of final cases or policy executions.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys


ENTRY = "f2a240b87d4df07ac91874b092db20b8c4378889"
CORE = (
    "v3/experiments/p308_common.py",
    "v3/experiments/p308_cnf.py",
    "v3/experiments/p308_hashcache.py",
    "v3/experiments/p308_broker.py",
    "v3/experiments/p308_ordinary.py",
    "v3/experiments/p308_mirrors.py",
    "v3/experiments/p308_cached_service.py",
    "v3/checks/07_selective_feedback.py",
    "v3/checks/07_selective_feedback_service.py",
    "v3/checks/07_computation_adapter.py",
)
OPTIONAL_REPORT = ("v3/experiments/p308_reporting.py",)
OBSERVERS = (
    "v3/experiments/p308_run.py",
    "v3/experiments/p308_reuse_run.py",
    "v3/experiments/p308_analyze.py",
    "v3/experiments/p308_reuse_analyze.py",
    "v3/experiments/p308_forecast_benchmarks.py",
    "v3/experiments/p308_price_envelope.py",
    "v3/experiments/p308_mean_price_envelope.py",
    "v3/experiments/p308_report_replay.py",
)
CONTEXT = (
    "v3/RESEARCH_PROTOCOL.md",
    "v3/STYLE.md",
    "v3/foundations/01_problem_contract.md",
    "v3/experiments/development.md",
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inspect_source(root, relative):
    data = (root / relative).read_bytes()
    prior = subprocess.check_output(
        ["git", "show", ENTRY + ":" + relative], cwd=root)
    row = {"path": relative, "bytes": len(data), "sha256": sha(data),
           "entry_bytes_identical": data == prior}
    if relative.endswith(".py"):
        text = data.decode("utf-8")
        tree = ast.parse(text, filename=relative)
        row["imports"] = [ast.unparse(node) for node in tree.body
                          if isinstance(node, (ast.Import, ast.ImportFrom))]
        row["definitions"] = [
            {"kind": type(node).__name__, "name": node.name,
             "line": node.lineno,
             "arguments": ast.unparse(node.args)
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             else None}
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef))]
        row["top_level_non_definition_statements"] = [
            {"kind": type(node).__name__, "line": node.lineno,
             "source": ast.get_source_segment(text, node)}
            for node in tree.body
            if not isinstance(node, (ast.Import, ast.ImportFrom,
                                     ast.FunctionDef, ast.AsyncFunctionDef,
                                     ast.ClassDef))
            and not (isinstance(node, ast.Expr)
                     and isinstance(node.value, ast.Constant)
                     and isinstance(node.value.value, str))]
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    root, out = Path(args.repo).resolve(), Path(args.out).resolve()
    if out.exists():
        raise FileExistsError("Preserve an existing source inventory.")
    rows = [inspect_source(root, path)
            for path in CORE + OPTIONAL_REPORT + OBSERVERS + CONTEXT]
    by_path = {row["path"]: row for row in rows}

    def tariff(paths):
        sizes = [by_path[path]["bytes"] for path in paths]
        words = sum(max(1, (size + 7) // 8) for size in sizes)
        blocks = sum((size + 72) // 64 for size in sizes)
        return {"files": len(sizes), "bytes": sum(sizes),
                "source_word_read": words, "installed_source_word": words,
                "source_sha256_block": blocks, "total": 2 * words + blocks,
                "derivation": "Static arithmetic matching p308_common.registry_setup; no procurement or import executed."}

    # Arithmetic envelope only: semantics is the fixed admitted label and the
    # source label may have128 ASCII characters. No research object is created.
    n, clauses, literals = 12, 64, 256
    key_words = 4 + (len("bounded-cnf-sat-v1") + 7) // 8 + 16 + clauses + literals
    admission = 4096 + 16 * key_words
    enumeration = (1 << n) * (16 * literals + 8 * clauses + 8 * n + 64)
    dpll = (admission + enumeration + ((1 << (n + 1)) - 1) * (n + 1)
            * (24 * literals + 24 * clauses + 128))
    result = {
        "schema": "value_logic.p309.broker_source_inventory.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "stage": "PREPARATION", "observer_only": True,
        "entry": ENTRY, "policy_imports": 0, "policy_executions": 0,
        "query_constructions": 0, "final_population_generation": False,
        "random_bits_generated": 0, "private_truth_computations": 0,
        "principal_clock_credit": 0,
        "python": sys.version, "implementation": platform.python_implementation(),
        "platform": platform.platform(), "byteorder": sys.byteorder,
        "core_paths": CORE, "optional_report_paths": OPTIONAL_REPORT,
        "observer_paths": OBSERVERS, "context_paths": CONTEXT,
        "core_tariff": tariff(CORE),
        "report_tariff": tariff(OPTIONAL_REPORT),
        "envelope_arithmetic": {"variables": n, "clauses": clauses,
            "literals": literals, "maximum_key_words": key_words,
            "enumeration_provider_cap": admission + 2 * enumeration,
            "dpll_provider_cap": dpll,
            "selected_cache_provider_cap": dpll + 131072,
            "candidate_episode_primary_suggested_horizon": 128,
            "proposed_common_local_budget": 1 << 38,
            "optional_report_funding_cap": 1 << 48,
            "this_is_a_static_bound_not_observed_execution": True},
        "all_entry_sources_identical": all(row["entry_bytes_identical"] for row in rows),
        "sources": rows,
        "inventory_program_sha256": sha(Path(__file__).read_bytes()),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"out": str(out), "source_count": len(rows),
        "core_tariff": result["core_tariff"],
        "report_tariff": result["report_tariff"],
        "envelope_arithmetic": result["envelope_arithmetic"],
        "all_entry_sources_identical": result["all_entry_sources_identical"],
        "sha256": sha(out.read_bytes())}, sort_keys=True))


if __name__ == "__main__":
    main()
