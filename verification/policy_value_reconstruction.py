"""Finite witnesses for the Task 22B policy/value reconstruction bounds.

The mathematical statements live in
``formalism/10_policy_value_reconstruction.md``.  This module makes their
finite boundary cases executable.  It is deliberately a transparent decoder
and decision-harness reference, not a learner and not an empirical certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf, isfinite, log, sqrt
from typing import Hashable, Mapping, Sequence


State = Hashable
Action = Hashable
ScoreTable = Mapping[State, Mapping[Action, float]]


def _nonnegative_radius(value: float, name: str) -> float:
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


@dataclass(frozen=True)
class ArgmaxDecoder:
    """A finite legal-action contract with an explicit deterministic tie rule."""

    version: str
    legal_actions: Mapping[State, tuple[Action, ...]]
    tie_priority: Mapping[State, tuple[Action, ...]]

    def __post_init__(self) -> None:
        if not self.version:
            raise ValueError("decoder version must be nonempty")
        if not self.legal_actions:
            raise ValueError("decoder requires at least one state")
        if set(self.legal_actions) != set(self.tie_priority):
            raise ValueError("legal actions and tie priorities need the same states")
        for state, actions in self.legal_actions.items():
            priority = self.tie_priority[state]
            if not actions or len(set(actions)) != len(actions):
                raise ValueError("every legal-action set must be finite, nonempty, and unique")
            if len(set(priority)) != len(priority) or set(priority) != set(actions):
                raise ValueError("tie priority must order every legal action exactly once")

    def validate_scores(self, scores: ScoreTable) -> None:
        if set(scores) != set(self.legal_actions):
            raise ValueError("score table must cover exactly the decoder state domain")
        for state in self.legal_actions:
            self.validate_score_row(scores, state)

    def validate_score_row(self, scores: ScoreTable, state: State) -> None:
        if state not in self.legal_actions or state not in scores:
            raise ValueError("score row state must belong to the decoder domain")
        actions = self.legal_actions[state]
        row = scores[state]
        if set(row) != set(actions):
            raise ValueError("each score row must cover exactly the legal actions")
        if any(not isfinite(float(row[action])) for action in actions):
            raise ValueError("action scores must be finite")

    def decode_state(self, scores: ScoreTable, state: State) -> Action:
        self.validate_score_row(scores, state)
        actions = self.legal_actions[state]
        row = scores[state]
        best = max(float(row[action]) for action in actions)
        return next(action for action in self.tie_priority[state] if float(row[action]) == best)

    def decode(self, scores: ScoreTable) -> dict[State, Action]:
        self.validate_scores(scores)
        return {state: self.decode_state(scores, state) for state in self.legal_actions}


@dataclass(frozen=True)
class FinitePolicy:
    """A deterministic policy bound to the decoder contract it expects."""

    version: str
    decoder_version: str
    choices: Mapping[State, Action]

    def validate(self, decoder: ArgmaxDecoder) -> None:
        if not self.version:
            raise ValueError("policy version must be nonempty")
        if self.decoder_version != decoder.version:
            raise ValueError("policy and decoder versions do not match")
        if set(self.choices) != set(decoder.legal_actions):
            raise ValueError("policy must cover exactly the decoder state domain")
        if any(
            action not in decoder.legal_actions[state]
            for state, action in self.choices.items()
        ):
            raise ValueError("policy choice must be legal at every state")


@dataclass(frozen=True)
class FiniteDistribution:
    """A named probability distribution on a finite subset of policy states."""

    name: str
    version: str
    weights: Mapping[State, float]

    def __post_init__(self) -> None:
        if not self.name or not self.version or not self.weights:
            raise ValueError("distribution name, version, and support must be nonempty")
        values = tuple(float(value) for value in self.weights.values())
        if any(not isfinite(value) or value < 0.0 for value in values):
            raise ValueError("distribution weights must be finite and nonnegative")
        if abs(sum(values) - 1.0) > 1e-12:
            raise ValueError("distribution weights must sum to one")

    def mass(self, states: set[State]) -> float:
        return sum(float(weight) for state, weight in self.weights.items() if state in states)


@dataclass(frozen=True)
class OracleReconstructionBound:
    """The evaluated terms in the Task 22B raw oracle inequality."""

    policy_version: str
    decoder_version: str
    distribution_name: str
    distribution_version: str
    rho: float
    disagreement: float
    error_event_mass: float
    small_gap_event_mass: float

    @property
    def union_upper_bound(self) -> float:
        return self.error_event_mass + self.small_gap_event_mass

    @property
    def clipped_upper_bound(self) -> float:
        return min(1.0, self.union_upper_bound)


def canonical_score_encoding(
    policy: FinitePolicy, decoder: ArgmaxDecoder
) -> dict[State, dict[Action, float]]:
    """Encode a policy by one-hot action scores with unit action gap."""

    policy.validate(decoder)
    return {
        state: {
            action: 1.0 if action == policy.choices[state] else 0.0
            for action in decoder.legal_actions[state]
        }
        for state in decoder.legal_actions
    }


def is_in_canonical_encoder_image(scores: ScoreTable, decoder: ArgmaxDecoder) -> bool:
    """Whether scores equal the canonical re-encoding of their decoded policy."""

    try:
        decoded = decoder.decode(scores)
    except ValueError:
        return False
    return all(
        float(scores[state][action]) == (1.0 if action == decoded[state] else 0.0)
        for state, actions in decoder.legal_actions.items()
        for action in actions
    )


def coordinate_error(
    intended_scores: ScoreTable,
    approximate_scores: ScoreTable,
    decoder: ArgmaxDecoder,
    state: State,
) -> float:
    return max(
        abs(float(approximate_scores[state][action]) - float(intended_scores[state][action]))
        for action in decoder.legal_actions[state]
    )


def policy_action_gap(
    policy: FinitePolicy,
    intended_scores: ScoreTable,
    decoder: ArgmaxDecoder,
    state: State,
) -> float:
    """Gap from the intended policy action; forced actions have infinite gap."""

    actions = decoder.legal_actions[state]
    if len(actions) == 1:
        return inf
    intended = policy.choices[state]
    alternatives = (action for action in actions if action != intended)
    return float(intended_scores[state][intended]) - max(
        float(intended_scores[state][action]) for action in alternatives
    )


def estimated_winner_and_gap(
    scores: ScoreTable, decoder: ArgmaxDecoder, state: State
) -> tuple[Action, float]:
    """Return the tie-broken estimated winner and its gap over other actions."""

    winner = decoder.decode_state(scores, state)
    actions = decoder.legal_actions[state]
    if len(actions) == 1:
        return winner, inf
    return winner, float(scores[state][winner]) - max(
        float(scores[state][action]) for action in actions if action != winner
    )


def oracle_reconstruction_bound(
    policy: FinitePolicy,
    intended_scores: ScoreTable,
    approximate_scores: ScoreTable,
    decoder: ArgmaxDecoder,
    distribution: FiniteDistribution,
    rho: float,
) -> OracleReconstructionBound:
    """Evaluate the raw disagreement/error/small-gap terms on a finite domain."""

    rho = _nonnegative_radius(rho, "rho")
    policy.validate(decoder)
    decoder.validate_scores(intended_scores)
    decoder.validate_scores(approximate_scores)
    if not set(distribution.weights).issubset(decoder.legal_actions):
        raise ValueError("evaluation support must lie in the policy state domain")

    decoded_intended = decoder.decode(intended_scores)
    for state in distribution.weights:
        if decoded_intended[state] != policy.choices[state]:
            raise ValueError("the intended policy action must win under intended scores")

    decoded_approximate = decoder.decode(approximate_scores)
    disagreements: set[State] = set()
    error_events: set[State] = set()
    small_gap_events: set[State] = set()
    for state in distribution.weights:
        if decoded_approximate[state] != policy.choices[state]:
            disagreements.add(state)
        if coordinate_error(intended_scores, approximate_scores, decoder, state) > rho:
            error_events.add(state)
        if policy_action_gap(policy, intended_scores, decoder, state) <= 2.0 * rho:
            small_gap_events.add(state)

    result = OracleReconstructionBound(
        policy.version,
        decoder.version,
        distribution.name,
        distribution.version,
        rho,
        distribution.mass(disagreements),
        distribution.mass(error_events),
        distribution.mass(small_gap_events),
    )
    if result.disagreement > result.union_upper_bound + 1e-12:
        raise AssertionError("finite fixture violated the oracle reconstruction theorem")
    return result


def certified_event_mass_risk_bound(eta_error: float, eta_gap: float) -> float:
    """Clip the corollary obtained from jointly accepted event-mass bounds."""

    eta_error = float(eta_error)
    eta_gap = float(eta_gap)
    if any(not isfinite(value) or value < 0.0 or value > 1.0 for value in (eta_error, eta_gap)):
        raise ValueError("event-mass bounds must lie in [0,1]")
    return min(1.0, eta_error + eta_gap)


def coordinate_gap_radius(rho: float) -> float:
    """Generic pairwise-gap error radius induced by coordinate radius rho."""

    return 2.0 * _nonnegative_radius(rho, "rho")


def conservative_decode_state(
    scores: ScoreTable,
    decoder: ArgmaxDecoder,
    state: State,
    gap_error_radius: float,
) -> Action | None:
    """Use a caller-supplied accepted gap radius to certify an estimated winner."""

    gap_error_radius = _nonnegative_radius(gap_error_radius, "gap_error_radius")
    winner, gap = estimated_winner_and_gap(scores, decoder, state)
    return winner if gap > gap_error_radius else None


@dataclass(frozen=True)
class ValueDecisionHarness:
    """One-step value decoder with every behavioral input exposed.

    ``orientation[state]`` is ``+1`` when the declared perspective maximizes
    return at that state and ``-1`` when it minimizes it.  Rewards, transitions,
    discount, perspective, legal actions, and tie handling are therefore all
    visible rather than hidden in a policy lookup.
    """

    version: str
    decoder: ArgmaxDecoder
    transitions: Mapping[tuple[State, Action], tuple[tuple[State, float], ...]]
    rewards: Mapping[tuple[State, Action], float]
    discount: float
    orientation: Mapping[State, int]

    def __post_init__(self) -> None:
        if not self.version:
            raise ValueError("harness version must be nonempty")
        if not isfinite(float(self.discount)) or not 0.0 <= float(self.discount) <= 1.0:
            raise ValueError("discount must lie in [0,1]")
        if set(self.orientation) != set(self.decoder.legal_actions):
            raise ValueError("orientation must cover exactly the decoder states")
        if any(value not in (-1, 1) for value in self.orientation.values()):
            raise ValueError("orientation must be +1 or -1")
        expected = {
            (state, action)
            for state, actions in self.decoder.legal_actions.items()
            for action in actions
        }
        if set(self.transitions) != expected or set(self.rewards) != expected:
            raise ValueError("harness must expose reward and transition for every legal action")
        if any(not isfinite(float(reward)) for reward in self.rewards.values()):
            raise ValueError("rewards must be finite")
        for successors in self.transitions.values():
            if not successors:
                raise ValueError("each transition distribution must be nonempty")
            probabilities = tuple(float(probability) for _, probability in successors)
            if any(not isfinite(value) or value < 0.0 for value in probabilities):
                raise ValueError("transition probabilities must be finite and nonnegative")
            if abs(sum(probabilities) - 1.0) > 1e-12:
                raise ValueError("transition probabilities must sum to one")

    def action_scores(self, values: Mapping[State, float]) -> dict[State, dict[Action, float]]:
        scores: dict[State, dict[Action, float]] = {}
        for state, actions in self.decoder.legal_actions.items():
            row: dict[Action, float] = {}
            sign = self.orientation[state]
            for action in actions:
                continuation = 0.0
                for successor, probability in self.transitions[(state, action)]:
                    if successor not in values or not isfinite(float(values[successor])):
                        raise ValueError("values must be finite on every successor state")
                    continuation += float(probability) * float(values[successor])
                row[action] = sign * (
                    float(self.rewards[(state, action)])
                    + float(self.discount) * continuation
                )
            scores[state] = row
        return scores

    def score_error_envelope(
        self, value_error_envelope: Mapping[State, float]
    ) -> dict[State, dict[Action, float]]:
        """Propagate accepted successor-value radii through an exact harness."""

        result: dict[State, dict[Action, float]] = {}
        for state, actions in self.decoder.legal_actions.items():
            row: dict[Action, float] = {}
            for action in actions:
                bound = 0.0
                for successor, probability in self.transitions[(state, action)]:
                    if successor not in value_error_envelope:
                        raise ValueError("an error radius is required for every successor")
                    radius = _nonnegative_radius(
                        value_error_envelope[successor], "value error radius"
                    )
                    bound += float(probability) * radius
                row[action] = float(self.discount) * bound
            result[state] = row
        return result


def modal_action(
    probabilities: Mapping[Action, float], tie_priority: Sequence[Action]
) -> Action:
    """Decode only the modal action of a categorical policy distribution."""

    if not probabilities or set(probabilities) != set(tie_priority):
        raise ValueError("probabilities and tie priority need the same nonempty actions")
    values = tuple(float(value) for value in probabilities.values())
    if any(not isfinite(value) or value < 0.0 for value in values):
        raise ValueError("probabilities must be finite and nonnegative")
    if abs(sum(values) - 1.0) > 1e-12:
        raise ValueError("probabilities must sum to one")
    best = max(values)
    return next(action for action in tie_priority if float(probabilities[action]) == best)


def total_variation(
    left: Mapping[Action, float], right: Mapping[Action, float]
) -> float:
    """Total-variation distance between two finite categorical policies."""

    actions = set(left) | set(right)
    if not actions:
        raise ValueError("categorical distributions must be nonempty")
    for distribution in (left, right):
        values = tuple(float(distribution.get(action, 0.0)) for action in actions)
        if any(not isfinite(value) or value < 0.0 for value in values):
            raise ValueError("probabilities must be finite and nonnegative")
        if abs(sum(values) - 1.0) > 1e-12:
            raise ValueError("probabilities must sum to one")
    return 0.5 * sum(
        abs(float(left.get(action, 0.0)) - float(right.get(action, 0.0)))
        for action in actions
    )


def iid_disagreement_upper_bound(
    disagreements: int, sample_size: int, delta: float
) -> float:
    """One-sided Hoeffding bound for a fixed pair on IID states from named mu."""

    if isinstance(disagreements, bool) or isinstance(sample_size, bool):
        raise ValueError("counts must be integers")
    if not isinstance(disagreements, int) or not isinstance(sample_size, int):
        raise ValueError("counts must be integers")
    if sample_size <= 0 or not 0 <= disagreements <= sample_size:
        raise ValueError("disagreements must lie between zero and sample size")
    delta = float(delta)
    if not isfinite(delta) or not 0.0 < delta < 1.0:
        raise ValueError("delta must lie strictly between zero and one")
    empirical = disagreements / sample_size
    radius = sqrt(log(1.0 / delta) / (2.0 * sample_size))
    return min(1.0, empirical + radius)


def trajectory_divergence_union_bound(
    matched_history_step_bounds: Sequence[float],
) -> float:
    """Union bound given stepwise action-error bounds conditional on no prior split."""

    bounds = tuple(
        _nonnegative_radius(value, "stepwise divergence bound")
        for value in matched_history_step_bounds
    )
    if any(value > 1.0 for value in bounds):
        raise ValueError("stepwise divergence bounds must lie in [0,1]")
    return min(1.0, sum(bounds))
