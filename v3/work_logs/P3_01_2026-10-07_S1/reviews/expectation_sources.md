# P3-01: expectation representations and contract review

Researcher: GPT-6 Astra Pro, `/root/p301_induction_sources`.
Date: 2026-10-07 UTC. Same-model internal, nonblind review. Scope: selected
primary definitions and a read-only check of the P3-01 contract; P3-02 remains
unstarted. No canonical edits or publication were made.

## 1. Compact primary-source import

Halpern and Pucella (2007), *Characterizing and Reasoning about Probabilistic
and Non-Probabilistic Expectation*.
[Author-hosted primary PDF](https://www.cs.cornell.edu/home/halpern/papers/expectation.pdf).

Finite worlds; real gambles measurable on algebra `F`.

| Representation | Functional | Characterization locator |
|---|---|---|
| Probability | `E_p(X) = sum_w p(w) X(w)` | Theorem 2.2: additive, affinely homogeneous, monotone; unique probability on `F` |
| Probability set | `lower E_P(X) = inf_(p in P) E_p(X)`; upper uses supremum | Theorem 2.4: super/subadditive, positively affinely homogeneous, monotone; canonical closed convex set |
| Belief function | Choquet expectation below, `nu = Bel` | Theorem 2.9: positive affine homogeneity, monotonicity, inclusion–exclusion (5), comonotonic additivity (6) |
| Possibility measure | Choquet expectation below, `nu = Poss` | Theorem 2.13: positive affine homogeneity, monotonicity, (6), indicator-max property (7) |

For increasing gamble values `x_1,...,x_m`,

\[
E_\nu(X)=x_1+\sum_{j=2}^{m}(x_j-x_{j-1})\nu(X>x_{j-1}).
\]

Indicators recover event values: `p(U)=E_p(1_U)`. Full functionals identify
closed convex hulls; generating sets may differ. Example 2.11: identical event
bounds, distinct gamble expectations. Section 3.2: expectation inequalities over
propositional gambles. Theorem 4.1: expectation/likelihood equivalence for
probability, belief and possibility; strict lower-expectation expressiveness
advantage for general credal sets.

## 2. Consequences for this project's contract — our assessment

The strongest immediate comparison is not a claim that a value must first be
defined as a probability. It is a functional interface whose algebraic behavior
can justify a representation by a law or a set of laws. Thus a future result
that merely recovers probabilities from all coherent linear cost queries would
not establish a new contribution. Equally, admitting nonadditive expectations
does not by itself establish a new uncertainty logic.

P3-02 should identify precisely what is retained and what can subsequently be
asked. The useful distinctions include a whole functional versus selected
queries; exact values versus bounded-precision records; the named event algebra
versus finer latent states; a credal set versus intervals for its individual
events; and available information versus information that requires paid access.
State the allowed class before claiming uniqueness or insufficiency. These are
problem-contract obligations, not a new derivation of P3-02's general theorem.

For a prospective nonlinear carrier, its laws must be named. An upper cost
bound need not be additive or obey negative affine homogeneity. A direct learned
cost estimate need not even be a coherent upper expectation. Calling all of
these an expectation without a type would conceal different inference rules.

### A separate fixture for the established distinction

The principal agent proposed this three-state fixture, inspired by HP's known
distinction but using different values. I checked it independently by exact
rational arithmetic. Let `Q` be the convex hull of

\[
\{(2/3,1/3,0),(0,2/3,1/3),(1/3,0,2/3)\},
\]

and `P` the convex hull of all six permutations of `(2/3,1/3,0)`.
Singleton probability intervals are `[0,2/3]` and doubleton intervals are
`[1/3,1]` for both sets. Empty and full events have their usual values. These
are all eight events, so no event interval distinguishes the two credal sets.

For task cost `g=(0,1,2)`, the three `Q` vertices give
`{1/3,4/3,4/3}`. The six `P` vertices give
`{1/3,2/3,2/3,4/3,4/3,5/3}`. Linear extrema are unchanged by convexification.
Thus

\[
\sup_{q\in Q}E_q(g)=4/3<3/2<5/3=\sup_{p\in P}E_p(g).
\]

Minimizing upper expected cost against the constant fallback `3/2` selects
`g` under `Q` and the fallback under `P`; both strict margins are `1/6`.
This is a distinguishing fixture for the project's decision duty, not a new
information obstruction or a superiority result for value logic. An ordinary
joint credal representation makes the same distinction. A comparator keeping
only event intervals may be weaker than the required O-PROB family.

## 3. Targeted audit of the current canonical draft

Read snapshots:

- `v3/foundations/01_problem_contract.md`, SHA256
  `39c50b4269cb3b9becb8d8d0d9793a63f848466b3b1727d952b459e72436aa21`.
- `v3/foundations/01_desiderata.md`, SHA256
  `81a6b8565826198a7af7893aa2a62295830caf9c24b4ecfde310bee918fb6851`.

**Finding:** no unambiguous technical false claim about LI, finite online
learning or the finite Boolean kernel was found in these inspected snapshots.
The contract already separates passive feedback from paid acquisition, rounds
from computation, complete theory models from an enumerated fragment, and
finite-expert regret from LI's language-wide criterion. The following concrete
clarifications would make later implementations harder to misinterpret:

1. **U03: name the expectation type.** Its example monotonicity condition is
   correct. If later expanded to more identities, specify whether the carrier
   is linear, lower, upper or merely a learned numerical estimate. Additivity
   cannot be required of arbitrary lower/upper functionals. The `S13 unread`
   description can be updated to the specific definitions actually inspected.

2. **U04: distinguish the hard evidence record from a forecast.** Exact
   next-update resolution is a valid proposed interface requirement. It is an
   additional design choice, not a finite-time property automatically supplied
   by the LI criterion. LI permits finite-prefix behavior that would fail this
   exact timing requirement. A separate truth/status record avoids suggesting
   that every soft forecast must already have adopted the hard coordinate.

3. **Contract §5.2 and U06: tag forecasts by prior resolution exposure.** Paid
   computation in step 2 may legitimately resolve the current query before the
   action in step 3. Such a decision is allowed and its cost should count, but
   its accurate forecast is not an anticipatory prediction. Save whether any
   current answer was received before the forecast, and use only the appropriate
   subset for a before-resolution claim. The existing timing prose points in
   this direction; an explicit field would close the ambiguity.

4. **O-FINITE plus O-ONLINE: declare the combined prediction operation.** A
   general projection or repair applied after a Hedge mixture need not preserve
   its scoring guarantee against raw experts. Either score the same transformed
   experts used to produce the mixture, or prove the particular postprocessing
   step cannot worsen the reported loss. The current requirement to retain all
   adaptation assumptions protects the contract; this is a concrete later
   obligation, not a discovered violation.

5. **Clerical:** the final line of the duty matrix contains
   `refuted,+narrowed`; the extra plus should be removed.

No gate or contribution pass follows from this review. The scientific hope can
remain a bounded useful combination with stronger information, accounting or
transport guarantees; the strongest relevant ordinary expectation machinery
should be included in its comparison.

## 4. Review boundaries and resource record

Read selected primary sections 2.1–2.4, 3.2 and 4, including the displayed
representation hypotheses and Example 2.11. Theorem 2.2's displayed proof was
read; the remaining long appendix proofs were not independently reconstructed.
The numerical decision fixture was checked by enumerating all eight events and
all vertex costs using Python's `fractions.Fraction`; every check passed.
This source is a substantial comparison input; this note does not infer a
novelty verdict for the still-unspecified future object.

Raw start observation: `2026-10-07T00:52:28.675076+00:00`,
`time.monotonic_ns() = 27517982227423`. The measured session span is recorded
below; concurrent subagent elapsed time is not added to the principal ledger.

Raw completion observation: `2026-10-07T00:57:20.564610+00:00`,
`time.monotonic_ns() = 27809871754482`. Observed subagent elapsed:
`291.889527059` seconds. This is not a separately measured engaged-mode total or
additive phase ledger credit. Token and billed resource totals are unavailable.
