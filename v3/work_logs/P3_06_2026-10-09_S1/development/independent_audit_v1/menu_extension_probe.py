"""Independent exact-rational CF-7 finite-menu extension probe.

This implements a separate multi-profile feature experiment. The principal
production module has one profile. Every output here is development evidence.
Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation reviewer.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import time
import traceback


def norm(xs):
    return sum((x * x for x in xs), F(0))


class Checks:
    def __init__(self):
        self.count = 0
        self.groups = {}

    def require(self, condition, group, **context):
        self.count += 1
        self.groups[group] = self.groups.get(group, 0) + 1
        if not condition:
            raise AssertionError(json.dumps({'group': group, **context}, default=str))


def issue(residual, weights, qs, alphas, betas, bins, tolerance, max_bisections):
    """Solve the single score formed from concatenated profile blocks."""
    def evaluate(p):
        tents = tuple(max(F(0), 1 - abs(bins * p - j)) for j in range(bins + 1))
        phi = tuple(value for w, alpha, beta in zip(weights, alphas, betas)
                    for value in tuple(w * alpha * (q - p) for q in qs)
                    + tuple(w * beta * b for b in tents))
        score = sum((r * v for r, v in zip(residual, phi)), F(0))
        score += (1 - 2 * p) * norm(phi) / 2
        return score, phi

    score, phi = evaluate(F(0))
    calls = 1
    steps = 0
    if score <= 0:
        p = F(0)
        accepted = True
    else:
        score, phi = evaluate(F(1))
        calls += 1
        if score >= 0:
            p = F(1)
            accepted = True
        else:
            lo, hi = F(0), F(1)
            p = (lo + hi) / 2
            score, phi = evaluate(p)
            calls += 1
            while abs(score) > tolerance and steps < max_bisections:
                if score > 0:
                    lo = p
                else:
                    hi = p
                p = (lo + hi) / 2
                score, phi = evaluate(p)
                calls += 1
                steps += 1
            accepted = abs(score) <= tolerance
    allowance = max(F(0), 2 * (1 - p) * score, -2 * p * score)
    return {'p': p, 'features': phi, 'score': score, 'allowance': allowance,
            'root_condition_met': accepted, 'bisections': steps, 'score_evaluations': calls}


def episode(outcomes, profiles, alphas, betas, bins, checks, max_bisections=14,
            names=('zero', 'one', 'past')):
    n = len(names)
    block = n + bins + 1
    residual = [F(0)] * (profiles * block)
    variance = allowance = F(0)
    profile_own = [F(0)] * profiles
    profile_expert = [[F(0)] * n for _ in range(profiles)]
    profile_distances = [[F(0)] * n for _ in range(profiles)]
    profile_calibration = [[F(0)] * (bins + 1) for _ in range(profiles)]
    trace = []
    for t, y in enumerate(outcomes):
        # Only the previous outcome slice enters the next expert computation.
        qs = (F(0), F(1), F(sum(outcomes[:t]) + 1, t + 2))[:n]
        weights = tuple(F(w) for w in profiles.weights_at(t))
        checks.require(len(weights) == len(alphas) and all(w >= 0 for w in weights),
                       'announced_nonnegative_profiles')
        pred = issue(residual, weights, qs, alphas, betas, bins, F(1, 257), max_bisections)
        p, phi = pred['p'], pred['features']
        changes = []
        for possible in (0, 1):
            next_r = [r + (possible - p) * f for r, f in zip(residual, phi)]
            delta = norm(next_r) - norm(residual) - p * (1 - p) * norm(phi)
            checks.require(delta <= pred['allowance'], 'both_outcomes_potential', round=t)
            changes.append(delta)
        checks.require(pred['allowance'] == max(changes), 'exact_allowance')
        residual = [r + (y - p) * f for r, f in zip(residual, phi)]
        variance += p * (1 - p) * norm(phi)
        allowance += pred['allowance']
        for r, w in enumerate(weights):
            profile_own[r] += w * (p - y) ** 2
            for i, q in enumerate(qs):
                profile_expert[r][i] += w * (q - y) ** 2
                profile_distances[r][i] += w * (q - p) ** 2
            for j in range(bins + 1):
                profile_calibration[r][j] += w * max(F(0), 1 - abs(bins * p - j)) * (y - p)
        trace.append({'round': t, 'p': p, 'y': y, 'weights': weights, 'experts': qs,
                      'score': pred['score'], 'allowance': pred['allowance'],
                      'root_condition_met': pred['root_condition_met'],
                      'bisections': pred['bisections'], 'score_evaluations': pred['score_evaluations']})
    bound = variance + allowance
    checks.require(norm(residual) <= bound, 'cumulative_potential')
    for r in range(profiles):
        for i in range(n):
            regret = profile_own[r] - profile_expert[r][i]
            checks.require(regret == 2 * residual[r * block + i] / alphas[r] - profile_distances[r][i],
                           'profile_regret_identity', profile=r, expert=i)
        for j in range(bins + 1):
            checks.require(profile_calibration[r][j] == residual[r * block + n + j] / betas[r],
                           'profile_calibration_identity', profile=r, bin=j)
    return {'trace': trace, 'residual': residual, 'variance': variance, 'allowance': allowance,
            'bound_squared': bound, 'profile_own_losses': profile_own,
            'profile_expert_losses': profile_expert, 'profile_distances': profile_distances,
            'profile_bin_residuals': profile_calibration,
            'alphas': alphas, 'betas': betas, 'bins': bins}


class MenuSize(int):
    """A fixed finite profile count with an announced deterministic schedule."""
    def weights_at(self, t):
        return (F(1), F(t % 2 == 0), F((t % 3) + 1, 2))[:int(self)]


class FirstRoundMenu(MenuSize):
    def weights_at(self, t):
        return (F(1), F(t == 0))


def mixture_check(data, coefficients, checks, require_nonnegative_coefficients=True):
    if require_nonnegative_coefficients:
        checks.require(all(value >= 0 for value in coefficients), 'nonnegative_coefficients')
    actual_weights = [sum((a * w for a, w in zip(coefficients, row['weights'])), F(0))
                      for row in data['trace']]
    own_from_summaries = sum((a * value for a, value in zip(coefficients, data['profile_own_losses'])), F(0))
    direct_own = sum((w * (row['p'] - row['y']) ** 2
                      for w, row in zip(actual_weights, data['trace'])), F(0))
    checks.require(own_from_summaries == direct_own, 'summary_vs_tape_own_loss')
    ca1 = sum((a / scale for a, scale in zip(coefficients, data['alphas'])), F(0))
    cb1 = sum((a / scale for a, scale in zip(coefficients, data['betas'])), F(0))
    ca2 = sum(((a / scale) ** 2 for a, scale in zip(coefficients, data['alphas'])), F(0))
    cb2 = sum(((a / scale) ** 2 for a, scale in zip(coefficients, data['betas'])), F(0))
    regrets = []
    calibrations = []
    for i in range(len(data['profile_expert_losses'][0])):
        expert_summary = sum((a * row[i] for a, row in zip(coefficients, data['profile_expert_losses'])), F(0))
        expert_tape = sum((w * (row['experts'][i] - row['y']) ** 2
                           for w, row in zip(actual_weights, data['trace'])), F(0))
        regret = direct_own - expert_tape
        regrets.append(regret)
        checks.require(expert_summary == expert_tape, 'summary_vs_tape_expert_loss')
        if all(w >= 0 for w in actual_weights):
            checks.require(regret <= 0 or regret * regret <= 4 * data['bound_squared'] * ca2,
                           'sharper_l2_regret')
            if require_nonnegative_coefficients:
                checks.require(regret <= 0 or regret * regret <= 4 * data['bound_squared'] * ca1 * ca1,
                               'stated_l1_regret')
    for j in range(data['bins'] + 1):
        cal_summary = sum((a * row[j] for a, row in zip(coefficients, data['profile_bin_residuals'])), F(0))
        cal_tape = sum((w * max(F(0), 1 - abs(data['bins'] * row['p'] - j)) * (row['y'] - row['p'])
                       for w, row in zip(actual_weights, data['trace'])), F(0))
        calibrations.append(cal_tape)
        checks.require(cal_summary == cal_tape, 'summary_vs_tape_bin_residual')
        checks.require(cal_tape * cal_tape <= data['bound_squared'] * cb2,
                       'sharper_l2_calibration')
        if require_nonnegative_coefficients:
            checks.require(cal_tape * cal_tape <= data['bound_squared'] * cb1 * cb1,
                           'stated_l1_calibration')
    return {'coefficients': coefficients, 'new_weights': actual_weights,
            'own_loss': direct_own, 'regrets': regrets, 'bin_residuals': calibrations,
            'coefficient_alpha_l1': ca1, 'coefficient_beta_l1': cb1,
            'coefficient_alpha_l2_squared': ca2, 'coefficient_beta_l2_squared': cb2}


def run():
    checks = Checks()
    episodes = []
    mixtures = 0
    for profile_count in (2, 3):
        menu = MenuSize(profile_count)
        alphas = (F(1), F(2), F(1, 2))[:profile_count]
        betas = (F(1), F(1, 2), F(2))[:profile_count]
        for outcomes in product((0, 1), repeat=5):
            data = episode(outcomes, menu, alphas, betas, 3, checks,
                           max_bisections=0 if outcomes[0] else 14)
            for coefficients in product((F(0), F(1, 2), F(1), F(2)), repeat=profile_count):
                mixture_check(data, coefficients, checks)
                mixtures += 1
            # Deliberately select a profile combination after seeing its regret.
            adaptive = tuple(F(2) if data['profile_own_losses'][r] > data['profile_expert_losses'][r][0]
                             else F(0) for r in range(profile_count))
            retrospective = mixture_check(data, adaptive, checks)
            mixtures += 1
            episodes.append({'profile_count': profile_count, 'outcomes': outcomes,
                             'result': data, 'retrospectively_selected_mixture': retrospective})

    # Equal original score (even equal unweighted calibration summaries) does
    # not identify new per-round prices. These are tapes, not algorithm traces.
    tape_a = ({'p': F(1), 'y': 0}, {'p': F(0), 'y': 0})
    tape_b = ({'p': F(0), 'y': 0}, {'p': F(1), 'y': 0})
    old = [sum((row['p'] - row['y']) ** 2 for row in tape) for tape in (tape_a, tape_b)]
    new = [sum(w * (row['p'] - row['y']) ** 2 for w, row in zip((F(2), F(0)), tape))
           for tape in (tape_a, tape_b)]
    checks.require(old[0] == old[1] and new[0] != new[1], 'old_score_nonidentification')

    # A signed coefficient need not produce negative weights. Naively replacing
    # nonnegative coefficients by signed ones in the l1 factor is invalid, while
    # the coefficient-norm bound remains valid for this nonnegative resulting tape.
    signed_data = episode((0, 0), FirstRoundMenu(2), (F(1), F(1)), (F(1), F(1)), 2, checks,
                          max_bisections=16, names=('zero', 'one'))
    signed = mixture_check(signed_data, (F(1), F(-1)), checks, False)
    checks.require(signed['new_weights'] == [F(0), F(1)], 'signed_coefficients_nonnegative_weights')
    checks.require(signed['coefficient_alpha_l1'] == 0 and signed['regrets'][0] > 0,
                   'naive_signed_l1_regret_obstruction')
    checks.require(signed['coefficient_beta_l1'] == 0 and any(signed['bin_residuals']),
                   'naive_signed_l1_calibration_obstruction')

    # If the resulting prices themselves are negative, good original performance
    # can turn into large positive regret. The distance term changes sign.
    negative_data = episode((0,) * 64, FirstRoundMenu(2), (F(1), F(1)), (F(1), F(1)), 2, checks,
                            max_bisections=20, names=('zero', 'one'))
    negative = mixture_check(negative_data, (F(-1), F(0)), checks, False)
    one_regret = negative['regrets'][1]
    checks.require(one_regret > 0 and one_regret ** 2 > 4 * negative_data['bound_squared'],
                   'negative_weight_regret_obstruction')

    return {'status': 'PASS', 'checks': checks.count, 'checks_by_group': checks.groups,
            'binary_sequence_episodes': len(episodes), 'mixture_evaluations': mixtures,
            'episodes': episodes,
            'old_score_nonidentification': {'tapes': [tape_a, tape_b], 'old_unit_weight_scores': old,
                                          'new_weights': (2, 0), 'new_scores': new,
                                          'scope': 'Information obstruction, not algorithm-produced traces.'},
            'signed_coefficients': {'episode': signed_data, 'mixture': signed,
                'interpretation': 'Signed-l1 substitution fails; l2 bound holds because new weights remain nonnegative.'},
            'negative_resulting_weights': {'episode': negative_data, 'mixture': negative,
                'interpretation': 'Nonnegative resulting weights are needed for the one-sided regret deduction.'}}


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    target = here / 'menu_extension_result.json'
    if target.exists():
        raise SystemExit('Refusing to overwrite an existing menu-extension result.')
    start = time.monotonic_ns()
    start_utc = datetime.now(timezone.utc).isoformat()
    try:
        result = run()
    except Exception:
        result = {'status': 'FAIL', 'traceback': traceback.format_exc()}
    result.update({'schema': 'value_logic.p306.independent_menu_extension_result.v1',
                   'start_utc': start_utc, 'end_utc': datetime.now(timezone.utc).isoformat(),
                   'execution_ns': time.monotonic_ns() - start, 'python': platform.python_version(),
                   'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'theorem_snapshot_sha256': hashlib.sha256((here / 'menu_extension_theorem_snapshot.md').read_bytes()).hexdigest(),
                   'contributor': 'ChatGPT (GPT-6 Astra Pro), independent implementation reviewer',
                   'research_time_credit_ns': 0,
                   'scope': 'Separate finite-menu extension implementation; development only; main module uses one profile.'})
    target.write_text(json.dumps(result, indent=2, default=str) + '\n')
    print(json.dumps({'status': result['status'], 'checks': result.get('checks'),
                      'execution_ns': result['execution_ns'], 'result': str(target)}))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
