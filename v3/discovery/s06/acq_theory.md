# Acquire evidence for the repair certificate that matters

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026 UTC.
DEVELOPMENT; same-model auxiliary derivation for the principal's s06 increment.
No auxiliary time is added to the principal clock. This extends
[calibrated repair](../s05/calibrated_repair.md), not its readiness status.
The principal owns the integrated implementation; the small arithmetic checks
here are separate and make no solver-performance claim.

## 1. Audits shrink the source; proofs enlarge an action's certificate region

Let `W` be a nonempty common warranted set of nonnegative penalty vectors.
Let `u` be a checked feasible violation vector. An admitted proof P has
supports `v_l` with `L_P(w)=min_l v_l dot w <= C*(w)` for every admitted w.
Replacement costs p. Write `h_W(c)=sup_(w in W) c dot w`.

For this fixed repair and proof, a valid uniform regret bound is

```text
G(u,P,W) = max(0, h_W(u)-p, max_l h_W(u-v_l)).
G(replace,P,W) = max(0, max_l [p+h_W(-v_l)]).
```

Indeed, `C*(w)>=L_P(w)`, so comparison with the best repair or replacement
is bounded by comparison with every support and with p. Hence the certificate
region for repair u is

```text
R_tau(u,P) = {w>=0 : u dot w-p<=tau,
                      (u-v_l) dot w<=tau for every l}.
```

Admission is the concrete containment query `W subseteq R_tau(u,P)`.
Cost receipts shrink W. A pointwise stronger checked lower proof enlarges R;
a new witness offers a different R. Retaining old witnesses, proofs and valid
source constraints keeps the best available bound nonincreasing under sound
refinement. An empty source set is a conflict to investigate, not a certificate.

With several independent valid lower proofs, taking the best complete bound
`min_P G(u,P,W)` is safe. It need not equal the stronger bound obtained by using
the pointwise envelope `max_P L_P(w)` inside the support optimization. The latter
must be computed and checked at its actual additional cost.

Two cheap blockers guide purchases without an outcome prior:

* **Cost ambiguity for a fixed action.** If an admitted feasible competitor v
  has `h_W(u-v)>tau`, some plausible w makes u worse than v by more than tau.
  No stronger lower proof can certify this same u over unchanged W. Audit or
  choose another action. This does not rule out an undiscovered third action.
* **Proof insufficiency for a fixed pair.** If one certificate contrast has
  `inf_W (u-v_l) dot w>tau`, every nonempty subset of W still fails that
  particular inequality. Audit alone cannot certify the unchanged `(u,P)`.
  Strengthen its proof or choose another witness/proof. The same statement
  applies to the absolute-cost comparison `u dot w-p`.

These are complementary directional statements, not universal prescriptions
to alternate audit and search. Candidate-level changes can evade either
fixed-pair obstruction.

## 2. A finite cohort supplies an exact adaptive observation contract

For the first integrated example, declare N persistent cost rows with fixed
features `Z_i` and target the **cohort mean** `w=(1/N)*sum_i Z_i`. Each row has
a known bounded nonempty feasible set `Q_i` containing its unobserved features.
An audit returns a source-bound exact value, or a checked interval/linear
constraint, and intersects Q_i with that receipt. All untouched entries remain
in Q_i. Audit selection may depend arbitrarily on earlier evidence.

When the only cross-row constraints are these row sets, retain

```text
W = (Q_1 + ... + Q_N)/N,
h_W(c) = (1/N)*sum_i h_Q_i(c).
```

The equality follows by independent maximization over the Cartesian product
of row sets. It does not assume the physical rows were generated independently.
For bounded closed polytopes the maxima are attained; with other sets use sup.
If there are genuine cross-row constraints, keeping them can tighten W; dropping
them is a safe relaxation whose support may be looser.

A cell audit, full-vector audit, or direct contrast audit is allowed only if
that observable is actually supplied by the declared paid interface. For
example, measuring `c dot Z_i` is not free because the controller requested c.
Exact row receipts support later adaptively selected contrasts without a new
statistical allowance. Source identity, cohort membership, feature meanings,
measurement precision, and the mapping of violations to these costs remain
part of the contract. This certifies this cohort's mean, with no population
generalization or hidden iid assumption.

This representation can preserve dependencies a coordinate box loses. If a
known row contract is `Z_i=(b_i+d_i,b_i)` and an audit reveals d_i, its contribution
to `h_W((1,-1))` is exactly d_i even when b_i remains unknown. Estimating both
absolute costs may still be necessary for comparison with replacement.
Conversely, if every Q_i already makes a requested contrast constant, no
remaining audit of these rows can improve that contrast's source interval.

