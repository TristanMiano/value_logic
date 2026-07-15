"""Finite witnesses for the Task 17 representation theorems.

The mathematical proofs live in ``ml/03_representation_theorems.md``.  This
module keeps the boundary cases executable: factorization collisions,
conservative margin decoding, elementary exact ReLU/CPWL identities, hard
seams, registry extension, normalized dual-use channels, and a small
proof-erased CPWL plan.  It is not a neural trainer or proof assistant.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Any, Callable, Hashable, Iterable, Mapping, Sequence


def factorization_collisions(
    samples: Iterable[Any],
    *,
    code: Callable[[Any], Hashable],
    observation: Callable[[Any], Hashable],
) -> tuple[tuple[int, int], ...]:
    """Return equal-code pairs that a requested observation separates."""

    samples = tuple(samples)
    return tuple(
        (left, right)
        for left, right in combinations(range(len(samples)), 2)
        if code(samples[left]) == code(samples[right])
        and observation(samples[left]) != observation(samples[right])
    )


def canonical_partition(
    samples: Iterable[Any], observation: Callable[[Any], Hashable]
) -> tuple[frozenset[int], ...]:
    """Finite canonical quotient by equality of the requested observation."""

    fibers: dict[Hashable, set[int]] = {}
    for index, sample in enumerate(samples):
        fibers.setdefault(observation(sample), set()).add(index)
    return tuple(
        sorted(
            (frozenset(indices) for indices in fibers.values()),
            key=lambda block: min(block),
        )
    )


class RobustValue(str, Enum):
    SUPPORTED = "supported"
    OPEN = "open"
    REFUTED = "refuted"


def propagated_affine_error(
    coefficients: Sequence[float], statistic_errors: Sequence[float]
) -> float:
    """L-infinity coordinate bounds propagated through one affine margin."""

    if len(coefficients) != len(statistic_errors):
        raise ValueError("one error bound is required per coefficient")
    if any(error < 0 for error in statistic_errors):
        raise ValueError("error bounds must be nonnegative")
    return sum(abs(coefficient) * error for coefficient, error in zip(coefficients, statistic_errors))


def robust_upper_risk(
    estimate: float,
    threshold: float,
    error_radius: float,
    *,
    can_support: bool = True,
    can_refute: bool = True,
) -> RobustValue:
    """Conservative interval decoder with inclusive support and strict refutation."""

    if error_radius < 0:
        raise ValueError("error radius must be nonnegative")
    lower = estimate - error_radius
    upper = estimate + error_radius
    if upper <= threshold and can_support:
        return RobustValue.SUPPORTED
    if lower > threshold and can_refute:
        return RobustValue.REFUTED
    return RobustValue.OPEN


def ideal_upper_risk(value: float, threshold: float) -> RobustValue:
    return RobustValue.SUPPORTED if value <= threshold else RobustValue.REFUTED


def relu(value: float) -> float:
    return max(0.0, float(value))


def relu_max(left: float, right: float) -> float:
    """Exact max identity used by finite CPWL constructions."""

    return relu(left - right) + right


def balanced_relu_max(values: Sequence[float]) -> float:
    """Balanced binary max; each round is one conceptual ReLU max layer."""

    if not values:
        raise ValueError("maximum requires at least one input")
    layer = [float(value) for value in values]
    while len(layer) > 1:
        next_layer: list[float] = []
        for index in range(0, len(layer), 2):
            if index + 1 == len(layer):
                next_layer.append(layer[index])
            else:
                next_layer.append(relu_max(layer[index], layer[index + 1]))
        layer = next_layer
    return layer[0]


@dataclass(frozen=True)
class AffineMap:
    matrix: tuple[tuple[float, ...], ...]
    bias: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.matrix) != len(self.bias):
            raise ValueError("one bias is required per output row")
        widths = {len(row) for row in self.matrix}
        if len(widths) > 1:
            raise ValueError("matrix rows must have a common width")

    def __call__(self, point: Sequence[float]) -> tuple[float, ...]:
        if self.matrix and len(point) != len(self.matrix[0]):
            raise ValueError("point dimension does not match affine map")
        return tuple(
            sum(weight * coordinate for weight, coordinate in zip(row, point)) + offset
            for row, offset in zip(self.matrix, self.bias)
        )


def traces_agree(
    left: AffineMap,
    right: AffineMap,
    face_points: Iterable[Sequence[float]],
    *,
    tolerance: float = 1e-12,
) -> bool:
    """Finite face witness used by the seam regression examples."""

    for point in face_points:
        if any(
            abs(a - b) > tolerance
            for a, b in zip(left(point), right(point))
        ):
            return False
    return True


def matrix_rank(matrix: Sequence[Sequence[float]], *, tolerance: float = 1e-12) -> int:
    """Small Gaussian-elimination helper for the rank-one seam witness."""

    work = [list(map(float, row)) for row in matrix]
    if not work:
        return 0
    columns = len(work[0])
    if any(len(row) != columns for row in work):
        raise ValueError("matrix rows must have a common width")
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(work)) if abs(work[row][column]) > tolerance),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            multiplier = work[row][column]
            if abs(multiplier) <= tolerance:
                continue
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def jacobian_difference_rank(left: AffineMap, right: AffineMap) -> int:
    if len(left.matrix) != len(right.matrix):
        raise ValueError("output dimensions must match")
    difference = tuple(
        tuple(a - b for a, b in zip(left_row, right_row))
        for left_row, right_row in zip(left.matrix, right.matrix)
    )
    return matrix_rank(difference)


def fixed_indexed_lookup(
    registry: Sequence[str], outputs: Sequence[Any], candidate_id: str
) -> Any:
    """A fixed output interface has no value for an unregistered candidate."""

    if len(registry) != len(outputs):
        raise ValueError("registry and output coordinates must have equal length")
    try:
        return outputs[registry.index(candidate_id)]
    except ValueError as error:
        raise KeyError(candidate_id) from error


def shared_candidate_scores(
    candidates: Iterable[tuple[str, Any]], scorer: Callable[[Any], float]
) -> dict[str, float]:
    """Pointwise shared scoring restores identities through the external registry."""

    result: dict[str, float] = {}
    for candidate_id, features in candidates:
        if candidate_id in result:
            raise ValueError("candidate identities must be unique")
        result[candidate_id] = float(scorer(features))
    return result


def undominated_in_evaluated_set(
    candidate_id: str,
    evaluated_candidates: Iterable[str],
    dominates: Iterable[tuple[str, str]],
) -> bool:
    evaluated = frozenset(evaluated_candidates)
    if candidate_id not in evaluated:
        raise ValueError("candidate must belong to the evaluated set")
    return not any(
        stronger in evaluated and weaker == candidate_id
        for stronger, weaker in dominates
    )


@dataclass(frozen=True)
class DualUseCode:
    states: tuple[RobustValue, ...]
    normalized_surplus: tuple[float, ...]


def dual_use_code(
    states: Sequence[RobustValue],
    margins: Sequence[float],
    scales: Sequence[float],
) -> DualUseCode:
    """Named exact state plus normalized positive surplus for each hypothesis."""

    if not (len(states) == len(margins) == len(scales)):
        raise ValueError("states, margins, and scales must align")
    if any(scale <= 0 for scale in scales):
        raise ValueError("normalization scales must be positive")
    surplus = tuple(
        relu(margin / scale) if state is RobustValue.SUPPORTED else 0.0
        for state, margin, scale in zip(states, margins, scales)
    )
    return DualUseCode(tuple(states), surplus)


def affine_consumer(
    code: DualUseCode, matrix: Sequence[Sequence[float]], bias: Sequence[float]
) -> tuple[float, ...]:
    if len(matrix) != len(bias):
        raise ValueError("one bias is required per consumer output")
    if any(len(row) != len(code.normalized_surplus) for row in matrix):
        raise ValueError("consumer row does not match channel count")
    return tuple(
        sum(weight * value for weight, value in zip(row, code.normalized_surplus)) + offset
        for row, offset in zip(matrix, bias)
    )


@dataclass(frozen=True)
class CPWLPlanNode:
    name: str
    operation: str
    predecessors: tuple[str, ...] = ()
    weights: tuple[float, ...] = ()
    bias: float = 0.0


def evaluate_cpwl_plan(
    point: Sequence[float],
    nodes: Sequence[CPWLPlanNode],
    outputs: Sequence[str],
) -> tuple[float, ...]:
    """Evaluate a topologically ordered proof-erased scalar CPWL plan DAG."""

    values: dict[str, float] = {}
    for node in nodes:
        if node.name in values:
            raise ValueError("plan node names must be unique")
        try:
            inputs = tuple(values[name] for name in node.predecessors)
        except KeyError as error:
            raise ValueError("nodes must be in topological order") from error

        if node.operation == "input":
            if len(node.weights) != len(point):
                raise ValueError("input weights must match point dimension")
            value = sum(weight * coordinate for weight, coordinate in zip(node.weights, point)) + node.bias
        elif node.operation == "affine":
            if len(node.weights) != len(inputs):
                raise ValueError("affine weights must match predecessors")
            value = sum(weight * item for weight, item in zip(node.weights, inputs)) + node.bias
        elif node.operation == "relu":
            if len(inputs) != 1:
                raise ValueError("ReLU nodes require one predecessor")
            value = relu(inputs[0])
        elif node.operation == "max":
            value = balanced_relu_max(inputs)
        elif node.operation == "min":
            value = -balanced_relu_max(tuple(-item for item in inputs))
        else:
            raise ValueError(f"unsupported CPWL operation: {node.operation}")
        values[node.name] = value

    try:
        return tuple(values[name] for name in outputs)
    except KeyError as error:
        raise ValueError("unknown plan output") from error
