#!/usr/bin/env python3
'''Independent P3-10-A1 broker arithmetic observer. Standard-library JSON only.

Contributor: ChatGPT (GPT-6 Astra Pro), agent /root/freeze_review.
No frozen code is imported. No paid method is replayed. Final reads require
an explicit principal-completion release receipt. Each observer attempt is new.
'''
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys
import traceback


def utc():
    return datetime.now(timezone.utc).isoformat()


def wire(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def digest(value, newline=False):
    return hashlib.sha256((wire(value) + ('\n' if newline else '')).encode('ascii')).hexdigest()


def frac(value):
    if value is None:
        return None
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    if type(value) is list and len(value) == 2 and all(type(x) is int for x in value) and value[1] > 0:
        return Fraction(value[0], value[1])
    if type(value) is str:
        return Fraction(value)
    raise TypeError('Expected an exact rational, got ' + repr(value))


def pair(value):
    value = frac(value)
    return None if value is None else [value.numerator, value.denominator]


def compatible_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('Duplicate JSON key: ' + key)
        out[key] = value
    return out


def decode(data):
    return json.loads(data, object_pairs_hook=compatible_pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))


def write_new(path, value):
    data = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + '\n').encode('utf-8')
    with path.open('xb') as stream:
        stream.write(data)


class Audit:
    def __init__(self, repo, out):
        self.repo, self.out = repo, out
        self.files, self.mismatches = {}, []
        self.comparisons = 0

    def load(self, path):
        path = path.resolve()
        data = path.read_bytes()
        record = {'path': str(path.relative_to(self.repo)), 'bytes': len(data),
                  'sha256': hashlib.sha256(data).hexdigest()}
        prior = self.files.get(record['path'])
        if prior is not None and prior != record:
            raise ValueError('Input changed during observation: ' + record['path'])
        self.files[record['path']] = record
        return decode(data)

    def check(self, label, got, wanted):
        if type(wanted) is dict:
            if type(got) is not dict:
                self.check(label + '.__type__', type(got).__name__, 'dict')
                return
            for key, value in wanted.items():
                self.check(label + '.' + key, got.get(key, '<MISSING>'), value)
            return
        if type(wanted) is list and wanted and type(wanted[0]) is dict and type(got) is list:
            self.check(label + '.__length__', len(got), len(wanted))
            for index, (a, b) in enumerate(zip(got, wanted)):
                self.check(label + '[' + str(index) + ']', a, b)
            return
        self.comparisons += 1
        if wire(got) != wire(wanted):
            self.mismatches.append({'field': label, 'observed': got, 'reconstructed': wanted})

    def require(self, value, message):
        if not value:
            raise ValueError(message)


class SealedStage:
    def __init__(self, audit, final, name, expected, binding):
        self.audit, self.final, self.name = audit, final, name
        self.expected = {unit['id']: unit for unit in expected}
        audit.require(len(self.expected) == len(expected), 'Duplicate expected unit')
        self.identity = {'stage': name, 'binding': binding, 'schedule_sha256': digest(expected, newline=True)}
        manifest = audit.load(final / 'stages' / name / 'schedule.json')
        audit.check(name + '.schedule', manifest, dict(self.identity, units=expected))
        completion = audit.load(final / 'stages' / name / 'complete.json')
        audit.check(name + '.completion', completion, dict(self.identity,
                    expected_units=len(expected), completed_units=len(expected)))
        self.seals = {row['unit_id']: row for row in completion['seals']}
        audit.require(len(self.seals) == len(completion['seals']) and set(self.seals) == set(self.expected),
                      'Completion index differs from complete expected unit universe: ' + name)

    def get(self, unit_id):
        audit, record = self.audit, self.seals[unit_id]
        path = (self.final / record['path']).resolve()
        expected_parent = (self.final / 'stages' / self.name / 'units' / unit_id).resolve()
        audit.require(path.name == 'seal.json' and path.parent.parent == expected_parent,
                      'Seal path is outside its exact unit directory')
        seal = audit.load(path)
        audit.check(self.name + '.' + unit_id + '.seal_hash', audit.files[str(path.relative_to(audit.repo))]['sha256'], record['sha256'])
        unit = self.expected[unit_id]
        audit.check(self.name + '.' + unit_id + '.seal', seal,
                    {'identity': self.identity, 'unit_sha256': digest(unit, newline=True)})
        result_path, start_path = path.parent / 'result.json', path.parent / 'start.json'
        result, start = audit.load(result_path), audit.load(start_path)
        for p, key in ((result_path, 'result_sha256'), (start_path, 'start_sha256')):
            audit.check(self.name + '.' + unit_id + '.' + key,
                        audit.files[str(p.relative_to(audit.repo))]['sha256'], seal[key])
        audit.check(self.name + '.' + unit_id + '.result_binding', result,
                    {'identity': self.identity, 'unit': unit, 'attempt': seal['attempt']})
        audit.check(self.name + '.' + unit_id + '.start_binding', start,
                    {'identity': self.identity, 'unit': unit, 'attempt': seal['attempt']})
        return result['value'], seal['result_sha256']


A1_ID = 'P3-10-A1'
A1_MANIFEST_SHA256 = '36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359'
ORIGINAL_MANIFEST_SHA256 = '69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70'
ORIGINAL_PROTOCOL_SHA256 = 'dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f'
ORIGINAL_FAILURE_SHA256 = '8a218fcdd465af660962cc608dbd87ecfecc46fcd9f673a63c01a0b7e4184d12'


def bound_file(audit, path):
    """Hash bytes without decoding payloads; retain the exact observer read set."""
    path = path.resolve()
    h, count = hashlib.sha256(), 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
            count += len(block)
    record = {'path': str(path.relative_to(audit.repo)), 'bytes': count, 'sha256': h.hexdigest()}
    prior = audit.files.get(record['path'])
    audit.require(prior is None or prior == record, 'Input changed during observation: ' + record['path'])
    audit.files[record['path']] = record
    return record


def exact(audit, label, got, wanted):
    audit.check(label, got, wanted)
    audit.require(wire(got) == wire(wanted), 'Provenance mismatch: ' + label)


def fields(audit, label, got, wanted):
    audit.check(label, got, wanted)
    audit.require(type(got) is dict and all(key in got and wire(got[key]) == wire(value)
                  for key, value in wanted.items()), 'Provenance fields mismatch: ' + label)


def repository_path(audit, relative):
    p = Path(relative)
    audit.require(type(relative) is str and not p.is_absolute() and '..' not in p.parts
                  and p.as_posix() == relative, 'Noncanonical repository-relative path')
    path = audit.repo / p
    audit.require(path.is_file() and not path.is_symlink() and path.resolve() == path,
                  'Missing or symbolic provenance file: ' + relative)
    return path


def inventory(audit, name, rows, within=None):
    audit.require(type(rows) is list and len({row['path'] for row in rows}) == len(rows),
                  'Duplicate or malformed evidence inventory: ' + name)
    for row in rows:
        path = repository_path(audit, row['path'])
        if within is not None:
            audit.require(path.is_relative_to(within), 'Evidence outside its original root')
        observed = bound_file(audit, path)
        fields(audit, name + '.' + row['path'], observed,
               {'path': row['path'], 'bytes': row['bytes'], 'sha256': row['sha256']})


