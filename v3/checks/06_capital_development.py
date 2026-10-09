"""Bounded P3-06 comparison of the ordinary capital-sum construction.

Contributor: ChatGPT (GPT-6 Astra Pro), October 9, 2026 UTC.
Reuses only the first 32 issue ticks of each already recorded public tape.
No new mathematical population, final controls, tuning loop or freeze.
"""
from __future__ import annotations

import argparse
from collections import Counter
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
SESSION = ROOT / 'v3/work_logs/P3_06_2026-10-09_S1'
CAPITAL_PATH = HERE.with_name('06_capital_forecasting.py')
REPLAY_PATH = HERE.with_name('06_price_replay.py')


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = result
    spec.loader.exec_module(result)
    return result


CAPITAL = module('p306_capital_development_core', CAPITAL_PATH)
REPLAY = module('p306_capital_development_replay', REPLAY_PATH)
BASE = CAPITAL.BASE
VERSION = 'p306-capital-development-v1'
HORIZON = 32
MAX_WEIGHT = {'recurring_shortcuts': 1, 'balanced_nonshortcut_null': 1,
              'delayed_pending_tail': 8, 'varying_stakes_actions': 8}
MAX_SLOPE = 6
CHECKS = Counter()


def ensure(condition, name):
    CHECKS[name] += 1
    if not condition:
        raise AssertionError(name)


def dump(path, value):
    path.write_text(json.dumps(BASE.encoded(value), sort_keys=True, indent=2) + '\n')


def score(predictions, labels, inputs):
    loss, mixed, weight = F(0), F(0), F(0)
    fixed, experts, residuals, masses = [F(0)] * 2, [F(0)] * 4, [F(0)] * 5, [F(0)] * 5
    for identity, y in labels.items():
        report, entry = predictions[identity], inputs[identity]
        p, s, w = report['probability'], report['action_one_probability'], F(entry['weight'])
        rows = tuple(tuple(F(x) for x in row) for row in entry['actions']['rows'])
        weight += w
        loss += w * (p - y) ** 2
        mixed += w * ((1 - s) * rows[0][y] + s * rows[1][y])
        for i in (0, 1):
            fixed[i] += w * rows[i][y]
        for i, expert in enumerate(REPLAY.EXPERTS):
            experts[i] += w * (report['experts'][expert] - y) ** 2
        for j in range(5):
            b = max(F(0), 1 - abs(4 * p - j))
            masses[j] += w * b
            residuals[j] += w * b * (y - p)
    ensure(sum(masses) == weight, 'same-cutoff bin mass')
    return {'settled': len(labels), 'weight': weight, 'brier': loss,
            'brier_per_weight': loss / weight if weight else None,
            'expert_losses': experts, 'brier_regret_best_expert': loss - min(experts),
            'mixed_action_loss': mixed, 'fixed_action_losses': fixed,
            'mixed_regret_best_fixed_action': mixed - min(fixed),
            'calibration_residuals': residuals, 'calibration_masses': masses}


