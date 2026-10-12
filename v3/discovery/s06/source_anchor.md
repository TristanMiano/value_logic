# Transport paid scalar proofs through partial cost observations

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026 UTC.
DEVELOPMENT. This is a constructive continuation of
[calibrated repair](../s05/calibrated_repair.md),
[scalar-anchor stitching](vertex_derivation.md), and
[the checked native proof bridge](rup_findings.md). It is not an efficiency,
novelty, population-calibration or readiness claim.

## 1. A source representation that preserves the proof's use

Let one fixed logical repair source have feasible violation masks `F`, and

`C*(w) = min_{z in F} w dot z`.

Replacement costs p. A feasible repair u has regret
`u dot w - min(p,C*(w))`; replacement has regret `p-min(p,C*(w))`.
The true repair optimum is concave and positively homogeneous in its weights:
for nonnegative convex coefficients, the minimum of the weighted sum is at
least the weighted sum of the separate minima. These are mathematical
properties of the same fixed feasible source; they do not say that any source
optimum or lower certificate has been computed for free.

Suppose there are N fixed cost rows. Public possible vectors are `m_k`; after
actual observations row i can have any mode in the nonempty set Q_i. The target
is the cohort **sum** `w=sum_i m_(h_i)`, `h_i in Q_i`. The cohort mean divides
all costs, p and tolerance by N. The common convex source is
`W=sum_i conv{m_k:k in Q_i}`. Row membership, coordinate meanings and every
observed value must have the declared source warrant. No independence or mode
probabilities are required. These are the existing s06 finite-cohort premises,
not a claim about an arbitrary unknown physical law.

For every public mode, now retain a **paid, independently checked scalar lower
bound**

`ell_k <= C*(N*m_k)`.

The bounds may come from different proofs and different query methods. Their
source and exact objective bindings must agree. A zero lower bound is allowed
for a nonnegative objective when no stronger proof has been admitted.
An UNSAT label, checksum, floating optimizer value or stored `checked` flag
cannot supply ell_k by itself.

For any compatible latent modes,

`w = (1/N) * sum_i (N*m_(h_i))`,

so concavity gives

`C*(w) >= (1/N) * sum_i ell_(h_i)`.

The same inequality extends to convex combinations within each row. This
transports old logical proof work through newly refined cost observations. It
does not require finding all vertices of W, all feasible logical models, or
all Boolean objective masks.

## 2. The resulting uniform action gate

Write `d_k=ell_k/N`. For one fixed checked repair u define

`A_u(Q) = sum_i max_{k in Q_i} u dot m_k - p`,

`D_u(Q) = sum_i max_{k in Q_i} (u dot m_k - d_k)`.

Then a valid uniform regret certificate is

`B_u(Q) = max(0, A_u(Q), D_u(Q))`.

For replacement it is

`B_replace(Q) = max(0, p - sum_i min_{k in Q_i} d_k)`.

The first repair term compares its actual cost with replacement. The second
compares it with the transported true-optimum lower bound, retaining the
correlation between each mode's action cost and its lower proof. Taking the
minimum of these bounds across admitted fixed repairs and replacement selects
one certifiable output. Each returned repair still carries its own checked
feasible witness. Observations can change which action is selected after they
actually arrive; unobserved modes cannot select different realized actions.

[`source_anchor.py`](source_anchor.py) implements these formulas with exact
rational arithmetic and named operation charges. Its interface consumes
admitted data; the executable probe establishes admission from raw receipts
before invoking it. Per query it scans the remaining row-mode sets, with cost
proportional to their sizes plus action-cost compilation. It does not build the
group-product hull used by [the earlier rehearsal](hull_findings.md).

For the initial source with identical Q_i, this is exactly the original
six-anchor fixed-action bound. As rows are observed it can improve through
smaller row-mode sets, without any new solver or LP call. It can still be weaker
than a new proof, direct evaluation of retained cut duals at the refined
weights, an optimized concave interpolation, or the full retained tree bank.
Keep those alternatives and use the next appropriate bound when it is
inconclusive. A weak scalar transport bound does not establish poor action
quality.

## 3. A concrete audit-versus-proof quotation

The same representation supports inexpensive complete-outcome quotations;
[`anchor_quotes.py`](anchor_quotes.py) makes these callable.

**A paid cell audit.** For row i and coordinate j, partition Q_i by the
observable value `m_k[j]`. For every possible returned value, intersect that
row set and recompute the best available fixed-action bound. The worst of all
these post-observation bounds is the guaranteed audit result. No outcome
probabilities are needed. A hypothetical partition is forecast computation,
not an acquired observation. An impossible observation is a source conflict,
not an empty-set certificate.

**A paid logical call.** Let its nonnegative integer objective be q and its
integer budget b. If a complete call returns checked UNSAT, then every feasible
z satisfies `q dot z >= b+1`. At full-cohort anchor `v_k=N*m_k`, binary violations
imply

