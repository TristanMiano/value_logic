"""A composed observed probe/adoption/calibration controller; Codex (GPT-6).

All methods have the same raw-trial budget, on their own induced streams.
The probing method has additional precise intervention authority. Query
economics are not assigned a fictitious price by this mechanism comparison.
"""
import json
from pathlib import Path
import numpy as np
from stochastic_judgment import Learner


class ProbeController:
    def __init__(self, paths, cost, alpha):
        self.cost, self.alpha = cost, alpha
        self.state = np.zeros(paths, dtype=int)  # 0 probe, 1 fine, 2 coarse
        self.u, self.v = np.zeros(paths), np.zeros(paths)
        self.b = np.zeros(paths)
        self.age = np.zeros(paths, dtype=int)
        self.adoption = np.full(paths, -1, dtype=int)
        self.initial_b = np.full(paths, np.nan)
        self.initial_lower = np.full(paths, np.nan)
        self.initial_upper = np.full(paths, np.nan)

    def action(self, rng):
        proposals = rng.choice([-1., 1.], size=len(self.b))
        return np.where(self.state == 0, proposals,
                        np.where(self.state == 1, self.b, 0.)), proposals

    def observe(self, z, proposals, trial):
        was_fine = self.state == 1
        accepted = (self.state == 0) & (z != proposals)
        self.u[accepted] += z[accepted]
        self.v[accepted] += 1
        valid = (self.state == 0) & (self.v > 0)
        v = np.maximum(self.v, 1)
        center = self.u/v
        radius = np.sqrt((v+1)*np.log((v+1)/(self.alpha**2)))/v
        lower, upper = np.maximum(-1, center-radius), np.minimum(1, center+radius)
        closest = np.where(lower > 0, lower, np.where(upper < 0, upper, 0.))
        fine = valid & (closest**2 > self.cost)
        coarse = valid & (np.maximum(lower**2, upper**2) < self.cost)
        assert not np.any(fine & coarse)
        self.state[fine], self.state[coarse] = 1, 2
        selected = fine | coarse
        self.adoption[selected] = trial
        self.initial_b[selected] = closest[selected]
        self.initial_lower[selected], self.initial_upper[selected] = lower[selected], upper[selected]
        self.b[fine] = closest[fine]
        # The selected probe that triggered adoption must not train the new
        # forecast as if it were an unselected deployment observation.
        gamma = (self.age[was_fine]+25.)**-.6
        self.b[was_fine] += gamma*(z[was_fine]-self.b[was_fine])
        self.age[was_fine] += 1


def main():
    cases = [
        {'name': 'weak_informative', 'a': .6, 'e': .05},
        {'name': 'no_distinction', 'a': 0., 'e': .05},
        {'name': 'small_distinction', 'a': .1, 'e': .05},
        {'name': 'decision_boundary', 'a': .2, 'e': .05},
        {'name': 'negative_environment', 'a': -.6, 'e': .05},
        {'name': 'moderate_exposure', 'a': .6, 'e': .2}]
    repetitions, steps, cost, alpha = 12, 100000, .04, .05
    a = np.repeat([c['a'] for c in cases], repetitions)
    e = np.repeat([c['e'] for c in cases], repetitions)
    b0 = np.where(a < 0, .5, -.5)
    coupled = Learner(b0, np.full(len(a), .01), eta=1.)
    full = b0.copy()
    controller = ProbeController(len(a), cost, alpha)
    rng = np.random.default_rng(20261126)
    for t in range(steps):
        uniform = rng.random(len(a))
        mean, proposals = controller.action(rng)
        q = e*a+(1-e)*mean
        z = np.where(uniform < (1+q)/2, 1., -1.)
        controller.observe(z, proposals, t+1)
        gamma = (t+25.)**-.6
        zc = np.where(uniform < (1+e*a+(1-e)*coupled.influence()*coupled.b)/2, 1., -1.)
        coupled.step(zc, gamma)
        zf = np.where(uniform < (1+e*a+(1-e)*full)/2, 1., -1.)
        full += gamma*(zf-full)
    rows = []
    for i, case in enumerate(cases):
        selection = slice(i*repetitions, (i+1)*repetitions)
        states = controller.state[selection]
        chosen = states != 0
        times = controller.adoption[selection]
        forecasts = controller.b[selection]
        # An unresolved controller defaults to coarse at the end of the trial budget.
        final_b = np.where(states == 1, forecasts, 0.)
        final_gain = 2*case['a']*final_b-final_b**2-cost*(states == 1)
        oracle = max(0., case['a']**2-cost)
        initial_b = controller.initial_b[selection]
        initial_gain = 2*case['a']*initial_b-initial_b**2-cost
        covered = (controller.initial_lower[selection] <= case['a']) & (case['a'] <= controller.initial_upper[selection])
        rows.append({**case,
                     'fine_decisions': int((states == 1).sum()),
                     'coarse_decisions': int((states == 2).sum()),
                     'unresolved': int((states == 0).sum()),
                     'decision_trial_median': float(np.median(times[chosen])) if np.any(chosen) else None,
                     'decision_trial_range': [int(times[chosen].min()), int(times[chosen].max())] if np.any(chosen) else None,
                     'probe_trials_mean': float(np.mean(np.where(chosen, times, steps))),
                     'accepted_marks': controller.v[selection].astype(int).tolist(),
                     'initial_intervals_cover': int(covered[chosen].sum()),
                     'initial_fine_reference_gain_min': float(np.min(initial_gain[states == 1])) if np.any(states == 1) else None,
                     'final_reference_regret_mean': float(np.mean(oracle-final_gain)),
                     'final_forecast_mse': float(np.mean((final_b-case['a'])**2)),
                     'passive_coupled_forecast_mse': float(np.mean((coupled.b[selection]-case['a'])**2)),
                     'passive_fine_weight_mean': float(np.mean(coupled.influence()[selection])),
                     'always_fine_forecast_mse': float(np.mean((full[selection]-case['a'])**2)),
                     'always_fine_reference_regret': float(oracle-np.mean(2*case['a']*full[selection]-full[selection]**2-cost)),
                     'individual_decisions': states.tolist(),
                     'individual_decision_trials': times.tolist(),
                     'individual_final_forecasts': final_b.tolist()})
    assert np.max(np.abs(coupled.identity_error())) < 1e-7
    assert np.max(np.abs(controller.b)) <= 1
    result = {'author': 'Codex (GPT-6)', 'status': 'passed', 'seed': 20261126,
              'raw_trials_per_path_per_method': steps, 'independent_paths_per_case': repetitions,
              'declared_fine_use_cost': cost, 'confidence_per_path': 1-alpha,
              'same_total_raw_budget': True,
              'additional_probe_authority': 'agent produces the proposed sign exactly; source share precedes the proposal',
              'economics': 'probe trial counts shown; intervention cost and foregone utility not priced',
              'unresolved_end_policy': 'coarse fallback without an adequacy certificate',
              'rows': rows}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}))
    for row in rows:
        print(json.dumps({k: v for k, v in row.items() if not k.startswith('individual_')}))


if __name__ == '__main__':
    main()
