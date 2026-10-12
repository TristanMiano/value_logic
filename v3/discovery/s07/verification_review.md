# F01 verification review and conditional cost screen

Contributor: **ChatGPT (GPT-6 Astra Pro)**. DEVELOPMENT, October 12, 2026.
Constructive review of the [prospective F01 record](forecast_design.md),
[a01](a01/results.json), [a02](a02/results.json) and [a03](a03/results.json).
No new source acquisitions or principal-clock claim.

## Keep the comparator meaningful

F01 should compare S28-B1 with the best **named, separately implemented**
conventional controller under its actual complete bill. The specified native
warm controller, audit-first, logic-first and conventional cost-directed
controller remain relevant. A generic robust finite AND/OR or Bellman planner
is also a relevant control when its finite state/outcome abstraction is
applicable. Give it the same admitted bounds, complete-call and unresolved
outcome contracts, and include its planning, checking and retention costs.

That ordinary planner may choose exactly the same acquisitions as S28-B1 while
requiring different work to compute them. Its actual implementation bill is
the meaningful comparison. A byte-identical copy of the candidate is a duplicate
arm, not an additional scientific baseline that must somehow be beaten by 10%.
If the closest ordinary construction and the candidate reduce to the same
method with the same bill, record equivalence and reconsider the material
resource claim. Do not invent either a weak control or an impossible identity
requirement. This clarifies the comparator sentence in the original proposal;
it does not remove a stronger independently specified ordinary algorithm.

## What the equal audit counts imply

For candidate c and comparator b, write a full-horizon cost as
`C_i = S + U_i + a*A_i + rho*T_i + s*B_i + R_i`, where S is the shared
historical/current named setup, U is the arm's named bill, T and B are recorded
CPU/storage components, and R retains **all** remaining costs. Rates must use
a billing convention that does not charge the same resource twice. B can be
converted to byte-time only under a declared retention horizon.

With the same A audits, 10% savings require

```text
rho*(0.9*T_b-T_c) + s*(0.9*B_b-B_c) + 0.9*R_b-R_c
    >= U_c-0.9*U_b + 0.1*S + 0.1*a*A.
```

Equal acquisition counts do not create an economic benefit when audit prices
increase: their common charge cancels in the raw difference but remains in the
10% denominator. A larger common audit bill makes the percentage target harder.
If named units and every other fully accounted component are no smaller, the
10% claim fails for nonnegative prices. With unmeasured components, only a
conditional dominance statement is justified.

For **a02 versus audit-first**, `S=177340`, `U_c=3385019`, `U_b=485066`,
and `A=14`. Current measured admission-plus-arm CPU is
1.580095854 versus 0.886098754 seconds. The consistently recorded
profile/planner/support storage subset is 101123 versus 71432 bytes. Absorb
unreported storage payloads and all other missing fees into R. The necessary
condition becomes

```text
0.9*R_b-R_c >= 2966193.6 + 1.4*a
                    + 0.7826069754*rho + 36834.2*s.
```

Every displayed coefficient is adverse. Without a substantial separately
warranted saving in R, no choice of nonnegative audit/CPU/storage rates rescues
that recorded implementation. For example, under the conditional assumption
`R_c >= 0.9*R_b`, the inequality is impossible; that assumption is not silently
asserted as an observed fact. More generally, any claimed CPU saving must
exceed the exact threshold obtained by solving the first inequality for T_c,
and needs its own measurement and rate warrant.

**a03 improves the implementation:** named units fall to **2306193** and
complete quotation cost to **1718749**, including its measured 2360-unit
initialization. It still executes **14 audits and 14 complete calls** versus
the same audit-first counts, and its named bill remains **4.7544 times** that
control's 485066 units. The common recorded storage subset is 129562 bytes;
newly itemized quotation payloads add **396177 bytes**. The first extractor
treated all earlier absent payload fields as unmeasured. The source-backed
reporting correction below establishes that these particular planner-owned
objects are absent in the archived controls, while other host/native storage
remains unmeasured. The same a03 conditional rescue threshold is

```text
0.9*R_b-R_c >= 1887367.6 + 1.4*a
                    + 0.3987251184*rho + 461450.2*s.
```

Here the candidate's known additional quotation payload is in B; the earlier
control's unitemized host/native memory remains in R. The control has no
planner-owned prepared quote, enclosure or margin payloads, as established
below; this is not a claim that it has zero omitted storage. The CPU observations are
single ordered development executions, not stable timing estimates. These
conditions explain **zero demonstrated full-cost benefit regions** without
turning unpriced components into zero or asserting all possible regions empty.

A constructive lower-budget screen is already available: subtracting every
measured a03 quotation unit leaves **587444 named arm units**. The 10% named
full-horizon target against audit-first would require at most **418825.4 arm
units**, so another **168618.6 nonquotation units** would still need to be
removed. This deliberately hypothetical removal of measured quote work is not
a zero price assigned to unknown costs. It shows why changing purchases or
other controller work is more promising than quotation optimization alone on
this particular trace.

## Concrete items to preregister before V1 exposure

