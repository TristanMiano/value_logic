# S08 development: censored mathematical computations retain value evidence

Codex (GPT-6), October 11, 2026. DEVELOPMENT; Q1/Q3/Q4/Q5, with explicit-edit
application to Q2. Builds on [the finite sampling service](value_sampling.md).

## 1. A bounded query need not return a mathematical answer

The finite truth population y_1,...,y_N is fixed. A sampled evaluator may
return 0, 1, or unresolved within its allocated budget. A prediction may guide
budget allocation, but unresolved is not a negative label and timeouts cannot
be dropped from the sampling population. The evaluator/checker contract must
ensure that returned labels are sound; the current SAT prototype will still
trust native UNSAT answers. Statistical coverage does not repair unsound labels.

Generate a uniform random permutation of indices, lazily if desired. At
prefix length s, retain k known ones, z known zeros and u=s-k-z unresolved
answers. The true count in that sampled prefix is in [k,k+u], regardless of
how computation budgets were chosen or how outcome-dependent runtimes are.
Earlier unresolved queries may be resumed in any model-guided order. Do not
replace a skipped query with another and pretend the completed labels are a
uniform sample of size k+z.

For any simultaneous full-label confidence set C_s(e) derived under the
uniform sampling law, report the outer set

    C_partial(s,k,u) = union_(e=k,...,k+u) C_s(e).

At every time, this set contains C_s(e_actual). Therefore the original
simultaneous 1-alpha coverage survives arbitrary dependent censoring and
adaptive completion of earlier sampled queries. This is an outer-set argument,
not a missing-at-random assumption. Taking an interval hull is conservative.
Intersecting all previously reported outer sets preserves simultaneous
coverage as well. Arithmetic cost must include the union or a proved shortcut.

This gives an explicit interface for useful fallible computation models:
they select which unresolved sampled questions to deepen, while the sound
label checker and the simultaneous sampling construction control inference.
They cannot label the unknown questions merely because the scheduler predicts
what additional computation would return.

## 2. A cheap direct decision test avoids enumerating missing labels

For the earlier one-sided test of total count M<=M0 against fixed M1>M0,
the likelihood ratio at a fixed s is monotone in the number e of ones. On
common positive support its consecutive ratio is

    ((M1-e)/(M0-e)) *
    ((N-M0-s+e+1)/(N-M1-s+e+1)) >= 1.

The zero-support rules from value_sampling.md preserve monotonicity: too
many zeros for the boundary give ratio zero, and more than M0 ones exactly
exclude the null. Thus the worst completion for rejecting this lower-count
null sets every unresolved label to zero. Reject safely by applying the
ordinary test to (s,k), not to (k+z,k). The opposite action uses (s,z) in the
complement population. For regret tolerance, place each null boundary at the
integer count where that proposed action first violates the tolerance.

Consequently the same one-sided tests remain safe under arbitrary compute
censoring at **constant extra count-state cost**, without enumerating u+1
possible label counts. Query storage and resumable evaluator state are
additional resource obligations. This is a developmental specialization of
ordinary monotone sequential tests and partial identification, not a claim
that uncertainty induced by computation has become a new probability law.

## 3. A concrete failure of discarding unresolved answers

Take N=8 with exactly three true ones. Suppose every zero times out and every
one completes. After attempting all eight, dropping timeouts leaves three
ones and no zeros. Falsely treating those as a uniform prefix of length three
gives likelihood ratio 56 against M0=3 using M1=8, because
P_M0(all three ones)=1/C(8,3)=1/56. A level .1 test rejects the true null on
every permutation. The nominal lottery guarantee has disappeared entirely.

The partial-label service retains s=8,k=3,z=0,u=5. Its lower-null ratio is zero
for the conservative completion, so it cannot warrant the positive action.
It also cannot yet warrant the negative action: the five unknown labels could
all be one. Further computation, a valid deterministic implication or an
honest insufficient-budget outcome is necessary. This example intentionally
assumes extreme outcome-dependent censoring to expose the information error.

