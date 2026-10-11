"""P3-10-A1: explicit continuation after deterministic structural bootstrap defect.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
No generator, old-source mutation, implicit replay, or original-completion repair.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True
from pathlib import Path
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / 'v3/experiments'))
import argparse
import json
import subprocess
import p309_lifecycle as L
import p309_freeze as F

AMENDMENT = REPO / 'v3/experiments/amendments/P3_10_A1'
OLD = REPO / 'v3/experiments/final_v1'
ROOT = REPO / 'v3/experiments/final_v1_amended_A1'
MANIFEST = AMENDMENT / 'manifest.json'
AID = 'P3-10-A1'
EXPECTED_FREEZE = '69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70'
EXPECTED_PROTOCOL = 'dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f'
FAILURE = OLD / 'stages/public/attempts/attempt_01/failure.json'


def require(condition, message):
    if not condition:
        raise L.IntegrityError(message)


def publish_or_compare(path, value):
    if path.exists():
        require(L.read_json(path) == value, 'Changed immutable derived record: ' + str(path))
    else:
        L.publish_json(path, value)


def checked_path(relative):
    p = Path(relative)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix() == relative,
            'Noncanonical repository-relative path')
    full = REPO / p
    require(full.is_file() and not full.is_symlink(), 'Missing or symbolic bound file: ' + relative)
    return full


def check_inventory(rows):
    for row in rows:
        path = checked_path(row['path'])
        require(path.stat().st_size == row['bytes'] and L.sha256_file(path) == row['sha256'],
                'Bound evidence changed: ' + row['path'])


def verify_amendment(stage):
    F.require_p310('P3-10')
    F.require_runtime_startup()
    m = L.read_json(MANIFEST)
    require(m['amendment_id'] == AID and m['status'] == 'SEALED_BEFORE_AMENDED_EXECUTION',
            'Amendment not prospectively sealed')
    require(m['original_manifest_sha256'] == EXPECTED_FREEZE and
            m['original_protocol_sha256'] == EXPECTED_PROTOCOL, 'Wrong inherited freeze')
    check_inventory(m['new_sources'])
    F.verify_source_snapshot(AMENDMENT / 'source', m['new_sources'])
    check_inventory(m['original_evidence'])
    require(L.sha256_file(AMENDMENT / 'protocol.json') == m['amendment_protocol_sha256'],
            'Amendment protocol changed')
    require(L.sha256_file(AMENDMENT / 'protocol.md') == m['amendment_prose_sha256'],
            'Amendment prose changed')
    require(L.sha256_file(FAILURE) == m['original_failure_sha256'], 'Original failure changed')
    require(not (OLD / 'stages/public/complete.json').exists(),
            'Original incomplete public lineage was unexpectedly completed')
    require(not (OLD / 'stages/evaluation').exists() and not (OLD / 'stages/analysis').exists(),
            'Original private lineage unexpectedly started')
    old_inventory = {p.relative_to(REPO).as_posix() for p in OLD.rglob('*')
                     if p.is_file() and p.name != 'writer.lock'}
    require(old_inventory == {r['path'] for r in m['original_evidence']},
            'Original evidence roster changed')
    # Run the EXACT old verifier in a separate clean interpreter. The new driver
    # is separately admitted below; its presence is never hidden from closure checks.
    command = ['python3'] + F.PYTHON_FLAGS + ['v3/experiments/p309_freeze.py', 'verify']
    observed = L.utc_now()
    child = subprocess.run(command, cwd=REPO, capture_output=True, text=True, check=False)
    require(child.returncode == 0, 'Original verification failed: ' + child.stderr)
    verification = json.loads(child.stdout)
    require(verification['status'] == 'VERIFIED' and
            verification['manifest_sha256'] == EXPECTED_FREEZE and
            verification['protocol_sha256'] == EXPECTED_PROTOCOL, 'Unexpected original verifier receipt')
    require(F.runtime_record() == L.read_json(REPO / F.FROZEN / 'runtime.json'),
            'Amended interpreter differs from exact original runtime')
    original_manifest = L.read_json(REPO / F.FROZEN / 'manifest.json')
    sources = [r['path'] for r in original_manifest['sources']] + [r['path'] for r in m['new_sources']]
    origins = F.validate_loaded_local_sources(sources)
    config = L.read_json(REPO / F.PROTOCOL)
    schedule = L.read_json(REPO / F.FROZEN / 'schedule.json')
    old_binding = {'freeze_id': verification['freeze_id'], 'manifest_sha256': EXPECTED_FREEZE,
                   'protocol_sha256': EXPECTED_PROTOCOL}
    binding = dict(old_binding, amendment_id=AID, amendment_manifest_sha256=L.sha256_file(MANIFEST))
    publish_or_compare(ROOT / 'amendment_binding.json', binding)
    # Unique per-command evidence. An amendment permits no implicit second attempt.
    L.publish_json(ROOT / 'verification' / (stage + '.json'), {
        'schema': 'value_logic.p310_a1.verification.v1', 'amendment_id': AID,
        'started_utc': observed, 'finished_utc': L.utc_now(), 'original_verify_command': command,
        'original_verifier': verification, 'stderr': child.stderr,
        'expanded_source_closure': sources, 'loaded_local_source_origins': origins,
        'runtime_exact_match': True, 'original_evidence_files': len(old_inventory), 'binding': binding})
    return m, binding, old_binding, config, schedule, sources


def row_reference(row, root, evidence_class):
    return {'unit_id': row['unit']['id'], 'origin_root': root.relative_to(REPO).as_posix(),
            'seal_path': row['seal_path'], 'seal_sha256': L.sha256_file(root / row['seal_path']),
            'result_path': row['result_path'], 'result_sha256': row['seal']['result_sha256'],
            'evidence_class': evidence_class}


def inherited_rows(old_binding, schedule, manifest):
    inputs_stage = L.Stage(OLD, 'inputs', old_binding, schedule['groups'])
    inputs_stage.verify_complete()  # Exists and must compare exactly; never recreated.
    inputs = inputs_stage.completed()
    old_stage = L.Stage(OLD, 'public', old_binding, schedule['units'])
    originals = [old_stage.completed_unit(u) for u in schedule['units']]
    reused = [r for r in originals if r is not None]
    remaining = [u for u, r in zip(schedule['units'], originals) if r is None]
    require(len(inputs) == 12 and len(reused) == 440 and len(remaining) == 60,
            'Amendment cannot change inherited or remaining denominators')
    require(all(r['unit']['arm'] in ('broker', 'certificates') for r in reused),
            'Wrong original-unit reuse scope')
    require(all(u['arm'] == 'conformance' for u in remaining), 'Wrong continuation scope')
    require(remaining == manifest['remaining_public_units'], 'Remaining fixed roster differs')
    require([r['unit']['id'] for r in reused] == manifest['reused_public_unit_ids'],
            'Inherited public roster differs')
    return inputs, reused, remaining


def composite(binding, schedule, reused, continuation, *, create):
    by_id = {r['unit']['id']: (r, OLD, 'original_prospective_unchanged_public_record') for r in reused}
    for row in continuation:
        uid = row['unit']['id']
        require(uid not in by_id, 'Duplicate composite public unit')
        by_id[uid] = (row, ROOT, 'post_exposure_amended_inherited_conformance')
    require(len(by_id) == 500 and set(by_id) == {u['id'] for u in schedule['units']},
            'Private barrier: all 500 scheduled public units must be validly sealed')
    refs = [row_reference(*by_id[u['id']]) for u in schedule['units']]
    value = {'schema': 'value_logic.p310_a1.composite_public.v1', 'binding': binding,
             'expected_units': 500, 'completed_units': 500, 'original_units': 440,
             'amended_units': 60, 'original_public_stage_complete': False,
             'original_failure_sha256': L.sha256_file(FAILURE), 'seals': refs,
             'scope': 'Explicit mixed-provenance public barrier; never an original v1 completion.'}
    path = ROOT / 'composite_public.json'
    if create:
        publish_or_compare(path, value)
    else:
        require(path.is_file() and L.read_json(path) == value, 'Missing or changed composite public barrier')
    return {uid: triple[0] for uid, triple in by_id.items()}


def bootstrap(loaded, unit):
    if unit['arm'] == 'conformance' and unit['engine'] == 'legacy_structural':
        legacy = loaded['conformance']._load('v3/experiments/p308_structural.py')
        # The sole execution amendment: inherited startup before the unchanged
        # paid worker/private checker. No method monkeypatch or tariff mutation.
        legacy._load_legacy()
        require(legacy.M is not None and legacy.K is not None, 'Structural bootstrap did not initialize')


def merged_history(current_unit_id):
    original = L.execution_history(OLD)
    amended = L.execution_history(ROOT, current_stage='analysis', current_unit_id=current_unit_id)
    unknown = [dict(r, origin_root=root.relative_to(REPO).as_posix())
               for root, audit in ((OLD, original), (ROOT, amended))
               for r in audit['unknown_unsealed_public_attempts']]
    other = [dict(r, origin_root=root.relative_to(REPO).as_posix())
             for root, audit in ((OLD, original), (ROOT, amended))
             for r in audit['unknown_other_stage_attempts']]
    require(any(r['origin_root'] == OLD.relative_to(REPO).as_posix() for r in unknown),
            'Original failed public prefix must remain unknown')
    return {'schema': 'value_logic.p310_a1.merged_execution_history.v1',
            'amendment_id': AID,
            'stages': [dict(s, origin_root=root.relative_to(REPO).as_posix())
                       for root, audit in ((OLD, original), (ROOT, amended)) for s in audit['stages']],
            'unknown_unsealed_public_attempts': unknown, 'unknown_other_stage_attempts': other,
            'complete_outer_paid_attempt_accounting': False,
            'complete_physical_run_accounting': False,
            'invoice_scope': 'Original failed prefix remains unknown; every sealed internal-attempt invoice retained.',
            'current_analysis_cost_location': 'Surrounding amended sealed analysis-unit resource observation',
            'original_public_stage_complete': False,
            'post_exposure_amendment_scope': 'All conformance records and overall orchestration labeled amended.'}


def execute(name):
    # A single new orchestrator and an original-root lock exclude both writers.
    with L.exclusive_lock(ROOT / 'orchestration.lock'), L.exclusive_lock(OLD / 'writer.lock'):
        m, binding, old_binding, config, schedule, sources = verify_amendment(name)
        loaded = F.adapters()
        inputs, reused, remaining = inherited_rows(old_binding, schedule, m)
        input_map = {r['unit']['id']: r for r in inputs}
        publish_or_compare(ROOT / 'input_reference.json', {
            'schema': 'value_logic.p310_a1.input_reference.v1', 'binding': binding,
            'expected_units': 12, 'completed_units': 12, 'new_generations': 0,
            'original_exposure_sha256': L.sha256_file(OLD / 'exposure.json'),
            'seals': [row_reference(r, OLD, 'original_prospective_input') for r in inputs]})
        public_stage = L.Stage(ROOT, 'public', binding, remaining)
        score_units = [dict(u, id='score-' + u['id'], public_unit_id=u['id']) for u in schedule['units']]
        evaluation = L.Stage(ROOT, 'evaluation', binding, score_units)
        analysis = L.Stage(ROOT, 'analysis', binding, [{'id': 'all-frozen-endpoints', 'arm': 'analysis'}])
        def public_input(unit):
            return input_map[unit['group_id']]['result']['value']
        def source_check():
            F.validate_loaded_local_sources(sources)
        if name == 'public':
            def run(unit):
                bootstrap(loaded, unit)
                source_check()
                paid = loaded[unit['arm']].run(unit, public_input(unit), config['arms'][unit['arm']])
                source_check()
                return {'input_result_sha256': input_map[unit['group_id']]['seal']['result_sha256'],
                        'paid_result': paid}
            result = public_stage.execute(run)
            composite(binding, schedule, reused, public_stage.completed(), create=True)
        else:
            public_stage.verify_complete()
            public = composite(binding, schedule, reused, public_stage.completed(), create=False)
            if name == 'evaluation':
                original = {u['id']: u for u in schedule['units']}
                def score(score_unit):
                    unit = original[score_unit['public_unit_id']]
                    row = public[unit['id']]
                    bootstrap(loaded, unit)
                    source_check()
                    value = loaded[unit['arm']].score(unit, row['result']['value']['paid_result'],
                                                      public_input(unit), config['arms'][unit['arm']])
                    source_check()
                    return {'public_result_sha256': row['seal']['result_sha256'],
                            'input_result_sha256': input_map[unit['group_id']]['seal']['result_sha256'],
                            'score': value}
                result = evaluation.execute(score)
            else:
                require(name == 'analysis', 'Unknown amended stage')
                evaluation.verify_complete()
                import p309_analyze
                source_check()
                scored = evaluation.completed()
                result = analysis.execute(lambda u: p309_analyze.analyze(
                    config, schedule, scored, execution_audit=merged_history(u['id'])))
        source_check()
        check_inventory(m['original_evidence'])
        return {'amendment_id': AID, 'scope': 'Mixed-provenance amended completion',
                'stage': name, 'completion': result,
                'complete_original_v1_execution': False,
                'original_failed_prefix_cost': 'unknown',
                'positive_end_to_end_economic_claim_permitted': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task', required=True, choices=('P3-10',))
    parser.add_argument('--stage', required=True, choices=('public', 'evaluation', 'analysis'))
    args = parser.parse_args()
    print(json.dumps(execute(args.stage), sort_keys=True, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
