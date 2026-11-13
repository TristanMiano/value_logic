"""Finite-trial diagnostics for R6.13. Codex (GPT-6)."""
from itertools import product
import json
from pathlib import Path

import numpy as np

from selection_learning import perron


def kernel(kernels, pi):
    return np.einsum('ia,aij->ij',pi,kernels)


def action_scores(kernels, pi, horizon=None):
    live=kernel(kernels,pi)
    if horizon is None:
        _,h=perron(live)
    else:
        h=np.linalg.matrix_power(live,horizon-1)@np.ones(live.shape[0])
    return np.einsum('aij,j->ia',kernels,h)


def update(log_pi, scores):
    assert np.all(scores > 0)
    log_pi=log_pi+np.log(scores)
    log_pi-=log_pi.max(axis=1,keepdims=True)
    pi=np.exp(log_pi)
    pi/=pi.sum(axis=1,keepdims=True)
    return log_pi,pi


def run(kernels,horizon=None,trials=None,seed=0):
    actions,states,_=kernels.shape
    log_pi=np.zeros((states,actions))
    pi=np.full((states,actions),1/actions)
    rng=np.random.default_rng(seed)
    factors=[perron(kernel(kernels,pi))[0]]
    accepted=0
    for _ in range(64):
        # This environment routine computes the success-count law. Only
        # the sampled count, not its hidden mean, reaches the update.
        means=action_scores(kernels,pi,horizon)
        if trials is None:
            scores=means
        else:
            observed=rng.binomial(trials,np.clip(means,0,1))
            accepted+=int(observed.sum())
            scores=(observed+1)/(trials+2)
        log_pi,pi=update(log_pi,scores)
        factors.append(perron(kernel(kernels,pi))[0])
    return {'initial_factor':factors[0],'final_factor':factors[-1],
            'smallest_step':float(np.diff(factors).min()),
            'downward_steps':int((np.diff(factors) < -1e-12).sum()),
            'accepted_trials':accepted,
            'attempted_trials':0 if trials is None else 64*states*actions*trials,
            'transition_upper_bound':0 if trials is None else 64*states*actions*trials*horizon}


def approximation_checks():
    rng=np.random.default_rng(61802)
    checked=0
    for _ in range(100):
        k=rng.uniform(.1,1,(2,2,3))
        k/=k.sum(axis=2,keepdims=True)
        k=k[:,:,:2]
        pi=rng.dirichlet([1,1],2)
        live=kernel(k,pi)
        lam,h=perron(live)
        h/=h.sum()
        m=float(k.min())/2
        beta=1-2*m*m
        q=live*h[None,:]/(lam*h[:,None])
        _,z=perron(q.T)
        z/=z.sum()
        scale=float(z@(1/h))
        target=action_scores(k,pi)
        # action_scores normalizes h differently; use the proof's h here.
        target=np.einsum('aij,j->ia',k,h)
        for horizon in (1,2,4,8,16,32):
            actual=action_scores(k,pi,horizon)
            relative=np.abs(actual/(lam**(horizon-1)*scale*target)-1).max()
            bound=beta**(horizon-1)/m
            assert relative <= bound+1e-10
            checked+=1
        eps=.01
        noise=rng.uniform(-eps,eps,target.shape)
        exact=pi*target/(pi*target).sum(axis=1,keepdims=True)
        perturbed=pi*target*(1+noise)
        perturbed/=perturbed.sum(axis=1,keepdims=True)
        distance=np.abs(exact-perturbed).sum(axis=1).max()
        assert distance <= 2*eps/(1-eps)+1e-12
        gap=abs(perron(kernel(k,exact))[0]-perron(kernel(k,perturbed))[0])
        assert gap <= 4*eps/m+1e-12
    return {'positive_models':100,'finite_horizon_relative_bound_checks':checked,
            'relative_policy_and_factor_perturbation_checks':200}


def main():
    rng=np.random.default_rng(61801)
    rows=[]
    for case in range(16):
        k=rng.uniform(.03,1,(2,2,3))
        k/=k.sum(axis=2,keepdims=True)
        k=k[:,:,:2]
        optimum=max(perron(k[np.array(p),np.arange(2),:])[0]
                    for p in product(range(2),repeat=2))
        exact=run(k)
        for horizon in (1,4,12):
            truncated=run(k,horizon)
            for trials in (64,512,4096):
                sampled=run(k,horizon,trials,6180100+100*case+10*horizon+trials)
                rows.append({'model':case,'horizon':horizon,'trials_per_row':trials,
                             'optimal_factor':optimum,'exact_perron_final':exact['final_factor'],
                             'exact_truncated_final':truncated['final_factor'],**sampled})
    summary=[]
    for horizon,trials in product((1,4,12),(64,512,4096)):
        selected=[r for r in rows if r['horizon']==horizon and r['trials_per_row']==trials]
        summary.append({'horizon':horizon,'trials_per_row':trials,
            'mean_optimal_factor':float(np.mean([r['optimal_factor'] for r in selected])),
            'mean_initial_factor':float(np.mean([r['initial_factor'] for r in selected])),
            'mean_final_factor':float(np.mean([r['final_factor'] for r in selected])),
            'mean_exact_perron_final':float(np.mean([r['exact_perron_final'] for r in selected])),
            'mean_exact_truncated_final':float(np.mean([r['exact_truncated_final'] for r in selected])),
            'models_worse_than_initial':sum(r['final_factor'] < r['initial_factor']-1e-12 for r in selected),
            'total_downward_steps':sum(r['downward_steps'] for r in selected),
            'accepted_fraction':sum(r['accepted_trials'] for r in selected)/sum(r['attempted_trials'] for r in selected),
            'attempted_trials_per_model':selected[0]['attempted_trials'],
            'transition_upper_bound_per_model':selected[0]['transition_upper_bound']})
    # Immediate survival favors entering the dangerous state. The two
    # available actions there coincide; no future luck can be controlled.
    example=np.array([[[.79,.01],[.1,.1]],[[.01,.94],[.1,.1]]])
    short=run(example,1)
    long=run(example,12)
    exact=run(example)
    assert short['final_factor'] < short['initial_factor']
    assert long['final_factor'] > long['initial_factor']
    out={'status':'passed','contract':{'seed':61801,'models':16,'rounds':64,
        'horizons':[1,4,12],'trials_per_state_action':[64,512,4096],
        'observation':'binomial survival count generated inside environment',
        'smoothing':'add one; not the conservative proposition schedule',
        'scope':'finite diagnostic panel; no total training-cost advantage'},
        'approximation':approximation_checks(),'summary':summary,'runs':rows,
        'short_horizon_boundary':{'kernels':example.tolist(),'horizon_one':short,
                                  'horizon_twelve':long,'exact_perron':exact}}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'runs'},indent=2))


if __name__ == '__main__':
    main()
