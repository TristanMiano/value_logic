"""Audit-only certificates for a small subset of Rational Lawvere source rules.

Not a full RLL prover, proof searcher, or the planned Value Logic reasoner.
Premises are explicit assumptions, never inferred from numerical samples.
Permutation, positioned cut, and positioned premise merging denote finite
combinations of Table 2's permutation/cut/prem rules. No contraction, semantic
oracle, unrestricted substitution, disjunctive case rule or logarithm rule exists.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import unittest
from typing import Any

Term = tuple
INF: Term = ('inf',)

def var(name: str) -> Term:
    return ('var', name)

def add(a: Term, b: Term) -> Term:
    return ('add', a, b)

def imp(a: Term, b: Term) -> Term:
    return ('imp', a, b)

def finite(a: Term) -> Term:
    return imp(imp(a, INF), INF)

def parse_term(data: Any) -> Term:
    if not isinstance(data, (list, tuple)) or not data:
        raise ValueError('Term must be a nonempty tagged sequence')
    tag = data[0]
    if tag == 'inf' and len(data) == 1:
        return INF
    if tag == 'var' and len(data) == 2 and isinstance(data[1], str) and data[1]:
        return (tag, data[1])
    if tag == 'rat' and len(data) == 2 and isinstance(data[1], str):
        try:
            number = Fraction(data[1])
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError('Invalid rational constant') from exc
        if number < 0:
            raise ValueError('RLL formula constants must be nonnegative')
        return (tag, str(number))
    if tag in ('add', 'imp') and len(data) == 3:
        return (tag, parse_term(data[1]), parse_term(data[2]))
    raise ValueError('Unsupported term constructor or arity')

@dataclass(frozen=True)
class Sequent:
    left: tuple[Term, ...]
    right: Term

    def json(self) -> dict:
        return {'left': self.left, 'right': self.right}

    @classmethod
    def parse(cls, data: Any) -> Sequent:
        if not isinstance(data, dict) or set(data) != {'left', 'right'}:
            raise ValueError('A sequent requires exactly left and right')
        if not isinstance(data['left'], (list, tuple)):
            raise ValueError('Antecedents must be a sequence')
        return cls(tuple(parse_term(t) for t in data['left']), parse_term(data['right']))


def check_certificate(document: dict) -> Sequent:
    """Return the certified goal or raise ValueError; all assumptions are explicit."""
    if not isinstance(document, dict) or document.get('schema_version') != 1:
        raise ValueError('Unsupported certificate schema')
    hypotheses = [Sequent.parse(h) for h in document.get('hypotheses', [])]
    nodes = document.get('steps')
    if not isinstance(nodes, list) or not nodes:
        raise ValueError('Certificate must contain steps')
    proved: list[Sequent] = []
    for n, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise ValueError(f'Step {n}: invalid node')
        out = Sequent.parse(node.get('sequent'))
        ids = node.get('parents', [])
        if not isinstance(ids, list) or any(type(i) is not int or not 0 <= i < n for i in ids):
            raise ValueError(f'Step {n}: parent is not an earlier step')
        ps = [proved[i] for i in ids]
        rule = node.get('rule')
        ok = False
        if rule == 'hypothesis' and not ps:
            i = node.get('hypothesis')
            ok = type(i) is int and 0 <= i < len(hypotheses) and out == hypotheses[i]
        elif rule == 'identity' and not ps:
            ok = out.left == (out.right,)
        elif rule == 'permutation' and len(ps) == 1:
            ok = out.right == ps[0].right and Counter(out.left) == Counter(ps[0].left)
        elif rule == 'weakening' and len(ps) == 1:
            ok = out.right == ps[0].right and len(out.left) == len(ps[0].left) + 1 and out.left[:-1] == ps[0].left
        elif rule in ('prem_fold', 'prem_unfold') and len(ps) == 1:
            i = node.get('index')
            old = ps[0]
            if type(i) is int and 0 <= i < len(old.left):
                if rule == 'prem_fold' and i + 1 < len(old.left):
                    want = old.left[:i] + (add(old.left[i], old.left[i+1]),) + old.left[i+2:]
                    ok = out == Sequent(want, old.right)
                elif rule == 'prem_unfold' and old.left[i][0] == 'add':
                    a, b = old.left[i][1:]
                    want = old.left[:i] + (a, b) + old.left[i+1:]
                    ok = out == Sequent(want, old.right)
        elif rule == 'quant_forward' and len(ps) == 1:
            old = ps[0]
            if len(old.left) == 1 and old.left[0][0] == 'add':
                a, b = old.left[0][1:]
                ok = out == Sequent((a,), imp(b, old.right))
        elif rule == 'quant_reverse' and len(ps) == 1:
            old = ps[0]
            if len(old.left) == 1 and old.right[0] == 'imp':
                b, c = old.right[1:]
                ok = out == Sequent((add(old.left[0], b),), c)
        elif rule == 'cut' and len(ps) == 2:
            a, b = ps
            i = node.get('index')
            if type(i) is int and 0 <= i < len(b.left) and b.left[i] == a.right:
                want = a.left + b.left[:i] + b.left[i+1:]
                ok = out == Sequent(want, b.right)
        elif rule == 'cancel' and len(ps) == 2:
            old, guard = ps
            if len(old.left) == 1 and old.left[0][0] == old.right[0] == 'add':
                a, common = old.left[0][1:]
                b, same = old.right[1:]
                ok = common == same and guard == Sequent((), finite(common)) and out == Sequent((a,), b)
        if not ok:
            raise ValueError(f'Step {n}: rule {rule!r} does not justify the stated sequent')
        proved.append(out)
    goal = Sequent.parse(document.get('goal'))
    if proved[-1] != goal:
        raise ValueError('Final step is not the advertised goal')
    return goal


class Builder:
    """Fixture assembly only. The separate checker validates the emitted nodes."""
    def __init__(self, hypotheses: list[Sequent]):
        self.hypotheses = hypotheses
        self.steps: list[dict] = []

    def emit(self, rule: str, out: Sequent, parents: list[int] | None = None, **extra: Any) -> int:
        self.steps.append({'rule': rule, 'parents': parents or [], 'sequent': out.json(), **extra})
        return len(self.steps) - 1

    def at(self, i: int) -> Sequent:
        return Sequent.parse(self.steps[i]['sequent'])

    def hyp(self, i: int) -> int:
        return self.emit('hypothesis', self.hypotheses[i], hypothesis=i)

    def fold(self, p: int, i: int) -> int:
        s = self.at(p)
        return self.emit('prem_fold', Sequent(s.left[:i]+(add(*s.left[i:i+2]),)+s.left[i+2:], s.right), [p], index=i)

    def unfold(self, p: int, i: int) -> int:
        s = self.at(p)
        return self.emit('prem_unfold', Sequent(s.left[:i]+s.left[i][1:]+s.left[i+1:], s.right), [p], index=i)

    def perm(self, p: int, left: tuple[Term, ...]) -> int:
        return self.emit('permutation', Sequent(left, self.at(p).right), [p])

    def cut(self, p: int, q: int, i: int) -> int:
        a, b = self.at(p), self.at(q)
        return self.emit('cut', Sequent(a.left+b.left[:i]+b.left[i+1:], b.right), [p,q], index=i)

    def ac(self, old: Term, new: Term) -> int:
        """Derive reassociation/permutation of sums using only prem and perm."""
        def leaves(t: Term) -> tuple[Term, ...]:
            return leaves(t[1])+leaves(t[2]) if t[0]=='add' else (t,)
        if Counter(leaves(old)) != Counter(leaves(new)):
            raise ValueError('Sum leaves differ')
        p = self.emit('identity', Sequent((new,),new))
        while any(t[0]=='add' for t in self.at(p).left):
            i = next(i for i,t in enumerate(self.at(p).left) if t[0]=='add')
            p = self.unfold(p,i)
        p = self.perm(p, leaves(old))
        def rebuild(p: int, i: int, t: Term) -> int:
            if t[0] != 'add':
                return p
            p = rebuild(p,i,t[1]); p = rebuild(p,i+1,t[2])
            return self.fold(p,i)
        return rebuild(p,0,old)

    def result(self) -> dict:
        return {'schema_version':1,'hypotheses':[h.json() for h in self.hypotheses],
                'steps':self.steps,'goal':self.steps[-1]['sequent']}


def direct_loss_certificate() -> dict:
    x,y,z,r,s = map(var, ('x','y','z','r','s'))
    u,v = imp(y,x),imp(z,y)
    b = Builder([Sequent((r,),u), Sequent((s,),v)])
    a = b.emit('identity',Sequent((u,),u))
    a = b.emit('quant_reverse',Sequent((add(u,y),),x),[a]); a=b.unfold(a,0)
    c = b.emit('identity',Sequent((v,),v))
    c = b.emit('quant_reverse',Sequent((add(v,z),),y),[c]); c=b.unfold(c,0)
    p=b.cut(c,a,1); p=b.perm(p,(u,v,z)); p=b.fold(p,0); p=b.fold(p,0)
    p=b.emit('quant_forward',Sequent((add(u,v),),imp(z,x)),[p]); p=b.unfold(p,0)
    p=b.cut(b.hyp(0),p,0); p=b.cut(b.hyp(1),p,1); p=b.perm(p,(r,s)); b.fold(p,0)
    return b.result()


def signed_chain_certificate() -> dict:
    xp,xm,yp,ym,zp,zm,r,s = map(var, ('xp','xm','yp','ym','zp','zm','r','s'))
    a,bb,c,d = add(add(yp,xm),r),add(xp,ym),add(add(zp,ym),s),add(yp,zm)
    common=add(yp,ym); left=add(add(add(zp,xm),r),s); right=add(xp,zm)
    b=Builder([Sequent((a,),bb),Sequent((c,),d),Sequent((),finite(common))])
    p=b.emit('identity',Sequent((add(bb,d),),add(bb,d))); p=b.unfold(p,0)
    p=b.cut(b.hyp(0),p,0); p=b.cut(b.hyp(1),p,1);p=b.perm(p,(a,c));p=b.fold(p,0)
    p=b.cut(b.ac(add(left,common),add(a,c)),p,0)
    p=b.cut(p,b.ac(add(bb,d),add(right,common)),0)
    b.emit('cancel',Sequent((left,),right),[p,b.hyp(2)])
    return b.result()


def eval_term(t: Term, values: dict[str, Fraction | float]) -> Fraction | float:
    tag=t[0]
    if tag=='var':
        v=values[t[1]]
        if v < 0 or (isinstance(v,float) and math.isnan(v)):
            raise ValueError('Nonnegative source values required')
        return v
    if tag=='rat': return Fraction(t[1])
    if tag=='inf': return math.inf
    a,b=eval_term(t[1],values),eval_term(t[2],values)
    if tag=='add': return a+b
    if tag=='imp':
        if a==math.inf: return Fraction(0)
        if b==math.inf: return math.inf
        return max(b-a,Fraction(0))
    raise ValueError(tag)


def holds(s: Sequent, values: dict) -> bool:
    return sum((eval_term(t,values) for t in s.left),Fraction(0)) >= eval_term(s.right,values)


def report() -> dict:
    out={'scope':'Audit-only finite source-rule certificates; no completeness or independent formal verification',
         'source':'S12, CSL 2026, Table 2; perm-position macros use finite permutations',
         'certificates':{}}
    for name,doc in [('direct_loss',direct_loss_certificate()),('finite_signed_chain',signed_chain_certificate())]:
        check_certificate(doc)
        out['certificates'][name]={'steps':len(doc['steps']),'hypotheses':len(doc['hypotheses']),
                                  'uses_finiteness_guard':name=='finite_signed_chain','proof':doc}
    return out


class F03CheckedDerivationTests(unittest.TestCase):
    def bad(self, doc: dict) -> None:
        with self.assertRaises(ValueError): check_certificate(doc)

    def test_direct_source_certificate(self):
        self.assertEqual(check_certificate(direct_loss_certificate()).right,imp(var('z'),var('x')))

    def test_signed_source_certificate(self):
        d=signed_chain_certificate(); self.assertEqual(check_certificate(d).right,add(var('xp'),var('zm')))

    def test_json_roundtrip(self):
        for d in (direct_loss_certificate(),signed_chain_certificate()):
            self.assertEqual(check_certificate(d),check_certificate(json.loads(json.dumps(d))))

    def test_missing_guard_rejected(self):
        d=signed_chain_certificate();d['steps'][-1]['parents'].pop();self.bad(d)

    def test_wrong_guard_rejected(self):
        d=signed_chain_certificate();d['steps'][-1]['parents'][1]=0;self.bad(d)

    def test_unlisted_assumption_rejected(self):
        d=direct_loss_certificate();d['hypotheses']=[];self.bad(d)

    def test_forward_reference_rejected(self):
        d=direct_loss_certificate();d['steps'][1]['parents']=[1];self.bad(d)

    def test_reversed_implication_rejected(self):
        d=direct_loss_certificate();n=next(n for n in d['steps'] if n['rule']=='quant_forward')
        t=n['sequent']['right'];n['sequent']['right']=imp(t[2],t[1]);self.bad(d)

    def test_contraction_disguised_as_permutation_rejected(self):
        a=var('a');b=Builder([Sequent((a,a),add(a,a))]);p=b.hyp(0)
        b.emit('permutation',Sequent((a,),add(a,a)),[p]);self.bad(b.result())

    def test_cut_removes_one_occurrence_only(self):
        a,r=var('a'),var('r');b=Builder([Sequent((r,),a),Sequent((a,a),add(a,a))])
        p=b.cut(b.hyp(0),b.hyp(1),0); good=b.result();check_certificate(good)
        self.assertEqual(b.at(p).left,(r,a))
        good['steps'][-1]['sequent']=Sequent((r,),add(a,a)).json();good['goal']=good['steps'][-1]['sequent'];self.bad(good)

    def test_negative_source_constant_rejected(self):
        with self.assertRaises(ValueError):parse_term(['rat','-1'])

    def test_unknown_rule_rejected(self):
        d=direct_loss_certificate();d['steps'][0]['rule']='numerically_true';self.bad(d)

    def test_forged_goal_rejected(self):
        d=direct_loss_certificate();d['goal']=Sequent((),var('x')).json();self.bad(d)

    def test_extended_source_grid(self):
        d=direct_loss_certificate();hs=[Sequent.parse(h) for h in d['hypotheses']];g=check_certificate(d)
        count=0
        for xs in itertools.product([Fraction(0),Fraction(1),Fraction(4),math.inf], repeat=5):
            v=dict(zip(('x','y','z','r','s'),xs))
            if all(holds(h,v) for h in hs):self.assertTrue(holds(g,v));count+=1
        self.assertGreater(count,0)

    def test_signed_coordinates_without_magnitude_cap(self):
        d=signed_chain_certificate();g=check_certificate(d)
        for scale in (1,10,10**50):
            v={k:Fraction(x*scale) for k,x in dict(xp=5,xm=8,yp=7,ym=9,zp=2,zm=6,r=1,s=2).items()}
            self.assertTrue(all(holds(Sequent.parse(h),v) for h in d['hypotheses']))
            self.assertTrue(holds(g,v))

    def test_infinite_cancellation_countermodel(self):
        z=('rat','0');o=('rat','1')
        self.assertTrue(holds(Sequent((add(z,INF),),add(o,INF)),{}))
        self.assertFalse(holds(Sequent((z,),o),{}))
        self.assertFalse(holds(Sequent((),finite(INF)),{}))

    def test_declared_guard_can_make_assumptions_inconsistent(self):
        d=signed_chain_certificate();check_certificate(d)
        v={k:Fraction(0) for k in ('xp','xm','yp','ym','zp','zm','r','s')};v['yp']=math.inf
        self.assertFalse(holds(Sequent.parse(d['hypotheses'][2]),v))

    def test_source_weakening_is_not_signed_weakening(self):
        self.assertGreaterEqual(Fraction(0),Fraction(0))
        self.assertFalse(Fraction(0)+Fraction(-1)>=Fraction(0))


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',type=Path);a=p.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F03CheckedDerivationTests))
    if not result.wasSuccessful(): return 1
    if a.json:
        a.json.parent.mkdir(parents=True,exist_ok=True);a.json.write_text(json.dumps(report(),indent=2)+'\n',encoding='utf-8')
    return 0

if __name__=='__main__':raise SystemExit(main())
