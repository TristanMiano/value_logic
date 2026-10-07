"""Finite bounded information/update kernel; DEVELOPMENT, P3-03.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-07.
The kernel allowance counts capped transactions, not equal CPU instructions.
Parsing/validation and serialization are separate recorded boundary work.
No point prior, arbitrary-arithmetic checker, or value-of-computation oracle.
"""
from __future__ import annotations

from collections import Counter, deque
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import re


LIMITS = dict(atoms=12, cells=4096, constraints=128, expr_nodes=256,
              expr_depth=48, program=64, registers=4, horizon=100000,
              input_bits=64, rational_bits=4096, input_bytes=1_000_000,
              input_nodes=100000, input_depth=64)
VM_VERSION = "nat-register-v1"
KERNEL_VERSION = "finite-cover-v2"
REPORT_VERSION = "finite-cover-report-v2"


class InputError(ValueError):
    pass


class ResourceLimit(ValueError):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise InputError("integer outside admitted range")
    return value


def label(value):
    if not isinstance(value, str) or not 1 <= len(value) <= 128:
        raise InputError("invalid version or identifier")
    return value


def rational(value):
    # Validate syntax and digit counts before Fraction can construct powers.
    # In particular, a short scientific-notation exponent is not an input cap.
    if not isinstance(value, str) or re.fullmatch(
            r"[+-]?[0-9]{1,20}(?:/[1-9][0-9]{0,19})?", value) is None:
        raise InputError("rational input must be a bounded integer or integer/positive-integer string")
    try:
        q = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise InputError("invalid rational") from exc
    if max(abs(q.numerator).bit_length(), q.denominator.bit_length()) > LIMITS["input_bits"]:
        raise InputError("rational literal exceeds input bit cap")
    return q


def admitted_data(value):
    """Bound traversal before JSON encoding/deepcopy of a caller-owned object.

    This does not charge or bound how the caller constructed that object.
    Repeated containers count per occurrence; cycles hit the depth/node cap.
    """
    stack = [(value, 0)]
    nodes = scalar_bytes = 0
    while stack:
        item, depth = stack.pop()
        nodes += 1
        if nodes > LIMITS["input_nodes"] or depth > LIMITS["input_depth"]:
            raise InputError("input traversal limit")
        if isinstance(item, dict):
            if len(item) > LIMITS["input_nodes"] - nodes:
                raise InputError("input object limit")
            for key, child in item.items():
                if not isinstance(key, str):
                    raise InputError("input keys must be strings")
                scalar_bytes += len(key)
                stack.append((child, depth + 1))
        elif isinstance(item, list):
            if len(item) > LIMITS["input_nodes"] - nodes:
                raise InputError("input array limit")
            stack.extend((child, depth + 1) for child in item)
        elif isinstance(item, str):
            scalar_bytes += len(item)
        elif type(item) is int:
            if abs(item).bit_length() > LIMITS["input_bits"]:
                raise InputError("input integer bit cap")
        elif item is not None and type(item) is not bool:
            raise InputError("input must use JSON-compatible finite types")
        if scalar_bytes > LIMITS["input_bytes"] or len(stack) + nodes > LIMITS["input_nodes"]:
            raise InputError("input traversal/size limit")
    raw = canonical(value)
    if len(raw) > LIMITS["input_bytes"]:
        raise InputError("input byte cap")
    return raw, nodes


def validate_expr(expr, atoms, kind, depth=0, count=None):
    count = [0] if count is None else count
    count[0] += 1
    if count[0] > LIMITS["expr_nodes"] or depth > LIMITS["expr_depth"]:
        raise InputError("expression size limit")
    if not isinstance(expr, list) or not expr or not isinstance(expr[0], str):
        raise InputError("expression must be an operator list")
    op = expr[0]
    if op == "var" and len(expr) == 2:
        integer(expr[1], 0, atoms - 1)
    elif kind == "bool" and op == "bool" and len(expr) == 2:
        integer(expr[1], 0, 1)
    elif kind == "loss" and op == "rat" and len(expr) == 2:
        rational(expr[1])
    elif kind == "bool" and op == "not" and len(expr) == 2:
        validate_expr(expr[1], atoms, kind, depth + 1, count)
    elif kind == "loss" and op == "scale" and len(expr) == 3:
        rational(expr[1])
        validate_expr(expr[2], atoms, kind, depth + 1, count)
    elif ((kind == "bool" and op in {"and", "or"}) or
          (kind == "loss" and op in {"add", "min", "max", "resid"})) and len(expr) == 3:
        validate_expr(expr[1], atoms, kind, depth + 1, count)
        validate_expr(expr[2], atoms, kind, depth + 1, count)
    else:
        raise InputError("unsupported operator, type, or arity")
    return count[0]


