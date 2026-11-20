"""W7.4. Exact coverage available to excluded ballots with a prior guarantee."""
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from budget_data import additive, coverage_counts, read_ballots, ticket_weights


def minimal(ballots):
    antichain=[]
    for b in sorted(ballots,key=lambda b:(b.bit_count(),b)):
        if not any(a&b==a for a in antichain):
            antichain.append(b)
    return antichain


def solve(directory):
    strata={}
    record,projects,ballots=read_ballots(directory/"Poland_Warszawa_2020_Wesola.pb",strata)
    costs=np.array([int(r["cost"]) for r in projects],dtype=np.int64)
    official=sum(1<<i for i,r in enumerate(projects) if r["selected"]=="1")
    budget=int(record["budget"])
    spent=additive(costs)
    masks=np.arange(len(spent),dtype=np.int32)
    maximal=spent<=budget
    for j,cost in enumerate(costs):
        maximal &= ((masks&(1<<j))!=0) | (spent+cost>budget)
    slates=masks[maximal]
    old=minimal(b for b in ballots if b&official)
    new=minimal(b for b in ballots if not b&official)
    all_rows=old+new
    patterns=np.array([(slates & b)!=0 for b in all_rows],dtype=np.int64)
    # Any feasible slate extends to a maximal one without lowering coverage.
    # Identical columns offer exactly the same protections.
    _,index=np.unique(np.sum(patterns*(1<<np.arange(len(all_rows)))[:,None],axis=0),
                      return_index=True)
    matrix=patterns[:,index]
    ncols=len(index)
    indicator=np.r_[np.zeros(len(old)),np.ones(len(new))]
    print("Old/new minimal ballots, maximal slates, distinct protection patterns",
          len(old),len(new),len(slates),ncols)
    caps=[]
    for risk in (F(0),F(1,100),F(1,20),F(1,10),F(1,5),F(759,2089)):
        keep=1-risk
        res=linprog(np.r_[np.zeros(ncols),-1],
                    A_ub=np.column_stack((-matrix,indicator)),b_ub=np.r_[np.full(len(old),-float(keep)),np.zeros(len(new))],
                    A_eq=[np.r_[np.ones(ncols),0]],b_eq=[1],
                    bounds=[(0,None)]*ncols+[(None,None)],method="highs")
        assert res.success
        active=res.x[:-1]>1e-10
        weights,den=ticket_weights(res.x[:-1][active])
        assert weights.sum()==den
        cover=matrix[:,active]@weights
        assert F(int(min(cover[:len(old)])),den)>=keep
        value=F(int(min(cover[len(old):])),den)
        prices,unit=ticket_weights(np.maximum(0,-res.ineqlin.marginals))
        assert sum(prices[len(old):])==unit
        upper=F(int(max(prices@patterns)),unit)-keep*F(int(sum(prices[:len(old)])),unit)
        assert value==upper
        if risk == F(1,100):
            assert sum(prices[:len(old)])==3*unit and max(prices@patterns)==3*unit
            print("Global support line for old risk / new minimum: slope three, intercept zero")
        caps.append(value)
        print("Allowed individual prior risk",risk,"best newly represented minimum",value,
              float(value),"lottery size",active.sum())
    # Maintain mean coverage in each predeclared voting channel and ballot
    # length group while keeping every prior beneficiary safe with 95% chance.
    thresholds=[]
    extra=[]
    for _,counts in sorted(strata.items()):
        served=coverage_counts(len(costs),counts)
        extra.append(served[slates])
        thresholds.append(int(served[official]))
    all_constraints=np.vstack((patterns,extra))
    rhs=np.r_[np.full(len(old),0.95),np.zeros(len(new)),thresholds]
    row_z=np.r_[indicator,np.zeros(len(extra))]
    res=linprog(np.r_[np.zeros(len(slates)),-1.],
                A_ub=np.column_stack((-all_constraints,row_z)),b_ub=-rhs,
                A_eq=[np.r_[np.ones(len(slates)),0.]],b_eq=[1.],
                bounds=[(0,None)]*len(slates)+[(None,None)],method="highs")
    assert res.success
    used=res.x[:-1]>1e-10
    mass,den=ticket_weights(res.x[:-1][used])
    assert sum(mass)==den
    actual=all_constraints[:,used]@mass
    assert 20*min(actual[:len(old)])>=19*den
    assert all(v>=h*den for v,h in zip(actual[len(all_rows):],thresholds))
    new_min=F(int(min(actual[len(old):len(all_rows)])),den)
    dual,scale=ticket_weights(np.maximum(0,-res.ineqlin.marginals))
    assert sum(dual[len(old):len(all_rows)])==scale
    upper=(F(int(max(dual@all_constraints)),scale)-F(19,20)*F(int(sum(dual[:len(old)])),scale)
           -F(sum(h*int(y) for h,y in zip(thresholds,dual[len(all_rows):])),scale))
    assert upper==new_min
    print("95% prior protection and all five group means protected: excluded minimum",new_min,
          "lottery size",sum(used))
    for (label,counts),num,orig in zip(sorted(strata.items()),actual[len(all_rows):],thresholds):
        gain=F(int(num),den)-orig
        print("Protected group",label,"old/expected covered",orig,F(int(num),den),
              "change in percentage points",round(float(100*gain/sum(counts.values())),4))
    return caps


if __name__=="__main__":
    solve(Path(sys.argv[1]))
