"""Independent reconstruction of the original P3-06 mathematical-query tape.

Read-only on saved outputs. Rebuilds admitted knowledge and expert inputs from
events, and checks the ordinary AA on that same information schedule using an
80-digit Decimal diagnostic. That diagnostic is not interval certification.
Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation reviewer.
"""
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import time
import traceback


def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def decimal(value):
    q = F(value)
    return D(q.numerator) / D(q.denominator)


class Checks:
    def __init__(self):
        self.count = 0
        self.groups = Counter()

    def require(self, condition, group, **context):
        self.count += 1
        self.groups[group] += 1
        if not condition:
            raise AssertionError(json.dumps({'group': group, **context}, default=str))


def run(folder):
    checks = Checks()
    manifest = json.loads((folder / 'manifest.json').read_text())
    for name, digest in manifest['artifacts_sha256'].items():
        checks.require(hashlib.sha256((folder / name).read_bytes()).hexdigest() == digest,
                       'saved_artifact_hash', file=name)
    summary = []
    for name in manifest['completed_cases']:
        data = json.loads((folder / (name + '.json')).read_text())
        events = data['events']
        by_query = {}
        for event in events:
            by_query.setdefault(event['query_id'], {})[event['kind']] = event
        records = {r['query']['query_id']: r for r in data['records']}
        admitted_residues = {}
        moduli, residues = Counter(), Counter()
        forecast_count = cached_count = answer_count = 0
        aa_copies, aa_pending = [], {}
        aa_max_error = D(0)
        aa_max_g_error = D(0)
        eta = D(2) / max(decimal(r['weight']) for r in records.values())
        expert_names = ('constant_half', 'residue_frequency', 'partial_exact_shortcut', 'fallible_parity')

        def lse(values):
            maximum = max(values)
            return maximum + sum(((v - maximum).exp() for v in values), D(0)).ln()

        for event in events:
            record = records[event['query_id']]
            q = record['query']
            key = (q['scope'], q['a'], q['n'], q['m'])
            if event['kind'] == 'all_reports_committed':
                checks.require(sha(record['reports']) == event['reports_sha256'] == record['issued_reports_sha256'],
                               'immutable_committed_report_hash')
                if record['status'] == 'known_at_issue':
                    checks.require(key in admitted_residues, 'cache_requires_earlier_admission')
                    residue, source = admitted_residues[key]
                    y = int(residue == q['r'])
                    checks.require(record['outcome'] == y, 'cached_answer_exact')
                    for method, report in record['reports'].items():
                        checks.require(F(report['probability']) == y
                                       and report['detail']['source_receipt_sha256'] == source,
                                       'equal_cache_access', method=method)
                        rows = record['actions']['rows']
                        realized = [F(row[y]) for row in rows]
                        p_action = F(report['action_one_probability'])
                        mixed = (1 - p_action) * realized[0] + p_action * realized[1]
                        checks.require(mixed == min(realized), 'cached_nonpositive_fixed_action_regret')
                    checks.require(all(F(v) == y for v in record['experts'].values()),
                                   'equal_cache_wrapped_experts')
                    cached_count += 1
                    continue

                checks.require(key not in admitted_residues, 'unknown_route_not_already_cached')
                base = q['a'] % q['m']
                result = None
                if q['n'] == 0:
                    result = 1 % q['m']
                elif base == 0:
                    result = 0
                elif base == 1:
                    result = 1
                elif base == q['m'] - 1:
                    result = base if q['n'] % 2 else 1
                expected = {
                    'constant_half': F(1, 2),
                    'residue_frequency': F(residues[(q['m'], q['r'])] + 1, moduli[q['m']] + q['m']),
                    'partial_exact_shortcut': F(int(result == q['r'])) if result is not None else F(1, 2),
                    'fallible_parity': F(3, 4) if (q['a'] + q['n'] + q['r']) % 2 else F(1, 4)}
                checks.require(expected == {k: F(v) for k, v in record['experts'].items()},
                               'experts_from_previously_admitted_information')
                sequence = by_query[q['query_id']]
                receipt = record['receipt']['record']
                checks.require(sequence['issue_input']['event'] < event['event']
                               < sequence['answer_produced_private']['event']
                               < sequence['answer_checked_private']['event'],
                               'report_before_answer_production')
                checks.require(receipt['issued_event'] == sequence['issue_input']['event']
                               and receipt['produced_event'] == sequence['answer_produced_private']['event']
                               and receipt['checked_event'] == sequence['answer_checked_private']['event'],
                               'receipt_event_binding')
                checks.require(sha(receipt) == record['receipt']['sha256'], 'receipt_saved_digest')
                exact = pow(q['a'], q['n'], q['m'])
                checks.require(receipt['residue'] == exact and receipt['answer'] == int(exact == q['r']),
                               'independent_exact_mathematical_answer')
                forecast_count += 1

                # The exact solver may compute the answer itself, but none of its
                # outputs is used for the AA or expert chronology reconstruction.
                report = record['reports']['ordinary_brier_aa_binary64']
                copy_index = next((i for i, c in enumerate(aa_copies) if c['pending'] is None), None)
                if copy_index is None:
                    copy_index = len(aa_copies)
                    aa_copies.append({'logweights': [D(0)] * 4, 'pending': None})
                checks.require(copy_index == report['detail']['copy'], 'AA_free_copy_schedule')
                copy = aa_copies[copy_index]
                qs = tuple(decimal(expected[k]) for k in expert_names)
                weight = decimal(record['weight'])
                kappa = eta * weight
                normalizer = lse(copy['logweights'])
                generalized = tuple(-(lse([v - kappa * (p - y)**2 for v, p in zip(copy['logweights'], qs)])
                                      - normalizer) / kappa for y in (0, 1))
                probability = min(D(1), max(D(0), (1 + generalized[0] - generalized[1]) / 2))
                error = abs(probability - decimal(report['probability']))
                aa_max_error = max(aa_max_error, error)
                aa_max_g_error = max(aa_max_g_error, *(abs(g - D.from_float(float(actual)))
                                                     for g, actual in zip(generalized, report['detail']['generalized_losses_binary64'])))
                checks.require(error <= D('1e-12'), 'AA_high_precision_diagnostic', error=error)
                copy['pending'] = (q['query_id'], qs, weight)
                aa_pending[q['query_id']] = copy_index

            if event['kind'] == 'answer_admitted':
                receipt = record['receipt']['record']
                checks.require(event['event'] > receipt['checked_event']
                               and event['tick'] == record['admission_tick'] == record['scheduled_admission_tick'],
                               'scheduled_admission_after_check')
                checks.require(event['receipt_sha256'] == sha(receipt) and event['answer'] == receipt['answer'],
                               'admission_digest_and_answer')
                admitted_residues[key] = (receipt['residue'], event['receipt_sha256'])
                moduli[q['m']] += 1
                residues[(q['m'], receipt['residue'])] += 1
                answer_count += 1
                copy = aa_copies[aa_pending.pop(q['query_id'])]
                identity, qs, weight = copy['pending']
                checks.require(identity == q['query_id'], 'AA_admits_its_pending_query')
                copy['logweights'] = [v - eta * weight * (p - receipt['answer'])**2
                                      for v, p in zip(copy['logweights'], qs)]
                copy['pending'] = None

        for record in records.values():
            if record['status'] == 'pending':
                checks.require(record['outcome'] is None and 'answer_admitted' not in by_query[record['query']['query_id']],
                               'pending_population_unscored')
        checks.require(set(aa_pending) == set(data['pending_ids']), 'AA_same_pending_population')
        for method, audit in data['core_audits'].items():
            measure = data['metrics'][method]['all_admitted']
            checks.require(audit['pool']['settled'] == answer_count
                           and measure['settled_queries'] == answer_count + cached_count,
                           'cached_rows_outside_core_inside_public_score')
            checks.require(F(measure['task_weighted_brier']) == F(audit['pool']['own_loss']),
                           'cached_Brier_extension_zero')
            cached_weight = sum((F(r['weight']) for r in records.values() if r['status'] == 'known_at_issue'), F(0))
            checks.require(F(measure['settled_weight']) == F(audit['pool']['settled_weight']) + cached_weight,
                           'cached_weight_accounting')
            checks.require(tuple(map(F, measure['calibration_bin_residuals'])) == tuple(map(F, audit['pool']['bin_residuals'])),
                           'cached_calibration_extension_zero')
        for method in data['metrics']:
            settled = [r for r in records.values() if r['outcome'] is not None]
            loss = sum((F(r['weight']) * (F(r['reports'][method]['probability']) - r['outcome'])**2 for r in settled), F(0))
            checks.require(loss == F(data['metrics'][method]['all_admitted']['task_weighted_brier']),
                           'independent_score_reconstruction')
        summary.append({'case': name, 'events': len(events), 'unknown_issued': forecast_count,
                        'cached_issued': cached_count, 'admitted_fresh': answer_count,
                        'pending': len(data['pending_ids']),
                        'maximum_AA_probability_difference_from_80_digit_replay': str(aa_max_error),
                        'maximum_AA_generalized_loss_difference_from_80_digit_replay': str(aa_max_g_error),
                        'reported_binary64_mixability_slack': data['aa_numeric']['maximum_observed_mixability_slack']})
    return {'status': 'PASS', 'checks': checks.count, 'checks_by_group': dict(checks.groups),
            'cases': summary, 'original_run_source_hashes': manifest['source_sha256'],
            'original_manifest_sha256': hashlib.sha256((folder / 'manifest.json').read_bytes()).hexdigest(),
            'scope': 'Independent saved-tape audit; Decimal diagnostics are not interval-certified or a new final evaluation.'}


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    target = here / 'saved_chronology_result.json'
    if target.exists():
        raise SystemExit('Refusing to overwrite an existing chronology result.')
    start_utc = datetime.now(timezone.utc).isoformat()
    start = time.monotonic_ns()
    try:
        with localcontext() as context:
            context.prec = 80
            result = run(here.parent / 'mathematical_queries_v1')
    except Exception:
        result = {'status': 'FAIL', 'traceback': traceback.format_exc()}
    result.update({'schema': 'value_logic.p306.independent_saved_chronology.v1',
                   'start_utc': start_utc, 'end_utc': datetime.now(timezone.utc).isoformat(),
                   'execution_ns': time.monotonic_ns() - start, 'python': platform.python_version(),
                   'review_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'contributor': 'ChatGPT (GPT-6 Astra Pro), independent implementation reviewer',
                   'research_time_credit_ns': 0})
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'checks': result.get('checks'), 'result': str(target)}))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
