"""Balanced fixed-policy averages over recorded seeds. DEVELOPMENT only.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
No policy execution, expectation estimate, or new deployment price run.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pair(x): return None if x is None else [x.numerator, x.denominator]


def run(input_dir, out):
    input_dir, out = Path(input_dir).resolve(), Path(out).resolve()
    assert not out.exists()
    manifest = json.loads((input_dir / "manifest.json").read_text())
    for r in manifest["files"]:
        assert sha(input_dir / r["path"]) == r["sha256"]
    source = json.loads((input_dir / "results.json").read_text())
    partitions = defaultdict(list)
    for r in source["lines"]:
        cfg = {k: v for k, v in r["configuration"].items() if k != "seed"}
        key = (r["scenario"], r["record"].split("/", 1)[0], json.dumps(cfg, sort_keys=True))
        partitions[key].append(r)
    omitted, means, seed_lines = [], [], defaultdict(list)
    for (scenario, family, encoded), rows in sorted(partitions.items()):
        cfg = json.loads(encoded)
        key = family + "/" + encoded
        if all(r["deterministic_across_seeds"] for r in rows):
            assert len(rows) == 1 and rows[0]["seed"] == 11
            expanded = {seed: rows[0] for seed in (11, 29, 47)}
            deterministic = True
        elif sorted(r["seed"] for r in rows) == [11, 29, 47]:
            expanded = {r["seed"]: r for r in rows}
            deterministic = False
        else:
            omitted.append({"scenario": scenario, "configuration": cfg, "family": family,
                            "seeds": sorted(r["seed"] for r in rows),
                            "reason": "No complete three-seed stochastic configuration; no imputation."})
            continue
        assert len({r["ordinary_kernel_equivalent"] for r in rows}) == 1
        assert len({r["ordinary_control"] for r in rows}) == 1
        e = sum(F(r["terminal_errors"]) for r in expanded.values()) / 3
        c = sum(F(r["cold_units_current_common_bundle"]) for r in expanded.values()) / 3
        assert all(r["cold_units_current_common_bundle"] - r["local_units"] == 50115 for r in rows)
        means.append({"key": key, "scenario": scenario, "family": family, "configuration": cfg,
                      "records": [r["record"] for r in rows], "deterministic_reuse": deterministic,
                      "mean_errors": pair(e), "mean_cold_units": pair(c),
                      "ordinary_control": rows[0]["ordinary_control"],
                      "ordinary_kernel_equivalent": rows[0]["ordinary_kernel_equivalent"]})
        for seed, r in expanded.items():
            seed_lines[(scenario, seed)].append((key, F(r["terminal_errors"]), F(r["cold_units_current_common_bundle"])))
    scenarios = []
    for scenario in ("cold_mixed", "repeat_online", "cheap_structure"):
        group = [r for r in means if r["scenario"] == scenario]
        frontier = []
        for r in group:
            e, c = F(*r["mean_errors"]), F(*r["mean_cold_units"])
            lo, hi, feasible = F(0), None, True
            for s in group:
                # (c-c_s)*lambda <= e_s-e, independently of seed.
                a, b = c-F(*s["mean_cold_units"]), F(*s["mean_errors"])-e
                if a > 0:
                    hi = b/a if hi is None else min(hi, b/a)
                elif a < 0:
                    lo = max(lo, b/a)
                elif b < 0:
                    feasible = False
            if not feasible or (hi is not None and lo > hi):
                continue
            witness = lo+1 if hi is None else (lo+hi)/2
            assert all(e+witness*c <= F(*s["mean_errors"])+witness*F(*s["mean_cold_units"]) for s in group)
            frontier.append({"key": r["key"], "lambda_min": pair(lo), "lambda_max": pair(hi),
                             "positive_width": hi is None or lo < hi,
                             "mean_errors": pair(e), "mean_cold_units": pair(c),
                             "ordinary_control": r["ordinary_control"],
                             "ordinary_kernel_equivalent": r["ordinary_kernel_equivalent"]})
        price = F(1, 30000)
        best_mean = min(F(*r["mean_errors"])+price*F(*r["mean_cold_units"]) for r in group)
        fixed_winners = [r["key"] for r in group if F(*r["mean_errors"])+price*F(*r["mean_cold_units"]) == best_mean]
        seed_bests = [min(e+price*c for _, e, c in seed_lines[(scenario, seed)]) for seed in (11, 29, 47)]
        adaptive_mean = sum(seed_bests)/3
        assert adaptive_mean <= best_mean
        assert all(len(seed_lines[(scenario, seed)]) == len(group) for seed in (11, 29, 47))
        scenarios.append({"scenario": scenario, "configuration_count": len(group),
                          "frontier": sorted(frontier, key=lambda r: (F(*r["lambda_min"]), r["key"])),
                          "price": pair(price), "fixed_configuration_minimum_mean": pair(best_mean),
                          "fixed_winners": fixed_winners, "per_seed_minima": list(map(pair, seed_bests)),
                          "mean_per_seed_minimum": pair(adaptive_mean),
                          "hindsight_configuration_selection_gap": pair(best_mean-adaptive_mean)})
    result = {"stage": "DEVELOPMENT", "source_sha256": sha(input_dir / "results.json"),
              "source_records": len(source["lines"]), "new_policy_runs": 0,
              "fair_bit_expectation_or_population_claim": False,
              "seedwise_selector_is_deployable": False,
              "configuration_count": len(means), "omitted_incomplete_groups": omitted,
              "mean_lines": means, "scenarios": scenarios}
    out.mkdir(parents=True)
    (out / "results.json").write_text(json.dumps(result, indent=2)+"\n")
    (out / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    (out / "manifest.json").write_text(json.dumps({"stage": "DEVELOPMENT", "files": [
        {"path": p.name, "bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted(out.iterdir())]}, indent=2)+"\n")
    return {"configurations": len(means), "omitted_groups": len(omitted), "scenarios": [
        {"scenario": s["scenario"], "positive_frontier": [r for r in s["frontier"] if r["positive_width"]],
         "hindsight_gap": s["hindsight_configuration_selection_gap"]} for s in scenarios]}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    print(json.dumps(run(args.input, args.out), indent=2))
