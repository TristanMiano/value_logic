"""Real nested-CNF thresholds and paid interval observations. DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. H is the first UNSAT vertex 0..7,
or 8 when all vertices are SAT. No threshold law or solve-price law is given.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import factorial
from pathlib import Path
import random
import sys
import time

import cnf_receipts as R
import threshold_plan as T

VERSION = "s05-nested-cnf-threshold-v1"
SEED = 261012117
SOURCE_ROWS = 64
DRAWS = 16
LEVELS = 8
SCHEDULE = ((3, 4), (1, 6), (0, 7))
MODES = ("endpoint_bank", "midpoint_full_threshold", "minimax_query_count")


@dataclass(frozen=True)
class ChainSource:
    queries: tuple
    identity: str
    description: dict

    def query(self, row, vertex):
        if type(row) is not int or not 0 <= row < len(self.queries):
            raise ValueError("Unknown cohort row")
        if type(vertex) is not int or not 0 <= vertex < LEVELS:
            raise ValueError("Unknown chain vertex")
        return self.queries[row][vertex]


def cohort(seed=SEED, size=SOURCE_ROWS):
    rng = random.Random(seed)
    rows = []
    regimes = []
    for row in range(size):
        n = (8, 10)[row % 2]
        num, den = ((3, 2), (3, 1), (17, 4))[(row // 2) % 3]
        m = n*num//den
        base = tuple(tuple(v if rng.getrandbits(1) else -v
                           for v in rng.sample(range(1, n+1), 3)) for _ in range(m))
        additions = tuple((v if rng.getrandbits(1) else -v,)
                          for v in rng.sample(range(1, n+1), LEVELS-1))
        rows.append(tuple(R.native.make_query(f"th-r{row}-k{k}", n,
                     base+additions[:k], source_version=VERSION)
                          for k in range(LEVELS)))
        regimes.append(dict(variables=n, ratio=[num, den], base_clauses=m,
                            added_units=additions))
    identity = R.digest([[q.record() for q in row] for row in rows])
    return ChainSource(tuple(rows), identity,
                       dict(seed=seed, rows=size, levels=LEVELS,
                            regimes=regimes, truth_generation_calls=0))


class ThresholdService:
    """The interval is a sound receipt consequence, not a free latent label."""
    def __init__(self, source):
        self.adapter = R.Adapter(source)
        self.intervals = {}
        self.events = []
        self.counts = Counter()

    def prepare(self, row):
        meter = self.adapter.meter
        meter.pay("controller", "threshold_source_interval_lookup", 5)
        if row in self.intervals:
            return
        previous = None
        first = self.adapter.source.query(row, 0)
        for k in range(LEVELS):
            q = self.adapter.source.query(row, k)
            meter.pay("check", "chain_semantics_and_clause_words", q.key_words+8)
            assert (q.variables, q.source_version, q.semantics_version) == (
                    first.variables, first.source_version, first.semantics_version)
            unique = []
            for clause in q.clauses:
                meter.pay("check", "chain_clause_dedup_compare", 2+len(clause))
                if not unique or clause != unique[-1]:
                    unique.append(clause)
                    meter.pay("storage", "chain_unique_clause_record", 1+len(clause))
            if previous is not None:
                i = j = 0
                while i < len(previous) and j < len(unique):
                    meter.pay("check", "nested_clause_subset_compare",
                              3+len(previous[i])+len(unique[j]))
                    if previous[i] == unique[j]:
                        i += 1
                        j += 1
                    elif previous[i] > unique[j]:
                        j += 1
                    else:
                        raise ValueError("Source is not a clause chain")
                assert i == len(previous)
            previous = unique
        self.intervals[row] = [0, LEVELS]
        meter.pay("storage", "threshold_interval_initialized", 4)
        self.counts["chain_verifications"] += 1

    def interval(self, row):
        self.prepare(row)
        return tuple(self.intervals[row])

    def get(self, row, k, provider_cap=R.native.SERVICE_CAP):
        self.prepare(row)
        lo, hi = before = tuple(self.intervals[row])
        meter = self.adapter.meter
        q = self.adapter.source.query(row, k)
        meter.pay("check", "threshold_query_source_and_bounds", q.key_words+8)
        if k < lo or k >= hi:
            answer = int(k < lo)
            status = "cached_vertex" if (row, k) in self.adapter.cache else "interval_implication"
            meter.pay("check", "retained_threshold_consequence", 8)
        else:
            got = self.adapter.acquire(row, k, provider_cap)
            if got is None:
                answer, status = None, "unresolved"
            else:
                answer, status = got.answer, got.origin
                meter.pay("check", "checked_threshold_interval_update", 12)
                if answer:
                    lo = max(lo, k+1)
                else:
                    hi = min(hi, k)
                assert lo <= hi
                self.intervals[row] = [lo, hi]
        self.counts[status] += 1
        self.events.append(dict(row=row, k=k, before=before,
                                after=tuple(self.intervals[row]),
                                answer=answer, status=status,
                                provider_cap=provider_cap))
        return answer

    def feature(self, row, pair):
        lo, hi = self.interval(row)
        a, b = pair
        self.adapter.meter.pay("assessment", "threshold_pair_membership_bounds", 8)
        if lo > a and hi <= b:
            return 1
        if hi <= a or lo > b:
            return 0
        return None


def bands(service, sample):
    """Fixed-n conditional DKW band; exact rational radius .35 for n=16."""
    n = len(sample)
    assert n == DRAWS
    epsilon = Fraction(7, 20)
    exponent = 2*n*epsilon**2
    exp_lower = sum(exponent**k/Fraction(factorial(k)) for k in range(13))
    assert exp_lower > 40  # 2 exp(-2 n eps^2) < 1/20, by positive Taylor terms.
    endpoints = {}
    for t in range(-1, LEVELS+1):
        lower_count = sum(service.interval(row)[1] <= t for row in sample)
        upper_count = sum(service.interval(row)[0] <= t for row in sample)
        lower = max(Fraction(0), Fraction(lower_count, n)-epsilon)
        upper = min(Fraction(1), Fraction(upper_count, n)+epsilon)
        if t == -1:
            lower = upper = Fraction(0)
        elif t == LEVELS:
            lower = upper = Fraction(1)
        endpoints[str(t)] = dict(empirical_lower_count=lower_count,
                                 empirical_upper_count=upper_count,
                                 lower=str(lower), upper=str(upper))
    service.adapter.meter.pay("assessment", "cdf_envelope_row_endpoint_arithmetic",
                               12*n*(LEVELS+2))
    return dict(fixed_draws=n, radius=str(epsilon), delta="1/20",
                exact_exp_lower=str(exp_lower), endpoints=endpoints,
                scope="Conditional DKW warrant for iid uniform-with-replacement identities, with all draw multiplicities retained; seeded execution is developmental, not an empirical coverage experiment")


def arm(source, sample, mode, service_class=ThresholdService):
    wall, cpu = time.perf_counter_ns(), time.process_time_ns()
    service = service_class(source)
    plan_cache = {}
    planner = dict(calls=0, cache_hits=0, process_ns=0, wall_ns=0,
                   criterion="worst complete-query count, not measured solve prices")
    stages = []
    active = []
    for stage, pair in enumerate(SCHEDULE):
        active.append(pair)
        features = []
        for draw, row in enumerate(sample):
            if mode == "endpoint_bank":
                for endpoint in pair:
                    if service.feature(row, pair) is not None:
                        break
                    service.get(row, endpoint)
            elif mode == "midpoint_full_threshold":
                while True:
                    lo, hi = service.interval(row)
                    if lo == hi:
                        break
                    if service.get(row, (lo+hi-1)//2) is None:
                        break
            else:
                assert mode == "minimax_query_count"
                masks = tuple((1 << a) | (1 << b) for a, b in active)
                while True:
                    lo, hi = service.interval(row)
                    key = masks, lo, hi
                    service.adapter.meter.pay("controller", "query_plan_cache_lookup", 8)
                    if key not in plan_cache:
                        pw, pc = time.perf_counter_ns(), time.process_time_ns()
                        value, tree = T.plan([1]*LEVELS, masks, mode="minimax", interval=(lo, hi))
                        planner["process_ns"] += time.process_time_ns()-pc
                        planner["wall_ns"] += time.perf_counter_ns()-pw
                        planner["calls"] += 1
                        plan_cache[key] = value, tree
                    else:
                        planner["cache_hits"] += 1
                    value, tree = plan_cache[key]
                    if tree[0] == "leaf":
                        break
                    if service.get(row, tree[1]) is None:
                        break
            features.append(service.feature(row, pair))
        cdf = bands(service, sample)
        stages.append(dict(stage=stage, pair=pair, feature_values=features,
                           draw_intervals=[service.interval(row) for row in sample],
                           cdf_band=cdf, invoice=service.adapter.snapshot(),
                           interval_counts=dict(service.counts), planner=dict(planner)))
    assert all(x in (0, 1) for stage in stages for x in stage["feature_values"])
    final_intervals = {str(row): service.interval(row) for row in sorted(set(sample))}
    return dict(mode=mode, stages=stages, final=service.adapter.snapshot(),
                final_intervals=final_intervals,
                interval_counts=dict(service.counts), planner=planner,
                interval_events=service.events, acquisition_events=service.adapter.events,
                process_ns=time.process_time_ns()-cpu,
                wall_ns=time.perf_counter_ns()-wall)


def smoke(source):
    service = ThresholdService(source)
    before = service.interval(0)
    assert service.get(0, 3, provider_cap=32) is None
    assert service.interval(0) == before == (0, LEVELS)
    answer = service.get(0, 3)
    after = service.interval(0)
    assert answer in (0, 1) and after != before
    assert service.get(0, 3) == answer
    assert service.counts["cached_vertex"] == 1
    return dict(before=before, after=after, events=service.events,
                invoice=service.adapter.snapshot(), acquisition_events=service.adapter.events)


def cost_diagnostic(source, arms):
    exact = next(a for a in arms if a["mode"] == "midpoint_full_threshold")
    truth = {int(row): interval[0] for row, interval in exact["final_intervals"].items()}
    assert all(lo == hi for lo, hi in exact["final_intervals"].values())
    grouped = defaultdict(dict)
    for arm_result in arms:
        for e in arm_result["acquisition_events"]:
            if e["status"] != "checked_purchase":
                continue
            row, k = e["row"], e["vertex"]
            key = source.query(row, k).variables, truth[row], k
            grouped[key][row] = e["provider_units"]
    return dict(exact_H=truth,
                groups=[dict(variables=n, H=h, query=k, rows=sorted(values),
                             invoices=[values[row] for row in sorted(values)],
                             min_units=min(values.values()), max_units=max(values.values()))
                        for (n, h, k), values in sorted(grouped.items())
                        if len(values) >= 2],
                scope="Same n,H,query can still have different checked proof bills; completed midpoint evidence supplies H only for post-run diagnostics, inaccessible to other acquisition methods")


def main(out):
    if out.exists():
        raise FileExistsError("Preserve prior threshold exposure")
    source = cohort()
    rng = random.Random(SEED+1)
    sample = [rng.randrange(SOURCE_ROWS) for _ in range(DRAWS)]
    old = json.loads(Path(__file__).with_name("cnf_results.json").read_text())
    files = {Path(__file__), Path(T.__file__)} | {R.EXPERIMENTS.parent.parent/p for p in old["sources"]}
    result = dict(status="running", evidence="DEVELOPMENT",
                  contributor="ChatGPT (GPT-6 Astra Pro)", python=sys.version,
                  start_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv,
                  source=source.description, source_identity=source.identity,
                  sample_with_replacement=sample, unique_sample_rows=len(set(sample)),
                  schedule=SCHEDULE, modes=MODES,
                  sources={str(p.relative_to(R.EXPERIMENTS.parent.parent)):
                           hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                  scope="One fixed recipe, 16 uniform-with-replacement draws, eight nested CNF levels. Same checked receipt/interval interface for all methods. Provider and adapter tariff units exclude the new exact planner's internal Fraction arithmetic, which is measured separately in process/wall time and included in arm timers; its unit input weights target query count only. No supplied source accuracy or solve-cost law.",
                  arms=[])
    def save():
        out.write_text(json.dumps(result, separators=(",", ":"))+"\n")
    save()
    result["smoke"] = smoke(source)
    save()
    for mode in MODES:
        result["arms"].append(arm(source, sample, mode))
        save()
    ref = [s["feature_values"] for s in result["arms"][0]["stages"]]
    assert all([s["feature_values"] for s in a["stages"]] == ref for a in result["arms"])
    result["cost_diagnostic"] = cost_diagnostic(source, result["arms"])
    result.update(status="complete", checks=dict(shared_feature_values_match=True,
                  repeated_draw_multiplicity_retained=True,
                  capped_receipt_preserves_interval=True),
                  end_utc=datetime.now(timezone.utc).isoformat())
    save()
    print(json.dumps(dict(status=result["status"], draws=sample,
          unique_rows=len(set(sample)), arms=[dict(mode=a["mode"],
          stages=[dict(stage=s["stage"], provider_calls=s["invoice"]["counts"].get("provider_calls", 0),
                 provider_units=s["invoice"]["provider_units"],
                 provider_and_adapter_units=s["invoice"]["total_units"]) for s in a["stages"]],
          process_ms=a["process_ns"]/1e6, planner_ms=a["planner"]["process_ns"]/1e6)
          for a in result["arms"]])))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
