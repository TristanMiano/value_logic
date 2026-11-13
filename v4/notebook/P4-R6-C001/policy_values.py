"""Rational checks of rollout and single-value policy reconstruction; GPT-6."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def identity(n):
    return [[F(i==j) for j in range(n)] for i in range(n)]


def inverse(matrix):
    n=len(matrix)
    aug=[list(row)+identity(n)[i] for i,row in enumerate(matrix)]
    for col in range(n):
        pivot=next(i for i in range(col,n) if aug[i][col])
        aug[col],aug[pivot]=aug[pivot],aug[col]
        scale=aug[col][col]
        aug[col]=[v/scale for v in aug[col]]
        for row in range(n):
            if row!=col:
                factor=aug[row][col]
                aug[row]=[x-factor*y for x,y in zip(aug[row],aug[col])]
    return [row[n:] for row in aug]


def mv(matrix, vector):
    return [sum(x*y for x,y in zip(row,vector)) for row in matrix]


def induced(prob):
    n=len(prob)
    return [[(1-prob[s] if j==(s+1)%n else prob[s] if j==(s+2)%n else F(0))
             for j in range(n)] for s in range(n)]


def main():
    n=3; gamma=F(3,4); ident=identity(n); reward=[F(0),F(1),F(3)]
    codes=set(); constant_values=set(); single_recovered=0; ambiguous=0
    approximation_checks=0; deterministic_checks=0
    examples=[]
    for prob in product((F(0),F(1,4),F(1,2),F(3,4),F(1)),repeat=n):
        p=induced(prob)
        m=inverse([[ident[i][j]-gamma*p[i][j] for j in range(n)] for i in range(n)])
        minv=inverse(m)
        recovered=[[ (ident[i][j]-minv[i][j])/gamma for j in range(n)] for i in range(n)]
        assert recovered==p
        assert tuple(recovered[s][(s+2)%n] for s in range(n))==prob
        codes.add(tuple(v for row in m for v in row))
        const=tuple(mv(m,[F(1)]*n)); constant_values.add(const)
        assert const==(1/(1-gamma),)*n
        v=mv(m,reward)
        q=[[reward[s]+gamma*v[(s+1+a)%n] for a in range(2)] for s in range(n)]
        gaps=[abs(row[1]-row[0]) for row in q]
        if min(gaps)==0:
            ambiguous+=1
            continue
        recovered_prob=tuple((v[s]-q[s][0])/(q[s][1]-q[s][0]) for s in range(n))
        assert recovered_prob==prob
        single_recovered+=1
        epsilon=min(gaps)/(8*gamma)
        for signs in product((-1,1),repeat=n):
            vh=[v[s]+signs[s]*epsilon for s in range(n)]
            qh=[[reward[s]+gamma*vh[(s+1+a)%n] for a in range(2)] for s in range(n)]
            for s in range(n):
                ph=(vh[s]-qh[s][0])/(qh[s][1]-qh[s][0])
                ph=max(F(0),min(F(1),ph))
                bound=(1+gamma)*epsilon/(gaps[s]-2*gamma*epsilon)
                assert abs(ph-prob[s])<=bound
                approximation_checks+=1
        if all(x in (0,1) for x in prob):
            epsilon=min(gaps)/(4*(1+gamma))
            for signs in product((-1,1),repeat=n):
                vh=[v[s]+signs[s]*epsilon for s in range(n)]
                for s in range(n):
                    residual=[abs(vh[s]-reward[s]-gamma*vh[(s+1+a)%n]) for a in range(2)]
                    chosen=min(range(2),key=lambda a:residual[a])
                    assert chosen==prob[s]
                    deterministic_checks+=1
        if prob==(F(1,4),F(1,2),F(3,4)):
            examples.append({'policy_action_one_probabilities':[str(x) for x in prob],
                             'transition_matrix':[[str(x) for x in row] for row in p],
                             'occupancy_values':[[str(x) for x in row] for row in m],
                             'single_reward_values':[str(x) for x in v],
                             'action_value_gaps':[str(x) for x in gaps]})
    assert len(codes)==125 and len(constant_values)==1
    result={'status':'passed','policies':125,'distinct_occupancy_value_matrices':len(codes),
            'distinct_constant_reward_values':len(constant_values),
            'single_value_separated_policies':single_recovered,
            'single_value_ambiguous_policies':ambiguous,
            'stochastic_precision_inequalities':approximation_checks,
            'deterministic_precision_decisions':deterministic_checks,
            'gamma':str(gamma),'reward':[str(x) for x in reward], 'examples':examples}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
