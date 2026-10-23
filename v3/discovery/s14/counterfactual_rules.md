# Counterfactual use of jointly learned rules

Codex (GPT-6), October23,2026. DEVELOPMENT. A synthesis of the latent-span
certificate with ordinary affine weakest preconditions; no new causal
identification principle or abstract transformer is claimed.

Let the factual raw case be x in F2^n and fix the feature map z=Hx before
sampling. A truthful evidence state supplies a subspace S_hat containing
the latent span at the accepted cohort. Let E=S_hat^perp, so Q=EH represents
the retained equations on raw cases. The sound outer source is

    U={x:Hx in S_hat}=ker(Q).

On the common good training event, a fresh factual case belongs to U with
probability at least1-epsilon. The stronger underlying protected set from
learned_scope.md is retained when models change.

Suppose an intervention has explicitly justified semantics

    x'=P x+c.

For a requested parity t*x', the exact decision rule on this outer source is

    t*P in row(Q)  =>  t*x'=t*c for every x in U.          (1)

Conversely, if t*P is not in row(Q), there is a vector u in ker(Q) with
t*P*u=1. Cases0 and u then yield opposite counterfactual answers, so this
source cannot authorize either constant answer. This proves maximality
for the specified source and constant parity-output duty. It is simply
annihilator duality / the weakest precondition of an affine assignment.

Every permitted action/target pair satisfying(1) is correct on the SAME
factual set U. Choosing among those pairs after observing other information
about the new case does not require a union bound: on U they all hold.
This gives an unconditional per-case error bound, not a conditional error
bound among a rare selected subset. If future learned Q changes, require
its equations still hold on the original accepted latent span as before.

## Transporting the entire feature model is a stronger duty

For full-row-rank H, an exact feature-space intervention z'=Tz+Hc exists
iff HP=TH for some T, equivalently ker(H) is contained in ker(HP). This
can fail even when the particular parity requested in(1) is certifiable.
One should not demand a full transported feature model when the selected
counterfactual decision needs only a row-space test.

A simple insufficiency witness is H=[1 1], P=diag(1,0). Factual cases00
and11 have the same syndrome0, but their revised syndromes are0 and1.
Observational agreement on Hx cannot identify this intervention's answer.
No number of refinements about only that original syndrome distinguishes
these two cases. Extra raw evidence or a stronger structural premise is needed.

For a positive three-bit example take H with rows(1,1,0),(0,0,1), and
retain only the first equation, so U consists of x1=x2. Define

    x'=(x1+x3+1, x2+x3, x1).

The revised first parity x1'+x2' equals1 throughout U, although both
coordinates change and x3 is unresolved. The revised second feature x3'
is not determined by Hx:000 and110 share factual features00 but give
revised second features0 and1. Thus the full feature model cannot be
transported, while the chosen counterfactual parity is authorized exactly.

## Cost and statistical interpretation

Equation(1) needs a row-space membership test after the old equations and
intervention description have been acquired. No new truth sample or
raw-case audit is required for that test. This is an additional capability
of retained evidence, not a measured reduction of complete computation.
Compilation, storage, provenance, statistical calibration and checking the
intervention semantics remain paid.

The risk statement concerns new factual x drawn from the original law,
followed by a declared intervention. An arbitrary new population is a
different problem and needs a shift warrant such as confidence_scope.md.
Learning Hx relations alone never establishes the physical/semantic claim
x'=Px+c. Ordinary affine abstract interpretation and the same statistical
composition tie. Moderate novelty, if present, would concern the explicit
partial-evidence/common-event service, not affine program analysis itself.
