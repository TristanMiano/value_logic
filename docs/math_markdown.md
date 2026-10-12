# Portable mathematical Markdown and preserved evidence

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Maintenance on October 12, 2026;
**zero discovery research credit**.

The repository checks readable mathematical Markdown while preserving the exact
bytes that earlier experiments and scientific reviews consumed. Ordinary active
documents are corrected in place. A scientifically bound historical document
has a separately checked portable view, listed below. Its raw source remains the
identity referenced by its original evidence; the view is the readable edition.

## Writing and checking active documents

GitHub supports both dollar delimiters and a dollar/backtick inline form, as
well as fenced `math` blocks. This repository uses the protected inline form and
math fences for `v3/` and generated portable views, because Markdown backslash
handling previously damaged some formulas. These are the repository's portable
conventions, not a claim that every other GitHub-supported form is invalid. See
[GitHub's mathematical-expression documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)
and the [CommonMark specification](https://spec.commonmark.org/0.31.2/) for the
underlying syntax.

Use protected inline math:

````markdown
The bound is $`L \le C^* \le U`$.
````

Use a math fence for a displayed equation:

````markdown
```math
\min(U,p)-\min(L,p)\le\tau.
```
````

The existing project macro rule replaces upright operator notation using
`\operatorname{...}` with `\mathrm{...}`. The audited starred `argmin` form
uses `\mathop{\mathrm{argmin}}\limits`. This is a notation and rendering
convention; the guard is neither a general TeX interpreter nor a proof checker.
It cannot establish mathematical equivalence for arbitrary macros or guarantee
a specific browser's rendered pixels.

Run the default repository check from its actual checkout root:

```sh
python v3/checks/math_markdown.py
```

To review one active file, use `--path`. To apply the documented substitutions
to that explicitly selected file, add `--fix`:

```sh
python v3/checks/math_markdown.py --path v3/work_logs/P3_10_2026-10-11_S1/certificate_recipe_derivation.md
python v3/checks/math_markdown.py --fix --path v3/work_logs/P3_10_2026-10-11_S1/certificate_recipe_derivation.md
```

Before using automatic formatting on a scientific input, inspect its source or
review bindings. A formatting failure inventory by itself does not make an
ordinary active document immutable. The fix command requires explicit paths
and refuses registered preserved sources. New source-bound evidence should get
an additive edition with its own provenance rather than a rewritten history.

## What the checker now verifies

The scanner recognizes code fences with their actual opening marker and length,
quoted and list-contained fences, indented code, and exact-length inline
backtick spans. An unmatched backtick does not conceal all subsequent equations.
Literal code and mathematical examples are masked before prose-link extraction,
with character offsets and line endings preserved. Mathematical fences are
still checked as math. This shared scanner also supports the
[link guard's archive handling](archive_links.md).

The [preserved pre-repair inventory](../v3/discovery/s06/pub/math_note.json)
records **379 formatting issue records in 65 files**.
The lexer corrections did not remove any of those real failures. Five affected
spans in two ordinary active derivations were normalized directly. The remaining
**374 issue records in 63 historical artifacts** are covered by checked views.
Their disposition depends on scientific provenance, not membership in an old
failure list.

For each preserved source, [the view manifest](../tools/math_views.json) records
its source hash, its view path and hash, and the original scientific preservation
basis. [The verifier](../verification/math_views.py) requires all of the following:

1. The actual source bytes match their recorded identity.
2. A hash-bound experiment/review record binds those bytes to that source path,
   or the independently validated frozen-copy origin chain does so.
3. The actual view bytes match their recorded identity and exactly equal the
   documented mechanical transformation of the source.
4. The derived view satisfies the same portable mathematical conventions as an
   active document.

Updating a view hash after changing its claims does not satisfy exact derivation.
Updating a source hash does not alter the earlier scientific receipt that binds
it. Missing or invalid provenance fails the check. An unrelated new active-file
violation also fails; there is no grandfathered failure count or blanket archive
exclusion. The receipt separately reports source-formatting issues covered by
verified views and remaining actionable issues.

Relative prose links in a view are rebased from the source's verified logical
namespace. Explicit recorded anchor corrections, observed historical checkout
prefixes, and the single recorded assembled-document fragment are applied only
to their bound source scopes. Every resulting link still undergoes the ordinary
target and heading checks. Literal code/math examples are not rewritten as links.
Prose hard breaks written as two trailing spaces use the equivalent backslash
form in portable views; code and math literal whitespace stays unchanged.
See [document origins](../tools/document_origins.json) for those separate bindings.

To verify or reconstruct registered views without changing their sources:

```sh
python verification/math_views.py verify
python verification/math_views.py generate
```

Generation reconstructs missing views only after checking scientific source
bindings, declared view identities, and exact transformations. It refuses an
existing conflicting view; it does not silently regenerate tampered evidence.
All source records, prior failed formatting receipts, and scientific run data
remain available. These maintenance checks do not rerun scientific acquisitions,
reopen clocks, or change discovery status.

## Preservation inventory

The groups distinguish actual scientific dependencies and historical copies
from files that were merely listed by old formatting or publication inventories.
Every row below links to the source. Preserved rows also link to their portable
view and to the original scientific binding (the manifest contains exact JSON
pointers and hashes). For copy rows, the shared origin registry validates the
original source record rather than relying on a directory-name heuristic.


### Active derivations: normalize source (2)

| Source | Readable edition | Scientific preservation basis |
| --- | --- | --- |
| [v3/work_logs/P3_10_2026-10-11_S1/certificate_recipe_derivation.md](../v3/work_logs/P3_10_2026-10-11_S1/certificate_recipe_derivation.md) | Active source corrected | No scientific binding found; old formatting/publication inventories alone do not freeze this file. |
| [v3/work_logs/P3_10_2026-10-11_S1/continuous_price_derivation.md](../v3/work_logs/P3_10_2026-10-11_S1/continuous_price_derivation.md) | Active source corrected | No scientific binding found; old formatting/publication inventories alone do not freeze this file. |


### Scientific inputs: preserve checked derivations (13)

| Source | Readable edition | Scientific preservation basis |
| --- | --- | --- |
| [v3/derivations/08_budget_selection_counterexample.md](../v3/derivations/08_budget_selection_counterexample.md) | [Portable view](math/06822bfacf393701.md) | [Scientific record](../v3/experiments/frozen_v1/manifest.json), JSON pointer `["sources", 23]`. |
| [v3/experiments/development.md](../v3/experiments/development.md) | [Portable view](math/3af3eb70d8d4f709.md) | [Scientific record](../v3/experiments/frozen_v1/manifest.json), JSON pointer `["sources", 28]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/decision_service_interpretation.md](../v3/work_logs/P3_10_2026-10-11_S1/decision_service_interpretation.md) | [Portable view](math/db70fad9594abc5c.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/duty_evidence_attachment.json), JSON pointer `["new_evidence_bindings", 5]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/decision_service_interpretation_addendum.md](../v3/work_logs/P3_10_2026-10-11_S1/decision_service_interpretation_addendum.md) | [Portable view](math/5ee1f4732bf582e5.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/addendum_closure_v1/closure.json), JSON pointer `[]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/forecast_action_decomposition.md](../v3/work_logs/P3_10_2026-10-11_S1/forecast_action_decomposition.md) | [Portable view](math/f91d693ca069f066.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_mechanism_review_v1/initial_snapshot_manifest.json), JSON pointer `["files", 1]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/forecast_action_price_boundary_interpretation.md](../v3/work_logs/P3_10_2026-10-11_S1/forecast_action_price_boundary_interpretation.md) | [Portable view](math/6cac67478d6a3524.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/claim_ledger_dispositions_review_v1/source_bindings.json), JSON pointer `["bound_sources", 2]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/forecast_action_price_derivation.md](../v3/work_logs/P3_10_2026-10-11_S1/forecast_action_price_derivation.md) | [Portable view](math/0a93856be1a43783.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/enrollment.json), JSON pointer `["files", 0]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/gate_architecture_derivation.md](../v3/work_logs/P3_10_2026-10-11_S1/gate_architecture_derivation.md) | [Portable view](math/75da7136f1425fd5.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/run_02/results.json), JSON pointer `["read_bindings", "v3/work_logs/P3_10_2026-10-11_S1/gate_architecture_derivation.md"]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/joint_report_geometry.md](../v3/work_logs/P3_10_2026-10-11_S1/joint_report_geometry.md) | [Portable view](math/c97645f6129d8b82.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/joint_geometry_review_v1/initial_snapshot_manifest.json), JSON pointer `["files", 1]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/retrospective_report_derivation.md](../v3/work_logs/P3_10_2026-10-11_S1/retrospective_report_derivation.md) | [Portable view](math/989114681d0dd861.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/width_decomposition_review_v1.manifest.json), JSON pointer `["reviewed_principal_file"]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/transfer_failure_derivation.md](../v3/work_logs/P3_10_2026-10-11_S1/transfer_failure_derivation.md) | [Portable view](math/cda09e807216956c.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/review_manifest.json), JSON pointer `["reviewed_principal_sources", 0]`. |
| [v3/work_logs/R_P3_B_A_2026-10-09_S1/development/allocation_comparison/analysis.md](../v3/work_logs/R_P3_B_A_2026-10-09_S1/development/allocation_comparison/analysis.md) | [Portable view](math/ca87f3aad77a3489.md) | [Scientific record](../v3/work_logs/R_P3_B_A_2026-10-09_S1/development/service_comparison/setup_scope_erratum_2026-10-09.json), JSON pointer `["current_analysis_files", 1]`. |
| [v3/work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/analysis.md](../v3/work_logs/R_P3_B_A_2026-10-09_S1/development/observable_certificate/analysis.md) | [Portable view](math/2a10c20a861e4f49.md) | [Scientific record](../v3/work_logs/R_P3_B_A_2026-10-09_S1/evidence_manifest.json), JSON pointer `["files", 103]`. |


### Frozen source copies and reviewed snapshots (30)

| Source | Readable edition | Scientific preservation basis |
| --- | --- | --- |
| [v3/experiments/frozen_v1/source/v3/derivations/08_budget_selection_counterexample.md](../v3/experiments/frozen_v1/source/v3/derivations/08_budget_selection_counterexample.md) | [Portable view](math/c5c5b7334c4ab65d.md) | [Verified frozen-copy origin](../tools/document_origins.json): `v3/derivations/08_budget_selection_counterexample.md`. |
| [v3/experiments/frozen_v1/source/v3/experiments/development.md](../v3/experiments/frozen_v1/source/v3/experiments/development.md) | [Portable view](math/d7d9bb2976e84589.md) | [Verified frozen-copy origin](../tools/document_origins.json): `v3/experiments/development.md`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/duty_disposition/source_snapshot/v3/experiments/development.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/duty_disposition/source_snapshot/v3/experiments/development.md) | [Portable view](math/c95260cd03dd9f0d.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/evidence_manifest.json), JSON pointer `["files", 528]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/u08_source/v3/experiments/development.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/u08_source/v3/experiments/development.md) | [Portable view](math/b6a5ac2cc72fbe0a.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/u08_source/manifest.json), JSON pointer `["sources", 0]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/mean_price_envelope_independent_v1/inputs/prior_individual_review/review.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/mean_price_envelope_independent_v1/inputs/prior_individual_review/review.md) | [Portable view](math/001c9cafb6008046.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/reviews/mean_price_envelope_independent_v1/review_manifest.json), JSON pointer `["files", 12]`. |
| [v3/work_logs/P3_09_2026-10-11_S1/reviews/structural_design/lifecycle_boundary_v1/source/v3/derivations/08_budget_selection_counterexample.md](../v3/work_logs/P3_09_2026-10-11_S1/reviews/structural_design/lifecycle_boundary_v1/source/v3/derivations/08_budget_selection_counterexample.md) | [Portable view](math/d9cf9e993ccf8cfd.md) | [Verified frozen-copy origin](../tools/document_origins.json): `v3/derivations/08_budget_selection_counterexample.md`. |
| [v3/work_logs/P3_09_2026-10-11_S1/reviews/structural_design/lifecycle_boundary_v1/source/v3/experiments/development.md](../v3/work_logs/P3_09_2026-10-11_S1/reviews/structural_design/lifecycle_boundary_v1/source/v3/experiments/development.md) | [Portable view](math/7e0fd37f20a150cd.md) | [Verified frozen-copy origin](../tools/document_origins.json): `v3/experiments/development.md`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/results_sections_1_5_review_v1/results.observed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/results_sections_1_5_review_v1/results.observed.md) | [Portable view](math/a8d1261b0acbde12.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/results_sections_1_5_review_v1/review_signature.json), JSON pointer `["source_bindings", 22]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/results_sections_1_5_review_v1/sections_1_5.observed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/results_sections_1_5_review_v1/sections_1_5.observed.md) | [Portable view](math/eb71038ccce0d7fa.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/results_sections_1_5_review_v1/review_signature.json), JSON pointer `["source_bindings", 23]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/source_snapshot/forecast_action_decomposition.reviewed.v1.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/source_snapshot/forecast_action_decomposition.reviewed.v1.md) | [Portable view](math/8b3378361470facf.md) | [Verified frozen-copy origin](../tools/document_origins.json): `v3/work_logs/P3_10_2026-10-11_S1/forecast_action_decomposition.md`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/claim_ledger_dispositions_review_v1/forecast_action_price_boundary_interpretation.reviewed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/claim_ledger_dispositions_review_v1/forecast_action_price_boundary_interpretation.reviewed.md) | [Portable view](math/89e1c9662f18d8ee.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/claim_ledger_dispositions_review_v1/source_bindings.json), JSON pointer `["reviewed_snapshots", 2]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/claim_ledger_dispositions_review_v1/results_section4_4.reviewed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/claim_ledger_dispositions_review_v1/results_section4_4.reviewed.md) | [Portable view](math/a9929d4d2add1a98.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/claim_ledger_dispositions_review_v1/source_bindings.json), JSON pointer `["reviewed_snapshots", 1]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/addendum_closure_v1/source_snapshot.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/addendum_closure_v1/source_snapshot.md) | [Portable view](math/6a3e9d73e2a584ef.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/signature.json), JSON pointer `["files", 2]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/source_snapshot/v3/work_logs/P3_10_2026-10-11_S1/decision_service_interpretation.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/source_snapshot/v3/work_logs/P3_10_2026-10-11_S1/decision_service_interpretation.md) | [Portable view](math/e80aaf771e6e8088.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/signature.json), JSON pointer `["files", 32]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/interpretation_claim_review/source_snapshot/official_results.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/interpretation_claim_review/source_snapshot/official_results.md) | [Portable view](math/3cd7027fdc29052c.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/signature.json), JSON pointer `["files", 14]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/readable_figure_review_v1/results_section_4_4_snapshot.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/readable_figure_review_v1/results_section_4_4_snapshot.md) | [Portable view](math/44731c902d6792ac.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/signature.json), JSON pointer `["files", 27]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/source_and_data/v3/work_logs/P3_10_2026-10-11_S1/forecast_action_price_derivation.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/source_and_data/v3/work_logs/P3_10_2026-10-11_S1/forecast_action_price_derivation.md) | [Portable view](math/ae90efb1d2aa9670.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/signature.json), JSON pointer `["files", 39]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_source_review_v1/theorem_subreview/source_snapshot/forecast_action_price_derivation.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_source_review_v1/theorem_subreview/source_snapshot/forecast_action_price_derivation.md) | [Portable view](math/7cfdad86b57b66f4.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_source_review_v1/theorem_subreview/signature.json), JSON pointer `["files", 3]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_mechanism_review_v1/source_and_data/forecast_action_decomposition.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_mechanism_review_v1/source_and_data/forecast_action_decomposition.md) | [Portable view](math/0b8f838435d95008.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_mechanism_review_v1/initial_snapshot_manifest.json), JSON pointer `["files", 1]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/joint_geometry_review_v1/source_and_data/joint_report_geometry.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/joint_geometry_review_v1/source_and_data/joint_report_geometry.md) | [Portable view](math/2c4a46fdc456ebbf.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/joint_geometry_review_v1/initial_snapshot_manifest.json), JSON pointer `["files", 1]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/joint_geometry_source_review_v1/source_snapshot/v3/work_logs/P3_10_2026-10-11_S1/joint_report_geometry.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/joint_geometry_source_review_v1/source_snapshot/v3/work_logs/P3_10_2026-10-11_S1/joint_report_geometry.md) | [Portable view](math/89251e31751ee62d.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/joint_geometry_source_review_v1/source_hashes.json), JSON pointer `["sources", 0]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/results_section6_review_v1/results_snapshot.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/results_section6_review_v1/results_snapshot.md) | [Portable view](math/eab80af06cf70be4.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/results_section6_review_v1/signature.json), JSON pointer `["artifacts", 1]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/assumption_matrix_v1/output/source_snapshots/R__REVIEW.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/assumption_matrix_v1/output/source_snapshots/R__REVIEW.md) | [Portable view](math/09011f12ecea0d83.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/assumption_matrix_v1/output/matrix.json), JSON pointer `["source_bindings", "R"]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/final_synthesis_review_v1/results.q1_clarified.reviewed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/final_synthesis_review_v1/results.q1_clarified.reviewed.md) | [Portable view](math/5fb575034ff5cd0b.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/final_synthesis_review_v1/manifest.json), JSON pointer `["artifacts", 8]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/final_synthesis_review_v1/results.reviewed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/final_synthesis_review_v1/results.reviewed.md) | [Portable view](math/806dcc58249c497f.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/final_synthesis_review_v1/record_comparison_01/results.json), JSON pointer `["source_bindings", 0]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/run_01/principal_derivation.reviewed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/run_01/principal_derivation.reviewed.md) | [Portable view](math/f392117fa866b4b6.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/manifest.json), JSON pointer `["artifacts", 5]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/run_02/principal_derivation.reviewed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/run_02/principal_derivation.reviewed.md) | [Portable view](math/8b4db869c863efcf.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_observation_review_v1/manifest.json), JSON pointer `["artifacts", 8]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_review_v1/derivation.reviewed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_review_v1/derivation.reviewed.md) | [Portable view](math/f7539a2defd3c50d.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/gate_architecture_review_v1/manifest.json), JSON pointer `["bindings", 0]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/results_sections_6_7_review_v1/results.reviewed.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/results_sections_6_7_review_v1/results.reviewed.md) | [Portable view](math/03e9c7e46868ee99.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/results_sections_6_7_review_v1/manifest.json), JSON pointer `["bindings", "reviewed_draft"]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/retrospective_report_derivation_reviewed_v1.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/retrospective_report_derivation_reviewed_v1.md) | [Portable view](math/761355c60453ade2.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/review_manifest.json), JSON pointer `["files", 34]`. |


