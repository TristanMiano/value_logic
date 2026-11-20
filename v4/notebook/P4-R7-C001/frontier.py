"""W7.5. A finite changing portfolio, procurement costs and conditional survival."""
from fractions import Fraction as F
from math import log, log1p, sqrt

import numpy as np


def challenger(index):
    """Van der Corput base two, rescaled to [1/4,3/4]."""
    value, weight = 0., .5
    while index:
        index, digit = divmod(index, 2)
        value += weight * digit
        weight *= .5
    return .25 + .5 * value


def expected_score(p, theta):
    return theta * log(p) + (1 - theta) * log1p(-p)


def contest(horizon=2048, delta=.05, seed=7506, fixed_batch=False):
    rng = np.random.default_rng(seed)
    theta = sqrt(.5)
    incumbent = .25
    accepted = downhill = jobs = 0
    for n in range(1, horizon + 1):
        rival = challenger(n)
        m = 16 if fixed_batch else n * n
        observations = rng.binomial(m, theta) / m
        jobs += m
        error = sqrt(log(2 * n * (n + 1) / delta) / (2 * m))
        logit_gap = log(rival / (1 - rival)) - log(incumbent / (1 - incumbent))
        expected = expected_score(rival, theta) - expected_score(incumbent, theta)
        observed = expected_score(rival, observations) - expected_score(incumbent, observations)
        assert abs((observed - expected) - (observations - theta) * logit_gap) < 1e-14
        # Rival-minus-incumbent prestige can have either sign and is observable.
        bound = 1 / (10 * n * n)
        bonus = bound if n % 2 else -bound
        if observed + bonus > abs(logit_gap) * error + bound:
            downhill += int(expected <= 0)
            if abs(observations - theta) <= error:
                assert expected > 0
            accepted += 1
            incumbent = rival
        if n in {16, 128, 512, horizon}:
            print("Fixed batch" if fixed_batch else "Growing batch",
                  n, jobs, accepted, downhill, round(incumbent, 8),
                  "loss to truth", round(expected_score(theta, theta) -
                                         expected_score(incumbent, theta), 9))


def archived_contest(horizon=32768, delta=.05, seed=7506):
    """Review on all independent work to date, storing only two counts."""
    rng = np.random.default_rng(seed)
    theta = sqrt(.5)
    successes, accepted = 0, 0
    incumbent = .25
    for n in range(1, horizon + 1):
        successes += int(rng.random() < theta)
        observed = successes / n
        error = sqrt(log(2 * n * (n + 1) / delta) / (2 * n))
        rival = challenger(n)
        advantage = expected_score(rival, observed) - expected_score(incumbent, observed)
        slope = abs(log(rival / (1 - rival)) - log(incumbent / (1 - incumbent)))
        if advantage > slope * error:
            incumbent = rival
            accepted += 1
        if n in {128, 2048, horizon}:
            print("Shared count", n, accepted, round(incumbent, 8), "sample mean",
                  round(observed, 8), "simultaneous lower bound", round(observed-error, 8))


def physical_scale():
    # Conditional laws on live paths are equal, including endpoint.
    K = ((F(3,5), F(2,5)), (F(1,10), F(3,5)))
    scale = F(9,10)
    x = [F(1), F(1)]
    for _ in range(10):
        x = [sum(k * z for k, z in zip(row, x)) for row in K]
    p, q = float(x[0]), float(scale**10 * x[0])
    threshold = .1
    assert q < threshold < p
    kl = p * log(p / q) + (1-p) * log((1-p) / (1-q))
    print("P(alive 10 | A,B)", list(map(float, x)), "scaled", q,
          "KL", kl, "critical fraction against .01 log subsidy", .01 / kl)


def procurement():
    anchor = F(1,4)
    critical = (anchor / (1-anchor)) ** 2
    for rho in (F(0), F(1,20), F(1,10), F(1,9)):
        first = next((m for m in range(1, 1000)
                      if rho + (1-rho)/m < critical), None)
        print("Planning load correlation", rho, "first strictly central batch", first)
        if first is not None:
            assert first > 1 and rho+(1-rho)/(first-1) >= critical


if __name__ == "__main__":
    contest()
    contest(fixed_batch=True)
    archived_contest()
    physical_scale()
    procurement()
