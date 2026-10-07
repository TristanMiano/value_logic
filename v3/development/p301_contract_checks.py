"""Exact finite checks for P3-01 development examples, not a frozen evaluation.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-07.
Run from repository root with --out a new, explicitly named attempt file.
Completed groups and failures are durably saved; an existing attempt is refused.
"""
from argparse import ArgumentParser
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import platform
import sys
import time
import traceback


ASSERTIONS = 0


def check(condition, message):
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(message)


def equal(actual, expected, message):
    check(actual == expected, f"{message}: {actual!r} != {expected!r}")


def serial(value):
    if isinstance(value, F):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def dot(p, x):
    return sum((a * b for a, b in zip(p, x, strict=True)), F(0))


def finite_fragment():
    all_rows = list(product((0, 1), repeat=3))
    initial = [v for v in all_rows if v[1] == 1 - v[0]]
    resolved_chi = [v for v in initial if v[2] == 1]
    resolved_phi = [v for v in resolved_chi if v[0] == 1]
    equal((len(initial), len(resolved_chi), len(resolved_phi)), (4, 2, 1), "fragment counts")
    equal(resolved_phi, [(1, 0, 1)], "fully resolved row")
    for rows in (initial, resolved_chi, resolved_phi):
        means = [F(sum(v[j] for v in rows), len(rows)) for j in range(3)]
        equal(means[0] + means[1], F(1), "known complementary relation")
    equal(F(sum(v[2] for v in initial), len(initial)), F(1, 2), "initial chi mean")
    for actual in resolved_chi:
        check(actual in initial, "a new true constraint preserves the actual assignment")
    inconsistent = [v for v in resolved_chi if v[2] == 0]
    equal(inconsistent, [], "conflicting hard constraints")
    prefix = [v for v in initial if v[2] == 0]
    check(max(v[2] for v in prefix) < max(v[2] for v in initial), "partial enumeration can understate a bound")
    return {"examples": ["EX01"], "initial": initial, "after_chi": resolved_chi,
            "after_phi": resolved_phi, "conflict_status": "INCONSISTENT_FRAGMENT",
            "partial_enumeration_status": "BOUND_NOT_CERTIFIED"}


def binary_bridge():
    recovered = {k: F(1) - F(3, k) for k in (10, 100)}
    equal(recovered, {10: F(7, 10), 100: F(97, 100)}, "known penalty inversion")
    for k, p in recovered.items():
        equal(k * (1 - p), F(3), "same cost, different belief")
    equal(F(1) + 10 * (1 - F(4, 5)), F(3), "additive charge confounding")
    return {"examples": ["EX02"], "cost": F(3), "success_probabilities": recovered}


def joint_decision():
    laws = {"same": [(0, 0), (1, 1)], "opposite": [(0, 1), (1, 0)]}
    result = {}
    for name, rows in laws.items():
        means = [F(sum(v[j] for v in rows), 2) for j in range(2)]
        mean_max = F(sum(max(v) for v in rows), 2)
        mean_sum = F(sum(sum(v) for v in rows), 2)
        equal(means, [F(1, 2), F(1, 2)], "marginal agreement")
        equal(mean_sum, F(1), "sum is identified")
        result[name] = {"marginals": means, "mean_max": mean_max,
                        "selected": "joint_action" if mean_max < F(3, 4) else "fallback"}
    equal(result["same"]["mean_max"], F(1, 2), "same max")
    equal(result["opposite"]["mean_max"], F(1), "opposite max")
    equal([v["selected"] for v in result.values()], ["joint_action", "fallback"], "decision reverses")
    return {"examples": ["EX03"], "laws": result, "fallback": F(3, 4)}


