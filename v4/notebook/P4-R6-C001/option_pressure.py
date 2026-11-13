"""Independent grid counts and exact option/retargeting arithmetic; GPT-6."""
from fractions import Fraction as F
from pathlib import Path
import json


def analytic(k,gamma,cost):
    if cost>=gamma: return F(0)
    return gamma*k/(k+1)-cost+cost**(k+1)/((k+1)*gamma**k)


def finite_grid(k,gamma,cost,n):
    # Each of k delayed rewards and the immediate one independently takes a
    # midpoint on the n-point grid. Count maximum levels combinatorially.
    favorable=0
    for level in range(1,n+1):
        maximum=F(2*level-1,2*n)
        value=gamma*maximum-cost
        # Count immediate reward midpoints strictly below the delayed value.
        threshold=n*value+F(1,2)
        immediate_count=max(0,min(n,(threshold.numerator-1)//threshold.denominator))
        favorable+=(level**k-(level-1)**k)*immediate_count
    return F(favorable,n**(k+1))


def main():
    rows=[]; n=4096
    for k in (1,3,9,31):
        for gamma in (F(2,5),F(3,5),F(9,10),F(1)):
            for cost in (F(0),F(1,10),gamma):
                probability=analytic(k,gamma,cost)
                grid=finite_grid(k,gamma,cost,n)
                # Rounding each continuous reward to its nearest midpoint
                # changes the two values by at most (1+gamma)/(2*n). The
                # uniform immediate reward bounds the crossing probability.
                error_bound=(1+gamma)/n
                assert abs(grid-probability)<=error_bound
                rows.append({'options':k,'discount':str(gamma),'cost':str(cost),
                             'probability_exact':str(probability),
                             'probability':float(probability),
                             'grid_probability':float(grid),
                             'absolute_error':float(abs(grid-probability)),
                             'error_bound':float(error_bound),
                             'mean_value_difference':str(gamma*k/(k+1)-cost-F(1,2))})
    # Three unfavorable atoms; two disjoint images with different weights.
    base=[F(1),F(2),F(3)]; lambdas=[F(1,2),F(2)]
    unfavorable=sum(base); favorable=sum(lam*x for lam in lambdas for x in base)
    assert favorable==sum(lambdas)*unfavorable
    conditional=favorable/(favorable+unfavorable)
    assert conditional==sum(lambdas)/(1+sum(lambdas))
    rare_cost_mean=F(99,100)*F(1,1000)-F(1,100)
    assert rare_cost_mean<0
    result={'status':'passed','grid_size':n,'settings':len(rows),
            'maximum_grid_error':max(r['absolute_error'] for r in rows),
            'weighted_retargeting_conditional_favorable_mass':str(conditional),
            'favorable_goal_fraction_rare_cost_example':'99/100',
            'mean_gain_rare_cost_example':str(rare_cost_mean),'rows':rows}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))


if __name__=='__main__': main()
