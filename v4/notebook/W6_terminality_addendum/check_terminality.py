"""Exact finite examples in R6.17. Run with Python 3.10+ (standard library)."""

from fractions import Fraction as F


def dot(row, column):
    return sum(x * y for x, y in zip(row, column, strict=True))


def advance(row, kernel):
    """Unnormalized live-state masses after one further baseline step."""
    return tuple(dot(row, column) for column in zip(*kernel, strict=True))


def apply(kernel, column):
    return tuple(dot(row, column) for row in kernel)


def scaled_kernel(baseline, weight):
    return tuple(tuple(w * p for p in row) for w, row in zip(weight, baseline, strict=True))


def envelope():
    # Choosing A or B as the next state cancels the current survival chance.
    k = ((F(3, 5), F(2, 5)), (F(1, 10), F(3, 5)))
    a, b = (1, 0), (0, 1)
    for m in range(1, 33):
        a, b = advance(a, k), advance(b, k)
        ratios = [x / y for x, y in zip(a, b, strict=True)]
        scale = 2**m
        assert min(ratios) == F(2*(scale-1), scale+1)
        assert max(ratios) == F(2*(scale+1), scale-1)
        # The terminal assessment accepts only the second state in the worst case.
        assert ratios[1] == min(ratios)
        for end in ((1, 1), (9, 1), (1, 9)):
            assert min(ratios) <= dot(a, end) / dot(b, end) <= max(ratios)
    print("Endpoint-robust odds at m=1,2 and infinity: 2/3, 6/5, 2")


def exit_and_continuing_work():
    k = ((F(3, 5), F(2, 5)), (F(1, 10), F(3, 5)))
    a, b = (1, 0), (0, 1)
    work = (F(17, 3), F(19, 6))
    assert apply(k, tuple(1 + v for v in work)) == work
    assert work[0] - work[1] == F(5, 2)
    truncated = [0, 0]
    for m in range(41):
        signed = (-1, 1)
        advantage = dot(a, signed) - dot(b, signed)
        assert advantage == (F(4, 5)**m - 9*F(2, 5)**m)/4
        assert (advantage > 0) == (m >= 4)
        # Every fixed end in this family eventually favors A, but at each m
        # there is still an end with positive limiting average that favors B.
        near_zero = (-1, F(1, 2) + F(1, 2)**m)
        assert dot((1, 2), near_zero) > 0
        assert dot(a, near_zero) < dot(b, near_zero)
        if m:
            truncated[0] += sum(a)
            truncated[1] += sum(b)
        a, b = advance(a, k), advance(b, k)
    assert abs(truncated[0] - truncated[1] - F(5, 2)) < F(1, 1000)
    print("Signed end buys A at m >= 4; expected further work gained by A = 5/2")

def exact_ends():
    # C survives with probability 3/5, then chooses a lottery over A, B, C.
    # Equal baseline mixing over the two offers produces the C row of P.
    p = ((F(3, 5), F(1, 5), F(1, 5)), (F(1, 5), F(3, 5), F(1, 5)),
         (F(1, 4), F(1, 4), F(1, 2)))
    k = scaled_kernel(p, (1, 1, F(3, 5)))
    left = (F(9, 40), F(3, 40), F(3, 10))
    right = (F(3, 40), F(9, 40), F(3, 10))
    h = (2, 2, 1)
    assert tuple((x+y)/2 for x, y in zip(left, right)) == k[2]
    assert apply(k, h) == tuple(F(9, 10)*x for x in h)
    assert dot(left, h) == dot(right, h)
    for m in range(33):
        advantage = F(3, 20) * F(2, 5)**m
        assert left[0]-right[0] == advantage
        assert left[1]-right[1] == -advantage
        assert sum(left) == sum(right)
        left, right = advance(left, k), advance(right, k)
    print("Opposite exact choices for goals A and B, equal survival, m=0..32")


def maxima():
    p = ((F(8, 10), F(1, 10), F(1, 10)),
         (F(1, 10), F(1, 10), F(8, 10)),
         (F(1, 10), F(1, 10), F(8, 10)))
    s = (F(5, 9), 1, F(1, 3))
    h = (4, 3, 1)
    k = scaled_kernel(p, s)
    assert apply(k, h) == tuple(F(1, 2)*x for x in h)
    assert s.index(max(s)) == 1 and h.index(max(h)) == 0
    # Equal baseline rows are a repair for the same three survival probabilities.
    equal = ((F(1, 3),)*3,)*3
    assert apply(scaled_kernel(equal, s), s) == tuple(sum(s)*x/3 for x in s)
    print("Maximum baseline survival value at A, best unrestricted destination B")


