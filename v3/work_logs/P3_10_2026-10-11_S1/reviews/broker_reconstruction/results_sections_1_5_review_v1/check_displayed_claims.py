"""Read-only arithmetic comparison of a results prose snapshot to saved JSON.

This does not import or execute any observer or scientific implementation.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OWN = HERE.parent
W = OWN.parents[1]
DOC = (HERE / "sections_1_5.observed.md").read_text()
T = json.loads((OWN / "findings_tables_A1.json").read_text())
RAW = json.loads((OWN / "attempt_A1_01/reconstructed.json").read_text())
N = json.loads((W / "numeric_observation_A1/results.json").read_text())
M = json.loads((W / "transfer_failure_observation_A1/results.json").read_text())
R = json.loads((W / "retrospective_report_observation_A1/public_bounds.json").read_text())
G = json.loads((W / "joint_report_geometry_observation_A1/public_geometry.json").read_text())
GV = json.loads((W / "joint_report_geometry_observation_A1/validation.json").read_text())
C = json.loads((W / "continuous_price_observation_A1/results.json").read_text())
CHECKS = []


def clean(s):
    return str(s).replace("**", "").replace("`", "").replace(",", "").replace("−", "-")


def check(section, name, observed, expected):
    CHECKS.append({"section": section, "claim": name, "observed": observed,
                   "expected": expected, "pass": clean(observed) == clean(expected)})


def fmt(q, places, sign=False):
    return format(float(F(*q)), ("+" if sign else "") + f".{places}f")


def table(header):
    lines = DOC.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(header)) + 2
    rows = []
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        rows.append([value.strip() for value in line.strip("|").split("|")])
    return rows


def config(family, cid):
    return next(c for c in T["all_configuration_summaries"]
                if c["family"] == family and c["configuration_id"] == cid)


def family(s):
    if s.startswith("Cheap"):
        return "cheap_null"
    if s.startswith("Mixed"):
        return "mixed"
    if s.startswith("Gate"):
        return "gate_transfer"
    raise ValueError(s)


for row in table("| Family | Selector | Equal-advice Brier"):
    c = config(family(row[0]), "value_" + row[1].lower() + "_cold")
    key = row[0] + " / " + row[1]
    for i, field in [(2, "uniform_brier_mean"), (3, "base_brier_mean")]:
        check("3.1", key + " " + field, row[i], fmt(c["means"][field], 9))
    check("3.1", key + " A2", row[4], fmt(c["uniform_minus_base_brier"], 9, True))
    label = "Yes" if c["practical_learning_effect"] else "No; adverse" if F(*c["uniform_minus_base_brier"]) < 0 else "No"
    check("3.1", key + " threshold", row[5], label)

for row in table("| Family | Selector | Exact mean terminal-error reduction"):
    p = next(p for p in T["paired_configuration_effects"] if p["family"] == family(row[0])
             and p["configuration_id"] == "value_" + row[1].lower() + "_cold" and p["relation"] == "base_id")
    key = row[0] + " / " + row[1]
    check("4.1", key + " exact delta", row[2], str(F(*p["mean_action_improvement"])))
    check("4.1", key + " decimal", row[3], fmt(p["mean_action_improvement"], 9))
    check("4.1", key + " threshold", row[4], "Yes" if p["practical_action_effect"] else "No")

for row in table("| Family | Selector | Mean cold units/request"):
    cold = config(family(row[0]), "value_" + row[1].lower() + "_cold")
    cached = config(family(row[0]), "value_" + row[1].lower() + "_cached_hashed")
    key = row[0] + " / " + row[1]
    check("4.2", key + " cold/T", row[2], fmt(cold["mean_cold_units_per_request"], 6))
    check("4.2", key + " cached/T", row[3], fmt(cached["mean_cold_units_per_request"], 6))
    ratio = F(*cached["means"]["cold_units"]) / F(*cold["means"]["cold_units"])
    check("4.2", key + " ratio", row[4], format(float(ratio), ".6f"))

for row in table("| Family | Distinct ordinary witness"):
    c = config(family(row[0]), clean(row[1]))
    check("4.3", row[0] + " W", row[2], str(F(*c["means"]["action_loss_mean"])))
    check("4.3", row[0] + " cold/T", row[3], str(F(*c["mean_cold_units_per_request"])))

for row in table("| Family and reporting path"):
    fam = family(row[0])
    if "other six" in row[0]:
        configs = [r for r in T["report_configuration_summaries"]
                   if r["family"] == fam and r["configuration_id"] != "finite_uniform_cold"]
        check("5.1", row[0] + " roster", len(configs), 6)
    else:
        cid = ("finite_" if "finite" in row[0] else "value_") + ("uniform" if "uniform" in row[0] else "tickets") + "_cold"
        configs = [r for r in T["report_configuration_summaries"] if r["family"] == fam and r["configuration_id"] == cid]
    for c in configs:
        for i, endpoint in enumerate(["F", "V", "Z"], 1):
            q = c["endpoints"][endpoint]["means"]["normalized_width_reduction"]
            check("5.1", row[0] + " / " + c["configuration_id"] + " / " + endpoint,
                  row[i], "0" if F(*q) == 0 else fmt(q, 10))

for row in table("| Family | Mean polygon/rectangle area"):
    for i, selector in [(1, "uniform"), (2, "tickets")]:
        summaries = [s for s in G["summaries"] if s["family"] == family(row[0])
                     and (selector in s["configuration_id"] or (selector == "uniform" and s["configuration_id"] == "ordinary_kernel_mirror"))]
        for s in summaries:
            check("5.3", row[0] + " / " + s["configuration_id"] + " area fraction", row[i],
                  fmt(s["mean_convex_hull_area_fraction_of_rectangle"], 9))

mixtures = [r for r in RAW["independent_per_unit_metrics"] if r["unit"]["engine"] in ["broker", "mirror"]]
checks = [
    ("2", "all broker episodes", len(RAW["independent_per_unit_metrics"]), 336),
    ("2", "all broker positions", sum(r["score"]["horizon"] for r in RAW["independent_per_unit_metrics"]), 28160),
    ("2", "mixture/live/mirror paths", len(mixtures), 126),
    ("2", "mixture positions", sum(r["score"]["horizon"] for r in mixtures), 10752),
    ("2", "numeric four-position blocks", N["counts"]["purchases"], 2688),
    ("2", "mirror episodes", sum(r["unit"]["engine"] == "mirror" for r in RAW["independent_per_unit_metrics"]), 18),
    ("2", "mirror positions", sum(r["score"]["horizon"] for r in RAW["independent_per_unit_metrics"] if r["unit"]["engine"] == "mirror"), 1536),
    ("3.1", "first-key positions", sum(r["score"]["first_occurrence"]["horizon"] for r in mixtures), 8946),
    ("3.3", "changed forecasts", N["counts"]["changed_forecasts"], 526),
    ("3.3", "changed prospective actions", N["counts"]["changed_prospective_actions"], 162),
    ("3.3", "terminal corrections", N["counts"]["corrected_terminal_actions"], 98),
    ("5.1", "report total", sum(r["planned_reports"] for r in T["report_configuration_summaries"]), 126),
    ("5.1", "report configuration cells", len(T["report_configuration_summaries"]), 21),
    ("5.1", "report endpoint cells", len(T["report_endpoint_rows"]), 63),
    ("5.1", "additional report fee", T["known_total_report_fees"], 65407686),
    ("5.3", "two-dimensional regions", sum(s["dimensions"].get("2", 0) for s in G["summaries"]), 126),
    ("5.3", "four-incompatible-corner regions", sum(s["incompatible_corner_counts"].get("4", 0) for s in G["summaries"]), 126),
    ("5.3", "validated actual targets", GV["validated_reports"], 126),
]
for row in checks:
    check(*row)
for fam, expected in [("mixed", 13655933), ("cheap_null", 3062889), ("gate_transfer", 48688864)]:
    check("5.1", fam + " report fee", T["known_total_report_fees_by_family"][fam], expected)
for endpoint, zeros, positives, practical in [("F", 118, 8, 2), ("V", 118, 8, 2), ("Z", 95, 31, 25)]:
    r = next(r for r in T["report_individual_endpoint_sign_counts"] if r["endpoint"] == endpoint and r["metric"] == "normalized_width_reduction")
    check("5.1", endpoint + " zero reports", r["counts"].get("zero", 0), zeros)
    check("5.1", endpoint + " positive reports", r["counts"].get("positive", 0), positives)
    check("5.1", endpoint + " individual practical reports", r["individual_reports_at_least_001"], practical)
regions = [r for cell in C["cells"] for r in cell["candidate_regions"]]
check("4.3", "candidate region count", len(regions), 12)
for kind in ["weak_nonnegative_region", "strict_positive_region", "practical_region_threshold_1_100"]:
    check("4.3", kind + " empty regions", sum(r[kind]["empty"] for r in regions), 12)
for selector, displays in [("uniform", ["0.73748418", "0.35601249"]), ("tickets", ["0.61910605", "0.26474164"])]:
    s = next(s for s in M["aggregates"] if s["family"] == "gate_transfer" and s["configuration_id"] == "value_" + selector + "_cold" and s["slice"] == "transfer")
    for k, observed in zip(["mean_forecast", "brier_mean"], displays):
        check("3.2", selector + " suffix " + k, observed, fmt(s["base_moments"][k], 8))
    check("3.2", selector + " truth fraction", s["base_moments"]["mean_truth"], [31, 64])
    if selector == "uniform":
        for k, observed in [("squared_mean_bias", "-0.0689171173"), ("forecast_variance", "-0.0037935725"), ("negative_twice_covariance", "-0.0220170754")]:
            check("3.2", "uniform suffix " + k, observed, fmt(s["a2_contributions"][k], 10))

retro = next(s for s in R["summaries"] if s["family"] == "gate_transfer" and s["configuration_id"] == "value_uniform_cold")
retro_gaps = {}
for endpoint, display in [("F", "0.00136358"), ("V", "0.00136358"), ("Z", "0.04004628")]:
    q = -F(*retro["endpoints"][endpoint]["means_per_scheduled_horizon"]["frozen_width_minus_end_key_width"])
    check("5.2", endpoint + " ALREADY-normalized new-minus-delivered width magnitude", display, format(float(q), ".8f"))
    retro_gaps[endpoint] = [q.numerator, q.denominator]

out = {"created_utc": datetime.now(timezone.utc).isoformat(), "scope": "Prose/table reconciliation to saved exact records only; no scientific execution",
       "source_snapshot_sha256": hashlib.sha256((HERE / "sections_1_5.observed.md").read_bytes()).hexdigest(),
       "checks": CHECKS, "check_count": len(CHECKS),
       "mismatch_count": sum(not r["pass"] for r in CHECKS),
       "retrospective_width_values_are_already_normalized": retro_gaps,
       "editorial_findings_separate": ["Section 5.2 repeats /H after already-normalized values", "Section 4.3 first paragraph should explicitly say candidate minus ordinary", "Section 3.3 should distinguish Bernoulli-parameter variance from temporal variance"],
       "principal_research_minutes_claimed": 0}
with (HERE / "displayed_claim_checks.json").open("x") as handle:
    json.dump(out, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps({"check_count": len(CHECKS), "mismatch_count": out["mismatch_count"],
                  "mismatches": [r for r in CHECKS if not r["pass"]]}, indent=2))
