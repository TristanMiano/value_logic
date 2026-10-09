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

from dataclasses import dataclass
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

VERSION = "p307-paired-profile-controller-v1"
FEATURE_VERSION = "fp-fn-fallback-and-eleven-resource-categories-v1"
MAX_POLICIES, MAX_FEATURES, MAX_ROWS = 16, 32, 8192
MAX_PRICE_BITS, MAX_ARITHMETIC_BITS = 32, 2048
MAX_HORIZON, MAX_CHECKPOINTS, RADIUS_BITS = 10000, 16, 16
POLICY_BUDGET = 1024
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
        if type(self.name) is not str or not 1 <= len(self.name) <= 64:
            raise Rejected("Policy identity must be a capped string.")
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
            if type(v) is not str or not 1 <= len(v) <= 256:
                raise Rejected("Scope fields must be nonempty capped strings.")

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
    meter = A.Meter(max(0, limit - 1))
    adapter = A.Adapter(meter, cache_cap=0)
    answer, progress, status = None, None, "unresolved"
    initial_report = F(1, 2)
    try:
        meter.pay("forecast", "issue_known_half_report", 1)
        answer = adapter.lookup(query)
        if answer is None:
            answer = adapter.shortcut(query)
        if answer is None and policy.transactions:
            handle = adapter.start(query)
            progress = adapter.advance(handle, policy.transactions)
            if progress.checked_ready:
                answer = adapter.acquire(handle)
            else:
                status = "budget_exhausted" if progress.budget_exhausted else "transaction_timeout"
        if answer is not None:
            status = "checked_answer"
    except A.BudgetExhausted:
        status = "budget_exhausted"
    action = answer.answer if answer is not None else policy.unresolved_action
    snapshot = meter.snapshot()
    # The reserved terminal emission is an actual separately charged action.
    emission = 1 if limit else 0
    snapshot["by_category"]["forecast"] += emission
    snapshot["operations"]["forecast.emit_terminal_action"] = emission
    snapshot["total"] += emission
    snapshot["limit_total"] = limit
    snapshot["remaining"] = limit - snapshot["total"]
    if not limit:
        action, status = None, "no_output_budget"
    assert snapshot["total"] <= limit
    return {"policy": policy.name, "initial_report": str(initial_report),
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

    def __post_init__(self):
        if type(self.scope) is not Scope or type(self.names) is not tuple or not 1 <= len(self.names) <= MAX_POLICIES:
            raise Rejected("Invalid immutable profile scope/catalogue.")
        if len(set(self.names)) != len(self.names) or any(type(s) is not str or not 1 <= len(s) <= 64 for s in self.names):
            raise Rejected("Unique bounded policy identities required.")
        if type(self.feature_names) is not tuple or not 1 <= len(self.feature_names) <= MAX_FEATURES or len(set(self.feature_names)) != len(self.feature_names):
            raise Rejected("Distinct immutable feature identities required.")
        nat(self.n, MAX_ROWS, "profile count")
        if not self.n:
            raise Rejected("An empty profile cannot certify a mean.")
        if type(self.checkpoints) is not tuple or not 1 <= len(self.checkpoints) <= MAX_CHECKPOINTS:
            raise Rejected("A fixed finite checkpoint tuple is required.")
        if tuple(sorted(set(self.checkpoints))) != self.checkpoints or self.n not in self.checkpoints:
            raise Rejected("Count must be a member of the predeclared distinct ordered checkpoints.")
        for n in self.checkpoints:
            nat(n, MAX_ROWS, "checkpoint")
            if not n:
                raise Rejected("Checkpoints must be positive.")
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

    def record(self):
        return {"scope": self.scope.record(), "names": self.names,
                "feature_names": self.feature_names, "ranges": self.ranges,
                "sums": self.sums, "n": self.n, "checkpoints": self.checkpoints,
                "delta": str(self.delta), "setup_resources": self.setup_resources}

    @property
    def identity(self):
        return digest(self.record())


class ProfileBuilder:
    """Fixed catalogue full-information sums; no profile receives future labels."""
    def __init__(self, scope, names, feature_names, ranges, checkpoints, delta):
        self.scope, self.names, self.feature_names = scope, names, feature_names
        self.ranges, self.checkpoints, self.delta = ranges, checkpoints, exact(delta)
        self.sums = [[0] * len(feature_names) for _ in names]
        self.n = 0

    def add(self, paired_rows, meter):
        if self.n >= max(self.checkpoints) or type(paired_rows) is not tuple or len(paired_rows) != len(self.names):
            raise Rejected("Profile hard cap or row count mismatch.")
        # Each cell: read, range-check twice, add, write; finite validation first.
        for bounds, row in zip(self.ranges, paired_rows):
            if type(row) is not tuple or len(row) != len(bounds):
                raise Rejected("Full immutable paired row required.")
            for (lo, hi), v in zip(bounds, row):
                if type(v) is not int or not lo <= v <= hi:
                    raise Rejected("Observed feature violates the frozen range.")
        cells = len(self.names) * len(self.feature_names)
        meter.pay_many((("profile", "paired_cell_check_add", 3 * cells),
                        ("storage", "paired_cell_read_write", 2 * cells),
                        ("profile", "profile_count_increment", 1)))
        for i, row in enumerate(paired_rows):
            for j, v in enumerate(row):
                self.sums[i][j] += v
        self.n += 1

    def freeze(self, setup_resources):
        return Profile(self.scope, self.names, self.feature_names, self.ranges,
                       tuple(tuple(row) for row in self.sums), self.n,
                       self.checkpoints, self.delta, tuple(setup_resources))


def profile_intervals(profile, expected_scope, meter):
    if type(profile) is not Profile or type(expected_scope) is not Scope:
        raise Rejected("Exact immutable profile and independently supplied scope required.")
    # Identity metadata is compared before any old result is used.
    words = (len(canonical(profile.scope.record()).encode()) + 7) // 8
    meter.pay("assessment", "scope_word_comparison", 2 * words)
    if profile.scope != expected_scope:
        raise Rejected("Stale or different whole procedure/population scope.")
    cells = sum(lo != hi for row in profile.ranges for lo, hi in row)
    r, k = certified_radius(profile.n, cells, profile.delta, len(profile.checkpoints), meter)
    count = len(profile.names) * len(profile.feature_names)
    meter.pay_many((("assessment", "profile_validate_and_interval_arithmetic", 8 * count),
                    ("storage", "profile_cell_read_and_interval_write", 5 * count)))
    profile.__post_init__()
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
    pp = tuple(exact(x, price=True) for x in prices)
    # Repricing itself is a bounded readout; every coordinate is charged.
    count = len(profile.names) * len(pp)
    meter.pay_many((("assessment", "price_check_multiply_add", 4 * count),
                    ("storage", "price_and_interval_word_read", 3 * count)))
    result = []
    for row in intervals:
        score = F(0)
        for p, (lo, hi) in zip(pp, row):
            score = exact(score + exact(p * (lo if p >= 0 else hi)))
        result.append(score)
    return tuple(result)


def select(profile, expected_scope, prices, horizon, *, setup_to_recover=F(0),
           assessment_limit=20000, pre_screen=True):
    """Choose a fixed policy for a future constant-price cohort.

    Continuation choice maximizes L including baseline zero after assessment
    is sunk. Costs paid to find that choice remain in all-in flags, including
    the no-certificate branch. A cheap optional gate uses only a *known upper*
    bound on gross task saving; it is not a performance oracle. It applies to
    this modular nonnegative-price catalogue with fallback as baseline.
    """
    nat(horizon, MAX_HORIZON, "deployment horizon")
    if not horizon:
        raise Rejected("A positive actual deployment horizon is required.")
    if type(prices) is not tuple or len(prices) != len(profile.feature_names):
        raise Rejected("Price dimension mismatch.")
    pp = tuple(exact(x, price=True) for x in prices)
    if any(x < 0 for x in pp):
        raise Rejected("The deployed resource/task price domain is nonnegative.")
    setup_to_recover = exact(setup_to_recover)
    if setup_to_recover < 0:
        raise Rejected("Setup recovery cost must be nonnegative.")
    meter = A.Meter(assessment_limit)
    # A paid constant-plan check has bounded cost on every branch.
    meter.pay("assessment", "preflight_horizon_price_and_gate_checks", 4 * len(pp) + 8)
    kind, intervals, radius, scores = "assessed", None, None, None
    try:
        # Scope and catalogue restrictions are checked even when the gate exits.
        if profile.scope != expected_scope or profile.names != tuple(p.name for p in CATALOGUE) or profile.feature_names != FEATURES:
            raise Rejected("The modular selector requires its exact current catalogue and scope.")
        # Every full assessment must spend at least the explicit radius bundle.
        # All incremental computation quantities are nonnegative against fallback.
        lower_assessment_cost = 160 * pp[3 + A.CATEGORIES.index("assessment")]
        if pre_screen and horizon * pp[2] <= lower_assessment_cost:
            kind, selected, selected_lower = "gross_value_screen", 0, F(0)
        else:
            intervals, radius = profile_intervals(profile, expected_scope, meter)
            scores = lower_scores(profile, intervals, pp, meter)
            meter.pay("assessment", "policy_max_and_flags", 4 * len(scores) + 8)
            # Frozen baseline has exact zero differences. First entry wins ties.
            if scores[0] != 0:
                raise Rejected("Fallback comparison must have exact zero saving.")
            selected = max(range(len(scores)), key=lambda i: (scores[i], -i))
            selected_lower = scores[selected]
    except A.BudgetExhausted:
        kind, selected, selected_lower = "assessment_budget_exhausted", 0, F(0)
    costs = meter.snapshot()
    online = sum((pp[3 + j] * costs["by_category"][c] for j, c in enumerate(A.CATEGORIES)), F(0))
    conditional = horizon * selected_lower
    return {"version": VERSION, "profile_id": profile.identity,
            "scope": expected_scope.record(), "kind": kind,
            "horizon": horizon, "policy": profile.names[selected],
            "lower_gain_per_query": str(selected_lower),
            "conditional_batch_lower_gain": str(conditional),
            "assessment_cost": str(online), "setup_to_recover": str(setup_to_recover),
            "all_in_lower_gain": str(conditional - online - setup_to_recover),
            "positive_continuation_certificate": selected_lower > 0,
            "positive_all_in_certificate": conditional > online + setup_to_recover,
            "scores": None if scores is None else dict(zip(profile.names, map(str, scores))),
            "radius": radius, "meter": costs,
            "boundary": "Expected fresh-cohort guarantee on the simultaneous event; no fixed-query or pathwise promise."}


def price_vector(fp, fn, fallback, unit, storage=None):
    prices = [F(fp), F(fn), F(fallback)] + [F(unit)] * len(A.CATEGORIES)
    if storage is not None:
        prices[3 + A.CATEGORIES.index("storage")] = F(storage)
    return tuple(prices)


def total_cost(features, prices):
    if len(features) != len(prices):
        raise Rejected("Cost vector dimension mismatch.")
    return sum((exact(v) * exact(p, price=True) for v, p in zip(features, prices)), F(0))