## 3. A population extension with a separate optional-stopping warrant

This section is a future interface, not the s06 finite-cohort experiment.
Suppose latent full vectors `Z_1,Z_2,...` are iid under one declared source,
`0<=Z_ij<=B_j`, and `w_j=E Z_ij`. Record each draw before selective inspection.
Retain intervals `l_ij<=Z_ij<=u_ij` for every occurrence, including unresolved
ones. At n draws let

```text
r_j(n) = B_j*sqrt(log(2*m*n*(n+1)/alpha)/(2*n)),
W_n = product_j [mean_i l_ij-r_j(n), mean_i u_ij+r_j(n)]
                      intersect product_j [0,B_j].
```

The bounded-sum exponential estimate gives a failure allowance
`alpha/[m*n*(n+1)]` per coordinate and sample count. Summing over coordinates
and n gives alpha. Pathwise, the latent sample mean lies between the two
partial-observation means. Consequently, with probability at least `1-alpha`,
every W_n contains w, at every subsequent adaptive refinement of those draws.
Intersect retained W_n sets to preserve monotonicity. No independence between
the feature coordinates is required.

The source premise must survive the sampling policy. Revealing cheap cells
only is compatible with retaining all unresolved cells in the denominator;
retrospectively treating only the cheaply resolved cells as iid is not.
Refining old draws changes their censoring ranges, not the statistical radius.
All later data-selected proof contrasts can query this common W. A newly
selected scalar contrast cannot instead borrow an individually fixed-query
bound without an appropriate fresh or uniform construction.

