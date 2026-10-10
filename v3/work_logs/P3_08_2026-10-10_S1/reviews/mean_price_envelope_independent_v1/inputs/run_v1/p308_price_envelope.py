"""Exact fixed-transcript price envelopes. DEVELOPMENT, no policy runs.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
Native acquisition parameters are held fixed during this external repricing.
Every candidate line has its identical ordinary-kernel interpretation.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

COMMON_SOURCE = 50115


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pair(value): return None if value is None else [value.numerator, value.denominator]


def verified_scores(path):
    path = Path(path).resolve()
    public = json.loads((path / "public_seal.json").read_text())
    private = json.loads((path / "private/seal.json").read_text())
    for row in public["files"]:
        assert sha(path / row["path"]) == row["sha256"]
    for row in private["files"]:
        assert sha(path / "private" / row["path"]) == row["sha256"]
    return json.loads((path / "private/scores.json").read_text())


def analyze(common, reuse, out):
    common, reuse, out = Path(common).resolve(), Path(reuse).resolve(), Path(out).resolve()
    assert not out.exists()
    primary, extension = verified_scores(common), verified_scores(reuse)
    lines = []
    for source_name, data in (("common_v2", primary), ("reuse_v1_1", extension)):
        for row in data["runs"]:
            cfg = row["configuration"]
            assert row["status"] == "success"
            scenario = row.get("scenario", cfg.get("scenario"))
            is_broker = source_name == "reuse_v1_1" or cfg["kind"] == "broker"
            deterministic = source_name == "common_v2" and not is_broker and cfg["method"] not in ("probability_cost", "ordinary_combo", "ordinary_combo_hashed")
            actual_source = row["source_units"]
            assert actual_source == (48274 if source_name == "common_v2" else COMMON_SOURCE)
            lines.append({"record": source_name+"/"+row["run_id"],
                "scenario": scenario, "seed": cfg["seed"],
                "configuration": cfg, "deterministic_across_seeds": deterministic,
                "terminal_errors": row["terminal_errors"],
                "local_units": row["local_units"],
                "cold_units_current_common_bundle": row["local_units"]+COMMON_SOURCE,
                "source_procurement_transfer": COMMON_SOURCE-actual_source,
                "recorded_acquisition_price": cfg.get("unit_price"),
                "ordinary_kernel_equivalent": is_broker,
                "ordinary_control": not is_broker})
    # Verify that the scientific source transfer really only adds the adapter.
    before = {r["path"]: r["sha256"] for r in json.loads((common / "source_before.json").read_text())["sources"]}
    after = {r["path"]: r["sha256"] for r in json.loads((reuse / "source_before.json").read_text())["sources"]}
    assert all(after.get(name) == digest for name, digest in before.items())
    envelopes = []
    for scenario in ("cold_mixed", "repeat_online", "cheap_structure"):
        for seed in (11, 29, 47):
            group = [r for r in lines if r["scenario"] == scenario and (r["seed"] == seed or r["deterministic_across_seeds"])]
            frontier = []
            for candidate in group:
                e, c = candidate["terminal_errors"], candidate["cold_units_current_common_bundle"]
                low, high, impossible = F(0), None, False
                for other in group:
                    de = e-other["terminal_errors"]
                    dc = other["cold_units_current_common_bundle"]-c
                    if dc > 0:
                        low = max(low, F(de, dc))
                    elif dc < 0:
                        bound = F(de, dc)
                        high = bound if high is None else min(high, bound)
                    elif de > 0:
                        impossible = True
                if impossible or (high is not None and low > high):
                    continue
                witness = low+1 if high is None else (low+high)/2
                objective = e+witness*c
                assert all(objective <= r["terminal_errors"]+witness*r["cold_units_current_common_bundle"] for r in group)
                ties = [r["record"] for r in group if r["terminal_errors"] == e and r["cold_units_current_common_bundle"] == c]
                frontier.append({"record": candidate["record"],
                    "lambda_min": pair(low), "lambda_max": pair(high),
                    "positive_width": high is None or low < high,
                    "rational_witness": pair(witness), "witness_objective": pair(objective),
                    "terminal_errors": e, "cold_units": c,
                    "coincident_record_lines": ties,
                    "has_identical_ordinary_kernel": candidate["ordinary_kernel_equivalent"],
                    "ordinary_control": candidate["ordinary_control"]})
            # The best existing line at a displayed intermediate price is an
            # explicit hindsight query, not a new native-controller run.
            display_price = F(1, 30000)
            best = min(r["terminal_errors"]+display_price*r["cold_units_current_common_bundle"] for r in group)
            winners = [r["record"] for r in group if r["terminal_errors"]+display_price*r["cold_units_current_common_bundle"] == best]
            envelopes.append({"scenario": scenario, "seed": seed, "line_count": len(group),
                "frontier": sorted(frontier, key=lambda r: (F(*r["lambda_min"]), r["record"])),
                "display_price": pair(display_price), "display_objective": pair(best),
                "display_winners": winners,
                "native_controller_at_display_price_was_not_executed": True})
    result = {"stage": "DEVELOPMENT", "kind": "exact fixed-transcript repricing",
        "common_source_units": COMMON_SOURCE, "policy_runs_added": 0,
        "hindsight_envelope_is_deployable_selector": False,
        "ordinary_kernel_equivalence_retained": True,
        "all_existing_common_source_hashes_unchanged": True,
        "common_scores_sha256": sha(common / "private/scores.json"),
        "reuse_scores_sha256": sha(reuse / "private/scores.json"),
        "lines": lines, "envelopes": envelopes}
    out.mkdir(parents=True)
    (out / "results.json").write_text(json.dumps(result, indent=2)+"\n")
    (out / Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    (out / "manifest.json").write_text(json.dumps({"stage": "DEVELOPMENT", "files": [
        {"path": p.name, "bytes": p.stat().st_size, "sha256": sha(p)} for p in sorted(out.iterdir())]}, indent=2)+"\n")
    return {"stage": "DEVELOPMENT", "records": len(lines), "envelopes": len(envelopes),
            "display": [{k: r[k] for k in ("scenario", "seed", "display_price", "display_winners")} for r in envelopes]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--common", required=True)
    parser.add_argument("--reuse", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(json.dumps(analyze(args.common, args.reuse, args.out), sort_keys=True))
