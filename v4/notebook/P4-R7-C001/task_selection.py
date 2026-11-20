"""W7.3. Repeated work, report sharing and fitness of rules for assigning jobs."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb, exp, prod
from random import Random

B = F(4)
SUBSIDY = F(3,5)
FEE = F(1,5)
COVERAGE = F(4,5)
TRANSFER = B/2-SUBSIDY
LAYOUTS = ((0,0,1,1),(0,1,0,1))


def probes(layout, performers):
    """Return the proposed partner of job 0 and the number of pairs used."""
    for n, bits in enumerate(performers,1):
        if bits[layout[0]] != bits[layout[1]]:
            return 2,n
    return 1,len(performers)


def enumerate_jobs(depth):
    # Fresh workers for each probe and for deployment. Condition the last
    # worker on the observed success at job 0 used to offer them a second job.
    bits = tuple(product(range(2),repeat=2))
    total=Counter()
    for layout in LAYOUTS:
        for trial in product(bits,repeat=depth):
            job,spent=probes(layout,trial)
            for worker in bits:
                if worker[layout[0]]:
                    total.update(dict(rows=1,conventional=(job==1),paid=spent,
                                      correct=(layout[job]==layout[0]),
                                      finished=worker[layout[job]]))
    return {key:F(n,total["rows"]) for key,n in total.items() if key!="rows"}


def expectations(depth):
    miss=F(1,2)**depth
    return dict(conventional=(1+miss)/2,paid=F(depth,2)+1-miss,
                correct=1-miss/2,finished=1-miss/4)


def best_depth(payers):
    depth = 0
    while TRANSFER/(2*(1+2**depth)) > FEE/payers:
        depth += 1
    return depth


def subsidy_and_access():
    for depth in range(6):
        assert enumerate_jobs(depth) == expectations(depth)
    base=expectations(0)
    two=expectations(2)
    benefit=(two["finished"]-base["finished"])*B+(two["conventional"]-1)*SUBSIDY
    cost=FEE*two["paid"]
    share=(1-cost/benefit)/COVERAGE
    assert share == F(5,12)
    using=share+(1-share)*COVERAGE*share
    success=base["finished"]+using*(two["finished"]-base["finished"])
    print("Private investigation",share,"share; overall job success",success,float(success))
    assert best_depth(1)==2 and best_depth(4)==4
    for users,depth in ((1,2),(4,2),(4,4)):
        stats = expectations(depth)
        net=B*stats["finished"]+SUBSIDY*stats["conventional"]-FEE*stats["paid"]/users
        print("Joint transcript",users,depth,net,float(net))
    for e_low,e_high in ((.1,.9),(.39,.61)):
        x=.31
        for _ in range(200):
            for e in (e_low,e_high):
                before = x
                odds=x/(1-x)*exp(2*(e*(1.15-.84*x)-.4))
                x=odds/(1+odds)
        print("Periodic copying",e_low,e_high,round(x,8),round(before,8))


def noisy_readers():
    # Under either type of local world, pay for d new pairs. Each judge's
    # approval of each task flips independently with error 0.1.
    mismatch = 2*F(1,10)*F(9,10)
    fee=F(1,40)
    best=(F(0),0,[])
    for depth in range(29):
        delta=[]
        for different in range(depth+1):
            mass1=F(comb(depth,different),2**depth)
            mass0=comb(depth,different)*mismatch**different*(1-mismatch)**(depth-different)
            delta.append((mass1*TRANSFER-mass0*(B/2+SUBSIDY))/2)
        choose=[k for k,v in enumerate(delta) if v>0]
        winnings=sum(delta[k] for k in choose)-fee*depth
        if winnings>best[0]:
            best=winnings,depth,choose
        if depth==9:
            print("Noisy judgments, any discrepancy at fixed depth",float(sum(delta[1:])-fee*depth))
    assert best[1:]==(9,[4,5,6,7,8,9])
    assert F(29)*fee>TRANSFER/2
    print("Noisy judgments, best fixed budget",best[1],best[2],float(best[0]))


def signatures(groups,depth):
    p=F(1,2)**depth
    complete=prod(1-i*p for i in range(groups)) if groups<=2**depth else 0
    right=sum(comb(groups-1,r)*p**r*(1-p)**(groups-1-r)/ (1+2*r) for r in range(groups))
    return complete,(1+right)/2


def unlabelled_trial(rng,groups,depth):
    layout=list(range(groups))*2
    rng.shuffle(layout)
    signatures=[[] for _ in layout]
    for _ in range(depth):
        skill=[rng.randrange(2) for _ in range(groups)]
        for job,group in enumerate(layout):
            signatures[job].append(skill[group])
    bins=set(map(tuple,signatures))
    choices=[j for j in range(1,len(layout)) if signatures[j]==signatures[0]]
    job=rng.choice(choices)
    next_worker=[rng.randrange(2) for _ in range(groups)]
    next_worker[layout[0]]=1
    return len(bins)==groups,next_worker[layout[job]]


def main():
    subsidy_and_access()
    noisy_readers()
    groups,depth=8,4
    exact=signatures(groups,depth)
    rng=Random(731)
    trials=12000
    observed=[sum(events)/trials for events in zip(*(unlabelled_trial(rng,groups,depth) for _ in range(trials)))]
    for value,obs in zip(exact,observed):
        assert abs(float(value)-obs)<.025
    print("Unlabelled job twins, complete recovery and work",*(round(float(v),6) for v in exact),
          "seeded check",observed)


if __name__=="__main__":
    main()
