"""Finite exact audits of F05 observation, relative-cost and report semantics.

This module checks supplied finite interpretations, not arbitrary polyhedral
validity or proof derivability. Mathematical generalizations are proved in
03b_observation_and_revision_audit.md. Log-loss reference checks use binary64
only as numerical regressions; the rational enclosure is justified analytically.
Python 3.10+, standard library only; no network training or external solver.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path
from typing import Mapping, Sequence
import unittest


class InterpretationError(ValueError):
    """Ill-formed finite interpretation, not a mathematical countermodel."""


def exact(x: int | F) -> F:
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise InterpretationError('Use exact integers or Fractions, not floats/bools.')
    return F(x)


def vector(xs: Sequence[int | F]) -> tuple[F, ...]:
    result = tuple(exact(x) for x in xs)
    if not result:
        raise InterpretationError('An empty vector is not an interpretation.')
    return result


def probability(x: int | F) -> F:
    x = exact(x)
    if not 0 <= x <= 1:
        raise InterpretationError('Probability/report must lie in [0,1].')
    return x


def lottery(xs: Sequence[int | F]) -> tuple[F, ...]:
    xs = vector(xs)
    if any(x < 0 for x in xs) or sum(xs) != 1:
        raise InterpretationError('A lottery must be nonnegative and normalized.')
    return xs


def dot(a: Sequence[int | F], b: Sequence[int | F]) -> F:
    a, b = vector(a), vector(b)
    if len(a) != len(b):
        raise InterpretationError('Dimension mismatch.')
    return sum((x*y for x, y in zip(a, b)), F(0))


def relative(cost: Sequence[int | F], reference: int = 0) -> tuple[F, ...]:
    cost = vector(cost)
    if isinstance(reference, bool) or not isinstance(reference, int) or not 0 <= reference < len(cost):
        raise InterpretationError('Invalid reference action.')
    return tuple(x-cost[reference] for x in cost)


def contrast(cost: Sequence[int | F], new: Sequence[int | F], old: Sequence[int | F]) -> F:
    new, old = lottery(new), lottery(old)
    if len(new) != len(old):
        raise InterpretationError('Policy action dimensions differ.')
    return dot(tuple(a-b for a, b in zip(new, old)), cost)


def span(xs: Sequence[int | F]) -> F:
    xs = vector(xs)
    return max(xs)-min(xs)


def total_variation(p: Sequence[int | F], q: Sequence[int | F]) -> F:
    p, q = lottery(p), lottery(q)
    if len(p) != len(q):
        raise InterpretationError('Policy action dimensions differ.')
    return sum((abs(x-y) for x, y in zip(p, q)), F(0))/2


@dataclass(frozen=True)
class CostCase:
    observation: str
    hidden_case: str
    costs: tuple[F, ...]


@dataclass(frozen=True)
class FiniteUse:
    scope: str
    revision: str
    unit: str
    actions: tuple[str, ...]
    cases: tuple[CostCase, ...]

    def validate(self) -> None:
        for label in (self.scope, self.revision, self.unit, *self.actions):
            if not isinstance(label, str) or not label:
                raise InterpretationError('Scopes, units and action/version identifiers must be named.')
        if not self.actions or len(set(self.actions)) != len(self.actions) or not self.cases:
            raise InterpretationError('Nonempty distinct actions and nonempty cases required.')
        keys = set()
        for case in self.cases:
            if not isinstance(case.observation, str) or not case.observation or not isinstance(case.hidden_case, str) or not case.hidden_case:
                raise InterpretationError('Observation and hidden-case labels must be named.')
            key = case.observation, case.hidden_case
            if key in keys:
                raise InterpretationError('Duplicate observation/case interpretation.')
            keys.add(key)
            if len(vector(case.costs)) != len(self.actions):
                raise InterpretationError('Every available action needs a cost in every case.')

    def policies(self, policy: Mapping[str, Sequence[int | F]]) -> dict[str, tuple[F, ...]]:
        self.validate()
        observations = {c.observation for c in self.cases}
        if set(policy) != observations:
            raise InterpretationError('Policy keys must be exactly the available observations, not hidden cases.')
        result = {o: lottery(ws) for o, ws in policy.items()}
        if any(len(ws) != len(self.actions) for ws in result.values()):
            raise InterpretationError('A policy must cover the same complete action list.')
        return result

    def changes(self, new: Mapping[str, Sequence[int | F]], old: Mapping[str, Sequence[int | F]],
                *, scope: str, revision: str, unit: str) -> tuple[F, ...]:
        if (scope, revision, unit) != (self.scope, self.revision, self.unit):
            raise InterpretationError('Stale or incompatible scope/revision/unit.')
        p, q = self.policies(new), self.policies(old)
        return tuple(contrast(c.costs, p[c.observation], q[c.observation]) for c in self.cases)

    def observation_bounds(self, new: Mapping[str, Sequence[int | F]], old: Mapping[str, Sequence[int | F]]) -> dict[str, F]:
        ds = self.changes(new, old, scope=self.scope, revision=self.revision, unit=self.unit)
        return {o: max(d for c, d in zip(self.cases, ds) if c.observation == o)
                for o in sorted({c.observation for c in self.cases})}


def failure(p: int | F, s: int | F, r: int | F) -> F:
    p, s, r = probability(p), probability(s), probability(r)
    return (1-r)*p+r*s


def controller_cost(p: int | F, s: int | F, r: int | F, charge: int | F) -> F:
    charge = exact(charge)
    if charge < 0:
        raise InterpretationError('This example uses a nonnegative branch charge.')
    return failure(p, s, r)+probability(r)*charge


def execution_rows(p: int | F, s: int | F, r: int | F, charge: int | F) -> tuple[tuple[F, F, F], ...]:
    p, s, r = probability(p), probability(s), probability(r)
    charge = exact(charge)
    if charge < 0:
        raise InterpretationError('Negative branch charge not in this example.')
    # Each row: probability, failure indicator, cost; branch coin independent
    # of its outcome under the declared conditional execution law.
    return ((r*s, F(1), 1+charge), (r*(1-s), F(0), charge),
            ((1-r)*p, F(1), F(1)), ((1-r)*(1-p), F(0), F(0)))


def report_audit(p: int | F, s: int | F, reports: Sequence[int | F], weights: Sequence[int | F]) -> dict[str, F | bool]:
    reports = tuple(probability(r) for r in reports)
    weights = lottery(weights)
    if len(reports) != len(weights):
        raise InterpretationError('Report/weight dimensions differ.')
    hs = tuple(failure(p, s, r) for r in reports)
    excess = tuple(h-r for h, r in zip(hs, reports))
    mean_excess = dot(weights, excess)
    positive = dot(weights, tuple(max(F(0), e) for e in excess))
    return {'mean_excess': mean_excess, 'clipped_mean': max(F(0), mean_excess),
            'mean_positive_shortfall': positive,
            'every_emitted_report_valid': all(w == 0 or e <= 0 for w, e in zip(weights, excess))}


def brier(p: int | F, s: int | F, r: int | F) -> F:
    r = probability(r)
    h = failure(p, s, r)
    return h*(1-r)**2+(1-h)*r**2


def finite_update(points: Sequence[tuple[F, F]], upper: int | F) -> tuple[F, ...]:
    upper = exact(upper)
    if not points:
        raise InterpretationError('No empty source interpretation.')
    selected = tuple(sorted({exact(d) for d, y in points if exact(y) <= upper}))
    if not selected:
        raise InterpretationError('Update leaves no feasible point; not a zero bound.')
    return selected


def lower_fibre(points: Sequence[tuple[F, F]]) -> dict[F, F]:
    if not points:
        raise InterpretationError('No empty source interpretation.')
    out: dict[F, F] = {}
    for d, y in points:
        d, y = exact(d), exact(y)
        out[d] = min(out.get(d, y), y)
    return out


def log_loss(m: float) -> float:
    # Stable finite binary64 reference, not a native logarithm or proof oracle.
    return max(0.0, -m)+math.log1p(math.exp(-abs(m)))


def softmax_loss(z: Sequence[float], label: int) -> float:
    top = max(z)
    return top-z[label]+math.log(sum(math.exp(x-top) for x in z))


def swapped(revealed: bool = False) -> FiniteUse:
    return FiniteUse('swapped-actions-v1', 'evidence-v1', 'U', ('A@1', 'B@1', 'ref@1'),
                     (CostCase('left' if revealed else 'blind', 'left', (F(0), F(2), F(0))),
                      CostCase('right' if revealed else 'blind', 'right', (F(2), F(0), F(0)))))


class F05ObservationTests(unittest.TestCase):
    def test_relative_cost_exact_for_all_test_lotteries(self):
        policies = [(F(i, 4), F(j, 4), F(4-i-j, 4)) for i in range(5) for j in range(5-i)]
        for p, q in product(policies, repeat=2):
            for z in (-10**60, 0, 10**60):
                costs = (F(z), F(z+2), F(z-1))
                self.assertEqual(contrast(costs, p, q), contrast(relative(costs), p, q))

    def test_marginals_do_not_determine_joint_relative_image(self):
        diagonal = ((0, 0), (2, 2)); antidiagonal = ((0, 2), (2, 0))
        self.assertEqual([{x[i] for x in diagonal} for i in (0, 1)], [{x[i] for x in antidiagonal} for i in (0, 1)])
        self.assertEqual({relative(x) for x in diagonal}, {(F(0), F(0))})
        self.assertEqual({relative(x)[1] for x in antidiagonal}, {F(-2), F(2)})

    def test_baseline_needed_for_different_exposure(self):
        vals = []
        for z in (0, 2):
            self.assertEqual(relative((z, z+1)), (0, 1))
            vals.append(2*z-(z+1))
        self.assertEqual(vals, [-1, 1])

    def test_span_ignores_unbounded_common_error(self):
        p, q = (F(1, 4), F(3, 4), F(0)), (F(0), F(1), F(0))
        for z in (-10**100, 0, 10**100):
            e = (F(z)+F(1,4), F(z)-F(1,8), F(z))
            self.assertEqual(span(e), F(3,8))
            self.assertEqual(abs(contrast(e, p, q)), F(3,32))
            self.assertEqual(total_variation(p, q)*span(e), F(3,32))

    def test_span_bound_exhaustive_small_errors_and_lotteries(self):
        policies = [(F(i,2), F(j,2), F(2-i-j,2)) for i in range(3) for j in range(3-i)]
        for e in product((-1, 0, 1), repeat=3):
            for p, q in product(policies, repeat=2):
                self.assertLessEqual(abs(contrast(e, p, q)), total_variation(p, q)*span(e))

    def test_optimal_center_and_sharp_pure_action_contrast(self):
        for e in product((-2, 0, 3), repeat=3):
            center = F(max(e)+min(e), 2)
            self.assertEqual(max(abs(exact(x)-center) for x in e), span(e)/2)
            p = tuple(F(i == e.index(max(e))) for i in range(3))
            q = tuple(F(i == e.index(min(e))) for i in range(3))
            self.assertEqual(contrast(e, p, q), span(e))

    def test_unnormalized_and_inexact_policies_rejected(self):
        for p in ((F(1,2), 0), (-1, 2), (0.5, 0.5), (True, 0), ()):
            with self.assertRaises(InterpretationError): lottery(p)
        self.assertEqual(dot((F(1,2), -1), (10,10)), -5)
        self.assertEqual(span((10,10)), 0)

    def test_blind_and_revealed_use_differ(self):
        blind, known = swapped(), swapped(True)
        old = {'blind': (0,0,1)}
        trial = [max(blind.observation_bounds({'blind': (F(i,4), 1-F(i,4), 0)}, old).values()) for i in range(5)]
        self.assertEqual(min(trial), 1)
        self.assertEqual(known.observation_bounds({'left':(1,0,0),'right':(0,1,0)}, {'left':(0,0,1),'right':(0,0,1)}), {'left':0,'right':0})
        self.assertEqual({c.costs for c in blind.cases}, {c.costs for c in known.cases})

    def test_hidden_case_policy_keys_rejected(self):
        with self.assertRaises(InterpretationError):
            swapped().policies({'left': (1,0,0), 'right': (0,1,0)})

    def test_missing_interpretation_and_duplicate_case_rejected(self):
        m = swapped()
        for cases in ((), (CostCase('blind','x',(F(0),)),), (m.cases[0],m.cases[0])):
            with self.assertRaises(InterpretationError):
                FiniteUse(m.scope,m.revision,m.unit,m.actions,cases).validate()

    def test_malformed_program_names_and_policy_width_rejected(self):
        m = swapped()
        for actions in (('A','A','ref'), ('A','','ref')):
            with self.assertRaises(InterpretationError): FiniteUse(m.scope,m.revision,m.unit,actions,m.cases).validate()
        with self.assertRaises(InterpretationError): m.policies({'blind':(1,0)})
        with self.assertRaises(InterpretationError): m.policies({'blind':(1,0,0),'extra':(1,0,0)})

    def test_stale_scope_revision_and_units_rejected(self):
        m = swapped(); p={'blind':(1,0,0)}; q={'blind':(0,0,1)}
        for scope,rev,unit in (('other',m.revision,m.unit),(m.scope,'v2',m.unit),(m.scope,m.revision,'seconds')):
            with self.assertRaises(InterpretationError): m.changes(p,q,scope=scope,revision=rev,unit=unit)

    def test_paid_information_and_observation_specific_budgets(self):
        self.assertGreater(F(0)+2, F(1))  # Known-case free cost + observation charge versus blind mixed cost.
        m=FiniteUse('table','v1','U',('old','new'),(CostCase('o1','h',(F(0),F(-2))),CostCase('o2','h',(F(0),F(1)))))
        ds=m.observation_bounds({'o1':(0,1),'o2':(0,1)}, {'o1':(1,0),'o2':(1,0)})
        self.assertEqual(ds,{'o1':-2,'o2':1}); self.assertEqual(max(ds.values()),1)
        self.assertLess(F(1,2)*sum(ds.values()),0)  # An average would answer a different question.

    def test_convex_hull_can_change_nonlinear_query(self):
        endpoints=((F(0),F(2)),(F(2),F(0)))
        self.assertEqual(max(min(x) for x in endpoints),0)
        self.assertEqual(min((F(1),F(1))),1)

    def test_same_projection_different_nonempty_updates(self):
        c1=((F(0),F(0)),(F(2),F(1))); c2=((F(0),F(1)),(F(2),F(0)))
        self.assertEqual({x for x,y in c1},{x for x,y in c2})
        self.assertEqual(finite_update(c1,0),(F(0),)); self.assertEqual(finite_update(c2,0),(F(2),))

    def test_saturated_update_commutes_for_all_small_subsets(self):
        universe=list(product((F(0),F(1)),repeat=2))
        for mask in range(1,16):
            points=[p for i,p in enumerate(universe) if mask>>i&1]
            projected={d for d,y in points}
            for cap in (-1,0,1):
                self.assertEqual({d for d,y in points if d<=cap}, {d for d in projected if d<=cap})

    def test_empty_update_not_a_zero_cost_certificate(self):
        with self.assertRaises(InterpretationError): finite_update(((F(0),F(2)),),1)

    def test_two_cuts_break_initial_convex_summary(self):
        # Extrema occur at these endpoints of the surviving top/right half-edges.
        boundary=((F(1,2),F(1)),(F(1),F(1,2)),(F(1),F(1)))
        naive=(*boundary,(F(1,2),F(1,2)))
        self.assertEqual(max(-sum(p) for p in boundary),F(-3,2))
        self.assertEqual(max(-sum(p) for p in naive),-1)
        self.assertEqual(max(-sum(p)/2 for p in boundary),F(-3,4))
        self.assertEqual(max(-sum(p)/2 for p in naive),F(-1,2))

    def test_lower_fibre_exact_for_upper_cuts(self):
        points=((F(-1),F(1)),(F(-1),F(3)),(F(0),F(0)),(F(1),F(1)),(F(2),F(2)))
        a=lower_fibre(points)
        for c in (0,1,2,3):
            self.assertEqual(finite_update(points,c),tuple(sorted(d for d,y in a.items() if y<=c)))
        self.assertEqual(a,{-1:1,0:0,1:1,2:2})

    def test_fibre_endpoints_insufficient_for_an_interior_cut(self):
        a=(0,2); b=(0,1,2)
        self.assertEqual((min(a),max(a)),(min(b),max(b)))
        self.assertFalse(any(y==1 for y in a)); self.assertTrue(any(y==1 for y in b))

    def test_randomized_report_mean_can_hide_invalid_emitted_report(self):
        a=report_audit(F(1,2),0,(0,1),(F(1,2),F(1,2)))
        self.assertEqual(a['mean_excess'],F(-1,4)); self.assertEqual(a['clipped_mean'],0)
        self.assertEqual(a['mean_positive_shortfall'],F(1,4)); self.assertFalse(a['every_emitted_report_valid'])

    def test_zero_probability_report_has_no_conditional_obligation(self):
        a=report_audit(F(1,2),0,(0,1),(0,1))
        self.assertEqual(a['mean_positive_shortfall'],0); self.assertTrue(a['every_emitted_report_valid'])

    def test_report_shortfall_equivalence_on_finite_grid(self):
        vals=(F(0),F(1,2),F(1))
        for p,s,r1,r2,w in product(vals,repeat=5):
            a=report_audit(p,s,(r1,r2),(w,1-w))
            self.assertEqual(a['mean_positive_shortfall']==0,a['every_emitted_report_valid'])

    def test_report_shortfall_probability_bound_not_error_probability(self):
        weights=(F(1,2),F(1,2)); shortfalls=(F(1,1000),F(0)); eps=dot(weights,shortfalls)
        self.assertEqual(eps,F(1,2000)); self.assertEqual(sum(w for w,e in zip(weights,shortfalls) if e>0),F(1,2))
        for tau in (F(1,10000),F(1,2000),F(1,1000),F(1,100)):
            self.assertLessEqual(sum(w for w,e in zip(weights,shortfalls) if e>tau),eps/tau)

    def test_execution_rows_match_expected_formulas(self):
        vals=(F(0),F(1,2),F(1))
        for p,s,r,k in product(vals,repeat=4):
            rows=execution_rows(p,s,r,k)
            self.assertEqual(sum(w for w,f,c in rows),1)
            self.assertEqual(sum(w*f for w,f,c in rows),failure(p,s,r))
            self.assertEqual(sum(w*c for w,f,c in rows),controller_cost(p,s,r,k))

    def test_invalid_probability_checked_even_in_zero_weight_branch(self):
        for args in ((2,0,1),(0,-1,0),(0,0,2),(0.5,0,1)):
            with self.assertRaises(InterpretationError): failure(*args)
        with self.assertRaises(InterpretationError): report_audit(0,0,(0,1),(1,))
        with self.assertRaises(InterpretationError): controller_cost(0,0,0,-1)

    def test_self_referential_brier_optimum_can_be_invalid(self):
        p,s=F(1),F(1,2); r_bad=F(5,8); r_valid=F(2,3)
        self.assertEqual(failure(p,s,r_bad),F(11,16))
        self.assertEqual(failure(p,s,r_bad)-r_bad,F(1,16))
        self.assertEqual(brier(p,s,r_bad),F(7,32))
        self.assertEqual(brier(p,s,r_valid),F(2,9))
        self.assertEqual(brier(p,s,r_valid)-brier(p,s,r_bad),F(1,288))
        for i in range(33): self.assertGreaterEqual(brier(p,s,F(i,32)),brier(p,s,r_bad))

    def test_fixed_outcome_brier_remains_proper(self):
        h=F(3,4)
        fixed=lambda r: h*(1-r)**2+(1-h)*r**2
        for i in range(17): self.assertGreaterEqual(fixed(F(i,16)),fixed(h))

    def test_shared_source_principal_composition(self):
        for theta in (F(0),F(1,2),F(1)):
            for z1,z2 in ((0,0),(10**60,10**70)):
                old=z1+F(3,4)+z2+theta; new=z1+theta+z2+F(1,4)
                self.assertEqual(new-old,F(-1,2))
        self.assertEqual(1-F(3,4)+F(1,4)-0,F(1,2))  # Unrelated source copies.

    def test_reflective_principal_pair_and_source_weakening(self):
        for beta in (F(1,32),F(3,64)):
            vals=[]
            for s,e in product((F(0),F(1,4)),(-beta,beta)):
                p=s+F(1,2)
                self.assertLessEqual(failure(p,s,F(1,2)),F(1,2))
                self.assertLessEqual(failure(p,s,F(3,4)),F(3,4))
                vals.append(controller_cost(p,s,F(3,4),F(1,4))-controller_cost(p,s,F(1,2),F(1,4))+e)
            self.assertEqual(max(vals),F(-1,16)+beta)

    def test_compact_reflective_source_has_explicit_lift(self):
        for d,u in product((F(-3,32),F(-1,32)),(F(-1,4),F(0))):
            e=d+F(1,16); s=u+F(1,4); p=s+F(1,2)
            self.assertTrue(F(-1,32)<=e<=F(1,32))
            self.assertTrue(0<=s<=F(1,4))
            self.assertEqual(failure(p,s,F(1,2))-F(1,2),u)
            self.assertEqual(failure(p,s,F(3,4))-F(3,4),u-F(3,8))
            self.assertEqual(controller_cost(p,s,F(3,4),F(1,4))-controller_cost(p,s,F(1,2),F(1,4))+e,d)

    def test_adaptive_visible_report_cost_and_failure_move_oppositely(self):
        old=F(1,2); new=F(5,12); charge=F(3,4)
        for s in (F(0),F(1,8)):
            p=s+F(1,2)
            self.assertLessEqual(failure(p,s,new),new)
            self.assertEqual(failure(p,s,new)-failure(p,s,old),F(1,24))
            self.assertEqual((new-old)*charge,F(-1,16))
            self.assertEqual(controller_cost(p,s,new,charge)-controller_cost(p,s,old,charge),F(-1,48))
        self.assertEqual(F(-1,48)+F(1,96),F(-1,96))

    def test_reused_random_seed_invalidates_standalone_mixture(self):
        # A(U)=1[U=0], B(U)=1[U=1]; select A at U=0, B at U=1.
        reused=sum(F(int((u==0 and u==0) or (u==1 and u==1)),2) for u in (0,1))
        fresh=sum(F(int((u==0 and v==0) or (u==1 and v==1)),4) for u,v in product((0,1),repeat=2))
        self.assertEqual(reused,1); self.assertEqual(fresh,F(1,2))

    def test_quadratic_chord_and_refinement_gap(self):
        for i in range(17):
            theta=F(1,4)+F(i,32); upper=theta-F(3,16)
            self.assertGreaterEqual(upper,theta**2)
        theta=F(1,2); self.assertEqual(theta**2-theta,F(-1,4))
        self.assertEqual(theta-F(3,16),F(5,16))
        self.assertLess(F(-1,4),F(-7,32)); self.assertGreater(F(-3,16),F(-7,32))

    def test_native_absolute_error_example(self):
        from v2.checks.f05_semantics import Signature,src,add,sub,absolute,evaluate,num
        sig=Signature('MAE-v1',('U',),(('y','U'),('z','U'),('c','U')))
        expression=sub(add(add(absolute(sub(src('y'),num(1))),src('c')),src('z')),add(absolute(src('y')),src('z')))
        for y,c,z in product((F(3,4),F(1),F(2),F(10**30)),(F(0),F(1,4)),(F(0),F(10**40))):
            self.assertLessEqual(evaluate(expression,sig,{'y':y,'c':c,'z':z}),F(-1,4))

    def test_rational_log_loss_enclosure_expression(self):
        from v2.checks.f05_semantics import Signature,src,add,sub,residual,evaluate,num
        sig=Signature('log-adapter-v1',('U',),(('m','U'),('ro','U'),('rn','U'),('z','U')))
        h_old=residual(src('m'),num(0)); h_new=residual(add(src('m'),num(1)),num(0))
        old=add(add(h_old,src('ro')),src('z'))
        new=add(add(add(h_new,src('rn')),num(F(1,8))),src('z'))
        for m,ro,rn,z in product((F(-1),F(-2),F(-10**30)),(F(0),F(3,4)),(F(0),F(3,4)),(F(0),F(10**40))):
            self.assertLessEqual(evaluate(sub(new,old),sig,{'m':m,'ro':ro,'rn':rn,'z':z}),F(-1,8))
        self.assertEqual(-1+F(3,4)+F(1,8),F(-1,8))

    def test_log_adapter_numerical_reference(self):
        for m in (-1000.,-10.,-2.,-1.,0.,1.,2.,10.,1000.):
            rem=log_loss(m)-max(0.,-m)
            self.assertGreaterEqual(rem,-1e-12); self.assertLessEqual(rem,.75+1e-12)
        for m in (-1000.,-10.,-2.,-1.):
            self.assertLessEqual(log_loss(m+1)-log_loss(m)+.125,-.125+1e-12)

    def test_log_adapter_domain_and_uniform_margin_boundaries(self):
        # Outside m<=-1, the added charge can exceed the small gain.
        self.assertGreater(log_loss(20.)-log_loss(19.)+.125,0)
        ds=[log_loss(x+1)-log_loss(x) for x in (0.,5.,10.,20.)]
        self.assertTrue(all(d<0 for d in ds)); self.assertGreater(ds[-1],-1e-8)
        for m in (-2.,0.,2.):
            if m < 1:
                self.assertNotEqual(max(0.,1-m),max(0.,-m))

    def test_multiclass_common_shift_and_span_reference(self):
        zs=((-2.,0.,1.),(1000.,999.,998.),(-1000.,-1001.,-999.))
        for z,y in product(zs,range(3)):
            ell=softmax_loss(z,y); h=max(z)-z[y]
            self.assertGreaterEqual(ell-h,-1e-12); self.assertLessEqual(ell-h,math.log(3)+1e-12)
            self.assertAlmostEqual(softmax_loss(tuple(x+10000 for x in z),y),ell,places=10)
            e=(.25,-.125,0.)
            diff=softmax_loss(tuple(a+b for a,b in zip(z,e)),y)-ell
            self.assertGreaterEqual(diff,min(e)-e[y]-1e-12); self.assertLessEqual(diff,max(e)-e[y]+1e-12)

    def test_clipping_separate_suprema_loses_strict_improvement(self):
        first=(-3,-1); second=(-3,0)
        summaries=lambda xs:(max(max(x,0) for x in xs),max(max(-x,0) for x in xs))
        self.assertEqual(summaries(first),summaries(second)); self.assertNotEqual(max(first),max(second))
        for d in (*first,*second): self.assertEqual(max(d,0)-max(-d,0),d)

    def test_latent_decomposition_is_not_blind_constant_allocation(self):
        worlds=((1,0,1),(0,1,1))
        for a,b,c in worlds:
            c1=min(c,a); c2=c-c1
            self.assertTrue(0<=c1<=a and 0<=c2<=b)
        feasible=[]
        for c1 in (F(0),F(1,2),F(1)):
            if all(c1<=a and 1-c1<=b for a,b,c in worlds): feasible.append(c1)
        self.assertEqual(feasible,[])

    def test_marginal_coverage_not_conditional_on_every_observation(self):
        covered=(True,False); probabilities=(F(9,10),F(1,10))
        self.assertEqual(sum(p for p,c in zip(probabilities,covered) if c),F(9,10))
        self.assertEqual(F(0)/probabilities[1],0)


def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [serial(v) for v in x]
    return x


def report() -> dict:
    return serial({
        'scope':'F05 finite interpretation regressions; analytic generalizations remain in the proof note',
        'relative_example': {'uniform_span_error':F(3,8),'quarter_mass_contrast_error':F(3,32)},
        'report_wrapper':report_audit(F(1,2),0,(0,1),(F(1,2),F(1,2))),
        'performative_brier':{'optimal_report':F(5,8),'failure':F(11,16),'positive_shortfall':F(1,16),
                             'brier_loss':F(7,32),'valid_report':F(2,3),'valid_brier_loss':F(2,9),'loss_gap':F(1,288)},
        'adaptive_controller':{'charge':F(3,4),'old_report':F(1,2),'new_report':F(5,12),'failure_change':F(1,24),
                               'cost_change':F(-1,48),'intended_cost_bound':F(-1,96)},
        'principal_interpretations':{'shared_cost_change':F(-1,2),'reflective_intended_bound':F(-1,32),
                                     'weakened_bound':F(-1,64),'quadratic_bound':F(-3,16)},
        'log_adapter':{'rational_remainder_cap':F(3,4),'resource_charge':F(1,8),'cost_change_bound':F(-1,8),
                       'scope':'m<=-1; fixed one-unit signed margin shift; no logarithm primitive or trained network'},
        'two_cut_update':{'exact_mixture_bound':F(-3,4),'premature_convex_bound':F(-1,2)},
        'enumeration':{'relative_lottery_cases':675,'span_error_cases':972,'report_wrapper_cases':243,'execution_laws':81},
        'numerical_log_checks':'binary64 reference at explicitly listed inputs; not an interval certificate',
        'not_claimed':['universal decision procedure','F06 proof rules','F07 soundness','neural training','causal discovery','full repository CI']})


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F05ObservationTests))
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
