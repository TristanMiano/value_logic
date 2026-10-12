# S17: conditional value evidence for a program edit

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

Let Y_0(X),Y_1(X) in [0,1] be two immutable bounded programs on the same context
law P. A checked semantic relation supplies a computable guard A(X) such that
Y_1=Y_0 outside A. The relation may come from a pure program's changed branch,
a verified dependency slice, or a separately checked output comparison. A guard
guessed by a fallible model is not enough. Let pi=P(A), and Delta=Y_1-Y_0.

For pi>0, the exact decomposition is

    mu_1 = mu_0 + pi d,       d=E[Delta | A].

For pi=0, equality holds almost surely. A bound on the conditional residual
can update a previously warranted old mean without re-estimating the common
part. This is ordinary paired/control-variate and conditional sampling logic,
attached here to explicit program versions and a checked unaffected-region claim.

## Evidence polarity and signed scaling

If old and new evaluations provide intervals [L_0,U_0],[L_1,U_1], then

    L_1-U_0 <= Delta <= U_1-L_0.

Two lower receipts alone do not give a lower difference. For example old truth
1 with receipt 0 and new truth 1/2 with receipt 1/2 would incorrectly suggest
gain 1/2 from subtracting the receipts; the actual change is -1/2. Joint symbolic
cancellation can provide a much tighter difference than separate intervals:
Y_0=C+H_0 and Y_1=C+H_1 give Delta=H_1-H_0 regardless of a costly unresolved C.
The purity/shared-source hypothesis is essential; evaluating C may not mutate
a cache or environment in one branch but not the other without that successor
state appearing in the target semantics.

A conditional residual lies in [-1,1], so Z=(Delta+1)/2 lies in [0,1]. Its lower
receipt (L_1-U_0+1)/2 can use S16's forecast-audit procedure. Convert a lower
bound z_L back to d_L=2z_L-1, then mu_1>=L(mu_0)+pi d_L. Opposite-signed stakes
require upper rather than lower residual evidence. With uncertain pi in
[pi_L,pi_U], minimize pi*d_L over that interval: choose pi_L if d_L>=0,
pi_U if d_L<0. For two-sided residual bounds, use the four rectangle corners.

## Adaptive edits and fresh conditional samples

At a stopping time, an edit, guard and audit predictor may be chosen from prior
history. Conditional on that history, freeze the new target semantics and guard.
Fresh independent X draws, accepted only when A(X), are iid from P(.|A).
The fresh residual confidence event can therefore hold conditionally on every
selection history. Combine it with the old source's event by a union bound;
independence of the two events is unnecessary. If the old source already has
one simultaneous validity event, it is paid once, not once per subsequent edit.
New edit-specific error allocations must sum to their declared total, or edits
must already belong to a valid simultaneous family such as S14.

In a fixed finite context population, fresh random indices can hit previously
computed contexts. Their checked receipts may be reused without another solver
call. The sampling draw is still paid and random; selecting only convenient
old receipts without the corresponding inclusion law is a different experiment.
Knowing pi can itself be costly: an arbitrary program guard may require model
counting. A structured prefix guard has a cheap exact mass only under the stated
context law. A population scan or rejection sampler must be included in costs.

For illustration, fixed-n Hoeffding gives conditional residual radius
sqrt(2 log(2/alpha)/n); the global difference radius is pi times this. Achieving
epsilon thus needs at most the familiar range-based requirement
2 pi^2 log(2/alpha)/epsilon^2 accepted evaluations. This is not a fair universal
pi^2 speedup claim: a strong unconditional variance-aware estimator already
benefits from the sparse guard, and an ordinary conditional estimator is the
same construction. Rejection sampling consumes about n/pi context/guard calls.
Direct conditional generation can avoid those calls when its law is verified.

## What changing value queries can reuse

Once a simultaneous source bounds the old mean, affected mass and signed
residual, later tariff or objective weights may optimize over that same source.
The coefficients must describe the same programs and source law. A chain of
edits can sum residual intervals, but widths can accumulate. Multiple certified
version paths give ordinary difference constraints on program means; graph
shortest-path tightening is safe on the joint event, without treating duplicated
evidence as independent. Measuring a direct cumulative residual may be cheaper
than refining every intermediate edge when the current decision has a margin.

Next constructive prototype: compile a pure expression edit into its cancelled
residual and exact guard, evaluate only affected contexts, and compare full,
memoized paired, and the identical ordinary incremental/conditional pipeline.
Charge compilation, sampling, expression work and certificate checking. Preserve
cases where nonlinear or stateful edits defeat the cancellation.
