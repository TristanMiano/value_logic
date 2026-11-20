"""Physical calibration of changing binary dictionaries, with priced sequential audits."""
from fractions import Fraction as F
from itertools import count
from math import ceil, comb, exp, log, log1p


def audit(k, accuracy):
    odds = accuracy / (1 - accuracy)
    error = 1 / (1 + odds**k)
    expected_checks = k * (1 - 2 * error) / (2 * accuracy - 1)
    return error, expected_checks


def next_threshold(k, accuracy, fee):
    odds = accuracy / (1 - accuracy)
    return fee * (1 + 2*k + (odds**(k+1) - odds**(-k))/(odds-1)) / (2*accuracy-1)


def best(stake, accuracy, fee):
    k = 0
    while stake > next_threshold(k, accuracy, fee):
        k += 1
    return k


def bellman_check(stake, accuracy, fee):
    """Solve the chosen policy and test both alternatives at every relevant belief."""
    k = best(stake, accuracy, fee)
    odds = accuracy / (1-accuracy)

    def mistake(n):
        return 1 / (1 + odds**abs(n))

    def up(n):
        posterior = odds**n / (1 + odds**n)
        return posterior * accuracy + (1-posterior) * (1-accuracy)

    # Express the interior values as affine functions of V(-k+1).
    value = {}
    if k:
        coeff = {-k: (0, stake*mistake(k)), -k+1: (1, 0)}
        for n in range(-k+1, k):
            a, b = coeff[n]
            left_a, left_b = coeff[n-1]
            p = up(n)
            coeff[n+1] = ((a-(1-p)*left_a)/p, (b-fee-(1-p)*left_b)/p)
        a, b = coeff[k]
        first = (stake*mistake(k)-b)/a
        value = {n: a*first+b for n, (a,b) in coeff.items()}

    def optimal(n):
        return value.get(n, stake*mistake(n))

    n_max = k+1
    while stake*mistake(n_max) > fee:
        n_max += 1
    for n in range(-n_max, n_max+1):
        keep = fee + up(n)*optimal(n+1) + (1-up(n))*optimal(n-1)
        assert optimal(n) == min(stake*mistake(n), keep)
    error, draws = audit(k, accuracy)
    assert optimal(0) == stake*error + fee*draws


def lineage():
    # A mistranslation ends this particular carrier. Pools used to fund
    # calibration are charged, but assumed to cover each attempted test.
    accuracy, fee, delta = F(3,4), 1, .05
    odds = float(accuracy/(1-accuracy))
    local_survival = protected_survival = 0.
    local_loss = protected_loss = 0.
    for n in range(1,4097):
        log_left, log_right = log(n+1), log(n+2)
        weight = log(2)*log1p(1/(n+1))/(log_left*log_right)
        k_local = best(n,accuracy,fee)
        k_protected = ceil(log((1-delta*weight)/(delta*weight))/log(odds))
        e_local, d_local = audit(k_local,accuracy)
        e_safe, d_safe = audit(k_protected,accuracy)
        assert float(e_safe) <= delta*weight
        local_survival += log1p(-float(e_local))
        protected_survival += log1p(-float(e_safe))
        local_loss += float(n*e_local+d_local)
        protected_loss += float(n*e_safe+d_safe)
        if n in (16,256,4096):
            print("Cohorts, all correct under local and protected audits, extra loss per job",
                  n,exp(local_survival),exp(protected_survival),
                  (protected_loss-local_loss)/(n*(n+1)/2))


def prepaid_chain():
    # On a correct installation cohort n earns n only after paying for
    # every test. Its successor inherits the actual remaining reserves.
    tails = {}
    receipts, required, worst = 0, 0, 0
    schedule = []
    for n in range(1,514):
        for checks in count(1,2):
            if checks not in tails:
                tails[checks] = F(sum(comb(checks,j)*3**j for j in range(checks//2+1)),
                                  4**checks)
            if tails[checks] <= F(1,20*n*(n+1)):
                break
        schedule.append(checks)
        if checks-receipts > required:
            required, worst = checks-receipts, n
        receipts += n-checks
        if n in (1,16,64,513):
            print("Prepaid cohort, checks before work, accumulated net on success",n,checks,receipts)
    # Beyond this point n's output covers the entire next cohort.
    # Both the bound and its log derivative dominate the required risk.
    assert exp(-(512-1)/8) < 1/(20*513*514)
    assert 1/8 > 1/513+1/514
    print("Required founding reserve for this paid schedule, tight at cohort",required,worst)
    for floor in range(1,64,2):
        counts = [max(floor,min(k,(n//2)*2-1)) for n,k in enumerate(schedule,1)]
        # After the enumerated prefix the prior cohort can fund the
        # risk-allocated rule. Its remaining union bound telescopes.
        risk = sum(tails[k] for k in counts) + F(1,20*(len(counts)+1))
        if risk <= F(1,20):
            receipts = budget = 0
            for n,k in enumerate(counts,1):
                budget = max(budget,k-receipts)
                receipts += n-k
            assert budget == floor*(floor+1)//2
            print("Feasible cheaper founding reserve, initial tests, error upper bound",
                  budget,floor,float(risk))
            break


def main():
    prepaid_chain()
    lineage()
    for accuracy in (F(3,5), F(3,4), F(4,5)):
        for fee in (F(1,2), F(1), F(7,3)):
            for k in range(7):
                boundary = next_threshold(k, accuracy, fee)
                for offset in (F(-1,100), F(0), F(1,100)):
                    bellman_check(boundary+offset, accuracy, fee)
    r = F(3,4)
    for stake in (8, 88, 100, 10000):
        k = best(stake, r, 1)
        error, draws = audit(k, r)
        print("Stake, stopping margin, error, mean checks, expected loss",
              stake, k, error, draws, stake*error+draws)
    workers = 11
    local_stake = 8
    error, draws = audit(best(local_stake, r, 1), r)
    vote_error = sum(comb(workers,j)*error**j*(1-error)**(workers-j)
                     for j in range(workers//2+1, workers+1))
    pooled_stake = workers*local_stake
    centralized_error, centralized_draws = audit(best(pooled_stake, r, 1), r)
    separate = workers*(draws+local_stake*error)
    voting = workers*draws + pooled_stake*vote_error
    shared = centralized_draws + pooled_stake*centralized_error
    assert separate == 33 and shared == F(61,7) and shared < voting < separate
    print("Independent, common majority, sequential common losses", separate, float(voting), shared)
    print("Majority error",vote_error,"single common audit error",centralized_error)
    print("Probability a ten-link dictionary chain is right",(1+(2*r-1)**10)/2)


if __name__ == "__main__":
    main()
