#!/usr/bin/env python3
"""Recorded ordinary ADD evidence producer; R-P3-B-B DEVELOPMENT.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
The inherited ADD and portfolio sources are unchanged. The independent receiver
is 05_add_evidence_check.py. Only the explicit verified-domain adapter imports
and invokes that checker; ordinary production does not call it. Untrusted
producer output gains authority only after independent receipt.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import gcd
from pathlib import Path
import sys

sys.dont_write_bytecode = True


def _load(name, filename):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    if spec is None or spec.loader is None:
        raise ImportError("Missing pinned ADD evidence dependency: " + filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


A = _load("_rp3bb_ordinary_add", "05_ordinary_add.py")
P = _load("_rp3bb_portfolio", "05_portfolio_transport.py")
M, K = A.M, A.K
assert P.M is M

VERSION = "rp3bb-add-evidence-v1"
SCHEMA = "rp3bb.add-evidence.v1"
SOURCE_SCHEMA = "rp3bb.add-evidence-source.v1"
MAX_BITS = 10
MAX_NODES = 100000
MAX_APPLIES = 200000
MAX_EXPRESSIONS = 200000
MAX_CHUNKS = 256
MAX_WIRE_BYTES = 32 * 1024 * 1024
MAX_SOURCE_BYTES = 1024 * 1024
MAX_CURRENT_BYTES = 8 * 1024 * 1024
MAX_EXPRESSION_BYTES = 256 * 1024
MAX_EPOCH_CHARS = 256
MAX_OUTER_DEPTH = 12
MAX_TERMINAL_BITS = 4096
MAX_BOUND_BITS = 128
MAX_SOURCE_FILES = 64
MAX_SOURCE_PATH_BYTES = 4096
OPERATORS = frozenset(("add", "mul", "min", "max", "eq", "le", "gt", "and", "or", "sub"))
COMMUTATIVE = frozenset(("add", "mul", "min", "max", "eq", "and", "or"))
DEFAULT_SOURCE_PATHS = (
    "v3/checks/04_counterfactual_repair.py",
    "v3/checks/05_counterfactual_transport.py",
    "v3/checks/05_portfolio_transport.py",
    "v3/checks/05_ordinary_add.py",
    "v3/checks/05_add_evidence.py",
    "v3/checks/05_add_evidence_check.py",
)


class EvidenceRejected(M.Rejected):
    """Malformed or incompatible producer/wire input; no certified answer."""


class EvidenceLimit(EvidenceRejected):
    """Paid cap failure, not falsity of the mathematical claim."""


class NoBoundProof(ValueError):
    """The ordinary computation found a violating current-sublevel point."""
    def __init__(self, counterexample, current_record, bound):
        self.counterexample = counterexample
        self.current_record = current_record
        self.bound = bound
        super().__init__("Requested current bound fails at " + str(counterexample))


def inc(work, name, amount=1):
    if work is not None:
        work[name] = work.get(name, 0) + amount


def _integer(value, low=0, high=None):
    if type(value) is not int or value < low or (high is not None and value > high):
        raise EvidenceRejected("Exact bounded integer required.")
    return value


def _text(value, max_bytes, *, nonempty=True):
    if type(value) is not str or (nonempty and not value):
        raise EvidenceRejected("Exact text required.")
    try:
        length = len(value.encode("utf-8"))
    except UnicodeError as error:
        raise EvidenceRejected("Invalid UTF-8 text.") from error
    if length > max_bytes:
        raise EvidenceLimit("Text byte cap.")
    return value


def _rational_pair(value, bits):
    if type(value) is not tuple or len(value) != 2:
        raise EvidenceRejected("Immutable rational pair required.")
    numerator, denominator = value
    if type(numerator) is not int or type(denominator) is not int or denominator <= 0:
        raise EvidenceRejected("Exact signed numerator and positive denominator required.")
    if max(abs(numerator).bit_length(), denominator.bit_length()) > bits:
        raise EvidenceLimit("Evidence rational component cap.")
    if gcd(abs(numerator), denominator) != 1:
        raise EvidenceRejected("Reduced rational pair required.")
    return value


def _pair(value, bits=MAX_TERMINAL_BITS):
    if type(value) not in (int, F):
        raise EvidenceRejected("Exact computed rational required.")
    q = F(value)
    return _rational_pair((q.numerator, q.denominator), bits)


def _header(source_record, epoch, bits, order):
    _text(source_record, MAX_SOURCE_BYTES)
    _text(epoch, MAX_SOURCE_BYTES)
    if len(epoch) > MAX_EPOCH_CHARS:
        raise EvidenceLimit("Epoch character cap.")
    _integer(bits, 1, MAX_BITS)
    if (type(order) is not tuple or len(order) != bits
            or any(type(index) is not int for index in order)
            or set(order) != set(range(bits))):
        raise EvidenceRejected("Exact complete input permutation required.")


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def make_source_record(paths=None, *, repo_root=None, work=None):
    """Read and bind the actual complete source closure, never a supplied digest.

    The caller independently supplies this resulting full record to the receiver.
    Default sources include both new files; they must already exist. Extra shared
    outer-service sources may be included by supplying their complete path set.
    """
    root = Path(__file__).resolve().parents[2] if repo_root is None else Path(repo_root).resolve()
    paths = DEFAULT_SOURCE_PATHS if paths is None else tuple(paths)
    if not 1 <= len(paths) <= MAX_SOURCE_FILES:
        raise EvidenceLimit("Source closure file-count cap.")
    entries, seen = [], set()
    for supplied in paths:
        path = (root / supplied).resolve()
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError as error:
            raise EvidenceRejected("Source path lies outside the declared root.") from error
        if relative in seen:
            raise EvidenceRejected("Duplicate source path.")
        _text(relative, MAX_SOURCE_PATH_BYTES)
        seen.add(relative)
        content = path.read_bytes()
        inc(work, "source_bytes_read", len(content))
        inc(work, "source_hash_bytes", len(content))
        if not 1 <= len(content) <= MAX_WIRE_BYTES:
            raise EvidenceLimit("Individual source-file byte cap.")
        entries.append({"path": relative, "bytes": len(content),
                        "sha256": hashlib.sha256(content).hexdigest()})
    if not entries:
        raise EvidenceRejected("Nonempty source closure required.")
    result = canonical({"schema": SOURCE_SCHEMA, "evidence_schema": SCHEMA,
                        "sources": sorted(entries, key=lambda item: item["path"])})
    _text(result, MAX_SOURCE_BYTES)
    inc(work, "source_record_bytes", len(result.encode("utf-8")))
    return result


def _node_record(node):
    if node[0] == "terminal":
        return ("T", *_pair(node[1]))
    if node[0] == "node":
        return ("N", node[1], node[2], node[3])
    raise EvidenceRejected("Unknown producer node.")


def _bad_json_number(_):
    raise EvidenceRejected("Floating or nonfinite JSON number is not permitted.")


def _unique_object(pairs):
    answer = {}
    for key, value in pairs:
        if key in answer:
            raise EvidenceRejected("Duplicate JSON object key.")
        answer[key] = value
    return answer


def _json_loads(text):
    try:
        return json.loads(text, object_pairs_hook=_unique_object,
                          parse_float=_bad_json_number, parse_constant=_bad_json_number)
    except (ValueError, TypeError, RecursionError) as error:
        if isinstance(error, EvidenceRejected):
            raise
        raise EvidenceRejected("Malformed exact JSON.") from error


def _expression_key(key, bits):
    """Wire syntax check only; semantic root checking belongs to the receiver."""
    _text(key, MAX_EXPRESSION_BYTES)
    parsed = _json_loads(key)
    visits = 0
    def decode(expression, depth=0):
        nonlocal visits
        visits += 1
        if visits > K.MAX_NODES or depth > K.MAX_DEPTH:
            raise EvidenceLimit("Expression shape cap.")
        if type(expression) is not list or not expression or type(expression[0]) is not str:
            raise EvidenceRejected("Exact expression list required.")
        op = expression[0]
        if op == "lit" and len(expression) == 2 and type(expression[1]) is str:
            return K.lit(expression[1])
        if op == "bit" and len(expression) == 2:
            return K.bit(_integer(expression[1], 0, bits-1))
        if op == "not" and len(expression) == 2:
            return K.neg(decode(expression[1], depth+1))
        if op == "scale" and len(expression) == 3 and type(expression[1]) is str:
            return K.scale(expression[1], decode(expression[2], depth+1))
        if op in ("and", "or", "eq", "add", "min", "max") and len(expression) == 3:
            return (op, decode(expression[1], depth+1), decode(expression[2], depth+1))
        raise EvidenceRejected("Unknown expression instruction.")
    expression = decode(parsed)
    K.validate(expression, bits)
    if M._key(expression) != key:
        raise EvidenceRejected("Expression key is not canonical.")


@dataclass(frozen=True)
class ExportCursor:
    """An offered export position; use only after successful receiver admission.

    Producing this value alone confers no authority. The receiver independently
    enforces exact admitted base counts and the full source/order/epoch context.
    """
    source_record: str
    epoch: str
    bits: int
    order: tuple
    counts: tuple

    def __post_init__(self):
        _header(self.source_record, self.epoch, self.bits, self.order)
        if type(self.counts) is not tuple or len(self.counts) != 3:
            raise EvidenceRejected("Three immutable base counts required.")
        for value, cap in zip(self.counts, (MAX_NODES, MAX_APPLIES, MAX_EXPRESSIONS)):
            _integer(value, 0, cap)

    def record(self):
        return {"source_record": self.source_record, "epoch": self.epoch,
                "bits": self.bits, "order": list(self.order),
                "counts": dict(zip(("nodes", "applies", "expressions"), self.counts))}


@dataclass(frozen=True)
class AddEvidence:
    source_record: str
    epoch: str
    bits: int
    order: tuple
    mode: str
    base: tuple
    nodes: tuple
    applies: tuple
    expressions: tuple
    current_record: str
    witness: tuple
    bound: tuple
    roots: tuple

    def __post_init__(self):
        _header(self.source_record, self.epoch, self.bits, self.order)
        if type(self.mode) is not str or self.mode not in ("full", "delta"):
            raise EvidenceRejected("Full or delta mode required.")
        ExportCursor(self.source_record, self.epoch, self.bits, self.order, self.base)
        if self.mode == "full" and self.base != (0, 0, 0):
            raise EvidenceRejected("Full proof requires zero base counts.")
        for sequence, start, cap in zip((self.nodes, self.applies, self.expressions),
                                       self.base, (MAX_NODES, MAX_APPLIES, MAX_EXPRESSIONS)):
            if type(sequence) is not tuple or len(sequence)+start > cap:
                raise EvidenceLimit("Immutable evidence table or retained-count cap.")
        total_nodes = self.base[0] + len(self.nodes)
        for index, node in enumerate(self.nodes, self.base[0]):
            if type(node) is not tuple or not node:
                raise EvidenceRejected("Immutable node instruction required.")
            if node[0] == "T" and len(node) == 3:
                _rational_pair(node[1:], MAX_TERMINAL_BITS)
            elif node[0] == "N" and len(node) == 4:
                _integer(node[1], 0, self.bits-1)
                _integer(node[2], 0, index-1)
                _integer(node[3], 0, index-1)
                if node[2] == node[3]:
                    raise EvidenceRejected("Reduced decision required.")
            else:
                raise EvidenceRejected("Unknown node instruction.")
        seen_applies = set()
        for fact in self.applies:
            if type(fact) is not tuple or len(fact) != 4 or type(fact[0]) is not str or fact[0] not in OPERATORS:
                raise EvidenceRejected("Immutable Apply fact required.")
            for index in fact[1:]:
                _integer(index, 0, total_nodes-1)
            if fact[:3] in seen_applies:
                raise EvidenceRejected("Duplicate packet Apply key.")
            seen_applies.add(fact[:3])
            if fact[0] in COMMUTATIVE and fact[1] > fact[2]:
                raise EvidenceRejected("Canonical commutative Apply key required.")
        seen_expressions = set()
        for fact in self.expressions:
            if type(fact) is not tuple or len(fact) != 2:
                raise EvidenceRejected("Immutable expression binding required.")
            _expression_key(fact[0], self.bits)
            _integer(fact[1], 0, total_nodes-1)
            if fact[0] in seen_expressions:
                raise EvidenceRejected("Duplicate packet expression key.")
            seen_expressions.add(fact[0])
        _text(self.current_record, MAX_CURRENT_BYTES)
        if type(self.witness) is not tuple or len(self.witness) != self.bits:
            raise EvidenceRejected("Immutable full witness required.")
        for value in self.witness:
            _integer(value, 0, 1)
        _rational_pair(self.bound, MAX_BOUND_BITS)
        if type(self.roots) is not tuple or len(self.roots) != 4:
            raise EvidenceRejected("Four immutable current roots required.")
        for index in self.roots:
            _integer(index, 0, total_nodes-1)

    def record(self):
        return {"schema": SCHEMA, "mode": self.mode, "source_record": self.source_record,
                "epoch": self.epoch, "bits": self.bits, "order": self.order,
                "base": dict(zip(("nodes", "applies", "expressions"), self.base)),
                "nodes": self.nodes, "applies": self.applies, "expressions": self.expressions,
                "current_record": self.current_record, "witness": self.witness,
                "bound": self.bound,
                "roots": dict(zip(("guard", "rank", "difference", "bad"), self.roots))}

    def next_cursor(self):
        return ExportCursor(self.source_record, self.epoch, self.bits, self.order,
                            tuple(start+len(rows) for start, rows in
                                  zip(self.base, (self.nodes, self.applies, self.expressions))))


def to_wire(evidence, work=None):
    if type(evidence) is not AddEvidence:
        raise EvidenceRejected("Exact immutable AddEvidence required.")
    payload = canonical(evidence.record()).encode("utf-8")
    inc(work, "wire_encoded_bytes", len(payload))
    inc(work, "wire_encode_calls")
    if len(payload) > MAX_WIRE_BYTES:
        raise EvidenceLimit("Evidence wire byte cap.")
    return payload


def from_wire(payload, work=None):
    """Strict producer-side syntax decoder, not a semantic proof verifier."""
    if type(payload) is bytes:
        raw = payload
    elif type(payload) is str:
        try:
            raw = payload.encode("utf-8")
        except UnicodeError as error:
            raise EvidenceRejected("Invalid UTF-8 payload.") from error
    else:
        raise EvidenceRejected("Bytes or exact string payload required.")
    inc(work, "wire_decoded_bytes", len(raw))
    inc(work, "wire_decode_calls")
    if len(raw) > MAX_WIRE_BYTES:
        raise EvidenceLimit("Evidence wire byte cap.")
    try:
        parsed = _json_loads(raw.decode("utf-8"))
    except UnicodeError as error:
        raise EvidenceRejected("Invalid UTF-8 payload.") from error
    def depth(value, level=0):
        if level > MAX_OUTER_DEPTH:
            raise EvidenceLimit("Outer JSON nesting cap.")
        if type(value) is dict:
            for item in value.values():
                depth(item, level+1)
        elif type(value) is list:
            for item in value:
                depth(item, level+1)
    depth(parsed)
    keys = {"schema", "mode", "source_record", "epoch", "bits", "order", "base", "nodes",
            "applies", "expressions", "current_record", "witness", "bound", "roots"}
    if type(parsed) is not dict or set(parsed) != keys or parsed["schema"] != SCHEMA:
        raise EvidenceRejected("Exact evidence schema and fields required.")
    if type(parsed["base"]) is not dict or set(parsed["base"]) != {"nodes", "applies", "expressions"}:
        raise EvidenceRejected("Exact base-count fields required.")
    if type(parsed["roots"]) is not dict or set(parsed["roots"]) != {"guard", "rank", "difference", "bad"}:
        raise EvidenceRejected("Exact root fields required.")
    def array(name):
        if type(parsed[name]) is not list:
            raise EvidenceRejected("JSON array required.")
        return tuple(parsed[name])
    def table(name):
        items = array(name)
        if any(type(item) is not list for item in items):
            raise EvidenceRejected("JSON fact arrays required.")
        return tuple(tuple(item) for item in items)
    return AddEvidence(parsed["source_record"], parsed["epoch"], parsed["bits"], array("order"),
        parsed["mode"], tuple(parsed["base"][name] for name in ("nodes", "applies", "expressions")),
        table("nodes"), table("applies"), table("expressions"), parsed["current_record"],
        array("witness"), array("bound"),
        tuple(parsed["roots"][name] for name in ("guard", "rank", "difference", "bad")))


class _RecordingDict(dict):
    def __init__(self, owner, kind):
        super().__init__()
        self.owner, self.kind = owner, kind

    def __setitem__(self, key, value):
        work = self.owner._record_work
        inc(work, "recording_fresh_key_checks")
        if key in self:
            raise EvidenceRejected("Append-only producer proof fact was reassigned.")
        super().__setitem__(key, value)
        if self.kind == "apply":
            self.owner.apply_log.append((*key, value))
            inc(work, "recorded_apply_facts")
        else:
            self.owner.expression_log.append((key, value))
            inc(work, "recorded_expression_bindings")


class RecordingManager(A.Manager):
    """Unchanged ordinary algorithm with recorded cache insertions and a wire cap.

    The context is fixed for this producer lifetime. New contexts use a new
    manager, and receiver authority requires its independent explicit reset.
    A receiver never trusts this object's private flags, caches, or roots.
    """
    def __init__(self, bits, order=None, *, source_record, epoch, work=None):
        order = tuple(range(bits)) if order is None and type(bits) is int else order
        _header(source_record, epoch, bits, order)
        super().__init__(bits, order)
        self.context = ExportCursor(source_record, epoch, bits, order, (0, 0, 0))
        self.apply_log, self.expression_log = [], []
        self._record_work = None
        self.operations = _RecordingDict(self, "apply")
        self.expressions = _RecordingDict(self, "expression")
        inc(work, "recording_manager_order_entries", bits)
        inc(work, "recording_manager_context_bytes", len(source_record.encode("utf-8")))

    def apply(self, op, left, right, work=None):
        previous, self._record_work = self._record_work, work
        try:
            return super().apply(op, left, right, work)
        finally:
            self._record_work = previous

    def compile(self, expression, work=None):
        previous, self._record_work = self._record_work, work
        try:
            return super().compile(expression, work)
        finally:
            self._record_work = previous

    def terminal(self, value, work=None):
        # This narrows the producer only to the declared new wire fragment.
        inc(work, "wire_rational_cap_checks")
        if work is not None and type(value) in (int, F):
            q = F(value)
            work["max_requested_terminal_component_bits"] = max(
                work.get("max_requested_terminal_component_bits", 0),
                abs(q.numerator).bit_length(), q.denominator.bit_length())
        pair = _pair(value)
        if work is not None:
            work["max_wire_rational_component_bits"] = max(
                work.get("max_wire_rational_component_bits", 0),
                abs(pair[0]).bit_length(), pair[1].bit_length())
        return super().terminal(value, work)

    def cursor(self):
        return ExportCursor(self.context.source_record, self.context.epoch,
                            self.nbits, self.order,
                            (len(self.nodes), len(self.apply_log), len(self.expression_log)))

    def state_record(self, work=None):
        """Complete declared serialization proxy, including cache keys and logs.

        Repeated references are serialized in every named table. This proxy is
        explicit and reproducible; it is not a claim about Python heap bytes.
        """
        inc(work, "producer_state_node_records", len(self.nodes))
        inc(work, "producer_state_unique_records", len(self.unique))
        inc(work, "producer_state_apply_records", len(self.operations)+len(self.apply_log))
        inc(work, "producer_state_expression_records", len(self.expressions)+len(self.expression_log))
        return {"version": VERSION, "context": self.context.record(),
                "bits": self.nbits, "order": self.order,
                "positions": tuple(sorted(self.position.items())),
                "nodes": tuple(_node_record(node) for node in self.nodes),
                "boolean_flags": tuple(self.boolean),
                "unique_keys": tuple((_node_record(node), index) for node, index in self.unique.items()),
                "apply_cache": tuple((*key, value) for key, value in self.operations.items()),
                "apply_proof_log": tuple(self.apply_log),
                "expression_cache": tuple((M._key(expr), root) for expr, root in self.expressions.items()),
                "expression_proof_log": tuple((M._key(expr), root) for expr, root in self.expression_log)}

    def state_bytes(self, work=None):
        result = canonical(self.state_record(work)).encode("utf-8")
        inc(work, "producer_state_serialized_bytes", len(result))
        return result


def _context_matches(manager, base):
    if type(base) is not ExportCursor:
        raise EvidenceRejected("Exact immutable export cursor required.")
    actual = manager.cursor()
    if (base.source_record, base.epoch, base.bits, base.order) != (
            actual.source_record, actual.epoch, actual.bits, actual.order):
        raise EvidenceRejected("Producer cursor source/order/epoch mismatch.")
    if any(want > have for want, have in zip(base.counts, actual.counts)):
        raise EvidenceRejected("Producer cursor references unavailable facts.")


def _violating_point(manager, bad, work=None):
    point = [0] * manager.nbits
    current = bad
    while manager.nodes[current][0] != "terminal":
        inc(work, "counterexample_diagram_nodes")
        _, variable, low, high = manager.nodes[current]
        bit = int(manager.nodes[low] == ("terminal", F(0)))
        point[variable] = bit
        current = high if bit else low
    inc(work, "counterexample_diagram_nodes")
    if manager.nodes[current] != ("terminal", F(1)):
        raise EvidenceRejected("Producer bad-set diagram has an inconsistent Boolean terminal.")
    return tuple(point)


def _current_goal(manager, frame, witness, bound, expected_record, work=None):
    """Construct only the requested upper-bound service, not unused extrema."""
    if not isinstance(manager, A.Manager) or type(frame) is not M.Frame:
        raise EvidenceRejected("Declared ordinary manager and exact Frame required.")
    frame.__post_init__()
    if frame.request.nbits != manager.nbits or not 1 <= manager.nbits <= MAX_BITS:
        raise EvidenceRejected("Matching one-to-ten-bit frame required.")
    record = frame.record()
    _text(record, MAX_CURRENT_BYTES)
    if type(expected_record) is not str or expected_record != record:
        raise EvidenceRejected("Independent current record mismatch.")
    inc(work, "producer_record_characters_compared", 2*len(record))
    M._point(witness, manager.nbits)
    bound = K.rational(bound)
    for hard in frame.request.hard:
        inc(work, "producer_feasibility_checks")
        if K.interval(hard, witness, work) != (F(1), F(1)):
            raise EvidenceRejected("Current incumbent is not feasible.")
    cutoff = M.rank_bounds(frame, witness, work)[0]
    guard = manager.terminal(1, work)
    rank = manager.terminal(0, work)
    for hard in frame.request.hard:
        guard = manager.apply("and", guard, manager.compile(hard, work), work)
    for soft in frame.request.soft:
        failure = manager.apply("sub", manager.terminal(1, work), manager.compile(soft.formula, work), work)
        term = manager.apply("mul", manager.terminal(soft.weight, work), failure, work)
        rank = manager.apply("add", rank, term, work)
    rank_test = manager.apply("le", rank, manager.terminal(cutoff, work), work)
    guard = manager.apply("and", guard, rank_test, work)
    difference = manager.compile(frame.difference, work)
    loss_test = manager.apply("gt", difference, manager.terminal(bound, work), work)
    bad = manager.apply("and", guard, loss_test, work)
    if manager.nodes[bad] != ("terminal", F(0)):
        raise NoBoundProof(_violating_point(manager, bad, work), record, bound)
    return record, bound, cutoff, (guard, rank, difference, bad)


def export_dag(manager, frame, witness, bound, expected_record, *, base=None, work=None):
    """Produce full evidence or a resident delta; no receiving admission occurs.

    Only pass a prior next_cursor after the receiver accepted that packet.
    Calling with base=None after delta episodes still exports a full proof for
    a fresh receiver. All retained facts are exported in that full mode; this
    version does not claim minimum proof-closure size.
    """
    if type(manager) is not RecordingManager:
        raise EvidenceRejected("Recorded ordinary manager required for DAG export.")
    if base is None:
        mode, starts = "full", (0, 0, 0)
    else:
        _context_matches(manager, base)
        mode, starts = "delta", base.counts
    record, rational_bound, _, roots = _current_goal(
        manager, frame, witness, bound, expected_record, work)
    nodes = tuple(_node_record(node) for node in manager.nodes[starts[0]:])
    applies = tuple(manager.apply_log[starts[1]:])
    expressions = tuple((M._key(expr), root)
                        for expr, root in manager.expression_log[starts[2]:])
    inc(work, "exported_node_facts", len(nodes))
    inc(work, "exported_apply_facts", len(applies))
    inc(work, "exported_expression_bindings", len(expressions))
    inc(work, "exported_expression_characters", sum(len(key) for key, _ in expressions))
    return AddEvidence(manager.context.source_record, manager.context.epoch, manager.nbits,
                       manager.order, mode, starts, nodes, applies, expressions,
                       record, witness, _pair(rational_bound, MAX_BOUND_BITS), roots)


def export_tree(manager, frame, witness, bound, expected_record, *, symbolic=True, work=None):
    """Export an actual ADD-guided split tree into the unchanged old receiver.

    ADD terminals guide production but never justify a receiver leaf. The
    existing interval/context/multiplier rules must justify every leaf; remaining
    free coordinates are split when those rules cannot yet establish the bound.
    """
    if type(symbolic) is not bool:
        raise EvidenceRejected("Boolean symbolic option required.")
    record, rational_bound, cutoff, roots = _current_goal(
        manager, frame, witness, bound, expected_record, work)
    visited = 0
    def go(cell, guard, difference):
        nonlocal visited
        visited += 1
        inc(work, "legacy_export_cells")
        if visited > P.MAX_TREE_NODES:
            raise EvidenceLimit("Legacy proof tree node cap.")
        for index, hard in enumerate(frame.request.hard):
            if K.interval(hard, cell, work)[1] == 0:
                return ("hard", index)
        if M.rank_bounds(frame, cell, work)[0] > cutoff:
            return ("rank",)
        rows = P.context_rows(frame, cell, cutoff, work)
        multipliers = P.best_witness(frame.difference, rational_bound, rows, cell,
                                     symbolic=symbolic, work=work)
        if multipliers is not None:
            return ("direct", multipliers)
        free = [index for index in manager.order if cell[index] is None]
        if not free:
            raise P.Uncertified(cell, "ADD result did not yield a leaf in the legacy proof vocabulary")
        ng, nd = manager.nodes[guard], manager.nodes[difference]
        live = [node[1] for node in (ng, nd) if node[0] == "node"]
        if live:
            variable = min(live, key=manager.position.__getitem__)
            if cell[variable] is not None:
                raise EvidenceRejected("Producer cofactor traversal repeated an assigned variable.")
            inc(work, "legacy_add_guided_splits")
        else:
            variable = free[0]
            inc(work, "legacy_terminal_refinement_splits")
        def child(node_id, node, bit):
            return node[2+bit] if node[0] == "node" and node[1] == variable else node_id
        low = go(cell[:variable]+(0,)+cell[variable+1:],
                 child(guard, ng, 0), child(difference, nd, 0))
        high = go(cell[:variable]+(1,)+cell[variable+1:],
                  child(guard, ng, 1), child(difference, nd, 1))
        return ("split", variable, low, high)
    tree = go((None,)*manager.nbits, roots[0], roots[2])
    return P.PortfolioProof(record, (), witness, rational_bound, tree)


def receiver_module():
    """Canonical loader for the separately implemented checker and its exact type.

    This lazy import is used only by the explicit checked-admission adapter.
    Ordinary production and syntax decoding do not call the receiver. The
    checker never imports this producer, so there is no circular dependency.
    """
    module = _load("_rp3bb_add_evidence_receiver", "05_add_evidence_check.py")
    if module.M is not M:
        raise EvidenceRejected("Receiver uses a different Frame class identity.")
    return module


def admit_checked_add(receiver, cache, handle, payload, current,
                      expected_current_record, witness, bound, *,
                      expected_source_record, request_id, work=None):
    """Verify a fresh ADD receipt, then stage an ordinary portfolio-domain bridge.

    Returns (next_receiver, next_cache, report). Publish both staged objects only
    after the outer owner pays retention and terminal delivery. Original receiver
    and cache remain unchanged on success or failure. No caller-supplied report
    or dictionary can grant admission: this function invokes the exact receiver.

    The assignment to a fresh domain table below is the explicit new verified
    bridge. It neither bypasses a checked premise nor changes the old portfolio
    checker. Once admitted, ordinary and portfolio arms use the identical old
    domain/Choice/build/verify kernel for subsequent edits.
    """
    checker = receiver_module()
    if type(receiver) is not checker.Receiver or type(cache) is not P.PortfolioCache:
        raise EvidenceRejected("Exact owned Receiver and PortfolioCache required.")
    if type(expected_source_record) is not str or receiver.expected_source_record != expected_source_record:
        raise EvidenceRejected("Independent bridge source closure mismatch.")
    inc(work, "bridge_source_record_characters_compared", len(expected_source_record))
    cache._fresh(handle)
    inc(work, "bridge_fresh_handle_checks")
    if type(current) is not M.Frame:
        raise EvidenceRejected("Exact current Frame required for bridge admission.")
    current.__post_init__()
    record = current.record()
    if type(expected_current_record) is not str or record != expected_current_record:
        raise EvidenceRejected("Independent bridge current record mismatch.")
    inc(work, "bridge_current_record_characters_compared", len(record))
    M._point(witness, current.request.nbits)
    rational_bound = K.rational(bound)
    # The old domain/conditional-witness interface accepts an input-size cutoff.
    cutoff = K.rational(M.rank_bounds(current, witness, work)[0])
    if type(request_id) is not str or not request_id:
        raise EvidenceRejected("Explicit owner request id required for bridge admission.")
    next_receiver = receiver.fork(work=work)
    report = next_receiver.receive(payload, current, expected_current_record,
                                   witness, rational_bound, work=work,
                                   request_id=request_id)
    committed = next_receiver.current_receipt(request_id)
    report_record = canonical(report)
    committed_record = canonical(committed)
    inc(work, "bridge_receipt_characters_compared", len(report_record)+len(committed_record))
    if committed is None or report_record != committed_record:
        raise EvidenceRejected("No matching newly committed receiving receipt.")
    expected = {"status": "CURRENT_BOUND_CERTIFIED", "version": checker.VERSION,
                "current_record": record, "bound": str(rational_bound),
                "incumbent_rank": str(cutoff), "feasibility": "NONEMPTY",
                "coverage": "ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS",
                "selected_identities_claimed": False, "trusted_cache": True,
                "certificate_format": "INDEPENDENT_UNCONDITIONAL_ADD_DAG",
                "epoch": receiver.epoch, "request_id": request_id,
                "non_deterioration": rational_bound <= 0}
    if any(type(report.get(key)) is not type(value) or report.get(key) != value
           for key, value in expected.items()):
        raise EvidenceRejected("Checked receipt does not supply the exact required domain service.")
    next_cache = P.PortfolioCache()
    for old_handle, domain in cache._domains.items():
        if type(domain) is not P.DomainCertificate:
            raise EvidenceRejected("Malformed locally admitted portfolio domain.")
        next_cache._domains[old_handle] = domain
        inc(work, "bridge_existing_domains_copied")
    next_cache._fresh(handle)
    next_cache._domains[handle] = P.DomainCertificate(
        current, cutoff, rational_bound, "independently_checked_add_v1")
    inc(work, "bridge_verified_domains_admitted")
    return next_receiver, next_cache, report