class ReferencedOriginalPublic(SealedStage):
    """Original 500-unit identity, with only its 440 immutable completion references."""
    def __init__(self, audit, final, expected, binding, references):
        self.audit, self.final, self.name = audit, final, 'public'
        self.expected = {unit['id']: unit for unit in expected}
        self.identity = {'stage': 'public', 'binding': binding,
                         'schedule_sha256': digest(expected, newline=True)}
        exact(audit, 'original_public.schedule', audit.load(final / 'stages/public/schedule.json'),
              dict(self.identity, schema='value_logic.p309.stage.v1', units=expected))
        self.seals = {r['unit_id']: {'unit_id': r['unit_id'], 'path': r['seal_path'],
                                   'sha256': r['seal_sha256']} for r in references}
        audit.require(len(self.seals) == len(references), 'Repeated original reference')
        exact(audit, 'original_public.reference_universe', sorted(self.seals),
              sorted(u['id'] for u in expected if u['arm'] in ('broker', 'certificates')))


class CompositePublic:
    def __init__(self, original, amended):
        self.original, self.amended = original, amended

    def get(self, unit_id):
        stage = self.original if unit_id in self.original.seals else self.amended
        return stage.get(unit_id)


def bind_seal_metadata(stage, unit_id):
    """Verify metadata plus result bytes, without decoding the result payload."""
    audit = stage.audit
    index = stage.seals[unit_id]
    p = Path(index['path'])
    audit.require(not p.is_absolute() and '..' not in p.parts and p.as_posix() == index['path'],
                  'Noncanonical seal reference')
    path = stage.final / p
    expected_parent = stage.final / 'stages' / stage.name / 'units' / unit_id
    audit.require(path.is_file() and not path.is_symlink() and path.resolve() == path
                  and path.name == 'seal.json' and path.parent.parent == expected_parent,
                  'Seal outside its exact immutable unit directory')
    actual_seals = list(expected_parent.glob('attempt_*/seal.json'))
    audit.require(len(actual_seals) == 1 and actual_seals[0] == path,
                  'Unit does not have exactly one referenced completion seal')
    seal = audit.load(path)
    fields(audit, stage.name + '.' + unit_id + '.metadata_seal', seal,
           {'schema': 'value_logic.p309.unit_seal.v1', 'identity': stage.identity,
            'unit_sha256': digest(stage.expected[unit_id], newline=True)})
    exact(audit, unit_id + '.metadata_seal_hash', bound_file(audit, path)['sha256'], index['sha256'])
    audit.require(type(seal['attempt']) is int and 1 <= seal['attempt'] <= 2
                  and path.parent.name == 'attempt_%02d' % seal['attempt'], 'Invalid bound attempt directory')
    start_path, result_path = path.parent / 'start.json', path.parent / 'result.json'
    start = audit.load(start_path)
    fields(audit, unit_id + '.metadata_start', start,
           {'schema': 'value_logic.p309.unit_start.v1', 'identity': stage.identity,
            'unit': stage.expected[unit_id], 'attempt': seal['attempt']})
    exact(audit, unit_id + '.metadata_start_hash', bound_file(audit, start_path)['sha256'], seal['start_sha256'])
    exact(audit, unit_id + '.metadata_result_hash', bound_file(audit, result_path)['sha256'], seal['result_sha256'])
    return {'unit_id': unit_id, 'origin_root': stage.final.relative_to(audit.repo).as_posix(),
            'seal_path': path.relative_to(stage.final).as_posix(),
            'seal_sha256': index['sha256'],
            'result_path': result_path.relative_to(stage.final).as_posix(),
            'result_sha256': seal['result_sha256']}


def a1_stages(audit, repo, release, freeze, schedule, old_binding):
    """Independently reconstruct A1 lineage. No producer/helper code is imported."""
    old = repo / 'v3/experiments/final_v1'
    new = repo / 'v3/experiments/final_v1_amended_A1'
    amendment = repo / 'v3/experiments/amendments/P3_10_A1'
    exact(audit, 'pinned_original_manifest', old_binding['manifest_sha256'], ORIGINAL_MANIFEST_SHA256)
    exact(audit, 'pinned_original_protocol', old_binding['protocol_sha256'], ORIGINAL_PROTOCOL_SHA256)
    for stage in ('public', 'evaluation', 'analysis'):
        audit.require((new / 'stages' / stage / 'complete.json').is_file(),
                      'All amended public/evaluation/analysis completions are required')
    audit.require((old / 'stages/inputs/complete.json').is_file()
                  and not (old / 'stages/public/complete.json').exists()
                  and not (old / 'stages/evaluation').exists() and not (old / 'stages/analysis').exists(),
                  'Original failed lineage was changed or private work started there')
    manifest_path = amendment / 'manifest.json'
    manifest = audit.load(manifest_path)
    manifest_hash = bound_file(audit, manifest_path)['sha256']
    exact(audit, 'pinned_amendment_manifest', manifest_hash, A1_MANIFEST_SHA256)
    exact(audit, 'released_amendment_manifest', manifest_hash, release['amendment_manifest_sha256'])
    fields(audit, 'amendment_manifest', manifest,
           {'amendment_id': A1_ID, 'status': 'SEALED_BEFORE_AMENDED_EXECUTION',
            'original_manifest_sha256': ORIGINAL_MANIFEST_SHA256,
            'original_protocol_sha256': ORIGINAL_PROTOCOL_SHA256,
            'original_failure_sha256': ORIGINAL_FAILURE_SHA256,
            'original_public_stage_complete': False, 'original_private_evaluation_started': False,
            'new_input_generations': 0, 'original_failed_prefix_cost': 'unknown'})
    inventory(audit, 'original_evidence', manifest['original_evidence'], within=old)
    actual_paths = sorted(p.relative_to(repo).as_posix() for p in old.rglob('*')
                          if p.is_file() and p.name != 'writer.lock')
    exact(audit, 'original_evidence_exact_roster', actual_paths,
          sorted(row['path'] for row in manifest['original_evidence']))
    inventory(audit, 'amendment_sources', manifest['new_sources'])
    for row in manifest['new_sources']:
        snapshot = amendment / 'source' / row['path']
        fields(audit, 'amendment_source_snapshot.' + row['path'], bound_file(audit, snapshot),
               {'bytes': row['bytes'], 'sha256': row['sha256']})
    for name, key in (('protocol.json', 'amendment_protocol_sha256'), ('protocol.md', 'amendment_prose_sha256')):
        exact(audit, 'amendment_' + name, bound_file(audit, amendment / name)['sha256'], manifest[key])
    exact(audit, 'original_failure', bound_file(audit, old / 'stages/public/attempts/attempt_01/failure.json')['sha256'],
          ORIGINAL_FAILURE_SHA256)
    binding = dict(old_binding, amendment_id=A1_ID, amendment_manifest_sha256=manifest_hash)
    exact(audit, 'amendment_binding', audit.load(new / 'amendment_binding.json'), binding)
    all_units, groups = schedule['units'], schedule['groups']
    remaining = [u for u in all_units if u['arm'] == 'conformance']
    reused = [u for u in all_units if u['arm'] in ('broker', 'certificates')]
    exact(audit, 'amendment_remaining_schedule', manifest['remaining_public_units'], remaining)
    exact(audit, 'amendment_reuse_schedule', manifest['reused_public_unit_ids'], [u['id'] for u in reused])
    exact(audit, 'a1_unit_counts', [len(groups), len(all_units), len(reused), len(remaining)], [12, 500, 440, 60])
    before = len(audit.mismatches)
    inputs = SealedStage(audit, old, 'inputs', groups, old_binding)
    amended_public = SealedStage(audit, new, 'public', remaining, binding)
    evaluation = SealedStage(audit, new, 'evaluation',
        [dict(u, id='score-' + u['id'], public_unit_id=u['id']) for u in all_units], binding)
    analysis = SealedStage(audit, new, 'analysis', [{'id': 'all-frozen-endpoints', 'arm': 'analysis'}], binding)
    audit.require(len(audit.mismatches) == before, 'Stage schedule/completion binding mismatch')
    composite = audit.load(new / 'composite_public.json')
    fields(audit, 'composite_public', composite,
           {'schema': 'value_logic.p310_a1.composite_public.v1', 'binding': binding,
            'expected_units': 500, 'completed_units': 500, 'original_units': 440, 'amended_units': 60,
            'original_public_stage_complete': False, 'original_failure_sha256': ORIGINAL_FAILURE_SHA256})
    exact(audit, 'composite_ordered_universe', [r['unit_id'] for r in composite['seals']], [u['id'] for u in all_units])
    original_refs = [r for r, u in zip(composite['seals'], all_units) if u['arm'] != 'conformance']
    original_public = ReferencedOriginalPublic(audit, old, all_units, old_binding, original_refs)
    input_ref = audit.load(new / 'input_reference.json')
    fields(audit, 'input_reference', input_ref,
           {'schema': 'value_logic.p310_a1.input_reference.v1', 'binding': binding,
            'expected_units': 12, 'completed_units': 12, 'new_generations': 0,
            'original_exposure_sha256': bound_file(audit, old / 'exposure.json')['sha256']})
    exact(audit, 'input_reference_ordered_universe', [r['unit_id'] for r in input_ref['seals']], [g['id'] for g in groups])
    for group, ref in zip(groups, input_ref['seals']):
        expected = dict(bind_seal_metadata(inputs, group['id']), evidence_class='original_prospective_input')
        exact(audit, 'input_reference.' + group['id'], ref, expected)
    for unit, ref in zip(all_units, composite['seals']):
        is_new = unit['arm'] == 'conformance'
        stage = amended_public if is_new else original_public
        cls = 'post_exposure_amended_inherited_conformance' if is_new else 'original_prospective_unchanged_public_record'
        expected = dict(bind_seal_metadata(stage, unit['id']), evidence_class=cls)
        exact(audit, 'composite_reference.' + unit['id'], ref, expected)
    for stage in (inputs, amended_public, original_public, evaluation, analysis):
        physical_seals = list((stage.final / 'stages' / stage.name / 'units').glob('*/attempt_*/seal.json'))
        exact(audit, str(stage.final.relative_to(repo)) + '.' + stage.name + '.physical_seal_count',
              len(physical_seals), len(stage.seals))
    for identifier in evaluation.expected:
        bind_seal_metadata(evaluation, identifier)
    bind_seal_metadata(analysis, 'all-frozen-endpoints')
    audit.require(not (old / 'stages/public/complete.json').exists(), 'Original completion was created during observation')
    return {'inputs': inputs, 'public': CompositePublic(original_public, amended_public),
            'evaluation': evaluation, 'analysis': analysis}, (old, new), manifest_hash


