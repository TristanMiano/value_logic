"""Read saved F16 evidence once; do not execute experiments or probe code.

Contributor: ChatGPT (GPT-6 Astra Pro). This is a reporting calculation.
It validates journal counts and hashes the inputs used for the principal report.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'evidence_summary_attempt1.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUTPUT.exists():
        raise FileExistsError('Preserve the existing reporting calculation.')
    inputs = {}

    def read(rel, lines=False):
        path = ROOT / rel
        inputs[rel] = {'sha256': digest(path), 'bytes': path.stat().st_size}
        text = path.read_text()
        return [json.loads(line) for line in text.splitlines()] if lines else json.loads(text)

    math = read('math_checks/attempt1/records.jsonl', True)
    math_summary = read('math_checks/attempt1/summary.json')
    assert len(math) == math_summary['completed_records'] == 1439
    assert all(row['status'] == 'pass' for row in math)
    counts = Counter(row['family'] for row in math)
    k3 = [row for row in math if row['family'] == 'k3_nonexchangeable_fibers']
    dimensions = Counter((row['fiber_dimension'], row['nonexchangeable']) for row in k3)
    direct = sum(row['edited_query_checks'] for row in k3)
    assert direct == math_summary['families']['k3_nonexchangeable_fibers']['direct_edited_order_checks'] == 23616
    assert digest(ROOT / 'math_checks/attempt1/records.jsonl') == math_summary['records_sha256']

    impl = read('reviews/implementation/attempt1.jsonl', True)
    impl_summary = read('reviews/implementation/attempt1_summary.json')
    supplement = read('reviews/implementation/supplement1.json')['records']
    setup = [r for r in impl if r['name'] == 'source_manifest' or r['name'].endswith('_setup')]
    substantive = [r for r in impl if r not in setup] + supplement
    rejections = [r for r in substantive if 'exception' in r]
    assert len(impl) == impl_summary['records'] == 65
    assert len(setup) == 6 and len(substantive) == 62 and len(rejections) == 41
    assert all(r['status'] == 'PASS' for r in impl + supplement)

    candidate = read('reviews/price/coherent_center_search/attempt1/summary.json')
    candidate_rows = read('reviews/price/coherent_center_search/attempt1/records.jsonl', True)
    assert candidate['counts']['checked'] == candidate['counts']['candidate_pass'] == len(candidate_rows) == 735
    assert candidate['specified_but_unrun'] == 0
    price = read('reviews/price/reconstruct_checks_output.json')
    core = read('reviews/core/adversarial_results.json')
    verifiers = [read('reviews/integrity/' + name + '_attempt1.end.json') for name in ('f14_verify', 'nd01_verify')]
    assert all(r['attempt'] == 1 and r['returncode'] == 0 and r['stderr_bytes'] == 0 for r in verifiers)
    integrity = read('reviews/integrity/integrity_result.json')
    assert integrity['scientific_artifact_inventory_unchanged_during_review'] is True
    inputs['summarize_evidence.py'] = {'sha256': digest(Path(__file__)), 'bytes': Path(__file__).stat().st_size}
    result = {
        'id': 'F16-REPORT-01', 'attempt': 1, 'status': 'pass',
        'contributor': 'ChatGPT (GPT-6 Astra Pro)',
        'scope': 'Read-only saved-output analysis; no new probe, population, model or scientific stage.',
        'mathematical_checks': {
            'records': len(math), 'families': dict(counts),
            'k3_dimension_and_exchangeability': [
                {'dimension': dimension, 'nonexchangeable': nonexchangeable, 'records': count}
                for (dimension, nonexchangeable), count in sorted(dimensions.items())],
            'direct_edited_order_checks': direct,
            'resource_observation': {key: math_summary[key] for key in
                ('wall_seconds', 'user_cpu_seconds', 'system_cpu_seconds', 'peak_rss_kib')},
            'saved_735_certificates_are_not_a_second_experiment': True,
        },
        'implementation': {
            'main_journal_records': len(impl), 'setup_records': len(setup),
            'supplement_records': len(supplement), 'substantive_records': len(substantive),
            'expected_rejections': len(rejections), 'unexpected_failures': 0,
            'per_probe_wall_cpu_rss': None,
            'resource_limitation': 'These process resources were not separately measured; no estimate is invented.'},
        'core_probe_families': len(core),
        'price_checks': {key: price[key] for key in ('status', 'direct_rank_families', 'lower_moment_rank_cases')},
        'price_A1_cases': len(price['A1_cases']),
        'candidate_search': candidate,
        'freeze_verifiers': verifiers,
        'preservation_audit': {
            key: integrity[key] for key in ('source_base', 'inventory_files', 'differences_from_base',
                'scientific_artifact_inventory_unchanged_during_review', 'registered_freezes')},
        'inputs': inputs,
        'limits': ['Finite records are not independent statistical samples or an unrestricted proof.',
                   'Separate same-model reviews are not external replications.',
                   'Concurrent reviewer and process wall time is never added to principal engaged time.',
                   'F15 and ND01 conclusions, failures and saved bytes remain as previously recorded.'],
    }
    with OUTPUT.open('x') as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write('\n')
    print(json.dumps({'status': 'pass', 'output': str(OUTPUT), 'sha256': digest(OUTPUT),
                      'mathematical_records': len(math), 'implementation_substantive': len(substantive),
                      'expected_rejections': len(rejections)}))


if __name__ == '__main__':
    main()
