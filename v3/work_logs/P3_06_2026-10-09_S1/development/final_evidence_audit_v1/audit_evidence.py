"""Read-only scientific evidence verification; no forecaster/test-suite reruns.

Writes a new final audit only. Existing artifacts, manifests, sources, clocks,
ledgers, task states and publication files are not modified.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote
import zipfile

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]
SESSION = HERE.parents[2]
DEV = SESSION / 'development'
RESULT = SESSION / 'reviews/final_evidence_audit.json'
SELF_DIR = HERE.parent
CASES = ('recurring_shortcuts', 'balanced_nonshortcut_null', 'delayed_pending_tail', 'varying_stakes_actions')
CHECKS = Counter()
ISSUES = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def rel(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load(path):
    return json.loads(path.read_text())


def check(condition, group, detail):
    CHECKS[group] += 1
    if not condition:
        ISSUES.append({'kind': 'DATA_OR_HASH_CHECK_FAILED', 'group': group, 'detail': detail})


FILE_MAP_FIELDS = {'files', 'artifacts_sha256', 'source_sha256', 'sources_sha256',
    'source_files_sha256', 'input_manifests_sha256', 'original_run_source_hashes',
    'inputs_sha256'}
SCALAR_HASH_FIELDS = {'source_sha256', 'source_result_sha256', 'source_derivation_sha256',
    'theorem_snapshot_sha256', 'audit_source_sha256', 'legacy_source_sha256',
    'legacy_result_sha256', 'repro_source_sha256', 'review_source_sha256',
    'chronology_checker_sha256', 'script_sha256', 'initial_sha256',
    'original_manifest_sha256', 'input_manifest_sha256', 'old_result_sha256',
    'new_result_sha256', 'checkpoint_archive_sha256', 'reviewed_production_sha256',
    'production_sha256_after', 'v3/time_ledger.csv_sha256', 'v2/time_ledger.csv_sha256'}


def hash_claims(node, pointer=()):
    if isinstance(node, dict):
        for key, value in node.items():
            at = pointer + (key,)
            exact = isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value)
            mapped = pointer and pointer[-1] in FILE_MAP_FIELDS
            listed = key == 'sha256' and any(k in node for k in ('path', 'file', 'source'))
            if exact and (key in SCALAR_HASH_FIELDS or mapped or listed):
                hint = key if mapped else (node.get('path', node.get('file', node.get('source')))
                    if listed else node.get('source_path') if key == 'source_sha256' else None)
                if key.endswith('.csv_sha256'):
                    hint = key[:-7]
                yield {'field': '/'.join(map(str, at)), 'expected_sha256': value,
                       'declared_path': hint, 'snapshot_path': node.get('snapshot') if listed or key == 'source_sha256' else None,
                       'declared_bytes': node.get('bytes'),
                       'strict_artifact_location': key == 'sha256' and 'path' in node
                           or bool(pointer and pointer[-1] in ('files', 'artifacts_sha256')),
                       'map_field': pointer[-1] if pointer else None}
            if isinstance(value, (dict, list)):
                yield from hash_claims(value, at)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from hash_claims(value, pointer + (index,))


def candidates(record, claim):
    hints = []
    if claim.get('snapshot_path'):
        hints += [ROOT / claim['snapshot_path'], record.parent / claim['snapshot_path']]
    hint = claim.get('declared_path')
    if hint:
        p = Path(hint)
        if p.is_absolute():
            hints.append(p)
        elif claim['map_field'] == 'artifacts_sha256':
            hints.append(record.parent / p)
        elif record.name == 'archive_manifest.json':
            hints += [record.parent / p, ROOT / p]
        elif record.name == 'CHECKPOINT_MANIFEST.json':
            hints.append(record.parent / p)
        elif record.name == 'repaired_snapshot_manifest.json':
            hints += [record.parent / 'source_snapshot_v1_1' / p, record.parent / p]
        elif str(p).startswith('v3/') or str(p).startswith('v2/'):
            hints += [ROOT / p, record.parent / p]
        else:
            hints += [record.parent / p, ROOT / p]
    return list(dict.fromkeys(p.resolve() for p in hints))


def normalized_records(value, key=''):
    if key in ('producer_counts', 'checker_counts') and isinstance(value, list):
        value = dict(value)
    if isinstance(value, dict):
        return {k: (v is not None if k == 'known_answer_source' else normalized_records(v, k))
                for k, v in value.items()
                if k not in ('source_receipt_sha256', 'receipt_sha256', 'issued_reports_sha256', 'reports_sha256', 'sha256')}
    if isinstance(value, list):
        return [normalized_records(v, key) for v in value]
    return value


PRICE_PRESENTATION_FIELDS = {'elapsed_wall_ns', 'old_certificate_transferred',
    'rerun_uses_its_own_certificate', 'retained_action_original_cost_certificate_applicable',
    'retained_report_original_brier_calibration_certificate_applicable'}


def price_numeric_projection(value):
    if isinstance(value, dict):
        return {k: price_numeric_projection(v) for k, v in value.items() if k not in PRICE_PRESENTATION_FIELDS}
    if isinstance(value, list):
        return [price_numeric_projection(v) for v in value]
    return value


def public_projection(case):
    records = {row['query']['query_id']: row for row in case['records']}
    tape = []
    for event in case['events']:
        row = records[event['query_id']]
        if event['kind'] == 'issue_input':
            tape.append({'kind': 'issue', 'event': event['event'], 'tick': event['tick'],
                         'query': row['query'], 'weight': row['weight'], 'actions': row['actions']})
        elif event['kind'] == 'answer_admitted':
            receipt = row['receipt']['record']
            tape.append({'kind': 'admit', 'event': event['event'], 'tick': event['tick'],
                         'query_id': event['query_id'], 'scope': receipt['scope'],
                         'answer': event['answer'], 'residue': receipt['residue'],
                         'source_receipt_sha256': event['receipt_sha256']})
    return tape


def numeric_evidence():
    math_rows, replay_rows, capital_rows = [], [], []
    for case in CASES:
        runs = [load(DEV / f'mathematical_queries_v{i}/{case}.json') for i in (1, 2, 3)]
        old, peak, repaired = runs
        check(old['records'] == peak['records'], 'v1_v2_full_records_equal', case)
        check(normalized_records(old['records']) == normalized_records(repaired['records']),
              'v1_v3_all_record_content_equal_after_receipt_normalization', case)
        for field in ('metrics', 'core_audits', 'pending_ids', 'input_generation_counts', 'shared_expert_actual_counters'):
            check(old[field] == peak[field] == repaired[field], 'v1_v2_v3_numeric_field_equal', case + ':' + field)
        check(peak['state_fraction_bit_observations'] == repaired['state_fraction_bit_observations'],
              'v2_v3_full_instrumentation_trace_equal', case)
        check(normalized_records(old['events']) == normalized_records(repaired['events']),
              'v1_v3_event_tape_equal_after_receipt_digest_normalization', case)
        for i, run in enumerate(runs, 1):
            manifest = load(DEV / f'mathematical_queries_v{i}/manifest.json')
            check(run['queries'] == len(run['records']) == manifest['queries_per_case'] == 128,
                  'declared_128_query_count', f'{case}:v{i}')
            for row in run['records']:
                check(digest(row['reports']) == row['issued_reports_sha256'], 'saved_report_digest', f'{case}:v{i}')
                if row.get('receipt'):
                    check(digest(row['receipt']['record']) == row['receipt']['sha256'],
                          'saved_receipt_representation_digest', f'{case}:v{i}')
            by_identity = {row['query']['query_id']: row for row in run['records']}
            receipts_by_digest = {row['receipt']['sha256']: row['receipt']
                                  for row in run['records'] if row.get('receipt')}
            issue_events = {e['query_id']: e for e in run['events'] if e['kind'] == 'issue_input'}
            admission_events = {e['query_id']: e for e in run['events'] if e['kind'] == 'answer_admitted'}
            for event in run['events']:
                row = by_identity[event['query_id']]
                if event['kind'] == 'all_reports_committed':
                    check(event['reports_sha256'] == row['issued_reports_sha256'],
                          'committed_event_report_digest_link', f'{case}:v{i}')
                if event['kind'] == 'answer_admitted':
                    check(event['receipt_sha256'] == row['receipt']['sha256'],
                          'admitted_event_receipt_digest_link', f'{case}:v{i}')
            for row in run['records']:
                for interpretation in row['interpretations']:
                    cached_source = interpretation.get('known_answer_source')
                    if cached_source is None:
                        continue
                    receipt = receipts_by_digest.get(cached_source)
                    claim = receipt['record'] if receipt else {}
                    prior_admission = admission_events.get(claim.get('query_id'))
                    query = row['query']
                    check(receipt is not None and receipt['admitted']
                          and claim['claim_key'] == [query[k] for k in ('scope', 'a', 'n', 'm', 'r')]
                          and claim['answer'] == row['outcome']
                          and prior_admission is not None
                          and prior_admission['event'] < issue_events[query['query_id']]['event']
                          and prior_admission['tick'] <= row['tick'],
                          'cached_source_is_same_claim_previously_admitted_receipt', f'{case}:v{i}')
        settled = [r for r in old['records'] if r['outcome'] is not None]
        cached = [r for r in old['records'] if r['status'] == 'known_at_issue']
        pending = [r['query']['query_id'] for r in old['records'] if r['outcome'] is None]
        check(sorted(pending) == sorted(old['pending_ids']), 'full_case_pending_partition', case)
        check(len(cached) == 1 and len(old['records']) - len(cached) == 127, 'cached_and_fresh_counts', case)
        math_rows.append({'case': case, 'queries': 128, 'fresh_issues': 127,
                          'cached_at_issue': len(cached), 'settled_with_cache': len(settled),
                          'fresh_admissions': sum(e['kind'] == 'answer_admitted' for e in old['events']),
                          'pending': len(pending), 'first_cached_issue_tick': cached[0]['tick'],
                          'forecast_metrics_and_core_audits_equal_v1_v2_v3': True,
                          'receipt_normalization': 'drop digest links and normalize immutable counter pair lists to mappings; preserve all remaining record values',
                          'cached_source_receipt_links_verified_all_versions': True,
                          'v2_v3_all_peak_observations_equal': True})
        prices = [load(DEV / f'price_replay_v{i}/{case}.json') for i in (1, 2)]
        tape = public_projection(old)
        check(price_numeric_projection(prices[0]) == price_numeric_projection(prices[1]),
              'price_v1_v2_numeric_equivalence', case)
        for i, data in enumerate(prices, 1):
            check(data['public_tape'] == tape, 'price_public_projection_matches_saved_source', f'{case}:v{i}')
            check(digest(data['public_tape']) == data['public_tape_sha256'], 'public_tape_digest', f'price:{case}:v{i}')
            for profile, replay in data['replays'].items():
                check(len(replay['labels']) == len(settled) and sorted(replay['pending_ids']) == sorted(pending),
                      'price_replay_same_admission_cutoff', f'{case}:v{i}:{profile}')
                for method, forecasts in replay['forecasts'].items():
                    check(len(forecasts) == 128, 'price_replay_forecast_population', f'{case}:v{i}:{profile}:{method}')
        replay_rows.append({'case': case, 'profiles': list(prices[1]['replays']),
                            'full_numeric_equivalence_v1_v2': True,
                            'excluded_fields': sorted(PRICE_PRESENTATION_FIELDS),
                            'public_tape_sha256': prices[1]['public_tape_sha256'],
                            'issued': 128, 'settled': len(settled), 'pending': len(pending)})
        capital = load(DEV / f'capital_comparison_v1/{case}.json')
        expected_tape = [e for e in tape if e['tick'] <= 32]
        check(capital['public_tape'] == expected_tape, 'capital_exact_tick32_public_prefix', case)
        check(digest(expected_tape) == capital['public_tape_sha256'], 'public_tape_digest', 'capital:' + case)
        inputs = {e['query']['query_id']: e for e in expected_tape if e['kind'] == 'issue'}
        labels = {e['query_id']: e['answer'] for e in expected_tape if e['kind'] == 'admit'}
        pending_ids = sorted(set(inputs) - set(labels))
        check(len(inputs) == capital['horizon'] == 32 and set(capital['reports']) == set(inputs),
              'capital_prefix_count_and_identity', case)
        check(labels == capital['admitted_labels'] and pending_ids == capital['pending_ids'],
              'capital_actual_admission_cutoff_partition', case)
        check(capital['counts']['issue_calls'] == 32 and capital['counts']['reveal_calls'] == len(labels),
              'capital_recorded_call_counts', case)
        weight = sum((F(inputs[q]['weight']) for q in labels), F(0))
        for method, metric in capital['metrics'].items():
            check(metric['settled'] == len(labels) and F(metric['weight']) == weight,
                  'capital_all_comparators_same_population_weight', f'{case}:{method}')
        check(sum(a['state']['settled'] for a in capital['copy_audits']) == len(labels),
              'capital_copy_settlement_count', case)
        check(sum(a['pending'] for a in capital['copy_audits']) == len(pending_ids),
              'capital_copy_pending_count', case)
        capital_rows.append({'case': case, 'issued_at_cutoff': 32, 'fresh_issues': capital['counts']['issue_calls'],
                             'cached_at_issue': capital['counts'].get('cache_hits', 0),
                             'settled_at_cutoff': len(labels), 'pending_at_cutoff': len(pending_ids),
                             'pending_ids': pending_ids, 'settled_weight': str(weight),
                             'copy_count': len(capital['copy_audits']),
                             'allowance_misses': capital['counts']['allowance_misses'],
                             'not_scored_using_eventual_labels_after_tick32': True})
    old = load(SESSION / 'recovery/checkpoint_original/saved_workspaces/p306_defensive_addendum/development_result.json')
    new = load(DEV / 'preserved_rerun_v1/development_result.json')
    exclusions = set(load(DEV / 'preserved_rerun_v1/rerun_receipt.json')['excluded_environment_fields'])
    check({k:v for k,v in old.items() if k not in exclusions} == {k:v for k,v in new.items() if k not in exclusions},
          'preserved_addendum_deterministic_saved_payload_equal', sorted(exclusions))
    return {'mathematical_queries': math_rows, 'price_replay': replay_rows,
            'capital_prefix': capital_rows, 'preserved_addendum_assertions': old['assertions'],
            'no_forecaster_or_original_test_suite_rerun': True}


def targeted_stored_probes():
    """Check result populations and source bindings, without executing either probe."""
    bria_dir = DEV / 'bria_constant_bound_v1'
    bria_plan = load(bria_dir / 'plan.json')
    bria = load(bria_dir / 'result.json')
    check(bria['status'] == 'PASS' and bria['assertions'] == sum(bria['checks'].values()) == 20588,
          'targeted_probe_declared_assertion_count', 'bria_constant_bound_v1')
    check(bria_plan['horizon'] == bria['horizon'] == len(bria['records']) == 127
          and [row['t'] for row in bria['records']] == list(range(1, 128)),
          'targeted_probe_declared_prefix_population', 'bria_constant_bound_v1')
    unit_dir = DEV / 'unit_covariance_v1'
    unit_plan = load(unit_dir / 'plan.json')
    unit = load(unit_dir / 'result.json')
    check(unit['status'] == 'PASS' and unit['assertions'] == sum(unit['checks'].values()) == 3522,
          'targeted_probe_declared_assertion_count', 'unit_covariance_v1')
    expected_profiles = [(case, profile) for case in unit_plan['cases'] for profile in unit_plan['profiles']]
    check([(row['case'], row['profile']) for row in unit['cases']] == expected_profiles,
          'unit_covariance_announced_cases_and_profiles', 'two cases times three profiles')
    unit_rows = []
    reports_by_case = {}
    for row in unit['cases']:
        source = load(DEV / f"mathematical_queries_v1/{row['case']}.json")
        tape = [e for e in public_projection(source) if e['tick'] <= unit_plan['prefix_issue_ticks']]
        issues = [e['query']['query_id'] for e in tape if e['kind'] == 'issue']
        admitted = [e['query_id'] for e in tape if e['kind'] == 'admit']
        pending = sorted(set(issues) - set(admitted))
        description = row['case'] + ':' + row['profile']['name']
        check(unit_plan['prefix_issue_ticks'] == row['issued'] == len(issues) == len(row['capital_reports']) == 16
              and [report['query'] for report in row['capital_reports']] == issues,
              'unit_covariance_exact_tick16_issue_population', description)
        check(row['admitted'] == len(admitted) and row['pending'] == len(pending),
              'unit_covariance_actual_admission_cutoff_partition', description)
        original_reports = reports_by_case.setdefault(row['case'], row['capital_reports'])
        check(row['capital_reports'] == original_reports,
              'unit_covariance_saved_capital_report_and_copy_identity_across_profiles', description)
        unit_rows.append({'case': row['case'], 'profile': row['profile'], 'issued': len(issues),
                          'admitted': len(admitted), 'pending': len(pending), 'pending_ids': pending})
    return {'bria_constant_bound': {'status': bria['status'], 'stored_assertions': bria['assertions'],
                'horizon': bria['horizon'], 'stored_records': len(bria['records']),
                'capital_scope': bria['capital_scope'], 'result_sha256': sha(bria_dir / 'result.json')},
            'unit_covariance': {'status': unit['status'], 'stored_assertions': unit['assertions'],
                'prefix_issue_ticks': unit_plan['prefix_issue_ticks'], 'cases': unit_rows,
                'capital_reports_total': sum(row['issued'] for row in unit_rows),
                'admissions_total_across_profiles': sum(row['admitted'] for row in unit_rows),
                'result_sha256': sha(unit_dir / 'result.json')},
            'scope': 'Stored source and input hashes, assertion-count arithmetic, prefix populations and cross-profile retained-report identity only; neither probe executed.'}


def markdown_links(files):
    rows = []
    for file in files:
        for match in re.finditer(r'\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', file.read_text()):
            link = match.group(1)
            if link.startswith(('https://', 'http://', 'mailto:', '#')):
                continue
            target = link[8:] if link.startswith('sandbox:') else link
            target = (file.parent / unquote(target.split('#', 1)[0])).resolve()
            rows.append({'document': rel(file), 'link': link, 'target': rel(target),
                         'exists': target.exists(), 'historical_snapshot': 'source_snapshot' in file.parts})
    return rows


def main():
    started = datetime.now(timezone.utc).isoformat()
    scientific_files = sorted(p for area in ('development', 'reviews', 'recovery')
        for p in (SESSION / area).rglob('*') if p.is_file() and '__pycache__' not in p.parts
        and SELF_DIR not in p.parents and p != RESULT and p.name != 'final_evidence_audit.md')
    modules = sorted((ROOT / 'v3/checks').glob('06_*.py'))
    docs = sorted((ROOT / 'v3/derivations').glob('06_*.md')) + sorted((ROOT / 'v3/literature').glob('06_*.md'))
    archive = ROOT.parent / 'upload/value_logic_P3_06_checkpoint(1).zip'
    other = [ROOT / 'v3/time_ledger.csv', ROOT / 'v2/time_ledger.csv', archive]
    files = list(dict.fromkeys(scientific_files + modules + docs + other))
    index, observations = defaultdict(list), {}
    for path in files:
        observations[path] = {'path': rel(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}
        index[observations[path]['sha256']].append(path)
    manifests = [p for p in scientific_files if p.suffix == '.json' and 'manifest' in p.name.lower()]
    claims = []
    for record in (p for p in scientific_files if p.suffix == '.json'):
        for claim in hash_claims(load(record)):
            claim['record'] = rel(record)
            places = candidates(record, claim)
            actual = next((p for p in places if p.is_file()), None)
            matches = index.get(claim['expected_sha256'], [])
            exact_declared = next((p for p in places if p.is_file() and sha(p) == claim['expected_sha256']), None)
            claim['declared_location_observed'] = rel(actual) if actual else None
            claim['declared_location_sha256'] = sha(actual) if actual else None
            claim['matching_files'] = [rel(p) for p in matches]
            if exact_declared:
                claim['resolution'] = 'EXACT_AT_DECLARED_OR_SNAPSHOT_LOCATION'
                selected = exact_declared
            elif matches:
                claim['resolution'] = 'EXACT_SOURCE_CONTENT_PRESERVED_ELSEWHERE'
                selected = matches[0]
                if actual and claim['strict_artifact_location']:
                    claim['resolution'] = 'DECLARED_ARTIFACT_LOCATION_MISMATCH'
                    ISSUES.append({'kind': claim['resolution'], 'record': rel(record), 'field': claim['field']})
            else:
                selected = None
                claim['resolution'] = 'SOURCE_BYTES_NOT_LOCATED'
                ISSUES.append({'kind': claim['resolution'], 'record': rel(record),
                               'field': claim['field'], 'expected_sha256': claim['expected_sha256']})
            if actual and sha(actual) != claim['expected_sha256'] and matches:
                claim['historical_path_now_has_a_newer_revision'] = True
            if selected and claim['declared_bytes'] is not None:
                claim['bytes_match'] = selected.stat().st_size == claim['declared_bytes']
                check(claim['bytes_match'], 'declared_byte_count', rel(record) + ':' + claim['field'])
            if selected:
                check(sha(selected) == claim['expected_sha256'], 'file_hash_claim', rel(record) + ':' + claim['field'])
            claims.append(claim)
    zipped = []
    with zipfile.ZipFile(archive) as source:
        check(source.testzip() is None, 'checkpoint_archive_crc', rel(archive))
        for info in source.infolist():
            if info.is_dir():
                continue
            target = SESSION / 'recovery/checkpoint_original' / info.filename
            original = source.read(info)
            check(target.is_file() and target.read_bytes() == original, 'checkpoint_member_preserved_exactly', info.filename)
            zipped.append({'archive_member': info.filename, 'bytes': len(original),
                           'sha256': hashlib.sha256(original).hexdigest(), 'preserved_path': rel(target)})
    numeric = numeric_evidence()
    targeted = targeted_stored_probes()
    links = markdown_links([p for p in scientific_files if p.suffix == '.md'] + docs)
    current_missing = [row for row in links if not row['exists'] and not row['historical_snapshot']
                       and row['target'] != rel(RESULT)]
    for row in current_missing:
        ISSUES.append({'kind': 'CURRENT_MISSING_MARKDOWN_TARGET', **row})
    review_coverage = []
    for file in sorted((SESSION / 'reviews').glob('*.md')):
        if file.name == 'final_evidence_audit.md':
            continue
        current = sha(file)
        covered = [claim['record'] for claim in claims if 'manifest' in Path(claim['record']).name.lower()
                   and claim['expected_sha256'] == current and rel(file) in claim['matching_files']]
        review_coverage.append({'path': rel(file), 'sha256_at_audit': current,
                                'prior_hash_manifests_covering_current_bytes': sorted(set(covered))})
    current_modules = []
    for module in modules:
        data = observations[module]
        match = re.search(r'^VERSION\s*=\s*[\'\"]([^\'\"]+)', module.read_text(), re.M)
        data['version'] = match.group(1) if match else None
        data['matching_source_records'] = sorted({claim['record'] for claim in claims
            if claim['expected_sha256'] == data['sha256'] and 'source' in claim['field']})
        check(bool(data['matching_source_records']), 'current_module_has_matching_saved_source_record', rel(module))
        current_modules.append(data)
    stable = []
    for file in scientific_files + modules:
        unchanged = sha(file) == observations[file]['sha256']
        stable.append({'path': rel(file), 'unchanged_during_audit': unchanged})
        check(unchanged, 'existing_scientific_evidence_unchanged_during_audit', rel(file))
    result = {'schema': 'value_logic.p306.final_scientific_evidence_audit.v1',
              'status': 'VERIFIED_WITH_DECLARED_PROVENANCE_LIMITATION' if ISSUES else 'PASS',
              'reviewer': 'ChatGPT (GPT-6 Astra Pro), independent implementation reviewer',
              'principal_research90_seconds': 0, 'started_utc': started,
              'completed_utc': datetime.now(timezone.utc).isoformat(),
              'script_path': rel(HERE), 'script_sha256': sha(HERE),
              'checker_draft_preservation': load(SELF_DIR / 'draft_1_preservation.json'),
              'successful_audit_draft_preservation': load(SELF_DIR / 'draft_3_preservation.json'),
              'checks': sum(CHECKS.values()), 'checks_by_group': dict(CHECKS),
              'issues': ISSUES, 'manifest_count': len(manifests),
              'manifests': [{'path': rel(p), 'sha256': sha(p),
                            'hash_claim_count': sum(claim['record'] == rel(p) for claim in claims)} for p in manifests],
              'file_hash_claim_count': len(claims), 'file_hash_claims': claims,
              'current_six_modules': current_modules,
              'checkpoint_archive': {'path': rel(archive), 'sha256': sha(archive), 'members': zipped},
              'frozen_data_numeric_evidence': numeric,
              'late_targeted_stored_probes': targeted,
              'markdown_links_checked': len(links), 'missing_markdown_links': [r for r in links if not r['exists']],
              'review_hash_coverage': review_coverage,
              'historical_dependency_context': [{
                  'source': rel(DEV / 'price_replay_v1/source_snapshot/v3/checks/06_price_replay.py'),
                  'missing_adjacent_dependency': '06_defensive_forecasting.py',
                  'matching_dependency_sha256': sha(ROOT / 'v3/checks/06_defensive_forecasting.py'),
                  'available_dependency': 'v3/checks/06_defensive_forecasting.py',
                  'meaning': 'Exact historical source bytes are preserved; restore the matching unchanged dependency beside it before executing this partial snapshot.'}],
              'observed_scientific_files': [observations[p] for p in scientific_files],
              'stability_checks': stable,
              'scope': 'File identity, saved numerical equivalence, report/receipt digests and exact population cutoffs; no forecaster, original test-suite, clock/gate or publication operation.'}
    with RESULT.open('x') as handle:
        # A closing review links to this result, which is created only here.
        # Verify that target after exclusive creation; it is not an old input.
        for row in links:
            if row['target'] == rel(RESULT):
                row['exists'] = RESULT.is_file()
        result['missing_markdown_links'] = [row for row in links if not row['exists']]
        json.dump(result, handle, indent=2, sort_keys=True); handle.write('\n')
    print(json.dumps({'status': result['status'], 'checks': result['checks'],
                      'manifests': len(manifests), 'file_hash_claims': len(claims),
                      'issues': ISSUES, 'capital_prefixes': numeric['capital_prefix']}))


if __name__ == '__main__':
    main()
