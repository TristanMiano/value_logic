"""Exact finite audits of F05's provisional semantics; NOT a validity decider.

Every evaluation uses a supplied rational model. Tests illustrate separately
written arguments; successful point checks do not establish universal validity.
Python 3.10+, standard library only. No floating-point inputs are accepted.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import unittest
from typing import Mapping


class SemanticError(ValueError):
    """Malformed typed input, source, model or stale context (not refutation)."""


def rat(value: int | F) -> F:
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise SemanticError('Use exact integers or Fraction values, not floats/bools.')
    return F(value)


@dataclass(frozen=True)
class Conversion:
    name: str
    source: str
    target: str
    factor: F


@dataclass(frozen=True)
class Signature:
    scope: str
    units: tuple[str, ...]
    sources: tuple[tuple[str, str], ...]
    conversions: tuple[Conversion, ...] = ()

    def validate(self) -> None:
        if not self.scope or not self.units or len(set(self.units)) != len(self.units):
            raise SemanticError('Nonempty versioned scope and unique units required.')
        if any(not isinstance(u, str) or not u for u in self.units):
            raise SemanticError('Invalid unit.')
        keys = [k for k, _ in self.sources]
        if len(set(keys)) != len(keys) or any(not isinstance(k, str) or not k for k in keys):
            raise SemanticError('Source keys must be unique, nonempty strings.')
        if any(u not in self.units for _, u in self.sources):
            raise SemanticError('Undeclared source unit.')
        names = [c.name for c in self.conversions]
        if len(names) != len(set(names)):
            raise SemanticError('Duplicate conversion.')
        for c in self.conversions:
            if (not c.name or c.source not in self.units or c.target not in self.units
                    or rat(c.factor) <= 0):
                raise SemanticError('Conversions need declared units and positive factors.')

    def conversion(self, name: str) -> Conversion:
        found = [c for c in self.conversions if c.name == name]
        if len(found) != 1:
            raise SemanticError('Unknown conversion.')
        return found[0]


@dataclass(frozen=True)
class Term:
    op: str
    args: tuple[Term, ...] = ()
    name: str = ''
    unit: str = ''
    value: F | None = None


def num(value: int | F, unit: str = 'U') -> Term:
    return Term('const', unit=unit, value=rat(value))


def src(name: str) -> Term:
    return Term('source', name=name)


def loc(name: str) -> Term:
    return Term('local', name=name)


def add(a: Term, b: Term) -> Term:
    return Term('add', (a, b))


def scale(a: int | F, t: Term) -> Term:
    return Term('scale', (t,), value=rat(a))


def sub(a: Term, b: Term) -> Term:
    return add(a, scale(-1, b))


def minimum(a: Term, b: Term) -> Term:
    return Term('min', (a, b))


def maximum(a: Term, b: Term) -> Term:
    return Term('max', (a, b))


def residual(a: Term, b: Term) -> Term:
    return Term('res', (a, b))


def absolute(t: Term) -> Term:
    return maximum(t, scale(-1, t))


def let(name: str, rhs: Term, body: Term) -> Term:
    return Term('let', (rhs, body), name=name)


def convert(name: str, t: Term) -> Term:
    return Term('convert', (t,), name=name)


def infer(t: Term, sig: Signature, locals_: Mapping[str, str] | None = None) -> str:
    sig.validate()
    env = dict(locals_ or {})
    arities = {'const': 0, 'source': 0, 'local': 0, 'add': 2, 'scale': 1,
               'min': 2, 'max': 2, 'res': 2, 'let': 2, 'convert': 1}
    if not isinstance(t, Term) or t.op not in arities or len(t.args) != arities[t.op]:
        raise SemanticError('Unknown or malformed expression node.')
    if t.op == 'const':
        rat(t.value)
        if t.unit not in sig.units:
            raise SemanticError('Unknown literal unit.')
        return t.unit
    if t.op in ('source', 'local'):
        table = dict(sig.sources) if t.op == 'source' else env
        if t.name not in table:
            raise SemanticError(f'Unbound {t.op}: {t.name}')
        return table[t.name]
    if t.op == 'let':
        if not t.name:
            raise SemanticError('Empty local binder.')
        unit = infer(t.args[0], sig, env)
        env[t.name] = unit
        return infer(t.args[1], sig, env)
    unit = infer(t.args[0], sig, env)
    if t.op == 'scale':
        rat(t.value)
        return unit
    if t.op == 'convert':
        c = sig.conversion(t.name)
        if c.source != unit:
            raise SemanticError('Conversion source unit mismatch.')
        return c.target
    if infer(t.args[1], sig, env) != unit:
        raise SemanticError('Mixed-unit arithmetic or comparison.')
    return unit


def assignment(sig: Signature, values: Mapping[str, int | F]) -> dict[str, F]:
    sig.validate()
    if set(values) != {k for k, _ in sig.sources}:
        raise SemanticError('Model must assign exactly the declared source keys.')
    return {k: rat(v) for k, v in values.items()}


def evaluate(t: Term, sig: Signature, values: Mapping[str, int | F]) -> F:
    infer(t, sig)
    point = assignment(sig, values)

    def ev(node: Term, env: dict[str, F]) -> F:
        if node.op == 'const':
            return rat(node.value)
        if node.op == 'source':
            return point[node.name]
        if node.op == 'local':
            return env[node.name]
        if node.op == 'let':
            rhs = ev(node.args[0], env)
            return ev(node.args[1], {**env, node.name: rhs})
        a = ev(node.args[0], env)
        if node.op == 'scale':
            return rat(node.value) * a
        if node.op == 'convert':
            return rat(sig.conversion(node.name).factor) * a
        b = ev(node.args[1], env)
        if node.op == 'add': return a + b
        if node.op == 'min': return min(a, b)
        if node.op == 'max': return max(a, b)
        if node.op == 'res': return max(b - a, F(0))
        raise SemanticError('Unreachable unknown operation.')

    return ev(t, {})


def affine(t: Term, sig: Signature) -> tuple[dict[str, F], F]:
    """Normalize declared affine SOURCE ROWS, not general CPWA expressions."""
    infer(t, sig)

    def combine(a, b):
        keys = set(a[0]) | set(b[0])
        return ({k: a[0].get(k, F(0)) + b[0].get(k, F(0)) for k in keys}, a[1]+b[1])

    def mul(a, factor):
        return ({k: factor*v for k, v in a[0].items()}, factor*a[1])

    def go(node, env):
        if node.op == 'const': return ({}, rat(node.value))
        if node.op == 'source': return ({node.name: F(1)}, F(0))
        if node.op == 'local': return env[node.name]
        if node.op == 'add': return combine(go(node.args[0], env), go(node.args[1], env))
        if node.op == 'scale': return mul(go(node.args[0], env), rat(node.value))
        if node.op == 'convert': return mul(go(node.args[0], env), rat(sig.conversion(node.name).factor))
        if node.op == 'let':
            value = go(node.args[0], env)
            return go(node.args[1], {**env, node.name: value})
        raise SemanticError('Context rows must be explicitly affine.')
    return go(t, {})


@dataclass(frozen=True)
class Row:
    lhs: Term
    rhs: Term


@dataclass(frozen=True)
class Case:
    name: str
    rows: tuple[Row, ...]
    witness: tuple[tuple[str, F], ...]


@dataclass(frozen=True)
class Context:
    signature: Signature
    observation: str
    revision: str
    cases: tuple[Case, ...]

    def validate(self) -> None:
        self.signature.validate()
        names = [c.name for c in self.cases]
        if not names or len(names) != len(set(names)) or any(not n for n in names):
            raise SemanticError('A deployment context needs distinct nonempty live cases.')
        if not self.observation or not self.revision:
            raise SemanticError('Observation/revision identity missing.')
        for case in self.cases:
            if len(dict(case.witness)) != len(case.witness):
                raise SemanticError('Duplicate witness coordinate.')
            point = assignment(self.signature, dict(case.witness))
            for row in case.rows:
                if infer(row.lhs, self.signature) != infer(row.rhs, self.signature):
                    raise SemanticError('Mixed-unit source row.')
                affine(row.lhs, self.signature); affine(row.rhs, self.signature)
                if evaluate(row.lhs, self.signature, point) > evaluate(row.rhs, self.signature, point):
                    raise SemanticError('Supplied context witness is not feasible.')

    def feasible(self, case_name: str, values: Mapping[str, int | F]) -> bool:
        self.validate()
        point = assignment(self.signature, values)
        found = [c for c in self.cases if c.name == case_name]
        if len(found) != 1:
            raise SemanticError('Unknown case.')
        return all(evaluate(r.lhs, self.signature, point) <= evaluate(r.rhs, self.signature, point)
                   for r in found[0].rows)


def serial(value):
    if isinstance(value, F): return str(value)
    if hasattr(value, '__dataclass_fields__'):
        return {k: serial(getattr(value, k)) for k in value.__dataclass_fields__}
    if isinstance(value, (tuple, list)): return [serial(v) for v in value]
    if isinstance(value, dict): return {k: serial(v) for k, v in value.items()}
    return value


def fingerprint(ctx: Context) -> str:
    ctx.validate()
    return hashlib.sha256(json.dumps(serial(ctx), sort_keys=True, separators=(',', ':')).encode()).hexdigest()


@dataclass(frozen=True)
class Goal:
    context_id: str
    new: Term
    old: Term
    budget: F
    unit: str


def goal(ctx: Context, new: Term, old: Term, budget: int | F) -> Goal:
    u = infer(new, ctx.signature)
    if infer(old, ctx.signature) != u:
        raise SemanticError('Mixed-unit goal.')
    return Goal(fingerprint(ctx), new, old, rat(budget), u)


def check_point(ctx: Context, query: Goal, case: str, point: Mapping[str, int | F]) -> dict:
    """A supplied feasible point either satisfies or refutes a universal goal.

