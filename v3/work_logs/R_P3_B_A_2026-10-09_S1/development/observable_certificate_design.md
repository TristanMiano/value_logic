# Observable episode performance from purchased labels alone

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
R-P3-B-A, DEVELOPMENT. Prospective principal D/X extension within the
selected paid selective-feedback question; no P3-08 integration.

## New question and intended scope

The private evaluator can score every answer, but a deployed reasoner cannot
use those labels for free. Can the already purchased labels certify the
completed episode's unbought conditional-action loss and immutable Brier
score? This is a meaningful remaining usefulness-estimation question, distinct
from the expert-relative expectation theorem. Derive a concentration bound,
then inspect it as an explicitly post-run diagnostic on the existing evidence.
No new learner, service, label or seed run is authorized by this note.

## Candidate observable estimators

For each block, let d_t=q_t if y_t=0 and 1−q_t if y_t=1 be the actual emitted
dyadic forecast's randomized-action error probability. It is in [0,1]. The
frozen weights, fixed public tape and conditionally selected pi make all d_t
fixed before J, although unbought values remain unknown to the learner.
Define

U_k=(1/pi_J−1)d_J,   V_k=sum_{t!=J}d_t.

Then V_k−U_k=sum_t d_t−d_J/pi_J has conditional mean zero. Its conditional
range has width at most S=max_t(1/pi_t). For uniform sampling S=B; for the
ticket rule S=2B. A conditional Hoeffding/MGF argument therefore suggests
Pr(sum V_k > sum U_k + S sqrt(m log(1/delta)/2)) <=delta.
This estimates the realized-selector conditional action mean, not the
expectation over all fresh episode histories.

For all-issued Brier g_t=(q_t−y_t)^2, use A_k=g_J/pi_J. Then
sum_t g_t−A_k has the same mean-zero/range-width argument. This supplies a
separate Brier certificate; it never corrects an already issued forecast.
All updates and estimators use only purchased receipts and pre-issued q.

For realized terminal errors, a second action-randomization deviation bound
can be added. Under the implemented policy, weights/selectors do not depend
on sampled actions; conditional on selector history, T−m unbought independent
Bernoulli actions have mean sum V_k. Thus a union bound with delta_s+delta_a
covers U_total + sampling_radius + action_radius. Correct purchases contribute
zero terminal errors. Fresh fair randomness is a theorem premise; seeded
DEVELOPMENT traces are calculations of the formula, not validated confidence
statements for the deterministic seed generator.

## Exact finite reporting option

Use delta_s=delta_a=1/40. Since exp(4)>sum_{j=0}^5 4^j/j!>40, log40<4.
Integer radii S*ceil_sqrt(2m) and ceil_sqrt(2(T−m)) safely dominate the two
one-sided Hoeffding radii. The final terminal statement has coverage at least
19/20 under the fair-bit theorem contract; conditional-mean and Brier upper
bounds separately have coverage at least39/40. Do not claim joint Brier and
terminal coverage19/20 without allocating the additional error probability.
Clipping at T−m (terminal) or T (Brier) remains valid.

Uniform U has denominator2^h and Brier estimator denominator2^(2h).
For tickets a common denominator multiplies each by B+1; ticket multiplicity
is either1 orB+1, so exact integer accumulators suffice. At maximum admitted
h=32, all-issued Brier accumulation can need more than64 bits, which must be
priced if deployed. This task will first implement an offline certificate
calculator over retained public records, with its analysis computation
separate from the observed deployment invoices. No free online calculator
or measured deployment improvement is thereby claimed.

## Prospective diagnostic plan

After independent proof reconstruction, compute these estimators for all20
uniform and3adaptive saved arms. The calculator must read only purchased
labels, issued probabilities and published allocation records when building
the certificate. It may compare with already existing private evaluator
scores in a clearly separate second stage, with no policy selection or new
execution. Retain all rows, exact fractions, source/record hashes and any
failure. Check that no unpurchased-label field is consumed by the first stage.
