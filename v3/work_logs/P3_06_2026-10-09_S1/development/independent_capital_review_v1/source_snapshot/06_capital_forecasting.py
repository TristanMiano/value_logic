"""P3-06 ordinary capital-sum benchmark with exact rational enclosures.

Contributor: ChatGPT (GPT-6 Astra Pro), October 9, 2026 UTC.
Research implementation, separately versioned from the polynomial K29 core.
Exponential capital uses Vovk (2007), Lemmas 1-2 and finite positive sums.
The declared horizon/stake/slope caps and all numerical allowances are explicit.
No floating-point number is used in forecast selection or its certificates.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from collections.abc import Mapping
from fractions import Fraction as F
from functools import lru_cache
import importlib.util
from math import isqrt
from pathlib import Path
import sys

BASE_PATH = Path(__file__).resolve().with_name('06_defensive_forecasting.py')
SPEC = importlib.util.spec_from_file_location('p306_capital_base', BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)
VERSION = 'p306-capital-enclosure-v1'


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def floor_fraction(x):
    return x.numerator // x.denominator


def exp_interval(x, bits=64):
    """Proved dyadic enclosure of exp(rational x), using a positive Taylor sum.

    Reduce |x| to z<=1 by exact halvings. After terms through n, the positive
    series remainder is at most 2/(n+1)!. Outward dyadic rounding followed by
    outward-rounded squaring preserves the enclosure. Invert for negative x.
    This bounds committed values, not transient arithmetic memory or CPU.
    """
    x = BASE.rational(x)
    if type(bits) is not int or bits < 8:
        raise ValueError('An integer enclosure precision of at least 8 bits is required.')
    if x == 0:
        return F(1), F(1)
    scale, z, squares = 1 << bits, abs(x), 0
    while z > 1:
        z /= 2
        squares += 1
    term, partial, factorial, n = F(1), F(1), 1, 0
    tail = F(2)
    target = F(1, 1 << (bits + 8))
    while tail > target:
        n += 1
        term *= z / n
        partial += term
        factorial *= n
        tail = F(2, factorial * (n + 1))
    lo = floor_fraction(partial * scale)
    hi = ceil_fraction((partial + tail) * scale)
    for _ in range(squares):
        lo = (lo * lo) // scale
        hi = -((-hi * hi) // scale)
    if x < 0:
        lo, hi = (scale * scale) // hi, -((-scale * scale) // lo)
    return F(lo, scale), F(hi, scale)


@lru_cache(maxsize=128)
def log_upper(x, bits=48):
    """Exact rational upper bound on ln(x) for rational x>=1.

    Reduce to [1,2], then use ln(x)=2*atanh((x-1)/(x+1)). The positive
    remainder after n terms is bounded by 2*z**(2*n+1)/((2*n+1)*(1-z*z)).
    """
    x = BASE.rational(x)
    if x < 1 or type(bits) is not int or bits < 8:
        raise ValueError('Require x>=1 and at least 8 precision bits.')
    if x == 1:
        return F(0)
    k, reduced = 0, x
    while reduced > 2:
        reduced /= 2
        k += 1
    target = F(1, (k + 1) * (1 << bits))

    def local(q):
        z = (q - 1) / (q + 1)
        if z == 0:
            return F(0)
        partial, power, n = F(0), z, 0
        while True:
            partial += 2 * power / (2 * n + 1)
            n += 1
            power *= z * z
            tail = 2 * power / ((2 * n + 1) * (1 - z * z))
            if tail <= target:
                return partial + tail

    return k * local(F(2)) + local(reduced)


@dataclass(frozen=True)
class CapitalSettings:
    experts: tuple[str, ...]
    horizon: int
    max_weight: F
    max_slope_range: F
    bins: int
    scope: str
    total_numeric_budget: F
    max_bisections: int
    initial_bits: int
    max_bits: int


@dataclass(frozen=True)
class CapitalPrediction:
    query: str
    scope: str
    probability: F
    expert_values: tuple[F, ...]
    weight: F
    actions: object
    action_one_probability: F
    logs_by_outcome: tuple[tuple[F, ...], tuple[F, ...]]
    capital_before_interval: tuple[F, F]
    capital_after_intervals: tuple[tuple[F, F], tuple[F, F]]
    capital_allowance: F
    requested_allowance: F
    allowance_met: bool
    bisections: int
    capital_evaluations: int
    max_enclosure_bits: int


@dataclass(frozen=True)
class CapitalState:
    logs: tuple[F, ...]
    capital_bound: F
    own_loss: F
    expert_losses: tuple[F, ...]
    calibration_residuals: tuple[F, ...]
    calibration_variances: tuple[F, ...]
    action_residuals: tuple[F, F]
    action_variances: tuple[F, F]
    mixed_loss: F
    fixed_losses: tuple[F, F]
    smoothing_slack: F
    weight: F
    settled: int


class CapitalForecaster:
    """One pending query, fixed prospective horizon and variance envelopes.

    Fixed positive priors allocate one third to experts, one third to the
    signed tent tests, and one third to two one-sided action residual tests.
    lambda values are fixed before the run; no optimization at observed V.
    Capped search may exhaust: its actual certified capital allowance survives.
    """
    def __init__(self, experts, horizon, max_weight=1, max_slope_range=2, bins=4,
                 scope=VERSION, total_numeric_budget=F(1, 65536),
                 max_bisections=64, initial_bits=48, max_bits=192):
        if not isinstance(experts, (tuple, list)):
            raise ValueError('Supply an explicit expert-name sequence.')
        names = tuple(experts)
        if not names or len(set(names)) != len(names) or any(type(n) is not str or not n for n in names):
            raise ValueError('Distinct nonempty expert names required.')
        for value in (horizon, bins, max_bisections, initial_bits, max_bits):
            if type(value) is not int:
                raise ValueError('Integer horizon, bins and numerical caps required.')
        if (horizon < 1 or not 1 <= bins <= 64 or max_bisections < 0
                or initial_bits < 16 or max_bits < initial_bits):
            raise ValueError('Invalid prospective horizon or numerical cap.')
        wmax, dmax, budget = map(BASE.rational, (max_weight, max_slope_range, total_numeric_budget))
        if wmax <= 0 or dmax <= 0 or budget <= 0 or type(scope) is not str or not scope:
            raise ValueError('Positive caps/budget and nonempty scope required.')
        self._settings = CapitalSettings(names, horizon, wmax, dmax, bins, scope,
                                        budget, max_bisections, initial_bits, max_bits)
        root = isqrt(horizon)
        root += root * root < horizon
        self._expert_rate = 2 / wmax
        self._calibration_rate = F(4, root) / wmax
        self._action_rate = F(4, root) / (wmax * dmax)
        self._priors = ((F(1, 3 * len(names)),) * len(names)
                       + (F(1, 6 * (bins + 1)),) * (2 * (bins + 1))
                       + (F(1, 6), F(1, 6)))
        assert sum(self.priors) == 1
        self._state = CapitalState((F(0),) * len(self.priors), F(1), F(0),
            (F(0),) * len(names), (F(0),) * (bins + 1), (F(0),) * (bins + 1),
            (F(0), F(0)), (F(0), F(0)), F(0), (F(0), F(0)), F(0), F(0), 0)
        self._pending = None
        self._history = []
        self._used = set()

    @property
    def settings(self):
        return self._settings

    @property
    def priors(self):
        return self._priors

    @property
    def expert_rate(self):
        return self._expert_rate

    @property
    def calibration_rate(self):
        return self._calibration_rate

    @property
    def action_rate(self):
        return self._action_rate

    @property
    def state(self):
        return self._state

    @property
    def pending(self):
        return self._pending

    @property
    def history(self):
        return tuple(self._history)

    def _tests(self, p, w, actions):
        tents = tuple(w * max(F(0), 1 - abs(self.settings.bins * p - j))
                      for j in range(self.settings.bins + 1))
        d0, d1 = actions.slopes
        mean = d0 + actions.mix(p) * (d1 - d0)
        return tents, (w * (mean - d0), w * (mean - d1))

    def _next_logs(self, p, qs, w, actions, y):
        e, rate, ac = y - p, self.calibration_rate, self.action_rate
        increments = tuple(self.expert_rate * w * ((p - y) ** 2 - (q - y) ** 2) for q in qs)
        tents, action_features = self._tests(p, w, actions)
        for value in tents:
            increments += (rate * value * e - rate * rate * value * value / 8,
                           -rate * value * e - rate * rate * value * value / 8)
        increments += tuple(ac * value * e - ac * ac * value * value / 8 for value in action_features)
        return tuple(old + inc for old, inc in zip(self.state.logs, increments))

    def _capital(self, logs, bits):
        intervals = [exp_interval(value, bits) for value in logs]
        return tuple(sum((prior * pair[edge] for prior, pair in zip(self.priors, intervals)), F(0))
                     for edge in (0, 1))

    def issue(self, query, experts, weight=1, *, rows=((0, 1), (1, 0)), eta=F(1, 2)):
        if self.pending is not None:
            raise ValueError('Settle the outstanding query before issuing another.')
        if type(query) is not str or not query or query in self._used:
            raise ValueError('A fresh nonempty query identity is required.')
        if len(self._used) >= self.settings.horizon:
            raise ValueError('The announced horizon has ended; use a separately declared episode.')
        if not isinstance(experts, Mapping) or set(experts) != set(self.settings.experts):
            raise ValueError('Exactly the declared expert mapping is required.')
        qs = tuple(BASE.rational(experts[name]) for name in self.settings.experts)
        w, actions = BASE.rational(weight), BASE.ActionTable(rows, eta)
        if any(q < 0 or q > 1 for q in qs) or not 0 <= w <= self.settings.max_weight:
            raise ValueError('Expert or weight outside its announced bound.')
        if actions.slope_range > self.settings.max_slope_range:
            raise ValueError('Action slope range exceeds the announced envelope.')
        requested = self.settings.total_numeric_budget / self.settings.horizon
        evaluations, highest_bits = 0, self.settings.initial_bits
        old_intervals, candidates = {}, []

        def evaluate(p, bits, depth):
            nonlocal evaluations, highest_bits
            if bits not in old_intervals:
                old_intervals[bits] = self._capital(self.state.logs, bits)
                evaluations += 1
            old = old_intervals[bits]
            logs = tuple(self._next_logs(p, qs, w, actions, y) for y in (0, 1))
            capitals = tuple(self._capital(log, bits) for log in logs)
            evaluations += 2
            highest_bits = max(highest_bits, bits)
            allowance = max(F(0), *(interval[1] - old[0] for interval in capitals))
            entry = (allowance, p, logs, old, capitals, depth)
            candidates.append(entry)
            return entry

        bits, low, high, depth = self.settings.initial_bits, F(0), F(1), 0
        chosen = None
        for p in (F(0), F(1)):
            candidate = evaluate(p, bits, depth)
            if candidate[0] <= requested:
                chosen = candidate
                break
        while chosen is None:
            p = (low + high) / 2
            candidate = evaluate(p, bits, depth)
            if candidate[0] <= requested:
                chosen = candidate
                break
            intervals = candidate[4]
            difference = (intervals[1][0] - intervals[0][1],
                          intervals[1][1] - intervals[0][0])
            if difference[0] <= 0 <= difference[1]:
                if bits < self.settings.max_bits:
                    bits = min(2 * bits, self.settings.max_bits)
                    continue
                break
            if depth >= self.settings.max_bisections:
                break
            if difference[0] > 0:
                low = p
            else:
                high = p
            depth += 1
        if chosen is None:
            chosen = min(candidates, key=lambda c: (c[0], c[1]))
        allowance, p, logs, old, capitals, used_depth = chosen
        prediction = CapitalPrediction(query, self.settings.scope, p, qs, w, actions,
            actions.mix(p), logs, old, capitals, allowance, requested, allowance <= requested,
            used_depth, evaluations, highest_bits)
        self._pending = prediction
        self._used.add(query)
        return prediction

    def reveal(self, query, outcome, *, scope):
        if (self.pending is None or query != self.pending.query or scope != self.settings.scope
                or type(outcome) is not int or outcome not in (0, 1)):
            raise ValueError('Require the pending scoped identity and a strict binary integer answer.')
        pred, old = self.pending, self.state
        p, w, y = pred.probability, pred.weight, outcome
        tents, action_features = self._tests(p, w, pred.actions)
        e = y - p
        own = old.own_loss + w * (p - y) ** 2
        expert = tuple(loss + w * (q - y) ** 2 for loss, q in zip(old.expert_losses, pred.expert_values))
        cal = tuple(total + v * e for total, v in zip(old.calibration_residuals, tents))
        calv = tuple(total + v * v for total, v in zip(old.calibration_variances, tents))
        act = tuple(total + v * e for total, v in zip(old.action_residuals, action_features))
        actv = tuple(total + v * v for total, v in zip(old.action_variances, action_features))
        s, rows = pred.action_one_probability, pred.actions.rows
        fixed = tuple(old.fixed_losses[i] + w * rows[i][y] for i in (0, 1))
        mixed = old.mixed_loss + w * ((1 - s) * rows[0][y] + s * rows[1][y])
        updated = CapitalState(pred.logs_by_outcome[y], old.capital_bound + pred.capital_allowance,
            own, expert, cal, calv, act, actv, mixed, fixed,
            old.smoothing_slack + w * pred.actions.eta / 8, old.weight + w, old.settled + 1)
        assert pred.capital_after_intervals[y][1] <= updated.capital_bound
        expected = tuple(self.expert_rate * (own - other) for other in expert)
        rate, ac = self.calibration_rate, self.action_rate
        for residual, variance in zip(cal, calv):
            expected += (rate * residual - rate * rate * variance / 8,
                         -rate * residual - rate * rate * variance / 8)
        expected += tuple(ac * residual - ac * ac * variance / 8 for residual, variance in zip(act, actv))
        assert expected == updated.logs
        assert all(mixed - other <= updated.smoothing_slack + residual
                   for other, residual in zip(fixed, act))
        self._state = updated
        self._history.append((pred, outcome))
        self._pending = None
        return updated

    def audit(self):
        state, cfg = self.state, self.settings
        n = len(cfg.experts)
        log_expert = log_upper(state.capital_bound / self.priors[0])
        log_cal = log_upper(state.capital_bound / self.priors[n])
        log_act = log_upper(state.capital_bound / self.priors[-1])
        expert_bound = log_expert / self.expert_rate
        cal_bounds = tuple(self.calibration_rate * v / 8 + log_cal / self.calibration_rate
                           for v in state.calibration_variances)
        act_bounds = tuple(state.smoothing_slack + self.action_rate * v / 8 + log_act / self.action_rate
                           for v in state.action_variances)
        assert all(state.own_loss - other <= expert_bound for other in state.expert_losses)
        assert all(abs(r) <= b for r, b in zip(state.calibration_residuals, cal_bounds))
        assert all(state.mixed_loss - other <= b for other, b in zip(state.fixed_losses, act_bounds))
        return {'version': VERSION, 'scope': cfg.scope, 'settled': state.settled,
                'pending': self.pending is not None, 'capital_bound': state.capital_bound,
                'capital_allowance': state.capital_bound - 1,
                'expert_regret_upper': expert_bound, 'calibration_absolute_upper': cal_bounds,
                'mixed_action_regret_upper': act_bounds, 'state': asdict(state),
                'rates': (self.expert_rate, self.calibration_rate, self.action_rate),
                'priors': self.priors, 'settings': asdict(cfg)}
