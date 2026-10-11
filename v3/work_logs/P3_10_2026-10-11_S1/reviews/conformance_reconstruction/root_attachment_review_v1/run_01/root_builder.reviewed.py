"""Attach P3-10 interpretation without rewriting accepted duty dispositions.

Contributor: ChatGPT (GPT-6 Astra Pro), principal /root, 2026-10-11.
This is a document/evidence constructor; it does not run a paid method.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json

REPO = Path(__file__).resolve().parents[3]
W = Path(__file__).resolve().parent
OLD = REPO / "v3/checkpoints/B_1_R_P3_B_B.v1.json"


def bind(path):
    p = REPO / path
    data = p.read_bytes()
    return {"path": path, "bytes": len(data), "sha256": sha256(data).hexdigest()}


# Every row is an interpretation of already acquired evidence. Full inherited
# records, including historical scope and limitations, are copied below.
NOTES = {
    "U01": ("A0; B0; C0", "336 broker episodes and 104 certificate histories use their admitted source/runtime and charged interfaces. The original stage then fails before completing conformance; A1 preserves that boundary and supplies a separately sealed continuation.", "Finite admission and honest staging are supported. The deterministic initialization defect is an integration failure, and the source/meter contract remains a trusted finite implementation rather than a physical or hostile-host resource theorem."),
    "U02": ("A0; B0/B1; failure audit", "416 certificate attempts yield 356 valid current warrants and 60 explicit ResourceExhausted denials. The separate unsealed original structural exception has unknown exact prefix cost.", "A denied service is neither a false mathematical statement nor an invalid delivered warrant. A saved failure stage does not recover the rejected charge, and the exception cannot be silently scored as an ordinary null or free work."),
    "U03": ("A0; numerical reconstruction; C0", "Saved CNF labels and hard-receipt bindings reconstruct exactly; information and structural outputs satisfy their represented finite reference constraints.", "Correct marginal truth checks and checked bound domains do not make the learned forecast vector a coherent joint probability law. The two advice signatures can merge opposite truths without implying that those mathematical truths are indeterminate."),
    "U04": ("A1/A3; B1", "The numerical reconstruction separates 526 prior-receipt forecast corrections, 162 prospective action changes and 98 terminal corrections, while preserving original issuance records. Current certificate identity is independently checked over the edited sublevel.", "The earlier owned CNF hardening integration is retained. The ADD/native certificate receiver is still separate from that learner; final broker report epochs are unchanged, so this run does not add an unseen withdrawal or combined structural-learning result."),
    "U05": ("first-occurrence slice; actual capped histories", "First-occurrence and transfer positions remain scored even when adverse. After 60 capped certificate failures, 52 further attempts are actually made, 28 delivering and 24 failing again.", "Finite recovery and correct recurring replies do not prove eventual discovery. Additional budget does not erase grammar/arithmetic caps or establish nested formats, and successful paths do not imply affordable uninterrupted service."),
    "U06": ("A2; transfer interpretation", "Three of six distinct selector/family means meet the frozen base-versus-equal-advice threshold. Both gate suffix comparisons are adverse, and all 8,946 first-occurrence positions exclude prior receipt hardening.", "The gains are finite before-resolution effects against the declared original advice mixture. Retrospective signature fits use saved truth and add no new anticipation; the stronger paid ordinary catalogue still prevents an affirmative general economic-discovery claim."),
    "U07": ("A2/A5; fixed-cohort limitations", "All 126 reports deliver; no aggregate F/V cell meets practical narrowing, while four gate/uniform Z cells do, including coupled duplicate paths.", "These counts and widths are neither empirical coverage nor calibration. The fixed-end reporting theorem retains its exogeneity, positive-propensity, fair-bit and all-path-funding hypotheses; the MT cohort does not prove them."),
    "U08": ("A2; rounding and transfer derivations", "The original six expert readouts, equal mixture, constant half and descriptive hard-mask readouts all remain available. Final dyadic projection contributes at most 5/196608 absolute Brier change per position.", "The rounding bound applies after integer weight updates and is not a bound on accumulated update rounding. The original fixed-expert theorem is not replaced by regret against experts upgraded with realized hard evidence, or by an adaptive-policy/action guarantee."),
    "U09": ("A0/A1/A5; 2,688 numerical acquisition blocks", "Owned four-position block traces, selected receipts and forecast/action chronology reconstruct from the saved public transcripts. New gate keys are checked both for suffix uniqueness and disjointness from the prefix.", "This preserves the frozen exogenous selective-feedback setting. It does not identify a causal selector effect, turn pseudorandom paths into independent fair-bit experiments, or implement endogenous discovery, delay correction or a new propensity law."),
    "V01": ("A2/A3/A5; B0; C0", "Issued Brier F, conditional terminal-error functional V, realized terminal count Z, known-stakes action loss, current uniform bounds and separately priced resource accounts are interpreted with their declared types.", "The exact public F-V identity is an affine relation between report targets; it does not turn their values into the same service. Robust maxima (4,4,3) in the tied fixture violate a common-expectation linear identity, and valid positive bounds do not certify non-deterioration."),
    "V02": ("C0 information; public report geometry", "The 36 information certificates give 20 full-law recoveries and 16 nonidentifications, with 37 of 64 target rows recoverable. Exact F/V translations and binary-key report geometry are reconstructed separately.", "The expected-loss theorem requires a full-simplex law, shared nuisance calibration and exact observations; 12 one-state controls and four empty target families retain their trivial/vacuous status. The 24 minimum repair queries are hypothetical additions, not acquired data or recovered unknown truths."),
    "V03": ("A3; B0; tied decision interpretation", "All six paired hardening action means improve, four practically; known asymmetric-stakes orientations have different signs. The tied structural menu selects fallback by fixed pure minimax, while current certificate bounds remain +1 or +3/2.", "Action effects, uniform difference bounds and expected losses are different bridges. The supplied incumbent is not an acquired optimizer. A hypothetical independent lottery has a different risk quantifier and no executed paid structural implementation in this experiment."),
    "V04": ("A3/A4/A5; B2; unknown-prefix audit", "All cached broker bills exceed cold bills. Direct ordinary checking is cheaper in all eight full certificate group/recipient cells and covers 14/16 capped requests per recipient versus reuse's 6/16. All 60 failed certificate invoices remain included.", "Completed-path adverse comparisons are supported independently of the global positive-economic gate, which remains false because the original conformance prefix bill is unknown. Broker, certificate and structural tariffs are not summed or exchanged; optional report fees and physical runtime remain distinct."),
    "M01": ("distinct ordinary catalogue; B2; C0", "Three distinct ordinary witnesses each have lower realized loss and lower charged cost per request than all four numerical candidate configurations on their family. Direct ordinary checking realizes the same current-bound service, and ordinary structural outputs match on all nine fixtures.", "These fixed-path limitations do not establish that plurality can never help. The transported old warrants are sound conditional facts, not learned fallible models; affirmative advantage over the strongest ordinary combination remains OPEN and P3-N01 retains only its accepted modest support."),
    "R01": ("A0; B1; A1 lineage", "Original exposure, 440 sealed public records and the failed prefix are preserved. Certificate request/source/current bindings survive exact reconstruction; failed attempts withdraw current receipt authority while retaining completed source installation.", "Withdrawing a current receipt does not make every earlier mathematical fact false. Equal output and unchanged counts are not a replacement for complete source/history binding, and the explicit amendment does not restore unamended confirmatory status to the affected conformance records."),
    "C01": ("C0 structural; certificate edits", "The inherited nine-case structural panel distinguishes conditioning, occurrence, actor, shared-code, stored-copy and predictor changes, while certificate histories separately edit hard constraints, rank, incumbent and loss.", "The operations remain separately defined. Equivalent diagram syntax or a valid transported bound does not select a new counterfactual policy or permit another occurrence, stored copy or predictor to change without its own declared intervention."),
    "C02": ("C0 source quantifiers; tied decision interpretation", "Both unresolved sources with minimum repair ranks 1 and 2 remain admitted; sourcewise positive affine rank changes preserve their own minima. The fixed action cannot depend on a hidden retained state.", "The supplied graph, repairs, ranks and source uncertainty are not identified from observations. Joint source/repair minimization would impose unprovided cross-source rank units, and a unique minimax reply neither identifies the true source nor supplies a hidden probability law."),
    "C03": ("B0/B1; C0 ties", "Scalar reconstruction checks feasible incumbents and every current sublevel member, including nonminimal states at the rank-one cutoff; both tied structural states and all unresolved sources remain included.", "A receipt's assignment-domain coverage and a capped history's delivered request-ID set are different objects. Positive attained bounds do not imply action improvement, and pure minimax over the declared deterministic menu is not optimality over an expanded lottery menu."),
    "C04": ("C0 known counterpossible regression", "The original classical contradiction remains infeasible under conditioning; the explicit exceptional paired-support fixture retains both tied repairs and returns the declared fixed minimax action.", "This is post-exposure amended replay of a known finite exceptional policy. Topic preservation, policy justification, unseen counterpossible robustness and composition with selective feedback remain open; Option C is unselected."),
    "I01": ("A1/A4; B0/B2; C0", "150 prescribed broker pair records and 18 executed identity mirrors reconstruct. The full direct certificate primitive vector weakly dominates P-REUSE in all eight cells, but actual cap histories have different request coverage and future states.", "Equal mathematical outputs do not imply equal bills, internal state, grammar admission or funded availability. Fixed-path repricing is not a changed-budget rerun, and full-service primitive dominance must not be imported into capped comparisons with different delivered outputs."),
    "F01": ("A5; observers; staged provenance", "The paid reporter uses its owned transcript. Separate post-outcome observers produce deterministic retrospective bounds, report geometry, transfer moments and architecture decompositions with sources, failures and independent reconstructions retained.", "These external, unbilled, unblinded interpretations are not deployed self-assessment or paid report improvements. They prove no self-trust, reflection, empirical randomness, endogenous-feedback guarantee or author-gate completion, and agent overlap earns no principal Research90 credit."),
}


def main():
    prior = json.loads(OLD.read_text())
    assert sha256(OLD.read_bytes()).hexdigest() == "4dbff438e98fcdf2abd03abd29596ecbc5b99f22557e0d7d20374f05049d5677"
    assert set(NOTES) == {d["id"] for d in prior["duties"]}
    broker_path = "v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/broker_duty_evidence_attachment_A1.json"
    conf_path = "v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/duty_attachment_v1/output/attachment.json"
    broker = {d["id"]: d for d in json.loads((REPO/broker_path).read_text())["duties"]}
    conf = {d["id"]: d for d in json.loads((REPO/conf_path).read_text())["duties"]}
    rows = []
    for d in prior["duties"]:
        assert broker[d["id"]]["prior_record_retained_verbatim"] == d
        c = conf[d["id"]]
        assert c["accepted_status"] == d["status"]
        assert c["accepted_residuals_verbatim"] == d["limitations_and_open_obligations"]
        endpoint, evidence, boundary = NOTES[d["id"]]
        rows.append({"id": d["id"], "accepted_record_retained_verbatim": d,
                     "authoritative_status_change": False, "P3_10_endpoint_scope": endpoint,
                     "P3_10_finite_evidence": evidence, "P3_10_interpretation_and_retained_boundary": boundary,
                     "independent_broker_attachment": {k: v for k, v in broker[d["id"]].items() if k != "prior_record_retained_verbatim"},
                     "independent_conformance_attachment": c})
    evidence_paths = [broker_path, conf_path,
        "v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/final_review_v1/review.md",
        "v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/final_observation_v4/results.json",
        "v3/work_logs/P3_10_2026-10-11_S1/gate_architecture_observation_A1/results.json",
        "v3/work_logs/P3_10_2026-10-11_S1/decision_service_interpretation.md",
        "v3/work_logs/P3_10_2026-10-11_S1/joint_report_geometry_observation_A1/public_geometry.json"]
    obj = {"schema": "P3-10-duty-evidence-attachment-v1", "task": "P3-10",
           "contributor": "ChatGPT (GPT-6 Astra Pro), principal /root",
           "signed_utc": datetime.now(timezone.utc).isoformat(),
           "kind": "post-outcome scientific interpretation; no accepted status replacement",
           "accepted_overlay": bind(str(OLD.relative_to(REPO))), "duties": rows,
           "duty_count": 21, "accepted_statuses_changed": 0, "accepted_residuals_changed": 0,
           "new_paid_executions": 0, "accepted_overlay_historical_metadata_treated_as_current": False,
           "new_evidence_bindings": [bind(p) for p in evidence_paths],
           "P3_N01": "SUPPORTED at the accepted modest formal-adaptation and implementation-synthesis scope",
           "Q3_affirmative_strongest_ordinary_advantage": "OPEN",
           "P3_11": "unstarted", "P3_C": "unattempted", "P3_D": "unattempted",
           "conformance_status": "post-exposure amended inherited conformance",
           "original_public_complete": False, "original_failed_prefix_exact_cost": None}
    target = W / "duty_evidence_attachment.json"
    assert not target.exists(), "Preserve the initial signed attachment; use a versioned correction."
    target.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    lines = ["# P3-10 evidence against all 21 accepted duties", "",
        "Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.", "",
        "This is an additive interpretation of completed finite evidence. The accepted",
        "[Option B overlay](../../checkpoints/B_1_R_P3_B_B.v1.json) remains authoritative.",
        "Its 21 full duty records, status strings and residual obligations are retained",
        "verbatim in the [machine attachment](duty_evidence_attachment.json), together",
        "with independently prepared broker and conformance attachments. Historical",
        "task metadata in the old checkpoint is not treated as current status.", "",
        "The original 440 sealed broker/certificate acquisitions are unchanged; the",
        "60 affected conformance records are post-exposure amended inherited checks.",
        "Later algebra and saved-data observers are exploratory interpretation. None",
        "of these records supplies a new paid method, calibration/LI theorem, author",
        "decision, P3-11 selection or automatic contribution upgrade.", ""]
    for d in prior["duties"]:
        endpoint, evidence, boundary = NOTES[d["id"]]
        lines += [f"## {d['id']} — {d['title']}", "", f"**Evidence ({endpoint}).** {evidence}", "",
                  f"**Interpretation.** {boundary}", "",
                  f"Accepted status retained: `{d['status']}`.", ""]
    lines += ["## Retained project boundary", "",
        "P3-N01 remains SUPPORTED only at its accepted modest formal-adaptation and",
        "implementation-synthesis scope. Affirmative Q3 advantage over the strongest",
        "ordinary combination remains OPEN. The finite owned CNF broker integration",
        "is retained; it is not a joined ADD/counterpossible learner. P3-11 is unstarted,",
        "P3-C/D are unattempted, and Option C and R-P3-N01 remain unselected.", "",
        "This scientific attachment does not itself close Research90 or publication.", ""]
    (W / "duty_evidence_attachment.md").write_text("\n".join(lines))
    print(json.dumps({"path": str(target.relative_to(REPO)), "duties": 21,
                      "accepted_statuses_changed": 0, "accepted_residuals_changed": 0,
                      "sha256": sha256(target.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
