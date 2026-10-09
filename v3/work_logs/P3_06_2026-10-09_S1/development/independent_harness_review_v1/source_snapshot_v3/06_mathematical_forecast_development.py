"""Bounded P3-06 modular-query development, not a frozen evaluation.

Contributor: ChatGPT (GPT-6 Astra Pro), October 9, 2026 UTC.
Python 3.10+, standard library. Run from anywhere; existing output is refused.

The simulator prepares reproducible inputs, issues immutable reports, then
produces and checks answers, and finally releases them on a declared schedule.
The checker is trusted local code, not a formal-proof authentication service.
Known same-scope residues bypass fallible forecasting even under fresh IDs.

The two ordinary K29 adapters intentionally use the identical numerical core.
The separate Brier AA uses binary64 log/exp; its observed numerical slack is
reported, not certified. The exact modular-power baseline gets the full input
and pays for its ordinary fast computation. All runs remain development.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass, replace
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys
import time
import traceback


HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
CORE_PATH = HERE.with_name("06_defensive_forecasting.py")
SPEC = importlib.util.spec_from_file_location("p306_scalar_development_core", CORE_PATH)
assert SPEC is not None and SPEC.loader is not None
CORE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CORE
SPEC.loader.exec_module(CORE)

VERSION = "p306-modular-development-v3"
# Instrumentation correction only: retain v1's exact input population.
INPUT_GENERATION_VERSION = "p306-modular-development-v1"
SCOPE = "modexp-equality-v1:a=0..8191:n=0..192:m=2..97:r=0..m-1"
EXPERTS = ("constant_half", "residue_frequency", "partial_exact_shortcut", "fallible_parity")
METHODS = ("scalar_without_decision", "scalar_with_decision",
           "ordinary_k29_without_decision", "ordinary_k29_with_decision",
           "ordinary_brier_aa_binary64", "ordinary_fast_exact")
DEFAULT_OUTPUT = ROOT / "v3/work_logs/P3_06_2026-10-09_S1/development/mathematical_queries_v3"
AA_SOURCE = "https://www.jmlr.org/papers/volume10/vovk09a/vovk09a.pdf"


def sha(value) -> str:
    return hashlib.sha256(json.dumps(CORE.encoded(value), sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(CORE.encoded(value), sort_keys=True, indent=2) + "\n")


def input_bits(a: int, n: int, m: int, r: int) -> int:
    return sum(max(1, v.bit_length()) for v in (a, n, m, r))


@dataclass(frozen=True)
class Query:
    query_id: str
    a: int
    n: int
    m: int
    r: int
    scope: str = SCOPE

    def __post_init__(self):
        if (type(self.query_id) is not str or not self.query_id
                or type(self.scope) is not str or self.scope != SCOPE
                or any(type(x) is not int for x in (self.a, self.n, self.m, self.r))
                or not 0 <= self.a <= 8191 or not 0 <= self.n <= 192
                or not 2 <= self.m <= 97 or not 0 <= self.r < self.m):
            raise ValueError("Outside the declared bounded modular-query scope.")

    @property
    def key(self):
        # Exact claim identity does not include the display/request identity.
        return (self.scope, self.a, self.n, self.m, self.r)

    @property
    def residue_key(self):
        # A checked residue entails answers for every target r at these inputs.
        return (self.scope, self.a, self.n, self.m)


def multiply_power(a: int, n: int, m: int):
    """Producer: n modular multiplications, including n=0's explicit identity."""
    result, base, largest = 1 % m, a % m, 1
    for _ in range(n):
        product = result * base
        largest = max(largest, product.bit_length())
        result = product % m
    return result, {"modular_multiplies": n, "modular_reductions": n + 2,
                    "loop_iterations": n, "max_product_bits": largest}


def square_power(a: int, n: int, m: int):
    """Independent binary algorithm, also the ordinary fast exact baseline."""
    result, base, exponent = 1 % m, a % m, n
    products, iterations, largest = 0, 0, 1
    while exponent:
        iterations += 1
        if exponent & 1:
            product = result * base
            largest = max(largest, product.bit_length())
            result = product % m
            products += 1
        exponent >>= 1
        if exponent:
            product = base * base
            largest = max(largest, product.bit_length())
            base = product % m
            products += 1
    return result, {"modular_multiplies": products, "modular_reductions": products + 2,
                    "loop_iterations": iterations, "max_product_bits": largest}


@dataclass(frozen=True)
class Receipt:
    query_id: str
    scope: str
    claim_key: tuple
    residue: int
    answer: int
    issued_event: int
    produced_event: int
    checked_event: int
    producer_counts: tuple[tuple[str, int], ...]
    checker_counts: tuple[tuple[str, int], ...]
    python_pow_crosscheck: bool

    @property
    def digest(self):
        return sha(asdict(self))


