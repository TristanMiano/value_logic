#!/usr/bin/env python3
"""Small exact reconstruction of row_margins.py; no acquisition calls."""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s05"))
import maxsat_repair as source
import row_margins


def encode(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, dict):
        return {k: encode(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)):
        return [encode(x) for x in v]
    return v


def run(path):
    if path.exists():
        raise FileExistsError("Preserve reconstruction evidence")
    wall, cpu = time.perf_counter_ns(), time.process_time_ns()
    meter = source.Meter()
    cases = [
        dict(name="one_anticorrelated_row", modes=[[0, 2], [2, 0]], possible=[[0, 1]], q=[1, 1]),
        dict(name="different_fixed_rows", modes=[[0, 2], [2, 0]], possible=[[0], [1]], q=[2, 2]),
        dict(name="known_plus_unknown_row", modes=[[0, 2], [2, 0]], possible=[[0], [0, 1]], q=[1, 3]),
        dict(name="zero_query_residual", modes=[[0, 2], [2, 0]], possible=[[0], [0, 1]], q=[0, 0]),
        dict(name="three_features", modes=[[1, 4, 0], [4, 0, 2], [2, 3, 1]], possible=[[0, 1], [1, 2]], q=[5, 3, 2]),
        dict(name="signed_supplied_reference", modes=[[0, 2], [2, 0]], possible=[[0], [0, 1]], q=[1, 3], references=[[-1, 2], [2, 1]]),
    ]
    records, total = [], 0
    for c in cases:
        quote = row_margins.margins(c["modes"], c["possible"], c["q"], meter, c.get("references"))
        assert quote["alpha"] <= quote["box_alpha"] and quote["delta"] <= quote["box_delta"]
        cases_checked = 0
        for configuration in itertools.product(*c["possible"]):
            w = [sum(c["modes"][h][j] for h in configuration) for j in range(len(c["q"]))]
            for z in itertools.product((0, 1), repeat=len(c["q"])):
                value = sum((wj - qj) * zj for wj, qj, zj in zip(w, c["q"], z))
                assert value <= quote["alpha"] and -value <= quote["delta"]
                cases_checked += 1
                meter.pay("construction_check", "direct_finite_objective_transfer", 5 * len(c["q"]) + 2)
        records.append(c | dict(quote=quote, direct_configurations_and_objective_masks=cases_checked))
        total += cases_checked
    first = records[0]["quote"]
    assert (first["alpha"], first["delta"], first["box_alpha"], first["box_delta"]) == (1, 1, 2, 2)
    assert records[1]["quote"]["alpha"] == records[1]["quote"]["delta"] == 0
    assert records[2]["quote"]["decompositions"][0]["rows"][0] == dict(alpha=0, delta=0)
    result = dict(status="passed", evidence="DEVELOPMENT exact arithmetic reconstruction",
                  contributor="ChatGPT (GPT-6 Astra Pro)", created_utc=datetime.now(timezone.utc).isoformat(),
                  source_sha256=hashlib.sha256((HERE / "row_margins.py").read_bytes()).hexdigest(),
                  check_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  cases=records, direct_finite_checks=total, actual_acquisition_calls=0,
                  scope="The check enumerates only these declared small source configurations and objective masks. Production quotations never enumerate either set.",
                  invoice=meter.record(), timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))
    path.write_text(json.dumps(encode(result), indent=2) + "\n")
    print(json.dumps(dict(status="passed",finite_checks=total,quotes=len(cases),units=meter.total)))


if __name__ == "__main__":
    run(Path(sys.argv[1]))
