"""W7.2. Payoffs for inherited revision rules and advisers who choose to file."""

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Rule:
    name: str
    useful: F    # Probability this rule accepts a filed, appropriate change
    mistaken: F  # Probability this rule accepts a filed, inappropriate change
    upkeep: F


OPEN = Rule("open", F(1), F(1), F(0))
GUARD = Rule("guarded", F(9,10), F(1,10), F(3,20))
RIGID = Rule("rigid", F(0), F(0), F(0))
LOW, HIGH = F(9,20), F(13,20)


def filing(accept):
    """A file earns one adoption bonus and has an independent private cost."""
    return min(F(1), max(F(0), (accept-LOW)/(HIGH-LOW)))


def payoff(rule, population, disclosure, change=F(1,4)):
    """Expected resource gain from the adviser’s two information sets."""
    result = -rule.upkeep
    assert sum(weight for _,weight in population) == 1
    for field, chance, benefit in (("useful", change, 3), ("mistaken", 1-change, -2)):
        own = getattr(rule,field)
        hidden = sum(weight*getattr(other,field) for other,weight in population)
        rate = disclosure*filing(own)+(1-disclosure)*filing(hidden)
        result += chance*rate*own*benefit
    return result


def two_type_gain(first, second, share, disclosed, change=F(1,4)):
    population = ((first,share),(second,1-share))
    return payoff(first,population,disclosed,change)-payoff(second,population,disclosed,change)


def finite_fixation(size, founders, disclosed, baseline=3):
    """Absorption in a finite birth/death population of guarded and rigid programs."""
    from math import exp, fsum, log

    logarithms = [0.0]
    for k in range(1,size):
        delta = float(two_type_gain(GUARD,RIGID,F(k,size),disclosed))
        logarithms.append(logarithms[-1] + log(baseline/(baseline+delta)))
    largest = max(logarithms)
    weights = [exp(v-largest) for v in logarithms]
    return [fsum(weights[:j])/fsum(weights) for j in founders]


def pooled_review():
    from math import comb, fsum, log, prod

    # Each binomial probability at p=1/4 has the common denominator 4^n.
    # Raising to that power gives an exact sign check for the average log.
    for n in (1,2,3):
        ratios = [(F(12,5)+F(27,10)*k/n)/3 for k in range(n+1)]
        counts = [comb(n,k)*3**(n-k) for k in range(n+1)]
        powered = prod(r**w for r,w in zip(ratios,counts))
        assert (powered > 1) == (n >= 3)
        gap = fsum(w*log(r) for r,w in zip(ratios,counts))/4**n
        print("Independent markets",n,"log growth advantage",round(gap,6))


def audit_schedules():
    # Generate conditional success probabilities by the physical two-state
    # transition. Stop searching after incremental work falls below its mean.
    for switch, cost in ((F(1,20),F(3,4)),(F(2,5),F(3,4)),(F(1,10),F(3,10))):
        if cost >= 1/(4*switch):
            print("Audit schedule", switch, cost, "no paid inspection; mean 0.5")
            continue
        success, total = F(1), -cost
        for length in range(1,10000):
            total += success
            value = total/length
            formula = F(1,2)+((1-(1-2*switch)**length)/(4*switch)-cost)/length
            assert value == formula
            success = (1-switch)*success+switch*(1-success)
            if success <= value:
                print("Audit schedule",switch,cost,"best length",length,"mean",float(value))
                break
        else:
            raise ArithmeticError("optimal interval not found")


def joint_dynamics():
    # Hidden clients and a second inherited trait: advisers that recommend
    # appropriately or ones that submit every proposal. Constant application cost.
    x0, y0 = F(1,2), F(1,6)
    cx, cy = F(27,20), F(27,40)
    for x in (F(1,13),F(4,9),F(5,6)):
        for y in (F(1,8),F(1,4),F(9,10)):
            # Material receiver payoffs under unconditional versus guarded receipt.
            open_gain = F(1,4)*3 - F(3,4)*2*y
            guard_gain = F(1,4)*3*GUARD.useful - F(3,4)*2*GUARD.mistaken*y - GUARD.upkeep
            filing_advantage = F(3,4)*(x+(1-x)*GUARD.mistaken-F(11,20))
            assert open_gain-guard_gain == cx*(y0-y)
            assert filing_advantage == cy*(x-x0)
            assert cy*(x-x0)*(open_gain-guard_gain) + cx*(y-y0)*filing_advantage == 0