class Evidence:
    """Local receipt registry with admission separated from computation.

    Equality to an internally checked immutable record is an integrity rule,
    not evidence that arbitrary external certificates or software are trusted.
    A production receipt remains private to the scheduler until admit().
    """
    def __init__(self):
        self.issued = {}
        self.checked = {}
        self._registered_receipt_sha256 = {}
        self.claims = {}
        self.residues = {}
        self.admitted = set()
        self.events = []
        self.counts = Counter()

    def event(self, kind, **fields):
        value = len(self.events)
        self.events.append({"event": value, "kind": kind, **fields})
        return value

    def register(self, query, tick):
        if query.query_id in self.issued:
            raise ValueError("Query identity reused.")
        event = self.event("issue_input", query_id=query.query_id, tick=tick)
        self.issued[query.query_id] = (query, event)
        return event

    def lookup(self, query):
        self.counts["cache_lookups"] += 1
        if query.residue_key not in self.residues:
            return None
        residue, source = self.residues[query.residue_key]
        self.counts["cache_hits"] += 1
        return int(residue == query.r), source

    def prepare(self, query, tick):
        issued = self.issued[query.query_id][1]
        residue, producer = multiply_power(query.a, query.n, query.m)
        produced = self.event("answer_produced_private", query_id=query.query_id, tick=tick)
        checked_residue, checker = square_power(query.a, query.n, query.m)
        crosscheck = pow(query.a, query.n, query.m)
        if residue != checked_residue or residue != crosscheck:
            raise AssertionError("Independent modular computations disagree.")
        checked = self.event("answer_checked_private", query_id=query.query_id, tick=tick)
        receipt = Receipt(query.query_id, query.scope, query.key, residue,
                          int(residue == query.r), issued, produced, checked,
                          tuple(sorted(producer.items())), tuple(sorted(checker.items())), True)
        self.checked[query.query_id] = receipt
        # Snapshot this canonical digest now, rather than recomputing both sides
        # from a shared live object when checking an external candidate later.
        self._registered_receipt_sha256[query.query_id] = receipt.digest
        for label, counts in (("producer", producer), ("checker", checker)):
            for key, value in counts.items():
                if key.startswith("max_"):
                    self.counts[label + "_" + key] = max(self.counts[label + "_" + key], value)
                else:
                    self.counts[label + "_" + key] += value
        self.counts["python_pow_crosscheck_calls"] += 1
        return receipt

    def admit(self, receipt, tick):
        # Dataclass equality treats True, 1, 1.0 and Fraction(1) as equal.
        # Validate exact representation types before identity/digest checks.
        if type(receipt) is not Receipt:
            raise ValueError("Use this adapter's receipt record type.")
        if (type(receipt.query_id) is not str or not receipt.query_id
                or type(receipt.scope) is not str or not receipt.scope
                or type(receipt.answer) is not int or receipt.answer not in (0, 1)
                or type(receipt.residue) is not int
                or type(receipt.python_pow_crosscheck) is not bool or not receipt.python_pow_crosscheck
                or type(tick) is not int or tick < 1):
            raise ValueError("Receipt scalar types or values are invalid.")
        if (type(receipt.claim_key) is not tuple or len(receipt.claim_key) != 5
                or type(receipt.claim_key[0]) is not str
                or any(type(value) is not int for value in receipt.claim_key[1:])):
            raise ValueError("Receipt claim key must use exact immutable field types.")
        if any(type(value) is not int or value < 0 for value in
               (receipt.issued_event, receipt.produced_event, receipt.checked_event)):
            raise ValueError("Receipt event identities must be nonnegative integers.")
        counter_names = ("loop_iterations", "max_product_bits", "modular_multiplies", "modular_reductions")
        for counters in (receipt.producer_counts, receipt.checker_counts):
            if (type(counters) is not tuple or len(counters) != len(counter_names)
                    or any(type(pair) is not tuple or len(pair) != 2
                           or type(pair[0]) is not str or type(pair[1]) is not int or pair[1] < 0
                           for pair in counters)
                    or tuple(pair[0] for pair in counters) != counter_names):
                raise ValueError("Receipt counters must be canonical immutable integer pairs.")
        entry = self.issued.get(receipt.query_id)
        if entry is None:
            raise ValueError("Receipt has no issued query.")
        query, issue_event = entry
        # Scope and the actual mathematical claim are checked before mutation.
        if receipt.scope != query.scope or receipt.claim_key != query.key:
            raise ValueError("Receipt scope or mathematical claim does not match.")
        if (not 0 <= receipt.residue < query.m or receipt.answer != int(receipt.residue == query.r)
                or tick < self.events[issue_event]["tick"]
                or self.checked.get(receipt.query_id) != receipt
                or self._registered_receipt_sha256.get(receipt.query_id) != receipt.digest
                or not issue_event < receipt.produced_event < receipt.checked_event
                or receipt.query_id in self.admitted):
            raise ValueError("Receipt is not this pending internally checked record.")
        old = self.residues.get(query.residue_key)
        if old is not None and old[0] != receipt.residue:
            raise ValueError("Conflicting exact same-scope evidence.")
        self.claims[query.key] = (receipt.answer, receipt.digest)
        self.residues[query.residue_key] = (receipt.residue, receipt.digest)
        self.admitted.add(query.query_id)
        return self.event("answer_admitted", query_id=query.query_id, tick=tick,
                          receipt_sha256=receipt.digest, answer=receipt.answer)

    def cache_fingerprint(self):
        return sha({"claims": sorted(self.claims.items()),
                    "residues": sorted(self.residues.items()),
                    "admitted": sorted(self.admitted)})

    def full_fingerprint(self):
        return sha({"issued": self.issued, "checked": self.checked,
                    "registered_receipt_sha256": self._registered_receipt_sha256,
                    "cache": self.cache_fingerprint(), "events": self.events, "counts": self.counts})


