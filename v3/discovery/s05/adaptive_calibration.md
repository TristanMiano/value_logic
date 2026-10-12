# Adaptive paid calibration from shared vertex receipts

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; constructive protocol variants. Readiness unassessed.
This broadens the [session](session.md) portfolio beyond the T-join closure.
The principal owns the clock; overlapping agent work adds no research credit.

## Common interface

Start with a fixed cohort of N task identities and deterministic vertex labels
`x_v(i) in {0,1}`, or an iid task source with a fixed label-generating rule.
A receipt fixes one label at a specific source/task/vertex version. Its proof
must be checked. An unfinished computation supplies no label and retains its
paid cost. A source feature h is a fixed bounded function of specified labels;
pair disagreement `Y_uv(i)=x_u(i) XOR x_v(i)` is the first useful library.
Its source mean is `mu_h`. Do not alter the feature after seeing its labels.

Register a finite or countable feature library and positive weights w_h with
`sum_h w_h <= 1`. For m known vertices, all pairs can receive equal weight.
Unqueried pairs need not be evaluated or explicitly materialized. This prior
coverage permits requesting a pair later without inventing a new statistical
event. Arbitrary parity masks can also be covered prospectively, for example
by allocating equal total weight to each support size and then equally among
its masks; their observation cost still grows with the support.

Every partially evaluated occurrence has sound endpoints
`0 <= l_h <= Y_h <= u_h <= 1`. Missing labels initially give [0,1]. A checked
receipt may tighten many occurrences and features; retain each original task
draw and its multiplicity. Known receipts can be reused without rerunning
their production, while lookup/checking/update costs remain payable.

## Variant A: exact cohort envelopes

For a fixed finite cohort, keep endpoints for every task, including [0,1]
for tasks never selected. Then

```text
sum_i l_h(i)/N <= mu_h <= sum_i u_h(i)/N.
```

This deterministic guarantee tolerates any adaptive allocation, arbitrary
stopping and later feature requests. No sampling assumption or risk budget is
needed. Store only nontrivial endpoints and their sums. It is inexpensive when
a small cohort or heavily reused receipt cache becomes substantially resolved;
it is usually wide when only a small fraction of the cohort is known.

## Variant B: select the vertex batch before drawing the task

**Recommended first implementation.** At round t:

1. From previous evidence, choose a vertex batch V_t and computation budgets.
   Commit that choice before drawing the next task identity.
2. Draw I_t uniformly with replacement from the cohort, or draw a fresh iid
   task. Save the batch/draw row before starting checks.
3. For each feature with support contained in V_t, that row contributes one
   occurrence to its audit stream. Attempt the checks, retaining unresolved
   endpoints; the occurrence remains even after timeouts or interruption.
4. Reuse receipts to refine all supported endpoints. Choose the next batch
   using current uncertainty, expected downstream use and measured costs.

Let n_h be the number of selected occurrences, not completed evaluations.
Because selection precedes the fresh task draw, each latent exact value in
that feature's selected stream has conditional mean mu_h. Adaptive allocation
changes how quickly a feature is sampled, not the sampling law within its
stream. No propensity correction is required. For `n >= 1`, define

```text
e(h,n) = sqrt(log(2*n*(n+1)/(alpha*w_h)) / (2*n)).
L_h    = max(0, mean_of_current_lower_endpoints - e(h,n_h)).
U_h    = min(1, mean_of_current_upper_endpoints + e(h,n_h)).
```

At every feature/sample-count pair, conditional Hoeffding bounds each tail
with allowance `alpha*w_h/(2*n*(n+1))`. Summing both tails over n and h gives
total failure probability at most alpha. On that single event, the latent
full-value sample means satisfy the bounds for every n. Endpoint domination
then covers every sound delayed refinement, regardless of when it occurs.
The intersection of previously issued and updated intervals remains valid.
The [source note](sources.md) records the primary bounded-mean and sequential
methods; this explicit risk-spending formula is an elementary specialization.

This permits batches targeted to previously difficult pairs and new requests
from the covered library. Stored batches determine which old draws were
eligible for each feature even if its statistics are computed only later.
To keep this simple warrant, do not add old draws merely because their task
identities happen to have enough cached labels: eligibility is determined by
the vertex batch selected before that draw. Those other cached labels still
help Variant A and future selected occurrences.

