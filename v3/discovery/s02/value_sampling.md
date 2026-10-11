# S08: construct the noisy value service from paid residual queries

Codex (GPT-6), October 11, 2026. DEVELOPMENT; S05/S06 lineage.

## 1. The missing object

The earlier [value-contrast branch](../s01/value_queries.md) assumed priced
reports with justified error bounds. Construct such a service instead. Take a
fixed finite population of N deterministic, decidable mathematical questions,
with unknown exact bits y_i. Its true frequency mu=sum(y_i)/N is a well-defined
quantity without making mathematical truth random. Exact evaluation has a
paid, declared solver/checker contract. A fallible binary predictor partitions
the population into predicted-zero and predicted-one strata of sizes N0,N1.
Freeze the predictor and partition before drawing the evaluation sample.

Let E0 be false negatives in stratum 0 and E1 false positives in stratum 1.
Then mu=(N1-E1+E0)/N. Prediction preparation, determining stratum sizes and
accessing a uniform random index within a stratum all have costs. They are not
free because inference is cheaper than exact evaluation on a single item.

## 2. Exact finite-population evidence

At a fixed sample size s_h, draw uniformly without replacement within stratum
h and observe e_h errors by exact evaluation. Conditional on the fixed finite
truth population, e_h has a hypergeometric sampling law with parameters
(N_h,E_h,s_h). An exact two-sided confidence set for E_h can be obtained by
retaining integers M whose lower and upper observed-count tail probabilities
are each at least delta/2. This is a probability guarantee over the sampling
lottery, not a pointwise logical constraint saying unqueried bits are known.

For simultaneous intervals E_h in [L_h,U_h], the induced value interval is

    [(N1-U1+L0)/N, (N1-L1+U0)/N].

The result is ordinary stratified sampling / prediction-assisted inference in
another notation. Its potential usefulness is resolving a value contrast with
fewer expensive exact mathematical computations, while forecasts can be wrong.
A conventional controller receives the same predictor, population and sampling
access and may use this exact kernel. No generic novelty is implied.

## 3. Optional stopping and allocation must be paid for correctly

Use predeclared sample stages s_j within each stratum and error allocations
delta_hj with sum_(h,j) delta_hj<=alpha. Each stratum's draws form the prefix of
an independent uniform random permutation. A union bound makes every reported
interval simultaneously valid, even if a fallible scheduler chooses which
stratum/stage to inspect next from previous results. Do not substitute a
fixed-time interval at an adaptively chosen sample count without this argument.
Finite stages can spend alpha/HJ uniformly; an infinite dyadic schedule can use
alpha/[H*(j+1)*(j+2)]. Empty strata need no sampling; full enumeration is exact.

For actions with losses 1-mu and mu, a lower value bound L warrants choosing
the first with regret at most max(0,1-2L); an upper bound U warrants the second
with regret at most max(0,2U-1). Stop once the requested epsilon is covered by
one of those **statistical** bounds, or report insufficient budget. An action
at equality is a tie. A point estimate evaluated at a data-dependent stopping
time is not automatically unbiased, even though fixed-size residual estimates
are unbiased under the stipulated sampling law.

## 4. Why the predictor may change acquisition complexity

When few errors appear, upper bounds on error counts can shrink roughly like
log(1/alpha)/s instead of a generic square-root bound for a balanced raw label
population. This intuition requires an exact derived finite bound or a precise
primary-source theorem before it is used quantitatively. Bad predictors must
retain coverage; they may offer no economic benefit. A full predictor scan and
an expensive exact-tail computation can erase saved solver calls, just as
earlier guard overhead did.

Next inspect prediction-powered inference and exact finite-population sampling
sources; derive/check small exact confidence sets and a valid stage scheduler.
Then compare strong ordinary unstratified/stratified sampling under the same
information, including identical kernels, and charge predictor preparation,
interval construction, failed acquisitions and exact evaluators. This is a new
constructive direction within C001, not a readiness or confirmation claim.

## 5. Strengthen the ordinary statistical control before implementation

The primary-source screen found finite-population rectification already in
PPI Corollary B.1 and simultaneous without-replacement confidence sets in
Waudby-Smith/Ramdas Theorem 2.1; see [source locators](sources.md). Use that
stronger sequential construction, not only Bonferroni stage intervals.

Here is the direct finite likelihood calculation for implementation. For a
fixed error count M, let L_s(M) be the likelihood of the ordered sampled error
prefix. Choose a data-independent full-support working mass pi(M), and put
Z_s=sum_M pi(M)L_s(M). At the true count M*, R_s=Z_s/L_s(M*) is a nonnegative
supermartingale: condition on the current history, sum next-step likelihoods
over outcomes possible under M*, and bound this by the sum over all outcomes.
The latter equals R_(s-1). The inequality handles boundary counts whose next
outcome is deterministic. R_0=1, so the maximal inequality gives

    Pr[there exists s with R_s >= 1/alpha] <= alpha.