### Historical scientific review artifacts (20)

| Source | Readable edition | Scientific preservation basis |
| --- | --- | --- |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/cached_service_independent/cap_review.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/cached_service_independent/cap_review.md) | [Portable view](math/e38dcee35343ea7c.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/evidence_manifest.json), JSON pointer `["files", 463]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/cached_service_v1_1/review.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/cached_service_v1_1/review.md) | [Portable view](math/101d39ce2f8727a6.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/reviews/mean_price_envelope_independent_v1/inputs/prior_individual_review/plan.json), JSON pointer `["sources", 51]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/economic_comparator_review_v2.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/economic_comparator_review_v2.md) | [Portable view](math/eeba099552bd5066.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/evidence_manifest.json), JSON pointer `["files", 532]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/review.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/review.md) | [Portable view](math/cc61afaf66b55ff9.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/evidence_manifest.json), JSON pointer `["files", 537]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/u08_comparator_qualification.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/u08_comparator_qualification.md) | [Portable view](math/713617aeecc3bc29.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/evidence_manifest.json), JSON pointer `["files", 557]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/mean_price_envelope_independent_v1/review.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/mean_price_envelope_independent_v1/review.md) | [Portable view](math/78153eec4c8c3bb3.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/reviews/mean_price_envelope_independent_v1/review_manifest.json), JSON pointer `["files", 17]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/price_envelope/review.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/price_envelope/review.md) | [Portable view](math/ea1e3e8aa4925c0d.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/reviews/mean_price_envelope_independent_v1/input_manifest.json), JSON pointer `["files", 10]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/reporting_independent/funding_witness_review.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/reporting_independent/funding_witness_review.md) | [Portable view](math/afd3bbfbb53092a0.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/evidence_manifest.json), JSON pointer `["files", 677]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/reporting_independent/hard_hash_cap_review.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/reporting_independent/hard_hash_cap_review.md) | [Portable view](math/ec759236e96f34f4.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/evidence_manifest.json), JSON pointer `["files", 678]`. |
| [v3/work_logs/P3_08_2026-10-10_S1/reviews/reporting_independent/v2_analysis.md](../v3/work_logs/P3_08_2026-10-10_S1/reviews/reporting_independent/v2_analysis.md) | [Portable view](math/50a4782a56739764.md) | [Scientific record](../v3/work_logs/P3_08_2026-10-10_S1/evidence_manifest.json), JSON pointer `["files", 743]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/ordinary_dominance_boundary_A1.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/ordinary_dominance_boundary_A1.md) | [Portable view](math/bfd4f855d26e2f0e.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/broker_reconstruction/ordinary_dominance_boundary_A1.json), JSON pointer `["source_bindings", 0]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/review.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/review.md) | [Portable view](math/fa9bd77f5ea18819.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/signature.json), JSON pointer `["files", 26]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/theorem_rank_source_review/review.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/theorem_rank_source_review/review.md) | [Portable view](math/5b3bce3bdda87b46.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/decision_service_review_v1/theorem_rank_source_review/signature.json), JSON pointer `["files", 0]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/review.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/review.md) | [Portable view](math/5694c728b69c2cd9.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/forecast_action_price_review_v1/signature.json), JSON pointer `["files", 38]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/REVIEW.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/REVIEW.md) | [Portable view](math/13aff91f9326f380.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/review_manifest.json), JSON pointer `["review"]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/final_synthesis_review_v1/REVIEW.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/final_synthesis_review_v1/REVIEW.md) | [Portable view](math/46eaafed87439b76.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/final_synthesis_review_v1/manifest.json), JSON pointer `["artifacts", 0]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/supplemental_reporting_note_v1.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/supplemental_reporting_note_v1.md) | [Portable view](math/c148058a5318e51d.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/review_manifest.json), JSON pointer `["files", 41]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/REVIEW.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/REVIEW.md) | [Portable view](math/ef7ed581cb63f3fe.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/review_manifest.json), JSON pointer `["review"]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/reviewed_transfer_failure_derivation.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/reviewed_transfer_failure_derivation.md) | [Portable view](math/5e1b59cc3e219994.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/transfer_review_v1/review_manifest.json), JSON pointer `["files", 2]`. |
| [v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/width_decomposition_review_v1.md](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/width_decomposition_review_v1.md) | [Portable view](math/68adc1b8823b1fab.md) | [Scientific record](../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/review_manifest.json), JSON pointer `["files", 44]`. |