def infer_relative_weight(p, q, origin):
    """Reconstruct h and w from one positive row of Q and the whole known P."""
    score = tuple(x/y for x, y in zip(q[origin], p[origin], strict=True))
    h = tuple(v/score[0] for v in score)
    weight = tuple(v/d for v, d in zip(h, apply(p, h), strict=True))
    return tuple(w/weight[0] for w in weight)


def two_exposures():
    # Keep P and the running incentive fixed while a move requires one or
    # two independent passes of the same state-specific survival test.
    p = ((F(3, 5), F(2, 5)), (F(1, 7), F(6, 7)))
    survival = (F(3, 4), F(11, 18))
    incentive = (F(4, 3), F(63, 55))
    inferred = []
    for exposure, h, growth in ((1, (2, 1), F(4, 5)), (2, (3, 1), F(11, 20))):
        w = tuple(s**exposure * e for s, e in zip(survival, incentive))
        k = scaled_kernel(p, w)
        assert apply(k, h) == tuple(growth*x for x in h)
        # Construct Q from the live path weights. The inverse receives no w or h.
        q = tuple(tuple(k[i][j]*h[j]/(growth*h[i]) for j in range(2)) for i in range(2))
        assert all(sum(row) == 1 for row in q)
        ratios = [infer_relative_weight(p, q, origin) for origin in range(2)]
        assert ratios[0] == ratios[1] == tuple(x/w[0] for x in w)
        inferred.append(ratios[0][1])
    environmental = inferred[1]/inferred[0]
    internal = inferred[0]/environmental
    assert environmental == survival[1]/survival[0] == F(22, 27)
    assert internal == incentive[1]/incentive[0] == F(189, 220)
    print("From two positive exposures: survival B/A=22/27, incentive B/A=189/220")


def separable_end():
    # Check all four joint rows against the isolated Y controller's choices.
    x = ((F(3, 5), F(2, 5)), (F(1, 10), F(3, 5)))
    p_y = ((F(1, 2), F(1, 2)), (F(3, 4), F(1, 4)))
    y = scaled_kernel(p_y, (F(1, 2), 2))
    hx, hy = (2, 1), (1, 3)
    states = [(i, j) for i in range(2) for j in range(2)]
    h = [hx[i]*hy[j] for i, j in states]
    for i, j in states:
        joint = [x[i][a]*y[j][b] for a, b in states]
        growth = dot(joint, h)
        assert growth == F(4, 5)*hx[i]*hy[j]
        retained = [weight*value/growth for weight, value in zip(joint, h)]
        for dest in range(2):
            marginal = sum(v for v, (_, b) in zip(retained, states) if b == dest)
            assert marginal == y[j][dest]*hy[dest]/hy[j]
            assert marginal != p_y[j][dest]

def permanent_support():
    # A forward, finite-time computation. No eigenvalue routine, root finder,
    # or draws from the claimed ancestral transition law are used.
    switch = F(1, 50)
    advantage = 2
    matrix = scaled_kernel(((1-switch, switch), (switch, 1-switch)), (1, advantage))
    lo, hi = (1, 0), (0, 1)
    thresholds = {}
    for m in range(1, 81):
        lo, hi = advance(lo, matrix), advance(hi, matrix)
        guaranteed = min(x/y for x, y in zip(hi, lo))
        for cost in (F(1), F(6, 5), F(2), F(49)):
            if guaranteed > cost:
                thresholds.setdefault(cost, m)
    assert thresholds == {F(1): 5, F(6, 5): 5, F(2): 6, F(49): 21}
    population_priority = hi[1]/sum(hi)
    future_mass = (sum(lo), sum(hi))
    h_ratio = future_mass[1]/future_mass[0]
    q = tuple(tuple(row[j]*future_mass[j]/dot(row, future_mass) for j in range(2))
              for row in matrix)
    assert round(float(population_priority), 6) == 0.960816
    assert round(float(h_ratio), 4) == 49.0408
    assert round(float(100*q[1][0]), 4) == 0.0416
    assert round(1/q[1][0]) == 2404
    assert abs(q[1][1]/q[0][0] - advantage) < F(1, 10**20)
    assert q[0][1]*q[1][0]/(q[0][0]*q[1][1]) == (switch/(1-switch))**2
    # Calibrate a family of exact strict/tie prices H with mu fixed. For each
    # H the value equation must agree, and both pure endpoints straddle H.
    for ratio in (F(6, 5), F(2), F(3), F(49)):
        r = (1-switch+switch*ratio)/(1-switch+switch/ratio)
        test_matrix = scaled_kernel(((1-switch, switch), (switch, 1-switch)), (1, r))
        h = (1, ratio)
        growth, second = apply(test_matrix, h)
        assert second == growth*ratio
        first, second = (1, 0), (0, 1)
        for m in range(10):
            first, second = advance(first, test_matrix), advance(second, test_matrix)
            assert second[0]/first[0] < ratio < second[1]/first[1]
    print("Permanent support: share 96.08%, ancestral loss 0.0416%, mean run 2404")
    print("Five subsequent steps suffice for a 6/5 price, six for a twofold price")


