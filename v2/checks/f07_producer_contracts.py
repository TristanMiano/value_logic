"""F07 finite audits of producer postconditions, not a new inference kernel.

The expected softening contract is reconstructed without calling the producer
or its localizer. A separate denotation from f07_soundness checks finite points.
All generated traces still go through the unchanged F06 checker. Python 3.10+.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path
from typing import Mapping, Sequence
import unittest

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f06_residual_discharge as S
from v2.checks import f06_derived_cases as C
from v2.checks import f07_soundness as A


class ContractError(A.AuditError):
    """Valid arithmetic is not necessarily the requested producer result."""


def integer(value, lower: int, upper: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not lower <= value <= upper:
        raise ContractError('Integer index outside the declared finite range.')
    return value


def numeric_operation(ctx: K.Context, node: K.Step, parents: Sequence[F]) -> F:
    """Independent local budget recurrence; not a rule-validation oracle."""
    p = tuple(A.exact(x) for x in parents)
    tag = node.rule
    if tag in ('row', 'constant', 'lattice'): return A.exact(node.budget)
    if tag in ('rewrite', 'negate'): return p[0]
    if tag in ('add', 'trans'): return p[0] + p[1]
    if tag == 'scale': return A.exact(node.data[0]) * p[0]
    if tag == 'convert': return A.exact(ctx.signature.conversion(node.data[0]).factor) * p[0]
    if tag == 'slack': return p[0] + A.exact(node.data[0])
    if tag == 'meet_proofs': return min(p)
    if tag in ('max_common', 'min_common', 'congruence'): return max(p)
    if tag == 'res_congruence': return max(p[0] + p[1], F(0))
    raise ContractError('Localize the graph before numerical recurrence.')


def symbolic_operation(ctx: K.Context, node: K.Step, parents: Sequence[K.Term]) -> K.Term:
    p = tuple(parents); tag = node.rule
    unit = K.infer(node.new, ctx.signature)
    if tag in ('constant', 'lattice'): return K.num(node.budget, unit)
    if tag in ('rewrite', 'negate'): return p[0]
    if tag in ('add', 'trans'): return K.add(p[0], p[1])
    if tag == 'scale': return K.scale(A.exact(node.data[0]), p[0])
    if tag == 'convert': return K.convert(node.data[0], p[0])
    if tag == 'slack': return K.add(p[0], K.num(node.data[0], unit))
    if tag == 'meet_proofs': return K.minimum(p[0], p[1])
    if tag in ('max_common', 'min_common', 'congruence'): return K.maximum(p[0], p[1])
    if tag == 'res_congruence': return K.maximum(K.add(p[0], p[1]), K.num(0, unit))
    raise ContractError('Unexpected node in the independent allowance grammar.')


@dataclass(frozen=True)
class ExpectedSoftening:
    context: K.Context
    case: str
    new: K.Term
    old: K.Term
    allowance: K.Term
    penalty: K.Term
    baseline: F
    withdrawn: tuple[int, ...]


def expected_softening(ctx: K.Context, proof: K.Proof, case: str,
                       withdrawn: tuple[int, ...], revision: str) -> ExpectedSoftening:
    """Reconstruct the contract from the old inputs, never from the output."""
    root = K.check(ctx, proof)
    cases = {h.name: h for h in ctx.cases}
    if case not in cases or root.case not in (None, case):
        raise ContractError('Requested localization does not match the old root.')
    h = cases[case]
    if (not isinstance(withdrawn, tuple) or len(set(withdrawn)) != len(withdrawn)
            or not isinstance(revision, str) or not revision):
        raise ContractError('Explicit distinct withdrawal indices and revision required.')
    for i in withdrawn: integer(i, 0, len(h.rows)-1)
    removed = frozenset(withdrawn)
    updated = replace(h, rows=tuple(row for i, row in enumerate(h.rows) if i not in removed))
    target = replace(ctx, revision=revision,
                     cases=tuple(updated if old.name == case else old for old in ctx.cases))
    target.validate()
    zero_point = {name: F(0) for name, _ in ctx.signature.sources}
    memo: dict[int, tuple[K.Term, F]] = {}

    def visit(index: int) -> tuple[K.Term, F]:
        if index in memo: return memo[index]
        node = proof.steps[index]
        if node.case not in (None, case):
            raise ContractError('A foreign case entered the selected derivation.')
        if node.rule == 'all_cases':
            matches = [p for p in node.parents if proof.steps[p].case == case]
            if len(matches) != 1: raise ContractError('Missing or duplicated selected case.')
            answer = visit(matches[0])
        elif node.rule == 'row':
            i = node.data[0]; row = h.rows[i]
            unit = K.infer(row.lhs, ctx.signature)
            # Zero need not be feasible: this computes an affine intercept only.
            intercept = A.value(row.lhs, ctx.signature, zero_point) - A.value(row.rhs, ctx.signature, zero_point)
            direction = K.sub(K.sub(row.lhs, row.rhs), K.num(intercept, unit))
            eta = -intercept
            if i in removed:
                allowance = K.add(K.num(eta, unit),
                                  K.maximum(K.sub(direction, K.num(eta, unit)), K.num(0, unit)))
            else: allowance = K.num(eta, unit)
            answer = allowance, eta
        else:
            parents = [visit(p) for p in node.parents]
            answer = (symbolic_operation(ctx, node, [p[0] for p in parents]),
                      numeric_operation(ctx, node, [p[1] for p in parents]))
        memo[index] = answer
        return answer

    allowance, baseline = visit(proof.root)
    unit = K.infer(root.new, ctx.signature)
    return ExpectedSoftening(target, case, root.new, root.old, allowance,
                             K.sub(allowance, K.num(baseline, unit)), baseline,
                             tuple(sorted(removed)))


def receive_softening(ctx: K.Context, proof: K.Proof, case: str,
                      withdrawn: tuple[int, ...], revision: str,
                      result: S.SoftResult) -> K.Step:
    """Check both the exact auxiliary fields and the current requested trace."""
    expected = expected_softening(ctx, proof, case, withdrawn, revision)
    if not isinstance(result, S.SoftResult): raise ContractError('Expected a softening result.')
    result.context.validate()
    if result.context != expected.context:
        raise ContractError('The producer changed more than the requested evidence rows.')
    if (not isinstance(result.withdrawn, tuple) or any(type(i) is not int for i in result.withdrawn)
            or result.withdrawn != expected.withdrawn):
        raise ContractError('The advertised withdrawal set is wrong.')
    if A.exact(result.old_local_budget) != expected.baseline:
        raise ContractError('Original LOCAL baseline mismatch.')
    sig = expected.context.signature; unit = K.infer(expected.new, sig); zero = K.num(0, unit)
    if not K.same_difference(result.allowance, zero, expected.allowance, zero, sig):
        raise ContractError('The field called allowance is not the promised budget program.')
    if not K.same_difference(result.penalty, zero, expected.penalty, zero, sig):
        raise ContractError('The field called penalty does not have the promised meaning.')
    # Use the validated presentation of E, not a root copied from the output.
    wanted = A.request(expected.context, expected.case, expected.new,
                       K.add(expected.old, result.allowance), 0, unit)
    return A.receive(expected.context, result.proof, wanted)


def casewise_salvage_bound(ctx: K.Context, proof: K.Proof, case: str,
                          alive: frozenset[tuple[str, int]]) -> F | None:
    """Independent case-selecting optional-bound recurrence on the OLD graph.

    It uses K's exact normal form for the grammar's constant simplification,
    but neither the transport/localize routines nor their support frontiers.
    It is not an oracle for arbitrary semantic entailment.
    """
    root = K.check(ctx, proof)
    names = {h.name for h in ctx.cases}
    keys = {(h.name, i) for h in ctx.cases for i in range(len(h.rows))}
    if case not in names or root.case not in (None, case) or not alive <= keys:
        raise ContractError('Invalid case or source-availability contract.')
    memo: dict[int, F | None] = {}
    def visit(index):
        if index in memo: return memo[index]
        node = proof.steps[index]
        if node.case not in (None, case): raise ContractError('Foreign local proof.')
        form = K._form(K.sub(node.new, node.old), ctx.signature)
        if not form[0]: result = form[1]
        elif node.rule == 'all_cases':
            chosen = [p for p in node.parents if proof.steps[p].case == case]
            if len(chosen) != 1: raise ContractError('Case coverage mismatch.')
            result = visit(chosen[0])
        elif node.rule == 'row':
            result = node.budget if (case, node.data[0]) in alive else None
        elif node.rule == 'lattice': result = F(0)
        elif node.rule == 'meet_proofs':
            values = [v for p in node.parents if (v := visit(p)) is not None]
            result = min(values) if values else None
        else:
            values = [visit(p) for p in node.parents]
            result = None if any(v is None for v in values) else numeric_operation(ctx, node, values)
        memo[index] = result
        return result
    return visit(proof.root)


def local_defect_bounds(ctx: K.Context, proof: K.Proof,
                        defects: Sequence[int | F]) -> tuple[tuple[F, ...], tuple[F, ...]]:
    """Numerical P12 recurrence; each defect's interpretation is an input premise."""
    root = K.check(ctx, proof)
    if root.case is None or any(n.case != root.case or n.rule == 'all_cases' for n in proof.steps):
        raise ContractError('A single localized trace is required.')
    if len(defects) != len(proof.steps): raise ContractError('One defect per node required.')
    eps = tuple(A.exact(x) for x in defects)
    if any(x < 0 for x in eps): raise ContractError('Nonnegative defect bounds required.')
    upper = []
    for i, node in enumerate(proof.steps):
        upper.append(numeric_operation(ctx, node, [upper[p] for p in node.parents]) + eps[i])
    excess = tuple(u - A.exact(n.budget) for u, n in zip(upper, proof.steps))
    if any(e < 0 for e in excess): raise ContractError('Monotone-defect invariant failed.')
    return tuple(upper), excess


