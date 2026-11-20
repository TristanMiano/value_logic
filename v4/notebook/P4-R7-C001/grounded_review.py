"""W7.5. Grounded mutual licensing, choice of evidence checks and self-prediction."""
from fractions import Fraction as F
from itertools import product
from math import log
from random import Random


def grounded(roots,tests):
    # tests[i][j] lists already precommitted, positively settled IDs needed
    # by i to license j. A missing entry means it has no such contract.
    data=[set(s) for s in roots]
    while True:
        nxt=[d.copy() for d in data]
        for i,row in enumerate(tests):
            for j,needed in row.items():
                if needed<=data[i]:
                    nxt[i].update(data[j])
        if data==nxt:
            return data
        data=nxt


def mutual_review():
    roots=[{"u"},{"v"}]
    tests=[{1:{"u"}},{0:{"v"}}]
    both=grounded(roots,tests)
    assert both==[{"u","v"},{"u","v"}]
    assert grounded(roots,[tests[0],{}])==[{"u","v"},{"v"}]
    assert grounded(roots,[{},tests[1]])==[{"u"},{"u","v"}]
    assert grounded([set(),set()],tests)==[set(),set()]
    # Both schools can now use a self-audit requiring u AND v.
    print("Cyclic receipt and both self-licenses",both,[{"u","v"}<=d for d in both])


def div(p,q):
    return p*log(p/q)+(1-p)*log((1-p)/(1-q))


def lineage():
    # Joint mass of (the world, the votes, whether all copied one report).
    # Reconstruct the public optimum using the full observation distribution.
    s=F(3,4)
    data={}
    for truth,shared in product(range(2),repeat=2):
        for votes in product(range(2),repeat=3):
            if shared:
                prob=(s if votes[0]==truth else 1-s) if len(set(votes))==1 else F(0)
            else:
                prob=F(1)
                for v in votes:
                    prob*=s if v==truth else 1-s
            data[truth,votes,shared]=prob/4
    assert sum(data.values())==1
    gain,info,seen=F(0),0.,F(0)
    threshold=F(9,10)
    for votes in product(range(2),repeat=3):
        majority=int(sum(votes)>=2)
        matched=sum(v for (h,z,l),v in data.items() if h==majority and z==votes)
        mass=sum(v for (h,z,l),v in data.items() if z==votes)
        posterior=matched/mass
        if len(set(votes))==1:
            seen+=mass
            assert posterior==F(75,92)
        for shared in range(2):
            weight=sum(data[h,votes,shared] for h in (0,1))
            if weight:
                p=data[majority,votes,shared]/weight
                info+=float(weight)*div(float(p),float(posterior))
                gain+=weight*(max(F(0),p-threshold)-max(F(0),posterior-threshold))
    assert seen==F(23,32) and gain==F(9,640) and gain/seen==F(9,460)
    print("Value of lineage: log reward",round(info,7),"decision",gain,"per check",gain/seen)


def score_pair(p,theta,anchor,correlation):
    q=anchor*theta+(1-anchor)*p
    total=F(0)
    for left,right in product((0,1),repeat=2):
        a=q if left else 1-q
        b=q if right else 1-q
        joint=(1-correlation)*a*b+correlation*a*int(left==right)
        total+=joint*(p-left)*(p-right)
    assert total==(p-q)**2+correlation*q*(1-q)
    return total


def reflexive_selection():
    half=F(1,2)
    anchor=F(1,4)
    for corr in (F(0),F(1,10),F(1,9),F(3,20),F(1)):
        vals=[score_pair(F(i,20),half,anchor,corr) for i in range(21)]
        minima=[i for i,v in enumerate(vals) if v==min(vals)]
        expected=[10] if corr<F(1,9) else ([0,20] if corr>F(1,9) else list(range(21)))
        assert minima==expected
        print("Shared-output probability",corr,"best forecast(s) in twentieths",minima)


def growth():
    # W7.3's genuine crossed grouping gives mismatch probability 0.5.
    # Other physical tasks are uninformative. A false model has a copying
    # bonus each period, regardless of whether the measurement is made.
    k=div(.5,.18)
    bonus=.06
    print("KL per distinguishing observation",round(k,7),"critical coverage",round(bonus/k,7))
    for numerator in (1,2):
        rng=Random(751)
        total=0
        n=100000
        for t in range(n):
            total-=bonus
            if t%5<numerator:
                y=rng.randrange(2)
                total+=log(.5/(.18 if y else .82))
        expected=numerator/5*k-bonus
        assert (total>0)==(expected>0)
        print("Coverage",numerator/5,"true-minus-false log growth per round",
              round(total/n,7),"expectation",round(expected,7))
    # Unrelated popularity swaps which true-world reviewer leads without
    # altering their elemental predictions or the factual frontier sentences.
    front=[]
    for t in range(4):
        w=([4,1] if t%2 else [1,4])+[.1/(t+1)]
        front.append([i for i,z in enumerate(w) if z>=max(w)/2])
    assert front==[[1],[0],[1],[0]]


if __name__=="__main__":
    mutual_review()
    lineage()
    reflexive_selection()
    growth()
