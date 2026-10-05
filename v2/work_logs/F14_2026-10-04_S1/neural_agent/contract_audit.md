# Independent narrow audit of the F14 neural reporting contract

Scope: `analysis.py` against the implemented neural result schema. This audit
used development streams only. The auditor did not edit `analysis.py`, the
runner, or `neural.py`; the principal agent made the interpretation/guard
repairs. A new focused suite lives in
`verification/test_v2_f14_neural_contract.py`.

## Valid statistical components

For a fixed trained model and fixed discovered alignment, probability MAE,
decision disagreement, separation indicators and normalized decision regret
are bounded in `[0,1]`. The paired difference between two absolute probability
errors lies in `[-1,1]`. The two-sided Hoeffding radius for sample range width
`w` is `w*sqrt(log(2K/alpha)/(2n))` with the prospective finite-family cap.
No candidate-search factor is needed in the final union bound because all
search/selection uses independent discovery data and is frozen first.

The five equally sized strata are independent but need not be identically
distributed. Pooling their `n` rows yields a mean estimating the equal-weight
mixture of the five conditional-population means. Hoeffding applies to the
independent bounded rows with that target. Reusing those rows across different
metrics or hypotheses is permitted by the union bound.

Normal and incorrect-donor streams use distinct stream IDs for every role and
stratum. Incorrect donors are newly generated from an independent sample of
the same stratum donor marginal. A finite permutation of the intended donors
is not used, so the dependence problem identified in the earlier design
review is absent.

The exact largest absolute cost gap is `11/8`: at eta `3/4`, `cFN=2` and
`cFP=1/2`, the difference is `3/2-1/8=11/8`; the opposite extreme is symmetric.
Since wrong-action regret is either zero or the absolute gap, the implementation's
normalization by 1.375 places every row in `[0,1]`.

The all-rival `scale_separating` rejection rule implies that every retained
row satisfies every declared scale gap. The same-identity-subset comparison
on this stratum must therefore have exactly the full fixed denominator `n`.
It is not an adaptively filtered comparison. Other-stratum masked comparisons
remain diagnostic.

## Concrete findings and resolution

1. The original reporting guard accepted missing rival numerical-gauge records
   because it checked only the records that happened to be present. The revised
   guard requires all four hypotheses and inspects recorded transport errors,
   scales, permutation, tolerance and zero refits; copied success booleans
   cannot override a bad observed error.
2. The original scale reporting allowed a changed `total_pairs` denominator or
   a partial comparison with only the minimum count. The revised code requires
   full consistent total, separating and comparison counts before applying the
   fixed-population interval.
3. Actual intervention MAE and global ordinary-task MAE alone did not control
   baseline prediction error on each conditional intervention stratum. Before
   freeze, the principal added ten conditional-base intervals per model and
   prospectively changed the family cap from 510 to 560.
4. Supplied CLI configuration and manifest-bound configuration were separately
   validated but not bound to each other in the initially inspected runner.
   This was reported to the principal for a separate runner repair; the neural
   contract suite does not purport to verify that repair.

The initial contract test run deliberately exposed findings 1–2 with three
failed assertions. After the principal's repairs, all 14 focused contract
tests pass. A constant-array rounding test also verifies that harmless
floating-point differences between empirical mean and extrema are tolerated,
while inconsistent moments are rejected.

## Adjusted-effect bound and final claim count

For a given role/stratum, let the actual and high-level intervened probabilities
be `pI,hI`, and their base probabilities `pB,hB`. Pointwise,

```
|(pI-pB)-(hI-hB)| <= |pI-hI| + |pB-hB|.
```

Consequently, simultaneous upper bounds .05 on the actual intervention MAE
and .05 on the corresponding conditional-base MAE imply an adjusted-effect
MAE bound .10. Every positive g in the fixed family leaves the high-level base
probability unchanged, so the same ten conditional-base intervals serve all
four hypotheses. This derived sum bound consumes no additional confidence
row. It does not bound adjusted-effect RMSE or untouched-decoder drift, which
remain diagnostic.

| Confidence rows | Five-model count |
|---|---:|
| Uniform task MAE and normalized regret | 10 |
| Conditional base MAE, two roles and five strata | 50 |
| Intervention MAE, four hypotheses and two roles/five strata | 200 |
| Near/far decision disagreement, four hypotheses/two roles | 80 |
| Four matched controls, four hypotheses/two roles | 160 |
| Same-subset alternative-scale contrasts | 30 |
| Scale-separation frequencies | 30 |
| **Total** | **560** |

The code produces exactly 112 rows per model and rejects claim-family overflow.
The suite checks this count, interval width, mixture pooling, regret bound,
denominator consistency, conditional-base effects and all-family transport
guards. These remain statements conditional on the fixed models and declared
input generators, not a population guarantee across arbitrary training seeds.
