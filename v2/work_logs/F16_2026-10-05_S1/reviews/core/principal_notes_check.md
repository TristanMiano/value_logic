# F16 core check of principal notes §§7–9

**Signed: ChatGPT (GPT-6 Astra Pro), delegated reviewer.**
2026-10-05 UTC. Principal time credit: **zero**.

**Finding:** the displayed arithmetic, kernel/rank constructions, A1 upper
certificate and geometric counterexamples check out. Three generalizations
need the precise qualifications below. They do not refute the stated
all-accepted probability example or the mean-regret theorem.

I read the principal `root_reconstruction.md` §§7–9. After reconstructing its
formulas, I consulted `09_c4_price_revision.md` for the k>=2/positive-price
scope, A1's M>0 scope, and the displayed k=4 witness data. A text search also
surfaced matching numbers in the existing price review; the calculations
below were checked directly from the displayed laws. This is a disclosed
comparison-stage review. No experiment, saved check, signed-price extension
check, or normalized-capacity experiment was rerun. No principal/frozen file
was edited.

## 1. Qualifications with exact counterexamples

### PN-01 — the expectation repair needs validity on the whole event

Earliest dependency: §7's formula immediately after the high-probability
counterexample.

The inequality

`E Delta <= b + E[(Delta-b)_+ 1_(E^c)]`

requires `Delta<=b` almost surely **on E**. The preceding always-accepted
example meets that condition. The earlier generic receiving contract only
gives it on `accepted intersect E`, which is insufficient for an unconditional
expectation over all outcomes.

Minimal witness to the stronger selective-acceptance reading: let E be the
whole sample space, b=0, accept on an event A of probability 1/2, and let
Delta be zero on A and one on its complement. Every accepted output is
correct and coverage is perfect, but the proposed excess term is zero while
E Delta=1/2.

**Status:** explicit-premise clarification. State `Delta<=b on E` before the
repair. For selective outputs the valid form is

`E[Delta 1_A] <= b P(A) + E[(Delta-b)_+ 1_(A intersect E^c)]`.

Conditioning then divides the excess allowance by P(A)>0. This is the same
acceptance-probability boundary already recognized earlier in §7.

### PN-02 — distinguish a uniform L1 rate from qualitative continuity

Earliest dependency: §7's sentence about integrability/first moments not
giving a vanishing-in-delta improvement.

There is no uniform numerical rare-event rate from a first-moment bound
alone: `X_delta=(M/delta)1_(E_delta)`, with P(E_delta)=delta, has EX_delta=M
and contributes M on the exceptional event for every delta>0.

For **one fixed integrable** nonnegative X, however, the contribution does
vanish as event probabilities go to zero. Indeed

`E[X 1_A] <= E[X 1_(X>L)] + L P(A)`;

first choose L to make the integrable tail small, then shrink P(A). Thus
integrability supplies qualitative absolute continuity, although it supplies
no distribution-free rate depending only on a stated L1 bound.

**Status:** narrow the sentence to “no uniform quantitative rate over the
admissible distributions/query family from an L1 bound alone.” The displayed
Lp/Cauchy–Schwarz repairs and the unbounded-family counterexample are correct.

### PN-03 — CVaR requires the matching old objective and comparator

Earliest dependency: §8's extension of the small-edit mean argument to any
monotone, translation-equivariant objective.

The extension is valid when the old action is optimal (or eta-optimal) for
**that same old objective**. Exact old means and their optimizer alone do
not supply a CVaR guarantee. For fixed finite losses, let action A cost 0
with probability 0.9 and 10 with probability 0.1; let B cost 2 surely.
The mean-optimal action is A (mean 1), but its upper-tail CVaR at level 0.9
is 10 versus B's 2. Its CVaR regret is 8 even with no price change.

**Status:** explicitly require the corresponding old objective values and
optimizer. The same interval proof then works for fixed-law CVaR. For a
worst-CVaR objective over a source, compare old and new worst-CVaR objectives
over that same source; do not promote that bound to same-law regret against
each law's separate CVaR optimizer. The existing mean-regret calculation is
unchanged and correct.