## 4. Edits, common receipts and cost accounting

For added clauses, old UNSAT truth transports directly; a checked old SAT
assignment may satisfy the additions and cheaply warrant a retained SAT label.
Otherwise bounded native solving may yield a sound new label or unresolved.
A sampled index remains in the prefix regardless of which route answers it.
The base receipt history and all witness tests, failed reuse, solver budgets,
sampling, interval arithmetic and storage are paid. If a prior history is
common input, report both marginal and history-inclusive costs.

A model can prioritize unresolved sampled instances likely to finish cheaply,
or those whose labels would most alter the conservative decision test. That
scheduler can improve completion cost without an assumption that its runtime
forecasts are calibrated. It has no universal gain guarantee and can waste
work; ordinary portfolios and the identical scheduler remain comparisons.
The current application is an explicit executable CNF intervention, not a
semantics for a contradictory mathematical antecedent.

## 5. Prospective cheap prototype

First implement generalized one-sided count tests and exact tiny missing-label
checks, then a small seeded SAT-family edit cohort. Compare deterministic
early stopping, uniform direct decision tests and structural stratification
under common prior receipts. Add conflict-budget censoring only after basic
receipts and costs work. Keep failures and exposed changes separate. The
application is generative development, not a new confirmation experiment.

## 6. One-sided statistical values can use positive proof production alone

Suppose a bounded SAT computation yields either a checked satisfying
assignment or no accepted evidence. Ignore every unsupported UNSAT answer.
At a uniformly sampled prefix of s formula indices, let k have accepted SAT
proofs; all other sampled labels remain unknown. The actual positive count
is at least k. The monotone one-sided test at (s,k) can therefore warrant a
lower bound on the true satisfiable fraction with its stated sampling risk,
without any trusted negative label. A malicious or weak proposer can withhold
useful witnesses and increase computation, but cannot increase the false
positive risk if every accepted witness is checked against the right formula.

This is a statistical aggregate certificate conditional on an honest uniform
sampling lottery and sound deterministic checkers. It is not a logical proof
that every sampled failure was UNSAT, and it is not an externally verifiable
probability claim if the proposer may choose or cherry-pick the sample seed.
The verifier must control random selection, or a separately specified trusted
randomness/transcript protocol must establish it. Runtime and randomness costs
belong to the interface. Individual mathematical bits remain deterministic.

Prior checked SAT receipts support a useful specialization after clause
addition. Let K formulas have old SAT witnesses. Other old formulas need not
have accepted UNSAT proofs. Among the K, scan old witnesses against the new
unit clause, obtaining b immediate accepted SAT proofs and R=K-b unresolved
members. The unscreened outside population contributes a nonnegative amount,
so the full new mean obeys mu >= (b+M_R)/N. A lower-count test on a uniform
prefix of those R can warrant a favorable action. This uses no false claim
that the other N-K formulas are UNSAT. If it fails, report insufficient
evidence or invoke a separately priced stronger service; it cannot in general
warrant the opposite action with positive proofs alone.

An ordinary exact positive-proof controller is the strongest immediate
control: it may try low-budget proof search on unresolved formulas and stop
when b+k reaches the action threshold. It too need not pay for negative
certificates and may schedule candidates by any available runtime forecast.
Compare this bounded exact controller with the statistical lower-bound
controller before attributing a benefit to statistics. Every failed budget
and the complete initial proof-acquisition bill must be charged.

## 7. Positive-only prototype outcome and present limit

[proof_values01.json](proof_values01.json) implements a stricter total-
assignment checker, including consistency, variable scope, source clauses
and the edited unit. Eleven malformed/contradictory/wrong-unit proposals are
rejected in a small screen. All 80 positive warrants on the two exposed SAT
cohorts agree with reference values. This is finite development, not a claim
that the complete provider boundary has undergone adversarial confirmation.

