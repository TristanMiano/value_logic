"""Selecting a review practice when the reviewer's local reliability is unknown."""
from fractions import Fraction as F
from functools import lru_cache


HIGH,LOW,BASE = F(17,20),F(7,20),F(3,5)
JOBS = 16


def beliefs(passed,failed):
    hi = HIGH**passed*(1-HIGH)**failed
    lo = LOW**passed*(1-LOW)**failed
    prior = hi/(hi+lo)
    return prior, prior*HIGH+(1-prior)*LOW


def evaluate(fee,maximum=8):
    @lru_cache(None)
    def value(passed,failed):
        _,q = beliefs(passed,failed)
        rewards = {"adopt":q,"reverse":1-q,"fallback":BASE}
        best = max(rewards,key=rewards.get)
        stop = JOBS*rewards[best]
        if passed+failed == maximum:
            return stop,best
        yes,_ = value(passed+1,failed)
        no,_ = value(passed,failed+1)
        inspect = q*yes+(1-q)*no-fee
        return (inspect,"audit") if inspect>stop else (stop,best)

    @lru_cache(None)
    def performance(passed,failed,theta):
        action=value(passed,failed)[1]
        if action == "audit":
            a,b=performance(passed+1,failed,theta),performance(passed,failed+1,theta)
            return (theta*a[0]+(1-theta)*b[0],1+theta*a[1]+(1-theta)*b[1])
        hit={"adopt":theta,"reverse":1-theta,"fallback":BASE}[action]
        return JOBS*hit,F(0)
    @lru_cache(None)
    def myopic(passed,failed):
        _,q=beliefs(passed,failed)
        def stop(i,j):
            _,p=beliefs(i,j)
            return JOBS*max(p,1-p,BASE)
        now=stop(passed,failed)
        if passed+failed==maximum:
            return now,0
        immediate=q*stop(passed+1,failed)+(1-q)*stop(passed,failed+1)-fee
        if immediate<=now:
            return now,0
        go1,n1=myopic(passed+1,failed)
        go0,n0=myopic(passed,failed+1)
        return q*go1+(1-q)*go0-fee,1+q*n1+(1-q)*n0
    greedy,n_greedy=myopic(0,0)
    assert greedy<=value(0,0)[0]
    print("Local advantageous one-test branch construction: value/mean tests",
          round(float(greedy),6),round(float(n_greedy),4))
    success = []
    for theta in (HIGH,LOW):
        actual,audits = performance(0,0,theta)
        success.append(actual-fee*audits)
        print("Fee, realized regime, correct jobs out of 16, audits",
              float(fee),float(theta),round(float(actual),5),round(float(audits),5))
    avg = sum(success)/2
    assert avg==value(0,0)[0]
    print("Net per placement",round(float(avg),6),"over best fixed",round(float(avg-JOBS*BASE),6))
    vals = []
    for n in range(maximum+1):
        from math import comb
        gross=F(0)
        for i in range(n+1):
            prior,q=beliefs(i,n-i)
            hist=(HIGH**i*(1-HIGH)**(n-i)+LOW**i*(1-LOW)**(n-i))/2
            gross+=comb(n,i)*hist*JOBS*max(q,1-q,BASE)
        vals.append(gross-fee*n)
    print("Best fixed sample size/value",max(range(len(vals)),key=vals.__getitem__),
          round(float(max(vals)),6))
    return avg


def originate():
    def stop(i,j):
        _,p=beliefs(i,j)
        return JOBS*max(p,1-p,BASE)
    def increment(i,j):
        _,p=beliefs(i,j)
        return p*stop(i+1,j)+(1-p)*stop(i,j+1)-stop(i,j)
    assert increment(0,0)==1
    exposure,upkeep,fee=F(1,5),F(1,10),F(1,4)
    print("Single-rule gains along byproduct route",
          exposure*increment(0,0)-upkeep,(1-exposure)*(increment(0,0)-fee))
    for history in [(1,0),(0,1)]:
        print("Gross value of one more judgment after",history,increment(*history))


def team_review():
    from math import comb
    size=4
    a,fee=F(7,10),F(6,5)
    def gross(n):
        value=F(0)
        for i in range(n+1):
            _,q=beliefs(i,n-i)
            prob=(HIGH**i*(1-HIGH)**(n-i)+LOW**i*(1-LOW)**(n-i))/2
            value+=comb(n,i)*prob*JOBS*max(q,1-q,BASE)
        return value
    B=[gross(n) for n in range(size+1)]
    print("Public benefit by number of distinct tests",[round(float(v),6) for v in B])
    for rho in (F(0),F(13,100),F(1,5),F(1)):
        b=[B[0]]+[(1-rho)*v+rho*B[1] for v in B[1:]]
        coef=[a*(b[-1]-b[0])+(1-a)*(hi-lo)-fee for lo,hi in zip(b,b[1:])]
        def diff(x):
            return sum(v*comb(size-1,i)*x**i*(1-x)**(size-1-i)
                       for i,v in enumerate(coef))
        print("Shared data",rho,"selection differences rare / three quarters / fixation",
              [round(float(diff(x)),6) for x in (F(0),F(3,4),F(1))])
        if rho==F(13,100):
            assert [(v>0) for v in coef]==[True,True,False,True]
            assert diff(F(3,4))<0
            # Opposite endpoint signs in each bracket; exactly two roots by Descartes.
            for left,right in [(F(0),F(3,4)),(F(3,4),F(1))]:
                for _ in range(35):
                    mid=(left+right)/2
                    if (diff(left)>0)==(diff(mid)>0):
                        left=mid
                    else:
                        right=mid
                print("Interior rest point",round(float((left+right)/2),7))
        if rho==0:
            assert min(coef)>0
        if rho==1:
            assert max(coef)<0


def gated():
    for theta,yes,no in ((HIGH,F(2,5),F(2,5)),(LOW,F(34,35),F(6,65))):
        these=(theta*yes,(1-theta)*no,1-theta*yes-(1-theta)*no)
        assert these==(F(17,50),F(3,50),F(3,5))
    threshold=HIGH*(1-BASE)/(BASE*(1-HIGH))
    assert threshold==F(34,9)
    print("Max favorable retention ratio for guaranteed advantage",threshold)
    print("Twofold retention ratio lower success",HIGH/(HIGH+2*(1-HIGH)))


if __name__=="__main__":
    for amount in (F(0),F(1,10),F(1,4),F(1,2),F(1)):
        evaluate(amount)
    gated()
    originate()
    team_review()
