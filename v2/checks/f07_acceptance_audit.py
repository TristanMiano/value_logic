"""F07 paired-difference envelopes and full-pipeline acceptance checks.

Research author: ChatGPT (GPT-6 Astra Pro), 2026-09-28.
These are exact finite audits, not new kernel rules or empirical moment tests.
The normalized-form dependency is the unchanged, separately audited F06 kernel.
Moment and coordinate-error bounds supplied by a caller remain external premises.
Python 3.10+; standard library only.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
from typing import Mapping
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f06_residual_discharge as S
from v2.checks import f06_derived_cases as D
from v2.checks import f07_soundness as H
from v2.checks import f07_producer_contracts as P
from v2.checks import f07_near_exclusion_receiver as N

AUTHOR = 'ChatGPT (GPT-6 Astra Pro)'


@dataclass(frozen=True)
class DifferenceEnvelope:
    """Computed numeric-coordinate summary, not an untrusted certificate receiver."""
    unit: str
    value_at_zero: F
    source_weights: tuple[tuple[str, F], ...]


def difference_envelope(sig: K.Signature, new: K.Term, old: K.Term) -> DifferenceEnvelope:
    """Construct a sufficient global coordinatewise Lipschitz envelope of new-old.

    Normalize the paired difference first so exact shared atoms cancel. The
    returned coefficients need not be smallest, and zero is not assumed feasible.
    This function does not assert that a comparison is valid in any context.
    """
    sig.validate()
    unit = K.infer(new, sig)
    if K.infer(old, sig) != unit:
        raise H.AuditError('A paired difference requires the same declared unit.')
    names = tuple(name for name, _ in sig.sources)
    index = {name: i for i, name in enumerate(names)}
    zero = (F(0),) * len(names)

    @lru_cache(maxsize=None)
    def form_weights(form):
        result = list(zero)
        for atom, coefficient in form[0]:
            weight = atom_weights(atom)
            for i, value in enumerate(weight):
                result[i] += abs(H.exact(coefficient)) * value
        return tuple(result)

    @lru_cache(maxsize=None)
    def atom_weights(atom):
        if atom[0] == 'source':
            result = list(zero)
            result[index[atom[1]]] = F(1)
            return tuple(result)
        if atom[0] not in ('min', 'max'):
            raise H.AuditError('Unexpected atom from the fixed native normalizer.')
        left, right = form_weights(atom[1]), form_weights(atom[2])
        return tuple(max(a, b) for a, b in zip(left, right))

    normalized = K._form(K.sub(new, old), sig)
    weights = form_weights(normalized)
    origin = {name: F(0) for name in names}
    # Independent recursive denotation, not the algebraic collector, at zero.
    value_at_zero = H.value(new, sig, origin) - H.value(old, sig, origin)
    return DifferenceEnvelope(unit, value_at_zero,
                              tuple((name, value) for name, value in zip(names, weights) if value))


def _weighted_bound(envelope: DifferenceEnvelope, supplied: Mapping[str, int | F]) -> F:
    expected = {name for name, _ in envelope.source_weights}
    if set(supplied) != expected:
        raise H.AuditError('Supply exactly the coordinates with nonzero envelope weights.')
    values = {name: H.exact(value) for name, value in supplied.items()}
    if any(value < 0 for value in values.values()):
        raise H.AuditError('Absolute moment/error upper bounds must be nonnegative.')
    return sum((weight * values[name] for name, weight in envelope.source_weights), F(0))


def absolute_mean_ceiling(sig: K.Signature, new: K.Term, old: K.Term,
                          moments: Mapping[str, int | F]) -> F:
    """Sufficient E|new-old| ceiling IF supplied first absolute moments are valid.

    Recompute the envelope from the supplied expression pair; do not trust an
    externally constructed DifferenceEnvelope. No distribution is inferred.
    """
    envelope = difference_envelope(sig, new, old)
    return abs(envelope.value_at_zero) + _weighted_bound(envelope, moments)


def perturbation_allowance(sig: K.Signature, new: K.Term, old: K.Term,
                           errors: Mapping[str, int | F]) -> F:
    """Bound paired-difference drift under the explicitly supplied coordinate errors."""
    return _weighted_bound(difference_envelope(sig, new, old), errors)


def expression_catalogue():
    """A fixed declared finite syntax sample, not exhaustive over native terms."""
    x, y, z = map(K.src, ('x', 'y', 'z'))
    terms = [K.num(0), K.num(F(-3, 2)), x, K.scale(-2, y),
             K.add(x, y), K.sub(x, x), K.maximum(x, y), K.minimum(x, y),
             K.residual(x, y), K.residual(z, K.add(z, x)),
             K.sub(K.maximum(K.add(z, x), K.add(z, y)), z),
             K.add(K.maximum(K.sub(x, y), K.num(F(1, 3))), K.scale(-3, z)),
             K.let('u', K.add(x, z), K.sub(K.loc('u'), z)),
             K.let('u', x, K.let('u', K.add(K.loc('u'), y), K.scale(-1, K.loc('u')))),
             K.minimum(K.scale(-2, K.maximum(x, K.num(0))), K.add(y, z))]
    sig = K.Signature('F07-S4-envelope-v1', ('U',), tuple((name, 'U') for name in ('x','y','z')))
    return sig, tuple(terms)


class F07AcceptanceTests(unittest.TestCase):
    def test_fixed_report_certificate_cannot_be_reused_after_update(self):
        ctx, _, _, _ = N.paired_policy_fixture()
        p, s = K.src('p'), K.src('s')
        for r, expected in ((F(3,4), F(-5,16)), (F(7,16), F(15,64)), (F(4,7), F(0))):
            with self.subTest(report=r):
                h = K.add(K.scale(1-r, p), K.scale(r, s))
                b = K.Builder(ctx, 'h')
                i = b.add(b.scale(1-r, b.row(1)), b.scale(r, b.row(3)))
                i = b.add(i, b.constant(K.num(-r, 'P'), K.num(0, 'P')))
                b.rewrite(i, h, K.num(r, 'P'))
                proof = b.proof()
                root = H.receive(ctx, proof, H.request(ctx, 'h', h, K.num(r, 'P'), expected, 'P'))
                self.assertEqual(root.budget, expected)
                point = dict(p=F(1), s=F(1,4), e=F(0), z=F(0))
                self.assertTrue(H.case_feasible(ctx, 'h', point))
                self.assertEqual(H.value(h, ctx.signature, point)-r, expected)
                if r == F(7,16):
                    with self.assertRaises(H.AuditError):
                        H.receive(ctx, proof, H.request(ctx, 'h', h, K.num(r, 'P'), 0, 'P'))

    def test_naive_report_update_can_raise_modeled_cost(self):
        first = P.reflective_rates(1, F(1,4), F(3,4), F(7,16), cost=F(1,4))
        self.assertEqual(first['old_failure'], F(7,16))
        self.assertEqual(first['new_failure'], F(43,64))
        self.assertEqual(first['report_overrun'], F(15,64))
        self.assertEqual(first['paired_change'], F(5,32))

    def test_calibration_cost_is_a_separate_declared_criterion(self):
        def criterion(r, weight):
            risk = 1-F(3,4)*r
            return risk+r/4+weight*abs(risk-r)
        old, calibrated = F(3,4), F(4,7)
        self.assertEqual(criterion(calibrated,0)-criterion(old,0), F(5,56))
        self.assertEqual(criterion(calibrated,F(1,2))-criterion(old,F(1,2)), F(-15,224))
        for r in (F(4,7), F(3,4), F(1)):
            self.assertEqual(criterion(r,F(2,7)), F(5,7))

    def test_constant_has_no_moment_obligation(self):
        sig, _ = expression_catalogue()
        e = difference_envelope(sig, K.num(-7), K.num(2))
        self.assertEqual((e.value_at_zero, e.source_weights), (F(-9), ()))
        self.assertEqual(absolute_mean_ceiling(sig, K.num(-7), K.num(2), {}), 9)

    def test_common_unbounded_baseline_cancels(self):
        sig, _ = expression_catalogue(); x, z = K.src('x'), K.src('z')
        e = difference_envelope(sig, K.add(z, K.scale(F(-2,3), x)), z)
        self.assertEqual(e.source_weights, (('x', F(2,3)),))
        self.assertEqual(absolute_mean_ceiling(sig, K.add(z, x), z, {'x': 3}), 3)

    def test_residual_pre_activation_cancellation(self):
        sig, _ = expression_catalogue(); x, z = K.src('x'), K.src('z')
        e = difference_envelope(sig, K.residual(z, K.add(z, x)), K.num(0))
        self.assertEqual(e, DifferenceEnvelope('U', F(0), (('x', F(1)),)))

    def test_same_nonlinear_atom_cancels(self):
        sig, _ = expression_catalogue(); m = K.maximum(K.src('x'), K.src('y'))
        e = difference_envelope(sig, K.add(m, K.src('z')), m)
        self.assertEqual(e.source_weights, (('z', F(1)),))

    def test_negative_scaling_changes_weights_not_their_sign(self):
        sig, _ = expression_catalogue()
        e = difference_envelope(sig, K.scale(-3, K.maximum(K.src('x'), K.src('y'))), K.num(0))
        self.assertEqual(e.source_weights, (('x', F(3)), ('y', F(3))))

    def test_lexical_shadowing_and_source_identity(self):
        sig, _ = expression_catalogue()
        term = K.let('x', K.src('y'), K.let('x', K.add(K.loc('x'), K.src('z')), K.sub(K.loc('x'), K.src('y'))))
        self.assertEqual(difference_envelope(sig, term, K.num(0)).source_weights, (('z', F(1)),))

    def test_positive_named_conversion(self):
        sig = K.Signature('F07-S4-priced', ('P','J'), (('p','P'),),
                          (K.Conversion('price', 'P', 'J', F(7,2)),))
        e = difference_envelope(sig, K.convert('price', K.src('p')), K.num(0,'J'))
        self.assertEqual(e, DifferenceEnvelope('J', F(0), (('p', F(7,2)),)))

    def test_mixed_units_rejected(self):
        sig = K.Signature('F07-S4-units', ('P','J'), (('p','P'),))
        with self.assertRaises(H.AuditError): difference_envelope(sig, K.src('p'), K.num(0,'J'))

    def test_inexact_or_unbound_term_rejected(self):
        sig, _ = expression_catalogue()
        for term in (K.Term('const', unit='U', value=0.5), K.loc('free')):
            with self.subTest(term=term):
                with self.assertRaises(K.SemanticError): difference_envelope(sig, term, K.num(0))

    def test_moment_input_is_exact_and_nonnegative(self):
        sig, _ = expression_catalogue()
        for value in (True, 0.5, F(-1), float('inf')):
            with self.subTest(value=value):
                with self.assertRaises(H.AuditError): absolute_mean_ceiling(sig, K.src('x'), K.num(0), {'x':value})

    def test_missing_or_extra_moment_coordinate_rejected(self):
        sig, _ = expression_catalogue()
        for moments in ({}, {'x':1,'z':1}, {'y':1}):
            with self.subTest(moments=moments):
                with self.assertRaises(H.AuditError): absolute_mean_ceiling(sig, K.src('x'), K.num(0), moments)

    def test_zero_point_need_not_be_feasible(self):
        x = K.src('x'); c = K.context(('x',), (K.Row(K.num(2), x),), {'x':2})
        self.assertFalse(H.case_feasible(c, 'h', {'x':0}))
        self.assertEqual(difference_envelope(c.signature, K.sub(x,K.num(2)), K.num(0)).value_at_zero, -2)

    def test_envelope_not_claimed_minimal(self):
        sig, _ = expression_catalogue(); x,y,z=map(K.src,('x','y','z'))
        a=K.sub(K.maximum(K.add(z,x),K.add(z,y)),z); b=K.maximum(x,y)
        self.assertIn('z', dict(difference_envelope(sig,a,K.num(0)).source_weights))
        self.assertNotIn('z', dict(difference_envelope(sig,b,K.num(0)).source_weights))
        for vx,vy,vz in product((F(-7),F(0),F(11)),repeat=3):
            point=dict(x=vx,y=vy,z=vz)
            self.assertEqual(H.value(a,sig,point),H.value(b,sig,point))

    def test_finite_lipschitz_and_growth_probe(self):
        sig, terms = expression_catalogue()
        points = [dict(zip(('x','y','z'), p)) for p in product((F(-2),F(0),F(3,2)),repeat=3)]
        # 15 terms x 27 x 27 pairs; this finite probe is not the general proof.
        for term in terms:
            e=difference_envelope(sig,term,K.num(0)); weights=dict(e.source_weights)
            values=[H.value(term,sig,p) for p in points]
            for p,v in zip(points,values):
                self.assertLessEqual(abs(v),abs(e.value_at_zero)+sum((w*abs(p[k]) for k,w in weights.items()),F(0)))
            for i,p in enumerate(points):
                for j,q in enumerate(points):
                    self.assertLessEqual(abs(values[i]-values[j]),sum((w*abs(p[k]-q[k]) for k,w in weights.items()),F(0)))

    def test_large_finite_coordinates_not_clipped(self):
        sig, terms = expression_catalogue(); p=dict(x=F(10**30),y=F(-10**25),z=F(10**40))
        for term in terms:
            e=difference_envelope(sig,term,K.num(0))
            upper=abs(e.value_at_zero)+sum((w*abs(p[k]) for k,w in e.source_weights),F(0))
            self.assertLessEqual(abs(H.value(term,sig,p)),upper)

    def test_paired_policy_has_no_baseline_moment(self):
        c,a,g,r=N.paired_policy_fixture()
        e=difference_envelope(c.signature,r.new,r.old)
        self.assertEqual(e.value_at_zero,F(1,16))
        self.assertEqual(dict(e.source_weights),dict(p=F(1,4),s=F(1,4),e=F(1)))
        self.assertEqual(absolute_mean_ceiling(c.signature,r.new,r.old,dict(p=1,s=1,e=F(1,32))),F(19,32))
        H.receive(c,N.receive_near_exclusion(c,a,g,replace(r,budget=F(0)),strict=True),r)

    def test_perturbed_policy_threshold_is_attained(self):
        c,a,g,r=N.paired_policy_fixture(); original=dict(p=F(7,16),s=F(0),e=F(1,32),z=F(10**20))
        self.assertTrue(H.case_feasible(c,'h',original))
        for eps in (F(0),F(1,64),F(1,32),F(1,16)):
            current=dict(original,p=original['p']-eps,s=eps)
            slack=perturbation_allowance(c.signature,r.new,r.old,dict(p=eps,s=eps,e=0))
            change=H.value(r.new,c.signature,current)-H.value(r.old,c.signature,current)
            self.assertEqual(change,r.budget+slack)
            self.assertEqual(change<0,eps<F(1,32))

    def test_current_pair_not_historical_baseline_drift(self):
        sig, _=expression_catalogue(); z=K.src('z'); new=K.sub(z,K.num(1)); old=z
        self.assertEqual(difference_envelope(sig,new,old).source_weights,())
        p=dict(x=0,y=0,z=0); q=dict(x=0,y=0,z=100)
        self.assertEqual(H.value(new,sig,q)-H.value(old,sig,q),-1)
        self.assertEqual(H.value(new,sig,q)-H.value(old,sig,p),99)

    def test_finite_heavy_tail_truncations_cancel_pointwise(self):
        # Unbounded limiting absolute means are justified in the written proof,
        # not established by this finite family of exact truncations.
        for n in (2,8,32):
            mass=[F(1,2**i) for i in range(1,n+1)]
            mass[-1]+=F(1,2**n)
            z=[F(2**i) for i in range(1,n+1)]
            self.assertEqual(sum(mass,F(0)),1)
            self.assertEqual(sum((p*((v-1)-v) for p,v in zip(mass,z)),F(0)),-1)
            self.assertEqual(sum((p*v for p,v in zip(mass,z)),F(0)),n+1)

    def test_complete_producer_serialization_and_receiver(self):
        c,a,g,r=N.paired_policy_fixture(); out=N.receive_near_exclusion(c,a,g,replace(r,budget=F(0)),strict=True)
        decoded=D.unpack_proof(c,D.pack_proof(out))
        self.assertEqual(H.receive(c,decoded,r),H.receive(c,out,r))

    def test_transport_global_root_requires_explicit_localization(self):
        c,p=T.alternative_example()
        current,transported=T.restrict_rows(c,p,frozenset({('h',1)}))
        root=K.check(current,transported)
        self.assertIsNone(root.case)
        local_request=H.request(current,'h',root.new,root.old,root.budget)
        with self.assertRaises(H.AuditError): H.receive(current,transported,local_request)
        H.receive(current,T.localize(current,transported,'h'),local_request)

    def test_softening_penalty_field_is_not_authenticated_by_trace_alone(self):
        c,p=T.alternative_example(); out=S.soften_rows(c,p,'h',(0,1),revision='S4-withdraw')
        P.receive_softening(c,p,'h',(0,1),'S4-withdraw',out)
        forged=replace(out,penalty=K.num(0))
        K.check(forged.context,forged.proof)
        with self.assertRaises(P.ContractError): P.receive_softening(c,p,'h',(0,1),'S4-withdraw',forged)

    def test_scalar_hinge_bound_not_source_relative_optimum(self):
        c=K.context((),(),{}); raw=K.num(0)
        proof=D.offset_hinge_certificate(c,raw,F(0),F(0),F(0),F(1),F(1),F(1))
        root=K.check(c,proof)
        self.assertEqual(root.budget,1)
        self.assertEqual(H.value(root.new,c.signature,{})-H.value(root.old,c.signature,{}),0)

    def test_strict_at_the_attained_bound_is_rejected(self):
        c,a,g,r=N.paired_policy_fixture()
        point=dict(p=F(7,16),s=0,e=F(1,32),z=0)
        self.assertTrue(H.case_feasible(c,'h',point))
        self.assertEqual(H.value(r.new,c.signature,point)-H.value(r.old,c.signature,point),r.budget)
        with self.assertRaises(H.AuditError): N.receive_near_exclusion(c,a,g,r,strict=True)
        out=N.receive_near_exclusion(c,a,g,replace(r,budget=F(0)),strict=True)
        self.assertLess(K.check(c,out).budget,0)

    def test_ray_adapter_needs_the_actual_unit_conversion(self):
        p=K.src('p')
        c=K.context((('p','P'),),(K.Row(K.scale(-1,p),K.num(-1,'P')),),{'p':1},
                    units=('P','U'),conversions=(K.Conversion('price','P','U',F(2)),))
        guard=K.convert('price',p)
        with self.assertRaises(K.ProofError):
            D.exclusion_proof(c,guard,D.EmptyBranch((F(2),),F(1)))
        b=K.Builder(c,'h'); i=b.conversion('price',b.row(0))
        i=b.rewrite(i,K.scale(-1,guard),K.num(0))
        self.assertEqual(K.check(c,b.proof(i)).budget,-2)

    def test_claimed_moments_are_external_hypotheses(self):
        sig,_=expression_catalogue(); x=K.src('x')
        conditional=absolute_mean_ceiling(sig,x,K.num(0),{'x':0})
        actual=F(1,10)*F(10)+F(9,10)*F(0)
        self.assertEqual(conditional,0)
        self.assertGreater(actual,conditional)  # the supplied moment premise is false

    def test_weak_guard_can_be_used_without_claiming_strict_exclusion(self):
        x=K.src('x'); c=K.context(('x',),(K.Row(K.scale(-1,x),K.num(0)),),{'x':0})
        with self.assertRaises(K.ProofError): D.exclusion_proof(c,x,D.EmptyBranch((F(1),),F(1)))
        branch=D.branch_context(c,x,True,{'x':F(0)})
        b=K.Builder(branch,'h'); b.row(1); old=b.proof()
        b=K.Builder(c,'h'); b.row(0); replacement=b.proof()
        out=T.transport(branch,c,old,{('h','h',1):replacement},{'h':'h'})
        self.assertEqual(K.check(c,out).budget,0)
        self.assertTrue(H.case_feasible(branch,'h',{'x':0}))

    def test_complete_weighted_cover_matches_direct_derivation(self):
        c,p,d,entries,cov=D.triple_example(F(1,8))
        a,b=K.check(c,p),K.check(c,d)
        self.assertEqual(a.budget,F(-5,24))
        self.assertEqual(a.budget,b.budget)
        self.assertTrue(K.same_difference(a.new,a.old,b.new,b.old,c.signature))
        for e in entries: K.check(c,e.proof)
        K.check(c,cov)


def report():
    c,a,g,r=N.paired_policy_fixture()
    e=difference_envelope(c.signature,r.new,r.old)
    return {'author':AUTHOR, 'scope':'Constructed exact audits; external moments/interpretations are hypotheses.',
            'envelope':{'unit':e.unit,'value_at_zero':str(e.value_at_zero),
                        'source_weights':{k:str(v) for k,v in e.source_weights}},
            'paired_bound':str(H.receive(c,N.receive_near_exclusion(c,a,g,replace(r,budget=F(0)),strict=True),r).budget),
            'finite_probe':{'terms':15,'points':27,'ordered_point_pairs_per_term':729,
                            'total_lipschitz_checks':10935,'growth_checks':405},
            'not_claimed':['minimum Lipschitz coefficients','empirical moment verification',
                           'full proof search','formal verification','F08 completion']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    else:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F07AcceptanceTests))
        if not result.wasSuccessful(): raise SystemExit(1)

if __name__=='__main__': main()