class ExpertLibrary:
    def __init__(self):
        self.moduli = Counter()
        self.residues = Counter()
        self.counts = Counter()

    def forecasts(self, query):
        base = query.a % query.m
        exact_residue = None
        if query.n == 0:
            exact_residue = 1 % query.m
        elif base == 0:
            exact_residue = 0
        elif base == 1:
            exact_residue = 1
        elif base == query.m - 1:
            exact_residue = base if query.n % 2 else 1
        shortcut = F(int(exact_residue == query.r)) if exact_residue is not None else F(1, 2)
        frequency = F(self.residues[(query.m, query.r)] + 1,
                      self.moduli[query.m] + query.m)
        fallible = F(3, 4) if (query.a + query.n + query.r) % 2 else F(1, 4)
        self.counts["calls"] += 1
        self.counts["residue_frequency_counter_lookups"] += 2
        self.counts["base_remainders"] += 1
        self.counts["fallible_parity_remainders"] += 1
        self.counts["shortcut_parity_remainders"] += int(query.n > 0 and base == query.m - 1)
        self.counts["shortcut_exact_answers"] += int(exact_residue is not None)
        return dict(zip(EXPERTS, (F(1, 2), frequency, shortcut, fallible)))

    def admit(self, query, receipt):
        self.moduli[query.m] += 1
        self.residues[(query.m, receipt.residue)] += 1


class BrierAA:
    """Binary substitution from Vovk--Zhdanov (2009), Algorithm 1/Section 5.

    Their vector Brier loss is twice our binary squared loss. We use fixed
    update rate 2/wmax and current scaled rate kappa=2*w/wmax <= 2.
    Generalized scalar losses g0,g1 give p=(1+g0-g1)/2. Log-sum-exp implements
    this in binary64. Observed per-round violations are not interval-certified.
    Idle copies receive feedback only for their own outstanding query.
    """
    def __init__(self, wmax):
        self.eta = 2.0 / float(wmax)
        self.copies = []
        self.pending = {}
        self.counts = Counter()

    def lse(self, values):
        maximum = max(values)
        self.counts["exp_calls"] += len(values)
        self.counts["log_calls"] += 1
        return maximum + math.log(math.fsum(math.exp(x - maximum) for x in values))

    def issue(self, query, experts, weight):
        index = next((i for i, c in enumerate(self.copies) if c["pending"] is None), None)
        if index is None:
            index = len(self.copies)
            self.copies.append({"logweights": [0.0] * len(EXPERTS), "pending": None, "settled": 0})
        copy = self.copies[index]
        qs = tuple(float(experts[name]) for name in EXPERTS)
        kappa = self.eta * float(weight)
        normalizer = self.lse(copy["logweights"])
        gs = tuple(-(self.lse([v - kappa * (q - y) ** 2
                              for v, q in zip(copy["logweights"], qs)]) - normalizer) / kappa
                   for y in (0, 1))
        raw = (1.0 + gs[0] - gs[1]) / 2.0
        probability = min(1.0, max(0.0, raw))
        if not math.isfinite(probability):
            raise AssertionError("Nonfinite AA report.")
        diagnostic = max(0.0, probability ** 2 - gs[0], (1 - probability) ** 2 - gs[1])
        copy["pending"] = (query, qs, float(weight))
        self.pending[query] = index
        return F.from_float(probability), {"copy": index, "generalized_losses_binary64": gs,
               "unclipped_probability_binary64": raw, "observed_mixability_slack_binary64": diagnostic,
               "numeric_bound_certified": False}

    def reveal(self, query, outcome):
        index = self.pending.pop(query)
        copy = self.copies[index]
        identity, qs, weight = copy["pending"]
        assert identity == query
        copy["logweights"] = [value - self.eta * weight * (q - outcome) ** 2
                              for value, q in zip(copy["logweights"], qs)]
        copy["settled"] += 1
        copy["pending"] = None


def action_table(tick):
    rows = (((0, 2), (1, 0)), ((0, 1), (3, 0)), ((2, 0), (0, 1)),
            ((1, 4), (3, 1)), ((4, 2), (1, 5)), ((0, 4), (2, 0)))[(tick - 1) % 6]
    return CORE.ActionTable(rows, CORE.dyadic_eta(tick))


def cases(size):
    output = []
    for name in ("recurring_shortcuts", "balanced_nonshortcut_null", "delayed_pending_tail", "varying_stakes_actions"):
        queries, generation_counts = [], Counter()
        for j in range(size):
            if j == 32:
                query = replace(queries[0]["query"], query_id=f"{name}:{j:03d}")
            else:
                modulus = (17, 19, 23, 29, 31, 37)[j % 6]
                token = int(hashlib.sha256(f"{INPUT_GENERATION_VERSION}:{name}:{j}".encode()).hexdigest(), 16)
                exponent = 1 + token % 192
                shortcut = name == "recurring_shortcuts" or (name == "delayed_pending_tail" and j % 3 == 0)
                residue_base = (0, 1, modulus - 1)[j % 3] if shortcut else 2 + (token >> 16) % (modulus - 3)
                base = residue_base + modulus * (j + 1)
                # This is deliberately outcome-balanced synthetic DEVELOPMENT
                # selection. The full public generator and its exact computation
                # cost are saved; its labels carry no distributional claim.
                result, generation = square_power(base, exponent, modulus)
                for key, value in generation.items():
                    if key.startswith("max_"):
                        generation_counts[key] = max(generation_counts[key], value)
                    else:
                        generation_counts[key] += value
                selected_answer = (token >> 32) & 1
                target = result if selected_answer else (result + 1) % modulus
                query = Query(f"{name}:{j:03d}", base, exponent, modulus, target)
            tick = j + 1
            delayed = name == "delayed_pending_tail"
            admission = tick + (0, 1, 2, 4, 7)[j % 5] if delayed else tick
            if delayed and j >= size - 8:
                admission = None
            stakes = F((1, 2, 4, 8)[j % 4]) if name in ("varying_stakes_actions", "delayed_pending_tail") else F(1)
            queries.append({"query": query, "tick": tick, "scheduled_admission_tick": admission,
                            "weight": stakes, "actions": action_table(tick)})
        output.append((name, queries, dict(generation_counts)))
    return output


