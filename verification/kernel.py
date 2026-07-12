"""Compact ``WF + K_3`` kernel for finite-stage license assessment.

The mathematical core deliberately has no closed ``ReasonCode`` enumeration.
Meaningful atoms are supported, open, or refuted.  Human-facing reason labels
are derived from the atom address and its witness or obstacle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Iterable, Mapping


class AtomValue(IntEnum):
    """Strong-Kleene values ordered for conjunctive meet."""

    REFUTED = 0
    OPEN = 1
    SUPPORTED = 2


class Outcome(Enum):
    """The four public outcomes derived from well-formedness and ``K_3``."""

    UNDEFINED = "Undefined"
    REFUSED = "Refused"
    WITHHELD = "Withheld"
    GRANTED = "Granted"


@dataclass(frozen=True, order=True)
class Interval:
    lower: float
    upper: float

    def __post_init__(self) -> None:
        if self.lower > self.upper:
            raise ValueError("interval lower bound exceeds upper bound")

    def contains(self, value: float) -> bool:
        return self.lower <= value <= self.upper

    def shift(self, amount: float) -> "Interval":
        return Interval(self.lower + amount, self.upper + amount)

    def overlaps(self, other: "Interval") -> bool:
        return not (self.upper < other.lower or other.upper < self.lower)

    def strictly_better_than(self, other: "Interval") -> bool:
        """Certify smaller-is-better dominance using separated intervals."""

        return self.upper < other.lower


@dataclass(frozen=True)
class Diagnostic:
    """Lossless atom-indexed diagnostic data.

    Exactly one of support, counterwitness, or obstacles is required according
    to the atom value.  Provenance is mandatory for every semantic diagnostic.
    """

    atom: str
    value: AtomValue
    support: tuple[str, ...] = ()
    counterwitness: tuple[str, ...] = ()
    obstacles: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    safety: bool = False

    def __post_init__(self) -> None:
        if not self.atom:
            raise ValueError("diagnostic atom must be named")
        if not self.provenance:
            raise ValueError(f"diagnostic {self.atom!r} lacks provenance")
        if self.value is AtomValue.SUPPORTED and not self.support:
            raise ValueError(f"supported atom {self.atom!r} lacks a witness")
        if self.value is AtomValue.REFUTED and not self.counterwitness:
            raise ValueError(f"refuted atom {self.atom!r} lacks a counterwitness")
        if self.value is AtomValue.OPEN and not self.obstacles:
            raise ValueError(f"open atom {self.atom!r} lacks an obstacle")


@dataclass(frozen=True)
class WFError:
    obligation: str
    detail: str
    provenance: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.obligation or not self.detail or not self.provenance:
            raise ValueError("well-formedness errors require obligation, detail, and provenance")


@dataclass(frozen=True)
class Profile:
    name: str
    required: tuple[str, ...]
    report_only: tuple[str, ...] = ()
    safety_atoms: frozenset[str] = frozenset()
    action_authorizing: bool = True

    def __post_init__(self) -> None:
        if not self.name or not self.required:
            raise ValueError("profiles require a name and at least one required atom")
        if len(set(self.required)) != len(self.required):
            raise ValueError(f"profile {self.name!r} repeats a required atom")
        if set(self.required) & set(self.report_only):
            raise ValueError(f"profile {self.name!r} requires and reports the same atom")
        if not self.safety_atoms.issubset(self.required):
            raise ValueError("safety atoms must be required atoms")


@dataclass(frozen=True)
class UsePlan:
    name: str
    executable_cases: frozenset[str]
    deployment_cost: float
    memory: float
    robustness: Interval
    frame: str = "standard"


@dataclass(frozen=True)
class EvaluationContext:
    name: str
    cases: frozenset[str]
    tolerance: float
    fallback: str | None
    fallback_risk: Interval | None
    required_advantage: float
    frame: str = "standard"


@dataclass(frozen=True)
class Request:
    request_id: str
    plan: str
    context: str
    profile: str | None
    frame: str = "standard"


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    label: str


@dataclass(frozen=True)
class ProvenanceGraph:
    nodes: frozenset[str]
    edges: tuple[Edge, ...]

    def __post_init__(self) -> None:
        missing = {
            endpoint
            for edge in self.edges
            for endpoint in (edge.source, edge.target)
            if endpoint not in self.nodes
        }
        if missing:
            raise ValueError(f"provenance edges reference missing nodes: {sorted(missing)}")

    def successors(self, node: str) -> tuple[str, ...]:
        return tuple(edge.target for edge in self.edges if edge.source == node)

    def path_exists(self, source: str, target: str) -> bool:
        if source not in self.nodes or target not in self.nodes:
            return False
        frontier = [source]
        visited: set[str] = set()
        while frontier:
            node = frontier.pop()
            if node == target:
                return True
            if node in visited:
                continue
            visited.add(node)
            frontier.extend(next_node for next_node in self.successors(node) if next_node not in visited)
        return False

    def extends(self, earlier: "ProvenanceGraph") -> bool:
        return earlier.nodes.issubset(self.nodes) and set(earlier.edges).issubset(self.edges)


@dataclass(frozen=True)
class Assessment:
    outcome: Outcome
    required: Mapping[str, Diagnostic] = field(default_factory=dict)
    reports: Mapping[str, Diagnostic] = field(default_factory=dict)
    wf_error: WFError | None = None
    alarms: tuple[str, ...] = ()
    open_safety: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.outcome is Outcome.UNDEFINED and self.wf_error is None:
            raise ValueError("undefined assessment requires a well-formedness error")
        if self.outcome is not Outcome.UNDEFINED and self.wf_error is not None:
            raise ValueError("meaningful assessment cannot carry a well-formedness error")


@dataclass(frozen=True)
class EpistemicState:
    name: str
    plans: Mapping[str, UsePlan]
    contexts: Mapping[str, EvaluationContext]
    profiles: Mapping[str, Profile]
    requests: Mapping[str, Request]
    diagnostics: Mapping[str, Mapping[str, Diagnostic]]
    deployment_requests: Mapping[str, str]
    routes: Mapping[str, str]
    archive: frozenset[str]
    graph: ProvenanceGraph


def meet(values: Iterable[AtomValue]) -> AtomValue:
    values = tuple(values)
    if not values:
        raise ValueError("finite meet requires at least one value")
    return min(values)


def check_well_formed(state: EpistemicState, request: Request) -> WFError | None:
    if request.profile is None:
        return WFError(
            "profile_ref",
            "missing mandatory license profile",
            (f"wf:{request.request_id}:missing-profile",),
        )
    if request.profile not in state.profiles:
        return WFError(
            "profile_ref",
            f"unknown profile {request.profile!r}",
            (f"wf:{request.request_id}:unknown-profile",),
        )
    if request.plan not in state.plans:
        return WFError(
            "plan_ref",
            f"unknown use plan {request.plan!r}",
            (f"wf:{request.request_id}:unknown-plan",),
        )
    if request.context not in state.contexts:
        return WFError(
            "context_ref",
            f"unknown evaluation context {request.context!r}",
            (f"wf:{request.request_id}:unknown-context",),
        )

    plan = state.plans[request.plan]
    context = state.contexts[request.context]
    profile = state.profiles[request.profile]
    if request.frame != context.frame or request.frame != plan.frame:
        return WFError(
            "frame_interface",
            f"request frame {request.frame!r} does not match plan/context frame",
            (f"wf:{request.request_id}:frame-mismatch",),
        )
    missing_cases = context.cases - plan.executable_cases
    if missing_cases:
        return WFError(
            "executable_interface",
            f"plan {plan.name!r} is not executable on {sorted(missing_cases)}",
            (f"wf:{request.request_id}:undefined-interface",),
        )
    if profile.action_authorizing and (context.fallback is None or context.fallback_risk is None):
        return WFError(
            "fallback_ref",
            "action-authorizing request lacks an explicit fallback",
            (f"wf:{request.request_id}:missing-fallback",),
        )
    return None


def assess_request(state: EpistemicState, request_id: str) -> Assessment:
    request = state.requests[request_id]
    wf_error = check_well_formed(state, request)
    if wf_error is not None:
        return Assessment(Outcome.UNDEFINED, wf_error=wf_error)

    assert request.profile is not None
    profile = state.profiles[request.profile]
    available = state.diagnostics.get(request_id, {})
    missing = [atom for atom in profile.required if atom not in available]
    if missing:
        raise KeyError(f"request {request_id!r} lacks required diagnostics {missing}")

    required = {atom: available[atom] for atom in profile.required}
    for atom, diagnostic in required.items():
        if diagnostic.atom != atom:
            raise ValueError(f"diagnostic key {atom!r} disagrees with atom {diagnostic.atom!r}")
    reports = {atom: available[atom] for atom in profile.report_only if atom in available}

    aggregate = meet(diagnostic.value for diagnostic in required.values())
    outcome = {
        AtomValue.SUPPORTED: Outcome.GRANTED,
        AtomValue.OPEN: Outcome.WITHHELD,
        AtomValue.REFUTED: Outcome.REFUSED,
    }[aggregate]
    alarms = tuple(
        atom
        for atom in profile.required
        if atom in profile.safety_atoms and required[atom].value is AtomValue.REFUTED
    )
    open_safety = tuple(
        atom
        for atom in profile.required
        if atom in profile.safety_atoms and required[atom].value is AtomValue.OPEN
    )
    return Assessment(
        outcome=outcome,
        required=required,
        reports=reports,
        alarms=alarms,
        open_safety=open_safety,
    )


def supported(atom: str, witness: str, provenance: Iterable[str], *, safety: bool = False) -> Diagnostic:
    return Diagnostic(
        atom=atom,
        value=AtomValue.SUPPORTED,
        support=(witness,),
        provenance=tuple(provenance),
        safety=safety,
    )


def refuted(atom: str, counterwitness: str, provenance: Iterable[str], *, safety: bool = False) -> Diagnostic:
    return Diagnostic(
        atom=atom,
        value=AtomValue.REFUTED,
        counterwitness=(counterwitness,),
        provenance=tuple(provenance),
        safety=safety,
    )


def open_atom(atom: str, obstacle: str, provenance: Iterable[str], *, safety: bool = False) -> Diagnostic:
    return Diagnostic(
        atom=atom,
        value=AtomValue.OPEN,
        obstacles=(obstacle,),
        provenance=tuple(provenance),
        safety=safety,
    )


def assess_upper_bound(
    atom: str,
    region: Interval | None,
    threshold: float,
    certificate: str,
    provenance: Iterable[str],
    *,
    safety: bool = False,
    missing_obstacle: str = "InsufficientEvidence",
) -> Diagnostic:
    if region is None:
        return open_atom(atom, missing_obstacle, provenance, safety=safety)
    if region.upper <= threshold:
        return supported(atom, certificate, provenance, safety=safety)
    if region.lower > threshold:
        return refuted(atom, certificate, provenance, safety=safety)
    return open_atom(atom, "CertificateStraddlesBoundary", provenance, safety=safety)


def assess_improvement(
    atom: str,
    candidate: Interval | None,
    fallback: Interval | None,
    required_advantage: float,
    certificate: str,
    provenance: Iterable[str],
) -> Diagnostic:
    if candidate is None or fallback is None:
        return open_atom(atom, "ComparisonEvidenceMissing", provenance)
    if candidate.upper + required_advantage <= fallback.lower:
        return supported(atom, certificate, provenance)
    if candidate.lower + required_advantage > fallback.upper:
        return refuted(atom, certificate, provenance)
    return open_atom(atom, "ComparisonStraddlesBoundary", provenance)


def assess_relative_undefeated(
    atom: str,
    evaluated_scope: str,
    provenance: Iterable[str],
    *,
    certified_dominators: Iterable[str] = (),
) -> Diagnostic:
    dominators = tuple(certified_dominators)
    if dominators:
        return refuted(atom, f"dominator:{dominators[0]}", provenance)
    return supported(atom, f"no-certified-dominator:{evaluated_scope}", provenance)


def assess_certified_undominated(
    atom: str,
    evaluated_scope: str,
    provenance: Iterable[str],
    *,
    certified_dominators: Iterable[str] = (),
    unknown_pairs: Iterable[str] = (),
) -> Diagnostic:
    dominators = tuple(certified_dominators)
    unknown = tuple(unknown_pairs)
    if dominators:
        return refuted(atom, f"dominator:{dominators[0]}", provenance)
    if unknown:
        return open_atom(atom, f"UnresolvedComparison:{','.join(unknown)}", provenance)
    return supported(atom, f"all-comparisons-resolved:{evaluated_scope}", provenance)


def render_legacy_label(item: Diagnostic | WFError) -> str:
    """Render historical labels without making them semantic constructors."""

    if isinstance(item, WFError):
        return {
            "profile_ref": "MissingLicenseProfile",
            "frame_interface": "FrameMismatch",
            "executable_interface": "UndefinedInterface",
            "fallback_ref": "MissingExplicitFallback",
        }.get(item.obligation, f"TypeError({item.obligation})")

    if item.value is AtomValue.REFUTED:
        return {
            "adequacy": "HardRiskViolation",
            "fallback_improvement": "FallbackNotBeaten",
            "hard_constraints": "HardConstraintViolation",
            "relative_undefeated": "CertifiedDominatorFound",
            "certified_undominated": "CertifiedDominatorFound",
        }.get(item.atom, f"Fail({item.atom})")
    if item.value is AtomValue.OPEN:
        return item.obstacles[0]
    return f"Supported({item.atom})"
