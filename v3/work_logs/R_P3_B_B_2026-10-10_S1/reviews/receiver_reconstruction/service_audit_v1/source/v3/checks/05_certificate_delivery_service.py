#!/usr/bin/env python3
"""Finite equal certificate service and declared event/byte tariff, R-P3-B-B.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT.
The measuring apparatus and experiment writer are outside the worker tariff.
All scientific orchestration runs inside Meter.run; nested stages only relabel
the active bill. The service is an owned finite interpreter, not a hostile-code
sandbox or a physical CPU/heap resource claim. Older sources are unchanged.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name, filename):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


A = load('_rp3bb_add_evidence_producer', '05_add_evidence.py')
C = A.receiver_module()
P, M, K = A.P, A.M, A.K
VERSION = 'rp3bb-certificate-service-v2'
TARIFF = 'rp3bb-cpython31214-observed-events-plus-live-byte-periods-v1'
SUCCESS_BUDGET = 2**27
FAILURE_RESERVE = 1024
MAX_PAYLOAD = 32 * 1024 * 1024
MAX_STATE = 64 * 1024 * 1024
CONSUMER_THRESHOLDS = (2**20, 2**22, 2**24)
METHODS = ('P-REUSE', 'P-FRESH', 'O-ADD-COLD', 'O-ADD-WARM',
           'O-ENUM-RECEIVER', 'O-ADD-PORTFOLIO')
SOURCE_PATHS = (*A.DEFAULT_SOURCE_PATHS,
                'v3/checks/05_certificate_delivery_service.py',
                'v3/checks/05_certificate_delivery_cases.py')
FAILURE_PAYLOAD = (b'{"schema":"rp3bb.current-bound.v1","status":'
                   b'"NO_CURRENT_CERTIFICATE","reason":"RESOURCE_OR_VALIDATION_FAILURE"}')


class ResourceExhausted(BaseException):
    """Cannot be swallowed by a producer's ordinary ValueError fallback."""
    def __init__(self, stage, category, count):
        self.stage, self.category, self.count = stage, category, count
        super().__init__(stage + ': reserved budget exhausted')


