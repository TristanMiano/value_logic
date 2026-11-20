"""W7.6. Matched-stake elicitation and endogenous teaching markets."""
from fractions import Fraction as F


def trustee_prices():
    delta = F(3,10)
    stakes = F(1,2), F(2)
    for direct, coverage in [(F(2,5),1), (0,F(3,5)), (F(1,10),F(4,5))]:
        v,w = stakes
        p,q = [delta*(direct + amount*(1-coverage)) for amount in stakes]
        intercept = (w*p-v*q)/(delta*(w-v))
        slope = (q-p)/(delta*(w-v))
        assert (intercept,slope)==(direct,1-coverage)
        print("Project stakes", *stakes, "prices", p,q, "identified direct",intercept)
    v,w = stakes
    price_uncertainty = F(1,100)
    belief_drift = F(1,20)
    radius = (v*w*belief_drift + (v+w)*price_uncertainty/delta)/(w-v)
    print("Price bands plus coverage drift: direct-value error at most",radius,float(radius))
    for n_escrow in range(5):
        n = 100
        price = delta*F(n,n*n_escrow+2*n+n_escrow+1)
        print("New project-only coaching records",n_escrow,"buys safety at .08",price>F(2,25))
    for scale in (F(1,5),F(1),F(5)):
        premium = delta*(100*scale**2)/(1+100*(1+scale**2))
        print("Presence-feature multiplier",scale,"premium on delivered model",float(premium))


def sorting(x):
    """Wardrop placement before local copying. Totals are population shares."""
    if x < F(1,5):
        a_safe, a_project = x, (1-5*x)/2
    elif x > F(2,3):
        a_safe, a_project = x-(3*x-2)/2, 0
    else:
        a_safe, a_project = x, 0
    b_safe, b_project = x-a_safe, 1-x-a_project
    a_tickets = 4*a_safe+a_project
    b_tickets = b_safe+2*b_project
    a_s, b_s = F(2)/a_tickets, F(1,2)/b_tickets
    a_p, b_p = F(1,2)/a_tickets, F(1)/b_tickets
    if a_safe:
        assert a_s>=b_s
    if b_safe:
        assert b_s>=a_s
    if a_project:
        assert a_p>=b_p
    if b_project:
        assert b_p>=a_p
    next_safe = a_safe*a_s + b_safe*b_s
    assert next_safe + a_project*a_p + b_project*b_p == 1
    if x < F(1,5):
        assert next_safe==4*x/(1+3*x) and next_safe>x
    elif x > F(2,3):
        assert next_safe==x/(2-x) and next_safe<x
    else:
        assert next_safe==F(1,2)
    return next_safe


def local_markets():
    for i in range(1,100):
        x = F(i,100)
        first = sorting(x)
        generations = 1
        x = first
        while x != F(1,2):
            x = sorting(x)
            generations += 1
            assert generations <= 10
        if i in (1,10,30,60,80,99):
            print("Initial S",F(i,100),"next",first,"generations to half",generations)


def scarce_trials():
    f,r = F(1,2),F(1,2)
    expected_draws = 1/f + 1/(1-f) - 1
    assert expected_draws == 3
    for grade in (0,1,3,7,15):
        p = f**grade
        direct = (1-r)*p / ((1-r)*p + r*(1-f)*p)
        # No actual edit before the next research slot.
        z = r/(r+(1-r)*p)
        no_edit = z*z*f*(1-f)*(1/(1-f*z)+1/(1-(1-f)*z))
        # First-step calculation in the three research states (neither,
        # pass only, fail only) before completing both observations.
        from_pass = z*(1-f)/(1-z*f)
        from_fail = z*f/(1-z*(1-f))
        assert no_edit == z*(f*from_pass+(1-f)*from_fail)
        assert 1-no_edit <= expected_draws*(1-r)/r*p
        print("Grade",grade,"edit before promotion: cold/restart",
              str(direct),round(float(1-no_edit),7))
    late_risk = expected_draws*(1-r)/r*f**7/(1-f)
    print("From grade seven: at least this probability of no future edit", 1-late_risk)


def costly_inspection():
    p,V,d,b,c = F(1,2),8,1,4,F(3,2)
    s,f,a,I = F(9,10),F(1,10),F(1,20),1
    def scout(g):
        return 0, g*s*(p*b-c)-(1-g)*f*c-a, p*b*g-c
    def founder(test, blind):
        old = p*V*(blind+f*test)
        changed = p*(V-d)*(blind+s*test)-I
        return old, changed
    for g,test,blind in [(F(1,3),F(4,11),0),(F(13,14),F(6,13),F(7,13))]:
        skip, audit, search = scout(g)
        assert audit==max(skip,audit,search)
        assert (audit==skip if blind==0 else audit==search)
        old, changed = founder(test,blind)
        assert old==changed
        print("Adopters / inspections / blind search",g,test,blind,"founder return",old)
    high = founder(F(6,13),F(7,13))[0]
    public_bond_break_even = p*V-c*d/b-high
    assert high==F(152,65) and public_bond_break_even==F(669,520)
    print("Public fractional commitment displaces high-adoption outcome below setup",
          public_bond_break_even)
    # A hidden fractional delegate with acceptance probability z is inspected
    # with pass probability f+(s-f)z, independently of its real action given z.
    # Its pre-implementation-cost payoff is concave; positive terminal slope
    # proves the largest gross return is attained at z=1.
    test, blind = F(6,13),F(7,13)
    derivative_at_one = p*(test*(s-f)*V-d*(blind+test*f)-2*test*(s-f)*d)
    assert derivative_at_one>0
    assert p*(blind+test*s)*(V-d)-F(13,10)<high


if __name__ == "__main__":
    trustee_prices()
    local_markets()
    scarce_trials()
    costly_inspection()
