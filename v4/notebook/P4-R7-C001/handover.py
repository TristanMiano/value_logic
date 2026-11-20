"""Loss and transmission of a demonstrated work technique in a finite group."""
from fractions import Fraction as F
from math import comb

import numpy as np


def mass(n, k, p):
    return comb(n,k)*p**k*(1-p)**(n-k)


def transition(n, b, s, t, reserve):
    if reserve and b==n:
        raise ValueError("a handover requires a place for one experienced carrier")
    matrix=[]
    for r in range(n+1):
        row=[F(0)]*(n+1)
        if not r:
            row[0]=1
        else:
            keep=int(reserve)
            for h in range(keep, min(r,n-b)+1):
                ordinary = n-b-h
                if ordinary>n-r:
                    continue
                survive=F(comb(r-keep,h-keep)*comb(n-r,ordinary),
                          comb(n-keep,b))
                if not h:
                    row[0]+=survive
                    continue
                for a in range(ordinary+1):
                    for c in range(b+1):
                        row[h+a+c]+=survive*mass(ordinary,a,s)*mass(b,c,t)
        assert sum(row)==1
        matrix.append(row)
    return matrix


def main():
    n,s,t = 6,F(1,20),F(9,10)
    for b in range(n+1):
        for reserve in ((False,True) if 0<b<n else (False,)):
            P=transition(n,b,s,t,reserve)
            # From one qualified source, all acquisition depends on retaining it.
            factor = F(1) if reserve else F(n-b,n)
            assert sum(i*w for i,w in enumerate(P[1]))==factor*(1+(n-b-1)*s+b*t)
            x=np.eye(n+1)[1]
            p=np.array(P,dtype=float)
            rows=[]
            for j in range(1,29):
                x=x@p
                if j in [1,7,28]:
                    rows.append(tuple(round(v,5) for v in (x@np.arange(n+1)/n,1-x[0])))
            print("Replacements / handover",b,reserve,"mean technique share / survives",rows)


if __name__ == "__main__":
    main()