def run_case(case):
    name = case['case']
    tape = [event for event in REPLAY.public_projection(case) if event['tick'] <= HORIZON]
    scope = tape[0]['query']['scope']
    inputs, outputs, labels, pending, copies, cache = {}, {}, {}, {}, [], {}
    counts, moduli, residues = Counter(), Counter(), Counter()
    for event in tape:
        if event['kind'] == 'issue':
            query = event['query']
            identity = query['query_id']
            inputs[identity] = event
            key = tuple(query[k] for k in ('scope', 'a', 'n', 'm'))
            if key in cache:
                p = F(int(cache[key] == query['r']))
                labels[identity] = int(p)
                qs = {name: p for name in REPLAY.EXPERTS}
                actions = BASE.ActionTable(event['actions']['rows'], event['actions']['eta'])
                costs = actions.forecast_costs(p)
                outputs[identity] = {'probability': p, 'action_one_probability': F(int(costs[1] < costs[0])),
                    'experts': qs, 'known_at_issue': True, 'prediction': None}
                counts['cache_hits'] += 1
                continue
            qs = REPLAY.expert_values(query, moduli, residues)
            free = next((i for i, learner in enumerate(copies) if learner.pending is None), None)
            if free is None:
                free = len(copies)
                copies.append(CAPITAL.CapitalForecaster(REPLAY.EXPERTS, HORIZON,
                    max_weight=MAX_WEIGHT[name], max_slope_range=MAX_SLOPE, scope=scope))
            started = time.perf_counter_ns()
            pred = copies[free].issue(identity, qs, event['weight'],
                                      rows=event['actions']['rows'], eta=event['actions']['eta'])
            counts['issue_wall_ns'] += time.perf_counter_ns() - started
            outputs[identity] = {'probability': pred.probability,
                'action_one_probability': pred.action_one_probability, 'experts': qs,
                'known_at_issue': False, 'prediction': pred, 'copy': free}
            pending[identity] = free
            counts['issue_calls'] += 1
            counts['capital_evaluations'] += pred.capital_evaluations
            counts['exp_enclosure_calls'] += pred.capital_evaluations * len(copies[free].priors)
            counts['bisections_at_accepted_candidate'] += pred.bisections
            counts['allowance_misses'] += int(not pred.allowance_met)
            counts['max_enclosure_bits'] = max(counts['max_enclosure_bits'], pred.max_enclosure_bits)
        elif event['kind'] == 'admit':
            identity = event['query_id']
            ensure(identity in pending, 'admission is issued and outstanding')
            copy = copies[pending[identity]]
            started = time.perf_counter_ns()
            copy.reveal(identity, event['answer'], scope=event['scope'])
            counts['reveal_wall_ns'] += time.perf_counter_ns() - started
            counts['reveal_calls'] += 1
            labels[identity] = event['answer']
            del pending[identity]
            query = inputs[identity]['query']
            key = tuple(query[k] for k in ('scope', 'a', 'n', 'm'))
            cache[key] = event['residue']
            moduli[query['m']] += 1
            residues[query['m'], event['residue']] += 1
    ensure(len(outputs) == HORIZON, 'announced prefix length')
    audits = [learner.audit() for learner in copies]
    used = [a for a in audits if a['state']['weight'] > 0]
    cert = {'expert_regret_upper': sum((a['expert_regret_upper'] for a in used), F(0)),
            'calibration_absolute_upper': [sum((a['calibration_absolute_upper'][j] for a in used), F(0))
                                           for j in range(5)],
            'mixed_action_regret_upper': [sum((a['mixed_action_regret_upper'][i] for a in used), F(0))
                                          for i in (0, 1)],
            'capital_allowance': sum((a['capital_allowance'] for a in used), F(0)),
            'copies_with_positive_settled_weight': len(used)}
    metrics = {'ordinary_capital_sum': score(outputs, labels, inputs)}
    original_by_id = {r['query']['query_id']: r for r in case['records']}
    for method in ('scalar_without_decision', 'scalar_with_decision',
                   'ordinary_brier_aa_binary64', 'ordinary_fast_exact'):
        original = {}
        for identity in outputs:
            record = original_by_id[identity]
            ensure(BASE.encoded(outputs[identity]['experts']) == record['experts'],
                   'same admitted expert policy')
            report = record['reports'][method]
            original[identity] = {'probability': F(report['probability']),
                'action_one_probability': F(report['action_one_probability']),
                'experts': {name: F(value) for name, value in record['experts'].items()}}
        metrics[method] = score(original, labels, inputs)
    own = metrics['ordinary_capital_sum']
    ensure(own['brier_regret_best_expert'] <= cert['expert_regret_upper'], 'aggregate Brier certificate')
    ensure(all(abs(value) <= bound for value, bound in
               zip(own['calibration_residuals'], cert['calibration_absolute_upper'])),
           'aggregate calibration certificates')
    ensure(all(own['mixed_action_loss'] - own['fixed_action_losses'][i] <= cert['mixed_action_regret_upper'][i]
               for i in (0, 1)), 'aggregate action certificates')
    ensure(set(labels).isdisjoint(pending) and set(labels) | set(pending) == set(outputs),
           'settled and pending partition')
    return {'case': name, 'horizon': HORIZON, 'max_weight': MAX_WEIGHT[name], 'max_slope_range': MAX_SLOPE,
            'public_tape': tape, 'public_tape_sha256': REPLAY.digest(tape), 'reports': outputs,
            'admitted_labels': labels, 'pending_ids': sorted(pending), 'copy_audits': audits,
            'certificate': cert, 'metrics': metrics, 'counts': dict(counts),
            'comparison_scope': 'Recorded methods rescored on this exact admission cutoff, not all eventually resolved prefix queries.',
            'resource_scope': 'Capital enclosure/issue/reveal work recorded; shared experts and original arithmetic production/checking remain separately charged by the source harness.'}


