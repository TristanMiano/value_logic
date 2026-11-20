"""Targeted review of Moniz, Druckman and Freese (2025), Table 1.

The published percentages and group sizes uniquely recover integer counts.
The audit enumerates finite sample distributions, conditional on these cohorts.
"""
from fractions import Fraction as F
from math import comb


def count(n, percent):
    hits=[x for x in range(n+1) if abs(100*F(x,n)-F(percent))<=F(1,200)]
    assert len(hits)==1
    return hits[0]


def tails(total, marked, sample):
    denom = comb(total,sample)
    probs = [F(comb(marked,j)*comb(total-marked,sample-j),denom)
             if 0<=j<=marked and 0<=sample-j<=total-marked else F(0)
             for j in range(sample+1)]
    accum = F(0)
    tail = {}
    for j in reversed(range(sample+1)):
        accum += probs[j]
        tail[j]=accum
    assert accum==1
    return tail


def report(label,n,ypercent,m,npercent):
    y = [count(n,v) for v in ypercent]
    no = [count(m,v) for v in npercent]
    assert sum(y)==n and sum(no)==m
    ys = [sum(y[i:]) for i in range(4)]
    ns = [sum(no[i:]) for i in range(4)]
    rates = [F(ys[i+1],ys[i])/F(ns[i+1],ns[i]) for i in range(3)]
    prod = rates[0]*rates[1]*rates[2]
    assert prod == F(ys[-1],ys[0])/F(ns[-1],ns[0])
    print(label,"significant/insignificant by furthest stage",y,no)
    print("Conditional retention ratios",[round(float(x),4) for x in rates],"total",round(float(prod),4))
    print("Published and all-submitted yield gaps",
          *(round(float(F(ys[i],n)-F(ns[i],m)),4) for i in (3,2)))
    overall=n+m
    known=ys[-1]
    unpub=overall-known-ns[-1]
    missing_no=m-ns[-1]
    max_true_for_decline = (2*overall)//3
    need = unpub + known - max_true_for_decline
    assert 0<need<=missing_no
    # Expected position of the 'need'-th negative in a simple random permutation.
    expected=F(need*(unpub+1),missing_no+1)
    print("Unpublished, negative records required for certainty, mean draws",unpub,need,expected)
    for sample in range(1,unpub+1):
        null_tail=tails(unpub,need-1,sample)
        actual_tail=tails(unpub,missing_no,sample)
        cutoff=next((j for j in range(sample+1) if null_tail[j]<=F(1,20)),None)
        if cutoff is not None and actual_tail[cutoff]>=F(4,5):
            print("Smallest fixed sample at 5% size, 80% design power: draws, cutoff, power",
                  sample,cutoff,round(float(actual_tail[cutoff]),4))
            break


if __name__ == "__main__":
    report("TESS",61,["8.20","0.00","16.39","75.41"],
           46,["28.26","15.22","10.87","45.65"])
    report("Collected outside TESS",171,["13.45","7.02","22.22","57.31"],
           97,["41.24","13.40","9.28","36.08"])
