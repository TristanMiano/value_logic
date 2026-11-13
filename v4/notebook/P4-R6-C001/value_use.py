"""A continuation value, a recurring bonus, and correction. Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

import numpy as np


def exact_preparation():
    rows, potential_checks = [], 0
    direct, cost = F(2,5),F(1,10)
    for p,gamma,beta in product((F(7,10),F(4,5),F(9,10)),
                                (F(1,2),F(9,10),F(99,100),F(999,1000)),
                                (F(0),F(1,200),F(1,50),F(1,5))):
        bonus = beta*p
        complete, wait = p+bonus,bonus/(1-gamma)
        assert (wait > complete) == (beta > (1-gamma)/gamma)
        best = max(complete,wait)
        assert best == max(p+bonus,bonus+gamma*best)
        prepare = -cost+gamma*best > direct
        actual = (-cost if wait > complete else -cost+gamma*p) if prepare else direct
        rows.append({'p':str(p),'gamma':str(gamma),'beta':str(beta),
                     'true_optimum':str(max(direct,-cost+gamma*p)),
                     'proxy_prefers_wait':wait > complete,
                     'proxy_prefers_prepare':prepare,
                     'true_value_of_proxy_policy':str(actual)})
        for hundredths in range(121):
            q = F(hundredths,100)
            prep_score,complete_score,wait_score = -cost+gamma*q,p-q,-(1-gamma)*q
            uniquely_good = prep_score > direct and complete_score > wait_score
            assert uniquely_good == ((direct+cost)/gamma < q < p/gamma)
            # The fully planned shaped value is V*-Phi, including the
            # infinite-wait alternative; test its Bellman equation exactly.
            shaped_b = p-q
            assert shaped_b == max(p-q,-(1-gamma)*q+gamma*shaped_b)
            shaped_root = max(direct,-cost+gamma*p)
            assert shaped_root == max(direct,-cost+gamma*q+gamma*shaped_b)
            potential_checks += 1
    return {'bonus_settings':len(rows),'potential_bellman_checks':potential_checks,'runs':rows}


def approximate_greedy():
    rng = np.random.default_rng(61501)
    checks, policy_changes, largest_loss = 0,0,0.0
    margin_checks = 0
    for _ in range(80):
        n,actions = 3,2
        transition = rng.dirichlet(np.ones(n),(n,actions))
        reward = rng.uniform(-1,1,(n,actions))
        gamma = float(rng.choice([.5,.8,.95]))
        policy_values = []
        for choices in product(range(actions),repeat=n):
            choices = np.array(choices)
            matrix = transition[np.arange(n),choices]
            rr = reward[np.arange(n),choices]
            policy_values.append(np.linalg.solve(np.eye(n)-gamma*matrix,rr))
        optimal = np.max(policy_values,axis=0)
        qstar = reward+gamma*np.einsum('iaj,j->ia',transition,optimal)
        assert np.max(np.abs(qstar.max(axis=1)-optimal)) < 1e-11
        for eta in (.001,.01,.1,.5):
            potential = optimal+rng.uniform(-eta,eta,n)
            score = reward+gamma*np.einsum('iaj,j->ia',transition,potential)
            chosen = score.argmax(axis=1)
            matrix = transition[np.arange(n),chosen]
            value = np.linalg.solve(np.eye(n)-gamma*matrix,reward[np.arange(n),chosen])
            loss = optimal-value
            assert loss.min() >= -1e-11 and loss.max() <= 2*gamma*eta/(1-gamma)+1e-11
            separated = np.abs(qstar[:,0]-qstar[:,1]) > 2*gamma*eta
            assert np.all(chosen[separated] == qstar.argmax(axis=1)[separated])
            margin_checks += int(separated.sum())
            policy_changes += int(np.any(chosen != qstar.argmax(axis=1)))
            largest_loss = max(largest_loss,float(loss.max()))
            checks += 1
    return {'seed':61501,'models':80,'approximate_value_checks':checks,
            'separated_action_checks':margin_checks,
            'cases_changing_action':policy_changes,'largest_observed_value_loss':largest_loss}


def correction():
    p,gamma,alpha,q = F(4,5),F(99,100),F(1,10),F(9,10)
    factor = 1-alpha*(1-gamma)
    waited = 0
    while p-q <= -(1-gamma)*q:
        q *= factor
        waited += 1
    assert q < p/gamma
    assert q/factor >= p/gamma
    actual = -F(1,10)+gamma**(waited+1)*p
    return {'initial_estimate':.9,'true_completion_value':.8,'gamma':.99,'step_size':.1,
            'waiting_steps':waited,'corrected_estimate':float(q),
            'true_root_value_with_delay':float(actual),
            'true_root_value_with_exact_estimate':float(-F(1,10)+gamma*p)}


def main():
    out={'status':'passed','preparation':exact_preparation(),
         'approximation':approximate_greedy(),'correction':correction()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'preparation'},indent=2))
    print('preparation', {k:v for k,v in out['preparation'].items() if k != 'runs'})


if __name__ == '__main__':
    main()
