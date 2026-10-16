"""Finite off-path classification and selection-bias screen. Codex (GPT-6)."""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


def orders(n, d):
    return [p for p in permutations(range(n))
            if all(abs(i-v) <= d for i, v in enumerate(p))]


def stopped(x, state, threshold):
    yes = sum(x[i] for i in state)
    return yes >= threshold or yes+len(x)-len(state) < threshold


def run(case):
    n, d = [(5, 1), (6, 2)][case]
    paths = orders(n, d)
    states = sorted({frozenset(p[:k]) for p in paths for k in range(n)},
                    key=lambda s: (len(s), tuple(sorted(s))))
    counts = dict(executions=0, early_checks=0, late_checks=0,
                  unclassified_states=0)
    for x in product((0, 1), repeat=n):
        for threshold in range(1, n+1):
            for p in paths:
                m = next(k for k in range(1, n+1)
                         if stopped(x, frozenset(p[:k]), threshold))
                before = frozenset(p[:m-1])
                after = frozenset(p[:m])
                counts['executions'] += 1
                unknown_layers = set()
                for s in states:
                    k = len(s)
                    if k <= m-1-2*d:
                        assert s <= before and not stopped(x, s, threshold)
                        counts['early_checks'] += 1
                    elif k >= m+2*d:
                        assert s >= after and stopped(x, s, threshold)
                        counts['late_checks'] += 1
                    else:
                        unknown_layers.add(k)
                        counts['unclassified_states'] += 1
                assert len(unknown_layers) <= 4*d
    bias_paths = orders(6, 1)
    containing = sum(p[:2] == (0, 1) for p in bias_paths)
    propensity = Fraction(containing, len(bias_paths))
    assert propensity == Fraction(5, 13)
    for p in bias_paths:
        assert next(k for k in range(1, 7)
                    if stopped((0,)*6, frozenset(p[:k]), 1)) == 6
    naive_mean = 1/propensity
    assert naive_mean == Fraction(13, 5) and naive_mean != 1
    return dict(case=case, n=n, bandwidth=d, paths=len(paths), states=len(states),
                counts=counts, bias_example=dict(path_propensity=str(propensity),
                observation_probability='1', true_loss='1', naive_mean=str(naive_mean)),
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                contributor='Codex (GPT-6)', status='DEVELOPMENT_PASS')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    result = run(args.case)
    args.out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))