- **Exact generator:** retain the planted eight-variable family and six stated
  cohort/mode cells. Freeze clause generation, unique mode-catalog sampling,
  hidden-row generation, fresh seed procedure and the 24 complete stream IDs.
  Cost modes and hidden rows are independently committed before purchases;
  controllers receive no free outcome distribution or realized optimum.
- **Precisely named controls:** bind each implementation, admitted interface,
  purchase menu, stopping rule and initialization. The generic ordinary planner
  needs an explicit finite outcome abstraction and its real resource limits,
  not a label suggesting an unimplemented optimal oracle.
- **Fixed economic question:** choose the reference rates, twofold audit-price
  interval, host/storage ranges, full retention horizon and treatment of setup
  before fresh exposure. State whether one frozen acquisition policy is repriced
  throughout the region or policies adapt to price. Repricing one observed
  trace does not execute the unobserved price-adapted policies.
- **Cost closure:** freeze how admission, quote construction, source reads,
  checkpoints, final output serialization, native CPU/memory, retained raw
  evidence and failed attempts enter the invoice. Bound any remaining residual
  instead of omitting it. Preserve the current incremental and full-horizon
  views; the common setup affects percentage savings even when differences cancel.
- **Analysis unit and endpoint:** the independent sampling unit is a whole
  stream, not its sixteen correlated requests or its timing repeats. Define
  the comparator envelope mathematically. A pointwise hindsight envelope is a
  conservative benchmark, not a deployable controller with free foreknowledge.
  Recompute it inside each paired, six-cell-stratified bootstrap resample.
- **Uncertainty and region selection:** with only four streams per cell,
  bootstrap tail accuracy is limited. Keep the proposed 95% bound labeled as
  an inferential procedure, not a finite-sample theorem. Fix the procedure and
  interval endpoints before exposure; account simultaneously for the claimed
  price region. For a fixed trace, each candidate-versus-control margin is
  affine in prices, so all relevant box vertices can be checked. Additional
  adaptive policy regions require their separately specified executions.
- **Outcome disposition:** failed or unresolved final requests remain failures
  under the original all-output claim. No dropping difficult streams, replacing
  seeds or weakening the threshold after exposure. S29 source-conservation
  constructions change the source contract and need their own event; they do
  not automatically raise F01's probability.

These are specific preparation obligations for eventual confirmation, not a
request to launch an adversarial campaign during this discovery hour.

## Source audit of the progress extractor

[progress_report.py](progress_report.py) now checks the bound archived
implementation and any locally archived dependency hashes. It reconstructs
output/purchase/plan counts, rejects inconsistent summaries or invoices, and
uses all per-plan meter deltas plus separately measured constructor work.
The quote categories alone would miss interface, projection and lookup work.

The common source, ordered request signature and raw initial-admission hashes
bind comparisons; common evaluator hash equality is also displayed. Actual
source/cap/menu contracts remain in the bound run and code archives rather
than being inferred from aggregate counts. The extractor's output counts are
record reconstruction, not another independent raw-proof check.

V3 payload fields are retained separately. Older missing candidate payloads
appear as explicit unknowns in the symbolic cost inequality. The narrow
source-backed absence correction below applies only to the archived controls,
preserving the distinction between a missing field and an absent object. Setup is
included once; quotation costs are a subset of the controller invoice and are
not added to it twice. The zero price-region entry means no qualifying complete
region is established by these unpriced development invoices. A future run
with a verified region needs that evidence imported explicitly; this extractor
must not be used to overwrite a later positive result with its current zero.

### Reporting correction: source-proven control absence

Extractor **`s07-progress-extraction-v2`** is preserved byte-for-byte as
[progress_report_v2.py](progress_report_v2.py), SHA-256
`51b155021357b33d39eedd7a64b46bd4a3aedd5c9f44c4f84bb4694fb745debc`.
Version **v3** narrows its blanket unknown treatment using the exact archived
[a01 implementation](a01/bundle_service.py), SHA-256
`b2df479412f688a4b0b717a084a175a83fe248af276c4e671b5bd7682a7d44c4`.
That version's `run_arm` constructs `BundlePlanner` only for policy `bundle`.
Its three conventional arms also explicitly retain `planner_cache_bytes=0`,
`plans=[]` and `planner_stats={}`. Thus prepared-quote, enclosure and margin
payloads belonging to that planner are structurally absent in those arms.
Each derived zero records the verified source hash and corroborating selectors;
the raw missing field remains missing. Other implementations do not inherit
this rule merely because their policy name or storage field is similar.

The [derived report](progress_results.json) consequently lists known serialized
payload totals of **71432** bytes for audit-first, **82207** each for logic-first
and native-IHS, and **525739** for a03. The extra candidate payloads in a01/a02
remain **unknown**. These totals still omit general host/native memory, peak
allocation, archival retention and byte-time. None of those costs is zeroed.
Raw a01/a02/a03 records and their hashes are unchanged; the revised inequality
only removes the three controls' spurious quotation-payload unknowns. It leaves
the displayed a03 rescue threshold and the F01 forecast unchanged.
