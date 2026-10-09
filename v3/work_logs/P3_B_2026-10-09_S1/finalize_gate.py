"""Bind the closed P3-B gate and update only its current repository controls.

ChatGPT (GPT-6 Astra Pro), 2026-10-09. Administrative work; no research credit.
Run after close_accounting.py. Refuse unexpected control changes. This does
not publish, run scientific modules, select recurrence, or start P3-08.
"""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
REL = "v3/work_logs/P3_B_2026-10-09_S1"
BASE = "c7e2967d18475bda54a327864601c245c8a29062"


def binding(path):
    data = (REPO / path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def encoded(value):
    return (json.dumps(value, indent=2) + "\n").encode()


def base_bytes(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=REPO)


def replace_once(text, before, after):
    assert text.count(before) == 1, ("Unexpected control text", before)
    return text.replace(before, after, 1)


def main():
    actuals = json.loads((HERE / "actuals.json").read_text())
    decision = json.loads((HERE / "decision.json").read_text())
    options = json.loads((HERE / "recurrence_options.json").read_text())
    assert decision["verdict"] == "PASS"
    assert binding("v3/checkpoints/B_1.md") == decision["final_gate"]
    assert actuals["clock_stopped"] and actuals["gate_research_floor_minutes"] == 0
    assert options["selected"] is None
    resolution = json.loads((HERE / "reviews/semantics_agent/resolution.json").read_text())
    assert "f4441edea890377efb958a72bb5089c57ecbbe419ff63d8375e1d59a7c510652" in json.dumps(resolution)
    rmin = actuals["research_minutes"]
    phase = actuals["phase_research_minutes"]
    remaining = actuals["phase_remaining_floor_minutes"]

    # The historical P3-01 table is preserved. This is a current scoped overlay.
    duty_rows = [
        ("U01", "implemented_restricted", "P3-03/P3-07", "Bounded local computation and declared admitted observations; no global CPU/heap or malicious-code guarantee."),
        ("U02", "implemented_restricted", "P3-03/P3-06/P3-07", "Checked, unresolved, failed, conflicted and stale channels remain distinct under the relevant trusted checker and version contract."),
        ("U03", "conditional_finite_semantics", "P3-02/P3-03", "Conservative coverage of received finite constraints and optional coherent expectation adapters; scalar forecasts are not a joint Boolean law or unprocessed arithmetic closure."),
        ("U04", "implemented_restricted", "P3-03/P3-06/P3-07", "Eligible checked receipt updates or stale status under the soundness/execution bridge; historical issued forecasts stay immutable."),
        ("U05", "proved_fixed_query_under_premises", "P3-03", "Eventual fixed-query resolution needs the declared stream, soundness, scheduling, capacity and retained progress; no unrestricted learner convergence theorem."),
        ("U06", "finite_pre_resolution_evidence_broader_open", "P3-06/P3-07", "Issued finite-family forecasts exist; economical anticipation and discovery on fresh mathematics are not established and cheap exact shortcuts remain controls."),
        ("U07", "proved_selected_finite_feature_scope", "P3-06", "Potential-based finite/continuous-test bounds retain issue weights, numerical allowances and settled-feedback assumptions; no full LI or selected-only all-issued calibration import."),
        ("U08", "proved_fixed_expert_full_feedback_scope", "P3-06", "Actual-scalar expert-relative score bound and ordinary aggregator comparisons; not unrestricted efficient-trader non-exploitation or adaptive-policy regret."),
        ("U09", "qualified_delays_selective_feedback_open", "P3-06/P3-07", "Settled-prefix/copy guarantees retain their feedback conditions; purchased-only feedback has no current all-issued implementation guarantee."),
        ("V01", "explicit_typed_interfaces", "P3-02/P3-06/P3-07", "Semantic payoff, coherent expectation, fallible estimate, certified bound, acquired mean and realized score have separate meanings and evidence."),
        ("V02", "proved_stated_finite_information_services", "P3-02", "Known calibration/source/loss assumptions characterize laws, targets, bounds and decisions recoverable from the retained record; arbitrary costs need not identify probabilities."),
        ("V03", "proved_conditional_action_bridges", "P3-03/P3-06/P3-07", "Uniform action bounds, selected forecast/action bridges and finite paired-policy envelopes retain their particular comparators; expected value is not a pathwise guarantee."),
        ("V04", "implemented_local_paid_services", "P3-07", "Named complete policies, acquired profiles, assessment, cleanup and setup costs are charged under local tariffs; a common integrated resource account remains P3-08 work."),
        ("M01", "scoped_plurality_comparison_benefit_open", "P3-03/P3-05/P3-07", "Multiple scoped proofs/models/policies may be retained; usefulness beyond the strongest ordinary combination remains undemonstrated."),
        ("R01", "proved_and_implemented_finite_transport", "P3-03/P3-05/P3-06/P3-07", "Withdrawal and scope/objective changes require current applicability or proved domain/loss/error transport; changed policy trajectories require new coverage or justified replay."),
        ("C01", "finite_operations_distinguished", "P3-04/P3-05", "Conditioning, occurrence intervention, shared/actor replacement, ranked repair and genuine counterpossible evaluation retain distinct supplied interpretations."),
        ("C02", "proved_identification_limits", "P3-04/P3-05", "Observed information alone need not identify hypothetical consequences; dependence, frame and repair policies are supplied rather than uniquely learned."),
        ("C03", "proved_and_implemented_all_optimum_scope", "P3-04/P3-05", "Feasibility, optimality, complete tied consequences and policy choice are separate; unresolved sources remain outside repair minimization."),
        ("C04", "finite_counterpossible_adapter", "P3-04/P3-05", "The original quoted contradiction remains fixed while paired-support exception rules are declared; ordinary overlap is conditional and philosophical relevance is not uniquely identified."),
        ("I01", "proved_selected_operational_transports", "P3-02/P3-04/P3-05/P3-06/P3-07", "Selected information, domain, unit and fixed-feature transformations have explicit evidence; numeral recoding alone supplies no operational equivalence."),
        ("F01", "bounded_versioned_procedure_audit", "P3-07", "Fixed-profile and rebuilding-procedure expected-performance audits under named episode laws; not self-proof, report-dependent reflection or unpriced self-assessment."),
    ]
    assert len(duty_rows) == len({r[0] for r in duty_rows}) == 21
    reviews = sorted(p for p in (HERE / "reviews").rglob("*") if p.is_file() and p.suffix in (".md", ".json"))
    contract = {
        "schema": "value_logic.P3-B.readiness.v1", "gate": "P3-B", "attempt": "P3-B-1",
        "session": "2026-10-09-S1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "created_utc": actuals["recorded_end_utc"], "verdict": "PASS",
        "scope": decision["scope"], "source_commit": BASE, "source_tree": decision["source_tree"],
        "final_gate": decision["final_gate"], "decision": binding(REL + "/decision.json"),
        "actuals": binding(REL + "/actuals.json"),
        "review_kind": decision["review_kind"],
        "reviews": [binding(str(p.relative_to(REPO))) for p in reviews],
        "principal_reconstruction": binding(REL + "/principal_bridge_audit.md"),
        "principal_source_manifest": binding(REL + "/principal_source_manifest.json"),
        "primary_scope_review": binding(REL + "/source_scope_review.md"),
        "criteria": [{"id": f"B-C{i:02}", "criterion": name, "verdict": "PASS" if i < 7 else "SATISFIED"}
                     for i, name in enumerate(("Coherent restricted semantics", "Checkable independently reconstructed central arguments",
                        "Explicit uncertainty and counterfactual boundaries", "Nonvacuous examples and strong ordinary comparison",
                        "Implementable predictions", "No unresolved error in accepted downstream premises",
                        "Five-question judgment and optional recurrence advice"), 1)],
        "accepted_representation": {"id": "P3-A-REP01", "name": "Versioned finite rational constraints and loss queries",
            "revisable": True, "universal_carrier_selected": False, "new_contract_id": "P3-B-COMPOSE01",
            "kind": "conditional_composable_services", "end_to_end_reasoner_implemented": False,
            "default_probability_over_source_cases_or_repair_ties": None,
            "required_bridges": ["received-premise intended-answer soundness", "outer-source/inner-repair selection and branch feasibility",
                "all-current-optimum domain and fixed-comparison loss transport", "immutable forecast and admitted feedback chronology",
                "justified request/episode law and complete-policy state contract", "paid initial-root resource account and funded fallback"]},
        "duty_overlay_scope": "Current restricted disposition after P3-B. The historical P3-01 duty contract is unchanged; PASS does not mean all broad duties are solved.",
        "duties": [{"id": id, "status": status, "sources": owner, "scope": scope} for id, status, owner, scope in duty_rows],
        "questions": [
            {"id": "Q1", "status": "bounded checked refinement and finite forecasts; economical fresh mathematical anticipation open"},
            {"id": "Q2", "status": "coherent finite hypothetical/transport semantics; dependence and relevance policies supplied"},
            {"id": "Q3", "status": "plurality retention/coverage coherent; comparative useful delta not demonstrated"},
            {"id": "Q4", "status": "conditional forecast and paid-policy results; economical selective-feedback learning bridge open"},
            {"id": "Q5", "status": "mature finite information characterization under explicit loss/calibration/source premises"}],
        "comparison": {"primary": "O-COMB", "same_code_and_representations_allowed": True,
            "same_initial_information_access_and_budgets_for_policy_comparisons": True,
            "identical_evidence_for_fixed_transcript_comparisons": True,
            "different_paid_histories_allowed_for_policy_comparisons": True,
            "ordinary_exact_cache_analytic_and_label_efficient_controls_admitted": True,
            "universal_superiority_required_for_modest_contribution": False},
        "implementable_predictions": ["B-P01", "B-P02", "B-P03", "B-P04", "B-P05", "B-P06"],
        "prediction_definitions": "v3/checkpoints/B_1.md#5-implementable-predictions-for-the-next-cycle",
        "blocking_repairs": [], "contribution_obligation": "P3-N01", "contribution_status": "NOT YET SUPPORTED",
        "recurrence_advice": binding(REL + "/recurrence_options.json"),
        "optional_recurrence_recommended": "P3-B-OPTION-A", "optional_recurrence_selected": None,
        "named_contribution_recurrence_selected": False, "next_task": "P3-08", "next_task_started": False,
        "gate_research_floor_minutes": 0, "research_ns": actuals["research_ns"],
        "phase_research_ns": actuals["phase_research_ns"], "parallel_reviewer_credit_ns": 0,
        "experimental_freeze_created": False, "final_evaluation_exposed": False,
    }

    plan_path = REPO / "v3/plan.v1.json"
    plan = json.loads(plan_path.read_text())
    assert plan["gates"]["P3-B"]["status"] in ("in_progress", "passed")
    original_plan = json.loads(base_bytes("v3/plan.v1.json"))
    assert plan["chunks"] == original_plan["chunks"]
    for name in ("P3-A", "P3-C", "P3-D"):
        assert plan["gates"][name] == original_plan["gates"][name]
    plan["gates"]["P3-B"].update(status="passed", verdict="PASS", record="v3/checkpoints/B_1.md",
        contract="v3/checkpoints/B_1.v1.json", actuals=REL+"/actuals.json", session=REL+".md",
        research_ns=actuals["research_ns"], scope=decision["scope"], decision_utc=decision["decision_utc"])
    plan.update(next_task="P3-08", active_session=None, last_completed_session=REL+".md", last_preserved_session=REL+".md")
    plan["observed_progress"] = {"research_ns": actuals["phase_research_ns"],
        "measured_engaged_ns": actuals["phase_measured_engaged_ns"], "remaining_floor_ns": actuals["phase_remaining_floor_ns"],
        "source": REL+"/actuals.json", "next_checkpoint_minutes": 960,
        "evidence_disposition": "P3-B restricted mathematics/local implementation PASS; P3-01–07 and defensive-forecasting evidence preserved; no historical or parallel credit; P3-N01 not yet supported; optional A advised but unselected; P3-08 unstarted."}
    plan["optional_recurrence_advice"] = {"record": REL+"/recurrence_options.json", "recommended": "P3-B-OPTION-A",
        "selected": None, "gate": "P3-B", "technical_blocker": False, "timing": "before P3-08; if deferred decide before P3-09 feedback freeze"}

    todo = base_bytes("TODO_v3.md").decode()
    todo = replace_once(todo, "Phase-three qualifying research is **652.160106918517 minutes**;\n**307.839893081483 minutes** remain", f"Phase-three qualifying research is **{phase} minutes**;\n**{remaining} minutes** remain")
    todo = replace_once(todo, "**Next: P3-B — mathematical and implementation contract, unattempted.**\nThis task boundary does not start P3-B or P3-08.\nPhase two remains complete; P3-B–D remain unattempted.",
        f"**P3-B is PASS at restricted mathematics and local implementation readiness**,\nwith **{rmin} measured research minutes** and no added gate floor.\n[Gate assessment](v3/checkpoints/B_1.md) and [bound contract](v3/checkpoints/B_1.v1.json)\nrecord the independently reconstructed bridges, remaining integration duty and\nfive-question judgment. **Next: P3-08, unstarted.** The recommended optional\n[paid-selective-feedback recurrence](v3/work_logs/P3_B_2026-10-09_S1/recurrence_options.json)\nis unselected; the author may choose it before P3-08. Neither begins here.\nPhase two remains complete; P3-C–D remain unattempted.")
    todo = replace_once(todo, "- [ ] **P3-B — mathematical and implementation contract.**", "- [x] **P3-B — mathematical and implementation contract. PASS at restricted scope.**")
    todo = replace_once(todo, "  steps. Unresolved errors in downstream premises block the gate. No added floor.",
        "  steps. Unresolved errors in downstream premises block the gate. No added floor.\n  Completed: [B_1](v3/checkpoints/B_1.md), its [21-duty overlay](v3/checkpoints/B_1.v1.json),\n  and [exact session](v3/work_logs/P3_B_2026-10-09_S1.md). No blocking repair.\n  A combined reasoner remains P3-08 work. Optional recurrence A is recommended\n  now for paid selective feedback; B concerns equal certificate delivery before\n  freeze, and C concerns counterpossible-policy robustness later in the phase.\n  All three remain unselected, separate from R-P3-N01.")
    todo = replace_once(todo, "scopes. P3-A has passed at restricted-representation readiness scope.\nNext: P3-B, unattempted; P3-C–D remain unattempted and P3-08 is unstarted.**",
        "scopes. P3-A and P3-B have passed at their restricted readiness scopes.\nNext: P3-08, unstarted; P3-C–D remain unattempted. Optional recurrence A is\nrecommended before P3-08 but is unselected and is not a blocking repair.**")

    readme = base_bytes("v3/README.md").decode()
    readme = replace_once(readme, "No anticipatory learner,\npaid-computation policy or final experiment has been established.",
        "The P3-03 prototype itself supplies no anticipatory learner or\npaid-computation policy. Later P3-06/07 add scoped forecasting and paid selection;\nno final experiment has been established.")
    readme = replace_once(readme, "**652.160106918517 minutes**, with **307.839893081483** remaining to the\n960-minute floor. P3-B is next and unattempted; P3-08 remains unstarted.",
        f"**{phase} minutes**, with **{remaining}** remaining to the\n960-minute floor. **P3-B has passed** at restricted mathematical/local implementation\nreadiness. P3-08 remains unstarted. Optional paid-selective-feedback recurrence\nis recommended before it and remains unselected; see the [gate assessment](checkpoints/B_1.md).")
    readme = replace_once(readme, "| Mathematical Markdown |", "| Mathematics and implementation readiness | [P3-B decision](checkpoints/B_1.md) · [Current 21-duty overlay](checkpoints/B_1.v1.json) · [Optional recurrence advice](work_logs/P3_B_2026-10-09_S1/reviews/recurrence_agent/advice.md) |\n| Mathematical Markdown |")
    readme += "\n\n## P3-B completion and recurrence advice — October 9, 2026\n\n" + (
        "The [technical gate](checkpoints/B_1.md) is **PASS**. Independent targeted\n"
        "reviews reconstruct the received-source soundness bridge, sourcewise repair\n"
        "selection, all-current-optimum transport, forecast/feedback distinction and\n"
        "complete-policy expectation contract. Current local evidence and bounded\n"
        "admission interfaces support integration; the single combined reasoner is\n"
        "still P3-08 work. Historical completion sections above retain their original\n"
        "gate status; this section and the current plan give the latest state.\n\n"
        "The five-question assessment gives Q5 the strongest mature answer and\n"
        "identifies useful model-combination evidence (Q3) and economical selected\n"
        "feedback (Q4) as the weakest links. P3-N01 remains **NOT YET SUPPORTED**\n"
        "under the broad modest-synthesis criterion. No empirical superiority or\n"
        "unrestricted Logical Induction is inferred from the gate.\n\n"
        "**Recommended optional recurrence: one Research90 chunk now, before\n"
        "P3-08, on paid selective feedback.** Target a justified all-issued cost\n"
        "inequality and an informative break-even regime or precise obstruction.\n"
        "[The dossier](work_logs/P3_B_2026-10-09_S1/reviews/recurrence_agent/advice.md)\n"
        "also specifies certificate-delivery recurrence before final freeze and\n"
        "counterpossible-policy robustness later in the phase. All options remain\n"
        "unselected and unstarted; none activates R-P3-N01. Direct P3-08 progression\n"
        "is technically justified under the narrower accepted contract.\n\n"
        f"The [session](work_logs/P3_B_2026-10-09_S1.md) records **{rmin} research\n"
        "minutes**, with no added gate floor, no historical inference and no parallel\n"
        "reviewer credit. P3-01–07 and the surviving defensive-forecasting evidence\n"
        "remain unchanged. P3-A/B are PASS; P3-08 is unstarted; P3-C/D are\n"
        "unattempted. No final challenge is frozen or exposed.\n")

    claims = base_bytes("v3/claim_ledger.md").decode()
    claims = replace_once(claims, "readiness; P3-B–D remain unattempted.", "readiness; P3-B now passes at restricted mathematical/local implementation\nreadiness and P3-C–D remain unattempted.")
    claims = replace_once(claims, "with observed Research90. Next: P3-B, unattempted; P3-08 remains unstarted.",
        "with observed Research90. P3-B is now PASS with no additional floor.\nNext: P3-08, unstarted; optional recurrence A is recommended but unselected.")
    claims += "\n\n## P3-B — restricted readiness and optional recurrence\n\n" + (
        "The [gate](checkpoints/B_1.md) is **PASS**. This is the latest readiness\n"
        "overlay; earlier dated entries retain their historical task/gate pointers.\n\n"
        "| Record | Current finding | Evidence and boundary |\n"
        "|---|---|---|\n"
        "| P3-GB01 | Coherent restricted semantics, reconstructed central arguments, nonvacuous cases and implementable predictions are ready for integration. | [B_1](checkpoints/B_1.md), [21-duty contract](checkpoints/B_1.v1.json), principal reconstruction and three nonblind same-model reviews. A single combined reasoner is not yet implemented. |\n"
        "| P3-GB02 | Unresolved sources stay outside repair minimization; all current optima retain coverage; forecasts, checked evidence and request-law expectations have separate bridges. | Independent reconstruction and six tiny finite check groups. This is conditional composition readiness, not a universal theorem or a new numerical advantage. |\n"
        "| P3-GB03 | Current source/evidence bindings and bounded profile admission are coherent. | Three narrow current-selector calls; 508 initial binding passes and two historical locations resolved exactly with the failed record preserved. No old experiment rerun. |\n"
        "| P3-GB04 | Optional paid selective feedback is the recommended additional research route before P3-08. | [Options and forecasts](work_logs/P3_B_2026-10-09_S1/recurrence_options.json): A now; B before freeze if equal certificate delivery matters; C later for counterpossible-policy robustness. All unselected, distinct from R-P3-N01. |\n"
        "| P3-N01 | **NOT YET SUPPORTED.** Q3 has the weakest affirmative comparison and Q4 retains the paid-feedback gap. | Gate passage does not decide contribution. A useful modest adaptation, application, synthesis or consequential limitation can qualify without worldwide priority or universal superiority. |\n\n"
        f"The [closed gate](work_logs/P3_B_2026-10-09_S1.md) adds **{rmin}**\n"
        f"research minutes. Phase total: **{phase}**; remaining floor:\n"
        f"**{remaining}**. Prior ledger bytes and P3-01–07 evidence, including\n"
        "the defensive-forecasting addendum, are preserved. No historical or parallel\n"
        "time is credited. P3-08 remains unstarted, P3-C/D unattempted, and all\n"
        "recurrences unselected. No final challenge is frozen or exposed.\n")

    session = f"""# P3-B — 2026-10-09 S1

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Attempt **P3-B-1**.
Published input: `{BASE}`. All timestamps are UTC.

## Outcome and evidence

**PASS at restricted mathematical and local implementation readiness.** The
[gate](../checkpoints/B_1.md) gives the full scientific judgment; its
[contract](../checkpoints/B_1.v1.json) binds the current 21-duty overlay,
review evidence, decision and actuals. P3-07 publication and its exact tree
were verified at entry. No P3-B clock or prior attempt was found.

Independent same-model nonblind assignments reconstructed semantic bridges,
current implementation/evidence contracts and scientific recurrence value.
The principal reconstructed and reconciled their load-bearing content.
Six tiny finite semantic groups and three current selector calls are new
development evidence. No previous development suite or experiment was rerun.
The first historical binding failures and their exact dispositions survive.

The final semantic reconciliation corrected three integration-prediction
qualifications: an already loose sound bound need not widen, failure of one
cutoff route does not refute a comparison, and fallback needs funded output.
The original review and the [resolution](P3_B_2026-10-09_S1/reviews/semantics_agent/resolution.json)
are preserved separately. No existing source theorem needed repair.

## Recurrence decision and next boundary

**Recommend optional Research90 A now, before P3-08, on paid selective feedback.**
The [options](P3_B_2026-10-09_S1/recurrence_options.json) and
[dossier](P3_B_2026-10-09_S1/reviews/recurrence_agent/advice.md) state the target,
ordinary controls, central/high forecasts and alternatives. No option is
selected or started. Direct P3-08 progress is technically justified under the
current narrower contract. P3-N01 remains **NOT YET SUPPORTED**; no R-P3-N01
recurrence is activated. P3-08 is unstarted and P3-C/D are unattempted.

## Observed accounting

P3-B has **no added research floor**. Actual new research is **{rmin} minutes**
(`{actuals['research_ns']}` ns), and measured engaged time is
**{actuals['total_engaged_minutes']} minutes**. Category totals:

| Mode | Observed minutes |
|---|---:|
"""
    for mode in ("D", "L", "E", "O", "unmeasured", "recovery"):
        session += f"| {mode} | {actuals['category_minutes'].get(mode, '0')} |\n"
    session += f"""
The [raw clock](P3_B_2026-10-09_S1/clocks.jsonl),
[raw segments](P3_B_2026-10-09_S1/segments.jsonl),
[disposition](P3_B_2026-10-09_S1/clock_dispositions.jsonl) and
[effective segments](P3_B_2026-10-09_S1/effective_segments.jsonl) retain exact
observations. The open literature interval across context compaction was
excluded in full because no later direct pre-gap boundary existed. No time
was inferred from conversation duration. Reviewer credit is zero.

Phase qualifying research is now **{phase} minutes**, leaving
**{remaining} minutes** to the 960-minute floor. No new phase checkpoint was
crossed. P3-08–11 already contain 330 planned protected research minutes;
recurrence is advised for scientific value, not to fill time.

The [actuals](P3_B_2026-10-09_S1/actuals.json) record exact R/X totals,
forecast errors and the base/append/result ledger hashes. The prior
148,588-byte ledger is an unchanged prefix; only this gate's effective
segments are appended. Phase-two accounting is unchanged. Publication,
packaging and response work after the observed close are unmeasured, with
zero additional research or engaged credit.

No final challenge is frozen or exposed. Prior P3-01–07 artifacts and the
surviving defensive-forecasting addendum and evidence are preserved. The
task boundary stops here pending the author's next selection.
"""

    outputs = {"v3/checkpoints/B_1.v1.json": encoded(contract), "v3/plan.v1.json": encoded(plan),
        "TODO_v3.md": todo.encode(), "v3/README.md": readme.encode(), "v3/claim_ledger.md": claims.encode(), REL+".md": session.encode()}
    # All current-control expectations are checked before any write.
    for rel in ("TODO_v3.md", "v3/README.md", "v3/claim_ledger.md"):
        assert (REPO/rel).read_bytes() in (base_bytes(rel), outputs[rel]), ("Unexpected current edit", rel)
    for rel, data in outputs.items():
        path = REPO / rel
        if rel in ("v3/checkpoints/B_1.v1.json", REL+".md") and path.exists():
            assert path.read_bytes() == data, ("Refuse to overwrite different gate artifact", rel)
        temp = path.with_suffix(path.suffix + ".tmp")
        temp.write_bytes(data)
        temp.replace(path)
    print(json.dumps({"verdict": "PASS", "duties": len(duty_rows), "review_artifacts": len(reviews),
        "research_minutes": rmin, "phase_research_minutes": phase, "remaining_minutes": remaining,
        "next": "P3-08", "next_started": False, "recurrence_selected": None}, indent=2))


if __name__ == "__main__":
    main()