def fault_envelope(bounds: Sequence[int | F], k: int) -> F:
    values = sorted(A.exact(x) for x in bounds)
    if not values: raise ContractError('Nonempty proof family required.')
    return values[integer(k, 0, len(values)-1)]


def registered_failure_bound(alpha: Sequence[int | F], r: int) -> F:
    values = sorted((A.exact(x) for x in alpha), reverse=True)
    r = integer(r, 1, len(values))
    if any(a < 0 or a > 1 for a in values): raise ContractError('Probability allowances outside [0,1].')
    return min(F(1), *(sum(values[t:], F(0))/F(r-t) for t in range(r)))


def finite_policy_factor(observations: Sequence[str], actions: Sequence[Sequence[int | F]]) -> dict:
    if len(observations) != len(actions) or not observations:
        raise ContractError('Nonempty aligned observation/action table required.')
    result = {}; width = None
    for observation, raw in zip(observations, actions):
        if not isinstance(observation, str): raise ContractError('String observation key required.')
        vector = tuple(A.exact(x) for x in raw)
        if not vector or any(x < 0 for x in vector) or sum(vector, F(0)) != 1:
            raise ContractError('Not a probability distribution over actions.')
        if width is None: width = len(vector)
        if len(vector) != width: raise ContractError('Inconsistent action alphabet.')
        if observation in result and result[observation] != vector:
            raise ContractError('Policy uses information absent from its observation.')
        result[observation] = vector
    return result