def funded_signal():
    # An independent adviser can buy a noisy indication before learning
    # their private filing cost. Integrate the positive filing surplus over H.
    accuracy = F(4,5)
    prior = F(1,4)
    chance_good_tip = prior*accuracy+(1-prior)*(1-accuracy)
    private_value = receiver_return = F(0)
    for useful, mistaken in ((prior*accuracy,(1-prior)*(1-accuracy)),
                             (prior*(1-accuracy),(1-prior)*accuracy)):
        mass=useful+mistaken
        acceptance=(useful*GUARD.useful+mistaken*GUARD.mistaken)/mass
        ceiling=min(HIGH,max(LOW,acceptance))
        share=(ceiling-LOW)/(HIGH-LOW)
        private_value += mass*share*(acceptance-(ceiling+LOW)/2)
        receiver_return += share*(useful*GUARD.useful*3-mistaken*GUARD.mistaken*2)
    assert chance_good_tip==F(7,20) and private_value==F(9,896)
    assert receiver_return-GUARD.upkeep==F(69,560)
    assert prior*GUARD.useful+(1-prior)*GUARD.mistaken < LOW
    print("Optional adviser investigation",private_value,receiver_return-GUARD.upkeep)


def optimal_response(resident,disclosure,screen):
    # At fixed false acceptance u, admitting passed certificates first
    # maximizes useful acceptance t. Each filing segment is quadratic in u.
    f,s=GUARD.mistaken,GUARD.useful
    points={F(0),LOW,HIGH,F(1)}
    if screen:
        points.add(f)
        for threshold in (LOW,HIGH):
            u=threshold*f/s if threshold<=s else f+(1-f)*(threshold-s)/(1-s)
            points.add(u)
    def value(u):
        t=min(s*u/f,s+(1-s)*(u-f)/(1-f)) if screen else u
        rule=Rule("challenger",t,u,GUARD.upkeep if screen else F(0))
        return payoff(rule,resident,disclosure)
    checks=sorted(points)
    for left,right in zip(checks,checks[1:]):
        a,b,mid=value(left),value(right),value((left+right)/2)
        curvature=2*(a+b-2*mid)
        linear=b-a-curvature
        if curvature<0:
            vertex=-linear/(2*curvature)
            if 0<vertex<1:
                points.add(left+vertex*(right-left))
    return max((value(u),u) for u in points)


def disclosure_thresholds():
    relaxed=Rule("optimal visible",F(169,180),LOW,GUARD.upkeep)
    visible=((relaxed,F(1)),)
    rigid=((RIGID,F(1)),)
    hidden=((OPEN,F(23,54)),(GUARD,F(31,54)))
    assert optimal_response(hidden,0,True)==(F(1,2),GUARD.mistaken)
    assert optimal_response(hidden,0,False)==(F(1,2),F(1))
    for q in (F(47,360),F(9,50),F(36,169),F(1)):
        own=payoff(relaxed,visible,q)
        assert optimal_response(visible,q,True)==(own,LOW)
        assert optimal_response(visible,q,False)[0]<=own
        assert optimal_response(rigid,q,True)[0]==q*F(169,240)-GUARD.upkeep
        print("Full certificate menu; visibility, rare in rigid, guard among own",
              q,optimal_response(rigid,q,True)[0],own)
    assert optimal_response(rigid,F(36,169),True)[0]==0
    assert optimal_response(visible,F(47,360),False)[0]==F(133,240)


def who_learns():
    # A fixed license is bought before an adviser learns its client's type.
    from math import log,sqrt
    gross=F(153,560)
    info=F(9,896)
    private_fee=F(1,125)
    x_star,y_star=private_fee/info,GUARD.upkeep/gross
    def signed_root(reference,x):
        d=reference*log(reference/x)+(1-reference)*log((1-reference)/(1-x))
        return (1 if x>=reference else -1)*sqrt(max(0,d))
    for x in (.1,.5,.95):
        lo,hi=0.,1.
        for _ in range(50):
            y=(lo+hi)/2
            if sqrt(float(info))*signed_root(float(x_star),x)+sqrt(float(gross))*signed_root(float(y_star),y)>0:
                hi=y
            else:
                lo=y
        print("Initial reviewers, critical trained advisers",x,round((lo+hi)/2,6))
    # The private adoption prize values advance access to a realized
    # certificate differently from learning a new fact about production.
    correct_tip,wrong_tip=F(27,280),F(9,1120)
    correct_leak,wrong_leak=F(9,40),F(3,40)
    assert 3*(correct_leak-correct_tip)/(wrong_leak-wrong_tip)==F(144,25)
    for loss in (2,8):
        print("Loss from a bad switch; independent/advance certificate payoffs",
              loss,3*correct_tip-loss*wrong_tip-GUARD.upkeep,
              3*correct_leak-loss*wrong_leak-GUARD.upkeep)


