# F13: scientific and staged reasoning case results

Contributor: **Codex (GPT-6)**, October 4, 2026.
**Technical case-study scope complete; novelty NOT YET SUPPORTED.**
[Derivations](../derivations/06_case_studies.md),
[literature](../literature/05_f13_case_comparison.md),
[work and timing](../work_logs/F13_2026-10-04_S1.md).

## What the two cases establish

The scientific family executes quadrature on an explicit degree-six model,
derives error from its coefficients and prices actual sample counts. Shared
discrepancy gives a native replacement budget **-4873/770000** for the stated
1/12-node comparison, even when the common error coordinate is unbounded.
Withdrawing joint evidence or demanding absolute adequacy changes the answer.
Ordinary interpolation and support functions obtain the same bounds.

The reflective family actually runs bounded versions of the native proof
procedure, records current receiver outcomes, selects a policy from that
evidence, and executes it on later current requests. Under two declared
populations it selects a three-version cascade costing **35/4** or a complete
fallback costing **9**. Unresolved search never means a false object theorem.
A source-aware ordinary solver emits only **5/6 expected proof nodes** on
those populations, so the example supplies no emitted-work advantage. These
counts are a proxy, not total measured runtime or statistical calibration.

Optional derivations add noisy acquisition, consumer-specific retention,
weighted/zero-cost information ranks, sharp mean-profile ambiguity, physical
error optimization, drift and confidence frontiers, and cost-rounding regret.
The useful fallback comparison has a stronger ordinary simplification:
**20q + 30rho + 4alpha <= 1/4** under the stated source/drift assumptions.
It needs a mean bound, not the complete tail distribution. The equal-cost
rank has a direct maximal-chain antecedent. These findings sharpen the next
question but do not yet support a distinctive project contribution.

## Executable coverage and limitations

| Scope | Observed result |
|---|---|
| Initial 22 native/scientific/cascade tests | Passed on bundled Python 3.12.14 before the two later native additions. |
| Two added native tests | Passed together in one isolated run: eight actual calibration/selection/deployment scenarios and 20 compiled risk-threshold checks. |
| Final 16 ordinary retention/acquisition/refinement tests | Passed together on the first attempt. |
| Intermediate combined 35-test suite | All three attempts crashed with native access violations; no combined pass. |
| Optional larger `case_study` generator | All three attempts failed; no complete results JSON exists. Later deployment refactoring was tested only in the smaller scope above. |
| Repository-wide suite | Not run during F13. The F12 1,523-test pass remains historical. |

The 40 distinct focused tests therefore have passing coverage in separate
scoped runs; this is not a claim that the final aggregate suite passed.
The scientific test covers 72 price/source queries over 36 parameter triples,
not 36 independently sampled physical systems. The rank checks use direct
world execution through k=4: 28 price/penalty cases for means, differences and
distributions, plus eight all-subset matrices. Positive-price reconstruction
is checked on 112 point-mass summaries and 1,760 order costs. General results
rest on the written proofs, not these finite checks.

System Python 3.13 failed on three initial attempts. Bundled Python also
experienced failures: access violations and one unexpected
`tuple_iterator`-not-callable exception in existing validation code. All logs
are retained under [the session directory](../work_logs/F13_2026-10-04_S1/).
No hardware/interpreter cause is established. A host exception is a failed
experiment, not a silently recoded outcome in the development population.
No F05/F06/F07 kernel change, CI pass, frozen challenge or deployment claim is
part of F13.

## Reproduction

From the repository root, use a known Python environment:

```text
python -X faulthandler -m unittest verification.test_v2_f13_cases -v
python -X faulthandler -m unittest verification.test_v2_f13_retention -v
```

The optional broad report can be attempted with a **fresh** output filename:

```text
python -X faulthandler -m v2.verification.case_study --json ../f13-reproduction.json
```

It refuses to overwrite existing output. That command has no successful F13
run on this host. Preserve failed attempts, cap retries, and do not stitch
partial outputs into a purported full pass.