def fraction_bits(value):
    if isinstance(value, F):
        return max(abs(value.numerator).bit_length(), value.denominator.bit_length())
    if hasattr(value, "__dataclass_fields__"):
        return fraction_bits(asdict(value))
    if isinstance(value, dict):
        return max((fraction_bits(v) for v in value.values()), default=0)
    if isinstance(value, (list, tuple)):
        return max((fraction_bits(v) for v in value), default=0)
    return 0


def observe_fraction_state(pool, phase, query_id, tick, counts, observations):
    """Peak exact-Fraction bit size at every committed issue/reveal boundary.

    Pending reports are included. Immutable history stores former pending
    reports, so every Fraction it retains was already observed at issue. The
    running maximum therefore covers retained history without rescanning it.
    This is not peak memory or the size of transient arithmetic intermediates.
    """
    copies = []
    for index, snapshot in enumerate(pool.copies):
        copies.append({"copy": index,
            "accumulator": fraction_bits(snapshot.accumulator),
            "pending_prediction": fraction_bits(snapshot.pending)})
    current = max([fraction_bits(pool.settings), counts["max_report_fraction_bits"]]
                  + [value for item in copies for key, value in item.items() if key != "copy"])
    peak = max(counts["peak_state_max_fraction_bits"], current)
    counts["peak_state_max_fraction_bits"] = peak
    counts["state_fraction_observations"] += 1
    observations.append({"phase": phase, "query_id": query_id, "tick": tick,
                         "settings": fraction_bits(pool.settings), "copies": copies,
                         "retained_report_max": counts["max_report_fraction_bits"],
                         "current_state_max_fraction_bits": current,
                         "peak_state_max_fraction_bits": peak})


def scored_metrics(records, method, start=1, end=None):
    settled = [r for r in records if r["outcome"] is not None and r["tick"] >= start
               and (end is None or r["tick"] <= end)]
    weight = sum((r["weight"] for r in settled), F(0))
    loss, mixed, hard = F(0), F(0), F(0)
    fixed, experts, residuals, masses = [F(0)] * 2, [F(0)] * len(EXPERTS), [F(0)] * 5, [F(0)] * 5
    for record in settled:
        report, y, w = record["reports"][method], record["outcome"], record["weight"]
        p, s, rows = report["probability"], report["action_one_probability"], record["actions"].rows
        loss += w * (p - y) ** 2
        mixed += w * ((1 - s) * rows[0][y] + s * rows[1][y])
        hard += w * rows[report["hard_action"]][y]
        for i in (0, 1):
            fixed[i] += w * rows[i][y]
        for i, name in enumerate(EXPERTS):
            experts[i] += w * (record["experts"][name] - y) ** 2
        for j in range(5):
            membership = max(F(0), 1 - abs(4 * p - j))
            masses[j] += w * membership
            residuals[j] += w * membership * (y - p)
    assert sum(masses, F(0)) == weight
    return {"settled_queries": len(settled), "settled_weight": weight,
            "positive_answers": sum(r["outcome"] for r in settled),
            "task_weighted_brier": loss, "brier_per_weight": loss / weight if weight else None,
            "expert_brier": dict(zip(EXPERTS, experts)),
            "brier_regret_each_expert": dict(zip(EXPERTS, (loss - other for other in experts))),
            "brier_regret_best_expert": loss - min(experts),
            "mixed_action_loss": mixed, "hard_action_loss": hard,
            "fixed_action_losses": fixed,
            "mixed_regret_each_fixed_action": [mixed - other for other in fixed],
            "mixed_regret_best_fixed_action": mixed - min(fixed),
            "hard_regret_best_fixed_action": hard - min(fixed),
            "calibration_bin_residuals": residuals, "calibration_bin_masses": masses,
            "calibration_residual_per_bin_mass": [r / m if m else None for r, m in zip(residuals, masses)],
            "calibration_max_absolute_residual_per_total_weight": max(map(abs, residuals)) / weight if weight else None}


