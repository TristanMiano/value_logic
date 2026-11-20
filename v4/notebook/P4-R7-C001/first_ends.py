"""Acquiring a first end through transmission; compare habits and priced flexibility."""
from fractions import Fraction as F
from math import ceil, log2, prod


def conditional_return(limit, cutoff, credit):
    """Uniform prices in [0, limit], safe option taken below cutoff."""
    assert 0 <= cutoff <= limit
    return (credit*cutoff-cutoff**2/2)/limit


def fixation(birth, resident, size):
    if birth == resident:
        return F(1,size)
    reverse = resident/birth
    return (1-reverse)/(1-reverse**size)


def first_end():
    q, delta, target, base = F(1,2),F(3,10),F(2,5),F(3,2)
    flat = base + q*(target*delta/2-delta/4)
    money = base
    both = base + q*conditional_return(delta,delta*target,delta*target)
    assert money-flat == F(3,400) and both-money == F(3,250)
    assert both-flat == q*delta*((target-F(1,2))**2/2+F(1,8))
    print("Initial coin, priced cash, acquired presence: copying weights",flat,money,both)
    for variant, resident in ((money,flat),(both,money),(both,flat)):
        print("Single mutant, population 100: fixation probability",float(fixation(variant,resident,100)))
    low, high, cap = F(1,10),F(3,10),F(3,10)
    optimum = [d*target for d in (low,high)]
    fixed = sum(optimum)/2
    adaptable = sum(conditional_return(cap,c,c) for c in optimum)/2
    reflex = sum(conditional_return(cap,fixed,c) for c in optimum)/2
    assert q*(adaptable-reflex) == F(1,750)
    print("Two physical gains: terminal-score cutoffs, price-only cutoff, value of conditioning",
          optimum,fixed,q*(adaptable-reflex))


def three_motives():
    delta = F(3,10)
    for direct,coverage,pupils in ((F(2,5),1,0),(0,F(3,5),0),(0,1,F(2,5))):
        def price(stake,seats):
            return delta*(direct+(1-coverage)*stake+pupils*seats)
        a,b,c,d = [price(stake,seats) for stake,seats in ((1,0),(2,0),(1,1),(2,1))]
        assert c == F(3,25) and d-b == c-a
        assert ((2*a-b)/delta,(b-a)/delta,(c-a)/delta) == (direct,1-coverage,pupils)
        print("Protected-price menus for presence, incomplete cover or pupils",a,b,c,d)


def delayed_help():
    participation = F(3,4)
    assert F(95,100)**5 > participation > F(95,100)**6
    for start in (2,3):
        for delay in (1,5,6,64,1000):
            retention = prod(1-F(1,(t+start)**2) for t in range(1,delay+1))
            limit = F(start,start+1)
            assert retention == limit*F(start+delay+1,start+delay)
            if start==3:
                assert retention>participation
            if start==2 and delay==6:
                assert retention==participation
            print("Review schedule, delay, delivery retention",start,delay,float(retention))
    # The original may exit; successors actually deliver if both the
    # ranking and an executing carrier survive each transition.
    survival = F(9,10)
    for delay in (1,10,100,1000):
        goal = prod(1-F(1,(t+7)**2) for t in range(1,delay+1))
        service = F(1)
        for t in range(1,delay+1):
            transfer = 1-F(1,(t+7)**2)/(1-survival)
            assert 0 <= transfer <= 1
            service *= survival+(1-survival)*transfer
        assert goal*service == (F(7,8)*F(delay+8,delay+7))**2 > F(49,64)
        assert goal*service > participation
    print("All-delay service survival lower bound with recurring individual mortality", F(49,64))
    for day in range(1,1025):
        depth = ceil(2*log2(day+3))
        assert F(1,2**depth) <= F(1,(day+3)**2)
        assert sum(F(1,2**i) for i in range(depth)) < 2


if __name__ == "__main__":
    first_end()
    three_motives()
    delayed_help()
