"""Reanalyze the group choices in the Toyokawa, Whalen and Laland experiment.

Pass the authors' allBehaviouralData2.csv as the sole argument. All outputs
are aggregates. See R7_task_selection.md for the pinned source and design.
"""
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
from pathlib import Path
from statistics import mean
import sys

EXPECTED = "f10baa02c49abf3407cd7daa5fb9628de9cafc45480649e5c4158e71ac791dd0"
WINDOWS = (31,41,61)
ARMS = (0,1,2)


@dataclass(frozen=True)
class Choice:
    arm: int
    grade: int
    reward: Decimal


def consistent_assignments(series):
    """Keep every assignment consistent with known design and observed grades."""
    pairs = set((t>40,x.arm,x.grade) for t,choices in series.items() for x in choices)
    def grade(late,arm,old,new):
        if arm==old:
            return 2
        return 3 if late and arm==new else 1
    possible=[(old,new) for old,new in permutations(ARMS,2)
              if all(g==grade(late,arm,old,new) for late,arm,g in pairs)]
    assert possible
    return possible


def select_room(series):
    return all(any(len(series.get(t,()))>=2 for t in range(start,start+10))
               for start in WINDOWS)


def bounds(values):
    return min(values),max(values)


def fractions(choices,old,new,late):
    n=len(choices)
    freq=Counter(x.arm for x in choices)
    best=new if late else old
    return [freq[old]/n,freq[new]/n,float(2*freq[best]>n)]


def room_windows(series,possible):
    for start in WINDOWS:
        rounds=[series[t] for t in range(start,start+10) if len(series.get(t,()))>=2]
        per_layout=[]
        for old,new in possible:
            values=[fractions(choices,old,new,start>40) for choices in rounds]
            per_layout.append(tuple(map(mean,zip(*values))))
        yield start,len(rounds),sum(map(len,rounds)),list(map(bounds,zip(*per_layout)))


def predict(series,possible):
    rows=[]
    for t in range(41,71):
        if len(series.get(t,()))<2:
            continue
        prior=[x for j in range(t-10,t) for x in series.get(j,())]
        counts=Counter(x.arm for x in prior)
        if len(counts)<3:
            rows.append(None)
            continue
        rewards=[sum(x.reward for x in prior if x.arm==a)/counts[a] for a in ARMS]
        scores=[]
        for ranking in ([counts[a] for a in ARMS],rewards):
            winners=[a for a in ARMS if ranking[a]==max(ranking)]
            scores.append(bounds([float(F(int(new in winners),len(winners))) for _,new in possible]))
        rows.append(scores)
    return rows


def main(path):
    assert sha256(path.read_bytes()).hexdigest()==EXPECTED,"wrong edition of source table"
    rooms=defaultdict(lambda:defaultdict(list))
    difficulty={}
    subjects=defaultdict(set)
    with path.open(encoding="utf8",newline="") as file:
        for r in csv.DictReader(file):
            name,t=r["room"],int(r["round"])
            difficulty[name]=r["taskDifficulty"]
            subjects[name].add(r["ID"])
            x=Choice(int(r["machine"]),int(r["performance"]),Decimal(r["result"]))
            assert int(r["optimalChoice"])==int(x.grade==(3 if t>40 else 2))
            rooms[name][t].append(x)
    keep={name:s for name,s in rooms.items() if select_room(s)}
    print("Archive/eligible rooms, eligible participants",len(rooms),len(keep),
          sum(len(subjects[name]) for name in keep))
    for diff in ["25%","50%","78%"]:
        group=[s for name,s in keep.items() if difficulty[name]==diff]
        print("Difficulty",diff,"rooms",len(group))
        windows=defaultdict(list)
        forecasts=[]
        membership=[]
        ambiguity=0
        for s in group:
            possible=consistent_assignments(s)
            ambiguity+=len(possible)>1
            membership.append((len(s.get(31,())),len(s.get(70,()))))
            forecasts.append(predict(s,possible))
            for start,nr,nc,vals in room_windows(s,possible):
                windows[start].append((nr,nc,vals))
        print("Rooms of ambiguous layout",ambiguity,"active choices at 31/70",list(map(sum,zip(*membership))))
        for start,rows in windows.items():
            intervals=[]
            for metric in range(3):
                intervals.append(tuple(round(mean(r[2][metric][edge] for r in rows),4) for edge in range(2)))
            pooled=[]
            for name,s in keep.items():
                if difficulty[name]==diff:
                    for t in range(start,start+10):
                        if len(s.get(t,()))>=2:
                            pooled.extend(x.grade==(3 if start>40 else 2) for x in s[t])
            print(start,"rounds",sum(r[0] for r in rows),"choices",len(pooled),
                  "old/new/majority",intervals,"pooled best",round(mean(pooled),4))
        support=sum(sum(v is not None for v in room) for room in forecasts)
        total=sum(map(len,forecasts))
        scores=[[v for v in room if v is not None] for room in forecasts]
        usable=[r for r in scores if r]
        print("Prior all-arm coverage",support,total,"rooms",len(usable))
        # The three uncertain layouts induce identical scores wherever all
        # three arms were visited in the input window.
        assert all(lo==hi for room in usable for row in room for lo,hi in row)
        gains=[sum(v[1][0]-v[0][0] for v in r if v is not None)/len(r)
               for r in forecasts]
        print("Same fallback without coverage: mean advantage",
              round(mean(gains),4),"rooms with positive, tied, negative difference",
              sum(g>1e-12 for g in gains),sum(abs(g)<=1e-12 for g in gains),
              sum(g< -1e-12 for g in gains))
        for rule in (0,1):
            print("frequency" if rule==0 else "observed mean",
                  tuple(round(mean(mean(v[rule][edge] for v in r) for r in usable),4) for edge in (0,1)))


if __name__=="__main__":
    main(Path(sys.argv[1]))
