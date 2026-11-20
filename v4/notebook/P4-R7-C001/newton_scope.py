"""W7.5 handoff to W2: approximation, externally settled jobs and scope."""
from fractions import Fraction as F
from math import comb, sqrt

import numpy as np


def exact_energy(x):
    s=sqrt(1-x*x)
    return x*x/(s*(1+s))


def multiplier(x):
    s=sqrt(1-x*x)
    return 2/(s*(1+s))


def cutoff(tolerance):
    s=(sqrt(9-8*tolerance)-1)/2
    return sqrt(1-s*s)


def polynomial(x,k):
    return sum(F(comb(2*j,j),4**j)*x**(2*j) for j in range(1,k+1))


def scope():
    for x in (.02,.08,.10,.60):
        print("Speed in c, relative Newton shortfall",x,1-1/multiplier(x))
    print("Largest speed at 1% and 0.5%",cutoff(.01),cutoff(.005))
    for j in range(1,21):
        lo, hi=polynomial(F(1,10),j),polynomial(F(3,5),j)
        assert float(lo)<=exact_energy(.1)+2e-17
        assert 1-float(F(1,200)/lo)<.01
        if j>=2:
            assert 1-float(F(9,50)/hi)>.20
    # Sufficient derivative bound on [.02,.1] under the displayed law.
    s=sqrt(.99)
    derivative_bound=2*.1*3/(s**3*(1+s)**2)
    radius=.0005
    lipschitz=.16
    grid=[.02*j for j in range(1,6)]
    low=min(map(multiplier,grid))-radius-lipschitz*.01
    high=max(map(multiplier,grid))+radius+lipschitz*.01
    assert derivative_bound<lipschitz and low>=1/1.01 and high<=1/.99
    # A second curve can equal every sample and violate the license between
    # them. The bump is excluded by the stipulated regularity check.
    bump=lambda x: .02*max(0,1-abs(x-.09)/.01)
    assert all(bump(x)<1e-14 for x in grid)
    assert 1-1/(multiplier(.09)+bump(.09))>.01
    print("Conditional envelope / sufficient slope bound",low,high,derivative_bound)
    rng=np.random.default_rng(752)
    n=32768
    actual=np.array([multiplier(x) for x in grid])
    average=actual+.02*(2*rng.binomial(n,.5,len(grid))/n-1)
    err=.04*sqrt(np.log(2*len(grid)/.01)/(2*n))
    band=(min(average)-err-.01*lipschitz,max(average)+err+.01*lipschitz)
    print("Simulated five-bin 99% envelope",tuple(round(v,7) for v in band),
          "per-bin readings",n)
    assert band[0]>=1/1.01 and band[1]<=1/.99


def selection():
    grid=(.1,.6)
    weights=np.array([.8,.2])
    measurements=np.array([exact_energy(x) for x in grid])
    models=np.array([[float(polynomial(F(str(x)),k)) for x in grid] for k in range(1,15)])
    physical=((models-measurements)**2)@weights
    assert np.all(np.diff(physical)<0)
    for fee in (1e-3,1e-4,1e-6,1e-8,1e-12):
        # For a fixed unit price, marginal benefit strictly decreases. Confirm
        # the optimum by comparing it with the very next degree as well.
        best=int(np.argmin(physical+fee*np.arange(1,15)))
        assert best<13 and physical[best]-physical[best+1]<fee
        print("Fee per retained coefficient, selected degree",fee,best+1)
    # Observation noise is an input, not the theoretical truth used as a
    # training label. These are independent normalized energy readings per
    # regime with a bounded symmetric zero-mean perturbation.
    rng=np.random.default_rng(7505)
    for n in (32,512,8192,131072):
        read=measurements*(1+(.02/n)*(2*rng.binomial(n,.5,size=2)-n))
        best=int(np.argmin(((models-read)**2)@weights+np.arange(1,15)/n**2))+1
        print("New physical readings per regime",n,"available 14, selected",best)


if __name__=="__main__":
    scope()
    selection()
