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


def peer_receipt():
    """One decision on continuity; the pilot observed a different founder."""
    delta, cost = F(3, 10), F(7, 50)
    types = F(1, 5), F(4, 5)
    for h in (0, F(2, 5)):
        def purchase_value(mean):
            return max(0, delta * (h + 1 - mean) - cost)
        baseline = purchase_value(F(1, 2))
        for error in (0, F(1, 5), F(11, 27), F(1, 2)):
            after = 0
            means = []
            for label in (0, 1):
                weights = []
                for prob in types:
                    seen = prob * (1-error) + (1-prob)*error
                    weights.append((seen if label else 1-seen) / 2)
                mean = sum(w*t for w, t in zip(weights, types)) / sum(weights)
                means.append(mean)
                after += sum(weights) * purchase_value(mean)
            gain = after - baseline
            predicted = max(0, F(11, 500)-F(27, 500)*error) if h == 0 else 0
            assert gain == predicted
            print("Direct premium", h, "error", error,
                  "coverage on failure/success", *means, "one-record value", gain)


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


def transmission_of_premiums():
    """Term-valued safety, separate teaching payments, and copying errors."""
    step, delta, q, teaching = F(1, 10), F(3, 10), F(1, 2), F(4, 5)
    grid = [i*step for i in range(11)]
    for own in (F(0), F(1, 2), F(1)):
        target = own*teaching
        def private(h):
            return q*delta*(target*h-h*h/2)
        assert max(grid, key=private) == target
        for h in grid:
            assert private(target)-private(h) == q*delta*(h-target)**2/2
        scores = list(map(float, map(private, grid)))
        for mutation in (.001, .01):
            shares = [1.] + [0.]*10
            for _ in range(20_000):
                mean = sum(i/10*p for i,p in enumerate(shares))
                common = float(1 + teaching*F(3, 5)) + float((1-own)*teaching*q*delta)*mean
                seats = [p*(common+score) for p, score in zip(shares, scores)]
                total = sum(seats)
                following = [(1-mutation)*s for s in seats]
                for i, s in enumerate(seats):
                    following[max(0,i-1)] += mutation*s/2
                    following[min(10,i+1)] += mutation*s/2
                updated = [s/total for s in following]
                if max(abs(a-b) for a,b in zip(updated,shares)) < 1e-14:
                    shares = updated
                    break
                shares = updated
            print("Own teaching share", own, "target", target, "copy error", mutation,
                  "modal premium", shares.index(max(shares))/10,
                  "mean", round(sum(i/10*p for i,p in enumerate(shares)),5),
                  "target share", round(shares[grid.index(target)],5))


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


def moving_needs():
    # The sensing apparatus updates a stored ranking, which is then deployed.
    d, q, fee = F(1,50), F(9,10), F(1,10)
    a = F(3,8)
    correct = (d+a*(q-d))/(2*d+a*(1-2*d))
    before = d+(1-2*d)*correct
    assert correct == (1-a)*before+a*q
    assert d*(2*q-1) == fee*(2*d+a*(1-2*d))**2
    changed = a*(q*(1-before)+(1-q)*before)
    gross = correct-fee*a
    def periodic(gap):
        return F(1,2)+(q-F(1,2))*sum((1-2*d)**j for j in range(gap))/gap-fee/gap
    best = max(range(1,50),key=periodic)
    assert best == 4 and periodic(best)>gross
    print("Moving needs: installed ranking correctness, edit rate, net",
          correct,changed,gross,"better periodic gap/net", best,float(periodic(best)))


def grade_edit_risk(grade, f, wipe):
    """One work and one study per day. Solve U(s)=E[(1-f**grade)**T | s]."""
    z = 1-f**grade
    kept = z*(1-wipe)
    lost = z*wipe
    # Store constant and cold-start coefficient in each conditional U.
    def one_kind(seen_again):
        return (kept*(1-seen_again)/(1-kept*seen_again),
                lost/(1-kept*seen_again))
    passed, failed = one_kind(f), one_kind(1-f)
    ready = (kept*(f*passed[0]+(1-f)*failed[0]),
             lost+kept*(f*passed[1]+(1-f)*failed[1]))
    C, D = ready
    for _ in range(grade):
        C, D = kept*f*C/(1-kept*(1-f)), (lost+kept*f*D)/(1-kept*(1-f))
    cold = C/(1-D)
    return 1-(ready[0]+ready[1]*cold)


def erasures():
    f = F(1,2)
    for b in (F(0), F(1,5), F(1,3), F(2,5)):
        cross = (1-b)*f/(b+(1-b)*f)
        assert (cross>f) == (b<(1-f)/(2-f))
        risks = [grade_edit_risk(k,f,b) for k in (1,4,8,16,32)]
        assert all(0 < x < 1 for x in risks)
        if b == 0:
            for k, risk in zip((1,4,8,16,32), risks):
                z = 1-f**k
                no_edit = z**2*f*(1-f)*(1/(1-f*z)+1/(1-(1-f)*z))
                assert 1-risk == no_edit
        print("Study wipe", b, "prefix step before wipe", cross,
              "risk at grades 1/4/8/16/32", [round(float(x),7) for x in risks])


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


def repeated_search():
    p, value, help_cost, benefit, price = F(1,2), 8, 1, 4, F(3,2)
    conversion, binding, t = 1, F(13,10), F(2,5)
    gross_good = p*(value-help_cost)
    honest = gross_good/(1-t)
    changed = honest-conversion
    upper = p*value/(1-t)
    bond = (p*value-price*help_cost/benefit)/(1-t)-binding
    bounty_only = (p*value-price)/(1-t)
    # A clean, irreplaceable reputation can induce effort. If a founder
    # can certify a new end after breach, the continuation spread shrinks.
    assert t*honest > help_cost
    lower = max(0,changed,bond,bounty_only)
    assert t*(upper-lower) == F(11,15) < help_cost
    assert changed == F(29,6) and bond == F(569,120) and bounty_only == F(25,6)
    assert changed > max(bond,bounty_only)
    bond_threshold = conversion + (p*help_cost-price*help_cost/benefit)/(1-t)
    assert bond_threshold == F(29,24)
    print("Repeated search: old end with reputation, adoption, bond, bounty",
          honest, changed, bond, bounty_only, "max reputation stake after re-entry", t*(upper-lower))
    # If a scout can buy verified delivery, both agents can have strict
    # incentives under the old preference, even in an isolated encounter.
    eps = F(1,100)
    payment_for_help, discovery_bounty = help_cost+eps, 2*eps
    scout = p*(benefit-payment_for_help+discovery_bounty)-price
    old = p*(value+payment_for_help-help_cost-discovery_bounty)/(1-t)
    assert scout>0 and payment_for_help>help_cost and old>changed
    print("Two-way payments: scout per date",scout,"old founder lifetime",old)


if __name__ == "__main__":
    trustee_prices()
    peer_receipt()
    local_markets()
    transmission_of_premiums()
    scarce_trials()
    erasures()
    moving_needs()
    costly_inspection()
    repeated_search()
