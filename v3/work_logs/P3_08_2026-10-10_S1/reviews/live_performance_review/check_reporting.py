"""Independent source-bound reporter checks; P3-08 DEVELOPMENT only.

ChatGPT (GPT-6 Astra Pro), same-model nonblind integration reviewer.
Private Fraction/truth calculations run only after the owned public episode
and its deployed report have been saved. They are evaluator work, not part
of the reporter's information or tariff. No coverage is estimated from seeds.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
import traceback

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "source_snapshot/v3/experiments"))
import p308_common as M
import p308_broker as B
import p308_cnf as S
import p308_reporting as R

C = M.C


def require(value, message):
    if not value:
        raise AssertionError(message)


def frac(pair):
    return F(pair[0], pair[1])


def rootceil(value):
    root = math.isqrt(value)
    return root if root * root == value else root + 1


def queries(count=8, repeated=False, source=S.SOURCE_VERSION):
    forms = [((),), ((),), ((1,),), ((1,),), ((),),
             ((1,),), ((-1,), (1,)), ((-2, 1), (2,))]
    return tuple(S.make_query(f"report-review-{i}", 2,
                              forms[0] if repeated else forms[i % len(forms)],
                              source_version=source)
                 for i in range(count))


def seal(name, episode, report):
    data = json.dumps({"stage": "DEVELOPMENT", "episode": episode,
                       "report": report}, indent=2).encode() + b"\n"
    path = HERE / (name + "_owned_record.json")
    path.write_bytes(data)
    return {"path": path.name, "sha256": hashlib.sha256(data).hexdigest()}


def truth(query):
    # Deliberately separate complete truth evaluator, used only after sealing.
    return int(any(all(any((lit > 0) == bool(bits[abs(lit) - 1])
                           for lit in clause)
                       for clause in query.clauses)
                   for bits in itertools.product((0, 1), repeat=query.variables)))


def audit(episode, report, tape):
    require(episode["status"] == report["status"] == "success", "Expected complete episode/report")
    rows = episode["trace"]
    t, b = len(rows), episode["contract"]["block_size"]
    m = t // b
    q = [frac(row["base_q"]) for row in rows]
    live = [frac(row["emitted_q"]) for row in rows]
    y = [truth(query) for query in tape]
    selected = [row["selected"] for row in rows]
    hard = [row["hard_before"] == "checked" for row in rows]
    pi = [frac(row["propensity"]) for row in rows]
    d = [qq + (1 - 2 * qq) * yy for qq, yy in zip(q, y)]
    dlive = [qq + (1 - 2 * qq) * yy for qq, yy in zip(live, y)]
    base_f = sum(((qq - yy) ** 2 for qq, yy in zip(q, y)), F())
    live_f = sum(((qq - yy) ** 2 for qq, yy in zip(live, y)), F())
    base_v = sum((d[i] for i in range(t) if not selected[i]), F())
    live_v = sum((dlive[i] for i in range(t) if not selected[i]), F())
    base_z = sum(row["base_terminal"] != yy for row, yy in zip(rows, y))
    live_z = sum(row["terminal_action"] != yy for row, yy in zip(rows, y))
    delta_f = sum(((q[i] - y[i]) ** 2 for i in range(t) if hard[i]), F())
    delta_v = sum((d[i] for i in range(t) if hard[i] and not selected[i]), F())
    delta_z = sum(rows[i]["base_action"] != y[i]
                  for i in range(t) if hard[i] and not selected[i])
    require(base_f - delta_f == live_f and base_v - delta_v == live_v
            and base_z - delta_z == live_z, "Exact correction identity failed")
    base_u = F(t - m, 2) + sum(((1 / pi[i] - 1) * (d[i] - F(1, 2))
                                for i in range(t) if selected[i]), F())
    base_a = F(t, 2) - sum((qq * (1 - qq) for qq in q), F())
    base_a += sum(((d[i] - F(1, 2)) / pi[i]
                   for i in range(t) if selected[i]), F())
    live_u, live_a = base_u - delta_v, base_a - delta_f
    require(base_v - base_u == base_f - base_a == live_v - live_u == live_f - live_a,
            "Shared residual was not retained")
    widths = [max(abs(1 - 2 * q[i]) / pi[i] for i in range(start, start + b))
              for start in range(0, t, b)]
    Q = sum((width * width for width in widths), F())
    Sbound = b if episode["contract"]["selector"] == "uniform" else 2 * b
    rate = Sbound * rootceil(2 * m)
    radius = Q / rate + F(5 * rate, 8)
    n_live = sum(not selected[i] and not hard[i] for i in range(t))
    action_radius = rootceil((5 * n_live + 1) // 2)
    for name, actual, expected in (
        ("base V center", frac(report["base_centers"]["V"]), base_u),
        ("base F center", frac(report["base_centers"]["F"]), base_a),
        ("live V center", frac(report["live_centers"]["V"]), live_u),
        ("live F center", frac(report["live_centers"]["F"]), live_a),
        ("Delta F", frac(report["corrections"]["F"]), delta_f),
        ("Delta V", frac(report["corrections"]["V"]), delta_v),
        ("Delta Z", report["corrections"]["Z"], delta_z),
        ("Q", frac(report["Q"]), Q),
        ("R", report["R"], rate),
        ("sampling radius", frac(report["sampling_radius"]), radius),
        ("action radius", report["action_radius"], action_radius),
        ("live action count", report["n_live"], n_live),
    ):
        require(actual == expected, name + " disagrees with independent Fraction calculation")
    vlow = sum((min(q[i], 1 - q[i]) for i in range(t)
                if not selected[i] and not hard[i]), F())
    vhigh = sum((max(q[i], 1 - q[i]) for i in range(t)
                 if not selected[i] and not hard[i]), F())
    flow, fhigh = F(), F()
    for i in range(t):
        if hard[i] or selected[i]:
            flow += (live[i] - y[i]) ** 2
            fhigh += (live[i] - y[i]) ** 2
        else:
            flow += min(live[i] ** 2, (1 - live[i]) ** 2)
            fhigh += max(live[i] ** 2, (1 - live[i]) ** 2)
    envelopes = {"V": (vlow, vhigh), "F": (flow, fhigh), "Z": (F(), F(n_live))}
    require(vlow <= live_v <= vhigh and flow <= live_f <= fhigh
            and 0 <= live_z <= n_live, "Deterministic envelope failed")
    if n_live:
        intervals = {"V": (max(live_u - radius, vlow), min(live_u + radius, vhigh)),
                     "F": (max(live_a - radius, flow), min(live_a + radius, fhigh)),
                     "Z": (max(live_u - radius - action_radius, F()),
                           min(live_u + radius + action_radius, F(n_live)))}
    else:
        require(flow == fhigh == live_f and live_v == live_z == 0, "Exact all-known exception failed")
        intervals = {"V": (F(), F()), "F": (live_f, live_f), "Z": (F(), F())}
    for name in ("V", "F", "Z"):
        require(tuple(map(frac, report["deterministic_envelopes"][name])) == envelopes[name],
                name + " deterministic envelope differs")
        row = report["intervals"][name]
        low, high = intervals[name]
        require((frac(row["lower"]), frac(row["upper"])) == (low, high),
                name + " endpoints differ")
        require(row["confidence_conflict"] == (low > high), "Conflict flag differs")
    for owner in (episode, report):
        meter = owner["meter"]
        require(meter["total"] == sum(meter["by_category"].values())
                == sum(op["units"] for op in meter["operations"]), "Meter does not reconcile")
    require(report["development_seed_is_coverage_evidence"] is False,
            "A deterministic seed was promoted to coverage evidence")
    return {"F0": str(base_f), "F1": str(live_f), "V0": str(base_v), "V1": str(live_v),
            "Z0": base_z, "Z1": live_z, "Delta_F": str(delta_f), "Delta_V": str(delta_v),
            "Delta_Z": delta_z, "n_live": n_live, "Q": str(Q), "R": rate,
            "rho": str(radius), "action_radius": action_radius,
            "broker_paid": episode["meter"]["total"], "report_paid": report["meter"]["total"],
            "peak_reporting_bits": report["peak_integer_bits"]}


def fraction_algebra():
    outcomes = []
    for selector in ("uniform", "tickets"):
        for precision in (4, 32):
            tape = queries()
            contract = B.Contract(8, 4, 6, precision, precision, selector=selector)
            episode = B.execute(S, tape, contract, seed=308775)
            report = R.report_owned_episode(S, episode)
            artifact = seal(f"algebra_{selector}_{precision}", episode, report)
            result = audit(episode, report, tape)
            require(report["confidence_eligible"] is True, "Full interface/funding eligibility missing")
            outcomes.append(dict(selector=selector, precision=precision, artifact=artifact, **result))
    return outcomes


def source_label_limit():
    tape = queries(4, repeated=True, source="s" * 128)
    contract = B.Contract(4, 2, 6, 4, 4)
    episode = B.execute(S, tape, contract, seed=308775)
    report = R.report_owned_episode(S, episode)
    artifact = seal("source_128", episode, report)
    result = audit(episode, report, tape)
    return dict(source_length=128, artifact=artifact, **result)


def exact_all_known():
    tape = queries(2, repeated=True)
    episode = B.execute(S, tape, B.Contract(2, 2, 6, 4, 4), seed=308775)
    report = R.report_owned_episode(S, episode)
    artifact = seal("exact_all_known", episode, report)
    result = audit(episode, report, tape)
    require(episode["blocks"][0]["selected"] == 0, "Prospectively selected seed no longer selects first")
    require(report["exact_all_remaining_known"] and report["n_live"] == 0,
            "First purchase did not make the remaining repeated query exact")
    require(frac(report["intervals"]["F"]["lower"]) > 0,
            "Selected issued Brier loss was retroactively erased")
    return dict(artifact=artifact, **result)


def restricted_reporting_funding():
    tape = queries(4, repeated=True)
    episode = B.execute(S, tape, B.Contract(4, 2, 6, 4, 4), seed=308775)
    full = R.report_owned_episode(S, episode)
    limit = full["meter"]["total"]
    small = R.report_owned_episode(S, episode, unit_limit=limit)
    denied = R.report_owned_episode(S, episode, unit_limit=0)
    artifact = seal("restricted_reporting", episode, small)
    result = audit(episode, small, tape)
    require(limit < R.REPORT_FUNDING_CAP and small["status"] == "success",
            "Chosen limited reporting calculation did not complete")
    require(not small["confidence_eligible"] and not small["all_path_reporting_funded"],
            "Completed limited report was promoted to all-path confidence eligibility")
    require(denied["status"] == "failed" and not denied["confidence_eligible"]
            and denied["meter"]["total"] == 0, "Zero report budget was not a typed unfunded failure")
    (HERE / "report_zero_budget.json").write_text(json.dumps(denied, indent=2) + "\n")
    return dict(limit=limit, report_cap=R.REPORT_FUNDING_CAP,
                failed_report=denied["failure_detail"], artifact=artifact, **result)


def restricted_broker_funding():
    tape = queries(4, repeated=True)
    contract = B.Contract(4, 2, 6, 4, 4)
    full = B.execute(S, tape, contract, seed=308775)
    limit = full["meter"]["total"] + max(S.service_cap(query, "enumeration") for query in tape)
    episode = B.execute(S, tape, contract, seed=308775, unit_limit=limit)
    report = R.report_owned_episode(S, episode)
    artifact = seal("restricted_broker", episode, report)
    result = audit(episode, report, tape)
    require(limit < full["funded_cap"] and episode["status"] == "success"
            and not episode["all_path_funded"], "Restricted broker classification is incorrect")
    require(report["all_path_reporting_funded"] and not report["confidence_eligible"],
            "Funded reporting erased the broker's missing all-path premise")
    return dict(limit=limit, broker_cap=full["funded_cap"], artifact=artifact, **result)


def chronology_rejection():
    tape = queries(2, repeated=True)
    episode = B.execute(S, tape, B.Contract(2, 2, 6, 4, 4), seed=308775)
    perturbed = deepcopy(episode)
    row = perturbed["trace"][0]
    require(row["hard_before"] == "unresolved", "Test requires no earlier hard warrant")
    row["hard_before"] = "checked"
    row["emitted_q"] = [0, row["emitted_q"][1]]
    row["prospective_action"] = 0
    report = R.report_owned_episode(S, perturbed)
    artifact = seal("chronology_perturbed", perturbed, report)
    require(report["status"] == "failed" and not report["confidence_eligible"],
            "Later selected receipt was incorrectly accepted as a pre-issue warrant")
    require("earlier current owned receipt" in report["failure_detail"],
            "Perturbation did not fail at the chronology boundary")
    return {"artifact": artifact, "failure_detail": report["failure_detail"],
            "paid": report["meter"]["total"],
            "scope": "Perturbed trusted-record validation check; not an external authentication test"}


def main():
    started = datetime.now(timezone.utc).isoformat()
    results = []
    for case in (fraction_algebra, source_label_limit, exact_all_known,
                 restricted_reporting_funding, restricted_broker_funding,
                 chronology_rejection):
        try:
            results.append({"case": case.__name__, "status": "PASS", "detail": case()})
        except Exception as error:
            results.append({"case": case.__name__, "status": "FAIL",
                            "exception": type(error).__name__, "message": str(error),
                            "traceback": traceback.format_exc()})
    output = {"stage": "DEVELOPMENT", "started_utc": started,
              "finished_utc": datetime.now(timezone.utc).isoformat(),
              "source_manifest": "plan.json", "script": Path(__file__).name,
              "principal_clock_credit_seconds": 0,
              "passed": sum(row["status"] == "PASS" for row in results),
              "failed": sum(row["status"] == "FAIL" for row in results),
              "results": results}
    (HERE / "results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({key: output[key] for key in ("stage", "passed", "failed")}))
    for row in results:
        print(row["case"], row["status"], row.get("message", ""))
    raise SystemExit(int(output["failed"] != 0))


if __name__ == "__main__":
    main()