def receipt_boundary_probes(evidence, pools, receipt, tick, reports, issued_hash):
    """Regression witnesses for typed local admission, not authentication."""
    def snapshot():
        states = {}
        for method, pool in pools.items():
            states[method] = {"audit": pool.audit(), "pending": pool.pending,
                "copies": [{"settings": c.settings, "accumulator": c.accumulator,
                            "pending": c.pending, "history": c.history, "used": sorted(c.used)}
                           for c in pool.copies]}
        return {"evidence": evidence.full_fingerprint(), "cores": sha(states)}

    changed_counts = tuple((key, value + int(key == "modular_multiplies"))
                           for key, value in receipt.producer_counts)
    bad = [
        ("wrong_scope_receipt", replace(receipt, scope=SCOPE + ":stale")),
        ("boolean_answer_alias", replace(receipt, answer=bool(receipt.answer))),
        ("fraction_answer_alias", replace(receipt, answer=F(receipt.answer))),
        ("float_answer_alias", replace(receipt, answer=float(receipt.answer))),
        ("fraction_residue_alias", replace(receipt, residue=F(receipt.residue))),
        ("float_residue_alias", replace(receipt, residue=float(receipt.residue))),
        ("fraction_event_alias", replace(receipt, issued_event=F(receipt.issued_event))),
        ("claim_field_numeric_alias", replace(receipt, claim_key=(receipt.scope, F(receipt.claim_key[1]),
                                                               *receipt.claim_key[2:]))),
        ("mutable_counter_dictionary", replace(receipt, producer_counts=dict(receipt.producer_counts))),
        ("integer_counter_digest_mismatch", replace(receipt, producer_counts=changed_counts)),
        ("counter_numeric_alias", replace(receipt, checker_counts=tuple((key, F(value))
                                                          for key, value in receipt.checker_counts))),
        ("changed_integer_answer", replace(receipt, answer=1 - receipt.answer)),
    ]
    results = []
    for name, candidate in bad:
        before = snapshot()
        try:
            evidence.admit(candidate, tick)
        except ValueError as exc:
            after = snapshot()
            assert before == after, "Rejected receipt changed evidence or a learner."
            assert sha(reports) == issued_hash
            results.append({"check": name, "exception": str(exc), "state_before": before,
                "state_after": after, "evidence_and_cores_unchanged": True,
                "candidate_sha256": candidate.digest, "registered_sha256": receipt.digest,
                "original_report_preserved": True})
        else:
            raise AssertionError("Malformed receipt was admitted: " + name)
    before = snapshot()
    try:
        receipt.producer_counts[0] = ("loop_iterations", -123)
    except TypeError as exc:
        assert before == snapshot()
        results.append({"check": "registered_counter_mutation", "exception": str(exc),
                        "evidence_and_cores_unchanged": True,
                        "registered_digest_unchanged": receipt.digest == evidence._registered_receipt_sha256[receipt.query_id]})
    else:
        raise AssertionError("Registered receipt counters were mutable.")
    return results


