"""Paid vertex receipts for a fixed CNF revision source. DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. No prediction accuracy or hidden labels
are supplied. Only checked purchases and checked transport create labels.
The tariff is an explicit service model; process/wall timers measure Python
execution separately. Provider caps exclude the separately invoiced adapter.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import random
import sys
import time

EXPERIMENTS = Path(__file__).resolve().parents[2] / "experiments"
if str(EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS))
import p308_cnf as native
from p308_common import C, resources

VERSION = "s05-cnf-vertex-receipts-v1"
EDGES = ((0, 1), (0, 2), (1, 3), (0, 4), (0, 5), (4, 6))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class Source:
    queries: tuple[tuple[native.Query, ...], ...]
    identity: str
    description: dict

    def query(self, row, vertex):
        if type(row) is not int or not 0 <= row < len(self.queries):
            raise ValueError("Unknown source row")
        if type(vertex) is not int or not 0 <= vertex < 7:
            raise ValueError("Unknown revision vertex")
        return self.queries[row][vertex]


def cohort(seed=26101257, size=96):
    """Generate public CNFs and syntactic edits, with no truth evaluation."""
    rng = random.Random(seed)
    rows = []
    regimes = []
    for i in range(size):
        n = (8, 10)[i % 2]
        num, den = ((17, 5), (83, 20), (5, 1))[(i // 2) % 3]
        m = (n * num) // den
        base = tuple(sorted(tuple(sorted(v if rng.getrandbits(1) else -v
                              for v in rng.sample(range(1, n + 1), 3)))
                            for _ in range(m)))
        forms = (base, base + ((1,),), base + ((-1,),),
                 base + ((1,), (2,)), base[1:],
                 base[1:] + ((-3, 2, 4),), base[1:] + ((-2,),))
        rows.append(tuple(native.make_query(f"s05-r{i}-v{v}", n, form,
                                            source_version=VERSION)
                          for v, form in enumerate(forms)))
        regimes.append(dict(variables=n, ratio=[num, den], base_clauses=m))
    description = dict(seed=seed, size=size, vertices=7, edges=EDGES,
                       regimes=regimes, edits=["base", "add +1", "add -1",
                       "add +1,+2", "delete first canonical clause",
                       "replace first clause by (-3,2,4)",
                       "delete first clause; add -2"],
                       forecast="fixed +1 edge parity; accuracy unknown")
    identity = digest([[q.record() for q in row] for row in rows])
    return Source(tuple(rows), identity, description)


@dataclass(frozen=True)
class VertexReceipt:
    row: int
    vertex: int
    claim_key: tuple
    answer: int
    witness: int | None
    origin: str
    parent_vertex: int | None


class Adapter:
    """A local trusted receipt service, not external proof authentication."""
    def __init__(self, source):
        self.source = source
        self.cache = {}
        self.events = []
        self.meter = C.CostMeter()
        self.provider_total = 0
        self.provider_operations = Counter()
        self.counts = Counter()
        self.wall_ns = self.process_ns = 0
        words = sum(q.key_words for row in source.queries for q in row)
        self.meter.pay("setup", "public_source_words_admitted", words)
        self.meter.pay("storage", "public_source_words_retained", words)

    def _transport(self, row, vertex, query):
        for (r, v), old in sorted(self.cache.items()):
            if r != row:
                continue
            self.counts["transport_attempts"] += 1
            self.meter.pay("controller", "transport_source_identity_read",
                           8 + len(old.claim_key[3]))
            if old.answer:
                # The inherited independent checker charges its actual scans.
                if native._verify_witness(query, old.witness, self.meter):
                    self.counts["sat_witness_transports"] += 1
                    return VertexReceipt(row, vertex, query.claim_key, 1,
                                         old.witness, "checked_sat_transport", v)
                self.counts["failed_witness_checks"] += 1
            else:
                # A CNF with more conjuncts cannot become satisfiable.
                clauses = query.clauses
                included = True
                for old_clause in old.claim_key[3]:
                    found = False
                    for clause in clauses:
                        self.meter.pay("check", "unsat_subset_clause_compare",
                                       1 + len(old_clause) + len(clause))
                        if old_clause == clause:
                            found = True
                            break
                    if not found:
                        included = False
                        break
                if included:
                    self.counts["unsat_subset_transports"] += 1
                    return VertexReceipt(row, vertex, query.claim_key, 0,
                                         None, "checked_unsat_transport", v)
        return None

    def acquire(self, row, vertex, provider_cap=native.SERVICE_CAP):
        """Return a checked vertex or None; every failed attempt is retained."""
        wall = time.perf_counter_ns()
        cpu = time.process_time_ns()
        before = self.meter.total
        query = self.source.query(row, vertex)
        self.meter.pay("controller", "source_and_cache_identity_lookup",
                       8 + query.key_words)
        key = row, vertex
        result = self.cache.get(key)
        provider_bill = 0
        event = dict(row=row, vertex=vertex, provider_cap=provider_cap,
                     claim_sha256=digest(query.claim_key))
        if result is not None:
            self.meter.pay("check", "cached_claim_identity_check", query.key_words)
            if result.claim_key != query.claim_key:
                raise ValueError("Receipt does not match the requested source")
            self.counts["cache_hits"] += 1
            event["status"] = "cache_hit"
        else:
            result = self._transport(row, vertex, query)
            if result is None:
                self.counts["provider_calls"] += 1
                got = native.checked_purchase(query, limit_total=provider_cap)
                provider_bill = got.resources.total
                self.provider_total += provider_bill
                for category, op, units in got.resources.operations:
                    self.provider_operations[category, op] += units
                event.update(provider_status=got.status,
                             provider_detail=got.detail)
                if got.successful and got.checked and got.answer in (0, 1):
                    if got.claim_key != query.claim_key:
                        raise ValueError("Provider returned another claim")
                    result = VertexReceipt(row, vertex, query.claim_key,
                                           got.answer, got.witness,
                                           "checked_purchase", None)
                else:
                    self.counts["unresolved_attempts"] += 1
            if result is None:
                event["status"] = "unresolved"
            else:
                self.meter.pay("storage", "checked_vertex_receipt_retained",
                               16 + query.key_words)
                self.cache[key] = result
                event["status"] = result.origin
        self.meter.pay("output", "vertex_response_record", 16)
        event.update(answer=None if result is None else result.answer,
                     witness=None if result is None else result.witness,
                     parent_vertex=None if result is None else result.parent_vertex,
                     provider_units=provider_bill,
                     adapter_units=self.meter.total-before,
                     process_ns=time.process_time_ns()-cpu,
                     wall_ns=time.perf_counter_ns()-wall)
        self.process_ns += event["process_ns"]
        self.wall_ns += event["wall_ns"]
        self.events.append(event)
        return result

    def feature(self, row, vertices, provider_cap=native.SERVICE_CAP):
        """A product of vertex signs; even multiplicities cancel before buying."""
        raw = tuple(vertices)
        self.meter.pay("controller", "boundary_multiplicity_reduction", 4*len(raw)+1)
        support = sorted(v for v, count in Counter(raw).items() if count % 2)
        value = 1
        unresolved = False
        for vertex in support:
            got = self.acquire(row, vertex, provider_cap)
            if got is None:
                unresolved = True
            else:
                self.meter.pay("assessment", "boundary_sign_product", 3)
                value *= 2*got.answer-1
        return None if unresolved else value

    def direct_pair_contrast(self, row, a, b):
        """Equal-vs-opposite prediction loss contrast, using the same anchor.

        Both policies acquire a and forecast b. Their common acquisition cost
        cancels. Loss(equal)-loss(opposite)=-X_a X_b. A strong ordinary direct
        audit can use this identical endpoint reduction and receipt service.
        """
        value = self.feature(row, (a, b))
        self.meter.pay("assessment", "direct_paired_loss_contrast", 1)
        return None if value is None else -value

    def snapshot(self):
        adapter = resources(self.meter).record()
        return dict(provider_units=self.provider_total,
                    adapter_units=adapter["total"],
                    total_units=self.provider_total+adapter["total"],
                    adapter_by_category=adapter["by_category"],
                    adapter_operations=adapter["operations"],
                    provider_operations=[dict(category=c, operation=o, units=n)
                          for (c, o), n in sorted(self.provider_operations.items())],
                    counts=dict(self.counts), unique_receipts=len(self.cache),
                    acquisition_process_ns=self.process_ns,
                    acquisition_wall_ns=self.wall_ns,
                    events=len(self.events))
