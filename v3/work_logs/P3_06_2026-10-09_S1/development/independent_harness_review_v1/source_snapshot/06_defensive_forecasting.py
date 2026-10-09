"""P3-06 scalar forecasting, reconstructed version 2 (development).

Finite exact-rational K29* features for Brier regret, continuous-bin calibration,
and optionally smooth two-action external regret. No proof/label oracle is here.
Semantic answer checking belongs to the caller's versioned evidence adapter.

The preserved October 8 sources are immutable historical evidence. This version
repairs input aliasing and rejected-call mutation and adds a certified root-work
mode and the separately reconstructed smooth decision feature block.

Contributor: ChatGPT (GPT-6 Astra Pro), October 9, 2026 UTC.
Python 3.10+, standard library only.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from math import isqrt
from typing import Mapping

VERSION = "p306-scalar-v2.1"


def rational(value: object) -> F:
    """Only declared exact input types; normalize malformed inputs to ValueError."""
    if isinstance(value, bool) or not isinstance(value, (int, str, F)):
        raise ValueError("Use integers, rational strings or Fraction; no floats/bools.")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("Invalid finite rational.") from exc


def norm_squared(values) -> F:
    return sum((x * x for x in values), F(0))


def encoded(value):
    """Detached JSON-compatible exact values; not an authentication mechanism."""
    if isinstance(value, F):
        return str(value)
    if hasattr(value, "__dataclass_fields__"):
        return encoded(asdict(value))
    if isinstance(value, dict):
        return {str(k): encoded(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encoded(v) for v in value]
    return value


def sqrt_upper(value: F, bits: int = 32) -> F:
    """Exact dyadic upper enclosure, including non-square rational inputs."""
    if value < 0 or isinstance(bits, bool) or not isinstance(bits, int) or bits < 0:
        raise ValueError("Nonnegative value and integer precision required.")
    numerator = value.numerator << (2 * bits)
    denominator = value.denominator
    root = isqrt(numerator // denominator)
    if root * root * denominator < numerator:
        root += 1
    return F(root, 1 << bits)


def sufficient_bisections(lipschitz: F, tolerance: F) -> int:
    """k bracket updates suffice when L / 2**(k+1) <= tolerance."""
    if lipschitz < 0 or tolerance <= 0:
        raise ValueError("Invalid Lipschitz bound or tolerance.")
    k = 0
    denominator = 2 * tolerance
    while lipschitz > denominator:
        denominator *= 2
        k += 1
    return k


def dyadic_eta(issue_number: int, scale=1) -> F:
    """c / 2**ceil(log2(t+1)); avoids cumulative harmonic denominators."""
    if isinstance(issue_number, bool) or not isinstance(issue_number, int) or issue_number < 1:
        raise ValueError("Issue number must be a positive integer.")
    c = rational(scale)
    if c <= 0:
        raise ValueError("Positive smoothing scale required.")
    return c / (1 << issue_number.bit_length())


@dataclass(frozen=True)
class ActionTable:
    """Two known outcome-contingent rows: rows[action][binary outcome]."""

    rows: tuple[tuple[F, F], tuple[F, F]]
    eta: F

    def __post_init__(self):
        if (not isinstance(self.rows, (tuple, list)) or len(self.rows) != 2
                or any(not isinstance(row, (tuple, list)) or len(row) != 2 for row in self.rows)):
            raise ValueError("Supply exactly two rows and two outcomes per row.")
        rows = tuple(tuple(rational(x) for x in row) for row in self.rows)
        eta = rational(self.eta)
        if eta <= 0:
            raise ValueError("Positive smoothing eta required.")
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "eta", eta)

    @property
    def slopes(self) -> tuple[F, F]:
        return tuple(row[1] - row[0] for row in self.rows)

    @property
    def slope_range(self) -> F:
        left, right = self.slopes
        return abs(right - left)

    def forecast_costs(self, probability: F) -> tuple[F, F]:
        return tuple(row[0] + probability * (row[1] - row[0]) for row in self.rows)

    def mix(self, probability: F) -> F:
        cost0, cost1 = self.forecast_costs(probability)
        return min(F(1), max(F(0), F(1, 2) - (cost1 - cost0) / (2 * self.eta)))


@dataclass(frozen=True)
class Settings:
    experts: tuple[str, ...]
    bins: int = 4
    alpha: F = F(1)
    beta: F = F(1)
    scope: str = VERSION
    decision_features: bool = False
    gamma: F = F(1)

    def __post_init__(self):
        if not isinstance(self.experts, (tuple, list)) or not self.experts:
            raise ValueError("Supply a nonempty expert-name sequence.")
        names = tuple(self.experts)
        if any(not isinstance(x, str) or not x for x in names) or len(set(names)) != len(names):
            raise ValueError("Expert names must be distinct nonempty strings.")
        if isinstance(self.bins, bool) or not isinstance(self.bins, int) or not 1 <= self.bins <= 64:
            raise ValueError("bins must be an integer in 1..64.")
        if not isinstance(self.scope, str) or not self.scope:
            raise ValueError("Scope must be a nonempty string.")
        if not isinstance(self.decision_features, bool):
            raise ValueError("decision_features must be Boolean.")
        object.__setattr__(self, "experts", names)
        for name in ("alpha", "beta", "gamma"):
            value = rational(getattr(self, name))
            if value <= 0:
                raise ValueError("Feature scales must be positive.")
            object.__setattr__(self, name, value)

    @property
    def dimension(self) -> int:
        return len(self.experts) + self.bins + 1 + (2 if self.decision_features else 0)


@dataclass(frozen=True)
class Prediction:
    query: str
    scope: str
    probability: F
    expert_values: tuple[F, ...]
    weight: F
    features: tuple[F, ...]
    score: F
    allowance: F
    tolerance: F
    tolerance_met: bool
    boundary: bool
    bisections: int
    score_evaluations: int
    lipschitz_bound: F
    sufficient_bisections: int
    configured_bisections: int | None
    actions: ActionTable | None
    action_one_probability: F | None


@dataclass(frozen=True)
class Observation:
    prediction: Prediction
    outcome: int


@dataclass(frozen=True)
class Accumulator:
    residual: tuple[F, ...]
    variance: F
    allowance: F
    weight: F
    own_loss: F
    expert_losses: tuple[F, ...]
    expert_distances: tuple[F, ...]
    mixed_action_loss: F
    action_losses: tuple[F, F]
    forecast_action_gaps: tuple[F, F]
    smoothing_slack: F
    settled: int

    @property
    def bound(self) -> F:
        return self.variance + self.allowance


@dataclass(frozen=True)
class CopySnapshot:
    settings: Settings
    accumulator: Accumulator
    pending: Prediction | None
    history: tuple[Observation, ...]
    used: frozenset[str]

    @property
    def experts(self) -> tuple[str, ...]:
        return self.settings.experts


class Forecaster:
    """One outstanding request; root exhaustion returns its actual allowance.

    max_bisections=None chooses a sufficient count from the current Lipschitz
    bound. An explicit nonnegative cap can be smaller; then the guarantee uses
    the actual allowance and does not claim the requested tolerance was met.

    Public records are immutable or detached. Validation and invariant checks
    occur before state commits. Exact arithmetic and retained history are not
    protected by a hard byte/CPU limit; their costs must be reported separately.
    """

    def __init__(self, experts, bins=4, alpha=1, beta=1, scope=VERSION,
                 decision_features=False, gamma=1):
        self._settings = Settings(experts, bins, alpha, beta, scope, decision_features, gamma)
        self._acc = Accumulator(
            (F(0),) * self._settings.dimension, F(0), F(0), F(0), F(0),
            (F(0),) * len(self.experts), (F(0),) * len(self.experts), F(0),
            (F(0), F(0)), (F(0), F(0)), F(0), 0)
        self._pending: Prediction | None = None
        self._used: set[str] = set()
        self._history: list[Observation] = []

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def experts(self) -> tuple[str, ...]:
        return self._settings.experts

    @property
    def pending(self) -> Prediction | None:
        return self._pending

    @property
    def accumulator(self) -> Accumulator:
        return self._acc

    @property
    def history(self) -> tuple[Observation, ...]:
        return tuple(self._history)

    @property
    def used(self) -> frozenset[str]:
        return frozenset(self._used)

    def _features(self, p: F, qs: tuple[F, ...], weight: F,
                  actions: ActionTable | None) -> tuple[F, ...]:
        cfg = self.settings
        features = tuple(weight * cfg.alpha * (q - p) for q in qs)
        features += tuple(weight * cfg.beta * max(F(0), 1 - abs(cfg.bins * p - j))
                          for j in range(cfg.bins + 1))
        if actions is not None:
            s = actions.mix(p)
            d0, d1 = actions.slopes
            mean = d0 + s * (d1 - d0)
            features += (weight * cfg.gamma * (mean - d0), weight * cfg.gamma * (mean - d1))
        return features

    def _score(self, p, qs, weight, actions):
        features = self._features(p, qs, weight, actions)
        score = sum((r * f for r, f in zip(self._acc.residual, features)), F(0))
        score += (1 - 2 * p) * norm_squared(features) / 2
        return score, features

    def _lipschitz(self, weight: F, actions: ActionTable | None) -> F:
        cfg = self.settings
        md = [(weight * cfg.alpha, weight * cfg.alpha)] * len(cfg.experts)
        md += [(weight * cfg.beta, cfg.bins * weight * cfg.beta)] * (cfg.bins + 1)
        if actions is not None:
            d = actions.slope_range
            md += [(weight * cfg.gamma * d, weight * cfg.gamma * d * d / (2 * actions.eta))] * 2
        return sum((abs(r) * lip + bound * bound + bound * lip
                    for r, (bound, lip) in zip(self._acc.residual, md)), F(0))

    def issue(self, query: str, experts: Mapping[str, object], weight=1,
              tolerance=F(1, 1024), max_bisections: int | None = None,
              actions: ActionTable | None = None) -> Prediction:
        if self.pending is not None:
            raise ValueError("This copy already has outstanding feedback.")
        if not isinstance(query, str) or not query or query in self._used:
            raise ValueError("Query identity must be new and nonempty.")
        if not isinstance(experts, Mapping) or set(experts) != set(self.experts):
            raise ValueError("Provide exactly the declared expert mapping.")
        qs = tuple(rational(experts[name]) for name in self.experts)
        if any(q < 0 or q > 1 for q in qs):
            raise ValueError("Expert probabilities must lie in [0,1].")
        w, tol = rational(weight), rational(tolerance)
        if w < 0 or tol <= 0:
            raise ValueError("Nonnegative weight and positive tolerance required.")
        if max_bisections is not None and (isinstance(max_bisections, bool)
                or not isinstance(max_bisections, int) or max_bisections < 0):
            raise ValueError("Root cap must be None or a nonnegative integer.")
        if self.settings.decision_features != (actions is not None):
            raise ValueError("The declared decision feature mode requires matching action inputs.")
        if actions is not None and not isinstance(actions, ActionTable):
            raise ValueError("Use a validated immutable ActionTable.")

        lipschitz = self._lipschitz(w, actions)
        sufficient = sufficient_bisections(lipschitz, tol)
        budget = sufficient if max_bisections is None else max_bisections
        score, features = self._score(F(0), qs, w, actions)
        evaluations, steps = 1, 0
        boundary = True
        if score <= 0:
            p = F(0)
        else:
            score, features = self._score(F(1), qs, w, actions)
            evaluations += 1
            if score >= 0:
                p = F(1)
            else:
                boundary = False
                lo, hi, p = F(0), F(1), F(1, 2)
                score, features = self._score(p, qs, w, actions)
                evaluations += 1
                while abs(score) > tol and steps < budget:
                    if score > 0:
                        lo = p
                    else:
                        hi = p
                    p = (lo + hi) / 2
                    score, features = self._score(p, qs, w, actions)
                    evaluations += 1
                    steps += 1
        allowance = 2 * max(F(0), (1 - p) * score, -p * score)
        met = boundary or abs(score) <= tol
        if max_bisections is None and not met:
            raise AssertionError("Certified Lipschitz budget failed before report commit.")
        pred = Prediction(query, self.settings.scope, p, qs, w, features, score, allowance,
                          tol, met, boundary, steps, evaluations, lipschitz, sufficient,
                          max_bisections, actions, actions.mix(p) if actions is not None else None)
        self._used.add(query)
        self._pending = pred
        return pred

    def reveal(self, query: str, outcome: int, *, scope: str) -> Prediction:
        if isinstance(outcome, bool) or not isinstance(outcome, int) or outcome not in (0, 1):
            raise ValueError("Use an admitted integer binary answer, never an unresolved label.")
        pred = self.pending
        if (pred is None or not isinstance(query, str) or query != pred.query
                or not isinstance(scope, str) or scope != pred.scope):
            raise ValueError("Feedback query and scope must match the outstanding forecast.")
        old, p, w = self._acc, pred.probability, pred.weight
        error = F(outcome) - p
        residual = tuple(r + error * f for r, f in zip(old.residual, pred.features))
        variance = old.variance + p * (1 - p) * norm_squared(pred.features)
        allowance = old.allowance + pred.allowance
        own = old.own_loss + w * error * error
        expert_losses = tuple(loss + w * (q - outcome) ** 2
                              for loss, q in zip(old.expert_losses, pred.expert_values))
        distances = tuple(dist + w * (q - p) ** 2
                          for dist, q in zip(old.expert_distances, pred.expert_values))
        mixed, action_losses = old.mixed_action_loss, old.action_losses
        gaps, slack = old.forecast_action_gaps, old.smoothing_slack
        if pred.actions is not None:
            table, s = pred.actions, pred.action_one_probability
            costs = tuple(row[outcome] for row in table.rows)
            forecast_costs = table.forecast_costs(p)
            forecast_mix = (1 - s) * forecast_costs[0] + s * forecast_costs[1]
            if forecast_mix - min(forecast_costs) > table.eta / 8:
                raise AssertionError("Smoothing inequality failed before settlement commit.")
            mixed += w * ((1 - s) * costs[0] + s * costs[1])
            action_losses = tuple(loss + w * cost for loss, cost in zip(action_losses, costs))
            gaps = tuple(gap + w * (forecast_mix - cost) for gap, cost in zip(gaps, forecast_costs))
            slack += w * table.eta / 8
        new = Accumulator(residual, variance, allowance, old.weight + w, own, expert_losses,
                          distances, mixed, action_losses, gaps, slack, old.settled + 1)
        self._check_accumulator(new)
        self._history.append(Observation(pred, outcome))
        self._acc = new
        self._pending = None
        return pred

    def _check_accumulator(self, acc: Accumulator):
        if norm_squared(acc.residual) > acc.bound:
            raise AssertionError("Potential invariant failed.")
        for index in range(len(self.experts)):
            expected = 2 * acc.residual[index] / self.settings.alpha - acc.expert_distances[index]
            if acc.own_loss - acc.expert_losses[index] != expected:
                raise AssertionError("Expert regret identity failed.")
        if self.settings.decision_features:
            for index in (0, 1):
                expected = acc.forecast_action_gaps[index] + acc.residual[-2 + index] / self.settings.gamma
                if acc.mixed_action_loss - acc.action_losses[index] != expected:
                    raise AssertionError("Decision regret identity failed.")
                if acc.forecast_action_gaps[index] > acc.smoothing_slack:
                    raise AssertionError("Forecast decision slack failed.")

    def audit(self) -> dict:
        self._check_accumulator(self._acc)
        return {"version": VERSION, "settings": self.settings, "accumulator": self._acc,
                "pending": self.pending.query if self.pending else None,
                "history_count": len(self._history)}

    def snapshot(self) -> CopySnapshot:
        return CopySnapshot(self.settings, self.accumulator, self.pending, self.history, self.used)


class DelayedPool:
    """Free-copy reduction with no invented labels and detached audit output."""

    def __init__(self, experts, bins=4, alpha=1, beta=1, scope=VERSION,
                 decision_features=False, gamma=1):
        self._settings = Settings(experts, bins, alpha, beta, scope, decision_features, gamma)
        self._copies: list[Forecaster] = []
        self._pending: dict[str, int] = {}
        self._used: set[str] = set()

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def copies(self) -> tuple[CopySnapshot, ...]:
        # No mutable learner handle escapes the pool's settlement bookkeeping.
        return tuple(copy.snapshot() for copy in self._copies)

    @property
    def pending(self) -> dict[str, int]:
        return dict(self._pending)

    @property
    def used(self) -> frozenset[str]:
        return frozenset(self._used)

    def _new_copy(self) -> Forecaster:
        cfg = self.settings
        return Forecaster(cfg.experts, cfg.bins, cfg.alpha, cfg.beta, cfg.scope,
                          cfg.decision_features, cfg.gamma)

    def issue(self, query, experts, weight=1, tolerance=F(1, 1024),
              max_bisections=None, actions=None) -> Prediction:
        if not isinstance(query, str) or not query or query in self._used:
            raise ValueError("Pool query identity must be new and nonempty.")
        index = next((i for i, copy in enumerate(self._copies) if copy.pending is None), None)
        candidate = self._new_copy() if index is None else self._copies[index]
        # A failed issue on a new candidate changes no pool allocation or history.
        prediction = candidate.issue(query, experts, weight, tolerance, max_bisections, actions)
        if index is None:
            index = len(self._copies)
            self._copies.append(candidate)
        self._pending[query] = index
        self._used.add(query)
        return prediction

    def reveal(self, query, outcome, *, scope) -> Prediction:
        if not isinstance(query, str) or query not in self._pending:
            raise ValueError("Unknown or already settled pool query.")
        index = self._pending[query]
        prediction = self._copies[index].reveal(query, outcome, scope=scope)
        del self._pending[query]
        return prediction

    def audit(self, sqrt_bits: int = 32) -> dict:
        if isinstance(sqrt_bits, bool) or not isinstance(sqrt_bits, int) or sqrt_bits < 0:
            raise ValueError("Square-root enclosure precision must be a nonnegative integer.")
        cfg = self.settings
        accumulators = tuple(copy.accumulator for copy in self._copies)
        for copy in self._copies:
            copy._check_accumulator(copy.accumulator)
        residual = tuple(sum((a.residual[j] for a in accumulators), F(0))
                         for j in range(cfg.dimension))
        bounds = tuple(a.bound for a in accumulators)
        positive = sum(b > 0 for b in bounds)
        cauchy = positive * sum(bounds, F(0))
        h_upper = sum((sqrt_upper(b, sqrt_bits) for b in bounds), F(0))
        combined = min(cauchy, h_upper * h_upper)
        if norm_squared(residual) > combined:
            raise AssertionError("Delayed aggregate potential failed.")
        own = sum((a.own_loss for a in accumulators), F(0))
        other = tuple(sum((a.expert_losses[i] for a in accumulators), F(0))
                      for i in range(len(cfg.experts)))
        expert_regrets = tuple(own - loss for loss in other)
        for regret in expert_regrets:
            if regret > 0 and regret * regret * cfg.alpha * cfg.alpha > 4 * combined:
                raise AssertionError("Delayed expert regret bound failed.")
        bin_residuals = tuple(residual[len(cfg.experts) + j] / cfg.beta for j in range(cfg.bins + 1))
        mixed = sum((a.mixed_action_loss for a in accumulators), F(0))
        action_losses = tuple(sum((a.action_losses[i] for a in accumulators), F(0)) for i in (0, 1))
        slack = sum((a.smoothing_slack for a in accumulators), F(0))
        action_regrets = tuple(mixed - loss for loss in action_losses)
        if cfg.decision_features:
            for regret in action_regrets:
                excess = regret - slack
                if excess > 0 and excess * excess * cfg.gamma * cfg.gamma > combined:
                    raise AssertionError("Delayed action regret bound failed.")
        return {"version": VERSION, "scope": cfg.scope, "copies": len(self._copies),
                "positive_bound_copies": positive, "settled": sum(a.settled for a in accumulators),
                "pending": len(self._pending), "settled_weight": sum((a.weight for a in accumulators), F(0)),
                "copy_bounds": bounds, "residual": residual, "bound_squared": combined,
                "bound_squared_cauchy": cauchy, "sum_sqrt_upper": h_upper,
                "sqrt_enclosure_bits": sqrt_bits, "own_loss": own, "expert_losses": other,
                "expert_regrets": expert_regrets, "bin_residuals": bin_residuals,
                "mixed_action_loss": mixed if cfg.decision_features else None,
                "action_losses": action_losses if cfg.decision_features else None,
                "action_regrets": action_regrets if cfg.decision_features else None,
                "smoothing_slack": slack if cfg.decision_features else None}
