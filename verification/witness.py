"""Executable fixtures for the integrated Task 11A witness.

The concrete example lives here; :mod:`verification.kernel` remains generic.
Every public outcome is derived from well-formedness plus atom diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .kernel import (
    Assessment,
    AtomValue,
    Diagnostic,
    Edge,
    EpistemicState,
    EvaluationContext,
    Interval,
    Outcome,
    Profile,
    ProvenanceGraph,
    Request,
    UsePlan,
    assess_certified_undominated,
    assess_improvement,
    assess_relative_undefeated,
    assess_request,
    assess_upper_bound,
    open_atom,
    refuted,
    supported,
)


ADEQUACY = "adequacy"
IMPROVEMENT = "fallback_improvement"
CONSTRAINTS = "hard_constraints"
TRACE = "trace"
REL_UNDEFEATED = "relative_undefeated"
CERT_UNDOMINATED = "certified_undominated"
COMPARISON_REPORT = "comparison_report"
SPLIT_READY = "split_ready"

BASE_ATOMS = (ADEQUACY, IMPROVEMENT, CONSTRAINTS, TRACE)


@dataclass(frozen=True)
class BridgeRecord:
    bridge_id: str
    source: str
    target: str
    cases: frozenset[str]
    kind: str
    status: str
    tolerance: float | None
    provenance: tuple[str, ...]


@dataclass(frozen=True)
class IntegratedWitness:
    states: Mapping[str, EpistemicState]
    representative_losses: Mapping[tuple[str, str], float | None]
    risk_certificates: Mapping[tuple[str, str, str], Interval]
    robustness: Mapping[str, Interval]
    marginal_scores: Mapping[str, Interval]
    joint_scores: Mapping[str, Interval]
    bridges: tuple[BridgeRecord, ...]

    def assessment(self, stage: str, request_id: str) -> Assessment:
        return assess_request(self.states[stage], request_id)

    def active_set(self, stage: str, case: str) -> frozenset[str]:
        state = self.states[stage]
        active: set[str] = set()
        for plan_name, request_id in state.deployment_requests.items():
            request = state.requests[request_id]
            context = state.contexts[request.context]
            if case in context.cases and self.assessment(stage, request_id).outcome is Outcome.GRANTED:
                active.add(plan_name)
        return frozenset(active)

    def selected_plans(self, stage: str) -> frozenset[str]:
        state = self.states[stage]
        return frozenset(value for value in state.routes.values() if value in state.plans)

    def comparison_eligible(self, stage: str, plan: str, context: str) -> bool:
        state = self.states[stage]
        key = (stage, plan, context)
        if plan not in state.plans or context not in state.contexts or key not in self.risk_certificates:
            return False
        plan_record = state.plans[plan]
        context_record = state.contexts[context]
        if not context_record.cases.issubset(plan_record.executable_cases):
            return False
        if self.risk_certificates[key].upper > context_record.tolerance:
            return False
        return self.robustness[plan].upper <= 0.15

    def edge_eligible(self, plan: str, memory_limit: float = 2.0) -> bool:
        return self.states["t1"].plans[plan].memory <= memory_limit

    def provenance_complete(self, stage: str) -> bool:
        state = self.states[stage]
        stage_node = f"stage:{stage}"
        for request_id, request in state.requests.items():
            status_node = f"status:{request_id}"
            model_node = f"model:{request.plan}"
            if not state.graph.path_exists(model_node, status_node):
                return False
            if not state.graph.path_exists(status_node, stage_node):
                return False
            for diagnostic in state.diagnostics.get(request_id, {}).values():
                if any(node not in state.graph.nodes for node in diagnostic.provenance):
                    return False
        return True


class _GraphBuilder:
    def __init__(self, earlier: ProvenanceGraph | None = None) -> None:
        self.nodes = set(earlier.nodes if earlier else ())
        self.edges = set(earlier.edges if earlier else ())

    def add_chain(self, nodes: Iterable[str], label: str = "derived_from") -> None:
        chain = tuple(nodes)
        self.nodes.update(chain)
        for source, target in zip(chain, chain[1:]):
            self.edges.add(Edge(source, target, label))

    def freeze(self) -> ProvenanceGraph:
        return ProvenanceGraph(
            nodes=frozenset(self.nodes),
            edges=tuple(sorted(self.edges, key=lambda edge: (edge.source, edge.target, edge.label))),
        )


def _profiles() -> dict[str, Profile]:
    reports = (COMPARISON_REPORT,)
    return {
        "P_rely": Profile(
            "P_rely",
            BASE_ATOMS,
            report_only=reports,
            safety_atoms=frozenset({CONSTRAINTS}),
        ),
        "P_pref_rel": Profile(
            "P_pref_rel",
            BASE_ATOMS + (REL_UNDEFEATED,),
            report_only=reports,
            safety_atoms=frozenset({CONSTRAINTS}),
        ),
        "P_pref_cert": Profile(
            "P_pref_cert",
            BASE_ATOMS + (CERT_UNDOMINATED,),
            report_only=reports,
            safety_atoms=frozenset({CONSTRAINTS}),
        ),
        "P_split": Profile("P_split", (SPLIT_READY,), action_authorizing=False),
    }


def _contexts() -> dict[str, EvaluationContext]:
    fallback = Interval(0.30, 0.30)
    common = dict(tolerance=0.20, fallback="Defer", fallback_risk=fallback, required_advantage=0.02)
    return {
        "D_O": EvaluationContext("D_O", frozenset("abc"), **common),
        "D_cloud": EvaluationContext("D_cloud", frozenset("bcd"), **common),
        "D_Q": EvaluationContext("D_Q", frozenset("ab"), **common),
        "D_expanded": EvaluationContext("D_expanded", frozenset("bcde"), **common),
        "D_overlap": EvaluationContext("D_overlap", frozenset("bc"), **common),
        "D_edge": EvaluationContext("D_edge", frozenset("a"), **common),
    }


def _all_plans() -> dict[str, UsePlan]:
    return {
        "O": UsePlan("O", frozenset("abc"), 1.0, 1.0, Interval(0.04, 0.06)),
        # S is executable on e, but no t0 certificate covers e.
        "S": UsePlan("S", frozenset("bcde"), 3.0, 3.0, Interval(0.02, 0.04)),
        "Q": UsePlan("Q", frozenset("ab"), 0.5, 1.0, Interval(0.21, 0.24)),
        "N": UsePlan("N", frozenset("bcd"), 2.0, 4.0, Interval(0.05, 0.08)),
    }


def _request(request_id: str, plan: str, context: str, profile: str | None, frame: str = "standard") -> Request:
    return Request(request_id, plan, context, profile, frame)


def _hard_constraint(plan: UsePlan, certificate: str) -> Diagnostic:
    return assess_upper_bound(
        CONSTRAINTS,
        plan.robustness,
        0.15,
        certificate,
        (certificate,),
        safety=True,
    )


def _core_diagnostics(
    plan: UsePlan,
    context: EvaluationContext,
    risk: Interval | None,
    certificate: str,
    *,
    adequacy_obstacle: str = "InsufficientEvidence",
    improvement_obstacle: str | None = None,
) -> dict[str, Diagnostic]:
    adequacy = assess_upper_bound(
        ADEQUACY,
        risk,
        context.tolerance,
        certificate,
        (certificate,),
        missing_obstacle=adequacy_obstacle,
    )
    if improvement_obstacle is None:
        improvement = assess_improvement(
            IMPROVEMENT,
            risk,
            context.fallback_risk,
            context.required_advantage,
            f"{certificate}:fallback",
            (certificate, "fallback:F"),
        )
    else:
        improvement = open_atom(
            IMPROVEMENT,
            improvement_obstacle,
            (certificate, "fallback:F"),
        )
    return {
        ADEQUACY: adequacy,
        IMPROVEMENT: improvement,
        CONSTRAINTS: _hard_constraint(plan, f"k_resource_{plan.name}"),
        TRACE: supported(TRACE, f"trace:{plan.name}:{context.name}", (f"p_{plan.name}_{context.name}",)),
    }


def _with_comparison(
    core: Mapping[str, Diagnostic],
    diagnostic: Diagnostic,
    report: Diagnostic | None = None,
) -> dict[str, Diagnostic]:
    result = dict(core)
    result[diagnostic.atom] = diagnostic
    if report is not None:
        result[COMPARISON_REPORT] = report
    return result


def _build_graph(
    stage: str,
    requests: Mapping[str, Request],
    diagnostics: Mapping[str, Mapping[str, Diagnostic]],
    *,
    earlier: ProvenanceGraph | None = None,
    wf_nodes: Mapping[str, str] | None = None,
    extra_chains: Iterable[Iterable[str]] = (),
) -> ProvenanceGraph:
    builder = _GraphBuilder(earlier)
    route_node = f"route:{stage}"
    stage_node = f"stage:{stage}"
    wf_nodes = wf_nodes or {}
    for request_id, request in requests.items():
        model_node = f"model:{request.plan}"
        context_node = f"context:{request.context}"
        status_node = f"status:{request_id}"
        if request_id in diagnostics:
            for atom, diagnostic in diagnostics[request_id].items():
                builder.add_chain(
                    (
                        model_node,
                        context_node,
                        *diagnostic.provenance,
                        f"atom:{request_id}:{atom}",
                        f"request:{request_id}",
                        status_node,
                        route_node,
                        stage_node,
                    )
                )
        else:
            builder.add_chain(
                (
                    model_node,
                    context_node,
                    wf_nodes[request_id],
                    f"request:{request_id}",
                    status_node,
                    route_node,
                    stage_node,
                )
            )
    for chain in extra_chains:
        builder.add_chain(chain)
    return builder.freeze()


def _make_t0(
    plans: Mapping[str, UsePlan],
    contexts: Mapping[str, EvaluationContext],
    profiles: Mapping[str, Profile],
    risks: Mapping[tuple[str, str, str], Interval],
) -> EpistemicState:
    requests = {
        "r_t0_O_rely": _request("r_t0_O_rely", "O", "D_O", "P_rely"),
        "r_t0_S_rely": _request("r_t0_S_rely", "S", "D_cloud", "P_rely"),
        "r_t0_Q_rely": _request("r_t0_Q_rely", "Q", "D_Q", "P_rely"),
        "r_t0_S_expanded": _request("r_t0_S_expanded", "S", "D_expanded", "P_rely"),
        "r_t0_O_wrong_frame": _request("r_t0_O_wrong_frame", "O", "D_O", "P_rely", "wrong"),
        "r_t0_O_bare": _request("r_t0_O_bare", "O", "D_O", None),
        "r_t0_O_pref_overlap": _request("r_t0_O_pref_overlap", "O", "D_overlap", "P_pref_rel"),
        "r_t0_S_pref_overlap": _request("r_t0_S_pref_overlap", "S", "D_overlap", "P_pref_rel"),
    }
    diagnostics: dict[str, dict[str, Diagnostic]] = {
        "r_t0_O_rely": _core_diagnostics(plans["O"], contexts["D_O"], risks[("t0", "O", "D_O")], "k_O^0"),
        "r_t0_S_rely": _core_diagnostics(
            plans["S"], contexts["D_cloud"], risks[("t0", "S", "D_cloud")], "k_S^0"
        ),
        "r_t0_Q_rely": _core_diagnostics(plans["Q"], contexts["D_Q"], risks[("t0", "Q", "D_Q")], "k_Q^0"),
        "r_t0_S_expanded": _core_diagnostics(
            plans["S"],
            contexts["D_expanded"],
            None,
            "scope_gap_e^0",
            adequacy_obstacle="NoScopeEvidence:e",
            improvement_obstacle="NoScopeEvidence:e",
        ),
    }
    o_overlap = _core_diagnostics(
        plans["O"], contexts["D_overlap"], risks[("t0", "O", "D_overlap")], "k_O_overlap^0"
    )
    s_overlap = _core_diagnostics(
        plans["S"], contexts["D_overlap"], risks[("t0", "S", "D_overlap")], "k_S_overlap^0"
    )
    diagnostics["r_t0_O_pref_overlap"] = _with_comparison(
        o_overlap,
        assess_relative_undefeated(
            REL_UNDEFEATED,
            "E_sigma0:D_overlap",
            ("k_SO_overlap^0", "sigma_0"),
            certified_dominators=("S",),
        ),
    )
    diagnostics["r_t0_S_pref_overlap"] = _with_comparison(
        s_overlap,
        assess_relative_undefeated(
            REL_UNDEFEATED,
            "E_sigma0:D_overlap",
            ("k_SO_overlap^0", "sigma_0"),
        ),
    )
    wf_nodes = {
        "r_t0_O_wrong_frame": "wf:r_t0_O_wrong_frame:frame-mismatch",
        "r_t0_O_bare": "wf:r_t0_O_bare:missing-profile",
    }
    graph = _build_graph("t0", requests, diagnostics, wf_nodes=wf_nodes)
    return EpistemicState(
        name="t0",
        plans={name: plans[name] for name in ("O", "S", "Q")},
        contexts=contexts,
        profiles=profiles,
        requests=requests,
        diagnostics=diagnostics,
        deployment_requests={"O": "r_t0_O_rely", "S": "r_t0_S_rely", "Q": "r_t0_Q_rely"},
        routes={"a": "O", "b": "S", "c": "S", "d": "S", "e": "Defer"},
        archive=frozenset({"O", "S", "Q"}),
        graph=graph,
    )


def _make_t1(
    plans: Mapping[str, UsePlan],
    contexts: Mapping[str, EvaluationContext],
    profiles: Mapping[str, Profile],
    risks: Mapping[tuple[str, str, str], Interval],
    t0: EpistemicState,
) -> EpistemicState:
    requests = {
        "r_t1_O_rely": _request("r_t1_O_rely", "O", "D_O", "P_rely"),
        "r_t1_S_rely": _request("r_t1_S_rely", "S", "D_cloud", "P_rely"),
        "r_t1_Q_rely": _request("r_t1_Q_rely", "Q", "D_Q", "P_rely"),
        "r_t1_N_rely": _request("r_t1_N_rely", "N", "D_cloud", "P_rely"),
        "r_t1_O_pref_overlap": _request("r_t1_O_pref_overlap", "O", "D_overlap", "P_pref_rel"),
        "r_t1_N_pref_overlap": _request("r_t1_N_pref_overlap", "N", "D_overlap", "P_pref_rel"),
        "r_t1_O_pref_edge": _request("r_t1_O_pref_edge", "O", "D_edge", "P_pref_rel"),
        "r_t1_S_pref_cloud": _request("r_t1_S_pref_cloud", "S", "D_cloud", "P_pref_rel"),
        "r_t1_N_pref_cloud": _request("r_t1_N_pref_cloud", "N", "D_cloud", "P_pref_rel"),
        "r_t1_S_rel_local": _request("r_t1_S_rel_local", "S", "D_cloud", "P_pref_rel"),
        "r_t1_N_rel_local": _request("r_t1_N_rel_local", "N", "D_cloud", "P_pref_rel"),
        "r_t1_S_cert_local": _request("r_t1_S_cert_local", "S", "D_cloud", "P_pref_cert"),
        "r_t1_N_cert_local": _request("r_t1_N_cert_local", "N", "D_cloud", "P_pref_cert"),
        "r_t1_O_split": _request("r_t1_O_split", "O", "D_O", "P_split"),
        "r_t1_S_split": _request("r_t1_S_split", "S", "D_cloud", "P_split"),
    }
    diagnostics: dict[str, dict[str, Diagnostic]] = {
        "r_t1_O_rely": _core_diagnostics(plans["O"], contexts["D_O"], risks[("t1", "O", "D_O")], "k_O^0"),
        "r_t1_S_rely": _core_diagnostics(
            plans["S"], contexts["D_cloud"], risks[("t1", "S", "D_cloud")], "k_S^0"
        ),
        "r_t1_Q_rely": _core_diagnostics(plans["Q"], contexts["D_Q"], risks[("t1", "Q", "D_Q")], "k_Q^0"),
        "r_t1_N_rely": _core_diagnostics(
            plans["N"], contexts["D_cloud"], risks[("t1", "N", "D_cloud")], "k_N^1"
        ),
    }

    def comparative(
        request_id: str,
        plan: str,
        context: str,
        certificate: str,
        *,
        dominators: tuple[str, ...] = (),
        unknown: tuple[str, ...] = (),
        certified: bool = False,
    ) -> None:
        core = _core_diagnostics(plans[plan], contexts[context], risks[("t1", plan, context)], certificate)
        report = None
        if unknown:
            report = open_atom(COMPARISON_REPORT, f"UnknownPair:{','.join(unknown)}", ("sigma_1",))
        if certified:
            comparison = assess_certified_undominated(
                CERT_UNDOMINATED,
                f"E_sigma1:{context}",
                ("sigma_1", certificate),
                certified_dominators=dominators,
                unknown_pairs=unknown,
            )
        else:
            comparison = assess_relative_undefeated(
                REL_UNDEFEATED,
                f"E_sigma1:{context}",
                ("sigma_1", certificate),
                certified_dominators=dominators,
            )
        diagnostics[request_id] = _with_comparison(core, comparison, report)

    comparative("r_t1_O_pref_overlap", "O", "D_overlap", "k_O_overlap^0", dominators=("N",))
    comparative("r_t1_N_pref_overlap", "N", "D_overlap", "k_N_overlap^1")
    comparative("r_t1_O_pref_edge", "O", "D_edge", "k_O_edge^1")
    comparative("r_t1_S_pref_cloud", "S", "D_cloud", "k_S^0", dominators=("N",))
    comparative("r_t1_N_pref_cloud", "N", "D_cloud", "k_N^1")
    comparative("r_t1_S_rel_local", "S", "D_cloud", "k_S^0", unknown=("S:N:local",))
    comparative("r_t1_N_rel_local", "N", "D_cloud", "k_N^1", unknown=("S:N:local",))
    comparative(
        "r_t1_S_cert_local", "S", "D_cloud", "k_S^0", unknown=("S:N:local",), certified=True
    )
    comparative(
        "r_t1_N_cert_local", "N", "D_cloud", "k_N^1", unknown=("S:N:local",), certified=True
    )
    diagnostics["r_t1_O_split"] = {
        SPLIT_READY: supported(SPLIT_READY, "certified-partition:edge+overlap", ("cert_split^1",))
    }
    diagnostics["r_t1_S_split"] = {
        SPLIT_READY: open_atom(SPLIT_READY, "LocalSplitUncertified", ("postselected_split_S^1",))
    }

    bridge_chains = (
        ("model:O", "beta_OS", "model:S"),
        ("model:O", "beta_ON", "model:N"),
        ("model:S", "beta_SN_decision", "model:N"),
        ("model:S", "beta_SN_tight", "model:N"),
        ("model:Q", "beta_QN", "model:N"),
    )
    graph = _build_graph("t1", requests, diagnostics, earlier=t0.graph, extra_chains=bridge_chains)
    return EpistemicState(
        name="t1",
        plans=dict(plans),
        contexts=contexts,
        profiles=profiles,
        requests=requests,
        diagnostics=diagnostics,
        deployment_requests={
            "O": "r_t1_O_rely",
            "S": "r_t1_S_rely",
            "Q": "r_t1_Q_rely",
            "N": "r_t1_N_rely",
        },
        routes={"a": "O", "b": "N", "c": "N", "d": "N", "e": "Defer"},
        archive=frozenset({"O", "S", "Q", "N"}),
        graph=graph,
    )


def _make_t2(
    plans: Mapping[str, UsePlan],
    contexts: Mapping[str, EvaluationContext],
    profiles: Mapping[str, Profile],
    risks: dict[tuple[str, str, str], Interval],
    t1: EpistemicState,
) -> EpistemicState:
    requests = {
        "r_t2_O_rely": _request("r_t2_O_rely", "O", "D_O", "P_rely"),
        "r_t2_S_rely": _request("r_t2_S_rely", "S", "D_cloud", "P_rely"),
        "r_t2_Q_rely": _request("r_t2_Q_rely", "Q", "D_Q", "P_rely"),
        "r_t2_N_rely": _request("r_t2_N_rely", "N", "D_cloud", "P_rely"),
    }
    o_lapsed = _core_diagnostics(
        plans["O"],
        contexts["D_O"],
        None,
        "d_O_leak^2",
        adequacy_obstacle="BrokenAssumption",
        improvement_obstacle="BrokenAssumption",
    )
    s_bad = Interval(0.24, 0.27)
    risks[("t2", "S", "D_cloud")] = s_bad
    diagnostics = {
        "r_t2_O_rely": o_lapsed,
        "r_t2_S_rely": _core_diagnostics(plans["S"], contexts["D_cloud"], s_bad, "k_S_bad^2"),
        "r_t2_Q_rely": _core_diagnostics(plans["Q"], contexts["D_Q"], risks[("t2", "Q", "D_Q")], "k_Q^0"),
        "r_t2_N_rely": _core_diagnostics(
            plans["N"], contexts["D_cloud"], risks[("t2", "N", "D_cloud")], "k_N^1"
        ),
    }
    extra = (
        (
            "d_O_leak^2",
            "k_O^0",
            "atom:r_t2_O_rely:adequacy",
            "request:r_t2_O_rely",
            "status:r_t2_O_rely",
            "route:t2",
        ),
        (
            "d_S_rebut^2",
            "k_S_bad^2",
            "atom:r_t2_S_rely:adequacy",
            "request:r_t2_S_rely",
            "status:r_t2_S_rely",
            "route:t2",
        ),
    )
    graph = _build_graph("t2", requests, diagnostics, earlier=t1.graph, extra_chains=extra)
    return EpistemicState(
        name="t2",
        plans=dict(plans),
        contexts=contexts,
        profiles=profiles,
        requests=requests,
        diagnostics=diagnostics,
        deployment_requests={
            "O": "r_t2_O_rely",
            "S": "r_t2_S_rely",
            "Q": "r_t2_Q_rely",
            "N": "r_t2_N_rely",
        },
        routes={"a": "Defer", "b": "N", "c": "N", "d": "N", "e": "Defer"},
        archive=frozenset({"O", "S", "Q", "N"}),
        graph=graph,
    )


def build_witness() -> IntegratedWitness:
    plans = _all_plans()
    contexts = _contexts()
    profiles = _profiles()
    risks: dict[tuple[str, str, str], Interval] = {
        ("t0", "O", "D_O"): Interval(0.09, 0.11),
        ("t0", "S", "D_cloud"): Interval(0.035, 0.055),
        ("t0", "Q", "D_Q"): Interval(0.08, 0.12),
        ("t0", "O", "D_overlap"): Interval(0.11, 0.13),
        ("t0", "S", "D_overlap"): Interval(0.040, 0.050),
        ("t1", "O", "D_O"): Interval(0.09, 0.11),
        ("t1", "S", "D_cloud"): Interval(0.035, 0.055),
        ("t1", "Q", "D_Q"): Interval(0.08, 0.12),
        ("t1", "N", "D_cloud"): Interval(0.035, 0.050),
        ("t1", "O", "D_overlap"): Interval(0.11, 0.13),
        ("t1", "N", "D_overlap"): Interval(0.035, 0.045),
        ("t1", "O", "D_edge"): Interval(0.05, 0.07),
        ("t2", "Q", "D_Q"): Interval(0.08, 0.12),
        ("t2", "N", "D_cloud"): Interval(0.035, 0.050),
    }
    t0 = _make_t0(plans, contexts, profiles, risks)
    t1 = _make_t1(plans, contexts, profiles, risks, t0)
    t2 = _make_t2(plans, contexts, profiles, risks, t1)

    representative_losses = {
        ("O", "a"): 0.06,
        ("O", "b"): 0.10,
        ("O", "c"): 0.14,
        ("O", "d"): None,
        ("S", "a"): None,
        ("S", "b"): 0.04,
        ("S", "c"): 0.05,
        ("S", "d"): 0.03,
        ("Q", "a"): 0.08,
        ("Q", "b"): 0.11,
        ("Q", "c"): None,
        ("Q", "d"): None,
        ("N", "a"): None,
        ("N", "b"): 0.03,
        ("N", "c"): 0.04,
        ("N", "d"): 0.05,
    }

    marginal_scores = {
        "N": risks[("t1", "N", "D_cloud")].shift(0.005 * plans["N"].deployment_cost),
        "S": risks[("t1", "S", "D_cloud")].shift(0.005 * plans["S"].deployment_cost),
    }
    joint_scores = {"N": Interval(0.048, 0.050), "S": Interval(0.054, 0.056)}
    bridges = (
        BridgeRecord("beta_OS", "O", "S", frozenset("b"), "observable", "exact", 0.0, ("beta_OS",)),
        BridgeRecord(
            "beta_ON", "O", "N", frozenset("bc"), "predictive", "approximate", 0.03, ("beta_ON",)
        ),
        BridgeRecord(
            "beta_SN_decision",
            "S",
            "N",
            frozenset("bc"),
            "decision",
            "decision-compatible",
            None,
            ("beta_SN_decision",),
        ),
        BridgeRecord(
            "beta_SN_tight",
            "S",
            "N",
            frozenset("bc"),
            "predictive",
            "incompatible",
            0.005,
            ("beta_SN_tight",),
        ),
        BridgeRecord("beta_QN", "Q", "N", frozenset("b"), "translation", "unknown", None, ("beta_QN",)),
    )
    return IntegratedWitness(
        states={"t0": t0, "t1": t1, "t2": t2},
        representative_losses=representative_losses,
        risk_certificates=risks,
        robustness={name: plan.robustness for name, plan in plans.items()},
        marginal_scores=marginal_scores,
        joint_scores=joint_scores,
        bridges=bridges,
    )


WITNESS = build_witness()
