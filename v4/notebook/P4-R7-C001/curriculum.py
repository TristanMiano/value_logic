"""W7.3. Endogenous coverage of repeated judgments, and tracking a moving fact."""
from math import pi, sinh, sqrt


def recovery(depth,power,reserve):
    # Distribution of the number of reviews in context zero. Approval bits
    # come from new workers and, in this version, do not change endorsements.
    mass=[1.]
    missed=1.
    for t in range(depth):
        nxt=[0.]*(t+2)
        scheduled=1/(t+1) if reserve else 0.
        for n,weight in enumerate(mass):
            left=(1+n)**power
            right=(1+t-n)**power
            p=(1-scheduled)*left/(left+right)+scheduled/2
            nxt[n+1]+=weight*p
            nxt[n]+=weight*(1-p)
        mass=nxt
        missed*=1-scheduled/4
    remaining=sum(weight*.5**n for n,weight in enumerate(mass))
    both=1-2*remaining+.5**depth
    assert abs(sum(mass)-1)<1e-12 and remaining<=missed+1e-12
    if power==1 and not reserve:
        assert max(abs(p-1/(depth+1)) for p in mass)<1e-14
    if power==0:
        assert abs(both-(1-2*.75**depth+.5**depth))<1e-12
    return remaining,both


def audit_growth():
    for t in (20,100,500):
        for m,r in ((0,False),(1,False),(2,False),(2,True)):
            miss,accurate=recovery(t,m,r)
            print("Rounds/endorsements/reserve",t,m,r,"one entry missed / both corrected",
                  round(miss,6),round(accurate,6))
    no_visit=1.
    for k in range(1,20001):
        no_visit*=1/(1+k**-2)
    exact=pi/sinh(pi)
    assert 0<no_visit-exact<1/20000
    print("Never even visiting one initially wrong context",round(exact,6))


def tracking():
    nu,b,c=.1,4.,.6
    e=(sqrt(b*nu/(2*c))-2*nu)/(1-2*nu)
    def state_accuracy(e):
        return .5+e/(2*(e+2*nu*(1-e)))
    def surplus(e):
        return b*(state_accuracy(e)-.5)/2-c*e
    for fraction in (0,e,1):
        acc=state_accuracy(fraction)
        assert abs(acc-(fraction+(1-fraction)*(nu+(1-2*nu)*acc)))<1e-12
        print("Fresh-audit probability",round(fraction,6),"correct choice",round(acc,6),
              "actual successful work",round((1+acc)/2,6),"net increment",round(surplus(fraction),6))
    assert surplus(e)>=max(surplus(i/1000) for i in range(1001))
    acc=1.
    for t in range(1,10001):
        prob=1/t
        acc=prob+(1-prob)*(nu+(1-2*nu)*acc)
    print("Sparse reserve in changing world at round 10000",round(acc,6))


def check_supported_partitions():
    from fractions import Fraction as F
    from itertools import combinations
    # Generate restricted-growth strings, once per partition without naming
    # its blocks. Enumerate every possible set of priced pair jobs.
    n=5
    parts=[(0,)]
    for _ in range(1,n):
        parts=[p+(a,) for p in parts for a in range(max(p)+2)]
    edges=tuple(combinations(range(n),2))
    truths={p:sum(1<<j for j,(u,v) in enumerate(edges) if p[u]==p[v]) for p in parts}
    for menu in range(1<<len(edges)):
        groups={}
        for p,equal in truths.items():
            groups.setdefault(equal & menu,[]).append(p)
        for signature,compatible in groups.items():
            names=list(range(n))
            for j,(a,b) in enumerate(edges):
                if signature & (1<<j):
                    u,v=names[a],names[b]
                    names=[u if z==v else z for z in names]
            blocks=set(names)
            negative={tuple(sorted((names[a],names[b]))) for j,(a,b) in enumerate(edges)
                      if menu & (1<<j) and not signature & (1<<j)}
            complete=len(negative)==len(blocks)*(len(blocks)-1)//2
            assert complete==(len(compatible)==1)
    p,q=F(1,2),F(1,4)
    # Integrate actual receipts on the set of prices at which buying differs.
    assert (p-q)*(p-(p+q)/2)==(p-q)**2/2==F(1,32)
    print("Priced paired jobs",len(parts),"partitions,",1<<len(edges),"test menus")


if __name__=="__main__":
    audit_growth()
    tracking()
    check_supported_partitions()