def validate_query(q):
    if not isinstance(q, dict):
        raise InputError("query must be an object")
    label(q.get("id")); label(q.get("version"))
    if q.get("kind") == "opaque":
        if set(q) != {"id", "version", "kind", "statement"}:
            raise InputError("opaque query fields")
        if not isinstance(q["statement"], str) or len(q["statement"]) > 2048:
            raise InputError("opaque statement limit")
        return
    if q.get("kind") != "bounded_run" or set(q) != {
            "id", "version", "kind", "program", "registers", "horizon", "target"}:
        raise InputError("unsupported query kind or fields")
    p, regs = q["program"], q["registers"]
    if not isinstance(p, list) or not 1 <= len(p) <= LIMITS["program"]:
        raise InputError("program size")
    if not isinstance(regs, list) or not 1 <= len(regs) <= LIMITS["registers"]:
        raise InputError("register count")
    for r in regs:
        integer(r, 0, 2 ** LIMITS["input_bits"] - 1)
    integer(q["horizon"], 0, LIMITS["horizon"]); integer(q["target"], 0, 1)
    for ins in p:
        if not isinstance(ins, list) or not ins:
            raise InputError("instruction syntax")
        if ins[0] == "INC" and len(ins) == 2:
            integer(ins[1], 0, len(regs) - 1)
        elif ins[0] == "DECJZ" and len(ins) == 3:
            integer(ins[1], 0, len(regs) - 1); integer(ins[2], 0, len(p) - 1)
        elif ins[0] == "JUMP" and len(ins) == 2:
            integer(ins[1], 0, len(p) - 1)
        elif ins[0] == "HALT" and len(ins) == 2:
            integer(ins[1], 0, 1)
        else:
            raise InputError("unsupported instruction")
    if p[-1][0] not in {"HALT", "JUMP"}:
        raise InputError("last instruction must prevent fall-through")


def tri(expr, cube, work):
    work["bool_nodes"] += 1
    op = expr[0]
    if op == "var":
        work["coordinate_reads"] += 1
        return cube[expr[1]]
    if op == "bool":
        return expr[1]
    if op == "not":
        a = tri(expr[1], cube, work)
        return None if a is None else 1 - a
    a, b = tri(expr[1], cube, work), tri(expr[2], cube, work)
    if op == "and":
        return 0 if 0 in (a, b) else (1 if a == b == 1 else None)
    return 1 if 1 in (a, b) else (0 if a == b == 0 else None)


def bounded_arithmetic(op, a, b, work):
    bits = max(abs(a.numerator).bit_length(), a.denominator.bit_length(),
               abs(b.numerator).bit_length(), b.denominator.bit_length(), 1)
    work["rational_operations"] += 1
    work["rational_operand_bits_sum"] += bits
    work["max_rational_operand_bits"] = max(work["max_rational_operand_bits"], bits)
    # Check a conservative unreduced result-size bound before allocation.
    if 2 * bits + 2 > LIMITS["rational_bits"]:
        raise ResourceLimit("rational intermediate cap")
    if op == "add":
        return a + b
    if op == "sub":
        return a - b
    return a * b


