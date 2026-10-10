# Independent reconstruction of the live-hard performance lemma

Contributor: **ChatGPT (GPT-6 Astra Pro)**, integration-review sub-agent,
October 10, 2026 UTC. Task **P3-08**, **DEVELOPMENT**.

**Disposition: ACCEPT the captured mathematical statement under its explicit
premises.** This is an independent reconstruction by another instance of the
same model, with the author's derivation visible: **same-model, nonblind**.
It is not an external review, a final evaluation, or a contribution gate.
Agent time and resource use are unmeasured. Principal-clock and historical
research credit from this review are both **zero**.

## 1. Source binding and the resolved objection

The exact reviewed sources are retained under
`live_performance_review/source_snapshot/`; the complete manifest is
`live_performance_review/plan.json`. The load-bearing hashes are:

| Source path, relative to repository | SHA-256 |
|---|---|
| `v3/derivations/08_live_hard_performance.md` | `82108d6b9b70b8c3cadcb667dbcf16b1528396029177d39e6699c32fefb02db5` |
| `v3/derivations/07_observable_performance.md` | `178ed397b699c06da1056e0e660dd6e35c498def127dc6b54d4dc876e44f7a8f` |
| `v3/derivations/07_selective_feedback.md` | `b8b79d95fcfde60f749fc4e872e38ae20d608a786462002660b97658597103cd` |
| `v3/experiments/p308_reporting.py` | `33ecde23b45ca9696da44ffb925797b52dc450d141e16b79fa17ec937fdb347d` |
| `v3/experiments/p308_broker.py` | `399080c950a48c1cd935efbee8ed7769a7af54b7afa14859b5671397638e2e4d` |
| `v3/RESEARCH_PROTOCOL.md` | `ef57593ce23cbe06b1683fc3609526f700b6ab5c395befacbbcd01bd48f3aa52` |

An earlier, uncaptured working wording required all-path funding for the
expectation claim while displaying an unconditional confidence statement
after selecting successful episodes. I raised this as a substantive funding
objection. The author corrected sections 2 and 5 before this source snapshot.
The captured version explicitly requires all-path completion and funding,
including reporting, for both statements and denies 95% coverage conditional
on selectively successful completion. That objection is resolved. I do not
assign a fabricated hash or an execution result to the earlier wording.

## 2. Reconstruct the processes before manipulating the estimates

Fix the inherited exogenous binary query tape and the declared finite
contract, with one owned positive-propensity selector per block. Given the
preceding selected answers, all base forecasts in the next block are
mathematically fixed. A sequential implementation need not have computed
them all before selection; the proof needs their mathematical dependence,
while the deployment must pay when computing and retaining them.

The live service retains the base forecast and uses the same action draw at
every position, including positions whose answer it already knows. Selected
terminal actions are corrected by a current checked receipt in both services.
The selected receipt still enters the base update at the same block boundary.
Thus hard correction cannot change later base weights, selector probabilities,
label purchases, or the partition of supplied randomness.

Let H_t mean that a sound warrant for the complete current semantic key
existed **before** the live forecast at t. The time qualifier matters twice:
an early purchase may make H one for a later position in the same block, and
the purchase at t cannot rewrite the already issued forecast at t. The current
scope and generation must remain valid. Pending, conflicted and stale warrants
do not satisfy H_t. Withdrawal ends the epoch and removes current authority
to present an incomplete or invalidated episode as successful.

These premises imply q'_t=y_t for H_t=1 and q'_t=q_t otherwise. They do not
make the complete live vector predictable before the current selector.

## 3. Exact loss reduction is the additional information

Write d_t=q_t+(1-2q_t)y_t and g_t=(q_t-y_t)^2. On H_t=1, the live forecast
has Brier loss zero. On an unselected H_t=1 position, the live action has
error probability zero and the shared draw turns any base prospective error
into zero. On a selected position, both terminal actions were already
corrected, so there is no terminal reduction to count there.

The three exact observable reductions are therefore

```math
\Delta_F=\sum_{H_t=1}g_t,\qquad
\Delta_V=\sum_{t\notin\{J_k\},\ H_t=1}d_t,\qquad
\Delta_Z=\sum_{t\notin\{J_k\},\ H_t=1}\mathbf1\{a_t^0\ne y_t\}.
```

The retained prior checked answer supplies y on every summand. No missing
unselected label is required. In particular, Delta_Z uses the retained base
action, not a newly drawn counterfactual action. Exhausting the selected,
unselected, hard and unresolved cases gives

```math
F_1=F_0-\Delta_F,\qquad V_1=V_0-\Delta_V,\qquad Z_1=Z_0-\Delta_Z.
```

These are equalities on every admitted complete path. They are stronger than
pointwise domination. If L<=X<=U holds on some event and X'=X-Delta exactly,
then L-Delta<=X'<=U-Delta holds on the identical event. Delta may depend on the
selector, X and the interval itself. No independence argument is needed for
this elementary translation. The historical restriction on transferring a
lower bound by domination alone remains correct.

## 4. The residual is retained rather than re-proved for the live mask

For the base process the inherited identity is

```math
V_0-U_c=F_0-A_c
=\sum_k\left(\sum_t r_{kt}-r_{kJ_k}/\pi_{kJ_k}\right),
\qquad r_t=d_t-1/2.
```

