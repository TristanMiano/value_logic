"""Prospective P3-09 certificate-transfer adapter; no cases at import.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
Final generation requires the exact P3-10 exposure token. The development
selfcheck constructs separate two-bit constant/rank toys, never final recipes.
The unchanged Option B workers provide paid certificate delivery; the scalar
reference is an observer used only by the separately scheduled score endpoint.
"""
from __future__ import annotations

import base64
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
VERSION = 'p309-certificates-v1'
ARM = 'certificates'
EXPOSURE_TOKEN = 'P3-10-EXPOSED'
INPUT_SCHEMA = 'value_logic.p309.certificate_inputs.v1'
RESULT_SCHEMA = 'value_logic.p309.certificate_paid_result.v1'
SCORE_SCHEMA = 'value_logic.p309.certificate_score.v1'
COVERAGE = 'ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS'
BASE_METHODS = ('P-REUSE', 'P-FRESH', 'O-ADD-COLD', 'O-ADD-WARM',
                'O-ENUM-RECEIVER', 'O-ADD-PORTFOLIO')
PRUNED = 'O-ADD-WARM-PRUNED'
_REGISTRY = None


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False)


def source_paths():
    """Complete application closure, with the same installation fee for all."""
    return [
        'v3/checks/04_counterfactual_repair.py',
        'v3/checks/05_counterfactual_transport.py',
        'v3/checks/05_portfolio_transport.py',
        'v3/checks/05_ordinary_add.py',
        'v3/checks/05_add_evidence.py',
        'v3/checks/05_add_evidence_check.py',
        'v3/checks/05_certificate_delivery_service.py',
        'v3/checks/05_certificate_delivery_cases.py',
        'v3/checks/05_add_evidence_prune.py',
        'v3/checks/05_certificate_delivery_pruned_service.py',
        'v3/experiments/p309_certificates.py',
    ]


def _configuration_template():
    # All entries are protocol metadata. No formula, seed or case is made here.
    return {
        'schema': 'value_logic.p309.certificate_config.v1',
        'version': VERSION,
        'families': ['majority_dnf_cnf', 'selector_mux_sum'],
        'sizes': [4, 7],
        'edit_slots': ['initial', 'hard_rank_edit', 'nonoptimal_incumbent',
                       'weight_loss_scope_edit'],
        'fresh_methods': [*BASE_METHODS, PRUNED],
        'resident_methods': list(BASE_METHODS),
        'candidate_methods': ['P-REUSE'],
        'budget_conditions': [
            {'id': 'full', 'budget': 2**27, 'consumer_budget': None},
            {'id': 'capped', 'budget': 2**27, 'consumer_budget': 2**20},
        ],
        'budget_scope': 'PER_ATTEMPT_ACTUAL_STATEFUL_HISTORY_NOT_REPRICED_FULL_PATH',
        'full_budget_is_completion_guarantee': False,
        'consumer_cap_basis': 'PUBLISHED_DEVELOPMENT_2_POW_20_ENGINEERING_REGIME',
        'variable_order': 'ASCENDING_COORDINATE_INDEX',
        'random_seeds': [],
        'coverage': COVERAGE,
        'source_installation': 'COMMON_ELEVEN_FILE_SHARED_PROGRAM',
        'source_paths': source_paths(),
        'tariff': 'rp3bb-cpython31214-observed-events-plus-live-byte-periods-v1',
        'runtime': {'implementation': 'cpython', 'version': [3, 12, 14]},
        'limits': {
            'grammar_input_rational_component_bits': 128,
            'native_context_rational_component_bits': 128,
            'inherited_add_terminal_component_bits': 16384,
            'checked_add_terminal_component_bits': 4096,
            'checked_add_bits': 10,
            'checked_add_nodes': 100000,
            'checked_add_apply_or_expression_rows': 200000,
            'checked_add_receipts': 256,
            'wire_bytes': 32 * 1024 * 1024,
            'serialized_state_object_bytes': 64 * 1024 * 1024,
            'native_tree_nodes': 2047,
            'pruner_dependency_steps': 8000000,
            'failure_terminal_reserve': 1024,
        },
        'expected_groups': 4,
        'expected_histories': 104,
        'expected_delivery_attempts': 416,
        'population_unit': 'COMPLETE_GENERATOR_STREAM_NOT_INDEPENDENT_REQUEST_OR_METHOD',
        'fresh_pruned_resident_status': 'INELIGIBLE_NOT_MISSING',
        'cross_tariff_aggregation': False,
        'exposure_token_required': EXPOSURE_TOKEN,
    }


