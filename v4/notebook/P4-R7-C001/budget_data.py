"""W7.4. Feasible public offers on two Pabulib records (NumPy and SciPy).

Only project costs, selections and approval sets enter the calculation.
Run with the directory containing both pinned .pb files as the argument.
"""
import csv
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import lcm
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog


SOURCES={
    "Poland_Warszawa_2020_Wesola.pb":"823c6b7489bd52d37d996ad6421ed8bb8eb1334575509eff50bdaaae1a31fbe3",
    "Poland_Warszawa_2020_Zoliborz.pb":"c4573c6c709d125f80fcc3a411d9cf0a9fd117047280bdea9ef81d92b0c56985",
}


def read_ballots(path):
    data=path.read_bytes()
    assert sha256(data).hexdigest()==SOURCES[path.name],"unexpected data revision"
    lines=[line for line in data.decode("utf-8-sig").splitlines() if line.strip()]
    a,b=lines.index("PROJECTS"),lines.index("VOTES")
    headers=csv.DictReader(lines[1:a],delimiter=";")
    meta={r["key"]:r["value"] for r in headers}
    projects=list(csv.DictReader(lines[a+1:b],delimiter=";"))
    lookup={r["project_id"]:j for j,r in enumerate(projects)}
    ballots=Counter()
    for r in csv.DictReader(lines[b+1:],delimiter=";"):
        choices=set(r["vote"].split(",")) if r["vote"] else set()
        ballots[sum(1<<lookup[p] for p in choices)]+=1
    assert meta["vote_type"]=="approval" and meta["rule"]=="greedy"
    assert len(lookup)==int(meta["num_projects"]) and sum(ballots.values())==int(meta["num_votes"])
    return meta,projects,ballots


def additive(weights):
    values=np.zeros(1<<len(weights),dtype=weights.dtype)
    for j,c in enumerate(weights):
        size=1<<j
        values[size:2*size]=values[:size]+c
    return values


def coverage_counts(n,ballots):
    # Zeta transform: a ballot is missed iff it is contained in the complement.
    missed=np.zeros(1<<n,dtype=np.int32)
    for mask,count in ballots.items():
        missed[mask]=count
    for j in range(n):
        stride=1<<j
        blocks=missed.reshape(-1,2*stride)
        blocks[:,stride:]+=blocks[:,:stride]
    return sum(ballots.values())-missed[::-1]


def ticket_weights(probabilities):
    # Recover a rational candidate from the solver. Optimality is established
    # below by exact feasible-slate enumeration, independently of the floats.
    rational=[F(float(max(0,p))).limit_denominator(100000) for p in probabilities]
    denominator=lcm(*(w.denominator for w in rational))
    integers=[int(w*denominator) for w in rational]
    if sum(integers)>10**12:
        raise ArithmeticError("could not reconstruct a small rational certificate")
    return np.array(integers,dtype=np.int64),denominator


def lottery(n,singles,feasible,coverage,tally,initial,min_target=None):
    # The primary game has one constraint per inclusion-minimal ballot.
    # Here all of those ballots are singletons. At the second stage retain
    # their certified minimum and maximize mean approval-set coverage.
    columns=list(dict.fromkeys(int(v) for v in initial))
    for _ in range(1500):
        bits=np.array([[(mask>>j)&1 for mask in columns] for j in singles],dtype=float)
        if min_target is None:
            obj=np.r_[np.zeros(len(columns)),-1.]
            inequalities=np.column_stack([-bits,np.ones(len(singles))])
            bounds=np.zeros(len(singles))
            equal=np.r_[np.ones(len(columns)),0.]
        else:
            obj=-coverage[columns].astype(float)
            inequalities=-bits
            bounds=np.full(len(singles),-float(min_target))
            equal=np.ones(len(columns))
        res=linprog(obj,A_ub=inequalities,b_ub=bounds,A_eq=[equal],b_eq=[1.],
                    method="highs",options={"dual_feasibility_tolerance":1e-9,
                                             "primal_feasibility_tolerance":1e-9})
        if not res.success:
            raise RuntimeError(res.message)
        y=np.maximum(0,-res.ineqlin.marginals)
        unit=np.zeros(n)
        unit[singles]=y
        price=additive(unit)
        if min_target is not None:
            price+=coverage
        price[~feasible]=-np.inf
        entrant=int(np.argmax(price))
        if price[entrant]<=-res.eqlin.marginals[0]+2e-9:
            break
        if entrant in columns:
            raise ArithmeticError("inconsistent pricing certificate")
        columns.append(entrant)
    else:
        raise ArithmeticError("column generation did not finish")
    chosen=np.array(columns,dtype=np.int32)
    tickets,denominator=ticket_weights(res.x[:len(columns)])
    assert tickets.sum()==denominator
    chosen,tickets=chosen[tickets>0],tickets[tickets>0]
    total=int(tickets.sum())
    minimum=F(min(int(tickets[(chosen&(1<<j))!=0].sum()) for j in singles),total)
    avg=F(int(coverage[chosen]@tickets),tally*total)
    dual,dual_denom=ticket_weights(y)
    weights=np.zeros(n,dtype=np.int64)
    weights[singles]=dual
    integer_prices=additive(weights)
    if min_target is None:
        assert int(dual.sum())==dual_denom
        upper=F(int(integer_prices[feasible].max()),dual_denom)
        assert minimum==upper
    else:
        # For any lottery meeting gamma: mean <= max_S(g(S)+y(S))-gamma*sum(y).
        prices=integer_prices+coverage.astype(np.int64)*dual_denom
        upper=F(int(prices[feasible].max()),tally*dual_denom)-min_target*F(int(dual.sum()),tally*dual_denom)
        assert minimum>=min_target and avg==upper
    return minimum,avg,upper,chosen,tickets


