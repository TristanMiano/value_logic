"""Focused proof_solver amendment check. DEVELOPMENT; no cohort comparison."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "v3/experiments"))
import p308_cnf as S
import p308_ordinary as O


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise RuntimeError("Retain prior evidence; use a new output directory.")
    args.out.mkdir(parents=True)
    paths = [REPO / "v3/experiments" / name for name in (
        "p308_ordinary.py", "p308_cnf.py", "p308_common.py", "p308_broker.py")]
    paths += [REPO / "v3/checks/07_selective_feedback.py", Path(__file__).resolve(),
              Path(__file__).with_name("proof_solver_input_plan.json")]
    hashes = {str(p.relative_to(REPO)): sha(p) for p in paths}
    dump(args.out / "started.json", {
        "stage": "DEVELOPMENT", "sources": hashes, "argv": sys.argv,
        "python": sys.version, "wall_start_ns": time.time_ns(),
        "principal_clock_credit_ns": 0,
        "scope": "Only the prospective two-formula proof-solver amendment check."
    })
    tape = (
        S.make_query("proof-sat", 3, ((1,), (-2,), (3,))),
        S.make_query("proof-unsat", 3, ((1,), (-1,))),
    )
    dump(args.out / "public_tape.json", [q.record() for q in tape])
    runs, checks = {}, []
    for solver in ("enumeration", "dpll"):
        cap = max(S.service_cap(q, solver) for q in tape)
        successful = O.run_method(tape, "proof_only", proof_cap=cap,
                                  proof_solver=solver, fallback_action=0)
        runs[solver + "_full_public_cap"] = successful
        assert successful["status"] == "success"
        assert successful["configuration"]["proof_solver"] == solver
        assert successful["successful_purchases"] == 2
        assert [r["terminal_action"] for r in successful["trace"]] == [1, 0]
        assert [r["hard_after"]["status"] for r in successful["trace"]] == ["checked"] * 2
        assert successful["meter"]["reservations"] == {}
        assert successful["common_source_setup_included"] is False
        for query, invoice in zip(tape, successful["invoices"]):
            requested = min(cap, S.service_cap(query, solver))
            direct = S.checked_purchase(query, limit_total=requested, solver=solver)
            assert invoice["solver"] == solver
            assert invoice["purpose"] == "bounded_proof"
            assert invoice["requested_cap"] == requested
            assert invoice == {"index": tape.index(query), "purpose": "bounded_proof",
                               "requested_cap": requested, "solver": solver,
                               **direct.record()}
        checks.append({"name": "checked_" + solver + "_through_existing_purchase_path",
                       "answers": [1, 0],
                       "provider_units": [r["resources"]["total"]
                                          for r in successful["invoices"]]})
        if solver == "enumeration":
            default = O.run_method(tape, "proof_only", proof_cap=cap, fallback_action=0)
            runs["default_enumeration"] = default
            assert default == successful
            checks.append({"name": "default_equals_explicit_enumeration"})

        for clamp in ("proof_cap", "provider_limit"):
            kwargs = {"proof_cap": 64 if clamp == "proof_cap" else cap,
                      "provider_limit": 64 if clamp == "provider_limit" else None}
            failed = O.run_method(tape, "proof_only", proof_solver=solver,
                                  fallback_action=1, **kwargs)
            runs[solver + "_failed_" + clamp] = failed
            assert failed["status"] == "success"  # Episode closes with unresolved outputs.
            assert failed["purchases"] == failed["provider_failures"] == 2
            assert failed["successful_purchases"] == failed["known_terminal_rounds"] == 0
            assert failed["meter"]["reservations"] == {}
            for row in failed["trace"]:
                assert row["terminal_action"] == 1
                assert row["hard_after"] == {"status": "unresolved", "answer": None,
                                               "interval": [0, 1]}
            for invoice in failed["invoices"]:
                assert invoice["requested_cap"] == 64 and invoice["solver"] == solver
                assert invoice["status"] == "budget_exhausted"
                assert invoice["answer"] is None and invoice["checked"] is False
                assert 0 < invoice["resources"]["total"] <= 64
            absorbed = sum(op["units"] for op in failed["meter"]["operations"]
                           if op["operation"].startswith("ordinary_provider:"))
            assert absorbed == sum(i["resources"]["total"] for i in failed["invoices"])
            checks.append({"name": solver + "_failed_" + clamp + "_retains_fallback_and_cost",
                           "provider_units": absorbed})

    for invalid in ("oracle", 0):
        rejected = O.run_method(tape, "proof_only", proof_solver=invalid)
        runs["invalid_" + str(invalid)] = rejected
        assert rejected["status"] == "failed" and rejected["purchases"] == 0
        assert "Proof solver" in rejected["failure_detail"]
    checks.append({"name": "bounded_solver_option_rejection", "cases": 2})
    assert hashes == {str(p.relative_to(REPO)): sha(p) for p in paths}
    dump(args.out / "runs.json", runs)
    result = {"stage": "DEVELOPMENT", "status": "PASS", "sources": hashes,
              "checks": checks, "principal_clock_credit_ns": 0,
              "version": O.VERSION, "wall_end_ns": time.time_ns()}
    dump(args.out / "result.json", result)
    print(json.dumps({"status": "PASS", "checks": len(checks), "sources": hashes}, sort_keys=True))


if __name__ == "__main__":
    main()
