"""P3-06 price replay and immutable-report rescoring development audit.

Contributor: ChatGPT (GPT-6 Astra Pro), October 9, 2026 UTC.
This consumes saved development cases, not a new evaluation population.
Only issue inputs and explicitly admitted answers cross the replay interface.
The original mathematical harness/source manifest remains immutable evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time
import traceback

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
CORE_PATH = HERE.with_name('06_defensive_forecasting.py')
SPEC = importlib.util.spec_from_file_location('p306_price_replay_core', CORE_PATH)
CORE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CORE
SPEC.loader.exec_module(CORE)
VERSION = 'p306-price-replay-v2'
SESSION = ROOT / 'v3/work_logs/P3_06_2026-10-09_S1'
EXPERTS = ('constant_half', 'residue_frequency', 'partial_exact_shortcut', 'fallible_parity')
METHODS = ('scalar_without_decision', 'scalar_with_decision')
PROFILES = ('identity', 'changed_weights', 'changed_rows')
CHECKS = Counter()


def ensure(test, name):
    CHECKS[name] += 1
    if not test:
        raise AssertionError(name)


def digest(value):
    return hashlib.sha256(json.dumps(CORE.encoded(value), sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(CORE.encoded(value), sort_keys=True, indent=2) + '\n')


def public_projection(case):
    """Exclude private receipts, old forecasts, exact-baseline reports and outcomes.

    An admission event supplies its checked residue when and only when admitted.
    Reading this projected input is sufficient for a deterministic full-policy
    replay of this particular expert library on the fixed query/delay schedule.
    """
    records = {r['query']['query_id']: r for r in case['records']}
    result = []
    for event in case['events']:
        r = records[event['query_id']]
        if event['kind'] == 'issue_input':
            result.append({'kind': 'issue', 'event': event['event'], 'tick': event['tick'],
                           'query': deepcopy(r['query']), 'weight': r['weight'],
                           'actions': deepcopy(r['actions'])})
        elif event['kind'] == 'answer_admitted':
            receipt = r['receipt']['record']
            result.append({'kind': 'admit', 'event': event['event'], 'tick': event['tick'],
                           'query_id': event['query_id'], 'scope': receipt['scope'],
                           'answer': event['answer'], 'residue': receipt['residue'],
                           'source_receipt_sha256': event['receipt_sha256']})
    return result


def price_inputs(event, profile):
    """Price rules read only issue-time query fields, tick and original prices."""
    w = F(event['weight'])
    rows = tuple(tuple(F(x) for x in row) for row in event['actions']['rows'])
    eta = F(event['actions']['eta'])
    if profile == 'changed_weights':
        # Declared before replay; no answer, forecast or performance enters it.
        w *= (1, 3, 2, 5)[event['tick'] % 4]
    elif profile == 'changed_rows':
        # A changed false-negative/false-positive pricing question.
        rows = ((rows[0][0], 3 * rows[0][1]),
                (2 * rows[1][0], rows[1][1]))
    elif profile != 'identity':
        raise ValueError('Unknown declared price profile.')
    return w, CORE.ActionTable(rows, eta)


def expert_values(query, seen_moduli, seen_residues):
    a, n, m, r = (query[k] for k in ('a', 'n', 'm', 'r'))
    base = a % m
    shortcut = None
    if n == 0:
        shortcut = 1 % m
    elif base in (0, 1):
        shortcut = base
    elif base == m - 1:
        shortcut = base if n % 2 else 1
    return dict(zip(EXPERTS, (
        F(1, 2), F(seen_residues[m, r] + 1, seen_moduli[m] + m),
        F(1, 2) if shortcut is None else F(int(shortcut == r)),
        F(3, 4) if (a + n + r) % 2 else F(1, 4))))


def replay(public_tape, profile):
    """No source case, private receipt or original report is an input here."""
    scope = next(e['query']['scope'] for e in public_tape if e['kind'] == 'issue')
    pools = {method: CORE.DelayedPool(EXPERTS, scope=scope,
                                    decision_features=(method == METHODS[1])) for method in METHODS}
    cache, issued, forecasts, labels = {}, {}, {m: {} for m in METHODS}, {}
    seen_moduli, seen_residues = Counter(), Counter()
    operations = Counter()
    began = time.perf_counter_ns()
    for event in public_tape:
        if event['kind'] == 'issue':
            q = event['query']
            identity = q['query_id']
            ensure(identity not in issued and q['scope'] == scope, 'unique scoped issue')
            key = tuple(q[k] for k in ('scope', 'a', 'n', 'm'))
            known = key in cache
            qs = ({name: F(int(cache[key] == q['r'])) for name in EXPERTS} if known
                  else expert_values(q, seen_moduli, seen_residues))
            issued[identity] = (q, event)
            w, actions = price_inputs(event, profile)
            for method, pool in pools.items():
                prediction = None
                if known:
                    p = F(int(cache[key] == q['r']))
                    labels[identity] = int(p)
                else:
                    prediction = pool.issue(identity, qs, w, tolerance=F(1, 4096),
                        actions=actions if method == METHODS[1] else None)
                    p = prediction.probability
                    operations['score_evaluations'] += prediction.score_evaluations
                    operations['bisections'] += prediction.bisections
                costs = actions.forecast_costs(p)
                hard = int(costs[1] < costs[0])
                mix = F(hard) if known else actions.mix(p)
                forecasts[method][identity] = {
                    'probability': p, 'action_one_probability': mix,
                    'forecast_action_costs': costs, 'hard_action': hard,
                    'experts': qs, 'weight': w, 'actions': actions,
                    'known_at_issue': known, 'core_prediction': prediction,
                    'tick': event['tick']}
                operations['issue_calls'] += int(not known)
        elif event['kind'] == 'admit':
            identity = event['query_id']
            ensure(identity in issued and identity not in labels, 'admit only pending issued query')
            q, issue = issued[identity]
            ensure(event['scope'] == scope and type(event['answer']) is int
                   and event['answer'] in (0, 1), 'strict admitted label type and scope')
            ensure(event['event'] > issue['event'] and event['tick'] >= issue['tick'],
                   'admission follows issue')
            ensure(type(event['residue']) is int and 0 <= event['residue'] < q['m']
                   and event['answer'] == int(event['residue'] == q['r']),
                   'admitted residue and answer agree')
            key = tuple(q[k] for k in ('scope', 'a', 'n', 'm'))
            ensure(key not in cache or cache[key] == event['residue'], 'no admitted residue conflict')
            for pool in pools.values():
                pool.reveal(identity, event['answer'], scope=scope)
                operations['reveal_calls'] += 1
            labels[identity] = event['answer']
            cache[key] = event['residue']
            seen_moduli[q['m']] += 1
            seen_residues[q['m'], event['residue']] += 1
        else:
            raise ValueError('Unknown public event.')
    pending = sorted(set(issued) - set(labels))
    ensure(all(sorted(pool.pending) == pending for pool in pools.values()), 'pending partition')
    return {'profile': profile, 'forecasts': forecasts, 'labels': labels, 'pending_ids': pending,
            'audits': {method: pool.audit() for method, pool in pools.items()},
            'operations': dict(operations), 'elapsed_wall_ns': time.perf_counter_ns() - began}


def score(forecasts, labels, public_tape, profile, retain_issued_action):
    """Rescore fixed reports; optionally answer new actions from their old scalar."""
    inputs = {e['query']['query_id']: e for e in public_tape if e['kind'] == 'issue'}
    total, loss, mixed = F(0), F(0), F(0)
    expert_losses, fixed = [F(0)] * len(EXPERTS), [F(0), F(0)]
    residuals, masses = [F(0)] * 5, [F(0)] * 5
    for identity, y in labels.items():
        report = forecasts[identity]
        p = report['probability']
        w, actions = price_inputs(inputs[identity], profile)
        if retain_issued_action:
            s = report['action_one_probability']
        elif report['known_at_issue']:
            costs = actions.forecast_costs(p)
            s = F(int(costs[1] < costs[0]))
        else:
            s = actions.mix(p)
        total += w
        loss += w * (p - y) ** 2
        mixed += w * ((1 - s) * actions.rows[0][y] + s * actions.rows[1][y])
        for i in (0, 1):
            fixed[i] += w * actions.rows[i][y]
        for i, name in enumerate(EXPERTS):
            expert_losses[i] += w * (report['experts'][name] - y) ** 2
        for j in range(5):
            membership = max(F(0), 1 - abs(4 * p - j))
            masses[j] += w * membership
            residuals[j] += w * membership * (y - p)
    ensure(sum(masses) == total, 'rescored bin mass partition')
    return {'settled': len(labels), 'weight': total, 'brier': loss,
            'brier_per_weight': loss / total if total else None,
            'brier_regret_best_expert': loss - min(expert_losses),
            'expert_losses': expert_losses, 'mixed_loss': mixed,
            'fixed_action_losses': fixed, 'mixed_regret_best_fixed_action': mixed - min(fixed),
            'calibration_residuals': residuals, 'calibration_masses': masses}


def check_identity(case, result):
    for record in case['records']:
        identity = record['query']['query_id']
        for method in METHODS:
            original, current = record['reports'][method], result['forecasts'][method][identity]
            for key in ('probability', 'action_one_probability', 'forecast_action_costs', 'hard_action'):
                ensure(CORE.encoded(current[key]) == original[key], 'same-price report equality')
            ensure(CORE.encoded(current['experts']) == record['experts'], 'independent expert tape equality')
            if current['core_prediction'] is not None:
                ensure(CORE.encoded(current['core_prediction']) == original['detail']['core_prediction'],
                       'same-price complete numeric issue equality')
    for method in METHODS:
        ensure(CORE.encoded(result['audits'][method]) == case['core_audits'][method]['pool'],
               'same-price complete pool audit equality')
    ensure(result['pending_ids'] == sorted(case['pending_ids']), 'same-price unresolved set')


def analyze_case(case):
    before = digest(case)
    tape = public_projection(case)
    poisoned = deepcopy(case)
    for record in poisoned['records']:
        # None of these fields belongs to the replay's admissible input.
        record['reports'] = {'private_exact_baseline': 'redacted'}
        if record['status'] == 'pending':
            record['outcome'] = 'unavailable'
            record['receipt'] = {'private': 'redacted'}
    ensure(public_projection(poisoned) == tape, 'private pending and baseline noninterference')
    runs = {profile: replay(tape, profile) for profile in PROFILES}
    original = runs['identity']
    check_identity(case, original)
    summary = {}
    for profile, run in runs.items():
        ensure(run['labels'] == original['labels'], 'price change preserves admitted semantic answers')
        summary[profile] = {}
        for method in METHODS:
            old, new = original['forecasts'][method], run['forecasts'][method]
            changed = [identity for identity in old
                       if old[identity]['probability'] != new[identity]['probability']]
            keep = score(old, run['labels'], tape, profile, True)
            new_action = score(old, run['labels'], tape, profile, False)
            rerun = score(new, run['labels'], tape, profile, True)
            if profile == 'identity':
                ensure(keep == new_action == rerun, 'identity services agree')
                metric = case['metrics'][method]['all_admitted']
                ensure(str(rerun['brier']) == metric['task_weighted_brier']
                       and str(rerun['mixed_regret_best_fixed_action']) == metric['mixed_regret_best_fixed_action'],
                       'independent identity metric equality')
            audit = run['audits'][method]
            root = CORE.sqrt_upper(audit['bound_squared'])
            ensure(rerun['brier_regret_best_expert'] <= 2 * root, 'rerun own-weight Brier certificate')
            ensure(all(abs(e) <= root for e in rerun['calibration_residuals']),
                   'rerun own-weight calibration certificate')
            if method == METHODS[1]:
                ensure(rerun['mixed_regret_best_fixed_action'] <= audit['smoothing_slack'] + root,
                       'rerun own-price mixed-action certificate')
            summary[profile][method] = {
                'changed_probability_count': len(changed), 'first_changed_query': changed[0] if changed else None,
                'rescore_issued_scalar_and_issued_action': keep,
                'new_action_from_retained_scalar': new_action,
                'rerun_learner_and_action': rerun,
                'retained_report_original_brier_calibration_certificate_applicable': profile != 'changed_weights',
                'retained_action_original_cost_certificate_applicable': (profile == 'identity' and method == METHODS[1]),
                'rerun_uses_its_own_certificate': True,
                'rerun_certificate': run['audits'][method]}
    ensure(digest(case) == before, 'original case never mutated')
    return {'case': case['case'], 'public_tape': tape, 'public_tape_sha256': digest(tape),
            'summary': summary, 'replays': runs,
            'scope': 'Fixed query/admission schedule and price-independent expert policy; no acquisition-policy replay.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=SESSION / 'development/mathematical_queries_v1')
    parser.add_argument('--output', type=Path, default=SESSION / 'development/price_replay_v2')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest_path = args.input / 'manifest.json'
    source_manifest = json.loads(manifest_path.read_text())
    result = {'version': VERSION, 'status': 'running', 'python': platform.python_version(),
              'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (HERE, CORE_PATH)},
              'input_manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
              'profiles_declared_in_source': PROFILES, 'stage': 'development_not_frozen',
              'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'completed_cases': []}
    dump(args.output / 'manifest.json', result)
    started = time.perf_counter_ns()
    try:
        for name in source_manifest['completed_cases']:
            path = args.input / (name + '.json')
            ensure(hashlib.sha256(path.read_bytes()).hexdigest() == source_manifest['artifacts_sha256'][path.name],
                   'immutable input case hash')
            analyzed = analyze_case(json.loads(path.read_text()))
            dump(args.output / path.name, analyzed)
            result['completed_cases'].append(name)
            dump(args.output / 'manifest.json', result)
            print(json.dumps({'case': name, 'status': 'PASS', 'public_tape': analyzed['public_tape_sha256']}), flush=True)
        result.update(status='PASS', checks=dict(CHECKS), assertions=sum(CHECKS.values()),
                      elapsed_wall_ns=time.perf_counter_ns() - started)
        result['artifacts_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                     for p in sorted(args.output.iterdir()) if p.name != 'manifest.json'}
        dump(args.output / 'manifest.json', result)
    except BaseException as exc:
        result.update(status='FAIL', checks=dict(CHECKS), elapsed_wall_ns=time.perf_counter_ns() - started)
        dump(args.output / 'failure.json', {'type': type(exc).__name__, 'message': str(exc),
                                          'traceback': traceback.format_exc()})
        dump(args.output / 'manifest.json', result)
        raise


if __name__ == '__main__':
    main()
