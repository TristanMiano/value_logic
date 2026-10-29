# Report check for P3-D-1

Codex (GPT-6), October 29, 2026. Editorial/package verification; no new
independent confirmation or empirical exposure.

The whole common scientific source was read against the claim/source map and
the original five-question contract. Section 5.1 required one explicit premise
repair: forecasts/experts in [0,1], finite nonnegative issue-time weights, and
fixed positive feature scales. These were already conditions of CF-2/CF-3 in
`v3/derivations/06_cost_forecast_refinement.md`, sections 1 and 3. The weighted
square term in the original proof explains the necessity. No result number,
equation, measured table value, bibliography entry or evidence level changed.

`python -X utf8 v3/report/build.py --pdf` was run with the pinned Pandoc 3.13
and Tectonic 0.17.0 executables documented in the build guide. It regenerated
both editions, bibliography and consistency hashes. The package verifier passed:
29 result/equation labels, 17 references, 151 local package links, V19's 24-file
freeze and 60-file exit seal, upstream bytes and all 30 recurrence rows intact.
The table extraction rechecked seven development rows, four cost rows and all
sixteen underlying cost records, without rerunning scientific experiments.

The actual PDF remains fourteen pages. All pages were rendered with PyMuPDF at
1.3 pixels per PDF point. Pages 1–7 and 14 were pixel-identical to the previously
inspected delivery. Changed pages 8–13 were each inspected at full render size:
the forecasting paragraph, statements/proofs, worked episode, two tables and
bibliography remain readable and unclipped. TeX reports no undefined citation
or reference, missing character, overfull box or underfull box. Existing harmless
inputenc/host Fontconfig advisories remain. No authoring artifact is inferred
from text extraction alone.

The current PDF SHA256 is
`ec602e98756e247fba63fb750d4eeb9c3c9d0898f12005b4ae8649aca4071b54`.
The [consistency manifest](../../report/consistency.json) binds both editions to
the updated common source. The original report delivery remains available at
PR23's merge commit. The later audit recommendation is recorded separately;
the paper's closing sentence remains its P3-12 readiness recommendation.

The accounting check initially exposed two supported historical formats the
new reader needed to handle: s01's indexed mode disposition and s05's explicitly
recorded partial-interval exclusion. The reader was corrected, then all 2,324
closed segments reproduced their saved effective totals. Historical clocks and
scientific records were not edited to make the check pass.