def fallible_models():
    rows = []
    for a in (F(1, 10), F(1, 2)):
        error = max(abs((x + x**3) - x) for x in (-a, a))
        cheap, accurate = error + F(1, 1000), F(8, 1000)
        equal(error, a**3, "inherited approximation fixture")
        rows.append({"a": a, "error": error, "cheap": cheap, "accurate": accurate})
    equal(rows[0]["cheap"], F(2, 1000), "small-domain cheap loss")
    equal(rows[1]["cheap"], F(126, 1000), "large-domain cheap loss")
    check(rows[0]["cheap"] < rows[0]["accurate"], "cheap wins small domain")
    check(rows[1]["cheap"] > rows[1]["accurate"], "accurate wins large domain")
    return {"examples": ["EX04"], "inherited_fixture": True, "rows": rows}


def cost(a, b):
    return 2 + a - 2 * b


def operation_cases():
    all_rows = list(product((0, 1), repeat=2))
    conditioned = [v for v in all_rows if v[0] == 0 and v[1] == 0 and v[0] == 1]
    equal(conditioned, [], "conditioning contradicts the retained actual equations")
    vals = {"actual": cost(0, 0), "token": cost(1, 0),
            "shared_replacement": cost(1, 1), "actor_only": cost(1, 0)}
    equal(vals, {"actual": 2, "token": 3, "shared_replacement": 1, "actor_only": 3}, "operation table")
    observations = []
    interventions = []
    for u in (0, 1):
        direct = (u, u, cost(u, u))
        common = (u, u, cost(u, u))
        equal(direct, common, "pointwise observational identity implies every-law identity")
        observations.append({"u": u, "direct": direct, "common": common})
        interventions.append({"u": u, "direct_A1": cost(1, 1), "common_A1": cost(1, u)})
    equal((interventions[0]["direct_A1"], interventions[0]["common_A1"]), (1, 3), "intervention separation")
    return {"examples": ["EX05", "EX06A"], "operations": vals,
            "conditioning_status": "CERTIFIED_EMPTY", "observations": observations,
            "interventions": interventions}


def repairs():
    predicates = {"a0": lambda a, b: a == 0, "b0": lambda a, b: b == 0,
                  "same": lambda a, b: a == b}
    presentations = {"base": ["a0", "b0", "same"],
                     "duplicate_same": ["a0", "b0", "same", "same"],
                     "duplicate_b0": ["a0", "b0", "same", "b0"]}
    report = {}
    subsets = 0
    for name, records in presentations.items():
        original = [v for v in product((0, 1), repeat=2) if all(predicates[r](*v) for r in records)]
        equal(original, [(0, 0)], "same original model set")
        feasible = []
        for count in range(len(records) + 1):
            for deleted in combinations(range(len(records)), count):
                subsets += 1
                survivors = [r for i, r in enumerate(records) if i not in deleted]
                states = [v for v in product((0, 1), repeat=2)
                          if v[0] == 1 and all(predicates[r](*v) for r in survivors)]
                if states:
                    feasible.append({"deleted_indices": deleted, "edit_cost": count,
                                     "states": states, "losses": sorted({cost(*v) for v in states})})
        minimum = min(r["edit_cost"] for r in feasible)
        optimal = [r for r in feasible if r["edit_cost"] == minimum]
        losses = sorted({v for r in optimal for v in r["losses"]})
        report[name] = {"feasible": feasible, "minimum": minimum, "optimal": optimal,
                        "optimal_loss_set": losses}
        equal(minimum, 2, "minimum edit count")
    equal(subsets, 40, "all deletion subsets")
    equal(report["base"]["optimal_loss_set"], [1, 3], "tied repairs")
    equal(report["duplicate_same"]["optimal_loss_set"], [1], "duplicating shared relation selects one repair")
    equal(report["duplicate_b0"]["optimal_loss_set"], [3], "duplicating fixed token selects the other")
    return {"examples": ["EX06B", "EX09"], "subsets": subsets,
            "assignments_per_subset": 4, "presentations": report}


