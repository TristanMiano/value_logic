"""Finite F06 proof transport and withdrawal audits (Python 3.10+, stdlib).

Every successful reconstruction returns an ordinary S1 proof, checked against
its *new* context. This is neither arbitrary proof search nor empirical source
validation. Missing evidence is not represented as a numerical cost.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from typing import Mapping
import unittest

from v2.checks import f06_inference_rules as R
from v2.checks.f05_semantics import substitute

PRIMITIVES = frozenset({'constant', 'row', 'rewrite', 'add', 'scale', 'convert',
                        'lattice', 'max_common', 'min_common', 'all_cases'})
RowKey = tuple[str, int]
ReplacementKey = tuple[str, str, int]  # new case, old case, old row


class UnavailableProof(R.ProofError):
    """The retained proof family has no reconstruction for a required case."""


class FrontierLimit(R.ProofError):
    """Explicit frontier enumeration exceeded its declared resource limit."""


def reachable(proof: R.Proof) -> tuple[int, ...]:
    """Strict-backward-reference validation is performed by the caller's check."""
    todo = [proof.root]
    found: set[int] = set()
    while todo:
        i = todo.pop()
        if i not in found:
            found.add(i)
            todo.extend(proof.steps[i].parents)
    return tuple(sorted(found))


def prune(ctx: R.Context, proof: R.Proof) -> R.Proof:
    R.check(ctx, proof)
    order = reachable(proof)
    remap = {old: new for new, old in enumerate(order)}
    out = R.Proof(tuple(replace(proof.steps[i], parents=tuple(remap[p] for p in proof.steps[i].parents))
                        for i in order), remap[proof.root])
    R.check(ctx, out)
    return out


def used_rows(ctx: R.Context, proof: R.Proof) -> frozenset[RowKey]:
    R.check(ctx, proof)
    return frozenset((proof.steps[i].case, proof.steps[i].data[0])
                     for i in reachable(proof) if proof.steps[i].rule == 'row')


def _append_checked_shape(builder: R.Builder, template: R.Step,
                          parents: tuple[int, ...], case: str | None,
                          term_map=lambda t: t) -> int:
    def payload(value):
        if isinstance(value, R.Term):
            return term_map(value)
        if isinstance(value, tuple):
            return tuple(payload(x) for x in value)
        return value
    step = R.Step(template.rule, parents, case, term_map(template.new),
                  term_map(template.old), F(0), builder.cid, payload(template.data))
    t, s, budget = R._expected(builder.ctx, step, builder.steps)
    if not R.same_difference(step.new, step.old, t, s, builder.ctx.signature):
        raise R.ProofError('Substituted rule conclusion does not match its premises.')
    builder.steps.append(replace(step, budget=budget))
    return len(builder.steps) - 1


def localize(ctx: R.Context, proof: R.Proof, case: str) -> R.Proof:
    """Specialize a global trace to one existing hidden case; no action choice."""
    R.check(ctx, proof)
    if case not in {h.name for h in ctx.cases}:
        raise R.ProofError('Unknown localization case.')
    builder = R.Builder(ctx, case)
    cache: dict[int, int] = {}

    def visit(i: int) -> int:
        if i in cache:
            return cache[i]
        old = proof.steps[i]
        if old.case not in (None, case):
            raise R.ProofError('A local proof cannot be reassigned to another case.')
        if old.rule == 'all_cases':
            parent = next(p for p in old.parents if proof.steps[p].case == case)
            out = builder.rewrite(visit(parent), old.new, old.old)
        else:
            out = _append_checked_shape(builder, old, tuple(visit(p) for p in old.parents), case)
        cache[i] = out
        return out

    root = visit(proof.root)
    return prune(ctx, builder.proof(root))


def _copy_into(builder: R.Builder, proof: R.Proof) -> int:
    proof = prune(builder.ctx, proof)
    offset = len(builder.steps)
    builder.steps.extend(replace(s, parents=tuple(p + offset for p in s.parents)) for s in proof.steps)
    return proof.root + offset


def _source_mapping(old: R.Context, new: R.Context,
                    mapping: Mapping[str, R.Term] | None):
    if old.signature.scope != new.signature.scope or old.observation != new.observation:
        raise R.ProofError('Versioned interpretation/observation changed: a separate bridge is required.')
    if old.signature.units != new.signature.units or old.signature.conversions != new.signature.conversions:
        raise R.ProofError('This adapter keeps unit and conversion meanings fixed.')
    if mapping is None:
        if old.signature != new.signature:
            raise R.ProofError('Changed coordinates require an explicit source substitution.')
        mapping = {k: R.src(k) for k, _ in old.signature.sources}
    mapping = dict(mapping)
    if set(mapping) != {k for k, _ in old.signature.sources}:
        raise R.ProofError('Supply every old source key, exactly once.')
    for key, unit in old.signature.sources:
        if R.infer(mapping[key], new.signature) != unit:
            raise R.ProofError('Substitution has a wrong source unit or free local.')
    return lambda t: substitute(t, mapping, old.signature, new.signature)


