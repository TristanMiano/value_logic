# Buying useful value precision from partial proof receipts

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; constructive acquisition rules for the [session](session.md).
The principal owns the clock. These are derivations and candidate interfaces,
not a new confirmation run or an assertion of optimal CNF expenditure.

## 1. Separate what another proof can change from what another draw can change

Use the fixed ordered source in [threshold calibration](threshold_calibration.md):
`H in {0,...,M}`, with a checked interval `I_i=[l_i,u_i]` for each sampled
physical row. There are n iid draw occurrences. Distinct row i has multiplicity
`m_i`, with `sum_i m_i=n`; repeat occurrences share proof receipts but retain
their statistical multiplicity. All unresolved draws remain recorded.

For a requested bounded payoff or paired contrast g, define

```text
a_i(g) = min_(h in I_i) g(h).
b_i(g) = max_(h in I_i) g(h).
r_i(g) = b_i(g)-a_i(g).
V(g)   = sum_(j=0..M-1) |g(j+1)-g(j)|.
```

V is discrete total variation, not variance. The telescoping identity in
[threshold values](threshold_values.md) shows that, on the common event
`sup_j |F(j)-G_n(j)| <= epsilon_n`,

```text
|E g(H) - (1/n)*sum_i m_i*g(H_i)| <= epsilon_n*V(g).
```