def reflective_rates(p, s, r0, r1, cost=F(1,8)):
    p,s,r0,r1,c = map(A.exact, (p,s,r0,r1,cost))
    if any(not 0 <= x <= 1 for x in (p,s,r0,r1)):
        raise ContractError('Numerical arithmetic does not certify legal branch probabilities.')
    h0=(1-r0)*p+r0*s; h1=(1-r1)*p+r1*s
    return dict(old_failure=h0,new_failure=h1,old_cost=h0+c*r0,new_cost=h1+c*r1,
                paired_change=(h1+c*r1)-(h0+c*r0),report_overrun=h1-r1)


def two_case_example():
    x=K.src('x'); z=K.num(0)
    sig=K.Signature('F07-complementary-support-v1',('U',),(('x','U'),))
    ctx=K.Context(sig,'one-common-observation','v1',(
        K.Case('a',(K.Row(x,K.num(0)),K.Row(x,K.num(1))),(('x',F(0)),)),
        K.Case('b',(K.Row(x,K.num(1)),K.Row(x,K.num(0))),(('x',F(0)),))))
    global_builder=K.Builder(ctx); globals_=[]
    for index in (0,1):
        parts=[]
        for h in ctx.cases:
            b=K.Builder(ctx,h.name); i=b.rewrite(b.row(index),x,z)
            parts.append(T._copy_into(global_builder,b.proof(i)))
        globals_.append(global_builder.all_cases(parts))
    out=global_builder.meet(*globals_)
    return ctx,global_builder.proof(out)


def aggregation_example():
    x,y=K.src('x'),K.src('y'); z=K.num(0)
    sig=K.Signature('F07-aligned-bounds-v1',('U',),(('x','U'),('y','U')))
    ctx=K.Context(sig,'same-observation','v1',tuple(K.Case(name,
        (K.Row(x,K.num(a)),K.Row(y,K.num(b))),(('x',F(0)),('y',F(0))))
        for name,a,b in (('a',0,2),('b',2,0))))
    gb=K.Builder(ctx); roots=[]
    for i,t in ((0,x),(1,y)):
        parts=[]
        for h in ctx.cases:
            b=K.Builder(ctx,h.name); q=b.rewrite(b.row(i),t,z)
            parts.append(T._copy_into(gb,b.proof(q)))
        roots.append(gb.all_cases(parts))
    i=gb.add(*roots); i=gb.rewrite(i,K.add(x,y),z)
    return ctx,gb.proof(i)


def fault_case_example(bounds=(F(-1),F(0),F(2)), k=1):
    values=tuple(A.exact(x) for x in bounds); expected=fault_envelope(values,k)
    if len(values)>6: raise ContractError('This finite fixture permits at most six arguments.')
    d=K.src('d'); z=K.num(0); sig=K.Signature('F07-fault-envelope',('U',),(('d','U'),))
    groups=list(combinations(range(len(values)),len(values)-k))
    cases=tuple(K.Case('valid-'+','.join(map(str,group)),tuple(K.Row(d,K.num(values[i])) for i in group),
                     (('d',min(values)),)) for group in groups)
    ctx=K.Context(sig,'one-fixed-claim','v1',cases); gb=K.Builder(ctx); roots=[]
    for h in cases:
        b=K.Builder(ctx,h.name); i=b.rewrite(b.row(0),d,z)
        for j in range(1,len(h.rows)): i=b.meet(i,b.rewrite(b.row(j),d,z))
        roots.append(T._copy_into(gb,b.proof(i)))
    proof=gb.proof(gb.all_cases(roots)); A.receive(ctx,proof,A.request(ctx,None,d,z,expected))
    return ctx,proof


def alias_example():
    x,y,z=map(K.src,('x','y','z')); zero=K.num(0)
    old=K.context(('x','y'),(K.Row(x,zero),K.Row(K.scale(-1,y),K.num(-1))),{'x':0,'y':1},scope='alias-v1')
    b=K.Builder(old,'h'); i=b.rewrite(b.add(b.row(0),b.row(1)),K.sub(x,y),zero); proof=b.proof(i)
    new=K.context(('z',),(),{'z':0},scope='alias-v1',revision='aliased')
    out=T.transport(old,new,proof,{}, {'h':'h'}, {'x':z,'y':z})
    return old,proof,new,out