def _prepared_source_record():
    # Independent preparation supplies the full expected record. The worker
    # subsequently pays enrollment and verifies every actual source byte again.
    entries = []
    for relative in source_paths():
        path = ROOT / relative
        if path.is_symlink() or not path.is_file():
            raise ValueError('A regular source file is required: ' + relative)
        content = path.read_bytes()
        if not 1 <= len(content) <= 32 * 1024 * 1024:
            raise ValueError('Source file is outside the admitted byte cap.')
        entries.append({'path': relative, 'bytes': len(content),
                        'sha256': hashlib.sha256(content).hexdigest()})
    return _canonical({'schema': 'rp3bb.add-evidence-source.v1',
                       'evidence_schema': 'rp3bb.add-evidence.v1',
                       'sources': sorted(entries, key=lambda row: row['path'])})


def default_config():
    answer = _configuration_template()
    answer['expected_source_record'] = _prepared_source_record()
    return answer


def validate_config(config):
    if type(config) is not dict:
        raise ValueError('An exact certificate configuration is required.')
    expected = _configuration_template()
    if set(config) != set(expected) | {'expected_source_record'}:
        raise ValueError('Certificate configuration fields differ.')
    if _canonical({key: config[key] for key in expected}) != _canonical(expected):
        raise ValueError('Certificate methods, recipes, caps or service changed.')
    record = config['expected_source_record']
    if type(record) is not str or len(record.encode('ascii')) > 1024 * 1024:
        raise ValueError('A bounded complete expected source record is required.')
    value = json.loads(record)
    if (_canonical(value) != record
            or set(value) != {'schema', 'evidence_schema', 'sources'}
            or value['schema'] != 'rp3bb.add-evidence-source.v1'
            or value['evidence_schema'] != 'rp3bb.add-evidence.v1'):
        raise ValueError('Noncanonical source record.')
    rows = value['sources']
    if (type(rows) is not list or len(rows) != len(source_paths())
            or [row['path'] for row in rows] != sorted(source_paths())):
        raise ValueError('Full source closure differs.')
    for row in rows:
        if (set(row) != {'path', 'bytes', 'sha256'} or type(row['bytes']) is not int
                or not 1 <= row['bytes'] <= 32 * 1024 * 1024
                or type(row['sha256']) is not str or len(row['sha256']) != 64
                or any(c not in '0123456789abcdef' for c in row['sha256'])):
            raise ValueError('Malformed source binding.')
    # Do not silently authenticate a supplied digest here. Paid enrollment is
    # responsible for detecting live source-length or source-hash mismatch.
    return True


def groups(config):
    """Opaque public schedules only; no formulas or witnesses are instantiated."""
    validate_config(config)
    result = []
    for family in config['families']:
        for nbits in config['sizes']:
            result.append({
                'id': 'certificates-' + family.replace('_', '-') + '-n' + str(nbits),
                'arm': ARM,
                'recipe': {'family': family, 'version': 1, 'nbits': nbits,
                           'representation': 'FIXED_EXPANDED_ORDERED_EXPRESSION_TREES',
                           'generation': 'DETERMINISTIC_STRUCTURE_NOT_RESEEDING'},
                'request_count': 4,
            })
    return result


def _unit(group_id, method, recipient, condition):
    configuration_id = method + '.' + recipient + '.' + condition['id']
    return {'id': group_id + '.' + configuration_id,
            'group_id': group_id, 'arm': ARM,
            'method': method,
            'method_kind': 'candidate' if method == 'P-REUSE' else 'ordinary',
            'recipient': recipient, 'budget_condition': condition['id'],
            'configuration_id': configuration_id,
            'budget': condition['budget'], 'consumer_budget': condition['consumer_budget'],
            'request_count': 4}


def units(group, config):
    validate_config(config)
    if group not in groups(config):
        raise ValueError('Undeclared certificate group.')
    result = []
    for recipient, methods in (('fresh', config['fresh_methods']),
                               ('resident', config['resident_methods'])):
        for method in methods:
            for condition in config['budget_conditions']:
                result.append(_unit(group['id'], method, recipient, condition))
    return result


