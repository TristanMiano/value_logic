"""Developmental threshold certificate acquisition, Codex (GPT-6).

Query costs are stipulated integer work tariffs, NOT measured solver time.
Only the oracle sees hidden values. All policies use the same exact stop rule.
SBB is the conventional Salloum--Breuer--Ben-Dov rule (DS03), not our invention.
Run: python v3/discovery/s01/probe.py v3/discovery/s01/run01.json
"""
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import cmp_to_key, lru_cache
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import sys
import time
import traceback


@dataclass(frozen=True)
class Request:
    weights: tuple
    prices: tuple
    threshold: int
    prediction: tuple
    probabilities: tuple


class Oracle:
    def __init__(self, values, prices):
        self._values = tuple(values)
        self.prices = prices
        self.receipts = {}
        self.bill = 0

    def query(self, index):
        assert index not in self.receipts, 'Duplicate paid query.'
        answer = self._values[index]
        self.bill += self.prices[index]
        self.receipts[index] = answer
        return answer


def sorted_counted(items, key, counts):
    decorated = []
    for item in items:
        counts['selector_scores'] += 1
        decorated.append((key(item), item))

    def compare(a, b):
        counts['sort_comparisons'] += 1
        return (a > b) - (a < b)

    return [i for _, i in sorted(decorated, key=cmp_to_key(compare))]


def make_selector(req, policy, counts):
    n = len(req.weights)
    if policy == 'index':
        order = list(range(n))
    elif policy == 'reverse':
        order = list(range(n-1, -1, -1))
    elif policy == 'cheap':
        order = sorted_counted(range(n), lambda i: req.prices[i], counts)
    elif policy == 'weight':
        order = sorted_counted(range(n), lambda i: -F(req.weights[i], req.prices[i]), counts)
    elif policy == 'guided':
        counts['prediction_reads'] += n
        predicted_answer = sum(w*x for w, x in zip(req.weights, req.prediction)) >= req.threshold
        order = sorted_counted(range(n), lambda i: (req.prediction[i] != predicted_answer,
                                                      -F(req.weights[i], req.prices[i])), counts)
    elif policy == 'sbb':
        assert all(w == 1 for w in req.weights)
        counts['prediction_reads'] += n
        # This implementation re-sorts the remaining set on each query.
        # A cached-order control below avoids claiming an avoidable overhead win.
        order = None
    elif policy == 'sbb_cached':
        assert all(w == 1 for w in req.weights)
        counts['prediction_reads'] += n
        one_order = sorted_counted(range(n), lambda i: F(req.prices[i]) / req.probabilities[i], counts)
        zero_order = sorted_counted(range(n), lambda i: F(req.prices[i]) / (1-req.probabilities[i]), counts)
        order = None
    else:
        raise ValueError(policy)

    def choose(known, ones, remaining_weight):
        counts['selector_calls'] += 1
        if order is not None:
            for i in order:
                counts['membership_checks'] += 1
                if i not in known:
                    return i
        remaining = []
        for i in range(n):
            counts['membership_checks'] += 1
            if i not in known:
                remaining.append(i)
        k = req.threshold - ones
        if policy == 'sbb':
            one = sorted_counted(remaining, lambda i: F(req.prices[i]) / req.probabilities[i], counts)
            zero = sorted_counted(remaining, lambda i: F(req.prices[i]) / (1-req.probabilities[i]), counts)
        else:
            one, zero = [], []
            for i in one_order:
                counts['membership_checks'] += 1
                if i not in known:
                    one.append(i)
            for i in zero_order:
                counts['membership_checks'] += 1
                if i not in known:
                    zero.append(i)
        candidates = set(one[:k]) & set(zero[:len(remaining)-k+1])
        counts['intersection_items'] += len(one[:k]) + len(zero[:len(remaining)-k+1])
        assert candidates
        return min(candidates)

    return choose


def execute(req, policy, query):
    counts = Counter()
    choose = make_selector(req, policy, counts)
    known, path = {}, []
    ones, remaining = 0, sum(req.weights)
    while True:
        counts['bound_checks'] += 1
        if ones >= req.threshold:
            return dict(answer=1, known=known, path=path, control=dict(counts))
        if ones + remaining < req.threshold:
            return dict(answer=0, known=known, path=path, control=dict(counts))
        i = choose(known, ones, remaining)
        assert i not in known
        x = query(i)
        if x is None:
            return dict(answer=None, known=known, path=path, blocked=i, control=dict(counts))
        assert x in (0, 1)
        path.append(i)
        known[i] = x
        ones += req.weights[i] * x
        remaining -= req.weights[i]
        counts['bound_updates'] += 1


def run(req, values, policy):
    oracle = Oracle(values, req.prices)
    result = execute(req, policy, oracle.query)
    result['query_cost'] = oracle.bill
    assert result['answer'] == int(sum(w*x for w, x in zip(req.weights, values)) >= req.threshold)
    return result


def replay(req, policy, receipts):
    result = execute(req, policy, lambda i: receipts.get(i))
    lower = sum(req.prices[i] for i in result['path'])
    if result['answer'] is None:
        lower += req.prices[result['blocked']]
        upper = sum(req.prices)
    else:
        upper = lower
    return dict(lower=lower, upper=upper, exact=lower == upper,
                completed=result['answer'] is not None, control=result['control'])


def expected_query_cost(req, policy):
    expected = F(0)
    for values in product((0, 1), repeat=len(req.weights)):
        mass = F(1)
        for p, x in zip(req.probabilities, values):
            mass *= p if x else 1-p
        expected += mass * run(req, values, policy)['query_cost']
    return expected


