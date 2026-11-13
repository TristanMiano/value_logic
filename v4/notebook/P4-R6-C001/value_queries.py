"""Value judgments identify action dynamics under separation; Codex (GPT-6).

Exact finite witness and adverse comparisons for the R6.8 supplement.
This program receives supplied values; it is not a rollout-learning run.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random

from policy_values import identity, inverse, mv


def mm(a,b):
    return [[sum(x*y for x,y in zip(row,column)) for column in zip(*b)] for row in a]


def norm(a):
    return max(sum(abs(x) for x in row) for row in a)


def difference(a,b):
    return [[x-y for x,y in zip(row,other)] for row,other in zip(a,b)]


def det(a):
    a=[row[:] for row in a]
    result=F(1)
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:
            a[j],a[pivot]=a[pivot],a[j]
            result=-result
        p=a[j][j];result*=p
        a[j]=[x/p for x in a[j]]
        for i in range(j+1,len(a)):
            p=a[i][j]
            a[i]=[x-p*y for x,y in zip(a[i],a[j])]
    return result


def value(kernels,policy,reward,gamma):
    n=len(reward)
    p=[[sum(policy[i][a]*kernels[a][i][j] for a in range(len(kernels)))
        for j in range(n)] for i in range(n)]
    m=inverse([[F(i==j)-gamma*p[i][j] for j in range(n)] for i in range(n)])
    v=mv(m,reward)
    # Check against the original action-wise Bellman equation, not only
    # the matrix product used to calculate the values.
    assert all(v[i] == reward[i]+gamma*sum(policy[i][a]*sum(
        kernels[a][i][j]*v[j] for j in range(n)) for a in range(len(kernels)))
        for i in range(n))
    return v


def system(state,policies,values,rewards,gamma):
    n=len(values[0]);actions=len(policies[0][0])
    matrix=[[F(a==b) for a in range(actions) for j in range(n)] for b in range(actions)]
    right=[F(1)]*actions
    for pi,v,r in zip(policies,values,rewards):
        matrix.append([pi[state][a]*v[j] for a in range(actions) for j in range(n)])
        right.append((v[state]-r[state])/gamma)
    return matrix,right


def witness():
    n=3;gamma=F(3,4);reward=list(map(F,(0,1,3)))
    kernels=[[[F(4,5)*int(j==(i+1+a)%3)+F(1,15) for j in range(n)]
              for i in range(n)] for a in range(2)]
    choices=((0,0,0),(1,1,1),(0,1,1),(1,0,0))
    policies=[[[F(a==pi[i]) for a in range(2)] for i in range(n)] for pi in choices]
    rewards=[reward]*len(policies)
    values=[value(kernels,pi,reward,gamma) for pi in policies]
    determinants=[];matrices=[];inverse_norms=[]
    for i in range(n):
        b,r=system(i,policies,values,rewards,gamma)
        determinant=det(b)
        assert determinant
        recovered=mv(inverse(b),r)
        assert recovered == [kernels[a][i][j] for a in range(2) for j in range(n)]
        determinants.append(str(determinant));matrices.append([[str(x) for x in row] for row in b])
        inverse_norms.append(str(norm(inverse(b))))
    # Finite bounded errors: verify the computable certificate and retain
    # reconstruction failures of stochasticity rather than silently projecting.
    rng=random.Random(61901)
    bounds=[]
    for epsilon in (F(1,10000),F(1,1000),F(1,100),F(1,20)):
        checked=0;outside=0;max_error=F(0);max_bound=F(0);singular=0
        for _ in range(80):
            vh=[[x+rng.choice((-1,1))*epsilon for x in row] for row in values]
            for i in range(n):
                bh,rh=system(i,policies,vh,rewards,gamma)
                if det(bh)==0:
                    singular+=1;continue
                bi=inverse(bh);uh=mv(bi,rh)
                u=[kernels[a][i][j] for a in range(2) for j in range(n)]
                error=max(abs(x-y) for x,y in zip(uh,u))
                bound=norm(bi)*(1+1/gamma)*epsilon
                assert error <= bound
                assert all(sum(uh[a*n:(a+1)*n])==1 for a in range(2))
                outside+=any(x < 0 or x > 1 for x in uh)
                max_error=max(max_error,error);max_bound=max(max_bound,bound);checked+=1
        bounds.append({'entry_error':str(epsilon),'invertible_checks':checked,
            'singular_cases':singular,'raw_nonstochastic_cases':outside,
            'maximum_reconstruction_entry_error':float(max_error),
            'maximum_certificate':float(max_bound)})
    return {'gamma':str(gamma),'reward':list(map(str,reward)),
        'policies':choices,'values':[[str(x) for x in v] for v in values],
        'action_kernels':[[[str(x) for x in row] for row in k] for k in kernels],
        'state_matrices':matrices,'exact_determinants':determinants,
        'inverse_row_sum_norms':inverse_norms,'precision_seed':61901,'precision_panel':bounds}


def coverage_cases():
    rng=random.Random(61902);checks=0
    for _ in range(40):
        n=3;actions=2;gamma=F(3,4);eye=identity(n)
        kernels=[]
        for a in range(actions):
            raw=[[F(rng.randint(1,9)) for j in range(n)] for i in range(n)]
            kernels.append([[x/sum(row) for x in row] for row in raw])
        for theta,tau in product((F(1),F(1,2),F(1,10)),repeat=2):
            r=[[theta*eye[i][j]+(1-theta)/n for j in range(n)] for i in range(n)]
            mix=[[tau*F(k==a)+(1-tau)/actions for a in range(actions)] for k in range(actions)]
            reconstructed=[]
            for k in range(actions):
                pi=[mix[k] for _ in range(n)]
                vv=[value(kernels,pi,list(column),gamma) for column in zip(*r)]
                v=[list(row) for row in zip(*vv)]
                m=mm(v,inverse(r));mi=inverse(m)
                reconstructed.append([[(eye[i][j]-mi[i][j])/gamma for j in range(n)]for i in range(n)])
            for i in range(n):
                assert mm(inverse(mix),[p[i] for p in reconstructed]) == [k[i] for k in kernels]
                checks+=1
        # Missing policy coverage: equal mixtures cannot distinguish a
        # positive mass transfer in one action from its opposite in the other.
        changed=[[row[:] for row in k] for k in kernels]
        step=min(kernels[a][0][j] for a in range(2) for j in range(3))/2
        for a in range(2):
            changed[a][0][0]+=(-1)**a*step
            changed[a][0][1]-=(-1)**a*step
        assert changed != kernels
        for reward in ([F(0),F(1),F(3)],*identity(n)):
            pi=[[F(1,2),F(1,2)] for _ in range(n)]
            assert value(kernels,pi,reward,gamma) == value(changed,pi,reward,gamma)
            checks+=1
    return {'positive_models':40,'seed':61902,'exact_reconstruction_and_missing_coverage_checks':checks}


def near_constant_and_frontier():
    gamma=F(1,2);eye=identity(2)
    p=[[[1-rho,rho],[rho,1-rho]] for rho in (F(1,5),F(2,5))]
    m=[inverse([[eye[i][j]-gamma*k[i][j] for j in range(2)] for i in range(2)])for k in p]
    rows=[]
    for theta in (F(1),F(1,10),F(1,100),F(1,1000),F(0)):
        r=[[theta*eye[i][j]+(1-theta)/2 for j in range(2)]for i in range(2)]
        vv=[mm(k,r) for k in m]
        assert norm(difference(p[0],p[1])) == F(2,5)
        assert all(abs(x)==10*theta/63 for row in difference(*vv) for x in row)
        rows.append({'theta':str(theta),'model_row_distance':'2/5',
                     'maximum_value_entry_difference':str(10*theta/63)})
    frontier=0
    for u0,u1 in product(map(F,(-2,-1,0,1,2)),repeat=2):
        values=[]
        for mixture in (F(1,4),F(3,4)):
            action_values=[u0,u1,mixture*u0+(1-mixture)*u1]
            values.append(max(action_values))
            assert max(action_values)==max(u0,u1)
            frontier+=1
        assert values[0]==values[1]
    return {'near_constant':rows,'frontier_checks':frontier,
            'named_action_C_probability_values':['1/4','3/4'],
            'C_value_for_reward_1_0':['1/4','3/4']}


def four_state_witness():
    n=4;gamma=F(3,4);reward=list(map(F,(0,1,3,7)))
    kernels=[[[F(4,5)*F(j==(i+step)%n)+F(1,20) for j in range(n)]
              for i in range(n)] for step in (1,2)]
    choices=((0,0,0,0),(1,1,1,1),(0,0,1,1),(1,1,0,0),(0,1,0,1),(1,0,1,0))
    policies=[[[F(a==pi[i]) for a in range(2)] for i in range(n)] for pi in choices]
    values=[value(kernels,pi,reward,gamma) for pi in policies]
    determinants=[]
    for i in range(n):
        b,r=system(i,policies,values,[reward]*len(policies),gamma)
        d=det(b)
        assert d
        assert mv(inverse(b),r) == [kernels[a][i][j] for a in range(2) for j in range(n)]
        determinants.append(str(d))
    return {'gamma':str(gamma),'reward':list(map(str,reward)),'policies':choices,
            'values':[[str(x) for x in row] for row in values],
            'action_kernels':[[[str(x) for x in row] for row in k] for k in kernels],
            'exact_determinants':determinants,'exact_state_reconstructions':n}


def all_policy_ambiguity():
    n=3;reward=list(map(F,(0,1,3)))
    base=[[[F(1,3) for j in range(n)] for i in range(n)] for a in range(2)]
    changed=[[row[:] for row in k] for k in base]
    changed[0][0]=list(map(lambda x:F(x,30),(8,13,9)))
    checks=0
    for gamma in (F(1,4),F(1,2),F(3,4)):
        expected=[r+gamma*F(4,3)/(1-gamma) for r in reward]
        for probs in product((F(0),F(1,2),F(1)),repeat=3):
            pi=[[1-p,p] for p in probs]
            assert value(base,pi,reward,gamma)==expected
            assert value(changed,pi,reward,gamma)==expected
            checks+=2
    return {'reward':list(map(str,reward)),'base_row':['1/3']*3,
            'changed_action_zero_state_zero_row':['4/15','13/30','3/10'],
            'exact_value_checks':checks,'scope':'proof covers all stationary policies and all discounts in (0,1)'}


def main():
    out={'status':'passed','observation_contract':'supplied values, not a sampled learner',
        'witness':witness(),'four_state_witness':four_state_witness(),'all_policy_ambiguity':all_policy_ambiguity(),'coverage':coverage_cases(),'limits':near_constant_and_frontier()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'passed','determinants':out['witness']['exact_determinants'],
        'four_state_determinants':out['four_state_witness']['exact_determinants'],
        'precision':out['witness']['precision_panel'],'coverage':out['coverage']},indent=2))


if __name__=='__main__':main()