**Primary source actually read:** Howard, Ramdas, McAuliffe and Sekhon,
[Time-uniform, nonparametric, nonasymptotic confidence sequences,
arXiv:1810.08240v9](https://arxiv.org/pdf/1810.08240v9), Section 1 equation (1)
and properties P1-P4, PDF pp. 1-2; Section 2, PDF pp. 4-5; Appendix J Table 3,
PDF p. 47, bounded-increment Hoeffding I row. The paper supplies the common
time coverage framework and bounded-increment moment premise. The elementary
coordinate/time union and partial-observation wrapper above are derived here;
they do not claim the paper's sharper stitched or mixture widths. An attempted
full-text retrieval of Hoeffding's 1963 original through the RPI copy timed out;
it is not recorded as read.

## 4. Guaranteed purchase gain needs complete outcomes and a complete bill

Let `B(D)` be the minimum valid bound among currently admitted output actions
and proof options, where D includes source constraints. A purchase q with
possible checked outcomes O_q has local guaranteed certificate improvement

```text
Delta_min(q,D) = B(D) - sup_(o in O_q) B(D plus o).
```

For monotone retained evidence this is nonnegative. If a warranted quote
`c_max(q,D)>0` bounds the whole purchase, `Delta_min/c_max` is a concrete
local benefit-per-bounded-expenditure score. It does not prove greedy
optimality. Charge receipt acquisition, checking, objective compilation,
source updates, support queries and prospective outcome evaluation. Measured
CPU/wall time and any operation tariff remain distinct.

Include a no-progress timeout whenever the provider cap permits it. Such an
outcome makes the one-purchase guaranteed gain zero. Removing that outcome
requires a genuinely complete-answer contract or proved terminating cost bound,
not an optimal-status flag or an empirical success rate. An expected score
instead needs a justified conditional distribution of outcomes and costs.
W constrains mean penalty values; it does not supply a solver-runtime law or
the conditional law of the next audit. A heuristic may choose among zero-score
options, but its proposed benefit must be labeled as heuristic.

For small complete-query menus, a finite decision-tree recursion can price
complementary bundles: terminal states satisfy `B(D)<=tau`; otherwise choose
q minimizing `c(q,D)+max_o T(D plus o)`. The state must include retained solver
state whenever it affects future quotes. Cycles/no-progress outcomes cannot
be discarded to create a finite guarantee. This is conventional minimax
decision-tree planning, adapted to the joined certificate state.

## 5. Singleton scores can miss a useful audit-and-proof bundle

Consider a source whose minimal feasible violation vectors are `(1,0)` and
`(0,1)`, W initially `[0,1]^2`, and replacement p=2. Both witnesses are already
admitted. The initial valid lower receipt is only `L_0=0`, so `B=1`.
There are two complete purchases, each with its own fully billed quote:

1. Audit the second cost, revealing `w_2=y in [0,1]`, leaving `w_1 in [0,1]`.
2. Buy a checked logical proof establishing `L_1(w)=min(w_1,w_2)`.

The audit alone yields `B=y`, whose worst outcome is 1. The proof alone also
leaves `B=1`. Both singleton guaranteed gains are zero. Together, however,

```text
B_fixed(y) = min(y,1-y) <= 1/2.
```

Thus the two-purchase bundle guarantees a fixed action within tolerance 1/2
even though neither singleton scores positively. This statement charges both
complete purchases and assumes their actual receipt interfaces; it is not a
runtime prediction for arbitrary MaxSAT instances.

If the requested output permits randomization with **expected-action** regret,
let q be the probability of returning witness `(1,0)`. The contrast between
the two actions lies in `[-y,1-y]`, giving

```text
B_mix(q,y) = max(q*(1-y), (1-q)*y).
q*=y,                 B_mix*=y*(1-y) <= 1/4.
```

Both realized witnesses remain feasible. This guarantee concerns expected
loss over the service's randomization, not every realized action. More
generally, for action contrast `[l,u]` with `l<0<u`, the minimax mixture uses
`q=-l/(u-l)` and has bound `-l*u/(u-l)`. Conventional controls receive these
same mixtures when this is the output duty. This may reduce the paid precision
required, but no empirical acquisition advantage is established.

## 6. Improve a bounded-call quote before paying for that call

This section joins the principal's lower-endpoint bounded-query construction.
Use an integer-scaled objective `q=lo` and source box `lo<=w<=hi`. A checked
SAT answer to `q dot z<=b` gives a feasible Boolean z. The coarse uniform cost
quote `b+sum_j(hi_j-lo_j)` can be tightened without enumerating logical models:

```text
H_b = max { hi dot z : z in {0,1}^m, lo dot z<=b },
H_b <= F_b(lambda)
     = lambda*b + sum_j max(0,hi_j-lambda*lo_j),  lambda>=0.
```

For every coordinate, `hi_j*z_j <= lambda*lo_j*z_j+
max(0,hi_j-lambda*lo_j)`. Sum and apply the budget. Any evaluated nonnegative
lambda gives a certified upper bound; minimizing at the finite breakpoints
`hi_j/lo_j` and zero yields the usual fractional-knapsack relaxation. Terms
with zero lo remain in the sum. Take the minimum with the coarse bound and
other already warranted quotes. Pay for this calculation. It enumerates a
relaxed objective set, not the feasible repair source or a diagnostic optimum.

A stronger signed version uses the actual retained proof supports. For a
Boolean support v, box support of the new witness contrast is

```text
max_W (z-v) dot w
 = sum_j z_j*(lo_j if v_j=1 else hi_j) - v dot lo.
```

Maximize this expression over `lo dot z<=b`, use its knapsack/dual upper
bound, and take the maximum over the proof's leaves. Combine with `H_b-p`
and zero. This bounds every possible SAT witness's full certificate regret
under that proof. Taking the minimum over independently valid proof options
is safe. Cap the resulting post-purchase bound by the current B, since old
outputs remain available. This proof-compatible version was independently
derived by the principal and communicated during s06; it is included here to
keep the cheaper fractional relaxation and the integrated quote reconstructable.

The UNSAT side requires a genuinely checked negative receipt. For integer q,
it proves `q dot z>=b+1` for every feasible z, and since `w>=q`, supplies that
uniform scalar lower bound over W. An unverified backend status contributes
no such lower receipt. Native warm-state reuse and this independent proof
bridge remain distinct capabilities.

One further constructive option is to query an interior objective q. Uniform
coarse margins become `A(q)=sum(hi-q)_+` on a SAT answer and
`D(q)=sum(q-lo)_+` on a negative answer: the respective cost and lower bounds
are `b+A(q)` and `b+1-D(q)`. This trades the two outcome qualities explicitly.
Exact rational/integer scaling and every objective update must be checked and
charged. It is an alternative for a later recurrence, not implemented here.

## 7. Small reconstruction checks and disposition

Run `python v3/discovery/s06/acq_theory_checks.py` from the repository root.
[The saved results](acq_theory_results.json) verify the two-action formulas on
nine exact rational audit outcomes, the common-source support calculation,
and one three-feature knapsack/dual example, including zero lower weight.
The code checks all eight Boolean vectors of that objective-only example.
It never calls a repair provider or uses a source optimum to choose a gate.
The general guarantees are the arguments above; this finite check is only a
cheap arithmetic reconstruction.

The most useful next construction is the principal's source-bound finite
cohort controller with both audit and checked bounded logical purchases.
Retain the signed-support quotation, complementary bundle, partially observed
population and permitted-mixture alternatives. No claim is made that these
standard robust/statistical ingredients are novel individually, that the
controller economically dominates equally informed robust optimization, or
that P3-POS01 has been verified. S26-S28 stay in DEVELOPMENT; readiness remains
unassessed.
