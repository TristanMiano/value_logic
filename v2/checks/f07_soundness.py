"""F07 finite soundness audit and request-bound receiver.

Not a universal semantic decider, formal proof assistant, or empirical validator.
The reference interpreter below shares the AST only: it does not call F05's
interpreter/normalizer or F06's algebraic equality checker. Python 3.10+.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from typing import Mapping, Sequence
import unittest

from v2.checks import f06_inference_rules as K

NATIVE_RULES = frozenset(('constant','row','rewrite','trans','add','scale','negate',
    'convert','slack','meet_proofs','max_common','min_common','congruence',
    'res_congruence','lattice','all_cases'))


class AuditError(ValueError):
    """Rejected audit input; not automatically a countermodel to its claim."""


def exact(value: int | F) -> F:
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise AuditError('Only exact integers and Fractions are admitted.')
    return F(value)


def reference_denotation(term: K.Term, signature: K.Signature,
                         point: Mapping[str, int | F]) -> tuple[F, str]:
    """Independent recursive typed evaluation; no algebraic collection."""
    sources = dict(signature.sources)
    if len(sources) != len(signature.sources) or set(point) != set(sources):
        raise AuditError('Supply exactly the unique declared source coordinates.')
    units = set(signature.units)
    if not units or len(units) != len(signature.units):
        raise AuditError('Invalid unit declaration.')
    if any(u not in units for u in sources.values()):
        raise AuditError('Undeclared source unit.')
    values = {name: exact(v) for name, v in point.items()}
    conversions = {c.name: c for c in signature.conversions}
    if len(conversions) != len(signature.conversions):
        raise AuditError('Duplicate conversion name.')
    for c in conversions.values():
        if c.source not in units or c.target not in units or exact(c.factor) <= 0:
            raise AuditError('Invalid positive conversion.')
    arities = {'const':0,'source':0,'local':0,'add':2,'scale':1,
               'min':2,'max':2,'res':2,'let':2,'convert':1}

    def visit(t: K.Term, environment: dict[str, tuple[F, str]]) -> tuple[F, str]:
        if not isinstance(t, K.Term) or t.op not in arities or len(t.args) != arities[t.op]:
            raise AuditError('Malformed term.')
        if t.op == 'const':
            if t.unit not in units: raise AuditError('Unknown literal unit.')
            return exact(t.value), t.unit
        if t.op == 'source':
            if t.name not in sources: raise AuditError('Unknown source.')
            return values[t.name], sources[t.name]
        if t.op == 'local':
            if t.name not in environment: raise AuditError('Unbound local.')
            return environment[t.name]
        if t.op == 'let':
            if not t.name: raise AuditError('Empty binder.')
            captured = visit(t.args[0], environment)
            extended = dict(environment); extended[t.name] = captured
            return visit(t.args[1], extended)
        a, u = visit(t.args[0], environment)
        if t.op == 'scale': return exact(t.value)*a, u
        if t.op == 'convert':
            if t.name not in conversions: raise AuditError('Unknown conversion.')
            c = conversions[t.name]
            if u != c.source: raise AuditError('Conversion source mismatch.')
            return exact(c.factor)*a, c.target
        b, v = visit(t.args[1], environment)
        if u != v: raise AuditError('Mixed-unit term.')
        if t.op == 'add': return a+b, u
        if t.op == 'min': return (a if a <= b else b), u
        if t.op == 'max': return (a if a >= b else b), u
        if t.op == 'res': return (b-a if b > a else F(0)), u
        raise AuditError('Unreachable term tag.')
    return visit(term, {})


def value(t: K.Term, sig: K.Signature, point: Mapping[str, int | F]) -> F:
    return reference_denotation(t, sig, point)[0]


def case_feasible(ctx: K.Context, case: str, point: Mapping[str, int | F]) -> bool:
    found = [h for h in ctx.cases if h.name == case]
    if len(found) != 1: raise AuditError('Unknown case.')
    # Validate assignment even when the row list is empty.
    reference_denotation(K.num(0, ctx.signature.units[0]), ctx.signature, point)
    for row in found[0].rows:
        a, u = reference_denotation(row.lhs, ctx.signature, point)
        b, v = reference_denotation(row.rhs, ctx.signature, point)
        if u != v: raise AuditError('Mixed-unit source row.')
        if a > b: return False
    return True


@dataclass(frozen=True)
class Request:
    context_id: str
    case: str | None
    new: K.Term
    old: K.Term
    budget: F
    unit: str


def request(ctx: K.Context, case: str | None, new: K.Term, old: K.Term,
            budget: int | F, unit: str = 'U') -> Request:
    return Request(K.fingerprint(ctx), case, new, old, exact(budget), unit)


def receive(ctx: K.Context, proof: K.Proof, expected: Request) -> K.Step:
    """Check trace AND requested root. Adds no inference rule or search."""
    if expected.context_id != K.fingerprint(ctx):
        raise AuditError('The request belongs to a different context.')
    if expected.case is not None and expected.case not in {h.name for h in ctx.cases}:
        raise AuditError('Unknown requested case.')
    b = exact(expected.budget)
    if (K.infer(expected.new, ctx.signature) != expected.unit or
            K.infer(expected.old, ctx.signature) != expected.unit):
        raise AuditError('Request unit mismatch.')
    root = K.check(ctx, proof)
    if root.case != expected.case or (root.new, root.old) != (expected.new, expected.old):
        raise AuditError('Valid trace does not prove the requested pair and scope.')
    if K.infer(root.new, ctx.signature) != expected.unit or exact(root.budget) > b:
        raise AuditError('Root does not meet the requested unit or strength.')
    return root


def audit_points(ctx: K.Context, proof: K.Proof,
                 points: Sequence[Mapping[str, int | F]]) -> dict[str, int]:
    """Check all trace nodes at supplied admissible points, not all reals."""
    K.check(ctx, proof)
    node_checks = 0; feasible_points = 0
    for x in points:
        feasible = {h.name: case_feasible(ctx, h.name, x) for h in ctx.cases}
        if any(feasible.values()): feasible_points += 1
        for node in proof.steps:
            in_domain = any(feasible.values()) if node.case is None else feasible[node.case]
            if not in_domain: continue
            delta = value(node.new, ctx.signature, x)-value(node.old, ctx.signature, x)
            if delta > exact(node.budget):
                raise AuditError(f'Finite countermodel at {node.rule}: {delta} > {node.budget}')
            node_checks += 1
    if not feasible_points: raise AuditError('No supplied point is in the source.')
    return {'feasible_points': feasible_points, 'node_evaluations': node_checks}


def row_coordinates(ctx: K.Context, case: str, point: Mapping[str, int | F]):
    """Affine intercepts obtained by independent zero evaluation, not normalization."""
    h = next((h for h in ctx.cases if h.name == case), None)
    if h is None: raise AuditError('Unknown case.')
    zero = {k:F(0) for k, _ in ctx.signature.sources}
    actual = []; eta = []
    for row in h.rows:
        c = value(row.lhs, ctx.signature, zero)-value(row.rhs, ctx.signature, zero)
        actual.append(value(row.lhs, ctx.signature, point)-value(row.rhs, ctx.signature, point)-c)
        eta.append(-c)
    return actual, eta


def budget_program(ctx: K.Context, proof: K.Proof, bounds: Sequence[int | F]):
    """Evaluate the independently reconstructed LOCAL bound recurrence and L vector."""
    K.check(ctx, proof)
    if any(n.rule == 'all_cases' for n in proof.steps):
        raise AuditError('Localize global cases before graded replay.')
    root_case = proof.steps[proof.root].case
    if root_case is None: raise AuditError('This fixture expects one local case.')
    count = len(next(h for h in ctx.cases if h.name == root_case).rows)
    if len(bounds) != count: raise AuditError('Wrong number of row bounds.')
    zeta = tuple(exact(b) for b in bounds)
    numbers: list[F] = []; sensitivities: list[tuple[F,...]] = []
    zero = (F(0),)*count
    for node in proof.steps:
        if node.case != root_case: raise AuditError('Local trace required.')
        p = [numbers[i] for i in node.parents]
        ls = [sensitivities[i] for i in node.parents]
        tag = node.rule
        if tag == 'row':
            i = node.data[0]; b = zeta[i]; l = tuple(F(int(j==i)) for j in range(count))
        elif tag in ('constant','lattice'):
            b = exact(node.budget); l = zero
        elif tag in ('rewrite','negate'):
            b = p[0]; l = ls[0]
        elif tag == 'slack':
            b = p[0]+exact(node.data[0]); l = ls[0]
        elif tag in ('scale','convert'):
            k = exact(node.data[0]) if tag == 'scale' else exact(
                next(c.factor for c in ctx.signature.conversions if c.name==node.data[0]))
            b = k*p[0]; l = tuple(k*x for x in ls[0])
        elif tag in ('add','trans','res_congruence'):
            b = sum(p, F(0)); l = tuple(a+c for a,c in zip(*ls))
            if tag == 'res_congruence': b = max(b,F(0))
        elif tag in ('meet_proofs','max_common','min_common','congruence'):
            b = min(p) if tag == 'meet_proofs' else max(p)
            l = tuple(max(a,c) for a,c in zip(*ls))
        else: raise AuditError('Unsupported local recurrence tag.')
        numbers.append(b); sensitivities.append(l)
    return numbers[proof.root], sensitivities[proof.root]


def grade_at(ctx: K.Context, proof: K.Proof, withdrawn: tuple[int,...],
             point: Mapping[str,int | F]) -> dict[str,F]:
    root = K.check(ctx,proof)
    if root.case is None: raise AuditError('Local proof required.')
    a, eta = row_coordinates(ctx, root.case, point)
    if (not isinstance(withdrawn,tuple) or len(set(withdrawn)) != len(withdrawn) or
        any(isinstance(i,bool) or not isinstance(i,int) or not 0<=i<len(a) for i in withdrawn)):
        raise AuditError('Invalid withdrawal indices.')
    if any(a[i] > eta[i] for i in range(len(a)) if i not in withdrawn):
        raise AuditError('A retained premise fails at this point.')
    penalties = [max(a[i]-eta[i],F(0)) if i in withdrawn else F(0) for i in range(len(a))]
    bound, L = budget_program(ctx, proof, [e+p for e,p in zip(eta,penalties)])
    excess = bound-exact(root.budget)
    return {'bound':bound, 'penalty':excess,
            'linear_penalty':sum((w*p for w,p in zip(L,penalties)),F(0)),
            'actual_difference':value(root.new,ctx.signature,point)-value(root.old,ctx.signature,point)}


def native_catalogue():
    x,y = K.src('x'),K.src('y'); z=K.num(0)
    ctx = K.context(('x','y'),(K.Row(x,K.num(1)),K.Row(y,K.num(2)),
        K.Row(K.scale(-1,x),K.num(1)),K.Row(K.scale(-1,y),K.num(1))),
        dict(x=0,y=0),units=('U','V'),conversions=(K.Conversion('uv','U','V',F(2)),))
    b=K.Builder(ctx,'h'); rx=b.rewrite(b.row(0),x,z); ry=b.rewrite(b.row(1),y,z)
    b.row(2); b.row(3); b.constant(K.add(x,K.num(3)),x)
    shift=b.rewrite(rx,K.add(x,y),y); b.trans(shift,ry)
    b.add(rx,rx); b.scale(2,rx); nx=b.negate(rx); ny=b.negate(ry)
    b.conversion('uv',rx); loose=b.slack(3,rx); b.meet(rx,loose)
    b.max_common(rx,ry); b.min_common(nx,ny)
    b.congruence('min',rx,ry); b.congruence('max',rx,ry); b.res_congruence(rx,ry)
    for tag in ('min_left','min_right','max_left','max_right'): b.lattice(tag,x,y)
    return ctx,b.proof()


def case_example():
    x=K.src('x'); sig=K.Signature('F07-cases',('U',),(('x','U'),))
    cases=tuple(K.Case(str(v),(K.Row(x,K.num(v)),K.Row(K.scale(-1,x),K.num(-v))),
                       (('x',F(v)),)) for v in (0,1))
    ctx=K.Context(sig,'fixed-policy','v1',cases); b=K.Builder(ctx); roots=[]
    for h in cases:
        b.case=h.name; roots.append(b.rewrite(b.row(0),x,K.num(0)))
    b.all_cases(roots)
    return ctx,b.proof(),roots


def logistic_example():
    m,lo,ln,c,z=map(K.src,('m','old','new','c','z'))
    rows=(K.Row(K.sub(K.scale(-1,m),lo),K.num(0)),K.Row(ln,K.num(F(3,4))),
          K.Row(m,K.num(-1)),K.Row(c,K.num(F(1,8))),K.Row(K.num(0),c),K.Row(K.num(0),z))
    ctx=K.context(('m','old','new','c','z'),rows,dict(m=-1,old=1,new=0,c=0,z=0),scope='F07-logistic-envelope')
    b=K.Builder(ctx,'h'); i=b.row(0)
    for j in (1,2,3): i=b.add(i,b.row(j))
    b.rewrite(i,K.add(K.add(ln,z),c),K.add(lo,z))
    return ctx,b.proof()


def reflective_example():
    p,s,e,z=map(K.src,('p','s','e','z'))
    rows=(K.Row(K.add(p,s),K.num(1)),K.Row(K.sub(s,p),K.num(F(-1,4))),
          K.Row(e,K.num(F(1,32))),K.Row(K.num(0),p),K.Row(K.num(0),s))
    ctx=K.context(('p','s','e','z'),rows,dict(p=F(5,8),s=F(3,8),e=F(1,32),z=0),scope='F07-reflective-model')
    h0=K.scale(F(1,2),K.add(p,s)); h1=K.add(K.scale(F(1,4),p),K.scale(F(3,4),s))
    b=K.Builder(ctx,'h'); base=b.scale(F(1,2),b.row(0)); gap=b.scale(F(1,4),b.row(1))
    report=b.add(base,gap); report=b.add(report,b.constant(K.num(F(-3,4)),K.num(0)))
    report=b.rewrite(report,h1,K.num(F(3,4)))
    i=b.add(gap,b.row(2)); i=b.rewrite(i,K.add(K.add(h1,z),e),K.add(h0,z))
    return ctx,b.proof(),report


def jsonable(obj):
    if isinstance(obj,F): return str(obj)
    if isinstance(obj,dict): return {k:jsonable(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)): return [jsonable(v) for v in obj]
    return obj


def report():
    ctx,p=native_catalogue(); cx,cp,_=case_example()
    coverage=sorted({n.rule for n in p.steps+cp.steps})
    g=[dict(x=F(a,2),y=F(b,2)) for a,b in product(range(-4,5),range(-4,7))]
    lg,lp=logistic_example(); rf,rp,ri=reflective_example()
    return jsonable({'scope':'finite fixtures for separately proved S1-S10/G1-G8; not a universal verifier',
      'native_tags':coverage,'native_tag_count':len(coverage),
      'independent_evaluator_uses':'AST fields and exact rational arithmetic; no old evaluate/affine/_form',
      'native_grid':audit_points(ctx,p,g),
      'case_grid':audit_points(cx,cp,[dict(x=0),dict(x=1)]),
      'logistic_bound':K.check(lg,lp).budget,
      'reflective_bound':K.check(rf,rp).budget,
      'reflective_report_excess':rp.steps[ri].budget,
      'probability_bridge':F(7,16)+F(1,20)*(1-F(7,16)),
      'scope_correction':'U1 requires coverage of the requested case/domain; union membership is insufficient for local claims',
      'checker_modified':False,'formal_proof_assistant':False,'trained_network':False})


class F07SoundnessTests(unittest.TestCase):
    def simple(self):
        x=K.src('x'); ctx=K.context(('x',),(K.Row(x,K.num(1)),),dict(x=0),scope='F07-simple')
        b=K.Builder(ctx,'h'); b.rewrite(b.row(0),x,K.num(0))
        return ctx,b.proof()

    def test_all_sixteen_tags_have_reference_points(self):
        r=report(); self.assertEqual(set(r['native_tags']),NATIVE_RULES)
        self.assertGreater(r['native_grid']['node_evaluations'],0)

    def test_reference_linear_arithmetic(self):
        sig=K.Signature('s',('U',),(('x','U'),))
        self.assertEqual(value(K.add(K.scale(-3,K.src('x')),K.num(2)),sig,dict(x=F(2,3))),0)

    def test_reference_residual_orientation(self):
        sig=K.Signature('s',('U',),())
        self.assertEqual(value(K.residual(K.num(3),K.num(1)),sig,{}),0)
        self.assertEqual(value(K.residual(K.num(1),K.num(3)),sig,{}),2)

    def test_reference_rejects_missing_source(self):
        ctx,_=self.simple()
        with self.assertRaises(AuditError): value(K.src('x'),ctx.signature,{})

    def test_reference_rejects_float_and_bool(self):
        for v in (1.0,True):
            with self.subTest(v=v),self.assertRaises(AuditError): exact(v)

    def test_reference_rejects_mixed_units(self):
        sig=K.Signature('s',('U','V'),())
        with self.assertRaises(AuditError): value(K.add(K.num(0),K.num(0,'V')),sig,{})

    def test_zero_does_not_hide_unbound_child(self):
        sig=K.Signature('s',('U',),()); t=K.scale(0,K.loc('missing'))
        with self.assertRaises(AuditError): value(t,sig,{})
        with self.assertRaises(K.SemanticError): K.infer(t,sig)

    def test_lexical_captured_value_survives_shadowing(self):
        sig=K.Signature('s',('U',),(('x','U'),('y','U')))
        t=K.let('h',K.src('x'),K.let('k',K.loc('h'),K.let('h',K.src('y'),K.maximum(K.loc('k'),K.num(0)))))
        self.assertEqual(value(t,sig,dict(x=2,y=-3)),2)
        self.assertTrue(K.same_difference(t,K.num(0),K.maximum(K.src('x'),K.num(0)),K.num(0),sig))

    def test_lexical_rhs_uses_old_environment(self):
        sig=K.Signature('s',('U',),(('x','U'),))
        t=K.let('h',K.src('x'),K.let('h',K.add(K.loc('h'),K.num(1)),K.loc('h')))
        self.assertEqual(value(t,sig,dict(x=2)),3)

    def test_same_node_under_two_bindings_does_not_cancel(self):
        sig=K.Signature('s',('U',),()); child=K.maximum(K.loc('h'),K.num(0))
        a=K.let('h',K.num(1),child); b=K.let('h',K.num(0),child)
        self.assertEqual(value(K.sub(a,b),sig,{}),1)
        self.assertFalse(K.same_difference(a,b,K.num(0),K.num(0),sig))

    def test_conversion_and_budget(self):
        ctx,p=native_catalogue(); n=next(s for s in p.steps if s.rule=='convert')
        self.assertEqual(n.budget,2)
        self.assertEqual(reference_denotation(n.new,ctx.signature,dict(x=1,y=0)),(F(2),'V'))

    def test_nonreciprocal_conversion_not_identity(self):
        sig=K.Signature('s',('U','V'),(('x','U'),),
            (K.Conversion('uv','U','V',F(2)),K.Conversion('vu','V','U',F(3))))
        t=K.convert('vu',K.convert('uv',K.src('x')))
        self.assertEqual(value(t,sig,dict(x=1)),6)
        self.assertFalse(K.same_difference(t,K.src('x'),K.num(0),K.num(0),sig))

    def test_receiver_accepts_exact_request(self):
        c,p=self.simple(); root=receive(c,p,request(c,'h',K.src('x'),K.num(0),1))
        self.assertEqual(root.budget,1)

    def test_receiver_accepts_weaker_budget(self):
        c,p=self.simple(); self.assertEqual(receive(c,p,request(c,'h',K.src('x'),K.num(0),2)).budget,1)

    def test_receiver_rejects_stronger_request(self):
        c,p=self.simple(); K.check(c,p)
        with self.assertRaises(AuditError): receive(c,p,request(c,'h',K.src('x'),K.num(0),0))

    def test_receiver_rejects_wrong_pair(self):
        c,p=self.simple()
        with self.assertRaises(AuditError): receive(c,p,request(c,'h',K.num(2),K.num(0),1))

    def test_receiver_rejects_local_as_global(self):
        c,p=self.simple()
        with self.assertRaises(AuditError): receive(c,p,request(c,None,K.src('x'),K.num(0),1))

    def test_receiver_rejects_stale_request(self):
        c,p=self.simple(); r=request(c,'h',K.src('x'),K.num(0),1)
        with self.assertRaises(AuditError): receive(c,p,replace(r,context_id='stale'))

    def test_receiver_rejects_wrong_unit(self):
        c,p=self.simple()
        with self.assertRaises(AuditError): receive(c,p,request(c,'h',K.src('x'),K.num(0),1,'V'))

    def test_receiver_literal_matching_is_conservative(self):
        c,p=self.simple()
        with self.assertRaises(AuditError): receive(c,p,request(c,'h',K.add(K.src('x'),K.num(0)),K.num(0),1))

    def test_case_union_uses_maximum(self):
        c,p,_=case_example(); self.assertEqual(K.check(c,p).budget,1)
        audit_points(c,p,[dict(x=0),dict(x=1)])
        nodes=list(p.steps); nodes[-1]=replace(nodes[-1],budget=F(0))
        with self.assertRaises(K.ProofError): K.check(c,K.Proof(tuple(nodes),p.root))

    def test_local_membership_not_union_coverage(self):
        c,p,ids=case_example(); local=K.Proof(p.steps,ids[0]); root=K.check(c,local)
        x=dict(x=1)
        self.assertTrue(any(case_feasible(c,h.name,x) for h in c.cases))
        self.assertFalse(case_feasible(c,root.case,x))
        self.assertGreater(value(root.new,c.signature,x)-value(root.old,c.signature,x),root.budget)
        with self.assertRaises(AuditError): receive(c,local,request(c,None,root.new,root.old,0))

    def test_missing_case_is_rejected(self):
        c,p,_=case_example(); nodes=list(p.steps)
        nodes[-1]=replace(nodes[-1],parents=(nodes[-1].parents[0],))
        with self.assertRaises(K.ProofError): K.check(c,K.Proof(tuple(nodes),p.root))

    def test_nonempty_context_guard(self):
        c,_=self.simple()
        with self.assertRaises(K.SemanticError): replace(c,cases=()).validate()

    def test_infeasible_witness_rejected(self):
        c,_=self.simple(); h=replace(c.cases[0],witness=(('x',F(2)),))
        with self.assertRaises(K.SemanticError): replace(c,cases=(h,)).validate()

    def test_cycle_reference_rejected(self):
        c,p=self.simple(); nodes=list(p.steps); nodes[-1]=replace(nodes[-1],parents=(len(nodes)-1,))
        with self.assertRaises(K.ProofError): K.check(c,K.Proof(tuple(nodes),p.root))

    def test_negative_scaling_rule_rejected(self):
        c,p=self.simple(); b=K.Builder(c,'h'); i=b.row(0); b.scale(-1,i)
        with self.assertRaises(K.ProofError): K.check(c,b.proof())

    def test_duplicate_row_contribution_not_deduplicated(self):
        c,_=self.simple(); b=K.Builder(c,'h'); i=b.row(0); b.add(i,i); p=b.proof()
        self.assertEqual(K.check(c,p).budget,2)
        nodes=list(p.steps); nodes[-1]=replace(nodes[-1],budget=F(1))
        with self.assertRaises(K.ProofError): K.check(c,K.Proof(tuple(nodes),p.root))

    def test_residual_zero_floor_is_necessary(self):
        c=K.context((),(),{},scope='zero'); b=K.Builder(c,'h')
        i=b.constant(K.num(1),K.num(2)); j=b.constant(K.num(0),K.num(0)); b.res_congruence(i,j)
        p=b.proof(); self.assertEqual(K.check(c,p).budget,0)
        self.assertEqual(value(p.steps[-1].new,c.signature,{}),0)
        nodes=list(p.steps); nodes[-1]=replace(nodes[-1],budget=F(-1))
        with self.assertRaises(K.ProofError): K.check(c,K.Proof(tuple(nodes),p.root))

    def test_normalizer_is_not_complete_equality_decider(self):
        c=K.context(('x','y'),(),dict(x=0,y=0)); x,y=K.src('x'),K.src('y')
        a,b=K.minimum(x,y),K.minimum(y,x); build=K.Builder(c,'h')
        with self.assertRaises(K.ProofError): build.constant(a,b)
        i=build.lattice('min_right',x,y); j=build.lattice('min_left',x,y)
        build.min_common(i,j); proof=build.proof()
        self.assertEqual(K.check(c,proof).budget,0)
        audit_points(c,proof,[dict(x=x,y=y) for x,y in product(range(-2,3),repeat=2)])

    def test_unbounded_source_allows_negative_constant_comparison(self):
        c=K.context(('z',),(),dict(z=0)); z=K.src('z'); b=K.Builder(c,'h')
        b.constant(K.add(z,K.num(1)),K.add(z,K.num(2)))
        self.assertEqual(K.check(c,b.proof()).budget,-1)
        audit_points(c,b.proof(),[dict(z=10**100),dict(z=-10**100)])

    def test_composition_against_independent_reference(self):
        c,p=K.composition_example(); points=[]
        for theta,o1,o2 in product((F(-2),F(1,2),F(3)),(F(0),F(4)),(F(0),F(4))):
            points.append(dict(theta=theta,O1=o1,O2=o2,N1=o1+theta-F(3,4),N2=o2+F(1,4)-theta))
        self.assertEqual(K.check(c,p).budget,F(-1,2)); audit_points(c,p,points)

    def test_logistic_component_enclosure_proof(self):
        c,p=logistic_example(); self.assertEqual(K.check(c,p).budget,F(-1,8))
        points=[dict(m=-k,old=k,new=F(3,4),c=F(1,8),z=z) for k,z in product((1,2,10),(0,10**20))]
        audit_points(c,p,points)

    def test_reflective_model_independent_reference(self):
        c,p,r=reflective_example(); self.assertEqual(K.check(c,p).budget,F(-1,32))
        self.assertEqual(p.steps[r].budget,F(-5,16))
        points=[dict(p=F(a,8),s=F(b,8),e=F(1,32),z=17) for a,b in product(range(9),repeat=2)]
        audit_points(c,p,points)

    def test_graded_snapshot_all_local_tags(self):
        c,p=native_catalogue(); _,eta=row_coordinates(c,'h',dict(x=0,y=0))
        for i,node in enumerate(p.steps):
            b,_=budget_program(c,K.Proof(p.steps,i),eta); self.assertEqual(b,node.budget)

    def test_graded_bound_and_sensitivity_outside_old_source(self):
        c,_=self.simple(); b=K.Builder(c,'h'); i=b.row(0); b.add(i,i); p=b.proof()
        for x in (F(-3),F(0),F(1),F(5,4),F(100)):
            a=grade_at(c,p,(0,),dict(x=x))
            self.assertLessEqual(a['actual_difference'],a['bound'])
            self.assertGreaterEqual(a['penalty'],0)
            self.assertLessEqual(a['penalty'],a['linear_penalty'])
            self.assertEqual(a['penalty'],2*max(x-1,F(0)))

    def test_graded_penalty_vanishes_on_old_source(self):
        c,p=self.simple()
        for x in range(-5,2): self.assertEqual(grade_at(c,p,(0,),dict(x=x))['penalty'],0)

    def test_graded_rejects_failed_retained_row(self):
        c,p=self.simple()
        with self.assertRaises(AuditError): grade_at(c,p,(),dict(x=2))

    def test_graded_penalty_is_proof_relative(self):
        x=K.src('x'); c=K.context(('x',),(K.Row(x,K.num(0)),K.Row(K.scale(-1,x),K.num(0))),dict(x=0))
        b=K.Builder(c,'h'); i=b.add(b.row(0),b.row(1)); b.rewrite(i,K.num(0),K.num(0))
        direct=K.Builder(c,'h'); direct.constant(K.num(0),K.num(0))
        self.assertEqual(grade_at(c,b.proof(),(0,1),dict(x=3))['penalty'],3)
        self.assertEqual(grade_at(c,direct.proof(),(0,1),dict(x=3))['penalty'],0)

    def test_graded_reflective_discrepancy(self):
        c,p,_=reflective_example()
        x=dict(p=F(5,8),s=F(3,8),e=F(3,64),z=100)
        g=grade_at(c,p,(2,),x)
        self.assertEqual(g['bound'],F(-1,64)); self.assertEqual(g['penalty'],F(1,64))
        self.assertLessEqual(g['actual_difference'],g['bound'])

    def test_sensitivity_one_sided(self):
        c,p=native_catalogue()
        for before,after in product(((F(1),F(2),F(1),F(1)),(F(3),F(0),F(4),F(2))),repeat=2):
            for i in range(len(p.steps)):
                q=K.Proof(p.steps,i); b,L=budget_program(c,q,before); a,_=budget_program(c,q,after)
                self.assertLessEqual(a-b,sum((l*max(v-u,F(0)) for l,u,v in zip(L,before,after)),F(0)))

    def test_discharge_emitter_remains_checked(self):
        from v2.checks.f06_residual_discharge import soften_rows
        c,p=self.simple(); out=soften_rows(c,p,'h',(0,))
        root=K.check(out.context,out.proof)
        for x in (-2,0,1,2):
            self.assertLessEqual(value(root.new,out.context.signature,dict(x=x)),
                                 value(root.old,out.context.signature,dict(x=x))+root.budget)

    def test_global_grade_requires_localization(self):
        c,p,_=case_example()
        with self.assertRaises(AuditError): budget_program(c,p,(0,0))

    def test_point_grid_outside_domain_does_not_count(self):
        c,p=self.simple()
        with self.assertRaises(AuditError): audit_points(c,p,[dict(x=2)])

    def test_adaptive_context_selection_can_destroy_marginal_coverage(self):
        covers=[sum(F(int(0 <= (-1 if d==j else 1)),20) for d in range(20)) for j in range(20)]
        self.assertEqual(set(covers),{F(19,20)})
        selected_fail=sum(F(int(0 > -1),20) for d in range(20))
        self.assertEqual(selected_fail,1)

    def test_conditional_on_issuance_not_same_error_rate(self):
        alpha=F(1,20); issuance=alpha; joint_failure=alpha
        self.assertEqual(joint_failure/issuance,1); self.assertLessEqual(joint_failure,alpha)

    def test_expected_max_not_max_of_expected(self):
        a=(F(0),F(2)); b=(F(2),F(0))
        self.assertEqual(max(sum(a)/2,sum(b)/2),1)
        self.assertEqual(sum(max(x,y) for x,y in zip(a,b))/2,2)

    def test_conditional_branch_rates_not_marginal_potential_rates(self):
        potential0=[0,1]; potential1=[1,0]
        selected=[potential1[0],potential0[1]]
        self.assertEqual(F(sum(selected),2),1)
        self.assertEqual(F(sum(potential0),2),F(1,2)); self.assertEqual(F(sum(potential1),2),F(1,2))
        independent=[(potential0[u] if a==0 else potential1[u]) for u,a in product((0,1),repeat=2)]
        self.assertEqual(F(sum(independent),4),F(1,2))

    def test_evidence_and_future_failure_probability_bridge(self):
        b,alpha=F(7,16),F(1,20)
        self.assertEqual(b+(1-b)*alpha,F(149,320)); self.assertLess(b+(1-b)*alpha,b+alpha)

    def test_contradictory_requirements_have_nonzero_violation_cost(self):
        c=K.context(('x',),(),dict(x=F(1,2))); x=K.src('x'); one_minus=K.sub(K.num(1),x)
        b=K.Builder(c,'h'); i=b.lattice('max_left',x,K.num(0)); j=b.lattice('max_left',one_minus,K.num(0))
        q=b.add(i,j); loss=K.add(K.maximum(x,K.num(0)),K.maximum(one_minus,K.num(0)))
        q=b.rewrite(q,K.num(1),loss); self.assertEqual(K.check(c,b.proof(q)).budget,0)
        audit_points(c,b.proof(q),[dict(x=F(k,2)) for k in range(-8,9)])
        self.assertEqual(value(loss,c.signature,dict(x=F(1,2))),1)

    def test_report_is_deterministic(self):
        self.assertEqual(json.dumps(report(),sort_keys=True),json.dumps(report(),sort_keys=True))


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    text=json.dumps(report(),indent=2,sort_keys=True)+'\n'
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True); args.json.write_text(text,encoding='utf-8')
    else: print(text,end='')


if __name__=='__main__': main()