class Meter:
    """An explicitly priced event model; the apparatus does not bill itself."""
    def __init__(self, budget=SUCCESS_BUDGET, *, consumer_budget=None):
        if sys.implementation.name != 'cpython' or sys.version_info[:3] != (3, 12, 14):
            raise ValueError('This tariff requires CPython 3.12.14.')
        if type(budget) is not int or budget < FAILURE_RESERVE:
            raise ValueError('Exact integer budget must cover the terminal reserve.')
        if consumer_budget is not None and (type(consumer_budget) is not int
                                           or consumer_budget < FAILURE_RESERVE):
            raise ValueError('Invalid independent consumer budget.')
        self.budget, self.consumer_budget = budget, consumer_budget
        self.units = self.consumer_units = 0
        self.by_stage = {}
        self.current, self.active = None, False
        self.max_object_bytes = self.max_retained_bytes = 0
        self.retained = {}
        self.observed_packets = []
        self.failure = None

    def _consumer(self, stage):
        return stage.startswith('receiver_') or stage in ('terminal', 'failure_terminal', 'common_source')

    def charge(self, stage, category, count):
        if type(count) is not int or count < 0:
            raise ValueError('Exact nonnegative tariff count required.')
        reserve = 0 if stage == 'failure_terminal' else FAILURE_RESERVE
        if self.units + count > self.budget - reserve:
            raise ResourceExhausted(stage, category, count)
        consumer = self._consumer(stage)
        if (consumer and self.consumer_budget is not None
                and self.consumer_units + count > self.consumer_budget - reserve):
            raise ResourceExhausted(stage, category, count)
        self.by_stage.setdefault(stage, Counter())[category] += count
        self.units += count
        if consumer:
            self.consumer_units += count

    def _trace(self, frame, event, arg):
        if frame.f_code in _METER_CODES:
            return None
        if event == 'call':
            frame.f_trace_opcodes = True
            return self._trace
        if event == 'opcode' and self.active:
            self.charge(self.current, 'observed_python_opcode_events', 1)
        return self._trace

    def _profile(self, frame, event, arg):
        if event == 'c_call' and self.active and frame.f_code not in _METER_CODES:
            self.charge(self.current, 'bounded_native_c_call_events', 1)

    def run(self, stage, function):
        previous_stage, previous_active = self.current, self.active
        self.current, self.active = stage, True
        if previous_active:
            try:
                return function()
            finally:
                self.current, self.active = previous_stage, previous_active
        old_trace, old_profile = sys.gettrace(), sys.getprofile()
        frame = sys._getframe()
        old_flag = frame.f_trace_opcodes
        frame.f_trace_opcodes = True
        try:
            sys.settrace(self._trace)
            sys.setprofile(self._profile)
            return function()
        finally:
            self.active = False
            sys.settrace(old_trace)
            sys.setprofile(old_profile)
            frame.f_trace_opcodes = old_flag
            self.current, self.active = previous_stage, previous_active
            del frame

    def bytes(self, stage, category, payload):
        size = len(payload)
        self.charge(stage, category, size)
        self.max_object_bytes = max(self.max_object_bytes, size)
        # An observer retains these already transmitted/materialized immutable
        # bytes for source-bound replay. Capturing the experiment is apparatus,
        # never extra authority supplied to a producer or receiving worker.
        self.observed_packets.append((stage, category, payload))
        return size

    def retain(self, key, side, make_record):
        stage = side + '_storage'
        payload = self.run(stage, lambda: encode(make_record()))
        if len(payload) > MAX_STATE:
            raise ValueError('Declared serialized-state object cap.')
        self.bytes(stage, 'retained_serialized_byte_periods', payload)
        self.retained[key] = len(payload)
        self.max_retained_bytes = max(self.max_retained_bytes, sum(self.retained.values()))
        return len(payload)

    def fail(self, error):
        self.failure = {'type': type(error).__name__, 'message': str(error),
                        'stage': getattr(error, 'stage', self.current)}
        # The owner emits this literal and evicts failed mutable state. These
        # bounded ownership events are expressly priced, not traced worker work.
        self.charge('failure_terminal', 'terminal_bytes', len(FAILURE_PAYLOAD))
        self.charge('failure_terminal', 'delivery_events', 1)
        self.charge('failure_terminal', 'state_eviction_events', 1)
        return FAILURE_PAYLOAD

    def invoice(self):
        stages = {key: dict(sorted(value.items()))
                  for key, value in sorted(self.by_stage.items())}
        assert sum(sum(row.values()) for row in stages.values()) == self.units
        assert sum(sum(row.values()) for key, row in stages.items()
                   if self._consumer(key)) == self.consumer_units
        return {'tariff': TARIFF, 'total_units': self.units,
                'consumer_units': self.consumer_units, 'budget': self.budget,
                'consumer_budget': self.consumer_budget, 'by_stage': stages,
                'failure_terminal_reserve': FAILURE_RESERVE,
                'max_serialized_object_bytes': self.max_object_bytes,
                'max_retained_serialized_bytes': self.max_retained_bytes,
                'retained_proxy_bytes': dict(sorted(self.retained.items())),
                'failure': self.failure, 'instrumentation_included': False,
                'physical_cpu_or_heap_bound_claimed': False}


_METER_CODES = {value.__code__ for value in Meter.__dict__.values()
                if callable(value) and hasattr(value, '__code__')}


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key.')
        result[key] = value
    return result


def _bad_number(value):
    raise ValueError('Inexact JSON numbers are unsupported.')


def _int(text):
    if len(text.lstrip('-')) > 1234 or text == '-0':
        raise ValueError('JSON integer cap or noncanonical negative zero.')
    return int(text)


def encode(value):
    payload = M.canonical(value).encode('ascii')
    if len(payload) > MAX_STATE:
        raise ValueError('Serialization cap.')
    return payload


def decode(payload):
    if type(payload) is not bytes or not 0 < len(payload) <= MAX_PAYLOAD:
        raise ValueError('Bounded byte packet required.')
    text = payload.decode('ascii')
    # Bound parser nesting before invoking the native JSON parser.
    depth, quoted, escaped = 0, False, False
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
            if depth > 80:
                raise ValueError('Packet nesting cap.')
        elif char in ']}':
            depth -= 1
            if depth < 0:
                raise ValueError('Packet nesting mismatch.')
    if depth or quoted:
        raise ValueError('Incomplete packet.')
    return json.loads(text, object_pairs_hook=_pairs, parse_int=_int,
                      parse_float=_bad_number, parse_constant=_bad_number)


