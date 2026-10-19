"""Codex (GPT-6), s12 DEVELOPMENT risk-priced graphic recovery example.

Enumerate the declared 29 methods and their two-method mixtures, check explicit
cut/flow lower certificates, and execute the selected inference on all tiny inputs.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent


def methods():
    out = []
    prices, errors = [F(3,2), F(3,2), F(201,2)], [F(2,5), F(2,5), F(1,100)]
    for actions in product(['a_exact','a_model','b_exact'], repeat=3):
        cost = risk = F(0)
        for i, action in enumerate(actions):
            if action == 'a_exact':
                cost += prices[i]
            elif action == 'a_model':
                cost += 1
                risk += errors[i]
            else:
                cost += F(201,2)
        out.append(dict(name='/'.join(actions), cost=cost, risk=risk))
    out += [dict(name='direct_exact',cost=F(201,2),risk=F(0)),
            dict(name='fair_guess',cost=F(0),risk=F(1,2))]
    return out


def optimum(methods_, alpha):
    candidates = [(m['cost'], [(m['name'],F(1))]) for m in methods_ if m['risk'] <= alpha]
    checks = 0
    for i, a in enumerate(methods_):
        for b in methods_[i+1:]:
            checks += 1
            if a['risk'] == b['risk']:
                continue
            weight = (alpha-b['risk'])/(a['risk']-b['risk'])
            if 0 <= weight <= 1:
                candidates.append((weight*a['cost']+(1-weight)*b['cost'],
                                   [(a['name'],weight),(b['name'],1-weight)]))
    return min(candidates, key=lambda row: row[0]), checks


def separator(lam):
    prices, errors = [F(3,2), F(3,2), F(201,2)], [F(2,5), F(2,5), F(1,100)]
    a = [min(prices[i],1+lam*errors[i]) for i in range(3)]
    b = [F(201,2)]*3
    # Each path supports this much flow. Picking the cheaper edge on each
    # path gives a cut of the same value: an explicit primal/dual witness.
    path_flows = [min(x,y) for x,y in zip(a,b)]
    cut_value = sum(path_flows)
    return min(cut_value,F(201,2),lam/2), path_flows


def main():
    started = time.perf_counter_ns()
    menu = methods()
    panels, mixture_checks = [], 0
    for alpha in map(F,[0,F(1,1000),F(1,100),F(1,20),F(1,10),F(1,4),F(1,2)]):
        (cost, mix), checks = optimum(menu, alpha)
        mixture_checks += checks
        lam = F(9650) if alpha < F(1,100) else F(400,49)
        if alpha == F(1,100):
            lam = F(10)
        if alpha == F(1,2):
            lam = F(0)
        z, flow = separator(lam)
        assert z == min(m['cost']+lam*m['risk'] for m in menu)
        assert cost == z-lam*alpha, (alpha,cost,z,lam)
        panels.append(dict(alpha=str(alpha), certified_fee=str(cost),
                           mixture=[dict(method=name,weight=str(w)) for name,w in mix],
                           lambda_=str(lam), z=str(z), path_flow=[str(x) for x in flow],
                           direct_and_guess_fee=str(F(201,2)*(1-2*alpha))))
    executions = 0
    for hidden in range(8):
        bits = [(hidden>>i)&1 for i in range(3)]
        target = sum(bits)%2
        # Graph truth consists of (target, a1,b1,a2,b2,a3,b3); each path's
        # two edges agree, and target equals the three path bits' parity.
        graph_truth = [target]+[bit for bit in bits for _ in range(2)]
        assert graph_truth[0]^graph_truth[1]^graph_truth[3]^graph_truth[5] == 0
        for predicted in range(8):
            costs = []
            for orientation in [0,1]:
                inferred = (predicted>>2)&1
                cost = 1  # Evaluate only the a3 model.
                for i in [0,1]:
                    invoice = 1+(bits[i]^orientation)
                    inferred ^= (invoice-1)^orientation
                    cost += invoice
                assert (inferred^target) == (((predicted>>2)&1)^bits[2])
                costs.append(cost)
                executions += 1
            assert F(sum(costs),2) == 4
    # Attain the 1% error by making only the used a3 prediction wrong with
    # that probability. The other supplied marginal bounds are then respected.
    model_risk = F(1,100)
    mixture_risk = F(40,49)*model_risk+F(9,49)*F(1,2)
    assert mixture_risk == F(1,10)
    result = dict(status='PASS', contributor='Codex (GPT-6)', scope='DEVELOPMENT',
                  python=sys.version, elapsed_ns=time.perf_counter_ns()-started,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  totals=dict(methods=len(menu), risk_levels=len(panels), pair_checks=mixture_checks,
                              explicit_invoice_executions=executions), panels=panels,
                  limitations='Constructed three-path example; optimality only for the declared '
                  'union-bound certificate-accounting class. Calibration/source preparation and '
                  'controller costs are excluded, and zero coin/episode price is explicit.')
    (HERE/'risk_cut_probe.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({k:result[k] for k in ('status','elapsed_ns','totals')},indent=2))
    for row in panels:
        print(json.dumps({k:row[k] for k in ('alpha','certified_fee','lambda_','direct_and_guess_fee')}))


if __name__ == '__main__':
    main()
