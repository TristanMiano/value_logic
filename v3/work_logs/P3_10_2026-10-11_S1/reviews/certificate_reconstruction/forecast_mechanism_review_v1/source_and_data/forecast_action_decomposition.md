# Separating forecast reweighting, hard evidence and terminal action

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**.
Developed on **2026-10-11 before reading private P3-10 outcomes**.
This is an interpretation lemma and supplemental audit specification. It does
not alter any frozen endpoint, forecast, paid path, or action policy.

## 1. Why the A2 reference matters

For each recorded position, let `y` be the privately checked binary truth,
`r` the exact equal mixture of the six original binary advice values, `w` the
unrounded mixture under the block's recorded learned weights, and `p` the actual
base dyadic forecast. Let `q` be the issued forecast after any current hard
receipt overrides the base. The frozen A2 difference is

\[
\Delta_{A2}=\operatorname{mean}[(r-y)^2-(p-y)^2].
\]

It compares a learned base forecast with the original equal advice mixture.
It does not use the later hard forecast as evidence for learning, and does not
assert advantage over a constant-half forecast, the best individual expert,
a distinct deployed ordinary controller, or an ordinary implementation of the
same kernel. The frozen scorer records those other forecast readouts separately.
An A2 effect can be real on the finite cohort while a stronger comparator wins.

## 2. An exact pointwise forecast/action-functional decomposition

Define the affine binary-error functional and forecast variance term by

\[
d(p,y)=p+(1-2p)y,\qquad v(p)=p(1-p).
\]

For binary `y`, expansion using `y^2=y` gives

\[
(p-y)^2=d(p,y)-v(p).
\]

Therefore each A2 improvement decomposes exactly as

\[
(r-y)^2-(p-y)^2
=\{d(r,y)-d(p,y)\}-\{v(r)-v(p)\}.
\]

The first term measures a change in the binary-error functional. The second
removes the change in forecast variance. Neither term alone is the realized
terminal action difference. The equality is deterministic and needs no fair-bit
hypothesis. Interpreting `d(p,y)` as a conditional expected Bernoulli-action loss
additionally requires the matching independent fair action draw. The actual
recorded dyadic draw can be reconstructed, but its fixed MT bit string does not
establish that hypothesis.

This decomposition explains how a Brier change can have a different sign from
a binary action-functional change. For example, with `y=0`, moving from `r=1/2`
to `p=1/4` improves Brier by `3/16`, while the error-functional improvement is
`1/4` and the variance decrease is `1/16`. For a mixture of positions, these
separate terms can cancel in either direction. Any resulting table must retain
the original population/seed hierarchy instead of pooling positions differently.

## 3. Exact separation of reweighting from forecast quantization

The identity

\[
(r-y)^2-(p-y)^2
=\underbrace{(r-y)^2-(w-y)^2}_{\text{unrounded reweighting}}
+\underbrace{(w-p)(w+p-2y)}_{\text{quantization contribution}}
\]

holds before hardening. The frozen implementation has six experts, state precision
16 and action precision 16. Its strictly positive weights sum to `6*65536` after
each fixed-mass update. If `W` is the total weight of positive advice and
`D=65536`, then

\[
w=\frac{W}{6D},\qquad p=\frac{\lfloor W/6\rfloor}{D},\qquad
0\leq w-p\leq\frac{5}{6D}.
\]

Consequently the absolute pointwise quantization contribution is at most
`2*(5/(6D)) = 5/196608`, about `0.0000254313`. Averaging with nonnegative weights
preserves this bound, including the frozen equal-seed-then-equal-population
hierarchy. A practical A2 effect of at least `0.01` therefore cannot be produced
by this quantization alone: the corresponding unrounded reweighting advantage
is at least `0.01 - 5/196608`, about `0.0099745687`, provided all recorded fixed-mass
and full-denominator conditions hold. This is an interpretation bound, not an
extra statistical effect estimate.

Rounding downward helps Brier at a false query and harms it at a true query:
the sign follows from `(w-p)(w+p-2y)`. It should not be treated as neutral noise.
In the first block, the weights are equal, so any exact-versus-dyadic equal-mixture
difference is entirely this arithmetic effect. A later effect need not be caused
by better acquisitions; uniform and ticket selectors also use different update
factors and bit schedules, which remain bundled in their frozen configurations.

## 4. Hard evidence and current purchases are separate mechanisms

On a successful sound epoch, a previously purchased receipt with exactly the
same full semantic/source/version key sets the issued forecast to its known
truth. Thus `q=p` without a prior matching receipt and `q=y` with one. Pointwise,

\[
(p-y)^2-(q-y)^2
=\mathbf 1\{\text{prior current hard receipt}\}(p-y)^2\geq0.
\]

The current position's newly purchased label arrives after its forecast is
issued. It can correct that position's terminal action, but cannot retrospectively
make its issued forecast perfect. A receipt acquired later in the episode can
help a retrospective report about an earlier forecast; it does not rewrite the
historical forecast or the frozen scoring chronology.

The base and hard trajectories use the same recorded action draw. At a selected
position both terminal actions use the checked purchased label. At an unselected
position, a sound prior hard receipt replaces a possibly wrong base action with
the truth. Hence

\[
\mathbf1\{a_{\rm base}\ne y\}-\mathbf1\{a_{\rm live}\ne y\}
=\mathbf1\{\text{unselected, prior hard receipt, base action wrong}\}\geq0.
\]

This exact coupling explains action corrections without claiming that a Brier
improvement forces a particular realized action improvement. It also shows why
hardening can improve forecasts at selected repeated positions without changing
those positions' already-correct purchased terminal actions.

The first occurrence of an exact full key cannot already have a receipt for that
key within an initially empty epoch. A first-occurrence improvement can reflect
learned weight transfer through paid advice, but not a same-key hard-cache hit.
“First occurrence” is a canonical-key definition, not a proof that two different
syntactic keys are logically unrelated. The gate-transfer suffix is the
prespecified stronger content-family slice; it is still a fixed finite cohort.

## 5. What the supplemental observer will check

After the full amended experiment closes, a separate read-only calculation will
use the independently reconstructed numerical transcript and exact source-bound
public advice. It will compute the above identities for all 126 scheduled
broker/mirror paths, preserving failures and horizons, then aggregate by the
frozen configuration, family, population, seed and named slice. Every identity
must hold exactly as a rational equality. Quantization bounds must hold
pointwise. First occurrences must have no prior hard hit. Hardening must preserve
its nonnegative Brier and terminal-error coupling.

The calculation may explain a frozen result; it cannot replace a failed primary
endpoint, supply free deployed advice, establish calibration or coverage, or
turn source-level identities into a novelty/contribution decision. Its extra
arithmetic is unbilled and will carry no new economic advantage claim.

## Source basis

The definitions above follow the frozen `p309_broker._metrics` and `score`
contracts, `p308_broker` fixed-mass forecasting/update implementation, and
`p309_analyze` hierarchical A2 calculation. Numerical paths and private truth
are still unread while this derivation is written. Independent reviewers are
asked to check the algebra separately from any eventual finite observations.
