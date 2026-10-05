"""Independent ND01 report/repeatability check using saved artifacts only.

No experiment module imports, model executions, fits, or populations.
Contributor: ChatGPT (GPT-6 Astra Pro), independent protocol/statistics audit.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re
import struct


SESSION = Path(__file__).resolve().parent
ROOT = SESSION.parents[2]
ANALYSIS = ROOT / 'v2/experiments/F15_ND01_analysis'
RUN = ROOT / 'v2/work_logs/F15_ND01_v1_run1'
REPORT = ROOT / 'v2/experiments/F15_ND01_results.md'
checks = []
inputs = {}


def check(name, condition, detail=None):
    row = {'name': name, 'passed': bool(condition)}
    if detail is not None:
        row['detail'] = detail
    checks.append(row)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path, sidecar=False):
    path = path.resolve()
    inputs[str(path.relative_to(ROOT))] = digest(path)
    if sidecar:
        expected = Path(str(path) + '.sha256').read_text().strip().split()[0]
        check(str(path.relative_to(ROOT)) + '/sidecar', digest(path) == expected)
    return json.loads(path.read_text())


def close(name, actual, expected, tolerance=2e-12):
    check(name, math.isclose(actual, expected, rel_tol=1e-10, abs_tol=tolerance),
          {'actual': actual, 'expected': expected})


def rounded_cells(label, expected):
    matching = [line for line in prose.splitlines() if line.startswith('| ' + label + ' |')]
    if label == 'Exhaustive binary':
        matching = [line for line in matching if '/5' not in line]
    check('report_row/' + label + '/unique', len(matching) == 1)
    if len(matching) != 1:
        return
    cells = [x.strip().replace('**', '') for x in matching[0].split('|')[2:-1]]
    check('report_row/' + label + '/width', len(cells) == len(expected))
    for i, (got, wanted) in enumerate(zip(cells, expected)):
        if isinstance(wanted, str):
            check('report_row/' + label + '/' + str(i), got == wanted,
                  {'actual': got, 'expected': wanted})
        else:
            close('report_row/' + label + '/' + str(i), float(got.replace(',', '')), wanted, 5.1e-7)


def packed_hash(*arrays):
    result = hashlib.sha256()
    for shape, flat in arrays:
        result.update(json.dumps(shape, separators=(',', ':')).encode('ascii'))
        result.update(struct.pack('<' + 'd' * len(flat), *flat))
    return result.hexdigest()


prose = REPORT.read_text()
inputs[str(REPORT.relative_to(ROOT))] = digest(REPORT)
core = read(ANALYSIS / 'core_summary.json')
mechanism = read(ANALYSIS / 'mechanism_results.json', True)
repeat = read(ANALYSIS / 'repeatability.json', True)
manifest = read(RUN / 'preparation_complete.json', True)
eval_manifest = read(RUN / 'evaluation_complete.json', True)
selection = read(ANALYSIS / 'selection_diagnostics.json')

# Check only local links in Markdown prose; exclude mathematical/code blocks.
link_prose = re.sub(r'```[\s\S]*?```', '', prose)
link_prose = re.sub(r'\\\[[\s\S]*?\\\]', '', link_prose)
links = []
for target in re.findall(r'!?\[[^\]\n]+\]\(([^)\n]+)\)', link_prose):
    if target.startswith(('https://', 'http://', '#')):
        continue
    path = (REPORT.parent / target.split('#', 1)[0]).resolve()
    links.append(str(path.relative_to(ROOT)))
    check('report_link/' + target, path.exists())

# Saved source and completion hashes quoted in the report.
for name, path in [
    ('F14 freeze', ROOT / 'v2/experiments/freeze.v1.json'),
    ('ND01 freeze', ROOT / 'v2/experiments/neural_diagnostic_v1/freeze.json'),
    ('ND01 config', ROOT / 'v2/experiments/neural_diagnostic_v1/config.json'),
    ('preparation complete', RUN / 'preparation_complete.json'),
    ('evaluation complete', RUN / 'evaluation_complete.json'),
    ('core summary', ANALYSIS / 'core_summary.json'),
    ('mechanism results', ANALYSIS / 'mechanism_results.json'),
    ('selection diagnostic', ANALYSIS / 'selection_diagnostics.json'),
]:
    inputs[str(path.relative_to(ROOT))] = digest(path)
    check('reported_hash/' + name, digest(path) in prose)

masks = {x['method']: x for x in core['masks']['methods']}
for label, method in [
    ('Original F15 selected subset', 'frozen_original'),
    ('Exhaustive binary, eight coordinates', 'binary_global'),
    ('Top-eight rounding of fractional mask', 'rounded_top8'),
    ('Fractional mask, total mass eight', 'fractional_mask'),
]:
    m = masks[method]
    adequate = sum(r['error_and_decision_point_thresholds_met'] for r in m['role_rows'])
    rounded_cells(label, [m['mean_mae'], m['mean_near_disagreement'], m['mean_far_disagreement'],
                         m['mean_role_equal_target_output_effect_rms'], str(adequate) + '/10',
                         str(m['models_with_both_roles_meeting_point_thresholds']) + '/5'])

baseline = core['ordinary_conditional_baselines']['summary']
for label, stratum in [('Mixed near', 'mixed_near'), ('Mixed far', 'mixed_far'),
                       ('Preserve other cost', 'preserve_other'), ('Equal target cost', 'equal_target'),
                       ('Scale separating', 'scale_separating')]:
    values = [next(x['mean_mae'] for x in baseline[key]['by_stratum'] if x['stratum'] == stratum)
              for key in ['base_prediction', 'no_swap', 'whole_layer_swap']]
    values.append(next(x['mean_mae'] for x in masks['fractional_mask']['by_stratum'] if x['stratum'] == stratum))
    rounded_cells(label, values)

variants = {x['method']: x for x in core['search']['variants']}
for label, family in [('Cost correlation', 'cost_corr'), ('Log-cost correlation', 'log_cost_corr'),
                       ('Positive native-contribution covariance', 'positive_contribution_cov'),
                       ('Uniform', 'uniform'), ('Permuted cost correlation', 'permuted_cost_corr')]:
    rounded_cells(label, [variants[f'{family}/budget_{b}/{s}']['mean_mae']
                         for s, b in [('frozen_mse', 128), ('frozen_mse', 1024), ('robust', 128), ('robust', 1024)]])
    comparison = core['search']['paired_comparisons']['budgets'][family + '/frozen_mse']
    check('all_frozen_mse_budget_role_gains_nonnegative/' + family, comparison['negative_role_means'] == 0)

for label, method in [('Original subset', 'frozen_original'), ('Exhaustive binary', 'binary_global'),
                       ('Fractional', 'fractional_mask')]:
    rows = [x for x in mechanism['error_decomposition'] if x['method'] == method]
    check('decomposition_cell_count/' + method, len(rows) == 50)
    rounded_cells(label, [math.fsum(x[k] for x in rows) / len(rows) for k in
                         ['base_logit_mse', 'contribution_residual_change_mse', 'twice_cross_moment', 'total_logit_mse']])

for label, method in [('Original subsets', 'frozen_original'), ('Exhaustive binary', 'binary_global'),
                       ('Fractional masks', 'fractional_mask')]:
    rows = [x for x in mechanism['secondary_composition'] if x['method'] == method]
    # The label Exhaustive binary also occurs in the decomposition table, so
    # locate the joint table explicitly instead of guessing the first row.
    if label == 'Exhaustive binary':
        line = next(x for x in prose.splitlines() if x.startswith('| Exhaustive binary |') and '/5' in x)
        values = [v.strip().replace('**', '') for v in line.split('|')[2:-1]]
        expected = [str(sum(x['order_probability_max_abs'] > 1e-12 for x in rows)) + '/5'] + [
            math.fsum(x[k] for x in rows) / 5 for k in ['order_probability_rms', 'role0_then_role1_joint_probability_mae',
                                                      'role1_then_role0_joint_probability_mae']]
        check('joint_row/binary_global/count', values[0] == expected[0])
        for i in range(1, 4):
            close('joint_row/binary_global/' + str(i), float(values[i]), expected[i], 5.1e-7)
    else:
        rounded_cells(label, [str(sum(x['order_probability_max_abs'] > 1e-12 for x in rows)) + '/5'] + [
            math.fsum(x[k] for x in rows) / 5 for k in ['order_probability_rms', 'role0_then_role1_joint_probability_mae',
                                                      'role1_then_role0_joint_probability_mae']])

for label, filename in [('Preparation', 'prepare_attempt1.end.json'),
                        ('Pre-evaluation all-unit verification', 'pre_evaluation_verify.end.json'),
                        ('Evaluation', 'evaluate_attempt1.end.json'),
                        ('Supplementary same-array mechanism reconstruction', 'mechanism_analysis_attempt1.end.json'),
                        ('Post-outcome repeatability from saved moments', 'repeatability_attempt1.end.json')]:
    command = read(SESSION / 'commands' / filename)
    rounded_cells(label, [1, command['returncode'], command['observed_wall_seconds'],
                         command['child_user_cpu_seconds'] + command['child_system_cpu_seconds'],
                         command['child_max_rss_kib']])

# Repeatability independently uses only the recorded Gram matrices and masks.
# For T(h)=(I-M)h+Md, T(T(h))-T(h)=M(I-M)(d-h).
repeat_script = ANALYSIS / 'repeatability.py'
check('repeatability/script_hash', digest(repeat_script) == repeat['script_sha256'])
for filename, expected in repeat['inputs'].items():
    check('repeatability/input_hash/' + filename, digest(ROOT / filename) == expected)
for k in ['new_pairs', 'new_fits', 'new_model_executions']:
    check('repeatability/no_execution/' + k, repeat[k] == 0)
check('repeatability/post_outcome', repeat['post_outcome_supplementary'] is True)
check('repeatability/development_only', repeat['development_only'] is True)
quadratics = {(x['model_index'], x['role']): x for x in mechanism['discovery_quadratics']}
repeat_rows = {(x['model_index'], x['role']): x for x in repeat['rows']}
check('repeatability/full_cartesian_keys', set(repeat_rows) == {(i, r) for i in range(5) for r in range(2)})
recomputed_rms = []
for unit in manifest['units']:
    if unit['kind'] != 'soft_mask':
        continue
    prepared = read(RUN / unit['file'], True)
    for role, fitted in enumerate(prepared['roles']):
        key = (unit['index'], role)
        q = quadratics[key]
        saved = repeat_rows[key]
        gram, linear, constant = q['gram'], q['linear'], q['constant']
        check('repeatability/quadratic_hash/' + str(key), packed_hash(
            ([32, 32], [x for row in gram for x in row]), ([32], linear), ([1], [constant]))
            == q['quadratic_hash'] == fitted['binary_global']['quadratic_coefficients_hash'])
        mask = fitted['mask']['values']
        drift = [x * (1 - x) for x in mask]
        for j, (got, expected) in enumerate(zip(saved['fractional_replacement_drift_weights'], drift)):
            close('repeatability/drift/' + str(key) + '/' + str(j), got, expected)
        mse = math.fsum(drift[i] * gram[i][j] * drift[j] for i in range(32) for j in range(32))
        check('repeatability/mse_nonnegative/' + str(key), mse >= 0)
        rms = math.sqrt(mse)
        recomputed_rms.append(rms)
        close('repeatability/mse/' + str(key), saved['fractional_repeated_application_logit_mse'], mse)
        close('repeatability/rms/' + str(key), saved['fractional_repeated_application_logit_rms'], rms)
        for subset in [fitted['original_subset'], fitted['binary_global']['subset']]:
            check('repeatability/binary_idempotence/' + str(key), len(subset) == len(set(subset)) == 8
                  and all(0 <= x < 32 for x in subset))
        check('repeatability/scope/' + str(key), saved['discovery_pair_count'] == 640
              and saved['new_validation_or_support_test'] is False
              and saved['original_binary_structurally_idempotent']
              and saved['global_binary_structurally_idempotent'])
close('repeatability/mean_rms', repeat['mean_role_logit_rms'], math.fsum(recomputed_rms) / 10)
close('repeatability/min_rms', repeat['logit_rms_range'][0], min(recomputed_rms))
close('repeatability/max_rms', repeat['logit_rms_range'][1], max(recomputed_rms))

findings = [
    {'id': 'R01', 'severity': 'clarification', 'target': 'opening',
     'issue': 'Principal causes suggests a unique causal attribution to the original 0/5.',
     'recommendation': 'Describe concrete contributing limitations.',
     'resolved_in_snapshot': 'principal causes now supported' not in prose},
    {'id': 'R02', 'severity': 'correction', 'target': 'section 4 selector comparison',
     'issue': '10 improved/31 worsened refers to validation worst-normalized objective, not validation MAE.',
     'recommendation': 'Name the validation worst-normalized objective beside those counts.',
     'resolved_in_snapshot': bool(re.search(r'validation[^.]{0,250}worst-normalized[^.]{0,250}(?:10|31)|(?:10|31)[^.]{0,250}validation worst-normalized', prose))},
    {'id': 'R03', 'severity': 'clarification', 'target': 'section 6 first hypothesis row',
     'issue': 'Original ordinary accuracy requirements is ambiguous because ordinary task readiness passed.',
     'recommendation': 'Say original ordinary-network intervention adequacy was not established.',
     'resolved_in_snapshot': 'original ordinary accuracy requirements' not in prose},
    {'id': 'R04', 'severity': 'correction', 'target': 'section 3 fractional counts',
     'issue': '3-10 fractionally weighted coordinates uses the recorded 1e-10 classification tolerance.',
     'recommendation': 'State the tolerance instead of an unqualified strictly fractional count.',
     'resolved_in_snapshot': 'strictly fractional coordinates' not in prose and 'classification tolerance' in prose},
]
result = {'schema': 'F15-ND01-independent-final-report-audit-v1',
          'reviewer': 'ChatGPT (GPT-6 Astra Pro)',
          'scope': 'saved-artifact report arithmetic, local links and independent repeated-edit quadratic reconstruction',
          'checks': checks, 'check_count': len(checks),
          'failure_count': sum(not x['passed'] for x in checks),
          'passed': all(x['passed'] for x in checks), 'findings': findings,
          'inputs': inputs, 'report_sha256': digest(REPORT),
          'local_link_count': len(links), 'local_links': links,
          'repeatability_independent_method': 'stdlib math.fsum of all 1024 Gram quadratic terms per role; no import of repeatability or experiment modules',
          'repeatability_rms_range': [min(recomputed_rms), max(recomputed_rms)],
          'new_model_executions': 0, 'new_populations': 0, 'new_fits': 0,
          'principal_minutes_added': 0,
          'timing_disposition': 'final clock and ledger pending; this is not a Research90 completion certification',
          'literature_review_scope': 'local primary_literature.md provenance/disclosure inspected; no independent full-text retrieval in this audit',
          'joint_panel_review_scope': 'reported aggregates checked against saved outputs; unsaved joint-panel RMS/MAE not independently regenerated',
          'script_sha256': digest(Path(__file__))}
out = SESSION / 'audit_final_report.json'
out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
Path(str(out) + '.sha256').write_text(digest(out) + '\n')
print(json.dumps({'passed': result['passed'], 'checks': len(checks),
                  'failures': [x for x in checks if not x['passed']],
                  'findings': findings, 'report_sha256': result['report_sha256']}))