def transport(old: R.Context, new: R.Context, proof: R.Proof,
              replacements: Mapping[ReplacementKey, R.Proof],
              case_map: Mapping[str, str],
              source_map: Mapping[str, R.Term] | None = None) -> R.Proof:
    """Graft current proofs of used source leaves and recalculate all budgets.

    Replacements need not be at least as strong as old rows. Weaker replacements
    yield newly calculated bounds, never a copied historical bound. A missing
    replacement can be bypassed only by an available alternative or an exact
    constant simplification. Every new live case is covered on success.
    """
    R.check(old, proof)
    new.validate()
    sigma = _source_mapping(old, new, source_map)
    new_names = {h.name for h in new.cases}
    old_names = {h.name for h in old.cases}
    if set(case_map) != new_names or any(v not in old_names for v in case_map.values()):
        raise R.ProofError('The case map must cover exactly every new live case.')
    checked_replacements = {}
    for key, q in replacements.items():
        if (not isinstance(key, tuple) or len(key) != 3 or key[0] not in new_names
                or key[1] not in old_names):
            raise R.ProofError('Malformed replacement key.')
        a, _, unit, _ = R.normalized_row(old, key[1], key[2])
        root = R.check(new, q)
        if root.case not in (None, key[0]):
            raise R.ProofError('Replacement is local to a different new case.')
        if not R.same_difference(root.new, root.old, sigma(a), R.num(0, unit), new.signature):
            raise R.ProofError('Replacement proves a different source expression/direction.')
        checked_replacements[key] = localize(new, q, key[0])

    global_builder = R.Builder(new)
    local_roots = []
    for h in new.cases:
        old_case = case_map[h.name]
        local = localize(old, proof, old_case)
        builder = R.Builder(new, h.name)
        cache: dict[int, int | None] = {}
        graft_cache: dict[ReplacementKey, int] = {}

        def visit(i: int) -> int | None:
            if i in cache:
                return cache[i]
            step = local.steps[i]
            t, s = sigma(step.new), sigma(step.old)
            form = R._form(R.sub(t, s), new.signature)
            if not form[0]:
                out = builder.constant(t, s)
            elif step.rule == 'row':
                key = (h.name, old_case, step.data[0])
                q = checked_replacements.get(key)
                if q is None:
                    out = None
                else:
                    if key not in graft_cache:
                        graft_cache[key] = _copy_into(builder, q)
                    out = builder.rewrite(graft_cache[key], t, s)
            elif step.rule == 'meet_proofs':
                available = [v for p in step.parents if (v := visit(p)) is not None]
                out = None if not available else builder.rewrite(
                    min(available, key=lambda j: (builder.steps[j].budget, j)), t, s)
            else:
                parents = tuple(visit(p) for p in step.parents)
                out = None if any(p is None for p in parents) else _append_checked_shape(
                    builder, step, parents, h.name, sigma)
            cache[i] = out
            return out

        local_root = visit(local.root)
        if local_root is None:
            raise UnavailableProof(f'No retained reconstruction for live case {h.name!r}.')
        q = prune(new, builder.proof(local_root))
        local_roots.append(_copy_into(global_builder, q))
    # A uniform expression pair prevents hidden-case-dependent policy choices.
    root = global_builder.all_cases(local_roots)
    return prune(new, global_builder.proof(root))


def restrict_rows(ctx: R.Context, proof: R.Proof,
                  alive: frozenset[RowKey], revision: str = 'withdrawal-v2') -> tuple[R.Context, R.Proof]:
    """Identity-coordinate example adapter: drop rows, reindex, and reconstruct."""
    ctx.validate()
    keys = {(h.name, i) for h in ctx.cases for i in range(len(h.rows))}
    if not alive <= keys:
        raise R.ProofError('Unknown row in alive set.')
    cases = []
    index = {}
    for h in ctx.cases:
        keep = [i for i in range(len(h.rows)) if (h.name, i) in alive]
        cases.append(R.Case(h.name, tuple(h.rows[i] for i in keep), h.witness))
        index.update({(h.name, old_i): new_i for new_i, old_i in enumerate(keep)})
    new = replace(ctx, revision=revision, cases=tuple(cases))
    replacements = {}
    for (name, old_i), new_i in index.items():
        b = R.Builder(new, name)
        b.row(new_i)
        replacements[(name, name, old_i)] = b.proof()
    result = transport(ctx, new, proof, replacements, {h.name: h.name for h in ctx.cases})
    return new, result


