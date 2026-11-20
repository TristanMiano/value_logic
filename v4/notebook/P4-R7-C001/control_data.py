"""Reanalyze choice for control with and without card-to-reward contingency."""
import argparse
from hashlib import sha256
from pathlib import Path
from statistics import mean

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv",type=Path)
    path = parser.parse_args().csv
    if sha256(path.read_bytes()).hexdigest() != "21be9c620753c8442a48f6adc845086a7d6510fbaf852bea5ab214ff1a878a07":
        raise ValueError("Expected choiceval, exp2/models/choice_exp2_clean.csv, revision 29f1cb81")
    data = pd.read_csv(path,usecols=["subject","trial","trial_index","mutual_info","choose_choice"])
    print("Cleaned participants and choices",data.subject.nunique(),len(data))
    for span in (12,6,20):
        records = []
        repeats = []
        for _,sub in data.groupby("subject"):
            sub = sub.sort_values("trial_index")
            assert sub.trial_index.is_unique and sub.trial.is_monotonic_increasing
            runs = sub.groupby(sub.mutual_info.ne(sub.mutual_info.shift()).cumsum())
            if len(runs) != 4 or min(runs.size()) < span:
                continue
            selected = runs.tail(span)
            by = selected.groupby("mutual_info").choose_choice
            assert list(by.size()) == [2*span]*2
            low,high = by.mean()
            records.append([sub.mutual_info.iat[0],low,high])
            counts = {0:[],1:[]}
            for _,run in runs:
                counts[run.mutual_info.iat[0]].append(run.choose_choice.tail(span).sum())
            repeats.append((counts[0][0],counts[1][0],counts[0][1],counts[1][1]))
        scores = pd.DataFrame(records,columns=["start","low","high"])
        for label,group in [("all",scores),*scores.groupby("start")]:
            low,high = group.low,group.high
            print("Final choices per run, first regime, subjects, low/high means,",
                  "low majority, more at high, both, same counts",
                  span,label,len(group),round(low.mean(),6),round(high.mean(),6),
                  int((low>.5).sum()),int((high>low).sum()),int(((low>.5)&(high>low)).sum()),
                  int((high==low).sum()))


        if span == 12:
            recurring = sum(a>span/2 and b>a and c>span/2 and d>c for a,b,c,d in repeats)
            losses = dict.fromkeys(("common","personal","regime personal","shared shift","regime only"),0.)
            for i,(a,b,c,d) in enumerate(repeats):
                others = [row for j,row in enumerate(repeats) if i != j]
                low = mean(row[0]/span for row in others)
                high = mean(row[1]/span for row in others)
                personal = (a+b+.5)/(2*span+1)
                shift = (high-low)/2
                forecasts = {"common":((high+low)/2,)*2,
                             "personal":(personal,personal),
                             "regime personal":((a+.5)/(span+1),(b+.5)/(span+1)),
                             "shared shift":(max(0,min(1,personal-shift)),max(0,min(1,personal+shift))),
                             "regime only":(low,high)}
                for name,pair in forecasts.items():
                    for successes,p in zip((c,d),pair):
                        losses[name] += successes*(1-p)**2+(span-successes)*p**2
            print("Both features in both successive pairs of runs",recurring)
            print("Second-cycle Brier losses",{k:round(v/(2*span*len(repeats)),7) for k,v in losses.items()})


if __name__ == "__main__":
    main()
