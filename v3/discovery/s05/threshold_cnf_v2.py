"""Exposed-cohort developmental replay with saturated SAT witnesses.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. A failed witness proves no UNSAT fact.
Prior threshold_cnf.py and its source-bound result are left unchanged.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import cnf_receipts as R
import threshold_cnf as old


class SaturatedThresholdService(old.ThresholdService):
    def __init__(self, source):
        super().__init__(source)
        self.additions = {}
        self.witness_frontiers = {}

    def prepare(self, row):
        super().prepare(row)
        if row in self.additions:
            return
        meter = self.adapter.meter
        previous = ()
        deltas = []
        for k in range(old.LEVELS):
            q = self.adapter.source.query(row, k)
            meter.pay("check", "prefix_delta_source_identity", q.key_words+4)
            unique = []
            for clause in q.clauses:
                meter.pay("check", "prefix_delta_dedup_compare", 2+len(clause))
                if not unique or clause != unique[-1]:
                    unique.append(clause)
            i = 0
            added = []
            for clause in unique:
                meter.pay("check", "prefix_delta_merge_compare",
                          3+len(clause)+(len(previous[i]) if i < len(previous) else 0))
                if i < len(previous) and clause == previous[i]:
                    i += 1
                else:
                    if i < len(previous):
                        assert clause < previous[i]
                    added.append(clause)
                    meter.pay("storage", "prefix_delta_clause_retained", 1+len(clause))
            assert i == len(previous)
            deltas.append(tuple(added))
            previous = unique
        self.additions[row] = tuple(deltas)
        self.counts["delta_preparations"] += 1

    def get(self, row, k, provider_cap=R.native.SERVICE_CAP):
        answer = super().get(row, k, provider_cap)
        receipt = self.adapter.cache.get((row, k))
        if answer != 1 or receipt is None:
            return answer
        witness = receipt.witness
        assert witness is not None
        key = row, witness
        meter = self.adapter.meter
        meter.pay("check", "witness_frontier_identity_lookup", 8)
        if key in self.witness_frontiers:
            frontier = self.witness_frontiers[key]
            assert frontier["failed_at"] is None or k < frontier["failed_at"]
            self.counts["cached_witness_frontiers"] += 1
            return answer
        last, failed_at = k, None
        for j in range(k+1, old.LEVELS):
            wall, cpu = time.perf_counter_ns(), time.process_time_ns()
            before_units = meter.total
            before = tuple(self.intervals[row])
            q = self.adapter.source.query(row, j)
            meter.pay("check", "prefix_extension_claim_identity", q.key_words+6)
            ok = True
            for clause in self.additions[row][j]:
                meter.pay("check", "prefix_added_clause_begin", 3)
                satisfied = False
                for literal in clause:
                    meter.pay("check", "prefix_added_literal_witness_check", 6)
                    bit = (witness >> (abs(literal)-1)) & 1
                    satisfied |= bit == int(literal > 0)
                self.counts["added_clause_checks"] += 1
                if not satisfied:
                    ok = False
                    break
            if not ok:
                failed_at = j
                status = "witness_extension_failed"
                result_answer = None
                self.counts["failed_extension_witnesses"] += 1
                # No change to the upper endpoint, and no false label stored.
                assert tuple(self.intervals[row]) == before
            else:
                lo, hi = self.intervals[row]
                lo = max(lo, j+1)
                assert lo <= hi
                self.intervals[row] = [lo, hi]
                meter.pay("check", "saturated_lower_endpoint_update", 8)
                if (row, j) not in self.adapter.cache:
                    self.adapter.cache[row, j] = R.VertexReceipt(
                        row, j, q.claim_key, 1, witness,
                        "saturated_sat_transport", last)
                    meter.pay("storage", "saturated_vertex_receipt_retained", 16+q.key_words)
                    self.adapter.counts["saturated_sat_transports"] += 1
                    self.counts["new_saturated_sat_receipts"] += 1
                    status = "saturated_sat_transport"
                else:
                    assert self.adapter.cache[row, j].answer == 1
                    meter.pay("check", "existing_saturated_receipt_identity", q.key_words)
                    status = "saturated_existing_sat"
                result_answer = 1
                last = j
            meter.pay("output", "prefix_extension_record", 16)
            event = dict(row=row, vertex=j, provider_cap=provider_cap,
                         claim_sha256=R.digest(q.claim_key), status=status,
                         answer=result_answer, witness=witness, parent_vertex=k,
                         provider_units=0, adapter_units=meter.total-before_units,
                         process_ns=time.process_time_ns()-cpu,
                         wall_ns=time.perf_counter_ns()-wall)
            self.adapter.process_ns += event["process_ns"]
            self.adapter.wall_ns += event["wall_ns"]
            self.adapter.events.append(event)
            self.events.append(dict(row=row, k=j, before=before,
                                    after=tuple(self.intervals[row]),
                                    answer=result_answer, status=status,
                                    witness=witness, source_vertex=k))
            if not ok:
                break
        self.witness_frontiers[key] = dict(last_sat=last, failed_at=failed_at)
        meter.pay("storage", "saturated_witness_frontier_retained", 8)
        return answer


def smoke():
    # The first witness sets x1=x2=1. Adding -x1 invalidates that witness but
    # leaves another SAT assignment. This explicitly checks the key distinction.
    base = ((1, 2),)
    units = ((-1,), (2,), (3,), (-3,), (1,), (-2,), (-1,))
    queries = tuple(R.native.make_query(f"sat-prefix-smoke-{k}", 3,
                       base+units[:k], source_version="s05-saturated-smoke")
                    for k in range(old.LEVELS))
    source = old.ChainSource((queries,), "explicit-saturation-smoke", {})
    service = SaturatedThresholdService(source)
    assert service.get(0, 0) == 1
    assert service.interval(0) == (1, old.LEVELS)
    assert (0, 1) not in service.adapter.cache
    assert service.get(0, 1) == 1
    assert service.interval(0)[1] == old.LEVELS
    assert service.get(0, 3) == 1
    assert service.interval(0)[1] == old.LEVELS
    assert service.get(0, 4) == 0
    assert service.interval(0) == (4, 4)
    assert service.counts["failed_extension_witnesses"] >= 2
    return dict(status="complete", events=service.events,
                acquisition_events=service.adapter.events,
                counts=dict(service.counts), invoice=service.adapter.snapshot())


def main(out):
    if out.exists():
        raise FileExistsError("Preserve previous saturation exposure")
    baseline_path = Path(__file__).with_name("threshold_cnf_results.json")
    baseline = json.loads(baseline_path.read_text())
    source = old.cohort()
    assert source.identity == baseline["source_identity"]
    sample = baseline["sample_with_replacement"]
    files = {Path(__file__)} | {R.EXPERIMENTS.parent.parent/p for p in baseline["sources"]}
    result = dict(status="running", evidence="DEVELOPMENT",
                  contributor="ChatGPT (GPT-6 Astra Pro)",
                  start_utc=datetime.now(timezone.utc).isoformat(), python=sys.version,
                  command=sys.argv, source_identity=source.identity,
                  sample_with_replacement=sample,
                  baseline_result_sha256=hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
                  sources={str(p.relative_to(R.EXPERIMENTS.parent.parent)):
                           hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                  scope="Explicit exposed same-input replay. For each original query rule, compare its own nonsaturated and saturated service. Every new SAT witness is checked against successive added clauses; a failed witness narrows no UNSAT endpoint. Extension preprocessing, checks, storage and output are charged. Same cohort and replacement draws, no fresh source or confirmation claim.",
                  comparisons=[])
    def save():
        out.write_text(json.dumps(result, separators=(",", ":"))+"\n")
    save()
    result["smoke"] = smoke()
    save()
    for mode in old.MODES:
        ordinary = old.arm(source, sample, mode)
        saturated = old.arm(source, sample, mode, service_class=SaturatedThresholdService)
        old_arm = next(a for a in baseline["arms"] if a["mode"] == mode)
        assert ordinary["final"]["provider_units"] == old_arm["final"]["provider_units"]
        ref = [s["feature_values"] for s in ordinary["stages"]]
        assert [s["feature_values"] for s in saturated["stages"]] == ref
        result["comparisons"].append(dict(mode=mode, ordinary=ordinary,
                                          saturated=saturated,
                                          feature_values_match=True))
        save()
        print(json.dumps(dict(mode=mode, arms=[dict(service=label,
              provider_calls=a["final"]["counts"].get("provider_calls", 0),
              provider_units=a["final"]["provider_units"],
              provider_and_adapter_units=a["final"]["total_units"],
              process_ms=a["process_ns"]/1e6, interval_counts=a["interval_counts"])
              for label, a in (("ordinary", ordinary), ("saturated", saturated))])), flush=True)
    result.update(status="complete", end_utc=datetime.now(timezone.utc).isoformat())
    save()


if __name__ == "__main__":
    main(Path(sys.argv[1]))