def compile_primitives(ctx: R.Context, proof: R.Proof) -> R.Proof:
    """Elaborate six derived tags away at this fixed numerical snapshot."""
    R.check(ctx, proof)
    b = R.Builder(ctx)
    memo: dict[int, int] = {}

    def trans(i: int, j: int) -> int:
        left, right = b.steps[i], b.steps[j]
        k = b.add(i, j)
        return b.rewrite(k, left.new, right.old)

    def congruence(kind: str, i: int, j: int) -> int:
        left, right = b.steps[i], b.steps[j]
        if kind == 'max':
            p = trans(i, b.lattice('max_left', left.old, right.old))
            q = trans(j, b.lattice('max_right', left.old, right.old))
            return b.max_common(p, q)
        p = trans(b.lattice('min_left', left.new, right.new), i)
        q = trans(b.lattice('min_right', left.new, right.new), j)
        return b.min_common(p, q)

    def visit(i: int) -> int:
        if i in memo:
            return memo[i]
        s = proof.steps[i]
        if s.rule == 'meet_proofs':
            chosen = min(s.parents, key=lambda p: (proof.steps[p].budget, p))
            p = visit(chosen)
            b.case = s.case
            out = b.rewrite(p, s.new, s.old)
        else:
            parents = tuple(visit(p) for p in s.parents)
            b.case = s.case
            if s.rule in PRIMITIVES:
                out = _append_checked_shape(b, s, parents, s.case)
            elif s.rule == 'trans':
                out = trans(*parents)
            elif s.rule == 'negate':
                out = b.rewrite(parents[0], s.new, s.old)
            elif s.rule == 'slack':
                k = R.rat(s.data[0]); u = R.infer(s.new, ctx.signature)
                zero, amount = R.num(0, u), R.num(k, u)
                q = b.lattice('min_right', zero, amount)
                q = b.add(q, b.constant(amount, zero))
                out = b.add(parents[0], q)
            elif s.rule == 'congruence':
                out = congruence(s.data[0], *parents)
            elif s.rule == 'res_congruence':
                left, right = (b.steps[p] for p in parents)
                u = R.infer(left.new, ctx.signature)
                reverse = b.rewrite(parents[0], R.scale(-1, left.old), R.scale(-1, left.new))
                inner = b.add(parents[1], reverse)
                zero = b.constant(R.num(0, u), R.num(0, u))
                out = congruence('max', inner, zero)
            else:
                raise R.ProofError('No primitive expansion for rule.')
            out = b.rewrite(out, s.new, s.old)
        if b.steps[out].budget != s.budget:
            raise R.ProofError('Elaboration changed a fixed-snapshot budget.')
        memo[i] = out
        return out

    root = visit(proof.root)
    result = prune(ctx, b.proof(root))
    check_primitives(ctx, result)
    return result


def check_primitives(ctx: R.Context, proof: R.Proof) -> R.Step:
    if any(s.rule not in PRIMITIVES for s in proof.steps):
        raise R.ProofError('An unexpanded derived rule remains in this trace.')
    return R.check(ctx, proof)


@dataclass(frozen=True)
class Label:
    support: frozenset[RowKey]
    budget: F


def irredundant(labels) -> tuple[Label, ...]:
    normalized = {Label(frozenset(x.support), R.rat(x.budget)) for x in labels}
    kept = [x for x in normalized if not any(y != x and y.support <= x.support
                                            and y.budget <= x.budget for y in normalized)]
    return tuple(sorted(kept, key=lambda x: (len(x.support), tuple(sorted(x.support)), x.budget)))


def best_label(labels: tuple[Label, ...], alive: frozenset[RowKey]) -> F | None:
    choices = [x.budget for x in labels if x.support <= alive]
    return min(choices) if choices else None