def report(results):
    lines = ['# Ordinary capital-sum development comparison', '',
        'Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.', '',
        'This separately versioned ordinary benchmark instantiates the nonnegative forecast-continuous',
        'supermartingale method in [Vovk (2007), §§2–3](https://arxiv.org/pdf/0708.1503).',
        'Expert, signed tent and centered smooth-action components share one scalar report.',
        'The exponential and logarithmic calculations use outward exact rational enclosures.',
        'The source module records a capital allowance, which is different from the K29 squared-potential allowance.', '',
        'The declared comparison reuses the first 32 issue ticks of each existing development tape.',
        'It fixes the horizon, stake/slope envelopes, equal prior budgets, rational rate rule and numerical caps',
        'before this run. Every method is scored only on the labels admitted by the same tick-32 cutoff.',
        'Pending answers, including ones admitted later in the original full run, remain unscored here.',
        'This later development comparison is not a final prospective evaluation or a priority claim.', '',
        '| Case / method | Settled / pending | Brier per weight | Brier regret | Mixed-action regret |',
        '|---|---:|---:|---:|---:|']
    for result in results:
        for method, values in result['metrics'].items():
            lines.append(f"| {result['case']} / {method} | {values['settled']} / {len(result['pending_ids'])} | "
                         f"{float(values['brier_per_weight']):.6f} | {float(values['brier_regret_best_expert']):.6f} | "
                         f"{float(values['mixed_regret_best_fixed_action']):.6f} |")
    lines += ['', 'The matched ordinary K29 copies remain identical to their scalar counterparts and are omitted here.',
        'Exact solver work and the binary64 AA remain available ordinary comparisons. No external authentication,',
        'hard resource bound, unbounded-stake constant regret or guarantee for sampled hard actions is claimed.',
        'The capital construction has its own finite-horizon calibration/action constants. More copies add their',
        'individual constant expert-regret bounds; no free delayed-feedback theorem is assumed.',
        'Complete exact certificates, per-copy states, intervals, prior masses and rate choices are in the JSON files.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=SESSION / 'development/mathematical_queries_v1')
    parser.add_argument('--output', type=Path, default=SESSION / 'development/capital_comparison_v1')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    source_manifest_path = args.input / 'manifest.json'
    source_manifest = json.loads(source_manifest_path.read_text())
    result = {'version': VERSION, 'core_version': CAPITAL.VERSION, 'status': 'running',
              'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (HERE, CAPITAL_PATH, REPLAY_PATH, CAPITAL.BASE_PATH)},
              'input_manifest_sha256': hashlib.sha256(source_manifest_path.read_bytes()).hexdigest(),
              'declared_horizon': HORIZON, 'max_weight': MAX_WEIGHT, 'max_slope_range': MAX_SLOPE,
              'python': platform.python_version(), 'stage': 'development_not_frozen',
              'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'completed_cases': []}
    dump(args.output / 'manifest.json', result)
    began, results = time.perf_counter_ns(), []
    try:
        for name in source_manifest['completed_cases']:
            path = args.input / (name + '.json')
            ensure(hashlib.sha256(path.read_bytes()).hexdigest() == source_manifest['artifacts_sha256'][path.name],
                   'source case hash')
            analyzed = run_case(json.loads(path.read_text()))
            results.append(analyzed)
            dump(args.output / path.name, analyzed)
            result['completed_cases'].append(name)
            dump(args.output / 'manifest.json', result)
            print(json.dumps({'case': name, 'status': 'PASS', 'pending': len(analyzed['pending_ids']),
                              'capital_allowance_misses': analyzed['counts'].get('allowance_misses', 0)}), flush=True)
        (args.output / 'REPORT.md').write_text(report(results))
        result.update(status='PASS', elapsed_wall_ns=time.perf_counter_ns() - began,
                      checks=dict(CHECKS), assertions=sum(CHECKS.values()))
        result['artifacts_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                     for p in sorted(args.output.iterdir()) if p.name != 'manifest.json'}
        dump(args.output / 'manifest.json', result)
    except BaseException as exc:
        result.update(status='FAIL', elapsed_wall_ns=time.perf_counter_ns() - began, checks=dict(CHECKS))
        dump(args.output / 'failure.json', {'type': type(exc).__name__, 'message': str(exc),
                                          'traceback': traceback.format_exc()})
        dump(args.output / 'manifest.json', result)
        raise


if __name__ == '__main__':
    main()
