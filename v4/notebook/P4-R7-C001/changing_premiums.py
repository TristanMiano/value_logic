"""Independently test partial reprioritization against all policies on a finite grid."""
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog


def check(fee, switch):
    exposure, peak = F(3,20), F(4,5)
    lower = min(peak/2,2*fee*switch/exposure)
    upper = peak-lower
    exact = exposure*lower**2/2 + fee*switch*(upper-lower)
    fixed, complete = exposure*peak**2/8, fee*switch*peak

    # Occupation mass over (present teaching regime, inherited and new premiums).
    grid = sorted(set([F(i,10) for i in range(9)]+[lower,upper]))
    states = [(z,h) for z in (0,1) for h in grid]
    columns = [(z,previous,h) for z,previous in states for h in grid]
    flow = np.zeros((1+len(states),len(columns)))
    flow[-1] = 1.
    costs = []
    for j,(z,previous,h) in enumerate(columns):
        flow[states.index((z,previous)),j] = 1
        flow[states.index((z,h)),j] -= float(1-switch)
        flow[states.index((1-z,h)),j] -= float(switch)
        costs.append(float(exposure*(h-z*peak)**2/2 + fee*abs(h-previous)))
    target = np.zeros(len(states)+1)
    target[-1] = 1
    outcome = linprog(costs,A_eq=flow,b_eq=target,bounds=(0,None),method="highs")
    assert outcome.success and abs(outcome.fun-float(exact)) < 1e-8
    print("Switch, fee, selected premiums, material loss, fixed, full response",
          switch,fee,(str(lower),str(upper)),exact,fixed,complete)


if __name__ == "__main__":
    for switch in (F(1,10),F(1,2)):
        for fee in (F(0),F(1,20),F(3,20),F(3,10),F(1)):
            check(fee,switch)