A batch of three vertices can support all three pair features for one set of
vertex computations. A strong direct-policy comparator receives the same
receipts and can exploit the same sharing. The benefit to investigate is
adaptive evidence acquisition and broader subsequent reuse, not exclusive
ownership of that elementary sharing rule.

## Variant C: choose after seeing current context, with known inclusion

If current task metadata materially improves allocation, draw the task first.
Before observing any new labels, sample a vertex batch from a recorded design.
For each feature h, let A_h indicate that its required labels are either
already cached or selected. Record its exact conditional joint inclusion
probability q_h, with a prospective bound `q_h >= q_min,h > 0` for all tasks
and rounds. A feature already known from the cache may have q_h=1. Use the
joint probability, not a product of marginal vertex probabilities unless the
selection design makes that product correct.

For a latent complete label, the estimator

```text
Z_h = A_h*Y_h/q_h
```

has conditional expectation Y_h given the task and prior state, hence mu_h
before the fresh task draw. Its range is [0,1/q_min,h]. Partial checks give
`Z_h^- = A_h*l_h/q_h` and `Z_h^+ = A_h*u_h/q_h`. Use the same anytime formula
as Variant B on the global round count t, replacing its radius by
`e(h,t)/q_min,h`. Average the lower and upper Z endpoints, then clip the final
mean interval to [0,1]. A selected audit that times out stays an interval;
q_h describes selection, not successful completion.

A bounded forecast b_h chosen before unseen labels gives the usual alternative
`Z_h=b_h+A_h*(Y_h-b_h)/q_h`. It remains conditionally unbiased. With b_h in
[0,1], a uniform range is `[1-1/q_min,h, 1/q_min,h]`; a simple Hoeffding
radius therefore scales by `2/q_min,h-1`. Forecasts can help a variance-sensitive
bound, as in Howard et al., but do not automatically improve this conservative
range bound. Preserve original A, q and b for each occurrence. Later receipts
can refine its endpoints; they cannot retroactively change its sampling design.

This generality has a real price. For constant inclusion q and homogeneous
label costs, the simple no-forecast range bound needs approximately 1/q^2
as many rounds for a fixed precision, paying approximately 1/q times as many
audits as full sampling. Variant C therefore needs useful context selection,
heterogeneous costs, a sharper variance-sensitive bound, or another concrete
reason to beat Variant B. Do not make inverse weighting the default solely
because it supports a broader policy class.

## New features, queries and source revisions

- **New value/query from existing intervals:** checked consequences hold on
  the same event. Later prices, stakes or parity targets incur computation
  cost but no new sampling risk when their derivation uses only that event.
- **New request for a precovered feature:** reconstruct its eligible stream
  from retained rows and receipts. Keep its original w_h, target and designs.
- **Genuinely new feature or learned predictor:** bind its definition now,
  allocate a fresh allowance, and begin independent future task draws for its
  calibration. An allowance sequence `alpha_new/2^j` for the j-th admission
  gives conditional coverage and total additional risk at most alpha_new.
  Data that selected the feature may train a proposal; it is not fresh
  confirmation. Variant A's exact cohort endpoints remain available.
- **Changed source/label semantics:** create a new source identity. A new
  allocation on the same source is different from a changed estimand.

These are calibration-allocation guarantees. They do not turn S25's fixed
deployment query-set guarantee into a guarantee for query choices conditioned
on newly observed deployment labels.

## Minimal records and next constructive move

Record the source and feature versions, library/risk weights, batch-selection
order, task draws, batch/budget choices, raw receipts and unresolved attempts.
Variant C additionally needs the selection-design version, q values, q floors
and any forecasts. Preserve sample occurrence counts separately from distinct
paid receipts. Charge proposal, primitive execution, proof checking, cache
lookup, confidence update and downstream answering costs once each.

Start with Variant B plus Variant A as an inexpensive deterministic bound.
Use a small shared vertex source, changing the batch allocation as requested
pairs change. Compare with a receipt-sharing fixed-policy bank and uniform
batches. Introduce informative timeouts and later receipt completions to check
the interface. Develop Variant C only when the experiment identifies useful
current-context information that the simpler ordering cannot exploit.
All those probes remain revisable development; no single closure is frozen.