def rates_without_zero():
    # For k >= 2, rate = 2^-k, initial mass = 2^(1-k), always type 0.
    # Dividing the whole population by 2 each generation gives a live kernel.
    # The omitted mass stays <= its original mass at every horizon.
    last_rate_index = 42
    times = (8, 32, 128, 512)
    snapshots = {t: [F(0), F(0), F(0)] for t in times}
    for k in range(2, last_rate_index+1):
        denominator = 1 << k
        absent, present = 1, 0
        for t in range(1, max(times)+1):
            absent, present = ((denominator-1)*absent + 2*present,
                               absent + 2*(denominator-1)*present)
            if t in snapshots:
                scale = 1 << (k-1 + (k+1)*t)
                mass = F(absent + present, scale)
                snapshots[t][0] += mass
                snapshots[t][1] += F(present, scale)
                # Weight parents by their number of outgoing transmissions.
                snapshots[t][2] += F(absent + 2*present, scale*denominator)
    tail_bound = F(1, 1 << (last_rate_index-1))
    for t, (mass, with_priority, rate_sum) in snapshots.items():
        def bounds(observed, total, omitted):
            return observed/(total+omitted), (observed+omitted)/(total+omitted)
        q_low, q_high = bounds(with_priority, mass, tail_bound)
        rate_low, rate_high = bounds(rate_sum, mass+with_priority, 2*tail_bound)
        assert q_high-q_low < F(1, 10**6)
        assert rate_high-rate_low < F(1, 10**6)
        print(f"No zero-rate programs, t={t}: share ~{float((q_low+q_high)/2):.7f}, "
              f"next-transmission flip probability ~{float((rate_low+rate_high)/2):.7f} "
              "(exact interval widths below 1e-6)")

def changing_revision():
    # Same permanent twofold advantage in both worlds. Compute population
    # shares from descendant masses and the probability of no physical flips
    # on a single unselected forward line independently.
    for summable in (True, False):
        masses = (F(1, 2), F(1, 2))
        unbroken = F(1)
        for t in range(100):
            rate = F(1, (t+2)**2) if summable else F(1, t+3)
            k = scaled_kernel(((1-rate, rate), (rate, 1-rate)), (1, 2))
            masses = advance(masses, k)
            unbroken *= 1-rate
            m = t+1
            expected = F(m+2, 2*(m+1)) if summable else F(2, m+2)
            assert unbroken == expected
        share = masses[1]/sum(masses)
        print(f"At generation 100: priority share {float(share):.6f}, "
              f"no forward switch yet {float(unbroken):.6f}")


def unseen_transmission():
    # Two different physical advantages give identical observations of both
    # ancestral rows once an asymmetric physical transmission rule is allowed.
    for up, down, advantage, ratio in ((F(1, 7), F(2, 5), F(10, 7), 2),
                                       (F(1, 10), F(1, 2), F(9, 5), 3)):
        k = scaled_kernel(((1-up, up), (down, 1-down)), (1, advantage))
        h = (1, ratio)
        growth, second = apply(k, h)
        assert second == ratio*growth
        q = tuple(tuple(row[j]*h[j]/dot(row, h) for j in range(2)) for row in k)
        assert q == ((F(3, 4), F(1, 4)), (F(1, 4), F(3, 4)))

def survived(destination, steps, rng):
    """Physical trial with the declared baseline continuation. Death ends a trial."""
    state = destination
    for _ in range(steps):
        if state == "A":
            state = "A" if rng.randrange(5) < 3 else "B"
        else:
            if rng.randrange(10) >= 7:
                return False
            state = "A" if rng.randrange(7) == 0 else "B"
    return True


def learn_scores(rng, trials, steps):
    # Only a destination and a binary survival label enter the estimate.
    return {state: F(1 + sum(survived(state, steps, rng) for _ in range(trials)), trials + 2)
            for state in ("A", "B")}