def optimal_expected_query_cost(req):
    """Strong ordinary exact product-model Bellman control, tiny n only."""
    @lru_cache(None)
    def solve(state):
        lower = sum(w*x for w, x in zip(req.weights, state) if x != -1)
        remaining = sum(w for w, x in zip(req.weights, state) if x == -1)
        if lower >= req.threshold or lower + remaining < req.threshold:
            return F(0)
        candidates = []
        for i, x in enumerate(state):
            if x != -1:
                continue
            zero, one = list(state), list(state)
            zero[i], one[i] = 0, 1
            p = req.probabilities[i]
            candidates.append(req.prices[i] + (1-p)*solve(tuple(zero)) + p*solve(tuple(one)))
        return min(candidates)
    value = solve((-1,) * len(req.weights))
    return value, solve.cache_info().currsize


def main(output):
    assert not output.exists(), 'Development output already exists; preserve it.'
    start = time.monotonic_ns()
    result = dict(status='running', evidence='DEVELOPMENT', contributor='Codex (GPT-6)',
                  start_utc=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
                  command=sys.argv, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  cost_scope='stipulated exact-query tariffs plus separate counted controller events; not solver wall time')
    try:
        # Cheap exact correctness screen, not confirmation: all x and predictions
        # for every threshold through n=5; preserve case counts, not huge snapshots.
        cases = 0
        for n in range(1, 6):
            for k in range(1, n+1):
                for prediction in product((0, 1), repeat=n):
                    req = Request((1,)*n, (1,)*n, k, prediction, (F(1, 2),)*n)
                    for values in product((0, 1), repeat=n):
                        run(req, values, 'guided')
                        cases += 1
        result['guided_correctness_cases'] = cases
        # Exact counterexample to a tempting k + Hamming error cost bound.
        n, k = 32, 2
        values = (1,) + (0,)*(n-2) + (1,)
        prediction = (1, 1) + (0,)*(n-2)
        req = Request((1,)*n, (1,)*n, k, prediction, (F(1, 2),)*n)
        witness = run(req, values, 'guided')
        result['two_error_witness'] = dict(n=n, k=k, values=values, prediction=prediction,
                                            hamming=sum(x != y for x, y in zip(values, prediction)), result=witness)
        assert witness['query_cost'] == n
        # Reconstruct SBB against exact Bellman expected cost, including unequal
        # prices and nonconstant probabilities. Known-product assumption only.
        product_checks = []
        for n in (3, 5, 7):
            for k in sorted({1, (n+1)//2, n}):
                req = Request((1,)*n, tuple(1+i%3 for i in range(n)), k,
                              tuple(i%2 for i in range(n)), tuple(F(1+i%4, 5) for i in range(n)))
                optimum, states = optimal_expected_query_cost(req)
                sbb = expected_query_cost(req, 'sbb')
                cached = expected_query_cost(req, 'sbb_cached')
                assert sbb == optimum == cached
                product_checks.append(dict(n=n, k=k, sbb=str(sbb), exact_bellman=str(optimum),
                                           bellman_states=states, index=str(expected_query_cost(req, 'index')),
                                           guided=str(expected_query_cost(req, 'guided'))))
        result['product_model_checks'] = product_checks
        # Measure replay coverage under cheap exact finite policies. The selected
        # path alone supplies receipts; private truth is used only by evaluator.
        policies = ['index', 'reverse', 'cheap', 'weight', 'guided', 'sbb_cached']
        replay_records = []
        for n, k, ones in ((12, 2, (0, 1)), (12, 2, (10, 11)), (12, 6, tuple(range(6))),
                             (12, 6, tuple(range(0, 12, 2))), (12, 11, (0, 1)), (12, 2, tuple(range(12)))):
            values = tuple(int(i in ones) for i in range(n))
            prediction = tuple(values[i] if i%5 else 1-values[i] for i in range(n))
            req = Request((1,)*n, tuple(30+i%3 for i in range(n)), k, prediction,
                          tuple(F(4, 5) if x else F(1, 5) for x in prediction))
            actual = {p: run(req, values, p) for p in policies}
            for selected in policies:
                bounds = {p: replay(req, p, actual[selected]['known']) for p in policies}
                for p in policies:
                    assert bounds[p]['lower'] <= actual[p]['query_cost'] <= bounds[p]['upper']
                replay_records.append(dict(n=n, k=k, values=values, prediction=prediction,
                                           selected=selected, selected_result=actual[selected],
                                           query_costs={p: actual[p]['query_cost'] for p in policies},
                                           control={p: actual[p]['control'] for p in policies}, bounds=bounds))
        result['replay_records'] = replay_records
        result['replay_summary'] = dict(records=len(replay_records), policy_intervals=len(replay_records)*len(policies),
                                        completed=sum(b['completed'] for r in replay_records for b in r['bounds'].values()),
                                        exact_cost=sum(b['exact'] for r in replay_records for b in r['bounds'].values()),
                                        replay_controller_events=sum(sum(b['control'].values()) for r in replay_records for b in r['bounds'].values()))
        result['status'] = 'complete'
    except Exception:
        result['status'] = 'failed'
        result['failure'] = traceback.format_exc()
        raise
    finally:
        result['elapsed_ns'] = time.monotonic_ns()-start
        result['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({k: v for k, v in result.items() if k not in ('replay_records', 'two_error_witness')}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