## 2. Directly reconstructed results

**Selection/stopping and expectation.** The inclusion of accepted-and-false
outputs in E^c is exact; the conditional bound is
`min(1,delta/P(accepted))`. The singleton-source construction attains
conditional error one. Independent trials give `1-(1-delta)^T`; its infinite
limit is one for delta>0 (and zero at delta=0). The selected affine query
equals -1 in its current singleton source and K at the actual coordinate.
For delta=1/20,K=20, its expectation is exactly +1/20. The L2 and Lp tail
allowances follow by Cauchy–Schwarz/Hölder with the stated moment norms.

**Fixed policies and reports.** Direct subtraction gives
`Delta=(s-p)/4+1/16+e`. The displayed attainer has costs 11/32 and 21/64,
including e, hence difference -1/64. The endogenous-selector example fails
on every execution despite marginal rates 1/2; its conditional rates are
both one. The report numbers are exact: h(7/16)=43/64, excess 15/64, and
the fixed robust report threshold is 4/7. Common p,s across the compared
policies remain part of the stipulated execution law, not a consequence of
knowing one policy's conditional rates. Continuously varying r,p,s generally
introduces bilinear terms outside the native CPWA fragment.

**Price kernel and repair.** The adjacent-swap sign is correct. Dividing
the residual r-subset values by their nonzero price products and using
connected one-element exchanges gives the displayed elementary-symmetric
kernel. Each monomial is counted once, at its last element. For k>=2 its
common-value functional is nonzero because e_k is the nonzero full product.
The nonproportional second-profile swap eliminates every proper-size
parameter. The terminal moment remains visible exactly through the stated
penalty coefficients. Nested-prefix new means provide triangular equations
with nonzero diagonal products; recovering the full terminal moment needs
M>0 and recovering the prefixes by division needs epsilon!=0. The adaptive
lower bound correctly concerns deterministic exact linear-query responses
at an interior law, not sample complexity or every boundary fiber.

**A1 certificate.** For the pair reach, subtracting the displayed affine
function gives residuals

`(0,-1/[3(M+2)],(M-1)/[3(M+2)],0)`.

Their range is `max(1,M)/[3(M+2)]`, bounded by the singleton range A for
M>=0, hence for A1's M>0. The two witness laws both have every old order
mean equal to 2 and singleton-reach separation A. Half that revised-mean
separation gives the stated exact radius, including 1/160 at M=4 and
|epsilon|=1/40. This uses exchangeability of the **difference**, not an
assumption that each original law is exchangeable.

**General levels and coherence.** The two normalizations plus common mean
have rank three under the stated k>=2, nonnegative-penalty scope. A vertex
has at most three positive masses in total; a nonzero optimum is one level
against two bracketing levels. The fixed-fiber residual problem has only
two equalities, giving at most two positive residual levels.

For the saved k=4 witness, the singleton interval is `[5/124,1/8]`, giving
midpoint 41/496 and half-width 21/496. The other midpoint moments force
m4=5/372 and exact two-failure world mass -3/496. The displayed coherent
level law sums to one and has mean 9/8; its singleton moment is 41/496,
pair moment 871/26288, and triple moment 55/6572. These attain the stated
common maximum tolerance. Independently, the generic three-vertex convex
set has unconstrained radius 1/2 and constrained radius 2/3 by its
coordinate-sum-two constraint. Neither example proves a universal statement
about coherence penalties in reset-summary fibers.

**Choquet boundary.** Ordered nonnegative score differences are precisely
the subsequent prices and final M, giving the displayed subtraction identity.
The zero-score always-successful dummy normalizes the coverage capacity
without changing any positive superlevel set. At M=0, zero-score ties add
no increment and the terminal moment remains invisible. This uses the
intended positive prices and M>=0; the optional signed-price rank extension
does not automatically extend this nonnegative-score bridge. Keeping the
dummy face, coverage restrictions and original k! observation family is
necessary when applying an external normalized-capacity theorem. No
priority or literature-identification conclusion follows from this check.

No further mathematical correction was identified in the inspected scope.