`v_k dot z >= q dot z - sum_j max(q_j-v_k[j],0)`.

Consequently, the new scalar lower bank may use

`ell'_k = max(ell_k, 0, b+1-sum_j max(q_j-v_k[j],0))`.

This is a cheap, valid transport of that newly checked cut to every anchor.
It is also the elementary unit-multiplier case of the rational cut-dual
construction. The negative branch quotation recomputes the action certificate
with ell'. No raw core or native status is substituted for the checked cut.

If the call instead returns a checked witness u with `q dot u<=b`, form the
warranted coordinate enclosure

`hi_j = sum_i max_{k in Q_i} m_k[j]`,

`alpha_box = sum_j max(hi_j-q_j,0)`.

Then `u dot w <= b+alpha_box` throughout W. The already admitted uniform lower
bound `l=sum_i min_{k in Q_i} ell_k/N` gives the following conservative positive
branch certificate, choosing that witness or replacement:

`B_plus <= max(0, min(p,b+alpha_box)-min(p,l))`.

Both branches also retain the old certificate, so cap either quotation by the
old best bound B. A completed call's worst quoted bound is
`max(B_plus,B_minus)`. If it is at most the requested tolerance, the call has a
concrete one-purchase output guarantee. The coordinate enclosure can lose
correlation; [the complete-call contract](contract_findings.md) retains tighter
support-based transfer alternatives when their additional computation is worth
paying for.

For an ordinarily capped native attempt, include the unresolved/no-progress
outcome. Its worst bound remains B and its guaranteed singleton improvement is
zero. The `complete` parameter in the quotation code is explicitly a premise;
it is not permission to treat a native time/conflict cap as complete. The
actual finite branching provider has a separately admitted operation-cap
contract. Its native CPU/host/economic deadline is not bounded by that tariff.

**Comparing prices.** Write `Delta_a=B-B_a` and `Delta_q=B-B_q`. Only when
complete all-in prices are warranted in a common accounting unit may one use
local ratios such as `Delta_a/(A+c_a)` and `Delta_q/c_q`. For positive
`Delta_q`, the audit is preferred by that particular ratio when

`A <= Delta_a*c_q/Delta_q - c_a`.

Here A is the separately priced external observation; c_a includes its
processing/checking/update, and c_q must include acquisition, checking,
objective work, retention and the applicable implementation costs. Prospective
quote construction itself is paid. Operation units and measured native time do
not supply a common economic conversion automatically. With unassigned prices,
retain symbolic or multi-resource comparisons, not a total-cost ranking.
The ratio is a local heuristic, not an optimal acquisition policy. Ties and
complementary purchases still call for small complete bundles. A bounded
AND/OR recursion can quote an audit followed by an outcome-specific complete
logical call, paying every branch's work and preserving unresolved outcomes.
This remains the coherent next controller integration.

## 4. Actual uncertain-source and observation-refinement evidence

The preceding [rational-dual probe](cut_dual_results.json) queried singleton
supplied objectives. [`dual_hull_probe.py`](dual_hull_probe.py) now makes actual
LP proposals over the initial common eight-row uncertain source. For every
source bank with retained RUP cuts, it rechecks the raw cut exports and
witnesses, proposes one rational dual at each of six full-cohort anchors, and
checks the rational lower values. It also pays to reconstruct a same-cut
Boolean projection as a reference. The initial tree bank remains available
to each compared representation.

| Own completed logical arm | Source banks | New continuous LP calls | Dual/reference anchor-lower matches | Uniform tolerance-4 closures |
|---|---:|---:|---:|---:|
| Requested tolerance | 9 | 54 | 38 of 54 | 0 |
| Exact | 12 | 72 | 63 of 72 | 0 |

Neither coordinate-box, fixed-hull-dual, stitched-dual nor full-cut-projection
bounds close these initial broad-source queries. There is no extra closure or
strict final-bound improvement in that comparison. The saved hierarchy checks
pass. This is useful scope information, not a negative verdict on the logical
actions. The query has genuinely uncertain costs and the tolerance stays fixed.

[`dual_hull_results.json`](dual_hull_results.json) records **1,031,243 named
units**, including actual raw admission and reference projection; **126 new
LP calls**, and **zero new SAT/IHS/proof/audit calls**. Wall time is
304,545,969 ns and process time 559,492,952 ns. This is a retrospective
representation query using each completed arm's own paid results, not a rerun
of an acquisition controller or a benchmark population.

[`source_anchor_probe.py`](source_anchor_probe.py) next re-admits those scalar
anchors from raw RUP cuts and exact rational multipliers, without rerunning
any LP. It reads the same fourteen actual `audit_first` observations for both
logical evidence banks and uses the predeclared prefixes 0,4,8,12,14. It checks
only the already recorded cell values against the committed source, not new
hidden cells. Historical observations are disclosed as historical acquisitions.

