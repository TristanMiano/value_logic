"""Independent finite probes of the P3-06 smoothing-schedule bit distinction.

Core arithmetic uses only this file and the Python standard library. Exact
outputs supplement the separate denominator proof; they are not asymptotic
evidence or a final evaluation. Contributor: ChatGPT (GPT-6 Astra Pro).
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json
import time
import traceback


def run():
    checks = 0

    def check(statement, message):
        nonlocal checks
        checks += 1
        if not statement:
            raise AssertionError(message)

    def squared_norm(xs):
        return sum((x*x for x in xs), F(0))

    def bits(x):
        return max(abs(x.numerator).bit_length(), x.denominator.bit_length())

    def dyadic(x):
        return x.denominator & (x.denominator-1) == 0

    reports = []
    for schedule in ('harmonic', 'dyadic'):
        residual = [F(0)] * 7
        variance = allowance = slack = F(0)
        own_mixture = F(0)
        other_mixture = [F(0), F(0)]
        max_depth = 0
        snapshots = []
        for t in range(1, 257):
            h = t.bit_length()  # ceil(log2(t+1)) for integer t >= 1.
            eta = F(1, t+1) if schedule == 'harmonic' else F(1, 2**h)
            check(F(1, 2*(t+1)) <= eta <= F(1, t+1), 'Width comparison.')

            def features(p):
                # c_0(y)=y, c_1(y)=1-y; d_0=1, d_1=-1.
                s = min(F(1), max(F(0), F(1, 2)-(1-2*p)/(2*eta)))
                return ( -p, 1-p,
                         max(F(0), 1-2*p), 1-abs(2*p-1), max(F(0), 2*p-1),
                         -2*s, 2*(1-s) ), s

            def score(p):
                phi, s = features(p)
                return (sum((r*f for r, f in zip(residual, phi)), F(0))
                        +(1-2*p)*squared_norm(phi)/2), phi, s

            maxima = (F(1), F(1), F(1), F(1), F(1), F(2), F(2))
            lips = (F(1), F(1), F(2), F(2), F(2), 2/eta, 2/eta)
            lip_score = sum((abs(r)*d+m*m+m*d
                             for r, m, d in zip(residual, maxima, lips)), F(0))
            tolerance = F(1, 64)
            budget = 0
            while lip_score / 2**(budget+1) > tolerance:
                budget += 1
            s0, phi0, a0 = score(F(0))
            steps = 0
            if s0 <= 0:
                p, value, phi, a = F(0), s0, phi0, a0
            else:
                s1, phi1, a1 = score(F(1))
                if s1 >= 0:
                    p, value, phi, a = F(1), s1, phi1, a1
                else:
                    low, high = F(0), F(1)
                    p = F(1, 2)
                    value, phi, a = score(p)
                    while abs(value) > tolerance and steps < budget:
                        if value > 0:
                            low = p
                        else:
                            high = p
                        p = (low+high)/2
                        value, phi, a = score(p)
                        steps += 1
                    check(abs(value) <= tolerance, 'Certified root tolerance.')
            added_allowance = 2*max(F(0), (1-p)*value, -p*value)
            check(added_allowance <= 2*tolerance, 'Uniform potential allowance.')
            y = int(p <= F(1, 2))
            residual = [r+(y-p)*f for r, f in zip(residual, phi)]
            variance += p*(1-p)*squared_norm(phi)
            allowance += added_allowance
            slack += eta/8
            own_mixture += (1-a)*y+a*(1-y)
            other_mixture[0] += y
            other_mixture[1] += 1-y
            core = (*residual, variance, allowance, own_mixture, *other_mixture)
            check(all(dyadic(z) for z in core), 'Core fixed/dyadic denominator invariant.')
            if schedule == 'dyadic':
                check(dyadic(slack), 'Dyadic accumulated smoothing slack.')
            check(squared_norm(residual) <= variance+allowance, 'Potential bound.')
            max_depth = max(max_depth, p.denominator.bit_length()-1)
            if t in (16, 64, 128, 256):
                snapshots.append({'rounds': t, 'eta': str(eta),
                                  'max_dyadic_forecast_exponent': max_depth,
                                  'numeric_core_max_bits': max(map(bits, core)),
                                  'slack_numerator_bits': abs(slack.numerator).bit_length(),
                                  'slack_denominator_bits': slack.denominator.bit_length(),
                                  'slack': str(slack)})
        reports.append({'schedule': schedule, 'snapshots': snapshots})

    # For unit weights, the reduced harmonic denominator contains every prime
    # above half its upper summation index (apart from any fixed scale factors).
    harmonic_witnesses = []
    for n in (16, 64, 128, 256, 512):
        harmonic = sum((F(1, j) for j in range(1, n+1)), F(0))
        primes = [p for p in range(n//2+1, n+1)
                  if all(p%d for d in range(2, isqrt(p)+1))]
        prime_product = 1
        for p in primes:
            prime_product *= p
        check(harmonic.denominator % prime_product == 0,
              'Upper-half primes survive harmonic reduction.')
        harmonic_witnesses.append({'n': n, 'harmonic_denominator_bits': harmonic.denominator.bit_length(),
                                   'upper_half_prime_product_bits': prime_product.bit_length()})
    return {'status': 'PASS', 'assertions': checks, 'schedule_comparison': reports,
            'harmonic_denominator_witnesses': harmonic_witnesses,
            'scope': 'Finite exact witness and numeric-kernel checks; proof in independent review.'}


if __name__ == '__main__':
    start_utc = datetime.now(timezone.utc).isoformat()
    start_ns = time.monotonic_ns()
    try:
        result = run()
    except Exception:
        result = {'status': 'FAIL', 'traceback': traceback.format_exc()}
    result.update(start_utc=start_utc, end_utc=datetime.now(timezone.utc).isoformat(),
                  execution_ns=time.monotonic_ns()-start_ns,
                  source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  principal_research_time_credit_ns=0, subagent_research_effort='unmeasured')
    target = Path(__file__).with_name('precision_schedule_probe_result.json')
    if target.exists():
        raise SystemExit('Refusing to overwrite prior probe evidence.')
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result.get(k) for k in ('status', 'assertions', 'execution_ns', 'source_sha256')}))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
