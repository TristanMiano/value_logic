"""Request-bound near-exclusion audit, not a new inference kernel.

Numerical field consistency is checked against ordinary K proofs. This does not
verify empirical provenance, historical producer identity, or deployment meaning.
Supported inputs have the same finite, immutable, exact-data restrictions as K.
Python 3.10+; standard library only.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
import unittest
from unittest.mock import patch

from v2.checks import f06_inference_rules as K
from v2.checks import f06_derived_cases as D
from v2.checks import f07_soundness as H


def receive_near_exclusion(
    parent: K.Context,
    allowance: D.GuardAllowance,
    guard_upper: K.Proof,
    expected: H.Request,
    *,
    strict: bool = False,
    limits: D.Limits = D.Limits(),
) -> K.Proof:
    """Return a checked literal root for the independently supplied request.

    Validate new, old, guard, baseline and gain against the allowance proof;
    invoke the existing producer; then check its result independently. Both
    interface rewrites are explicit K steps. An improved producer may return
    a stronger bound than A+k*max(eta,0). No successful-return/optimality or
    resource guarantee is inferred from the existence of this receiver.

    ``strict=False`` requests new-old <= expected.budget. ``strict=True``
    additionally requires a returned bound strictly below expected.budget.
    This adapter intentionally accepts one local case, not global requests.
    """
    if not isinstance(allowance, D.GuardAllowance) or not isinstance(expected, H.Request):
        raise H.AuditError('Expected a GuardAllowance and an independently supplied Request.')
    if not isinstance(allowance.proof, K.Proof) or not isinstance(guard_upper, K.Proof):
        raise H.AuditError('Both premises must be finite K proofs.')
    if type(strict) is not bool or not isinstance(limits, D.Limits):
        raise H.AuditError('Strictness must be Boolean and limits must be explicit Limits.')
    limits.validate()
    name = D.single(parent)
    if expected.context_id != K.fingerprint(parent) or expected.case != name:
        raise H.AuditError('This receiver requires the current local-case request.')
    requested_budget = H.exact(expected.budget)
    if (K.infer(expected.new, parent.signature) != expected.unit or
            K.infer(expected.old, parent.signature) != expected.unit):
        raise H.AuditError('Request unit mismatch.')
    if (allowance.new, allowance.old) != (expected.new, expected.old):
        raise H.AuditError('Allowance metadata does not name the requested pair.')
    baseline, gain = H.exact(allowance.baseline), H.exact(allowance.gain)
    if gain < 0 or K.infer(allowance.guard, parent.signature) != expected.unit:
        raise H.AuditError('The guard requires the request unit and a nonnegative gain.')
    for proof in (allowance.proof, guard_upper):
        D.bounded(proof, limits)
    a, q = K.check(parent, allowance.proof), K.check(parent, guard_upper)
    target = K.add(expected.old, K.scale(gain, D.rho(allowance.guard, parent)))
    if (a.case != name or a.budget != baseline or
            not K.same_difference(a.new, a.old, expected.new, target, parent.signature)):
        raise H.AuditError('The proof does not establish the advertised guard allowance.')
    zero = K.num(0, expected.unit)
    if (q.case != name or
            not K.same_difference(q.new, q.old, allowance.guard, zero, parent.signature)):
        raise H.AuditError('The guard proof has the wrong difference or local scope.')
    # Normalize the allowance pair through a real checked inference, not a
    # silent reassignment of the returned proof's meaning.
    build = K.Builder(parent, name)
    build.steps = list(allowance.proof.steps)
    normalized = D.finish(build, build.rewrite(allowance.proof.root, expected.new, target), limits)
    supplied = replace(allowance, proof=normalized, baseline=baseline, gain=gain)
    ceiling = baseline + gain * max(H.exact(q.budget), F(0))
    candidate = D.almost_exclusion(parent, supplied, guard_upper, limits)
    D.bounded(candidate, limits)
    root = K.check(parent, candidate)
    if (root.case != name or root.budget > ceiling or
            not K.same_difference(root.new, root.old, expected.new, expected.old, parent.signature)):
        raise H.AuditError('Producer output violates the independently reconstructed postcondition.')
    build = K.Builder(parent, name)
    build.steps = list(candidate.steps)
    result = D.finish(build, build.rewrite(candidate.root, expected.new, expected.old), limits)
    root = H.receive(parent, result, expected)
    if strict and H.exact(root.budget) >= requested_budget:
        raise H.AuditError('An inclusive equality bound does not certify a strict request.')
    return result


def fixture(baseline=F(-1), gain=F(1), eta=F(1,2)):
    """A sharp CPWA numerical model; not evidence about deployed programs."""
    baseline, gain, eta = map(H.exact, (baseline, gain, eta))
    x, z = K.src('x'), K.src('z')
    ctx = K.context(('x','z'), (K.Row(x,K.num(eta)),), {'x':min(eta,F(0)), 'z':0})
    old = z
    new = K.add(old, K.add(K.num(baseline), K.scale(gain,D.rho(x,ctx))))
    target = K.add(old,K.scale(gain,D.rho(x,ctx)))
    b = K.Builder(ctx,'h'); b.constant(new,target)
    record = D.GuardAllowance(b.proof(),baseline,gain,x,new,old)
    b = K.Builder(ctx,'h'); b.row(0)
    request = H.request(ctx,'h',new,old,baseline+gain*max(eta,F(0)))
    return ctx,record,b.proof(),request


def paired_policy_fixture(eta=F(1,16), discrepancy=F(1,32)):
    """Report-dependent paired costs with a separately assumed proxy row.

    p,s are branch probabilities; r is fixed in each program. J(r) adds r/4
    resource cost and a common unbounded baseline. The new program has the
    paired proxy discrepancy e. No empirical correctness is inferred here.
    """
    eta, discrepancy = H.exact(eta), H.exact(discrepancy)
    p,s,e,z = map(K.src,('p','s','e','z'))
    guard = K.add(K.sub(s,p),K.num(F(1,2)))
    rows = (K.Row(K.num(0),p),K.Row(p,K.num(1)),
            K.Row(K.num(0),s),K.Row(s,K.num(F(1,4))),
            K.Row(e,K.num(discrepancy)),K.Row(guard,K.num(eta)))
    # These test parameters have an explicit feasible witness.
    ctx = K.context(('p','s','e','z'),rows,
                    {'p':max(F(1,2),F(1,2)-eta),'s':0,'e':discrepancy,'z':0},
                    scope='F07-S3-paired-policy/current-numerical-coordinates')
    def loss(r):
        return K.add(K.add(K.scale(1-r,p),K.scale(r,s)),K.add(K.num(r/4),z))
    old=loss(F(1,2)); new=K.add(loss(F(3,4)),e)
    baseline=discrepancy-F(1,16); gain=F(1,4)
    b=K.Builder(ctx,'h')
    i=b.scale(gain,b.lattice('max_left',guard,K.num(0)))
    i=b.add(i,b.row(4))
    i=b.add(i,b.constant(K.num(F(-1,16)),K.num(0)))
    b.rewrite(i,new,K.add(old,K.scale(gain,D.rho(guard,ctx))))
    record=D.GuardAllowance(b.proof(),baseline,gain,guard,new,old)
    b=K.Builder(ctx,'h'); b.row(5)
    req=H.request(ctx,'h',new,old,baseline+gain*max(eta,F(0)))
    return ctx,record,b.proof(),req


class F07NearExclusionTests(unittest.TestCase):
    def rejects(self,ctx,a,g,r,**kwargs):
        with self.assertRaises((H.AuditError,K.ProofError,K.SemanticError)):
            receive_near_exclusion(ctx,a,g,r,**kwargs)

    def test_honest_literal_request(self):
        c,a,g,r=fixture(); out=receive_near_exclusion(c,a,g,r)
        root=H.receive(c,out,r)
        self.assertEqual((root.new,root.old),(r.new,r.old))
        self.assertEqual(root.budget,F(-1,2))

    def test_current_raw_interface_counterexample_or_future_hardening(self):
        c,a,g,r=fixture()
        forged=replace(a,baseline=F(-100),new=K.num(3))
        try:
            out=D.almost_exclusion(c,forged,g)
        except (H.AuditError,K.ProofError,K.SemanticError):
            return  # A future input-contract repair is allowed, not frozen out.
        K.check(c,out)
        with self.assertRaises(H.AuditError):
            H.receive(c,out,H.request(c,'h',forged.new,forged.old,F(-100)))

    def test_forged_baseline(self):
        c,a,g,r=fixture(); self.rejects(c,replace(a,baseline=F(-100)),g,r)

    def test_forged_new_field(self):
        c,a,g,r=fixture(); self.rejects(c,replace(a,new=K.num(3)),g,r)

    def test_forged_old_field(self):
        c,a,g,r=fixture(); self.rejects(c,replace(a,old=K.num(0)),g,r)

    def test_also_forging_request_does_not_supply_missing_proof(self):
        c,a,g,r=fixture(); a=replace(a,new=K.num(3),baseline=F(-100))
        self.rejects(c,a,g,H.request(c,'h',a.new,a.old,F(-100)))

    def test_false_gain_on_nonconstant_guard(self):
        c,a,g,r=fixture(); self.rejects(c,replace(a,gain=F(0)),g,r)

    def test_wrong_guard_field(self):
        c,a,g,r=fixture(); self.rejects(c,replace(a,guard=K.add(a.guard,K.num(1))),g,r)

    def test_negative_gain(self):
        c,a,g,r=fixture(); self.rejects(c,replace(a,gain=F(-1)),g,r)

    def test_inexact_baseline_or_gain(self):
        c,a,g,r=fixture()
        for value in (True,0.5,float('inf'),float('nan')):
            with self.subTest(value=value):
                self.rejects(c,replace(a,baseline=value),g,r)
                self.rejects(c,replace(a,gain=value),g,r)

    def test_bad_request_budget(self):
        c,a,g,r=fixture()
        for value in (True,0.5): self.rejects(c,a,g,replace(r,budget=value))

    def test_bad_request_unit(self):
        c,a,g,r=fixture(); self.rejects(c,a,g,replace(r,unit='not-the-unit'))

    def test_wrong_request_context(self):
        c,a,g,r=fixture(); self.rejects(c,a,g,replace(r,context_id='stale'))

    def test_changed_current_revision(self):
        c,a,g,r=fixture(); new=replace(c,revision='current-v2')
        self.rejects(new,a,g,r)
        self.rejects(new,a,g,H.request(new,'h',a.new,a.old,r.budget))

    def test_global_request_is_outside_local_adapter(self):
        c,a,g,r=fixture(); self.rejects(c,a,g,replace(r,case=None))

    def test_unknown_case(self):
        c,a,g,r=fixture(); self.rejects(c,a,g,replace(r,case='missing'))

    def test_global_guard_needs_explicit_localization(self):
        c,a,g,r=fixture(); b=K.Builder(c); b.steps=list(g.steps)
        b.all_cases([g.root]); self.rejects(c,a,b.proof(),r)

    def test_wrong_guard_proof(self):
        c,a,g,r=fixture(); b=K.Builder(c,'h'); b.constant(K.num(0),K.num(0))
        self.rejects(c,a,b.proof(),r)

    def test_invalid_attached_allowance_trace(self):
        c,a,g,r=fixture(); steps=list(a.proof.steps)
        steps[a.proof.root]=replace(steps[a.proof.root],budget=F(-100))
        self.rejects(c,replace(a,proof=K.Proof(tuple(steps),a.proof.root)),g,r)

    def test_wrong_actual_allowance_budget(self):
        c,a,g,r=fixture(); b=K.Builder(c,'h'); b.steps=list(a.proof.steps)
        p=b.proof(b.slack(F(1),a.proof.root))
        self.rejects(c,replace(a,proof=p),g,r)

    def test_equivalent_allowance_pair_gets_explicit_rewrite(self):
        c,a,g,r=fixture(); n=K.check(c,a.proof); b=K.Builder(c,'h')
        b.steps=list(a.proof.steps)
        i=b.rewrite(a.proof.root,K.add(n.new,K.num(7)),K.add(n.old,K.num(7)))
        out=receive_near_exclusion(c,replace(a,proof=b.proof(i)),g,r)
        H.receive(c,out,r)
        self.assertEqual(K.check(c,out).new,a.new)

    def test_equivalent_guard_difference(self):
        c,a,g,r=fixture(); b=K.Builder(c,'h'); b.steps=list(g.steps)
        i=b.rewrite(g.root,K.add(a.guard,K.num(7)),K.num(7))
        H.receive(c,receive_near_exclusion(c,a,b.proof(i),r),r)

    def test_requested_strength_is_not_copied_from_producer(self):
        c,a,g,r=fixture(); self.rejects(c,a,g,replace(r,budget=r.budget-F(1,100)))

    def test_weaker_guard_bound_uses_its_actual_budget(self):
        c,a,g,r=fixture(); b=K.Builder(c,'h'); b.steps=list(g.steps)
        weak=b.proof(b.slack(1,g.root))
        self.rejects(c,a,weak,r)
        req=replace(r,budget=r.budget+1)
        self.assertEqual(K.check(c,receive_near_exclusion(c,a,weak,req)).budget,req.budget)

    def test_negative_zero_and_positive_guard_budgets(self):
        for eta in (F(-2),F(0),F(1,2),F(3)):
            c,a,g,r=fixture(eta=eta)
            self.assertEqual(K.check(c,receive_near_exclusion(c,a,g,r)).budget,F(-1)+max(eta,F(0)))

    def test_zero_gain(self):
        c,a,g,r=fixture(gain=F(0),eta=F(10))
        self.assertEqual(K.check(c,receive_near_exclusion(c,a,g,r)).budget,-1)

    def test_signed_baselines(self):
        for A in (F(-3),F(0),F(2)):
            c,a,g,r=fixture(baseline=A,gain=F(3,2))
            self.assertEqual(K.check(c,receive_near_exclusion(c,a,g,r)).budget,A+F(3,4))

    def test_strict_threshold_rejects_equality(self):
        c,a,g,r=fixture(); self.rejects(c,a,g,r,strict=True)

    def test_strict_threshold_accepts_margin(self):
        c,a,g,r=fixture(); req=replace(r,budget=r.budget+F(1,100))
        root=K.check(c,receive_near_exclusion(c,a,g,req,strict=True))
        self.assertLess(root.budget,req.budget)

    def test_strict_flag_is_boolean(self):
        c,a,g,r=fixture()
        for flag in (1,'yes',None): self.rejects(c,a,g,r,strict=flag)

    def test_expansion_refusal_is_not_acceptance(self):
        c,a,g,r=fixture(); self.rejects(c,a,g,r,limits=D.Limits(nodes=1,term_occurrences=1))

    def test_input_records_not_mutated(self):
        c,a,g,r=fixture(); before=K.serial((c,a,g,r))
        receive_near_exclusion(c,a,g,r)
        self.assertEqual(K.serial((c,a,g,r)),before)

    def test_unrelated_valid_producer_output_rejected(self):
        c,a,g,r=fixture(); b=K.Builder(c,'h'); b.constant(K.num(0),K.num(0))
        with patch.object(D,'almost_exclusion',return_value=b.proof()): self.rejects(c,a,g,r)

    def test_weaker_valid_producer_output_rejected(self):
        c,a,g,r=fixture(); raw=D.almost_exclusion(c,a,g)
        b=K.Builder(c,'h'); b.steps=list(raw.steps)
        weak=b.proof(b.slack(1,raw.root))
        with patch.object(D,'almost_exclusion',return_value=weak):
            self.rejects(c,a,g,replace(r,budget=r.budget+2))

    def test_stronger_valid_producer_output_is_allowed(self):
        x=K.src('x'); c=K.context(('x',),(K.Row(x,K.num(-1)),),{'x':-1})
        b=K.Builder(c,'h'); i=b.lattice('max_left',x,K.num(0))
        i=b.rewrite(i,x,K.add(K.num(0),K.scale(1,D.rho(x,c))))
        a=D.GuardAllowance(b.proof(i),F(0),F(1),x,x,K.num(0))
        b=K.Builder(c,'h'); i=b.rewrite(b.row(0),x,K.num(0)); g=b.proof(i)
        r=H.request(c,'h',x,K.num(0),0)
        with patch.object(D,'almost_exclusion',return_value=g):
            out=receive_near_exclusion(c,a,g,r,strict=True)
        self.assertEqual(K.check(c,out).budget,-1)

    def test_finite_reference_grid_and_unbounded_common_offset(self):
        for A in (F(-2),F(0),F(1)):
            for k in (F(0),F(1,2),F(2)):
                for eta in (F(-1),F(0),F(3,4)):
                    c,a,g,r=fixture(A,k,eta)
                    out=receive_near_exclusion(c,a,g,r); root=K.check(c,out)
                    for x in (eta-F(3),eta):
                        for z in (F(-10**50),F(0),F(10**50)):
                            # Direct formula is independent of proof construction.
                            self.assertLessEqual(A+k*max(x,F(0)),root.budget)
                            self.assertEqual(K.evaluate(root.new,c.signature,{'x':x,'z':z})-
                                             K.evaluate(root.old,c.signature,{'x':x,'z':z}),
                                             A+k*max(x,F(0)))
                    self.assertEqual(A+k*max(eta,F(0)),root.budget)

    def test_paired_policy_not_supplied_as_a_final_score(self):
        c,a,g,r=paired_policy_fixture(); out=receive_near_exclusion(c,a,g,r)
        self.assertEqual(K.check(c,out).budget,F(-1,64))
        self.assertEqual(sum(n.rule=='row' for n in a.proof.steps),1)
        self.assertIn('lattice',{n.rule for n in a.proof.steps})

    def test_paired_policy_strict_boundary_and_countermodel(self):
        for eta in (F(1,16),F(1,8),F(1,4)):
            c,a,g,r=paired_policy_fixture(eta)
            out=receive_near_exclusion(c,a,g,r); root=K.check(c,out)
            x={'p':F(1,2)-eta,'s':F(0),'e':F(1,32),'z':F(10**60)}
            self.assertTrue(c.feasible('h',x))
            # Reconstruct the policy loss from its branch law, not the AST.
            def J(q): return (1-q)*x['p']+q*x['s']+q/F(4)
            d=J(F(3,4))+x['e']-J(F(1,2))
            self.assertEqual(d,root.budget)
            zero=replace(r,budget=F(0))
            if eta<F(1,8): receive_near_exclusion(c,a,g,zero,strict=True)
            elif eta==F(1,8):
                receive_near_exclusion(c,a,g,zero)
                self.rejects(c,a,g,zero,strict=True)
            else:
                self.assertGreater(d,0); self.rejects(c,a,g,zero)

    def test_proxy_discrepancy_changes_actual_guarantee(self):
        c,a,g,r=paired_policy_fixture(F(1,16),F(3,32))
        self.assertEqual(K.check(c,receive_near_exclusion(c,a,g,r)).budget,F(3,64))
        self.rejects(c,a,g,replace(r,budget=F(0)))


if __name__ == '__main__':
    unittest.main()
