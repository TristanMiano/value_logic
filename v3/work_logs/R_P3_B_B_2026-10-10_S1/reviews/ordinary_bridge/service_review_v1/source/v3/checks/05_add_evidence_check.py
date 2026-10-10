#!/usr/bin/env python3
"""Independent receiver for the R-P3-B-B finite ADD evidence wire.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT only.
This module imports the accepted finite Frame grammar, but neither the ADD
manager nor the new producer. Every admitted Apply fact is unconditional.
The source record is bound to an independently supplied record, not discovered
or authenticated by this checker. Caller-owned process state is trusted.

Raw work counters are diagnostics. The parent service supplies the common
event/byte tariff and paid failure/terminal protocol; this module raises on
invalid input. A single final state-pointer swap admits a fully verified
receipt. An external interruption after that swap can observe a committed
state before receiving the return value; the owner must record that boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
_BASE_NAME = '_p305_portfolio_base'
if _BASE_NAME in sys.modules:
    M = sys.modules[_BASE_NAME]
else:
    _spec = importlib.util.spec_from_file_location(
        _BASE_NAME, Path(__file__).with_name('05_counterfactual_transport.py'))
    if _spec is None or _spec.loader is None:
        raise ImportError('Missing accepted finite Frame dependency.')
    M = importlib.util.module_from_spec(_spec)
    sys.modules[_BASE_NAME] = M
    _spec.loader.exec_module(M)
K = M.K

VERSION = 'rp3bb-add-evidence-check-v1'
SCHEMA = 'rp3bb.add-evidence.v1'
SOURCE_SCHEMA = 'rp3bb.add-evidence-source.v1'
MAX_BITS = 10
MAX_NODES = 100000
MAX_APPLIES = 200000
MAX_EXPRESSIONS = 200000
MAX_RECEIPTS = 256
MAX_WIRE_BYTES = 32 * 1024 * 1024
MAX_SOURCE_BYTES = 1024 * 1024
MAX_CURRENT_BYTES = 8 * 1024 * 1024
MAX_KEY_BYTES = 256 * 1024
MAX_EPOCH_CHARS = 256
MAX_OUTER_DEPTH = 12
MAX_TERMINAL_BITS = 4096
MAX_JSON_INT_DIGITS = 1234
_OPERATORS = frozenset(('add', 'mul', 'min', 'max', 'eq', 'le', 'gt',
                        'and', 'or', 'sub'))
_COMMUTATIVE = frozenset(('add', 'mul', 'min', 'max', 'eq', 'and', 'or'))


class Rejected(ValueError):
    """Malformed, stale or invalid evidence; not a disproof of the bound."""


def _inc(work, name, amount=1):
    if work is not None:
        work[name] = work.get(name, 0) + amount


def _require(condition, message):
    if not condition:
        raise Rejected(message)


def _exact_keys(value, keys, label):
    _require(type(value) is dict and set(value) == set(keys),
             label + ': exact object keys required.')


def _integer(value, lower, upper, label):
    _require(type(value) is int and lower <= value <= upper,
             label + ': exact bounded integer required.')
    return value


def _text_bytes(value, cap, label, nonempty=False):
    _require(type(value) is str and len(value) <= cap,
             label + ': bounded string required.')
    _require(not nonempty or bool(value), label + ': nonempty string required.')
    try:
        raw = value.encode('utf-8')
    except UnicodeError as error:
        raise Rejected(label + ': invalid UTF-8 text.') from error
    _require(len(raw) <= cap, label + ': byte cap exceeded.')
    return len(raw)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, 'Duplicate JSON object key.')
        result[key] = value
    return result


def _json_integer(text):
    _require(text != '-0' and len(text.lstrip('-')) <= MAX_JSON_INT_DIGITS,
             'JSON integer syntax or digit cap.')
    return int(text)


def _no_inexact(value):
    raise Rejected('Floating-point and nonfinite JSON values are forbidden.')


def _depth_scan(text, cap, work):
    """Bound JSON container nesting before the native JSON parser is called."""
    depth = 0
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in '[{':
            depth += 1
            _require(depth <= cap, 'JSON nesting cap exceeded.')
        elif char in ']}':
            depth -= 1
            _require(depth >= 0, 'Unbalanced JSON containers.')
    _require(not quoted and depth == 0, 'Unclosed JSON string or container.')
    _inc(work, 'json_depth_scan_characters', len(text))


def _json(text, depth, work):
    _depth_scan(text, depth, work)
    try:
        return json.loads(text, object_pairs_hook=_pairs,
                          parse_int=_json_integer, parse_float=_no_inexact,
                          parse_constant=_no_inexact)
    except (ValueError, TypeError, RecursionError) as error:
        if isinstance(error, Rejected):
            raise
        raise Rejected('Malformed bounded exact JSON.') from error


def _wire(payload, work):
    if type(payload) is bytes:
        _require(len(payload) <= MAX_WIRE_BYTES, 'Wire byte cap exceeded.')
        try:
            text = payload.decode('utf-8')
        except UnicodeError as error:
            raise Rejected('Wire must be valid UTF-8.') from error
        size = len(payload)
    else:
        size = _text_bytes(payload, MAX_WIRE_BYTES, 'Wire')
        text = payload
    _inc(work, 'wire_input_bytes', size)
    return _json(text, MAX_OUTER_DEPTH, work)


def _fraction(pair, bits, label, work):
    _require(type(pair) is list and len(pair) == 2,
             label + ': [numerator,denominator] required.')
    num, den = pair
    _require(type(num) is int and type(den) is int and den > 0,
             label + ': exact numerator and positive denominator required.')
    _require(abs(num).bit_length() <= bits and den.bit_length() <= bits,
             label + ': rational component cap exceeded.')
    value = F(num, den)
    _require(value.numerator == num and value.denominator == den,
             label + ': reduced canonical rational required.')
    _inc(work, 'rational_wire_checks')
    if work is not None:
        work['max_rational_component_bits'] = max(
            work.get('max_rational_component_bits', 0),
            abs(num).bit_length(), den.bit_length())
    return value


def _syntax_key(expression):
    """Independent encoding of the fixed accepted expression grammar."""
    def encode(node):
        tag = node[0]
        if tag == 'lit':
            return ['lit', str(F(node[1]))]
        if tag == 'bit':
            return ['bit', node[1]]
        if tag == 'scale':
            return ['scale', str(F(node[1])), encode(node[2])]
        return [tag] + [encode(child) for child in node[1:]]
    return json.dumps(encode(expression), separators=(',', ':'))


def _expression(key, bits, work):
    _text_bytes(key, MAX_KEY_BYTES, 'Expression key', nonempty=True)
    value = _json(key, K.MAX_DEPTH + 3, work)
    count = [0]

    def read(row, depth):
        count[0] += 1
        _require(count[0] <= K.MAX_NODES and depth <= K.MAX_DEPTH,
                 'Expression node/depth cap exceeded.')
        _require(type(row) is list and row and type(row[0]) is str,
                 'Expression must be a tagged array.')
        tag = row[0]
        if tag == 'lit' and len(row) == 2:
            _require(type(row[1]) is str and len(row[1]) <= 81,
                     'Canonical input rational string required.')
            try:
                value = K.rational(row[1])
            except (ValueError, ZeroDivisionError) as error:
                raise Rejected('Invalid expression rational.') from error
            _require(str(value) == row[1], 'Noncanonical expression rational.')
            return ('lit', value), ('bool' if value in (0, 1) else 'number')
        if tag == 'bit' and len(row) == 2:
            return ('bit', _integer(row[1], 0, bits - 1, 'Bit')), 'bool'
        if tag == 'not' and len(row) == 2:
            child, kind = read(row[1], depth + 1)
            _require(kind == 'bool', 'Boolean not operand required.')
            return ('not', child), 'bool'
        if tag == 'scale' and len(row) == 3:
            _require(type(row[1]) is str and len(row[1]) <= 81,
                     'Canonical scale rational required.')
            try:
                value = K.rational(row[1])
            except (ValueError, ZeroDivisionError) as error:
                raise Rejected('Invalid scale rational.') from error
            _require(str(value) == row[1], 'Noncanonical scale rational.')
            child, _ = read(row[2], depth + 1)
            return ('scale', value, child), 'number'
        _require(tag in ('and', 'or', 'eq', 'add', 'min', 'max')
                 and len(row) == 3, 'Unknown expression tag or arity.')
        left, left_kind = read(row[1], depth + 1)
        right, right_kind = read(row[2], depth + 1)
        if tag in ('and', 'or'):
            _require(left_kind == right_kind == 'bool',
                     'Boolean conjunction/disjunction operands required.')
        kind = 'bool' if tag in ('and', 'or', 'eq') else 'number'
        return (tag, left, right), kind

    expression, _ = read(value, 0)
    _require(_syntax_key(expression) == key, 'Noncanonical expression key.')
    _inc(work, 'expression_syntax_nodes', count[0])
    return expression


def _source_record(record, work):
    _text_bytes(record, MAX_SOURCE_BYTES, 'Expected source record', nonempty=True)
    data = _json(record, MAX_OUTER_DEPTH, work)
    _exact_keys(data, ('schema', 'evidence_schema', 'sources'), 'Source record')
    _require(data['schema'] == SOURCE_SCHEMA and data['evidence_schema'] == SCHEMA,
             'Source/evidence schema mismatch.')
    rows = data['sources']
    _require(type(rows) is list and 1 <= len(rows) <= 64,
             'Source closure must contain one through 64 entries.')
    previous = None
    for row in rows:
        _exact_keys(row, ('path', 'bytes', 'sha256'), 'Source entry')
        path = row['path']
        _text_bytes(path, 4096, 'Source path', nonempty=True)
        _require(not path.startswith('/') and '\\' not in path
                 and all(part not in ('', '.', '..') for part in path.split('/')),
                 'Source path must be a normalized relative POSIX path.')
        _require(previous is None or previous < path,
                 'Source paths must be distinct and sorted.')
        previous = path
        _integer(row['bytes'], 1, MAX_WIRE_BYTES, 'Source size')
        digest = row['sha256']
        _require(type(digest) is str and len(digest) == 64
                 and all(char in '0123456789abcdef' for char in digest),
                 'Lowercase SHA-256 source digest required.')
    _require(M.canonical(data) == record, 'Canonical complete source record required.')
    _inc(work, 'source_record_characters', len(record))


@dataclass(frozen=True)
class _Chunk:
    node_base: int
    nodes: tuple
    boolean: tuple
    unique: dict
    applies: dict
    expressions: dict


@dataclass(frozen=True)
class _State:
    chunks: tuple = ()
    nodes: int = 0
    applies: int = 0
    expressions: int = 0
    receipts: int = 0
    request_ids: tuple = ()
    receipt_json: str | None = None
    receipt_request_id: str | None = None
    receipt_attempt: int = 0


class _View:
    """A pending append, never exposed as admitted state until verification ends."""
    def __init__(self, state, bits, order, work):
        self.state = state
        self.bits = bits
        self.order = order
        self.position = {var: position for position, var in enumerate(order)}
        self.work = work
        self.nodes = []
        self.boolean = []
        self.unique = {}
        self.applies = {}
        self.expressions = {}

    def node(self, identifier):
        _integer(identifier, 0, self.state.nodes + len(self.nodes) - 1, 'Node id')
        _inc(self.work, 'node_lookups')
        if identifier >= self.state.nodes:
            offset = identifier - self.state.nodes
            return self.nodes[offset], self.boolean[offset]
        for chunk in reversed(self.state.chunks):
            _inc(self.work, 'resident_chunk_lookups')
            if chunk.node_base <= identifier < chunk.node_base + len(chunk.nodes):
                offset = identifier - chunk.node_base
                return chunk.nodes[offset], chunk.boolean[offset]
        raise Rejected('Missing resident node.')

    def lookup(self, table, key, required=True):
        _inc(self.work, table + '_lookups')
        pending = getattr(self, table)
        if key in pending:
            return pending[key]
        for chunk in reversed(self.state.chunks):
            _inc(self.work, 'resident_chunk_lookups')
            resident = getattr(chunk, table)
            if key in resident:
                return resident[key]
        _require(not required, 'Missing previously checked ' + table + ' fact.')
        return None

    def terminal(self, value):
        return self.lookup('unique', ('T', F(value)))

    def level(self, identifier):
        node, _ = self.node(identifier)
        return self.bits if node[0] == 'T' else self.position[node[1]]

    def operation(self, op, left, right):
        if op in _COMMUTATIVE and left > right:
            left, right = right, left
        return self.lookup('applies', (op, left, right))

    def expression_root(self, expression):
        return self.lookup('expressions', _syntax_key(expression))

    def admit_nodes(self, rows):
        _require(type(rows) is list and self.state.nodes + len(rows) <= MAX_NODES,
                 'Node rows/cap invalid.')
        for row in rows:
            _require(type(row) is list and row and type(row[0]) is str,
                     'Node must be a tagged array.')
            if row[0] == 'T' and len(row) == 3:
                value = _fraction(row[1:], MAX_TERMINAL_BITS, 'Terminal', self.work)
                node = ('T', value)
                boolean = value in (0, 1)
            else:
                _require(row[0] == 'N' and len(row) == 4,
                         'Unknown node tag or arity.')
                var = _integer(row[1], 0, self.bits - 1, 'Decision variable')
                low, high = row[2], row[3]
                _, low_boolean = self.node(low)
                _, high_boolean = self.node(high)
                _require(low != high and self.level(low) > self.position[var]
                         and self.level(high) > self.position[var],
                         'Reduced ordered back-reference node required.')
                node = ('N', var, low, high)
                boolean = low_boolean and high_boolean
            _require(self.lookup('unique', node, required=False) is None,
                     'Duplicate noncanonical diagram node.')
            identifier = self.state.nodes + len(self.nodes)
            self.unique[node] = identifier
            self.nodes.append(node)
            self.boolean.append(boolean)
            _inc(self.work, 'node_rows_checked')

    def admit_applies(self, rows):
        _require(type(rows) is list and self.state.applies + len(rows) <= MAX_APPLIES,
                 'Apply rows/cap invalid.')
        for row in rows:
            _require(type(row) is list and len(row) == 4
                     and type(row[0]) is str and row[0] in _OPERATORS,
                     'Exact supported Apply row required.')
            op, left, right, out = row
            left_node, left_boolean = self.node(left)
            right_node, right_boolean = self.node(right)
            self.node(out)
            _require(op not in _COMMUTATIVE or left <= right,
                     'Commutative Apply operands must use canonical order.')
            _require(op not in ('and', 'or') or left_boolean and right_boolean,
                     'Boolean Apply operands required.')
            key = (op, left, right)
            _require(self.lookup('applies', key, required=False) is None,
                     'Duplicate or reassigned Apply fact.')
            expected = self._operation_result(op, left, right, left_node, right_node)
            _require(expected == out, 'Apply result is not justified by checked premises.')
            self.applies[key] = out
            _inc(self.work, 'apply_rows_checked')

    def _operation_result(self, op, left, right, a, b):
        # These are exact identities or terminal equations; no producer flag is read.
        if left == right:
            if op in ('min', 'max', 'and', 'or'):
                return left
            if op in ('eq', 'le'):
                return self.terminal(1)
            if op in ('sub', 'gt'):
                return self.terminal(0)
        if a[0] == b[0] == 'T':
            x, y = a[1], b[1]
            if op == 'add': result = x + y
            elif op == 'sub': result = x - y
            elif op == 'mul': result = x * y
            elif op == 'min': result = min(x, y)
            elif op == 'max': result = max(x, y)
            elif op == 'eq': result = F(x == y)
            elif op == 'le': result = F(x <= y)
            elif op == 'gt': result = F(x > y)
            elif op == 'and': result = F(x == 1 and y == 1)
            else: result = F(x == 1 or y == 1)
            _inc(self.work, 'terminal_equations_checked')
            return self.terminal(result)
        az = a == ('T', F(0))
        bz = b == ('T', F(0))
        ao = a == ('T', F(1))
        bo = b == ('T', F(1))
        if op in ('mul', 'and') and (az or bz): return self.terminal(0)
        if op == 'or' and (ao or bo): return self.terminal(1)
        if op in ('add', 'or') and az: return right
        if op in ('add', 'or') and bz: return left
        if op in ('mul', 'and') and ao: return right
        if op in ('mul', 'and') and bo: return left
        level = min(self.level(left), self.level(right))
        _require(level < self.bits, 'Missing terminal equation.')
        var = self.order[level]
        lows = (a[2], a[3]) if self.level(left) == level else (left, left)
        highs = (b[2], b[3]) if self.level(right) == level else (right, right)
        low = self.operation(op, lows[0], highs[0])
        high = self.operation(op, lows[1], highs[1])
        _inc(self.work, 'shannon_equations_checked')
        return low if low == high else self.lookup('unique', ('N', var, low, high))

    def admit_expressions(self, rows):
        _require(type(rows) is list
                 and self.state.expressions + len(rows) <= MAX_EXPRESSIONS,
                 'Expression rows/cap invalid.')
        for row in rows:
            _require(type(row) is list and len(row) == 2,
                     'Expression binding pair required.')
            key, root = row
            self.node(root)
            expression = _expression(key, self.bits, self.work)
            _require(self.lookup('expressions', key, required=False) is None,
                     'Duplicate or reassigned expression binding.')
            tag = expression[0]
            if tag == 'lit':
                expected = self.terminal(expression[1])
            elif tag == 'bit':
                expected = self.lookup('unique',
                    ('N', expression[1], self.terminal(0), self.terminal(1)))
            elif tag == 'not':
                expected = self.operation('sub', self.terminal(1),
                                          self.expression_root(expression[1]))
            elif tag == 'scale':
                expected = self.operation('mul', self.terminal(expression[1]),
                                          self.expression_root(expression[2]))
            else:
                expected = self.operation(tag, self.expression_root(expression[1]),
                                          self.expression_root(expression[2]))
            _require(expected == root, 'Expression root lacks checked denotation.')
            self.expressions[key] = root
            _inc(self.work, 'expression_rows_checked')

    def next_state(self):
        chunk = _Chunk(self.state.nodes, tuple(self.nodes), tuple(self.boolean),
                       self.unique, self.applies, self.expressions)
        chunks = self.state.chunks + (chunk,)
        return _State(chunks, self.state.nodes + len(self.nodes),
                      self.state.applies + len(self.applies),
                      self.state.expressions + len(self.expressions),
                      self.state.receipts + 1)


class Receiver:
    """An owned finite receiver; source/epoch/order changes require explicit reset."""
    def __init__(self, expected_source_record, epoch, bits, order=None, work=None):
        self.reset(expected_source_record, epoch, bits, order, work=work)

    def reset(self, expected_source_record, epoch, bits, order=None, work=None):
        _source_record(expected_source_record, work)
        _integer(bits, 1, MAX_BITS, 'Receiver bit count')
        _require(type(epoch) is str and 1 <= len(epoch) <= MAX_EPOCH_CHARS,
                 'Bounded nonempty owner epoch required.')
        _text_bytes(epoch, 4 * MAX_EPOCH_CHARS, 'Epoch', nonempty=True)
        order = tuple(range(bits)) if order is None else order
        _require(type(order) is tuple and len(order) == bits
                 and all(type(var) is int for var in order)
                 and set(order) == set(range(bits)), 'Total variable order required.')
        # Reset is an explicit trusted owner action, never controlled by wire fields.
        self.expected_source_record = expected_source_record
        self.epoch = epoch
        self.bits = bits
        self.order = order
        self._state = _State()
        self._active_attempt = 0

    def state_counts(self):
        state = self._state
        return {'nodes': state.nodes, 'applies': state.applies,
                'expressions': state.expressions}

    def fork(self, work=None):
        """Share immutable admitted chunks; all later admissions affect the fork only.

        The outer budget owner can publish this fork after complete terminal
        delivery, or discard it on any later failure. No pending mutable tables
        are shared and no old table is changed by receive.
        """
        other = object.__new__(Receiver)
        other.expected_source_record = self.expected_source_record
        other.epoch = self.epoch
        other.bits = self.bits
        other.order = self.order
        other._state = self._state
        other._active_attempt = self._active_attempt
        _inc(work, 'receiver_forks')
        return other

    def current_receipt(self, expected_request_id):
        """Retrieve only this attempt's committed receipt for the caller's unique id."""
        _require(type(expected_request_id) is str and expected_request_id,
                 'Explicit expected request id required.')
        state = self._state
        if (state.receipt_json is None or state.receipt_attempt != self._active_attempt
                or state.receipt_request_id != expected_request_id):
            return None
        return json.loads(state.receipt_json)

    def receive(self, payload, current, expected_current_record, witness, bound,
                work=None, request_id=None):
        # If interrupted before entry, the independently unique requested id
        # still prevents an older receipt from being mistaken for this one.
        self._active_attempt += 1
        if request_id is None:
            request_id = 'implicit:' + str(self._active_attempt)
        _require(type(request_id) is str and 1 <= len(request_id) <= 256,
                 'Bounded unique caller request id required.')
        _text_bytes(request_id, 1024, 'Request id', nonempty=True)
        _require(request_id not in self._state.request_ids,
                 'Request id was already admitted in this epoch.')
        _require(self._state.receipts < MAX_RECEIPTS, 'Resident receipt cap reached.')
        message = _wire(payload, work)
        _exact_keys(message, ('schema', 'mode', 'source_record', 'epoch', 'bits',
                             'order', 'base', 'nodes', 'applies', 'expressions',
                             'current_record', 'witness', 'bound', 'roots'), 'Wire')
        _require(message['schema'] == SCHEMA and message['mode'] in ('full', 'delta'),
                 'Evidence schema/mode mismatch.')
        _require(type(message['source_record']) is str
                 and message['source_record'] == self.expected_source_record,
                 'Independent source closure mismatch.')
        _inc(work, 'source_record_characters_compared', len(self.expected_source_record))
        _require(type(message['epoch']) is str and message['epoch'] == self.epoch,
                 'Stale or foreign epoch.')
        _require(type(message['bits']) is int and message['bits'] == self.bits,
                 'Coordinate-count mismatch.')
        _require(type(message['order']) is list
                 and all(type(var) is int for var in message['order'])
                 and tuple(message['order']) == self.order, 'Variable-order mismatch.')
        _exact_keys(message['base'], ('nodes', 'applies', 'expressions'), 'Base')
        for key, cap in (('nodes', MAX_NODES), ('applies', MAX_APPLIES),
                         ('expressions', MAX_EXPRESSIONS)):
            _integer(message['base'][key], 0, cap, 'Base ' + key)
        _require(message['base'] == self.state_counts(), 'Stale resident base counts.')
        if message['mode'] == 'full':
            _require(self._state.receipts == 0 and all(value == 0 for value in
                     message['base'].values()), 'Full mode requires a fresh receiver.')
        _require(type(current) is M.Frame and current.request.nbits == self.bits,
                 'Matching independently supplied current Frame required.')
        current.__post_init__()
        record = current.record()
        _text_bytes(record, MAX_CURRENT_BYTES, 'Current Frame record')
        _text_bytes(expected_current_record, MAX_CURRENT_BYTES, 'Expected current record')
        _require(record == expected_current_record
                 and type(message['current_record']) is str
                 and record == message['current_record'], 'Independent current record mismatch.')
        _inc(work, 'current_record_characters_compared', 2 * len(record))
        _require(type(witness) is tuple and len(witness) == self.bits
                 and all(type(bit) is int and bit in (0, 1) for bit in witness),
                 'Independently fixed complete Boolean incumbent required.')
        _require(type(message['witness']) is list
                 and len(message['witness']) == self.bits
                 and all(type(bit) is int and bit in (0, 1) for bit in message['witness'])
                 and tuple(message['witness']) == witness, 'Incumbent substitution.')
        try:
            requested_bound = K.rational(bound)
        except (ValueError, ZeroDivisionError) as error:
            raise Rejected('Invalid independently fixed receiving bound.') from error
        _require(_fraction(message['bound'], 128, 'Requested bound', work)
                 == requested_bound, 'Receiving bound substitution.')
        for hard in current.request.hard:
            _inc(work, 'feasibility_rows_checked')
            _require(K.interval(hard, witness, work) == (F(1), F(1)),
                     'Current incumbent is not feasible.')
        cutoff = F(0)
        for soft in current.request.soft:
            truth = K.interval(soft.formula, witness, work)
            _require(truth[0] == truth[1] and truth[0] in (0, 1),
                     'Soft formula lacks a Boolean incumbent value.')
            cutoff += F(soft.weight) * (1 - truth[0])
            _inc(work, 'incumbent_rank_rows_checked')
        view = _View(self._state, self.bits, self.order, work)
        view.admit_nodes(message['nodes'])
        view.admit_applies(message['applies'])
        view.admit_expressions(message['expressions'])
        roots = message['roots']
        _exact_keys(roots, ('guard', 'rank', 'difference', 'bad'), 'Claim roots')
        for identifier in roots.values():
            view.node(identifier)
        zero, one = view.terminal(0), view.terminal(1)
        guard, rank = one, zero
        for hard in current.request.hard:
            guard = view.operation('and', guard, view.expression_root(hard))
        for soft in current.request.soft:
            failure = view.operation('sub', one, view.expression_root(soft.formula))
            weighted = view.operation('mul', view.terminal(soft.weight), failure)
            rank = view.operation('add', rank, weighted)
        guard = view.operation('and', guard,
                               view.operation('le', rank, view.terminal(cutoff)))
        difference = view.expression_root(current.difference)
        bad = view.operation('and', guard,
                             view.operation('gt', difference,
                                            view.terminal(requested_bound)))
        expected_roots = {'guard': guard, 'rank': rank,
                          'difference': difference, 'bad': bad}
        _require(roots == expected_roots, 'Claim roots do not follow from the current request.')
        _require(bad == zero, 'Current bad-set function is not identically zero.')
        next_state = view.next_state()
        report = {'status': 'CURRENT_BOUND_CERTIFIED', 'version': VERSION,
                  'current_record': record, 'bound': str(requested_bound),
                  'non_deterioration': requested_bound <= 0,
                  'feasibility': 'NONEMPTY', 'incumbent_rank': str(cutoff),
                  'coverage': 'ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS',
                  'selected_identities_claimed': False,
                  'certificate_format': 'INDEPENDENT_UNCONDITIONAL_ADD_DAG',
                  'mode': message['mode'], 'epoch': self.epoch,
                  'request_id': request_id,
                  'admitted': {'nodes': next_state.nodes,
                               'applies': next_state.applies,
                               'expressions': next_state.expressions},
                  'receipt_number': next_state.receipts,
                  'trusted_cache': True,
                  'meaning': 'Uniform bound on the independently fixed receiving loss difference.'}
        receipt_json = M.canonical(report)
        next_state = _State(next_state.chunks, next_state.nodes, next_state.applies,
                            next_state.expressions, next_state.receipts,
                            self._state.request_ids + (request_id,), receipt_json,
                            request_id, self._active_attempt)
        _inc(work, 'claims_checked')
        # All validation and report construction precede the sole admission mutation.
        self._state = next_state
        return report

    def state_record(self):
        """Full serialized retained-table proxy, not authenticated state import.

        Unique keys and Boolean flags are included even when they duplicate
        information derivable from nodes. Python object overhead is not measured.
        """
        def node_record(node):
            if node[0] == 'T':
                return ['T', node[1].numerator, node[1].denominator]
            return list(node)
        chunks = []
        for chunk in self._state.chunks:
            chunks.append({'node_base': chunk.node_base,
                           'nodes': [node_record(node) for node in chunk.nodes],
                           'boolean': list(chunk.boolean),
                           'unique': [[node_record(key), value]
                                      for key, value in chunk.unique.items()],
                           'applies': [list(key) + [value]
                                       for key, value in chunk.applies.items()],
                           'expressions': [[key, value]
                                           for key, value in chunk.expressions.items()]})
        return {'schema': SCHEMA, 'source_record': self.expected_source_record,
                'epoch': self.epoch, 'bits': self.bits, 'order': self.order,
                'counts': self.state_counts(), 'receipts': self._state.receipts,
                'request_ids': self._state.request_ids,
                'last_committed_receipt_json': self._state.receipt_json,
                'last_committed_request_id': self._state.receipt_request_id,
                'last_committed_attempt': self._state.receipt_attempt,
                'active_attempt': self._active_attempt,
                'chunks': chunks}

    def storage(self, work=None):
        raw = M.canonical(self.state_record()).encode('utf-8')
        _inc(work, 'retained_serialization_bytes', len(raw))
        return {**self.state_counts(), 'receipts': self._state.receipts,
                'retained_serialization_bytes': len(raw),
                'scope': 'Full retained node/index/Boolean/fact/receipt tables and source/order binding; not native heap size.'}
