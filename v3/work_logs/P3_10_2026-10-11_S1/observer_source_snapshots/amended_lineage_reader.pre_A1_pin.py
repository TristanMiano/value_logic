"""Independent read-only P3-10-A1 provenance and completion barrier.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
Pure standard library. No frozen source import, generator, scorer or worker.
The constructor validates metadata and hashes score bytes without parsing scores.
"""
from pathlib import Path
import hashlib
import json

REPO = Path(__file__).resolve().parents[3]
OLD = REPO / 'v3/experiments/final_v1'
NEW = REPO / 'v3/experiments/final_v1_amended_A1'
AMEND = REPO / 'v3/experiments/amendments/P3_10_A1'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False) + '\n').encode()


def read(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise AssertionError('duplicate metadata key')
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(AssertionError('nonfinite metadata')))


class Lineage:
    def __init__(self):
        # Every stage completion check precedes any score-result parsing.
        assert (OLD / 'stages/inputs/complete.json').is_file()
        assert not (OLD / 'stages/public/complete.json').exists()
        assert not (OLD / 'stages/evaluation').exists()
        assert not (OLD / 'stages/analysis').exists()
        for stage in ('public', 'evaluation', 'analysis'):
            assert (NEW / 'stages' / stage / 'complete.json').is_file(), stage
        assert (NEW / 'composite_public.json').is_file()
        self.binding = read(NEW / 'amendment_binding.json')
        self.old_binding = {k: self.binding[k] for k in ('freeze_id', 'manifest_sha256', 'protocol_sha256')}
        assert self.binding['amendment_id'] == 'P3-10-A1'
        assert self.binding['amendment_manifest_sha256'] == digest(AMEND / 'manifest.json')
        assert self.old_binding['manifest_sha256'] == '69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70'
        assert self.old_binding['protocol_sha256'] == 'dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f'
        assert digest(REPO / 'v3/experiments/frozen_v1/manifest.json') == self.old_binding['manifest_sha256']
        assert digest(REPO / 'v3/experiments/protocol.v1.json') == self.old_binding['protocol_sha256']
        manifest = read(AMEND / 'manifest.json')
        assert manifest['status'] == 'SEALED_BEFORE_AMENDED_EXECUTION'
        for row in manifest['original_evidence']:
            assert digest(REPO / row['path']) == row['sha256']
        for row in manifest['new_sources']:
            assert digest(REPO / row['path']) == row['sha256']
            assert digest(AMEND / 'source' / row['path']) == row['sha256']
        assert digest(AMEND / 'protocol.json') == manifest['amendment_protocol_sha256']
        assert digest(AMEND / 'protocol.md') == manifest['amendment_prose_sha256']
        failure = OLD / 'stages/public/attempts/attempt_01/failure.json'
        assert digest(failure) == manifest['original_failure_sha256']
        frozen_manifest = read(REPO / 'v3/experiments/frozen_v1/manifest.json')
        assert digest(REPO / 'v3/experiments/frozen_v1/schedule.json') == frozen_manifest['schedule_sha256']
        self.schedule = read(REPO / 'v3/experiments/frozen_v1/schedule.json')
        self.indices = {}
        self._stage(OLD, 'inputs', self.old_binding, self.schedule['groups'], 'inputs')
        self._stage(NEW, 'public', self.binding, manifest['remaining_public_units'], '_amended_public')
        score_units = [dict(u, id='score-' + u['id'], public_unit_id=u['id']) for u in self.schedule['units']]
        self._stage(NEW, 'evaluation', self.binding, score_units, 'evaluation')
        self._stage(NEW, 'analysis', self.binding, [{'id': 'all-frozen-endpoints', 'arm': 'analysis'}], 'analysis')
        input_ref = read(NEW / 'input_reference.json')
        assert input_ref['binding'] == self.binding and input_ref['new_generations'] == 0
        assert input_ref['expected_units'] == input_ref['completed_units'] == 12
        assert input_ref['original_exposure_sha256'] == digest(OLD / 'exposure.json')
        assert [r['unit_id'] for r in input_ref['seals']] == [g['id'] for g in self.schedule['groups']]
        for row in input_ref['seals']:
            path, _, _, _ = self.indices['inputs'][row['unit_id']]
            self._reference(row, OLD, path, 'original_prospective_input')
        composite = read(NEW / 'composite_public.json')
        assert composite['binding'] == self.binding
        assert composite['expected_units'] == composite['completed_units'] == 500
        assert composite['original_units'] == 440 and composite['amended_units'] == 60
        assert composite['original_public_stage_complete'] is False
        assert composite['original_failure_sha256'] == digest(failure)
        assert [r['unit_id'] for r in composite['seals']] == [u['id'] for u in self.schedule['units']]
        old_public = read(OLD / 'stages/public/schedule.json')
        old_identity = {k: old_public[k] for k in ('stage', 'binding', 'schedule_sha256')}
        assert old_public['units'] == self.schedule['units'] and old_identity['binding'] == self.old_binding
        assert old_identity['schedule_sha256'] == hashlib.sha256(canonical(self.schedule['units'])).hexdigest()
        self.indices['public'] = {}
        old_count = 0
        for unit, ref in zip(self.schedule['units'], composite['seals']):
            if unit['arm'] == 'conformance':
                entry = self.indices['_amended_public'][unit['id']]
                root, cls = NEW, 'post_exposure_amended_inherited_conformance'
            else:
                seals = list((OLD / 'stages/public/units' / unit['id']).glob('attempt_*/seal.json'))
                assert len(seals) == 1
                entry = self._seal(seals[0], old_identity, unit)
                root, cls = OLD, 'original_prospective_unchanged_public_record'
                old_count += 1
            self._reference(ref, root, entry[0], cls)
            self.indices['public'][unit['id']] = entry
        assert old_count == 440 and len(self.indices['_amended_public']) == 60
        assert len(list((OLD / 'stages/public/units').glob('*/attempt_*/seal.json'))) == 440
        self.receipt = {'amendment_id': 'P3-10-A1', 'manifest_sha256': digest(AMEND / 'manifest.json'),
                        'composite_public_sha256': digest(NEW / 'composite_public.json'),
                        'input_reference_sha256': digest(NEW / 'input_reference.json'),
                        'reader_source_sha256': digest(Path(__file__)),
                        'original_units': 440, 'amended_units': 60, 'score_units': 500,
                        'original_public_stage_complete': False, 'original_failed_prefix_cost': 'unknown',
                        'private_score_payloads_parsed_by_barrier': 0}

    def _reference(self, row, root, path, cls):
        assert row['origin_root'] == root.relative_to(REPO).as_posix()
        assert row['seal_path'] == path.relative_to(root).as_posix()
        assert row['seal_sha256'] == digest(path)
        assert row['result_path'] == (path.parent / 'result.json').relative_to(root).as_posix()
        assert row['result_sha256'] == digest(path.parent / 'result.json')
        assert row['evidence_class'] == cls

    def _seal(self, path, identity, unit):
        seal = read(path)
        assert seal['identity'] == identity
        assert seal['unit_sha256'] == hashlib.sha256(canonical(unit)).hexdigest()
        result_path = path.parent / 'result.json'
        assert digest(result_path) == seal['result_sha256']
        start_path = path.parent / 'start.json'
        assert digest(start_path) == seal['start_sha256']
        start = read(start_path)
        assert start['identity'] == identity and start['unit'] == unit and start['attempt'] == seal['attempt']
        return path, seal, identity, unit

    def _stage(self, root, stage, binding, units, key):
        roster = read(root / 'stages' / stage / 'schedule.json')
        identity = {'stage': stage, 'binding': binding,
                    'schedule_sha256': hashlib.sha256(canonical(units)).hexdigest()}
        assert roster == dict(identity, schema='value_logic.p309.stage.v1', units=units)
        complete = read(root / 'stages' / stage / 'complete.json')
        assert all(complete[k] == v for k, v in identity.items())
        assert complete['expected_units'] == complete['completed_units'] == len(units)
        assert [r['unit_id'] for r in complete['seals']] == [u['id'] for u in units]
        self.indices[key] = {}
        for unit, row in zip(units, complete['seals']):
            p = Path(row['path'])
            assert not p.is_absolute() and '..' not in p.parts
            path = root / p
            assert digest(path) == row['sha256']
            self.indices[key][unit['id']] = self._seal(path, identity, unit)
        assert len(list((root / 'stages' / stage / 'units').glob('*/attempt_*/seal.json'))) == len(units)

    def record(self, stage, identifier):
        path, seal, identity, unit = self.indices[stage][identifier]
        result = read(path.parent / 'result.json')
        assert result['identity'] == identity and result['unit'] == unit
        assert result['attempt'] == seal['attempt']
        return result, seal
