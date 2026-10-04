"""Run the optional finite-program adapter; F13 remains a separate task."""
import argparse
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

from v2.checks import f07_soundness as A
from . import program
from .program_model import ProgramEvidence, ProgramQuery
from .program_reference import difference, loss_law, reference


def ordinary_bound(evidence, query, *, reduct=False):
    """Constant-size baseline at the same information access as each domain."""
    evidence.validate(); query.validate()
    if query.kind == 'mean_edit':
        return Q(evidence.second_cap)-Q(9, 40)
    error = Q(0) if evidence.foreign_zero and not reduct else Q(evidence.error_cap)
    mass = Q(1)-Q(query.alpha)
    return min(Q(3, 20)+(error+Q(3, 40))/mass,
               Q(3, 10)+Q(17, 20)*error/mass, Q(23, 20))-Q(3, 10)


def assess(evidence, query):
    outcome = program.produce(evidence, query)
    full, full_point = reference(evidence, query)
    reduct, reduct_point = reference(evidence, query, reduct=True)
    if ordinary_bound(evidence, query) != full or ordinary_bound(evidence, query, reduct=True) != reduct:
        raise AssertionError('Ordinary closed form disagrees with independently executed losses.')
    if outcome.upper_bound != reduct:
        raise AssertionError('Program producer and independent reduct reference disagree.')
    ctx = program.context(evidence)
    if outcome.status == 'certified':
        A.receive(ctx, outcome.proof, program.request(ctx, query))
        if full > query.budget:
            raise AssertionError('False certification on a full-source point.')
        decision = 'certified'
    elif full > query.budget:
        if not A.case_feasible(ctx, 'h', dict(zip(('error', 'second'), full_point))):
            raise AssertionError('Full-source counterexample violates the source.')
        decision = 'refuted'
    else:
        decision = 'unavailable'
    return {
        'consumer': query.kind, 'alpha': str(query.alpha), 'budget': str(query.budget),
        'decision': decision, 'producer_status': outcome.status,
        'native_bound': str(outcome.upper_bound), 'full_source_maximum': str(full),
        'target_unit_reduct_maximum': str(reduct),
        'ordinary_full_source_bound': str(ordinary_bound(evidence, query)),
        'ordinary_reduct_bound': str(ordinary_bound(evidence, query, reduct=True)),
        'full_source_attainer': [str(x) for x in full_point],
        'reduct_attainer': [str(x) for x in reduct_point],
        'reduct_attainer_satisfies_full_source': A.case_feasible(ctx, 'h', dict(zip(('error', 'second'), reduct_point))),
        'countermodel_domain': 'full_source' if decision == 'refuted' else
                               ('target_unit_reduct' if reduct > query.budget else None),
        'proof_steps': len(outcome.proof.steps), 'basis_checks': outcome.basis_checks,
    }


def report():
    cases = []
    queries = (ProgramQuery(), *(ProgramQuery('risk_vs_full', a)
                                  for a in (Q(0), Q(1, 6), Q(1, 3), Q(9, 10))))
    for i, (error_cap, second_cap) in enumerate(product((Q(0), Q(1, 20)),
                                                       (Q(1, 5), Q(9, 40), Q(3, 10)))):
        evidence = ProgramEvidence(error_cap, second_cap, f'program-{i}')
        cases.append({'error_cap': str(error_cap), 'second_cap': str(second_cap),
                      'results': [assess(evidence, query) for query in queries]})
    old_law = loss_law('adaptive', Q(1, 20), Q(1, 5))
    if old_law != loss_law('adaptive', Q(1, 20), Q(3, 10)):
        raise AssertionError('The old full-loss-law discriminator failed.')
    deltas = [difference(ProgramQuery(), Q(1, 20), u) for u in (Q(1, 5), Q(3, 10))]
    gap = assess(ProgramEvidence(foreign_zero=True), ProgramQuery('risk_vs_full', budget=Q(-1, 20)))
    if gap['decision'] != 'unavailable' or gap['reduct_attainer_satisfies_full_source']:
        raise AssertionError('The reduct counterexample was confused with a full-source one.')
    return {
        'status': 'PASS', 'scope': 'optional F11 finite-program adapter; not F13 completion',
        'native_kernel_changed': False, 'novelty': 'NOT YET SUPPORTED',
        'cases': cases, 'family_queries': 30, 'unit_boundary_control': gap,
        'old_loss_law': [[str(x), str(p)] for x, p in old_law],
        'same_old_law_edit_differences': [str(d) for d in deltas],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    data = report()
    if args.json:
        args.json.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k != 'cases'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
