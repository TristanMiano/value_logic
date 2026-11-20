"""W7.4. Actual joint offers, two-sided copying, missing voices and transfers."""
from fractions import Fraction as F
from math import exp, log
from random import Random


def gains(x,table):
    return [x*a+(1-x)*b for a,b in zip(*table)]


def best_two(rows):
    # Each column is a line in the probability of choosing row 0. Its
    # minimum is piecewise affine, so include the endpoints and crossings.
    points={F(0),F(1)}
    for i,last_i in enumerate(rows[1]):
        for j,last_j in enumerate(rows[1][:i]):
            slope=(rows[0][i]-last_i)-(rows[0][j]-last_j)
            if slope:
                meet=F(last_j-last_i,slope)
                if 0<meet<1:
                    points.add(meet)
    return max((min(gains(x,rows)),x) for x in points)


def logistic(x):
    if x<0:
        return exp(x)/(1+exp(x))
    return 1/(1+exp(-x))


def run_copying(table,bonus,attenuation,eta=.12,steps=12000):
    # Each column is one stakeholder's forecast gain from an offered rule.
    # Each step is a finite revision with two actual copying factors per side.
    log_x=log_y=total_x=total_y=0.
    for _ in range(steps):
        x,y=logistic(log_x),logistic(log_y)
        returns=[y*r[0]+(1-y)*r[1]+b for r,b in zip(table,bonus)]
        actual=gains(x,table)
        total_x+=x
        total_y+=y
        log_x+=eta*(returns[0]-returns[1])
        log_y+=-eta*(actual[0]-actual[1])+log(attenuation[0]/attenuation[1])
    return total_x/steps,total_y/steps


def odds_example():
    table=((3,-1),(-1,2))
    assert best_two(table)==(F(5,7),F(3,7))
    for name,bonus,survival in (("complete",[0,0],[1,1]),
                                ("publicity",[4,0],[1,1]),
                                ("suppressed second role",[0,0],[1,exp(-.12*5)])):
        x,y=run_copying(table,bonus,survival)
        print(name,"row 0 and critic 0",round(x,6),round(y,6),
              "actual role gains",*(round(v,6) for v in gains(x,table)))
    # Joint sharpness of the row/column range correction.
    B,D,small=F(2),F(3),F(1,100)
    true=((0,0),(-B+small,-B-D+small))
    tilted=((0,D),(small,small))
    assert best_two(true)==(0,1) and best_two(tilted)==(small,0)
    assert min(gains(0,true))==small-B-D


def voluntary_inputs():
    # Each role supplies nonnegative effort s maximizing
    # g*s-(s-base)^2/2. One unit of each is needed per new workshop.
    table=((3,-1),(-1,2))
    for x in (F(0),F(3,7),F(1)):
        g=gains(x,table)
        supply=[max(0,2+v) for v in g]
        assert (min(supply)>2)==(min(g)>0)
    g=gains(1,table)
    assert min(2+g[0],5+g[1])==4 > min(2,5)
    print("Voluntary balanced/surplus-voice capacities",
          min(2+g[0],2+g[1]),min(2+g[0],5+g[1]))


def binary_offers():
    # Prospective participants vote on one binding, fully described lottery.
    table=((F(1),-F(3)),(-F(1,10),F(1)))
    threshold=F(1,11),F(1,4)
    assert best_two(table)==(F(7,51),F(11,51))
    assert min(gains(F(1,2),table))<0
    for i in range(101):
        x=F(i,100)
        assert (min(gains(x,table))>0)==(threshold[0]<x<threshold[1])
    print("Uniform offer acceptance",threshold[1]-threshold[0],
          "expected proposals",1/(threshold[1]-threshold[0]))
    rng=Random(747)
    accepted=sum(min(gains(rng.random(),table))>0 for _ in range(30000))
    print("Seeded acceptance rate",round(accepted/30000,5))


def service_transfer():
    # At rare share 1/4 the three-nomination workshop allocates 9/10 of
    # successful places to rare teachers. One nomination allocates 1/2.
    x=F(1,4)
    p3=x**-2/(x**-2+(1-x)**-2)
    assert p3==F(9,10)
    teaching=F(1,2)-p3
    next_rare=F(3,16)+(1-2*F(3,16))*p3
    clients=abs(next_rare-F(1,2))
    gains_before=[teaching,-teaching,clients]
    gains_after=sum(gains_before)/3
    transfers=[gains_after-g for g in gains_before]
    assert sum(transfers)==0 and all(g+t>0 for g,t in zip(gains_before,transfers))
    assert clients < -teaching
    print("Service change before binding transfers",gains_before,
          "transfers",transfers,"each after",gains_after)


if __name__=="__main__":
    odds_example()
    voluntary_inputs()
    binary_offers()
    service_transfer()