Invert these tests and intersect over time. Coverage is over the sampling
lottery for fixed mathematical bits; pi is a working device, not a truth law.

For uniform pi on M=0,...,N, the mixture probability of a sampled error count
e is 1/(s+1). With hypergeometric mass

    H_M(e) = C(M,e)*C(N-M,s-e)/C(N,s),

the current confidence set is exactly H_M(e)>alpha/(s+1). Compare integers
after clearing alpha's denominator. No floating tail approximation is needed.
For fixed s,e, consecutive mass ratios are

    H_(M+1)(e)/H_M(e)
      = (M+1)*(N-M-s+e) / ((M+1-e)*(N-M)).

The mass increases until M+1 passes e*(N+1)/s, then decreases. Clip the mode
to [e,N-s+e] and find the two confidence endpoints by binary search. s=0
returns [0,N]; s=N returns [e,e]. This needs O(log N) membership calls, but
each exact binomial coefficient has a nonconstant, charged arithmetic cost.

Two stratum sequences at error levels alpha0+alpha1<=alpha can be queried in
any adaptive order while maintaining simultaneous validity. A positive working
beta-binomial mass centered on small error counts is another admissible
ordinary comparator; it needs its own exact mixture calculation and cost.

## 6. One-sided decisions can need only the adverse error stratum

If the predictor favors action A, false positives E1 can make that choice bad,
while false negatives E0 only help. Thus mu>=(N1-U1)/N can suffice without
sampling predicted zeros at all. A symmetric rule uses E0 to certify B.
This strengthens the acquisition target beyond recovering a two-sided mean.
It is ordinary decision-directed stratified sampling, not a new identity.

For zero observed errors, H_M(0)<=exp(-s*M/N_h). The uniform-working-mass
confidence criterion therefore implies

    U_h <= min(N_h, N_h*log((s+1)/alpha_h)/s).

This supports an approximately inverse-margin rather than inverse-squared-
margin sample requirement in a sufficiently accurate predictor regime. It is
conditional on the zero-error observation path; actual guarantees must include
the probability of other paths and the complete predictor/query/checker bill.
The exact hypergeometric endpoint, not this floating heuristic, will decide
the initial prototype's stopping event.

If the adverse stratum fails to support the proposed action, inspect the other
stratum or use an independently valid ordinary sampling fallback. Shared exact
receipts may be reused only without changing either lane's declared sampling
prefix. A full-cost dovetail can protect against slow guidance if every part
is resumable and scheduler overhead is charged; merely alternating query
counts does not protect against expensive predictor or confidence arithmetic.

## 7. Grouping usefulness is not prediction accuracy

The first synthetic probe found that completely inverted predictions can be
as useful as perfect predictions. This is explained by the representation:
the predictor supplies a partition; independently checked labels supply the
orientation. A globally inverted predictor gives exactly the same two groups
with exchanged names. Under coupled within-group random samples and a
label-symmetric confidence construction, its value intervals and query count
are unchanged. The particular seeded implementation uses seeds indexed by
group name, so this is a coupled-distribution statement, not an assertion that
every fixed seed has identical paths after renaming.

A perfectly accurate yet expensive predictor may be economically useless.
A systematically wrong but cheaply computed grouping may be useful. Moderate
errors can be worse than either endpoint because they increase within-group
heterogeneity. These are ordinary stratification consequences, now attached
to an explicit paid mathematical-query interface. They do not establish
accuracy-free improvement for arbitrary fallible models.

The 12 exposed fixtures have N=4096 and true positive frequencies near .52,
.55 and .65. Guided versus uniform queries were 256/4096, 128/1024 and 32/256
with perfect predictions; the fully inverted fixtures gave the same counts.
At 20% corruption, guidance used 3131/4096, 2446/1024 and 2048/256 queries.
Every realized action was correct. This finite outcome does not estimate the
failure probability or establish a realistic end-to-end resource benefit.
Exact small sampling-law enumeration checked 130 (N,M,alpha) cases, N<=10,
including binary-search agreement with all possible count parameters and
ever-exclusion probability at most alpha. The largest observed risk was 1/10
in the alpha=1/5 family, not a violation of the alpha=1/20 contract.

## 8. A symmetric working mixture removes a zero-error logarithmic penalty

