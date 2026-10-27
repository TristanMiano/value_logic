"""Development integration: stepped finite refutations and fallible bank advice."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import time
import traceback

SEED = 191927
CORES = (
    ((1,), (-1, 2), (-2,)),
    ((1, 2), (-1, 2), (1, -2), (-1, -2)),
    ((1,), (-1, 2), (-2, 3), (-3,)),
    ((1,), (-1, 2)),
)
SPECS = tuple((i, reverse, False) for i in range(4) for reverse in (False, True)) + ((0, False, True),)


def true_literal(lit, assignment):
    value = bool(assignment & (1 << (abs(lit) - 1)))
    return value if lit > 0 else not value


def produce(core, reverse):
    """One named tick per header, literal test or witness write."""
    n = max(abs(x) for c in core for x in c)
    order = tuple(reversed(range(len(core)))) if reverse else tuple(range(len(core)))
    cert = []
    for assignment in range(1 << n):
        yield 'producer_assignment'
        for ci in order:
            violated = True
            for lit in core[ci]:
                yield 'producer_literal'
                if true_literal(lit, assignment):
                    violated = False
                    break
            if violated:
                yield 'producer_witness'
                cert.append(ci)
                break
        else:
            return None
    return tuple(cert)


def verify(core, cert):
    """Separate replay validates every assignment, without using search state."""
    yield 'checker_header'
    n = max(abs(x) for c in core for x in c)
    if not isinstance(cert, tuple) or len(cert) != 1 << n:
        return False
    for assignment, ci in enumerate(cert):
        yield 'checker_assignment'
        if type(ci) is not int or not 0 <= ci < len(core):
            return False
        for lit in core[ci]:
            yield 'checker_literal'
            if true_literal(lit, assignment):
                return False
    return True


def pipeline(spec):
    ci, reverse, corrupt = spec
    cert = yield from produce(CORES[ci], reverse)
    if cert is None:
        return False
    if corrupt:
        yield 'producer_corruption'
        cert = (len(CORES[ci]),) + cert[1:]
    return (yield from verify(CORES[ci], cert))


class Machine:
    def __init__(self, spec):
        self.iterator = pipeline(spec)
        self.counts = Counter()
        self.terminal = None

    def step(self):
        assert self.terminal is None
        try:
            kind = next(self.iterator)
            self.counts[kind] += 1
            return 'running'
        except StopIteration as result:
            self.counts['termination'] += 1
            self.terminal = 'accepted' if result.value else 'exhausted'
            return self.terminal

    @property
    def ticks(self):
        return sum(self.counts.values())


def full_costs():
    rows = []
    for spec in SPECS:
        machine = Machine(spec)
        while machine.step() == 'running':
            pass
        core = CORES[spec[0]]
        n = max(abs(x) for c in core for x in c)
        # Semantic cross-check uses a direct, independent full assignment test.
        unsat = not any(all(any(true_literal(lit, a) for lit in c) for c in core) for a in range(1 << n))
        expected = unsat and not spec[2]
        assert (machine.terminal == 'accepted') == expected
        rows.append(dict(spec=spec, accepted=expected,
                         completion=machine.ticks if expected else None,
                         terminal_ticks=machine.ticks, counts=dict(machine.counts)))
    return rows


def hit(clauses, bank, counts=None):
    if counts is not None:
        counts['condition_calls'] += 1
    for clause in clauses:
        found = False
        for j in clause:
            if counts is not None:
                counts['membership_tests'] += 1
            if j in bank:
                found = True
                break
        if not found:
            return False
    return True


def compile_request(targets):
    clauses = []
    for target in targets:
        target_set = set(target)
        clauses.append(tuple(j for j, spec in enumerate(SPECS)
                             if set(CORES[spec[0]]) <= target_set))
    return tuple(clauses)


def run(requests, advice, epsilon):
    assert 0 < epsilon <= 1
    machines = [Machine(s) for s in SPECS]
    m = len(machines)
    credit = [Q(0)] * m
    steps = [0] * m
    bank, exhausted = set(), set()
    control = Counter()
    duals = []
    fallback = Q(0)
    fallback_rounds = 0
    for clauses, price in requests:
        advised = hit(clauses, advice, control)
        cap = price if advised else epsilon * price
        used = Q(0)
        row = [Q(0)] * len(clauses)
        while not hit(clauses, bank, control) and used < cap:
            ci = next(a for a, c in enumerate(clauses) if not hit((c,), bank, control))
            active = tuple(j for j in clauses[ci] if j not in exhausted)
            preferred = next((j for j in active if j in advice), None) if advised else None
            rates = {j: (1 / epsilon if j == preferred else Q(1)) for j in active}
            delta = min([cap - used] + [(Q(steps[j] + 1) - credit[j]) / rates[j] for j in active])
            assert delta > 0
            used += delta
            row[ci] += delta
            control['virtual_events'] += 1
            control['threshold_candidates'] += len(active) + 1
            for j in active:
                credit[j] += rates[j] * delta
                control['credit_updates'] += 1
            for j in active:
                if credit[j] == steps[j] + 1:
                    steps[j] += 1
                    outcome = machines[j].step()
                    if outcome == 'accepted':
                        bank.add(j)
                    elif outcome == 'exhausted':
                        exhausted.add(j)
                assert credit[j] < steps[j] + 1
        if not hit(clauses, bank, control):
            assert used == cap
            fallback += price
            fallback_rounds += 1
        duals.append(row)
    total = Counter()
    for machine in machines:
        total.update(machine.counts)
    assert sum(total.values()) == sum(steps)
    return dict(credit=credit, steps=steps, bank=sorted(bank), exhausted=sorted(exhausted),
                duals=duals, work=sum(steps), fallback=fallback,
                bill=Q(sum(steps)) + fallback, fallback_rounds=fallback_rounds,
                completed_ticks=sum(steps[j] for j in bank),
                failed_ticks=sum(steps[j] for j in exhausted),
                unfinished_ticks=sum(steps[j] for j in range(m) if j not in bank | exhausted),
                instruction_counts=dict(total), controller_counts=dict(control))


def bank_cost(lengths, requests, bank):
    if any(lengths[j] is None for j in bank):
        return None
    return Q(sum(lengths[j] for j in bank)) + sum((p for cs, p in requests if not hit(cs, bank)), Q(0))


def offline(lengths, requests):
    candidates = []
    for mask in range(1 << len(lengths)):
        bank = {j for j in range(len(lengths)) if mask >> j & 1}
        cost = bank_cost(lengths, requests, bank)
        if cost is not None:
            candidates.append((cost, mask))
    return min(candidates)


def audit(result, lengths, requests, advice, epsilon, opt):
    d = max([len(c) for cs, p in requests for c in cs] + [0])
    y = sum((sum(row, Q(0)) for row in result['duals']), Q(0))
    for j, length in enumerate(lengths):
        column = sum((row[a] for (cs, p), row in zip(requests, result['duals'])
                      for a, c in enumerate(cs) if j in c), Q(0))
        if length is not None:
            assert column <= result['credit'][j] <= length
        assert result['steps'][j] == result['credit'][j].numerator // result['credit'][j].denominator
    for (cs, p), row in zip(requests, result['duals']):
        assert sum(row, Q(0)) <= p
    assert y <= opt
    rho = d + 1 / epsilon
    assert result['bill'] <= rho * y <= rho * opt
    advice_cost = bank_cost(lengths, requests, advice)
    if advice_cost is not None:
        assert y <= epsilon * advice_cost
        assert result['bill'] <= (1 + d * epsilon) * advice_cost
    return dict(width=d, opt=opt, advice_cost=advice_cost, dual=y,
                robust_bound=rho * opt,
                advice_bound=(1 + d * epsilon) * advice_cost if advice_cost is not None else None)


def serial(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [serial(v) for v in x]
    return x


def compact(result):
    return {k: v for k, v in result.items() if k not in ('credit', 'duals', 'steps')}


def main():
    rng = random.Random(SEED)
    schedules = []
    for case in range(24):
        requests, contexts = [], []
        for t in range((8, 32, 128)[case % 3]):
            targets = []
            for _ in range(rng.randrange(3)):
                core = CORES[rng.randrange(len(CORES))]
                if rng.randrange(2):
                    core = core + ((1, -1),)
                targets.append(core)
            cs = compile_request(targets)
            price = rng.choice((Q(1, 3), Q(1), Q(4), Q(16)))
            requests.append((cs, price))
            contexts.append(targets)
        schedules.append((contexts, requests))
    input_hash = hashlib.sha256(json.dumps(serial(schedules), sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    costs = full_costs()
    lengths = [row['completion'] for row in costs]
    rows = []
    checks = 0
    for case, (contexts, requests) in enumerate(schedules):
        opt, mask = offline(lengths, requests)
        banks = dict(empty=set(), first={0, 2, 4}, second={1, 3, 5},
                     satisfiable={6}, corrupt={8},
                     hindsight={j for j in range(len(SPECS)) if mask >> j & 1})
        methods = []
        for name, advice in banks.items():
            for epsilon in (Q(1), Q(1, 2), Q(1, 4)):
                result = run(requests, advice, epsilon)
                bounds = audit(result, lengths, requests, advice, epsilon, opt)
                methods.append(dict(advice=name, epsilon=epsilon, result=compact(result), bounds=bounds))
                checks += 1
        independent = Counter()
        independent_fallback = Q(0)
        for request in requests:
            result = run([request], set(), Q(1))
            independent['work'] += result['work']
            independent_fallback += result['fallback']
        rows.append(dict(case=case, requests=len(requests), opt=opt, offline_mask=mask,
                         fallback_only=sum((p for cs, p in requests if not hit(cs, set())), Q(0)),
                         independent_work=independent['work'], independent_fallback=independent_fallback,
                         independent_bill=Q(independent['work']) + independent_fallback,
                         methods=methods))
    totals = {}
    for name in ('empty', 'first', 'second', 'satisfiable', 'corrupt', 'hindsight'):
        for epsilon in (Q(1), Q(1, 2), Q(1, 4)):
            selected = [m['result'] for row in rows for m in row['methods']
                        if m['advice'] == name and m['epsilon'] == epsilon]
            totals[f'{name}:{epsilon}'] = {key: sum((r[key] for r in selected), Q(0))
                                          for key in ('work', 'fallback', 'bill', 'failed_ticks', 'unfinished_ticks')}
    return dict(status='PASS', seed=SEED, input_sha256=input_hash,
                procedure_costs=costs, schedules=len(rows), policy_checks=checks,
                totals=totals, fallback_only=sum((r['fallback_only'] for r in rows), Q(0)),
                independent_bill=sum((r['independent_bill'] for r in rows), Q(0)),
                offline_bill=sum((r['opt'] for r in rows), Q(0)), rows=rows,
                scope='Finite truth-table refutations, separate replay validation, exact credit and bank bounds. Named ticks are not CPU instructions. Hindsight advice is an oracle control, not a learned predictor.')


if __name__ == '__main__':
    start = time.perf_counter_ns()
    try:
        result = main()
    except Exception:
        result = dict(status='FAIL', traceback=traceback.format_exc())
    result['runtime_ns'] = time.perf_counter_ns() - start
    result['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    target = Path(__file__).with_name('proof_machine_result.json')
    assert not target.exists(), 'Preserve prior evidence; version any repair.'
    target.write_bytes((json.dumps(serial(result), indent=2) + '\n').encode())
    print(json.dumps(serial({k: v for k, v in result.items() if k not in ('rows',)}), indent=2))
    if result['status'] != 'PASS':
        raise SystemExit(1)
