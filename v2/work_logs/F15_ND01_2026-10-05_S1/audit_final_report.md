# Independent review of the F15-ND01 report

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, independent protocol/statistics
collaborator. Date: 2026-10-05. This is an ND01 reporting audit; it does not
perform F16, determine a contribution gate, or add principal research minutes.

## Disposition

**No outstanding scientific or numerical correction in the reviewed report.**
The four interpretation/precision issues raised during review were corrected
in the saved snapshot. Final Research90 and ledger closure remain a separate
pending accounting obligation.

Reviewed report:
[`F15_ND01_results.md`](../../experiments/F15_ND01_results.md), SHA256
`2ba0372855335965d98e8514e4cb06556d41c86c2010ecf96676397d992de598`.
This hash identifies the snapshot audited, rather than asserting that a later
accounting update must preserve the report's bytes.

The [machine-readable audit](audit_final_report.json), reproduced by
[`audit_final_report.py`](audit_final_report.py), records **621 passing checks**
with no failures. It reads saved artifacts only; it imports no experiment or
reporting implementation and executes no model, fit, or population generator.

## Concrete corrections resolved

| Item | Reason | Saved resolution |
|---|---|---|
| Opening causal language | The diagnostic identifies concrete contributing limitations, without uniquely allocating the original 0/5 to them. | “Principal causes” changed to “concrete contributing limitations.” |
| Robust-selector 10/31 counts | These compare the validation worst-normalized objective; the surrounding paragraph also discusses MAE. | The exact objective is now named beside the counts. |
| Task readiness versus intervention adequacy | The ordinary networks passed task readiness, while original intervention adequacy was not established. | The first hypothesis row now explicitly names ordinary-network intervention adequacy. |
| Fractional-coordinate count | The 3–10 count uses the stored `1e-10` classification tolerance; a few nominally one values differ from one at floating-point roundoff. | The tolerance is now explicit, with no unqualified “strictly” count. |

## Scientific and numerical checks

All cells in the main mask, ordinary-baseline, search, error-decomposition,
and joint-composition tables agree with their saved numerical sources at the
displayed precision. The counts distinguish role-level point adequacy from
models satisfying both roles. They are neither the original complete endpoint
nor confidence-qualified support. Each of the five frozen-MSE proposal
families has nonnegative observed role-level improvements at the larger nested
budget, as stated.

The report preserves the central calibration distinction: five layouts of one
constructed function have adequate searched identity interventions but zero
complete endpoints because of the matched-control conjunction. It correctly
reports the supported scale comparisons, capable optimized controls, the
point-level margin limitation, and all 560 original assessment statuses.
Previously completed independent saved-output, core-summary and interval
audits establish those source artifacts; this report review does not replace
their stronger artifact-level checks.

The report's fractional-mask and exhaustive-binary comparison is properly
limited to the shared finite discovery logit objective and descriptive
validation results. It retains the three capped fractional optimizers and
does not claim exact-real optimality. Its approximately 78%/22% arithmetic
comparison is explicitly not a causal attribution. The repeated-edit and
joint-order findings prevent single-role gains from being presented as a
complete two-cost representation.

The native-head/projector discussion correctly separates an algebraic
output-equivalence construction from a trained DAS result or a unique learned
feature. It specifies the exact inactive-unit certificate's real-function
scope and the separate observed floating-point agreement. Technical
superposition remains unestablished; ordinary training's lack of a dedicated
cost-block incentive remains salient.

## Independent repeatability reconstruction

The reviewer derives

```math
T(h)=(I-M)h+Md,
\qquad T(T(h))-T(h)=M(I-M)(d-h).
```

With stored native contribution matrix `A` and Gram matrix `G=A^T A/n`,
set `b=m*(1-m)`. The squared additional logit change is `b^T G b`.
The audit independently sums all 1,024 quadratic terms per role using
standard-library `math.fsum`, checks the binary64 quadratic hashes and their
preparation bindings, and compares every saved drift coefficient and all ten
saved MSE/RMS values. It does not import or invoke `repeatability.py`.

The reconstructed RMS range is **0.038512246008960915–0.13017859991780278**,
agreeing with the report and saved result to floating-point precision.
The binary masks are structurally idempotent. The fractional calculation is
explicitly post-outcome, uses the existing **640 discovery pairs per role**
through their saved moments, and generates zero new validation data or
acceptance conditions.

## Independent selection/control-ceiling audit

The separately delegated accounting/statistics reviewer saved
[`audit_selection.md`](audit_selection.md),
[`audit_selection.json`](audit_selection.json), and its reproducible source.
That audit passed **18,965 checks** against the saved preparation/evaluation
statistics without importing neural, population, or reporting modules.
It reconstructs all 100 comparisons, all group aggregates, and all 160
control-ceiling records.

The 41 subset changes all improve the discovery worst-normalized objective;
validation improves in 10 and worsens in 31, with 59 unchanged. The fixed
control radius is independently recovered as
`2*sqrt(log(2*560/.05)/(2*40960)) = .022115658601168407`.
Seven identity permuted-control roles and one random-control role impose the
reported conditional ceilings, covering all five constructed layouts.
The report appropriately discloses the dependence among these settings and
conditions the bound on the same observed controls and interval rule.

## Provenance, costs, links and limitations

All quoted binding hashes match the current files. All **28 local links**
in the reviewed report resolve. The five external command rows agree with
their recorded exit codes, wall times, child user-plus-system CPU, and peak
RSS. Nested runner costs are explicitly included rather than added twice.
The original scientific stages remain first-attempt successes; supplementary
analysis and formatting revisions are distinguished from scientific retries.

The failure section and linked raw records preserve pre-freeze drafting,
reporting-schema/path, formatting, and retrieval limitations. The primary
literature note records the failed accesses and the primary versions actually
used. This audit inspected that local provenance/disclosure record; it does
not claim another independent retrieval of those full texts.

Joint-panel summary cells were checked against the saved mechanism result.
As the report states, the mechanism auditor did not independently regenerate
the unsaved joint panel's exact RMS/MAE. The scalar report review makes no
stronger claim. Prior exact model/array integrity checks remain available.

The report defers final exact mode/lane accounting to the work log. It does
not reset POST-B-1 or count reviewers as additional elapsed effort. The
Research90 floor and final ledger preservation must still pass the separate
close audit. The contribution and next-task discussion remains a bounded
diagnostic/application disposition and an unstarted recommendation; this
review itself supplies no F16 work or Gate C/D pass.
