# Repricing acquired repair proofs under changed weights

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT. [Implementation](maxsat_reprice.py),
[profiles, invoices and diagnostic](maxsat_reprice_results.json).
Input: the conventional arm's [weighted repair evidence](maxsat_repair_results.json).
All original artifacts are preserved. This adapts established branch-proof
and incumbent reasoning to a paid counterfactual value interface; it is not
a new branch-and-bound principle or a readiness claim.

## What can change while the proof remains useful

Keep the hard clauses, soft-clause identities/order, variable interpretation
and repair assignments fixed. Only their weights change from the original
positive integer vector w0 to a **nonnegative** integer vector w. Objective
costs may change; hard feasibility does not. Source and input-result hashes
bind this restriction. Different hard clauses or soft-clause meanings require
a separate checked bridge and are outside this transport rule.

A checked negative branch tree covers every Boolean assignment. Each leaf is
either a hard-clause conflict, or carries a set A of soft clauses already
forced false on that branch. Write a_A for its zero/one incidence vector.
Any hard-feasible assignment reaching that leaf has new cost at least
`a_A dot w`: additional violated clauses cannot reduce cost because w>=0.
Hard-conflict leaves contain no feasible assignment, so they can be omitted.
Consequently the old tree T supplies the new lower profile

```text
L_T(w) = min_(soft leaves A of T) a_A dot w.
L(w)   = max_T L_T(w), or zero if no negative tree is retained.
```

A hard-only refutation would contradict the source's checked feasible public
witness; this implementation rejects that inconsistency rather than silently
assigning an infinite bound. The lower profile need not equal the new optimum:
some leaf assignments may have no feasible completion, and the minimum ignores
that additional structure.

Each retained feasible witness x supplies its checked soft-violation vector
a_x. A single objective pass compiles that vector. Subsequent repricing is
a charged dot product, giving

```text
U(w) = min_(retained feasible x) a_x dot w.
L(w) <= C*(w) <= U(w).
```

The selected witness actually attains U(w). At replacement price p, use that
repair when U(w)<p and otherwise replace. The resulting action regret is at
most `min(U(w),p)-min(L(w),p)`. Proofs now carry useful bounds through a declared
change in value weights, rather than just repeating an old SAT answer.

All archived witnesses are available to every control. A witness dominated
under w0 can become cheapest under w, so the old single-incumbent compression
is not valid for arbitrary repricing. No winner changed in the five edits
below; this remains a structural limitation rather than an observed gain.

## Scalar controls and a predictable dominance relation

Let L_old be the already checked optimum lower bound at w0. The requested
coarse control is

```text
L_add(w) = max(0, L_old + sum_j min(0,w_j-w0_j)).
```

The stronger scalar control also uses ordinary homogeneity/relative weights:

```text
r = min_j w_j/w0_j.
L_scalar(w) = max(L_add(w), ceil(r*L_old)).
```

Fractions and integer rounding are exact. Both controls use the **same** U(w)
and witness compilation. In particular, uniform doubling should not count as
a structural advantage over this scalar control.

Tree reuse dominates these two lower bounds. Choose a retained tree whose
original budget gives L_old. Every soft leaf has original weight at least
L_old. Its new weight is at least both `L_old+sum min(0,w-w0)` and `r*L_old`.
Taking the leaf minimum, then the tree maximum, preserves those inequalities.
Rows with L_old=0 are covered by nonnegativity. Dominance concerns bound
precision; it does not imply that compiling or evaluating the tree is cheaper.

## Declared edits and actual results

Before exact new optima were evaluated, the script declared five recipes:
identity; uniform doubling; doubling the first four weights; zeroing the last
four; and a one-position cyclic shift to the right. The original weights are
(1,2,3,1,2,3,1,2). All 16 original rows and their conventional-arm evidence
remain included. No new solver was invoked.

