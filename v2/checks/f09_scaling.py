"""Exact F09 numerical presentation audits; original kernels stay unchanged.

Research contributor: Codex (GPT-6), 2026-09-30. Typed affine presentation
compiles to existing term macros. Direct proof transformation is deliberately
limited to a common positive scale: per-unit relabeling need not preserve the
native normalizer's recognized equalities.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as H
from v2.checks import f08_unit_characterization as U


class Presentation:
    """An explicitly declared rational affine coordinate map, not new evidence."""
    def __init__(self, signature, factors, offsets=None):
        signature.validate()
        if set(factors) != set(signature.units):
            raise H.AuditError('Supply exactly one factor for every unit.')
        self.original = signature
        self.factors = {u:H.exact(a) for u,a in factors.items()}
        if any(a <= 0 for a in self.factors.values()):
            raise H.AuditError('Presentation factors must be positive.')
        offsets = {u:F(0) for u in signature.units} if offsets is None else offsets
        if set(offsets) != set(signature.units):
            raise H.AuditError('Supply exactly one offset for every unit.')
        self.offsets = {u:H.exact(c) for u,c in offsets.items()}
        self.signature = replace(signature, scope=signature.scope+'/F09-affine-presentation',
            conversions=tuple(replace(c,factor=self.factors[c.target]*c.factor/self.factors[c.source])
                              for c in signature.conversions))
        self.signature.validate()

    def term(self, term, environment=None):
        environment = {} if environment is None else environment
        unit = K.infer(term,self.original,environment)
        a,c = self.factors[unit],self.offsets[unit]
        if term.op == 'const': return K.num(a*term.value+c,unit)
        if term.op in ('source','local'): return term
        if term.op == 'let':
            rhs,body = term.args
            local_unit = K.infer(rhs,self.original,environment)
            return K.let(term.name,self.term(rhs,environment),
                         self.term(body,{**environment,term.name:local_unit}))
        first = self.term(term.args[0],environment)
        if term.op == 'scale':
            out, correction = K.scale(term.value,first),(1-term.value)*c
        elif term.op == 'convert':
            conversion = self.original.conversion(term.name)
            gain = self.signature.conversion(term.name).factor
            out,correction = K.convert(term.name,first),c-gain*self.offsets[conversion.source]
        else:
            second = self.term(term.args[1],environment)
            constructor = {'add':K.add,'min':K.minimum,'max':K.maximum,'res':K.residual}[term.op]
            out = constructor(first,second)
            correction = -c if term.op == 'add' else c if term.op == 'res' else F(0)
        return K.add(out,K.num(correction,unit)) if correction else out

    def point(self, point):
        if set(point) != {n for n,_ in self.original.sources}:
            raise H.AuditError('Supply exactly the original source coordinates.')
        return {n:self.factors[u]*H.exact(point[n])+self.offsets[u]
                for n,u in self.original.sources}

    def context(self, ctx):
        ctx.validate()
        if ctx.signature != self.original: raise H.AuditError('Different original signature.')
        cases = tuple(replace(h,rows=tuple(K.Row(self.term(r.lhs),self.term(r.rhs)) for r in h.rows),
                              witness=tuple(self.point(dict(h.witness)).items())) for h in ctx.cases)
        out = replace(ctx,signature=self.signature,revision=ctx.revision+'/F09-affine-presentation',cases=cases)
        out.validate()
        return out


def _relabel_proof(ctx, proof, presentation):
    """Candidate instruction map; private because general unit gauges can fail."""
    new = presentation.context(ctx)
    steps = []
    for step in proof.steps:
        factor = presentation.factors[K.infer(step.new,ctx.signature)]
        data = step.data
        if step.rule == 'slack': data = (factor*data[0],)
        if step.rule == 'lattice': data = (data[0],presentation.term(data[1]),presentation.term(data[2]))
        steps.append(replace(step,new=presentation.term(step.new),old=presentation.term(step.old),
                             budget=factor*step.budget,data=data,context_id=K.fingerprint(new)))
    return new,K.Proof(tuple(steps),proof.root)


def uniform_scale_proof(ctx, proof, factor):
    """Checked direct proof compiler for one common positive rational scale."""
    K.check(ctx,proof)
    presentation = Presentation(ctx.signature,{u:H.exact(factor) for u in ctx.signature.units})
    new,out = _relabel_proof(ctx,proof,presentation)
    K.check(new,out)
    return new,out


def nested_unit_fixture():
    sig = K.Signature('F09-unit-normalizer-v1',('U','V'),(('x','U'),),
                      (K.Conversion('out','U','V',F(1)),K.Conversion('back','V','U',F(1))))
    ctx = K.Context(sig,'fixed-visible-observation','r1',(K.Case('h',(),(('x',F(0)),)),))
    x,z = K.src('x'),K.num(0)
    first = K.minimum(x,z)
    second = K.convert('back',K.minimum(K.convert('out',x),K.num(0,'V')))
    builder = K.Builder(ctx,'h')
    builder.constant(first,second)
    proof = builder.proof()
    K.check(ctx,proof)
    return ctx,proof


def repaired_unit_certificate():
    ctx,proof = nested_unit_fixture()
    presentation = Presentation(ctx.signature,{'U':F(1),'V':F(2)})
    new = presentation.context(ctx)
    forward,_ = U.lattice_path_equivalence(new,'h',K.src('x'),K.num(0),('out',),'min')
    builder = K.Builder(new,'h')
    root = builder.conversion('back',T._copy_into(builder,forward))
    oldroot = proof.steps[proof.root]
    root = builder.rewrite(root,presentation.term(oldroot.new),presentation.term(oldroot.old))
    out = builder.proof(root)
    request = H.request(new,'h',presentation.term(oldroot.new),presentation.term(oldroot.old),F(0))
    H.receive(new,out,request)
    return new,out,request


def squash(x):
    x = H.exact(x)
    return x/(1+abs(x))


class F09ScalingTests(unittest.TestCase):
    def test_uniform_scale_native_examples_and_inverse(self):
        for name,(ctx,proof) in K.examples().items():
            for factor in (F(1,3),F(2)):
                with self.subTest(name=name,factor=factor):
                    new,out = uniform_scale_proof(ctx,proof,factor)
                    self.assertEqual(K.check(new,out).budget,factor*K.check(ctx,proof).budget)
                    again,back = uniform_scale_proof(new,out,1/factor)
                    self.assertEqual(K.check(again,back).budget,K.check(ctx,proof).budget)

    def test_typed_affine_semantics_with_shadowing_and_unused_binding(self):
        ctx,_ = nested_unit_fixture()
        sig = ctx.signature
        x = K.src('x')
        terms = (K.add(x,K.num(2)),K.scale(-3,x),K.minimum(x,K.num(1)),
                 K.maximum(x,K.num(-1)),K.residual(x,K.num(1)),K.convert('out',x),
                 K.let('a',K.convert('out',x),K.let('a',K.add(x,K.num(1)),K.residual(K.loc('a'),x))),
                 K.let('dead',K.convert('out',x),K.minimum(x,K.num(2))))
        presentation = Presentation(sig,{'U':F(3),'V':F(5)},{'U':F(-2),'V':F(7)})
        for value,term in product((F(-5),F(0),F(1,2),F(8)),terms):
            point = {'x':value}
            unit = K.infer(term,sig)
            encoded = H.value(presentation.term(term),presentation.signature,presentation.point(point))
            self.assertEqual(encoded,presentation.factors[unit]*H.value(term,sig,point)+presentation.offsets[unit])

    def test_rows_and_witnesses_correspond(self):
        ctx = K.context(('x','y'),(K.Row(K.add(K.src('x'),K.src('y')),K.num(1)),),{'x':F(0),'y':F(0)})
        presentation = Presentation(ctx.signature,{'U':F(2)},{'U':F(3)})
        new = presentation.context(ctx)
        for x,y in product(range(-2,3),repeat=2):
            point = {'x':F(x),'y':F(y)}
            self.assertEqual(H.case_feasible(ctx,'h',point),H.case_feasible(new,'h',presentation.point(point)))

    def test_conversion_factor_must_move(self):
        ctx,_ = nested_unit_fixture()
        presentation = Presentation(ctx.signature,{'U':F(3),'V':F(5)})
        self.assertEqual(presentation.signature.conversion('out').factor,F(5,3))
        term = K.convert('out',K.src('x'))
        self.assertEqual(H.value(presentation.term(term),presentation.signature,{'x':F(3)}),5)
        self.assertEqual(H.value(term,ctx.signature,{'x':F(3)}),3)

    def test_per_unit_instruction_relabeling_is_not_a_general_compiler(self):
        ctx,proof = nested_unit_fixture()
        presentation = Presentation(ctx.signature,{'U':F(1),'V':F(2)})
        new,candidate = _relabel_proof(ctx,proof,presentation)
        with self.assertRaises(K.ProofError): K.check(new,candidate)
        good,certificate,request = repaired_unit_certificate()
        self.assertEqual(H.receive(good,certificate,request).budget,0)

    def test_old_fingerprint_is_not_reused(self):
        ctx,proof = nested_unit_fixture()
        new,_ = uniform_scale_proof(ctx,proof,F(2))
        with self.assertRaises(K.ProofError): K.check(new,proof)

    def test_invalid_scales_and_inexact_parameters_rejected(self):
        ctx,_ = nested_unit_fixture()
        for factor in (F(0),F(-1),1.5,True):
            with self.assertRaises(H.AuditError):
                Presentation(ctx.signature,{'U':factor,'V':F(1)})

    def test_affine_offsets_need_arithmetic_corrections(self):
        h = lambda x:x+1
        self.assertNotEqual(h(1+1),h(1)+h(1))
        self.assertNotEqual(h(max(1-1,0)),max(h(1)-h(1),0))
        self.assertEqual(h(1)-h(2),1-2)

    def test_monotone_component_recoding_reverses_sum_preference(self):
        self.assertLess(1+2,0+4)
        self.assertGreater(squash(1)+squash(2),squash(0)+squash(4))
        self.assertLess(squash(3),squash(4))

    def test_no_common_budget_map_for_nonlinear_hinge(self):
        h = lambda x:max(x,2*x)
        self.assertEqual(h(F(1))-h(F(0)),2)
        self.assertEqual(F(-1,2)-F(-2),F(3,2))
        self.assertEqual(h(F(-1,2))-h(F(-2)),F(3,2))
        # Any encoded budget accepting original gap 1 here also accepts gap 3/2.
        self.assertLess(h(F(-1,2))-h(F(-2)),h(F(1))-h(F(0)))

    def test_signed_secant_bound_and_negative_budget_counterexample(self):
        h = lambda x:max(x,2*x)
        for t,s,b in product((F(k,2) for k in range(-6,7)),repeat=3):
            if t-s <= b:
                self.assertLessEqual(h(t)-h(s),2*max(b,0)+min(b,0))
        self.assertGreater(h(F(-2))-h(F(-1)),F(-2))

    def test_unbounded_baseline_loses_uniform_encoded_margin(self):
        for z in (F(0),F(1),F(10),F(1000)):
            self.assertEqual(squash(z)-squash(z+1),-1/((1+z)*(2+z)))
            self.assertLess(squash(z)-squash(z+1),0)
        self.assertGreater(squash(1000)-squash(1001),F(-1,1000000))

    def test_sharp_bounded_squash_budgets(self):
        M = F(3)
        grid = tuple(F(k,4) for k in range(13))
        for budget in (F(-2),F(-1),F(0),F(1),F(2)):
            expected = budget/(1+budget) if budget >= 0 else budget/((1+M+budget)*(1+M))
            actual = max(squash(t)-squash(s) for t,s in product(grid,repeat=2) if t-s <= budget)
            self.assertEqual(actual,expected)


if __name__ == '__main__': unittest.main()
