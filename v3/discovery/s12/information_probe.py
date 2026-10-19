"""Codex (GPT-6), s12 DEVELOPMENT: Fisher information per invoice fee.

Enumerated private programs, exact arithmetic, public stopping allowed at any
cell. No simulation or asymptotic statistical performance claim.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys
import time
from parity_price_probe import all_invoice_functions, partitions

HERE = Path(__file__).resolve().parent


def solve_panel(fees, cap, overhead, target):
    n = len(fees)
    full = (1 << (1 << n)) - 1
    bank = partitions(all_invoice_functions(fees, cap))
    signed = [1 if (x & target).bit_count() % 2 == 0 else -1 for x in range(1 << n)]
    stats = dict(exact_states=0, information_states=0, program_choices=0, ratio_iterations=0)

    @lru_cache(None)
    def moment(source):
        return F(sum(signed[x] for x in range(1 << n) if source >> x & 1), source.bit_count())

    @lru_cache(None)
    def choices(source):
        size = source.bit_count()
        out = []
        for index, program in enumerate(bank):
            groups = [(fee, subset & source) for fee, subset in program if subset & source]
            if len(groups) <= 1:
                continue
            mean = sum((F(subset.bit_count(), size) * (fee + overhead) for fee, subset in groups), F(0))
            out.append((index, mean, tuple((F(subset.bit_count(), size), subset) for _, subset in groups)))
        return tuple(out)

    @lru_cache(None)
    def exact(source):
        if abs(moment(source)) == 1:
            return F(0)
        stats['exact_states'] += 1
        return min(mean + sum((p * exact(subset) for p, subset in groups), F(0))
                   for _, mean, groups in choices(source))

    exact_cost = exact(full)

    def information(lam):
        policy = {}
        @lru_cache(None)
        def value(source):
            stats['information_states'] += 1
            best_cost, best_info = F(0), moment(source) ** 2
            best_objective = best_cost - lam * best_info
            policy[source] = None
            for index, mean, groups in choices(source):
                stats['program_choices'] += 1
                children = [(p, value(subset)) for p, subset in groups]
                cost = mean + sum((p * result[0] for p, result in children), F(0))
                info = sum((p * result[1] for p, result in children), F(0))
                objective = cost - lam * info
                if objective < best_objective or (objective == best_objective and info > best_info):
                    best_cost, best_info, best_objective = cost, info, objective
                    policy[source] = index
            return best_cost, best_info
        cost, info = value(full)
        def witness(source):
            index = policy[source]
            if index is None:
                return dict(source=source, stop_moment=str(moment(source)))
            branches = []
            for fee, subset in bank[index]:
                if subset & source:
                    branches.append(dict(invoice=fee, child=witness(subset & source)))
            return dict(source=source, program_index=index, branches=branches)
        return cost, info, witness

    lam = exact_cost
    trace = []
    for _ in range(100):
        stats['ratio_iterations'] += 1
        cost, info, witness = information(lam)
        assert info > 0, (fees, cap, overhead, target, lam, cost, info)
        residual = cost - lam * info
        assert residual <= 0
        trace.append(dict(lambda_=str(lam), cost=str(cost), information=str(info), residual=str(residual)))
        if residual == 0:
            break
        lam = cost / info
    else:
        raise RuntimeError('Prospective 100-iteration cap reached')
    result = dict(fees=fees, cap=cap, overhead=overhead, target=target, programs=len(bank),
                  exact_mean_cost=str(exact_cost), best_fee_per_information=str(lam),
                  cost=str(cost), information=str(info), improved=lam < exact_cost,
                  trace=trace, stats=stats)
    if lam < exact_cost:
        result['witness'] = witness(full)
    return result


def main():
    started = time.perf_counter_ns()
    panels = [solve_panel(fees, cap, overhead, target)
              for fees in [(1, 1, 1), (1, 2, 7), (1, 1, 100), (2, 3, 5)]
              for cap in [2, 3] for overhead in [0, 1, 3] for target in [1, 3, 7]]
    totals = {key: sum(p['stats'][key] for p in panels) for key in panels[0]['stats']}
    totals.update(panels=len(panels), improved=sum(p['improved'] for p in panels))
    result = dict(status='PASS', contributor='Codex (GPT-6)', scope='DEVELOPMENT',
                  python=sys.version, elapsed_ns=time.perf_counter_ns()-started,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  dependency_sha256=hashlib.sha256((HERE/'parity_price_probe.py').read_bytes()).hexdigest(),
                  totals=totals, panels=panels,
                  limitations='Three-bit full-cube parity tilt at theta=0 only. Exact invoice, '
                  'all enumerated private programs and stopping policies. No controller work, '
                  'all-size theorem, independent confirmation or online-regret optimality.')
    (HERE/'information_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps({k: result[k] for k in ('status', 'elapsed_ns', 'totals')}, indent=2))
    for panel in panels:
        if panel['improved']:
            print(json.dumps({k: panel[k] for k in ('fees','cap','overhead','target','exact_mean_cost','best_fee_per_information')}))


if __name__ == '__main__':
    main()
