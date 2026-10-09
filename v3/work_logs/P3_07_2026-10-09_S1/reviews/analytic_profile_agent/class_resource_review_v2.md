# Independent class-count and resource-path review, analytic profile v2

## Verdict and scope

**PASS. No mathematical label-count defect, unsupported within-class resource extrapolation, or hidden need for individual query labels was found in the frozen construction.** This conclusion is restricted to the declared five-prime domain, cold state with cache capacity zero, six fixed policies, default response budget, frozen sources, and their flat abstract operation model.

This was a same-model, targeted, nonblind review. Agent time was unmeasured, with zero principal Research90 credit. No adapter, policy, or whole-driver solver was rerun. No individual modular-power labels were computed. The independent arithmetic check read the saved analytic profile and compared algebraically derived category vectors, statuses, and feature sums. No next phase was attempted.

At the source read, all four root sources matched their frozen snapshots and recorded SHA-256 values:

| Source | SHA-256 |
| --- | --- |
| `07_computation_adapter.py` | `06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615` |
| `07_paid_reasoning.py` | `be6a575a9cf4de042823e4c8a2c03c31fffe70b4c8e047dd1680655d05f1e0ec` |
| `07_paid_reasoning_development.py` | `c8be07643e21c2f3eb7d5dc0df9128ff28bfecd48f8db299061f68d62561d2dd` |
| `07_analytic_profile.py` | `3acc5db6d65c6dcec75c3d7c46bd648d2f17371102211d0c15e3cdc787aae209` |

The reviewed evidence is `development/analytic_profile_run_v2/analytic_profile.json`, identity `a084e5129427a85fbaedf445205062ebdfb242a7a84b2b4cd9f3fb930ae0fa54`, together with its frozen sources and result metadata.

## Independent hand proof of the label counts

The query label is one exactly when a^n = 1 modulo p, where p is one of 17, 31, 47, 61, 97, n=(p-1)/2, and a ranges over all nonzero residues 1,...,p-1. These five numbers are prime: trial division by the primes at most their square roots suffices. The relevant divisors are subsets of 2, 3, 5, 7, and none divides its candidate. The runtime performs the stronger check of every integer divisor from 2 through the integer square root.

For an odd prime p, the nonzero square map has exactly n distinct values. Indeed, u^2=v^2 implies (u-v)(u+v)=0 in the field, hence v=u or v=-u; those are distinct for nonzero u. Every nonzero square s=u^2 satisfies s^n=u^(p-1)=1. The latter identity follows by multiplying the permutation of the nonzero field elements induced by multiplication by u and cancelling their nonzero product. Finally, the nonzero polynomial T^n-1 has at most n roots, by the factor theorem and induction on degree. Consequently exactly n of the p-1 nonzero residues give positive labels.

The residue a=1 is always positive. The residue a=p-1 is positive precisely when n is even. Removing those two residues leaves p-3 ordinary residues, with positive count n-1-1[n even] and negative count n-1+1[n even].

| p | n | Ordinary size | Ordinary positive | Ordinary negative | Positive at a=-1 |
| --- | --- | --- | --- | --- | --- |
| 17 | 8 | 14 | 6 | 8 | 1 |
| 31 | 15 | 28 | 14 | 14 | 0 |
| 47 | 23 | 44 | 22 | 22 | 0 |
| 61 | 30 | 58 | 28 | 30 | 1 |
| 97 | 48 | 94 | 46 | 48 | 1 |

There are 248 queries, 124 positive labels and 124 negative labels. The ordinary classes contain 238 queries, with 116 positive and 122 negative labels. The class weights in the analytic construction match the uniform law on the 248 queries; the primes are not being weighted equally.

## Why representative resources extend to every class member

All queries use the same version strings, so `Query.key_words` is 9. The query identifier is not part of this word tariff. All numeric and label admission checks succeed in the declared domain. Every policy creates a fresh adapter with an empty, disabled cache, so lookup always misses and storage never evicts or retains cache entries.

The shortcut eagerly charges all four branch tests and the parity operation. For a=1 or a=p-1 it returns a checked correct answer before any optional binary work. For every ordinary a it returns no answer, after exactly the same charged prefix. Neither shortcut path inspects an unacquired label.