def report():
    ctx,p=two_case_example(); alive=frozenset({('a',0),('b',1)})
    new,out=T.restrict_rows(ctx,p,alive)
    soft=S.soften_rows(ctx,p,'a',(0,),revision='F07-soft-example')
    receive_softening(ctx,p,'a',(0,),'F07-soft-example',soft)
    ag,ap=aggregation_example(); aq=T.localize(ag,ap,'a')
    fc,fp=fault_case_example(); old,op,nc,np=alias_example()
    before=reflective_rates(F(1,4),F(0),F(1,4),F(1,2))
    after=reflective_rates(F(3,4),F(1,2),F(1,4),F(1,2))
    return {
        'scope':'Finite producer-contract audit. No new checking rule, full Python verification, or empirical certificate.',
        'support':{'alive':sorted(alive),'static_bound':T.best_label(T.support_frontier(ctx,p),alive),
                   'casewise_bounds':{h.name:casewise_salvage_bound(ctx,p,h.name,alive) for h in ctx.cases},
                   'received_global_bound':K.check(new,out).budget,'proof':C.pack_proof(out)},
        'aggregation':{'before':K.check(ag,ap).budget,'after_localization':K.check(ag,aq).budget},
        'softening':{'baseline':soft.old_local_budget,'withdrawn':soft.withdrawn,
                     'proof':C.pack_proof(soft.proof)},
        'alias':{'old_bound':K.check(old,op).budget,'current_bound':K.check(nc,np).budget},
        'fault_envelope':{'bound':K.check(fc,fp).budget,'proof':C.pack_proof(fp)},
        'reflective':{'before':before,'after':after,'historical_change':after['new_cost']-before['old_cost']},
        'probability_bound':registered_failure_bound((F(1,4),)*3,2),
    }


