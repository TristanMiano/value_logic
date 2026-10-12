#!/usr/bin/env python3
"""Finite paid weighted-repair receipts and savings queries. DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. A stateless direct weighted-budget
branch provider, not a production incremental MaxSAT solver. Every controller
gets the same public feasible repair and objective-saturation mechanism.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import sys
import time


VERSION = "s05-weighted-repair-v1"
SEED = 26101280
ROWS = 16
WEIGHTS = (1, 2, 3, 1, 2, 3, 1, 2)
PRICES = (3, 6, 9)
TOLERANCE = 1
PROVIDER_CAP = 1_000_000


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


class CapReached(Exception):
    pass


class Meter:
    """Declared unit tariff; CPU time is measured separately."""
    def __init__(self, cap=None):
        self.operations = Counter()
        self.total = 0
        self.cap = cap

    def pay(self, category, operation, units=1):
        if self.cap is not None and self.total + units > self.cap:
            raise CapReached
        self.operations[category, operation] += units
        self.total += units

    def record(self):
        categories = Counter()
        for (category, _), value in self.operations.items():
            categories[category] += value
        return {"total": self.total, "by_category": dict(categories),
                "operations": [{"category": c, "operation": o, "units": v}
                               for (c, o), v in sorted(self.operations.items())]}


def make_cohort():
    """Public planting ensures a feasible repair; no optimum is evaluated."""
    rng = random.Random(SEED)
    result = []
    n = len(WEIGHTS)
    for row in range(ROWS):
        incumbent = rng.randrange(1 << n)
        hard = []
        target = (18, 24)[row % 2]
        while len(hard) < target:
            clause = [v if rng.getrandbits(1) else -v
                      for v in rng.sample(range(1, n + 1), 3)]
            # A declared, public feasible assignment, not hidden optimum filtering.
            if any(bool(incumbent & (1 << (abs(lit) - 1))) == (lit > 0)
                   for lit in clause):
                hard.append(sorted(clause))
        instance = {"row": row, "variables": n, "hard": sorted(hard),
                    "soft": [{"weight": w, "clause": [-v]}
                             for v, w in enumerate(WEIGHTS, 1)],
                    "public_incumbent": incumbent,
                    "objective_max": sum(WEIGHTS)}
        instance["identity"] = digest(instance)
        result.append(instance)
    return result


def provider_clause_status(clause, assignment, meter):
    """True, False or None; used only by the search provider."""
    unresolved = False
    meter.pay("solve", "clause_header")
    for lit in clause:
        meter.pay("solve", "literal_inspection")
        value = assignment[abs(lit) - 1]
        if value is None:
            unresolved = True
        elif value == (lit > 0):
            return True
    return None if unresolved else False


def budget_provider(instance, budget, cap):
    """Branch proof leaves cite a false hard clause or forced soft cost."""
    meter = Meter(cap)
    n = instance["variables"]
    assignment = [None] * n

    def visit():
        meter.pay("solve", "branch_node")
        for index, clause in enumerate(instance["hard"]):
            if provider_clause_status(clause, assignment, meter) is False:
                meter.pay("solve", "hard_leaf_create", 2)
                return False, None, ["h", index]
        forced, cost = [], 0
        for index, soft in enumerate(instance["soft"]):
            if provider_clause_status(soft["clause"], assignment, meter) is False:
                meter.pay("solve", "forced_weight_add")
                cost += soft["weight"]
                forced.append(index)
        meter.pay("solve", "budget_compare")
        if cost > budget:
            meter.pay("solve", "cost_leaf_create", 1 + len(forced))
            return False, None, ["w", forced]
        if all(value is not None for value in assignment):
            meter.pay("solve", "model_create", n)
            model = sum(int(value) << i for i, value in enumerate(assignment))
            return True, model, None
        variable = assignment.index(None)
        assignment[variable] = False
        sat, model, left = visit()
        if sat:
            assignment[variable] = None
            return sat, model, None
        assignment[variable] = True
        sat, model, right = visit()
        assignment[variable] = None
        if sat:
            return sat, model, None
        meter.pay("solve", "split_certificate_create", 2)
        return False, None, ["b", variable, left, right]

    try:
        sat, model, proof = visit()
        answer = {"status": "SAT" if sat else "UNSAT", "model": model,
                  "proof": proof}
    except CapReached:
        answer = {"status": "UNRESOLVED", "model": None, "proof": None}
    answer["invoice"] = meter.record()
    return answer


def checked_objective(instance, model, meter):
    """Separate full witness check and ONE objective pass, even for loose b."""
    n = instance["variables"]
    if type(model) is not int or not 0 <= model < (1 << n):
        raise ValueError("Malformed assignment")
    for clause in instance["hard"]:
        satisfied = False
        meter.pay("check", "witness_hard_clause_header")
        for lit in clause:
            meter.pay("check", "witness_hard_literal")
            bit = (model >> (abs(lit) - 1)) & 1
            if bit == int(lit > 0):
                satisfied = True
                break
        if not satisfied:
            raise ValueError("Assignment violates a hard clause")
    cost = 0
    meter.pay("objective", "full_objective_pass")
    for soft in instance["soft"]:
        satisfied = False
        meter.pay("objective", "soft_clause_header")
        for lit in soft["clause"]:
            meter.pay("objective", "soft_literal")
            if ((model >> (abs(lit) - 1)) & 1) == int(lit > 0):
                satisfied = True
                break
        if not satisfied:
            meter.pay("objective", "weight_add")
            cost += soft["weight"]
    return cost


def check_negative(instance, budget, proof, meter):
    """Check the explicit proof tree, without calling the search provider."""
    assignment = {}

    def is_false(clause):
        meter.pay("check", "negative_clause_header")
        for lit in clause:
            meter.pay("check", "negative_literal")
            variable = abs(lit) - 1
            if variable not in assignment or assignment[variable] == (lit > 0):
                return False
        return True

    def visit(node):
        meter.pay("check", "negative_proof_node")
        if not isinstance(node, list) or not node:
            raise ValueError("Malformed proof node")
        if node[0] == "h" and len(node) == 2:
            index = node[1]
            if type(index) is not int or not 0 <= index < len(instance["hard"]):
                raise ValueError("Bad hard clause index")
            if not is_false(instance["hard"][index]):
                raise ValueError("Claimed hard conflict does not hold")
            return
        if node[0] == "w" and len(node) == 2:
            indices = node[1]
            if not isinstance(indices, list):
                raise ValueError("Malformed cost support")
            seen, cost = set(), 0
            for index in indices:
                meter.pay("check", "negative_weight_index")
                if type(index) is not int or index in seen or not 0 <= index < len(instance["soft"]):
                    raise ValueError("Invalid or repeated soft clause index")
                seen.add(index)
                soft = instance["soft"][index]
                if not is_false(soft["clause"]):
                    raise ValueError("Claimed forced soft cost does not hold")
                meter.pay("check", "negative_weight_add")
                cost += soft["weight"]
            if cost <= budget:
                raise ValueError("Forced cost does not exceed the budget")
            return
        if node[0] == "b" and len(node) == 4:
            variable = node[1]
            if type(variable) is not int or not 0 <= variable < instance["variables"] or variable in assignment:
                raise ValueError("Invalid split variable")
            assignment[variable] = False
            visit(node[2])
            assignment[variable] = True
            visit(node[3])
            del assignment[variable]
            return
        raise ValueError("Unknown proof node")

    visit(proof)


def proof_words(node):
    if node[0] == "h":
        return 2
    if node[0] == "w":
        return 1 + len(node[1])
    return 2 + proof_words(node[2]) + proof_words(node[3])


class Service:
    def __init__(self, instances):
        self.instances = instances
        self.meter = Meter()
        self.provider_units = 0
        self.provider_operations = Counter()
        self.calls = self.unresolved = 0
        self.events = []
        self.state = []
        for instance in instances:
            n = instance["variables"]
            words = 8 + sum(1 + len(c) for c in instance["hard"])
            words += sum(2 + len(s["clause"]) for s in instance["soft"])
            self.meter.pay("setup", "weighted_source_admission", words)
            self.meter.pay("storage", "weighted_source_retention", words)
            if instance["identity"] != digest({k: v for k, v in instance.items() if k != "identity"}):
                raise ValueError("Source payload does not match its identity")
            if n < 1:
                raise ValueError("Empty variable universe")
            for clause in instance["hard"] + [s["clause"] for s in instance["soft"]]:
                if any(type(lit) is not int or not 1 <= abs(lit) <= n for lit in clause):
                    raise ValueError("Malformed source clause")
            if any(type(s["weight"]) is not int or s["weight"] <= 0 for s in instance["soft"]):
                raise ValueError("Require positive integer soft weights")
            if instance["objective_max"] != sum(s["weight"] for s in instance["soft"]):
                raise ValueError("Incorrect declared objective range")
            upper = checked_objective(instance, instance["public_incumbent"], self.meter)
            self.state.append({"lower": 0, "upper": upper,
                               "witness": instance["public_incumbent"],
                               "negative_receipt_event": None})
            self.meter.pay("storage", "initial_frontier_receipt", 8 + n)

    def acquire(self, row, budget, cap=PROVIDER_CAP):
        if type(budget) is not int:
            raise ValueError("An integer budget is required")
        before = self.meter.total
        state = self.state[row]
        instance = self.instances[row]
        old = [state["lower"], state["upper"]]
        self.meter.pay("controller", "source_bound_frontier_lookup", 8)
        event = {"row": row, "source_identity": instance["identity"],
                 "budget": budget, "before": old, "cap": cap}
        if budget < state["lower"]:
            event["status"] = "CACHED_UNSAT"
        elif budget >= state["upper"]:
            event["status"] = "CACHED_SAT"
        else:
            got = budget_provider(instance, budget, cap)
            self.calls += 1
            self.provider_units += got["invoice"]["total"]
            for op in got["invoice"]["operations"]:
                self.provider_operations[op["category"], op["operation"]] += op["units"]
            event.update(got)
            if got["status"] == "SAT":
                actual_cost = checked_objective(instance, got["model"], self.meter)
                if actual_cost > budget:
                    raise ValueError("Returned assignment exceeds its query budget")
                state["upper"] = actual_cost
                state["witness"] = got["model"]
                event["checked_actual_objective"] = actual_cost
                event["saturated_budget_range"] = [actual_cost, instance["objective_max"]]
                self.meter.pay("storage", "checked_positive_receipt", 8 + instance["variables"])
            elif got["status"] == "UNSAT":
                check_negative(instance, budget, got["proof"], self.meter)
                state["lower"] = budget + 1
                state["negative_receipt_event"] = len(self.events)
                self.meter.pay("storage", "checked_negative_receipt", 8 + proof_words(got["proof"]))
            else:
                self.unresolved += 1
        if state["lower"] > state["upper"]:
            raise ValueError("Inconsistent checked frontiers")
        self.meter.pay("output", "query_receipt_event", 16)
        event.update(after=[state["lower"], state["upper"]],
                     adapter_units=self.meter.total - before)
        self.events.append(event)
        return event["status"] != "UNRESOLVED"

    def value_interval(self, row, price):
        state = self.state[row]
        self.meter.pay("assessment", "savings_endpoints", 4)
        return [max(0, price - state["upper"]), max(0, price - state["lower"])]

    def snapshot(self):
        adapter = self.meter.record()
        return {"provider_units": self.provider_units, "adapter_units": adapter["total"],
                "total_units": self.provider_units + adapter["total"],
                "provider_calls": self.calls, "unresolved_calls": self.unresolved,
                "adapter_invoice": adapter,
                "provider_operations": [{"category": c, "operation": o, "units": v}
                                        for (c, o), v in sorted(self.provider_operations.items())]}


def run_arm(instances, mode):
    start, cpu = time.perf_counter_ns(), time.process_time_ns()
    service = Service(instances)
    stages = []
    for price in PRICES:
        for row, state in enumerate(service.state):
            while True:
                service.meter.pay("controller", "requested_precision_check", 3)
                lower, upper = state["lower"], state["upper"]
                effective_upper = upper if mode == "full_exact_optimization" else min(upper, price)
                tolerance = 0 if mode == "full_exact_optimization" else TOLERANCE
                if effective_upper - lower <= tolerance:
                    break
                if mode == "requested_value_midpoint":
                    budget = (lower + effective_upper - 1) // 2
                else:
                    budget = effective_upper - tolerance - 1
                service.meter.pay("controller", "budget_selection", 3)
                if not service.acquire(row, budget):
                    break
        values = [service.value_interval(i, price) for i in range(len(instances))]
        bounds = [[s["lower"], s["upper"]] for s in service.state]
        max_cost = max(i["objective_max"] for i in instances)
        service.meter.pay("assessment", "cdf_count_comparisons", 2 * len(instances) * (max_cost + 1))
        cdf = [[sum(upper <= k for _, upper in bounds), sum(lower <= k for lower, _ in bounds)]
               for k in range(max_cost + 1)]
        service.meter.pay("assessment", "cohort_value_sums", 2 * len(instances))
        stages.append({"price": price, "tolerance": TOLERANCE,
                       "optimum_intervals": bounds, "value_intervals": values,
                       "mean_value_interval": [[sum(v[0] for v in values), len(instances)],
                                               [sum(v[1] for v in values), len(instances)]],
                       "cdf_count_envelope": {"denominator": len(instances), "thresholds": list(range(max_cost + 1)),
                                              "lower_upper_counts": cdf},
                       "snapshot": service.snapshot()})
    return {"mode": mode, "stages": stages, "events": service.events,
            "final_state": service.state, "final": service.snapshot(),
            "process_ns": time.process_time_ns() - cpu,
            "wall_ns": time.perf_counter_ns() - start}


def targeted_checks():
    fixture = {"row": 0, "variables": 3, "hard": [[1, 2], [-1, 3]],
               "soft": [{"weight": w, "clause": [-v]} for v, w in enumerate((1, 2, 3), 1)],
               "public_incumbent": 5, "objective_max": 6}
    fixture["identity"] = digest(fixture)
    service = Service([fixture])
    initial = dict(service.state[0])
    assert not service.acquire(0, 1, cap=1)
    assert service.state[0] == initial
    assert service.acquire(0, 1)
    assert service.state[0]["lower"] == 2
    assert service.acquire(0, 2)
    assert service.state[0]["upper"] == 2
    calls = service.calls
    assert service.acquire(0, 6)
    assert service.acquire(0, 0)
    assert service.calls == calls
    rejected = False
    try:
        check_negative(fixture, 2, ["w", [1, 1]], Meter())
    except ValueError:
        rejected = True
    assert rejected
    return {"status": "complete", "fixture": fixture,
            "checks": ["cap leaves bounds unchanged", "negative proof raises lower bound",
                       "checked actual objective saturates all looser budgets",
                       "frontier queries avoid a new provider call", "invalid negative proof rejected"],
            "events": service.events, "invoice": service.snapshot()}


def main(destination):
    if destination.exists():
        raise FileExistsError("Preserve existing development evidence")
    start = time.perf_counter_ns()
    source_cpu = time.process_time_ns()
    instances = make_cohort()
    source_process_ns = time.process_time_ns() - source_cpu
    result = {"status": "running", "evidence": "DEVELOPMENT", "version": VERSION,
              "contributor": "ChatGPT (GPT-6 Astra Pro)",
              "start_utc": datetime.now(timezone.utc).isoformat(),
              "python": sys.version, "command": sys.argv,
              "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "source_identity": digest(instances), "instances": instances,
              "design": {"seed": SEED, "rows": ROWS, "weights": WEIGHTS,
                         "prices": PRICES, "absolute_value_tolerance": TOLERANCE,
                         "provider_cap": PROVIDER_CAP,
                         "source": "Public planted feasible repairs; fixed weighted distance to all-zero desired configuration. No optimum filtering.",
                         "target": "V_p=max(0,p-C*), the best objective saving against replacement price p.",
                         "sampling": "All rows of a fixed finite cohort; uniform cohort values and CDF envelopes are deterministic, with no iid generalization claim."},
              "tariff": "One unit per named admitted/retained word, logical inspection, arithmetic update, proof node operation or controller operation. Explicit service tariff, not a complete CPU instruction count. Common generation and JSON/hashing harness work have separate timing or are included in arm process/wall time. Objective cost is distinct from proof-service cost.",
              "source_generation_process_ns": source_process_ns, "arms": []}

    def save():
        destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    save()
    try:
        result["targeted_checks"] = targeted_checks()
        save()
        for mode in ("conventional_requested_value", "requested_value_midpoint", "full_exact_optimization"):
            result["arms"].append(run_arm(instances, mode))
            save()
        optima = [s["lower"] for s in result["arms"][-1]["final_state"]]
        assert all(s["lower"] == s["upper"] for s in result["arms"][-1]["final_state"])
        for arm in result["arms"]:
            assert arm["final"]["unresolved_calls"] == 0
            for stage in arm["stages"]:
                for optimum, interval, value in zip(optima, stage["optimum_intervals"], stage["value_intervals"]):
                    assert interval[0] <= optimum <= interval[1]
                    actual = max(0, stage["price"] - optimum)
                    assert value[0] <= actual <= value[1]
                    assert value[1] - value[0] <= TOLERANCE
        result["post_run_exact_optima"] = optima
        result["checks"] = {"all_value_intervals_contain_checked_exact_reference": True,
                            "all_requested_widths_at_most_tolerance": True,
                            "all_cohort_provider_calls_complete": True,
                            "shared_objective_saturation_and_public_incumbents": True}
        result["status"] = "complete"
    except Exception as error:
        result["status"] = "failed"
        result["error"] = {"type": type(error).__name__, "message": str(error)}
        save()
        raise
    result["end_utc"] = datetime.now(timezone.utc).isoformat()
    result["elapsed_wall_ns"] = time.perf_counter_ns() - start
    save()
    print(json.dumps({"status": result["status"], "source_identity": result["source_identity"],
                     "optima": optima, "arms": [{"mode": a["mode"],
                       "stages": [{"price": s["price"], "calls": s["snapshot"]["provider_calls"],
                                   "units": s["snapshot"]["total_units"],
                                   "mean_value_interval": s["mean_value_interval"]} for s in a["stages"]],
                       "process_ms": a["process_ns"] / 1e6} for a in result["arms"]]}))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("maxsat_repair_results.json"))
