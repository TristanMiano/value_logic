# F15 results review: retention sections 3–4

Reviewer: **delegated ChatGPT (GPT-6 Astra Pro), F15 retention report review**.
Scope: review of the drafted results report against the completed original
retention units and the independent rational output audit. No report edit,
population generation, experimental-stage rerun, or F16 work was performed.
Parallel review minutes are not additive to the principal time ledger.

Reviewed report SHA256:
`ef97ee03d02d946896f9fa46f7373cf46bba0b5a57693ce3685f8b826a752ada`.
Reviewed sections 3–4 SHA256:
`8d22a781f7557be111ee08263bd9aa85ebb35187065e10054de96ed82884df0a`.
These hashes identify the draft reviewed, before any resulting wording edits.

## Finding requiring a small correction

**Section 4.2 assigns archive construction to the wrong incremental service
in its prose.** The draft says the native-inclusive update also includes
"archive/context construction" after describing arithmetic-only update.
The recorded arithmetic-only measure already includes archive construction.
Every one of the 1,920 original rows satisfies exactly:

```text
arithmetic update = archive production + acquisition + update/solve + decision
native-inclusive update = arithmetic update + current context + current native protocol
```

Suggested wording:

> Arithmetic-only update includes archive construction, retained solving,
> acquisition where required, and decision computation. Native-inclusive
> update adds current context construction and the complete current
> proof/reception protocol.

The numerical time table is correct. This finding concerns the accounting
description, not a timer, experimental result, or double count in the saved
data. The resource-conservation equations were checked directly against all
original method rows.

## Optional clarification

In section 3.1, **"16 initial-population seeds × 10 revisions"** is more
precise than "16 population draws × 10 revisions". There are 16 shared
initial laws; the source-drift variant also draws a different current scoring
law for each seed. The episode denominator of 160 and the warning that
within-seed revisions are dependent are correct. This wording refinement
does not change any support count.

## Numerical tables: no corrections needed

[`results_retention_review.py`](results_retention_review.py) independently
extracts the report's retention tables and recomputes their quantities from
the **160 original, individually hash-checked case files**. It imports no
experiment code. The saved result is
[`results_retention_review.json`](results_retention_review.json).

All **193 table checks passed**:

| Table or claim family | Checks |
|---|---:|
| Method/access outcome counts, receipts, useful rows, mean regret | 60 |
| Distinct useful episodes by revision | 5 |
| Resident, context, proof, and total stored-byte medians | 24 |
| Initial, arithmetic, and native-inclusive time means | 36 |
| Adaptive acquisition counts and decision cost | 12 |
| Scalar-fee totals including all common charges | 36 |
| Horizon eligible-pair counts and wins | 20 |

Exact count/storage values were compared directly. Six-decimal time/loss
entries were checked within half of the displayed final decimal place.
An additional direct inspection checked **all seven section 3.4 examples**;
their orders, intervals, costs, regrets, bounds, and acquisition counters agree
with the original units.

## Interpretation checks that passed

### Decisions and native receipt are kept separate

The report correctly distinguishes **1,220 certified orders** from **1,218
selected-order receipts**. There are two epsilon-regret-certified orders that
do not meet the tighter zero-budget fallback comparison. Conversely, eight
of the **1,226** total receipts concern diagnostic options rather than the
executed certified order. Those diagnostics are not counted as useful
decisions. The separate illustrations in section 3.4 correctly explain both
directions of this distinction.

The report's **248** true-under-the-full-law comparisons that are not valid
over the retained/current fiber, **58** approximate-selected-cost certified
orders, and **276** above-tolerance realized regrets are reproduced. All 276
above-tolerance regrets occur after refusal. The report retains certified
fallback and refusal-to-fallback as different outcomes.

### Acquisition totals include common charges

The fee table recomputes as the mean of

```math
C_{\mathrm{executed}} + q(8+k_{\mathrm{current\ common}}+m_{\mathrm{repair}})
```

at each frozen scalar fee. Thus it includes the eight common initial fields,
the three current fields in the known-marginal variant, and method-specific
repair. It is the `h=1` quantity, as labeled. It is not merely the recorded
decision-plus-current-acquisition column with initial charges omitted.

The paired acquisition comparison legitimately cancels the identical common
charges, leaving action-cost reduction minus repair fees. The report correctly
states that numeric-answer utility, CPU, and archive bytes have not been
invented as additional monetary benefits or costs. For each selective method,
the reported **78** acquiring episodes, **38** with zero action benefit,
**32** with a previously certified decision, and **40/21/0** strict net wins
at the registered fees all reproduce exactly.

### Payload savings do not hide context or cache cost

The reported resident savings of **18 bytes** against exact intervals and
**12 bytes** against fresh are also the medians of the corresponding paired
differences, not only differences between unpaired medians. Cached resident
cost includes the old source context and proof. Current context/proof and
adaptive archive storage remain in the complete serialized totals. The report
explicitly refrains from interpreting these wire sizes as RSS or information
lower bounds.

### Horizon wins use the advertised eligibility rule

The review independently reconstructs each full quality signature and checks
all-number admission, a certified nonfallback order, and receipt for that
selected order before counting a timing win. The report's complete horizon
table reproduces directly from `initial_total_ns + h * one_update_total_ns`.

In particular, the **28/95** eligible tailored-versus-fresh pairs in section
4.4 differ legitimately from the **59/126** admitted tailored-versus-interval
pairs in section 4.2: the comparator and exact-quality-equality requirement
are different. The seven eventual cached no-reacquisition crossings over all
rows provide zero matched admitted-service wins, as reported. The single
adaptive cached projection that wins at horizons 16 and 64 is retained in the
table. None of these projections is described as a measured repeated-update
experiment.

## Overall disposition

Apart from the archive-timing prose correction and optional seed wording,
the reviewed sections give a numerically accurate and appropriately bounded
account of the recorded retention outcomes, ordinary controls, failure/refusal
cases, costs, and horizon projections. No result, application criterion, or
scientific disposition needs to change on the basis of this review.