The statistical input is the DKW inequality; its primary source and the
pathwise justification for adaptively refined intervals are recorded in
[the calibration note](threshold_calibration.md). See also
[Reeve, primary author paper, pp. 1–3](https://arxiv.org/pdf/2403.16651v1).
The following allocation algebra is a consequence of that event, rather than
an additional imported statistical theorem.

Before clipping to the range of g, a warranted interval is

```text
[(1/n)*sum_i m_i*a_i - epsilon_n*V,
 (1/n)*sum_i m_i*b_i + epsilon_n*V].

W_n(g) = C_n(g) + S_n(g),
C_n(g) = (1/n)*sum_i m_i*r_i(g),
S_n(g) = 2*epsilon_n*V(g).
```

This is an exact decomposition of **this constructed interval's width**.
C is its censoring contribution; S is its sampling contribution. Neither is
asserted to be a universal lower bound on attainable uncertainty. Clipping,
the [compatible CDF oracle](threshold_queries.py), and a stronger source that
retains row-allocation constraints can all yield a narrower answer.

At fixed n, additional receipts only reduce C in this formula. They do not
change epsilon or V. In particular, when every `r_i(g)=0`, the existing rows
already determine the empirical mean of this g. Finding their exact H values
has zero remaining value for this certificate. For arbitrary nonmonotone g,
this does not claim that every stronger uncertainty-set oracle is also
unchanged: it may use where mass can lie within equal-payoff regions.

## 2. A complete-query score with an explicit cost scope

For a genuinely unresolved threshold query `l_i <= j < u_i`, the nominal
checked outcomes give

```text
I_i^- = [l_i,j]       if H_i <= j,
I_i^+ = [j+1,u_i]     if H_i > j.
r_i^- = oscillation of g on I_i^-;
r_i^+ = oscillation of g on I_i^+.
```

Every complete answer reduces the preclipped certificate width by at least

```text
Delta_min(i,j;g) = (m_i/n)*(r_i - max(r_i^-,r_i^+)).
```

The best possible reduction is obtained by replacing max with min. A checked
SAT witness that saturates farther along the chain can narrow its child
interval further, so the nominal complete-answer bound remains conservative.
Multiplicity matters: one proof about a repeatedly drawn physical row improves
every occurrence, and is paid for once.

If the **entire complete-answer action** has a warranted cost bound `c_ij>0`,
`Delta_min/c_ij` is a local guaranteed width improvement per bounded expenditure.
It is useful for ranking concrete options. It is not a proof that repeatedly
taking the largest ratio minimizes total acquisition cost.

The cost scope is substantive. A known complete-answer tariff, or a sound
uniform bound for a specified terminating procedure, can supply c. An ordinary
solver cap that can expire without an answer cannot: if unchanged I is a
possible outcome, the worst-case width improvement is zero. Such a capped
probe may still be a good exploratory purchase, but an expected-gain score
needs a justified outcome/cost model or must be labeled a proposal. Timeout
does not create a label.

Charge provider execution, receipt checking, witness extension, cache and
source-identity checks, confidence updates, and the acquisition calculation.
The actual invoice need not be a function of H. The same-H cost variation in
[the CNF findings](threshold_cnf_findings.md) remains relevant even when truth
transport can be represented by a small interval/frontier state.

## 3. Avoid discarding useful bundles because their first probe scores zero

Let `g(0..3)=(0,1,1,0)` and the current row interval be `[0,3]`. Every single
threshold query has a possible child whose payoff oscillation remains one.
Its guaranteed one-step score is therefore zero. Nevertheless, query 0 and,
when necessary, query 2 resolve g in at most two complete answers. They need
not identify whether a middle threshold is 1 or 2.

This makes a small range-target dynamic program a useful alternative to
singleton ranking. With known nonnegative complete-answer tariffs c_j, define

```text
B_rho(l,u) = 0                              if osc_g([l,u]) <= rho;
B_rho(l,u) = min_(l<=j<u) {
                 c_j + max(B_rho(l,j), B_rho(j+1,u))
             }                             otherwise.
```

The proof is the same finite decision-tree recursion used by
[the threshold planner](threshold_plan.py): a complete first query partitions
the remaining thresholds; the adversarial branch determines worst-case cost.
Nonempty children make the recursion terminate. Its leaf target is sufficient
payoff precision, which can be cheaper than finding H or determining every
requested truth label. The example above has `B_0(0,3)=2` under unit tariffs.

Completing this bundle on physical row i gives a guaranteed width reduction
of at least `(m_i/n)*max(0,r_i-rho)`, at complete-query expenditure at most
`B_rho(l_i,u_i)`. Add planning and other overhead not already in the tariffs
to the bundle invoice.
Enumerating a few attainable rho values gives actual alternatives along a
cost/precision frontier. Guaranteed quote bounds may replace tariffs. If
prices depend on retained witnesses or provider state, either use bounds
uniform over that state or enlarge the planning state; do not silently price
real proof work with the interval alone. This note derives the range-target
variant but adds no new implementation or benchmark claim.

## 4. What buying fresh rows guarantees

Compare an existing-row refinement with a batch of b additional iid draws,
while holding the old intervals fixed. Suppose the new draw occurrences are
refined to payoff oscillations `r'_1,...,r'_b`, with average `r_bar_new`.
This comparison credits no incidental narrowing of old occurrences from a
repeated identity's new receipt; such shared updates can improve it further.
Then exact algebra gives

```text
C_(n+b) = (n*C_n + b*r_bar_new)/(n+b).

W_n-W_(n+b)
  = [b/(n+b)]*(C_n-r_bar_new)
    + 2*V*(epsilon_n-epsilon_(n+b)).
```

Thus a complete acquisition plan guaranteeing `r'_k<=rho` for every new
occurrence has the computable lower bound

```text
Delta_fresh >= [b/(n+b)]*(C_n-rho)
               + 2*V*(epsilon_n-epsilon_(n+b)).
```

This exposes two different effects. Fresh adequately resolved rows dilute
old censoring and improve the statistical term. Fresh unresolved row identities
can instead increase the censoring contribution: substitute
`rho=max(g)-min(g)` to see whether the bound is useful. Merely increasing n
does not guarantee more precise value answers. Intersecting valid retained
bands preserves a previous warrant if a new raw band is wider; it does not
manufacture a reduction.

For a single fully resolved new draw, the bound simplifies to
`C_n/(n+1)+2*V*(epsilon_n-epsilon_(n+1))`. Compare its complete acquisition cost
with an existing-row bundle's reduction and cost. A negative or zero bound
means this particular worst-case criterion cannot justify the purchase;
expected or multipurpose benefits may still justify an explicitly scoped
proposal. No distribution of unobserved H is supplied by these formulas.

Repeated source identities are allowed only because the new identities are
actually drawn iid with replacement. A cache hit can eliminate proof
production while contributing a new occurrence to n. Draw generation,
lookup, checking as required, and updating still cost work. Choosing already
cached identities instead of following the declared draw law does not buy iid
sample size. Quotes for a fresh batch must cover its possible cache misses,
or be honestly marked expected rather than guaranteed costs.

### The confidence event must survive sample-size adaptation

The formulas require epsilon_n and epsilon_(n+b) from a valid joint risk
scheme. For example, the calibration note's elementary anytime choice is

```text
epsilon_n = sqrt(log(2*n*(n+1)/alpha)/(2*n)).
```

A prospective batch schedule with summable allowances is another option.
Unlimited refinements on one prespecified n use that n's original common
event; adaptively adding/reporting n does not inherit fixed-n coverage for
free. If an earlier report used the entire allowance, a new method or extension
must disclose the combined risk or use an appropriately designed future
stream. The numerical gain formula uses the actual authorized radii, which
need not decrease at every reporting boundary.

The [Bernoulli-mixture alternative](threshold_mixture.md) supplies cut-specific
anytime endpoints and can improve rare-cut precision. It does not have the
same scalar-epsilon decomposition without a conservative reduction. For that
source, use its actual robust-width oracle for action evaluation. Selecting
between independently warranted statistical families also requires a joint
allowance; a narrower endpoint is not free extra coverage.

## 5. Use the full source when the cheap score misses compatibility

Let D denote the retained evidence and `P(D)` its common warranted population
set. It may be the CDF-band polytope, its intersection with retained prefix
constraints, or a source retaining each row's allowed mass allocation. Define

```text
R_g(D) = max_(p in P(D)) E_p g - min_(p in P(D)) E_p g.
Delta_oracle(A) = R_g(D) - max_o R_g(D plus outcome o of A).
```

For complete outcomes whose constraints refine the original set,
`Delta_oracle>=0`; this is direct set inclusion. It is the exact local
guaranteed reduction for the chosen source representation, provided every
possible checked outcome is included. Capped no-progress outcomes again give
zero. A source inconsistency must be surfaced, not read as a zero-width
certificate. On the common coverage event the true population keeps the
relevant sets nonempty.

The cheap oscillation score can screen many actions; the full oracle can
price a smaller shortlist and complementary bundles. The
[CDF sweep implementation](cdf_sweep.py) makes the simpler source inexpensive
to query. A stronger retained-row source has a different computational bill.
Charge each prospective outcome calculation and retained-state update. No
general greedy-optimality claim is needed for this useful interface.

For a finite requested family g_a with nonnegative priority weights w_a, one
reusable objective is `sum_a w_a*W_n(g_a)`. Its censoring contribution on row i
is `sum_a w_a*r_i(g_a)`, and its sampling term is
`2*epsilon_n*sum_a w_a*V(g_a)`. A query's guaranteed reduction is

```text
(m_i/n) * [sum_a w_a*r_i(g_a)
          - max_o sum_a w_a*r_i^o(g_a)].
```

The same outcome occurs for every payoff, so max stays outside the sum. This
can reward a probe that sharpens several requested contrasts. A worst
normalized width or robust-regret target can instead use prospective oracle
evaluations. The common CDF event covers later choices of payoff and priority
weights; the weights are acquisition preferences, not a theorem about economic
value. Stop an individual row bundle when its requested payoff precision is
met, and keep the broader discovery allocation revisable.

## 6. Two strong alternatives belong in the purchase comparison

For a finite cohort of N known identities, checked intervals for **every** row,
including untouched rows, give the deterministic mean interval

```text
[(1/N)*sum_(i=1..N) a_i(g), (1/N)*sum_(i=1..N) b_i(g)].
```

There is no sampling term and no iid requirement for selecting the next
cohort row to refine. A row's guaranteed width reduction is its oscillation
reduction divided by N, regardless of sampled multiplicity. This option can
be attractive for a small or heavily cached cohort; it explicitly targets
that cohort's mean. It does not certify an unmodeled population beyond it.
All unvisited rows retain their full ranges. Sample n and population N are
different denominators, even when their receipts are shared.

A direct paired-payoff audit or confidence sequence is also a strong
comparator, especially when g has small range but many alternating jumps and
large V. It receives the same partial receipts and may stop as soon as the
pair's payoff is known. A genuinely new data-selected contrast can be bound
now and calibrated on future iid draws, or handled through an already covered
feature family; retrospectively calling its selected old data a fixed-target
sample is not justified. For real solver-bill contrasts, direct whole-policy
audits additionally measure cost variation that an H source does not contain.

## 7. Concrete disposition for the present order contrast

The [retained query results](threshold_query_results.json) use

```text
g(H) = 1 - 1[H<=3] - 1[H<=4]
     = -1 for H<=3, 0 for H=4, and +1 for H>=5.
```

After the initial request, all 16 draw occurrences already determine both
cut indicators. Therefore every `r_i(g)=0`. With outward radius `7/20` and
`V(g)=2`, the preclipped sampling width is `7/5`. The clipped variation
interval is `[-31/80,1]`; the compatible CDF answer is the sharper
`[-31/80,73/80]`. All nine recorded arm/stage combinations return those same
endpoints despite later proof purchases.

For this monotone g the conclusion also holds for the stronger retained-row
source, not merely the simple variation interval. Every compatible empirical
law q has the same values `F_q(3)` and `F_q(4)`. Its upper and lower shifted
CDFs `min(1,F_q+epsilon)` and `max(0,F_q-epsilon)`, with the known support
endpoints restored, are feasible population laws within the DKW radius.
They simultaneously attain the relevant cut extremes. The value
`1-F(3)-F(4)` therefore depends only on those already fixed empirical cuts;
locating mass more precisely inside the three constant-payoff regions cannot
improve its current source-calibration interval.

The useful next purchase for this particular contrast is fresh iid rows with
enough paid proof work to determine g, a properly warranted sharper statistical
method, or deterministic coverage of additional cohort identities. Comparing
these options requires their actual acquisition bills. Further exact-H search
on the current rows can serve other requested payoffs or proof-reuse goals,
but does not purchase additional precision for this contrast.

For a proposed width target eta, first check the actual oracle answer. If it
is insufficient and `2*epsilon_n*V>eta`, existing-row refinement alone cannot
meet eta through the simple preclipped certificate. Once the sampling term is
at most eta, the remaining censoring budget is explicit:
`C_n <= eta-2*epsilon_n*V`. Range-target bundles and fresh-row batch options can
then be compared against that budget. This is a concrete acquisition decision,
not a promise that greater precision will yield a favorable contrast or a
reason to freeze the surrounding hypothesis search.