Subtract Delta_V from U_c and Delta_F from A_c. Direct cancellation yields

```math
V_1-(U_c-\Delta_V)=V_0-U_c
=F_0-A_c=F_1-(A_c-\Delta_F).
```

Consequently the conditional centered moment proof applies to exactly the
same residual it bounded before correction. The block widths must remain
the base widths C_k=max_t |1-2q_t|/pi_kt, and Q remains their squared sum.
The construction does not claim a new zero-mean residual after inserting a
selection-dependent live mask into the old formula.

For either sign and the fixed rate lambda=8/R, the base conditional moment
process bounds failure of

```math
|V_0-U_c|\le Q/R+5R/8
```

by two tails of at most exp(-5), each less than 1/80. The same event controls
F_0-A_c because the residuals are identical. The fact that predictable Q may
be random is handled by the fixed-rate exponential argument; the rate is not
optimized after observing Q. No additional error allowance is spent merely
to translate the event.

## 5. A random unresolved-action count is permitted here

Condition on the **complete action-independent selector and hard-state
history**. In this construction that means the history generated by the
fixed public tape, selectors, selected checked answers, and the consequent
base updates and hard state. It excludes conditioning on sampled terminal
actions or an action-dependent success filter. The fixed disjoint bit
schedule and the stated fresh fair-bit premise leave all action draws
independent of this history.

Under that conditioning, n_1 and the surviving live forecast probabilities
are fixed. The remaining n_1 error indicators are independent Bernoulli
variables whose mean sums to V_1. For n_1>0, the two-tail bounded-moment bound
at radius r_1 gives

```math
\Pr(|Z_1-V_1|>r_1\mid\mathcal G)
\le2\exp(-2r_1^2/n_1)
\le2\exp(-5)<1/40,
```

because r_1=ceil(sqrt(ceil(5n_1/2))) has r_1^2>=5n_1/2. If n_1=0, the error
is identically zero. The bound holds for every conditioning history, so
taking expectation over that history preserves it when n_1 varies. No
independence between this action event and the base sampling event is
asserted or needed: their union bound costs at most 1/20.

On their intersection, the triangle inequality gives the proposed terminal
radius rho+r_1 about U_c-Delta_V. Both F and V use radius rho. This proves
the displayed simultaneous 19/20 fixed-end statement. It does not make the
complete terminal statement anytime. It does not give joint coverage across
several policies, selected rates, epochs or development arms.

The chosen report combines the translated base sampling event with this
single live action event. A separate translated base-Z interval could also
be valid, but taking a favorable endpoint from independently allocated action
bounds would require a new joint allocation. The captured proposal explicitly
avoids that operation.

## 6. Deterministic intersections and the exact exception

For unresolved unselected positions, min(q,1-q) and max(q,1-q) bound the
conditional error probability. The binary Brier minima and maxima give the
forecast envelope; prior hard forecasts contribute zero and selected issued
forecasts are scored exactly using their purchased label. The terminal count
lies in [0,n_1]. Intersecting with these deterministic statements preserves
the confidence event. An empty intersection must remain a recorded conflict,
not be silently removed or treated as a favorable interval.

If n_1=0, every unselected live forecast was already hard-known before issue.
Its forecast loss is zero and its terminal action is correct. Every remaining
position is selected, and its receipt reveals the exact loss of its immutable
issued forecast. Thus V_1=Z_1=0 and F_1 is exactly observed. F_1 need not be
zero: a just-purchased position can still have issued a fallible forecast.
These exact assertions do not require stochastic coverage, although the
source's funding and identity checks still govern whether the calculation
can be completed and exported.

Adding the observed, fully paid bill to c times the terminal interval is a
pathwise transformation for c>=0. The bill can correlate with the selector;
it must be the same episode's bill and must include reporting and source
procurement when those services are deployed. The result does not estimate
the future bill of a changed purchase policy.

## 7. The B=2 separator remains decisive and is now resolved correctly

For a repeated false query with q=(1/4,1/4), J=1 yields live q=(1/4,0),
Delta_V=1/4, Delta_F=1/16, V_1=0 and F_1=1/16. J=2 yields no correction,
V_1=1/4 and F_1=1/8. Base centers U_c=1/4 and A_c=1/8 have zero residual in
both cases, so the translated centers equal the live targets in both cases.

The earlier failures remain: direct constant-half recomputation on the live
vector has mean V residual -1/8; the selection-dependent hard-mask center
has mean residual +1/8. Neither failure threatens the translated-base proof.
The translation succeeds because its exact deltas preserve the base
residual, not because those failed martingale claims become true.

## 8. Acceptance scope

The captured correction-translation result is sound. Its genuinely new
integration premise is retaining enough immutable, chronologically warranted
information to observe the exact loss reduction while preserving the entire
base sampling process. It neither changes the historical P3-07 theorem nor
licenses lower-bound transfer from an upper-only domination statement.

The funding wording objection was material and has been repaired. I found
no further mathematical flaw in the captured revision. Implementation
agreement, tariff adequacy and input-boundary checks are separately recorded
in the companion broker and reporting reviews. Deterministic finite checks
can verify those formulas and paths; they cannot establish frequentist
coverage from development seeds or satisfy a final-evaluation gate.
