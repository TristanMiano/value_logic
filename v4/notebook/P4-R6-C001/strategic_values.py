"""Observable commitment and two-type value dynamics; Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
import json
import math


def investment(x,tau):
    return 1/(1+math.exp(-(2*x-1)/tau))


def difference(x,q,cost,tau):
    return q-cost-2*(1-q)*investment(x,tau)


def derivative(x,q,cost,tau):
    return x*(1-x)*difference(x,q,cost,tau)


def run(x,q,cost,tau,horizon=200,dt=0.02):
    trace=[{'time':0,'return_fraction':x}]
    for step in range(1,round(horizon/dt)+1):
        k1=derivative(x,q,cost,tau)
        k2=derivative(x+dt*k1/2,q,cost,tau)
        k3=derivative(x+dt*k2/2,q,cost,tau)
        k4=derivative(x+dt*k3,q,cost,tau)
        x+=dt*(k1+2*k2+2*k3+k4)/6
        assert 0<=x<=1
        if step in (500,2500,10000):
            trace.append({'time':step*dt,'return_fraction':x})
    return trace


def main():
    # Preference installation changes whole-outcome ordering. Its adoption
    # is nevertheless favored by the previous own-wealth objective.
    lam=F(6,5); install_cost=F(1,10)
    assert 1+2*lam>3
    assert 1-install_cost>0
    cases=[]
    for q,cost in ((0.9,0.1),(0.5,0.1),(0.1,0.2)):
        tau=0.1
        d0,d1=difference(0,q,cost,tau),difference(1,q,cost,tau)
        if d0>0>d1:
            z=(q-cost)/(2*(1-q))
            target=0.5+tau/2*math.log(z/(1-z))
            low,high=0.,1.
            for _ in range(60):
                mid=(low+high)/2
                if difference(mid,q,cost,tau)>0: low=mid
                else: high=mid
            assert abs(target-(low+high)/2)<1e-12
            disposition='mixed attracting equilibrium'
        elif d1>0:
            target=1.; disposition='Return grows from interior starts'
        else:
            assert d0<0
            target=0.; disposition='Grab grows from interior starts'
        trajectories=[]
        for start in (0.1,0.9):
            trace=run(start,q,cost,tau)
            assert abs(trace[-1]['return_fraction']-target)<1e-7
            trajectories.append({'start':start,'trace':trace})
        cases.append({'observability':q,'maintenance_cost':cost,'tau':tau,
                      'difference_at_zero':d0,'difference_at_one':d1,
                      'target':target,'disposition':disposition,'trajectories':trajectories})
    certificate=[]
    for s,f,cost in ((F(9,10),F(1,10),F(1,10)),(F(3,5),F(3,10),F(1,10))):
        low=f/(s+f); high=(1-f)/(2-s-f)
        x=(low+high)/2
        pass_return=x*s/(x*s+(1-x)*f)
        fail_return=x*(1-s)/(x*(1-s)+(1-x)*(1-f))
        assert pass_return>F(1,2)>fail_return
        material_return=s-cost; material_grab=3*f
        assert material_return-material_grab==s-3*f-cost
        certificate.append({'true_positive':str(s),'false_positive':str(f),'cost':str(cost),
                            'pass_only_population_interval':[str(low),str(high)],
                            'checked_population':str(x),'return_material_advantage':str(s-3*f-cost)})
    result={'status':'passed','installation_lambda':str(lam),
            'previous_goal_gain_after_installation':str(1-install_cost),
            'dynamics':'continuous replicator; RK4 dt=0.02 for 200 time units',
            'cases':cases,'certificate_examples':certificate}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'passed','equilibria':[r['target'] for r in cases],
                      'certificate_examples':certificate},indent=2))


if __name__=='__main__': main()
