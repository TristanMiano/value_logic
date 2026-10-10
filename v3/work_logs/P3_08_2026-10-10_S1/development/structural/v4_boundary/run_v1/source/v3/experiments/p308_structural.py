#!/usr/bin/env python3
"""P3-08 DEVELOPMENT: finite structural/repair integration, not final evaluation.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.

The candidate reuses unchanged P3-04/05 interfaces. The ordinary method has an
independent point evaluator, paired-support compiler and exhaustive selector.
Both receive identical public finite inputs and pay the same local checking
and reporting service. The independently supplied sources are outside repair
minimization. All tied minima survive. This module claims no novel semantics,
generic superiority, physical CPU bound, or unmeasured principal research time.

Resource units are STRUCTURAL-VM-v1, NOT the selective-feedback primitive tariff.
Every executed Python opcode in worker stages (including Python library callees)
and every C-call profile event is billed. Native arithmetic/container work inside
an opcode is a bounded primitive of this finite tariff: these fixtures have at
most six support bits, two source cases, integer inputs of magnitude at most 8,
and 128-bit rational intermediate caps. Every source, input, retained state and
reported byte is also charged. The native JSON/string bound is 32 KiB per worker
object. Interpreter bootstrap, instrumentation and external experiment auditing
are not deployed service work; source enrolment prices the supplied code bytes.
These are complete declared abstract charges, not measurements of C internals,
Python allocator/GC work, operating-system time or whole-process heap usage.

The resource-failure API below covers the nine exact published fixtures, with
an exact integer budget of at least TERMINAL_RESERVE. Smaller/non-integer
accounts are rejected before paid work. No arbitrary-input success bound is
claimed. Normal reporting protects a separately funded fixed failure receipt.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import platform
import sys
import time
import traceback

sys.dont_write_bytecode = True
VERSION = "p308-structural-v4"
STAGE = "DEVELOPMENT"
TARIFF = "STRUCTURAL-VM-v1"
ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve()
CHECKS = ROOT / "v3/checks"
MAX_OBJECT_BYTES = 32768
MAX_RATIONAL_BITS = 128
TERMINAL_RESERVE = 100_000
FAILURE_READOUT_RESERVE = 1024
SUCCESS_BUDGET = 50_000_000
UNKNOWN_BUDGET_PAYLOAD = ('{"decision":{"action":null,"status":"UNKNOWN",'
                          '"useful_action_warrant":false},"received_answer":false,'
                          '"sources":[],"status":"UNKNOWN_BUDGET"}')
M = K = None


def serializable(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [serializable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): serializable(v) for k, v in value.items()}
    return value


def wire(value):
    return json.dumps(serializable(value), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False)


def digest(value):
    return hashlib.sha256(wire(value).encode("ascii")).hexdigest()


def _load_legacy():
    global M, K
    if M is None:
        name = "_p308_structural_transport"
        spec = importlib.util.spec_from_file_location(name, CHECKS / "05_counterfactual_transport.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        M, K = module, module.K


class ResourceExhausted(RuntimeError):
    def __init__(self, message, stage):
        super().__init__(message)
        self.stage = stage


class StaleWarrant(ValueError):
    pass


class StructuralMeter:
    """All worker stages are traced; this measuring apparatus is not self-billed.

    A terminal reserve cannot fund earlier computation. Failed execution retains
    every actually admitted opcode/C-call/byte charge; an unexecuted over-budget
    instruction is not charged. The experiment writer is external to the worker.
    """
    def __init__(self, budget=SUCCESS_BUDGET):
        if type(budget) is not int or budget < TERMINAL_RESERVE:
            raise ValueError("Admission requires an exact integer budget >= TERMINAL_RESERVE; no paid work occurred.")
        self.budget = budget
        self.units = 0
        self.by_stage = {}
        self.current = None
        self.active = False
        self.max_object_bytes = 0
        self.max_retained_bytes = 0
        self.retained = {}
        self.failures = []
        self.failure_readout = False

    def _meter_charge(self, stage, category, count):
        if type(count) is not int or count < 0:
            raise ValueError("Nonnegative integer primitive count required.")
        if stage == "terminal_reporting":
            ceiling = self.budget if self.failure_readout else self.budget - FAILURE_READOUT_RESERVE
        else:
            ceiling = self.budget - TERMINAL_RESERVE
        if self.units + count > ceiling:
            raise ResourceExhausted(f"{stage}: {count} {category} would exceed reserved budget", stage)
        counts = self.by_stage.setdefault(stage, Counter())
        counts[category] += count
        self.units += count

    def _meter_event(self, category):
        self._meter_charge(self.current, category, 1)

    def _meter_trace(self, frame, event, arg):
        if frame.f_code in _METER_CODES:
            return None
        if event == "call":
            frame.f_trace_opcodes = True
            return self._meter_trace
        if event == "opcode" and self.active:
            self._meter_event("python_opcodes")
        return self._meter_trace

    def _meter_profile(self, frame, event, arg):
        if event == "c_call" and self.active and frame.f_code not in _METER_CODES:
            self._meter_event("bounded_native_c_calls")

    def _meter_run(self, stage, function):
        old_trace, old_profile = sys.gettrace(), sys.getprofile()
        old_current, old_active = self.current, self.active
        self.current, self.active = stage, True
        try:
            sys.settrace(self._meter_trace)
            sys.setprofile(self._meter_profile)
            return function()
        finally:
            self.active = False
            sys.settrace(old_trace)
            sys.setprofile(old_profile)
            self.current, self.active = old_current, old_active

    def _meter_bytes(self, stage, category, payload):
        length = len(payload.encode("ascii")) if isinstance(payload, str) else len(payload)
        self._meter_charge(stage, category, length)
        return length

    def _meter_retain(self, key, value):
        payload = self._meter_run("storage", lambda: wire(value))
        size = len(payload.encode("ascii"))
        if size > MAX_OBJECT_BYTES:
            raise ValueError("Retained worker object exceeds declared native size cap.")
        self._meter_bytes("storage", "retained_byte_periods", payload)
        self.retained[key] = size
        self.max_object_bytes = max(self.max_object_bytes, size)
        self.max_retained_bytes = max(self.max_retained_bytes, sum(self.retained.values()))

    def _meter_invoice(self):
        counts = {stage: dict(sorted(values.items())) for stage, values in sorted(self.by_stage.items())}
        assert sum(sum(v.values()) for v in counts.values()) == self.units
        return {"tariff": TARIFF, "total_units": self.units, "budget": self.budget,
                "terminal_reserve": TERMINAL_RESERVE, "by_stage": counts,
                "failure_readout_reserve": FAILURE_READOUT_RESERVE,
                "failure_readout_released": self.failure_readout,
                "max_serialized_object_bytes": self.max_object_bytes,
                "max_retained_serialized_bytes": self.max_retained_bytes,
                "failures": self.failures,
                "physical_cpu_and_heap_cap_claimed": False,
                "accounting_instrumentation_included": False}


_METER_CODES = {value.__code__ for value in StructuralMeter.__dict__.values()
                if callable(value) and hasattr(value, "__code__")}


@dataclass(frozen=True)
class NativeRequest:
    nbits: int
    hard: tuple
    soft: tuple
    losses: tuple
    scope_record: str


def lit(number):
    return ("lit", Fraction(number))


def bit(index):
    return ("bit", index)


def add(left, right):
    return ("add", left, right)


def scale(number, value):
    return ("scale", Fraction(number), value)


def eq(left, right):
    return ("eq", left, right)


def not_(value):
    return ("not", value)


def bounded_rational(value):
    answer = Fraction(value)
    if max(abs(answer.numerator).bit_length(), answer.denominator.bit_length()) > MAX_RATIONAL_BITS:
        raise ValueError("Native rational operand cap exceeded.")
    return answer


def ordinary_point(expression, assignment):
    """Independent exact evaluator: no legacy interval, compiler or rank calls."""
    op = expression[0]
    if op == "lit":
        answer = Fraction(expression[1])
    elif op == "bit":
        answer = Fraction(assignment[expression[1]])
    elif op == "not":
        answer = 1 - ordinary_point(expression[1], assignment)
    elif op == "scale":
        answer = Fraction(expression[1]) * ordinary_point(expression[2], assignment)
    else:
        a = ordinary_point(expression[1], assignment)
        b = ordinary_point(expression[2], assignment)
        if op == "add":
            answer = a + b
        elif op in ("and", "min"):
            answer = min(a, b)
        elif op in ("or", "max"):
            answer = max(a, b)
        elif op == "eq":
            answer = Fraction(a == b)
        else:
            raise ValueError("Unknown ordinary expression operation.")
    return bounded_rational(answer)


def ordinary_support(formula, atoms):
    """Independent Belnap-Dunn compilation of the *unchanged quoted* formula."""
    op = formula[0]
    if op == "atom":
        index = atoms.index(formula[1])
        return bit(2 * index), bit(2 * index + 1)
    if op == "top":
        return lit(1), lit(0)
    if op == "bottom":
        return lit(0), lit(1)
    if op == "not":
        pos, neg = ordinary_support(formula[1], atoms)
        return neg, pos
    apos, aneg = ordinary_support(formula[1], atoms)
    bpos, bneg = ordinary_support(formula[2], atoms)
    if op == "and":
        return ("and", apos, bpos), ("or", aneg, bneg)
    if op == "or":
        return ("or", apos, bpos), ("and", aneg, bneg)
    raise ValueError("Unsupported quote.")


def classical_point(formula, atoms, assignment):
    op = formula[0]
    if op == "atom":
        return assignment[atoms.index(formula[1])]
    if op == "top":
        return 1
    if op == "bottom":
        return 0
    if op == "not":
        return 1 - classical_point(formula[1], atoms, assignment)
    a = classical_point(formula[1], atoms, assignment)
    b = classical_point(formula[2], atoms, assignment)
    if op == "and":
        return int(bool(a) and bool(b))
    if op == "or":
        return int(bool(a) or bool(b))
    raise ValueError("Unsupported classical quote.")


def validate_input(spec):
    encoded = wire(spec)
    if len(encoded.encode("ascii")) > MAX_OBJECT_BYTES:
        raise ValueError("Input object exceeds fixed native bound.")
    if not 1 <= len(spec["sources"]) <= 2 or not 1 <= len(spec["actions"]) <= 3:
        raise ValueError("Finite source/action cap.")
    if spec["kind"] == "paired":
        if not 1 <= len(spec["atoms"]) <= 3:
            raise ValueError("At most six support bits in this development arm.")
        for source in spec["sources"]:
            if any(type(w) is not int or not 1 <= w <= 8 for _, w in source["weights"]):
                raise ValueError("Fixed positive integer normality-weight cap.")
    elif spec["kind"] == "routing":
        if (spec["original_table"], spec["replacement_table"], spec["history"]) != ((0, 0, 1), (1, 0, 1), 0):
            raise ValueError("This finite routing adapter uses the declared three-entry table fixture.")
    else:
        raise ValueError("Unspecified finite adapter.")
    return encoded


def source_scope(spec, source):
    return wire({"version": VERSION, "request": spec, "source": source,
                 "source_quantifier": "EXTERNAL_UNRESOLVED_CASE_NOT_A_REPAIR"})


def ordinary_compile(spec):
    validate_input(spec)
    if spec["kind"] == "routing":
        return tuple((source, None) for source in spec["sources"])
    atoms = spec["atoms"]
    requests = []
    for source in spec["sources"]:
        hard = [ordinary_support(spec["quote"], atoms)[0]]
        soft = []
        weights = dict(source["weights"])
        frame = dict(source["frame"])
        for index, atom in enumerate(atoms):
            positive, negative = bit(2 * index), bit(2 * index + 1)
            normal = eq(add(positive, negative), lit(1))
            if atom in spec["exceptions"]:
                soft.append(("normal:" + atom, normal, Fraction(weights[atom]), 0))
            else:
                hard.append(normal)
            if atom in frame:
                hard.extend((eq(positive, lit(frame[atom])), eq(negative, lit(1 - frame[atom]))))
            if spec["preserve_baseline"]:
                baseline = spec["baseline"][index]
                soft.extend((("reference:" + atom + ":t", eq(positive, lit(baseline)), Fraction(1), 1),
                             ("reference:" + atom + ":f", eq(negative, lit(1 - baseline)), Fraction(1), 1)))
        requests.append((source, NativeRequest(2 * len(atoms), tuple(hard), tuple(soft),
                                              spec["actions"], source_scope(spec, source))))
    return tuple(requests)


def candidate_compile(spec):
    validate_input(spec)
    if spec["kind"] == "routing":
        equations = (K.Equation("Z", (0, 1), (), (((), 0),)),
                     K.Equation("A", (0, 1), ("Z",), (((0,), 0), ((1,), 1))),
                     K.Equation("B", (0, 1), ("Z",), (((0,), 0), ((1,), 1))),
                     K.Equation("C", (0, 1), (), (((), 0),)),
                     K.Equation("P", (0, 1), (), (((), 0),)))
        return tuple((source, equations) for source in spec["sources"])
    requests = []
    for source in spec["sources"]:
        # The accepted constructor provides the original quote and fixed rules.
        baseline = tuple(dict(source["frame"]).get(atom, spec["baseline"][i])
                         for i, atom in enumerate(spec["atoms"]))
        request = K.paired_request(spec["atoms"], spec["quote"], baseline,
                                   spec["exceptions"], tuple(a for a, _ in source["frame"]), (),
                                   spec["preserve_baseline"], spec["actions"])
        weights = dict(source["weights"])
        soft = tuple(replace(row, weight=Fraction(weights[row.identity.split(":")[1]]))
                     if row.identity.startswith("normal:") else row for row in request.soft)
        # Reference preferences must remain tied to the declared ordinary baseline,
        # independently of a newly supplied hard frame in an unresolved source.
        if spec["preserve_baseline"]:
            rewritten = []
            for row in soft:
                if row.identity.startswith("reference:"):
                    _, atom, side = row.identity.split(":")
                    i = spec["atoms"].index(atom)
                    index = 2 * i + (side == "f")
                    target = spec["baseline"][i] if side == "t" else 1 - spec["baseline"][i]
                    row = replace(row, formula=K.eq(K.bit(index), K.lit(target)))
                rewritten.append(row)
            soft = tuple(rewritten)
        request = replace(request, soft=soft, scope=f"p308/{spec['name']}/{source['id']}",
                          metadata_json=source_scope(spec, source))
        requests.append((source, request))
    return tuple(requests)


def summarize_source(spec, source, rank, models, evaluator, losses):
    values = []
    for state in models:
        values.append({"state": state,
                       "losses": {name: evaluator(expr, state) for name, expr in losses}})
    images = {name: sorted({row["losses"][name] for row in values}) for name, _ in losses}
    return {"source_id": source["id"], "scope_record": source_scope(spec, source),
            "feasibility": "NONEMPTY" if models else "INFEASIBLE",
            "identities_complete": True, "optimal_rank": rank,
            "models": tuple(models), "loss_images": images, "case_values": values}


def ordinary_rank(request, state):
    tiers = max((row[3] for row in request.soft), default=0) + 1
    rank = [Fraction(0)] * tiers
    for _, formula, weight, tier in request.soft:
        rank[tier] += weight * (1 - ordinary_point(formula, state))
    return tuple(rank)


def ordinary_route(spec, source):
    """Explicit original/new table routing; no legacy structural function calls."""
    original = spec["original_table"]
    replacement = spec["replacement_table"]
    history = spec["history"]
    if replacement[history] != 1:
        raise ValueError("Required changed output absent.")
    operation = source["operation"]
    if operation == "conditioning":
        return () if original[history] != 1 else ((1, 1, 0, 0),)
    if operation == "occurrence":
        return ((1, original[history], 0, 0),)
    outputs = tuple((replacement if follows else original)[history]
                    for _, follows in source["routing"])
    return (outputs,)


def candidate_route(spec, source, equations):
    operation = source["operation"]
    if operation == "conditioning":
        actual = K.structural(equations, {})
        return () if actual["A"] != 1 else (tuple(actual[n] for n in ("A", "B", "C", "P")),)
    if operation == "occurrence":
        changed = K.structural(equations, {}, {"A": 1})
        return (tuple(changed[n] for n in ("A", "B", "C", "P")),)
    reply = K.route_replacement(spec["original_table"], spec["replacement_table"],
                                spec["history"], source["routing"], required=1)
    return (tuple(reply["outputs"][n] for n in ("A", "B", "C", "P")),)


def solve_ordinary(spec, requests):
    rows = []
    for source, request in requests:
        if spec["kind"] == "routing":
            models = ordinary_route(spec, source)
            rows.append(summarize_source(spec, source, (Fraction(0),) if models else None,
                                         models, ordinary_point, spec["actions"]))
            continue
        best_rank = None
        best = []
        for state in product((0, 1), repeat=request.nbits):
            if not all(ordinary_point(expr, state) == 1 for expr in request.hard):
                continue
            rank = ordinary_rank(request, state)
            if best_rank is None or rank < best_rank:
                best_rank, best = rank, [state]
            elif rank == best_rank:
                best.append(state)
        rows.append(summarize_source(spec, source, best_rank, tuple(best), ordinary_point, request.losses))
    return rows


def solve_candidate(spec, requests):
    rows = []
    for source, request in requests:
        if spec["kind"] == "routing":
            models = candidate_route(spec, source, request)
            rows.append(summarize_source(spec, source, (Fraction(0),) if models else None,
                                         models, lambda e, x: K.interval(e, x)[0], spec["actions"]))
            continue
        search = K.Search(request)
        while search.frontier:
            search.advance(1)
        report = search.report()
        if not report["identities_complete"]:
            raise AssertionError("Incomplete inherited search cannot claim all minima.")
        rows.append(summarize_source(spec, source, report["incumbent_rank"],
                                     tuple(report["best_witnesses"]),
                                     lambda e, x: K.interval(e, x)[0], request.losses))
    return rows


def verify_complete_reply(spec, reply):
    """Same priced local exhaustive checker for both candidate and ordinary.

    Recompilation here is independent of the inherited candidate compiler.
    There is no uncharged oracle or independently exported proof service.
    """
    expected = solve_ordinary(spec, ordinary_compile(spec))
    if wire(expected) != wire(reply):
        raise ValueError("Received complete finite result fails independent reconstruction.")
    return {"checked": True, "scope": "complete local finite report", "sources": reply}


def choose_fixed_action(spec, rows):
    if any(row["feasibility"] != "NONEMPTY" for row in rows):
        return {"status": "INFEASIBLE", "action": None, "useful_action_warrant": False,
                "reason": "No established nonempty target for every retained source."}
    case_values = [case for source in rows for case in source["case_values"]]
    actions = tuple(name for name, _ in spec["actions"])
    worst = {a: max(row["losses"][a] for row in case_values) for a in actions}
    action = min(actions, key=lambda a: (worst[a], actions.index(a)))
    oracle = max(min(row["losses"][a] for a in actions) for row in case_values)
    lowest_rank = min(source["optimal_rank"] for source in rows)
    wrongly_kept = [source for source in rows if source["optimal_rank"] == lowest_rank]
    wrong_cases = [case for source in wrongly_kept for case in source["case_values"]]
    wrong_worst = {a: max(row["losses"][a] for row in wrong_cases) for a in actions}
    return {"status": "CHECKED_COMPLETE", "action": action, "fixed_action_worst_loss": worst[action],
            "worst_loss_by_fixed_action": worst, "useful_action_warrant": True,
            "all_ties_preserved": True,
            "selection_order": "ONE_ACTION_THEN_ALL_UNRESOLVED_SOURCES_THEN_ALL_PER_SOURCE_MINIMA",
            "nonimplementable_pointwise_action_oracle": oracle,
            "oracle_is_policy": False,
            "forbidden_joint_source_repair_minimum": {
                "retained_sources": [source["source_id"] for source in wrongly_kept],
                "minimum_fixed_loss": min(wrong_worst.values()),
                "is_an_admissible_service": False}}


def make_terminal(spec, checked):
    rows = checked["sources"]
    result = {"status": "SUCCESS", "sources": rows, "decision": choose_fixed_action(spec, rows),
              "source_information": "Each named source is unresolved and retained outside minimization.",
              "check_service": checked["scope"]}
    if spec["kind"] == "paired":
        count = sum(classical_point(spec["quote"], spec["atoms"], bits)
                    for bits in product((0, 1), repeat=len(spec["atoms"])))
        result["quoted_antecedent"] = spec["quote"]
        result["ordinary_interpretation"] = "Fixed ordinary Boolean interpretation of the original quote."
        result["ordinary_satisfying_valuations"] = count
        result["hypothetical_interpretation"] = "Declared paired-support evaluation; not a truth probability."
    return result


def source_files(method):
    files = [SELF]
    if method == "candidate":
        files.extend((CHECKS / "04_counterfactual_repair.py", CHECKS / "05_counterfactual_transport.py"))
    return files


def deployment_setup(meter, spec, method, *, source_sizes=None):
    # Source-byte enrolment is the declared bootstrap tariff. It does not claim
    # to time CPython import compilation or historical code development.
    if source_sizes is None:
        source_sizes = []
    for path in source_files(method):
        size = len(path.read_bytes())
        meter._meter_charge("setup", "source_admission_bytes", size)
        source_sizes.append({"path": str(path.relative_to(ROOT)), "bytes": size})
    meter._meter_bytes("input_admission", "input_bytes", wire(spec))
    return source_sizes


def compiled_records(requests):
    records = []
    for source, request in requests:
        if isinstance(request, NativeRequest):
            body = {"nbits": request.nbits, "hard": request.hard, "soft": request.soft,
                    "losses": request.losses, "scope_record": request.scope_record}
        elif request is None:
            body = {"source": source, "compiler": "direct ordinary table evaluator"}
        elif isinstance(request, tuple):
            body = [{"name": equation.name, "domain": equation.domain,
                     "parents": equation.parents, "table": equation.table} for equation in request]
        else:
            body = request.record()
        records.append({"source_id": source["id"], "compiled": body})
    return records


def method_execution(meter, spec, method):
    compiler = candidate_compile if method == "candidate" else ordinary_compile
    solver = solve_candidate if method == "candidate" else solve_ordinary
    meter._meter_retain("input", spec)
    requests = meter._meter_run("dependency_construction", lambda: compiler(spec))
    meter._meter_retain("compiled_dependencies", compiled_records(requests))
    raw = meter._meter_run("search", lambda: solver(spec, requests))
    meter._meter_retain("complete_search_result", raw)
    checked = meter._meter_run("checking", lambda: verify_complete_reply(spec, raw))
    # The checked object aliases the retained answer; only its new receipt is stored.
    meter._meter_retain("check_receipt", {"checked": checked["checked"], "scope": checked["scope"]})
    return meter._meter_run("terminal_reporting", lambda: make_terminal(spec, checked))


def unknown_budget_payload():
    # Two traced worker opcodes load/return this 140-byte admitted source literal.
    return UNKNOWN_BUDGET_PAYLOAD


def run_method(spec, method, *, budget=None):
    """Paid-prefix failure receipts for the nine published fixtures.

    Admission requires type(budget) is int and budget >= TERMINAL_RESERVE.
    Success is demonstrated only at the declared finite fixture account;
    arbitrary caller-created input objects are outside this finite guarantee.
    """
    if method not in ("candidate", "ordinary"):
        raise ValueError("Unknown matched method.")
    meter = StructuralMeter(SUCCESS_BUDGET if budget is None else budget)
    sources, input_admitted = [], False
    try:
        deployment_setup(meter, spec, method, source_sizes=sources)
        input_admitted = True
        result = meter._meter_run("controller", lambda: method_execution(meter, spec, method))
        payload = meter._meter_run("terminal_reporting", lambda: wire(result))
        if len(payload.encode("ascii")) > MAX_OBJECT_BYTES:
            raise ValueError("Terminal object exceeds declared bounded native primitive cap.")
        meter.max_object_bytes = max(meter.max_object_bytes, len(payload))
        meter._meter_bytes("terminal_reporting", "report_bytes", payload)
    except ResourceExhausted as exc:
        meter.failures.append({"kind": "BUDGET_EXHAUSTED", "stage": exc.stage, "reason": str(exc),
                               "paid_prefix_units": meter.units})
        meter.failure_readout = True
        payload = meter._meter_run("terminal_reporting", unknown_budget_payload)
        meter._meter_bytes("terminal_reporting", "report_bytes", payload)
    meter.max_object_bytes = max(meter.max_object_bytes, len(payload))
    return {"method": method, "input_sha256": digest(spec), "output": json.loads(payload),
            "source_admission": sources,
            "admission": {"sources_complete": len(sources) == len(source_files(method)),
                          "input_complete": input_admitted},
            "invoice": meter._meter_invoice()}


def fixtures():
    p = ("atom", "p")
    r = ("atom", "r")
    quote = ("or", ("and", p, ("not", p)), ("and", r, ("not", r)))
    source0 = {"id": "q0", "frame": (("q", 0),), "weights": (("p", 1), ("r", 1))}
    common = {"schema": "p308.structural.input.v1", "kind": "paired", "atoms": ("p", "r", "q"),
              "quote": quote, "ordinary_interpretation_version": "usual-Boolean-v1",
              "baseline": (0, 0, 0), "exceptions": ("p", "r"), "preserve_baseline": True,
              "scope_version": "v1", "sources": (source0,),
              "actions": (("take_p", scale(4, bit(2))), ("take_r", scale(4, bit(0))), ("fallback", lit(3)))}
    tied = {**common, "name": "counterpossible_tied_minima"}
    external = {**common, "name": "external_sources_not_repairs", "preserve_baseline": False,
                "sources": ({"id": "q0_cheaper_rank", "frame": (("q", 0),), "weights": (("p", 1), ("r", 2))},
                            {"id": "q1_dearer_rank", "frame": (("q", 1),), "weights": (("p", 3), ("r", 2))}),
                "actions": (("act0", scale(4, bit(4))), ("act1", scale(4, not_(bit(4)))), ("fallback", lit(3)))}
    false_constant = {**common, "name": "fixed_falsity_constant_infeasible", "quote": ("bottom",)}
    routing = []
    masks = (("conditioning", "conditioning", (False, False, False, False)),
             ("occurrence", "occurrence", (False, False, False, False)),
             ("actor_replacement", "replacement", (True, False, False, False)),
             ("shared_replacement", "replacement", (True, True, False, False)),
             ("shared_and_copy", "replacement", (True, True, True, False)),
             ("shared_copy_and_new_predictor", "replacement", (True, True, True, True)))
    expense = add(lit(6), add(bit(0), add(scale(-2, bit(1)), add(scale(-1, bit(2)), scale(-2, bit(3))))))
    for name, operation, mask in masks:
        routing.append({"schema": "p308.structural.input.v1", "kind": "routing", "name": name,
                        "scope_version": "v1", "original_table": (0, 0, 1), "replacement_table": (1, 0, 1),
                        "history": 0, "call_roles": ("actor", "shared_call", "stored_copy", "predictor_of_old"),
                        "predictor_changes_only_when_explicitly_rerouted": True,
                        "sources": ({"id": name, "operation": operation,
                                     "routing": tuple(zip(("A", "B", "C", "P"), mask))},),
                        "actions": (("commit", expense), ("fallback", lit(6)))})
    return (tied, external, false_constant, *routing)


def transport_frame(*, frame_q=True, shift=0, version="v1"):
    quote = ("and", ("atom", "p"), ("not", ("atom", "p")))
    difference = K.add(K.scale(4, K.bit(2)), K.lit(-1 + shift))
    request = K.paired_request(("p", "q"), quote, (0, 0), ("p",),
                               ("q",) if frame_q else (), (), False, (("D", difference),))
    request = replace(request, scope="p308/transport/" + version,
                      metadata_json=wire({"quoted_antecedent": quote, "ordinary_interpretation": "Boolean-v1",
                                          "frame_q0": frame_q, "payoff_shift": shift,
                                          "program_version": version}))
    return M.Frame(request, "D", "U")


def ordinary_from_frame(frame):
    req = frame.request
    return NativeRequest(req.nbits, req.hard,
                         tuple((s.identity, s.formula, Fraction(s.weight), s.tier) for s in req.soft),
                         req.losses, frame.record())


def ordinary_bound(frame):
    # Public request conversion only; no legacy solver or interval evaluator.
    request = ordinary_from_frame(frame)
    ranks = []
    for state in product((0, 1), repeat=request.nbits):
        if all(ordinary_point(e, state) == 1 for e in request.hard):
            ranks.append((ordinary_rank(request, state), state))
    if not ranks:
        return {"status": "INFEASIBLE", "bound": None}
    optimum = min(rank for rank, _ in ranks)
    chosen = [state for rank, state in ranks if rank == optimum]
    expression = dict(request.losses)["D"]
    return {"status": "CHECKED_BOUND", "bound": max(ordinary_point(expression, state) for state in chosen),
            "witness": chosen[0], "optimal_rank": optimum,
            "models": chosen, "frame_record": frame.record()}


def check_bound(frame, proposed):
    exact = ordinary_bound(frame)
    if exact["status"] != "CHECKED_BOUND" or Fraction(proposed) < exact["bound"]:
        raise ValueError("Claimed bound fails the matched local finite checker.")
    return {"status": "CHECKED_BOUND", "bound": Fraction(proposed),
            "frame_record": frame.record(), "non_deterioration": Fraction(proposed) <= 0,
            "feasibility": "NONEMPTY", "coverage": "ALL_CURRENT_MINIMIZERS"}


def read_current_bound(warrant, current):
    """A retained local warrant cannot be read as evidence in a different scope."""
    if warrant["frame_record"] != current.record():
        raise StaleWarrant("Prior checked bound is stale for this complete current request.")
    return warrant


def transport_execution(meter, method):
    frames = meter._meter_run("dependency_construction", lambda: (
        transport_frame(), transport_frame(shift=2, version="repriced-v2"),
        transport_frame(frame_q=False, version="frame-withdrawn-v3")))
    old, repriced, withdrawn = frames
    meter._meter_retain("frame_records", [frame.record() for frame in frames])
    rows = []
    prior_warrant = None
    if method == "candidate":
        work = {}
        proof = meter._meter_run("search", lambda: M.build_band(old, 1, -1, work))
        cache = M.CertificateCache()
        meter._meter_run("checking", lambda: cache.admit("baseline", proof, old.record(), work))
        meter._meter_retain("retained_band_proof", proof.record())
    for index, current in enumerate(frames):
        prior_record = old.record()
        rejected_stale_read = False
        if prior_warrant is None:
            active = meter._meter_run("scope_matching", lambda: current.record() == prior_record)
        else:
            try:
                meter._meter_run("scope_matching", lambda: read_current_bound(prior_warrant, current))
                active = True
            except StaleWarrant:
                active, rejected_stale_read = False, True
        if method == "candidate":
            report = meter._meter_run("transport", lambda: cache.derive(
                "baseline", old.record(), current, (0, 1, 2, 3), (1, 1, 0, 1), work=work))
            initial = serializable(report)
            if report["status"] == "REUSE_CERTIFIED":
                bound = Fraction(report["bound"])
            else:
                # A rejected reuse is not current falsity; compute the current
                # answer while preserving the failed check and its invoice.
                request = current.request
                search = K.Search(request)
                def complete_current():
                    while search.frontier:
                        search.advance(1)
                    return search.report()
                fresh = meter._meter_run("search", complete_current)
                bound = max(fresh["losses"]["D"]["image"])
        else:
            fresh = meter._meter_run("search", lambda: ordinary_bound(current))
            bound = fresh["bound"]
            initial = {"status": "FRESH_ORDINARY_ENUMERATION"}
        checked = meter._meter_run("checking", lambda: check_bound(current, bound))
        meter._meter_retain("current_checked_bound", checked)
        prior_warrant = checked
        rows.append({"edit_index": index, "direct_prior_record_active": active,
                     "stale_prior_warrant_before_explicit_check": not active,
                     "prior_warrant_read_rejected": rejected_stale_read,
                     "initial_attempt": initial, "current": checked})
    if method == "candidate":
        before = meter.units
        try:
            meter._meter_run("checking", lambda: M.verify_band(replace(proof, bound=Fraction(-100)), old.record()))
        except M.Rejected as exc:
            rejection = {"status": "REJECTED_CHECKED_EVIDENCE", "message": str(exc),
                         "spent_units": meter.units - before, "answer_received": False,
                         "useful_action_warrant": False}
        else:
            raise AssertionError("Forged certificate was accepted.")
        if rejection["spent_units"] <= 0:
            raise AssertionError("Failed proof check erased actual work.")
    else:
        before = meter.units
        try:
            meter._meter_run("checking", lambda: check_bound(old, Fraction(-100)))
        except ValueError as exc:
            rejection = {"status": "REJECTED_CHECKED_EVIDENCE", "message": str(exc),
                         "spent_units": meter.units - before, "answer_received": False,
                         "useful_action_warrant": False}
        else:
            raise AssertionError("Ordinary false bound was accepted.")
    result = {"rows": rows, "failed_receipt": rejection}
    return result


def transport_development():
    """Same current bound service; all old construction/storage work remains paid."""
    answers = []
    for method in ("candidate", "ordinary"):
        meter = StructuralMeter()
        # Both transport arms use the same inherited typed source front end;
        # enrol its dependencies equally, even though ordinary search is separate.
        deployment_setup(meter, {"task": "fixed-quote-versioned-transport", "version": VERSION}, "candidate")
        result = meter._meter_run("controller", lambda: transport_execution(meter, method))
        # Internal proposal/check traces belong to the external experiment audit.
        # The deployed terminal service has an identical schema and byte payload.
        def terminal_record():
            return {"rows": [{k: v for k, v in row.items() if k != "initial_attempt"}
                             for row in result["rows"]],
                    "failed_receipt": {k: result["failed_receipt"][k]
                                       for k in ("status", "answer_received", "useful_action_warrant")}}
        payload = meter._meter_run("terminal_reporting", lambda: wire(terminal_record()))
        if len(payload) > MAX_OBJECT_BYTES:
            raise ValueError("Transport readout cap.")
        meter._meter_bytes("terminal_reporting", "report_bytes", payload)
        meter.max_object_bytes = max(meter.max_object_bytes, len(payload))
        answers.append({"method": method, "output": json.loads(payload),
                        "audit": result, "invoice": meter._meter_invoice()})
    current_candidate = [row["current"] for row in answers[0]["output"]["rows"]]
    current_ordinary = [row["current"] for row in answers[1]["output"]["rows"]]
    if current_candidate != current_ordinary:
        raise AssertionError("Matched current bound service differs.")
    if answers[0]["output"] != answers[1]["output"]:
        raise AssertionError("Matched terminal readout service differs.")
    if any([row["prior_warrant_read_rejected"] for row in answer["output"]["rows"]] != [False, True, True]
           for answer in answers):
        raise AssertionError("Changed scopes did not refuse a stale warrant read.")
    return {"methods": answers, "same_current_bound_outputs": True,
            "same_terminal_outputs": True,
            "claim": "Finite transport plus charged fallback; no theorem of generic economic advantage."}


def _save_json(path, value):
    path.write_text(json.dumps(serializable(value), sort_keys=True, indent=2) + "\n", encoding="utf-8")


def run_development(output_dir):
    """Write a fresh, fully source-bound development run; never overwrite a run."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    _load_legacy()
    inputs = fixtures()
    snapshots = out / "sources"
    snapshots.mkdir()
    for path in source_files("candidate"):
        (snapshots / path.name).write_bytes(path.read_bytes())
    manifest = {"schema": "p308.structural.run.v1", "version": VERSION, "stage": STAGE,
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "python": sys.version, "platform": platform.platform(), "tariff": TARIFF,
                "source_files": [{"path": str(path.relative_to(ROOT)), "snapshot": "sources/" + path.name,
                                  "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                  "bytes": len(path.read_bytes())}
                                 for path in source_files("candidate")],
                "fixture_input_sha256": digest(inputs), "fixture_count": len(inputs),
                "terminal_reserve": TERMINAL_RESERVE, "success_budget": SUCCESS_BUDGET,
                "failure_readout_reserve": FAILURE_READOUT_RESERVE,
                "admission_contract": "Exact integer budget >= TERMINAL_RESERVE; nine published fixtures only.",
                "limits": {"support_bits": 6, "source_cases": 2, "actions": 3,
                           "normality_weight_magnitude": 8, "rational_bits": MAX_RATIONAL_BITS,
                           "worker_object_bytes": MAX_OBJECT_BYTES},
                "parallel_principal_credit_ns": 0,
                "final_freeze": False, "final_evaluation": False,
                "native_tariff_scope": __doc__}
    _save_json(out / "manifest.json", manifest)
    _save_json(out / "inputs.json", inputs)
    records = []
    started = time.monotonic_ns()
    try:
        for spec in inputs:
            pair = [run_method(spec, method) for method in ("candidate", "ordinary")]
            if pair[0]["output"] != pair[1]["output"]:
                raise AssertionError("Candidate/control mismatch on " + spec["name"])
            if any(row["output"]["status"] != "SUCCESS" for row in pair):
                raise AssertionError("Success fixture unexpectedly exhausted resources.")
            record = {"name": spec["name"], "equal_outputs": True, "methods": pair,
                      "ordinary_minus_candidate_units": pair[1]["invoice"]["total_units"] - pair[0]["invoice"]["total_units"]}
            records.append(record)
            with (out / "completed_units.jsonl").open("a", encoding="utf-8") as file:
                file.write(wire(record) + "\n")
        # Prospectively fixed 2,000-opcode/native-call remainder after explicit
        # source/input admission; the reserve must still produce UNKNOWN.
        budgeted = []
        for method in ("candidate", "ordinary"):
            spec = inputs[0]
            admission = sum(len(path.read_bytes()) for path in source_files(method)) + len(wire(spec))
            failure = run_method(spec, method, budget=admission + TERMINAL_RESERVE + 2000)
            if failure["output"]["status"] != "UNKNOWN_BUDGET" or failure["invoice"]["total_units"] <= admission:
                raise AssertionError("Required spent-prefix budget failure is missing.")
            budgeted.append(failure)
        _save_json(out / "budget_failures.json", budgeted)
        transport = transport_development()
        _save_json(out / "transport.json", transport)
        # These expectations were fixed in fixtures()/plan; no cases are omitted.
        tie = records[0]["methods"][0]["output"]
        external = records[1]["methods"][0]["output"]
        assert len(tie["sources"][0]["models"]) == 2
        assert tie["decision"]["fixed_action_worst_loss"] == "3"
        assert tie["decision"]["nonimplementable_pointwise_action_oracle"] == "0"
        assert external["decision"]["fixed_action_worst_loss"] == "3"
        assert external["decision"]["forbidden_joint_source_repair_minimum"]["minimum_fixed_loss"] == "0"
        assert all(row["methods"][0]["output"].get("ordinary_satisfying_valuations", 0) == 0 for row in records[:3])
        summary = {"schema": "p308.structural.summary.v1", "stage": STAGE, "version": VERSION,
                   "fixture_count": len(records), "equal_output_pairs": sum(r["equal_outputs"] for r in records),
                   "all_completed": True, "budget_failure_methods": len(budgeted),
                   "transport_same_current_bounds": transport["same_current_bound_outputs"],
                   "tied_optimum_count": 2, "fixed_action_worst_loss": "3",
                   "nonimplementable_pointwise_oracle_loss": "0",
                   "unresolved_source_joint_minimization_rejected": True,
                   "finite_comparison": [{"name": row["name"],
                                           "candidate_units": row["methods"][0]["invoice"]["total_units"],
                                           "ordinary_units": row["methods"][1]["invoice"]["total_units"],
                                           "equal_outputs": row["equal_outputs"]} for row in records],
                   "observed_run_elapsed_ns": time.monotonic_ns() - started,
                   "observed_run_elapsed_is_principal_credit": False,
                   "method_selection_after_observation": False,
                   "conclusion": "All finite answers match the independent ordinary solver; semantic/source/action boundaries survive integration. No generic superiority or final-evaluation result.",
                   "ordinary_shared_adapter_control": "Ordinary methods may use the same accepted repair/transport library. With identical code and inputs their outputs and this tariff's invoice are identical by construction; no duplicate run is treated as additional evidence."}
        _save_json(out / "summary.json", summary)
        _save_json(out / "results.json", {"units": records, "budget_failures": budgeted, "transport": transport})
        return summary
    except BaseException as exc:
        _save_json(out / "failure.json", {"type": type(exc).__name__, "message": str(exc),
                                          "traceback": traceback.format_exc(), "completed_units": len(records),
                                          "stage": STAGE, "version": VERSION})
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(json.dumps(run_development(args.out), sort_keys=True, indent=2))