A satisfying point is NOT a proof of the universal goal. Invalid points raise.
"""
    if query.context_id != fingerprint(ctx):
        raise SemanticError('Stale/different context: explicit transport or new goal required.')
    if infer(query.new, ctx.signature) != query.unit or infer(query.old, ctx.signature) != query.unit:
        raise SemanticError('Goal unit does not match its expressions.')
    budget = rat(query.budget)
    if not ctx.feasible(case, point):
        raise SemanticError('Point outside the declared source is not a countermodel.')
    new, old = evaluate(query.new, ctx.signature, point), evaluate(query.old, ctx.signature, point)
    difference = new - old
    return {'new': new, 'old': old, 'difference': difference, 'budget': budget,
            'holds_at_point': difference <= budget, 'is_countermodel': difference > budget,
            'shortfall': max(difference, F(0))}


def substitute(t: Term, replacements: Mapping[str, Term], old: Signature, new: Signature) -> Term:
    """Closed-source substitution, not a proof that a source-domain map is valid."""
    infer(t, old)
    for key, expr in replacements.items():
        if key not in dict(old.sources) or infer(expr, new) != dict(old.sources)[key]:
            raise SemanticError('Unknown replacement key or wrong unit.')
    if old.conversions != new.conversions or old.units != new.units:
        raise SemanticError('This substitution adapter keeps operation/conversion meanings fixed.')

    def walk(node):
        if node.op == 'source' and node.name in replacements: return replacements[node.name]
        return Term(node.op, tuple(walk(a) for a in node.args), node.name, node.unit, node.value)
    result = walk(t)
    infer(result, new)
    return result


def interval_rows(name: str, lo: F | int | None, hi: F | int | None, unit='U') -> tuple[Row, ...]:
    rows = []
    if lo is not None: rows.append(Row(num(lo, unit), src(name)))
    if hi is not None: rows.append(Row(src(name), num(hi, unit)))
    return tuple(rows)


def simple_context(sig, rows=(), witness=(), revision='v1', name='only'):
    return Context(sig, 'same-visible-information', revision, (Case(name, tuple(rows), tuple(witness)),))


def composition():
    sig = Signature('two-stage-v1/loss-U', ('U',), (('theta','U'),('z1','U'),('z2','U')))
    rows = interval_rows('theta', 0, 1)+interval_rows('z1',0,None)+interval_rows('z2',0,None)
    ctx = simple_context(sig, rows, (('theta',F(1,2)),('z1',F(0)),('z2',F(0))))
    old = add(add(src('z1'),num(F(3,4))),add(src('z2'),src('theta')))
    new = add(add(src('z1'),src('theta')),add(src('z2'),num(F(1,4))))
    return ctx, goal(ctx,new,old,F(-1,2))


def reflection(beta=F(1,32), revision='e-bound-v1', version='SELF-MIX-v1'):
    sig = Signature(version+'/expected-loss-U/criterion-v1', ('1','U'),
        (('p','1'),('s','1'),('e','U'),('z','U'),('w','U')),
        (Conversion('event-price','1','U',F(1)),))
    rows = interval_rows('p',0,1,'1')+interval_rows('s',0,F(1,4),'1')
    rows += (Row(sub(src('p'),src('s')),num(F(1,2),'1')),
             Row(num(F(1,2),'1'),sub(src('p'),src('s'))))
    rows += interval_rows('e',F(-1,32),rat(beta))+interval_rows('z',0,None)+interval_rows('w',0,None)
    ctx = simple_context(sig, rows, (('p',F(1,2)),('s',F(0)),('e',F(0)),('z',F(0)),('w',F(0))),revision)

    def terms(r):
        r=rat(r)
        if not 0<=r<=1: raise SemanticError('Invalid report/policy parameter.')
        if version == 'SELF-MIX-v1':
            h=add(scale(1-r,src('p')),scale(r,src('s'))); charge=F(1,4)*r
        elif version == 'SELF-MIX-reversed':
            h=add(scale(r,src('p')),scale(1-r,src('s'))); charge=F(1,4)*(1-r)
        else: raise SemanticError('No declared kernel for this version.')
        loss=add(src('z'),add(convert('event-price',h),num(charge)))
        return h,loss
    h0,l0=terms(F(1,2));h1,l1=terms(F(3,4))
    old=add(l0,src('w'));new=add(add(l1,src('w')),src('e'))
    return ctx, goal(ctx,new,old,F(-1,32)), terms


def quadratic():
    sig=Signature('two-independent-draws-v1/expected-events', ('1','U'),
                  (('theta','1'),('q','1'),('z','U')),
                  (Conversion('event-price','1','U',F(1)),))
    points=tuple(F(2+i,8) for i in range(5)); cases=[]; lines=[]
    for i,(a,b) in enumerate(zip(points,points[1:])):
        u=add(scale(a+b,src('theta')),num(-a*b,'1'));lines.append(u)
        rows=interval_rows('theta',a,b,'1')+interval_rows('q',0,None,'1')+interval_rows('z',0,None)
        rows+=(Row(sub(u,num(F(1,256),'1')),src('q')),Row(src('q'),u))
        cases.append(Case(str(i),rows,(('theta',a),('q',a*a),('z',F(0)))))
    ctx=Context(sig,'parameter-unobserved','component-envelope-v1',tuple(cases))
    new=add(src('z'),convert('event-price',src('q')));old=add(src('z'),convert('event-price',src('theta')))
    upper=lines[0]
    for line in lines[1:]: upper=maximum(upper,line)
    return ctx,goal(ctx,new,old,F(-3,16)),upper


def expected_rate(p,s,r):
    p,s,r=rat(p),rat(s),rat(r)
    if not all(0<=v<=1 for v in (p,s,r)): raise SemanticError('Invalid kernel probability.')
    return (1-r)*p+r*s


def least_report(S,dl,du):
    S,dl,du=rat(S),rat(dl),rat(du)
    if not (0<=S<=1 and 0<=dl<=du<=1): raise SemanticError('Invalid source ranges.')
    if du<=1-S: return (S+du)/(1+du)
    if dl>=1-S: return 1/(1+dl)
    return 1/(2-S)


class F05SemanticsTests(unittest.TestCase):
    def setUp(self):
        self.sig=Signature('arithmetic-v1',('1','U'),(('x','U'),('y','U'),('p','1')),
            (Conversion('price','1','U',F(2)),))
        self.point={'x':F(-2),'y':F(3),'p':F(1,2)}

    def test_signed_residual_and_minmax(self):
        self.assertEqual(evaluate(residual(src('x'),src('y')),self.sig,self.point),5)
        self.assertEqual(evaluate(sub(src('x'),src('y')),self.sig,self.point),-5)
        self.assertEqual(evaluate(minimum(src('x'),src('y')),self.sig,self.point),-2)
        self.assertEqual(evaluate(maximum(src('x'),src('y')),self.sig,self.point),3)

    def test_conversion_and_cost_sum(self):
        self.assertEqual(evaluate(add(convert('price',src('p')),src('y')),self.sig,self.point),4)

    def test_mixed_units_rejected(self):
        with self.assertRaises(SemanticError): infer(add(src('x'),src('p')),self.sig)

    def test_unknown_keys_and_locals_rejected(self):
        for t in (src('missing'),loc('x')):
            with self.assertRaises(SemanticError): infer(t,self.sig)

    def test_unknown_conversion_and_invalid_factor(self):
        with self.assertRaises(SemanticError): infer(convert('missing',src('p')),self.sig)
        for factor in (F(0),F(-1)):
            with self.assertRaises(SemanticError):
                Signature('v',('1','U'),(),(Conversion('c','1','U',factor),)).validate()

    def test_wrong_conversion_direction(self):
        with self.assertRaises(SemanticError): infer(convert('price',src('x')),self.sig)

    def test_inexact_values_rejected(self):
        for x in (0.1,float('inf'),float('nan'),True):
            with self.assertRaises(SemanticError): num(x)

    def test_duplicate_signature_keys_rejected(self):
        with self.assertRaises(SemanticError):
            Signature('v',('U',),(('x','U'),('x','U'))).validate()

    def test_unknown_op_and_bad_arity_rejected(self):
        for t in (Term('oracle'),Term('add',(src('x'),)),Term('mul',(src('x'),src('y')))):
            with self.assertRaises(SemanticError): infer(t,self.sig)

    def test_complete_assignment_required(self):
        for p in ({'x':F(1)},dict(self.point,extra=F(1)),dict(self.point,x=1.0)):
            with self.assertRaises(SemanticError): evaluate(src('x'),self.sig,p)

    def test_lexical_shadowing_is_not_source_capture(self):
        t=let('x',num(7),add(src('x'),loc('x')))
        self.assertEqual(evaluate(t,self.sig,self.point),5)
        s=substitute(t,{'x':src('y')},self.sig,self.sig)
        self.assertEqual(evaluate(s,self.sig,self.point),10)

    def test_nested_let_uses_outer_binding_in_rhs(self):
        t=let('x',num(2),let('x',add(loc('x'),num(1)),loc('x')))
        self.assertEqual(evaluate(t,self.sig,self.point),3)
        with self.assertRaises(SemanticError): infer(let('x',loc('x'),loc('x')),self.sig)

    def test_let_may_change_unit_after_conversion(self):
        t=let('r',src('p'),convert('price',loc('r')))
        self.assertEqual(infer(t,self.sig),'U')
        self.assertEqual(evaluate(t,self.sig,self.point),1)

    def test_substitution_requires_closed_same_unit_replacement(self):
        for replacement in (src('p'),loc('x')):
            with self.assertRaises(SemanticError): substitute(src('x'),{'x':replacement},self.sig,self.sig)

    def test_affine_normalization(self):
        t=let('a',add(src('x'),num(2)),add(scale(3,loc('a')),scale(-1,src('y'))))
        coeff,c=affine(t,self.sig)
        self.assertEqual(coeff,{'x':F(3),'y':F(-1)}); self.assertEqual(c,6)
        self.assertEqual(sum(v*self.point[k] for k,v in coeff.items())+c,evaluate(t,self.sig,self.point))

    def test_nonlinear_source_row_rejected(self):
        row=Row(maximum(src('x'),num(0)),num(5))
        ctx=simple_context(self.sig,(row,),tuple(self.point.items()))
        with self.assertRaises(SemanticError): ctx.validate()

    def test_empty_or_contradictory_context_rejected(self):
        with self.assertRaises(SemanticError): Context(self.sig,'o','v',()).validate()
        ctx=simple_context(self.sig,(Row(num(1),src('x')),Row(src('x'),num(0))),tuple(self.point.items()))
        with self.assertRaises(SemanticError): ctx.validate()

    def test_outside_source_not_countermodel(self):
        ctx,g=composition()
        with self.assertRaises(SemanticError): check_point(ctx,g,'only',{'theta':2,'z1':0,'z2':0})

    def test_goal_unit_and_unknown_case_rejected(self):
        ctx,g=composition()
        with self.assertRaises(SemanticError):
            check_point(ctx,Goal(g.context_id,g.new,g.old,g.budget,'1'),'only',dict(ctx.cases[0].witness))
        with self.assertRaises(SemanticError): check_point(ctx,g,'other',dict(ctx.cases[0].witness))

    def test_stale_context_rejected(self):
        old,g,_=reflection();new,_,_=reflection(F(3,64),'e-bound-v2')
        with self.assertRaises(SemanticError): check_point(new,g,'only',dict(new.cases[0].witness))
        self.assertNotEqual(fingerprint(old),fingerprint(new))

    def test_scope_and_observation_change_fingerprint(self):
        ctx,g,_=reflection(); rev,_,_=reflection(version='SELF-MIX-reversed')
        self.assertNotEqual(fingerprint(ctx),fingerprint(rev))
        o=Context(ctx.signature,'now-observed-mode',ctx.revision,ctx.cases)
        self.assertNotEqual(fingerprint(ctx),fingerprint(o))

    def test_shared_composition_exact_and_unbounded(self):
        ctx,g=composition()
        for theta in (F(0),F(1,2),F(1)):
            for z in (0,10**100):
                result=check_point(ctx,g,'only',{'theta':theta,'z1':z,'z2':z})
                self.assertEqual(result['difference'],F(-1,2))
                self.assertTrue(result['holds_at_point'])

    def test_shared_composition_no_absolute_adequacy(self):
        ctx,g=composition();absolute_goal=goal(ctx,g.new,num(0),100)
        self.assertTrue(check_point(ctx,absolute_goal,'only',{'theta':0,'z1':10**6,'z2':0})['is_countermodel'])

    def test_cloned_source_breaks_cancellation(self):
        sig=Signature('cloned',('U',),(('a','U'),('b','U')))
        term=sub(sub(src('a'),src('b')),num(F(1,2)))
        self.assertEqual(evaluate(term,sig,{'a':1,'b':0}),F(1,2))

    def test_clipped_shortfall_cannot_recover_negative_budget(self):
        ctx,g=composition();query=goal(ctx,g.old,g.old,F(-1))
        r=check_point(ctx,query,'only',dict(ctx.cases[0].witness))
        self.assertEqual(r['shortfall'],0);self.assertTrue(r['is_countermodel'])

    def test_reflective_interpretation_direct_kernel(self):
        ctx,g,terms=reflection()
        for s in (F(0),F(1,8),F(1,4)):
            point={'p':s+F(1,2),'s':s,'e':F(1,32),'z':10**60,'w':10**80}
            for r in (F(1,2),F(3,4)):
                self.assertEqual(evaluate(terms(r)[0],ctx.signature,point),expected_rate(point['p'],s,r))
            self.assertEqual(check_point(ctx,g,'only',point)['difference'],F(-1,32))

    def test_report_validity_distinct_from_actual_rate(self):
        ctx,_,terms=reflection();rates=[]
        report=goal(ctx,terms(F(3,4))[0],num(F(3,4),'1'),0)
        for s in (F(0),F(1,4)):
            point={'p':s+F(1,2),'s':s,'e':0,'z':0,'w':0}
            result=check_point(ctx,report,'only',point)
            self.assertTrue(result['holds_at_point']);rates.append(result['new'])
        self.assertEqual(rates,[F(1,8),F(3,8)])

    def test_mixed_report_has_model_and_countermodel(self):
        ctx,_,terms=reflection();g=goal(ctx,terms(F(2,5))[0],num(F(2,5),'1'),0)
        low=check_point(ctx,g,'only',{'p':F(1,2),'s':0,'e':0,'z':0,'w':0})
        high=check_point(ctx,g,'only',{'p':F(3,4),'s':F(1,4),'e':0,'z':0,'w':0})
        self.assertTrue(low['holds_at_point']);self.assertTrue(high['is_countermodel'])

    def test_proxy_weakening_changes_only_affected_goal(self):
        ctx,g,terms=reflection(F(3,64),'weakened')
        p={'p':F(1,2),'s':0,'e':F(3,64),'z':0,'w':0}
        self.assertTrue(check_point(ctx,g,'only',p)['is_countermodel'])
        new=goal(ctx,g.new,g.old,F(-1,64))
        self.assertTrue(check_point(ctx,new,'only',p)['holds_at_point'])
        report=goal(ctx,terms(F(3,4))[0],num(F(3,4),'1'),0)
        self.assertTrue(check_point(ctx,report,'only',p)['holds_at_point'])

    def test_reversed_program_invalidates_old_cost_formula(self):
        ctx,g,_=reflection(version='SELF-MIX-reversed')
        result=check_point(ctx,g,'only',dict(ctx.cases[0].witness))
        self.assertEqual(result['difference'],F(1,16));self.assertTrue(result['is_countermodel'])

    def test_expected_improvement_not_pathwise(self):
        # Common U=5/8 switches the branch; V=3/4 makes neither branch fail.
        u,v,p,s=F(5,8),F(3,4),F(1,2),F(0)
        def run(r):
            branch_s=u<r; fail=v<(s if branch_s else p)
            return F(int(fail))+F(1,4)*int(branch_s)
        self.assertEqual(run(F(3,4))-run(F(1,2)),F(1,4))
        self.assertEqual(expected_rate(p,s,F(3,4))+F(3,16)-expected_rate(p,s,F(1,2))-F(1,8),F(-1,16))

    def test_visible_evidence_selector_not_sequential_non_deterioration(self):
        def chosen(beta): return F(3,4) if beta-F(1,16)<=0 else F(1,2)
        self.assertEqual(chosen(F(1,32)),F(3,4));self.assertEqual(chosen(F(3,32)),F(1,2))
        # Reverting remains safe against fixed r0, but worsens against r1.
        def c(r): return expected_rate(F(1,2),F(0),r)+F(1,4)*r
        self.assertEqual(c(chosen(F(3,32)))-c(chosen(F(1,32))),F(1,16))

    def test_least_report_normalized_polyhedron(self):
        for S,dl,du in ((F(1,4),F(1,2),F(1,2)),(F(3,4),F(1,4),F(1,2)),(F(0),F(0),F(1))):
            r=least_report(S,dl,du)
            dstar=min(max(1-S,dl),du)
            sstar=min(S,1-dstar)
            self.assertEqual(expected_rate(sstar+dstar,sstar,r),r)
            for d in (dl,du,dstar):
                for s in (F(0),min(S,1-d)):
                    self.assertLessEqual(expected_rate(s+d,s,r),r)
        self.assertEqual(least_report(F(3,4),F(1,4),F(1,2)),F(4,5))

    def test_invalid_probabilities_and_report_rejected(self):
        with self.assertRaises(SemanticError): expected_rate(F(5,4),0,F(1,2))
        with self.assertRaises(SemanticError): least_report(F(1,2),F(3,4),F(1,4))
        _,_,terms=reflection()
        with self.assertRaises(SemanticError): terms(F(5,4))

    def test_quadratic_exact_model_maps_into_enclosure(self):
        ctx,g,upper=quadratic()
        for i in range(4):
            a,b=F(2+i,8),F(3+i,8)
            for k in range(9):
                t=a+(b-a)*F(k,8);point={'theta':t,'q':t*t,'z':10**30}
                self.assertTrue(ctx.feasible(str(i),point))
                self.assertTrue(check_point(ctx,g,str(i),point)['holds_at_point'])
                err=evaluate(upper,ctx.signature,point)-t*t
                self.assertTrue(0<=err<=F(1,256))

    def test_quadratic_abstract_model_goal_all_cell_vertices(self):
        ctx,g,_=quadratic()
        for i in range(4):
            a,b=F(2+i,8),F(3+i,8)
            for t in (a,b):
                u=(a+b)*t-a*b
                for q in (u-F(1,256),u):
                    self.assertTrue(check_point(ctx,g,str(i),{'theta':t,'q':q,'z':0})['holds_at_point'])
        self.assertEqual(check_point(ctx,g,'0',{'theta':F(1,4),'q':F(1,16),'z':0})['difference'],F(-3,16))

    def test_abstract_countermodel_can_be_spurious_for_exact_kernel(self):
        ctx,_,_=quadratic();point={'theta':F(1,2),'q':F(63,256),'z':0}
        g=goal(ctx,num(F(1,4),'1'),src('q'),0)
        self.assertTrue(check_point(ctx,g,'1',point)['is_countermodel'])
        self.assertEqual(F(1,2)**2,F(1,4))

    def test_one_chord_suffices_for_specific_comparison(self):
        for k in range(33):
            t=F(1,4)+F(k,64);u=t-F(3,16)
            self.assertLessEqual(t*t,u)
            self.assertEqual(u-t,F(-3,16))
        self.assertEqual((F(1,2)-F(3,16))-F(1,4),F(1,16))

    def test_reusing_one_random_draw_breaks_quadratic_adapter(self):
        t=F(1,2)
        self.assertEqual(t*t-t,F(-1,4));self.assertEqual(t-t,0)
        self.assertGreater(t-t,F(-3,16))

    def test_pointwise_minimum_is_not_hidden_action_selection(self):
        self.assertEqual(min(0,2),0);self.assertEqual(min(2,0),0)
        for k in range(21):
            q=F(k,20);self.assertGreaterEqual(max(2*q,2*(1-q)),1)

    def test_numeric_recoding_not_evidence_equivalence(self):
        x,y=F(3),F(0)
        self.assertTrue(x+y<=3 and y<=2);self.assertFalse(x<=1)

    def test_projection_does_not_commute_with_later_join(self):
        grid=(F(0),F(1,2),F(1))
        gamma={(x,y) for x in grid for y in grid if x==y}
        delta={(x,y) for x in grid for y in grid if y==0}
        self.assertEqual({x for x,y in gamma},{x for x,y in delta})
        self.assertEqual({x for x,y in gamma&delta},{F(0)})

    def test_substitution_needs_domain_transport(self):
        t=absolute(src('x'));sigma={'x':scale(-1,src('x'))}
        t2=substitute(t,sigma,self.sig,self.sig);s2=substitute(src('x'),sigma,self.sig,self.sig)
        p=dict(self.point,x=F(1))
        self.assertGreater(evaluate(t2,self.sig,p),evaluate(s2,self.sig,p))
        p['x']=F(-1);self.assertLessEqual(evaluate(t2,self.sig,p),evaluate(s2,self.sig,p))

    def test_absolute_error_and_resource_cost_native(self):
        sig=Signature('MAE-plus-use-cost',('U',),(('y','U'),('c','U'),('z','U')))
        rows=interval_rows('y',F(3,4),None)+interval_rows('c',0,F(1,4))+interval_rows('z',0,None)
        ctx=simple_context(sig,rows,(('y',F(3,4)),('c',F(1,4)),('z',F(0))))
        new=add(add(absolute(sub(src('y'),num(1))),src('c')),src('z'))
        old=add(absolute(src('y')),src('z'));g=goal(ctx,new,old,F(-1,4))
        for y in (F(3,4),F(1),F(2),F(10**80)):
            self.assertTrue(check_point(ctx,g,'only',{'y':y,'c':F(1,4),'z':10**90})['holds_at_point'])
        self.assertEqual(check_point(ctx,g,'only',dict(ctx.cases[0].witness))['difference'],F(-1,4))

    def test_saturation_erases_negative_improvement(self):
        self.assertEqual(F(2)-F(3),-1)
        self.assertEqual(min(F(2),F(1))-min(F(3),F(1)),0)
        self.assertEqual(max(F(-2),F(0))-max(F(-1),F(0)),0)

    def test_upper_enclosure_cannot_be_negated_as_upper(self):
        q=F(0);self.assertLessEqual(q,1);self.assertGreater(-q,-1)

    def test_finite_pair_translation_preserves_signed_budget(self):
        pairs=((F(0),F(0)),(F(3),F(1)),(F(1),F(4)),(F(10**40),F(10**40)+1))
        for a,b in pairs:
            for c,d in pairs:
                self.assertEqual(min(a+d,c+b)-(b+d),min(a-b,c-d))
                self.assertEqual(max((c+b)-(a+d),F(0)),max((c-d)-(a-b),F(0)))
                for budget in (F(-1),F(0),F(3,2)):
                    pos,neg=max(budget,F(0)),max(-budget,F(0))
                    self.assertEqual(a+d+neg<=b+c+pos,(a-b)-(c-d)<=budget)

    def test_positive_unit_change_not_same_numeric_budget(self):
        difference=F(-1,2); factor=F(100)
        self.assertEqual(factor*difference,F(-50))
        self.assertNotEqual(difference,factor*difference)


def report() -> dict:
    ctx,g=composition();rc,rg,_=reflection();qc,qg,_=quadratic()
    return {'status':'F05 provisional first pass; rational supplied-model audits, not a global validity procedure',
        'source_base':'a95f4a06efe2b181f9001017e3c4908131fddf50',
        'new_tests':unittest.defaultTestLoader.loadTestsFromTestCase(F05SemanticsTests).countTestCases(),
        'comparison_orientation':'new minus old <= signed budget',
        'shared_composition':serial(check_point(ctx,g,'only',dict(ctx.cases[0].witness))),
        'reflective_sharp':serial(check_point(rc,rg,'only',{'p':F(1,2),'s':F(0),'e':F(1,32),'z':F(0),'w':F(0)})),
        'weakened_reflective_bound':'-1/64',
        'quadratic_endpoint':serial(check_point(qc,qg,'0',dict(qc.cases[0].witness))),
        'quadratic_component_enclosure_error':'1/256',
        'native_MAE_resource_bound':'-1/4',
        'normalized_uncertain_gap_least_report':str(least_report(F(3,4),F(1,4),F(1,2))),
        'finite_enumerations':{'quadratic_exact_points_per_cell':9,'quadratic_cells':4,
            'lottery_weights':21,'one_chord_points':33,'pair_values':4,'pair_budgets':3},
        'limits':['No general soundness/completeness theorem for an adopted deductive calculus.',
          'No F11 reasoner, optimizer, neural training or confidence calibration.',
          'Analytic universal results require the separate mathematical arguments.']}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F05SemanticsTests))
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
