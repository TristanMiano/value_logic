#!/usr/bin/env python3
"""Write an additive broker evidence attachment; never edit the accepted overlay."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


W = Path(__file__).resolve().parent
REPO = W.parents[4]
OVERLAY = REPO / "v3/checkpoints/B_1_R_P3_B_B.v1.json"
EXPECTED_OVERLAY_SHA = "4dbff438e98fcdf2abd03abd29596ecbc5b99f22557e0d7d20374f05049d5677"


def bound(path):
    raw = path.read_bytes()
    return {"path": str(path.relative_to(REPO)), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


assert bound(OVERLAY)["sha256"] == EXPECTED_OVERLAY_SHA
prior = json.loads(OVERLAY.read_text())
assert len(prior["duties"]) == 21
review = json.loads((W / "broker_reconstruction_review_A1.json").read_text())
assert review["status"] == "PASS_SCOPED"

notes = {
    "U01": (
        "A0; staged provenance",
        "336 complete broker episodes / 28,160 positions pass the independently reconstructed admitted-information and receipt checks. The explicit 440-original + 60-amended composite public barrier precedes 500 private scores and one analysis; source/runtime and old/new bindings remain recorded.",
        "This adds finite execution evidence in the declared broker grammar/tariff. Preserve the accepted structural-service caps separately; neither arm's account establishes general physical CPU/heap bounds, malicious-host protection, or arbitrary-code safety."),
    "U02": (
        "A0; failure accounting",
        "All broker denominators close validly. The separate original conformance exception remains a deterministic infrastructure failure with unknown paid prefix, never a false mathematical label. A1 references preserved broker records and completes only the remaining units.",
        "The original public stage remains incomplete. No missing invoice is imputed, no unfavorable record is dropped, and no universal failure diagnostic is added. The global economic gate is false."),
    "U03": (
        "A0; scope retention",
        "Exact CNF truth, received-coordinate hard state and pre-purchase forecast records are checked on the finite cohort. This does not change the represented probability object's type.",
        "Retain the accepted distinction between numerical marginals and a coherent joint law; there is no new unreceived-entailment closure, additivity result, or joint-belief implementation."),
    "U04": (
        "A0–A1; A3",
        "72 base/live pairs preserve their declared base paths. Current-key hardening preserves historical forecasts and yields positive action improvements in every whole family/selector cell; uniform mixed and gate effects are below .01. The 36 cached/cold pairs preserve delivered/action paths.",
        "The prior finite broker integration closure is retained with its hypotheses. The separate certificate receiver has not been joined to this learner; no joint logical reasoner or changed historical forecast is inferred."),
    "U05": (
        "Finite horizon results",
        "All 336 scheduled finite episodes and every whole/first-key/prefix/transfer denominator are reported, including adverse gate-transfer outcomes.",
        "Completion through horizons 64 or 128 supplies no new infinite-stream convergence, eventual query discovery, unrestricted availability, or affordable uninterrupted-service theorem."),
    "U06": (
        "A2; first occurrence",
        "Before current-key receipt acquisition, first-key A2 effects are +.0410705697/+ .0026159470 on mixed and +.0765567602/+ .0100588499 on cheap for uniform/tickets. Gate first-key effects are −.0313025743/−.0007455880; suffix effects are −.0947277652/−.0034569141.",
        "First key means the full canonical formula/source key, not semantic independence. Cheap ordinary shortcuts and the complete catalogue remain available. Economic anticipation remains open; same-key reuse is post-resolution evidence, not a new learning theorem."),
    "U07": (
        "A2; A5 limits",
        "Exact finite Brier/action means and all 126 optional reports are disclosed. No configuration attains .01 F/V width reduction; gate-uniform Z narrowing is the limited practical report result.",
        "No calibration, seed-population inference, empirical coverage or fair-bit verification is added. The fixed MT paths do not establish Logical Induction non-exploitation or a coherent probability law."),
    "U08": (
        "A2; original readouts",
        "All six original expert, equal, dyadic-equal, constant-half and recorded same-hard-mask readouts are retained across all 200 slices. Whole A2 passes for uniform mixed/cheap and tickets cheap; both gate whole effects are adverse. The source forecast-rounding contribution is bounded by 5/196608 per position.",
        "A2 is a finite effect against the original equal readout. Same-hard readouts remain descriptive. Preserve original scoring/timing/propensity hypotheses; no adaptive-policy regret, greedy-action guarantee, trader-immunity or expanded fixed-expert theorem follows. Forecast rounding does not remove state-weight quantization."),
    "U09": (
        "A0–A1; A5 chronology",
        "Owned receipt/issuance chronology and all declared path equalities are reconstructed. Reporting uses the owned public transcript. The uniform and ticket selectors' common seed labels do not assert equal feedback paths across controllers.",
        "Retain exogenous tapes, frozen blocks, positive owned propensities, successful selected receipts and fixed-end funding assumptions. No missing/delayed/action-dependent discovery extension is supplied. The numerical weight/selector implementation is outside this observer's independent replay scope."),
    "V01": (
        "A2–A5; source identity",
        "Truth, base/issued probabilities, realized normalized W, J(λ), hard receipts, F/V/Z intervals and separate fees remain distinct. The source identity Brier = d(p,y) − p(1−p) is reviewed separately from observed action means.",
        "No conversion of an empirical score into exact expectation or fair randomness is made. V retains its conditional bit premise. Broker word units, certificate event/byte units and observed wall time are not exchanged or pooled."),
    "V03": (
        "A3; common stakes",
        "Hardening ΔW values are mixed 1/192 and 7/384, cheap 3/128 and 1/32, gate 1/256 and 3/256. Common-stakes probability-cost ΔW is 19/384 for stakes0 and −37/1152 for stakes1. Combined readout effects are 1/128 and −13/1152, retaining the adverse result.",
        "The named lottery/known-stakes bridges keep their conditions. Re-score both paths under common stakes and S before comparison; native means under different costs are not directly subtractable. No uniform action-cost estimation error rate, better greedy policy, or optimized incumbent search is established."),
    "V04": (
        "A3–A5 economics",
        "All 36 equal-output cached paths cost more than their cold mates; all six aggregate ratios exceed one. Distinct ordinary paths defeat every candidate at all applicable frozen prices. Reporting adds 65,407,686 units across actual executions. The two combined asymmetric completed-path ΔJ gains are retained descriptively.",
        "The unknown original paid prefix keeps end-to-end positive economics blocked. At positive price, completed-path threshold hits do not override that gate. Tariff claims are not physical speed, universal amortization, componentwise tariff dominance, or optimal value-of-computation claims."),
    "M01": (
        "A1; strong catalogue",
        "All 54 catalogue rows retain whole-configuration minima/ties and separate native-price eligibility from fixed-record repricing. All 120 applicable candidate differences against distinct ordinary minima are negative. Eighteen ordinary mirror executions are exactly identical, including fees.",
        "Affirmative Q3/P3-H03 remains OPEN. Identity mirrors are not independent methods or positive replications. The finite adverse catalogue does not prove universal impossibility of plurality; P3-N01 remains at its accepted modest scope pending separate P3-11 review."),
    "R01": (
        "A0–A1; A1 lineage",
        "Immutable issuance records and full query/source/provider/version/path identities are preserved. A1 binds new driver/manifest bytes while retaining original IDs and original bindings for 440 reused seals; the failed original remains visible.",
        "Final broker episodes use unchanged source epochs, so this adds no new final withdrawal experiment. Prior withdrawal/generation boundaries remain in force. Hashes bind observed bytes, not a malicious host, and changed runtimes or scopes still need justified rebinding/transport."),
    "F01": (
        "A5; versioned audit",
        "The public reporter succeeds on all 126 scheduled requests, and one saved-JSON observer reconstructs endpoints/fees after the explicit completion release. Original failure, versioned amendment, observer source, raw execution receipts, and auxiliary projection errors remain preserved.",
        "An external reconstruction is not a deployed self-model, self-proof, reflection, anytime coverage or report-dependent feedback theorem. Report exogeneity/fair-bit/fixed-end assumptions remain conditional. Agent minutes add zero to principal Research90; no later task or author gate is closed."),
}
assert set(notes) == {f"U{i:02d}" for i in range(1, 10)} | {"V01", "V03", "V04", "M01", "R01", "F01"}

rows = []
for row in prior["duties"]:
    attached = row["id"] in notes
    entry = {
        "id": row["id"], "title": row["title"],
        "disposition": "ADD_FINITE_BROKER_EVIDENCE_WITHOUT_STATUS_CHANGE" if attached else "UNCHANGED_NO_BROKER_ATTACHMENT",
        "prior_status_retained_verbatim": row["status"],
        "prior_record_retained_verbatim": row,
        "prior_residuals_retained_verbatim": row["limitations_and_open_obligations"],
        "authoritative_status_change": False,
    }
    if attached:
        endpoint, evidence, limits = notes[row["id"]]
        entry.update({"endpoint_scope": endpoint,
                      "P3_10_broker_finite_evidence": evidence,
                      "P3_10_additional_scope_caution": limits})
    rows.append(entry)
assert len(rows) == 21 and sum("P3_10_broker_finite_evidence" in r for r in rows) == 15
assert all(a["prior_record_retained_verbatim"] == b for a, b in zip(rows, prior["duties"]))

utc = datetime.now(timezone.utc).isoformat()
files = [OVERLAY, REPO / "v3/checkpoints/B_1_R_P3_B_B.md",
         REPO / "v3/experiments/protocol.md", REPO / "v3/experiments/protocol.v1.json",
         REPO / "v3/experiments/amendments/P3_10_A1/manifest.json",
         W / "broker_reconstruction_review_A1.md", W / "broker_reconstruction_review_A1.json",
         W / "findings_tables_A1.json", W / "findings_tables_A1.md",
         W / "attempt_A1_01/summary.json", W / "attempt_A1_01/input_manifest.json",
         W / "forecast_and_lineage_source_review.v1.json", Path(__file__)]
obj = {
    "schema": "value_logic.P3-10-A1.broker_duty_evidence_attachment.v1",
    "signed_utc": utc, "contributor": "ChatGPT (GPT-6 Astra Pro)",
    "reviewer_agent": "/root/freeze_review", "task": "P3-10",
    "kind": "Review draft finite evidence attachment; no author decision or replacement overlay",
    "accepted_overlay": bound(OVERLAY),
    "all_21_prior_statuses_and_residuals_retained": True,
    "amendment_manifest_sha256": "36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359",
    "broker_observer_status": "PASS_SCOPED",
    "broker_observer_comparisons": 193933, "broker_observer_mismatches": 0,
    "complete_outer_attempt_economic_claim_permitted": False,
    "duties": rows,
    "attached_duty_count": 15, "other_duty_count_unchanged": 6,
    "contribution_position_retained": prior["contribution"],
    "Q3_position_retained": prior["Q3"],
    "later_boundaries": {"P3-11": "unstarted by this attachment",
                          "P3-C": "unattempted by this attachment",
                          "P3-D": "unattempted by this attachment",
                          "Option C": "unselected",
                          "R-P3-N01": "unselected"},
    "accepted_overlay_historical_task_metadata_not_rewritten_or_treated_as_current": True,
    "principal_research_minutes_claimed": 0, "authoritative_status_or_gate_changes": False,
    "new_paid_executions": 0, "new_observer_executions": 0,
    "source_bindings": [bound(p) for p in files],
    "signature": "ChatGPT (GPT-6 Astra Pro), agent /root/freeze_review; observation-bound agent attestation",
}

lines = ["# P3-10-A1 broker evidence attachment to the accepted 21-duty overlay", "",
         f"Signed: **ChatGPT (GPT-6 Astra Pro)**, agent `/root/freeze_review`, **{utc}**. Principal Research90 time added: **0 minutes**.", "",
         "**Review draft: finite evidence mapping only.** The accepted overlay remains `v3/checkpoints/B_1_R_P3_B_B.v1.json`, SHA-256 `" + EXPECTED_OVERLAY_SHA + "`. Its 21 statuses, inherited scopes, and residual obligations are unchanged. The companion JSON retains every prior duty record and residual verbatim, adds broker evidence to 15 duties, and leaves the other six without a broker attachment. No accepted checkpoint file is edited.", "",
         "The attachment uses the signed A0–A5 reconstruction: 336 complete broker episodes, 28,160 positions, 126 successful reports, 150 pairs, 76 configuration means, 54 catalogue rows, and 193,933 comparisons with zero mismatches. All means and the 200 slices retain the frozen population/seed hierarchy and full scheduled denominators. Exact values, individual records, source hashes, and limitations are in `broker_reconstruction_review_A1.md/json` and `findings_tables_A1.md/json`.", "",
         "The versioned composite comprises 440 original seals and 60 amended conformance seals; all 500 private scores and the analysis completed. The original public stage remains failed, its interrupted prefix cost remains unknown, and the global end-to-end economic gate is false. Zero-price action effects and completed-path price diagnostics retain their stated separate meanings.", "",
         "## Broker evidence by duty", "",
         "Each row below retains the accepted status. The JSON is the exact status/residual record; the final column summarizes both the inherited boundary and the new result's limits.", "",
         "| Duty | Added finite evidence | Retained boundary and interpretation |",
         "| --- | --- | --- |"]
for row in rows:
    if "P3_10_broker_finite_evidence" not in row:
        continue
    lines.append("| **" + row["id"] + " — " + row["title"] + "** | "
                 + row["P3_10_broker_finite_evidence"] + " | "
                 + row["P3_10_additional_scope_caution"] + " |")
lines += ["", "## Unchanged duties and stopping boundary", "",
          "V02, C01, C02, C03, C04, and I01 retain their complete accepted records without a new broker evidence attachment. Their separate information, structural, certificate, and service-equivalence evidence is not reviewed by this mapping. The presence of all 500 seals is a lineage check, not an independent semantic reconstruction of those other arms.", "",
          "**P3-N01 remains SUPPORTED at its accepted modest formal-adaptation and implementation-synthesis scope. Affirmative Q3/P3-H03 remains OPEN.** The observed ordinary catalogue wins and identity mirrors limit an exclusive economic interpretation but do not decide the later contribution review or prove universal impossibility of plurality.", "",
          "**P3-11 remains unstarted by this attachment; P3-C and P3-D remain unattempted.** Option C and R-P3-N01 remain unselected. This attachment neither makes an author decision nor supplies principal research-clock credit. Historical task metadata inside the accepted October 10 overlay remains historical and is not rewritten as a claim that P3-09 or P3-10 has not occurred.", "",
          "## Source binding", "",
          "The companion JSON binds the accepted overlay, current protocol, exact A1 manifest, signed reconstruction, exact tables, source-only proof review and this attachment writer. It preserves the old records rather than replacing their statuses or residuals. No new final stage, paid method, or observer execution was run for this mapping.", ""]

md = W / "broker_duty_evidence_attachment_A1.md"
with md.open("x") as handle:
    handle.write("\n".join(lines))
obj["markdown_binding"] = bound(md)
out = W / "broker_duty_evidence_attachment_A1.json"
with out.open("x") as handle:
    json.dump(obj, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps({"status": "SIGNED_EVIDENCE_ATTACHMENT", "signed_utc": utc,
                  "all_21_statuses_and_residuals_retained": True,
                  "new_evidence_duties": 15, "markdown": bound(md), "json": bound(out)}, indent=2))