def evaluate(path):
    meta,projects,ballots=read_ballots(path)
    n=len(projects)
    costs=np.array([int(r["cost"]) for r in projects],dtype=np.int64)
    official=sum(1<<j for j,r in enumerate(projects) if r["selected"]=="1")
    budget=int(meta["budget"])
    tally=sum(ballots.values())
    baseline=sum(w for v,w in ballots.items() if v&official)
    spent=sum(int(costs[j]) for j in range(n) if official&(1<<j))
    print(path.stem.rsplit("_",1)[1],"projects/ballots/represented",n,tally,baseline,
          "budget/official cost",budget,spent,"empty ballots",ballots[0])
    assert ballots[0]==0 and spent<=budget
    if sum(costs)<=budget:
        assert official==(1<<n)-1 and baseline==tally
        print("All projects fit; unanimous coverage at official outcome.")
        return
    singles=[j for j in range(n) if ballots[1<<j]>0]
    essentials=sum(1<<j for j in singles)
    assert all(v&essentials for v in ballots),"a non-singleton minimum needs its own constraint"
    print("Required singleton projects and total cost",len(singles),sum(costs[singles]))
    masks=np.arange(1<<n,dtype=np.int32)
    feasible=additive(costs)<=budget
    coverage=coverage_counts(n,ballots)
    assert coverage[official]==baseline
    maxmean=int(coverage[feasible].max())
    protected=coverage_counts(n,{v:w for v,w in ballots.items() if v&official})
    weak=feasible & (protected==baseline)
    best_safe=int(coverage[weak].max())
    choices=masks[weak & (coverage==best_safe)]
    example=int(choices[np.argmin(additive(costs)[choices])])
    ids=[r["project_id"] for r in projects]
    def selected(mask):
        return [p for j,p in enumerate(ids) if mask&(1<<j)]
    count_loss=sum(w for v,w in ballots.items() if (v&example).bit_count()<(v&official).bit_count())
    print("Best mean count / best retaining all former coverage",maxmean,best_safe,
          "example changes: remove/add",selected(official & ~example),selected(example & ~official),
          "reduced approved-project count on example",count_loss)
    # Any count-preserving lottery must retain every prior winner appearing
    # on a ballot consisting entirely of such winners, with probability one.
    union=0
    fully_served=0
    for v,w in ballots.items():
        if v & ~official==0:
            union|=v
            fully_served+=w
    assert union==official
    losers=[]
    for alternative in masks[weak & (coverage>baseline)].tolist():
        losers.append(sum(w for v,w in ballots.items()
                          if (v&alternative).bit_count()<(v&official).bit_count()))
    print("Only prior winners approved on",fully_served,"ballots; union covers all",official.bit_count(),
          "prior winners; number of coverage-preserving slates",int(weak.sum()),
          "fewest count losses when coverage strictly expands",min(losers))
    initial=[1<<j for j in singles]+[official,example,int(np.flatnonzero(feasible&(coverage==maxmean))[0])]
    lower,avg,upper,support,_=lottery(n,singles,feasible,coverage,tally,initial)
    print("Worst-ballot coverage certified",lower,float(upper),"support",len(support))
    target=lower
    worst,average,bound,cols,tickets=lottery(n,singles,feasible,coverage,tally,
                                     initial+support.tolist(),target)
    print("Best mean with exact worst coverage; worst/mean/upper",
          worst,average,float(bound),"support",len(cols))
    # The old/unrepresented mixture is an explicit prior over one's future
    # ballot. A different optimum could distribute gains differently.
    # Pinned schedule for the two-constituency calculation, since optimizing
    # the primary and secondary objectives need not specify all ticket weights.
    # Bit j selects the j-th project in the pinned source, indexed from zero.
    witness=[(1371147,47),(1183151,297),(1396620,186),(510757,220),(518022,15),
             (1435050,224),(1368876,54),(1566218,162),(502444,118),(475309,56),
             (321317,23),(192043,101),(1190951,135),(240519,209),(1336233,85),
             (1435267,140),(191269,17)]
    cols,tickets=map(np.array,zip(*witness))
    total=int(tickets.sum())
    assert all(feasible[cols]) and total==2089
    assert F(min(int(tickets[(cols & (1 << j))!=0].sum()) for j in singles),total)==lower
    assert F(int(coverage[cols]@tickets),tally*total)==average
    in_old=F(int(protected[cols]@tickets),baseline*total)
    in_missed=F(int((coverage[cols]-protected[cols])@tickets),(tally-baseline)*total)
    crossing=(1-in_old)/(1-in_old+in_missed)
    assert F(baseline,tally)*in_old+F(tally-baseline,tally)*in_missed==average
    print("Award coverage under one exact efficient lottery: originally represented / unrepresented",
          in_old,in_missed,"prior probability of exclusion above which it beats official",
          crossing,float(crossing))
    costs_all=additive(costs)
    cheapest=int(min(costs[j] for j in range(n) if not official&(1<<j)))
    extra_subset=next(1<<j for j in range(n) if not official&(1<<j) and costs[j]==cheapest)
    print("Minimal added budget to improve counts / reach all / do both",
          spent+cheapest-budget,int(costs_all[essentials])-budget,
          int(costs_all[essentials|official])-budget,
          "newly represented on cheapest extension",coverage[official|extra_subset]-baseline)
    print("Full arbitrary approved-project weights: slack / least unfunded cost",
          budget-spent,min(int(costs[j]) for j in range(n) if not (official&(1<<j))))


if __name__=="__main__":
    for filename in SOURCES:
        evaluate(Path(sys.argv[1])/filename)
