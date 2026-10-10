"""Sealed-record forecast diagnostics; no policy execution. DEVELOPMENT.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
See the accompanying analysis contract for hindsight and information limits.
"""
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

EXPERTS = ("constant_unsat", "constant_sat", "sparse_sat",
           "unit_consistency_sat", "pure_coverage_sat", "literal_balance_sat")


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pair(value): return [value.numerator, value.denominator]


def run(directory, out):
    directory, out = Path(directory).resolve(), Path(out).resolve()
    assert not out.exists()
    seal = json.loads((directory / "public_seal.json").read_text())
    for entry in seal["files"]:
        assert sha(directory / entry["path"]) == entry["sha256"]
    private_seal = json.loads((directory / "private/seal.json").read_text())
    for entry in private_seal["files"]:
        assert sha(directory / "private" / entry["path"]) == entry["sha256"]
    truth_record = json.loads((directory / "private/truth.json").read_text())
    assert truth_record["public_seal_sha256"] == sha(directory / "public_seal.json")
    index = {r["run_id"]: r for r in
             json.loads((directory / "public_index.json").read_text())["records"]}
    results = []
    with gzip.open(directory / "public_records.jsonl.gz", "rt") as stream:
        for line in stream:
            record = json.loads(line)
            assert hashlib.sha256(line.rstrip("\n").encode()).hexdigest() == index[record["run_id"]]["record_sha256"]
            if record["configuration"]["kind"] != "broker":
                continue
            episode = record["episode"]
            truth = truth_record["answers"][record["scenario"]]
            trace = episode["trace"]
            assert episode["status"] == "success" and len(trace) == len(truth)
            base = live = F(0)
            static_exact = static_dyadic = matched_static_exact = matched_static_dyadic = F(0)
            expert_losses, matched_expert_losses = [0]*6, [0]*6
            hard_count = 0
            for i, (row, y) in enumerate(zip(trace, truth)):
                assert row["index"] == i and type(y) is int and y in (0, 1)
                q, q_live = F(*row["base_q"]), F(*row["emitted_q"])
                base += (q-y)**2
                live += (q_live-y)**2
                hard = row["hard_before"] == "checked"
                if hard:
                    assert q_live == y
                    hard_count += 1
                else:
                    assert q_live == q
                assert len(row["advice"]) == 6
                for j, advice in enumerate(row["advice"]):
                    assert type(advice) is int and advice in (0, 1)
                    loss = (advice-y)**2
                    expert_losses[j] += loss
                    if not hard:
                        matched_expert_losses[j] += loss
                average = F(sum(row["advice"]), len(row["advice"]))
                denominator = row["base_q"][1]
                dyadic = F((average.numerator*denominator)//average.denominator, denominator)
                static_exact += (average-y)**2
                static_dyadic += (dyadic-y)**2
                if not hard:
                    matched_static_exact += (average-y)**2
                    matched_static_dyadic += (dyadic-y)**2
            half = F(len(truth), 4)
            matched_half = F(len(truth)-hard_count, 4)
            best, matched_best = min(expert_losses), min(matched_expert_losses)
            results.append({
                "run_id": record["run_id"], "scenario": record["scenario"],
                "configuration": record["configuration"], "horizon": len(truth),
                "current_hard_before_issue": hard_count,
                "base_brier": pair(base), "live_brier": pair(live),
                "constant_half_brier": pair(half),
                "matched_hard_half_brier": pair(matched_half),
                "fixed_expert_brier": dict(zip(EXPERTS, expert_losses)),
                "matched_hard_expert_brier": dict(zip(EXPERTS, matched_expert_losses)),
                "hindsight_best_expert_brier": best,
                "matched_hindsight_best_expert_brier": matched_best,
                "base_minus_half": pair(base-half),
                "base_minus_best_fixed_expert": pair(base-best),
                "live_minus_matched_half": pair(live-matched_half),
                "live_minus_matched_best_expert": pair(live-matched_best),
                "static_equal_exact_brier": pair(static_exact),
                "static_equal_dyadic_brier": pair(static_dyadic),
                "matched_static_equal_exact_brier": pair(matched_static_exact),
                "matched_static_equal_dyadic_brier": pair(matched_static_dyadic),
                "base_minus_static_equal_exact": pair(base-static_exact),
                "base_minus_static_equal_dyadic": pair(base-static_dyadic),
                "live_minus_matched_static_equal_exact": pair(live-matched_static_exact),
                "live_minus_matched_static_equal_dyadic": pair(live-matched_static_dyadic),
                "free_perfect_foresight_brier": [0, 1],
                "free_oracle_is_deployable_control": False,
            })
    assert len(results) == 63
    summary = {}
    for field in ("base_minus_half", "base_minus_best_fixed_expert",
                  "live_minus_matched_half", "live_minus_matched_best_expert",
                  "base_minus_static_equal_exact", "base_minus_static_equal_dyadic",
                  "live_minus_matched_static_equal_exact", "live_minus_matched_static_equal_dyadic"):
        values = [F(*row[field]) for row in results]
        summary[field] = {"strictly_better": sum(v < 0 for v in values),
                          "equal": sum(v == 0 for v in values),
                          "strictly_worse": sum(v > 0 for v in values)}
    out.mkdir(parents=True)
    result = {"stage": "DEVELOPMENT", "version": "forecast-benchmarks-v2", "record_count": len(results),
              "policy_runs_added": 0, "records_are_not_independent_trials": True,
              "new_paid_benchmark_deployments": 0,
              "public_seal_sha256": sha(directory / "public_seal.json"),
              "private_seal_sha256": sha(directory / "private/seal.json"),
              "private_truth_sha256": sha(directory / "private/truth.json"),
              "summary": summary, "records": results}
    (out / "results.json").write_text(json.dumps(result, indent=2)+"\n")
    (out / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    manifest = {"stage": "DEVELOPMENT", "files": [
        {"path": p.name, "bytes": p.stat().st_size, "sha256": sha(p)}
        for p in sorted(out.iterdir())]}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    return {"stage": "DEVELOPMENT", "count": len(results), "summary": summary}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.run, args.out), sort_keys=True))