def support_frontier(ctx: R.Context, proof: R.Proof, *, limit: int = 4096) -> tuple[Label, ...]:
    """Exact explicit labels for the declared finite salvage grammar, not search."""
    R.check(ctx, proof)
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise R.ProofError('Positive integer frontier limit required.')
    fronts = []
    for s in proof.steps:
        form = R._form(R.sub(s.new, s.old), ctx.signature)
        labels = [] if form[0] else [Label(frozenset(), form[1])]
        if s.rule == 'row':
            labels.append(Label(frozenset({(s.case, s.data[0])}), s.budget))
        elif s.rule in ('constant', 'lattice'):
            labels.append(Label(frozenset(), s.budget))
        elif s.rule == 'meet_proofs':
            labels.extend(x for p in s.parents for x in fronts[p])
        elif s.rule == 'scale' and R.rat(s.data[0]) == 0:
            labels.append(Label(frozenset(), F(0)))
        else:
            combinations = 1
            for p in s.parents:
                combinations *= len(fronts[p])
            if combinations > limit:
                raise FrontierLimit('Declared explicit-frontier work limit exceeded.')
            for parents in product(*(fronts[p] for p in s.parents)):
                v = [p.budget for p in parents]
                support = frozenset().union(*(p.support for p in parents))
                if s.rule in ('rewrite', 'negate'): budget = v[0]
                elif s.rule in ('trans', 'add'): budget = sum(v, F(0))
                elif s.rule == 'scale': budget = R.rat(s.data[0]) * v[0]
                elif s.rule == 'convert': budget = ctx.signature.conversion(s.data[0]).factor * v[0]
                elif s.rule == 'slack': budget = v[0] + R.rat(s.data[0])
                elif s.rule in ('max_common', 'min_common', 'congruence', 'all_cases'): budget = max(v)
                elif s.rule == 'res_congruence': budget = max(sum(v, F(0)), F(0))
                else: raise R.ProofError('Unknown frontier rule.')
                labels.append(Label(support, budget))
        fronts.append(irredundant(labels))
        if len(fronts[-1]) > limit:
            raise FrontierLimit('Declared explicit-frontier size limit exceeded.')
    return fronts[proof.root]


def reflective_transport_example():
    old, proof, roots = R.reflection_example()
    p, s, e = map(R.src, ('p', 's', 'e'))
    rows = (R.Row(R.num(F(3,4), 'P'), p), R.Row(p, R.num(1, 'P')),
            R.Row(R.num(0, 'P'), s), R.Row(s, R.num(F(1,8), 'P')),
            R.Row(e, R.num(F(1,32), 'J')))
    new = replace(old, revision='withdraw-and-replace-v2',
                  cases=(R.Case('current', rows, (('p', F(3,4)), ('s', F(1,8)),
                                               ('e', F(0)), ('z', F(0)), ('w', F(0)))),))
    b = R.Builder(new, 'current')
    slope = b.add(b.row(0), b.row(3))
    slope = b.rewrite(slope, R.sub(s, p), R.num(0, 'P'))
    q_slope = b.proof(slope)
    b = R.Builder(new, 'current'); b.row(4); q_error = b.proof()
    final = transport(old, new, replace(proof, root=roots['intended']),
                      {('current','h',1): q_slope, ('current','h',3): q_error}, {'current':'h'})
    return old, new, final, proof, roots


def affine_transport_example():
    x, z = R.src('x'), R.src('z')
    old = R.context(('x',), (R.Row(x, R.num(1)), R.Row(R.num(0), x)), {'x':0}, scope='coordinate-v1')
    b = R.Builder(old, 'h'); b.row(0); p = b.proof()
    new = R.context(('z',), (R.Row(z, R.num(2)), R.Row(R.num(0), z)), {'z':0}, scope='coordinate-v1', revision='v2')
    b = R.Builder(new, 'h'); b.scale(F(1,2), b.row(0)); q = b.proof()
    out = transport(old, new, p, {('h','h',0): q}, {'h':'h'}, {'x': R.scale(F(1,2), z)})
    return old, new, out, p


def alternative_example():
    x = R.src('x')
    ctx = R.context(('x',), (R.Row(x, R.num(-1)), R.Row(x, R.num(0))), {'x':-1})
    b = R.Builder(ctx, 'h'); b.meet(b.row(0), b.row(1))
    return ctx, b.proof()


def symbolic_repair_example():
    d1, d2, u = map(R.src, ('d1','d2','u'))
    ctx = R.context(('d1','d2','u'),
        (R.Row(R.sub(d1, u), R.num(F(-3,4))), R.Row(R.add(d2, u), R.num(F(1,4)))),
        {'d1': F(-3,4), 'd2':F(1,4), 'u':0})
    # Move the finite row budget into the compared expression using a
    # constant equality; a rewrite alone cannot change the difference.
    b = R.Builder(ctx, 'h')
    a = b.add(b.row(0), b.constant(R.num(F(3,4)), R.num(0)))
    a = b.rewrite(a, d1, R.sub(u, R.num(F(3,4))))
    c = b.add(b.row(1), b.constant(R.num(F(-1,4)), R.num(0)))
    c = b.rewrite(c, d2, R.sub(R.num(F(1,4)), u))
    out = b.add(a, c)
    out = b.rewrite(out, R.add(d1,d2), R.num(F(-1,2)))
    out = b.add(out, b.constant(R.num(F(-1,2)), R.num(0)))
    b.rewrite(out, R.add(d1,d2), R.num(0))
    return ctx, b.proof()