class ProducerContractTests(unittest.TestCase):
    def simple(self):
        x=K.src('x'); ctx=K.context(('x',),(K.Row(x,K.num(1)),),{'x':0})
        b=K.Builder(ctx,'h'); i=b.rewrite(b.row(0),x,K.num(0)); return ctx,b.proof(i)

    def test_expected_allowance_without_using_producer(self):
        ctx,p=self.simple(); e=expected_softening(ctx,p,'h',(0,),'new')
        for x in (-3,0,1,2,5):
            self.assertEqual(A.value(e.allowance,ctx.signature,{'x':x}),max(F(1),F(x)))
            self.assertEqual(A.value(e.penalty,ctx.signature,{'x':x}),max(F(x)-1,F(0)))

    def test_softening_received_at_its_declared_request(self):
        ctx,p=self.simple(); result=S.soften_rows(ctx,p,'h',(0,),revision='new')
        self.assertEqual(receive_softening(ctx,p,'h',(0,),'new',result).budget,0)

    def test_changed_penalty_metadata_is_rejected(self):
        ctx,p=self.simple(); s=S.soften_rows(ctx,p,'h',(0,),revision='new')
        with self.assertRaises(ContractError): receive_softening(ctx,p,'h',(0,),'new',replace(s,penalty=K.num(0)))

    def test_changed_allowance_metadata_is_rejected(self):
        ctx,p=self.simple(); s=S.soften_rows(ctx,p,'h',(0,),revision='new')
        with self.assertRaises(ContractError): receive_softening(ctx,p,'h',(0,),'new',replace(s,allowance=K.num(1)))

    def test_changed_original_baseline_is_rejected(self):
        ctx,p=self.simple(); s=S.soften_rows(ctx,p,'h',(0,),revision='new')
        with self.assertRaises(ContractError): receive_softening(ctx,p,'h',(0,),'new',replace(s,old_local_budget=F(2)))

    def test_boolean_baseline_is_not_a_rational_payload(self):
        ctx,p=self.simple(); s=S.soften_rows(ctx,p,'h',(0,),revision='new')
        with self.assertRaises(A.AuditError): receive_softening(ctx,p,'h',(0,),'new',replace(s,old_local_budget=True))

    def test_wrong_withdrawal_field_is_rejected(self):
        ctx,p=self.simple(); s=S.soften_rows(ctx,p,'h',(0,),revision='new')
        with self.assertRaises(ContractError): receive_softening(ctx,p,'h',(0,),'new',replace(s,withdrawn=()))

    def test_boolean_withdrawal_index_is_rejected(self):
        ctx,p=self.simple()
        with self.assertRaises(ContractError): expected_softening(ctx,p,'h',(False,),'new')

    def test_duplicate_withdrawal_is_rejected(self):
        ctx,p=self.simple()
        with self.assertRaises(ContractError): expected_softening(ctx,p,'h',(0,0),'new')

    def test_wrong_revision_is_rejected(self):
        ctx,p=self.simple(); s=S.soften_rows(ctx,p,'h',(0,),revision='other')
        with self.assertRaises(ContractError): receive_softening(ctx,p,'h',(0,),'new',s)

    def test_valid_unrelated_trace_is_not_a_valid_producer_result(self):
        ctx,p=self.simple(); s=S.soften_rows(ctx,p,'h',(0,),revision='new')
        b=K.Builder(s.context,'h'); b.constant(K.num(0),K.num(0))
        with self.assertRaises(A.AuditError): receive_softening(ctx,p,'h',(0,),'new',replace(s,proof=b.proof()))

    def test_equivalent_allowance_presentation_keeps_semantic_contract(self):
        ctx,p=self.simple(); s=S.soften_rows(ctx,p,'h',(0,),revision='new')
        # Extra zero is a permitted equivalent presentation, not an altered bound.
        e=K.add(s.allowance,K.num(0)); b=K.Builder(s.context,'h')
        i=T._copy_into(b,s.proof); i=b.rewrite(i,K.src('x'),K.add(K.num(0),e))
        changed=replace(s,allowance=e,proof=b.proof(i))
        receive_softening(ctx,p,'h',(0,),'new',changed)

    def test_localized_baseline_not_global_maximum(self):
        ctx,p=aggregation_example(); e=expected_softening(ctx,p,'a',(0,),'new')
        self.assertEqual(K.check(ctx,p).budget,4); self.assertEqual(e.baseline,2)
        s=S.soften_rows(ctx,p,'a',(0,),revision='new')
        receive_softening(ctx,p,'a',(0,),'new',s)
        with self.assertRaises(ContractError): receive_softening(ctx,p,'a',(0,),'new',replace(s,old_local_budget=F(4)))

    def test_other_case_rows_remain_unchanged(self):
        ctx,p=aggregation_example(); e=expected_softening(ctx,p,'a',(0,),'new')
        self.assertEqual(e.context.cases[1],ctx.cases[1])

    def test_current_penalty_checked_outside_withdrawn_source(self):
        ctx,p=self.simple(); s=S.soften_rows(ctx,p,'h',(0,),revision='new')
        for x in (F(-10**12),F(3,2),F(10**12)):
            d=A.value(p.steps[p.root].new,ctx.signature,{'x':x})
            bound=A.value(s.allowance,ctx.signature,{'x':x})
            self.assertLessEqual(d,bound)
        receive_softening(ctx,p,'h',(0,),'new',s)

    def test_source_offset_is_reconstructed_correctly(self):
        x=K.src('x'); ctx=K.context(('x',),(K.Row(K.add(x,K.num(3)),K.num(5)),),{'x':0})
        b=K.Builder(ctx,'h'); p=b.proof(b.row(0)); e=expected_softening(ctx,p,'h',(0,),'new')
        self.assertEqual(e.baseline,2)
        self.assertEqual(A.value(e.penalty,ctx.signature,{'x':4}),2)
        s=S.soften_rows(ctx,p,'h',(0,),revision='new'); receive_softening(ctx,p,'h',(0,),'new',s)

    def test_static_frontier_can_miss_casewise_salvage(self):
        ctx,p=two_case_example(); alive=frozenset({('a',0),('b',1)})
        self.assertIsNone(T.best_label(T.support_frontier(ctx,p),alive))
        nc,q=T.restrict_rows(ctx,p,alive)
        self.assertEqual(K.check(nc,q).budget,0)
        A.receive(nc,q,A.request(nc,None,K.src('x'),K.num(0),0))

    def test_casewise_oracle_matches_all_sixteen_withdrawals(self):
        ctx,p=two_case_example(); keys=tuple((h.name,i) for h in ctx.cases for i in range(2))
        for mask in product((False,True),repeat=4):
            alive=frozenset(k for k,keep in zip(keys,mask) if keep)
            values=[casewise_salvage_bound(ctx,p,h.name,alive) for h in ctx.cases]
            if any(v is None for v in values):
                with self.assertRaises(T.UnavailableProof): T.restrict_rows(ctx,p,alive)
            else:
                nc,q=T.restrict_rows(ctx,p,alive)
                self.assertEqual(K.check(nc,q).budget,max(values))
                for h in nc.cases:
                    for x in (F(-4),F(0),F(1),F(2)):
                        if A.case_feasible(nc,h.name,{'x':x}):
                            self.assertLessEqual(x,K.check(nc,q).budget)

    def test_localization_can_improve_bound_without_withdrawal(self):
        ctx,p=aggregation_example(); self.assertEqual(K.check(ctx,p).budget,4)
        alive=frozenset((h.name,i) for h in ctx.cases for i in range(2))
        self.assertEqual([casewise_salvage_bound(ctx,p,h.name,alive) for h in ctx.cases],[2,2])
        nc,q=T.restrict_rows(ctx,p,alive); self.assertEqual(K.check(nc,q).budget,2)

    def test_static_grammar_remains_exact_for_its_own_choices(self):
        ctx,p=two_case_example(); alive=frozenset((h.name,i) for h in ctx.cases for i in range(2))
        self.assertEqual(T.best_label(T.support_frontier(ctx,p),alive),1)
        self.assertEqual(max(casewise_salvage_bound(ctx,p,h.name,alive) for h in ctx.cases),0)

    def test_casewise_refusal_does_not_prove_semantic_refutation(self):
        ctx,p=two_case_example(); alive=frozenset()
        self.assertIsNone(casewise_salvage_bound(ctx,p,'a',alive))
        # x-x=0 nevertheless has an ordinary source-free proof.
        b=K.Builder(ctx,'a'); q=b.proof(b.constant(K.src('x'),K.src('x')))
        self.assertEqual(K.check(ctx,q).budget,0)

    def test_noninjective_alias_changes_the_current_strength(self):
        old,p,new,q=alias_example()
        self.assertEqual(K.check(old,p).budget,-1); self.assertEqual(K.check(new,q).budget,0)
        pair=(K.sub(K.src('z'),K.src('z')),K.num(0))
        A.receive(new,q,A.request(new,None,*pair,0))
        with self.assertRaises(A.AuditError): A.receive(new,q,A.request(new,None,*pair,-1))

    def test_nonlinear_source_substitution_has_a_current_proof(self):
        old,p=self.simple(); z=K.src('z'); zero=K.num(0)
        new=K.context(('z',),(K.Row(z,K.num(-1)),),{'z':-1},revision='nonlinear')
        b=K.Builder(new,'h'); i=b.rewrite(b.row(0),z,zero); j=b.constant(zero,zero)
        i=b.rewrite(b.max_common(i,j),K.maximum(z,zero),zero)
        q=T.transport(old,new,p,{('h','h',0):b.proof(i)},{'h':'h'},{'x':K.maximum(z,zero)})
        self.assertEqual(K.check(new,q).budget,0)
        A.receive(new,q,A.request(new,None,K.maximum(z,zero),zero,0))

    def test_changed_observation_is_not_silently_transportable(self):
        ctx,p=self.simple(); new=replace(ctx,observation='less-information',revision='new')
        with self.assertRaises(K.ProofError): T.transport(ctx,new,p,{}, {'h':'h'})

    def test_primitive_expansion_keeps_only_its_snapshot_choice(self):
        x=K.src('x'); old=K.context(('x',),(K.Row(x,K.num(-2)),K.Row(x,K.num(-1))),{'x':-2})
        b=K.Builder(old,'h'); i=b.meet(b.row(0),b.row(1)); p=b.proof(i)
        compiled=T.compile_primitives(old,p)
        new=replace(old,revision='new',cases=(K.Case('h',(K.Row(x,K.num(1)),K.Row(x,K.num(-1))),(('x',F(-1)),)),))
        self.assertEqual(K.check(new,K.replay(old,new,compiled)).budget,1)
        self.assertEqual(K.check(new,K.replay(old,new,p)).budget,-1)

    def test_pack_roundtrip_preserves_lexical_shadowing(self):
        ctx,_=self.simple(); x=K.src('x')
        t=K.let('h',x,K.let('k',K.loc('h'),K.let('h',K.num(7),K.loc('k'))))
        b=K.Builder(ctx,'h'); p=b.proof(b.constant(t,x))
        decoded=C.unpack_proof(ctx,C.pack_proof(p))
        self.assertEqual(decoded,p); self.assertEqual(A.value(t,ctx.signature,{'x':3}),3)

    def test_decoded_valid_proof_still_needs_request_binding(self):
        ctx,p=self.simple(); q=C.unpack_proof(ctx,C.pack_proof(p))
        with self.assertRaises(A.AuditError): A.receive(ctx,q,A.request(ctx,'h',K.src('x'),K.num(0),0))

    def test_zero_defects_reproduce_every_local_snapshot_budget(self):
        for ctx,p in (A.native_catalogue(), self.simple()):
            if K.check(ctx,p).case is None: continue
            upper,errors=local_defect_bounds(ctx,p,(F(0),)*len(p.steps))
            self.assertEqual(upper,tuple(n.budget for n in p.steps)); self.assertFalse(any(errors))

    def test_shared_error_is_counted_twice_under_addition(self):
        ctx,p=self.simple(); b=K.Builder(ctx,'h'); i=b.row(0); j=b.add(i,i); q=b.proof(j)
        upper,error=local_defect_bounds(ctx,q,(F(2),F(0)))
        self.assertEqual(upper[q.root],6); self.assertEqual(error[q.root],4)

    def test_proof_minimum_hedges_a_local_error(self):
        x=K.src('x'); ctx=K.context(('x',),(K.Row(x,K.num(-1)),K.Row(x,K.num(0))),{'x':-1})
        b=K.Builder(ctx,'h'); i=b.meet(b.row(0),b.row(1)); p=b.proof(i)
        upper,error=local_defect_bounds(ctx,p,(F(2),F(0),F(0)))
        self.assertEqual(upper[p.root],0); self.assertEqual(error[p.root],1)

    def test_defect_recurrence_bounds_an_out_of_source_assignment(self):
        ctx,p=self.simple(); point={'x':F(5)}
        actual=[A.value(n.new,ctx.signature,point)-A.value(n.old,ctx.signature,point) for n in p.steps]
        errors=[max(d-numeric_operation(ctx,n,[actual[j] for j in n.parents]),F(0)) for d,n in zip(actual,p.steps)]
        upper,_=local_defect_bounds(ctx,p,errors)
        self.assertTrue(all(d<=u for d,u in zip(actual,upper)))

    def test_negative_defect_rejected_by_nonnegative_contract(self):
        ctx,p=self.simple()
        with self.assertRaises(ContractError): local_defect_bounds(ctx,p,(-1,)*len(p.steps))

    def test_global_defect_recurrence_requires_localization(self):
        ctx,p=two_case_example()
        with self.assertRaises(ContractError): local_defect_bounds(ctx,p,(0,)*len(p.steps))

    def test_fault_envelope_has_an_ordinary_case_proof(self):
        ctx,p=fault_case_example(); self.assertEqual(K.check(ctx,p).budget,0)
        self.assertEqual(len(ctx.cases),3)
        for h in ctx.cases:
            for d in (-2,-1,0,1,2):
                if A.case_feasible(ctx,h.name,{'d':d}): self.assertLessEqual(d,0)

    def test_fault_envelope_all_small_bounds_and_fault_counts(self):
        for bounds in product((-1,0,2),repeat=3):
            for k in range(3):
                envelope=fault_envelope(bounds,k)
                possible=[min(bounds[i] for i in valid) for valid in combinations(range(3),3-k)]
                self.assertEqual(envelope,max(possible))

    def test_one_valid_argument_does_not_license_minimum(self):
        d=F(1); bounds=(F(0),F(2))
        self.assertLessEqual(d,fault_envelope(bounds,1)); self.assertGreater(d,min(bounds))

    def test_uncertain_fault_count_needs_nonempty_valid_family(self):
        with self.assertRaises(ContractError): fault_envelope((0,1),2)
        with self.assertRaises(ContractError): fault_envelope((0,1),True)

    def test_registered_failure_bound_is_sharp_in_one_correlated_example(self):
        # Three two-failure patterns with mass 1/8 each, otherwise no failure.
        alpha=(F(1,4),)*3
        self.assertEqual(registered_failure_bound(alpha,2),F(3,8))

    def test_probability_bound_all_small_weighted_failure_patterns(self):
        patterns=tuple(product((0,1),repeat=3))
        for first,second in combinations(patterns,2):
            for weight in (F(0),F(1,4),F(1,2),F(1)):
                alpha=[weight*a+(1-weight)*b for a,b in zip(first,second)]
                for r in (1,2,3):
                    actual=weight*int(sum(first)>=r)+(1-weight)*int(sum(second)>=r)
                    self.assertLessEqual(actual,registered_failure_bound(alpha,r))

    def test_probability_endpoint_max_uses_intersection_not_union(self):
        self.assertEqual(registered_failure_bound((F(1,10),F(3,10)),2),F(1,10))
        self.assertEqual(registered_failure_bound((F(1,10),F(3,10)),1),F(2,5))

    def test_probability_inputs_are_not_arbitrary_confidence_labels(self):
        with self.assertRaises(ContractError): registered_failure_bound((F(2),),1)
        with self.assertRaises(A.AuditError): registered_failure_bound((0.1,),1)

    def test_reflective_comparison_survives_but_report_fails(self):
        first=reflective_rates(F(1,4),0,F(1,4),F(1,2))
        later=reflective_rates(F(3,4),F(1,2),F(1,4),F(1,2))
        self.assertEqual(first['paired_change'],F(-1,32)); self.assertEqual(later['paired_change'],F(-1,32))
        self.assertLessEqual(first['report_overrun'],0); self.assertEqual(later['report_overrun'],F(1,8))

    def test_historical_change_has_a_separate_source_drift(self):
        first=reflective_rates(F(1,4),0,F(1,4),F(1,2))
        later=reflective_rates(F(3,4),F(1,2),F(1,4),F(1,2))
        actual=later['new_cost']-first['old_cost']; drift=later['old_cost']-first['old_cost']
        self.assertEqual(actual,F(15,32)); self.assertEqual(actual,later['paired_change']+drift)

    def test_performative_branch_drift_identity_on_finite_grid(self):
        for p0,s0,p1,s1,r0,r1 in product((F(0),F(1,2),F(1)),repeat=6):
            actual=(1-r1)*p1+r1*s1-((1-r0)*p0+r0*s0)
            expected=(r1-r0)*(s0-p0)+(1-r1)*(p1-p0)+r1*(s1-s0)
            self.assertEqual(actual,expected)

    def test_favorable_arithmetic_does_not_certify_probability_domain(self):
        self.assertEqual((1-F(3,4))*2,F(1,2))
        with self.assertRaises(ContractError): reflective_rates(2,0,F(1,4),F(3,4))

    def test_observation_factor_accepts_common_randomized_policy(self):
        result=finite_policy_factor(('same','same'),((F(1,4),F(3,4)),(F(1,4),F(3,4))))
        self.assertEqual(len(result),1)

    def test_observation_factor_rejects_hidden_action_choice(self):
        with self.assertRaises(ContractError): finite_policy_factor(('same','same'),((1,0),(0,1)))

    def test_observation_factor_checks_normalization(self):
        with self.assertRaises(ContractError): finite_policy_factor(('seen',),((1,1),))

    def test_negative_baseline_softening_retains_improvement(self):
        x=K.src('x'); zero=K.num(0)
        ctx=K.context(('x',),(K.Row(K.scale(-1,x),K.num(-1)),),{'x':1})
        b=K.Builder(ctx,'h'); p=b.proof(b.rewrite(b.row(0),K.scale(-1,x),zero))
        soft=S.soften_rows(ctx,p,'h',(0,),revision='negative-baseline')
        receive_softening(ctx,p,'h',(0,),'negative-baseline',soft)
        self.assertEqual(soft.old_local_budget,-1)
        for q in (-5,0,1,2):
            self.assertEqual(A.value(soft.allowance,ctx.signature,{'x':q}),-1+max(1-q,0))
            self.assertGreaterEqual(A.value(soft.penalty,ctx.signature,{'x':q}),0)

    def test_every_native_local_prefix_has_received_discharge(self):
        ctx,p=A.native_catalogue()
        tags=set()
        for index,node in enumerate(p.steps):
            prefix=K.Proof(p.steps[:index+1],index)
            if node.case is None: continue
            tags.add(node.rule)
            soft=S.soften_rows(ctx,prefix,node.case,(0,1),revision='native-prefix')
            receive_softening(ctx,prefix,node.case,(0,1),'native-prefix',soft)
        self.assertTrue({'row','add','trans','slack','negate','congruence',
                         'res_congruence','meet_proofs','convert'} <= tags)

    def test_global_replacements_use_their_case_local_bounds(self):
        new,_=aggregation_example(); x,y=K.src('x'),K.src('y'); zero=K.num(0)
        old=K.Context(new.signature,new.observation,'old',
            (K.Case('h',(K.Row(x,K.num(2)),K.Row(y,K.num(2))),(('x',F(0)),('y',F(0)))),))
        b=K.Builder(old,'h'); i=b.add(b.row(0),b.row(1)); i=b.rewrite(i,K.add(x,y),zero); p=b.proof(i)
        replacements={}
        for index,term in enumerate((x,y)):
            gb=K.Builder(new); parts=[]
            for h in new.cases:
                local=K.Builder(new,h.name); j=local.rewrite(local.row(index),term,zero)
                parts.append(T._copy_into(gb,local.proof(j)))
            q=gb.proof(gb.all_cases(parts))
            self.assertEqual(K.check(new,q).budget,2)
            for h in new.cases: replacements[(h.name,'h',index)]=q
        out=T.transport(old,new,p,replacements,{h.name:'h' for h in new.cases})
        A.receive(new,out,A.request(new,None,K.add(x,y),zero,2))
        self.assertEqual(K.check(old,p).budget,4)
        self.assertEqual(K.check(new,out).budget,2)

    def test_affine_source_offset_must_be_in_replacement_claim(self):
        old,p=self.simple(); z=K.src('z'); zero=K.num(0)
        new=K.context(('z',),(K.Row(z,K.num(1)),),{'z':0},revision='shifted')
        b=K.Builder(new,'h'); j=b.rewrite(b.row(0),z,zero)
        with self.assertRaises(K.ProofError):
            T.transport(old,new,p,{('h','h',0):b.proof(j)},{'h':'h'},
                        {'x':K.add(z,K.num(2))})
        j=b.add(j,b.constant(K.num(2),zero)); j=b.rewrite(j,K.add(z,K.num(2)),zero)
        out=T.transport(old,new,p,{('h','h',0):b.proof(j)},{'h':'h'},
                        {'x':K.add(z,K.num(2))})
        A.receive(new,out,A.request(new,None,K.add(z,K.num(2)),zero,3))
        self.assertEqual(K.check(new,out).budget,3)

    def test_expansion_without_proof_minimum_commutes_with_rhs_replay(self):
        ctx,_=self.simple(); x=K.src('x'); z=K.num(0)
        b=K.Builder(ctx,'h'); j=b.add(b.row(0),b.row(0)); k=b.constant(z,z)
        j=b.congruence('max',j,k); p=b.proof(j)
        expanded=T.compile_primitives(ctx,p)
        for bound in (-2,-1,0,1,3):
            new=replace(ctx,revision='replay',cases=(K.Case('h',(K.Row(x,K.num(bound)),),(('x',F(bound)),)),))
            direct=K.replay(ctx,new,p); compiled=K.replay(ctx,new,expanded)
            self.assertEqual(K.check(new,direct).budget,K.check(new,compiled).budget)
            self.assertTrue(K.same_difference(K.check(new,direct).new,K.check(new,direct).old,
                                             K.check(new,compiled).new,K.check(new,compiled).old,new.signature))

    def test_duplicate_supports_do_not_provide_independent_fault_tolerance(self):
        labels=((frozenset({'a'}),F(0)),(frozenset({'a'}),F(0)),(frozenset({'b'}),F(1)))
        envelopes=[]
        for failed in (frozenset(),frozenset({'a'}),frozenset({'b'})):
            envelopes.append(min(b for support,b in labels if not support & failed))
        self.assertEqual(max(envelopes),1)
        self.assertEqual(fault_envelope(tuple(b for _,b in labels),1),0)
        self.assertEqual(envelopes[1],1)

    def test_strict_exclusion_residual_has_a_nonstrict_equality_boundary(self):
        # Parent x >= 1 proves -x <= -1. Its violation is rho=(1-x)+.
        for x in (F(1),F(1,2),F(0),F(-1,4)):
            rho=max(1-x,F(0)); bound=-1+rho
            self.assertLessEqual(-x,bound)
            self.assertLessEqual(max(-x,F(0)),max(bound,F(0)))
            if rho<1: self.assertGreater(x,0)
        self.assertEqual(-1+max(1-F(0),F(0)),0)

    def test_nonnegative_correction_dominates_actual_excess(self):
        for d,b in product((F(-2),F(0),F(3)),repeat=2):
            least=max(d-b,F(0))
            for correction in (least,least+F(1,3)):
                self.assertLessEqual(d,b+correction)
                self.assertGreaterEqual(correction,least)

    def test_report_is_deterministic(self):
        self.assertEqual(json.dumps(report(),default=A.jsonable,sort_keys=True),
                         json.dumps(report(),default=A.jsonable,sort_keys=True))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),default=A.jsonable,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    else:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProducerContractTests))
        if not result.wasSuccessful(): raise SystemExit(1)

if __name__=='__main__': main()