def paid_reasoning():
    simple = {k: {"guess": F(k, 2), "resolve": F(2)} for k in (1, 10)}
    check(simple[10]["resolve"] < simple[10]["guess"], "high stakes favor compute")
    check(simple[1]["resolve"] > simple[1]["guess"], "low stakes favor stopping")
    states = list(product((0, 1), repeat=2))
    strategies = []
    for observed in ((), (0,), (1,), (0, 1)):
        cells = {}
        for state in states:
            cells.setdefault(tuple(state[j] for j in observed), []).append(state[0] ^ state[1])
        error_mass = sum((F(min(ys.count(0), ys.count(1)), 4) for ys in cells.values()), F(0))
        total = len(observed) + 10 * error_mass
        strategies.append({"observed_coordinates": observed, "error_mass": error_mass, "total_cost": total})
    equal([r["total_cost"] for r in strategies], [F(5), F(6), F(6), F(2)], "complementary information")
    equal(min(strategies, key=lambda r: r["total_cost"])["observed_coordinates"], (0, 1), "best two-read strategy")
    return {"examples": ["EX07"], "simple": simple, "xor_strategies": strategies,
            "myopic_loss": F(5), "best_catalogue_loss": F(2)}


def predictions_and_decisions():
    squared = lambda p, y: (p - y)**2
    sole_expert = F(1, 2)
    equal(squared(sole_expert, 1), F(1, 4), "sole expert score")
    before = (F(49, 100), F(51, 100))
    scores = [squared(p, 1) for p in before]
    equal(scores[0] - scores[1], F(1, 50), "score difference across threshold")
    no_change = [squared(p, 1) for p in (F(3, 5), F(9, 10))]
    equal(no_change, [F(4, 25), F(1, 100)], "score improvement without action change")
    epsilon = F(1, 4)
    grid = [F(i, 4) for i in range(5)]
    offsets = [-epsilon, F(0), epsilon]
    count, max_regret = 0, F(0)
    for actual in product(grid, repeat=3):
        for errors in product(offsets, repeat=3):
            estimated = [a + e for a, e in zip(actual, errors, strict=True)]
            selected = min(range(3), key=lambda i: estimated[i])
            regret = actual[selected] - min(actual)
            check(regret <= 2 * epsilon, "uniform cost error bridge")
            max_regret = max(max_regret, regret)
            count += 1
    equal(count, 3375, "finite bridge enumeration count")
    equal(max_regret, 2 * epsilon, "bridge is attained on this grid")
    return {"examples": ["EX08"], "sole_expert_regret": F(0), "sole_expert_bias": F(-1, 2),
            "crossing_scores": scores, "same_action_scores": no_change,
            "uniform_bound_cases": count, "epsilon": epsilon, "maximum_regret": max_regret}


def withdrawal_and_prices():
    old = max(x - F(1, 2) for x in (F(0), F(1, 4)))
    new = max(x - F(1, 2) for x in (F(0), F(1)))
    equal((old, new), (F(-1, 4), F(1, 2)), "withdrawal changes the bound")
    p = F(7, 10)
    price_costs = [k * (1 - p) for k in (10, 20)]
    equal(price_costs, [F(3), F(6)], "same belief, changed stakes")
    check(price_costs[0] < 4 < price_costs[1], "price decision reversal")
    return {"examples": ["EX09"], "bounds": [old, new], "price_costs": price_costs}


def report_feedback():
    h = lambda r: (1 - r) * F(1) + r * F(1, 2)
    brier = lambda r: r*r + (1 - 2*r)*h(r)
    r_bad, r_fixed = F(5, 8), F(2, 3)
    equal(h(r_bad), F(11, 16), "report-induced failure rate")
    equal(h(r_bad) - r_bad, F(1, 16), "understatement")
    equal(brier(r_bad), F(7, 32), "lower invalid-report score")
    equal(h(r_fixed), r_fixed, "self-consistent report")
    equal(brier(r_fixed), F(2, 9), "fixed-point score")
    equal(brier(r_fixed) - brier(r_bad), F(1, 288), "inherited score gap")
    return {"examples": ["EX11"], "inherited_fixture": True, "invalid_report": r_bad,
            "failure_rate": h(r_bad), "invalid_score": brier(r_bad),
            "self_consistent_report": r_fixed, "self_consistent_score": brier(r_fixed)}