| Own logical bank | Query states | Prefix 0 | Prefix 4 | Prefix 8 | Prefix 12 | Prefix 14 |
|---|---:|---:|---:|---:|---:|---:|
| Requested tolerance | 45 | 0 | 0 | 0 | 1 | 4 |
| Exact | 60 | 0 | 0 | 0 | 4 | 5 |

Entries are queries with a checked bound at most four. Every one of the 21
banks has a strictly tighter final bound after source refinement. At prefix
12, one cost row is still unresolved. The prefix-12 closures are row 1 for
the requested bank, and rows 1,4,9,15 for the exact bank. These are conditional
query results on paid receipts, not newly executed repairs or a claim that the
listed audits are an efficient acquisition policy.

[`source_anchor_results.json`](source_anchor_results.json) records
**1,251,524 current replay units** and **zero new LP, SAT, IHS, proof or audit
calls**. Wall time is 208,992,802 ns and process time 395,816,484 ns. No hull
vertices or Boolean objective masks are enumerated by this transport run.
Raw readmission dominates portions of the invoice; neither native memory nor
all serialization/storage/hardware costs are assigned economic prices.

## 5. Focused quotation correspondence

[`anchor_quote_check.py`](anchor_quote_check.py) rechecks the existing paid tiny
contract example through the new scalar-anchor formulas. The admitted bounds
at modes (3,3) and (4,3) are both three; the initial fixed repair has bound
four, replacement costs eight and tolerance is two. Every complete single-cell
audit quotation has zero worst-outcome gain. The complete logical query
q=(3,3), b=4 has both checked branch bounds at most two. Restoring a possible
unresolved outcome returns guaranteed gain to zero. The already recorded SAT
witness actually has uniform bound zero and is rechecked again here.

The check makes **zero new acquisitions**, charges **8,242 replay/quotation
units**, and preserves its result in
[`anchor_quote_results.json`](anchor_quote_results.json). It is a correspondence
check on an exposed existing example, not new confirmation of the same two
historical calls. The substantive extension is the rowwise transport and the
callable two-outcome anchor update under the stated complete-call premise.

## Next constructive step

Put the cheap source-anchor evaluator and the existing tree/dual/hull bounds
behind the same admitted service interface. Give every conventional controller
the same representation and retained receipts. Quote a small audit-or-complete-
logical bundle using actual external audit prices or explicit symbolic regions;
keep the resident IHS path for paid warm work and the complete provider for a
supported finite fallback. Execute that controller as a new development run,
with its own source observations, retained native state, interrupted attempts
and full invoices. The three earlier stitched prefix gates are a motivation
for this integration, not already executed savings. The portfolio remains
DEVELOPMENT and discovery remains open.

## 6. Why the output action must remain revisable

For a fixed action u and a fixed scalar-anchor bank, the row-transport bound is
the maximum of fixed functions over the compatible latent configurations.
Any complete audit partitions that configuration set. Therefore

`max_outcome B_u(Q_after_outcome) = B_u(Q)`.

At least one outcome retains a configuration attaining the previous largest
component; monotonicity gives the reverse inequality. This explains zero
worst-outcome gain for a single fixed action without saying the observation is
useless. The relevant acquisition quotation instead permits a different fixed
action **after its actual outcome is known**:

`max_outcome min_u B_u(Q_after_outcome)`.

That can be strictly smaller than `min_u B_u(Q)`. It is a decision-region
property, not an expected-value assertion. Freezing the action before research
would hide this source of value.

The separate constructed [`audit_example.py`](audit_example.py) makes the
opposite regime from the logical-query example concrete. The same two-variable
hard clause `x1 OR x2` admits candidate assignments 1 and 2, both actually
checked and charged. A new one-row cost source has possible modes (0,2) and
(2,0); its fixed mode is committed before observation, with no outcome law.
Replacement costs three and tolerance is zero. Nonnegative objectives warrant
trivial scalar lower bounds zero at both anchors.

Before observing, either fixed repair has worst certificate two. For each one
held fixed, a coordinate audit's guaranteed gain is zero. Allowing the repair
choice to follow the actual observation gives a complete audit quotation of
zero regret in both outcomes. One **actual paid coordinate observation** returns
two; the service selects already checked model 2, whose certified regret is
zero. [`audit_results.json`](audit_results.json) retains the source, candidates,
pre-observation quotes, actual receipt and chosen action. No logical or LP call
is made. The audit's external price remains unassigned; provider software costs
four named units in addition to the recorded checking/quotation invoice.

The examples identify two useful acquisition regimes without an unknown prior:
one has a complete logical query that closes while every single-cell audit has
zero guaranteed gain; the other has a complete audit that closes by selecting
a different repair in each observed outcome. Neither establishes optimality of
a general greedy controller. Mixed cases can need a paid audit/proof bundle.
