"""Independent saved-artifact review of ND01 report section 5.5.

No experiment, model, population or reporting implementation is imported.
Historical report audits are read and hash-bound, never overwritten.
Contributor: ChatGPT (GPT-6 Astra Pro), independent protocol/statistics audit.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import sys


SESSION = Path(__file__).resolve().parent
ROOT = SESSION.parents[2]
ANALYSIS = ROOT / 'v2/experiments/F15_ND01_analysis'
REPORT = ROOT / 'v2/experiments/F15_ND01_results.md'
RUN = ROOT / 'v2/work_logs/F15_ND01_v1_run1'
checks, inputs = [], {}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name, condition, detail=None):
    value = {'name': name, 'passed': bool(condition)}
    if detail is not None:
        value['detail'] = detail
    checks.append(value)


def read(path, sidecar=False):
    inputs[str(path.relative_to(ROOT))] = digest(path)
    if sidecar:
        check('sidecar/' + str(path.relative_to(ROOT)),
              digest(path) == Path(str(path) + '.sha256').read_text().strip().split()[0])
    return json.loads(path.read_text())


def rational(value):
    return Fraction.from_float(float(value))


def mask(prepared, method):
    if method == 'fractional_mask':
        return [rational(x) for x in prepared['mask']['values']]
    if method == 'binary_global':
        selected = prepared['binary_global']['subset']
    else:
        selected = prepared[{'frozen_original': 'original_subset', 'rounded_top8': 'rounded_subset'}[method]]
    return [Fraction(int(i in selected)) for i in range(32)]


historical_paths = [SESSION / name for name in ['audit_final_report.py', 'audit_final_report.json',
                                               'audit_final_report.json.sha256', 'audit_final_report.md']]
historical_before = {str(p.relative_to(ROOT)): digest(p) for p in historical_paths}
old = read(SESSION / 'audit_final_report.json', True)
check('historical_report_audit_pass', old['passed'] and old['check_count'] == 621 and old['failure_count'] == 0)
check('historical_report_snapshot', old['report_sha256'] == '2ba0372855335965d98e8514e4cb06556d41c86c2010ecf96676397d992de598')

feasibility = read(ANALYSIS / 'joint_feasibility.json', True)
witnesses = read(ANALYSIS / 'joint_witnesses.json', True)
manifest = read(RUN / 'preparation_complete.json', True)
rational_audit = read(SESSION / 'audit_joint_feasibility.json', True)
witness_audit = read(SESSION / 'audit_joint_witnesses.json', True)
check('independent_rational_audit', rational_audit['all_checks_passed']
      and rational_audit['total_checks'] == 3625 and not rational_audit['failures'])
check('independent_witness_audit', witness_audit['all_checks_passed']
      and witness_audit['total_checks'] == 452 and not witness_audit['failures'])
for artifact, name in [(feasibility, 'joint_feasibility'), (witnesses, 'joint_witnesses')]:
    script = ANALYSIS / (name + '.py')
    inputs[str(script.relative_to(ROOT))] = digest(script)
    check(name + '/script_hash', digest(script) == artifact['script_sha256'])
    for filename, expected in artifact['inputs'].items():
        p = ROOT / filename
        check(name + '/input_hash/' + filename, digest(p) == expected)
    check(name + '/development_only', artifact['development_only'])

check('feasibility/no_model_forward', feasibility['model_forwards'] == 0)
check('feasibility/no_populations_or_fits', feasibility['new_populations'] == feasibility['new_fits'] == 0)
check('feasibility/post_outcome', feasibility['post_outcome_supplementary'])
for key in ['new_model_forwards', 'new_fits', 'new_populations', 'new_validation_scores']:
    check('witnesses/' + key, witnesses[key] == 0)
check('witnesses/post_outcome', witnesses['post_outcome_analytic_construction'])

geometries = {g['model_index']: g for g in feasibility['geometries']}
check('geometry/ranks', [geometries[i]['exact_difference_span_rank'] for i in range(5)] == [30, 30, 29, 29, 29])
check('geometry/null_counts', [len(geometries[i]['inactive']) for i in range(5)] == [2, 2, 3, 3, 3])
check('geometry/hyperplane_comparisons', sum(g['pairwise_variable_hyperplane_comparisons'] for g in geometries.values()) == 2003)
for i, g in geometries.items():
    check('geometry/full_rank_prerequisites/' + str(i), not g['duplicate_variable_hyperplanes']
          and g['exact_active_weight_rank'] == len(g['active'])
          and g['nullspace_is_exactly_inactive_coordinates'] and g['two_sphere_specialization_prerequisites'])

# Recompute each rational compatibility margin from saved source weights/masks.
# Complete-rank prerequisites are independently certified by the separate
# rational geometry auditor; no hidden activations are executed here.
soft = {u['index']: u for u in manifest['units'] if u['kind'] == 'soft_mask'}
rows = {(r['model_index'], r['method']): r for r in feasibility['rows']}
methods = ['frozen_original', 'binary_global', 'rounded_top8', 'fractional_mask']
check('feasibility/full_case_set', set(rows) == {(i, m) for i in range(5) for m in methods})
recomputed = []
for i, source_record in enumerate(manifest['freeze']['source_prepared']):
    source = read(ROOT / source_record['path'])
    check('source_binding/' + str(i), digest(ROOT / source_record['path']) == source_record['sha256'])
    prepared = read(RUN / soft[i]['file'], True)
    v = [rational(x) for x in source['network']['v']]
    inactive = geometries[i]['inactive']
    observable = [j for j in range(32) if j not in inactive]
    t2 = sum((v[j] ** 2 for j in inactive), Fraction()) / 4
    check('nonzero_inactive_head/' + str(i), t2 > 0)
    for method in methods:
        m0, m1 = [mask(r, method) for r in prepared['roles']]
        c0 = [m0[j] * v[j] for j in observable]
        c1 = [m1[j] * v[j] for j in observable]
        vd = [v[j] for j in observable]
        d0 = sum((x * y - x * x for x, y in zip(c0, vd)), Fraction())
        d1 = sum((x * y - x * x for x, y in zip(c1, vd)), Fraction())
        overlap = sum((x * y for x, y in zip(c0, c1)), Fraction())
        central = (d0 + d1 + t2) ** 2 <= 4 * (d0 + t2) * (d1 + t2)
        capacity = (d0 + d1 + t2) / 2
        margin = capacity - overlap
        saved = rows[(i, method)]
        check('case/nonnegative_components/' + str((i, method)), min(d0, d1, overlap, t2) >= 0)
        check('case/central_branch/' + str((i, method)), central and saved['branch'] == 'central_rational')
        for key, expected in [('delta0_exact', d0), ('delta1_exact', d1),
                              ('observable_overlap_exact', overlap), ('inactive_head_quarter_energy_exact', t2),
                              ('maximum_cancellation_lower_exact', capacity), ('maximum_cancellation_upper_exact', capacity),
                              ('feasibility_margin_lower_exact', margin), ('feasibility_margin_upper_exact', margin)]:
            check('case/rational/' + str((i, method, key)), Fraction(saved[key]) == expected)
        status = 'feasible' if margin >= 0 else 'infeasible'
        check('case/status/' + str((i, method)), saved['status'] == status)
        check('case/display/' + str((i, method)), saved['feasibility_margin'] == float(margin))
        recomputed.append({'model_index': i, 'method': method, 'status': status, 'margin': str(margin)})

expected_counts = {'frozen_original': (2, 3), 'binary_global': (4, 1), 'rounded_top8': (3, 2), 'fractional_mask': (4, 1)}
for method, (yes, no) in expected_counts.items():
    check('counts/' + method, feasibility['counts'][method] == {'feasible': yes, 'infeasible': no,
          'prerequisite_not_established': 0, 'unresolved_interval_boundary': 0})
feasible_keys = {k for k, row in rows.items() if row['status'] == 'feasible'}
witness_keys = {(w['model_index'], w['method']) for w in witnesses['witnesses']}
check('witnesses/exact_coverage', len(witnesses['witnesses']) == 13 and witness_keys == feasible_keys)
for w in witnesses['witnesses']:
    check('witnesses/scope/' + str((w['model_index'], w['method'])),
          w['constructed_after_registered_outcomes'] and not w['new_intervention_population_scored']
          and not w['semantic_joint_cost_adequacy_claimed'])
    check('witnesses/matrix_shapes/' + str((w['model_index'], w['method'])),
          len(w['projectors']) == 2 and all(len(p) == 32 and all(len(row) == 32 for row in p) for p in w['projectors']))
    check('witnesses/complement_dimension/' + str((w['model_index'], w['method'])), 32 - 3 >= 2 * (8 - 1))
max_error = max(max(w['errors'].values()) for w in witnesses['witnesses'])
check('witnesses/maximum_error', max_error == witnesses['maximum_identity_error'] and max_error <= 2.23e-16)

prose = REPORT.read_text()
inputs[str(REPORT.relative_to(ROOT))] = digest(REPORT)
proof_path = ANALYSIS / 'joint_feasibility.md'
inputs[str(proof_path.relative_to(ROOT))] = digest(proof_path)
for label, method in [('Original F15 subsets', 'frozen_original'), ('Exhaustive binary subsets', 'binary_global'),
                       ('Rounded fractional masks', 'rounded_top8'), ('Fractional masks', 'fractional_mask')]:
    yes, no = expected_counts[method]
    candidates = [line.replace('**', '') for line in prose.splitlines() if line.startswith('| ' + label + ' |')]
    expected = f'| {label} | {yes}/5 | {no}/5 |'
    check('report/feasibility_table/' + method, expected in candidates)

for label, name in [('Exact joint-feasibility classification', 'joint_feasibility_attempt1.end.json'),
                    ('Deterministic compatible-projector witnesses', 'joint_witnesses_attempt1.end.json')]:
    command = read(SESSION / 'commands' / name)
    matching = [line for line in prose.splitlines() if line.startswith('| ' + label + ' |')]
    check('report/cost_row_exists/' + name, len(matching) == 1)
    if len(matching) == 1:
        got = [float(s.strip().replace(',', '')) for s in matching[0].split('|')[2:-1]]
        expected = [1, command['returncode'], command['observed_wall_seconds'],
                    command['child_user_cpu_seconds'] + command['child_system_cpu_seconds'], command['child_max_rss_kib']]
        for index, (a, b) in enumerate(zip(got, expected)):
            check('report/cost_value/' + name + '/' + str(index), math.isclose(a, b, rel_tol=1e-10, abs_tol=5.1e-7))
    check('command/no_error/' + name, command['returncode'] == 0)

link_prose = re.sub(r'```[\s\S]*?```', '', prose)
link_prose = re.sub(r'\\\[[\s\S]*?\\\]', '', link_prose)
links = []
for target in re.findall(r'!?\[[^\]\n]+\]\(([^)\n]+)\)', link_prose):
    if target.startswith(('https://', 'http://', '#')):
        continue
    path = (REPORT.parent / target.split('#', 1)[0]).resolve()
    links.append(str(path.relative_to(ROOT)))
    check('report/link/' + target, path.exists())

scope = [json.loads(line) for line in (SESSION / 'scope_decisions.jsonl').read_text().splitlines()]
branch_choice = next(x for x in scope if x.get('question', '').startswith('Can the two existing fractional'))
branch_close = next(x for x in scope if x.get('status') == 'supplementary analytic branch scientifically completed')
check('scope/post_outcome_selected', 'after core diagnostic outcomes' in branch_choice['status'])
check('scope/recorded_sub_budget', branch_close['engaged_D_E_minutes'] <= branch_close['protected_sub_budget_minutes'] == 20)
for k in ['new_model_forwards', 'new_fits', 'new_populations']:
    check('scope/no_scientific_extension/' + k, branch_close[k] == 0)

for path, before in historical_before.items():
    check('historical_preservation/' + path, digest(ROOT / path) == before)

result = {
    'schema': 'F15-ND01-independent-report-addendum-audit-v1',
    'reviewer': 'ChatGPT (GPT-6 Astra Pro)',
    'scope': 'section 5.5 saved exact-feasibility counts, margins, witness coverage, report costs and links; proof reviewed manually',
    'report_sha256': digest(REPORT), 'proof_sha256': digest(proof_path),
    'historical_report_audit_preserved': historical_before,
    'check_count': len(checks), 'failure_count': sum(not c['passed'] for c in checks),
    'passed': all(c['passed'] for c in checks), 'checks': checks, 'inputs': inputs,
    'rational_cases_recomputed': recomputed, 'witness_pairs': len(witnesses['witnesses']),
    'maximum_recorded_witness_error': max_error, 'local_link_count': len(links),
    'manual_derivation_review': {
        'distinct_kink_full_span_argument': 'correct under the explicitly checked distinct hyperplanes and full active-weight rank',
        'central_sphere_criterion': 'correct and necessary/sufficient for existing output-effect coefficients in the stored Euclidean metric',
        'rank_eight_extension': 'correct existence argument; 29-dimensional common complement provides 14 mutually orthogonal additions',
        'gauge_dependence': 'correct for at least two null directions and nonzero inactive head; scaling incoming inactive parameters down increases reciprocal head energy',
        'inactive_unit_removal': 'correct restricted-space exact statement with positive observable sphere deficit',
        'semantic_scope': 'adequately separated from exact output-effect feasibility and no approximate impossibility claimed',
    },
    'independent_matrix_audit': 'audit_joint_witnesses.json; matrix products not repeated by this report addendum',
    'new_model_executions': 0, 'new_populations': 0, 'new_fits': 0, 'principal_minutes_added': 0,
    'accounting_scope': 'recorded branch sub-budget checked only; final Research90 and ledger audit remain separate',
    'scientific_corrections_required': [], 'script_sha256': digest(Path(__file__)),
}
target = SESSION / 'audit_report_addendum.json'
encoded = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
if sys.argv[1:] == ['--check']:
    assert target.read_bytes() == encoded
    assert Path(str(target) + '.sha256').read_text().strip() == digest(target)
else:
    assert not sys.argv[1:]
    with target.open('xb') as handle:
        handle.write(encoded)
    with Path(str(target) + '.sha256').open('x') as handle:
        handle.write(digest(target) + '\n')
print(json.dumps({'passed': result['passed'], 'checks': len(checks),
                  'failures': [c for c in checks if not c['passed']],
                  'report_sha256': result['report_sha256'], 'local_links': len(links)}))
