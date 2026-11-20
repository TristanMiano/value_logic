"""Recover the current task without telling the observer when it changed."""
import sys
from pathlib import Path
from statistics import mean, median

import numpy as np
from scipy.special import logsumexp

from bandit_monitor import ARMS, GAP, LAYOUTS, choices_at, job_cents, log_return, read


def unknown_schedule(series, difficulty, truth, unchanged, known_day=None, min_active=2):
    # Start 71 represents an unchanged room through the end of the experiment.
    hypotheses=[(old,old,71) for old in ARMS]
    hypotheses += [(old,new,t) for old,new in LAYOUTS for t in range(2,71)]
    if known_day is not None:
        hypotheses=[(old,new,known_day) for old,new in LAYOUTS]
    old,new,start=np.array(hypotheses).T
    weights=(np.full(6,1/6) if known_day is not None else
             np.where(start==71,unchanged/3,(1-unchanged)/(6*69)))
    assert np.isclose(weights.sum(),1)
    net=np.zeros(len(weights))
    keep=np.ones(len(weights),dtype=bool)
    accuracy=[]
    first_good=None
    first_dates=[]
    wrong=False
    dates=[]
    cash=cash_for_earnings=0.
    middle, high, low=job_cents((0,1),difficulty)
    for t in range(1,71):
        best=np.where(t>=start,new,old)
        posterior=np.exp(np.log(weights)+net-logsumexp(np.log(weights)+net))
        options=np.bincount(best,weights=posterior,minlength=3)
        choices=series.get(t,())
        if t>40 and len(choices)>=min_active:
            decision=choices_at(options)
            accuracy.append(decision[truth[1]])
            cash+=decision@job_cents(truth,difficulty)
            expected_money=np.array([low+(middle-low)*posterior[old==a].sum()
                                     +(high-low)*posterior[(new==a)&(t>=start)].sum() for a in ARMS])
            cash_for_earnings+=choices_at(expected_money)@job_cents(truth,difficulty)
            live=set(best[keep])
            if len(live)==1:
                if truth[1] in live:
                    if first_good is None:
                        first_good=t
                        first_dates=sorted(set(start[keep]))
                else:
                    wrong=True
        if t==70:
            dates=sorted(set(start[keep]))
            break
        for receipt in choices:
            logs=[log_return(float(receipt.reward*100),3.1-(2-j)*GAP[difficulty],.55)
                  for j in range(3)]
            grade=np.where((t>=start)&(receipt.arm==new),2,(receipt.arm==old).astype(int))
            net+=np.take(logs,grade)
        keep &= logsumexp(np.log(weights)+net)-net < np.log(20)
    return (mean(accuracy) if accuracy else None),first_good,wrong,dates,cash,cash_for_earnings,first_dates


def main(path):
    rooms=read(path)
    scheduled={name:unknown_schedule(s,b[0],answer,0,known_day=41) for name,b,s,answer in rooms}
    for null in (.1,.5,.9):
        for diff in GAP:
            outcomes=[unknown_schedule(s,diff,answer,null) for _,b,s,answer in rooms if b[0]==diff]
            known=[scheduled[name] for name,b,_,_ in rooms if b[0]==diff]
            if null==.5:
                first=[v[6] for v in outcomes if v[1] is not None]
                print("First correct action: count, exact true date, no-change still possible, median schedules",
                      len(first),sum(s==[41] for s in first),sum(71 in s for s in first),
                      median(map(len,first)) if first else None)
            print("Exact change day at 70, extra cents from knowing the schedule",
                  sum(v[3]==[41] for v in outcomes),round(mean(k[4]-v[4] for k,v in zip(known,outcomes)),4))
            print("Decision for money minus most likely winner, unknown/known date; calendar gain under money",
                  *[round(x,4) for x in (mean(v[5]-v[4] for v in outcomes),
                                         mean(k[5]-k[4] for k in known),
                                         mean(k[5]-v[5] for k,v in zip(known,outcomes)))])
            first=[v[1] for v in outcomes if v[1] is not None]
            dated=[v[3] for v in outcomes if v[3] and 71 not in v[3]]
            print("Unchanged prior / difficulty",null,diff,"accuracy, correct rooms, wrong rooms, median first",
                  round(mean(v[0] for v in outcomes),5),len(first),sum(v[2] for v in outcomes),
                  median(first) if first else None)
            print("Change required at 70, median compatible date count/span, true day removed",
                  len(dated),median(len(x) for x in dated) if dated else None,
                  median(x[-1]-x[0] for x in dated) if dated else None,
                  sum(41 not in v[3] for v in outcomes))


    # Enrol from pre-change records only, then count licenses before any
    # subsequent active round, including rooms that continued with one worker.
    whole=read(path,eligible_only=False)
    for diff in GAP:
        sub=[unknown_schedule(s,diff,answer,.5,min_active=1) for _,b,s,answer in whole
             if b[0]==diff and any(s.get(t) for t in range(1,41))]
        print("Prospective cohort",diff,"enrolled / active after / ever right / ever wrong",
              len(sub),sum(x[0] is not None for x in sub),
              sum(x[1] is not None for x in sub),sum(x[2] for x in sub))


if __name__=="__main__":
    main(Path(sys.argv[1]))