def interval(expr, cube, work):
    work["loss_nodes"] += 1
    op = expr[0]
    if op == "var":
        work["coordinate_reads"] += 1
        x = cube[expr[1]]
        return (Fraction(0), Fraction(1)) if x is None else (Fraction(x), Fraction(x))
    if op == "rat":
        q = rational(expr[1])
        work["rational_literal_reads"] += 1
        return q, q
    if op == "scale":
        q = rational(expr[1]); a, b = interval(expr[2], cube, work)
        lo, hi = (a, b) if q >= 0 else (b, a)
        return bounded_arithmetic("mul", q, lo, work), bounded_arithmetic("mul", q, hi, work)
    a, b = interval(expr[1], cube, work), interval(expr[2], cube, work)
    if op == "add":
        return bounded_arithmetic("add", a[0], b[0], work), bounded_arithmetic("add", a[1], b[1], work)
    if op == "min":
        work["rational_comparisons"] += 2
        return min(a[0], b[0]), min(a[1], b[1])
    if op == "max":
        work["rational_comparisons"] += 2
        return max(a[0], b[0]), max(a[1], b[1])
    lo = bounded_arithmetic("sub", a[0], b[1], work)
    hi = bounded_arithmetic("sub", a[1], b[0], work)
    work["rational_comparisons"] += 2
    return max(Fraction(0), lo), max(Fraction(0), hi)


def vm_initial(q):
    return dict(pc=0, regs=list(q["registers"]), steps=0, halted=False, output=None)


def vm_finished(q, state):
    return state["halted"] or state["steps"] >= q["horizon"]


def vm_transition(q, state, work):
    if vm_finished(q, state):
        return
    ins = q["program"][state["pc"]]
    work["vm_instructions"] += 1
    op = ins[0]
    if op == "INC":
        work["register_operand_bits"] += max(1, state["regs"][ins[1]].bit_length())
        state["regs"][ins[1]] += 1; state["pc"] += 1
    elif op == "DECJZ":
        r = ins[1]
        work["register_operand_bits"] += max(1, state["regs"][r].bit_length())
        if state["regs"][r] == 0:
            state["pc"] = ins[2]
        else:
            state["regs"][r] -= 1; state["pc"] += 1
    elif op == "JUMP":
        state["pc"] = ins[1]
    else:
        state["halted"] = True; state["output"] = ins[1]
    state["steps"] += 1


def receipt(q, state):
    return dict(query_sha256=digest(q), query_id=q["id"], vm_version=VM_VERSION,
                answer=int(state["halted"] and state["output"] == q["target"]),
                executed=state["steps"], halted=state["halted"], output=state["output"],
                terminal_sha256=digest(state))


