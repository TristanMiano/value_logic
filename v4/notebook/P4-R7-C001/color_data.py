"""Decode a physical two-chip choice from World Color Survey naming responses."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from math import log, log2
from pathlib import Path
from random import Random
from statistics import mean
from zipfile import ZipFile

ARCHIVE_SHA256 = "6708e7edf8ee7fa65977b545bc8cb28b0918e8ab235d21527f140e4d95aae19a"


def read(path):
    if sha256(path.read_bytes()).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("Expected Berkeley WCS-Data-20110316.zip")
    with ZipFile(path) as archive:
        def rows(filename):
            data = archive.read("WCS-Data-20110316/" + filename)
            return (line.split(b"\t") for line in data.splitlines())
        chips = {int(i):(row,int(column)) for i,row,column,_ in rows("chip.txt")}
        terms = {(int(lang),word) for lang,_,name,word in rows("dict.txt")
                 if lang.isdigit() and word and name.strip().lower() != b"blank"}
        responses = defaultdict(dict)
        for lang, speaker, chip, word in rows("term.txt"):
            row, column = chips[int(chip)]
            if column and row in (b"B",b"I",b"D",b"E"):
                key = int(lang), int(speaker), column
                assert row not in responses[key]
                responses[key][row] = word
    return responses, terms


def compare(responses, terms, upper, lower, strict):
    # Each held-out pair receives equal material weight on each of its two choices.
    pairs = []
    pooled = defaultdict(Counter)
    one_hue = defaultdict(Counter)
    half_circle = defaultdict(Counter)
    for (language,speaker,hue), pair in responses.items():
        a, b = pair[upper], pair[lower]
        if strict:
            if (language,a) not in terms or (language,b) not in terms:
                continue
        elif a in (b"",b"*",b"?") or b in (b"",b"*",b"?"):
            continue
        cohort = speaker % 2
        for word, change in ((a,1),(b,-1)):
            pooled[language,cohort,hue%2][word] += change
            one_hue[language,cohort,hue][word] += change
            half_circle[language,cohort,int(hue>20)][word] += change
        pairs.append((language,cohort,hue,a,b))

    def score(counts, a, b):
        # Correct quarters, counting a tied word as half a correct answer.
        return 2 + (counts[a]>0) - (counts[a]<0) - (counts[b]>0) + (counts[b]<0)

    opportunities = Counter(language for language,_,_ in responses)
    results = defaultdict(lambda:[0,0,0,0,0])
    for language,cohort,hue,a,b in pairs:
        out = results[language]
        out[0] += 1
        out[1] += score(pooled[language,1-cohort,1-hue%2],a,b)
        out[2] += score(one_hue[language,1-cohort,hue],a,b)
        out[3] += 2 if a==b else 4
        out[4] += score(half_circle[language,1-cohort,int(hue<=20)],a,b)
    assert len(results) == 110
    sums = [[r[j]/(4*r[0]) for r in results.values()] for j in (1,2,3,4)]
    assert all(r[1]<=r[3] and r[2]<=r[3] for r in results.values())
    print(upper.decode()+lower.decode(), "dictionary" if strict else "raw code",
          "pairs", len(pairs), "languages",len(results))
    for name,values in zip(("new hue","same hue","word ceiling","opposite half"),sums):
        print(" ",name,"mean/min/max",*[round(x,6) for x in (mean(values),min(values),max(values))],
              "above chance",sum(x>.5 for x in values),"at least .8",sum(x>=.8 for x in values))
    measures = {}
    for lang,r in results.items():
        total = opportunities[lang]
        lower = r[1]/(4*total)
        upper = (r[3]/4+total-r[0])/total
        measures[lang] = r[1]/(4*r[0]),r[3]/(4*r[0]),r[4]/(4*r[0]),lower,upper
    print("All assigned pairs",sum(opportunities.values()),"worst-case accuracy lower / oracle upper",
          round(mean(v[3] for v in measures.values()),6),round(mean(v[4] for v in measures.values()),6))
    return measures


def sparse(responses, terms, upper, lower):
    offers = defaultdict(list)
    difference = defaultdict(Counter)
    valid = Counter()
    for (language,speaker,hue), row in responses.items():
        key = language, speaker % 2, hue % 2
        a, b = row[upper], row[lower]
        if (language,a) in terms and (language,b) in terms:
            offers[key].append((a,b))
            difference[key][a] += 1
            difference[key][b] -= 1
            valid[key] += 1
        else:
            offers[key].append(None)

    budgets = (1,2,4,8,16,32)
    exact_gain = Counter()
    totals = Counter()
    for (language,cohort,parity), pool in offers.items():
        test = language,1-cohort,1-parity
        tally = difference[test]
        totals[language] += valid[test]
        gain = sum(tally[pair[0]]-tally[pair[1]] for pair in pool if pair is not None)
        exact_gain[language] += gain / len(pool)
    by_language = [exact_gain[k]/(4*totals[k]) for k in totals]
    exact = .5 + mean(by_language)
    print('Languages with positive one-pair gain, gain range',sum(x>0 for x in by_language),
          min(by_language),max(by_language))
    print("Exact one-pair accuracy",round(exact,6),"break-even jobs",2/(exact-.5))

    for horizon in ((12,16,24) if upper==b"B" else (595,900,1600)):
        mean_log_ratio = Counter()
        for (language,cohort,parity),pool in offers.items():
            test = language,1-cohort,1-parity
            m = valid[test]
            if not m:
                continue
            tally = difference[test]
            gain_counts = Counter(tally[pair[0]]-tally[pair[1]] if pair else 0 for pair in pool)
            for gain,nn in gain_counts.items():
                accuracy = .5+gain/(4*m)
                mean_log_ratio[language] += (m/totals[language])*(nn/len(pool))*log(
                    (1+horizon*accuracy)/(3+horizon/2))
        print("Jobs, extra mean receipts, mean relative log growth",horizon,
              round(horizon*(exact-.5)-2,6),round(mean(mean_log_ratio.values()),6))

    results = defaultdict(list)
    for seed in range(7100,7116):
        rng = Random(seed)
        gains = defaultdict(Counter)
        for (language,cohort,parity), pool in sorted(offers.items()):
            test = language,1-cohort,1-parity
            tally = difference[test]
            draw = rng.sample(pool,max(budgets))
            words = Counter()
            for i,pair in enumerate(draw,1):
                if pair:
                    a,b = pair
                    words[a] += 1
                    words[b] -= 1
                if i in budgets:
                    gains[i][language] += sum(((n>0)-(n<0))*tally[w]
                                               for w,n in words.items())
        for budget in budgets:
            results[budget].append(.5+mean(gains[budget][k]/(4*totals[k]) for k in totals))
    for budget, rates in results.items():
        acc = mean(rates)
        print("Calibration pairs",budget,"accuracy / seed range",
              *[round(x,6) for x in (acc,min(rates),max(rates))],
              "break-even jobs",round(2*budget/(acc-.5),2) if acc>.5 else None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive",type=Path)
    responses, terms = read(parser.parse_args().archive)
    for strict in (True,False):
        wide = compare(responses,terms,b"B",b"I",strict)
        close = compare(responses,terms,b"D",b"E",strict)
        print("Wide above close",sum(wide[k][0]>close[k][0] for k in wide),
              "wide above an adjacent-word oracle",sum(wide[k][0]>close[k][1] for k in wide),
              "wide outside semicircle above oracle",sum(wide[k][2]>close[k][1] for k in wide))
        print("Separation even on adversarially completed missing records",
              sum(wide[k][3]>close[k][4] for k in wide))
        p = mean(values[0] for values in wide.values())
        print("Wide information lower bound and adjacent upper bound (bits)",
              1+p*log2(p)+(1-p)*log2(1-p), mean(2*values[1]-1 for values in close.values()))
    for upper,lower in ((b"B",b"I"),(b"D",b"E")):
        print("Paid translations",upper+lower)
        sparse(responses,terms,upper,lower)


if __name__ == "__main__":
    main()