def main():
    disclosure_thresholds()
    who_learns()
    funded_signal()
    joint_dynamics()
    pooled_review()
    audit_schedules()
    q = F(9,50)
    for n in (64,256,1024):
        counts = [1,n//4,n//2,3*n//4]
        for visible in (q,F(3,10)):
            print("Finite guarded fixation",n,float(visible),counts,
                  [round(v,7) for v in finite_fixation(n,counts,visible)])
    all_guard = ((GUARD,F(1)),)
    all_rigid = ((RIGID,F(1)),)
    print("visibility 0.18, payoffs open / guarded / rigid when resident is")
    for pop in (all_guard,all_rigid):
        gains = [payoff(rule,pop,q) for rule in (OPEN,GUARD,RIGID)]
        print(pop[0][0].name, *(f"{float(g):.6f}" for g in gains))
        assert gains[(OPEN,GUARD,RIGID).index(pop[0][0])] == max(gains)
    hidden_open = F(23,54)
    assert two_type_gain(OPEN,GUARD,hidden_open,F(0)) == 0
    assert payoff(OPEN,((OPEN,hidden_open),(GUARD,1-hidden_open)),F(0)) == F(1,2)
    hidden_filing = (GUARD.upkeep/(F(1,4)*GUARD.useful*3)-q)/(1-q)
    threshold = (LOW+(HIGH-LOW)*hidden_filing)/GUARD.useful
    assert two_type_gain(GUARD,RIGID,threshold,q) == 0
    print("Hidden open share",hidden_open,"guarded seed threshold",threshold,float(threshold))
    for i in range(101):
        x=F(i,100)
        d1=two_type_gain(OPEN,GUARD,x,F(0))
        d2=two_type_gain(GUARD,RIGID,x,q)
        assert (d1>0) == (x<hidden_open)
        assert (d2>0) == (x>threshold)
    for rule in (OPEN,GUARD,RIGID):
        print(rule.name,"full disclosure ordinary and rare change",
              float(payoff(rule,all_guard,1)),float(payoff(rule,all_guard,1,F(1,100))))
    # When every filing costs the same regardless of truth, blind partial
    # acceptance induces the same filing frequency on both sorts of occasion.
    for j in range(101):
        accept=F(j,100)
        blind=Rule("blind lottery",accept,accept,F(0))
        assert payoff(blind,all_guard,1) <= 0
    # Guarded rule that also honors a share of negative certificates. Choose
    # this probability so false acceptance remains just below the lowest cost.
    loose=F(19,50)
    relaxed=Rule("relaxed",GUARD.useful+(1-GUARD.useful)*loose,
                 GUARD.mistaken+(1-GUARD.mistaken)*loose,GUARD.upkeep)
    assert relaxed.mistaken<LOW and relaxed.useful>HIGH
    assert payoff(relaxed,all_guard,1) > payoff(GUARD,all_guard,1)
    print("Tested relaxation",float(payoff(relaxed,all_guard,1)))


def testing_a_review_rule():
    """Hide a rule assignment until filing or announce it in advance."""
    def value(tau, cheap):
        u = F(1,10)+F(9,10)*tau
        share = max(0,min(1,(u-LOW)/(HIGH-LOW))) if cheap else 0
        return F(21,40)+F(9,40)*tau-F(3,2)*u*share
    cutoff = F(7,18)
    guarded, open_a, open_b = value(0,True), value(1,True), value(1,False)
    baseline = value(cutoff,True)
    assert guarded==F(21,40) and open_a==-F(3,4) and open_b==F(3,4)
    assert baseline==value(cutoff,False)==F(49,80)
    for k in range(101):
        tau=F(k,100)
        assert (value(tau,True)+value(tau,False))/2 <= baseline
    revealing=(HIGH-F(1,10))/F(9,10)
    assert revealing==F(11,18)
    now=(value(revealing,True)+value(revealing,False))/2
    assert now==F(7,40)
    for h in (8,9):
        gain=now-baseline+h*F(3,8)*(open_b-baseline)
        assert (gain>0)==(h==9)
        print("Announced mixed pilot",revealing,"future",h,"net advantage",gain)
    for h in range(17):
        ordinary=2+(h+1)*baseline
        change_a=open_a-baseline
        change_b=(open_b-baseline)*(1+F(3,4)*h)
        product_gain=(ordinary+change_a)*(ordinary+change_b)-ordinary**2
        assert (product_gain>0)==(h>=14)
        pilot_a=value(revealing,True)-baseline
        pilot_b=value(revealing,False)-baseline+F(3,4)*h*(open_b-baseline)
        partial_product=(ordinary+pilot_a)*(ordinary+pilot_b)-ordinary**2
        assert (partial_product>0)==(h>=10)
        if h in (9,10):
            print("Mixed pilot ecological change",h,(pilot_a+pilot_b)/2,partial_product)
        if h in (12,13,14):
            print("Later jobs",h,"arithmetic gain",(change_a+change_b)/2,
                  "two-habitat product gain",product_gain)
    for control in (guarded, baseline):
        advantage = F(3,8)*(open_b-control)
        for future in (6,7,11,12):
            print("Pre-filing pilot: comparator",control,"later jobs",future,
                  "increment",future*advantage-control)


if __name__=="__main__":
    main()
    testing_a_review_rule()
