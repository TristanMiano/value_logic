#!/usr/bin/env python3
"""Build a read-only P3-10 evidence attachment to the accepted 21-duty overlay.

Contributor: ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction.
Every accepted status, historical prior status, scope, and residual is copied
unchanged. This creates no checkpoint, approval, author gate, or phase advance.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import traceback

HERE = Path(__file__).resolve().parent
OWN = HERE.parent
REPO = HERE.parents[5]
AUTHOR = "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction"
FOCUS = ("V02", "C01", "C02", "C03", "C04", "I01", "F01")


def binding(path):
    data = path.read_bytes()
    return {"path": path.relative_to(REPO).as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def save(path, value):
    with path.open("x") as file:
        json.dump(value, file, indent=2, sort_keys=True, allow_nan=False)
        file.write("\n")


NOTES = {
    "U01": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "All 60 scheduled amended conformance obligations are independently reconstructed; structural invoices reconcile under the existing nine-fixture STRUCTURAL-VM-v1 tariff and 50,000,000-unit cap.",
        "limit": "Finite conformance adds no broader computational admission domain, physical CPU/heap guarantee, or hostile-code guarantee; the separate certificate domain and its caps remain unchanged."},
    "U02": {
        "evidence": ["conformance_result", "bootstrap_diagnosis", "release"],
        "addition": "Preserve four delivered complete structural infeasibility reports, six expected invalid-request rejections, and the original unsealed bootstrap exception as distinct events; A1 completes the 60 conformance units under its own binding.",
        "limit": "The original failed paid prefix remains unknown and is not a false label, failed mathematical bound, refunded service, or completed original-v1 public stage."},
    "U03": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "Exact paired-support truth conditions and supplied-law information certificates are checked within their separate finite semantics.",
        "limit": "Neither the paired-support interpretation nor the information auditor turns the learner's forecast vector into a coherent joint law or adds unreceived entailment closure."},
    "U04": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "The inherited structural and information arms retain distinct source-bound interfaces; their successful amended conformance does not alter the earlier accepted owned-broker integration closure.",
        "limit": "No composition of the structural counterpossible arm or ADD/native certificate receiver with the selective-feedback learner is supplied here."},
    "U05": {
        "evidence": ["conformance_result"],
        "addition": "The 60 saved finite conformance obligations have complete observed outcomes after A1.",
        "limit": "Finite completion proves no eventual discovery on an infinite stream, no nested-format availability theorem, and no affordable uninterrupted service."},
    "U06": {
        "evidence": ["conformance_result", "transfer_review", "transfer_check"],
        "addition": "Inherited conformance is separate from anticipation. The supplemental finite gate audit preserves favorable prefix and adverse transfer effects on the original forecast paths.",
        "limit": "Known fixtures, post-resolution certificates, and post-outcome moment explanations establish no economical anticipation on fresh mathematics."},
    "U07": {
        "evidence": ["conformance_result", "transfer_review"],
        "addition": "The information arm checks exact functional identifiability under declared expected-loss hypotheses; the transfer review checks deterministic finite moments.",
        "limit": "Neither certificate validity, recoverability counts, nor the mean-bias/covariance identity establishes calibration, sampling coverage, or a probability model for the experiment."},
    "U08": {
        "evidence": ["transfer_review", "transfer_check"],
        "addition": "All 56 supplemental A2 cells agree with frozen equal-original-advice versus base Brier comparisons, including the adverse uniform gate suffix.",
        "limit": "This preserves the comparator and finite outcome; it adds no adaptive-policy regret, hard-mask regret, action guarantee, or trader-immunity result."},
    "U09": {
        "evidence": ["transfer_review", "transfer_check", "retrospective_lemma"],
        "addition": "Saved feedback summaries, all 126 broker/mirror chronologies and unchanged gate-boundary weights are checked. Retrospective receipt interpretation leaves past issued forecasts and actions immutable.",
        "limit": "No new propensity law, causal acquisition identification, missing-label correction theorem, feedback composition, or report-dependent policy is established."},
    "V01": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "The audit distinguishes exact expected-loss inputs, recoverability/obstruction certificates, deterministic structural worst losses, input rejections, and charged tariff units.",
        "limit": "A loss certificate or tariff total is not automatically a probability, realized observation, acquired incumbent, optimal bound, or physical runtime."},
    "V02": {
        "evidence": ["conformance_result", "theory_comparison", "information_examples", "main_review"],
        "addition": "All 36 exact information certificates and six invalid-input controls check. Full law: 20 recoverable and 16 nonidentified. Requested family: 22 recoverable and 14 partly nonidentified. Original targets: 37 of 64 recoverable and 27 nonidentified. Fourteen positive repairs require 24 minimum extra raw queries in total. All 138 positive identities, 43 collisions/obstructions, and 48 repair dual pairings are independently verified.",
        "limit": "These are inherited finite supplied-law/source-fiber results under exact expected-loss rows, a full simplex and shared nuisance. Twelve one-state controls are trivial and four target-family flags are vacuous. The separate ADD receipt still exports its requested inequality service; neither it nor a broker forecast is upgraded to full-law recovery, closure of every consequence, or recovery of all producer information."},
    "V03": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "The structural suite delivers 14 fixed-action warrants across the two methods and four complete infeasibility reports. The fixed minimax action is evaluated against every retained source/minimum.",
        "limit": "This bounded known-loss decision check does not acquire the certificate service's incumbent, optimize its bound, learn action-cost errors, or strengthen the separate lottery/known-stakes bridge."},
    "V04": {
        "evidence": ["conformance_result", "main_review", "release"],
        "addition": "Structural cold totals over nine cases are 2,821,113 candidate and 1,603,090 ordinary; local totals are 2,047,338 and 1,181,962. Ordinary is lower on every fixture under both declared measures, with identical per-fixture terminals.",
        "limit": "These separate structural tariff sums establish no universal cost advantage or physical speed result, and the original unknown failed prefix prevents complete outer-attempt economic accounting. External observer and supplemental-report computation are unbilled."},
    "M01": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "Two supplied unresolved structural sources are retained when their minimum ranks differ, and the candidate is compared with the ordinary implementation on identical fixtures.",
        "limit": "Supplied source alternatives are not learned fallible empirical models; all nine terminal matches and lower ordinary costs establish no affirmative plurality advantage and do not close Q3/P3-H03."},
    "R01": {
        "evidence": ["conformance_result", "release", "bootstrap_diagnosis", "main_review"],
        "addition": "Pinned original and A1 manifest/protocol identities, 12 original input references and a mixed 440+60 public composition preserve exact provenance. The original public failure is retained without fabricating completion.",
        "limit": "Byte hashes and owned-process lineage checks do not authenticate a malicious host or justify arbitrary interpreter/coordinate transport; the accepted current-scope obligations remain."},
    "C01": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "Conditioning is infeasible; occurrence and actor-only replacement yield (1,0,0,0) with fallback 6; shared replacement yields (1,1,0,0) with commit 5; shared-and-copy yields (1,1,1,0) with commit 4; explicit predictor rerouting yields (1,1,1,1) with commit 2. Each of the nine fixtures has the same full terminal under both methods.",
        "limit": "Coinciding outcomes for two operations on this fixture do not identify their semantics generally. No new general counterfactual semantics or automatic transport from diagram equality is selected."},
    "C02": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "The external-sources fixture retains both supplied source cases, ranks 1 and 2, with two minima each. Fixed fallback loss is 3; the forbidden joint source/repair minimization would report 0 and is marked inadmissible.",
        "limit": "The structure, source cases, and repair weights are supplied. The result does not infer missing causal structure, resolve observationally indistinguishable structures, select an objectively preferred rank, or justify the exception policy."},
    "C03": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "All 18 structural terminals reconstruct exactly: 14 useful fixed-action warrants and four complete infeasibility reports. The counterpossible tied-minima case retains both minima, with fixed fallback loss 3 and an explicitly nonimplementable pointwise oracle value 0.",
        "limit": "The complete minimizer identity lists belong to the separate inherited structural suite. They do not change the ADD/native sublevel receipt into a minimizer-enumeration or action-choice service, nor make empty/failed selection a useful-action warrant."},
    "C04": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "The original contradictory quote has zero ordinary Boolean satisfying valuations while the explicit paired-support rule retains the declared finite minima. The fixed falsity constant remains infeasible. These exact named outcomes pass under both methods after A1.",
        "limit": "This is inherited counterpossible conformance, not a new counterpossible theorem. Topic preservation, justification of exceptional policies, and composition with selective feedback remain open in their accepted scopes."},
    "I01": {
        "evidence": ["conformance_result", "main_review"],
        "addition": "Candidate and ordinary produce identical complete terminal data on all nine structural fixtures; their invoices differ, with ordinary lower on every matched cold and local measure.",
        "limit": "Nine exact matches establish no universal representation theorem, total bidirectional compiler, equivalence of internal state/proof length, availability under another budget, or physical speed result. Earlier format/adapter and parity-fragment limits remain unchanged."},
    "F01": {
        "evidence": ["conformance_result", "release", "main_review", "retrospective_lemma", "retrospective_width", "transfer_review", "transfer_check"],
        "addition": "A source-bound release precedes independent saved-data reconstruction; original failures, unused observer revisions, one successful conformance observation and one successful transfer reconciliation are retained. Supplemental retrospective bounds and finite moment decompositions remain separately labeled external interpretations.",
        "limit": "These external unbilled observers are not deployed self-models, self-proofs, endogenous feedback guarantees, future/anytime guarantees, or evidence of fair bits. They add zero principal research credit and authorize no author gate or later phase."},
}


def main():
    out = HERE / "output"
    out.mkdir(exist_ok=False)
    save(out / "start.json", {"contributor": AUTHOR, "created_utc": datetime.now(timezone.utc).isoformat(),
         "principal_clock_credit_seconds": 0, "source": binding(Path(__file__))})
    try:
        overlay_path = REPO / "v3/checkpoints/B_1_R_P3_B_B.v1.json"
        overlay_binding = binding(overlay_path)
        assert overlay_binding["sha256"] == "4dbff438e98fcdf2abd03abd29596ecbc5b99f22557e0d7d20374f05049d5677"
        overlay = json.loads(overlay_path.read_text())
        assert len(overlay["duties"]) == len(NOTES) == 21
        assert {d["id"] for d in overlay["duties"]} == set(NOTES)
        paths = {
            "conformance_result": OWN / "runs/attempt_01/result.json",
            "main_review": OWN / "REVIEW.md",
            "theory_comparison": OWN / "derived_v1/theory_comparison.json",
            "information_examples": OWN / "derived_v1/certificate_examples.json",
            "release": OWN / "completion_release_A1.json",
            "bootstrap_diagnosis": OWN / "amendment_proposal_v1/diagnosis_and_minimal_amendment.md",
            "retrospective_lemma": OWN / "supplemental_reporting_note_v1.md",
            "retrospective_width": OWN / "width_decomposition_review_v1.md",
            "transfer_review": OWN / "transfer_review_v1/REVIEW.md",
            "transfer_check": OWN / "transfer_review_v1/run_01/results.json",
        }
        evidence = {key: binding(path) for key, path in paths.items()}
        result = json.loads(paths["conformance_result"].read_text())
        assert result["status"] == "PASS" and len(result["rows"]) == 60
        rows = []
        for old in overlay["duties"]:
            note = NOTES[old["id"]]
            old_bytes = (json.dumps(old, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False) + "\n").encode()
            rows.append({"id": old["id"], "title": old["title"],
                "accepted_duty_sha256": hashlib.sha256(old_bytes).hexdigest(),
                "accepted_status": old["status"], "status_after_attachment": old["status"],
                "accepted_historical_prior_status": old["prior_status"],
                "accepted_disposition": old["disposition"],
                "accepted_inherited_scope_retained_verbatim": old["inherited_scope_retained"],
                "accepted_scope_verbatim": old["scope"],
                "accepted_residuals_verbatim": old["limitations_and_open_obligations"],
                "attachment_disposition": "READ_ONLY_EVIDENCE_ATTACHMENT_STATUS_UNCHANGED",
                "focus_duty": old["id"] in FOCUS, "new_evidence_keys": note["evidence"],
                "new_evidence_interpretation": note["addition"], "attachment_specific_residual": note["limit"]})
        artifact = {"schema": "value_logic.p310.read_only_21_duty_evidence_attachment.v1",
            "contributor": AUTHOR, "signed_utc": datetime.now(timezone.utc).isoformat(),
            "kind": "Draft additive evidence mapping for principal review; no checkpoint or gate adoption",
            "principal_clock_credit_seconds": 0, "accepted_overlay": overlay_binding,
            "accepted_checkpoint_unmodified": True, "duty_count": 21, "accepted_statuses_changed": 0,
            "historical_prior_statuses_changed": 0, "accepted_residuals_changed": 0,
            "amendment_id": "P3-10-A1", "conformance_evidence_class": "post_exposure_amended_inherited_conformance",
            "original_v1_public_complete": False, "original_failed_prefix_cost": "unknown",
            "scientific_scope": "All 60 inherited conformance units; separately labeled external post-outcome interpretations",
            "focus_duties": list(FOCUS), "evidence": evidence, "duties": rows,
            "accepted_global_boundaries_retained_verbatim": {k: overlay[k] for k in ("Q3", "U04", "contribution", "preserve_boundaries")},
            "author_gate_action": None, "P3_11_action": None, "phase_advance": False,
            "accepted_duty_hash_serialization": "sorted compact ASCII JSON with one trailing newline",
            "limitations": ["No existing accepted status or residual is upgraded, downgraded, closed, or rewritten.",
                "The accepted overlay remains a dated historical snapshot; its older phase/exposure metadata is not edited by this attachment.",
                "Conformance on exposed inherited cases is not unseen-transfer evidence, novelty adjudication, or a positive economic result."]}
        for old, new in zip(overlay["duties"], rows):
            assert new["accepted_status"] == new["status_after_attachment"] == old["status"]
            assert new["accepted_historical_prior_status"] == old["prior_status"]
            assert new["accepted_residuals_verbatim"] == old["limitations_and_open_obligations"]
        save(out / "attachment.json", artifact)
        lines = ["# P3-10-A1 evidence attachment to the accepted 21-duty overlay", "",
            "**Signed draft:** ChatGPT (GPT-6 Astra Pro), `/root/conformance_reconstruction`, 2026-10-11. Principal clock credit: **0**.", "",
            "This is a read-only evidence attachment. All 21 accepted statuses, all historical `prior_status` values, and all explicit residual texts are preserved unchanged in `attachment.json`. It does not adopt a new checkpoint, author gate, P3-11 decision, or phase advancement.", "",
            "Accepted source: `v3/checkpoints/B_1_R_P3_B_B.v1.json`, SHA-256 `" + overlay_binding["sha256"] + "`.", "",
            "The new conformance evidence consists of 60 post-exposure amended inherited units: 18 structural outputs, 36 exact information certificates, and six expected invalid-input rejections. The original 440-record public prefix is preserved; its first structural attempt failed, and its unsealed paid prefix cost is unknown. A1 conformance does not make the original-v1 public stage complete.", "",
            "## Focus duties: evidence and retained limits", ""]
        by_id = {r["id"]: r for r in rows}
        for identifier in FOCUS:
            row = by_id[identifier]
            lines += ["### " + identifier + " — " + row["title"], "",
                "**Accepted status retained:** `" + row["accepted_status"] + "`.", "",
                row["new_evidence_interpretation"], "", row["attachment_specific_residual"], ""]
        lines += ["## All 21 accepted statuses remain unchanged", "",
            "| Duty | Accepted status, retained verbatim |", "|---|---|"]
        lines += ["| " + r["id"] + " | `" + r["accepted_status"] + "` |" for r in rows]
        lines += ["", "## Other-duty attachment scope", "",
            "U01/U02/V01/V04/R01 receive limited evidence about finite admission, exact typed outcomes, declared tariff reconciliation, and explicit A1/failure provenance. U03/U04/U05/U07 retain their joint-coherence, integration, eventual-discovery, and calibration limits. U06/U08/U09 can reference the separately labeled finite transfer/chronology audit, which preserves the original comparator and supplies no causal, regret, or feedback theorem. V03 receives the bounded fixed-action checks; M01 receives no affirmative plurality advantage. Each duty’s exact accepted residual text and its additional attachment-specific limitation are recorded in the JSON.", "",
            "The distinction between interfaces is essential: V02's 20 full-law recoveries concern the separate exact expected-loss auditor; they do not make the ADD receiver or broker forecast recover a full law. C03's complete minimizer lists concern the inherited structural suite; they do not change the sublevel receiver's service or remove its accepted limits. F01 receives external audit evidence, not deployed reflection.", "",
            "## Evidence files", ""]
        for key, row in evidence.items():
            lines.append("- **" + key + "**: [" + Path(row["path"]).name + "](sandbox:" + str(REPO / row["path"]) + "), SHA-256 `" + row["sha256"] + "`.")
        lines += ["", "The existing conformance and transfer review manifests remain unchanged. The attached mapping preserves the accepted Q3/P3-H03 open position and P3-N01 assessment as historical accepted statements, without performing a new contribution review.", "",
            "**Signed:** ChatGPT (GPT-6 Astra Pro), `/root/conformance_reconstruction`. Evidence attachment only; principal clock credit **0**."]
        with (out / "attachment.md").open("x") as file:
            file.write("\n".join(lines) + "\n")
        assert binding(overlay_path) == overlay_binding
        save(out / "manifest.json", {"schema": "value_logic.p310.duty_attachment_manifest.v1",
             "contributor": AUTHOR, "created_utc": datetime.now(timezone.utc).isoformat(),
             "principal_clock_credit_seconds": 0, "source": binding(Path(__file__)),
             "accepted_overlay": overlay_binding, "evidence": evidence,
             "outputs": [binding(p) for p in sorted(out.iterdir()) if p.is_file()],
             "accepted_statuses_changed": 0, "accepted_residuals_changed": 0, "existing_files_modified": 0})
        print(json.dumps({"status": "DRAFT_SAVED", "duty_count": 21, "statuses_changed": 0,
                          "residuals_changed": 0, "attachment": binding(out / "attachment.json"),
                          "prose": binding(out / "attachment.md"), "manifest": binding(out / "manifest.json")}, sort_keys=True))
    except BaseException as error:
        save(out / "failure.json", {"status": "ATTACHMENT_BUILD_FAILURE", "type": type(error).__name__,
             "message": str(error), "traceback": traceback.format_exc(), "existing_files_modified": False,
             "principal_clock_credit_seconds": 0})
        raise


if __name__ == "__main__":
    main()