def gated_bound(available: int, budget: F, lower: F, fallback: F = F(0)) -> F:
    """The bounded-domain CPWA construction, only at exact Boolean flags."""
    if isinstance(available, bool) or not isinstance(available, int) or available not in (0,1):
        raise R.ProofError('Availability is an exact 0/1 protocol field, not confidence.')
    budget, lower, fallback = map(R.rat, (budget, lower, fallback))
    if budget < lower or lower > fallback:
        raise R.ProofError('Gating domain certificate is not satisfied.')
    return min(fallback, budget + (fallback-lower)*(1-available))


def report():
    _, new, p, _, _ = reflective_transport_example()
    _, coord, q, _ = affine_transport_example()
    alt, ap = alternative_example()
    withdrawn, wp = restrict_rows(alt, ap, frozenset({('h',1)}))
    sym, sp = symbolic_repair_example()
    compiled = {}
    for name, (ctx, proof) in R.examples().items():
        cp = compile_primitives(ctx, proof)
        compiled[name] = {'original_nodes':len(proof.steps), 'primitive_nodes':len(cp.steps),
                          'budget':R.check(ctx, cp).budget}
    return R.serial({'scope':'Finite F06 audit; no empirical source validation or arbitrary proof search.',
        'primitive_rule_tags':sorted(PRIMITIVES), 'compiled_S1_examples':compiled,
        'reflection':{'budget':R.check(new,p).budget, 'current_used_rows':sorted(used_rows(new,p)),
                      'new_context':new, 'proof':p},
        'coordinate_transport':{'budget':R.check(coord,q).budget, 'proof':q},
        'withdrawal':{'old_budget':R.check(alt,ap).budget, 'current_budget':R.check(withdrawn,wp).budget,
                      'frontier':[{'support':sorted(x.support),'budget':x.budget} for x in support_frontier(alt,ap)], 'proof':wp},
        'symbolic_allowance':{'budget':R.check(sym,sp).budget, 'proof':sp},
        'boundaries':'Frontiers are snapshot-relative; no proof means no retained warrant, not refutation. '
                     'CPWA gating needs its domain; one current derivative is not a proof of a learned mechanism.'})