def run_case(name, units, generation_counts):
    evidence, library = Evidence(), ExpertLibrary()
    pools = {method: CORE.DelayedPool(EXPERTS, scope=SCOPE, decision_features=method.endswith("with_decision"))
             for method in METHODS[:4]}
    aa = BrierAA(max(u["weight"] for u in units))
    records, by_id, scheduled = [], {}, {}
    method_counts = {method: Counter() for method in METHODS}
    state_observations = {method: [] for method in pools}
    for method, pool in pools.items():
        observe_fraction_state(pool, "initial", None, 0, method_counts[method], state_observations[method])
    rejected = []
    for unit in units:
        query, tick, actions, weight = unit["query"], unit["tick"], unit["actions"], unit["weight"]
        evidence.register(query, tick)
        known = evidence.lookup(query)
        experts = ({expert: F(known[0]) for expert in EXPERTS} if known else library.forecasts(query))
        reports = {}
        for method in METHODS:
            started = time.perf_counter_ns()
            counts = method_counts[method]
            counts["issued_reports"] += 1
            counts["input_bits_total"] += input_bits(query.a, query.n, query.m, query.r)
            counts["input_bits_max"] = max(counts["input_bits_max"], input_bits(query.a, query.n, query.m, query.r))
            detail = {}
            if known:
                p = F(known[0])
                route = "admitted_exact_residue_cache"
                detail = {"source_receipt_sha256": known[1], "modular_multiplies": 0}
                counts["cache_hits"] += 1
            elif method in pools:
                prediction = pools[method].issue(query.query_id, experts, weight,
                    tolerance=F(1, 4096), actions=actions if method.endswith("with_decision") else None)
                p, route = prediction.probability, "unknown_scalar_forecast"
                detail = {"core_prediction": prediction, "copy": pools[method].pending[query.query_id]}
                counts["score_evaluations"] += prediction.score_evaluations
                counts["bisections"] += prediction.bisections
                counts["unmet_root_tolerances"] += int(not prediction.tolerance_met)
                counts["max_report_fraction_bits"] = max(counts["max_report_fraction_bits"], fraction_bits(prediction))
            elif method == "ordinary_brier_aa_binary64":
                p, detail = aa.issue(query.query_id, experts, weight)
                route = "unknown_brier_aa_forecast"
            else:
                residue, detail = square_power(query.a, query.n, query.m)
                p, route = F(int(residue == query.r)), "ordinary_exact_computation"
                for key, value in detail.items():
                    if key.startswith("max_"):
                        counts[key] = max(counts[key], value)
                    else:
                        counts[key] += value
            costs = actions.forecast_costs(p)
            hard = int(costs[1] < costs[0])
            mix = F(hard) if known or method == "ordinary_fast_exact" else actions.mix(p)
            reports[method] = {"report_version": "issued-v1", "probability": p,
                "action_one_probability": mix, "forecast_action_costs": costs,
                "hard_action": hard, "route": route, "detail": detail}
            counts["issue_wall_ns"] += time.perf_counter_ns() - started
            if method in pools:
                observe_fraction_state(pools[method], "after_issue", query.query_id, tick,
                                       counts, state_observations[method])
        for left, right in ((METHODS[0], METHODS[2]), (METHODS[1], METHODS[3])):
            assert reports[left] == reports[right], "Matched same-core adapters diverged."
        issued_hash = sha(reports)
        evidence.event("all_reports_committed", query_id=query.query_id, tick=tick,
                       reports_sha256=issued_hash)
        record = {**unit, "experts": experts, "reports": reports, "issued_reports_sha256": issued_hash,
                  "outcome": known[0] if known else None,
                  "admission_tick": tick if known else None,
                  "receipt": None, "status": "known_at_issue" if known else "pending",
                  "interpretations": [{"version": "issue-v1", "meaning": "immutable historical forecast",
                       "known_answer_source": known[1] if known else None}]}
        records.append(record)
        by_id[query.query_id] = record
        if known:
            assert query.key in evidence.claims or query.residue_key in evidence.residues
        else:
            receipt = evidence.prepare(query, tick)
            record["receipt"] = {"record": receipt, "sha256": receipt.digest,
                                 "admitted": False, "authentication_claim": False}
            if tick == 1:
                rejected.extend(receipt_boundary_probes(evidence, pools, receipt, tick, reports, issued_hash))
            admission = unit["scheduled_admission_tick"]
            if admission is not None:
                scheduled.setdefault(admission, []).append(query.query_id)
        # Admission is an END-of-tick event, always after this tick's reports.
        for identity in scheduled.pop(tick, []):
            earlier = by_id[identity]
            receipt = earlier["receipt"]["record"]
            event = evidence.admit(receipt, tick)
            for method, pool in pools.items():
                started = time.perf_counter_ns()
                pool.reveal(identity, receipt.answer, scope=SCOPE)
                method_counts[method]["reveal_wall_ns"] += time.perf_counter_ns() - started
                observe_fraction_state(pool, "after_reveal", identity, tick,
                                       method_counts[method], state_observations[method])
            started = time.perf_counter_ns()
            aa.reveal(identity, receipt.answer)
            method_counts["ordinary_brier_aa_binary64"]["reveal_wall_ns"] += time.perf_counter_ns() - started
            library.admit(earlier["query"], receipt)
            earlier["outcome"], earlier["admission_tick"] = receipt.answer, tick
            earlier["status"] = "admitted_after_issue"
            earlier["receipt"]["admitted"] = True
            earlier["interpretations"].append({"version": "admitted-v1", "admission_event": event,
                "exact_answer": receipt.answer, "source_receipt_sha256": receipt.digest,
                "replaces_issued_forecast": False})
            assert sha(earlier["reports"]) == earlier["issued_reports_sha256"]
    metrics, audits = {}, {}
    for method in METHODS:
        metrics[method] = {"all_admitted": scored_metrics(records, method),
                           "startup_issues_1_to_32": scored_metrics(records, method, end=32),
                           "later_issues_33_onward": scored_metrics(records, method, start=33)}
        if method in pools:
            pool, audit = pools[method], pools[method].audit()
            history = tuple(obs for copy in pool.copies for obs in copy.history)
            assert len(history) == audit["settled"]
            assert set(pool.pending) == {r["query"].query_id for r in records if r["status"] == "pending"}
            reported_allowance = sum((obs.prediction.allowance for obs in history), F(0))
            pending_allowance = sum((copy.pending.allowance for copy in pool.copies if copy.pending), F(0))
            root = CORE.sqrt_upper(audit["bound_squared"])
            audits[method] = {"pool": audit, "settled_root_allowance": reported_allowance,
                "pending_reported_allowance": pending_allowance,
                "certified_brier_regret_upper": 2 * root,
                "certified_calibration_absolute_residual_upper": root,
                "certified_mixed_action_regret_upper": (audit["smoothing_slack"] + root
                    if pool.settings.decision_features else None),
                "cache_extension": "zero Brier and calibration residual; nonpositive regret to each fixed action"}
            measure = metrics[method]["all_admitted"]
            assert measure["task_weighted_brier"] == audit["own_loss"]
            assert measure["brier_regret_best_expert"] <= 2 * root
            assert max(map(abs, measure["calibration_bin_residuals"])) <= root
            if pool.settings.decision_features:
                assert measure["mixed_regret_best_fixed_action"] <= audit["smoothing_slack"] + root
            method_counts[method]["final_accumulator_max_fraction_bits"] = max(
                (fraction_bits(copy.accumulator) for copy in pool.copies), default=0)
            method_counts[method]["final_state_max_fraction_bits"] = max(
                [fraction_bits(pool.settings)] + [fraction_bits(copy) for copy in pool.copies])
            assert method_counts[method]["peak_state_max_fraction_bits"] >= method_counts[method]["final_state_max_fraction_bits"]
            assert method_counts[method]["state_fraction_observations"] == 1 + len(records) + audit["settled"]
            assert method_counts[method]["peak_state_max_fraction_bits"] == max(
                observation["current_state_max_fraction_bits"] for observation in state_observations[method])
            method_counts[method]["max_simultaneous_copies"] = len(pool.copies)
        if method != "ordinary_fast_exact":
            # Standalone accounting assigns each consumer the shared library
            # work; this harness actually evaluates that library once per issue.
            for key, value in library.counts.items():
                method_counts[method]["assigned_shared_expert_" + key] = value
    assert metrics[METHODS[0]] == metrics[METHODS[2]]
    assert metrics[METHODS[1]] == metrics[METHODS[3]]
    for record in records:
        assert sha(record["reports"]) == record["issued_reports_sha256"]
    assert records[32]["status"] == "known_at_issue"
    assert records[32]["query"].key == records[0]["query"].key
    assert records[32]["query"].query_id != records[0]["query"].query_id
    # All computations are allowed; exact baseline succeeds even on the null.
    assert metrics["ordinary_fast_exact"]["all_admitted"]["task_weighted_brier"] == 0
    aa_diagnostics = [r["reports"][METHODS[4]]["detail"].get("observed_mixability_slack_binary64", 0.0)
                      for r in records]
    return {"case": name, "queries": len(records), "records": records, "events": evidence.events,
            "metrics": metrics, "core_audits": audits, "resource_counters": method_counts,
            "state_fraction_bit_observations": state_observations,
            "state_fraction_metric_scope": "maximum numerator/denominator bits of Fractions in committed settings, accumulators, pending reports, and retained immutable reports; every issue/reveal boundary; not transient arithmetic or peak RAM",
            "shared_expert_actual_counters": library.counts, "evidence_counters": evidence.counts,
            "input_generation_counts": generation_counts, "rejected_receipts": rejected,
            "cache_checks": {"fresh_id_same_claim_exact": True, "original_reports_immutable": True,
                             "same_scope_residue_entailment_enabled": True},
            "matched_k29_equivalence": "identical implementation and exact reports, not independent reconstruction",
            "aa_numeric": {"source": AA_SOURCE, "source_sections": "Section 2 Algorithm 1/Theorem 1; Section 5",
               "numeric_bound_certified": False, "maximum_observed_mixability_slack": max(aa_diagnostics),
               "transcendental_calls": dict(aa.counts), "copies": len(aa.copies),
               "ideal_exact_real_regret_constant_per_settled_copy": math.log(len(EXPERTS)) / aa.eta,
               "ideal_constant_is_not_an_implementation_certificate": True},
            "pending_ids": [r["query"].query_id for r in records if r["status"] == "pending"],
            "unreached_scheduled_admissions": scheduled}