On n=100, summing eight request timers: exact full proof search took 595.446
ms, statistical full proof search 205.082 ms, exact bounded random scheduling
551.970 ms, exact bounded base-conflict scheduling 521.337 ms, and statistical
bounded scheduling 544.713 ms. The bounded statistical arm made 3,496 proof
attempts with 2,073 unknown returns; it nearly lost the sampling advantage.
On n=60, full statistical search took 52.330 ms versus 119.889 exact, while
bounded statistical search took 76.976 ms. Base history remains costly and is
separately included in raw lifecycle totals. Journal writes are included in
the marginal lifecycle bill; the raw scope's excluded output serialization
means final artifact/checkpoint serialization outside those timers.

The useful capability currently supported is a lower value warrant using only
checked positive witnesses. Arbitrary failures can prevent a warrant. The
first fresh-first budget scheduler is not a generally better computation
policy. A malicious proposer can cause abstention, and random sample selection
must be controlled by the verifier. There is no claim of a transferable
deterministic proof of the probability guarantee from an untrusted chosen seed.

## 8. A two-endpoint shortcut for the implemented count confidence family

The uniform/extreme-mixture confidence family admits a useful specialization
of the outer-set construction. Fix N,s and alpha, and use the working mixture
with rho in [0,1), uniform mass 1-rho plus equal extreme atoms rho/2. Let
[l(e),u(e)] be the hypergeometric confidence interval for an observed count e.
Its endpoints are nondecreasing functions of e. This needs an argument; it
does not hold by declaration for every imaginable confidence procedure.

For interior e=1,...,s-1 the mixture threshold is the same
alpha*(1-rho)/(s+1). The hypergeometric mass as a function of candidate M is
unimodal, with a mode no larger than floor(e*(N+1)/s), after clipping to its
feasible support. The mode is included, since its mass is at least 1/(s+1)
and the threshold is smaller. Hence every M below l(e) is on the left of
that mode and fails the confidence inequality. For consecutive observations,
on positive support,

    H_M(e+1)/H_M(e)
      = (M-e)*(s-e) / ((e+1)*(N-M-s+e+1)).

This ratio is at most one when

    M <= (e+1)*(N+2)/(s+1)-1.

The latter threshold exceeds e*(N+1)/s by

    (s-e)*(N+1-s) / (s*(s+1)) >= 0.

Thus a previously excluded candidate below the lower endpoint remains
excluded at e+1 when both thresholds are interior. At e=0, l(0)=0 makes
the first transition automatic. At the final transition to e=s, the extreme
atom only raises the threshold, so exclusion below the previous lower bound
is preserved. Impossible support points stay impossible. Full enumeration
s=N has l(e)=u(e)=e directly. Symmetry gives u(e)=N-l(s-e), so the upper
endpoint is nondecreasing too. The s=0 case is [0,N].

For a prefix with k known ones, z known zeros and u_missing=s-k-z, the exact
interval hull of the confidence sets for all compatible complete counts is
therefore

    [l(k), u(k+u_missing)].

Only two endpoint evaluations are required. For positive proofs alone, the
lower endpoint is l(k), with all unproved sampled bits conservatively set to
zero for this calculation. It is still a confidence bound on the actual total
number of true bits, not on the number the current solver happened to prove.
Intersect these outer intervals across reports for an anytime-valid count
source. Newly accepted proofs tighten them without treating earlier timeouts
as labels. The sampling lottery and checker assumptions remain unchanged.

This supplies the missing link to [value transport](value_transport.md):
the resulting count source supports subsequent thresholds, outside-group
positive receipts and weighted/edit queries by pointwise confidence-set
propagation. The earlier fixed-boundary tests cannot be retargeted silently.
This shortcut is a specific constructive derivation, with no claim of a new
general confidence-sequence theorem or independent verification yet.

The [initial implementation](censored_count01.json) checked 1,380 monotone
prefix families through N=20 and 2,964 exact partial-label mass-union hulls
through N=8, across the stated alpha/rho values. At N=10,000,s=256 with 136
unknown sampled labels, two endpoints took .483 ms versus 29.456 ms for 137
separate completion-count intervals in one run. This measures only arithmetic;
receipt binding, sampling and evaluation remain additional costs.
