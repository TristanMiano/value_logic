"""Single-case quantitative assumption discharge into ordinary F06-S1 proofs.

A removed inequality becomes a residual-violation term, NOT an assumed error
bound or an empirical confidence. The unchanged S1 checker validates each
emitted trace. Global case splitting and operational policy checking are absent.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import unittest

from v2.checks import f06_inference_rules as R
from v2.checks import f06_source_transport as T


@dataclass(frozen=True)
class SoftResult:
    context: R.Context
    proof: R.Proof
    allowance: R.Term
    penalty: R.Term
    old_local_budget: F
    withdrawn: tuple[int, ...]


def soften_rows(ctx: R.Context, proof: R.Proof, case: str,
                withdrawn: tuple[int, ...], *, revision: str = 'soft-withdrawal-v2') -> SoftResult:
    """Remove selected rows in ONE case and emit t <=[0] s+allowance.

    The allowance is the original local budget program with removed leaf eta
    replaced by eta+ReLU(a-eta). It is not automatically bounded by a literal.
    Other cases are retained; the returned proof is local, not a global warrant.
    """
    local = T.localize(ctx, proof, case)
    old_case = next(h for h in ctx.cases if h.name == case)
    if (not isinstance(withdrawn, tuple) or len(set(withdrawn)) != len(withdrawn)
            or any(isinstance(i, bool) or not isinstance(i, int)
                   or not 0 <= i < len(old_case.rows) for i in withdrawn)):
        raise R.ProofError('Withdrawal needs distinct valid integer row indices.')
    removed = set(withdrawn)
    surviving = [i for i in range(len(old_case.rows)) if i not in removed]
    renumber = {i: j for j, i in enumerate(surviving)}
    new_case = replace(old_case, rows=tuple(old_case.rows[i] for i in surviving))
    new = replace(ctx, revision=revision,
                  cases=tuple(new_case if h.name == case else h for h in ctx.cases))
    new.validate()
    b = R.Builder(new, case)
    memo: dict[int, tuple[int, R.Term]] = {}

    def internalize(i: int) -> tuple[int, R.Term]:
        node = b.steps[i]
        u = R.infer(node.new, new.signature)
        e = R.num(node.budget, u)
        cancel = b.constant(R.num(-node.budget, u), R.num(0, u))
        out = b.rewrite(b.add(i, cancel), node.new, R.add(node.old, e))
        return out, e

    def raise_allowance(i: int, t: R.Term, s: R.Term, e: R.Term,
                        E: R.Term, side: str) -> int:
        # Explicit e <= E, where E=max(e1,e2), then add s and transit.
        a, c = E.args
        edge = b.lattice('max_left' if side == 'left' else 'max_right', a, c)
        edge = b.rewrite(b.add(edge, b.constant(s, s)), R.add(s, e), R.add(s, E))
        return b.rewrite(b.trans(i, edge), t, R.add(s, E))

    def lattice_congruence(kind: str, t1: R.Term, s1: R.Term, i: int, e1: R.Term,
                           t2: R.Term, s2: R.Term, j: int, e2: R.Term):
        E = R.maximum(e1, e2)
        i = raise_allowance(i, t1, s1, e1, E, 'left')
        j = raise_allowance(j, t2, s2, e2, E, 'right')
        if kind == 'max':
            target = R.maximum(s1, s2)
            out = []
            for k, s, side in ((i, s1, 'max_left'), (j, s2, 'max_right')):
                edge = b.lattice(side, s1, s2)
                edge = b.add(edge, b.constant(E, E))
                edge = b.rewrite(edge, R.add(s, E), R.add(target, E))
                out.append(b.trans(k, edge))
            return b.max_common(*out), E
        if kind != 'min':
            raise R.ProofError('Unknown lattice operation.')
        source = R.minimum(t1, t2)
        out = []
        for k, s, side in ((i, s1, 'min_left'), (j, s2, 'min_right')):
            edge = b.lattice(side, t1, t2)
            edge = b.trans(edge, k)
            out.append(b.rewrite(edge, R.sub(source, E), s))
        out_id = b.min_common(*out)
        return b.rewrite(out_id, source, R.add(R.minimum(s1, s2), E)), E

    def visit(index: int) -> tuple[int, R.Term]:
        if index in memo:
            return memo[index]
        node = local.steps[index]
        u = R.infer(node.new, ctx.signature)
        z = R.num(0, u)
        rule = node.rule
        parents = [visit(p) for p in node.parents]
        old_parents = [local.steps[p] for p in node.parents]
        if rule == 'row':
            old_index = node.data[0]
            a, eta, _, _ = R.normalized_row(ctx, case, old_index)
            if old_index in removed:
                v = R.residual(R.num(eta, u), a)
                e = R.add(R.num(eta, u), v)
                i = b.lattice('max_left', R.sub(a, R.num(eta, u)), z)
                i = b.rewrite(i, a, e)
            else:
                i, e = internalize(b.row(renumber[old_index]))
        elif rule == 'constant':
            e = R.num(node.budget, u)
            i = b.constant(node.new, R.add(node.old, e))
        elif rule == 'lattice':
            e = z
            i = b.lattice(*node.data)
        elif rule in ('rewrite', 'negate'):
            i, e = parents[0]
        elif rule in ('add', 'trans'):
            (i, e1), (j, e2) = parents
            i = b.add(i, j)
            e = R.add(e1, e2)
        elif rule == 'scale':
            i, e = parents[0]
            k = node.data[0]
            i, e = b.scale(k, i), R.scale(k, e)
        elif rule == 'convert':
            i, e = parents[0]
            name = node.data[0]
            i, e = b.conversion(name, i), R.convert(name, e)
        elif rule == 'slack':
            i, e = parents[0]
            k = R.num(node.data[0], u)
            edge = b.lattice('min_right', z, k)  # 0 <= k, budget zero.
            i, e = b.add(i, edge), R.add(e, k)
        elif rule == 'meet_proofs':
            (i, e1), (j, e2) = parents
            q = R.sub(node.new, node.old)
            i = b.rewrite(i, q, e1)
            j = b.rewrite(j, q, e2)
            i, e = b.min_common(i, j), R.minimum(e1, e2)
        elif rule == 'max_common':
            (i, e1), (j, e2) = parents
            a, c = old_parents
            e = R.maximum(e1, e2)
            i = raise_allowance(i, a.new, a.old, e1, e, 'left')
            j = raise_allowance(j, c.new, c.old, e2, e, 'right')
            i = b.max_common(i, j)
        elif rule == 'min_common':
            (i, e1), (j, e2) = parents
            a, c = old_parents
            e = R.maximum(e1, e2)
            i = raise_allowance(i, a.new, a.old, e1, e, 'left')
            j = raise_allowance(j, c.new, c.old, e2, e, 'right')
            i = b.rewrite(i, R.sub(node.new, e), a.old)
            j = b.rewrite(j, R.sub(node.new, e), c.old)
            i = b.min_common(i, j)
        elif rule == 'congruence':
            (i, e1), (j, e2) = parents
            a, c = old_parents
            i, e = lattice_congruence(node.data[0], a.new, a.old, i, e1,
                                      c.new, c.old, j, e2)
        elif rule == 'res_congruence':
            (i, e1), (j, e2) = parents
            a, c = old_parents
            # Parent a.new <= a.old; residual reverses this input.
            t, s = R.sub(c.new, a.old), R.sub(c.old, a.new)
            e_inner = R.add(e1, e2)
            i = b.rewrite(b.add(i, j), t, R.add(s, e_inner))
            zero = b.constant(z, z)
            i, e = lattice_congruence('max', t, s, i, e_inner, z, z, zero, z)
        else:
            raise R.ProofError('Unsupported local constructor after localization.')
        i = b.rewrite(i, node.new, R.add(node.old, e))
        memo[index] = i, e
        return i, e

    root, allowance = visit(local.root)
    out = T.prune(new, b.proof(root))
    result = R.check(new, out)
    if result.budget != 0:
        raise R.ProofError('Discharge invariant requires an emitted zero-budget proof.')
    original = R.check(ctx, local)
    penalty = R.sub(allowance, R.num(original.budget, R.infer(original.new, ctx.signature)))
    return SoftResult(new, out, allowance, penalty, original.budget, tuple(sorted(removed)))


def disjoint_hinges(ctx: R.Context, case: str, u: R.Term,
                    alpha: F = F(1), beta: F = F(1)) -> R.Proof:
    """Emit min(alpha*ReLU(u), beta*ReLU(-u)) <=[0] 0, using no rows."""
    alpha, beta = R.rat(alpha), R.rat(beta)
    if alpha < 0 or beta < 0:
        raise R.ProofError('Nonnegative weights are required.')
    unit = R.infer(u, ctx.signature)
    z = R.num(0, unit)
    a, c = R.maximum(u, z), R.maximum(R.scale(-1, u), z)
    m = R.minimum(a, c)
    b = R.Builder(ctx, case)
    zero_a = b.lattice('max_right', u, z)
    u_a = b.lattice('max_left', u, z)
    neg_u = b.rewrite(zero_a, R.scale(-1, u), R.sub(a, u))
    zero = b.rewrite(u_a, z, R.sub(a, u))
    c_bound = b.max_common(neg_u, zero)
    zero = b.rewrite(b.lattice('min_left', a, c), z, R.sub(a, m))
    upper_u = b.trans(b.lattice('min_right', a, c), c_bound)
    upper_u = b.rewrite(upper_u, u, R.sub(a, m))
    m_zero = b.rewrite(b.max_common(upper_u, zero), m, z)
    weighted = R.minimum(R.scale(alpha, a), R.scale(beta, c))
    K = max(alpha, beta)
    if K == 0:
        root = b.constant(weighted, z)
    else:
        results = []
        for weight, positive, side, nonnegative in (
                (alpha, a, 'min_left', zero_a),
                (beta, c, 'min_right', b.lattice('max_right', R.scale(-1, u), z))):
            projection = b.scale(1 / K, b.lattice(side, R.scale(alpha, a), R.scale(beta, c)))
            comparison = b.scale(1 - weight / K, nonnegative)
            comparison = b.rewrite(comparison, R.scale(weight / K, positive), positive)
            results.append(b.rewrite(b.trans(projection, comparison), R.scale(1 / K, weighted), positive))
        root = b.scale(K, b.trans(b.min_common(*results), m_zero))
        root = b.rewrite(root, weighted, z)
    return T.prune(ctx, b.proof(root))


def observation_factor(pairs: tuple[tuple[str, str], ...]) -> dict[str, str]:
    """A finite complete-table witness only; not a general policy checker."""
    if not isinstance(pairs, tuple) or not pairs:
        raise R.ProofError('A nonempty finite table is required.')
    result: dict[str, str] = {}
    for row in pairs:
        if (not isinstance(row, tuple) or len(row) != 2
                or not all(isinstance(s, str) and s for s in row)):
            raise R.ProofError('Observation/action labels must be nonempty strings.')
        obs, action = row
        if obs in result and result[obs] != action:
            raise R.ProofError('The desired action varies inside an observation fiber.')
        result[obs] = action
    return result


def report():
    ctx, p, roots = R.reflection_example()
    soft = soften_rows(ctx, replace(p, root=roots['intended']), 'h', (3,))
    hctx = R.context(('u',), (), {'u': 0})
    hinge = disjoint_hinges(hctx, 'h', R.src('u'), F(2), F(3))
    return {
        'scope': 'single-case symbolic discharge, not a literal-bound oracle or general policy checker',
        'soft_reflection': {
            'base_budget': str(soft.old_local_budget),
            'root_budget': str(R.check(soft.context, soft.proof).budget),
            'current_rows_used': [list(x) for x in sorted(T.used_rows(soft.context, soft.proof))],
            'allowance': R.serial(soft.allowance),
            'context': R.serial(soft.context), 'proof': R.serial(soft.proof),
            'high_discrepancy_point': {'e': '5/32', 'violation': '1/8', 'actual_difference': '3/32'},
            'separately_supplied_law': {'high_probability': '1/8', 'mean_violation': '1/64',
                                      'actual_mean_difference': '-11/256', 'guaranteed_bound': '-1/64'},
        },
        'disjoint_hinges': {'weights': ['2', '3'], 'budget': str(R.check(hctx, hinge).budget),
                            'source_rows_used': len(T.used_rows(hctx, hinge)), 'proof': R.serial(hinge)},
        'limitations': ['No new trusted instruction', 'No empirical calibration',
                        'No automatic sign splitter', 'No neural training',
                        'Expected claims require their extra probability law and integrability'],
    }


class F06DischargeTests(unittest.TestCase):
    def test_reflective_discharge_removes_only_discrepancy_assumption(self):
        ctx, p, roots = R.reflection_example()
        out = soften_rows(ctx, replace(p, root=roots['intended']), 'h', (3,))
        self.assertEqual(out.old_local_budget, F(-1, 32))
        self.assertEqual(R.check(out.context, out.proof).budget, 0)
        self.assertEqual(T.used_rows(out.context, out.proof), frozenset({('h', 1)}))
        self.assertEqual(len(out.context.cases[0].rows), len(ctx.cases[0].rows)-1)

    def test_discharge_valid_off_old_source(self):
        ctx, p, roots = R.reflection_example()
        out = soften_rows(ctx, replace(p, root=roots['intended']), 'h', (3,))
        for e in (F(-2), F(0), F(1, 32), F(5, 32), F(10**20)):
            point = dict(p=F(3, 4), s=F(1, 4), e=e, z=F(10**30), w=-F(10**30))
            self.assertTrue(R.reference_holds(out.context, out.proof, point, 'h'))
            expected = F(-1, 32)+max(e-F(1, 32), 0)
            self.assertEqual(R.evaluate(out.allowance, out.context.signature, point), expected)
            if e > F(1, 32): self.assertFalse(ctx.feasible('h', point))

    def test_no_withdrawal_internalizes_same_budget(self):
        ctx, p = R.composition_example()
        out = soften_rows(ctx, p, 'h', ())
        self.assertEqual(R.evaluate(out.allowance, ctx.signature, dict(ctx.cases[0].witness)), F(-1, 2))
        self.assertEqual(R.check(out.context, out.proof).budget, 0)

    def test_all_localized_S1_examples_emit_checked_soft_proofs(self):
        for name, (ctx, p) in R.examples().items():
            cases = ctx.cases if p.steps[p.root].case is None else tuple(h for h in ctx.cases if h.name == p.steps[p.root].case)
            for h in cases:
                out = soften_rows(ctx, p, h.name, tuple(range(len(h.rows))))
                self.assertEqual(R.check(out.context, out.proof).budget, 0, name)
                self.assertFalse(T.used_rows(out.context, out.proof), name)
                point = dict(h.witness)
                self.assertEqual(R.evaluate(out.penalty, ctx.signature, point), 0, name)

    def test_soft_lattice_congruence_both_kinds(self):
        x, y = R.src('x'), R.src('y')
        ctx = R.context(('x','y'), (R.Row(x,R.num(-1)), R.Row(y,R.num(1))), {'x':-1,'y':1})
        for kind in ('min', 'max'):
            b=R.Builder(ctx,'h'); b.congruence(kind,b.row(0),b.row(1))
            out=soften_rows(ctx,b.proof(),'h',(0,1))
            for a,c in product((F(-2),F(0),F(2)),repeat=2):
                point={'x':a,'y':c}
                self.assertTrue(R.reference_holds(out.context,out.proof,point,'h'))
                self.assertGreaterEqual(R.evaluate(out.penalty,ctx.signature,point),0)

    def test_slack_negation_and_nonnegative_scale(self):
        ctx,p=T.alternative_example(); b=R.Builder(ctx,'h')
        i=b.negate(b.row(0)); i=b.scale(2,i); b.slack(F(1,3),i)
        out=soften_rows(ctx,b.proof(),'h',(0,1))
        for x in (F(-3),F(0),F(5)):
            self.assertTrue(R.reference_holds(out.context,out.proof,{'x':x},'h'))

    def test_soft_result_does_not_keep_original_negative_scalar_budget(self):
        ctx,p,_=R.reflection_example(); out=soften_rows(ctx,p,'h',(3,))
        root=out.proof.steps[out.proof.root]
        damaged=replace(out.proof,steps=out.proof.steps[:-1]+(replace(root,budget=out.old_local_budget),))
        with self.assertRaises(R.ProofError): R.check(out.context,damaged)

    def test_root_remains_local_after_global_specialization(self):
        ctx,p,_=R.quadratic_example(); out=soften_rows(ctx,p,'1',(0,))
        self.assertEqual(out.old_local_budget,F(-15,64))
        self.assertEqual(R.check(out.context,out.proof).case,'1')
        self.assertEqual(R.evaluate(out.penalty,ctx.signature,dict(ctx.cases[1].witness)),0)

    def test_discharge_indices_and_unknown_case_rejected(self):
        ctx,p=T.alternative_example()
        for ids in ((True,),(-1,),(3,),(0,0),[0]):
            with self.assertRaises((R.ProofError,TypeError)): soften_rows(ctx,p,'h',ids)
        with self.assertRaises(R.ProofError): soften_rows(ctx,p,'absent',(0,))

    def test_old_context_unchanged(self):
        ctx,p=T.alternative_example(); before=R.fingerprint(ctx)
        out=soften_rows(ctx,p,'h',(0,1))
        self.assertEqual(R.fingerprint(ctx),before)
        self.assertNotEqual(R.fingerprint(out.context),before)

    def test_disjoint_hinge_trace_for_rational_weights(self):
        ctx=R.context(('u',),(),{'u':0})
        for a,c in product((F(0),F(1,2),F(1),F(2)),repeat=2):
            p=disjoint_hinges(ctx,'h',R.src('u'),a,c)
            self.assertEqual(R.check(ctx,p).budget,0)
            self.assertFalse(T.used_rows(ctx,p))
            for x in (F(-10**30),F(-1),F(0),F(1),F(10**30)):
                self.assertTrue(R.reference_holds(ctx,p,{'u':x},'h'))

    def test_hinge_proof_has_primitive_expansion(self):
        ctx=R.context(('u',),(),{'u':0})
        p=disjoint_hinges(ctx,'h',R.src('u'),F(2),F(3))
        self.assertEqual(T.check_primitives(ctx,T.compile_primitives(ctx,p)).budget,0)

    def test_unrelated_positive_hinges_do_not_vanish(self):
        self.assertEqual(min(max(F(1),0),max(F(2),0)),1)

    def test_negative_hinge_weight_not_admitted_by_macro(self):
        ctx=R.context(('u',),(),{'u':0})
        with self.assertRaises(R.ProofError): disjoint_hinges(ctx,'h',R.src('u'),F(-1),F(1))

    def test_expected_violation_bridge_finite_model(self):
        p=F(1,8); lo=F(0); hi=F(5,32)
        mean_violation=p*max(hi-F(1,32),0)+(1-p)*max(lo-F(1,32),0)
        actual=p*(F(-1,16)+hi)+(1-p)*(F(-1,16)+lo)
        self.assertEqual(mean_violation,F(1,64))
        self.assertEqual(actual,F(-11,256))
        self.assertLessEqual(actual,F(-1,32)+mean_violation)
        self.assertGreater(F(-1,16)+hi,0)

    def test_rare_violation_needs_magnitude_bound(self):
        for n in (2,10,10**6): self.assertEqual(F(1,n)*n,1)

    def test_nonlinear_budget_at_mean_is_not_mean_budget(self):
        self.assertEqual(F(1,2)*max(1,0)+F(1,2)*max(0,1),1)
        self.assertEqual(max(F(1,2),F(1,2)),F(1,2))

    def test_availability_pruning_not_complete_after_numeric_updates(self):
        P=lambda a,b:(a+3*b)/4
        Q=lambda a,b:(3*a+b)/4
        self.assertLess(Q(F(0),F(4)),P(F(0),F(4)))
        self.assertGreater(Q(F(4),F(0)),P(F(4),F(0)))

    def test_fixed_policy_can_ignore_lost_observation_detail(self):
        self.assertEqual(observation_factor((('hidden','stay'),('hidden','stay'))),{'hidden':'stay'})
        with self.assertRaises(R.ProofError): observation_factor((('hidden','left'),('hidden','right')))

    def test_richer_observation_has_finite_policy_translator(self):
        self.assertEqual(observation_factor((('seen_left','left'),('seen_right','right'))),
                         {'seen_left':'left','seen_right':'right'})

    def test_observation_table_validation(self):
        for value in ((),(('o',''),),[("o","a")],(('o',1),)):
            with self.assertRaises(R.ProofError): observation_factor(value)

    def test_hidden_bit_randomized_minimax_gap(self):
        for k in range(11):
            p=F(k,10)
            self.assertGreaterEqual(max(2*p,2*(1-p)),1)
        self.assertEqual(max(2*F(1,2),2*(1-F(1,2))),1)

    def test_selected_marginal_confidence_counterexample(self):
        pairs=((-1,1),(1,-1),(1,1),(1,1))
        self.assertEqual(sum(a>=0 for a,b in pairs),3)
        self.assertEqual(sum(b>=0 for a,b in pairs),3)
        self.assertEqual(sum(min(a,b)>=0 for a,b in pairs),2)

    def test_soft_budget_has_exact_finite_relu_availability_gate(self):
        for a in (0,1):
            for v in (F(0),F(1,4),F(1),F(5),F(10**20)):
                gate=T.gated_bound(a,F(-1)+v,F(-1))
                self.assertEqual(gate,-max(F(a)-v,F(0)))
        self.assertEqual(-max(F(1,2),0),F(-1,2))  # Not licensed by a confidence-only flag.


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--json',type=Path); args=p.parse_args()
    result=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(F06DischargeTests))
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),sort_keys=True,indent=2)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
