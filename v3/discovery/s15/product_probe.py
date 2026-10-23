"""DEVELOPMENT: exact rank-stop law and small, fully acquired F2 products.

Counts describe these Python algorithms, not hardware instructions or optimal
linear algebra. Input generation and truth validation are timed separately.
No output overwrite; all cases and negative controls are retained.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
import platform
from pathlib import Path
import random
import sys
from time import perf_counter_ns

ROOT = Path(__file__).resolve().parent


class Cost:
    def __init__(self):
        self.c = Counter()

    def xor(self, a, b, width):
        self.c["xor_calls"] += 1
        self.c["xor_bits"] += width
        return a ^ b

    def dot(self, a, b, width):
        self.c["dot_calls"] += 1
        self.c["dot_bits"] += width
        return (a & b).bit_count() & 1

    def scan(self, bits):
        self.c["bit_inspections"] += bits

    def totals(self):
        return dict(sorted(self.c.items()))


def insert(x, basis, width, cost):
    """Echelon basis of a span, represented by pivot-to-vector dict."""
    while x:
        j = x.bit_length() - 1
        cost.c["basis_lookups"] += 1
        if j not in basis:
            basis[j] = x
            return True
        x = cost.xor(x, basis[j], width)
    return False


def columns(rows, width, cost):
    out = []
    for j in range(width):
        v = 0
        for i, row in enumerate(rows):
            cost.scan(1)
            v |= ((row >> j) & 1) << i
        out.append(v)
    return out


def matvec(rows, x, width, cost):
    return sum(cost.dot(row, x, width) << i for i, row in enumerate(rows))


def row_product(p, q, m, n, cost):
    result = []
    for row in p:
        v = 0
        for i in range(m):
            cost.scan(1)
            if (row >> i) & 1:
                v = cost.xor(v, q[i], n)
        result.append(v)
    return result


def full_range(p, q, m, n, cost):
    z = row_product(p, q, m, n, cost)
    basis = {}
    for v in columns(z, n, cost):
        insert(v, basis, len(p), cost)
    return basis, {"product_rows": len(z)}


def q_factor_range(p, q, m, n, cost):
    qb, zb = {}, {}
    for v in columns(q, n, cost):
        if insert(v, qb, m, cost):
            insert(matvec(p, v, m, cost), zb, len(p), cost)
    return zb, {"q_rank": len(qb)}


def p_factor_range(p, q, m, n, cost):
    # P = U R, where the rows of R are insertion residuals. Coefficients
    # are formed during the same elimination; no free factorization.
    pivots, residuals, u = {}, [], []
    for row in p:
        v, coeff = row, 0
        while v:
            j = v.bit_length() - 1
            cost.c["basis_lookups"] += 1
            if j not in pivots:
                idx = len(residuals)
                pivots[j] = idx
                residuals.append(v)
                coeff = cost.xor(coeff, 1 << idx, m)
                break
            idx = pivots[j]
            v = cost.xor(v, residuals[idx], m)
            coeff = cost.xor(coeff, 1 << idx, m)
        u.append(coeff)
    vrows = row_product(residuals, q, m, n, cost)
    vb, zb = {}, {}
    for v in columns(vrows, n, cost):
        if insert(v, vb, len(residuals), cost):
            insert(matvec(u, v, len(residuals), cost), zb, len(p), cost)
    return zb, {"p_rank": len(residuals)}


def random_range(p, q, m, n, cost, seed, h=11):
    rng, basis, t = random.Random(seed), {}, 0
    while t - len(basis) < h:
        a = rng.getrandbits(n)
        cost.c["random_bits"] += n
        middle = matvec(q, a, n, cost)
        result = matvec(p, middle, m, cost)
        insert(result, basis, len(p), cost)
        t += 1
    return basis, {"probes": t, "redundancies": t - len(basis), "h": h}


def canonical(basis, width):
    # Validation only; independent, deterministic full reduction.
    b = dict(basis)
    for low in sorted(b):
        for high in sorted(b):
            if high > low and ((b[high] >> low) & 1):
                b[high] ^= b[low]
    return [b[k] for k in sorted(b)]


def rank(rows, width):
    b = {}
    c = Cost()
    for v in rows:
        insert(v, b, width, c)
    return len(b)


def inputs(r, m, n, d, seed):
    rng = random.Random(seed)
    k = m // 2
    if d == "generic":
        return ([rng.getrandbits(m) for _ in range(r)],
                [rng.getrandbits(n) for _ in range(m)])
    # Product rank <= d, while both factors have substantially larger rank.
    # P and the mixing sequence are fixed before iid Q columns are sampled.
    p = [rng.getrandbits(k) for _ in range(r)]
    q = [rng.getrandbits(n) if i < d or i >= k else 0 for i in range(m)]
    # Elementary transformations preserve P Q. P <- P S, Q <- S^-1 Q.
    # Row vectors: col j of P ^= col i; corresponding row i of Q ^= row j.
    mixing = random.Random(seed + 100000)
    for _ in range(8 * m):
        i, j = mixing.sample(range(m), 2)
        p = [row ^ ((((row >> i) & 1)) << j) for row in p]
        q[i] ^= q[j]
    return p, q


def exact_stop(d, h):
    # Markov dynamic program over actual rank and accumulated redundancies.
    states = {(0, 0): Fraction(1)}
    ended = defaultdict(Fraction)
    for _ in range(d + h):
        nxt = defaultdict(Fraction)
        for (j, f), mass in states.items():
            pr = Fraction(1, 1 << (d - j))
            if f + 1 == h:
                ended[j] += mass * pr
            else:
                nxt[j, f + 1] += mass * pr
            if j < d:
                nxt[j + 1, f] += mass * (1 - pr)
        states = nxt
    assert not any(states.values())
    assert sum(ended.values()) == 1
    bad = sum(v for j, v in ended.items() if j < d)
    good_formula = Fraction(1)
    for ell in range(h, d + h):
        good_formula *= 1 - Fraction(1, 1 << ell)
    assert bad == 1 - good_formula
    assert bad < Fraction(2, 1 << h)
    return bad


def main():
    output = ROOT / "product_probe.json"
    if output.exists():
        raise RuntimeError("Refusing to overwrite an exposed development run")
    start = perf_counter_ns()
    law = []
    for d in range(13):
        for h in range(1, 11):
            p = exact_stop(d, h)
            law.append({"d": d, "h": h, "false": str(p)})
    cases = []
    for r, m, n in [(128, 64, 96), (256, 96, 192), (512, 128, 384)]:
        for d in [1, 4, "generic"]:
            seed = 151000 + r + (0 if d == "generic" else d)
            started = perf_counter_ns()
            p, q = inputs(r, m, n, d, seed)
            prep_ns = perf_counter_ns() - started
            records, bases = [], []
            for name, method in [("full_row_xor", full_range),
                                 ("q_column_factor", q_factor_range),
                                 ("p_row_factor", p_factor_range),
                                 ("random_total_redundancy", random_range)]:
                c = Cost()
                began = perf_counter_ns()
                if name.startswith("random"):
                    basis, meta = method(p, q, m, n, c, seed + 17)
                else:
                    basis, meta = method(p, q, m, n, c)
                elapsed = perf_counter_ns() - began
                bases.append(canonical(basis, r))
                records.append({"method": name, "rank": len(basis),
                                "elapsed_ns_single_run": elapsed,
                                "cost": c.totals(), **meta})
            assert bases[0] == bases[1] == bases[2]
            # Record a randomized miss, rather than erase or rerun it.
            for rec, base in zip(records, bases):
                rec["correct_range"] = base == bases[0]
            dr = len(bases[0])
            assert records[-1]["probes"] <= dr + 11
            cases.append({"r": r, "m": m, "n": n,
                          "construction": d, "seed": seed,
                          "common_input_bits": r * m + m * n,
                          "input_generation_ns": prep_ns,
                          "input_sha256": hashlib.sha256(json.dumps([p,q]).encode()).hexdigest(),
                          "p_rank": rank(p, m), "q_rank": rank(q, n),
                          "true_product_rank": dr, "methods": records})
    result = {"status": "PASS", "label": "DEVELOPMENT",
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python": sys.version, "platform": platform.platform(),
              "elapsed_ns_including_generation_validation": perf_counter_ns()-start,
              "notes": ["No proof of novelty or optimal speed.",
                        "Single-run times are diagnostics, not CPU performance claims.",
                        "Counts are a resource vector; no arbitrary weighted total.",
                        "Uniform independent theoretical probes use Python pseudorandom draws in examples.",
                        "Generation and validation excluded from method times but explicitly retained."],
              "exact_law_cases": law, "product_cases": cases}
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "law_cases": len(law),
                      "product_cases": len(cases),
                      "random_misses": sum(not c["methods"][-1]["correct_range"] for c in cases),
                      "elapsed_ns": result["elapsed_ns_including_generation_validation"]}))


if __name__ == "__main__":
    main()
