"""P3-07 finite paired-profile controller, DEVELOPMENT ONLY.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.

This module implements the finite cohort certificate, not a conditional truth
oracle for the current mathematical query. Complete policies are fixed. The
controller chooses one for a batch under a constant price vector. A reset
episode, all initial state and the sampling contract are part of its binding.

The operation model has bounded rational arithmetic primitives (at most 2048
bits per component), scalar comparisons, and 64-bit storage words. It is not
Python elapsed-time accounting. Prepaid finite bundles cover the bounded
loops described below; the ordinary controller gets exactly the same model.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from math import isqrt
from pathlib import Path
import sys

_NAME = "_p307_modular_adapter"
if _NAME in sys.modules:
    A = sys.modules[_NAME]
else:
    _spec = spec_from_file_location(_NAME, Path(__file__).with_name("07_computation_adapter.py"))
    A = module_from_spec(_spec)
    sys.modules[_NAME] = A
    _spec.loader.exec_module(A)

VERSION = "p307-paired-profile-controller-v2"
FEATURE_VERSION = "fp-fn-fallback-and-eleven-resource-categories-v1"
MAX_POLICIES, MAX_FEATURES, MAX_ROWS = 16, 32, 8192
MAX_PRICE_BITS, MAX_ARITHMETIC_BITS = 32, 2048
MAX_HORIZON, MAX_CHECKPOINTS, RADIUS_BITS = 10000, 16, 16
POLICY_BUDGET = 1024
MAX_SETUP_BITS = 256
PROFILE_WORD_BOUND = 8192
SCOPE_WORD_BOUND = 320
SELECT_FINAL_UNITS = 256
CANCEL_RESERVE = 65
FEATURES = ("false_positive", "false_negative", "fallback") + tuple(
    "resource_" + k for k in A.CATEGORIES)


class Rejected(ValueError):
    pass


def exact(v, *, price=False):
    if type(v) not in (int, F):
        raise Rejected("Exact int/Fraction required; no bool or float.")
    q = F(v)
    cap = MAX_PRICE_BITS if price else MAX_ARITHMETIC_BITS
    if max(abs(q.numerator).bit_length(), q.denominator.bit_length()) > cap:
        raise Rejected("Rational component exceeds the declared primitive cap.")
    return q


def nat(v, limit, label):
    if type(v) is not int or not 0 <= v <= limit:
        raise Rejected("Invalid bounded integer: " + label)
    return v


def label(v, cap=64):
    if type(v) is not str or not 1 <= len(v) <= cap or not v.isascii():
        raise Rejected("An exact, nonempty, capped ASCII identity is required.")
    return v


def merged_meter(meters, limit):
    """Harness-only aggregation of disjoint prepaid budget partitions."""
    by_category, operations, max_bits = Counter(), Counter(), Counter()
    for meter in meters:
        by_category.update(meter.by_category)
        operations.update(meter.operations)
        for category, bits in meter.max_operand_bits.items():
            max_bits[category] = max(max_bits[category], bits)
    total = sum(m.total for m in meters)
    assert total <= sum(m.limit_total for m in meters) <= limit
    return dict(version=VERSION, limit_total=limit, total=total,
                remaining=limit-total, by_category=dict(by_category),
                category_limits={c: limit for c in A.CATEGORIES},
                operations=dict(sorted(operations.items())),
                max_operand_bits=dict(max_bits), events=sum(len(m.events) for m in meters),
                denials=sum(m.denials for m in meters),
                last_denial=next((m.last_denial for m in reversed(meters) if m.last_denial), None),
                partitions=[m.snapshot() for m in meters])


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def digest(value):
    """Harness/registry helper; construction and reading are separately charged."""
    return sha256(canonical(value).encode()).hexdigest()


@dataclass(frozen=True)
class Policy:
    name: str
    transactions: int
    unresolved_action: int | None

    def __post_init__(self):
        label(self.name)
        nat(self.transactions, A.MAX_FULL_TRANSACTIONS, "transaction cap")
        if self.unresolved_action is not None and (
                type(self.unresolved_action) is not int or self.unresolved_action not in (0, 1)):
            raise Rejected("Terminal action must be 0, 1, or fallback.")

    def record(self):
        return {"name": self.name, "transactions": self.transactions,
                "unresolved_action": self.unresolved_action}


CATALOGUE = (
    Policy("fallback", 0, None), Policy("guess0", 0, 0),
    Policy("guess1", 0, 1), Policy("cap6_fallback", 6, None),
    Policy("cap12_fallback", 12, None),
    Policy("full_fallback", A.MAX_FULL_TRANSACTIONS, None),
)


@dataclass(frozen=True)
class Scope:
    controller: str
    adapter: str
    catalogue: str
    features: str
    law: str
    initial_state: str
    sampler_contract: str
    schedule: str

    def __post_init__(self):
        for v in self.record().values():
            label(v, 256)

    def record(self):
        return dict(self.__dict__)


def modular_scope(law):
    return Scope(VERSION, A.VERSION, digest([p.record() for p in CATALOGUE]),
                 FEATURE_VERSION, law, "cold-per-query;cache_cap=0;no-pending-jobs",
                 "iid-with-replacement-model;seeded-development-trace-labelled",
                 "whole-fixed-policy;no-unacquired-feedback;constant-price-per-batch")


def run_policy(query, policy, *, limit=POLICY_BUDGET):
    """Execute one real bounded policy; the return contains no scoring label.

    One terminal-output unit is reserved before any optional work. On a denied
    operation/timeout, already paid costs remain and the declared unresolved
    action is emitted. Every policy gets the same initial report, exact-cache
    lookup, and public shortcut. No profile or future truth is consulted here.
    """
    if type(query) is not A.Query or type(policy) is not Policy:
        raise Rejected("Exact query and immutable complete policy required.")
    nat(limit, POLICY_BUDGET, "response budget")
    # Reserve bounded cancellation through the public API, and terminal output.
    # A low budget never opens a job it cannot subsequently release.
    cleanup_budget = CANCEL_RESERVE if limit > CANCEL_RESERVE else 0
    output_budget = int(limit > 0)
    meter = A.Meter(max(0, limit - cleanup_budget - output_budget))
    cleanup = A.Meter(cleanup_budget)
    output = A.Meter(output_budget)
    adapter = A.Adapter(meter, cache_cap=0)
    answer, progress, status = None, None, "unresolved"
    initial_report, handle = None, None
    try:
        meter.pay("forecast", "issue_known_half_report", 1)
        initial_report = F(1, 2)
        answer = adapter.lookup(query)
        if answer is None:
            answer = adapter.shortcut(query)
        if answer is None and policy.transactions and cleanup_budget:
            handle = adapter.start(query)
            progress = adapter.advance(handle, policy.transactions)
            if progress.checked_ready:
                answer = adapter.acquire(handle)
                handle = None  # acquire atomically funds and releases the job
            else:
                status = "budget_exhausted" if progress.budget_exhausted else "transaction_timeout"
        if answer is not None:
            status = "checked_answer"
    except A.BudgetExhausted:
        status = "budget_exhausted"
    finally:
        if handle is not None:
            adapter.meter = cleanup
            adapter.cancel(handle)
            handle = None
    action = answer.answer if answer is not None else policy.unresolved_action
    if output_budget:
        output.pay("forecast", "emit_terminal_action", 1)
    else:
        action, status = None, "no_output_budget"
    snapshot = merged_meter((meter, cleanup, output), limit)
    return {"policy": policy.name, "initial_report": None if initial_report is None else str(initial_report),
            "action": action, "status": status, "meter": snapshot,
            "answer": answer.record() if answer else None,
            "progress": None if progress is None else dict(progress.__dict__)}


def features_from_checked_label(result, label):
    """Profiling/audit function only: label must come from paid checked evidence."""
    if type(label) is not int or label not in (0, 1):
        raise Rejected("A checked binary scoring label is required.")
    action = result["action"]
    return (int(action == 1 and label == 0), int(action == 0 and label == 1),
            int(action is None)) + tuple(result["meter"]["by_category"][k] for k in A.CATEGORIES)


def paired_ranges(policy):
    """Analytic ranges relative to the fixed fallback complete policy.

    Public prefix and terminal emission are identical. A non-guessing policy
    either obtains a checked correct answer or falls back, so FP/FN are zero.
    Optional adapter work only adds resource use. Whole-response cap 1024 is
    conservative for every one of its individual resource categories.
    """
    if policy == CATALOGUE[0]:
        return ((0, 0),) * len(FEATURES)
    fp = (-1, 0) if policy.unresolved_action == 1 else (0, 0)
    fn = (-1, 0) if policy.unresolved_action == 0 else (0, 0)
    resource = []
    used = {"admission", "solve", "check", "acquisition", "storage"}
    for category in A.CATEGORIES:
        resource.append((-POLICY_BUDGET, 0) if policy.transactions and category in used else (0, 0))
    return (fp, fn, (0, 1)) + tuple(resource)


def certified_radius(n, cells, delta, checkpoints, meter):
    nat(n, MAX_ROWS, "profile rows")
    nat(cells, MAX_POLICIES * MAX_FEATURES, "nonconstant cells")
    nat(checkpoints, MAX_CHECKPOINTS, "fixed checkpoint count")
    delta = exact(delta, price=True)
    if not n or not checkpoints or not 0 < delta < 1:
        raise Rejected("Positive sample/checkpoint count and delta in (0,1) required.")
    # <=64 rounds for capped inputs; <=64-bit radius integer arithmetic.
    meter.pay("assessment", "radius_integer_bound_bundle", 160)
    k = 0
    while 2 * max(1, cells) * checkpoints * delta.denominator > delta.numerator * (1 << k):
        k += 1
        if k > 64:
            raise Rejected("Confidence construction exceeds the fixed arithmetic bound.")
    numerator = k * (1 << (2 * RADIUS_BITS))
    denominator = 2 * n
    target = (numerator + denominator - 1) // denominator
    root = isqrt(target)
    if root * root < target:
        root += 1
    r = F(root, 1 << RADIUS_BITS)
    assert 2 * n * r * r >= k
    assert F(2 * max(1, cells) * checkpoints, 1 << k) <= delta
    return r, k


@dataclass(frozen=True)
class Profile:
    scope: Scope
    names: tuple[str, ...]
    feature_names: tuple[str, ...]
    ranges: tuple[tuple[tuple[int, int], ...], ...]
    sums: tuple[tuple[int, ...], ...]
    n: int
    checkpoints: tuple[int, ...]
    delta: F
    setup_resources: tuple[int, ...]
    _identity: str = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        if type(self.scope) is not Scope or type(self.names) is not tuple or not 1 <= len(self.names) <= MAX_POLICIES:
            raise Rejected("Invalid immutable profile scope/catalogue.")
        for name in self.names:
            label(name)
        if len(set(self.names)) != len(self.names):
            raise Rejected("Unique bounded policy identities required.")
        if type(self.feature_names) is not tuple or not 1 <= len(self.feature_names) <= MAX_FEATURES:
            raise Rejected("Distinct immutable feature identities required.")
        for name in self.feature_names:
            label(name)
        if len(set(self.feature_names)) != len(self.feature_names):
            raise Rejected("Distinct immutable feature identities required.")
        nat(self.n, MAX_ROWS, "profile count")
        if not self.n:
            raise Rejected("An empty profile cannot certify a mean.")
        if type(self.checkpoints) is not tuple or not 1 <= len(self.checkpoints) <= MAX_CHECKPOINTS:
            raise Rejected("A fixed finite checkpoint tuple is required.")
        for n in self.checkpoints:
            nat(n, MAX_ROWS, "checkpoint")
            if not n:
                raise Rejected("Checkpoints must be positive.")
        if tuple(sorted(set(self.checkpoints))) != self.checkpoints or self.n not in self.checkpoints:
            raise Rejected("Count must be a member of the predeclared distinct ordered checkpoints.")
        if not 0 < exact(self.delta, price=True) < 1:
            raise Rejected("Invalid profile error probability.")
        if type(self.ranges) is not tuple or type(self.sums) is not tuple or len(self.ranges) != len(self.names) or len(self.sums) != len(self.names):
            raise Rejected("Profile matrix shape mismatch.")
        for bounds, row in zip(self.ranges, self.sums):
            if type(bounds) is not tuple or type(row) is not tuple or len(bounds) != len(self.feature_names) or len(row) != len(bounds):
                raise Rejected("Profile rows must be immutable and match feature count.")
            for interval, value in zip(bounds, row):
                if type(interval) is not tuple or len(interval) != 2 or any(type(x) is not int or abs(x) > 1_000_000 for x in interval):
                    raise Rejected("Invalid finite integer feature range.")
                lo, hi = interval
                if lo > hi or type(value) is not int or not self.n * lo <= value <= self.n * hi:
                    raise Rejected("Profile sum violates its declared feature range.")
        if type(self.setup_resources) is not tuple or len(self.setup_resources) != len(A.CATEGORIES):
            raise Rejected("Complete setup resource vector required.")
        for v in self.setup_resources:
            nat(v, 10**12, "setup resource quantity")
        encoded = canonical(self.record()).encode("ascii")
        if len(encoded) > 8 * PROFILE_WORD_BOUND:
            raise Rejected("Profile exceeds the paid bounded serialization envelope.")
        # Construction is paid by freeze(); direct input construction is an
        # external evidence-provider action. Receiving code pays validation.
        object.__setattr__(self, "_identity", sha256(encoded).hexdigest())

    def record(self):
        return {"scope": self.scope.record(), "names": self.names,
                "feature_names": self.feature_names, "ranges": self.ranges,
                "sums": self.sums, "n": self.n, "checkpoints": self.checkpoints,
                "delta": str(self.delta), "setup_resources": self.setup_resources}

    @property
    def identity(self):
        return self._identity


class ProfileBuilder:
    """Fixed catalogue full-information sums; no profile receives future labels."""
    def __init__(self, scope, names, feature_names, ranges, checkpoints, delta, meter):
        meter.pay("profile", "builder_bounded_metadata_admission", PROFILE_WORD_BOUND)
        if type(names) is not tuple or not 1 <= len(names) <= MAX_POLICIES or type(feature_names) is not tuple or not 1 <= len(feature_names) <= MAX_FEATURES:
            raise Rejected("Builder dimensions must be bounded before allocation.")
        if type(checkpoints) is not tuple or not 1 <= len(checkpoints) <= MAX_CHECKPOINTS:
            raise Rejected("Builder requires bounded checkpoints before iteration.")
        for n in checkpoints:
            nat(n, MAX_ROWS, "checkpoint")
            if not n:
                raise Rejected("Checkpoint must be positive.")
        # Reuse the complete immutable structural validator with an in-range
        # dummy sum; its temporary bounded allocation is paid above.
        if type(ranges) is not tuple or len(ranges) != len(names):
            raise Rejected("Builder range matrix must match its capped catalogue.")
        for row in ranges:
            if type(row) is not tuple or len(row) != len(feature_names):
                raise Rejected("Builder range row shape mismatch.")
            for interval in row:
                if type(interval) is not tuple or len(interval) != 2 or any(type(x) is not int or abs(x) > 1_000_000 for x in interval) or interval[0] > interval[1]:
                    raise Rejected("Builder requires bounded integer ranges.")
        Profile(scope, names, feature_names, ranges,
                tuple(tuple(checkpoints[0] * lo for lo, hi in row) for row in ranges),
                checkpoints[0], checkpoints, exact(delta, price=True), (0,) * len(A.CATEGORIES))
        self.scope, self.names, self.feature_names = scope, names, feature_names
        self.ranges, self.checkpoints, self.delta = ranges, checkpoints, exact(delta)
        self.sums = [[0] * len(feature_names) for _ in names]
        self.n = 0

    def add(self, paired_rows, meter):
        if self.n >= max(self.checkpoints) or type(paired_rows) is not tuple or len(paired_rows) != len(self.names):
            raise Rejected("Profile hard cap or row count mismatch.")
        cells = len(self.names) * len(self.feature_names)
        # Fund admitted row work before inspecting any cell. No partial update
        # occurs when a later cell is rejected, but already spent cost remains.
        meter.pay_many((("profile", "paired_cell_check_add", 3 * cells),
                        ("storage", "paired_cell_read_write", 2 * cells),
                        ("profile", "profile_count_increment", 1)))
        for bounds, row in zip(self.ranges, paired_rows):
            if type(row) is not tuple or len(row) != len(bounds):
                raise Rejected("Full immutable paired row required.")
            for (lo, hi), v in zip(bounds, row):
                if type(v) is not int or not lo <= v <= hi:
                    raise Rejected("Observed feature violates the frozen range.")
        for i, row in enumerate(paired_rows):
            for j, v in enumerate(row):
                self.sums[i][j] += v
        self.n += 1

    def freeze(self, meter, external_resources=None):
        external_resources = (0,) * len(A.CATEGORIES) if external_resources is None else external_resources
        meter.pay_many((("profile", "freeze_validate_copy_and_hash_words", 2 * PROFILE_WORD_BOUND),
                        ("storage", "freeze_retained_profile_words", PROFILE_WORD_BOUND)))
        if type(external_resources) is not tuple or len(external_resources) != len(A.CATEGORIES):
            raise Rejected("Freeze requires its complete external resource vector.")
        for v in external_resources:
            nat(v, 10**12, "external setup quantity")
        setup_resources = tuple(v + meter.by_category[c] for c, v in zip(A.CATEGORIES, external_resources))
        return Profile(self.scope, self.names, self.feature_names, self.ranges,
                       tuple(tuple(row) for row in self.sums), self.n,
                       self.checkpoints, self.delta, tuple(setup_resources))


def profile_intervals(profile, expected_scope, meter):
    if type(profile) is not Profile or type(expected_scope) is not Scope:
        raise Rejected("Exact immutable profile and independently supplied scope required.")
    # Identity metadata is compared before any old result is used.
    meter.pay("assessment", "scope_word_comparison", 2 * SCOPE_WORD_BOUND)
    if profile.scope != expected_scope:
        raise Rejected("Stale or different whole procedure/population scope.")
    count = len(profile.names) * len(profile.feature_names)
    meter.pay("assessment", "nonconstant_range_cell_inspection", count)
    cells = sum(lo != hi for row in profile.ranges for lo, hi in row)
    r, k = certified_radius(profile.n, cells, profile.delta, len(profile.checkpoints), meter)
    meter.pay_many((("assessment", "profile_validate_and_interval_arithmetic", 8 * count),
                    ("storage", "profile_cell_read_and_interval_write", 5 * count)))
    # Profile construction validates immutable data. Revalidating and hashing
    # its entire record would need the full freeze charge; no mutation is an
    # admitted operation on this exact frozen type.
    intervals = []
    for bounds, row in zip(profile.ranges, profile.sums):
        interval_row = []
        for (lo, hi), s in zip(bounds, row):
            mean, radius = F(s, profile.n), (hi - lo) * r
            interval_row.append((max(F(lo), mean - radius), min(F(hi), mean + radius)))
        intervals.append(tuple(interval_row))
    return tuple(intervals), {"r": str(r), "k": k, "nonconstant_cells": cells,
                             "checkpoints": len(profile.checkpoints), "tail_budget": str(profile.delta)}


def lower_scores(profile, intervals, prices, meter):
    if type(prices) is not tuple or len(prices) != len(profile.feature_names):
        raise Rejected("One immutable price per feature required.")
    # Repricing itself is a bounded readout; every coordinate is charged.
    count = len(profile.names) * len(prices)
    meter.pay_many((("assessment", "price_check_multiply_add", 4 * count),
                    ("storage", "price_and_interval_word_read", 3 * count)))
    pp = tuple(exact(x, price=True) for x in prices)
    result = []
    for row in intervals:
        score = F(0)
        for p, (lo, hi) in zip(pp, row):
            score = exact(score + exact(p * (lo if p >= 0 else hi)))
        result.append(score)
    return tuple(result)


def select(profile, expected_scope, prices, horizon, *, setup_to_recover=F(0),
           assessment_limit=20000, pre_screen=True):
    """Select for a fresh constant-price cohort, with a funded final readout.

    The nonnegative continuation score is chosen after assessment is sunk.
    Acquisition and actual assessment costs remain in the all-in certificate.
    The gross screen excludes only the complete assessments in this catalogue.

    If fewer than SELECT_FINAL_UNITS+1 units are available, the fixed control
    envelope emits fallback (one unit), or emits nothing at budget zero. It
    returns raw accounting but NO priced certificate, profile identity or
    forecast. This prevents an unfunded rational readout on tiny budgets.
    Transport of the diagnostic dict/Meter snapshot is harness instrumentation.
    """
    nat(assessment_limit, A.MAX_TOTAL_UNITS, "assessment budget")
    output = A.Meter(int(assessment_limit > 0))
    if assessment_limit < SELECT_FINAL_UNITS + 1:
        if assessment_limit:
            output.pay("assessment", "emit_unassessed_fallback", 1)
        return {"version": VERSION, "kind": "no_funded_assessment_readout",
                "policy": "fallback" if assessment_limit else None,
                "profile_id": None, "assessment_cost": None,
                "conditional_batch_lower_gain": None, "all_in_lower_gain": None,
                "positive_continuation_certificate": False,
                "positive_all_in_certificate": False,
                "meter": merged_meter((output,), assessment_limit),
                "boundary": "No priced or statistical certificate was computed."}
    final = A.Meter(SELECT_FINAL_UNITS)
    meter = A.Meter(assessment_limit - SELECT_FINAL_UNITS - 1)
    kind, intervals, radius, scores = "assessed", None, None, None
    selected, selected_lower, pp = 0, F(0), None
    # Final cost arithmetic, selected profile identity read and result fields
    # use this prepaid bounded bundle. Setup has a narrower 256-bit input cap;
    # the 14 prices each have <=32-bit components. Every intermediate is also
    # checked against 2048 bits before any certificate can be returned.
    final.pay("assessment", "final_bounded_arithmetic_identity_and_readout", SELECT_FINAL_UNITS)
    output.pay("assessment", "emit_assessment_action", 1)
    try:
        meter.pay("assessment", "preflight_horizon_price_and_gate_checks", 64)
        nat(horizon, MAX_HORIZON, "deployment horizon")
        if not horizon:
            raise Rejected("A positive deployment horizon is required.")
        if type(profile) is not Profile or type(expected_scope) is not Scope:
            raise Rejected("Exact immutable profile and scope required.")
        if type(prices) is not tuple or len(prices) != len(FEATURES):
            raise Rejected("The modular selector requires all 14 prices.")
        pp = tuple(exact(x, price=True) for x in prices)
        if any(x < 0 for x in pp):
            raise Rejected("Deployed task/resource prices must be nonnegative.")
        setup_to_recover = exact(setup_to_recover)
        if setup_to_recover < 0 or max(abs(setup_to_recover.numerator).bit_length(), setup_to_recover.denominator.bit_length()) > MAX_SETUP_BITS:
            raise Rejected("Setup recovery value must have nonnegative 256-bit components.")
        meter.pay("assessment", "catalogue_feature_range_and_scope_comparison",
                  2 * SCOPE_WORD_BOUND + 4 * len(CATALOGUE) * len(FEATURES))
        if (profile.scope != expected_scope
                or profile.names != tuple(p.name for p in CATALOGUE)
                or profile.feature_names != FEATURES
                or profile.ranges != tuple(paired_ranges(p) for p in CATALOGUE)):
            raise Rejected("Exact current catalogue, feature ranges and whole scope required.")
        lower_assessment_cost = exact(160 * pp[3 + A.CATEGORIES.index("assessment")])
        if pre_screen and exact(horizon * pp[2]) <= lower_assessment_cost:
            kind = "gross_value_screen"
        else:
            intervals, radius = profile_intervals(profile, expected_scope, meter)
            scores = lower_scores(profile, intervals, pp, meter)
            meter.pay("assessment", "policy_max_and_flags", 4 * len(scores) + 8)
            if scores[0] != 0:
                raise Rejected("Fallback must have exact zero paired saving.")
            selected = max(range(len(scores)), key=lambda i: (scores[i], -i))
            selected_lower = scores[selected]
    except A.BudgetExhausted:
        kind, selected, selected_lower = "assessment_budget_exhausted", 0, F(0)
    if pp is None:
        # A funded terminal decision exists, but the preflight did not obtain
        # validated prices. Do not invent an uncharged priced assessment.
        return {"version": VERSION, "kind": kind, "policy": "fallback",
                "profile_id": None, "assessment_cost": None,
                "conditional_batch_lower_gain": None, "all_in_lower_gain": None,
                "positive_continuation_certificate": False,
                "positive_all_in_certificate": False,
                "meter": merged_meter((meter, final, output), assessment_limit),
                "boundary": "Preflight exhausted before validated prices; no certificate."}
    # All charges, including final arithmetic and emission, are already fixed.
    quantities = tuple(sum(m.by_category[c] for m in (meter, final, output)) for c in A.CATEGORIES)
    online = F(0)
    for p, quantity in zip(pp[3:], quantities):
        online = exact(online + exact(p * quantity))
    conditional = exact(horizon * selected_lower)
    all_in = exact(exact(conditional - online) - setup_to_recover)
    result = {"version": VERSION, "profile_id": profile.identity,
              "scope": expected_scope.record(), "kind": kind,
              "horizon": horizon, "policy": profile.names[selected],
              "lower_gain_per_query": str(selected_lower),
              "conditional_batch_lower_gain": str(conditional),
              "assessment_cost": str(online), "setup_to_recover": str(setup_to_recover),
              "all_in_lower_gain": str(all_in),
              "positive_continuation_certificate": selected_lower > 0,
              "positive_all_in_certificate": all_in > 0,
              "scores": None if scores is None else dict(zip(profile.names, map(str, scores))),
              "radius": radius,
              "boundary": "Expected fresh-cohort guarantee on the simultaneous event; no fixed-query or pathwise promise."}
    result["meter"] = merged_meter((meter, final, output), assessment_limit)
    return result


def price_vector(fp, fn, fallback, unit, storage=None):
    prices = [F(fp), F(fn), F(fallback)] + [F(unit)] * len(A.CATEGORIES)
    if storage is not None:
        prices[3 + A.CATEGORIES.index("storage")] = F(storage)
    return tuple(prices)


def total_cost(features, prices):
    if len(features) != len(prices):
        raise Rejected("Cost vector dimension mismatch.")
    return sum((exact(v) * exact(p, price=True) for v, p in zip(features, prices)), F(0))
