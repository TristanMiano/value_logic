"""Finite regression witnesses for the Task 15 encoding contract.

This module does not implement a neural network.  It makes four exact interface
properties executable: dependency-scoped atom inputs, candidate equivariance,
typed-DAG isomorphism, and consumer-relative sufficiency.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Hashable, Iterable, Mapping, Sequence

from verification.footprints import RecordKey


FrozenValue = Hashable


def freeze(value: Any) -> FrozenValue:
    """Return a deterministic, hashable representation of finite test data."""

    if isinstance(value, Mapping):
        items = ((freeze(key), freeze(item)) for key, item in value.items())
        return ("map", tuple(sorted(items, key=repr)))
    if isinstance(value, (set, frozenset)):
        return ("set", tuple(sorted((freeze(item) for item in value), key=repr)))
    if isinstance(value, (list, tuple)):
        return ("seq", tuple(freeze(item) for item in value))
    if isinstance(value, (str, bytes, int, float, bool, type(None))):
        return value
    if hasattr(value, "__dict__"):
        return (type(value).__qualname__, freeze(vars(value)))
    raise TypeError(f"unsupported finite witness value: {type(value).__qualname__}")


@dataclass(frozen=True)
class AtomAddress:
    """Compact exact address used by the encoding witness."""

    kind: str
    subject: str
    scope: str
    criterion: str
    mode: str
    parameters: tuple[tuple[str, FrozenValue], ...] = ()


@dataclass(frozen=True)
class DependencyInput:
    """An address and the canonical projection of exactly its read keys."""

    address: AtomAddress
    present: tuple[tuple[RecordKey, FrozenValue], ...]
    missing: tuple[RecordKey, ...]
    opaque_handles: tuple[tuple[RecordKey, FrozenValue], ...]


def dependency_input(
    address: AtomAddress,
    environment: Mapping[RecordKey, Any],
    footprint: Iterable[RecordKey],
    *,
    opaque_namespaces: Iterable[str] = (),
) -> DependencyInput:
    """Project an environment onto a footprint with explicit missingness.

    Opaque handles remain in the complete projection and are additionally
    identified for the external registry/checker path.
    """

    keys = tuple(sorted(set(footprint)))
    opaque = frozenset(opaque_namespaces)
    present = tuple((key, freeze(environment[key])) for key in keys if key in environment)
    missing = tuple(key for key in keys if key not in environment)
    handles = tuple((key, value) for key, value in present if key.namespace in opaque)
    return DependencyInput(address, present, missing, handles)


def candidate_conditioned_scores(
    candidates: Iterable[tuple[str, Any]],
    scorer: Callable[[Any], Any],
) -> dict[str, FrozenValue]:
    """Apply one shared scorer and restore exact external identities."""

    result: dict[str, FrozenValue] = {}
    for candidate_id, features in candidates:
        if candidate_id in result:
            raise ValueError(f"duplicate candidate identity: {candidate_id}")
        result[candidate_id] = freeze(scorer(features))
    return result


def comparison_counts(
    candidate_ids: Sequence[str],
    requested_edges: Iterable[tuple[str, str]],
) -> tuple[int, int]:
    """Return dense ordered-pair and valid sparse-edge counts."""

    identities = set(candidate_ids)
    if len(identities) != len(candidate_ids):
        raise ValueError("candidate identities must be unique")
    edges = set(requested_edges)
    for left, right in edges:
        if left == right or left not in identities or right not in identities:
            raise ValueError(f"invalid requested comparison edge: {(left, right)!r}")
    n = len(candidate_ids)
    return n * (n - 1), len(edges)


@dataclass(frozen=True)
class TypedPlanNode:
    """The fields a plan-DAG isomorphism must preserve."""

    name: str
    operator: str
    version: str
    predecessors: tuple[tuple[str, str], ...]
    output_type: str
    frame: str
    metric: str
    grade_schema: tuple[tuple[str, str, str], ...]
    checker: str
    checker_version: str
    assumptions: tuple[str, ...]
    rank: int

    def invariant_fields(self) -> tuple[Any, ...]:
        return (
            self.operator,
            self.version,
            self.output_type,
            self.frame,
            self.metric,
            self.grade_schema,
            self.checker,
            self.checker_version,
            self.assumptions,
            self.rank,
        )


@dataclass(frozen=True)
class TypedPlanDAG:
    root: str
    nodes: tuple[TypedPlanNode, ...]

    def by_name(self) -> dict[str, TypedPlanNode]:
        result = {node.name: node for node in self.nodes}
        if len(result) != len(self.nodes) or self.root not in result:
            raise ValueError("plan node names must be unique and include the root")
        return result


def plan_isomorphism_holds(
    left: TypedPlanDAG,
    right: TypedPlanDAG,
    renaming: Mapping[str, str],
) -> bool:
    """Check one proposed root-, port-, and type-preserving DAG isomorphism."""

    left_nodes = left.by_name()
    right_nodes = right.by_name()
    if set(renaming) != set(left_nodes) or set(renaming.values()) != set(right_nodes):
        return False
    if len(set(renaming.values())) != len(renaming) or renaming[left.root] != right.root:
        return False
    for name, node in left_nodes.items():
        other = right_nodes[renaming[name]]
        if node.invariant_fields() != other.invariant_fields():
            return False
        mapped_predecessors = tuple((port, renaming[pred]) for port, pred in node.predecessors)
        if mapped_predecessors != other.predecessors:
            return False
    return True


@dataclass(frozen=True)
class SufficiencyViolation:
    left_index: int
    right_index: int
    consumer: str
    shared_code: FrozenValue


def sufficiency_violations(
    samples: Sequence[Any],
    code: Callable[[Any], Any],
    consumers: Mapping[str, Callable[[Any], Any]],
) -> tuple[SufficiencyViolation, ...]:
    """Find equal codes that disagree on a declared consumer."""

    codes = [freeze(code(sample)) for sample in samples]
    violations: list[SufficiencyViolation] = []
    for left in range(len(samples)):
        for right in range(left + 1, len(samples)):
            if codes[left] != codes[right]:
                continue
            for name, consumer in consumers.items():
                if freeze(consumer(samples[left])) != freeze(consumer(samples[right])):
                    violations.append(SufficiencyViolation(left, right, name, codes[left]))
    return tuple(violations)