def choose(scores, cost):
    return "A" if scores["A"]/cost > scores["B"] else "B"


def binomial_masses(trials, p):
    """Binomial masses scaled first at the mode to avoid tail underflow there."""
    from math import fsum

    mode = int((trials + 1)*p)
    masses = [0.0]*(trials + 1)
    masses[mode] = 1.0
    for k in range(mode, 0, -1):
        masses[k-1] = masses[k]*k/(trials-k+1)*(1-p)/p
    for k in range(mode, trials):
        masses[k+1] = masses[k]*(trials-k)/(k+1)*p/(1-p)
    total = fsum(masses)
    return [mass/total for mass in masses]


def training_choice_probability(mass_a, mass_b, price):
    """Independent binomial success counts with the deployed smoothing/tie rule."""
    from itertools import accumulate
    from math import fsum

    cdf_b = list(accumulate(mass_b))
    contributions = []
    for successes_a, probability in enumerate(mass_a):
        top = ((successes_a + 1)*price.denominator - 1)//price.numerator - 1
        if top >= 0:
            contributions.append(probability*cdf_b[min(top, len(cdf_b)-1)])
    return fsum(contributions)

def audit_choice_bounds():
    # Sharp direct-premium bound for two Bernoulli consequences in [0,1].
    expected_a, expected_b = F(51, 100), F(49, 100)
    fee, tolerance = F(1, 10), F(1, 100)
    premium = fee - tolerance - abs(expected_a-expected_b)
    assert premium == F(7, 100)
    assert expected_a + premium - fee == expected_b-tolerance
    # With misspecified forecasts the same fee can be paid with no premium.
    assert F(3, 5) - fee > expected_b

    # Cross-check the strict inequality and smoothing in the count-based
    # calculation against full enumeration under both tie and non-tie prices.
    from math import comb, isclose
    n = 8
    exact_a = [comb(n, k)*F(1, 2)**n for k in range(n+1)]
    exact_b = [comb(n, k)*F(1, 3)**k*F(2, 3)**(n-k) for k in range(n+1)]
    for price in (F(1), F(3, 2), F(2), F(5, 2)):
        exact = sum(x*y for a, x in enumerate(exact_a) for b, y in enumerate(exact_b)
                    if choose({"A": a+1, "B": b+1}, price) == "A")
        computed = training_choice_probability(binomial_masses(n, 0.5),
                                               binomial_masses(n, 1/3), price)
        assert isclose(float(exact), computed, abs_tol=1e-14)

def deployment():
    import random
    from statistics import mean

    steps, trials = 10, 4096
    prices = (F(3, 2), F(2), F(5, 2))
    scores = [learn_scores(random.Random(seed), trials, steps) for seed in range(17001, 17017)]
    k = ((F(3, 5), F(2, 5)), (F(1, 10), F(3, 5)))
    endpoints = {"A": (1, 0), "B": (0, 1)}
    for step in range(steps):
        endpoints = {action: advance(row, k) for action, row in endpoints.items()}
    # The following population probabilities are a post-deployment check. At
    # each destination the count of success flags is binomial under iid trials.
    mass_a, mass_b = (binomial_masses(trials, float(sum(row))) for row in endpoints.values())
    counts = []
    print("Deployment: price, times A / 16, mean regrets A and B, iid probability of A")
    for price in prices:
        choices = [choose(score, price) for score in scores]
        regret = []
        for j in (0, 1):
            payoff = {"A": endpoints["A"][j]/price, "B": endpoints["B"][j]}
            regret.append(mean(max(payoff.values())-payoff[action] for action in choices))
        probability = training_choice_probability(mass_a, mass_b, price)
        counts.append(choices.count("A"))
        print(price, counts[-1], *(f"{float(loss):.9f}" for loss in regret), f"{probability:.9f}")
        assert all(loss >= 0 for loss in regret)
        if price != 2:
            assert regret == [0, 0]
    assert counts == [16, 9, 0]
    equalized = [{"A": score["B"], "B": score["B"]} for score in scores]
    equalized_a = sum(choose(score, prices[0]) == "A" for score in equalized)
    assert equalized_a == 0
    print("At price 3/2 with equalized scores, A chosen:", equalized_a)


if __name__ == "__main__":
    envelope()
    exit_and_continuing_work()
    exact_ends()
    maxima()
    two_exposures()
    separable_end()
    permanent_support()
    rates_without_zero()
    changing_revision()
    unseen_transmission()
    audit_choice_bounds()
    deployment()