| Weight recipe | Mean regret bound at p=6, additive | Scalar with ratio | Retained trees | Rows certified to regret <=1, scalar/tree |
|---|---:|---:|---:|---:|
| Identity | .6250 | .6250 | .6250 | 16 / 16 |
| Uniform doubling | 2.6250 | 1.1250 | 1.1250 | 7 / 7 |
| Double first half | 1.3125 | 1.3125 | .9375 | 8 / 10 |
| Zero last half | 1.0000 | 1.0000 | .5625 | 13 / 15 |
| Rotate right | 2.9375 | 1.8125 | 1.7500 | 7 / 7 |

The tree lower bound strictly improves over the stronger scalar control on
five rows for doubling the first half, four for zeroing the last half and one
for rotation. Identity and uniform scaling give no additional precision.
This keeps an easy scaling improvement from being mistaken for new structural
information.

A concrete positive consequence appears when the last four weights become
zero. For row 8, the old optimum interval was [3,4]. The scalar controls now
give lower bound zero. The retained proof yields lower bound one, and the
retained repair costs one: **the changed-weight optimum is certified exactly
without a new solver purchase**. Rows 14 and 15 similarly obtain new exact
intervals [1,1] and [3,3] from the same old receipts. These facts follow from
the transported bounds; the exhaustive diagnostic is corroboration, not an
input needed to obtain them.

All methods have identical feasible witnesses and therefore identical actions
in this comparison. The positive gain is tighter warranted regret and value
information. For two row-requests in each of the first-half-doubling and
last-half-zeroing cases, the tree profile meets tolerance one at price six
where the scalar profile does not. This makes another purchase unnecessary
for those requests; it does not measure how expensive a scalar controller's
next purchase would have been.

## Paid compilation, repricing and separate diagnosis

The service compiles 29 archived feasible witnesses and 18 negative trees.
Deduplicating identical supports within each checked tree leaves 147 leaf
masks. Shared source/witness admission, hard checking and objective-vector
compilation cost **4,374 units**. Only the tree method pays the additional
**3,601 units** for original-proof rechecking and leaf compilation. Scalar
controls may trust the previously checked scalar archive receipts; they are
not charged for tree work they do not need.

Per recipe, common witness repricing/reporting costs 427 units. The additive
control costs another 352; the ratio refinement adds 384; tree evaluation and
regret reporting cost 1,856. Across the five recipes, including setup:

| Method | Additional service units |
|---|---:|
| Additive scalar | 8,269 |
| Additive plus ratio | 10,189 |
| Retained-tree profile | 19,390 |

The original conventional acquisition bill of 77,646 units is common historical
cost and is not erased or counted again here. These new invoices are an
explicit operation tariff, not an economic currency or a proof of net benefit.
The extra 9,201 units over the stronger scalar method must be repaid through
useful precision, avoided future acquisition or sufficiently many requests.
Compilation amortizes; the higher per-recipe evaluation bill remains.

The script saved completed profiles before invoking a separate exhaustive
diagnostic. That diagnostic considered 4,096 assignments once across the
fixed hard instances, then repriced every hard-feasible assignment under all
five recipes. Its separate bill is **121,664 units**. Every transported interval
contains its diagnostic optimum, and the identity recipe agrees with the old
checked exact reference. No diagnostic optimum or witness enters a profile.

Command: `python v3/discovery/s05/maxsat_reprice.py`; existing outputs cannot
be overwritten. A compile-only preflight preceded this execution. This is
same-model constructive checking, with all coefficient profiles, source hashes,
price bounds and invoices retained; no broader confirmation is claimed.

## Further constructive options

For nonnegative weights, componentwise dominated witness-violation vectors can
be removed while preserving U(w) for every permitted edit. Similarly, a soft
leaf support that strictly contains another support in the same tree cannot
minimize its nonnegative weighted sum. Paid Pareto/subset reduction may shrink
the profiles; this prototype only removes identical leaf masks.

More strongly, any hard-feasible violation mask contains at least one leaf
support from **every** retained tree. Minimizing new cost subject to all those
necessary conditions can strengthen `max_T min_leaf` by keeping their joint
requirements. That introduces another optimization bill and is a candidate
for the next constructive comparison, not an additional experiment performed
here. Changed-weight queries give the program a concrete way to connect
checked proof reuse, counterfactual value changes and paid action precision.