In ordinary binary work, producer control depends only on the shrinking exponent and checker control only on the fixed exponent bits and cursor. The arithmetic operands do vary with a, but the declared bounded modular arithmetic tariff does not vary with their values. `observe_bits` is explicitly audit-only and cannot affect charging or control.

The producer invariant is result * base^exponent = a^n modulo p. Each odd/even binary step preserves it; at exponent zero the producer result is correct. The checker maintains checked = a^(processed leading-bit prefix), updating it by squaring and, for a one bit, multiplying by a. After all bits it produces the same a^n. Thus the final producer/checker comparison succeeds for every valid class member; its success does not require assuming a representative's label extends to the class. Shortcut correctness follows directly from 1^n=1 and (-1)^n.

Let L be the bit length of n and w its number of one bits. Reaching ready requires L producer iterations, one producer-to-checker phase transition, one checker setup, L checker iterations, and one final comparison: 2L+3 transactions. The counts are 11, 11, 13, 13, 15 for the five primes.

In category order (admission, solve, check, acquisition, storage, cache, forecast), all remaining categories being zero:

- Every checked shortcut has vector (34,6,7,10,29,1,2), total 89.
- Each ordinary zero-transaction policy has vector (34,6,0,0,0,1,2), total 43.
- Each completed ordinary policy has vector (85,7+6L+2w,5+6L+2w,10,51+5L,1,2), total 161+17L+4w.

All ordinary timeouts have admission 85, acquisition 0, cache 1, forecast 2; their changing solve/check/storage components follow the fixed exponent-prefix trace. In particular, cancellation adds the same public handle admission and one storage unit for every unfinished job.

| p | cap6 solve/check/storage | cap6 total and outcome | cap12 total and outcome | Full total and outcome |
| --- | --- | --- | --- | --- |
| 17 | 33 / 3 / 35 | 159, timeout | 233, checked | 233, checked |
| 31 | 39 / 3 / 35 | 165, timeout | 245, checked | 245, checked |
| 47 | 45 / 0 / 34 | 167, timeout | 222, timeout | 262, checked |
| 61 | 45 / 0 / 34 | 167, timeout | 222, timeout | 262, checked |
| 97 | 46 / 0 / 36 | 170, timeout | 215, timeout | 271, checked |

For p=47 and p=61, cap12 ends after all checker bits but before the final comparison, so an answer is correctly unavailable. For p=97, cap12 has checked only the first four exponent bits. No representative or class member can exhaust the default optional budget of 958 units: even the largest whole response uses only 271 units. Cancellation needs 18 units, within its separately reserved 65. The terminal-output unit is also reserved. These observations close the budget-dependent branches without assuming a base-specific success.

## Why individual labels are unnecessary for the class table

Every checked policy has zero false-positive, false-negative, and fallback features, by the correctness argument above. Every unresolved guessing policy has a fixed action: guess0 contributes the class positive count as false negatives; guess1 contributes the class negative count as false positives. Every other unresolved policy contributes exactly the class size to fallback. Resource features are the constant representative vector multiplied by class size. Therefore aggregate class counts suffice for every feature used by this fixed catalogue.

The source constructs, hashes and writes the analytic profile before opening the external reference rows. Its subsequent reference loop is a development falsification step. The construction does not use per-query labels from those rows. The selected-cost calculation uses the analytic means already formed.

An independent, source-import-free arithmetic check matched all 90 retained representative category vectors and completion statuses and all 1,260 class feature-sum coordinates. It also checked the 248/124/124 population totals. This check used closed-form operation counts and label-count formulas, not adapter execution or per-query power evaluation.

## Evidence boundary

The theorem and source-path argument are mathematical prerequisites, not work performed by a general runtime theorem checker. Human theorem/code development cost remains unquantified, as the evidence explicitly states. The declared abstract procurement bill is not a measured physical CPU bill. This subreview did not independently audit the entire outer procurement tariff, reference-file completeness, or selection arithmetic; those are separate from the class-count and path-constancy claim reviewed here.

Changing the policy catalogue, initial cache or pending-job state, input/version tariff, computation implementation, early-stop behavior, numeric cost model, response budgets, or query law requires renewed analysis. In particular, these classes would be insufficient for a new controller that conditionally guesses using a base-dependent intermediate result. No such controller is present in the reviewed catalogue.
