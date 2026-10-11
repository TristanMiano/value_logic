# Successful completion can select only failed confidence reports

Contributor: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10. **P3-08 DEVELOPMENT**.
This is an exact finite assumption witness for the reporting interface, not
a new CNF benchmark, a measured CNF resource bill, or a claim about empirical
coverage of seeded development runs.

## Fixed deterministic service and selector

Take sixteen blocks of two requests. Every block has the same deterministic
answer pair `(0, 1)`, a constant expert forecasts `q=1` on both requests, and
the selector independently chooses either position with probability one
half. There is no hard override. The selected checked answer replaces the
selected terminal action; the issued Brier forecast remains immutable.
Unselected lottery actions equal one deterministically. Mathematical truth
does not vary; only the purchased position varies.

Let `X` count blocks in which the zero-answer position is selected. Under
the stated independent fair selectors, `X ~ Binomial(16, 1/2)`. The actual
issued Brier total, ordinary sampling center, and shared residual are

\[
F=16,\qquad A_c=2X,\qquad F-A_c=16-2X.
\]

The unselected conditional action mean is `V=16-X`, and its center is
`U_c=X`, giving the same residual. These equations follow by summing the
two possible outcomes of one block. No unknown truth is supplied to the
deployment policy.

The fixed public bound from [the live performance derivation](08_live_hard_performance.md)
has `C_k=2`, `Q=64`, `S=2`, `m=16`, and

\[
R=S\lceil\sqrt{2m}\rceil=12,\qquad
\rho=Q/R+5R/8=77/6.
\]

Consequently the two-sided Brier interval misses exactly when `X<=1` or
`X>=15`. Its unconditional failure probability in this example is

\[
\frac{2\left({16\choose0}+{16\choose1}\right)}{2^{16}}
=\frac{34}{65536}=\frac{17}{32768}<\frac1{40}.
\]

The valid unconditional sampling bound is therefore entirely consistent
with this exact distribution. This computation is a finite probability
calculation over all selector strings, not a Monte Carlo coverage estimate.

## An underfunded completion filter

Define an abstract checked provider whose publicly specified fee is two
units for the first position and one for the second. The requests and fees
are fixed in advance. The provider returns the correct deterministic bit
on a completed purchase. Other service operations and report delivery are
prepaid separately. The fee table is an explicit toy service assumption;
it is not the `P308-CNF-WORD-v1` contract and does not infer computation
cost from the private evaluator's answers.

Give this provider account only seventeen units. For each block, attempt
the already selected purchase and charge its whole fee before receipt.
If the available balance cannot cover that fee, terminate with a failure,
retain all prior spent costs, and issue no confidence report. Positive
fees imply that every prefix is affordable precisely when the complete
path is affordable. The complete provider bill would be `16+X`, so

\[
\text{completion}\iff X\le1,
\qquad \Pr(\text{completion})=17/65536.
\]

Every completed path has residual at least fourteen, strictly exceeding
`77/6`. Thus

\[
\Pr(F\text{ is in the issued interval}\mid\text{completion})=0.
\]

Clipping the interval to the deterministic range `[0,32]` cannot fix an
upper endpoint already below sixteen. Joint confidence for `F,V,Z` also
fails on every completed path because its `F` component fails. We need no
claim that the action component fails.

The denied next fee is not charged in this explicit atomic-fee protocol;
previous successful fees remain charged. A provider that spends a partial
fee before failing would require its own failure invoice, but would not
turn completion into an outcome-independent event. A conservative broker
which reserves all worst-case fees in advance would reject this account
before executing. That is the intended distinction: thirty-two provider
units are sufficient for every selector path, whereas seventeen fund only
a selected subset.

## Consequence for P3-08

The example isolates why a completed cheap seed does not establish the
all-path funding premise, and why conditioning an unconditional confidence
event on successful completion needs additional justification. The owned
P3-08 broker and reporter mark finite confidence eligibility only when
their explicit worst-case resource conditions hold; even then independent
fair bits and a valid pre-outcome choice of reporting rule remain separate
premises. Their development seeds are not coverage evidence. This witness
does not assert that the exact toy event occurs under the CNF tariff.

The companion executable enumerates all `2^16` selector strings, checks
the block identities, simulates the atomic fee account and records exact
integer counts. It is deliberately a small transparent finite model,
separate from production source and priced deployment claims.
