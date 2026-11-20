"""W7.6. Project and survival tradeoffs, transmitted ends and finite-evidence revisions."""
from fractions import Fraction as F
from math import ceil, expm1, log, log1p


def funded_choice():
    # Current installments are payable even if a later check cannot be made.
    safe,work,high=F(9,10),F(3,5),F(1,4)
    survival=(1-high)*safe+high*work
    value=10*high/(1-survival)
    threshold=(safe-work)*value
    assert 1<threshold<10 and value==F(100,7)
    assert value==(1-high)*max(safe*value,1+work*value)+high*max(safe*value,10+work*value)
    print("Risky-work threshold",threshold,"ten-period survival",float(survival**10),
          float(safe**10))
    # Both actions face permanent risk. A trustee completes the same project
    # after a founder's departure. Compare using prospective variables only.
    for direct,coverage in ((F(0),F(1)),(F(2,5),F(1)),(F(0),F(3,5))):
        price=(safe-work)*(1-coverage+direct)
        print("Matched-menu price; founder value, believed trustee coverage",direct,coverage,price)
    # Ridge learners are fitted to actually delivered project receipts. No
    # independent survival reward is ever supplied. Validate normal equations.
    for escrowed in (0,1,4,20):
        common,fee=100,1
        det=common*escrowed+fee*(2*common+escrowed)+fee**2
        project=F(common*escrowed+fee*(common+escrowed),det)
        survival_weight=F(fee*common,det)
        assert (common+escrowed+fee)*project+common*survival_weight==common+escrowed
        assert common*project+(common+fee)*survival_weight==common
        menu=[F(i,100) for i in range(1,21)]
        bought=[z for z in menu if survival_weight*(safe-work)>z]
        print("Escrowed records",escrowed,"matched price",round(float((safe-work)*survival_weight),5),
              "largest bought",str(max(bought,default=0)))


def transmission(x,local):
    # Adults choose according to their encoded end. Count physical survivors
    # and their work receipts in the two habitats before allocating places.
    weights=((F(4,5)*5,F(1,2)*2),(F(4,5)*F(5,4),F(1,2)*4))
    per_patch=[(x*s,(1-x)*p) for s,p in weights]
    local_share=sum(s/(s+p) for s,p in per_patch)/2
    global_share=sum(s for s,p in per_patch)/sum(s+p for s,p in per_patch)
    return local*local_share+(1-local)*global_share


def encoded_ends():
    assert transmission(F(5,6),F(1))==F(5,6)
    for local in (F(0),F(3,4),F(16,21),F(4,5),F(1)):
        x=0.23
        for _ in range(2000):
            x=float(transmission(x,float(local)))
        print("Share of places assigned locally",local,"safe end after 2000 rounds",round(x,6))
    for x in (F(1,8),F(2,3),F(19,20)):
        for local in (F(0),F(4,5),F(1)):
            pressure=local*(3/(1+3*x)-1/(2-x))/2+(1-local)/(F(3,2)+x)
            assert transmission(x,local)-x==x*(1-x)*pressure


def check_depths():
    s,f,gain,loss=F(9,10),F(1,5),F(3),F(2)
    for prevalence in (F(1,1000),F(1,100),F(1,10),F(1,4)):
        u=prevalence
        def cash(k):
            return u*gain*s**k-(1-u)*loss*f**k
        depth=max(0,ceil(log((1-u)*loss*(1-f)/(u*gain*(1-s)))/log(s/f)))
        assert cash(depth)==max(cash(k) for k in range(50))
        hazard=u*s**depth+(1-u)*f**depth
        print("Useful offers, optimal review depth and physical edit hazard",u,depth,float(hazard))


def physical_edits():
    # Time spent at each grade is geometric. Each season has an independent
    # production proposal and a possible workshop-comparison experiment.
    eta=.5
    f=.5
    for power in (0,1,2):
        values=[]
        for k in (1,4,16,32,64,128):
            p=f**k
            budget=(k+1)**power
            upgrade=eta*(-expm1(budget*log1p(-(1-f)*p)))
            ever=p/(p+upgrade-p*upgrade)
            values.append(round(ever,7))
        print("Comparison budget exponent",power,"grade edit probabilities",values)
    for power in (0,1,2):
        for k in (1,3,8):
            p=F(1,2)**k
            trials=(k+1)**power
            up=F(1,2)*(1-(1-F(1,2)*p)**trials)
            ever=p/(p+up-p*up)
            assert ever==p+(1-p)*(1-up)*ever


def voluntary_adoption():
    p,V,d,b,c=F(1,2),8,1,4,F(3,2)
    setup,freeze,weight=F(1,2),F(1,2),F(1,2)
    assert weight*b>d and p*b>c
    old_gain=p*(V-d)-setup-freeze
    assert old_gain==F(5,2)
    for fee in (F(13,10),F(1,10)):
        bond=p*V-c*d/b-fee
        print("Binding control fixed price",fee,"old incumbent: true adoption/control",old_gain,bond)
    # A held-out exchange after settlement compares same private cost and new
    # partner benefit. An expired one-job instrument has no effect here.
    assert -F(1)+weight*F(3)>0 and -F(1)<0


if __name__=="__main__":
    funded_choice()
    encoded_ends()
    check_depths()
    physical_edits()
    voluntary_adoption()
