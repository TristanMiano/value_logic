"""Public-syntax bridge acquisition, new developmental seeds, no hidden labels.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. Rule fixed before this probe's exposure:
include any unrequested vertex whose clauses are a strict subset of at least
two requested vertices; buy the resulting set weakest-first by distinct-clause
count, then vertex ID. Ordinary direct bank receives the identical rule.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import sys
import time

import cnf_receipts as R

SEEDS = (26101271, 26101293)
SOURCE_ROWS = 96
SAMPLE_ROWS = 24
INITIAL_PAIRS = ((0, 3), (2, 6), (3, 6))
SCHEDULES = {
    "one_pair": (((0, 3),),),
    "three_pairs_no_expansion": (INITIAL_PAIRS,),
    "full_expansion": (INITIAL_PAIRS, ((1, 5),), ((4, 6),)),
}
MODES = ("requested_weakest_first", "bridges_weakest_first",
         "direct_bank_same_bridges", "full_weakest_first")
EVENT_FIELDS = ("row", "vertex", "status", "answer", "witness",
                "parent_vertex", "provider_units", "adapter_units",
                "process_ns", "wall_ns")


class SyntaxPlanner:
    def __init__(self, adapter):
        self.adapter = adapter
        self.syntax = {}
        self.records = []
        self.counts = Counter()
        self.units = 0

    def clauses(self, row, vertex):
        meter = self.adapter.meter
        meter.pay("controller", "syntax_cache_identity_lookup", 4)
        key = row, vertex
        if key not in self.syntax:
            q = self.adapter.source.query(row, vertex)
            meter.pay("controller", "public_clause_words_read", q.key_words)
            # Input clauses are already in canonical order. Remove adjacent
            # duplicates with charged bounded-width comparisons.
            unique = []
            for clause in q.clauses:
                meter.pay("controller", "syntax_unique_clause_compare", 2+len(clause))
                if not unique or clause != unique[-1]:
                    meter.pay("storage", "syntax_unique_clause_retained", 1+len(clause))
                    unique.append(clause)
            self.syntax[key] = tuple(unique)
            self.counts["vertex_syntax_compilations"] += 1
        else:
            self.counts["syntax_cache_hits"] += 1
        return self.syntax[key]

    def strict_subset(self, left, right):
        meter = self.adapter.meter
        meter.pay("controller", "bridge_strict_length_check", 2)
        self.counts["structural_subset_tests"] += 1
        if len(left) >= len(right):
            return False
        i = j = 0
        while i < len(left) and j < len(right):
            meter.pay("controller", "bridge_sorted_clause_compare",
                      3+len(left[i])+len(right[j]))
            if left[i] == right[j]:
                i += 1
                j += 1
            elif left[i] > right[j]:
                j += 1
            else:
                return False
        return i == len(left)

    def plan(self, row, requested, mode, stage):
        meter = self.adapter.meter
        before = meter.total
        targets = set(requested)
        meter.pay("controller", "requested_vertex_set_record", 4*len(targets)+1)
        bridges = []
        if mode in ("bridges_weakest_first", "direct_bank_same_bridges"):
            # All eligibility comes from public syntax, before acquisition.
            sets = {v: self.clauses(row, v) for v in range(7)}
            for b in range(7):
                if b in targets:
                    continue
                covers = 0
                for v in sorted(targets):
                    if self.strict_subset(sets[b], sets[v]):
                        covers += 1
                if covers >= 2:
                    bridges.append(b)
            chosen = targets | set(bridges)
        elif mode == "full_weakest_first":
            chosen = set(range(7))
        else:
            assert mode == "requested_weakest_first"
            chosen = targets
        # Charge actual bounded insertion-sort comparisons, with deterministic
        # public key (number of distinct clauses, vertex index).
        ordered = []
        ranks = {v: (len(self.clauses(row, v)), v) for v in chosen}
        for v in sorted(chosen):
            pos = len(ordered)
            while pos:
                meter.pay("controller", "weakest_first_rank_compare", 3)
                if ranks[ordered[pos-1]] <= ranks[v]:
                    break
                pos -= 1
            meter.pay("controller", "weakest_first_insert_shift", 1+len(ordered)-pos)
            ordered.insert(pos, v)
        cached_bridges = [v for v in bridges if (row, v) in self.adapter.cache]
        meter.pay("controller", "bridge_cache_status_record", 4*len(bridges)+1)
        record = dict(row=row, stage=stage, requested=sorted(targets),
                      bridges=bridges, cached_bridges=cached_bridges,
                      fresh_bridges=[v for v in bridges if v not in cached_bridges],
                      ordered=ordered, planning_units=meter.total-before)
        self.units += record["planning_units"]
        self.counts["plans"] += 1
        self.counts["bridge_inclusions"] += len(bridges)
        self.counts["already_cached_bridge_inclusions"] += len(cached_bridges)
        self.records.append(record)
        return ordered


def compact_snapshot(adapter, planner):
    snap = adapter.snapshot()
    return {k: snap[k] for k in ("provider_units", "adapter_units", "total_units",
                                 "counts", "unique_receipts")} | {
        "syntax_planning_units": planner.units,
        "syntax_counts": dict(planner.counts)}


def arm(source, sample, schedule, mode):
    wall = time.perf_counter_ns()
    cpu = time.process_time_ns()
    adapter = R.Adapter(source)
    planner = SyntaxPlanner(adapter)
    requested = set()
    stages = []
    features = {}
    for stage, new_pairs in enumerate(schedule):
        requested.update(v for pair in new_pairs for v in pair)
        for row in sample:
            ordered = planner.plan(row, requested, mode, stage)
            for vertex in ordered:
                adapter.acquire(row, vertex)
            for a, b in new_pairs:
                if mode == "direct_bank_same_bridges":
                    contrast = adapter.direct_pair_contrast(row, a, b)
                    value = None if contrast is None else -contrast
                else:
                    value = adapter.feature(row, (a, b))
                features[f"{row}:{a}:{b}"] = value
        stages.append(dict(stage=stage, new_pairs=new_pairs,
                           snapshot=compact_snapshot(adapter, planner)))
    assert all(value in (-1, 1) for value in features.values())
    return dict(mode=mode, stages=stages, final=adapter.snapshot(),
                planner_counts=dict(planner.counts), planner_units=planner.units,
                plan_records=planner.records, features=features,
                event_fields=EVENT_FIELDS,
                events=[[e.get(field) for field in EVENT_FIELDS] for e in adapter.events],
                process_ns=time.process_time_ns()-cpu,
                wall_ns=time.perf_counter_ns()-wall)


def result_summary(case):
    return {"seed": case["seed"], "schedule": case["schedule"],
            "arms": [{"mode": a["mode"],
                      "provider_units": a["final"]["provider_units"],
                      "total_units": a["final"]["total_units"],
                      "provider_calls": a["final"]["counts"].get("provider_calls", 0),
                      "planning_units": a["planner_units"],
                      "cached_bridges": a["planner_counts"].get("already_cached_bridge_inclusions", 0)}
                     for a in case["arms"]]}


def main(out):
    if out.exists():
        raise FileExistsError("Preserve previous exposure")
    started = time.perf_counter_ns()
    inherited = json.loads(Path(__file__).with_name("cnf_results.json").read_text())
    files = {Path(__file__)} | {R.EXPERIMENTS.parent.parent/path for path in inherited["sources"]}
    result = dict(status="running", evidence="DEVELOPMENT",
                  contributor="ChatGPT (GPT-6 Astra Pro)",
                  start_utc=datetime.now(timezone.utc).isoformat(), python=sys.version,
                  command=sys.argv, seeds=SEEDS, source_rows=SOURCE_ROWS,
                  sample_rows=SAMPLE_ROWS, schedules=SCHEDULES,
                  rule="Cumulative requested endpoints R; add unrequested b iff clauses(b) is a strict subset of at least two requested clause sets; order by distinct-clause count then vertex. All choices use public syntax, never labels or realized costs.",
                  sources={str(p.relative_to(R.EXPERIMENTS.parent.parent)):
                           hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                  inherited_probe_sha256=hashlib.sha256(Path(__file__).with_name("cnf_results.json").read_bytes()).hexdigest(),
                  scope="Two fresh source seeds after the earlier exposed fixture. Six schedules across seeds, fixed arm order, explicit public-syntax planning bills, independent arm caches, common receipt/transport kernel. Full and requested-only controls use the same weakest-first ordering. No law, accuracy or label table is supplied. Instrumented warm timing is recorded, not a replicated timing claim. No new theorem, coverage or economic readiness is claimed.",
                  cases=[])
    def save():
        out.write_text(json.dumps(result, separators=(",", ":"))+"\n")
    save()
    for seed in SEEDS:
        source = R.cohort(seed, SOURCE_ROWS)
        sample = list(range(SOURCE_ROWS))
        random.Random(seed+1).shuffle(sample)
        sample = sample[:SAMPLE_ROWS]
        for name, schedule in SCHEDULES.items():
            case = dict(seed=seed, source_identity=source.identity,
                        sample_order=sample, schedule=name, arms=[])
            result["cases"].append(case)
            for mode in MODES:
                case["arms"].append(arm(source, sample, schedule, mode))
                save()
            ref = case["arms"][0]["features"]
            assert all(a["features"] == ref for a in case["arms"])
            bridge, direct = case["arms"][1:3]
            assert bridge["final"]["provider_units"] == direct["final"]["provider_units"]
            assert bridge["planner_units"] == direct["planner_units"]
            expected = sum(len(pairs) for pairs in schedule)*SAMPLE_ROWS
            assert direct["final"]["total_units"]-bridge["final"]["total_units"] == expected
            case["checks"] = dict(feature_values_match=True,
                                  ordinary_bank_evidence_and_planning_identical=True,
                                  direct_bank_additional_scalar_operations=expected)
            print(json.dumps(result_summary(case)), flush=True)
    result.update(status="complete", elapsed_wall_ns=time.perf_counter_ns()-started,
                  end_utc=datetime.now(timezone.utc).isoformat())
    save()


if __name__ == "__main__":
    main(Path(sys.argv[1]))
