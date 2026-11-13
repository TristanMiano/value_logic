"""Exact capability and information examples; Codex (GPT-6), W6."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def laws(channel):
    out=[]
    for policy in product(range(2), repeat=len(channel[0])):
        out.append(tuple(sum(F(1, 2)*channel[t][s] for s in range(len(policy))
                             if policy[s] == a) for t in range(2) for a in range(2)))
    return out


def support(points, direction):
    return max(sum(x*y for x,y in zip(point,direction)) for point in points)


def main():
    e=[[F(4,5), F(1,5)], [F(1,5),F(4,5)]]
    garble=[[F(3,4),F(1,4)],[F(1,4),F(3,4)]]
    f=[[sum(e[t][s]*garble[s][a] for s in range(2)) for a in range(2)] for t in range(2)]
    assert f == [[F(13,20),F(7,20)],[F(7,20),F(13,20)]]
    ep,fp= laws(e),laws(f)
    relabeled= laws([row[::-1] for row in e])
    strict=0
    for payoff in product((-1,0,1),repeat=4):
        ve,vf=support(ep,payoff), support(fp,payoff)
        assert ve >= vf
        assert ve == support(relabeled,payoff)
        strict += ve > vf
    state_independent=0
    for ua in product((-2,-1,0,1,2),repeat=2):
        payoff=ua+ua
        assert support(ep,payoff) == support(fp,payoff)
        state_independent += 1
    d=8
    full_codes=set(); first_codes=set()
    for b in product((0,1), repeat=d):
        points=[(0,)*d]+[tuple(int(i==j) for j in range(d)) for i in range(d) if b[i]]
        code=tuple(support(points,tuple(int(i==j) for j in range(d))) for i in range(d))
        assert code == b
        full_codes.add(code); first_codes.add(code[0])
    assert len(full_codes)==2**d and len(first_codes)==2
    # Fixed-total outcome laws allow signed weights to be shifted and scaled
    # into simplex weights without changing which outcome is best.
    simplex_checks=0
    for points in (ep, fp, relabeled):
        for w in product((-2,-1,0,1,2), repeat=4):
            b=1-min(w)
            a=sum(x+b for x in w)
            simplex=tuple(F(x+b,a) for x in w)
            assert support(points,w) == a*support(points,simplex)-b
            simplex_checks += 1
    # Removing the fixed-total assumption separates the positive queries.
    assert support([(0,), (1,)], (1,)) == support([(1,)], (1,))
    assert support([(0,), (1,)], (-1,)) != support([(1,)], (-1,))
    result={'status':'passed','payoff_tables':81,'strict_information_improvements':strict,
            'state_independent_payoff_ties':state_independent,
            'channel_e':[[str(x) for x in row] for row in e],
            'channel_f':[[str(x) for x in row] for row in f],
            'garbling':[[str(x) for x in row] for row in garble],
            'capability_dimension':d,'distinct_full_value_codes':len(full_codes),
            'distinct_single_goal_codes':len(first_codes),
            'fixed_total_signed_query_reconstructions':simplex_checks}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