def a1_unknown_public(audit, roots):
    unknown = []
    for root in roots:
        for unit_dir in sorted((root / 'stages/public/units').iterdir()):
            if unit_dir.is_dir():
                for attempt in sorted(unit_dir.glob('attempt_*')):
                    if not (attempt / 'seal.json').is_file():
                        if (attempt / 'start.json').is_file():
                            bound_file(audit, attempt / 'start.json')
                        unknown.append({'origin_root': root.relative_to(audit.repo).as_posix(),
                                        'unit_id': unit_dir.name, 'attempt_directory': attempt.name})
    audit.require(any(row['origin_root'] == 'v3/experiments/final_v1' and
                      row['unit_id'] == 'conformance_structural_legacy__counterpossible_tied_minima__candidate'
                      and row['attempt_directory'] == 'attempt_01' for row in unknown),
                  'The original failed-prefix cost must remain unknown')
    return unknown


def formula_key(query):
    return [query['semantics_version'], query['source_version'], query['variables'], query['clauses']]


def scalar_truth(query):
    '''Boolean tuples and direct signed-literal interpretation; no solver import.'''
    for assignment in itertools.product((False, True), repeat=query['variables']):
        if all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in query['clauses']):
            return 1
    return 0


def weighted(rows, value):
    '''Explicit prospective unit weights: 1 / (#populations * slots in population).'''
    counts = Counter(row['unit']['group_id'] for row in rows)
    total = Fraction(0)
    for row in rows:
        number = frac(value(row))
        if number is None:
            return None
        total += number / (len(counts) * counts[row['unit']['group_id']])
    return total if rows else None


def invoice(audit, label, value):
    total = value['total']
    audit.require(type(total) is int and total >= 0, 'Malformed total invoice')
    operations = [row['units'] for row in value['operations']]
    audit.require(all(type(n) is int and n >= 0 for n in operations), 'Malformed invoice operation')
    audit.check(label + '.categories', sum(value['by_category'].values()), total)
    audit.check(label + '.operations', sum(operations), total)
    return total


