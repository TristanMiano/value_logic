"""Optional F12 native finite-program coverage, not F13 case-study completion."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

from v2.checks import f07_soundness as A
from . import program
from .program_model import ProgramEvidence, ProgramQuery
from .program_reference import reference, difference
from .program_control import ordinary_bound

ERROR_CAPS = (Q(0), Q(1, 997), Q(1, 100), Q(1, 43), Q(1, 21), Q(1, 20))
SECOND_CAPS = (Q(1, 5), Q(2, 9), Q(9, 40), Q(2, 7), Q(3, 10))
ALPHAS = (Q(0), Q(1, 6), Q(1, 3), Q(1, 2), Q(9, 10), Q(999, 1000))


def sources():
    return tuple(ProgramEvidence(e, u, f'f12-program-{i}', foreign)
                 for i, (e, u, foreign) in enumerate(product(ERROR_CAPS, SECOND_CAPS, (False, True))))


def check_source(evidence):
    queries = (ProgramQuery(), *(ProgramQuery('risk_vs_full', alpha) for alpha in ALPHAS))
    rows = []
    for query in queries:
        outcome = program.produce(evidence, query)
        full, full_point = reference(evidence, query)
        reduct, reduct_point = reference(evidence, query, reduct=True)
        if outcome.upper_bound != reduct or ordinary_bound(evidence, query) != full or ordinary_bound(evidence, query, reduct=True) != reduct:
            raise AssertionError('Native program/reference/ordinary disagreement.')
        ctx = program.context(evidence)
        if not A.case_feasible(ctx, 'h', dict(zip(('error', 'second'), full_point))):
            raise AssertionError('Full-source program attainer is inadmissible.')
        if difference(query, *full_point) != full:
            raise AssertionError('Direct execution failed to reproduce the maximum.')
        new, old, _ = program.terms(query)
        A.receive(ctx, outcome.proof, A.request(ctx, None, new, old, reduct, 'L'))
        try:
            A.receive(ctx, outcome.proof, A.request(ctx, None, new, old, reduct-Q(1, 1000003), 'L'))
        except A.AuditError:
            pass
        else:
            raise AssertionError('Stricter program request was accepted.')
        if (outcome.status == 'certified') != (reduct <= query.budget):
            raise AssertionError('Native program status changed the target-unit contract.')
        decision = 'certified' if outcome.status == 'certified' else 'refuted' if full > query.budget else 'unavailable'
        rows.append({'consumer': query.kind, 'alpha': str(query.alpha), 'full_bound': str(full),
                     'native_reduct_bound': str(reduct), 'decision': decision,
                     'full_point': [str(x) for x in full_point],
                     'reduct_point': [str(x) for x in reduct_point],
                     'reduct_point_full_source': A.case_feasible(ctx, 'h', dict(zip(('error', 'second'), reduct_point))),
                     'proof_steps': len(outcome.proof.steps)})
    return rows


def report(start=0, stop=None, progress=None):
    population = sources()
    stop = len(population) if stop is None else stop
    if type(start) is not int or type(stop) is not int or not 0 <= start < stop <= len(population):
        raise ValueError('Invalid optional program interval.')
    cases = []
    counts = Counter()
    for i in range(start, stop):
        evidence = population[i]
        if progress:
            progress({'event': 'begin_program_source', 'index': i})
        answers = check_source(evidence)
        counts.update(r['decision'] for r in answers)
        cases.append({'index': i, 'error_cap': str(evidence.error_cap),
                      'second_cap': str(evidence.second_cap), 'foreign_zero': evidence.foreign_zero,
                      'answers': answers})
    return {'status': 'PASS', 'start': start, 'stop': stop, 'sources': stop-start,
            'queries': (stop-start)*7, 'decisions': dict(counts), 'cases': cases,
            'scope': '60 declared exact sources, seven consumers each; no F13 completion or novelty claim'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--stop', type=int)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    data = report(args.start, args.stop, lambda x: print(json.dumps(x), flush=True))
    args.json.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'cases'}, sort_keys=True))


if __name__ == '__main__':
    main()
