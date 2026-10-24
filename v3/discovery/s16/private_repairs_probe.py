"""Finite DEVELOPMENT screen of a privacy premise, not a general proof.
Codex (GPT-6), 2026-10-24. Field F7; A(x)=(x,x^2), rank bound2, degree2.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import time

t0 = time.perf_counter_ns()
q = 7
def A(x):
    return (x % q, x*x % q)
def member(v, basis):
    if not basis:
        return v == (0, 0)
    if len(basis) == 2:
        return True
    a, b = basis[0]
    return (a*v[1] - b*v[0]) % q == 0

outcomes = []
for secret in range(q):
    for public in range(1, q):
        # First proposed B=0, U=0 has false all-input scope.
        first_false_accept = member(A(secret), [])
        # Public point is an independent, uniformly selected nonzero point:
        # exactly the law of fresh uniform trials stopped at first A(x)!=0.
        U = [A(public)]
        second_error = ((secret-public) % q, 0)
        second_false_accept = member(second_error, U)
        # The second claimed scope is false: e1 is outside span A(public).
        assert not member((1, 0), U)
        # If rejected, an independently checked nonzero e1 residual completes R.
        assert member((1, 0), U + [(1, 0)])
        outcomes.append(first_false_accept or second_false_accept)
honest = Fraction(sum(outcomes), len(outcomes))
assert honest == Fraction(2, 7)

leaked = []
for secret in range(q):
    if member(A(secret), []):
        leaked.append(True)
        continue
    private_U = [A(secret)]
    # Revealing even just the subspace discloses secret via v2/v1.
    recovered = private_U[0][1] * pow(private_U[0][0], -1, q) % q
    assert recovered == secret
    assert not member((1, 0), private_U)
    leaked.append(member(((secret-recovered) % q, 0), private_U))
leaky = Fraction(sum(leaked), len(leaked))
bound = 2 * Fraction(2, 7)
assert honest <= bound < leaky == 1
result = {"status": "PASS", "public_outcomes": len(outcomes),
          "leaky_outcomes": len(leaked), "honest_false_accept": str(honest),
          "bound": str(bound), "leaky_false_accept": str(leaky),
          "elapsed_ns": time.perf_counter_ns() - t0,
          "python": platform.python_version(),
          "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
print(json.dumps(result))