class Kernel:
    """A finite operational instance, with explicit conditional-source semantics.

    Calls are interrupted only between complete transactions. A Python process
    crash inside a transaction is outside this in-memory call-boundary guarantee.
    Audit snapshots are not self-authenticating proofs or a free restore oracle.
    """
    def __init__(self, config):
        if not isinstance(config, dict):
            raise InputError("configuration must be an object")
        if set(config) != {"scope", "queries", "constraints", "losses", "cell_cap"}:
            raise InputError("configuration fields")
        raw, input_nodes = admitted_data(config)
        self.original = deepcopy(config)
        self.input_sha256 = hashlib.sha256(raw).hexdigest()
        self.scope = label(config["scope"])
        self.queries = deepcopy(config["queries"])
        if not isinstance(self.queries, list) or not 1 <= len(self.queries) <= LIMITS["atoms"]:
            raise InputError("active atom cap")
        for q in self.queries:
            validate_query(q)
        if len({q["id"] for q in self.queries}) != len(self.queries):
            raise InputError("duplicate query identifiers")
        self.cell_cap = integer(config["cell_cap"], 1, LIMITS["cells"])
        self.work = Counter(setup_input_bytes=len(raw), setup_input_nodes=input_nodes,
                            setup_validation_nodes=0)
        self.constraints = {}
        if not isinstance(config["constraints"], list):
            raise InputError("constraints must be a list")
        for h in config["constraints"]:
            self._validate_constraint(h)
            self.constraints[h["id"]] = deepcopy(h)
        self.losses = deepcopy(config["losses"])
        if not isinstance(self.losses, dict) or not 1 <= len(self.losses) <= 16:
            raise InputError("loss catalogue cap")
        for name, loss in self.losses.items():
            label(name)
            if not isinstance(loss, dict) or set(loss) != {"unit", "version", "expr"}:
                raise InputError("loss fields")
            label(loss["unit"]); label(loss["version"])
            self.work["setup_validation_nodes"] += validate_expr(loss["expr"], self.k, "loss")
        self.source_epoch = 0
        self.objective_epoch = 0
        self.cover_revision = 0
        self.event = 0
        self.cells = {0: (None,) * self.k}
        self.work["peak_cells"] = 1
        self.next_cell = 1
        self.agenda = deque([0])
        self.witness = (0,) * self.k if not self.constraints else None
        self.known = {}
        self.jobs = [self._new_job(q) for q in self.queries]
        self.cursor = 0
        self.last_event = None
        self.work["setup_coordinate_writes"] += self.k

    @property
    def k(self):
        return len(self.queries)

    def _new_job(self, q):
        return None if q["kind"] == "opaque" else dict(
            phase="produce", disposition="production_pending", vm=vm_initial(q), candidate=None)

    def _validate_constraint(self, h, boundary="setup"):
        if not isinstance(h, dict) or set(h) != {"id", "expr", "kind", "depends_on"}:
            raise InputError("constraint fields")
        label(h["id"])
        if h["id"].startswith("vm:") or h["id"] in self.constraints:
            raise InputError("reserved or duplicate evidence identifier")
        if h["kind"] != "conditional_assumption":
            raise InputError("only explicitly conditional caller premises are admitted here")
        if len(self.constraints) >= LIMITS["constraints"]:
            raise ResourceLimit("constraint capacity")
        if (not isinstance(h["depends_on"], list) or
                any(not isinstance(d, str) for d in h["depends_on"]) or
                len(h["depends_on"]) != len(set(h["depends_on"]))):
            raise InputError("dependency list")
        if any(d not in self.constraints for d in h["depends_on"]):
            raise InputError("dependency not active; forward/cyclic references not admitted")
        self.work[boundary + "_validation_nodes"] += validate_expr(h["expr"], self.k, "bool")

    def _event(self, kind, detail=None):
        # Cumulative counters are not fixed-width RAM. Their bit lengths are
        # exposed; no constant-CPU or fixed-total-memory theorem is asserted.
        self.work["control_operand_bits"] += sum(max(1, n.bit_length()) for n in
            (self.event, self.source_epoch, self.objective_epoch, self.cover_revision,
             self.cursor, self.next_cell))
        self.event += 1
        self.work["kernel_transactions"] += 1
        self.work["transaction_" + kind] += 1
        self.last_event = dict(event=self.event, kind=kind, detail=detail,
                               source_epoch=self.source_epoch, objective_epoch=self.objective_epoch)

    def source_record(self):
        """Full represented source; returned reports make their own historical copy."""
        return dict(vm_version=VM_VERSION, queries=self.queries, constraints=self.constraints)

    def source_identity(self):
        """Audit fingerprint; exact current-warrant checks compare full records."""
        raw = canonical(self.source_record())
        self.work["identity_bytes_hashed"] += len(raw)
        return hashlib.sha256(raw).hexdigest()

    def cover_identity(self):
        raw = canonical({str(i): list(c) for i, c in self.cells.items()})
        self.work["identity_bytes_hashed"] += len(raw)
        return hashlib.sha256(raw).hexdigest()

    def _overlay(self):
        known = {}
        for h in self.constraints.values():
            self.work["literal_records_scanned"] += 1
            e = h["expr"]
            item = (e[1], 1) if e[0] == "var" else None
            if e[0] == "not" and e[1][0] == "var":
                item = (e[1][1], 0)
            if item is not None:
                i, b = item
                if i in known and known[i] != b:
                    return None
                known[i] = b
        return known

    def _effective(self, cube, overlay):
        result = list(cube)
        for i, bit in overlay.items():
            self.work["coordinate_reads"] += 1
            if result[i] is not None and result[i] != bit:
                return None
            result[i] = bit
            self.work["coordinate_writes"] += 1
        return tuple(result)

    def _source_step(self):
        cid = self.agenda.popleft()
        cube = self.cells[cid]
        rejected = None
        for hid, h in self.constraints.items():
            if tri(h["expr"], cube, self.work) == 0:
                rejected = hid
                break
        if rejected is not None:
            del self.cells[cid]
            self.cover_revision += 1
            self._event("prune", dict(cell=cid, cube=list(cube), evidence=rejected))
        elif None not in cube:
            self.witness = cube
            self._event("feasible_leaf", dict(cell=cid, cube=list(cube)))
        elif len(self.cells) >= self.cell_cap:
            self.agenda.append(cid)
            self._event("capacity_stop", dict(cell=cid, cap=self.cell_cap))
        else:
            i = cube.index(None)
            left, right = list(cube), list(cube)
            left[i], right[i] = 0, 1
            # Both children exist before the single observable replacement.
            a, b = self.next_cell, self.next_cell + 1
            children = {a: tuple(left), b: tuple(right)}
            self.work["coordinate_writes"] += 2 * self.k
            self.cells.update(children)
            del self.cells[cid]
            self.next_cell += 2
            self.cover_revision += 1
            self.agenda.extend([a, b])
            self._event("split", dict(parent=cid, cube=list(cube), children=[a, b], coordinate=i))
        self.work["peak_cells"] = max(self.work["peak_cells"], len(self.cells))

    def _job_step(self, i):
        q, job = self.queries[i], self.jobs[i]
        phase = job["phase"]
        if phase == "produce":
            vm_transition(q, job["vm"], self.work)
            self._event("produce", dict(query=q["id"], executed=job["vm"]["steps"]))
            if vm_finished(q, job["vm"]):
                candidate = receipt(q, job["vm"])
                job.update(phase="check", candidate=candidate, vm=vm_initial(q),
                           produced_event=self.event, disposition="checking_pending")
                self.work["receipt_bytes_created"] += len(canonical(candidate))
        elif phase in {"check", "capacity"}:
            candidate = job["candidate"]
            if (candidate.get("query_sha256") != digest(q) or candidate.get("query_id") != q["id"]
                    or candidate.get("vm_version") != VM_VERSION):
                job["phase"] = "rejected"
                job["disposition"] = "request_binding_rejected"
                self._event("receipt_rejected", dict(query=q["id"], reason="original request binding"))
                return
            vm_transition(q, job["vm"], self.work)
            self._event("check", dict(query=q["id"], executed=job["vm"]["steps"]))
            if vm_finished(q, job["vm"]):
                expected = receipt(q, job["vm"])
                if canonical(candidate) != canonical(expected):
                    job["phase"] = "rejected"
                    job["disposition"] = "false_receipt_rejected"
                    self.last_event["detail"]["disposition"] = "false_receipt"
                    return
                if len(self.constraints) >= LIMITS["constraints"]:
                    job["phase"] = "capacity"
                    job["disposition"] = "evidence_capacity_blocked"
                    self.last_event["detail"]["disposition"] = "evidence_capacity"
                    return
                # Immutable admitted position disambiguates even equal hashes.
                # The digest is an audit suffix, not the evidence's sole key.
                rid = f"vm:{i}:{digest(q)}"
                bit = expected["answer"]
                self.constraints[rid] = dict(id=rid, expr=["var", i] if bit else ["not", ["var", i]],
                                            kind="checked_vm", depends_on=[])
                self.known[q["id"]] = dict(answer=bit, evidence=rid, accepted_event=self.event,
                                            produced_event=job["produced_event"], query_sha256=digest(q))
                job["phase"] = "done"
                job["disposition"] = "checked_answer_accepted"
                self.source_epoch += 1
                self.agenda = deque(self.cells)
                self.witness = None
                self.work["agenda_entries_written"] += len(self.cells)
                self.last_event["source_epoch"] = self.source_epoch
                self.last_event["detail"]["disposition"] = "accepted_signed_answer"

    def run(self, allowance, mode="all"):
        """Consume at most allowance capped transactions; retain partial jobs."""
        integer(allowance, 0, 1_000_000)
        if not isinstance(mode, str) or mode not in {"all", "source", "evidence"}:
            raise InputError("scheduling mode")
        used = 0
        for _ in range(allowance):
            selected = None
            for _ in range(self.k + 1):
                slot = self.cursor % (self.k + 1)
                self.cursor += 1
                self.work["dispatch_checks"] += 1
                if slot == 0 and mode != "evidence" and self.agenda:
                    selected = ("source", 0); break
                if slot and mode != "source":
                    job = self.jobs[slot - 1]
                    if job is not None and job["phase"] in {"produce", "check", "capacity"}:
                        selected = ("job", slot - 1); break
            if selected is None:
                break
            if selected[0] == "source":
                self._source_step()
            else:
                self._job_step(selected[1])
            used += 1
        return dict(allowance=allowance, used_transactions=used,
                    outcome="ALLOWANCE_EXHAUSTED" if used == allowance else "NO_SCHEDULED_WORK")

    def add_assumption(self, h, allowance=1):
        integer(allowance, 1, 1_000_000)
        raw, nodes = admitted_data(h)
        self.work["update_input_bytes"] += len(raw)
        self.work["update_input_nodes"] += nodes
        self._validate_constraint(h, "update")
        self.constraints[h["id"]] = deepcopy(h)
        self.source_epoch += 1
        self.agenda = deque(self.cells)
        self.witness = None
        self.work["agenda_entries_written"] += len(self.cells)
        self._event("add_conditional_assumption", h["id"])

    def withdraw(self, hid, allowance=1):
        integer(allowance, 1, 1_000_000)
        label(hid)
        if hid not in self.constraints:
            raise InputError("unknown active evidence")
        removed = {hid}
        while True:
            more = {i for i, h in self.constraints.items() if any(d in removed for d in h["depends_on"])}
            self.work["dependency_records_scanned"] += len(self.constraints)
            if more <= removed:
                break
            removed |= more
        self.constraints = {i: h for i, h in self.constraints.items() if i not in removed}
        for i, q in enumerate(self.queries):
            k = self.known.get(q["id"])
            if k is not None and k["evidence"] in removed:
                del self.known[q["id"]]
                self.jobs[i] = self._new_job(q)
        self.cells = {self.next_cell: (None,) * self.k}
        self.next_cell += 1
        self.agenda = deque(self.cells)
        self.source_epoch += 1
        self.cover_revision += 1
        self.witness = (0,) * self.k if not self.constraints else None
        self.work["coordinate_writes"] += self.k
        self._event("withdraw_and_reset", sorted(removed))
        return sorted(removed)

    def change_loss(self, name, loss, allowance=1):
        integer(allowance, 1, 1_000_000)
        label(name)
        if name not in self.losses or not isinstance(loss, dict) or set(loss) != {"unit", "version", "expr"}:
            raise InputError("loss update fields")
        raw, nodes = admitted_data(loss)
        self.work["update_input_bytes"] += len(raw)
        self.work["update_input_nodes"] += nodes
        label(loss["unit"]); label(loss["version"])
        self.work["update_validation_nodes"] += validate_expr(loss["expr"], self.k, "loss")
        self.losses[name] = deepcopy(loss)
        self.objective_epoch += 1
        self._event("change_objective", name)

    def report(self, name, allowance=1):
        integer(allowance, 1, 1_000_000)
        label(name)
        if name not in self.losses:
            raise InputError("unknown loss")
        self._event("report", name)
        loss = self.losses[name]
        overlay = self._overlay()
        effective = []
        if overlay is not None:
            for c in self.cells.values():
                d = self._effective(c, overlay)
                if d is not None:
                    effective.append(d)
        status, bounds = "CONDITIONAL_OUTER_BOUND", None
        if not effective:
            status = "FINITE_CONFLICT"
        else:
            try:
                values = [interval(loss["expr"], c, self.work) for c in effective]
                self.work["rational_comparisons"] += 2 * max(0, len(values) - 1)
                bounds = [str(min(a for a, _ in values)), str(max(b for _, b in values))]
            except ResourceLimit:
                status = "ARITHMETIC_LIMIT"
        exact_source = not self.agenda and all(None not in c for c in self.cells.values())
        result = dict(kernel_version=KERNEL_VERSION, vm_version=VM_VERSION, report_version=REPORT_VERSION,
                      input_sha256=self.input_sha256,
                      scope=self.scope, source_epoch=self.source_epoch, objective_epoch=self.objective_epoch,
                      active_source_sha256=self.source_identity(), source_record=self.source_record(),
                      cover_revision=self.cover_revision, cover_sha256=self.cover_identity(),
                      event=self.event, loss=name, loss_sha256=digest(loss), loss_record=loss, unit=loss["unit"],
                      status=status, bounds=bounds, source_exactly_filtered=exact_source,
                      feasibility="CONFLICT" if not effective else ("WITNESS" if self.witness is not None else "UNRESOLVED"),
                      witness=list(self.witness) if self.witness is not None else None,
                      assumptions=[i for i, h in self.constraints.items() if h["kind"] == "conditional_assumption"],
                      active_evidence=list(self.constraints),
                      coordinates={q["id"]: {"status": "CHECKED_TRUE" if self.known[q["id"]]["answer"] else "CHECKED_FALSE",
                                                **self.known[q["id"]]} if q["id"] in self.known else {"status": "UNRESOLVED"}
                                   for q in self.queries},
                      processes={q["id"]: {"phase": job["phase"], "disposition": job["disposition"],
                                            "executed_in_current_phase": job["vm"]["steps"]}
                                 if job is not None else {"phase": "unsupported", "disposition": "no_executable_producer"}
                                 for q, job in zip(self.queries, self.jobs)},
                      unresolved_default="no point probability; full Boolean possibility unless constrained",
                      resource_snapshot="after mathematical report work; before this report's JSON serialization",
                      resource_account=dict(self.work))
        self.work["report_bytes_created"] += len(canonical(result))
        return deepcopy(result)

    def report_is_current(self, report):
        """Check the current warrant, not whether refinement has made a tighter report.

        Exact canonical source/loss records determine represented applicability.
        Their encoding/comparison is boundary work outside run's allowance;
        fingerprints remain audit references. This does not authenticate JSON,
        verify numeric bounds, or establish exact execution-lineage identity.
        """
        if (not isinstance(report, dict) or report.get("scope") != self.scope or
                report.get("kernel_version") != KERNEL_VERSION or report.get("vm_version") != VM_VERSION or
                report.get("report_version") != REPORT_VERSION or
                report.get("source_epoch") != self.source_epoch or report.get("objective_epoch") != self.objective_epoch):
            return False
        name = report.get("loss")
        if not isinstance(name, str) or name not in self.losses:
            return False
        try:
            old_source, current_source = canonical(report.get("source_record")), canonical(self.source_record())
            old_loss, current_loss = canonical(report.get("loss_record")), canonical(self.losses[name])
        except (TypeError, ValueError, RecursionError):
            return False
        self.work["identity_record_comparisons"] += 2
        self.work["identity_comparison_byte_envelope"] += max(len(old_source), len(current_source)) + max(len(old_loss), len(current_loss))
        return old_source == current_source and old_loss == current_loss

    def snapshot(self):
        """Audit copy only. Serialization cost is separate from run's allowance."""
        s = dict(kernel_version=KERNEL_VERSION, vm_version=VM_VERSION, report_version=REPORT_VERSION, limits=LIMITS,
                 original_input_sha256=self.input_sha256, scope=self.scope,
                 source_epoch=self.source_epoch, objective_epoch=self.objective_epoch,
                 active_source_sha256=self.source_identity(),
                 cover_revision=self.cover_revision, cover_sha256=self.cover_identity(),
                 queries=self.queries, constraints=self.constraints, losses=self.losses,
                 cells={str(i): list(c) for i, c in self.cells.items()}, agenda=list(self.agenda),
                 next_cell=self.next_cell, cell_cap=self.cell_cap, witness=self.witness,
                 known=self.known, jobs=self.jobs, cursor=self.cursor,
                 event=self.event, last_event=self.last_event,
                 resource_snapshot="before this audit snapshot's JSON serialization",
                 resource_account=dict(self.work))
        data = canonical(s)
        self.work["audit_serialization_bytes"] += len(data)
        return json.loads(data)
