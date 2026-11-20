"""W7.2. Distinct errors in random panels from Emerson et al. (2010), Table.

Inputs are rounded published counts, means and sample standard deviations.
The unknown identities of the seven errors are varied, never imputed.
"""
from fractions import Fraction as F
from math import comb


def moments(n, mean, sd):
    radius = F(1, 200)
    mean, sd = F(mean), F(sd)
    sums = [v for v in range(7*n+1) if abs(F(v,n)-mean) <= radius]
    assert len(sums)==1
    hits = sums[0]
    squares = [v for v in range(hits,7*hits+1,2)
               if (sd-radius)**2 <= (v-F(hits**2,n))/(n-1) <= (sd+radius)**2]
    assert len(squares)==1
    return hits, squares[0]


def histograms(n, hits, squares):
    """All row-size histograms, from the observed number of co-detections."""
    pairs = (squares-hits)//2
    def visit(size, left_hits, left_pairs, rows):
        if size==1:
            zeros=n-sum(rows)-left_hits
            if left_pairs==0 and zeros>=0:
                yield [zeros,left_hits]+list(reversed(rows))
            return
        cost=comb(size,2)
        for count in range(min(left_pairs//cost,left_hits//size)+1):
            yield from visit(size-1,left_hits-size*count,left_pairs-cost*count,rows+[count])
    yield from visit(7,hits,pairs,[])


def distinct(n, sizes, m):
    return sum(1-F(comb(n-h,m),comb(n,m)) for h in sizes)


def main():
    journal1 = moments(60,"0.52","0.68")
    journal2 = moments(50,"0.28","0.45")
    assert journal1 == (31,43) and journal2 == (14,14)
    totals = moments(110,"0.41","0.60")
    assert totals == tuple(a+b for a,b in zip(journal1,journal2))
    assert moments(100,"0.85","1.16") == (85,205)
    # The second journal's detections are all singletons. Preserve its
    # table as well as the pooled moments for every example.
    nested = []
    for hist in histograms(60,*journal1):
        hist[0] += 36
        hist[1] += 14
        nested.append([sum(hist[j:]) for j in range(1,8)])
    assert len(nested)==4
    for m in (1,2,3,4):
        low = min(distinct(110,v,m) for v in nested)
        high = distinct(110,[7,7,7,6,6,6,6],m)
        if m==3:
            without_four = min(distinct(110,v,m) for v in nested if v[3]==0)
            assert low < F(85,100) < without_four
            print("Three-review lower bound if nobody found four",float(without_four))
        print("Panel size",m,"attainable mean distinct errors",
              round(float(low),7),round(float(high),7))
    assert distinct(110,[7,7,7,6,6,6,6],2) < F(85,100)
    assert min(distinct(110,v,4) for v in nested) > F(85,100)


if __name__ == "__main__":
    main()
