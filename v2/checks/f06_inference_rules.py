"""Exact audit checker for F06's first rule set, not a general proof searcher.

The checker inspects rule syntax and exact arithmetic. F05's point evaluator
checks source-witness feasibility and finite reference cases, not universal
conclusions of purported proofs.
Python 3.10+, standard library only. All coefficients are rational.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
import json
from pathlib import Path
import unittest

from v2.checks.f05_semantics import (
    SemanticError, Signature, Conversion, Context, Case, Row, Term, rat,
    num, src, loc, add, sub, scale, minimum, maximum, residual, absolute,
    let, convert, infer, affine, evaluate, fingerprint, serial,
)


class ProofError(ValueError):
    """Rejected proof input, not a semantic countermodel."""


def _form(t: Term, sig: Signature):
    """Exact linear collection with lexically instantiated nonlinear atoms.

    Residual unfolds its defining max(b-a,0). No sampled equality, optimization,
    active-region assumption, or source-equivalence oracle is used.
    """
    infer(t, sig)  # Check every child, including those multiplied by zero.

    def make(items, c):
        return (tuple(sorted(((k, v) for k, v in items.items() if v), key=lambda z: repr(z[0]))), c)

    def plus(a, b):
        d = dict(a[0])
        for k, v in b[0]: d[k] = d.get(k, F(0)) + v
        return make(d, a[1] + b[1])

    def mul(k, a):
        return make({key: k*v for key, v in a[0]}, k*a[1])

    def nonlinear(op, a, b):
        if not a[0] and not b[0]:
            return ((), min(a[1], b[1]) if op == 'min' else max(a[1], b[1]))
        return (((((op, a, b)), F(1)),), F(0))

    def go(n, env):
        if n.op == 'const': return ((), rat(n.value))
        if n.op == 'source': return (((('source', n.name), F(1)),), F(0))
        if n.op == 'local': return env[n.name]
        if n.op == 'let':
            value = go(n.args[0], env)
            return go(n.args[1], {**env, n.name: value})
        a = go(n.args[0], env)
        if n.op == 'scale': return mul(rat(n.value), a)
        if n.op == 'convert': return mul(rat(sig.conversion(n.name).factor), a)
        b = go(n.args[1], env)
        if n.op == 'add': return plus(a, b)
        if n.op == 'res': return nonlinear('max', plus(b, mul(F(-1), a)), ((), F(0)))
        return nonlinear(n.op, a, b)

    return go(t, {})


def same_difference(t: Term, s: Term, a: Term, b: Term, sig: Signature) -> bool:
    units = [infer(z, sig) for z in (t, s, a, b)]
    return len(set(units)) == 1 and _form(sub(t, s), sig) == _form(sub(a, b), sig)


def normalized_row(ctx: Context, case_name: str, index: int):
    cases = [c for c in ctx.cases if c.name == case_name]
    if len(cases) != 1 or isinstance(index, bool) or not isinstance(index, int):
        raise ProofError('Bad source case or row index.')
    if not 0 <= index < len(cases[0].rows): raise ProofError('Missing source row.')
    row = cases[0].rows[index]
    unit = infer(row.lhs, ctx.signature)
    difference = sub(row.lhs, row.rhs)
    coefficients, c = affine(difference, ctx.signature)
    direction = tuple(sorted((k, v) for k, v in coefficients.items() if v))
    return sub(difference, num(c, unit)), -c, unit, direction


@dataclass(frozen=True)
class Step:
    rule: str
    parents: tuple[int, ...]
    case: str | None
    new: Term
    old: Term
    budget: F
    context_id: str
    data: tuple = ()


@dataclass(frozen=True)
class Proof:
    steps: tuple[Step, ...]
    root: int


def _expected(ctx: Context, step: Step, earlier: list[Step]):
    """Check one local constructor; return its exact expected pair and budget."""
    p = []
    for i in step.parents:
        if isinstance(i, bool) or not isinstance(i, int) or not 0 <= i < len(earlier):
            raise ProofError('Premise references must point strictly backward.')
        p.append(earlier[i])
    rule, data = step.rule, step.data
    counts = {'constant':0, 'row':0, 'rewrite':1, 'trans':2, 'add':2,
              'scale':1, 'negate':1, 'convert':1, 'slack':1, 'meet_proofs':2,
              'max_common':2, 'min_common':2, 'congruence':2, 'res_congruence':2,
              'lattice':0, 'all_cases':None}
    if rule not in counts: raise ProofError('Unknown rule.')
    if counts[rule] is not None and len(p) != counts[rule]: raise ProofError('Wrong premise arity.')
    if rule != 'all_cases' and any(q.case != step.case for q in p):
        raise ProofError('Mixing hidden cases or local/global premises.')
    u = infer(step.new, ctx.signature)
    z = num(0, u)
    if rule == 'constant':
        if data: raise ProofError('Unexpected constant-rule data.')
        form = _form(sub(step.new, step.old), ctx.signature)
        if form[0]: raise ProofError('Difference is not an exact constant.')
        return step.new, step.old, form[1]
    if rule == 'row':
        if len(data) != 1 or step.case is None: raise ProofError('Row needs a local case and index.')
        t, b, ru, _ = normalized_row(ctx, step.case, data[0])
        return t, num(0, ru), b
    if rule == 'rewrite':
        if data: raise ProofError('Unexpected rewrite data.')
        return p[0].new, p[0].old, p[0].budget
    if rule == 'trans':
        if data or not same_difference(p[0].old, p[1].new, z, z, ctx.signature):
            raise ProofError('Transitivity middle terms do not match.')
        return p[0].new, p[1].old, p[0].budget+p[1].budget
    if rule == 'add':
        if data: raise ProofError('Unexpected addition data.')
        return add(p[0].new,p[1].new), add(p[0].old,p[1].old), p[0].budget+p[1].budget
    if rule == 'scale':
        if len(data) != 1 or rat(data[0]) < 0: raise ProofError('Nonnegative rational scale required.')
        k=rat(data[0]); return scale(k,p[0].new),scale(k,p[0].old),k*p[0].budget
    if rule == 'negate':
        if data: raise ProofError('Unexpected negation data.')
        return scale(-1,p[0].old),scale(-1,p[0].new),p[0].budget
    if rule == 'convert':
        if len(data) != 1: raise ProofError('Named conversion required.')
        c=ctx.signature.conversion(data[0])
        return convert(c.name,p[0].new),convert(c.name,p[0].old),rat(c.factor)*p[0].budget
    if rule == 'slack':
        if len(data) != 1 or rat(data[0]) < 0: raise ProofError('Fixed nonnegative slack required.')
        return p[0].new,p[0].old,p[0].budget+rat(data[0])
    if rule == 'meet_proofs':
        if data or not same_difference(p[0].new,p[0].old,p[1].new,p[1].old,ctx.signature):
            raise ProofError('Proof minimum requires an identical query.')
        return p[0].new,p[0].old,min(p[0].budget,p[1].budget)
    if rule in ('max_common','min_common'):
        left,right=(p[0].old,p[1].old) if rule=='max_common' else (p[0].new,p[1].new)
        if data or not same_difference(left,right,z,z,ctx.signature):
            raise ProofError('Common comparison term missing.')
        if rule=='max_common': return maximum(p[0].new,p[1].new),p[0].old,max(q.budget for q in p)
        return p[0].new,minimum(p[0].old,p[1].old),max(q.budget for q in p)
    if rule == 'congruence':
        if len(data)!=1 or data[0] not in ('min','max'): raise ProofError('Unknown lattice operation.')
        op=minimum if data[0]=='min' else maximum
        return op(p[0].new,p[1].new),op(p[0].old,p[1].old),max(q.budget for q in p)
    if rule == 'res_congruence':
        if data: raise ProofError('Unexpected residual data.')
        return residual(p[0].old,p[1].new),residual(p[0].new,p[1].old),max(p[0].budget+p[1].budget,F(0))
    if rule == 'lattice':
        if len(data)!=3 or data[0] not in ('min_left','min_right','max_left','max_right'):
            raise ProofError('Invalid lattice projection/injection.')
        kind,a,b=data
        if kind=='min_left': return minimum(a,b),a,F(0)
        if kind=='min_right': return minimum(a,b),b,F(0)
        if kind=='max_left': return a,maximum(a,b),F(0)
        return b,maximum(a,b),F(0)
    if rule == 'all_cases':
        if data or step.case is not None: raise ProofError('Global rule has no local case.')
        names=[q.case for q in p]
        if len(names)!=len(set(names)) or set(names)!={c.name for c in ctx.cases}:
            raise ProofError('Every live hidden case is required exactly once.')
        if any(not same_difference(step.new,step.old,q.new,q.old,ctx.signature) for q in p):
            raise ProofError('Case proofs disagree on their query.')
        # Exact same expression pair makes the no-hidden-policy convention explicit.
        if any((q.new,q.old)!=(step.new,step.old) for q in p):
            raise ProofError('This audit requires the same expression pair in every case.')
        return step.new,step.old,max(q.budget for q in p)
    raise ProofError('Unreachable rule.')


def check(ctx: Context, proof: Proof) -> Step:
    ctx.validate(); context_id=fingerprint(ctx)
    if (not proof.steps or isinstance(proof.root,bool) or not isinstance(proof.root,int)
            or not 0<=proof.root<len(proof.steps)):
        raise ProofError('Missing root.')
    seen=[]
    for step in proof.steps:
        if step.context_id!=context_id: raise ProofError('Stale or different context.')
        if step.case is not None and step.case not in {c.name for c in ctx.cases}:
            raise ProofError('Unknown hidden case.')
        b=rat(step.budget)
        if infer(step.new,ctx.signature)!=infer(step.old,ctx.signature):
            raise ProofError('Mixed-unit comparison.')
        t,s,expected=_expected(ctx,step,seen)
        if b!=expected or not same_difference(step.new,step.old,t,s,ctx.signature):
            raise ProofError('Conclusion or budget does not follow from this rule.')
        seen.append(step)
    return proof.steps[proof.root]


class Builder:
    """Convenience construction; check() still validates the emitted claims."""
    def __init__(self,ctx:Context,case:str|None=None):
        self.ctx=ctx; self.case=case; self.steps=[]; self.cid=fingerprint(ctx)
    def emit(self,rule,parents,new,old,budget,data=(),case='default'):
        c=self.case if case=='default' else case
        self.steps.append(Step(rule,tuple(parents),c,new,old,rat(budget),self.cid,tuple(data)))
        return len(self.steps)-1
    def constant(self,t,s):
        f=_form(sub(t,s),self.ctx.signature)
        if f[0]: raise ProofError('Not constant.')
        return self.emit('constant',(),t,s,f[1])
    def row(self,i):
        t,b,u,_=normalized_row(self.ctx,self.case,i)
        return self.emit('row',(),t,num(0,u),b,(i,))
    def rewrite(self,i,t,s): return self.emit('rewrite',(i,),t,s,self.steps[i].budget)
    def add(self,i,j):
        a,b=self.steps[i],self.steps[j]
        return self.emit('add',(i,j),add(a.new,b.new),add(a.old,b.old),a.budget+b.budget)
    def scale(self,k,i):
        a=self.steps[i]; return self.emit('scale',(i,),scale(k,a.new),scale(k,a.old),rat(k)*a.budget,(rat(k),))
    def negate(self,i):
        a=self.steps[i]; return self.emit('negate',(i,),scale(-1,a.old),scale(-1,a.new),a.budget)
    def conversion(self,name,i):
        a=self.steps[i]; k=self.ctx.signature.conversion(name).factor
        return self.emit('convert',(i,),convert(name,a.new),convert(name,a.old),k*a.budget,(name,))
    def slack(self,k,i):
        a=self.steps[i]; return self.emit('slack',(i,),a.new,a.old,a.budget+rat(k),(rat(k),))
    def trans(self,i,j):
        a,b=self.steps[i],self.steps[j]
        return self.emit('trans',(i,j),a.new,b.old,a.budget+b.budget)
    def meet(self,i,j):
        a,b=self.steps[i],self.steps[j]
        return self.emit('meet_proofs',(i,j),a.new,a.old,min(a.budget,b.budget))
    def max_common(self,i,j):
        a,b=self.steps[i],self.steps[j]
        return self.emit('max_common',(i,j),maximum(a.new,b.new),a.old,max(a.budget,b.budget))
    def min_common(self,i,j):
        a,b=self.steps[i],self.steps[j]
        return self.emit('min_common',(i,j),a.new,minimum(a.old,b.old),max(a.budget,b.budget))
    def congruence(self,kind,i,j):
        a,b=self.steps[i],self.steps[j]; op=minimum if kind=='min' else maximum
        return self.emit('congruence',(i,j),op(a.new,b.new),op(a.old,b.old),max(a.budget,b.budget),(kind,))
    def res_congruence(self,i,j):
        a,b=self.steps[i],self.steps[j]
        return self.emit('res_congruence',(i,j),residual(a.old,b.new),residual(a.new,b.old),max(a.budget+b.budget,F(0)))
    def lattice(self,kind,a,b):
        pairs={'min_left':(minimum(a,b),a),'min_right':(minimum(a,b),b),
               'max_left':(a,maximum(a,b)),'max_right':(b,maximum(a,b))}
        t,s=pairs[kind]; return self.emit('lattice',(),t,s,F(0),(kind,a,b))
    def all_cases(self,ids):
        a=self.steps[ids[0]]
        return self.emit('all_cases',ids,a.new,a.old,max(self.steps[i].budget for i in ids),case=None)
    def proof(self,root=None):
        return Proof(tuple(self.steps),len(self.steps)-1 if root is None else root)


def replay(old:Context,new:Context,proof:Proof)->Proof:
    """RHS-only replay; no row insertion, withdrawal, policy or matrix change."""
    check(old,proof); new.validate()
    if old.signature!=new.signature or old.observation!=new.observation:
        raise ProofError('Source meanings/units/observation changed.')
    if [c.name for c in old.cases]!=[c.name for c in new.cases]:
        raise ProofError('Live case schema changed.')
    for a,b in zip(old.cases,new.cases):
        if len(a.rows)!=len(b.rows): raise ProofError('Row schema changed.')
        for i in range(len(a.rows)):
            x=normalized_row(old,a.name,i); y=normalized_row(new,b.name,i)
            if x[2:]!=y[2:]: raise ProofError('Row direction or unit changed.')
    steps=[]; cid=fingerprint(new)
    for oldstep in proof.steps:
        step=replace(oldstep,context_id=cid)
        _,_,budget=_expected(new,step,steps)
        steps.append(replace(step,budget=budget))
    result=Proof(tuple(steps),proof.root)
    check(new,result)
    return result


def context(names,rows,witness,*,scope='F06-audit-v1',revision='v1',units=('U',),conversions=()):
    sig=Signature(scope,units,tuple((x,'U') if isinstance(x,str) else x for x in names),conversions)
    c=Context(sig,'fixed-visible-observation',revision,(Case('h',tuple(rows),tuple((k,rat(v)) for k,v in witness.items())),))
    c.validate(); return c


def composition_example():
    n1,n2,o1,o2,t=map(src,('N1','N2','O1','O2','theta'))
    rows=(Row(sub(sub(n1,o1),t),num(F(-3,4))),Row(add(sub(n2,o2),t),num(F(1,4))))
    ctx=context(('N1','N2','O1','O2','theta'),rows,dict(N1=F(3,4),N2=F(3,4),O1=1,O2=1,theta=F(1,2)))
    b=Builder(ctx,'h'); i=b.add(b.row(0),b.row(1)); b.rewrite(i,add(n1,n2),add(o1,o2))
    return ctx,b.proof()


def absolute_example():
    y,c,z=map(src,('y','c','z'))
    ctx=context(('y','c','z'),(Row(scale(-1,y),num(F(-3,4))),Row(c,num(F(1,4))),Row(num(0),c),Row(num(0),z)),dict(y=F(3,4),c=F(1,4),z=0))
    b=Builder(ctx,'h')
    i=b.scale(2,b.row(0)); j=b.constant(num(1),num(0)); i=b.add(i,j)
    i=b.rewrite(i,sub(num(1),y),y)
    j=b.constant(sub(y,num(1)),y)
    k=b.max_common(j,i)
    k=b.trans(k,b.lattice('max_left',y,scale(-1,y)))
    k=b.add(k,b.row(1)); k=b.add(k,b.constant(z,z))
    b.rewrite(k,add(absolute(sub(y,num(1))),add(c,z)),add(absolute(y),z))
    return ctx,b.proof()


def reflection_example(plus=F(1,2),minus=F(-1,2),e_bound=F(1,32),revision='v1',factor=F(1)):
    p,s,e,z,w=map(src,('p','s','e','z','w'))
    conversions=(Conversion('failure_cost','P','L',F(1)),Conversion('proxy_value','L','J',factor))
    rows=(Row(sub(p,s),num(plus,'P')),Row(sub(s,p),num(minus,'P')),Row(s,num(F(1,4),'P')),
          Row(e,num(e_bound,'J')),Row(num(0,'P'),s),Row(num(0,'P'),p),Row(p,num(1,'P')))
    ctx=context((('p','P'),('s','P'),('e','J'),('z','L'),('w','J')),rows,dict(p=F(1,2),s=0,e=0,z=0,w=0),scope='SELF-MIX-v1-cost-v1',revision=revision,units=('P','L','J'),conversions=conversions)
    b=Builder(ctx,'h'); roots={}
    def h(r): return add(scale(1-r,p),scale(r,s))
    for label,r in [('old_report',F(1,2)),('new_report',F(3,4))]:
        i=b.add(b.scale(1-r,b.row(0)),b.row(2))
        i=b.add(i,b.constant(num(-r,'P'),num(0,'P')))
        roots[label]=b.rewrite(i,h(r),num(r,'P'))
    def loss(r): return add(convert('failure_cost',h(r)),add(num(r/4,'L'),z))
    i=b.conversion('failure_cost',b.scale(F(1,4),b.row(1)))
    i=b.add(i,b.constant(num(F(1,16),'L'),num(0,'L')))
    roots['proxy']=b.rewrite(i,loss(F(3,4)),loss(F(1,2)))
    i=b.conversion('proxy_value',i); i=b.add(i,b.row(3))
    jnew=add(convert('proxy_value',loss(F(3,4))),add(w,e))
    jold=add(convert('proxy_value',loss(F(1,2))),w)
    roots['intended']=b.rewrite(i,jnew,jold)
    return ctx,b.proof(),roots


def quadratic_example():
    t,q,z=map(src,('theta','q','z')); cases=[]; endpoints=[F(1,4),F(3,8),F(1,2),F(5,8),F(3,4)]
    for j,(a,c) in enumerate(zip(endpoints,endpoints[1:])):
        rows=(Row(sub(q,scale(a+c,t)),num(-a*c)),Row(scale(-1,t),num(-a)),Row(t,num(c)),Row(num(0),q),Row(num(0),z))
        cases.append(Case(str(j),rows,(('theta',a),('q',a*a),('z',F(0)))))
    ctx=Context(Signature('quadratic-component-v1',('U',),(('theta','U'),('q','U'),('z','U'))),'same-policy','v1',tuple(cases))
    b=Builder(ctx); ids=[]
    for j,(a,c) in enumerate(zip(endpoints,endpoints[1:])):
        b.case=str(j); k=a+c
        i=b.add(b.row(0),b.scale(abs(k-1),b.row(1 if k<=1 else 2)))
        ids.append(b.rewrite(i,add(q,z),add(t,z)))
    b.all_cases(ids); return ctx,b.proof(),ids


def mixture_example():
    a,b,z=map(src,('A','B','B0')); sig=Signature('fresh-mixture-v1',('U',),(('A','U'),('B','U'),('B0','U')))
    cases=[]
    for name,x,y in [('h1',F(-2),F(0)),('h2',F(0),F(-2))]:
        cases.append(Case(name,(Row(sub(a,z),num(x)),Row(sub(b,z),num(y))),(('A',x+2),('B',y+2),('B0',F(2)))))
    ctx=Context(sig,'no-hidden-signal','v1',tuple(cases)); build=Builder(ctx); ids=[]
    for h in ctx.cases:
        build.case=h.name; i=build.add(build.scale(F(1,2),build.row(0)),build.scale(F(1,2),build.row(1)))
        ids.append(build.rewrite(i,scale(F(1,2),add(a,b)),z))
    build.all_cases(ids); return ctx,build.proof()


def consumer_example(budget=F(-1,4)):
    t,s=src('t'),src('s'); ctx=context(('t','s'),(Row(sub(t,s),num(budget)),),dict(t=budget,s=0))
    b=Builder(ctx,'h'); i=b.rewrite(b.row(0),t,s); j=b.constant(num(0),num(0))
    r=b.res_congruence(j,i); out=b.add(b.scale(2,i),r)
    b.rewrite(out,add(scale(2,t),residual(num(0),t)),add(scale(2,s),residual(num(0),s)))
    return ctx,b.proof()


def self_bound_example():
    u=src('u'); ctx=context(('u',),(),{'u':0}); b=Builder(ctx,'h')
    a=add(num(F(-3,4)),u); c=sub(num(F(-1,4)),u); m=minimum(a,c)
    i=b.add(b.lattice('min_left',a,c),b.lattice('min_right',a,c)); i=b.scale(F(1,2),i)
    i=b.rewrite(i,m,num(F(-1,2))); i=b.trans(i,b.constant(num(F(-1,2)),num(0)))
    return ctx,b.proof()


def report_portfolio_example(a=F(9,10),sbound=F(9,10),r=F(10,11)):
    p,s=src('p'),src('s'); ctx=context(('p','s'),(Row(sub(p,s),num(a)),Row(s,num(sbound)),Row(p,num(1)),Row(num(0),s),Row(num(0),p)),{'p':min(F(1),a+sbound),'s':sbound})
    b=Builder(ctx,'h'); H=add(scale(1-r,p),scale(r,s))
    i=b.add(b.scale(1-r,b.row(0)),b.row(1)); i=b.rewrite(i,H,num(0))
    j=b.add(b.scale(1-r,b.row(2)),b.scale(r,b.row(1))); j=b.rewrite(j,H,num(0))
    k=b.meet(i,j); k=b.add(k,b.constant(num(-r),num(0))); b.rewrite(k,H,num(r))
    return ctx,b.proof(),(i,j)


def report_transfer_example():
    ctx,proof,roots=reflection_example(plus=F(9,16),revision='report-update-v2')
    b=Builder(ctx,'h'); b.steps=list(proof.steps)
    p,s=src('p'),src('s')
    h0=add(scale(F(1,2),p),scale(F(1,2),s))
    h1=add(scale(F(1,4),p),scale(F(3,4),s))
    i=b.scale(F(1,4),b.row(1)); i=b.rewrite(i,h1,h0)
    i=b.trans(i,roots['old_report'])
    j=b.constant(num(F(1,2),'P'),num(F(3,4),'P'))
    transferred=b.trans(i,j)
    b.meet(transferred,roots['new_report'])
    return ctx,b.proof(),transferred


def examples():
    result={}
    for name,fun in [('component_composition',composition_example),('absolute_loss',absolute_example),
                     ('hidden_case_mixture',mixture_example),('signed_consumer',consumer_example),
                     ('reasoner_self_model',self_bound_example)]:
        ctx,p=fun(); result[name]=(ctx,p)
    ctx,p,roots=reflection_example()
    for name,root in roots.items(): result['reflection_'+name]=(ctx,replace(p,root=root))
    ctx,p,_=quadratic_example(); result['quadratic_enclosure']=(ctx,p)
    ctx,p,_=report_portfolio_example(); result['report_portfolio']=(ctx,p)
    ctx,p,_=report_transfer_example(); result['report_transfer']=(ctx,p)
    return result


def reference_holds(ctx:Context,proof:Proof,point,case:str)->bool:
    """A single hypothetical assignment, not proof acceptance or universality."""
    root=proof.steps[proof.root]
    if root.case not in (None,case) or not ctx.feasible(case,point): raise ProofError('Not an admitted reference point.')
    return evaluate(root.new,ctx.signature,point)-evaluate(root.old,ctx.signature,point)<=root.budget


class F06InferenceTests(unittest.TestCase):
    def bad(self,ctx,p,index=-1,**changes):
        steps=list(p.steps); steps[index]=replace(steps[index],**changes)
        with self.assertRaises((ProofError,SemanticError)):
            check(ctx,Proof(tuple(steps),p.root))

    def test_all_worked_proofs(self):
        expected={'component_composition':F(-1,2),'absolute_loss':F(-1,4),'hidden_case_mixture':F(-1),
                  'signed_consumer':F(-1,2),'reasoner_self_model':F(-1,2),'reflection_old_report':F(0),
                  'reflection_new_report':F(-3,8),'reflection_proxy':F(-1,16),'reflection_intended':F(-1,32),
                  'quadratic_enclosure':F(-3,16),'report_portfolio':F(0),'report_transfer':F(-23,64)}
        for name,(ctx,p) in examples().items(): self.assertEqual(check(ctx,p).budget,expected[name],name)

    def test_every_node_at_supplied_witness(self):
        for _,(ctx,p) in examples().items():
            check(ctx,p)
            for node in p.steps:
                for case in ctx.cases:
                    if node.case in (None,case.name):
                        point=dict(case.witness)
                        self.assertLessEqual(evaluate(node.new,ctx.signature,point)-evaluate(node.old,ctx.signature,point),node.budget)

    def test_component_contracts_not_final_scores(self):
        ctx,p=composition_example()
        self.assertEqual(len(ctx.cases[0].rows),2)
        self.assertEqual([x.rule for x in p.steps],['row','row','add','rewrite'])
        self.assertEqual(check(ctx,p).budget,F(-1,2))

    def test_component_sharing_countermodel(self):
        self.assertEqual((F(1)-F(3,4))+(F(1,4)-F(0)),F(1,2))
        self.assertEqual((F(1)-F(3,4))+(F(1,4)-F(1)),F(-1,2))

    def test_absolute_loss_unbounded_baseline(self):
        ctx,p=absolute_example()
        for y in (F(3,4),F(1),F(100000)):
            for z in (F(0),F(10)**50): self.assertTrue(reference_holds(ctx,p,{'y':y,'c':F(1,4),'z':z},'h'))

    def test_absolute_loss_domain_needed(self):
        self.assertEqual(abs(F(0)-1)+F(1,4)-abs(F(0)),F(5,4))

    def test_reflection_grid(self):
        ctx,p,roots=reflection_example()
        for k in range(9):
            s=F(k,32)
            point={'p':s+F(1,2),'s':s,'e':F(1,32),'z':F(10)**30,'w':-F(10)**40}
            for r in roots.values(): self.assertTrue(reference_holds(ctx,replace(p,root=r),point,'h'))

    def test_reflection_replay_discrepancy(self):
        old,p,roots=reflection_example(); new,_,_=reflection_example(e_bound=F(3,64),revision='v2')
        q=replay(old,new,p)
        self.assertEqual(q.steps[roots['intended']].budget,F(-1,64))
        self.assertEqual(q.steps[roots['old_report']].budget,0)

    def test_reflection_replay_two_rows(self):
        old,p,roots=reflection_example(); new,_,_=reflection_example(minus=F(-7,16),e_bound=F(3,64),revision='v2')
        self.assertEqual(replay(old,new,p).steps[roots['intended']].budget,0)

    def test_reflection_report_lapse_does_not_erase_paired_bound(self):
        old,p,roots=reflection_example(); new,_,_=reflection_example(plus=F(9,16),revision='v2')
        q=replay(old,new,p)
        self.assertEqual(q.steps[roots['old_report']].budget,F(1,32))
        self.assertEqual(q.steps[roots['new_report']].budget,F(-23,64))
        self.assertEqual(q.steps[roots['intended']].budget,F(-1,32))

    def test_reflection_changed_factor_rejected(self):
        old,p,_=reflection_example(); new,q,_=reflection_example(factor=F(1,4),revision='v2')
        with self.assertRaises(ProofError): replay(old,new,p)
        self.assertEqual(check(new,q).budget,F(1,64))

    def test_reflection_invalid_old_report_point(self):
        ctx,p,roots=reflection_example(plus=F(9,16),revision='v2')
        values=dict(p=F(13,16),s=F(1,4),e=0,z=0,w=0)
        self.assertTrue(ctx.feasible('h',values))
        r=p.steps[roots['old_report']]
        self.assertEqual(evaluate(r.new,ctx.signature,values)-evaluate(r.old,ctx.signature,values),F(1,32))

    def test_quadratic_case_budgets(self):
        ctx,p,ids=quadratic_example()
        self.assertEqual([p.steps[i].budget for i in ids],[F(-3,16),F(-15,64),F(-15,64),F(-3,16)])
        self.assertEqual(check(ctx,p).budget,F(-3,16))

    def test_quadratic_reference_dense_grid(self):
        ctx,p,_=quadratic_example()
        for case in ctx.cases:
            j=int(case.name); lo=F(2+j,8); hi=lo+F(1,8)
            for k in range(9):
                t=lo+(hi-lo)*F(k,8)
                self.assertTrue(reference_holds(ctx,p,{'theta':t,'q':t*t,'z':F(10)**20},case.name))

    def test_missing_hidden_case_rejected(self):
        ctx,p,_=quadratic_example(); self.bad(ctx,p,parents=p.steps[-1].parents[:-1])

    def test_duplicate_hidden_case_rejected(self):
        ctx,p,_=quadratic_example(); ids=p.steps[-1].parents
        self.bad(ctx,p,parents=(ids[0],ids[0],ids[2],ids[3]))

    def test_minimum_of_case_bounds_rejected(self):
        ctx,p,_=quadratic_example(); self.bad(ctx,p,budget=F(-15,64))

    def test_case_specific_query_not_global_policy(self):
        ctx,p,_=quadratic_example(); steps=list(p.steps)
        i=steps[-1].parents[0]; old=steps[i]
        steps[i]=replace(old,new=add(old.new,num(1)),old=add(old.old,num(1)))
        with self.assertRaises((ProofError,SemanticError)): check(ctx,Proof(tuple(steps),p.root))

    def test_same_hidden_policy_mixture_gain(self):
        ctx,p=mixture_example(); self.assertEqual(check(ctx,p).budget,-1)
        for case in ctx.cases: self.assertTrue(reference_holds(ctx,p,dict(case.witness),case.name))
        self.assertEqual((max(-2,0)+max(0,-2))/2,0)

    def test_signed_consumer_gain(self):
        for b,expected in [(F(-1,4),F(-1,2)),(F(1,4),F(3,4))]:
            ctx,p=consumer_example(b); self.assertEqual(check(ctx,p).budget,expected)
            for s in range(-5,6): self.assertTrue(reference_holds(ctx,p,{'s':s,'t':F(s)+b},'h'))

    def test_saturation_counterexample(self):
        self.assertEqual(max(-2,0)-max(-1,0),0)
        self.assertLessEqual(-2-(-1),-1)

    def test_constant_rule_negative(self):
        ctx=context(('x',),(),{'x':0}); b=Builder(ctx,'h')
        b.constant(sub(src('x'),num(7)),src('x'))
        self.assertEqual(check(ctx,b.proof()).budget,-7)

    def test_duplicate_premise_budget_doubles(self):
        ctx=context(('x',),(Row(src('x'),num(2)),),{'x':2}); b=Builder(ctx,'h')
        i=b.row(0); b.add(i,i); p=b.proof()
        self.assertEqual(check(ctx,p).budget,4); self.bad(ctx,p,budget=F(2))

    def test_transitivity_and_negative_budgets(self):
        ctx=context((),(),{}); b=Builder(ctx,'h')
        i=b.constant(num(1),num(2)); j=b.constant(num(2),num(4)); b.trans(i,j)
        self.assertEqual(check(ctx,b.proof()).budget,-3)

    def test_bad_middle_rejected(self):
        ctx=context((),(),{}); b=Builder(ctx,'h')
        i=b.constant(num(1),num(2)); j=b.constant(num(3),num(4)); b.trans(i,j)
        with self.assertRaises(ProofError): check(ctx,b.proof())

    def test_negative_scaling_rejected(self):
        ctx=context(('x',),(Row(src('x'),num(1)),),{'x':0}); b=Builder(ctx,'h')
        b.scale(-1,b.row(0))
        with self.assertRaises(ProofError): check(ctx,b.proof())

    def test_negation_reverses_pair_not_budget(self):
        ctx=context(('x',),(Row(src('x'),num(1)),),{'x':0}); b=Builder(ctx,'h')
        i=b.row(0); b.negate(i); self.assertEqual(check(ctx,b.proof()).budget,1)
        self.bad(ctx,b.proof(),budget=F(-1))

    def test_slack_replay(self):
        old=context(('x',),(Row(src('x'),num(1)),),{'x':1})
        new=context(('x',),(Row(src('x'),num(3)),),{'x':3},revision='v2')
        b=Builder(old,'h'); b.slack(1,b.row(0)); p=b.proof()
        self.assertEqual(check(old,p).budget,2)
        self.assertEqual(check(new,replay(old,new,p)).budget,4)

    def test_fixed_target_weakening_cannot_be_replayed_unchanged(self):
        old=context(('x',),(Row(src('x'),num(1)),),{'x':1})
        new=context(('x',),(Row(src('x'),num(3)),),{'x':3},revision='v2')
        b=Builder(old,'h'); b.slack(1,b.row(0)); q=replay(old,new,b.proof())
        self.bad(new,q,budget=F(2))

    def test_negative_slack_rejected(self):
        ctx=context((),(),{}); b=Builder(ctx,'h'); b.slack(-1,b.constant(num(0),num(0)))
        with self.assertRaises(ProofError): check(ctx,b.proof())

    def test_minimum_selects_a_proof(self):
        ctx=context(('x',),(Row(src('x'),num(1)),Row(src('x'),num(2))),{'x':0})
        b=Builder(ctx,'h'); b.meet(b.row(0),b.row(1)); self.assertEqual(check(ctx,b.proof()).budget,1)

    def test_minimum_different_queries_rejected(self):
        ctx=context(('x','y'),(Row(src('x'),num(1)),Row(src('y'),num(2))),{'x':0,'y':0})
        b=Builder(ctx,'h'); b.meet(b.row(0),b.row(1))
        with self.assertRaises(ProofError): check(ctx,b.proof())

    def test_all_lattice_rules(self):
        ctx=context((),(),{}); b=Builder(ctx,'h'); a,c=num(-2),num(3)
        for kind in ('min_left','min_right','max_left','max_right'): b.lattice(kind,a,c)
        i=b.constant(num(-4),num(-1)); j=b.constant(num(-3),num(-1)); b.max_common(i,j)
        i=b.constant(num(-4),num(2)); j=b.constant(num(-4),num(3)); b.min_common(i,j)
        i=b.constant(num(-2),num(1)); j=b.constant(num(-1),num(0))
        b.congruence('min',i,j); b.congruence('max',i,j)
        check(ctx,b.proof())
        for step in b.steps: self.assertLessEqual(evaluate(step.new,ctx.signature,{})-evaluate(step.old,ctx.signature,{}),step.budget)

    def test_lattice_signed_congruence_exhaustive_constants(self):
        import itertools
        ctx=context((),(),{})
        for a,b,c,d in itertools.product((-1,0,1),repeat=4):
            build=Builder(ctx,'h'); i=build.constant(num(a),num(b)); j=build.constant(num(c),num(d))
            for kind in ('min','max'):
                root=build.congruence(kind,i,j); p=build.proof(root)
                check(ctx,p); self.assertTrue(reference_holds(ctx,p,{},'h'))

    def test_residual_polarity_exhaustive_constants(self):
        import itertools
        ctx=context((),(),{})
        for ao,an,bn,bo in itertools.product((-1,0,1),repeat=4):
            b=Builder(ctx,'h'); i=b.constant(num(ao),num(an)); j=b.constant(num(bn),num(bo)); b.res_congruence(i,j)
            check(ctx,b.proof()); self.assertTrue(reference_holds(ctx,b.proof(),{},'h'))

    def test_residual_wrong_first_direction_rejected(self):
        ctx=context(('x',),(Row(src('x'),num(1)),),{'x':0}); b=Builder(ctx,'h')
        i=b.rewrite(b.row(0),src('x'),num(0)); j=b.constant(num(0),num(0)); b.res_congruence(i,j)
        self.bad(ctx,b.proof(),new=residual(src('x'),num(0)),old=residual(num(0),num(0)))

    def test_shifted_residual_encodes_negative_bound(self):
        ctx=context(('x',),(Row(src('x'),num(-1)),),{'x':-1}); b=Builder(ctx,'h')
        i=b.row(0); i=b.add(i,b.constant(num(1),num(0))); i=b.rewrite(i,add(src('x'),num(1)),num(0))
        j=b.constant(num(0),num(0)); i=b.max_common(i,j); b.rewrite(i,residual(num(-1),src('x')),num(0))
        self.assertEqual(check(ctx,b.proof()).budget,0)

    def test_lexical_opaque_atoms_not_merged(self):
        ctx=context(('x',),(),{'x':-1}); a=let('y',src('x'),minimum(loc('y'),num(0)))
        b=let('y',add(src('x'),num(1)),minimum(loc('y'),num(0)))
        self.assertNotEqual(_form(a,ctx.signature),_form(b,ctx.signature))
        proof=Proof((Step('constant',(),'h',a,b,F(0),fingerprint(ctx)),),0)
        with self.assertRaises(ProofError): check(ctx,proof)

    def test_capture_free_shadowing(self):
        ctx=context(('x',),(),{'x':2}); t=let('x',add(src('x'),num(1)),let('x',add(loc('x'),num(2)),minimum(loc('x'),num(8))))
        s=minimum(add(src('x'),num(3)),num(8)); b=Builder(ctx,'h'); b.constant(t,s)
        self.assertEqual(check(ctx,b.proof()).budget,0)

    def test_unused_ill_typed_subterm_not_erased(self):
        ctx=context((),(),{}); t=scale(0,src('missing'))
        proof=Proof((Step('constant',(),'h',t,num(0),F(0),fingerprint(ctx)),),0)
        with self.assertRaises(SemanticError): check(ctx,proof)

    def test_mixed_units_rejected(self):
        ctx=context((('x','U'),('y','V')),(),{'x':0,'y':0},units=('U','V'))
        proof=Proof((Step('constant',(),'h',src('x'),src('y'),F(0),fingerprint(ctx)),),0)
        with self.assertRaises((ProofError,SemanticError)): check(ctx,proof)

    def test_wrong_conversion_budget_rejected(self):
        ctx=context((('x','U'),),(Row(src('x'),num(1)),),{'x':0},units=('U','V'),conversions=(Conversion('c','U','V',F(2)),))
        b=Builder(ctx,'h'); b.conversion('c',b.row(0)); self.assertEqual(check(ctx,b.proof()).budget,2)
        self.bad(ctx,b.proof(),budget=F(1))

    def test_stale_context_rejected(self):
        ctx,p=composition_example(); self.bad(ctx,p,context_id='old-context')

    def test_changed_row_direction_replay_rejected(self):
        ctx=context(('x',),(Row(src('x'),num(1)),),{'x':0}); b=Builder(ctx,'h'); b.row(0)
        new=context(('x',),(Row(scale(2,src('x')),num(1)),),{'x':0},revision='v2')
        with self.assertRaises(ProofError): replay(ctx,new,b.proof())

    def test_changed_observation_replay_rejected(self):
        ctx,p=composition_example()
        with self.assertRaises(ProofError): replay(ctx,replace(ctx,observation='new-information'),p)

    def test_withdrawal_requires_rebuild(self):
        ctx=context(('x',),(Row(src('x'),num(1)),Row(src('x'),num(2))),{'x':0}); b=Builder(ctx,'h'); b.meet(b.row(0),b.row(1))
        new=context(('x',),(Row(src('x'),num(2)),),{'x':0},revision='v2')
        with self.assertRaises(ProofError): replay(ctx,new,b.proof())
        survivor=Builder(new,'h'); survivor.row(0)
        self.assertEqual(check(new,survivor.proof()).budget,2)

    def test_infeasible_source_rejected(self):
        with self.assertRaises(SemanticError): context(('x',),(Row(src('x'),num(0)),Row(num(1),src('x'))),{'x':0})

    def test_bad_forward_reference_rejected(self):
        ctx,p=composition_example(); self.bad(ctx,p,index=2,parents=(0,2))

    def test_budget_float_and_boolean_rejected(self):
        ctx,p=composition_example()
        for value in (0.5,True): self.bad(ctx,p,budget=value)

    def test_zero_scale_rechecks_types(self):
        ctx=context(('x',),(Row(src('x'),num(1)),),{'x':1}); b=Builder(ctx,'h'); b.scale(0,b.row(0))
        self.assertEqual(check(ctx,b.proof()).budget,0)

    def test_correlated_proof_calculator(self):
        ctx,p=self_bound_example(); self.assertEqual(check(ctx,p).budget,F(-1,2))
        for u in (F(-10)**30,F(-1),F(0),F(1,4),F(1),F(10)**30): self.assertTrue(reference_holds(ctx,p,{'u':u},'h'))

    def test_gap_aware_replay_bound(self):
        old=(F(1),F(2)); shock=(F(10),F(-1,2))
        exact=min(a+d for a,d in zip(old,shock))-min(old)
        self.assertEqual(exact,F(1,2)); self.assertLess(exact,max(shock))

    def test_report_portfolio_strict_gain(self):
        ctx,p,ids=report_portfolio_example(); root=check(ctx,p)
        self.assertEqual(root.budget,0)
        self.assertGreater(p.steps[ids[0]].budget-F(10,11),0)
        self.assertTrue(reference_holds(ctx,p,dict(ctx.cases[0].witness),'h'))

    def test_report_portfolio_degenerate_no_division(self):
        for r in (F(0),F(1,2),F(1)):
            ctx,p,_=report_portfolio_example(F(-1),F(1),r)
            self.assertEqual(check(ctx,p).budget,0)

    def test_improved_bound_can_worsen_selected_action(self):
        eps=F(1,10)
        before=(1-eps,1+eps); after=(1+2*eps,1-2*eps)
        self.assertLess(min(after),min(before))
        self.assertEqual(min(range(2),key=lambda i:before[i]),0)
        self.assertEqual(min(range(2),key=lambda i:after[i]),1)
        self.assertGreater(F(1,2),0) # Actual costs: 0 for A, 1/2 for B.

    def test_coverage_selection_counterexample(self):
        n=8
        self.assertEqual([sum(0 if d==i else 1 for d in range(n)) for i in range(n)],[n-1]*n)
        self.assertTrue(all(min(0 if d==i else 1 for i in range(n))==0 for d in range(n)))

    def test_reasoning_cost_is_not_free(self):
        self.assertGreater(F(9,10)+F(1,5),F(1))

    def test_report_transfer_after_lapse(self):
        ctx,p,root=report_transfer_example()
        self.assertEqual(check(ctx,replace(p,root=root)).budget,F(-11,32))
        self.assertEqual(check(ctx,p).budget,F(-23,64))


def report():
    data={'status':'F06 partial; finite proof audit, no general proof search',
          'arithmetic':'exact Fraction; point evaluator is a separate test oracle',
          'limitations':['no general source-map checker','no automatic case splitting','no proof search',
                         'no empirical calibration','no trained neural interpretation','not F07 global soundness'],
          'examples':{}}
    for name,(ctx,p) in examples().items():
        r=check(ctx,p)
        data['examples'][name]={'context':serial(ctx),'proof':serial(p),'conclusion_budget':str(r.budget),
                               'node_count':len(p.steps)}
    old,p,roots=reflection_example(); new,_,_=reflection_example(e_bound=F(3,64),revision='v2')
    replayed=replay(old,new,p)
    data['replay']={'old':{k:str(p.steps[i].budget) for k,i in roots.items()},
                    'new':{k:str(replayed.steps[i].budget) for k,i in roots.items()},
                    'rule':'same row directions, meanings, observations and cases; new feasible witnesses'}
    return data


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(F06InferenceTests))
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
