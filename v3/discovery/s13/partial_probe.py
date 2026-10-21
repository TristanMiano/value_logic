"""Small exposed development screen, 360 random adaptive public protocols.
Exact rational fees and losses; no independent confirmation or timing comparison.
Private answers reset at every episode. Cap and stopping are enforced structurally.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import random
import time

ROOT = Path(__file__).resolve().parent
SEED = 202610209
RNG = random.Random(SEED)


def beta(h, fee):
    return min((r + 2 - F(1, 2 ** (h - 1 - r)) + fee) /
               (r + 2 - F(2, 2 ** (h - 1 - r))) for r in range(h - 1))


def private_tree(available, remaining, root=False):
    if not remaining or (not root and RNG.random() < .4):
        return None
    i = RNG.choice(available)
    rest = tuple(j for j in available if j != i)
    return (i, private_tree(rest, remaining - 1), private_tree(rest, remaining - 1))


def bill(tree, x):
    count = 0
    while tree is not None:
        i, left, right = tree
        count += 1
        tree = (left, right)[(x >> i) & 1]
    return count


def experiment(n, cap, fee, episodes, mode):
    terminals = []
    fee_sum = F(0)
    calls = 0

    def visit(worlds, remaining):
        nonlocal fee_sum, calls
        signs = {1 if x.bit_count() % 2 == 0 else -1 for x in worlds}
        if not remaining or len(worlds) == 1 or (mode == 'parity' and len(signs) == 1):
            terminals.append(worlds)
            return
        if mode == 'partial' and RNG.random() < .15:
            terminals.append(worlds)
            return
        tree = private_tree(tuple(range(n)), cap, root=True)
        groups = defaultdict(list)
        for x in worlds:
            k = bill(tree, x)
            assert 1 <= k <= cap
            fee_sum += k + fee
            groups[k].append(x)
        calls += 1
        for group in groups.values():
            visit(group, remaining - 1)

    visit(list(range(1 << n)), episodes)
    assert sorted(x for w in terminals for x in w) == list(range(1 << n))
    cost = fee_sum / (1 << n)
    absolute = F(0)
    information = F(0)
    vector_wrong = 0
    edges = 0
    all_biased = True
    for w in terminals:
        m = len(w)
        sign_sum = sum(1 if x.bit_count() % 2 == 0 else -1 for x in w)
        absolute += F(abs(sign_sum), 1 << n)
        information += F(sign_sum * sign_sum, m * (1 << n))
        vector_wrong += m - 1
        ws = set(w)
        e = sum((x ^ (1 << i)) in ws for x in w for i in range(n)) // 2
        edges += e
        assert e <= F(n, 2) * (m - abs(sign_sum))
        assert e <= F(n * (1 << (n - 1)), (1 << n) - 1) * (m - 1)
        all_biased &= (abs(sign_sum) < m)
    rate = beta(cap, fee)
    vector_error = F(vector_wrong, 1 << n)
    q = max(F(0), 1 - vector_error / (1 - F(1, 1 << n)))
    assert cost >= rate * n * absolute >= rate * n * information
    assert cost >= q * rate * n
    # The local edge bound gives the common stronger intermediate inequality.
    assert cost >= 2 * rate * (F(n, 2) - F(edges, 1 << n))
    # Exact channel identities at a rational nonzero parameter.
    theta = F(1, 3)
    chi_square = F(0)
    tv = F(0)
    for w in terminals:
        p0 = F(len(w), 1 << n)
        bias = F(sum(1 if x.bit_count() % 2 == 0 else -1 for x in w), len(w))
        plus, minus = p0 * (1 + theta * bias), p0 * (1 - theta * bias)
        chi_square += (plus - p0) ** 2 / p0
        tv += abs(plus - minus) / 2
    assert chi_square == theta * theta * information and tv == theta * absolute
    return dict(cost=str(cost), information=str(information), absolute=str(absolute),
                vector_error=str(vector_error), lower_fee=str(rate*n*information),
                calls=calls, terminals=len(terminals), all_terminal_biases_partial=all_biased)


def main():
    began = time.perf_counter_ns()
    counts = dict(protocols=0, private_programs=0, terminal_cells=0,
                  informative=0, zero_information=0, strictly_partial_information=0)
    examples = []
    for n in range(3, 7):
        for cap in (2, 3, n):
            for fee in (F(0), F(1, 2), F(3)):
                for case in range(10):
                    mode = ('partial', 'parity', 'vector')[case % 3]
                    row = experiment(n, cap, fee, 2 + case, mode)
                    counts['protocols'] += 1
                    counts['private_programs'] += row['calls']
                    counts['terminal_cells'] += row['terminals']
                    info = F(row['information'])
                    counts['informative' if info else 'zero_information'] += 1
                    counts['strictly_partial_information'] += 0 < info < 1
                    if 0 < info < 1 and len(examples) < 4:
                        examples.append(dict(n=n, cap=cap, reset=str(fee), mode=mode, **row))
    result = dict(status='PASS', contributor='Codex (GPT-6)', seed=SEED, counts=counts,
                  examples=examples, elapsed_ns=time.perf_counter_ns()-began,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  scope='finite generated protocols only; not all protocols, proof, application gain, or independent confirmation')
    (ROOT/'partial_probe.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
