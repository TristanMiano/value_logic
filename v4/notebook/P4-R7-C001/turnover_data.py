"""Decompose changes in Chimento et al.'s cultural transmission experiment.

Pass publication v2.0 data/df_solves.Rda and data/df_surv.Rda, in order.
Uses rdata 1.0.0 and pandas. Only aggregate results are printed.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from statistics import mean, median
from math import log1p
import sys
import warnings

import rdata


SOLVES = "047e74cff3310d8a0163104405c56f2dffde6724c56548d0e00fe76ddc6c6af5"
ROSTER = "4d775b989ec0585682f404fe2c45fa4f7a1223e9ca7cfe38fef3656b61f77381"


def stage(counts, equal):
    total = sum(sum(v) for v in counts.values())
    return {i: (F(1,len(counts)) if equal else F(sum(v),total), F(v[1],sum(v)))
            for i,v in counts.items()}


def decompose(left, right, roster, cutoff):
    def average(data):
        return sum(w*p for w,p in data.values())
    a,b = average(left),average(right)
    center = (a+b)/2
    within = weight = replacements = activity = F(0)
    for i in left.keys() | right.keys():
        if i in left and i in right:
            w,p = left[i]
            v,q = right[i]
            within += (v+w)/2*(q-p)
            weight += (v-w)*((p+q)/2-center)
        else:
            if i in right:
                v,q = right[i]
                change = v*(q-center)
                assigned = roster[i][0] >= cutoff
            else:
                w,p = left[i]
                change = -w*(p-center)
                assigned = roster[i][1] <= cutoff
            if assigned:
                replacements += change
            else:
                activity += change
    assert b-a == within + weight + replacements + activity
    return (b-a,within,weight,replacements,activity)


def experienced_speed(solves):
    eligible=solves[solves.tutor.astype(str)=="0"]
    by_bird=[]
    for _,rows in eligible.groupby(["population","ID"]):
        last_count=len(rows)//10
        if not last_count:
            continue
        rows=rows.sort_values("ind_solve_count")
        assert rows.ind_solve_count.nunique()==len(rows)
        later=rows.iloc[-last_count:]
        before=rows[rows.ind_solve_count_bytype<=10]
        before=before[before.solve_speed.between(0,60)]
        pairs={}
        for rank,trial in before.groupby("ind_solve_count_bytype"):
            if len(trial)==2:
                types={str(v.Event):(v.solve_speed,v.ind_solve_count) for v in trial.itertuples()}
                assert set(types)=={"efficient","inefficient"}
                fast, slow=types["efficient"],types["inefficient"]
                pairs[rank]=(log1p(slow[0])-log1p(fast[0]),max(fast[1],slow[1]))
        if pairs and max(v[1] for v in pairs.values())<later.ind_solve_count.min():
            by_bird.append((len(pairs),mean(v[0] for v in pairs.values()),
                            mean(later.Event.astype(str)=="efficient")))
    for minimum in (3,5):
        keep=[(adv,choices) for count,adv,choices in by_bird if count>=minimum]
        print("Early matched uses >=",minimum,"eligible birds",len(keep),
              "positive / zero / negative early advantage",
              [sum((adv>0)-(adv<0)==sign for adv,c in keep) for sign in (1,0,-1)])
        for group in ([c for a,c in keep if a>0],[c for a,c in keep if a<=0]):
            print("Later majority / group size / mean share",sum(c>.5 for c in group),len(group),
                  round(mean(group),4) if group else None)
        print("Median log1p time advantage",round(median(a for a,c in keep),4))


def read(solve_path, roster_path):
    assert sha256(solve_path.read_bytes()).hexdigest()==SOLVES
    assert sha256(roster_path.read_bytes()).hexdigest()==ROSTER
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="rdata")
        solves = rdata.read_rda(solve_path)["df_solves"]
        residents = rdata.read_rda(roster_path)["df_surv"]
    solves = solves[solves.solver.astype(str)=="1"].copy()
    experienced_speed(solves)
    solves["base"] = solves.YMD-solves.exp_day_count
    bases = solves.groupby("population").base.first()
    assert solves.groupby("population").base.nunique().max()==1
    groups = {}
    for pop,rows in solves.groupby("population"):
        offset=bases.loc[pop]
        dates = {v.ID:(int(v.date_in_aviary-offset),int(v.date_out-offset))
                 for v in residents[residents.population==pop].itertuples()}
        # The roster file records nontutors. Restore tutors from the solve file.
        alternate = {}
        for i,rec in rows.groupby("ID"):
            entry = int(rec.date_in_aviary.iloc[0]-offset)
            exit_day = entry+int(rec.duration_of_stay.iloc[0])
            if i not in dates:
                assert set(rec.tutor.astype(str))=={"1"}
                dates[i] = (entry,exit_day)
            assert dates[i][1]==exit_day
            alternate[i] = (entry,exit_day)
        weeks = defaultdict(dict)
        for (week,i),seq in rows.groupby(["week","ID"],observed=True):
            times = seq.Event.value_counts()
            weeks[int(week[1:])][i] = (int(times.get("inefficient",0)),int(times.get("efficient",0)))
        groups[int(pop)] = (str(rows.condition.iloc[0]),weeks,dates,alternate)
    print("Archived solver rows, aviaries", len(solves), len(groups))
    return groups


def report(groups,equal=False,alternate=False):
    summary = defaultdict(list)
    endpoints = defaultdict(list)
    count = Counter()
    for name,weeks,dates,other_dates in groups.values():
        stages = {n:stage(v,equal) for n,v in weeks.items()}
        first = sum(w*p for w,p in stages[1].values())
        if 5 in stages:
            last = sum(w*p for w,p in stages[5].values())
            endpoints[name].append((last-first,last-first))
        else:
            endpoints[name].append((-first,1-first))
        series=[]
        for n in range(1,5):
            if n in stages and n+1 in stages:
                series.append(decompose(stages[n],stages[n+1],
                                        other_dates if alternate else dates,7*n))
                count[name]+=1
        if len(series)==4:
            summary[name].append(tuple(map(sum,zip(*series))))
    for name in sorted(summary):
        data=summary[name]
        print("Equal bird" if equal else "Solve-weighted",name,
              "transitions/complete groups",count[name],len(data))
        print("Change, within bird, reweight continuing, roster change, activity entry/exit:",
              [round(float(mean(col)),5) for col in zip(*data)])
        print("Across-group signs within and replacement",
              [(sum(v[j]>0 for v in data),sum(v[j]<0 for v in data)) for j in (1,3)])
        print("Full assigned-group endpoint change bounds",
              [round(float(mean(col)),5) for col in zip(*endpoints[name])])
    return summary


if __name__ == "__main__":
    data = read(*map(Path,sys.argv[1:]))
    baseline = report(data)
    report(data,equal=True)
    sensitivity = report(data,alternate=True)
    print("Changed components under alternate recorded entry dates",
          sum(x!=y for k in baseline for x,y in zip(baseline[k],sensitivity[k])))
