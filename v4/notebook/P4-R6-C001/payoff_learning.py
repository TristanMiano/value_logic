"""Learn judgments from actual trades; Codex (GPT-6), November 12, 2026.

Compare ordinary Exp3 with a conditional-frequency learner that exploits the
same observed payoff structure. Outcomes from declined trades are never given
to either update. Experiment declared in explore.md before execution.
"""
import json
import math
from pathlib import Path

import numpy as np

HORIZON = 131072
PREFIXES = (32768, HORIZON)
REPETITIONS = 16
PRIORS = np.array([[0.8, 0.1, 0.1], [0.1, 0.8, 0.1], [0.1, 0.1, 0.8], [1/3]*3])
MASTER_SEED = 60501


def main():
    rng = np.random.default_rng(MASTER_SEED)
    n = REPETITIONS*len(PRIORS)
    prior = np.tile(PRIORS, (REPETITIONS, 1))
    positive_world = np.repeat(np.arange(REPETITIONS) % 2 == 0, len(PRIORS))
    correct_arm = np.where(positive_world, 0, 2)
    truth = np.where(positive_world[:, None], np.array([0.2, 0.8]), np.array([0.8, 0.2]))
    bank = np.array([[0.2, 0.8], [0.5, 0.5], [0.8, 0.2]])
    gamma = np.minimum(1.0, np.sqrt(3*np.log(1/prior.min(axis=1))/((math.e-1)*HORIZON)))
    log_weight = np.log(prior)
    success_count = 2*(prior @ bank)
    total_count = np.full((n, 2), 2.0)
    payoff_sum = np.zeros((2, n))
    regret_sum = np.zeros((2, n))
    observations = np.zeros((2, n), dtype=np.int64)
    correct_sum = np.zeros(n, dtype=np.int64)
    recent_correct = np.zeros((4096, n), dtype=np.int8)
    rows = []
    indices = np.arange(n)
    for time in range(1, HORIZON+1):
        # Environment draws are independent of current actions. Hidden truth and
        # unbought outcomes are used here, never in either learner's update.
        randoms = rng.random((n, 4))
        x = (randoms[:, 0] >= 0.5).astype(int)
        price = randoms[:, 1]
        true_p = truth[indices, x]
        outcome = (randoms[:, 2] < true_p).astype(float)

        weight = np.exp(log_weight-log_weight.max(axis=1, keepdims=True))
        distribution = (1-gamma[:, None])*weight/weight.sum(axis=1, keepdims=True)+gamma[:, None]/3
        arm = (randoms[:, 3, None] > np.cumsum(distribution, axis=1)).sum(axis=1)
        q_exp = bank[arm, x]
        q_freq = np.clip(success_count[indices, x]/total_count[indices, x], 0.1, 0.9)
        bought = np.array([price < q_exp, price < q_freq])
        payoff = bought*(outcome-price)

        # Exp3 receives only the selected judge's realized trade return.
        normalized = (payoff[0]+1)/2
        log_weight[indices, arm] += gamma/3*normalized/distribution[indices, arm]
        log_weight -= log_weight.max(axis=1, keepdims=True)

        # Structured learner receives a decoded label only when it bought.
        selected = np.flatnonzero(bought[1])
        decoded = payoff[1, selected]+price[selected]
        assert np.all(np.abs(decoded-np.rint(decoded)) < 1e-12)
        success_count[selected, x[selected]] += decoded
        total_count[selected, x[selected]] += 1

        payoff_sum += payoff
        regret_sum += np.array([(q_exp-true_p)**2/2, (q_freq-true_p)**2/2])
        observations += bought
        correct = arm == correct_arm
        correct_sum += correct
        recent_correct[(time-1) % 4096] = correct
        if time in PREFIXES:
            weight = np.exp(log_weight-log_weight.max(axis=1, keepdims=True))
            final_distribution = ((1-gamma[:, None])*weight/weight.sum(axis=1, keepdims=True)
                                  +gamma[:, None]/3)
            model_mse = ((bank[None, :, :]-truth[:, None, :])**2).mean(axis=2)
            final_mse_exp = (final_distribution*model_mse).sum(axis=1)
            final_mse_freq = ((np.clip(success_count/total_count, 0.1, 0.9)-truth)**2).mean(axis=1)
            for case in range(n):
                for method in (0, 1):
                    row = {'repetition': case//len(PRIORS), 'prior_id': case % len(PRIORS),
                           'positive_world': bool(positive_world[case]),
                           'method': ('exp3', 'payoff_frequency')[method], 'opportunities': time,
                           'earned_payoff_per_opportunity': float(payoff_sum[method, case]/time),
                           'cumulative_population_regret': float(regret_sum[method, case]),
                           'mean_population_regret': float(regret_sum[method, case]/time),
                           'final_forecast_mse': float((final_mse_exp if method == 0 else final_mse_freq)[case]),
                           'bought_observations': int(observations[method, case])}
                    if method == 0:
                        row.update({'correct_judge_fraction': float(correct_sum[case]/time),
                                    'last_4096_correct_fraction': float(recent_correct[:, case].mean()),
                                    'gamma': float(gamma[case]),
                                    'raw_payoff_regret_bound_to_correct': float(2*(
                                        3*np.log(1/prior[case, correct_arm[case]])/gamma[case]
                                        +(math.e-1)*gamma[case]*time))})
                    else:
                        actual_n = total_count[case]-2
                        radius = np.sqrt(np.log(math.pi**2*(2*n)*actual_n**2/(3*0.05))/(2*actual_n))
                        radius += 2/(actual_n+2)
                        prediction = np.clip(success_count[case]/total_count[case], 0.1, 0.9)
                        row.update({'cell_observation_counts': actual_n.astype(int).tolist(),
                                    'final_forecast': prediction.tolist(),
                                    'simultaneous_confidence_radii': radius.tolist(),
                                    'confidence_event_holds': bool(np.all(np.abs(prediction-truth[case]) <= radius))})
                    rows.append(row)
    summary = []
    for time in PREFIXES:
        for method in ('exp3', 'payoff_frequency'):
            group = [r for r in rows if r['opportunities'] == time and r['method'] == method]
            summary.append({'method': method, 'opportunities': time, 'runs': len(group),
                            **{name: float(np.mean([r[name] for r in group])) for name in (
                                'earned_payoff_per_opportunity', 'cumulative_population_regret',
                                'mean_population_regret', 'final_forecast_mse', 'bought_observations')},
                            **({'correct_judge_fraction': float(np.mean([r['correct_judge_fraction'] for r in group])),
                                'last_4096_correct_fraction': float(np.mean([r['last_4096_correct_fraction'] for r in group]))}
                               if method == 'exp3' else {})})
    result = {'status': 'passed', 'contract': {'master_seed': MASTER_SEED,
              'repetitions': REPETITIONS, 'initial_priors': PRIORS.tolist(),
              'horizon': HORIZON, 'prefixes': PREFIXES, 'outcome_after_declining': False,
              'oracle_expected_payoff': 0.17, 'frequency_clip': [0.1, 0.9]},
              'summary': summary, 'rows': rows}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n',
                                                  encoding='utf-8', newline='\n')
    print(json.dumps({'status': 'passed', 'summary': summary}, indent=2))


if __name__ == '__main__':
    main()
