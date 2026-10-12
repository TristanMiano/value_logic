"""Small real-source acquisition comparison. DEVELOPMENT; not confirmation."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import sys
import time

import cnf_receipts as R

SEED = 26101257
SOURCE_ROWS = 96
SAMPLE_ROWS = 24
PAIRS = ((0, 3), (2, 6), (3, 6))
EXPANSIONS = ((1, 5), (4, 6))


def summary(values, N):
    known = [x for x in values if x is not None]
    positive = sum(x == 1 for x in known)
    negative = sum(x == -1 for x in known)
    return dict(sampled=len(values), completed=len(known), positive=positive,
                negative=negative, unresolved=len(values)-len(known),
                observed_mean=None if not known else sum(known)/len(known),
                deterministic_cohort_mean_interval=[2*positive/N-1,
                                                    1-2*negative/N],
                scope="Observed sample summary; interval is exact count containment, not a fitted source-accuracy assumption")


def smoke():
    base = R.native.make_query("smoke-base", 3, ((1, 2), (-1, 3)),
                               source_version=R.VERSION)
    sat = R.native.checked_purchase(base)
    assert sat.successful and sat.answer == 1 and sat.witness is not None
    literal = 1 if (sat.witness & 1) else -1
    forms = (base.clauses, base.clauses+((literal,),),
             base.clauses+((-literal,),), ((1,), (-1,)),
             ((1,), (-1,), (2,)), base.clauses, base.clauses)
    queries = tuple(R.native.make_query(f"smoke-{i}", 3, f,
                                       source_version=R.VERSION)
                    for i, f in enumerate(forms))
    source = R.Source((queries,), "explicit-smoke-source",
                       {"scope": "semantic checks, outside comparison cohort"})
    service = R.Adapter(source)
    assert service.acquire(0, 0, provider_cap=32) is None
    assert (0, 0) not in service.cache
    assert service.feature(0, (0,), provider_cap=32) is None
    assert service.acquire(0, 0).answer == 1
    assert service.acquire(0, 1).answer == 1
    assert service.acquire(0, 2) is not None
    assert service.acquire(0, 3).answer == 0
    assert service.acquire(0, 4).answer == 0
    before = service.snapshot()
    assert service.feature(0, (0, 1, 1, 0)) == 1
    after = service.snapshot()
    assert after["counts"]["provider_calls"] == before["counts"]["provider_calls"]
    assert after["unique_receipts"] == before["unique_receipts"]
    assert service.counts["unresolved_attempts"] == 2
    assert service.counts["sat_witness_transports"] >= 1
    assert service.counts["unsat_subset_transports"] >= 1
    assert service.counts["failed_witness_checks"] >= 1
    return dict(status="complete", initial_checked_fixture_provider_units=sat.resources.total,
                snapshot=service.snapshot(), events=service.events)


def run_arm(source, sample, mode):
    start = time.perf_counter_ns()
    cpu = time.process_time_ns()
    service = R.Adapter(source)
    observations = {str(pair): [] for pair in PAIRS+EXPANSIONS}
    stages = []
    for j, row in enumerate(sample, 1):
        if mode == "full_vertex_audit":
            for vertex in range(7):
                service.acquire(row, vertex)
        for a, b in PAIRS:
            if mode == "direct_fixed_pair_bank":
                contrast = service.direct_pair_contrast(row, a, b)
                value = None if contrast is None else -contrast
            else:
                value = service.feature(row, (a, b))
            observations[str((a, b))].append(value)
        if j in (8, 16, SAMPLE_ROWS):
            stages.append(dict(stage=f"initial_bank_{j}_rows",
                               snapshot=service.snapshot(),
                               summaries={str(p): summary(observations[str(p)],
                                          len(source.queries)) for p in PAIRS}))
    for pair in EXPANSIONS:
        a, b = pair
        for row in sample:
            if mode == "direct_fixed_pair_bank":
                contrast = service.direct_pair_contrast(row, a, b)
                value = None if contrast is None else -contrast
            else:
                value = service.feature(row, pair)
            observations[str(pair)].append(value)
        stages.append(dict(stage=f"add_pair_{a}_{b}", snapshot=service.snapshot(),
                           summary=summary(observations[str(pair)], len(source.queries))))
    return dict(mode=mode, stages=stages, observations=observations,
                final=service.snapshot(), receipts=[dict(row=r, vertex=v,
                 answer=x.answer, witness=x.witness, origin=x.origin,
                 parent_vertex=x.parent_vertex,
                 claim_sha256=R.digest(x.claim_key))
                 for (r, v), x in sorted(service.cache.items())],
                events=service.events,
                process_ns=time.process_time_ns()-cpu,
                wall_ns=time.perf_counter_ns()-start)


def main(out):
    if out.exists():
        raise FileExistsError("Preserve existing developmental evidence")
    start = time.perf_counter_ns()
    source_start = time.perf_counter_ns()
    source_cpu = time.process_time_ns()
    source = R.cohort(SEED, SOURCE_ROWS)
    source_process_ns = time.process_time_ns()-source_cpu
    source_wall_ns = time.perf_counter_ns()-source_start
    sample = list(range(SOURCE_ROWS))
    random.Random(SEED+1).shuffle(sample)
    sample = sample[:SAMPLE_ROWS]
    source_files = [Path(__file__), Path(R.__file__), Path(R.native.__file__),
                    R.EXPERIMENTS/"p308_common.py",
                    R.EXPERIMENTS.parent/"checks/07_selective_feedback.py",
                    R.EXPERIMENTS.parent/"checks/07_selective_feedback_service.py"]
    result = dict(status="running", evidence="DEVELOPMENT",
                  contributor="ChatGPT (GPT-6 Astra Pro)",
                  start_utc=datetime.now(timezone.utc).isoformat(),
                  python=sys.version, command=sys.argv,
                  sources={str(p.relative_to(R.EXPERIMENTS.parent.parent)):
                           hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
                  source_identity=source.identity, source=source.description,
                  sample_order=sample, source_setup_process_ns=source_process_ns,
                  source_setup_wall_ns=source_wall_ns, pairs=PAIRS,
                  expansions=EXPANSIONS, arms=[],
                  scope="Fixed 24-row lottery from a 96-row syntactic CNF cohort; seven revisions. Real checked evaluations, warm Python, fixed arm order. Each arm owns its paid cache. Common generation/import excluded from arm timers; source generation measured separately and identical public-source admission/storage is charged per arm. SHA/JSON trace construction is harness overhead included in arm wall/process time, not claimed a complete machine-operation tariff. No deployment, calibrated accuracy, independent coverage estimate or broad speedup is claimed.")
    def save():
        out.write_text(json.dumps(result, indent=2)+"\n")
    save()
    result["smoke"] = smoke()
    save()
    for mode in ("full_vertex_audit", "selected_boundary_pairs", "direct_fixed_pair_bank"):
        result["arms"].append(run_arm(source, sample, mode))
        save()
    reference = result["arms"][0]["observations"]
    assert all(arm["observations"] == reference for arm in result["arms"])
    assert all(v is not None for values in reference.values() for v in values)
    # Boundary acquisition and the direct bank use the same legitimate kernel.
    selected, bank = result["arms"][1:]
    assert selected["final"]["provider_units"] == bank["final"]["provider_units"]
    assert selected["receipts"] == bank["receipts"]
    expected_extra = SAMPLE_ROWS * (len(PAIRS)+len(EXPANSIONS))
    assert bank["final"]["adapter_units"]-selected["final"]["adapter_units"] == expected_extra
    result.update(status="complete", checks={"all_shared_feature_values_agree": True,
                      "initial_bank_receipts_are_shared": True,
                      "ordinary_direct_bank_uses_identical_paid_evidence": True,
                      "direct_bank_extra_scalar_operations": expected_extra},
                  elapsed_wall_ns=time.perf_counter_ns()-start,
                  end_utc=datetime.now(timezone.utc).isoformat())
    save()
    print(json.dumps({"status": result["status"], "source": source.identity,
        "arms": [{"mode": x["mode"], "stages": [{"stage": s["stage"],
         "units": s["snapshot"]["total_units"],
         "receipts": s["snapshot"]["unique_receipts"],
         "provider_calls": s["snapshot"]["counts"].get("provider_calls", 0)}
         for s in x["stages"]], "wall_ms": x["wall_ns"]/1e6}
         for x in result["arms"]]}))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
