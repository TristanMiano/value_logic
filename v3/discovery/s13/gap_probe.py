"""Finite exact development screen for the two-value spectral-gap certificate.
Codex (GPT-6), 2026-10-21. First execution evidence is retained separately.
"""
from fractions import Fraction as F
from itertools import combinations
import hashlib, json, platform, time
from pathlib import Path

start = time.perf_counter_ns()
def h(r, z):
    return z / (r + (1-r)*z)

checks = 0
laws = 0
strict = 0
for points in combinations([F(k,10) for k in range(1,11)], 2):
    a, b = points
    for weight in (F(1,5), F(1,2), F(4,5)):
        laws += 1
        mu = weight*a + (1-weight)*b
        for s in (F(3,2), F(2), F(4)):
            delta = weight*h(s,a)+(1-weight)*h(s,b)-h(s,mu)
            assert delta > 0
            for r in (F(1,4), F(1,2), F(1), F(3,2), F(3), F(8)):
                actual = weight*h(r,a)+(1-weight)*h(r,b)
                pref = r*abs(r-1)*(s+(1-s)*mu)**2/(s*(s-1)*(r+(1-r)*mu)**2)
                ratios = [(s+(1-s)*z)/(r+(1-r)*z) for z in (a,b)]
                gap = abs(actual-h(r,mu))
                assert pref*min(ratios)*delta <= gap <= pref*max(ratios)*delta
                assert (actual-h(r,mu))*(r-1) >= 0
                checks += 1
                strict += pref*min(ratios)*delta < gap < pref*max(ratios)*delta

mu, s, nu, r = F(3,4), F(2), F(47,78), F(3)
delta = nu-h(s,mu)
lo, hi = F(1,2)+F(25,7020), F(1,2)+F(25,4680)
assert delta == F(1,390)
assert lo < F(113,224) < hi
old_lo = max(h(r,mu), h(r/s,nu))
old_hi = min(mu,nu)
assert old_lo == F(94,187) and old_hi == F(47,78)
assert hi-lo == F(25,14040) and hi-lo < old_hi-old_lo
zero_gap = 0
for mu in (F(1,10), F(1,2), F(9,10), F(1)):
    for r in (F(1,4), F(1), F(2), F(8)):
        assert h(r,mu) == mu/(r+(1-r)*mu)
        zero_gap += 1

result = dict(contributor="Codex (GPT-6)", status="PASS",
    scope="Finite exact development; no independent reconstruction or novelty claim",
    laws=laws, gap_checks=checks, strict_checks=strict,
    single_atom_checks=zero_gap,
    example=dict(lower=str(lo), upper=str(hi), actual=str(F(113,224)),
                 separate_lower=str(old_lo), separate_upper=str(old_hi)),
    elapsed_ns=time.perf_counter_ns()-start,
    python=platform.python_version(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
print(json.dumps(result, indent=2))