def keys(record, expected):
    if type(record) is not dict or set(record) != set(expected):
        raise ValueError('Exact record fields required.')


def immutable(value):
    if type(value) is list:
        return tuple(immutable(child) for child in value)
    if type(value) is dict:
        keys(value, ('rational',))
        return K.rational(value['rational'])
    if value is None or type(value) in (str, int, bool):
        return value
    raise ValueError('Unexpected wire value.')


def frame_from_record(record):
    if type(record) is not str:
        raise ValueError('Full current record required.')
    value = decode(record.encode('ascii'))
    keys(value, ('receiver', 'request', 'loss', 'unit'))
    if value['receiver'] != M.VERSION:
        raise ValueError('Frame semantic version mismatch.')
    request = value['request']
    keys(request, ('version', 'scope', 'nbits', 'metadata', 'hard', 'soft', 'losses'))
    if request['version'] != K.VERSION:
        raise ValueError('Input grammar version mismatch.')
    soft = []
    for row in request['soft']:
        keys(row, ('id', 'formula', 'weight', 'tier'))
        soft.append(K.Soft(row['id'], immutable(row['formula']),
                           K.rational(row['weight']), row['tier']))
    answer = M.Frame(K.Request(request['nbits'], immutable(request['hard']),
                               tuple(soft), immutable(request['losses']),
                               request['scope'], M.canonical(request['metadata'])),
                     value['loss'], value['unit'])
    if answer.record() != record:
        raise ValueError('Noncanonical or mismatched full Frame record.')
    return answer


def request_wire(frame, witness, bound, request_id):
    frame.__post_init__()
    M._point(witness, frame.request.nbits)
    return encode({'schema': 'rp3bb.request.v1', 'current_record': frame.record(),
                   'witness': witness, 'bound': str(K.rational(bound)),
                   'request_id': request_id})


def request_from_wire(payload, expected_record, expected_request_id):
    value = decode(payload)
    keys(value, ('schema', 'current_record', 'witness', 'bound', 'request_id'))
    if (value['schema'] != 'rp3bb.request.v1'
            or value['current_record'] != expected_record
            or value['request_id'] != expected_request_id):
        raise ValueError('Independently expected request mismatch.')
    frame = frame_from_record(value['current_record'])
    witness = immutable(value['witness'])
    M._point(witness, frame.request.nbits)
    return frame, witness, K.rational(value['bound'])


def band_from_wire(payload, expected_record):
    value = decode(payload)
    keys(value, ('frame_record', 'cutoff', 'bound', 'tree'))
    if value['frame_record'] != expected_record:
        raise ValueError('Independently expected old band mismatch.')
    return M.BandProof(frame_from_record(value['frame_record']),
                       K.rational(value['cutoff']), K.rational(value['bound']),
                       immutable(value['tree']))


def portfolio_from_wire(payload):
    value = decode(payload)
    keys(value, ('version', 'current_record', 'choices', 'witness', 'bound', 'tree'))
    if value['version'] != P.VERSION or type(value['choices']) is not list:
        raise ValueError('Portfolio wire version or choices mismatch.')
    choices = []
    for choice in value['choices']:
        keys(choice, ('handle', 'old_record', 'replacements', 'alpha'))
        choices.append(P.Choice(choice['handle'], choice['old_record'],
                                immutable(choice['replacements']),
                                immutable(choice['alpha'])))
    return P.PortfolioProof(value['current_record'], tuple(choices),
                            immutable(value['witness']), immutable(value['bound']),
                            immutable(value['tree']))


def portfolio_state(cache):
    return {handle: {'frame_record': item.frame.record(), 'cutoff': str(item.cutoff),
                     'bound': str(item.bound), 'kind': item.kind}
            for handle, item in sorted(cache._domains.items())}


