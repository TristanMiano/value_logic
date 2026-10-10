"""Exact DEVELOPMENT witness for budget-conditioned confidence failure.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
This enumerates a toy fee contract, not the CNF tariff or a deployed method.
"""
from datetime import datetime, timezone
from fractions import Fraction
import argparse
import hashlib
import json
from math import comb
from pathlib import Path

VERSION = "p308-budget-selection-witness-v1"


def run(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve()
    captured = out / source.name
    captured.write_bytes(source.read_bytes())
    plan = {
        "stage": "DEVELOPMENT", "version": VERSION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "blocks": 16, "answers_per_block": [0, 1], "forecasts": [1, 1],
        "provider_fee_by_position": [2, 1], "provider_budget": 17,
        "other_costs": "Separately prepaid; toy units are not CNF word units.",
        "selectors": "All 65536 independent-fair-bit paths enumerated once.",
        "post_selection_changes": False, "coverage_estimation": False,
    }
    (out / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    radius = Fraction(77, 6)
    totals = dict(paths=0, complete=0, unconditional_misses=0,
                  completed_misses=0, incomplete=0)
    strata = []
    for x in range(17):
        misses = abs(16 - 2*x) > radius
        strata.append({"selected_zeros": x, "paths": comb(16, x),
                       "would_be_provider_bill": 16+x,
                       "complete": x <= 1, "F": 16, "A_center": 2*x,
                       "V": 16-x, "U_center": x, "misses": misses})
    for bits in range(1 << 16):
        spent = 0
        completed = True
        x = f_total = a_center = v_total = u_center = 0
        for block in range(16):
            position = (bits >> block) & 1
            y_selected = position
            x += int(y_selected == 0)
            f_total += 1
            a_center += 2 * (1-y_selected)
            v_total += y_selected
            u_center += 1-y_selected
            fee = 2-position
            if completed:
                if spent + fee > 17:
                    completed = False
                else:
                    spent += fee
        assert f_total == 16 and a_center == 2*x
        assert v_total == 16-x and u_center == x
        assert f_total-a_center == v_total-u_center
        assert completed == (x <= 1)
        assert 0 <= spent <= 17
        if completed:
            assert spent == 16+x
        misses = abs(f_total-a_center) > radius
        totals["paths"] += 1
        totals["complete"] += int(completed)
        totals["incomplete"] += int(not completed)
        totals["unconditional_misses"] += int(misses)
        totals["completed_misses"] += int(completed and misses)
    assert totals == {"paths": 65536, "complete": 17,
                      "unconditional_misses": 34, "completed_misses": 17,
                      "incomplete": 65519}
    assert Fraction(totals["unconditional_misses"], totals["paths"]) < Fraction(1, 40)
    result = {"stage": "DEVELOPMENT", "version": VERSION, "totals": totals,
              "radius": [77, 6], "Q": 64, "R": 12,
              "unconditional_failure": [17, 32768],
              "conditional_coverage_on_completion": [0, 1],
              "all_path_provider_funding": 32,
              "source_unchanged": source.read_bytes() == captured.read_bytes(),
              "strata": strata, "all_checks_pass": True}
    (out / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("totals", "conditional_coverage_on_completion", "all_checks_pass")}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    run(parser.parse_args().out)