def metrics(trace, truths, positions, fp, fn, bits, start, stop):
    chosen = [row for row in trace if row['index'] in set(positions)]
    planned, closed = len(positions), len(chosen)
    full = planned > 0 and closed == planned
    advice = all(len(row['advice']) == 6 for row in chosen)
    f_live = sum(((frac(row['emitted_q']) - truths[row['index']]) ** 2 for row in chosen), Fraction())
    f_base = sum(((frac(row['base_q']) - truths[row['index']]) ** 2 for row in chosen), Fraction())
    positives = sum(row['terminal_action'] == 1 and truths[row['index']] == 0 for row in chosen)
    negatives = sum(row['terminal_action'] == 0 and truths[row['index']] == 1 for row in chosen)
    action = fp * positives + fn * negatives
    readout = None
    equal = Fraction()
    if advice:
        equal = sum(((Fraction(sum(row['advice']), 6) - truths[row['index']]) ** 2 for row in chosen), Fraction())
        if full:
            readout = {
                'constant_half_brier_mean': [1, 4],
                'equal_mixture_brier_mean': pair(equal / planned),
                'dyadic_equal_mixture_brier_mean': pair(sum(((Fraction((sum(row['advice']) * (2 ** bits)) // 6, 2 ** bits) - truths[row['index']]) ** 2 for row in chosen), Fraction()) / planned),
                'same_hard_mask_half_brier_mean': pair(Fraction(sum(row['hard_before'] != 'checked' for row in chosen), 4 * planned)),
                'same_hard_mask_equal_mixture_brier_mean': pair(sum(((Fraction(sum(row['advice']), 6) - truths[row['index']]) ** 2 for row in chosen if row['hard_before'] != 'checked'), Fraction()) / planned),
                'expert_brier_means': [pair(Fraction(sum((row['advice'][j] - truths[row['index']]) ** 2 for row in chosen), planned)) for j in range(6)]}
    return {'start': start, 'stop': stop, 'horizon': planned, 'rounds_closed': closed,
            'full_horizon': full, 'brier_mean': pair(f_live / planned) if full else None,
            'base_brier_mean': pair(f_base / planned) if full else None,
            'uniform_brier_mean': pair(equal / planned) if full and advice else None,
            'action_loss_mean': pair(action / (max(fp, fn) * planned)) if full else None,
            'task_max_loss': pair(max(fp, fn)), 'weighted_action_loss_sum': pair(action),
            'issued_brier_sum': pair(f_live), 'base_issued_brier_sum': pair(f_base),
            'terminal_errors': positives + negatives, 'false_positives': positives, 'false_negatives': negatives,
            'closed_prefix_only_if_incomplete': {'brier_mean': pair(f_live / closed) if closed else None,
                'action_loss_mean': pair(action / (max(fp, fn) * closed)) if closed else None},
            'forecast_readouts': readout}


def report_numbers(optional, horizon):
    result = {'status': 'not_requested', 'horizon': horizon, 'additional_units': 0, 'endpoints': {}}
    if optional is None:
        return result
    report = optional['report']
    result.update(status=report['status'], report_status=report['status'], additional_units=optional['additional_units'])
    if report['status'] != 'success':
        return result
    for name in ('V', 'F', 'Z'):
        interval = report['intervals'][name]
        lo, hi = frac(interval['lower']), frac(interval['upper'])
        dlo, dhi = map(frac, report['deterministic_envelopes'][name])
        width, base = hi - lo, dhi - dlo
        conflict = bool(interval.get('confidence_conflict', False)) or width < 0
        result['endpoints'][name] = {
            'status': 'confidence_conflict' if conflict else 'success', 'confidence_conflict': conflict,
            'lower': interval['lower'], 'upper': interval['upper'],
            'width': None if conflict else pair(width), 'width_per_horizon': None if conflict else pair(width / horizon),
            'delivered_signed_span': pair(width),
            'deterministic_lower': report['deterministic_envelopes'][name][0],
            'deterministic_upper': report['deterministic_envelopes'][name][1],
            'deterministic_width': pair(base), 'deterministic_width_per_horizon': pair(base / horizon),
            'normalized_width_reduction': None if conflict else pair((base - width) / horizon),
            'lower_endpoint_gain': pair(lo - dlo), 'upper_endpoint_gain': pair(dhi - hi),
            'normalized_lower_endpoint_gain': pair((lo - dlo) / horizon),
            'normalized_upper_endpoint_gain': pair((dhi - hi) / horizon),
            'practical_width_reduction': bool(not conflict and (base - width) / horizon >= Fraction(1, 100)),
            'practical_lower_endpoint_gain': bool(not conflict and (lo - dlo) / horizon >= Fraction(1, 100)),
            'practical_upper_endpoint_gain': bool(not conflict and (dhi - hi) / horizon >= Fraction(1, 100))}
    if any(item['confidence_conflict'] for item in result['endpoints'].values()):
        result['status'] = 'confidence_conflict'
    return result


def episode_numbers(audit, unit, public, truth, paid, score, arm_config):
    label = unit['id']
    audit.check(label + '.paid_binding', paid, {'unit': unit, 'public_input_sha256': digest(public), 'policy_truth_access': False})
    ep, queries = paid['episode'], public['queries']
    trace, horizon = ep['trace'], len(queries)
    audit.check(label + '.trace_indices', [row['index'] for row in trace], list(range(len(trace))))
    audit.check(label + '.closed_count', ep['rounds_closed'], len(trace))
    audit.require(len(trace) <= horizon, 'Transcript exceeds planned horizon')
    valid, bought, prior_labels = True, {}, {}
    query_map = {q['query_id']: (q, y) for q, y in zip(queries, truth)}
    cached_provider = unit['engine'] in ('broker', 'mirror') and unit['parameters']['provider'] != 'cold'
    provider = 'owned_cached_cnf_receipt' if cached_provider else 'bounded_cnf_checked'
    version = 'p308-selected-receipt-cache-v1.1' if cached_provider else 'p308-bounded-cnf-services-v1.1'
    for receipt in ep['invoices']:
        known_query = query_map.get(receipt.get('query_id'))
        if known_query is None:
            valid = False
            continue
        q, y = known_query
        sound_binding = receipt.get('claim_key') == formula_key(q) and receipt.get('provider') == provider and receipt.get('provider_version') == version
        valid = valid and sound_binding
        if receipt.get('status') == 'success':
            sound_answer = receipt.get('checked') is True and type(receipt.get('answer')) is int and receipt['answer'] == y
            valid = valid and sound_answer
            if sound_answer and sound_binding:
                bought[q['query_id']] = y
        else:
            valid = valid and receipt.get('answer') is None and receipt.get('checked') is False
    for row, q, y in zip(trace, queries, truth):
        key = wire(formula_key(q))
        valid = valid and row.get('query_id') == q['query_id'] and row.get('claim_key') == formula_key(q)
        valid = valid and all(0 <= frac(row[field]) <= 1 for field in ('base_q', 'emitted_q'))
        valid = valid and type(row.get('terminal_action')) is int and row['terminal_action'] in (0, 1)
        valid = valid and len(row['advice']) in (0, 6) and all(type(x) is int and x in (0, 1) for x in row['advice'])
        if row.get('hard_before') == 'checked':
            valid = valid and prior_labels.get(key) == y and frac(row['emitted_q']) == y
        if row.get('purchased_label') is not None:
            valid = valid and type(row['purchased_label']) is int and row['purchased_label'] == y and bought.get(q['query_id']) == y
            prior_labels[key] = row['purchased_label']
        after = row.get('hard_after')
        valid = valid and type(after) is dict
        if type(after) is dict and after.get('status') == 'checked':
            valid = valid and type(after.get('answer')) is int and after['answer'] == y and after.get('interval') == [y, y] and prior_labels.get(key) == y
    audit.check(label + '.validity', score['validity_pass'], bool(valid))
    audit.require(valid, 'Independent public semantic audit failed; retained observer failure requires inspection: ' + label)
    fp, fn = frac(unit['stakes']['fp']), frac(unit['stakes']['fn'])
    record = metrics(trace, truth, list(range(horizon)), fp, fn, arm_config['action_bits'], 0, horizon)
    full = record['full_horizon'] and ep['status'] == 'success'
    if not full:
        for field in ('brier_mean', 'base_brier_mean', 'uniform_brier_mean', 'action_loss_mean'):
            record[field] = None
    record.update(full_horizon=full, validity_pass=bool(valid))
    source = invoice(audit, label + '.source', paid['common_source_invoice'])
    local = invoice(audit, label + '.local', ep['meter'])
    optional = paid.get('optional_reporting')
    additional = 0
    if optional is not None:
        additional = invoice(audit, label + '.report_source', optional['source_invoice']) + invoice(audit, label + '.report_execution', optional['report']['meter'])
        audit.check(label + '.additional_report_bill', optional['additional_units'], additional)
        if optional['report']['status'] == 'success':
            audit.check(label + '.report_basis', optional['report'], {'reference_basis': arm_config['report_basis'], 'radius_rule': arm_config['report_radius']})
            # Reconstruct the observable envelopes directly from issued public
            # forecasts and chronologically available labels. Unknown labels
            # range over 0 and 1; no private truth is needed for these bounds.
            v_lower = v_upper = f_lower = f_upper = Fraction(0)
            n_live = 0
            for row in trace:
                q = frac(row['emitted_q'])
                hard = row['hard_before'] == 'checked'
                selected = row['selected']
                audit.require(type(selected) is bool, 'Report selection flag is not Boolean')
                if not hard and not selected:
                    n_live += 1
                    v_lower += min(q, 1 - q)
                    v_upper += max(q, 1 - q)
                if hard:
                    loss_options = [Fraction(0)]
                elif selected:
                    loss_options = [(q - row['purchased_label']) ** 2]
                else:
                    loss_options = [q ** 2, (1 - q) ** 2]
                f_lower += min(loss_options)
                f_upper += max(loss_options)
            rebuilt = {'V': [pair(v_lower), pair(v_upper)], 'F': [pair(f_lower), pair(f_upper)],
                       'Z': [[0, 1], [n_live, 1]]}
            reduced_report = {key: [pair(endpoint) for endpoint in endpoints]
                              for key, endpoints in optional['report']['deterministic_envelopes'].items()}
            audit.check(label + '.observable_report_envelopes', reduced_report, rebuilt)
            audit.check(label + '.observable_report_denominators', optional['report'],
                        {'n_live': n_live, 'rows_read': horizon,
                         'purchased_labels_read': sum(row['selected'] for row in trace),
                         'exact_all_remaining_known': n_live == 0})
    record.update(cold_units=source + local, source_units=source, local_units=local,
                  optional_reporting_units=additional,
                  paid_report_comparison=report_numbers(optional, horizon))
    raw_price = frac(unit['parameters'].get('unit_price', '0')) if unit['engine'] == 'ordinary' else None
    record['native_price_normalized'] = pair(raw_price / max(fp, fn)) if raw_price is not None else None
    record['native_price_raw'] = pair(raw_price)
    record['native_normalized_objective_mean'] = pair((frac(record['weighted_action_loss_sum']) + raw_price * (source + local)) / (horizon * max(fp, fn))) if full and raw_price is not None else None
    fields = ('index', 'query_id', 'claim_key', 'advice', 'base_q', 'base_action', 'base_terminal', 'selected', 'propensity', 'purchased_label')
    common = {key: ep.get(key) for key in ('blocks', 'weights', 'random_bits_consumed', 'randomness')}
    record['base_path_sha256'] = digest(dict(common, trace=[{key: row[key] for key in fields} for row in trace]))
    record['delivered_path_sha256'] = digest(dict(common, trace=trace))
    record['action_path_sha256'] = digest([{key: row[key] for key in ('index', 'query_id', 'emitted_q', 'prospective_action', 'terminal_action')} for row in trace])
    seen, first = set(), []
    for index, query in enumerate(queries):
        key = wire(formula_key(query))
        if key not in seen:
            first.append(index)
            seen.add(key)
    record['first_occurrence'] = dict(metrics(trace, truth, first, fp, fn, arm_config['action_bits'], 0, horizon), indices=first, parent_full_horizon=full)
    record['segments'] = {segment['name']: metrics(trace, truth, list(range(segment['start'], segment['stop'])), fp, fn, arm_config['action_bits'], segment['start'], segment['stop']) for segment in unit['segments']}
    record['private_truth_unique_programs'] = len(seen)
    audit.check(label + '.score', score, record)
    return {'unit': unit, 'score': record}


def summarize(audit, units, analyses, config, group_map):
    thresholds = config['analysis']
    buckets = defaultdict(list)
    for row in units:
        u = row['unit']
        buckets[(group_map[u['group_id']]['recipe']['family'], wire(u['stakes']), u['configuration_id'])].append(row)
    actual = {(row['family'], wire(row['stakes']), row['configuration_id']): row for row in analyses['configuration_means']}
    audit.check('configuration_summary_keys', sorted([list(key) for key in actual]), sorted([list(key) for key in buckets]))
    output = []
    for key, rows in sorted(buckets.items()):
        family, stakes_key, name = key
        u = rows[0]['unit']
        complete = all(row['score']['full_horizon'] and row['score']['validity_pass'] for row in rows)
        means = {field: pair(weighted(rows, lambda row: row['score'][field])) for field in ('brier_mean', 'action_loss_mean', 'base_brier_mean', 'uniform_brier_mean', 'cold_units', 'local_units', 'optional_reporting_units')}
        learned = None if means['uniform_brier_mean'] is None else frac(means['uniform_brier_mean']) - frac(means['base_brier_mean'])
        item = {'family': family, 'stakes': json.loads(stakes_key), 'configuration_id': name,
                'method': u['method'], 'method_kind': u['method_kind'], 'engine': u['engine'],
                'group_ids': sorted({row['unit']['group_id'] for row in rows}),
                'planned_executions': len(rows), 'scored_executions': len(rows),
                'complete_episodes': sum(row['score']['full_horizon'] for row in rows),
                'complete_primary_denominator': complete,
                'executed_policy_seed_slots': [row['unit']['seed'] for row in rows],
                'known_total_executed_cold_units': sum(row['score']['cold_units'] for row in rows),
                'unknown_cost_episodes': 0, 'missing_or_incomplete_unit_ids': [row['unit']['id'] for row in rows if not row['score']['full_horizon'] or not row['score']['validity_pass']],
                'means': means, 'mean_cold_units_per_request': pair(weighted(rows, lambda row: Fraction(row['score']['cold_units'], row['score']['horizon']))),
                'native_price_normalized': rows[0]['score']['native_price_normalized'],
                'uniform_minus_base_brier': pair(learned),
                'practical_learning_effect': bool(complete and learned is not None and learned >= frac(thresholds['loss_improvement_threshold']))}
        observed = actual[key]
        audit.check('configuration.' + family + '.' + name, observed, item)
        slice_names = sorted({'first_occurrence'} | {segment['name'] for segment in u['segments']})
        observed_slices = {entry['slice']: entry for entry in observed['prespecified_slices']}
        slices = []
        for slice_name in slice_names:
            adapted = []
            for row in rows:
                parent = row['score']
                values = parent['first_occurrence'] if slice_name == 'first_occurrence' else parent['segments'][slice_name]
                usable = parent['full_horizon'] and parent['validity_pass'] and values['full_horizon']
                adapted.append({'unit': row['unit'], 'values': values, 'usable': usable,
                    'denominator': {'unit_id': row['unit']['id'], 'scheduled_positions': values['horizon'], 'closed_positions': values['rounds_closed'],
                                    'parent_complete_and_valid': parent['full_horizon'] and parent['validity_pass'], 'usable_full_slice': usable}})
            sm = {field: pair(weighted(adapted, lambda row: row['values'][field] if row['usable'] else None)) for field in ('brier_mean', 'base_brier_mean', 'uniform_brier_mean', 'action_loss_mean')}
            rm = {field: pair(weighted(adapted, lambda row: (row['values'].get('forecast_readouts') or {}).get(field) if row['usable'] else None)) for field in ('constant_half_brier_mean', 'equal_mixture_brier_mean', 'dyadic_equal_mixture_brier_mean', 'same_hard_mask_half_brier_mean', 'same_hard_mask_equal_mixture_brier_mean')}
            rm['expert_brier_means'] = [pair(weighted(adapted, lambda row: (row['values'].get('forecast_readouts') or {}).get('expert_brier_means', [None] * 6)[j] if row['usable'] else None)) for j in range(6)]
            delta = None if sm['uniform_brier_mean'] is None else frac(sm['uniform_brier_mean']) - frac(sm['base_brier_mean'])
            full = all(row['usable'] for row in adapted)
            si = {'slice': slice_name, 'planned_episodes': len(rows), 'complete_primary_denominator': full,
                  'per_episode_denominators': [row['denominator'] for row in adapted],
                  'known_scheduled_positions': sum(row['values']['horizon'] for row in adapted),
                  'unknown_scheduled_denominator_episodes': 0, 'means': sm, 'forecast_readout_means': rm,
                  'uniform_minus_base_brier': pair(delta),
                  'practical_learning_effect': bool(full and delta is not None and delta >= frac(thresholds['loss_improvement_threshold']))}
            audit.check('slice.' + family + '.' + name + '.' + slice_name, observed_slices[slice_name], si)
            slices.append(si)
        item['prespecified_slices'] = slices
        requested = u['engine'] in ('broker', 'mirror')
        report_summary = {'requested': requested, 'planned_reports': len(rows) if requested else 0, 'endpoints': {}}
        if requested:
            report_summary.update(mean_additional_units=pair(weighted(rows, lambda row: row['score']['optional_reporting_units'])),
                known_total_additional_units=sum(row['score']['optional_reporting_units'] for row in rows), unknown_fee_reports=0)
            report_summary['status_by_unit'] = [{'unit_id': row['unit']['id'], 'status': row['score']['paid_report_comparison']['status'],
                'parent_valid_and_complete': row['score']['validity_pass'] and row['score']['full_horizon']} for row in rows]
            for endpoint in ('V', 'F', 'Z'):
                def usable(row):
                    s = row['score']
                    p = s['paid_report_comparison']
                    return s['validity_pass'] and s['full_horizon'] and p['status'] == 'success' and p['endpoints'].get(endpoint, {}).get('status') == 'success'
                numbers = {field: pair(weighted(rows, lambda row: row['score']['paid_report_comparison']['endpoints'][endpoint][field] if usable(row) else None)) for field in ('deterministic_width_per_horizon', 'width_per_horizon', 'normalized_width_reduction', 'normalized_lower_endpoint_gain', 'normalized_upper_endpoint_gain')}
                finished = all(usable(row) for row in rows)
                reduction = frac(numbers['normalized_width_reduction'])
                report_summary['endpoints'][endpoint] = {'complete_report_denominator': finished, 'means': numbers,
                    'usable_reports': sum(usable(row) for row in rows), 'unavailable_unit_ids': [row['unit']['id'] for row in rows if not usable(row)],
                    'practical_width_reduction': bool(finished and reduction is not None and reduction >= frac(thresholds['report_width_improvement_threshold']))}
        audit.check('report_summary.' + family + '.' + name, observed['paid_reporting'], report_summary)
        item['paid_reporting'] = report_summary
        output.append(item)
    return output


def common_action(score, stakes):
    if not score['validity_pass'] or not score['full_horizon']:
        return None
    fp, fn = frac(stakes['fp']), frac(stakes['fn'])
    return (fp * score['false_positives'] + fn * score['false_negatives']) / (max(fp, fn) * score['horizon'])


def paired_effects(audit, rows, analysis, config, groups, cost_known):
    by_id = {row['unit']['id']: row for row in rows}
    observed = {(r['unit_id'], r['relation']): r for r in analysis['paired_records']}
    records, buckets = [], defaultdict(list)
    for row in rows:
        u, current = row['unit'], row['score']
        for relation in ('base_id', 'cold_id', 'identity_of', 'stakes_reference'):
            target_id = u.get('pairing', {}).get(relation)
            if target_id is None:
                continue
            target = by_id[target_id]['score']
            current_w, target_w = common_action(current, u['stakes']), common_action(target, u['stakes'])
            price = frac(current['native_price_normalized']) or Fraction(0)
            deltas = {field + '_target_minus_current': pair(frac(target[field]) - frac(current[field])) if target[field] is not None and current[field] is not None else None for field in ('brier_mean', 'action_loss_mean', 'cold_units', 'local_units', 'optional_reporting_units')}
            delta_w = None if current_w is None or target_w is None else target_w - current_w
            delta_j = None if delta_w is None else delta_w + price * Fraction(target['cold_units'] - current['cold_units'], current['horizon'])
            deltas.update(action_loss_mean_target_minus_current=pair(delta_w), common_native_objective_target_minus_current=pair(delta_j))
            same = {key: current[key] == target[key] for key in ('base_path_sha256', 'delivered_path_sha256', 'action_path_sha256')}
            required = ['base_path_sha256'] if relation == 'base_id' else list(same) if relation in ('cold_id', 'identity_of') else []
            complete = current['validity_pass'] and target['validity_pass'] and current['full_horizon'] and target['full_horizon']
            coupling = all(same[key] for key in required) if complete and required else None
            if relation == 'base_id' and coupling:
                coupling = frac(current['brier_mean']) <= frac(target['brier_mean']) and current_w <= target_w
            equal = complete and same['delivered_path_sha256'] and same['action_path_sha256'] and deltas['brier_mean_target_minus_current'] == [0, 1] and delta_w == 0
            ratio = Fraction(current['cold_units'], target['cold_units']) if complete and target['cold_units'] > 0 else None
            saving = bool(equal and ratio is not None and ratio <= frac(config['analysis']['saving_ratio_threshold']))
            item = {'unit_id': u['id'], 'relation': relation, 'target_id': target_id, 'differences': deltas,
                    'path_equalities': same, 'ordinary_identity_pass': bool(complete and coupling and all(value == [0, 1] for value in deltas.values())) if relation == 'identity_of' else None,
                    'coupling_pass': coupling, 'required_path_equalities': required, 'complete_pair': complete,
                    'equal_delivered_output': equal, 'common_stakes': u['stakes'], 'common_normalized_price': pair(price),
                    'current_action_loss_under_common_stakes': pair(current_w), 'target_action_loss_under_common_stakes': pair(target_w),
                    'cold_cost_ratio_current_to_target': pair(ratio), 'completed_path_equal_output_cost_threshold_met': saving,
                    'practical_equal_output_cost_saving': saving and cost_known}
            audit.check('pair.' + u['id'] + '.' + relation, observed[(u['id'], relation)], item)
            records.append(item)
            key = (groups[u['group_id']]['recipe']['family'], u['configuration_id'], relation)
            buckets[key].append({'unit': u, 'record': item, 'current': current['cold_units'], 'target': target['cold_units']})
    audit.check('pair_count', len(analysis['paired_records']), len(records))
    aggregate_observed = {(r['family'], r['configuration_id'], r['relation']): r for r in analysis['paired_configuration_effects']}
    aggregates = []
    for key, bucket in sorted(buckets.items()):
        family, name, relation = key
        dw = weighted(bucket, lambda row: row['record']['differences']['action_loss_mean_target_minus_current'])
        dj = weighted(bucket, lambda row: row['record']['differences']['common_native_objective_target_minus_current'])
        denominator = weighted(bucket, lambda row: row['target'])
        ratio = weighted(bucket, lambda row: row['current']) / denominator if denominator is not None and denominator > 0 else None
        complete = all(row['record']['complete_pair'] for row in bucket)
        equal = complete and all(row['record']['equal_delivered_output'] for row in bucket)
        saving = bool(equal and ratio is not None and ratio <= frac(config['analysis']['saving_ratio_threshold']))
        priced = bool(complete and dj is not None and dj >= frac(config['analysis']['loss_improvement_threshold']))
        price = frac(bucket[0]['record']['common_normalized_price'])
        item = {'family': family, 'configuration_id': name, 'relation': relation, 'paired_executions': len(bucket),
            'complete_denominator': complete, 'common_stakes': bucket[0]['record']['common_stakes'],
            'common_normalized_price': pair(price), 'mean_action_improvement': pair(dw), 'mean_common_objective_improvement': pair(dj),
            'practical_action_effect': bool(complete and dw is not None and dw >= frac(config['analysis']['loss_improvement_threshold'])),
            'completed_path_priced_threshold_met': priced, 'practical_priced_effect': priced and (price == 0 or cost_known),
            'every_pair_equal_delivered_output': equal, 'mean_cold_cost_ratio': pair(ratio),
            'completed_path_equal_output_cost_threshold_met': saving, 'practical_equal_output_cost_saving': saving and cost_known}
        audit.check('paired_aggregate.' + '.'.join(key), aggregate_observed[key], item)
        aggregates.append(item)
    audit.check('paired_aggregate_count', len(analysis['paired_configuration_effects']), len(aggregates))
    return records, aggregates


def catalogue_minima(audit, summaries, analysis, config, cost_known):
    cells = defaultdict(list)
    for row in summaries:
        cells[(row['family'], wire(row['stakes']), tuple(row['group_ids']))].append(row)
    actual = {(r['family'], wire(r['stakes']), tuple(r['group_ids']), tuple(r['price_normalized_per_unit']), r['selection']): r for r in analysis['catalogue_comparisons']}
    output = []
    for (family, stakes, group_ids), cell in sorted(cells.items()):
        prices = {frac(p) for p in config['analysis']['repricing_grid']}
        prices.update(frac(row['native_price_normalized']) for row in cell if row['native_price_normalized'] is not None)
        for price in sorted(prices):
            for selection in ('fixed_record_repricing', 'native_price_catalogue'):
                eligible = [row for row in cell if selection != 'native_price_catalogue' or not row['method'].startswith('ordinary_combo') or frac(row['native_price_normalized']) == price]
                objectives = {row['configuration_id']: frac(row['means']['action_loss_mean']) + price * frac(row['mean_cold_units_per_request']) for row in eligible if row['complete_primary_denominator'] and row['means']['action_loss_mean'] is not None and row['mean_cold_units_per_request'] is not None and not row['unknown_cost_episodes']}
                def minimum(kinds):
                    ids = [row['configuration_id'] for row in eligible if row['method_kind'] in kinds]
                    complete = bool(ids) and all(name in objectives for name in ids)
                    best = min(objectives[name] for name in ids) if complete else None
                    return {'complete_catalogue': complete, 'value': pair(best), 'ties': sorted(name for name in ids if complete and objectives[name] == best)}
                distinct = minimum(('ordinary',))
                mirrors = minimum(('ordinary', 'mirror'))
                aliases = minimum(('ordinary', 'mirror', 'candidate'))
                key = (family, stakes, group_ids, tuple(pair(price)), selection)
                observed = actual[key]
                item = {'family': family, 'stakes': json.loads(stakes), 'group_ids': list(group_ids),
                    'price_normalized_per_unit': pair(price), 'selection': selection,
                    'whole_configuration_objectives': {name: pair(value) for name, value in sorted(objectives.items())},
                    'distinct_ordinary_minimum': distinct, 'ordinary_including_mirror_minimum': mirrors,
                    'ordinary_including_identical_kernel_aliases': aliases, 'candidate_comparisons': []}
                for name in ('distinct_ordinary_minimum', 'ordinary_including_mirror_minimum', 'ordinary_including_identical_kernel_aliases'):
                    normalized = dict(observed[name], ties=sorted(observed[name]['ties']))
                    audit.check('catalogue.' + repr(key) + '.' + name, normalized, item[name])
                audit.check('catalogue_objectives.' + repr(key), observed['whole_configuration_objectives'], item['whole_configuration_objectives'])
                audit.check('catalogue_objective_ids.' + repr(key), sorted(observed['whole_configuration_objectives']), sorted(objectives))
                for row in eligible:
                    if row['method_kind'] != 'candidate':
                        continue
                    objective = objectives.get(row['configuration_id'])
                    gain = None if objective is None or distinct['value'] is None else frac(distinct['value']) - objective
                    effect = bool(gain is not None and gain >= frac(config['analysis']['loss_improvement_threshold']))
                    candidate = {'configuration_id': row['configuration_id'], 'objective': pair(objective),
                        'distinct_ordinary_minus_candidate': pair(gain), 'completed_path_practical_effect': effect,
                        'practical_effect': effect and (price == 0 or cost_known), 'ordinary_identical_configuration_objective': pair(objective)}
                    saved = next(v for v in observed['candidate_comparisons'] if v['configuration_id'] == row['configuration_id'])
                    audit.check('catalogue_candidate.' + repr(key) + '.' + row['configuration_id'], saved, candidate)
                    if objective is not None and aliases['value'] is not None:
                        audit.check('ordinary_alias_bound.' + repr(key) + '.' + row['configuration_id'], frac(aliases['value']) <= objective, True)
                    item['candidate_comparisons'].append(candidate)
                audit.check('catalogue_candidate_count.' + repr(key), len(observed['candidate_comparisons']), len(item['candidate_comparisons']))
                output.append(item)
    audit.check('catalogue_cell_count', len(actual), len(output))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--release-receipt', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    repo, out = Path(args.repo).resolve(), Path(args.out).resolve()
    owned = repo / 'v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction'
    if not out.is_relative_to(owned) or out == owned:
        raise ValueError('Observer output must be a new attempt beneath its assigned review directory')
    release_path = Path(args.release_receipt).resolve()
    if not release_path.is_relative_to(owned):
        raise ValueError('Release receipt must be within the assigned review directory')
    release = decode(release_path.read_bytes())
    if (release.get('task') != 'P3-10' or release.get('all_public_evaluation_analysis_complete') is not True
            or release.get('amendment_id') != A1_ID or release.get('amendment_manifest_sha256') != A1_MANIFEST_SHA256):
        raise PermissionError('Explicit principal A1 completion release with exact sealed manifest required before final reads')
    out.mkdir(parents=True, exist_ok=False)
    started = utc()
    write_new(out / 'started.json', {'started_utc': started, 'contributor': 'ChatGPT (GPT-6 Astra Pro)',
        'agent': '/root/freeze_review', 'scope': 'P3-10 broker independent JSON observation', 'release': release,
        'observer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'argv': sys.argv,
        'principal_research_minutes_claimed': 0})
    audit = Audit(repo, out)
    try:
        audit.load(release_path)
        config = audit.load(repo / 'v3/experiments/protocol.v1.json')
        freeze = audit.load(repo / 'v3/experiments/frozen_v1/manifest.json')
        schedule = audit.load(repo / 'v3/experiments/frozen_v1/schedule.json')
        audit.check('frozen_protocol_hash', audit.files['v3/experiments/protocol.v1.json']['sha256'], freeze['protocol_sha256'])
        audit.check('frozen_schedule_hash', audit.files['v3/experiments/frozen_v1/schedule.json']['sha256'], freeze['schedule_sha256'])
        binding = {'freeze_id': freeze['freeze_id'], 'manifest_sha256': audit.files['v3/experiments/frozen_v1/manifest.json']['sha256'], 'protocol_sha256': freeze['protocol_sha256']}
        all_units, groups = schedule['units'], schedule['groups']
        unit_schedule = [u for u in all_units if u['arm'] == 'broker']
        group_map = {group['id']: group for group in groups}
        stages, lineage_roots, amendment_hash = a1_stages(audit, repo, release, freeze, schedule, binding)
        final_analysis, analysis_hash = stages['analysis'].get('all-frozen-endpoints')
        audit.check('analysis_denominator', final_analysis, {'expected_score_units': 500, 'received_score_units': 500})
        audit.check('broker_unit_count', len(unit_schedule), 336)
        inputs, truths, memo = {}, {}, {}
        for group in groups:
            if group['arm'] != 'broker':
                continue
            data, bound_hash = stages['inputs'].get(group['id'])
            inputs[group['id']] = (data, bound_hash)
            labels = []
            for query in data['queries']:
                key = wire(formula_key(query))
                if key not in memo:
                    memo[key] = scalar_truth(query)
                labels.append(memo[key])
            truths[group['id']] = labels
        rows = []
        for index, unit in enumerate(unit_schedule, 1):
            public, input_hash = inputs[unit['group_id']]
            paid_wrapper, public_hash = stages['public'].get(unit['id'])
            score_wrapper, _ = stages['evaluation'].get('score-' + unit['id'])
            audit.check(unit['id'] + '.public_input_hash', paid_wrapper['input_result_sha256'], input_hash)
            audit.check(unit['id'] + '.score_hash_bindings', score_wrapper,
                {'input_result_sha256': input_hash, 'public_result_sha256': public_hash})
            rows.append(episode_numbers(audit, unit, public, truths[unit['group_id']], paid_wrapper['paid_result'], score_wrapper['score'], config['arms']['broker']))
            if index % 50 == 0:
                print(json.dumps({'completed_broker_observations': index, 'mismatches': len(audit.mismatches)}), flush=True)
        unknown_public = a1_unknown_public(audit, lineage_roots)
        cost_known = not unknown_public
        audit.check('complete_outer_paid_attempt_accounting', final_analysis['execution_attempt_audit']['complete_outer_paid_attempt_accounting'], cost_known)
        audit.check('complete_outer_attempt_economic_claim_permitted', final_analysis['complete_outer_attempt_economic_claim_permitted'], False)
        audit.check('amended_audit_fields', final_analysis['execution_attempt_audit'],
                    {'amendment_id': A1_ID, 'complete_outer_paid_attempt_accounting': False,
                     'complete_physical_run_accounting': False, 'original_public_stage_complete': False})
        observed_unknown = [{key: row[key] for key in ('origin_root', 'unit_id', 'attempt_directory')}
                            for row in final_analysis['execution_attempt_audit']['unknown_unsealed_public_attempts']]
        audit.check('unknown_outer_public_attempts', observed_unknown, unknown_public)
        broker = final_analysis['broker']
        summaries = summarize(audit, rows, broker, config, group_map)
        pairs, pair_means = paired_effects(audit, rows, broker, config, group_map, cost_known)
        minima = catalogue_minima(audit, summaries, broker, config, cost_known)
        violations = [row['unit_id'] for row in pairs if row['coupling_pass'] is False or row['ordinary_identity_pass'] is False]
        identities = [row['unit_id'] for row in pairs if row['ordinary_identity_pass'] is False]
        unavailable = [row['unit_id'] for row in pairs if row['required_path_equalities'] and row['coupling_pass'] is None]
        for name, expected in [('coupling_violations', violations), ('ordinary_identity_violations', identities), ('coupling_unavailable_pairs', unavailable)]:
            audit.check(name, broker[name], expected)
        details = {'configuration_means': summaries, 'paired_records': pairs,
            'paired_configuration_effects': pair_means, 'catalogue_comparisons': minima,
            'independent_per_unit_metrics': rows, 'truth_by_group': truths}
        write_new(out / 'reconstructed.json', details)
        summary = {'status': 'PASS' if not audit.mismatches else 'FAIL', 'contributor': 'ChatGPT (GPT-6 Astra Pro)',
            'reviewer_agent': '/root/freeze_review', 'started_utc': started, 'finished_utc': utc(),
            'numeric_and_binding_comparisons': audit.comparisons, 'mismatch_count': len(audit.mismatches),
            'broker_episodes': len(rows), 'complete_broker_episodes': sum(row['score']['full_horizon'] for row in rows),
            'broker_query_positions': sum(row['score']['horizon'] for row in rows),
            'independent_unique_cnf_truths': len(memo), 'configuration_summaries': len(summaries),
            'pair_records': len(pairs), 'paired_configuration_effects': len(pair_means),
            'catalogue_cells': len(minima), 'optional_reports': sum(row['unit']['engine'] in ('broker', 'mirror') for row in rows),
            'optional_report_statuses': dict(Counter(row['score']['paid_report_comparison']['status'] for row in rows if row['unit']['engine'] in ('broker', 'mirror'))),
            'coupling_violations': violations, 'ordinary_identity_violations': identities,
            'coupling_unavailable_pairs': unavailable, 'unknown_public_attempts': unknown_public,
            'analysis_result_sha256': analysis_hash, 'amendment_id': A1_ID,
            'amendment_manifest_sha256': amendment_hash, 'original_public_stage_complete': False,
            'frozen_imports': [], 'paid_method_replays': 0,
            'principal_research_minutes_claimed': 0,
            'scope': 'Independent saved-JSON broker reconstruction across explicit A1 lineage: unchanged original broker public records, original inputs, amended private scores/analysis, all 500 composite seals, and preserved unknown original public prefix. Arithmetic endpoints are unchanged from the v3 observer; mixture weight/selector numerical implementation is reviewed separately by the principal.'}
        write_new(out / 'summary.json', summary)
        write_new(out / 'mismatches.json', audit.mismatches)
        write_new(out / 'input_manifest.json', {'observed_files': list(audit.files.values()), 'observer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
        print(json.dumps(summary, indent=2), flush=True)
        return 0 if not audit.mismatches else 2
    except BaseException as error:
        write_new(out / 'failure.json', {'status': 'OBSERVER_FAILURE', 'observed_utc': utc(),
            'error_type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(),
            'completed_comparisons': audit.comparisons, 'mismatches_so_far': audit.mismatches,
            'principal_research_minutes_claimed': 0})
        write_new(out / 'input_manifest.json', {'observed_files': list(audit.files.values()), 'observer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
        raise


if __name__ == '__main__':
    raise SystemExit(main())