def event_intervals_and_costs():
    q_vertices = [(F(2, 3), F(1, 3), F(0)), (F(0), F(2, 3), F(1, 3)),
                  (F(1, 3), F(0), F(2, 3))]
    p_vertices = sorted(set(permutations(q_vertices[0])))
    equal(len(p_vertices), 6, "all permuted vertices")
    events = []
    for event in product((0, 1), repeat=3):
        q_values = [dot(p, event) for p in q_vertices]
        p_values = [dot(p, event) for p in p_vertices]
        q_interval, p_interval = (min(q_values), max(q_values)), (min(p_values), max(p_values))
        equal(q_interval, p_interval, "all event intervals coincide")
        events.append({"indicator": event, "interval": q_interval})
    g = (0, 1, 2)
    q_costs, p_costs = [dot(p, g) for p in q_vertices], [dot(p, g) for p in p_vertices]
    equal(sorted(q_costs), [F(1, 3), F(4, 3), F(4, 3)], "Q costs")
    equal(sorted(p_costs), [F(1, 3), F(2, 3), F(2, 3), F(4, 3), F(4, 3), F(5, 3)], "P costs")
    fallback = F(3, 2)
    check(max(q_costs) < fallback < max(p_costs), "robust action reverses")
    equal(fallback - max(q_costs), F(1, 6), "Q strict margin")
    equal(max(p_costs) - fallback, F(1, 6), "P strict margin")
    return {"examples": ["EX12"], "Q_vertices": q_vertices, "P_vertices": p_vertices,
            "events": events, "g": g, "Q_costs": q_costs, "P_costs": p_costs,
            "fallback": fallback, "decision_Q": "g", "decision_P": "fallback"}


GROUPS = [finite_fragment, binary_bridge, joint_decision, fallible_models,
          operation_cases, repairs, paid_reasoning, predictions_and_decisions,
          withdrawal_and_prices, report_feedback, event_intervals_and_costs]


def save(path, record):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(serial(record), indent=2, sort_keys=True) + "\n")
    temp.replace(path)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    out = args.out
    marker = out.with_suffix(out.suffix + ".started.json")
    if out.exists() or marker.exists():
        parser.error("Existing attempt found; inspect and preserve it. Use a named new attempt only with a recorded reason.")
    out.parent.mkdir(parents=True, exist_ok=True)
    start_ns, start_cpu = time.monotonic_ns(), time.process_time_ns()
    record = {"schema_version": 1, "task": "P3-01", "data_class": "development",
              "frozen_evaluation": False, "command": [sys.executable, *sys.argv],
              "python": platform.python_version(), "implementation": platform.python_implementation(),
              "platform": platform.platform(), "start_utc": datetime.now(timezone.utc).isoformat(),
              "start_monotonic_ns": start_ns,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "status": "RUNNING", "groups": [], "failure": None}
    with marker.open("x") as stream:
        json.dump(record, stream, indent=2)
        stream.write("\n")
    try:
        for group in GROUPS:
            begin = ASSERTIONS
            result = group()
            record["groups"].append({"name": group.__name__, "status": "PASS",
                                     "assertions": ASSERTIONS - begin, "result": result})
            save(out, record)
        record["status"] = "PASS"
    except Exception as exc:
        record["status"] = "FAIL"
        record["failure"] = {"type": type(exc).__name__, "message": str(exc),
                             "group": group.__name__, "traceback": traceback.format_exc()}
    record.update(end_utc=datetime.now(timezone.utc).isoformat(), end_monotonic_ns=time.monotonic_ns(),
                  process_cpu_ns=time.process_time_ns() - start_cpu, assertions=ASSERTIONS)
    record["elapsed_ns"] = record["end_monotonic_ns"] - start_ns
    save(out, record)
    print(json.dumps({"status": record["status"], "groups": len(record["groups"]),
                      "assertions": ASSERTIONS, "output": str(out), "elapsed_ns": record["elapsed_ns"]}))
    if record["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
