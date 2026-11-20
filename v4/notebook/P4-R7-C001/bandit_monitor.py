"""Pre-round identification of a hidden payoff change in the Toyokawa et al. archive."""
import csv
from collections import Counter, defaultdict
from decimal import Decimal
from hashlib import sha256
from itertools import permutations
from functools import lru_cache
from pathlib import Path
from statistics import mean, median
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.special import betaln, log_ndtr, logsumexp, ndtr, xlogy

from bandit_data import ARMS, Choice, EXPECTED, select_room


GAP={"25%":1.264,"50%":.742,"78%":.3}
LAYOUTS=list(permutations(ARMS,2))
# Old and new best arm, in the published server condition switch.
PROGRAM={1:(2,0),2:(2,1),3:(1,0),4:(1,2),5:(0,1),6:(0,2)}


def read(path, eligible_only=True):
    assert sha256(path.read_bytes()).hexdigest()==EXPECTED
    data=defaultdict(lambda:defaultdict(list))
    block={}
    answer={}
    with path.open(encoding="utf8",newline="") as source:
        for row in csv.DictReader(source):
            name,t=row["room"],int(row["round"])
            b=(row["taskDifficulty"],row["expNum"])
            assert name not in block or block[name]==b
            block[name]=b
            old,new=PROGRAM[int(row["condition"])]
            arm=int(row["machine"])
            grade=3 if t>40 and arm==new else (2 if arm==old else 1)
            assert grade==int(row["performance"]) and (name not in answer or answer[name]==(old,new))
            answer[name]=(old,new)
            data[name][t].append(Choice(int(row["machine"]),int(row["performance"]),
                                        Decimal(row["result"])))
    return [(name,block[name],series,answer[name]) for name,series in sorted(data.items())
            if not eligible_only or select_room(series)]


def shares(s,first,last):
    counts=Counter(v.arm for t in range(first,last) for v in s.get(t,()))
    total=sum(counts.values())
    return np.array([counts[a]/total for a in ARMS]) if total else np.full(3,1/3)


def public_features(s,t,difficulty):
    pre=shares(s,1,41)
    post=shares(s,41,t)
    recent=shares(s,max(41,t-3),t)
    ten=shares(s,max(41,t-10),t)
    old_end=shares(s,31,41)
    shift=post-pre
    after=(t-41)/30
    gap=GAP[difficulty]
    vectors=[pre,old_end,post,recent,ten,shift,pre*pre,post*post,pre*post,recent-pre,
             np.isclose(pre,max(pre)).astype(float), np.isclose(post,max(post)).astype(float)]
    return np.stack(vectors+[after*v for v in (pre,post,recent,shift)]
                    +[gap*v for v in (pre,post,recent,shift)],axis=1)


def choices_at(scores):
    winners=np.isclose(scores,np.max(scores),atol=1e-11,rtol=1e-11)
    return winners/sum(winners)


@lru_cache(None)
def job_cents(layout,diff):
    old,new=layout
    # Sum P(rounded positive payout >= k hundredths); the remaining Gaussian
    # tail after ten cents is below 1e-30 even at the largest mean.
    thresholds=(np.arange(1,1001)-.5)*.01
    return np.array([.01*np.sum(ndtr((3.1-(0 if a==new else 1 if a==old else 2)*GAP[diff]-thresholds)/.55))
                     for a in ARMS])


def choice_only(rooms,fee):
    datasets=[]
    for name,block,s,answer in rooms:
        ts=[t for t in range(41,71) if len(s.get(t,()))>=2]
        x=np.stack([public_features(s,t,block[0]) for t in ts])
        datasets.append((block,answer,x))
    predictions={}
    for test in sorted(set(block for block,_,_ in datasets)):
        train=[(layout[1],x) for block,layout,x in datasets if block!=test]
        X=np.concatenate([x for _,x in train])
        Y=np.concatenate([np.full(len(x),y) for y,x in train])
        w=np.concatenate([np.full(len(x),1/(len(train)*len(x))) for _,x in train])
        labels=np.eye(3)[Y]
        def loss(beta):
            raw=X@beta
            logs=raw-logsumexp(raw,axis=1,keepdims=True)
            grad=np.einsum("ij,ijk,i->k",np.exp(logs)-labels,X,w)
            return -np.sum(w*logs[np.arange(len(Y)),Y])+fee*(beta@beta)/2,grad+fee*beta
        fit=minimize(loss,np.zeros(X.shape[-1]),jac=True,method="L-BFGS-B",
                     options={"gtol":1e-7,"maxiter":250})
        assert fit.success
        for idx,(b,answer,x) in enumerate(datasets):
            if b==test:
                decisions=np.stack([choices_at(row) for row in x@fit.x])
                predictions[idx]=(float(decisions[:,answer[1]].mean()),
                                  float((decisions@job_cents(answer,b[0])).sum()))
    return predictions