Choose a full-support working count mass with weight rho/2 at each extreme
M=0,N and weight 1-rho spread uniformly over M=0,...,N, for 0<rho<1.
For s>0 its sampled-count mixture probability is

    q_s(e) = (1-rho)/(s+1) + (rho/2)*[e=0 or e=s].

The confidence criterion becomes H_M(e)>alpha*q_s(e), by the same direct
likelihood argument. On interior error paths this spends a constant factor
of the level; on the zero-error and all-error paths it has a fixed mixture
mass instead of 1/(s+1). The prior is a testing device, not an assertion that
errors arose from this law. It preserves full support and coverage for any
fixed error population. The extreme point masses are counted once each;
s=0 is handled separately because both extremes yield the empty prefix.

Let p=N1/N>1/2, delta=p-1/2, and suppose the predicted-one sample has zero
errors. For any M>=ceil(N*delta), H_M(0)<=exp(-s*M/N1). Therefore after

    s >= (N1 / ceil(N*delta))*log(1/(alpha1*rho/2))

all such M are excluded (unless full enumeration resolved the decision
earlier). The integer boundary can be tightened when an exact tie is allowed.
Thus perfect guidance has an inverse-margin sufficient query bound on this
path, without the uniform-mixture log(s) penalty. Deriving the condition is
constructive progress; it is not a new general confidence-sequence theorem.

## 9. Strengthen unguided decision testing too

Estimating a full mean interval is stronger than choosing between the two
actions. For testing a fixed count null M<=M0, compare the ordered-prefix
likelihood at an alternative M1>M0 with that at M0. While both are possible,
the ratio's next-step multiplier is larger on a one than a zero, and the
chance of a one under any M<=M0 is no greater than under M0 at that prefix.
Consequently the likelihood ratio is a nonnegative supermartingale under
the composite null. An alternative mixture also works. If the prefix has
more than M0 ones, the null is exactly impossible. If it has too many zeros
for M0, all larger alternatives are impossible too, and the ratio is set to
zero thereafter. Do not divide zero by zero or turn that case into rejection.

A predeclared mixture of alternatives above/below the action threshold can
provide two one-sided tests, splitting alpha. A frozen prediction average
may choose a single alternative without invalidating coverage: the truth
population and prediction array are fixed before the sampling lottery. This
would be an especially strong ordinary control on the perfect-prediction
fixtures. Adaptive alternatives chosen using observed sample labels need a
predictable-betting or restart argument; that extension is not yet supplied.

## 10. Explicit mathematical edits give a concrete next application

For a finite family of CNFs F_i, let y_i indicate satisfiability and define
y'_i for an explicitly specified edit T(F_i). These are deterministic
mathematical values. Sampling estimates the family-average edited value or
its difference from the base value; it does not learn the semantics of T.
For clause additions, y'_i<=y_i. Previously justified UNSAT instances need no
new solver call; only formerly SAT instances can change. For clause removals
the direction reverses. A checked old satisfying assignment may also answer
an added-clause request cheaply when it satisfies the new clause.

This suggests a practical integration: prior paid receipts provide a frozen
partition, monotonicity rules out one error direction, and uniform sampling
within the unresolved stratum buys edited truth until a value decision is
warranted. Lazy witness checking is charged on sampled instances; if it
fails, an ordinary exact solver supplies the label. Both statistical and
ordinary comparators receive the same prior receipts and may use identical
reuse rules. Pay the initial history explicitly when reporting amortization.
No claim about a counterlogical inconsistent antecedent follows from an
ordinary executable CNF edit.

## 11. Stronger-control developmental result

[sampling02.json](sampling02.json) preserves a distinct implementation and
source closure. Exact checks covered 108 (N,M,alpha) mixture-count cases and
188 composite-null/alternative/level cases, N<=9. The direct ordinary test
used the frozen prediction margin to choose its alternative, with its full
prediction scan charged. On the three perfect/inverted fixtures it used
2048,512,256 labels; the extreme-mixture guided rule used 128,64,32. At 20%
corruption the latter used 4096,2446,2048 and lost decisively. Every realized
decision was correct. These are exposed developmental fixtures, not a
reliability estimate or independent confirmation.

Controller timings were sub-millisecond to several milliseconds and can
matter for cheap evaluators. For example, at true mean near .65 with perfect
guidance, the direct rule took about .164 ms and guidance about .264 ms:
saving 224 labels would offset that observed .100 ms controller gap only
when their average marginal evaluation price exceeds about .45 microseconds,
before any unmeasured prediction inference/preparation. This illustrative
break-even uses one noisy run; it is not a stable cost estimate. The next
application must measure real solver work rather than assign a favorable
label price after seeing these outcomes.