def decimal(value):
    return f"{float(value):.6f}"


def report_text(results):
    lines = ["# P3-06 mathematical-query development", "",
        "Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.", "",
        "Version 3 repairs receipt representation checks: Boolean/float/Fraction integer aliases are rejected,",
        "counter pairs are immutable, and a digest fixed at receipt registration is checked before admission",
        "mutates any evidence. Version 2 source bytes and output remain under `mathematical_queries_v2/source_snapshot`.",
        "Malformed-receipt probes verify that both evidence and every scalar learner remain unchanged; valid",
        "admission still follows. These checks do not authenticate arbitrary external proofs or software.", "",
        "Version 2 corrects resource instrumentation while retaining version 1's exact input-generation identifier.",
        "Version 1 source bytes and output remain preserved under `mathematical_queries_v1/source_snapshot`.",
        "The old `max_state_fraction_bits` was the maximum over final accumulators, not a temporal peak.",
        "Version 2 separately reports final accumulator size, final complete state size, and a peak measured after",
        "every issue and reveal. Pending predictions are included; retained immutable reports were measured when",
        "issued. Per-boundary observations are saved. This measures Fraction numerator/denominator bit sizes,",
        "not RAM use or temporary arithmetic intermediates. No new population or parameter choice is introduced.", "",
        "This is a bounded development run. It neither freezes a final challenge nor selects paid computation.",
        "Subagent research time is unmeasured and contributes zero principal Research90 credit.", "",
        "## Declared contract", "",
        "Queries ask whether `(a**n mod m) == r`, with `0 <= a <= 8191`, `0 <= n <= 192`,",
        "`2 <= m <= 97`, and `0 <= r < m`. Inputs and issue-time weights/loss tables are saved.",
        "The full generator intentionally selects roughly balanced true/false queries using exact arithmetic.",
        "Its selection rule and computation are public and charged in generation counters; these are synthetic cases,",
        "not a claim about a natural mathematical-query distribution or an unpredictable outcome process.", "",
        "The null family excludes the partial shortcut's applicable bases and is null only relative to the declared",
        "small heuristic library. Its public generator is itself exploitable by an ordinary predictor that knows",
        "the case and index. No hidden-source advantage, distributional difficulty, or useful-expert guarantee is claimed.", "",
        "Every fresh unknown claim is reported before repeated-multiplication production and an independent binary",
        "square-and-multiply check. Python `pow` supplies an additional ordinary cross-check. Checked receipts are",
        "withheld from the learners until end-of-tick scheduled admission. Pending tail answers are saved for",
        "reproduction but never admitted, used in expert history, or included in reported scores. This is local",
        "deterministic checking, without a formal-proof or receipt-authentication claim.", "",
        "A same-scope admitted residue entails every target equality for those exact exponentiation inputs.",
        "The cached duplicate at issue 33 has a fresh ID but receives its known exact probability and exact action",
        "costs. No learner state is created for that request. Historical forecasts retain their original hashes;",
        "admission adds a separately versioned exact interpretation. A wrong-scope receipt is rejected without",
        "changing the evidence cache. No malformed external evidence is being certified by this small check.", "",
        "## Methods and accounting", "",
        "Four expert reports are available to each learned method: constant one half, a Laplace-smoothed admitted",
        "residue frequency by modulus, an exact partial shortcut for bases congruent to 0, 1, or minus 1 (and",
        "exponent zero), and a deliberately fallible parity heuristic. The scope cache wraps all these reports",
        "equally on already known claims. No expert receives a withheld answer. The exact modular-power baseline",
        "may compute every new query immediately; its answer is not passed to other methods before admission.", "",
        "Each scalar configuration is compared with an ordinary K29 adapter using the same features and identical",
        "core. Their equality is intentional and checked report by report; it is not independent validation.",
        "The decision configuration adds the two continuous exposure-difference features, with dyadic positive",
        "smoothing. Mixed losses are expected losses of this declared action mixture; hard-action losses are",
        "recorded separately and do not inherit that guarantee. Costs and weights vary according to public schedules.", "",
        f"The score-only baseline implements the binary specialization of [Vovk and Zhdanov's Brier AA]({AA_SOURCE}),",
        "JMLR 2009, Section 2 Algorithm 1/Theorem 1 and Section 5. The source's vector Brier loss equals twice",
        "our scalar squared loss. For a declared maximum stake, the fixed exponent-update rate is twice its",
        "reciprocal; the current weighted generalized losses use the corresponding scaled rate. Binary substitution",
        "uses `(1 + g0 - g1)/2`. Binary64 log/exp and clipping are logged. The ideal real-arithmetic constant",
        "regret is a source/reference comparison, not a certified guarantee for these floating outputs.", "",
        "Primitive modular multiplication/reduction counts are separate for production, checking, generation and",
        "the ordinary exact solver. The checker and solver independently run the binary algorithm. Python `pow`",
        "calls are counted but their internal multiplication counts are unknown. Core score evaluations, bisections,",
        "fraction bit lengths, copy counts and observed call wall times are recorded; these are not hard time or",
        "memory caps. Shared expert work is actually performed once and assigned to each learned method for a",
        "standalone comparison. Hashing, serialization, interpreter overhead and total memory are not fully metered.", "",
        "## Results", "",
        "All scores below use admitted queries only, including known-cache requests. Regret compares a fixed expert",
        "or fixed action index over the same issue-time weights. Negative action regret is legitimate. Exact values,",
        "the five calibration bin residuals and their masses, reported root allowances, and startup/later splits",
        "are in each case JSON. Rounded numbers here do not replace those exact records.", "",
        "| Case / method | Admitted / pending | Weight | Brier / weight | Regret to best expert | Mixed regret | Hard regret |",
        "|---|---:|---:|---:|---:|---:|---:|"]
    for result in results:
        for method in (METHODS[0], METHODS[1], METHODS[4], METHODS[5]):
            m = result["metrics"][method]["all_admitted"]
            lines.append(f"| {result['case']} / {method} | {m['settled_queries']} / {len(result['pending_ids'])} | "
                         f"{decimal(m['settled_weight'])} | {decimal(m['brier_per_weight'])} | "
                         f"{decimal(m['brier_regret_best_expert'])} | {decimal(m['mixed_regret_best_fixed_action'])} | "
                         f"{decimal(m['hard_regret_best_fixed_action'])} |")
    lines += ["", "The matched ordinary K29 rows are omitted from this display because every issued report and all",
              "metrics equal their scalar counterpart exactly. The JSON retains all six method records.", "",
              "## Interpretation and limits", "",
              "The exact solver incurs zero Brier loss on every admitted case and remains available throughout.",
              "This small arithmetic domain therefore supplies no evidence that fallible forecasting is preferable",
              "to ordinary exact computation at these budgets. The question tested is whether the forecast adapter",
              "preserves scope, chronology, expert comparisons, action accounting and residual certificates when",
              "fresh deterministic answers arrive on a delay schedule. The current comparisons do not establish",
              "a practical win, broad mathematical learning, or a contribution-gate result.", "",
              "Finite success of the scalar inequalities is checked against the exact audit; it does not establish",
              "asymptotic convergence on these short cases. Calibration ratios require their own positive bin",
              "mass, and pending forecasts are excluded rather than assigned fabricated outcomes. Larger decision",
              "feature norms and more simultaneous copies can enlarge a correct but loose bound.", "",
              "Issue-index startup and later summaries are descriptive, not selected test endpoints. No final",
              "evaluation population, final controls, paid computation policy, or freeze is created here.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--queries", type=int, default=128)
    args = parser.parse_args()
    if not 96 <= args.queries <= 192:
        parser.error("Development cases must contain 96..192 issued queries.")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    manifest = {"version": VERSION, "core_version": CORE.VERSION, "scope": SCOPE,
        "input_generation_version": INPUT_GENERATION_VERSION,
        "instrumentation_revision": "temporal peak includes pending predictions and retained immutable reports at all committed issue/reveal boundaries",
        "receipt_revision": "strict scalar/canonical immutable-counter types and registration-time digest; rejected-call evidence/core fingerprints",
        "python": platform.python_version(), "implementation": platform.python_implementation(),
        "stage": "development_not_frozen", "queries_per_case": args.queries,
        "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (HERE, CORE_PATH)},
        "clock_credit": "unmeasured subagent; zero principal Research90 credit",
        "command": [sys.executable, str(HERE.relative_to(ROOT)), "--queries", str(args.queries), "--output", str(output)],
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "running", "completed_cases": []}
    dump(output / "manifest.json", manifest)
    started = time.perf_counter_ns()
    results = []
    try:
        for name, units, generation in cases(args.queries):
            result = run_case(name, units, generation)
            results.append(result)
            dump(output / (name + ".json"), result)
            manifest["completed_cases"].append(name)
            dump(output / "manifest.json", manifest)
            print(json.dumps({"case": name, "queries": result["queries"],
                              "pending": len(result["pending_ids"]), "checks": "passed"}), flush=True)
        (output / "REPORT.md").write_text(report_text(results))
        manifest["status"] = "completed"
        manifest["elapsed_wall_ns"] = time.perf_counter_ns() - started
        manifest["artifacts_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                      for p in sorted(output.iterdir()) if p.name != "manifest.json"}
        dump(output / "manifest.json", manifest)
    except BaseException as exc:
        manifest["status"] = "failed"
        manifest["elapsed_wall_ns"] = time.perf_counter_ns() - started
        dump(output / "failure.json", {"type": type(exc).__name__, "message": str(exc),
                                       "traceback": traceback.format_exc()})
        dump(output / "manifest.json", manifest)
        raise


if __name__ == "__main__":
    main()
