#!/usr/bin/env python3
"""Finite recurrence evidence, controlled probes, and decision certificates.

Codex (GPT-6), November 10, 2026. Standard-library exact identities plus
NumPy simulations. No population ODE is simulated here. The controller sees
outcomes and declared mechanism parameters, never the environmental a.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import argparse
import json
from math import ceil, comb, log, sqrt
from pathlib import Path

import numpy as np


def boundary(v, alpha=.05, rho=1.):
    return np.sqrt((v + rho) * np.log((v + rho) / (rho * alpha * alpha)))


@dataclass
class Evidence:
    u: float = 0.
    v: float = 0.
    bias: float = 0.

    def corrected(self, z, e, b, mean_error=0.):
        self.u += float(np.sum(e * (z - (1 - e) * b)))
        self.v += int(np.size(z)) * e * e
        self.bias += int(np.size(z)) * e * mean_error

    def accepted(self, z, bias_bound=0.):
        self.u += float(np.sum(z))
        self.v += len(z)
        self.bias += len(z) * bias_bound

    def interval(self, alpha=.05, rho=1.):
        if not self.v:
            return -1., 1.
        radius = (float(boundary(self.v, alpha, rho)) + self.bias) / self.v
        lo = max(-1., self.u / self.v - radius)
        hi = min(1., self.u / self.v + radius)
        if lo > hi:
            raise ValueError('Empty confidence set: statistical/model alarm; do not fabricate a forecast.')
        return lo, hi


def decision(lo, hi, kappa):
    """Minimize worst-case regret among the coarse action and all fine b."""
    assert -1 <= lo <= hi <= 1 and kappa >= 0
    left, right = max(kappa, lo * lo), max(kappa, hi * hi)
    b = lo if hi == lo else min(hi, max(lo, (right - left) / (2 * (hi - lo))))
    fine = max(b * b - 2 * b * lo + left, b * b - 2 * b * hi + right)
    coarse = max(0., lo * lo - kappa, hi * hi - kappa)
    if coarse <= fine:
        return {'action': 'coarse', 'forecast': 0., 'regret_bound': coarse}
    return {'action': 'fine', 'forecast': b, 'regret_bound': fine}


def regret(a, selected, kappa):
    oracle = max(0., a * a - kappa)
    gain = 0. if selected['action'] == 'coarse' else 2 * a * selected['forecast'] - selected['forecast'] ** 2 - kappa
    return oracle - gain


def exact_checks():
    checks = 0
    for p, e, b in product((F(0), F(1, 5), F(1, 2), F(4, 5), F(1)),
                            (F(1, 10), F(1, 2), F(1)), (F(-1), F(0), F(1))):
        a = 2 * p - 1
        q = e * a + (1 - e) * b
        correction = sum((1 + z * q) / 2 * e * (z - (1 - e) * b) for z in (-1, 1))
        assert correction == e * e * a
        accepted = {z: sum(F(1, 2) * e * (1 + z * a) / 2 for action in (-1, 1)
                           if z != action) for z in (-1, 1)}
        assert sum(accepted.values()) == e / 2
        assert accepted[1] / sum(accepted.values()) == p
        checks += 1
    categorical = [F(1, 10), F(1, 5), F(7, 10)]
    e = F(1, 7)
    masses = [sum(F(1, 3) * e * p for a in range(3) if a != y)
              for y, p in enumerate(categorical)]
    assert masses == [e * F(2, 3) * p for p in categorical]
    # Outcome-dependent source exposure can bias the accepted law; the
    # construction requires a source share chosen before the fresh action.
    accepted_plus = F(1, 2) * F(3, 4) * F(1, 2)
    accepted_minus = F(1, 2) * F(1, 4) * F(1, 2)
    biased_mean = (accepted_plus - accepted_minus) / (accepted_plus + accepted_minus)
    assert biased_mean == F(1, 2)
    # Worst-case agent misfires, compared with the exact contamination cap.
    contamination_cases = 0
    for p, e, epsilon in product((F(0), F(1, 3), F(1)), (F(1, 10), F(1, 2)),
                                  (F(1, 100), F(1, 10))):
        for misfire_plus, misfire_minus in product((F(0), epsilon), repeat=2):
            env_plus, env_minus = e * p / 2, e * (1 - p) / 2
            bad_plus = (1 - e) * misfire_minus / 2
            bad_minus = (1 - e) * misfire_plus / 2
            mass = env_plus + env_minus + bad_plus + bad_minus
            observed_mean = (env_plus + bad_plus - env_minus - bad_minus) / mass
            cap = (1 - e) * epsilon / (e / 2 + (1 - e) * epsilon)
            assert abs(observed_mean - (2 * p - 1)) <= 2 * cap
            contamination_cases += 1
    return {'known_correction_and_exclusion_cases': checks,
            'categorical_accepted_masses': [str(x) for x in masses],
            'action_dependent_exposure_counterexample': {'true_mean': '0', 'accepted_mean': str(biased_mean)},
            'misfire_bias_cases': contamination_cases}


def information_checks():
    largest_error = 0.
    table = []
    for a, e in product((-.8, -.2, .0, .6), (.01, .1, .5, .9)):
        probs = np.array([e * (1 + a), e * (1 - a), 2 - e + e * a, 2 - e - e * a]) / 4
        da = np.array([e, -e, e, -e]) / 4
        de = np.array([1 + a, 1 - a, -1 + a, -1 - a]) / 4
        iaa, iae, iee = np.sum(da * da / probs), np.sum(da * de / probs), np.sum(de * de / probs)
        efficient = iaa - iae * iae / iee
        formula = e / ((1 - a * a) * (2 - e + e * a * a))
        accepted = e / (2 * (1 - a * a))
        largest_error = max(largest_error, abs(efficient - formula))
        assert abs(accepted / efficient - (1 - e * (1 - a * a) / 2)) < 1e-12
        if a == .6:
            table.append({'a': a, 'exposure': e,
                          'neutral_known_share_information': e * e / (1 - e * e * a * a),
                          'accepted_probe_information': accepted,
                          'full_probe_unknown_constant_share_information': efficient,
                          'accepted_fraction_of_full_information': accepted / efficient})
    assert largest_error < 1e-12
    # A deterministic radius target gives a transparent information-cost table.
    target = 1
    while boundary(target) / target > .1:
        target += 1
    costs = [{'exposure': e, 'known_neutral_raw_trials': ceil(target / (e * e)),
              'exclusion_expected_raw_trials': 2 * target / e,
              'observed_source_flag_expected_trials': target / e}
             for e in (.5, .2, .1, .05)]
    return {'fisher_cases': 16, 'maximum_formula_error': largest_error,
            'information_table': table, 'confidence_radius_target': .1,
            'intrinsic_evidence_target': target, 'radius_cost_table': costs}


def decision_checks():
    checked = 0
    grid = np.linspace(-1, 1, 81)
    for lo_index in range(0, 81, 8):
        for hi_index in range(lo_index, 81, 8):
            lo, hi = grid[lo_index], grid[hi_index]
            for kappa in (0., .01, .09, .5, 1.):
                chosen = decision(lo, hi, kappa)
                # Interior a can only improve the endpoint-based maximum.
                actual = max(regret(a, chosen, kappa) for a in np.linspace(lo, hi, 101))
                assert actual <= chosen['regret_bound'] + 1e-12
                candidates = [max(0., lo * lo - kappa, hi * hi - kappa)]
                for b in np.linspace(-1, 1, 1001):
                    candidates.append(max(b * b - 2 * b * lo + max(kappa, lo * lo),
                                          b * b - 2 * b * hi + max(kappa, hi * hi)))
                assert chosen['regret_bound'] <= min(candidates) + 1e-12
                checked += 1
    return checked


def worked_episode(seed=20261110):
    rng = np.random.default_rng(seed)
    a, kappa, horizon, block_cost = .6, .04, 100, .1
    evidence = Evidence()
    records = []
    total_outcomes = 0
    total_sum = 0
    for e, b, n in ((.2, .9, 5000), (.1, -.8, 5000)):
        z = 2 * (rng.random(n) < (1 + e * a + (1 - e) * b) / 2) - 1
        evidence.corrected(z, e, b)
        total_outcomes += n; total_sum += int(z.sum())
        lo, hi = evidence.interval()
        records.append({'stage': 'known_feedback', 'exposure': e, 'agent_mean': b,
                        'raw_outcomes': total_outcomes, 'u': evidence.u, 'v': evidence.v,
                        'naive_accumulated_mean': total_sum / total_outcomes,
                        'corrected_estimate': evidence.u / evidence.v, 'interval': [lo, hi],
                        'decision': decision(lo, hi, kappa)})
    initial_u, initial_v = evidence.u, evidence.v
    immediate_choice = decision(*evidence.interval(), kappa)
    immediate_regret = regret(a, immediate_choice, kappa)
    probe_outcomes = accepted_count = 0
    for block in range(1, 1001):
        # The inference code does not receive this varying source share.
        e = (.2, .1, .3)[(block - 1) % 3]
        action = 2 * rng.integers(0, 2, size=1000) - 1
        environmental = rng.random(1000) < e
        z_env = 2 * (rng.random(1000) < (1 + a) / 2) - 1
        observed = np.where(environmental, z_env, action)
        clean = observed[observed != action]
        evidence.accepted(clean)
        accepted_count += len(clean); probe_outcomes += len(observed)
        lo, hi = evidence.interval()
        chosen = decision(lo, hi, kappa)
        value_cap = horizon * chosen['regret_bound']
        if block in (1, 10, 50) or value_cap <= block_cost:
            records.append({'stage': 'unknown_share_probes', 'blocks': block,
                            'probe_outcomes': probe_outcomes, 'accepted_marks': accepted_count,
                            'u': evidence.u, 'v': evidence.v, 'interval': [lo, hi],
                            'decision': chosen, 'future_information_value_cap': value_cap,
                            'next_block_cost': block_cost})
        if value_cap <= block_cost:
            break
    else:
        raise AssertionError('Declared demonstration horizon exhausted without the stopping certificate')
    actual_regret = regret(a, chosen, kappa)
    covered = all(r['interval'][0] <= a <= r['interval'][1] for r in records)
    if covered:
        assert actual_regret <= chosen['regret_bound'] + 1e-12
    gain = a * a - kappa - actual_regret
    return {'seed': seed, 'environmental_parameter_for_scoring_only': a,
            'confidence_level_anytime': .95, 'rho': 1., 'fine_cost_per_future_use': kappa,
            'future_uses': horizon, 'probe_block_size': 1000, 'probe_block_cost': block_cost,
            'records': records, 'retained_initial_evidence': [initial_u, initial_v],
            'actual_final_regret_per_use': actual_regret, 'observed_coverage_at_recorded_stages': covered,
            'probe_cost_total': block * block_cost,
            'immediate_action_reference_gain': horizon * (a * a - kappa - immediate_regret),
            'reference_environment_future_gain_after_fine_cost': horizon * gain,
            'net_gain_after_probe_cost': horizon * gain - block * block_cost,
            'net_difference_from_immediate_action': horizon * (immediate_regret - actual_regret) - block * block_cost,
            'scope': 'Certificate-seeking path. Its cost can exceed the benefit of acting immediately; the upper bound is not a query authorization rule.'}


def bayes_batch_values(alpha, beta, horizon, kappa, clean_cost, maximum=500):
    """Exact beta-binomial predictive law and utility, with declared prior.

    alpha,beta are integer Beta parameters for p=(1+a)/2. The source share
    is irrelevant for the posterior; a declared lower share sets a conservative
    expected cost per accepted mark. This is ordinary Bayesian lookahead.
    """
    current_mean = F(alpha - beta, alpha + beta)
    current = max(F(0), current_mean ** 2 - kappa)
    rows = []
    for n in range(maximum + 1):
        expected = F(0)
        total = F(0)
        for successes in range(n + 1):
            probability = F(comb(successes + alpha - 1, successes)
                            * comb(n - successes + beta - 1, n - successes),
                            comb(n + alpha + beta - 1, n))
            posterior_mean = F(alpha - beta + 2 * successes - n, alpha + beta + n)
            total += probability
            expected += probability * max(F(0), posterior_mean ** 2 - kappa)
        assert total == 1
        net = horizon * (expected - current) - n * clean_cost
        rows.append((n, expected, net))
        # No future per-use gain can exceed one; this simple bound makes
        # the finite search complete once cost already exceeds horizon.
        if n * clean_cost > horizon:
            break
    best = max(rows, key=lambda x: (x[2], -x[0]))
    return best, rows


def bayes_episode(seed=20261111):
    # Same binary recurrence observations, a separately declared subjective
    # uniform prior, and a realistic intervention charge per raw probe.
    horizon, kappa, raw_cost, lower_share = F(100), F(1, 25), F(1, 100), F(1, 5)
    clean_cost = 2 * raw_cost / lower_share
    # A sharper complete-search ceiling uses the uniform prior's oracle gain.
    # E[(a^2-kappa)_+] = 1/3-kappa+(2/3) kappa^(3/2) = 112/375.
    oracle = F(112, 375)
    maximum = int(horizon * oracle / clean_cost) + 1
    best, rows = bayes_batch_values(1, 1, horizon, kappa, clean_cost, maximum)
    n = best[0]
    assert all(r[2] <= best[2] for r in rows)
    rng = np.random.default_rng(seed)
    a = .6
    marks, raw = [], 0
    while len(marks) < n:
        # Fixed e for a transparent expected-cost check; inference needs only
        # the accepted marks. The planning contract permits e >= lower_share.
        action = 2 * rng.integers(0, 2) - 1
        is_environment = rng.random() < float(lower_share)
        environmental = 1 if rng.random() < (1 + a) / 2 else -1
        z = environmental if is_environment else action
        raw += 1
        if z != action: marks.append(z)
    successes = sum(z == 1 for z in marks)
    aa, bb = 1 + successes, 1 + n - successes
    posterior_mean = F(aa - bb, aa + bb)
    action = 'fine' if posterior_mean ** 2 > kappa else 'coarse'
    chosen = {'action': action, 'forecast': float(posterior_mean) if action == 'fine' else 0.}
    actual = max(0., a * a - float(kappa)) - regret(a, chosen, float(kappa))
    # The same finite lookahead is revisited after the selected batch.
    second_moment = posterior_mean ** 2 + F(4 * aa * bb, (aa + bb) ** 2 * (aa + bb + 1))
    present_value = max(F(0), posterior_mean ** 2 - kappa)
    follow_cap = int(horizon * (second_moment - present_value) / clean_cost) + 1
    follow_best, _ = bayes_batch_values(aa, bb, horizon, kappa, clean_cost, maximum=follow_cap)
    return {'seed': seed, 'prior': 'p=(1+a)/2 ~ Beta(1,1)',
            'future_uses': int(horizon), 'fine_cost_per_use': str(kappa),
            'raw_probe_cost': str(raw_cost), 'assumed_lower_environment_share': str(lower_share),
            'conservative_expected_cost_per_accepted_mark': str(clean_cost),
            'perfect_information_gain_per_use': str(oracle),
            'complete_batch_search_n_max': maximum, 'selected_clean_batch_size': n,
            'prior_expected_net_gain': float(best[2]),
            'prior_expected_terminal_value_per_use': float(best[1]),
            'selected_batch_expected_cost_bound': float(n * clean_cost),
            'realized_raw_probes': raw, 'realized_success_marks': successes,
            'posterior_parameters': [aa, bb], 'posterior_mean_a': float(posterior_mean),
            'decision': chosen, 'actual_reference_gain_after_probe_cost': horizon * actual - raw * float(raw_cost),
            'complete_additional_batch_search_max': follow_cap,
            'best_additional_batch': follow_best[0],
            'best_additional_expected_net_gain': float(follow_best[2]),
            'scope': 'Exact one-batch Bayesian comparison under an explicit prior and cost model, not a prior-free optimal adaptive policy.'}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path); args = p.parse_args()
    result = {'author': 'Codex (GPT-6)', 'status': 'passed',
              'exact_identities': exact_checks(), 'information': information_checks(),
              'regret_grid_cases': decision_checks(), 'worked_episode': worked_episode(),
              'cost_aware_bayesian_episode': bayes_episode()}
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output: args.output.write_text(encoded, encoding='utf-8', newline='\n')
    print(encoded)


if __name__ == '__main__': main()
