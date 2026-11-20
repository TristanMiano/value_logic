"""W7.1. Finite copying in a two-service market. Standard library, Python 3.10+."""

from fractions import Fraction
from math import comb, fsum, log
from random import Random


def referral_law(first, size, checks, flip, demand=Fraction(1, 2)):
    """One family of independent client referrals, conditional on agreement.

    An absent service has no mentor. A referral is then reassigned to a
    provider of the service that exists. A copying error can revive the other.
    """
    if first == 0:
        return flip, Fraction(1, size)**(checks-1)
    if first == size:
        return 1-flip, Fraction(1, size)**(checks-1)
    p_first = demand/first
    p_second = (1-demand)/(size-first)
    one = first*p_first**checks
    two = (size-first)*p_second**checks
    agreement = one+two
    return flip+(1-2*flip)*one/agreement, agreement


def enumerate_referrals(first, size, checks, flip):
    """Enumerate all distinct tuples for a small classroom, before conditioning."""
    from itertools import product
    probabilities = ([Fraction(1, 2*first)]*first +
                     [Fraction(1, 2*(size-first))]*(size-first))
    first_mass, total = 0, 0
    for referrals in product(range(size), repeat=checks):
        if len(set(referrals)) != 1:
            continue
        prob = Fraction(1)
        for teacher in referrals:
            prob *= probabilities[teacher]
        total += prob
        if referrals[0] < first:
            first_mass += prob
    return (first_mass*(1-flip)+(total-first_mass)*flip)/total, total


def binomial_row(n, p):
    return [comb(n, j)*p**j*(1-p)**(n-j) for j in range(n+1)]


def stationary_classroom(size, checks, flip):
    # Independent apprentices stop on first agreement. Exact transition law;
    # normalized power iteration below is a floating-point approximation.
    transition = [binomial_row(size, float(referral_law(j, size, checks, flip)[0]))
                  for j in range(size+1)]
    # Half the stationary mass on each mirror pair by exchange of service names.
    mass = binomial_row(size, 0.5)
    for it in range(10000):
        nxt = [fsum(w*row[j] for w,row in zip(mass,transition)) for j in range(size+1)]
        total = fsum(nxt)
        nxt = [v/total for v in nxt]
        difference = sum(abs(a-b) for a,b in zip(mass,nxt))
        mass = nxt
        if difference < 2e-14:
            break
    else:
        raise ArithmeticError("classroom stationary iteration did not converge")
    centered = [j/size-0.5 for j in range(size+1)]
    variance = fsum(p*v*v for p,v in zip(mass,centered))
    lag = fsum(mass[i]*centered[i]*fsum(v*q for v,q in zip(centered,row))
               for i,row in enumerate(transition))/variance
    coverage = 1-fsum(p*abs(v) for p,v in zip(mass,centered))
    average = fsum(j*p/size for j,p in enumerate(mass))
    assert abs(average-0.5) < 1e-10
    return coverage, lag, mass[0]+mass[-1]


def inherited_ranking(share, expression, checks, flip, copy_action):
    """Independent action expression and nomination, then copy code or behavior."""
    faithful = (1+expression)/2
    # Entries are the masses of (encoded ranking, expressed job) in this epoch.
    entries = {(1,1): share*faithful, (1,0): share*(1-faithful),
               (0,1): (1-share)*(1-faithful), (0,0): (1-share)*faithful}
    workers = {job: sum(w for (_,j),w in entries.items() if j==job) for job in (0,1)}
    winners = {pair: w/(2*workers[pair[1]])**checks for pair,w in entries.items()}
    positive = sum(w for (code,job),w in winners.items() if (job if copy_action else code)==1)
    return flip+(1-2*flip)*positive/sum(winners.values())


def mechanism_checks():
    mu = Fraction(3,16)
    a = 1-2*mu
    # At beta=4/3 and 3 referrals the pre-error odds are the square of
    # provider odds. This uses (request odds)^3 = (provider odds)^4.
    for share in (Fraction(1,4),Fraction(3,4)):
        odds = share/(1-share)
        before = odds**4 / odds**2
        assert mu+a*before/(1+before) == share

    expression = Fraction(17,20)
    gap = Fraction(1,10**6)
    for copy_action in (True,False):
        above = inherited_ranking(Fraction(1,2)+gap,expression,3,mu,copy_action)
        below = inherited_ranking(Fraction(1,2)-gap,expression,3,mu,copy_action)
        slope = a*(-2)*expression if copy_action else a*(1-3*expression**2)
        assert abs((above-below)/(2*gap)-slope) < Fraction(1,10**9)
        print("Action copying" if copy_action else "Ranking inheritance", "local slope", float(slope))

    # Within-person updates and offspring pooling.
    p = (Fraction(1,10),Fraction(9,10))
    success = 3
    weight = [1+(success-1)*v for v in p]
    local = [success*v/d for v,d in zip(p,weight)]
    assert sum(local)/2 == Fraction(17,28)
    assert sum(d*g for d,g in zip(weight,local))/sum(weight) == Fraction(3,4)
    for n in (8,16,32,64):
        budget = 1
        target = (1+1/float(a))/3
        no_match = 1-1/n**2
        from math import ceil, log1p
        budget = ceil(log1p(-target)/log(no_match))
        assert 1-no_match**(budget-1) <= target < 1-no_match**budget
        print("Minimum nomination triples for local instability",n,budget)


def main():
    mechanism_checks()
    flip = Fraction(3,16)
    for first in range(1,8):
        for checks in (1,2,3):
            assert referral_law(first,8,checks,flip) == enumerate_referrals(first,8,checks,flip)
    assert referral_law(2,8,3,flip) == (Fraction(3,4), Fraction(5,144))
    assert referral_law(6,8,3,flip)[0] == Fraction(1,4)
    assert referral_law(4,8,3,flip) == (Fraction(1,2), Fraction(1,64))
    print("class size, referral count, expected demand served, lag-one correlation, boundary mass")
    for n in (16,32,64,128):
        for d in (1,2,3):
            coverage, lag, boundary = stationary_classroom(n,d,flip)
            print(n,d,f"{coverage:.6f}",f"{lag:.6f}",f"{boundary:.3g}")


if __name__ == "__main__":
    main()