class F06TransportTests(unittest.TestCase):
    def test_reflective_proof_graft(self):
        _, new, proof, _, _ = reflective_transport_example()
        self.assertEqual(R.check(new, proof).budget, F(-1,16))
        self.assertEqual(used_rows(new, proof), frozenset({('current',0),('current',3),('current',4)}))

    def test_reuse_without_full_context_inclusion(self):
        old, new, proof, _, _ = reflective_transport_example()
        point = dict(p=F(1),s=F(0),e=F(0),z=F(0),w=F(0))
        self.assertTrue(new.feasible('current', point))
        self.assertFalse(old.feasible('h', point))
        self.assertTrue(R.reference_holds(new, proof, point, 'current'))

    def test_report_and_improvement_remain_different(self):
        _, new, proof, _, _ = reflective_transport_example()
        point = dict(p=F(1),s=F(1,8),e=F(1,32),z=F(1000),w=F(-1000))
        self.assertTrue(new.feasible('current', point))
        h0 = F(1,2)*point['p'] + F(1,2)*point['s']
        h1 = F(1,4)*point['p'] + F(3,4)*point['s']
        self.assertEqual(h0-F(1,2), F(1,16))
        self.assertEqual(h1-F(3,4), F(-13,32))
        self.assertTrue(R.reference_holds(new, proof, point, 'current'))

    def test_affine_coordinate_substitution(self):
        _, new, proof, _ = affine_transport_example()
        self.assertEqual(R.check(new, proof).budget, 1)
        for z in (F(0), F(1), F(2)):
            self.assertTrue(R.reference_holds(new, proof, {'z':z}, 'h'))

    def test_tighter_and_weaker_leaf_budgets_recomputed(self):
        old, p = alternative_example()
        # The first row was x<=-1. A current x<=3/2 row is much weaker.
        new = replace(old, revision='weaker', cases=(R.Case('h', (R.Row(R.src('x'),R.num(F(3,2))),), (('x',F(0)),)),))
        b=R.Builder(new,'h'); b.row(0)
        out=transport(old,new,p,{('h','h',0):b.proof()},{'h':'h'})
        self.assertEqual(R.check(new,out).budget,F(3,2))
        self.assertTrue(R.reference_holds(new,out,{'x':F(3,2)},'h'))

    def test_mapping_one_point_does_not_preserve_old_bound(self):
        old, new, _, p=affine_transport_example()
        new=replace(new,cases=(R.Case('h',(R.Row(R.src('z'),R.num(1)),),(('z',F(0)),)),))
        b=R.Builder(new,'h'); b.scale(2,b.row(0))
        out=transport(old,new,p,{('h','h',0):b.proof()},{'h':'h'},{'x':R.scale(2,R.src('z'))})
        self.assertEqual(R.check(new,out).budget,2)
        root=R.check(new,out)
        self.assertGreater(R.evaluate(root.new,new.signature,{'z':F(1)})-R.evaluate(root.old,new.signature,{'z':F(1)}),1)

    def test_wrong_replacement_direction_rejected(self):
        old,new,_,p=affine_transport_example()
        b=R.Builder(new,'h'); b.scale(F(1,2),b.row(1))
        with self.assertRaises(R.ProofError):
            transport(old,new,p,{('h','h',0):b.proof()},{'h':'h'},{'x':R.scale(F(1,2),R.src('z'))})

    def test_changed_scope_rejected(self):
        old,p=alternative_example(); new=replace(old,signature=replace(old.signature,scope='other-program'))
        with self.assertRaises(R.ProofError): transport(old,new,p,{}, {'h':'h'})

    def test_changed_observation_rejected(self):
        old,p=alternative_example(); new=replace(old,observation='reveals-hidden-state')
        with self.assertRaises(R.ProofError): transport(old,new,p,{}, {'h':'h'})

    def test_missing_source_substitution_rejected(self):
        old,new,_,p=affine_transport_example()
        with self.assertRaises(R.ProofError): transport(old,new,p,{}, {'h':'h'}, {})

    def test_free_local_substitution_rejected(self):
        old,new,_,p=affine_transport_example()
        with self.assertRaises((R.ProofError,R.SemanticError)):
            transport(old,new,p,{}, {'h':'h'}, {'x':R.loc('z')})

    def test_conversion_table_change_rejected(self):
        old,p=alternative_example()
        new=replace(old,signature=replace(old.signature,conversions=(R.Conversion('scaleU','U','U',F(2)),)))
        with self.assertRaises(R.ProofError): transport(old,new,p,{}, {'h':'h'})

    def test_nonlinear_source_map_with_explicit_premise_proof(self):
        old,new,_,p=affine_transport_example()
        new=replace(new,cases=(R.Case('h',(R.Row(R.src('z'),R.num(1)),),(('z',F(0)),)),))
        b=R.Builder(new,'h'); b.max_common(b.row(0),b.constant(R.num(0),R.num(0)))
        out=transport(old,new,p,{('h','h',0):b.proof()},{'h':'h'}, {'x':R.maximum(R.src('z'),R.num(0))})
        self.assertEqual(R.check(new,out).budget,1)
        for z in (F(-10),F(0),F(1)):
            self.assertTrue(R.reference_holds(new,out,{'z':z},'h'))

    def test_lexical_source_substitution_does_not_capture(self):
        old,new,_,_=affine_transport_example()
        x=R.src('x'); b=R.Builder(old,'h')
        root=b.max_common(b.row(0),b.constant(R.num(0),R.num(0)))
        t=R.let('x',x,R.maximum(R.loc('x'),R.num(0)))
        b.rewrite(root,t,R.num(0)); p=b.proof()
        q=R.Builder(new,'h'); q.scale(F(1,2),q.row(0))
        out=transport(old,new,p,{('h','h',0):q.proof()},{'h':'h'},{'x':R.scale(F(1,2),R.src('z'))})
        self.assertTrue(R.reference_holds(new,out,{'z':F(2)},'h'))

    def test_all_new_cases_covered(self):
        old,p=alternative_example(); x=R.src('x')
        new=replace(old,revision='two-cases',cases=(R.Case('a',(R.Row(x,R.num(1)),),(('x',F(0)),)),
                                                     R.Case('b',(R.Row(x,R.num(2)),),(('x',F(0)),))))
        repl={}
        for name in ('a','b'):
            b=R.Builder(new,name); b.row(0); repl[(name,'h',0)]=b.proof()
        out=transport(old,new,p,repl,{'a':'h','b':'h'})
        self.assertEqual(R.check(new,out).budget,2)
        self.assertIsNone(R.check(new,out).case)

    def test_incomplete_case_map_rejected(self):
        old,p=alternative_example()
        with self.assertRaises(R.ProofError): transport(old,old,p,{}, {})

    def test_missing_live_case_proof_is_not_ignored(self):
        old,p=R.mixture_example()
        alive=frozenset({('h1',0),('h1',1)})
        with self.assertRaises(UnavailableProof): restrict_rows(old,p,alive)

    def test_one_alternative_survives_withdrawal(self):
        old,p=alternative_example()
        new,q=restrict_rows(old,p,frozenset({('h',1)}))
        self.assertEqual(R.check(new,q).budget,0)
        self.assertEqual(used_rows(new,q),frozenset({('h',0)}))

    def test_no_alternative_means_no_retained_proof(self):
        old,p=alternative_example()
        with self.assertRaises(UnavailableProof): restrict_rows(old,p,frozenset())

    def test_zero_scaling_discharges_withdrawn_row(self):
        old,_=alternative_example(); b=R.Builder(old,'h'); b.scale(0,b.row(0))
        new,p=restrict_rows(old,b.proof(),frozenset())
        self.assertEqual(R.check(new,p).budget,0)
        self.assertFalse(used_rows(new,p))

    def test_constant_closure_can_remove_used_rows(self):
        x=R.src('x'); ctx=R.context(('x',),(R.Row(x,R.num(1)),R.Row(R.scale(-1,x),R.num(-1))),{'x':1})
        b=R.Builder(ctx,'h'); b.add(b.row(0),b.row(1))
        new,p=restrict_rows(ctx,b.proof(),frozenset())
        self.assertEqual(R.check(new,p).budget,0)
        self.assertFalse(used_rows(new,p))

    def test_compiled_current_choice_is_not_the_future_family(self):
        old,p=alternative_example(); cp=compile_primitives(old,p)
        self.assertEqual(used_rows(old,cp),frozenset({('h',0)}))
        with self.assertRaises(UnavailableProof): restrict_rows(old,cp,frozenset({('h',1)}))
        new,q=restrict_rows(old,p,frozenset({('h',1)}))
        self.assertEqual(R.check(new,q).budget,0)

    def test_frontier_matches_every_small_withdrawal(self):
        old,p=alternative_example(); labels=support_frontier(old,p)
        for bits in product((0,1),repeat=2):
            alive=frozenset(('h',i) for i,x in enumerate(bits) if x)
            expected=best_label(labels,alive)
            try: new,q=restrict_rows(old,p,alive); actual=R.check(new,q).budget
            except UnavailableProof: actual=None
            self.assertEqual(actual,expected)

    def test_mandatory_comparison_needs_both_sources(self):
        x,y=R.src('x'),R.src('y')
        ctx=R.context(('x','y'),(R.Row(x,R.num(1)),R.Row(y,R.num(2))),{'x':0,'y':0})
        b=R.Builder(ctx,'h'); b.max_common(b.row(0),b.row(1)); p=b.proof()
        self.assertEqual(support_frontier(ctx,p),(Label(frozenset({('h',0),('h',1)}),F(2)),))
        with self.assertRaises(UnavailableProof): restrict_rows(ctx,p,frozenset({('h',0)}))

    def test_arithmetic_multiplicity_is_not_support_multiplicity(self):
        ctx,_=alternative_example(); b=R.Builder(ctx,'h'); p=b.row(0); b.add(p,p)
        self.assertEqual(support_frontier(ctx,b.proof()),(Label(frozenset({('h',0)}),F(-2)),))

    def test_support_cardinality_is_not_dominance(self):
        a=Label(frozenset({('h',0)}),F(0)); b=Label(frozenset({('h',1)}),F(1))
        self.assertEqual(len(irredundant([a,b])),2)

    def test_frontier_pruning_preserves_all_alive_queries(self):
        labels=[Label(frozenset({('h',0)}),F(1)),Label(frozenset({('h',0),('h',1)}),F(2)),
                Label(frozenset({('h',1)}),F(3)),Label(frozenset({('h',0)}),F(1))]
        compact=irredundant(labels)
        self.assertEqual(len(compact),2)
        self.assertEqual(compact,irredundant(reversed(labels)))
        for a,b in product((0,1),repeat=2):
            alive=frozenset(k for k,flag in [(('h',0),a),(('h',1),b)] if flag)
            self.assertEqual(best_label(tuple(labels),alive),best_label(compact,alive))

    def test_exponential_frontier_has_compact_origin(self):
        for n in range(1,7):
            xs=[R.src(f'x{i}') for i in range(n)]
            rows=tuple(R.Row(x,R.num(0)) for x in xs for _ in range(2))
            ctx=R.context(tuple(f'x{i}' for i in range(n)),rows,{f'x{i}':0 for i in range(n)})
            b=R.Builder(ctx,'h'); roots=[b.meet(b.row(2*i),b.row(2*i+1)) for i in range(n)]
            root=roots[0]
            for other in roots[1:]: root=b.add(root,other)
            p=b.proof(root)
            self.assertEqual(len(support_frontier(ctx,p)),2**n)
            self.assertLessEqual(len(p.steps),4*n)

    def test_explicit_frontier_limit_never_silently_truncates(self):
        ctx,p=alternative_example()
        with self.assertRaises(FrontierLimit): support_frontier(ctx,p,limit=1)
        with self.assertRaises(R.ProofError): support_frontier(ctx,p,limit=True)

    def test_all_S1_examples_elaborate_to_primitive_basis(self):
        for name,(ctx,p) in R.examples().items():
            out=compile_primitives(ctx,p)
            self.assertEqual(check_primitives(ctx,out).budget,R.check(ctx,p).budget,name)
            self.assertEqual((out.steps[out.root].new,out.steps[out.root].old),(p.steps[p.root].new,p.steps[p.root].old),name)

    def test_basis_filter_rejects_unexpanded_rule(self):
        ctx,p=R.consumer_example()
        with self.assertRaises(R.ProofError): check_primitives(ctx,p)

    def test_slack_macro_preserves_exact_budget(self):
        ctx,_=alternative_example(); b=R.Builder(ctx,'h'); b.slack(2,b.row(0))
        p=compile_primitives(ctx,b.proof())
        self.assertEqual(check_primitives(ctx,p).budget,1)
        self.assertNotIn('slack',{s.rule for s in p.steps})

    def test_minimum_congruence_and_negation_expand(self):
        ctx,_=alternative_example(); b=R.Builder(ctx,'h')
        a=b.negate(b.row(0)); z=b.constant(R.num(0),R.num(0)); b.congruence('min',a,z)
        p=compile_primitives(ctx,b.proof())
        self.assertEqual(check_primitives(ctx,p).budget,0)

    def test_symbolic_allowance_cancels_unbounded_shared_source(self):
        ctx,p=symbolic_repair_example()
        self.assertEqual(R.check(ctx,p).budget,F(-1,2))
        for u in (F(-10**30),F(0),F(10**30)):
            point={'u':u,'d1':u-F(3,4),'d2':F(1,4)-u}
            self.assertTrue(R.reference_holds(ctx,p,point,'h'))
        self.assertEqual(check_primitives(ctx,compile_primitives(ctx,p)).budget,F(-1,2))

    def test_bounded_gate_exact_at_boolean_flags(self):
        for a in (0,1):
            for b in (F(-2),F(-1),F(0),F(1),F(10**20)):
                self.assertEqual(gated_bound(a,b,F(-2)),min(F(0),b) if a else 0)

    def test_gate_rejects_fractional_confidence_and_missing_domain(self):
        for a in (F(1,2),True,-1,2):
            with self.assertRaises(R.ProofError): gated_bound(a,F(-1),F(-1))
        with self.assertRaises(R.ProofError): gated_bound(0,F(-2),F(-1))

    def test_unbounded_gate_has_no_fixed_cross_flag_lipschitz_constant(self):
        for k in (1,10,1000):
            b=F(-k-1)
            self.assertGreater(abs(min(F(0),b)-F(0)),k)

    def test_invalid_current_source_witness_rejected(self):
        old,p=alternative_example()
        bad=replace(old,cases=(replace(old.cases[0],witness=(('x',F(100)),)),))
        with self.assertRaises(R.SemanticError): transport(old,bad,p,{}, {'h':'h'})

    def test_replacement_row_indices_are_exact_integers(self):
        old,p=alternative_example()
        with self.assertRaises(R.ProofError): transport(old,old,p,{('h','h',True):p},{'h':'h'})

    def test_every_emitted_node_holds_at_current_witness(self):
        _,new,p,_,_=reflective_transport_example()
        for s in p.steps:
            for case in new.cases:
                if s.case in (None,case.name):
                    point=dict(case.witness)
                    self.assertLessEqual(R.evaluate(s.new,new.signature,point)-R.evaluate(s.old,new.signature,point),s.budget)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path)
    args=parser.parse_args()
    result=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(F06TransportTests))
    if not result.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),sort_keys=True,indent=2)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
