# P3-01: CB05 and selection-error delta review

Reviewer: **GPT-6 Astra Pro**, `/root/p301_induction_sources`.
Date: **2026-10-07 UTC**. Same-model internal, nonblind review.
Scope: new CB05, S09 updates, main contract §§6.1/7, and the new CB03
selection-error witness. No canonical/control edits, executable tests, clock
actions or principal time credit. The whole-contract review is not reopened.

**Disposition:** the new mathematical and source-scope statements are mutually
consistent. One small request-interface addition would make the newly stated
decision semantics explicit to a later implementer.

## Cross-document consistency

CB05's parameter family is the convex hull of the two endpoint laws in the
source note. Its separately ranging conditional probabilities retain a shared
sum constraint in the global family. S09 correctly limits the concatenation
statement to the source's natural extension of local assessments; CB05 does
not present its different global family as a counterexample to Theorem 7.
Theorem 7's selected source scope and the fixture arithmetic were already
independently reviewed in `imprecise_tree_review.md`; I checked the canonical
wording against that review without a new primary-source import.

The named decision is minimizing worst-case expected loss **at the root with
commitment**. The same original family can support a different newly made
conditional choice after observing `X`. This is consistent with main §6.1's
new distinction and is not a contradiction in the expectation calculation.
The affine ordinary reconstruction also retains the same coupling, so no
notation-based superiority is claimed.

Main §7 and S09 consistently distinguish the positive-probability condition
for the ordinary ratio rule from the nonempty-event condition for the inspected
conditional-price interface. Neither supplies empty-contradiction semantics.
The source index clearly supersedes its earlier abstract-only S09 status only
for the selected inspected passages and retains the proof/runtime limitations.

## One concrete interface addition

Main §6.1 already requires criterion and timing in prose. However, the §7 CF
tuple and `01_contract.v1.json` request fields do not explicitly distinguish an
enforced earlier commitment from permission to choose again. A creation time,
conditioning history, loss function or counterfactual operation alone does not
determine that service.

Minimal addition to the common request requirement:

> Where an action or policy recommendation is requested, specify the decision
> criterion, the information available at choice, and whether an earlier
> commitment is enforced or conditional reoptimization is permitted.

Mirror this in the machine-readable request fields and, when a counterfactual
request asks for a decision, in its request fields. A pure value query can mark
the decision service inapplicable. The response should identify which declared
service it answered. No new optimization algorithm or general dynamic-consistency
theorem is needed to add this field.

This is the only requested delta correction. It makes the existing CB05 warning
operational rather than relying on a later reader to infer policy semantics
from timestamps.

## CB03 selection witness

The finite witness was absent from the composition file assessed under the
previous readiness hash `7c03662d3e717d34b3f9b3c7d516f5c4af5cf38e11068143cf21265c1ef8ca72`.
Its current arithmetic is correct by inspection: a bad selected candidate
occurs iff at least one independent underestimation occurs, giving
`1-(19/20)^2=39/400`; each such event incurs regret `1/2`, giving `39/800`.
The exact fallback has zero estimation error. Thus separate 95-percent
fixed-action coverage does not give 95-percent selected-action coverage.
The existing union-bound discussion is consistent with this example.

The candidate costs are explicitly fixed for analysis but not supplied as
resolved inputs to the chooser. The fixture therefore does not instruct an
agent to ignore known costs. It is correctly labeled an elementary selection
counterexample, not a learner, empirical performance result or new bound.
The verification paragraph correctly excludes it and CB05 from the earlier
eleven-group numerical run.

## Assessed hashes and retained status

| File | SHA256 |
|---|---|
| `01_composition_boundaries.md` | `d60fc69e48d4914140c16822bd2f25beabf5693d90382effbfe1a9d85046292e` |
| `01_source_contracts.md` | `14e27e4e85ae1d0a708522fd4a52c1fbe99bbc3a14d6965ca599b096fc7a6879` |
| `01_problem_contract.md` | `e2e2a31518fb9b3539731970adf67b8d5d64d0ef5d5f210ff2866e3e81868a26` |
| `01_contract.v1.json` | `d343e0d46de8187bc114c4857afbb3a3eb057b1167925dcddd1f37c1f6dbefa3` |
| `reviews/imprecise_tree_review.md` | `2ae7344dcd93a97b8a86c737d88a0b44f1df7fb7f68a90efafb9a5d6f58556d5` |

P3-N01 remains **NOT YET SUPPORTED**. This delta review changes no task-floor,
gate or later-task status and supplies no clock credit.
