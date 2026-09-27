"""F06 finite case macros. Every output is checked by the unchanged S1 checker.

Inputs are supplied proofs and feasibility/infeasibility witnesses, not an
optimizer, automatic case search, policy verifier, or empirical calibration.
Python 3.10+; standard library; all numerical coefficients are exact rationals.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
import unittest

from v2.checks import f06_inference_rules as R
from v2.checks import f06_source_transport as T
from v2.checks import f06_residual_discharge as S


class ExpansionLimit(R.ProofError):
    """Explicit size refusal, never a truncated successful certificate."""


@dataclass(frozen=True)
class Limits:
    nodes: int = 20000
    term_occurrences: int = 1500000

    def validate(self):
        for n in (self.nodes, self.term_occurrences):
            if isinstance(n, bool) or not isinstance(n, int) or n < 1:
                raise R.ProofError('Positive integer expansion limits required.')


def bounded(proof: R.Proof, limits: Limits) -> None:
    limits.validate()
    if len(proof.steps) > limits.nodes:
        raise ExpansionLimit('Instruction expansion exceeds the declared limit.')
    todo = [x for s in proof.steps for x in (s.new, s.old)]
    count = 0
    while todo:
        t = todo.pop(); count += 1
        if count > limits.term_occurrences:
            raise ExpansionLimit('Term-occurrence expansion exceeds the declared limit.')
        todo.extend(t.args)


def single(ctx: R.Context) -> str:
    ctx.validate()
    if len(ctx.cases) != 1:
        raise R.ProofError('This macro expects one declared nonempty source case.')
    return ctx.cases[0].name


def finish(b: R.Builder, root: int, limits: Limits = Limits()) -> R.Proof:
    p = b.proof(root); bounded(p, limits)
    p = T.prune(b.ctx, p); bounded(p, limits)
    R.check(b.ctx, p)
    return p


def identity(b: R.Builder, t: R.Term) -> int:
    return b.constant(t, t)


def rho(t: R.Term, ctx: R.Context) -> R.Term:
    return R.maximum(t, R.num(0, R.infer(t, ctx.signature)))


def internal(b: R.Builder, i: int) -> int:
    """Turn t <=[q] s into t <=[0] s+q using a real rule step."""
    n = b.steps[i]; unit = R.infer(n.new, b.ctx.signature)
    j = b.constant(R.num(-n.budget, unit), R.num(0, unit))
    return b.rewrite(b.add(i, j), n.new, R.add(n.old, R.num(n.budget, unit)))


def external(b: R.Builder, i: int, constant: F,
             new: R.Term, old: R.Term) -> int:
    """An exact difference rewrite after adding the displayed constant."""
    unit = R.infer(new, b.ctx.signature)
    j = b.constant(R.num(constant, unit), R.num(0, unit))
    return b.rewrite(b.add(i, j), new, old)


def add_identity(b: R.Builder, i: int, t: R.Term,
                 new: R.Term | None = None, old: R.Term | None = None) -> int:
    j = b.add(i, identity(b, t))
    return j if new is None else b.rewrite(j, new, old)


def rehome(old: R.Context, new: R.Context, proof: R.Proof) -> R.Proof:
    """Same exact rows/signature/observation; witnesses/revision may differ."""
    a, c = single(old), single(new)
    if (old.signature != new.signature or old.observation != new.observation
            or a != c or old.cases[0].rows != new.cases[0].rows):
        raise R.ProofError('Rehoming is not a source weakening or source substitution.')
    R.check(old, proof)
    p = R.Proof(tuple(replace(s, context_id=R.fingerprint(new)) for s in proof.steps), proof.root)
    R.check(new, p)
    return p


@dataclass(frozen=True)
class LiveBranch:
    context: R.Context
    proof: R.Proof


@dataclass(frozen=True)
class EmptyBranch:
    multipliers: tuple[F, ...]
    guard_weight: F


def branch_context(parent: R.Context, cut: R.Term, positive: bool, witness: dict[str, F]) -> R.Context:
    """Append cut<=0 (False) or -cut<=0 (True), with a checked rational point."""
    name = single(parent)
    if not isinstance(positive, bool):
        raise R.ProofError('Branch polarity must be Boolean.')
    R.affine(cut, parent.signature)
    u = R.infer(cut, parent.signature)
    g = R.scale(-1, cut) if positive else cut
    h = R.Case(name, parent.cases[0].rows + (R.Row(g, R.num(0, u)),),
               tuple((k, R.rat(v)) for k, v in witness.items()))
    out = replace(parent, revision=parent.revision+('/cut-positive' if positive else '/cut-negative'), cases=(h,))
    out.validate()
    return out


def validate_live(parent: R.Context, cut: R.Term, positive: bool,
                  live: LiveBranch, limits: Limits) -> R.Step:
    if not isinstance(live, LiveBranch):
        raise R.ProofError('Expected a live branch proof.')
    name = single(parent); single(live.context)
    u = R.infer(cut, parent.signature)
    guard = R.scale(-1, cut) if positive else cut
    if (live.context.signature != parent.signature or live.context.observation != parent.observation
            or live.context.cases[0].name != name
            or live.context.cases[0].rows != parent.cases[0].rows + (R.Row(guard, R.num(0, u)),)):
        raise R.ProofError('Branch source is not the exact parent plus the declared sign guard.')
    bounded(live.proof, limits)
    root = R.check(live.context, live.proof)
    if R.infer(root.new, parent.signature) != u:
        raise R.ProofError('Convert the guard to the conclusion unit before splitting.')
    return root


@dataclass(frozen=True)
class Envelope:
    baseline: F
    gain: F
    error: R.Term
    upper: int
    nonnegative: int


def budget_envelope(b: R.Builder, allowance: R.Term, hinge: R.Term) -> Envelope:
    """Emit allowance <=[0] baseline+error and 0 <=[0] error.

    Only the symbolic budget grammar produced by S2 discharge is accepted.
    Nonconstant negative scales, free source terms and other operators fail.
    """
    sig = b.ctx.signature
    hinge_form = R._form(hinge, sig)
    cache: dict[R.Term, Envelope] = {}

    def build(t: R.Term) -> Envelope:
        if t in cache:
            return cache[t]
        unit = R.infer(t, sig); z = R.num(0, unit)
        form = R._form(t, sig)
        if not form[0]:
            c = form[1]
            ans = Envelope(c, F(0), z, b.constant(t, R.num(c, unit)), identity(b, z))
        elif form == hinge_form and unit == R.infer(hinge, sig):
            # Hinge identity is syntactic/exact, not a sampled equality.
            raw, zero = hinge.args if hinge.op == 'max' else (R.sub(hinge.args[1], hinge.args[0]), z)
            nz = b.lattice('max_right', raw, zero)
            nz = b.rewrite(nz, z, t)
            ans = Envelope(F(0), F(1), t, identity(b, t), nz)
        elif t.op in ('scale', 'convert'):
            child = build(t.args[0])
            if t.op == 'scale':
                k = R.rat(t.value)
                if k < 0:
                    raise R.ProofError('Budget allowance must be monotone in the guard loss.')
                error = R.scale(k, child.error)
                upper, nz = b.scale(k, child.upper), b.scale(k, child.nonnegative)
            else:
                k = R.rat(sig.conversion(t.name).factor)
                error = R.convert(t.name, child.error)
                upper, nz = b.conversion(t.name, child.upper), b.conversion(t.name, child.nonnegative)
            baseline = k * child.baseline
            upper = b.rewrite(upper, t, R.add(R.num(baseline, unit), error))
            nz = b.rewrite(nz, z, error)
            ans = Envelope(baseline, k*child.gain, error, upper, nz)
        elif t.op == 'add':
            left, right = map(build, t.args)
            error = R.add(left.error, right.error)
            baseline = left.baseline + right.baseline
            upper = b.rewrite(b.add(left.upper, right.upper), t, R.add(R.num(baseline, unit), error))
            nz = b.rewrite(b.add(left.nonnegative, right.nonnegative), z, error)
            ans = Envelope(baseline, left.gain+right.gain, error, upper, nz)
        elif t.op in ('min', 'max'):
            left, right = map(build, t.args)
            chosen = left if left.gain >= right.gain else right
            K, error, nz = chosen.gain, chosen.error, chosen.nonnegative
            def enlarge(child: Envelope) -> int:
                if K == 0:
                    edge = b.constant(child.error, error)
                else:
                    edge = b.scale(F(1)-child.gain/K, nz)
                    edge = b.rewrite(edge, child.error, error)
                edge = add_identity(b, edge, R.num(child.baseline, unit))
                return b.trans(child.upper, edge)
            il, ir = enlarge(left), enlarge(right)
            baseline = min(left.baseline, right.baseline) if t.op == 'min' else max(left.baseline, right.baseline)
            target = R.add(R.num(baseline, unit), error)
            if t.op == 'min':
                ix, kind = (il, 'min_left') if left.baseline <= right.baseline else (ir, 'min_right')
                upper = b.trans(b.lattice(kind, *t.args), ix)
                upper = b.rewrite(upper, t, target)
            else:
                raised = []
                for child, ix in ((left, il), (right, ir)):
                    edge = b.constant(R.num(child.baseline, unit), R.num(baseline, unit))
                    edge = add_identity(b, edge, error)
                    raised.append(b.trans(ix, edge))
                # The selected maximal baseline has budget zero, the other <=0.
                upper = b.rewrite(b.max_common(*raised), t, target)
            ans = Envelope(baseline, K, error, upper, nz)
        else:
            raise R.ProofError('Allowance contains a term outside the certified budget grammar.')
        if b.steps[ans.upper].budget != 0 or b.steps[ans.nonnegative].budget != 0:
            raise R.ProofError('Envelope construction lost its zero-budget invariant.')
        if R._form(ans.error, sig) != R._form(R.scale(ans.gain, hinge), sig):
            raise R.ProofError('Typed error expression does not match the certified gain.')
        cache[t] = ans
        return ans
    return build(allowance)


@dataclass(frozen=True)
class GuardAllowance:
    proof: R.Proof  # new <=[baseline] old + gain*ReLU(guard)
    baseline: F
    gain: F
    guard: R.Term
    new: R.Term
    old: R.Term


def discharge_branch(parent: R.Context, cut: R.Term, positive: bool,
                     branch: LiveBranch, limits: Limits = Limits()) -> GuardAllowance:
    root = validate_live(parent, cut, positive, branch, limits)
    name = single(parent)
    guard = R.scale(-1, cut) if positive else cut
    soft = S.soften_rows(branch.context, branch.proof, name, (len(parent.cases[0].rows),))
    p = rehome(soft.context, parent, soft.proof)
    b = R.Builder(parent, name)
    i = T._copy_into(b, p)
    h = rho(guard, parent)
    env = budget_envelope(b, soft.allowance, h)
    if env.baseline != soft.old_local_budget:
        raise R.ProofError('Budget baseline differs from the original local proof.')
    edge = add_identity(b, env.upper, root.old)
    j = b.trans(i, edge)
    target = R.add(root.old, R.scale(env.gain, h))
    j = external(b, j, env.baseline, root.new, target)
    return GuardAllowance(finish(b, j, limits), env.baseline, env.gain, guard, root.new, root.old)


def exclusion_proof(parent: R.Context, guard: R.Term, ray: EmptyBranch,
                    limits: Limits = Limits()) -> R.Proof:
    """An empty guard<=0 ray derives -guard<=[q]0 with q<0 in the parent."""
    name = single(parent); unit = R.infer(guard, parent.signature)
    _, offset = R.affine(guard, parent.signature)
    if not isinstance(ray, EmptyBranch) or not isinstance(ray.multipliers, tuple):
        raise R.ProofError('A finite rational infeasibility ray is required.')
    weights = tuple(R.rat(x) for x in ray.multipliers)
    k = R.rat(ray.guard_weight)
    if len(weights) != len(parent.cases[0].rows) or any(x < 0 for x in weights) or k <= 0:
        raise R.ProofError('Ray has invalid weights, dimensions or guard coefficient.')
    b = R.Builder(parent, name); zero = R.num(0, unit)
    total = b.constant(zero, zero)
    for index, weight in enumerate(weights):
        if weight:
            if R.normalized_row(parent, name, index)[2] != unit:
                raise R.ProofError('Nonzero ray weights must use compatible row units.')
            total = b.add(total, b.scale(weight, b.row(index)))
    coeff_guard = R.sub(guard, R.num(offset, unit))
    if not R.same_difference(b.steps[total].new, b.steps[total].old,
                             R.scale(-k, coeff_guard), zero, parent.signature):
        raise R.ProofError('Ray coefficients do not eliminate the source coordinates.')
    total = b.scale(F(1)/k, total)
    total = b.add(total, b.constant(R.num(-offset, unit), zero))
    total = b.rewrite(total, R.scale(-1, guard), zero)
    if b.steps[total].budget >= 0:
        raise R.ProofError('A strict negative infeasibility margin is required.')
    return finish(b, total, limits)


@dataclass(frozen=True)
class CaseResult:
    proof: R.Proof
    method: str
    branch_budgets: tuple[F, ...]
    gains: tuple[F, ...]


def compile_sign_split(parent: R.Context, cut: R.Term,
                       negative: LiveBranch | EmptyBranch,
                       positive: LiveBranch | EmptyBranch,
                       limits: Limits = Limits()) -> CaseResult:
    """Compile a supplied affine sign split into ordinary S1 local instructions."""
    name = single(parent); R.affine(cut, parent.signature); limits.validate()
    if not isinstance(negative, (LiveBranch, EmptyBranch)) or not isinstance(positive, (LiveBranch, EmptyBranch)):
        raise R.ProofError('Each branch needs either a live proof or a strict ray.')
    if isinstance(negative, EmptyBranch) and isinstance(positive, EmptyBranch):
        raise R.ProofError('A nonempty parent cannot be disposed by two empty children.')
    if isinstance(negative, EmptyBranch) or isinstance(positive, EmptyBranch):
        empty_positive = isinstance(positive, EmptyBranch)
        ray = positive if empty_positive else negative
        live = negative if empty_positive else positive
        live_positive = not empty_positive
        original = validate_live(parent, cut, live_positive, live, limits)
        guard = R.scale(-1, cut) if empty_positive else cut
        opposite = exclusion_proof(parent, guard, ray, limits)
        # Graft all actually used source rows; no infeasible live context exists.
        replacements = {}
        for _, index in T.used_rows(live.context, live.proof):
            if index < len(parent.cases[0].rows):
                q = R.Builder(parent, name); replacement = q.proof(q.row(index))
            else:
                q = R.Builder(parent, name)
                i = T._copy_into(q, opposite)
                a, _, _, _ = R.normalized_row(live.context, name, index)
                j = q.constant(R.sub(a, q.steps[i].new), q.steps[i].old)
                # Add the exact offset needed for the normalized row expression.
                replacement = finish(q, q.rewrite(q.add(i, j), a, R.num(0, R.infer(a, parent.signature))), limits)
            replacements[(name, name, index)] = replacement
        p = T.transport(live.context, parent, live.proof, replacements, {name:name})
        p = T.localize(parent, p, name)
        bounded(p, limits)
        return CaseResult(p, 'strict-ray-exclusion', (original.budget,), ())
    a = discharge_branch(parent, cut, False, negative, limits)
    c = discharge_branch(parent, cut, True, positive, limits)
    if (a.new, a.old) != (c.new, c.old):
        raise R.ProofError('Case proofs must retain the literal same query/policy pair.')
    b = R.Builder(parent, name)
    i, j = T._copy_into(b, a.proof), T._copy_into(b, c.proof)
    delta = R.sub(a.new, a.old)
    i = b.rewrite(i, delta, R.scale(a.gain, rho(cut, parent)))
    j = b.rewrite(j, delta, R.scale(c.gain, rho(R.scale(-1,cut), parent)))
    both = b.min_common(i, j)
    law = T._copy_into(b, S.disjoint_hinges(parent, name, cut, a.gain, c.gain))
    root = b.rewrite(b.trans(both, law), a.new, a.old)
    return CaseResult(finish(b, root, limits), 'derived-sign', (a.baseline,c.baseline), (a.gain,c.gain))


def hinge_shift(b: R.Builder, raw: R.Term, shift: F) -> int:
    """ReLU(raw) <=[0] shift + ReLU(raw-shift), for a literal shift>=0."""
    shift = R.rat(shift)
    if shift < 0:
        raise R.ProofError('Hinge shift must be nonnegative.')
    unit = R.infer(raw,b.ctx.signature); z=R.num(0,unit); k=R.num(shift,unit)
    v = R.sub(raw,k); h = rho(v,b.ctx); target=R.add(k,h)
    i = b.rewrite(b.lattice('max_left',v,z),raw,target)
    j = b.add(b.constant(z,k),b.lattice('max_right',v,z))
    j = b.rewrite(j,z,target)
    return b.max_common(i,j)


def sharp_hinge_bound(a, c, A, B, alpha, beta) -> F:
    a,c,A,B,alpha,beta=map(R.rat,(a,c,A,B,alpha,beta))
    if alpha<0 or beta<0: raise R.ProofError('Nonnegative hinge weights required.')
    if alpha==0 and beta==0: return min(A,B)
    if alpha==0: return A
    if beta==0: return B
    return max(A,B,(beta*A+alpha*B+alpha*beta*(c-a))/(alpha+beta))


def offset_hinge_certificate(ctx: R.Context, raw: R.Term, a, c, A, B, alpha, beta,
                             limits: Limits=Limits()) -> R.Proof:
    """Exact global supremum certificate for two weighted, shifted allowances."""
    name=single(ctx); unit=R.infer(raw,ctx.signature); z=R.num(0,unit)
    a,c,A,B,alpha,beta=map(R.rat,(a,c,A,B,alpha,beta))
    M=sharp_hinge_bound(a,c,A,B,alpha,beta)
    g=R.sub(raw,R.num(a,unit)); h=R.sub(R.num(c,unit),raw)
    left=R.add(R.num(A,unit),R.scale(alpha,rho(g,ctx)))
    right=R.add(R.num(B,unit),R.scale(beta,rho(h,ctx)))
    target=R.minimum(left,right); b=R.Builder(ctx,name)
    if not alpha or not beta:
        choose_left=(alpha==0 and (beta!=0 or A<=B))
        chosen=left if choose_left else right
        i=b.lattice('min_left' if choose_left else 'min_right',left,right)
        j=b.constant(chosen,z)
        return finish(b,b.trans(i,j),limits)
    k=(M-A)/alpha; l=(M-B)/beta
    ap=a+k; cp=c-l; v=R.sub(raw,R.num(ap,unit))
    # The left allowance is <= M+alpha*rho(v).
    il=b.scale(alpha,hinge_shift(b,g,k))
    il=add_identity(b,il,R.num(A,unit))
    il=b.rewrite(il,left,R.add(R.num(M,unit),R.scale(alpha,rho(v,ctx))))
    # Shift the right hinge, then use cp<=ap (equivalent to M>=Cstar).
    ir=b.scale(beta,hinge_shift(b,h,l)); ir=add_identity(b,ir,R.num(B,unit))
    hr=R.sub(R.num(cp,unit),raw); hr2=R.scale(-1,v)
    order=b.constant(hr,hr2)
    order=b.congruence('max',order,identity(b,z))
    order=b.scale(beta,order); order=add_identity(b,order,R.num(M,unit))
    ir=b.trans(ir,order)
    ir=b.rewrite(ir,right,R.add(R.num(M,unit),R.scale(beta,rho(hr2,ctx))))
    il=b.trans(b.lattice('min_left',left,right),il)
    ir=b.trans(b.lattice('min_right',left,right),ir)
    il=b.rewrite(il,R.sub(target,R.num(M,unit)),R.scale(alpha,rho(v,ctx)))
    ir=b.rewrite(ir,R.sub(target,R.num(M,unit)),R.scale(beta,rho(hr2,ctx)))
    out=b.min_common(il,ir)
    law=T._copy_into(b,S.disjoint_hinges(ctx,name,v,alpha,beta))
    out=b.trans(out,law)
    out=external(b,out,M,target,z)
    return finish(b,out,limits)


def positive_homogeneity(b: R.Builder, raw: R.Term, k: F) -> int:
    """Emit k*ReLU(raw) <=[0] ReLU(k*raw). The reverse is analogous."""
    k=R.rat(k); unit=R.infer(raw,b.ctx.signature); z=R.num(0,unit)
    if k<0: raise R.ProofError('Positive-part homogeneity needs k>=0.')
    target=rho(R.scale(k,raw),b.ctx)
    if not k: return b.constant(R.scale(k,rho(raw,b.ctx)),target)
    i=b.scale(1/k,b.lattice('max_left',R.scale(k,raw),z))
    i=b.rewrite(i,raw,R.scale(1/k,target))
    j=b.scale(1/k,b.lattice('max_right',R.scale(k,raw),z))
    j=b.rewrite(j,z,R.scale(1/k,target))
    out=b.scale(k,b.max_common(i,j))
    return b.rewrite(out,R.scale(k,rho(raw,b.ctx)),target)


@lru_cache(maxsize=32)
def _positive_min_lemma(ctx: R.Context, unit: str, limits: Limits) -> tuple[R.Context,R.Proof]:
    sig=replace(ctx.signature,sources=(('__lemma_a',unit),('__lemma_b',unit)))
    base=R.Context(sig,ctx.observation,'positive-min-generic',(R.Case('h',(),(('__lemma_a',F(0)),('__lemma_b',F(0)))),))
    a,c=R.src('__lemma_a'),R.src('__lemma_b'); z=R.num(0,unit)
    left=R.minimum(rho(a,base),rho(c,base)); right=rho(R.minimum(a,c),base)
    branches=[]
    for positive,w in ((False,{'__lemma_a':F(0),'__lemma_b':F(1)}),(True,{'__lemma_a':F(1),'__lemma_b':F(0)})):
        bc=branch_context(base,R.sub(a,c),positive,w); b=R.Builder(bc,'h')
        if not positive:
            order=b.rewrite(b.row(0),a,c)
            to_min=b.min_common(identity(b,a),order)
            to_rho=b.congruence('max',to_min,identity(b,z))
            out=b.trans(b.lattice('min_left',rho(a,bc),rho(c,bc)),to_rho)
        else:
            order=b.rewrite(b.row(0),c,a)
            to_min=b.min_common(order,identity(b,c))
            to_rho=b.congruence('max',to_min,identity(b,z))
            out=b.trans(b.lattice('min_right',rho(a,bc),rho(c,bc)),to_rho)
        out=b.rewrite(out,left,right)
        branches.append(LiveBranch(bc,finish(b,out,limits)))
    return base,compile_sign_split(base,R.sub(a,c),*branches,limits).proof


def positive_min(b: R.Builder, a: R.Term, c: R.Term,
                 limits: Limits=Limits()) -> int:
    """Instantiate a source-free, sign-compiled finite lattice lemma."""
    unit=R.infer(a,b.ctx.signature)
    if R.infer(c,b.ctx.signature)!=unit: raise R.ProofError('Mixed positive-min units.')
    old,p=_positive_min_lemma(b.ctx,unit,limits)
    mapped=T.transport(old,b.ctx,p,{}, {single(b.ctx):'h'}, {'__lemma_a':a,'__lemma_b':c})
    mapped=T.localize(b.ctx,mapped,single(b.ctx))
    return T._copy_into(b,mapped)


@dataclass(frozen=True)
class CoverInput:
    guard: R.Term
    baseline: F
    gain: F
    weight: F
    proof: R.Proof  # literal new <=[baseline] old+gain*ReLU(guard)


def weighted_cover(parent: R.Context, new: R.Term, old: R.Term,
                   entries: tuple[CoverInput,...], cover: R.Proof,
                   limits: Limits=Limits()) -> R.Proof:
    """Compile a supplied weighted raw-guard bound and common-query allowances."""
    name=single(parent); unit=R.infer(new,parent.signature); z=R.num(0,unit)
    if R.infer(old,parent.signature)!=unit or not isinstance(entries,tuple) or not entries:
        raise R.ProofError('A nonempty tuple of compatible allowances is required.')
    b=R.Builder(parent,name); delta=R.sub(new,old)
    normalized=[]; total=z; H=F(0); baseline_sum=F(0)
    for e in entries:
        if not isinstance(e,CoverInput): raise R.ProofError('Malformed cover argument.')
        A,k,w=map(R.rat,(e.baseline,e.gain,e.weight))
        if k<=0 or w<=0: raise R.ProofError('This cover macro requires positive gains and weights.')
        if R.infer(e.guard,parent.signature)!=unit: raise R.ProofError('Mixed cover units.')
        bounded(e.proof,limits); root=R.check(parent,e.proof)
        expected=R.add(old,R.scale(k,rho(e.guard,parent)))
        if (root.new,root.old)!=(new,expected) or root.budget!=A or root.case!=name:
            raise R.ProofError('Cover argument is not the declared common-query allowance.')
        normalized.append((e,A,k,w)); total=R.add(total,R.scale(w,e.guard))
        H+=w/k; baseline_sum+=w*A/k
    bounded(cover,limits); cover=T.localize(parent,cover,name); q=R.check(parent,cover)
    if not R.same_difference(q.new,q.old,total,z,parent.signature):
        raise R.ProofError('The source proof does not bound the declared weighted guard sum.')
    eta=q.budget; M=max(max(A for _,A,_,_ in normalized),(eta+baseline_sum)/H)
    shifted=[]; comparisons=[]
    for e,A,k,w in normalized:
        shift=(M-A)/k; h=R.sub(e.guard,R.num(shift,unit)); v=R.scale(k,h)
        i=T._copy_into(b,e.proof)
        i=internal(b,i)
        edge=b.scale(k,hinge_shift(b,e.guard,shift))
        edge=add_identity(b,edge,R.add(old,R.num(A,unit)))
        i=b.trans(i,edge)
        i=b.rewrite(i,R.sub(delta,R.num(M,unit)),R.scale(k,rho(h,parent)))
        i=b.trans(i,positive_homogeneity(b,h,k))
        shifted.append((v,h,w/k,w)); comparisons.append(i)
    out=comparisons[0]; raw_min=shifted[0][0]
    for j,(v,h,ratio,w) in zip(comparisons[1:],shifted[1:]):
        out=b.min_common(out,j)
        lemma=positive_min(b,raw_min,v,limits)
        out=b.trans(out,lemma)
        raw_min=R.minimum(raw_min,v)
    # Construct projections from the left-associated minimum to each raw entry.
    def projections(items):
        if len(items)==1: return [identity(b,items[0])],items[0]
        prev,m=projections(items[:-1]); v=items[-1]
        left=b.lattice('min_left',m,v); right=b.lattice('min_right',m,v)
        return [b.trans(left,i) for i in prev]+[right],R.minimum(m,v)
    ps,_=projections([x[0] for x in shifted])
    average=None; shifted_sum=z
    for p,(v,h,ratio,w) in zip(ps,shifted):
        qpart=b.scale(ratio,p)
        average=qpart if average is None else b.add(average,qpart)
        shifted_sum=R.add(shifted_sum,R.scale(w,h))
    average=b.scale(1/H,average)
    average=b.rewrite(average,raw_min,R.scale(1/H,shifted_sum))
    sum_bound=T._copy_into(b,cover)
    shift_amount=sum(w*(M-A)/k for _,A,k,w in normalized)
    sum_bound=b.add(sum_bound,b.constant(R.num(-shift_amount,unit),z))
    sum_bound=b.rewrite(sum_bound,shifted_sum,z)
    sum_bound=b.scale(1/H,sum_bound)
    raw_bound=b.trans(average,sum_bound)
    clipped=b.congruence('max',raw_bound,identity(b,z))
    clipped=b.rewrite(clipped,rho(raw_min,parent),z)
    out=b.trans(out,clipped)
    out=external(b,out,M,new,old)
    return finish(b,out,limits)


def almost_exclusion(parent: R.Context, allowance: GuardAllowance,
                     guard_upper: R.Proof, limits: Limits=Limits()) -> R.Proof:
    """Preserve a graded guarantee when the discharged guard is only nearly true."""
    name=single(parent); b=R.Builder(parent,name); unit=R.infer(allowance.new,parent.signature); z=R.num(0,unit)
    R.check(parent,allowance.proof); q=R.check(parent,guard_upper)
    if not R.same_difference(q.new,q.old,allowance.guard,z,parent.signature):
        raise R.ProofError('Wrong discharged-guard bound.')
    i=T._copy_into(b,allowance.proof); j=T._copy_into(b,guard_upper)
    j=b.rewrite(j,allowance.guard,z)
    j=b.congruence('max',j,identity(b,z)); j=b.scale(allowance.gain,j)
    j=add_identity(b,j,allowance.old)
    return finish(b,b.trans(i,j),limits)



def pack_proof(proof: R.Proof) -> dict:
    """Lossless term-DAG serialization; avoids duplicating large subexpressions."""
    terms=[]; indices={}
    def term(t):
        if t in indices: return indices[t]
        args=[term(a) for a in t.args]
        index=len(terms)
        terms.append({'op':t.op,'args':args,'name':t.name,'unit':t.unit,
                      'value':None if t.value is None else str(t.value)})
        indices[t]=index
        return index
    def data(x):
        if isinstance(x,R.Term): return {'term':term(x)}
        if isinstance(x,F): return {'rational':str(x)}
        if isinstance(x,tuple): return {'tuple':[data(y) for y in x]}
        if x is None or isinstance(x,(str,int)): return x
        raise R.ProofError('Unsupported certificate data value.')
    steps=[]
    for node in proof.steps:
        steps.append({'rule':node.rule,'parents':list(node.parents),'case':node.case,
            'new':term(node.new),'old':term(node.old),'budget':str(node.budget),
            'context_id':node.context_id,'data':data(node.data)})
    return {'format':'F06-term-dag-v1','terms':terms,'steps':steps,'root':proof.root}


def unpack_proof(ctx: R.Context, payload: dict, limits: Limits=Limits()) -> R.Proof:
    """Decode backward-only term references, then run the original checker."""
    limits.validate()
    if not isinstance(payload,dict) or set(payload)!={'format','terms','steps','root'} or payload['format']!='F06-term-dag-v1':
        raise R.ProofError('Unknown or malformed proof transport format.')
    if not isinstance(payload['terms'],list) or not isinstance(payload['steps'],list):
        raise R.ProofError('Term and step tables must be lists.')
    if len(payload['terms'])>limits.term_occurrences or len(payload['steps'])>limits.nodes:
        raise ExpansionLimit('Transport tables exceed the declared limit.')
    terms=[]
    def ref(index):
        if isinstance(index,bool) or not isinstance(index,int) or not 0<=index<len(terms):
            raise R.ProofError('Term references must point backward to existing terms.')
        return terms[index]
    def rational(x):
        if not isinstance(x,str): raise R.ProofError('Exact rational strings required.')
        try: return F(x)
        except (ValueError,ZeroDivisionError) as e: raise R.ProofError('Invalid rational string.') from e
    for item in payload['terms']:
        if not isinstance(item,dict) or set(item)!={'op','args','name','unit','value'}:
            raise R.ProofError('Malformed term-table entry.')
        if not all(isinstance(item[k],str) for k in ('op','name','unit')) or not isinstance(item['args'],list):
            raise R.ProofError('Malformed term attributes.')
        terms.append(R.Term(item['op'],tuple(ref(i) for i in item['args']),item['name'],item['unit'],
                            None if item['value'] is None else rational(item['value'])))
    def data(x):
        if isinstance(x,dict):
            if set(x)=={'term'}: return ref(x['term'])
            if set(x)=={'rational'}: return rational(x['rational'])
            if set(x)=={'tuple'} and isinstance(x['tuple'],list): return tuple(data(y) for y in x['tuple'])
            raise R.ProofError('Malformed tagged proof data.')
        if x is None or isinstance(x,(str,int)): return x
        raise R.ProofError('Unsupported proof data.')
    steps=[]
    for item in payload['steps']:
        if not isinstance(item,dict) or set(item)!={'rule','parents','case','new','old','budget','context_id','data'}:
            raise R.ProofError('Malformed instruction entry.')
        if not isinstance(item['parents'],list) or not isinstance(item['rule'],str) or not isinstance(item['context_id'],str):
            raise R.ProofError('Malformed instruction fields.')
        steps.append(R.Step(item['rule'],tuple(item['parents']),item['case'],ref(item['new']),ref(item['old']),
                            rational(item['budget']),item['context_id'],data(item['data'])))
    proof=R.Proof(tuple(steps),payload['root']);bounded(proof,limits);R.check(ctx,proof)
    return proof


def calculator_example():
    u=R.src('u'); ctx=R.context(('u',),(),{'u':0},scope='BOUND-SELECT-v1')
    cut=R.sub(u,R.num(F(1,4)))
    left=R.add(R.num(F(-3,4)),u); right=R.sub(R.num(F(-1,4)),u)
    query=R.minimum(left,right); branches=[]
    for pos,w in ((False,{'u':F(0)}),(True,{'u':F(1,2)})):
        bc=branch_context(ctx,cut,pos,w); b=R.Builder(bc,'h')
        bound=b.row(0)
        const=F(-1,4) if pos else F(-3,4)
        bound=b.add(bound,b.constant(R.num(const),R.num(0)))
        bound=b.rewrite(bound,right if pos else left,R.num(0))
        out=b.trans(b.lattice('min_right' if pos else 'min_left',left,right),bound)
        branches.append(LiveBranch(bc,finish(b,out)))
    return ctx,compile_sign_split(ctx,cut,*branches),tuple(branches)


def absolute_case_example():
    ctx,_=R.absolute_example(); y,c,z=map(R.src,('y','c','z')); cut=R.sub(y,R.num(1))
    new=R.add(R.absolute(cut),R.add(c,z)); old=R.add(R.absolute(y),z); branches=[]
    for pos,w in ((False,{'y':F(3,4),'c':F(0),'z':F(0)}),(True,{'y':F(1),'c':F(0),'z':F(0)})):
        bc=branch_context(ctx,cut,pos,w); b=R.Builder(bc,'h'); guard=b.row(len(ctx.cases[0].rows))
        # Normalize twice the guard to the absolute-value comparison.
        if pos:
            g=b.scale(2,guard)
            g=b.add(g,b.constant(R.num(2),R.num(0)))
            g=b.rewrite(g,R.scale(-1,cut),cut)
            abs_bound=b.max_common(identity(b,cut),g)
            drift=b.add(b.row(1),b.constant(R.num(-1),R.num(0)))
            drift=b.rewrite(drift,R.add(cut,c),y)
        else:
            g=b.scale(2,guard)
            # guard y<=1: the normalized bound must be shifted by -2.
            g=b.add(g,b.constant(R.num(-2),R.num(0)))
            g=b.rewrite(g,cut,R.scale(-1,cut))
            abs_bound=b.max_common(g,identity(b,R.scale(-1,cut)))
            drift=b.add(b.scale(2,b.row(0)),b.row(1))
            drift=b.add(drift,b.constant(R.num(1),R.num(0)))
            drift=b.rewrite(drift,R.add(R.scale(-1,cut),c),y)
        abs_bound=add_identity(b,abs_bound,c)
        out=b.trans(abs_bound,drift)
        out=b.trans(out,b.lattice('max_left',y,R.scale(-1,y)))
        out=add_identity(b,out,z,new,old)
        branches.append(LiveBranch(bc,finish(b,out)))
    return ctx,compile_sign_split(ctx,cut,*branches),tuple(branches)


def empty_example(delta=F(1,2)):
    x=R.src('x'); ctx=R.context(('x',),(R.Row(R.scale(-1,x),R.num(-delta)),),{'x':max(delta,F(0))},scope='empty-sign')
    cut=x; bc=branch_context(ctx,cut,True,{'x':max(delta,F(0))})
    b=R.Builder(bc,'h'); z=R.num(0)
    i=b.rewrite(b.row(1),R.scale(-1,x),z)
    i=b.congruence('max',i,identity(b,z))
    i=b.rewrite(i,rho(R.scale(-1,x),bc),z)
    i=b.add(i,b.constant(R.num(F(-1,2)),z))
    live=LiveBranch(bc,finish(b,i))
    result=compile_sign_split(ctx,cut,EmptyBranch((F(1),),F(1)),live)
    return ctx,result,live


def triple_example(epsilon=F(0)):
    epsilon=R.rat(epsilon)
    n,o,x,y=map(R.src,('N','O','x','y')); d=R.sub(n,o)
    rows=(R.Row(R.sub(d,x),R.num(F(-1,2)+epsilon)),
          R.Row(R.sub(d,y),R.num(F(-1,2))),
          R.Row(R.add(d,R.add(x,y)),R.num(F(1,4))))
    C=F(-1,4)+epsilon/3
    witness={'N':max(C,F(0)),'O':max(-C,F(0)), 'x':F(1,4)-2*epsilon/3,'y':F(1,4)+epsilon/3}
    ctx=R.context(('N','O','x','y'),rows,witness,scope='three-contracts-v1',revision=f'epsilon-{epsilon}')
    guards=(x,y,R.sub(R.num(F(3,4)),R.add(x,y)))
    entries=[]
    # A sufficiently negative d makes all three parent rows feasible in each branch.
    for index,g in enumerate(guards):
        point={'N':F(0),'O':F(4)+abs(epsilon),'x':F(0),'y':F(0)}
        if index==2: point['x']=F(3,4)
        bc=branch_context(ctx,g,False,point); b=R.Builder(bc,'h')
        out=b.add(b.row(index),b.row(3)); out=b.rewrite(out,n,o)
        live=LiveBranch(bc,finish(b,out))
        allowance=discharge_branch(ctx,g,False,live)
        entries.append(CoverInput(g,allowance.baseline,allowance.gain,F(1),allowance.proof))
    b=R.Builder(ctx,'h'); total=R.add(R.add(guards[0],guards[1]),guards[2])
    cov=finish(b,b.constant(total,R.num(0)))
    p=weighted_cover(ctx,n,o,tuple(entries),cov)
    b=R.Builder(ctx,'h'); direct=b.scale(F(1,3),b.add(b.add(b.row(0),b.row(1)),b.row(2)))
    direct=b.rewrite(direct,n,o)
    return ctx,p,finish(b,direct),tuple(entries),cov


class F06DerivedCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calc=calculator_example()
        cls.abs=absolute_case_example()
        cls.empty=empty_example()
        cls.triple=triple_example()
        cls.relaxed=triple_example(F(1))

    def test_calculator_sign_split(self):
        ctx,out,_=self.calc
        self.assertEqual(R.check(ctx,out.proof).budget,F(-1,2))
        self.assertEqual(out.gains,(F(1),F(1)))
        self.assertFalse(T.used_rows(ctx,out.proof))
        self.assertFalse(any(s.rule=='all_cases' for s in out.proof.steps))

    def test_calculator_outside_branch_witnesses(self):
        ctx,out,_=self.calc
        for u in (F(-10**12),F(-2),F(0),F(1,4),F(2),F(10**12)):
            self.assertTrue(R.reference_holds(ctx,out.proof,{'u':u},'h'))

    def test_absolute_loss_composition(self):
        ctx,out,_=self.abs
        self.assertEqual(R.check(ctx,out.proof).budget,F(-1,4))
        self.assertEqual(out.branch_budgets,(F(-1,4),F(-3,4)))
        self.assertTrue(all(i<len(ctx.cases[0].rows) for _,i in T.used_rows(ctx,out.proof)))
        for y,c,z in product((F(3,4),F(1),F(2),F(1000)),(F(0),F(1,4)),(F(0),F(10**10))):
            self.assertTrue(R.reference_holds(ctx,out.proof,dict(y=y,c=c,z=z),'h'))

    def test_direct_and_case_absolute_bounds_agree(self):
        _,p=R.absolute_example();ctx,out,_=self.abs
        self.assertEqual(R.check(ctx,p).budget,R.check(ctx,out.proof).budget)

    def test_wrong_branch_polarity_rejected(self):
        ctx,_,branches=self.calc
        with self.assertRaises(R.ProofError):
            compile_sign_split(ctx,R.sub(R.src('u'),R.num(F(1,4))),branches[0],branches[0])

    def test_changed_query_pair_rejected(self):
        ctx,_,branches=self.calc; live=branches[1]
        b=R.Builder(live.context,'h'); root=T._copy_into(b,live.proof)
        n=b.steps[root]
        root=b.rewrite(root,R.add(n.new,R.num(1)),R.add(n.old,R.num(1)))
        changed=LiveBranch(live.context,finish(b,root))
        with self.assertRaises(R.ProofError):
            compile_sign_split(ctx,R.sub(R.src('u'),R.num(F(1,4))),branches[0],changed)

    def test_stale_context_and_changed_observation_rejected(self):
        ctx,_,branches=self.calc; cut=R.sub(R.src('u'),R.num(F(1,4)))
        for changed in (replace(branches[0].context,revision='stale'),replace(branches[0].context,observation='hidden-oracle')):
            with self.assertRaises(R.ProofError):
                compile_sign_split(ctx,cut,LiveBranch(changed,branches[0].proof),branches[1])

    def test_invalid_nonempty_witness_rejected(self):
        ctx,_,_=self.calc; cut=R.sub(R.src('u'),R.num(F(1,4)))
        with self.assertRaises(ValueError): branch_context(ctx,cut,False,{'u':F(1)})

    def test_nonaffine_cut_rejected(self):
        ctx,_,branches=self.calc
        with self.assertRaises(ValueError): compile_sign_split(ctx,rho(R.src('u'),ctx),*branches)

    def test_both_empty_children_rejected(self):
        ctx,_,_=self.calc
        with self.assertRaises(R.ProofError):
            compile_sign_split(ctx,R.src('u'),EmptyBranch((),F(1)),EmptyBranch((),F(1)))

    def test_empty_branch_ray_emits_parent_proof(self):
        ctx,result,_=self.empty
        self.assertEqual(result.method,'strict-ray-exclusion')
        self.assertLessEqual(R.check(ctx,result.proof).budget,F(-1,2))
        for x in (F(1,2),F(1),F(1000)):
            self.assertTrue(R.reference_holds(ctx,result.proof,{'x':x},'h'))

    def test_bad_empty_coefficients_and_weights_rejected(self):
        ctx,_,live=self.empty
        for ray in (EmptyBranch((F(2),),F(1)),EmptyBranch((F(-1),),F(1)),
                    EmptyBranch((F(1),),F(0)),EmptyBranch((),F(1)),EmptyBranch((F(1),),True)):
            with self.assertRaises(ValueError): compile_sign_split(ctx,R.src('x'),ray,live)

    def test_zero_margin_not_empty(self):
        x=R.src('x');ctx=R.context(('x',),(R.Row(R.scale(-1,x),R.num(0)),),{'x':0})
        with self.assertRaises(R.ProofError): exclusion_proof(ctx,x,EmptyBranch((F(1),),F(1)))

    def test_constant_positive_guard_ray(self):
        ctx=R.context(('x',),(),{'x':0}); cut=R.num(1)
        bc=branch_context(ctx,cut,True,{'x':0});b=R.Builder(bc,'h')
        live=LiveBranch(bc,finish(b,b.constant(R.num(-2),R.num(0))))
        result=compile_sign_split(ctx,cut,EmptyBranch((),F(1)),live)
        self.assertEqual(R.check(ctx,result.proof).budget,F(-2))

    def test_constant_zero_guard_two_live(self):
        ctx=R.context(('x',),(),{'x':0});cut=R.num(0);branches=[]
        for pos in (False,True):
            bc=branch_context(ctx,cut,pos,{'x':0});b=R.Builder(bc,'h')
            branches.append(LiveBranch(bc,finish(b,b.constant(R.num(-1),R.num(0)))))
        p=compile_sign_split(ctx,cut,*branches).proof
        self.assertEqual(R.check(ctx,p).budget,F(-1))

    def test_near_exclusion_keeps_graded_guarantee(self):
        x=R.src('x'); ctx=R.context(('x',),(R.Row(R.scale(-1,x),R.num(F(1,8))),),{'x':0})
        bc=branch_context(ctx,x,True,{'x':0});b=R.Builder(bc,'h');z=R.num(0)
        i=b.rewrite(b.row(1),R.scale(-1,x),z);i=b.congruence('max',i,identity(b,z))
        i=b.rewrite(i,rho(R.scale(-1,x),ctx),z)
        i=b.add(i,b.constant(R.num(F(-1,2)),z))
        allowance=discharge_branch(ctx,x,True,LiveBranch(bc,finish(b,i)))
        q=R.Builder(ctx,'h'); p=almost_exclusion(ctx,allowance,finish(q,q.row(0)))
        self.assertEqual(R.check(ctx,p).budget,F(-3,8))
        self.assertTrue(R.reference_holds(ctx,p,{'x':F(-1,8)},'h'))

    def test_hinge_gap_bound_negative_and_positive(self):
        ctx=R.context(('x',),(),{'x':0});x=R.src('x')
        for a,c,expected in ((F(-1,4),F(1,4),F(-1,4)),(F(-1),F(1),F(1,2))):
            p=offset_hinge_certificate(ctx,x,a,c,F(-1,2),F(-1,2),1,1)
            self.assertEqual(R.check(ctx,p).budget,expected)
            self.assertEqual(R.evaluate(p.steps[p.root].new,ctx.signature,{'x':F(0)}),expected)

    def test_offset_hinge_exact_witnesses(self):
        for a,c,A,B,k,l in product((F(-1),F(1)),(F(0),F(2)),(F(-2),F(1)),(F(-1),F(3)),(F(1),F(2)),(F(1),F(3))):
            M=sharp_hinge_bound(a,c,A,B,k,l)
            f=lambda u:min(A+k*max(u-a,0),B+l*max(c-u,0))
            left=min(a,c-max((A-B)/l,0));right=max(c,a+max((B-A)/k,0))
            candidates=[f(left),f(right)]
            star=(B-A+k*a+l*c)/(k+l)
            candidates.append(f(star))
            self.assertEqual(max(candidates),M)
            for u in (F(-10),a,c,star,F(10)):
                self.assertLessEqual(f(u),M)

    def test_offset_hinge_coefficients_and_negative_budgets(self):
        ctx=R.context(('x',),(),{'x':0})
        for args in ((-2,1,-4,-1,2,3),(2,-1,-2,-3,1,2),(0,0,-3,-1,0,2),(0,0,-3,-1,2,0),(0,0,-3,-1,0,0)):
            p=offset_hinge_certificate(ctx,R.src('x'),*args)
            self.assertEqual(R.check(ctx,p).budget,sharp_hinge_bound(*args))
            for x in (F(-100),F(0),F(1),F(100)):
                self.assertTrue(R.reference_holds(ctx,p,{'x':x},'h'))
        with self.assertRaises(R.ProofError): offset_hinge_certificate(ctx,R.src('x'),0,0,0,0,-1,1)

    def test_zero_gain_boundary_not_continuous(self):
        self.assertEqual(sharp_hinge_bound(0,0,0,1,0,1),0)
        self.assertEqual(sharp_hinge_bound(0,0,0,1,F(1,10**12),1),1)

    def test_symbolic_budget_min_max_envelope(self):
        ctx=R.context(('u',),(),{'u':0});h=rho(R.src('u'),ctx);b=R.Builder(ctx,'h')
        A=R.maximum(R.minimum(R.add(R.num(-2),R.scale(2,h)),R.num(1)),R.add(R.num(-1),h))
        e=budget_envelope(b,A,h)
        p=finish(b,e.upper)
        self.assertEqual(e.baseline,F(-1));self.assertEqual(e.gain,F(2))
        for u in (F(-10),F(0),F(1,3),F(2),F(10)):
            self.assertTrue(R.reference_holds(ctx,p,{'u':u},'h'))

    def test_budget_envelope_rejects_unrecognized_source_and_negative_scale(self):
        ctx=R.context(('u','v'),(),{'u':0,'v':0});h=rho(R.src('u'),ctx)
        for t in (R.src('v'),R.scale(-1,h)):
            with self.assertRaises(R.ProofError): budget_envelope(R.Builder(ctx,'h'),t,h)

    def test_budget_envelope_keeps_named_conversion(self):
        conv=(R.Conversion('twice','V','U',F(2)),R.Conversion('half','U','V',F(1,2)))
        ctx=R.context((('u','U'),),(),{'u':0},units=('U','V'),conversions=conv)
        h=rho(R.src('u'),ctx);a=R.convert('twice',R.add(R.num(1,'V'),R.convert('half',h)))
        b=R.Builder(ctx,'h');e=budget_envelope(b,a,h);p=finish(b,e.upper)
        self.assertEqual((e.baseline,e.gain),(F(2),F(1)))
        self.assertEqual(R.infer(e.error,ctx.signature),'U')
        self.assertTrue(R.reference_holds(ctx,p,{'u':F(3)},'h'))

    def test_positive_part_min_compiled_without_source_rows(self):
        ctx=R.context(('x','y'),(),{'x':0,'y':0});b=R.Builder(ctx,'h')
        i=positive_min(b,R.src('x'),R.src('y'));p=finish(b,i)
        self.assertFalse(T.used_rows(ctx,p))
        for x,y in product((F(-2),F(0),F(3)),repeat=2):
            self.assertTrue(R.reference_holds(ctx,p,{'x':x,'y':y},'h'))

    def test_positive_part_min_native_term_substitution(self):
        ctx=R.context(('x',),(),{'x':0});x=R.src('x');b=R.Builder(ctx,'h')
        a=R.add(rho(x,ctx),R.num(-1));c=R.scale(2,R.minimum(x,R.num(3)))
        p=finish(b,positive_min(b,a,c))
        self.assertEqual(R.check(ctx,p).budget,0)
        for v in (F(-100),F(0),F(1),F(10)):
            self.assertTrue(R.reference_holds(ctx,p,{'x':v},'h'))

    def test_triple_cover_emits_same_direct_bound(self):
        ctx,p,direct,_,_=self.triple
        self.assertEqual(R.check(ctx,p).budget,F(-1,4))
        self.assertEqual(R.check(ctx,p).budget,R.check(ctx,direct).budget)
        self.assertEqual({i for _,i in T.used_rows(ctx,p)},{0,1,2})
        self.assertTrue(R.reference_holds(ctx,p,dict(ctx.cases[0].witness),'h'))
        self.assertFalse(any(s.rule=='all_cases' for s in p.steps))

    def test_triple_uncovered_point_is_not_discarded(self):
        ctx,p,_,entries,_=self.triple; point=dict(ctx.cases[0].witness)
        self.assertTrue(all(R.evaluate(e.guard,ctx.signature,point)>0 for e in entries))
        self.assertEqual(R.evaluate(R.sub(p.steps[p.root].new,p.steps[p.root].old),ctx.signature,point),F(-1,4))

    def test_every_pair_of_signed_contracts_is_insufficient(self):
        ctx,_,_,_,_=self.triple
        for Tval in (F(1),F(1000)):
            pairs=((0,1,{'x':Tval+F(1,2),'y':Tval+F(1,2)}),
                   (1,2,{'x':-2*Tval-F(1,4),'y':Tval+F(1,2)}),
                   (0,2,{'x':Tval+F(1,2),'y':-2*Tval-F(1,4)}))
            for i,j,point in pairs:
                point.update(N=Tval,O=F(0))
                for k in (i,j):
                    row=ctx.cases[0].rows[k]
                    self.assertLessEqual(R.evaluate(row.lhs,ctx.signature,point),R.evaluate(row.rhs,ctx.signature,point))

    def test_relaxed_cover_does_not_claim_signed_precision(self):
        ctx,p,direct,_,_=self.relaxed
        self.assertEqual(R.check(ctx,p).budget,F(1,2))
        self.assertEqual(R.check(ctx,direct).budget,F(1,12))
        self.assertEqual(R.check(ctx,p).budget-R.check(ctx,direct).budget,F(5,12))

    def test_cover_source_proof_and_parameters_are_checked(self):
        ctx,_,_,entries,cov=self.triple
        for bad in (replace(entries[0],gain=F(0)),replace(entries[0],weight=F(-1)),replace(entries[0],baseline=F(0))):
            with self.assertRaises(R.ProofError):
                weighted_cover(ctx,R.src('N'),R.src('O'),(bad,)+entries[1:],cov)
        b=R.Builder(ctx,'h');wrong=finish(b,b.constant(R.num(0),R.num(0)))
        with self.assertRaises(R.ProofError): weighted_cover(ctx,R.src('N'),R.src('O'),entries,wrong)

    def test_weighted_aggregate_bound_sharp_witnesses(self):
        for As,ks,ws,eta in product(((F(-1),F(-2),F(1)),(F(0),F(0),F(0))),
                                   ((F(1),F(2),F(3)),(F(1),F(1),F(1))),
                                   ((F(1),F(2),F(1)),), (F(-3),F(0),F(10))):
            H=sum(w/k for w,k in zip(ws,ks));C=(eta+sum(w*A/k for A,k,w in zip(As,ks,ws)))/H
            M=max(max(As),C)
            if C>=max(As): gs=[(C-A)/k for A,k in zip(As,ks)]
            else:
                j=As.index(max(As));gs=[(M-A)/k for A,k in zip(As,ks)]
                gs[j]=(eta-sum(w*g for i,(w,g) in enumerate(zip(ws,gs)) if i!=j))/ws[j]
            self.assertEqual(sum(w*g for w,g in zip(ws,gs)),eta)
            self.assertEqual(min(A+k*max(g,0) for A,k,g in zip(As,ks,gs)),M)

    def test_safe_replay_can_be_weaker_than_recompilation(self):
        x=R.src('x');old=R.context(('x',),(R.Row(x,R.num(0)),R.Row(x,R.num(10))),{'x':0})
        new=replace(old,revision='reversed',cases=(replace(old.cases[0],rows=(R.Row(x,R.num(10)),R.Row(x,R.num(0)))),))
        b=R.Builder(old,'h');i=b.meet(b.row(0),b.row(1));p=finish(b,i)
        soft=S.soften_rows(old,p,'h',())
        target=replace(new,revision=soft.context.revision+'-new')
        replayed=R.replay(soft.context,target,soft.proof)
        direct=R.replay(old,new,p);rebuilt=S.soften_rows(new,direct,'h',())
        self.assertEqual(R.check(target,replayed).budget,F(10))
        self.assertEqual(R.check(new,direct).budget,F(0))
        self.assertEqual(R.check(rebuilt.context,rebuilt.proof).budget,F(0))

    def test_case_proof_mutation_is_rejected_by_unchanged_checker(self):
        ctx,result,_=self.calc;p=result.proof;s=p.steps[p.root]
        changed=replace(s,budget=s.budget-F(1))
        broken=R.Proof(p.steps[:p.root]+(changed,)+p.steps[p.root+1:],p.root)
        with self.assertRaises(R.ProofError): R.check(ctx,broken)

    def test_resource_limits_refuse_not_truncate(self):
        ctx,_,branches=self.calc;cut=R.sub(R.src('u'),R.num(F(1,4)))
        for limits in (Limits(nodes=1),Limits(term_occurrences=1)):
            with self.assertRaises(ExpansionLimit): compile_sign_split(ctx,cut,*branches,limits)
        with self.assertRaises(R.ProofError): bounded(branches[0].proof,Limits(nodes=True))

    def test_rehome_requires_exact_rows_not_just_coordinates(self):
        ctx,_,live=self.empty
        with self.assertRaises(R.ProofError): rehome(live.context,ctx,live.proof)

    def test_sqrt_has_no_finite_linear_guard_gain(self):
        # Exact square comparison avoids relying on floating-point square roots.
        for k in (F(1),F(10),F(10**6)):
            u=1/(4*k*k)
            self.assertLess((k*u)**2,u)

    def test_probability_of_coverage_does_not_bound_expected_loss(self):
        for epsilon in (F(1,10),F(1,1000)):
            self.assertEqual(epsilon*(2/epsilon)-1,1)


    def test_replayed_exclusion_can_survive_as_a_graded_proof(self):
        old,out,_=self.empty;x=R.src('x')
        new=replace(old,revision='near-not-empty',cases=(replace(old.cases[0],
            rows=(R.Row(R.scale(-1,x),R.num(F(1,8))),),witness=(('x',F(0)),)),))
        with self.assertRaises(R.ProofError): exclusion_proof(new,x,EmptyBranch((F(1),),F(1)))
        p=R.replay(old,new,out.proof)
        self.assertEqual(R.check(new,p).budget,F(-3,8))
        self.assertTrue(R.reference_holds(new,p,{'x':F(-1,8)},'h'))

    def test_repeated_guard_use_has_gain_two(self):
        x=R.src('x');parent=R.context(('x',),(),{'x':0})
        bc=branch_context(parent,x,False,{'x':0});b=R.Builder(bc,'h')
        i=b.add(b.row(0),b.row(0));live=LiveBranch(bc,finish(b,i))
        out=discharge_branch(parent,x,False,live)
        self.assertEqual(out.gain,F(2))
        self.assertTrue(R.reference_holds(parent,out.proof,{'x':F(3)},'h'))

    def test_guard_and_query_units_must_match(self):
        parent=R.context((('x','U'),),(),{'x':0},units=('U','V'))
        branches=[]
        for pos in (False,True):
            bc=branch_context(parent,R.src('x'),pos,{'x':0});b=R.Builder(bc,'h')
            branches.append(LiveBranch(bc,finish(b,b.constant(R.num(-1,'V'),R.num(0,'V')))))
        with self.assertRaises(R.ProofError): compile_sign_split(parent,R.src('x'),*branches)

    def test_weighted_cover_single_guard(self):
        x=R.src('x');ctx=R.context(('x',),(R.Row(x,R.num(-2)),),{'x':-2})
        new=rho(x,ctx);old=R.num(0);target=R.add(old,R.scale(1,new));b=R.Builder(ctx,'h')
        p=finish(b,b.constant(new,target));b=R.Builder(ctx,'h');cov=finish(b,b.row(0))
        out=weighted_cover(ctx,new,old,(CoverInput(x,F(0),F(1),F(1),p),),cov)
        self.assertEqual(R.check(ctx,out).budget,0)

    def test_weighted_cover_unequal_parameters(self):
        A=(F(-1),F(0),F(1,2));ks=(F(1),F(2),F(3));ws=(F(1),F(2),F(1));eta=F(5)
        H=sum(w/k for w,k in zip(ws,ks));M=max(max(A),(eta+sum(w*a/k for w,a,k in zip(ws,A,ks)))/H)
        values=[(M-a)/k for a,k in zip(A,ks)]
        gs=tuple(map(R.src,('g1','g2','g3')));total=R.add(R.add(R.scale(ws[0],gs[0]),R.scale(ws[1],gs[1])),R.scale(ws[2],gs[2]))
        ctx=R.context(('g1','g2','g3'),(R.Row(total,R.num(eta)),),dict(zip(('g1','g2','g3'),values)))
        terms=[R.add(R.num(a),R.scale(k,rho(g,ctx))) for a,k,g in zip(A,ks,gs)]
        first=R.minimum(terms[0],terms[1]);new=R.minimum(first,terms[2]);old=R.num(0);entries=[]
        for j,(a,k,w,g) in enumerate(zip(A,ks,ws,gs)):
            b=R.Builder(ctx,'h')
            if j<2:
                i=b.trans(b.lattice('min_left',first,terms[2]),b.lattice('min_left' if j==0 else 'min_right',terms[0],terms[1]))
            else: i=b.lattice('min_right',first,terms[2])
            i=external(b,i,a,new,R.add(old,R.scale(k,rho(g,ctx))))
            entries.append(CoverInput(g,a,k,w,finish(b,i)))
        b=R.Builder(ctx,'h');cov=finish(b,b.row(0))
        out=weighted_cover(ctx,new,old,tuple(entries),cov)
        self.assertEqual(R.check(ctx,out).budget,M)
        self.assertEqual(R.evaluate(new,ctx.signature,dict(ctx.cases[0].witness)),M)

    def test_positive_guard_rescaling_preserves_cover_bound(self):
        As=(F(-1),F(1));ks=(F(2),F(3));ws=(F(1),F(4));eta=F(2);scales=(F(7),F(1,5))
        bound=lambda k,w:max(max(As),(eta+sum(a*x/y for a,x,y in zip(As,w,k)))/sum(x/y for x,y in zip(w,k)))
        self.assertEqual(bound(ks,ws),bound(tuple(k/s for k,s in zip(ks,scales)),tuple(w/s for w,s in zip(ws,scales))))

    def test_tampered_coverage_trace_rejected(self):
        ctx,p,_,_,_=self.triple
        row_i=next(i for i,s in enumerate(p.steps) if s.rule=='row')
        changed=replace(p.steps[row_i],budget=p.steps[row_i].budget-F(1))
        broken=R.Proof(p.steps[:row_i]+(changed,)+p.steps[row_i+1:],p.root)
        with self.assertRaises(R.ProofError): R.check(ctx,broken)


    def test_two_hinge_direct_and_weighted_emitters_agree(self):
        ctx=R.context(('u',),(),{'u':0});u=R.src('u');old=R.num(0)
        a,c,A,B,k,l=F(-1),F(2),F(-2),F(-1),F(2),F(3)
        gs=(R.sub(u,R.num(a)),R.sub(R.num(c),u))
        terms=(R.add(R.num(A),R.scale(k,rho(gs[0],ctx))),R.add(R.num(B),R.scale(l,rho(gs[1],ctx))))
        new=R.minimum(*terms);entries=[]
        for j,(base,gain,g) in enumerate(zip((A,B),(k,l),gs)):
            b=R.Builder(ctx,'h');i=b.lattice('min_left' if j==0 else 'min_right',*terms)
            i=external(b,i,base,new,R.add(old,R.scale(gain,rho(g,ctx))))
            entries.append(CoverInput(g,base,gain,F(1),finish(b,i)))
        b=R.Builder(ctx,'h');cov=finish(b,b.constant(R.add(*gs),old))
        generic=weighted_cover(ctx,new,old,tuple(entries),cov)
        direct=offset_hinge_certificate(ctx,u,a,c,A,B,k,l)
        self.assertEqual(R.check(ctx,direct).budget,R.check(ctx,generic).budget)
        self.assertEqual(R.check(ctx,direct).budget,sharp_hinge_bound(a,c,A,B,k,l))

    def test_tiny_ray_imbalance_is_material_on_unbounded_sources(self):
        e=F(1,10**12);x,y=R.src('x'),R.src('y')
        ctx=R.context(('x','y'),(R.Row(R.add(R.scale(-1,x),R.scale(e,y)),R.num(-1)),),{'x':0,'y':-1/e})
        bc=branch_context(ctx,x,False,{'x':0,'y':-1/e})
        self.assertTrue(bc.feasible('h',{'x':F(0),'y':-1/e}))
        with self.assertRaises(R.ProofError): exclusion_proof(ctx,x,EmptyBranch((F(1),),F(1)))


    def test_term_dag_transport_is_lossless(self):
        for ctx,p in ((self.calc[0],self.calc[1].proof),(self.abs[0],self.abs[1].proof),(self.triple[0],self.triple[1])):
            payload=json.loads(json.dumps(pack_proof(p)))
            recovered=unpack_proof(ctx,payload)
            self.assertEqual(recovered,p)
            self.assertLess(len(json.dumps(payload)),len(json.dumps(R.serial(p))))

    def test_term_dag_forward_reference_rejected(self):
        ctx,p=self.calc[0],self.calc[1].proof;data=pack_proof(p)
        data['terms'][0]['args']=[0]
        with self.assertRaises(R.ProofError): unpack_proof(ctx,data)

    def test_term_dag_tampered_budget_still_checked(self):
        ctx,p=self.calc[0],self.calc[1].proof;data=pack_proof(p)
        data['steps'][data['root']]['budget']='-1000'
        with self.assertRaises(R.ProofError): unpack_proof(ctx,data)


def report():
    examples={}
    for name,fn in (('bound_calculator',calculator_example),('absolute_loss',absolute_case_example),('strict_empty_branch',empty_example)):
        ctx,out,_=fn();root=R.check(ctx,out.proof)
        examples[name]={'context':R.serial(ctx),'proof':pack_proof(out.proof),'bound':str(root.budget),
                        'method':out.method,'branch_budgets':list(map(str,out.branch_budgets)),
                        'guard_gains':list(map(str,out.gains)),'instructions':len(out.proof.steps)}
    ctx,p,direct,_,_=triple_example()
    examples['three_argument_cover']={'context':R.serial(ctx),'proof':pack_proof(p),'bound':str(R.check(ctx,p).budget),
        'direct_signed_proof':pack_proof(direct),'instructions':len(p.steps)}
    ctx=R.context(('x',),(),{'x':0})
    p=offset_hinge_certificate(ctx,R.src('x'),F(-1,4),F(1,4),F(-1,2),F(-1,2),1,1)
    examples['improvement_despite_coverage_gap']={'context':R.serial(ctx),'proof':pack_proof(p),
        'bound':str(R.check(ctx,p).budget),'instructions':len(p.steps)}
    return {'scope':'F06 derived finite macros, supplied proofs; no automatic proof search or F07 audit',
        'kernel':'unchanged f06_inference_rules.py', 'arithmetic':'exact rational coefficients; finite real semantic scope',
        'proof_transport':'F06-term-dag-v1: full traces with backward term references, decoded and checked by unpack_proof',
        'examples':examples,'limits':['one declared parent case per macro','affine sign guards',
        'positive gains/weights for weighted cover','strict rational rays for empty branches',
        'no empirical calibration, policy execution verifier, neural training, or novelty priority'],
        'finite_validation':{'two_hinge_parameter_sets':64,'weighted_sharpness_cases':12,
                             'instruction_limit':20000,'term_occurrence_limit':1500000}}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',type=Path);args=p.parse_args()
    out=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(F06DerivedCaseTests))
    if not out.wasSuccessful(): return 1
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report(),sort_keys=True,indent=2)+'\n',encoding='utf-8')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
