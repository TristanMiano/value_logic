"""W7.4. Behavioral identification under defaults and feasibility of informed exit."""
from fractions import Fraction as F
from itertools import product

from scipy.optimize import linprog


def always_buyers(g0,green_share0,g1,green_share1,entrants):
    buy0,buy1=g0/green_share0,g1/green_share1
    always=buy1-entrants
    assert 0<always<=buy0 and 0<=entrants<=1-buy0
    lower=max(F(0),g1-entrants-g0)/always
    # Unknown individual response types: no purchase, ordinary, green under
    # each invitation. Independent group means specify only two marginals.
    left=(1-buy0,buy0-g0,g0)
    right=(1-buy1,buy1-g1,g1)
    eq=[[int(i==k) for i,j in product(range(3),repeat=2)] for k in range(3)]
    eq.extend([[int(j==k) for i,j in product(range(3),repeat=2)] for k in range(3)])
    eq.append([int(i==0 and j>0) for i,j in product(range(3),repeat=2)])
    obj=[int(i==1 and j==2) for i,j in product(range(3),repeat=2)]
    result=linprog(obj,A_eq=eq,b_eq=list(map(float,(*left,*right,entrants))),bounds=(0,None))
    assert result.success and abs(result.fun-float(always*lower))<1e-8
    return lower


def main():
    g0,h0=F(62,10000),F(72,1000)
    g1,h1=F(558,10000),F(691,1000)
    for e in (0,F(1,100),F(3,100),F(496,10000)):
        mid=always_buyers(g0,h0,g1,h1,e)
        possible=[always_buyers(g0+i*F(1,20000),h0+j*F(1,2000),
                                g1+k*F(1,20000),h1+m*F(1,2000),e)
                  for i,j,k,m in product((-1,1),repeat=4)]
        print("New buyers allowed among all visits",float(e),"forced standard-to-green",
              round(float(mid),5),"rounding range",tuple(round(float(f(possible)),5) for f in (min,max)))


if __name__=="__main__":
    main()