def _load(name, relative):
    if name in sys.modules:
        module = sys.modules[name]
        if Path(module.__file__).resolve() != (ROOT / relative).resolve():
            raise ImportError('A canonical worker module was loaded from another root.')
        return module
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise ImportError(relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class _WireInputMixin:
    """Convert public records inside paid stages, including after early denial."""
    def _execute(self, meter, frame_record, witness, bound, request_id, work):
        service = _REGISTRY[0]
        if not self.source_enrolled:
            self._enroll(meter)
        frame, point = meter.run('request_materialization', lambda: (
            service.frame_from_record(frame_record), tuple(witness)))
        return super()._execute(meter, frame, point, bound, request_id, work)

    def _bootstrap_producer(self, meter, work):
        # Conversion of the whole old-input tuple is atomic. A denial may leave
        # raw caller records or already converted caller Frames; neither is an
        # admitted proof. Failed scientific caches are evicted by the old owner.
        if self.old_specs and type(self.old_specs[0][0]) is str:
            service = _REGISTRY[0]
            converted = meter.run('producer_old_materialization', lambda: tuple(
                (service.frame_from_record(record), tuple(witness), service.K.rational(bound))
                for record, witness, bound in self.old_specs))
            self.old_specs = converted
        return super()._bootstrap_producer(meter, work)

    def _producer_state(self):
        # The base observer also calls this after failed source enrollment.
        # Preserve all raw old records then; never invoke .record() on a string
        # or lose an already paid failure invoice through observer cleanup.
        service = _REGISTRY[0]
        record = {
            'source_record': self.source_record, 'epoch': self._epoch(),
            'method': self.method, 'input_adapter': VERSION,
            'old_inputs': self.old_input_records,
            'old_request_inputs': [
                {'frame_record': old if type(old) is str else old.record(),
                 'witness': witness, 'bound': str(bound)}
                for old, witness, bound in self.old_specs],
            'old_packets': [packet.decode('ascii') for packet in self.old_packets],
            'portfolio_domains': None if self.producer_cache is None
                                 else service.portfolio_state(self.producer_cache),
            'add_manager': None if self.manager is None else self.manager.state_record(),
            'acknowledged_cursor': None if self.cursor is None else self.cursor.record(),
        }
        if hasattr(self, 'prune_limit_steps'):
            record['prune_limit_steps'] = self.prune_limit_steps
        return record


def _libraries():
    global _REGISTRY
    if _REGISTRY is None:
        pruned = _load('_p309_pruned_certificate_service',
                       'v3/checks/05_certificate_delivery_pruned_service.py')
        service = pruned.S
        if Path(service.__file__).resolve() != (ROOT / 'v3/checks/05_certificate_delivery_service.py').resolve():
            raise ImportError('The service registry belongs to another source root.')
        # The historical pruner expands its owned service registry at import.
        # Every method here uses this one expanded, source-bound installation.
        service.SOURCE_PATHS = tuple(source_paths())
        service.METHODS = (*BASE_METHODS, PRUNED)

        class WireSession(_WireInputMixin, service.Session):
            pass

        class WirePrunedSession(_WireInputMixin, pruned.PrunedSession):
            pass

        _REGISTRY = (service, pruned, WireSession, WirePrunedSession)
    if tuple(_REGISTRY[0].SOURCE_PATHS) != tuple(source_paths()):
        raise RuntimeError('Owned common source registry changed after initialization.')
    return _REGISTRY


def _frame(service, name, nbits, difference, hard=(), soft=(), *, version='v1', label='FINAL'):
    metadata = {'stage': label, 'adapter': VERSION, 'interpretation':
                'FIXED_BOOLEAN_COORDINATES_EXACT_RATIONAL_LOSS_AND_ONE_RANK_TIER',
                'frame_version': version, 'complete_scope': name}
    request = service.K.Request(nbits, tuple(hard), tuple(soft), (('D', difference),),
                                name, service.M.canonical(metadata))
    return service.M.Frame(request, 'D', 'declared-loss-unit')


def _fold(operation, values):
    values = tuple(values)
    if not values:
        raise ValueError('Nonempty fixed expression fold required.')
    answer = values[0]
    for value in values[1:]:
        answer = operation(answer, value)
    return answer


def _majority_identity(service, nbits):
    k = service.K
    left, right = [], []
    for start in range(1, nbits, 3):
        a, b, c = (k.bit(i) for i in range(start, start + 3))
        left.append(_fold(k.OR, (k.AND(a, b), k.AND(a, c), k.AND(b, c))))
        right.append(_fold(k.AND, (k.OR(a, b), k.OR(a, c), k.OR(b, c))))
    return _fold(k.AND, left), _fold(k.AND, right)


def _mux_identity(service, nbits):
    k = service.K
    address_bits = 1 if nbits == 4 else 2
    selectors = tuple(k.bit(1 + i) for i in range(address_bits))
    data = tuple(k.bit(1 + address_bits + i) for i in range(1 << address_bits))

    def nested(depth, index):
        if depth == address_bits:
            return data[index]
        low = nested(depth + 1, index << 1)
        high = nested(depth + 1, (index << 1) | 1)
        return k.OR(k.AND(k.neg(selectors[depth]), low), k.AND(selectors[depth], high))

    terms = []
    for index, datum in enumerate(data):
        guard = tuple(selector if index & (1 << (address_bits - 1 - j)) else k.neg(selector)
                      for j, selector in enumerate(selectors))
        terms.append(k.AND(_fold(k.AND, guard), datum))
    # The guards are mutually exclusive. Their arithmetic sum is Boolean in
    # denotation but deliberately remains an admitted numeric expression.
    return nested(0, 0), _fold(k.add, terms)


def _case_record(group_id, slot, frame, witness, bound):
    return {'id': group_id + '.r' + str(slot), 'slot': slot,
            'frame_record': frame.record(), 'witness': list(witness), 'bound': str(bound)}


def _generate_exposed(group):
    # This function is reachable from generate only after the exposure barrier.
    # selfcheck never calls it or either final-family expression constructor.
    service = _libraries()[0]
    k = service.K
    recipe, name = group['recipe'], group['id']
    nbits = recipe['nbits']
    left, right = (_majority_identity(service, nbits)
                   if recipe['family'] == 'majority_dnf_cnf' else _mux_identity(service, nbits))
    base_difference = k.add(k.sub(k.scale(2, k.bit(0)), k.lit(1)), k.sub(left, right))
    old = []
    for z in (0, 1):
        point = (z,) + (0,) * (nbits - 1)
        hard = (k.neg(k.bit(0)) if z == 0 else k.bit(0),)
        frame = _frame(service, name + '.old-z' + str(z), nbits, base_difference, hard)
        old.append({'frame_record': frame.record(), 'witness': list(point),
                    'bound': str(2 * z - 1)})
    zero = (0,) * nbits
    normal = [0] * nbits
    normal[1] = normal[3] = 1
    nonoptimal = list(normal)
    nonoptimal[3] = 0
    hard = (k.OR(k.bit(1), k.bit(2)),)
    soft = (k.Soft('normal-third-coordinate', k.bit(3), k.rational(1), 0),)
    shifted = k.add(base_difference, k.lit('1/2'))
    frames = [
        _frame(service, name + '.initial', nbits, base_difference),
        _frame(service, name + '.hard-rank-edit', nbits, base_difference, hard, soft),
        _frame(service, name + '.nonoptimal-incumbent', nbits, base_difference, hard, soft),
        _frame(service, name + '.weight-loss-scope-edit', nbits, shifted, hard,
               (k.Soft('normal-third-coordinate', k.bit(3), k.rational(2), 0),), version='v2'),
    ]
    witnesses = [zero, tuple(normal), tuple(nonoptimal), tuple(normal)]
    bounds = ['1', '1', '1', '3/2']
    return {'schema': INPUT_SCHEMA, 'version': VERSION, 'stage': 'FINAL_EXPOSED',
            'group_id': name, 'recipe': recipe, 'nbits': nbits,
            'order': list(range(nbits)), 'old_specs': old,
            'cases': [_case_record(name, index + 1, frame, witness, bound)
                      for index, (frame, witness, bound) in enumerate(zip(frames, witnesses, bounds))]}


def generate(group, config, *, exposure_token):
    if type(exposure_token) is not str or exposure_token != EXPOSURE_TOKEN:
        raise PermissionError('Final certificate generation requires P3-10-EXPOSED.')
    validate_config(config)
    if group not in groups(config):
        raise ValueError('Undeclared certificate generator recipe.')
    return _generate_exposed(group)


def _validate_unit(unit, config):
    validate_config(config)
    if type(unit) is not dict:
        raise ValueError('An exact method unit is required.')
    methods = config.get(unit.get('recipient', '') + '_methods', ())
    conditions = [row for row in config['budget_conditions'] if row['id'] == unit.get('budget_condition')]
    if (unit.get('arm') != ARM or unit.get('method') not in methods
            or len(conditions) != 1
            or unit != _unit(unit.get('group_id'), unit.get('method'), unit.get('recipient'), conditions[0])):
        raise ValueError('Undeclared method, recipient, budget or unit binding.')


def _validate_public(public_input, unit):
    if (type(public_input) is not dict or public_input.get('schema') != INPUT_SCHEMA
            or public_input.get('version') != VERSION
            or public_input.get('stage') not in ('DEVELOPMENT', 'FINAL_EXPOSED')
            or public_input.get('group_id') != unit['group_id']):
        raise ValueError('Public input is not bound to this complete history.')
    nbits = public_input.get('nbits')
    order = public_input.get('order')
    if (type(nbits) is not int or not 1 <= nbits <= 10 or type(order) is not list
            or any(type(value) is not int for value in order)
            or sorted(order) != list(range(nbits))):
        raise ValueError('Bounded coordinate order required.')
    cases = public_input.get('cases')
    old = public_input.get('old_specs')
    if type(cases) is not list or len(cases) != 4 or type(old) is not list or len(old) > 16:
        raise ValueError('Complete four-request history and bounded old catalogue required.')
    for index, row in enumerate(cases, 1):
        if (type(row) is not dict or set(row) != {'id', 'slot', 'frame_record', 'witness', 'bound'}
                or row['slot'] != index or type(row['slot']) is not int
                or row['id'] != unit['group_id'] + '.r' + str(index)):
            raise ValueError('Current request identity or slot differs.')
    for row in [*old, *cases]:
        if (type(row['frame_record']) is not str or type(row['witness']) is not list
                or type(row['bound']) is not str):
            raise ValueError('Public canonical input records required.')
    # Grammar, canonical record, rational, witness and feasibility validation
    # occur inside paid workers. This check is only schedule/input routing.


def _new_session(unit, public_input, config):
    service, pruned, ordinary, pruned_class = _libraries()
    name, nbits, order = unit['group_id'], public_input['nbits'], public_input['order']
    source = config['expected_source_record']
    if unit['method'] == PRUNED:
        return pruned_class(name, nbits, order, source)
    old = (tuple((row['frame_record'], row['witness'], row['bound'])
                 for row in public_input['old_specs'])
           if unit['method'] in ('P-REUSE', 'O-ADD-PORTFOLIO') else ())
    return ordinary(unit['method'], unit['recipient'], name, nbits, order, old, source)


def _json_paid_row(row):
    # Experiment capture is outside the service. The retained bytes below were
    # already priced by the worker before this lossless observer encoding.
    answer = dict(row)
    answer['audit_packets'] = [
        {'stage': stage, 'category': category, 'bytes': len(payload),
         'sha256': hashlib.sha256(payload).hexdigest(),
         'payload_base64': base64.b64encode(payload).decode('ascii')}
        for stage, category, payload in row['audit_packets']]
    return answer


def run(unit, public_input, config):
    """Execute a complete paid history. No independent truth routine is called."""
    _validate_unit(unit, config)
    _validate_public(public_input, unit)
    session = _new_session(unit, public_input, config)
    rows, previous = [], None
    for case in public_input['cases']:
        raw = session.deliver(case['frame_record'], case['witness'], case['bound'],
                              budget=unit['budget'], consumer_budget=unit['consumer_budget'])
        row = _json_paid_row(raw)
        row['shared_request_id'] = case['id']
        row['observer_current_receipt_present'] = session.current_receipt(raw['request_id']) is not None
        row['observer_previous_receipt_stale'] = previous is None or session.current_receipt(previous) is None
        previous = raw['request_id']
        rows.append(row)
    return {'schema': RESULT_SCHEMA, 'version': VERSION, 'stage': public_input['stage'],
            'unit': unit, 'group_id': unit['group_id'], 'request_count': 4,
            'tariff': config['tariff'], 'rows': rows,
            'truth_reference_called': False,
            'observer_packet_encoding_is_service_charge': False,
            'history_rule': 'ONE_FRESH_OWNER_EVICT_ON_ANY_FAILED_ATTEMPT_CONTINUE_FIXED_EDIT_ORDER'}


def _consumer_stage(stage):
    return stage.startswith('receiver_') or stage in ('terminal', 'failure_terminal', 'common_source')


def _invoice_totals(invoice, unit):
    stages = invoice['by_stage']
    if type(stages) is not dict:
        raise ValueError('Missing complete stage invoice.')
    total = consumer = 0
    categories = Counter()
    for stage, row in stages.items():
        if type(stage) is not str or type(row) is not dict:
            raise ValueError('Malformed tariff stage.')
        if any(type(key) is not str or type(value) is not int or value < 0 for key, value in row.items()):
            raise ValueError('Exact nonnegative tariff category counts required.')
        amount = sum(row.values())
        total += amount
        consumer += amount if _consumer_stage(stage) else 0
        categories.update(row)
    if (type(invoice['total_units']) is not int or invoice['total_units'] != total
            or type(invoice['consumer_units']) is not int or invoice['consumer_units'] != consumer
            or invoice['budget'] != unit['budget'] or invoice['consumer_budget'] != unit['consumer_budget']
            or total > unit['budget'] or consumer > total
            or (unit['consumer_budget'] is not None and consumer > unit['consumer_budget'])
            or invoice['failure_terminal_reserve'] != 1024):
        raise ValueError('Paid invoice does not reconcile with the actual account.')
    if invoice['failure'] is not None:
        if stages.get('failure_terminal') != {
                'delivery_events': 1, 'state_eviction_events': 1, 'terminal_bytes': 111}:
            raise ValueError('Incomplete paid fixed failure receipt.')
    elif 'failure_terminal' in stages:
        raise ValueError('A successful invoice contains a failure terminal.')
    partition = {'producer': total - consumer, 'consumer': consumer,
                 'output': sum(value for key, value in categories.items()
                               if key.endswith('_output_bytes') or key == 'terminal_bytes'),
                 'storage': categories.get('live_serialized_byte_periods', 0),
                 'source': sum(stages.get('common_source', {}).values())}
    return total, consumer, categories, partition


def score(unit, result, public_input, config):
    """Independent truth/service audit, scheduled only after all public runs."""
    _validate_unit(unit, config)
    _validate_public(public_input, unit)
    service = _libraries()[0]
    reference = _load('_p309_certificate_scalar_reference',
                      'v3/checks/05_certificate_delivery_cases.py')
    errors = []
    rows = result.get('rows', []) if type(result) is dict else []
    if (type(result) is not dict or result.get('schema') != RESULT_SCHEMA
            or result.get('unit') != unit or result.get('group_id') != unit['group_id']
            or result.get('request_count') != 4 or result.get('truth_reference_called') is not False
            or type(rows) is not list or len(rows) != 4):
        raise ValueError('Outer paid result/unit binding or complete history differs.')
    all_ids = [case['id'] for case in public_input['cases']]
    delivered, diagnostics = [], []
    totals, categories, partition = [], Counter(), Counter()
    unknown_cost = False
    for index, case in enumerate(public_input['cases']):
        frame = service.frame_from_record(case['frame_record'])
        expected = reference.scalar_report(frame, tuple(case['witness']), case['bound'],
                                           expected_current_record=case['frame_record'])
        if index >= len(rows):
            errors.append(case['id'] + ': missing paid attempt.')
            unknown_cost = True
            continue
        row = rows[index]
        local_errors = []
        accepted_delivery = False
        try:
            invoice = row['invoice']
            total, consumer, raw_categories, raw_partition = _invoice_totals(invoice, unit)
            if invoice['tariff'] != config['tariff']:
                raise ValueError('Unexpected tariff.')
            totals.append(total)
            categories.update(raw_categories)
            partition.update(raw_partition)
        except (ValueError, KeyError, TypeError) as error:
            local_errors.append('Unknown or inconsistent paid cost: ' + str(error))
            unknown_cost = True
        expected_receipt_id = unit['group_id'] + ':' + str(index + 1)
        if (row.get('shared_request_id') != case['id'] or row.get('request_id') != expected_receipt_id
                or row.get('request_index') != index + 1 or row.get('method') != unit['method']
                or row.get('recipient') != unit['recipient'] or row.get('stream') != unit['group_id']
                or row.get('observer_previous_receipt_stale') is not True):
            local_errors.append('Current attempt identity, method or stale-receipt withdrawal differs.')
        try:
            output = service.decode(row['output'].encode('ascii'))
            if row['status'] == 'DELIVERED':
                exact = {key: expected[key] for key in
                         ('status', 'current_record', 'bound', 'incumbent_rank', 'feasibility', 'coverage')}
                exact.update(schema='rp3bb.current-bound.v1', request_id=expected_receipt_id,
                             unit=frame.unit, witness=case['witness'],
                             source_record=config['expected_source_record'])
                if (not expected['holds'] or output != exact
                        or row.get('observer_current_receipt_present') is not True
                        or row['invoice']['failure'] is not None or row['error'] is not None):
                    local_errors.append('Delivered output is not the exact true current full-sublevel service.')
                else:
                    accepted_delivery = True
            elif row['status'] == 'NO_CURRENT_CERTIFICATE':
                if (output != {'schema': 'rp3bb.current-bound.v1', 'status': 'NO_CURRENT_CERTIFICATE',
                               'reason': 'RESOURCE_OR_VALIDATION_FAILURE'}
                        or row.get('observer_current_receipt_present') is not False
                        or row['invoice']['failure'] is None or row['error'] is None):
                    local_errors.append('Failure incorrectly publishes a current certificate or omits its bill.')
            else:
                local_errors.append('Unknown paid delivery status.')
        except (ValueError, KeyError, TypeError, UnicodeError) as error:
            local_errors.append('Malformed terminal output: ' + str(error))
        # Byte-for-byte audit preservation is an observer integrity check. It
        # neither supplies truth to workers nor imports unverified proof roots.
        for packet in row.get('audit_packets', []):
            try:
                payload = base64.b64decode(packet['payload_base64'], validate=True)
                if len(payload) != packet['bytes'] or hashlib.sha256(payload).hexdigest() != packet['sha256']:
                    raise ValueError('Captured byte packet digest/length differs.')
            except (ValueError, KeyError, TypeError) as error:
                local_errors.append('Invalid captured worker packet: ' + str(error))
        if accepted_delivery and not local_errors:
            delivered.append(case['id'])
        errors.extend(case['id'] + ': ' + error for error in local_errors)
        diagnostics.append({'request_id': case['id'], 'receipt_id': expected_receipt_id,
                            'delivery_status': row.get('status'), 'truth_status': expected['status'],
                            'oracle': expected['diagnostics'], 'incumbent_rank': expected['incumbent_rank'],
                            'request_validity_pass': not local_errors})
    return {'schema': SCORE_SCHEMA, 'version': VERSION,
            'stage': 'DEVELOPMENT_EVALUATION' if public_input['stage'] == 'DEVELOPMENT' else 'PRIVATE_EVALUATION',
            'status': 'PASS' if not errors else 'FAIL', 'validity_pass': not errors,
            'unit': unit, 'group_id': unit['group_id'], 'method': unit['method'],
            'method_kind': unit['method_kind'], 'recipient': unit['recipient'],
            'budget_condition': unit['budget_condition'], 'configuration_id': unit['configuration_id'],
            'request_count': 4, 'all_request_ids': all_ids,
            'delivered_request_ids': delivered,
            'full_service_delivered': len(delivered) == 4 and not errors,
            'total_units': None if unknown_cost else sum(totals),
            'consumer_units': None if unknown_cost else partition['consumer'],
            'category_totals': dict(sorted(partition.items())),
            'tariff_category_totals': dict(sorted(categories.items())),
            'category_totals_complete': not unknown_cost,
            'category_convention': 'PRODUCER_IS_ALL_NONCONSUMER; OUTPUT_STORAGE_SOURCE_ARE_OVERLAPPING_DIAGNOSTICS',
            'tariff': config['tariff'], 'errors': errors, 'requests': diagnostics,
            'population_recipe': public_input['recipe'],
            'failed_attempt_costs_included': not unknown_cost,
            'retrospective_threshold_flags_used_as_funding': False,
            'truth_reference_is_priced_worker': False}


def _development_input(service):
    # Explicit two-bit constants/normality. None of the final constructors,
    # dimension strata, group enumeration or recipe functions is invoked.
    k = service.K
    name = 'certificates-DEVELOPMENT-two-bit-constant-rank'
    old = []
    for z in (0, 1):
        frame = _frame(service, name + '.old' + str(z), 2, k.lit(0),
                       (k.bit(1) if z else k.neg(k.bit(1)),), label='DEVELOPMENT')
        old.append({'frame_record': frame.record(), 'witness': [0, z], 'bound': '0'})
    soft = (k.Soft('normal-first', k.bit(0), k.rational(1), 0),)
    cases = []
    for slot, value in enumerate((0, 1, 0, 0), 1):
        frame = _frame(service, name + '.request' + str(slot), 2, k.lit(value), (), soft,
                       version='v' + str(slot), label='DEVELOPMENT')
        cases.append(_case_record(name, slot, frame, (0, 0), '0'))
    return {'schema': INPUT_SCHEMA, 'version': VERSION, 'stage': 'DEVELOPMENT',
            'group_id': name, 'recipe': {'family': 'DEVELOPMENT_constant_rank_only', 'nbits': 2},
            'nbits': 2, 'order': [0, 1], 'old_specs': old, 'cases': cases}


def selfcheck():
    """Separate development endpoint. It never instantiates a final recipe."""
    config = default_config()
    service = _libraries()[0]
    public = _development_input(service)
    condition = {'id': 'full', 'budget': 2**27, 'consumer_budget': None}
    histories, failures = [], []
    for recipient, methods in (('fresh', [*BASE_METHODS, PRUNED]), ('resident', BASE_METHODS)):
        for method in methods:
            unit = _unit(public['group_id'], method, recipient, condition)
            result = run(unit, public, config)
            evaluated = score(unit, result, public, config)
            statuses = [row['status'] for row in result['rows']]
            desired = ['DELIVERED', 'NO_CURRENT_CERTIFICATE', 'DELIVERED', 'DELIVERED']
            okay = (statuses == desired and evaluated['validity_pass']
                    and all(row['oracle']['minimizer_count'] == 2
                            and row['oracle']['sublevel_count'] == 4 for row in evaluated['requests']))
            if not okay:
                failures.append(method + '/' + recipient)
            histories.append({'method': method, 'recipient': recipient, 'passed': okay,
                              'statuses': statuses, 'score': evaluated,
                              'paid_rows': [{key: value for key, value in row.items() if key != 'audit_packets'}
                                            for row in result['rows']]})
    # A current success, a reserve-only failure and recovery use a fresh owned
    # resident P-REUSE session, still on the same explicitly development toy.
    unit = _unit(public['group_id'] + '-reserve', 'P-REUSE', 'resident', condition)
    session = _new_session(unit, public, config)
    toy = public['cases'][0]
    reserve_rows = []
    for budget in (2**27, 1024, 2**27):
        row = session.deliver(toy['frame_record'], toy['witness'], toy['bound'], budget=budget)
        row = {key: value for key, value in row.items() if key != 'audit_packets'}
        row['current_present'] = session.current_receipt(row['request_id']) is not None
        reserve_rows.append(row)
    reserve_ok = ([row['status'] for row in reserve_rows] ==
                  ['DELIVERED', 'NO_CURRENT_CERTIFICATE', 'DELIVERED']
                  and reserve_rows[1]['invoice']['total_units'] == 113
                  and reserve_rows[1]['current_present'] is False
                  and session.current_receipt(reserve_rows[0]['request_id']) is None
                  and session.current_receipt(reserve_rows[1]['request_id']) is None)
    if not reserve_ok:
        failures.append('reserve-only-paid-failure-and-recovery')
    answer = {'schema': 'value_logic.p309.certificate_selfcheck.v1', 'stage': 'DEVELOPMENT',
              'status': 'PASS' if not failures else 'FAIL',
              'passed': not failures, 'final_population_generated': False,
              'final_groups_or_generators_called': False, 'seed_used': False,
              'history_count': len(histories), 'paid_attempt_count': 4 * len(histories) + 3,
              'source_record': config['expected_source_record'],
              'histories': histories, 'reserve_probe': {'passed': reserve_ok, 'paid_rows': reserve_rows},
              'failures': failures, 'principal_clock_credit_seconds': 0}
    if failures:
        raise AssertionError(_canonical(answer))
    return answer
