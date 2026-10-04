"""Compare separately constructed native, geometric and analytic answers."""
from collections import Counter
from fractions import Fraction as Q

from v2.checks import f07_soundness as A
from .model import Evidence, Query, core_states
from . import native
from .ordinary import analytic_bound
from .producer import Limits, produce
from .reference import feasible, reference, task_losses


def assess(evidence: Evidence, query: Query, limits: Limits = Limits()):
    report, _ = assess_with_proof(evidence, query, limits)
    return report


def assess_with_proof(evidence: Evidence, query: Query, limits: Limits = Limits()):
    produced = produce(evidence, query, limits)
    semantic = reference(evidence, query)
    ordinary = analytic_bound(evidence, query)
    if ordinary != semantic.maximum:
        raise AssertionError('Independent semantic reference disagrees with ordinary formula.')
    if produced.upper_bound is not None and produced.upper_bound < semantic.maximum:
        raise AssertionError('Native upper bound is below an admitted semantic witness.')
    if produced.status == 'certified':
        # Rebuild from the original inputs at the receiving boundary.
        ctx = native.context(evidence)
        A.receive(ctx, produced.proof, native.request(ctx, query))
        if semantic.maximum > query.budget:
            raise AssertionError('False certification of the declared query.')
        decision = 'certified'
    elif semantic.maximum > query.budget:
        if not feasible(evidence, semantic.witness):
            raise AssertionError('Refuting witness does not satisfy the full source.')
        losses = task_losses(semantic.witness)
        if losses[query.action] - losses['F'] <= query.budget:
            raise AssertionError('Witness does not refute the requested comparison.')
        decision = 'refuted'
    else:
        decision = 'unavailable'
    report = {
        'action': query.action, 'requested_budget': str(query.budget),
        'decision': decision, 'producer_status': produced.status,
        'producer_reason': produced.reason,
        'native_upper_bound': None if produced.upper_bound is None else str(produced.upper_bound),
        'reference_maximum': str(semantic.maximum), 'ordinary_bound': str(ordinary),
        'reference_attainer': [str(x) for x in semantic.witness],
        'countermodel_domain': 'full_source' if decision == 'refuted' else None,
        'target_unit_reduct_equals_full_source': semantic.target_unit_reduct_same,
        'basis_checks': produced.basis_checks, 'feasible_bases': produced.feasible_bases,
        'proof_steps': 0 if produced.proof is None else len(produced.proof.steps),
        'reference_candidates': semantic.candidate_count,
    }
    return report, produced


def core_report():
    cases = []
    counts = Counter()
    for evidence in core_states():
        comparisons = [assess(evidence, Query(action)) for action in ('T1', 'T2', 'R')]
        for result in comparisons:
            counts[result['decision']] += 1
            if result['native_upper_bound'] != result['reference_maximum']:
                raise AssertionError('Core slice lacks an exact native bound.')
        action = next((r['action'] for r in comparisons if r['decision'] == 'certified'), 'F')
        cases.append({'revision': evidence.revision,
                      'bounds': [None if x is None else str(x) for x in evidence.bounds],
                      'comparisons': comparisons, 'selected_action': action})
    limited = assess(Evidence(Q(0), Q(0), Q(0), Q(0)), Query('T1'), Limits(0))
    if limited['decision'] != 'unavailable' or Q(limited['reference_maximum']) > 0:
        raise AssertionError('A search limit must preserve a valid-but-unavailable outcome.')
    return {
        'status': 'PASS', 'scope': 'F11 first slice: 16 states, 3 queries; exact rational inputs',
        'native_kernel_changed': False, 'project_novelty': 'NOT YET SUPPORTED',
        'states': len(cases), 'queries': sum(counts.values()), 'decisions': dict(sorted(counts.items())),
        'all_native_bounds_match_reference': True,
        'ordinary_baseline': 'N01 twelve-expression closed form; no free native receipt',
        'countermodels': 'full-source; all rows are in the query unit in this fixed fragment',
        'limited_search_control': limited, 'cases': cases,
    }