def log_return(cents,mu,sd):
    hi=(cents+.005-mu)/sd
    if cents==0:
        return log_ndtr(hi)
    lo=(cents-.005-mu)/sd
    # Reflect upper tails to avoid subtracting two numbers very close to one.
    if lo>0:
        lo,hi=-hi,-lo
    return np.log(ndtr(hi)-ndtr(lo))


@lru_cache(None)
def payoff_bins(difficulty,late,arm,sd):
    # Quarter-cent categories suffice to choose a record to inspect. The actual
    # likelihood update below still uses every recorded hundredth of a cent.
    edges=np.arange(.125,7.,.25)
    rows=[]
    for old,new in LAYOUTS:
        grade=2 if late and arm==new else int(arm==old)
        mu=3.1-(2-grade)*GAP[difficulty]
        cdf=ndtr((edges-mu)/sd)
        rows.append(np.diff(np.r_[0.,cdf,1.]))
    return np.stack(rows)


def gain_on_answer(net,difficulty,late,arm,sd):
    weights=np.exp(net-logsumexp(net))
    joint=weights[:,None]*payoff_bins(difficulty,late,arm,sd)
    answers=np.stack([sum(joint[i] for i,(_,n) in enumerate(LAYOUTS) if n==a)
                      for a in ARMS])
    p_y=answers.sum(axis=0)
    p_a=answers.sum(axis=1)
    return (xlogy(answers,answers).sum()-xlogy(p_y,p_y).sum()-xlogy(p_a,p_a).sum())


def monitor(s,difficulty,mode,seed,answer,sd=.55):
    """Never read a grade when predicting. It is used only to score afterwards."""
    gap=GAP[difficulty]
    net=np.zeros(len(LAYOUTS))
    retained=np.ones(len(net),dtype=bool)
    rng=np.random.default_rng(seed)
    hits=[]; lic=[]; reads=0; first=None; cash=0.
    for t in range(1,71):
        choices=s.get(t,())
        if t>40 and len(choices)>=2:
            weights=np.exp(net-logsumexp(net))
            prob=[sum(w for w,(_,b) in zip(weights,LAYOUTS) if b==j) for j in ARMS]
            decision=choices_at(prob)
            hits.append(decision[answer[1]])
            cash+=decision@job_cents(answer,difficulty)
            answers={j for keep,(_,j) in zip(retained,LAYOUTS) if keep}
            if len(answers)==1:
                licensed_answer=next(iter(answers))
                lic.append((t,licensed_answer))
                if first is None:
                    first=(t,reads)
        if t==70:
            break  # No further paid work or forecasts after this choice.
        if mode=="all":
            selected=choices
        else:
            selected=[]
            capped=reads<(4 if t<=40 else 14) and first is None
            if choices and ((mode=="one in five" and t%5==0) or (mode=="early random" and capped)):
                selected=[choices[rng.integers(len(choices))]]
            elif choices and mode=="targeted" and capped:
                arms=sorted({v.arm for v in choices})
                info=[gain_on_answer(net,difficulty,t>40,arm,sd) for arm in arms]
                if max(info)>.005:
                    best=[arm for arm,g in zip(arms,info) if abs(g-max(info))<=1e-10]
                    arm=best[rng.integers(len(best))]
                    options=[v for v in choices if v.arm==arm]
                    selected=[options[rng.integers(len(options))]]
        for v in selected:
            reads+=1
            y=float(v.reward*100)
            l=[log_return(y,3.1-(2-i)*gap,sd) for i in range(3)]
            net+=np.array([l[2 if t>40 and v.arm==new else (1 if v.arm==old else 0)]
                           for old,new in LAYOUTS])
        ratio=logsumexp(net)-np.log(len(net))-net
        retained &= (ratio < np.log(20))
    return mean(hits),len(lic)/len(hits),first,reads,any(a!=answer[1] for _,a in lic),cash


def log_binom_fit(success,total):
    if not total:
        return 0.
    q=success/total
    return xlogy(success,q)+xlogy(total-success,1-q)


