"""Finite witnesses for proof-carrying plans and ranked assessment.

This module is deliberately smaller than a programming language.  A plan is a
finite typed DAG whose nodes expose one payload transformer, one quantitative
grade transformer, and one externally registered local certificate.  The
corresponding proofs are in ``formalism/08c_proof_carrying_plans.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Callable, Mapping


class PlanContractError(ValueError):
    """A plan, certificate, support graph, or rank contract is invalid."""


@dataclass(frozen=True, order=True)
class ResourceBound:
    dimension: str
    unit: str
    amount: float

    def __post_init__(self) -> None:
        if not self.dimension or not self.unit or self.amount < 0:
            raise ValueError("resource bounds require a dimension, unit, and nonnegative amount")


@dataclass(frozen=True)
class QuantitativeGrade:
    error_bound: float
    metric: str
    resources: tuple[ResourceBound, ...] = ()

    def __post_init__(self) -> None:
        if self.error_bound < 0 or not self.metric:
            raise ValueError("grades require a nonnegative error bound and named metric")
        keys = [(bound.dimension, bound.unit) for bound in self.resources]
        if len(keys) != len(set(keys)):
            raise ValueError("a grade repeats a typed resource dimension")


@dataclass(frozen=True)
class EvidenceRecord:
    """An independently supplied local certificate registry entry."""

    certificate_id: str
    node: str
    checker: str
    accepted: bool
    metric: str
    local_error_bound: float
    local_resources: tuple[ResourceBound, ...]
    sources: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.certificate_id or not self.node or not self.checker or not self.sources:
            raise ValueError("evidence records require identity, checker, node, and provenance")
        if self.local_error_bound < 0:
            raise ValueError("local error bounds must be nonnegative")


PayloadTransformer = Callable[[object, tuple[object, ...]], object]


@dataclass(frozen=True)
class PlanNode:
    """One generic typed constructor instance in a finite plan DAG."""

    name: str
    predecessors: tuple[str, ...]
    input_types: tuple[str, ...]
    input_frames: tuple[str, ...]
    input_metrics: tuple[str, ...]
    output_type: str
    output_frame: str
    output_metric: str
    transform: PayloadTransformer
    sensitivities: tuple[float, ...]
    local_error_bound: float
    local_resources: tuple[ResourceBound, ...]
    resource_operators: tuple[tuple[str, str, str], ...]
    certificate_id: str

    def __post_init__(self) -> None:
        arity = len(self.predecessors)
        if not self.name or not self.output_type or not self.output_frame or not self.output_metric:
            raise ValueError("plan nodes require named typed outputs")
        if not (
            len(self.input_types)
            == len(self.input_frames)
            == len(self.input_metrics)
            == len(self.sensitivities)
            == arity
        ):
            raise ValueError("predecessor interfaces and sensitivities must match node arity")
        if self.local_error_bound < 0 or any(value < 0 for value in self.sensitivities):
            raise ValueError("error bounds and sensitivities must be nonnegative")
        resource_keys = [
            (bound.dimension, bound.unit)
            for bound in self.local_resources
        ]
        if len(resource_keys) != len(set(resource_keys)):
            raise ValueError("a node repeats a typed local resource dimension")
        operator_keys = [(dimension, unit) for dimension, unit, _ in self.resource_operators]
        if len(operator_keys) != len(set(operator_keys)):
            raise ValueError("resource aggregation policy repeats a typed dimension")
        if any(operator not in {"sum", "max"} for _, _, operator in self.resource_operators):
            raise ValueError("resource aggregation is either sum or max")


@dataclass(frozen=True)
class PlanDAG:
    nodes: tuple[PlanNode, ...]
    root: str


@dataclass(frozen=True)
class ProofTerm:
    node: str
    local_certificate: str
    premises: tuple["ProofTerm", ...]
    grade: QuantitativeGrade
    provenance: tuple[str, ...]


@dataclass(frozen=True)
class AnnotatedResult:
    payload: object
    grade: QuantitativeGrade
    certificate: ProofTerm


def _node_map(plan: PlanDAG) -> dict[str, PlanNode]:
    result = {node.name: node for node in plan.nodes}
    if len(result) != len(plan.nodes):
        raise PlanContractError("plan node names must be unique")
    if plan.root not in result:
        raise PlanContractError("plan root is missing")
    return result


def topological_order(plan: PlanDAG) -> tuple[str, ...]:
    """Return a dependency-first order, rejecting missing nodes and cycles."""

    nodes = _node_map(plan)
    visiting: set[str] = set()
    visited: set[str] = set()
    order: list[str] = []

    def visit(name: str) -> None:
        if name in visiting:
            raise PlanContractError("cyclic plan is outside the finite well-founded contract")
        if name in visited:
            return
        if name not in nodes:
            raise PlanContractError(f"plan references missing node {name!r}")
        visiting.add(name)
        for predecessor in nodes[name].predecessors:
            visit(predecessor)
        visiting.remove(name)
        visited.add(name)
        order.append(name)

    visit(plan.root)
    return tuple(order)


def _validate_interfaces(plan: PlanDAG, order: tuple[str, ...]) -> None:
    nodes = _node_map(plan)
    for name in order:
        node = nodes[name]
        for index, predecessor_name in enumerate(node.predecessors):
            predecessor = nodes[predecessor_name]
            if predecessor.output_type != node.input_types[index]:
                raise PlanContractError(f"type mismatch on {predecessor_name!r} -> {name!r}")
            if predecessor.output_frame != node.input_frames[index]:
                raise PlanContractError(f"frame mismatch on {predecessor_name!r} -> {name!r}")
            if predecessor.output_metric != node.input_metrics[index]:
                raise PlanContractError(f"metric mismatch on {predecessor_name!r} -> {name!r}")


def _resource_map(resources: tuple[ResourceBound, ...]) -> dict[tuple[str, str], float]:
    return {(bound.dimension, bound.unit): bound.amount for bound in resources}


def _aggregate_resources(
    node: PlanNode,
    premises: tuple[ProofTerm, ...],
) -> tuple[ResourceBound, ...]:
    local = _resource_map(node.local_resources)
    children = [_resource_map(premise.grade.resources) for premise in premises]
    policies = {
        (dimension, unit): operator
        for dimension, unit, operator in node.resource_operators
    }
    observed = set(local)
    for child in children:
        observed.update(child)
    if observed != set(policies):
        raise PlanContractError(
            f"node {node.name!r} must declare exactly one operator for every typed resource"
        )
    result = []
    for (dimension, unit), operator in sorted(policies.items()):
        local_amount = local.get((dimension, unit), 0.0)
        child_amounts = [child.get((dimension, unit), 0.0) for child in children]
        if operator == "sum":
            amount = local_amount + sum(child_amounts)
        else:
            amount = local_amount + (max(child_amounts) if child_amounts else 0.0)
        result.append(ResourceBound(dimension, unit, amount))
    return tuple(result)


def _local_evidence(
    node: PlanNode,
    registry: Mapping[str, EvidenceRecord],
) -> EvidenceRecord:
    evidence = registry.get(node.certificate_id)
    if evidence is None or not evidence.accepted:
        raise PlanContractError(f"node {node.name!r} lacks an accepted external certificate")
    if (
        evidence.node != node.name
        or evidence.metric != node.output_metric
        or not isclose(evidence.local_error_bound, node.local_error_bound)
        or evidence.local_resources != node.local_resources
    ):
        raise PlanContractError(f"certificate {evidence.certificate_id!r} does not match its node")
    return evidence


def _derived_grade(node: PlanNode, premises: tuple[ProofTerm, ...]) -> QuantitativeGrade:
    error_bound = node.local_error_bound + sum(
        sensitivity * premise.grade.error_bound
        for sensitivity, premise in zip(node.sensitivities, premises)
    )
    return QuantitativeGrade(
        error_bound=error_bound,
        metric=node.output_metric,
        resources=_aggregate_resources(node, premises),
    )


def execute_plain(plan: PlanDAG, external_input: object) -> object:
    """Execute only the ordinary payload computation."""

    order = topological_order(plan)
    _validate_interfaces(plan, order)
    nodes = _node_map(plan)
    payloads: dict[str, object] = {}
    for name in order:
        node = nodes[name]
        inputs = tuple(payloads[predecessor] for predecessor in node.predecessors)
        payloads[name] = node.transform(external_input, inputs)
    return payloads[plan.root]


def execute_annotated(
    plan: PlanDAG,
    external_input: object,
    registry: Mapping[str, EvidenceRecord],
) -> AnnotatedResult:
    """Execute payloads and build a checked composite certificate by induction."""

    order = topological_order(plan)
    _validate_interfaces(plan, order)
    nodes = _node_map(plan)
    payloads: dict[str, object] = {}
    terms: dict[str, ProofTerm] = {}
    for name in order:
        node = nodes[name]
        evidence = _local_evidence(node, registry)
        premises = tuple(terms[predecessor] for predecessor in node.predecessors)
        inputs = tuple(payloads[predecessor] for predecessor in node.predecessors)
        payloads[name] = node.transform(external_input, inputs)
        provenance = tuple(
            sorted(
                set(evidence.sources).union(
                    *(set(premise.provenance) for premise in premises)
                )
            )
        )
        terms[name] = ProofTerm(
            node=name,
            local_certificate=evidence.certificate_id,
            premises=premises,
            grade=_derived_grade(node, premises),
            provenance=provenance,
        )
    root = plan.root
    return AnnotatedResult(payloads[root], terms[root].grade, terms[root])


def verify_proof_term(
    plan: PlanDAG,
    term: ProofTerm,
    registry: Mapping[str, EvidenceRecord],
) -> bool:
    """Independently recheck the finite certificate tree and its grade."""

    order = topological_order(plan)
    _validate_interfaces(plan, order)
    nodes = _node_map(plan)

    def verify(current: ProofTerm, visiting: frozenset[str]) -> QuantitativeGrade:
        if current.node in visiting:
            raise PlanContractError("certificate term is cyclic")
        node = nodes.get(current.node)
        if node is None or current.local_certificate != node.certificate_id:
            raise PlanContractError("certificate term names the wrong plan node")
        if tuple(premise.node for premise in current.premises) != node.predecessors:
            raise PlanContractError("certificate premises do not match plan dependencies")
        evidence = _local_evidence(node, registry)
        for premise in current.premises:
            verify(premise, visiting | {current.node})
        expected = _derived_grade(node, current.premises)
        if not isclose(current.grade.error_bound, expected.error_bound):
            raise PlanContractError("certificate term has an incorrect propagated error bound")
        if current.grade.metric != expected.metric or current.grade.resources != expected.resources:
            raise PlanContractError("certificate term has an incorrect typed grade")
        expected_provenance = tuple(
            sorted(
                set(evidence.sources).union(
                    *(set(premise.provenance) for premise in current.premises)
                )
            )
        )
        if current.provenance != expected_provenance:
            raise PlanContractError("certificate term drops or invents provenance")
        return expected

    verify(term, frozenset())
    if term.node != plan.root:
        raise PlanContractError("certificate term does not prove the plan root")
    return True


@dataclass(frozen=True)
class SupportNode:
    """A support derivation node; bases carry a typed source kind."""

    name: str
    premises: tuple[str, ...] = ()
    base_kind: str | None = None

    def __post_init__(self) -> None:
        if not self.name or self.base_kind == "":
            raise ValueError("support nodes require a name and any base kind must be nonempty")


def grounded_sources(
    nodes: tuple[SupportNode, ...],
    target: str,
) -> tuple[str, ...]:
    """Return every typed base source below a finite acyclic support target."""

    index = {node.name: node for node in nodes}
    if len(index) != len(nodes) or target not in index:
        raise PlanContractError("support nodes must be unique and include the target")

    def visit(name: str, visiting: frozenset[str]) -> set[str]:
        if name in visiting:
            raise PlanContractError("closed mutual support is not an acyclic derivation")
        node = index.get(name)
        if node is None:
            raise PlanContractError(f"support derivation references missing node {name!r}")
        if node.base_kind is not None:
            if node.premises:
                raise PlanContractError("a typed base source cannot also be a derived rule node")
            return {f"{node.base_kind}:{node.name}"}
        if not node.premises:
            raise PlanContractError("a nonbase support node requires at least one premise")
        sources: set[str] = set()
        for premise in node.premises:
            sources.update(visit(premise, visiting | {name}))
        return sources

    return tuple(sorted(visit(target, frozenset())))


RankedEvaluator = Callable[[tuple[object, ...]], object]


@dataclass(frozen=True)
class EvaluationNode:
    name: str
    rank: int
    dependencies: tuple[str, ...]
    evaluator: RankedEvaluator

    def __post_init__(self) -> None:
        if not self.name or self.rank < 0:
            raise ValueError("evaluation nodes require a name and nonnegative rank")


def evaluate_stratified(
    nodes: tuple[EvaluationNode, ...],
    exogenous: Mapping[str, object],
) -> dict[str, object]:
    """Evaluate a finite lower-rank dependency system in its unique order."""

    index = {node.name: node for node in nodes}
    if len(index) != len(nodes):
        raise PlanContractError("evaluation node names must be unique")
    values: dict[str, object] = {}
    for node in sorted(nodes, key=lambda item: (item.rank, item.name)):
        arguments = []
        for dependency in node.dependencies:
            if dependency in index:
                if index[dependency].rank >= node.rank or dependency not in values:
                    raise PlanContractError("every internal evaluation dependency must have lower rank")
                arguments.append(values[dependency])
            elif dependency in exogenous:
                arguments.append(exogenous[dependency])
            else:
                raise PlanContractError(f"missing exogenous dependency {dependency!r}")
        value = node.evaluator(tuple(arguments))
        if value is None:
            raise PlanContractError("local evaluators must be total on their declared inputs")
        values[node.name] = value
    return values