def scalar(expression, point):
    op = expression[0]
    if op == 'lit':
        return F(expression[1])
    if op == 'bit':
        return F(point[expression[1]])
    if op == 'not':
        return 1 - scalar(expression[1], point)
    if op == 'scale':
        return F(expression[1]) * scalar(expression[2], point)
    left, right = scalar(expression[1], point), scalar(expression[2], point)
    if op == 'add':
        return left + right
    if op in ('min', 'and'):
        return min(left, right)
    if op in ('max', 'or'):
        return max(left, right)
    if op == 'eq':
        return F(left == right)
    raise ValueError('Scalar grammar operation.')


def exact_receiver(frame, witness, bound, work):
    """Ordinary direct checking: no redundant producer table is required."""
    frame.__post_init__()
    M._point(witness, frame.request.nbits)
    if not all(scalar(hard, witness) == 1 for hard in frame.request.hard):
        raise ValueError('Nonempty incumbent is not feasible.')
    cutoff = sum((row.weight * (1 - scalar(row.formula, witness))
                  for row in frame.request.soft), F(0))
    for point in product((0, 1), repeat=frame.request.nbits):
        work['enumerated_assignments'] = work.get('enumerated_assignments', 0) + 1
        if not all(scalar(hard, point) == 1 for hard in frame.request.hard):
            continue
        rank = sum((row.weight * (1 - scalar(row.formula, point))
                    for row in frame.request.soft), F(0))
        if rank <= cutoff:
            work['checked_domain_points'] = work.get('checked_domain_points', 0) + 1
            if scalar(frame.difference, point) > bound:
                raise ValueError('Actual violating current-domain point: ' + str(point))
    return {'status': 'CURRENT_BOUND_CERTIFIED', 'current_record': frame.record(),
            'bound': str(bound), 'incumbent_rank': str(cutoff),
            'feasibility': 'NONEMPTY',
            'coverage': 'ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS'}


def common_report(report, frame, witness, bound, request_id, source_record):
    cutoff = M.rank_bounds(frame, witness)[0]
    expected = {'status': 'CURRENT_BOUND_CERTIFIED', 'current_record': frame.record(),
                'bound': str(bound), 'incumbent_rank': str(cutoff),
                'feasibility': 'NONEMPTY',
                'coverage': 'ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS'}
    if any(type(report.get(key)) is not type(value) or report.get(key) != value
           for key, value in expected.items()):
        raise ValueError('Receiver did not deliver the exact common service.')
    return dict(expected, schema='rp3bb.current-bound.v1', request_id=request_id,
                unit=frame.unit, witness=witness, source_record=source_record)


