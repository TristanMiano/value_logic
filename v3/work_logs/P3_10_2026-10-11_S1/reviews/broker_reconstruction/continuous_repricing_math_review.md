# Signed review: continuous fixed-record repricing intervals

Contributor: **ChatGPT (GPT-6 Astra Pro)**, agent `/root/freeze_review`.
Signed UTC: **2026-10-11T15:08:09.816389+00:00**. Scope: **P3-10 source-only mathematical interpretation review**. Zero principal Research90 minutes.

**Verdict: the proposed half-line intersection is correct.** It should remain an additional descriptive analytic extension of the sealed fixed paths. It does not replace the frozen reporting grid, re-execute a controller, or extrapolate the native-price catalogue.

## Exact statement

Within one fixed comparison cell (same family, public populations and normalized task stakes), write the candidate objective as `J_c(λ) = a_c + λ b_c` and each required ordinary objective as `J_i(λ) = a_i + λ b_i`. Here `a` is the frozen hierarchical mean normalized action loss and `b` is the same hierarchical mean of each episode's cold bill divided by its scheduled horizon. Both are exact rationals. The population/seed hierarchy applies to each whole configuration before the catalogue minimum.

For a finite nonempty catalogue, a practical advantage of at least `ε > 0` holds precisely when

`min_i J_i(λ) - J_c(λ) ≥ ε`, equivalently `∀i: (a_i-a_c) + λ(b_i-b_c) ≥ ε`.

Let `d_i = b_i-b_c` and `r_i = a_i-a_c`. Each condition is:

| Slope difference | Constraint |
| --- | --- |
| `d_i > 0` | `λ ≥ (ε-r_i)/d_i` |
| `d_i < 0` | `λ ≤ (ε-r_i)/d_i` |
| `d_i = 0`, `r_i ≥ ε` | No additional constraint |
| `d_i = 0`, `r_i < ε` | Empty feasible set |

Intersect these sets with `λ ≥ 0`. For the non-strict practical cutoff, finite endpoints are closed. The answer is an interval, a singleton, an unbounded interval, or empty; it cannot be several disjoint intervals. A singleton where lower and upper bounds coincide must be retained.

For strict advantage, replace the conditions by `r_i + λ d_i > 0`. Zero-slope conditions require `r_i > 0`; nonzero slopes impose strict half-lines. Keep endpoint inclusion flags when intersecting them. The domain endpoint **λ = 0 can still be included** if every strict comparison already holds there. For example, a constant positive advantage gives `[0,∞)`, not `(0,∞)`. A tie with an ordinary line at a finite boundary excludes that boundary from strict advantage.

## Identical ordinary aliases

Include the candidate's ordinary-identical fixed path as a comparator. Its difference has `r_i = d_i = 0`. The condition `0 ≥ ε` fails for every positive ε, and `0 > 0` also fails. Thus **all positive practical and strict-advantage intervals are empty** in the catalogue containing that alias. This does not add an independent execution; it preserves the declared exact implementation identity.

## Scope conditions

All required configurations must have complete valid denominators and known relevant bills for the original full-catalogue positive claim. Omitting an unavailable required comparator and intersecting only the remaining complete lines would instead describe a restricted catalogue. Unknown interrupted outer public costs still withhold an end-to-end economic claim, even where the sealed completed-path inequalities hold.

Keep the fixed configuration and its original acquisition price attached to every extrapolated line. Repricing its recorded cost does not change its decisions, purchases or cache history. A native-price controller's eligible point remains its actual normalized native price; it is not a continuous policy family obtained by relabelling λ.

No final input, public result, private score or analysis output was read for this note. The main broker observer is unchanged by this review. This is not a P3-11 contribution assessment.
