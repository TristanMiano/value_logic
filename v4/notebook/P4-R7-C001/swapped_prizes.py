"""Recover objective event odds by moving the payoff conditions across states."""
from fractions import Fraction as F
from itertools import combinations, permutations
from math import exp, log, prod


def normalized(values):
    den=sum(values)
    return [v/den for v in values]


def observed(p,prizes,venues):
    return [normalized([x*prizes[v[s]] for s,x in enumerate(p)]) for v in venues]


def recover(q,venues):
    n=len(q[0])
    centers=[sum(log(x) for x in row)/n for row in q]
    adj=[[] for _ in range(n)]
    for a,b in combinations(range(len(venues)),2):
        inverse={label:t for t,label in enumerate(venues[b])}
        for s,label in enumerate(venues[a]):
            t=inverse[label]
            ratio=(log(q[a][s])-centers[a])-(log(q[b][t])-centers[b])
            adj[t].append((s,ratio))
            adj[s].append((t,-ratio))
    reached={}
    components=[]
    for root in range(n):
        if root in reached:
            continue
        reached[root]=0.;stack=[root];component=[]
        while stack:
            s=stack.pop()
            component.append(s)
            for t,delta in adj[s]:
                v=reached[s]+delta
                if t in reached:
                    assert abs(v-reached[t])<1e-9
                else:
                    reached[t]=v
                    stack.append(t)
        components.append(sorted(component))
    return [(c,normalized([exp(reached[i]) for i in c])) for c in components]


def moving_odds():
    # All numbers in this assay are log odds. A and B swap the two prizes.
    odds = list(map(F,["-.5","-.2",".1"]))
    prizes = list(map(F,["1.2","1.1","1.0"]))
    earlier, previous = [odds[i]+prizes[i] for i in (0,1)]
    last = odds[2]-prizes[2]
    estimate = (2*previous-earlier+last)/2
    assert estimate == odds[2] and (previous+last)/2 == 0
    curve, precision = F(".04"), F(".005")
    radius = curve/2 + 2*precision
    for direction in (-1,1):
        # Opposing readout errors and maximal curvature attain each endpoint.
        past_a = earlier - direction*precision
        prior_a = previous + direction*precision
        true_b = last + direction*precision
        current_a = 2*prior_a-past_a+direction*curve
        target = (current_a+true_b)/2
        assert target == estimate+direction*radius
    lo, hi = [1/(1+exp(-float(x))) for x in (estimate-radius,estimate+radius)]
    assert lo > .51
    print("Current physical probability, bounded range, naive adjacent-swap estimate",
          round(1/(1+exp(-float(estimate))),6), (round(lo,6),round(hi,6)), .5)


def main():
    moving_odds()
    p=list(map(F,[".4",".3",".2",".1"]))
    prizes=[4,1,2,3]
    identity=(0,1,2,3); shifts=(1,0,3,2); cycle=(1,2,3,0)
    for venues in [[identity,shifts],[identity,cycle]]:
        q=observed(p,prizes,venues)
        ratios=recover(q,venues)
        print("Reachable components / inferred conditional probabilities",
              [(g,[round(x,6) for x in pr]) for g,pr in ratios])
        for group,pr in ratios:
            expected=normalized([p[i] for i in group])
            assert max(abs(x-y) for x,y in zip(pr,expected))<1e-10
        for a,b in combinations(range(len(venues)),2):
            for s,label in enumerate(venues[a]):
                t=venues[b].index(label)
                assert (q[a][s]/q[b][t])**4*prod(q[b])/prod(q[a])==(p[s]/p[t])**4
    alternate=normalized([p[i]*(3 if i>=2 else 1) for i in range(4)])
    values=[F(v,3 if j>=2 else 1) for j,v in enumerate(prizes)]
    venues=[identity,shifts]
    assert observed(p,prizes,venues)==observed(alternate,values,venues)
    assert p[0]>p[2] and alternate[0]<alternate[2]
    print("Same partially reassigned observations, different law",list(map(str,alternate)))
    for venue in permutations(range(4)):
        groups=recover(observed(p,prizes,[identity,venue]),[identity,venue])
        for group,pr in groups:
            expected=normalized([p[i] for i in group])
            assert max(abs(x-y) for x,y in zip(pr,expected))<1e-10
    theta=F(2,5)
    y=observed([theta,1-theta],[3,1],[(0,1),(1,0)])
    print("Two fair reference probabilities for the same event",y[0][0],y[1][0])
    assert y[0][0]==F(2,3) and y[1][0]==F(2,11)


if __name__=="__main__":
    main()
