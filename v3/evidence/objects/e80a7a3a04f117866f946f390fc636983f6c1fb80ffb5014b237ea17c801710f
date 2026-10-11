"""Readable exact witnesses for the already computed fixed-record price regions.

ChatGPT (GPT-6 Astra Pro), principal /root, 2026-10-11. No policy is run.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

W = Path(__file__).resolve().parent
SOURCE = W / "forecast_action_price_observation_A1/results.json"
OUT = W / "forecast_action_price_readable_A1"


def f(pair):
    return F(*pair)


def encode(v):
    if isinstance(v, F):
        return [v.numerator, v.denominator]
    if isinstance(v, dict):
        return {k: encode(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [encode(x) for x in v]
    return v


def main():
    OUT.mkdir(exist_ok=False)
    j = json.loads(SOURCE.read_text())
    assert j["status"] == "PASS_SCOPED" and len(j["cases"]) == 12
    results = []
    for r in j["cases"]:
        family, name = r["family"], r["candidate_id"]
        cv = {k: f(r["candidate"][k]) for k in ["W", "C", "B"]}
        oo = {o["id"]: {k: f(o[k]) for k in ["W", "C", "B"]} for o in r["ordinary"]}
        result = {"family": family, "candidate_id": name, "candidate": cv}
        if r["feasible"]:
            lam, mu = (F(1, 10000), F(33)) if family == "mixed" else (F(1, 100000), F(40))
            kc = cv["W"]+lam*cv["C"]+mu*cv["B"]
            scores = {i: o["W"]+lam*o["C"]+mu*o["B"] for i, o in oo.items()}
            best = min(scores.values())
            assert kc < best
            result.update(kind="strict illustrative point", lambda_value=lam, mu_value=mu,
                          candidate_K=kc, minimum_ordinary_K=best,
                          ordinary_minimizers=[i for i, score in scores.items() if score == best],
                          minimum_strict_margin=best-kc,
                          all_19_ordinary_scores=scores)
        else:
            if family == "cheap_null" and "tickets" in name:
                weights = {"exact_cache_hashed": F(1)}
            elif family == "cheap_null" and "cached" in name:
                weights = {"ordinary_combo_hashed_p1_1000": F(1)}
            elif family == "cheap_null":
                weights = {"probability_cost": F(1, 2), "ordinary_combo_hashed_p1_10000": F(1, 2)}
            elif family == "mixed" and "tickets" in name:
                weights = {"finite_uniform_cold": F(1)}
            elif family == "mixed":
                weights = {"finite_uniform_cold": F(9, 10), "ordinary_combo_hashed_p1_10000": F(1, 10)}
            else:
                weights = {"proof_dpll_fallback1": F(2, 3), "probability_cost": F(1, 3)}
            assert sum(weights.values()) == 1 and all(w > 0 for w in weights.values())
            mixture = {k: sum(w*oo[i][k] for i, w in weights.items()) for k in ["W", "C", "B"]}
            gaps = {k: cv[k]-mixture[k] for k in ["W", "C", "B"]}
            assert all(v > 0 for v in gaps.values())
            result.update(kind="strict three-coordinate convex certificate", weights=weights,
                          combined_coordinates=mixture, candidate_minus_combination=gaps,
                          paid_randomized_controller_executed=False)
        results.append(result)
    obj = {"schema": "P3-10-fixed-price-readable-witnesses-v1", "status": "PASS_SCOPED",
           "contributor": "ChatGPT (GPT-6 Astra Pro), principal /root",
           "signed_utc": datetime.now(timezone.utc).isoformat(),
           "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
           "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
           "source_scope": "Three nonempty and nine empty regions already computed before selecting these readable certificates",
           "new_paid_runs": 0, "cases": results,
           "fixed_primary_endpoint_or_global_economic_gate_changed": False}
    (OUT/"results.json").write_text(json.dumps(encode(obj), indent=2)+"\n")
    lines = ["# Readable certificates for the forecast/action price sensitivity", "",
        "Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.", "",
        "The initial [exact region reconstruction](../forecast_action_price_observation_A1/results.json)",
        "already found three nonempty and nine empty regions for `K=W+lambda*C+mu*B`.",
        "These subsequently selected small-rational examples make its conclusion",
        "readable. They are exact checked certificates, not additional experiments,",
        "a new practical threshold or a changed acquisition policy. Every comparison",
        "uses all 19 distinct ordinary configurations at the same symmetric stakes.", "",
        "## Three strict illustrative points", "",
        "| Family | Candidate | lambda | mu | Candidate K | Best ordinary K | Strict gap | Best ordinary |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in results:
        if r["kind"] == "strict illustrative point":
            lines += [f"| {r['family']} | {r['candidate_id']} | {r['lambda_value']} | {r['mu_value']} | {float(r['candidate_K']):.10f} | {float(r['minimum_ordinary_K']):.10f} | {float(r['minimum_strict_margin']):.10f} | {', '.join(r['ordinary_minimizers'])} |"]
    lines += ["", "The exact rational scores and all ordinary ties are in [results.json](results.json).",
        "A small positive gap here is a descriptive strict inequality; the frozen",
        "0.01 practical convention is not reassigned to this newly weighted score.", "",
        "## Nine empty regions have simple convex certificates", "",
        "| Family | Candidate | Mathematical combination of ordinary records | W gap | C gap | B gap |",
        "| --- | --- | --- | --- | --- | --- |"]
    for r in results:
        if r["kind"] != "strict illustrative point":
            combination = " + ".join(f"{w} {i}" for i, w in r["weights"].items())
            gaps = r["candidate_minus_combination"]
            lines += [f"| {r['family']} | {r['candidate_id']} | {combination} | {float(gaps['W']):.10f} | {float(gaps['C']):.10f} | {float(gaps['B']):.10f} |"]
    lines += ["", "Every displayed gap is candidate minus combination and is **strictly positive**.",
        "For any fixed nonnegative lambda and mu, the best component of a combination",
        "has score no greater than its weighted mean, which is strictly lower than",
        "the candidate. This certifies an ordinary-catalogue winner for every price",
        "pair. It does not deploy a randomized meta-controller or claim that such a",
        "controller, with unmeasured selection and interface costs, was run for free.", "",
        "## What the new scalarization changes", "",
        "The frozen objective assigns no extra price to issued Brier quality; its",
        "mu=0 boundary still rejects every candidate. A positive mu values an",
        "additional feature of the existing public service. It can expose a",
        "tradeoff that the original terminal objective does not price, but cannot",
        "repair that original endpoint or its unknown outer-attempt cost gate.", "",
        "The two gate ticketed candidates have identical W and B; cold has lower C.",
        "Thus at positive lambda the cold candidate beats its cached counterpart,",
        "even where both beat the distinct ordinary catalogue. The recorded mirror",
        "and the ordinary identical-kernel interpretation also remain separate:",
        "no strict advantage over an unrestricted ordinary realization follows.", "",
        "Optional paid report fees are excluded because the report is a further",
        "unequal service. The issued forecast was already produced within the",
        "terminal episode. Changing either score weight in a deployed controller",
        "could change the entire trajectory; this calculation does not do so.", ""]
    (OUT/"interpretation.md").write_text("\n".join(lines))
    print(json.dumps({"status": obj["status"], "strict_examples": 3, "strict_convex_certificates": 9,
                      "results_sha256": sha256((OUT/'results.json').read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