def supremum(candidate,success,total):
    # Fit three binomials subject only to the proposed winner's weak lead.
    if not total[candidate]:
        return sum(log_binom_fit(y,n) for y,n in zip(success,total))
    pooled_y,pooled_n=success[candidate],total[candidate]
    unpooled=[]
    others=sorted((i for i in ARMS if i!=candidate and total[i]),
                  key=lambda i:success[i]/total[i],reverse=True)
    for i in others:
        if success[i]*pooled_n>pooled_y*total[i]:
            pooled_y+=success[i]
            pooled_n+=total[i]
        else:
            unpooled.append(i)
    return log_binom_fit(pooled_y,pooled_n)+sum(log_binom_fit(success[i],total[i]) for i in unpooled)


def check_order_fit():
    """Compare the pooled fit with exact rational profile maxima in small tables."""
    from fractions import Fraction as F
    from itertools import product
    from math import log
    outcomes=[(n,y) for n in range(4) for y in range(n+1)]
    checked=0
    for table in product(outcomes,repeat=3):
        n,y=zip(*table)
        for candidate in ARMS:
            others=[i for i in ARMS if i!=candidate]
            levels={F(0),F(1)}
            for flags in product((False,True),repeat=2):
                tied=[candidate]+[i for i, active in zip(others,flags) if active]
                weight=sum(n[i] for i in tied)
                if weight:
                    levels.add(F(sum(y[i] for i in tied),weight))
            levels.update(F(hits,size) for size,hits in table if size)
            def likelihood(top):
                value=1
                for i in ARMS:
                    fitted=top if i==candidate or not n[i] else min(top,F(y[i],n[i]))
                    value*=fitted**y[i]*(1-fitted)**(n[i]-y[i])
                return value
            exact=max(map(likelihood,levels))
            assert abs(log(exact)-supremum(candidate,y,n))<1e-10
            checked+=1
    print("Exact small-sample null fits",checked)


def threshold_monitor(s,answer,target):
    success=[0,0,0]; total=[0,0,0]
    survive=set(ARMS)
    first=None; wrong=False; calls=eligible=0
    for t in range(41,71):
        choices=s.get(t,())
        if len(choices)>=2:
            eligible+=1
            if len(survive)==1:
                calls+=1
                if first is None:
                    first=t
                wrong |= answer not in survive
        for v in choices:
            total[v.arm]+=1
            success[v.arm]+=int(v.reward*100>=target)
        marginal=sum(betaln(y+.5,n-y+.5)-betaln(.5,.5) for y,n in zip(success,total))
        survive={i for i in survive if marginal-supremum(i,success,total)<np.log(20)}
    return first,wrong,calls/eligible


def main(path):
    check_order_fit()
    rooms=read(path)
    print("Rooms/held-out experiment blocks",len(rooms),len(set(b for _,b,_,_ in rooms)))
    for diff in GAP:
        sub=[threshold_monitor(s,ans[1],Decimal("2.5")) for _,b,s,ans in rooms if b[0]==diff]
        found=[first for first,_,_ in sub if first is not None]
        print("Threshold monitor",diff,"licensed / total, median first round, wrong, coverage",
              len(found),len(sub),median(found) if found else None,sum(w for _,w,_ in sub),
              round(mean(c for _,_,c in sub),4))
    for penalty in (.001,.005,.02):
        scores=choice_only(rooms,penalty)
        print("Prior choices, penalty",penalty,"room-weighted accuracy",
              [(diff,round(float(mean(scores[i][0] for i,(_,b,_,_) in enumerate(rooms)
                                      if b[0]==diff)),4)) for diff in GAP])
        if penalty==.005:
            reference=scores
    for mode in ("all","one in five","early random","targeted"):
        for seed in ([731] if mode=="all" else [731,732,733]):
            result=[monitor(s,b[0],mode,seed+i,ans) for i,(_,b,s,ans) in enumerate(rooms)]
            for diff in GAP:
                sub=[r for r,(_,b,_,_) in zip(result,rooms) if b[0]==diff]
                licensed=[x[2] for x in sub if x[2] is not None]
                print(mode,seed,diff,"hit, licensed share, ever/rooms, median round/reads, mean reads, incompatible",
                      *(round(float(mean(row[j] for row in sub)),4) for j in (0,1)),
                      len(licensed),len(sub),
                      [median(v[j] for v in licensed) for j in (0,1)] if licensed else None,
                      round(mean(row[3] for row in sub),2),sum(row[4] for row in sub))
                idx=[i for i,(_,b,_,_) in enumerate(rooms) if b[0]==diff]
                gross=sum(result[i][5]-reference[i][1] for i in idx)
                reads=sum(result[i][3] for i in idx)
                print("Shadow worker, added cents per group, per receipt",round(gross/len(idx),5),
                      round(gross/reads,6) if reads else None)


if __name__=="__main__":
    main(Path(sys.argv[1]))
