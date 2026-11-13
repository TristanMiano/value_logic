"""Selection of actions, not control over luck. Codex (GPT-6), W6."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random

import numpy as np


def frac_row(rng, size, killed=False):
    row = [F(rng.randint(1, 9)) for _ in range(size+int(killed))]
    total = sum(row)
    return [x/total for x in row[:size]]


def finite_checks():
    rng = random.Random(61301)
    inequalities, path_checks = 0, 0
    for case in range(60):
        size, actions, horizon = 2, 2, 4
        kernels = [[frac_row(rng, size, True) for _ in range(size)] for _ in range(actions)]
        pi = [frac_row(rng, actions) for _ in range(size)]
        terminal = [F(rng.randint(1, 9), 10) for _ in range(size)]
        baseline = [terminal]
        improvement = [terminal]
        picks = []
        for n in range(1, horizon+1):
            w = [[sum(kernels[a][i][j]*baseline[-1][j] for j in range(size))
                  for a in range(actions)] for i in range(size)]
            h = [sum(pi[i][a]*w[i][a] for a in range(actions)) for i in range(size)]
            policy = [[pi[i][a]*w[i][a]/h[i] for a in range(actions)] for i in range(size)]
            value = [sum(policy[i][a]*kernels[a][i][j]*improvement[-1][j]
                         for a in range(actions) for j in range(size)) for i in range(size)]
            for i in range(size):
                assert sum(policy[i]) == 1
                assert value[i] >= h[i]
                inequalities += 1
            baseline.append(h)
            improvement.append(value)
            picks.append(policy)
        # Independently enumerate action and state histories for some cases.
        if case < 10:
            for initial in range(size):
                first_weights = [F(0)]*actions
                for aa in product(range(actions), repeat=horizon):
                    for ss in product(range(size), repeat=horizon):
                        path = (initial,)+ss
                        weight = terminal[path[-1]]
                        for t, a in enumerate(aa):
                            weight *= pi[path[t]][a]*kernels[a][path[t]][path[t+1]]
                        first_weights[aa[0]] += weight
                        path_checks += 1
                assert sum(first_weights) == baseline[horizon][initial]
                assert [w/sum(first_weights) for w in first_weights] == picks[-1][initial]
    return {'rational_mdp_instances': 60, 'finite_horizon_improvements': inequalities,
            'action_state_paths_enumerated': path_checks}


def perron(k):
    vals, vecs = np.linalg.eig(k)
    idx = int(np.argmax(vals.real))
    lam, h = float(vals[idx].real), vecs[:, idx].real
    h /= h.max() if h.sum() > 0 else h.min()
    assert np.all(h > 0) and np.max(np.abs(k@h-lam*h)) < 1e-11
    return lam, h


def spectral_checks():
    rng = np.random.default_rng(61302)
    gaps, conditional_gaps = [], []
    for _ in range(300):
        size, actions = int(rng.integers(2, 6)), int(rng.integers(2, 5))
        kernels = rng.uniform(0.01, 1, (actions, size, size+1))
        kernels /= kernels.sum(axis=2, keepdims=True)
        kernels = kernels[:, :, :size]
        pi = rng.dirichlet(np.ones(actions), size)
        k = np.einsum('ia,aij->ij', pi, kernels)
        lam, h = perron(k)
        w = np.einsum('aij,j->ia', kernels, h)
        copied = pi*w/(lam*h[:, None])
        assert np.max(np.abs(copied.sum(axis=1)-1)) < 1e-12
        live = np.einsum('ia,aij->ij', copied, kernels)
        new_lam, _ = perron(live)
        variance = (pi*(w-(lam*h)[:, None])**2).sum(axis=1)
        assert np.max(np.abs(live@h-lam*h-variance/(lam*h))) < 2e-12
        assert new_lam >= lam-1e-12
        gaps.append(new_lam-lam)
        conditioned_state = k*h[None, :]/(lam*h[:, None])
        actual_live_conditioned = live/live.sum(axis=1, keepdims=True)
        conditional_gaps.append(float(np.abs(conditioned_state-actual_live_conditioned).sum(axis=1).max()/2))
    # With one available action, selected histories can change their apparent
    # transition frequencies while the controller has no policy to improve.
    k = np.array([[0.6, 0.4], [0.1, 0.6]])
    lam, h = perron(k)
    doob = k*h[None, :]/(lam*h[:, None])
    baseline_live = k/k.sum(axis=1, keepdims=True)
    return {'positive_mdp_instances': 300, 'minimum_growth_improvement': min(gaps),
            'maximum_growth_improvement': max(gaps),
            'mean_growth_improvement': float(np.mean(gaps)),
            'mean_conditioned_vs_controlled_live_tv': float(np.mean(conditional_gaps)),
            'one_action_example_no_policy_change': True,
            'one_action_conditioned_vs_actual_live_tv': float(np.abs(doob-baseline_live).sum(axis=1).max()/2)}


def repeat_exact_example():
    kernels = np.zeros((2, 2, 2))
    kernels[0, :, 0] = [1.0, 0.7]
    kernels[1, :, 1] = [1.0, 0.7]
    pi = np.array([[0.6, 0.4], [1/7, 6/7]])
    rows = []
    previous = 0.0
    for iteration in range(41):
        k = np.einsum('ia,aij->ij', pi, kernels)
        lam, h = perron(k)
        assert lam >= previous-1e-12
        previous = lam
        rows.append({'iteration': iteration, 'survival_factor': lam, 'policy': pi.tolist()})
        w = np.einsum('aij,j->ia', kernels, h)
        pi = pi*w/(lam*h[:, None])
    assert abs(rows[0]['survival_factor']-0.8) < 1e-12
    assert abs(rows[1]['survival_factor']-0.875) < 1e-12
    return rows


def sample_bound_check():
    source = Path(__file__).with_name('unrepresented_values.json')
    panel = json.loads(source.read_text(encoding='utf-8',newline='\n'))['cloning']
    count = len(panel['settings'])*panel['replicas']*2
    delta = 0.05
    checked, violations, max_radius = 0, 0, 0.0
    for row in panel['settings']:
        target = row['finite_selected_policy']
        for run in row['runs']:
            for i in (0, 1):
                accepted = sum(run['accepted_first_actions'][i])
                radius = min(1.0, np.sqrt(np.log(2*count/delta)/(2*accepted))+1/(accepted+2))
                error = abs(run['learned_policy'][i][0]-target[i][0])
                violations += int(error > radius)
                max_radius = max(max_radius, float(radius))
                checked += 1
    return {'simultaneous_delta': delta, 'row_checks': checked,
            'violations': violations, 'maximum_radius': max_radius}


def exact_iterations(kernels, initial, iterations):
    """Keep log frequencies so small positive actions can later recover."""
    log_pi = np.log(initial)
    previous = 0.0
    checkpoints = []
    for step in range(iterations+1):
        centered = log_pi-log_pi.max(axis=1, keepdims=True)
        pi = np.exp(centered)
        pi /= pi.sum(axis=1, keepdims=True)
        k = np.einsum('ia,aij->ij', pi, kernels)
        lam, h = perron(k)
        h /= h.sum()
        assert lam >= previous-3e-12
        previous = lam
        w = np.einsum('aij,j->ia', kernels, h)
        mean_w = (pi*w).sum(axis=1)
        residual = float(np.max(w/mean_w[:, None]-1))
        if step in (0, 1, 10, 100, 1000, iterations):
            checkpoints.append({'step': step, 'factor': lam,
                                'bellman_relative_residual': residual})
        # This normalized update is algebraically (7); normalize log weights
        # to avoid cumulative floating point row-sum drift.
        log_pi = centered+np.log(w)-np.log(mean_w[:, None])
    return lam, h, pi, checkpoints


def greedy_iterations(kernels, initial):
    """A genuinely different, fully informed maximizing-row comparator."""
    pi = initial.copy()
    for step in range(100):
        lam, h = perron(np.einsum('ia,aij->ij', pi, kernels))
        w = np.einsum('aij,j->ia', kernels, h)
        if np.max(w.max(axis=1)-lam*h) < 1e-12:
            return lam, step
        pi = np.eye(kernels.shape[0])[w.argmax(axis=1)]
    raise AssertionError('greedy comparator did not finish within declared cap')


def global_checks():
    rng = np.random.default_rng(61303)
    rows = []
    for case in range(80):
        size, actions = int(rng.integers(2, 6)), int(rng.integers(2, 5))
        kernels = rng.uniform(0.01, 1, (actions, size, size+1))
        kernels /= kernels.sum(axis=2, keepdims=True)
        kernels = kernels[:, :, :size]
        initial = rng.dirichlet(np.full(actions, 0.2 if case % 2 else 1.0), size)
        assert np.all(initial > 0)
        oracle, best = -1.0, None
        for chosen in product(range(actions), repeat=size):
            value, _ = perron(kernels[np.array(chosen), np.arange(size), :])
            if value > oracle:
                oracle, best = value, chosen
        lam, h, pi, checkpoints = exact_iterations(kernels, initial, 2000)
        greedy, greedy_steps = greedy_iterations(kernels, initial)
        assert lam <= oracle+3e-12 and abs(greedy-oracle) < 3e-12
        rows.append({'case': case, 'states': size, 'actions': actions,
                     'initial_smallest_probability': float(initial.min()),
                     'oracle_factor': oracle, 'oracle_policy': best,
                     'factor_after_2000': lam, 'gap': max(0.0, oracle-lam),
                     'greedy_iterations': greedy_steps, 'checkpoints': checkpoints})
    # Every action can reach either live state; this perturbation satisfies
    # Theorem 3, unlike the zero-entry illustrative model used above.
    kernels = np.array([[[.98, .02], [.686, .014]],
                        [[.02, .98], [.014, .686]]])
    initial = np.array([[.6, .4], [1/7, 6/7]])
    lam, h, pi, path = exact_iterations(kernels, initial, 2000)
    assert abs(lam-.994) < 1e-12
    assert np.max(np.abs(h-np.array([1, .7])/1.7)) < 1e-12
    return {'seed': 61303, 'models': 80, 'iterations_each': 2000,
            'maximum_gap_after_2000': max(row['gap'] for row in rows),
            'median_gap_after_2000': float(np.median([row['gap'] for row in rows])),
            'maximum_greedy_iterations': max(row['greedy_iterations'] for row in rows),
            'positive_tremble_example': {'factor': lam, 'normalized_h': h.tolist(),
                                         'policy': pi.tolist(), 'checkpoints': path},
            'runs': rows}


def persistence_boundaries():
    ratio = 9/7
    rare_odds = np.log(1e-12/(1-1e-12))
    crossing = int(np.floor(-rare_odds/np.log(ratio)))+1
    assert rare_odds+(crossing-1)*np.log(ratio) <= 0
    assert rare_odds+crossing*np.log(ratio) > 0
    # With no mutation, 1000 selection rounds accumulate 1000 log-odds
    # increments; exactly as many opposite rounds undo them.
    reversal_time = 1001
    mutation = .01
    q = .5
    for _ in range(1000):
        selected = ratio*q/(ratio*q+1-q)
        q = mutation+(1-2*mutation)*selected
    before = q
    revised_crossing = None
    for step in range(1, 1002):
        selected = q/(q+ratio*(1-q))
        q = mutation+(1-2*mutation)*selected
        if q < .5:
            revised_crossing = step
            break
    assert revised_crossing is not None and revised_crossing < reversal_time
    # A missing action stays absent under exact copying. Mutation supplies it.
    assert 0*ratio/(0*ratio+1) == 0
    return {'survival_factors': [.7, .9], 'initial_good_probability': 1e-12,
            'rounds_until_good_majority': crossing,
            'rounds_before_environment_reversal': 1000,
            'no_revision_rounds_to_reverse_majority': reversal_time,
            'symmetric_revision_rate': mutation,
            'probability_before_reversal_with_revision': before,
            'revision_rounds_to_reverse_majority': revised_crossing,
            'absent_action_without_revision_stays_absent': True}


def sparse_checks():
    rng = np.random.default_rng(61304)
    rows=[]
    for case in range(40):
        size,actions=int(rng.integers(3,6)),int(rng.integers(2,4))
        kernels=np.zeros((actions,size,size))
        for a in range(actions):
            for i in range(size):
                survival=float(rng.uniform(.5,.99))
                mix=float(rng.uniform(.2,.8))
                kernels[a,i,(i+1)%size] += survival*mix
                kernels[a,i,(i if a == 0 else i+a+1)%size] += survival*(1-mix)
        assert np.all(kernels[:,np.arange(size),(np.arange(size)+1)%size] > 0)
        assert np.any(kernels == 0)
        initial=rng.dirichlet(np.ones(actions),size)
        oracle=max(perron(kernels[np.array(p),np.arange(size),:])[0]
                   for p in product(range(actions),repeat=size))
        value,_,_,path=exact_iterations(kernels,initial,2000)
        greedy,steps=greedy_iterations(kernels,initial)
        assert value <= oracle+3e-12 and abs(greedy-oracle) < 3e-12
        rows.append({'case':case,'states':size,'actions':actions,
                     'oracle_factor':oracle,'gap_after_2000':max(0.0,oracle-value),
                     'greedy_iterations':steps,'checkpoints':path})
    return {'seed':61304,'models':40,'maximum_gap_after_2000':max(r['gap_after_2000'] for r in rows),
            'maximum_greedy_iterations':max(r['greedy_iterations'] for r in rows),'runs':rows}


def main():
    out = {'status': 'passed', 'finite': finite_checks(), 'spectral': spectral_checks(),
           'repeated_exact_update': repeat_exact_example(), 'sample_bound': sample_bound_check(),
           'global': global_checks(), 'persistence': persistence_boundaries(), 'sparse':sparse_checks()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('repeated_exact_update', 'global','sparse')}, indent=2))
    print('global', {k:v for k,v in out['global'].items() if k not in ('runs', 'positive_tremble_example')})
    print('sparse',{k:v for k,v in out['sparse'].items() if k != 'runs'})
    print('last exact iteration', out['repeated_exact_update'][-1])


if __name__ == '__main__':
    main()