class Session:
    """One declared stream, method and recipient condition; no cross-arm state."""
    def __init__(self, method, recipient, stream_name, nbits, order,
                 old_specs, expected_source_record):
        if method not in METHODS or recipient not in ('resident', 'fresh'):
            raise ValueError('Declared method and recipient mode required.')
        self.method, self.recipient, self.name = method, recipient, stream_name
        self.nbits, self.order = nbits, tuple(order)
        self.old_specs = tuple(old_specs)
        self.source_record = expected_source_record
        self.source_enrolled = False
        self.request_index = 0
        self.current_id = None
        self.current_payload = None
        self._evict()

    def _evict(self):
        self.manager = self.cursor = self.receiver = None
        self.producer_cache = self.receiver_cache = None
        self.old_packets = []
        self.old_input_records = []
        self.current_payload = None

    def _epoch(self):
        return 'rp3bb:' + self.name

    def _manager(self, meter):
        return meter.run('producer_init', lambda: A.RecordingManager(
            self.nbits, self.order, source_record=self.source_record, epoch=self._epoch()))

    def _receiver(self, meter, side='receiver'):
        return meter.run(side + '_init', lambda: C.Receiver(
            self.source_record, self._epoch(), self.nbits, self.order))

    def _enroll(self, meter):
        def go():
            actual = A.make_source_record(SOURCE_PATHS, repo_root=ROOT)
            if actual != self.source_record:
                raise ValueError('Live worker-source closure differs from declared bytes.')
            source_bytes = sum(item['bytes'] for item in json.loads(actual)['sources'])
            meter.charge('common_source', 'source_program_bytes', source_bytes)
            meter.charge('common_source', 'source_hash_input_bytes', source_bytes)
            meter.bytes('common_source', 'source_record_bytes', actual.encode('ascii'))
        meter.run('common_source', go)
        self.source_enrolled = True

    def _bootstrap_producer(self, meter, work):
        if self.producer_cache is not None:
            return
        self.producer_cache = meter.run('producer_init', P.PortfolioCache)
        if self.method not in ('P-REUSE', 'O-ADD-PORTFOLIO'):
            return
        hybrid = self.method == 'O-ADD-PORTFOLIO'
        manager = self._manager(meter) if hybrid else None
        receiver = self._receiver(meter, 'producer') if hybrid else None
        cursor = None
        for index, (old, witness, bound) in enumerate(self.old_specs):
            record = meter.run('producer_old_input', old.record)
            self.old_input_records.append(record)
            meter.bytes('producer_old_input', 'old_request_bytes', record.encode('ascii'))
            local = meter.run('producer_old_input', lambda: frame_from_record(record))
            if hybrid:
                evidence = meter.run('producer_old_build', lambda: A.export_dag(
                    manager, local, witness, bound, record, base=cursor, work=work))
                packet = meter.run('producer_old_export', lambda: A.to_wire(evidence, work))
                receiver, self.producer_cache, _ = meter.run(
                    'producer_old_admission', lambda: A.admit_checked_add(
                        receiver, self.producer_cache, 'old-' + str(index), packet,
                        local, record, witness, bound, expected_source_record=self.source_record,
                        request_id='bootstrap-producer-' + str(index), work=work))
                cursor = meter.run('producer_old_admission', evidence.next_cursor)
                meter.retain('bootstrap_producer_add', 'producer', manager.state_record)
                meter.retain('bootstrap_producer_receiver', 'producer', receiver.state_record)
            else:
                cutoff = meter.run('producer_old_build', lambda: M.rank_bounds(local, witness, work)[0])
                evidence = meter.run('producer_old_build', lambda: M.build_band(local, cutoff, bound, work))
                packet = meter.run('producer_old_export', lambda: encode(evidence.record()))
                meter.run('producer_old_admission', lambda: self.producer_cache.admit_band(
                    'old-' + str(index), evidence, record, work))
            meter.bytes('producer_old_export', 'old_proof_output_bytes', packet)
            self.old_packets.append(packet)
            meter.retain('bootstrap_producer_portfolio', 'producer',
                         lambda: {'domains': portfolio_state(self.producer_cache),
                                  'old_packets': [p.decode('ascii') for p in self.old_packets],
                                  'old_inputs': self.old_input_records})
        # The explicit hybrid discards temporary ADD construction/checking state
        # once typed domain lemmas and replayable packets have been obtained.
        for key in ('bootstrap_producer_add', 'bootstrap_producer_receiver',
                    'bootstrap_producer_portfolio'):
            meter.retained.pop(key, None)

    def _bootstrap_receiver(self, meter, work):
        if self.recipient == 'resident' and self.receiver_cache is not None:
            return self.receiver_cache
        cache = meter.run('receiver_init', P.PortfolioCache)
        if self.method not in ('P-REUSE', 'O-ADD-PORTFOLIO'):
            return cache
        hybrid = self.method == 'O-ADD-PORTFOLIO'
        receiver = self._receiver(meter) if hybrid else None
        for index, ((old, witness, bound), packet) in enumerate(zip(self.old_specs, self.old_packets)):
            record = meter.run('receiver_old_input', old.record)
            meter.bytes('receiver_old_input', 'old_request_bytes', record.encode('ascii'))
            meter.bytes('receiver_old_input', 'old_proof_input_bytes', packet)
            local = meter.run('receiver_old_input', lambda: frame_from_record(record))
            if hybrid:
                receiver, cache, _ = meter.run('receiver_old_check', lambda: A.admit_checked_add(
                    receiver, cache, 'old-' + str(index), packet, local, record, witness, bound,
                    expected_source_record=self.source_record,
                    request_id='bootstrap-recipient-' + str(index), work=work))
                meter.retain('bootstrap_recipient_add', 'receiver', receiver.state_record)
            else:
                proof = meter.run('receiver_old_import', lambda: band_from_wire(packet, record))
                meter.run('receiver_old_check', lambda: cache.admit_band('old-' + str(index), proof, record, work))
            meter.retain('bootstrap_recipient_portfolio', 'receiver', lambda: portfolio_state(cache))
        for key in ('bootstrap_recipient_add', 'bootstrap_recipient_portfolio'):
            meter.retained.pop(key, None)
        return cache

    def _producer_state(self):
        return {'source_record': self.source_record, 'epoch': self._epoch(),
                'method': self.method, 'old_inputs': self.old_input_records,
                'old_packets': [packet.decode('ascii') for packet in self.old_packets],
                'portfolio_domains': None if self.producer_cache is None else portfolio_state(self.producer_cache),
                'add_manager': None if self.manager is None else self.manager.state_record(),
                'acknowledged_cursor': None if self.cursor is None else self.cursor.record()}

    def _receiver_state(self, receiver, cache, output, request_id):
        return {'source_record': self.source_record, 'epoch': self._epoch(),
                'request_id': request_id, 'current_receipt': output.decode('ascii'),
                'add_receiver': None if receiver is None else receiver.state_record(),
                'portfolio_domains': None if cache is None else portfolio_state(cache)}

    def _execute(self, meter, frame, witness, bound, request_id, work):
        if not self.source_enrolled:
            self._enroll(meter)
        expected_record = meter.run('request_encoding', frame.record)
        request = meter.run('request_encoding', lambda: request_wire(frame, witness, bound, request_id))
        meter.bytes('receiver_input', 'current_request_bytes', request)
        current_r, witness_r, bound_r = meter.run('receiver_input', lambda: request_from_wire(
            request, expected_record, request_id))
        ordinary_enum = self.method == 'O-ENUM-RECEIVER'
        current_p = witness_p = bound_p = None
        if not ordinary_enum:
            meter.bytes('producer_input', 'current_request_bytes', request)
            current_p, witness_p, bound_p = meter.run('producer_input', lambda: request_from_wire(
                request, expected_record, request_id))
        candidate_receiver = candidate_cache = candidate_cursor = None
        if ordinary_enum:
            packet = b''
            report = meter.run('receiver_check', lambda: exact_receiver(current_r, witness_r, bound_r, work))
        elif self.method in ('O-ADD-COLD', 'O-ADD-WARM'):
            if self.method == 'O-ADD-COLD' or self.manager is None:
                self.manager = self._manager(meter)
            resident = self.method == 'O-ADD-WARM' and self.recipient == 'resident'
            base = self.cursor if resident else None
            evidence = meter.run('producer_build', lambda: A.export_dag(
                self.manager, current_p, witness_p, bound_p, expected_record, base=base, work=work))
            packet = meter.run('producer_export', lambda: A.to_wire(evidence, work))
            meter.bytes('producer_export', 'proof_output_bytes', packet)
            meter.bytes('receiver_input', 'proof_input_bytes', packet)
            candidate_receiver = (meter.run('receiver_init', lambda: self.receiver.fork(work))
                                  if resident and self.receiver is not None else self._receiver(meter))
            report = meter.run('receiver_check', lambda: candidate_receiver.receive(
                packet, current_r, expected_record, witness_r, bound_r,
                work=work, request_id=request_id))
            candidate_cursor = meter.run('producer_acknowledgement', evidence.next_cursor) if resident else None
        else:
            self._bootstrap_producer(meter, work)
            candidate_cache = self._bootstrap_receiver(meter, work)
            choices = meter.run('producer_build', lambda: tuple(P.Choice(
                'old-' + str(index), record, tuple(K.bit(i) for i in range(self.nbits)))
                for index, record in enumerate(self.old_input_records)))
            proof = meter.run('producer_build', lambda: self.producer_cache.build(
                current_p, choices, witness_p, bound_p, work=work))
            packet = meter.run('producer_export', lambda: encode(proof.record()))
            meter.bytes('producer_export', 'proof_output_bytes', packet)
            meter.bytes('receiver_input', 'proof_input_bytes', packet)
            received = meter.run('receiver_import', lambda: portfolio_from_wire(packet))
            report = meter.run('receiver_check', lambda: candidate_cache.verify(
                received, current_r, expected_record, work))
        common = meter.run('terminal', lambda: common_report(
            report, current_r, witness_r, bound_r, request_id, self.source_record))
        output = meter.run('terminal', lambda: encode(common))
        # A cursor becomes retained authority only after receiver validation.
        self.cursor = candidate_cursor
        # One live-state period at each delivery, before any cold/fresh disposal.
        # This is not elapsed byte-time or heap-peak accounting. The immutable
        # current packet and actual input are included on each applicable side.
        producer_bytes = meter.retain('producer', 'producer', lambda: {
            'retained': self._producer_state(),
            'current_request': None if ordinary_enum else request.decode('ascii'),
            'current_evidence': packet.decode('ascii')})
        receiver_bytes = meter.retain('receiver', 'receiver', lambda: {
            'retained': self._receiver_state(candidate_receiver, candidate_cache, output, request_id),
            'current_request': request.decode('ascii'),
            'current_evidence': packet.decode('ascii')})
        if self.method == 'O-ADD-COLD':
            self.manager = None
        meter.bytes('terminal', 'current_receipt_output_bytes', output)
        meter.charge('terminal', 'delivery_events', 1)
        meter.charge('terminal', 'candidate_publication_events', 1)
        return (output, candidate_receiver, candidate_cache, len(packet), producer_bytes, receiver_bytes)

    def deliver(self, frame, witness, bound, *, budget=SUCCESS_BUDGET, consumer_budget=None):
        meter = Meter(budget, consumer_budget=consumer_budget)
        self.request_index += 1
        request_id = self.name + ':' + str(self.request_index)
        # Caller-owned attempt identity withdraws the previous current receipt
        # even if the first worker instruction is denied.
        self.current_id, self.current_payload = request_id, None
        work, begin = {}, time.monotonic_ns()
        proof_bytes = producer_bytes = receiver_bytes = None
        error = None
        try:
            output, receiver, cache, proof_bytes, producer_bytes, receiver_bytes = meter.run(
                'coordination', lambda: self._execute(meter, frame, witness, K.rational(bound), request_id, work))
            # Publication is a governor event charged immediately before return.
            # All candidate construction, validation and serialization is paid.
            self.receiver = receiver if self.recipient == 'resident' else None
            self.receiver_cache = cache if self.recipient == 'resident' else None
            self.current_payload = output
            status = 'DELIVERED'
        except (ResourceExhausted, Exception) as failure:
            error = {'type': type(failure).__name__, 'message': str(failure)}
            self._evict()
            output = meter.fail(failure)
            status = 'NO_CURRENT_CERTIFICATE'
        elapsed = time.monotonic_ns() - begin
        invoice = meter.invoice()
        # Observer-only size measurement after the declared disposal, without
        # charging a duplicate period at this same delivery boundary. These
        # diagnostic bytes cannot affect proof production, admission or pricing.
        retained_producer = len(encode(self._producer_state()))
        retained_receiver = (len(encode(self._receiver_state(
            self.receiver, self.receiver_cache, output, request_id)))
            if status == 'DELIVERED' else 0)
        return {'method': self.method, 'recipient': self.recipient,
                'stream': self.name, 'request_index': self.request_index,
                'request_id': request_id, 'status': status,
                'output': output.decode('ascii'), 'proof_bytes': proof_bytes,
                'producer_live_snapshot_bytes': producer_bytes,
                'receiver_live_snapshot_bytes': receiver_bytes,
                'producer_retained_bytes': retained_producer,
                'receiver_retained_bytes': retained_receiver,
                'post_disposal_size_measurement_is_observer_only': True,
                'work': work, 'invoice': invoice, 'observed_wall_ns': elapsed,
                'audit_packets': meter.observed_packets,
                'error': error, 'consumer_thresholds': {
                    str(threshold): status == 'DELIVERED' and invoice['consumer_units'] <= threshold
                    for threshold in CONSUMER_THRESHOLDS}}

    def current_receipt(self, expected_request_id):
        if expected_request_id != self.current_id or self.current_payload is None:
            return None
        return decode(self.current_payload)
