"""Saved-before-calculation analytic q=1/2 diagnostic; no scientific rerun.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. DEVELOPMENT, zero principal credit.
For binary y, (1/2-y)^2=1/4; a fair binary terminal action errs with
probability 1/2. These formulae require no query calls or evaluator labels.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / "v3/work_logs/R_P3_B_A_2026-10-09_S1/development/allocation_comparison"
RUN = OUT / "run_001"
PLAN = OUT / "postrun_null_diagnostic_plan_v1.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def row(kind, arm, transferred_units=None):
    t, b = arm["horizon"], arm["block_size"]
    quota = t // b
    units = arm["resource_units"]["cold_total"]
    evaluation = arm["evaluation"]
    null_brier, null_terminal = F(t, 4), F(t - quota, 2)
    actual_brier = F(evaluation["immutable_issued_brier"])
    actual_terminal = F(evaluation["conditional_expected_terminal_01_loss"])
    result = {
        "kind": kind, "original_arm": arm["name"], "horizon": t, "block_size": b, "quota": quota,
        "null_issued_probability": F(1, 2), "null_immutable_issued_brier": null_brier,
        "null_prospective_conditional_action_loss": F(t, 2),
        "null_same_selector_terminal_conditional_action_loss": null_terminal,
        "observed_issued_brier": actual_brier, "observed_brier_minus_null": actual_brier - null_brier,
        "observed_selector_conditional_terminal_loss": actual_terminal,
        "observed_conditional_terminal_minus_null": actual_terminal - null_terminal,
        "same_complete_observed_resource_invoice_units": units,
        "identical_observed_invoice_null_price_totals": {
            str(price): price * null_terminal + F(units, 1000) for price in (1, 100)},
        "counterfactual_boundary": "Analytic output substitution with the original selected receipts, internal state, allocation, purchases and COMPLETE executed resource invoice retained. No newly deployed null controller or cheaper-method claim.",
    }
    if transferred_units is not None:
        result["uniform_v1_2_registry_only_transfer"] = {
            "kind": "Derived from the separately verified guard-only source transfer; not a new execution.",
            "derived_current_cold_units": transferred_units,
            "registry_only_delta": transferred_units - units,
            "identical_transferred_invoice_null_price_totals": {
                str(price): price * null_terminal + F(transferred_units, 1000) for price in (1, 100)},
        }
    return result


def main():
    plan = read(PLAN)
    assert plan["saved_before_diagnostic_rows"] is True
    assert digest(PLAN) == "d13da1472e38fe1ab4bb91b39157fbf2224c968a2bea3f2831f0577a34be689f"
    result_path = RUN / "result.json"
    assert digest(result_path) == plan["source_result"]["sha256"]
    result = read(result_path)
    prior_path = RUN / "sources/prior_uniform_result.json"
    prior = read(prior_path)
    rows = []
    for adaptive in result["learner_arms"]:
        rows.append(row("adaptive_observed_core_v1_2", adaptive))
        comparison = adaptive["prior_same_tape_comparison"]["uniform_fixed_state"]
        uniform = next(r for r in prior["learner_arms"] if r["name"] == comparison["arm"])
        rows.append(row("prior_uniform_observed_core_v1_1", uniform,
                        comparison["derived_current_v1_2_cold_units"]))
    assert len(rows) == 6 and all(r["observed_brier_minus_null"] > 0 for r in rows)
    output = {
        "schema": "value_logic.analytic_null_diagnostic.v1", "status": "PASS", "stage": "DEVELOPMENT",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "prospective_postrun_plan_sha256": digest(PLAN),
        "source_hashes": {str(p.relative_to(ROOT)): digest(p) for p in
                          (result_path, prior_path, PLAN, Path(__file__))},
        "position_in_protocol": "Requested after the three planned adaptive arms completed; the diagnostic note was saved before these complete rows were calculated. This is outside the planned run grid and is not an added seed/procedure run.",
        "proof": "Every binary label y satisfies (1/2-y)^2=1/4. Each independent fair binary action has error probability 1/2 for either y. Retaining the same m exact purchases gives zero purchased error and (T-m)/2 conditional expected unpurchased errors.",
        "label_calls": 0, "learner_calls": 0, "service_calls": 0, "random_draws": 0,
        "fee_scope": "All quoted fees retain an existing path's complete invoice. They are not unconditional expected fee estimates, and no reduced resource bill for a separately deployed null method is inferred.",
        "conclusion": "All six observed issued Brier values exceed their exact no-information T/4 baseline. Lower adaptive Brier than uniform in these traces is therefore not forecast superiority over this analytic null. The terminal-action comparison is a separate, same-purchase-path conditional diagnostic.",
        "rows": rows, "principal_clock_credit_ns": 0,
    }
    path = OUT / "postrun_null_diagnostic_v1.json"
    with path.open("x") as stream:
        stream.write(json.dumps(output, indent=2, default=str) + "\n")
    print(json.dumps({"status": "PASS", "diagnostic_rows": len(rows), "all_issued_brier_above_null": True,
                      "output_sha256": digest(path), "new_scientific_runs": 0}))


if __name__ == "__main__":
    main()
