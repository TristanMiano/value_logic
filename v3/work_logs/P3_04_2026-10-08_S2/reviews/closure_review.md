# P3-04 S2 — mathematical and implementation self-review

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 8, 2026 UTC.
Review type: **self-review**, with separately programmed point/set oracles.
These are not independent researchers or blind tests. No native prover was run.
The source identities of the tested code are bound in each development manifest.

## Load-bearing invariants

**Selection.** Each current partial cell denotes every Boolean completion, not
just visited points. A hard formula with sound interval upper bound zero cannot
hold at any completion. The weighted lower rank sums only unavoidable positive
violations in each tier; its lexicographic value is below every completion's
rank. With an incumbent witness, pruning strictly above that incumbent cannot
remove any global minimizer. Equality must remain eligible. Replacing an
incumbent by a better witness cannot revive a previously strict-pruned case.
DFS branching partitions the parent; leaves are evaluated exactly. Induction
therefore retains all global optima until termination, including unvisited ties.
Finite caps and a fixed request are premises; every report is conditional on
trusted in-process state and the declared evaluator.

**Reports.** An incumbent proves nonemptiness, not necessarily global optimality.
If every eligible frontier lower rank is at least the incumbent, its rank is
optimal, but unseen ties may remain. A constant enclosure across the covering
family determines a value even before that rank is known, provided feasibility
has a witness. To refute universal support using an incumbent, however, that
incumbent must itself be optimal. Exact interval endpoints require optimal
endpoint witnesses unless the whole cover is constant. The tests exercise
both distinctions. A complete empty family reports infeasibility, not utility.

**Paired support.** Quote identity is kept in request metadata. Four-valued
support is hypothetical; the original Boolean metatheory still refutes an
explicit contradiction. Negation swaps channels; conjunction/disjunction
use the declared positive/negative rules. Atomic normality is hard except at
explicitly permitted exception sites. Normality-first positive penalties give
ordinary overlap when a normal admissible case exists. A framed contradiction
supports the antecedent and its positive conjunct while leaving the unrelated
flag unsupported; frame removal exposes two different losses. This is an
explicit nonexplosive semantics, not an independently established philosophical
selection rule.

**Arithmetic example.** Positive signed Horn closure retains all reference
signs and adds seeds and rule consequences. Monotonicity guarantees a least
closure. Under positive conflict penalties, every extra complementary sign
would strictly add a conflict, so the admissible least closure is uniquely
minimal. A forbidden conflict proves infeasibility for that rule/exception
policy. The separate truth-table reference validates each admitted arithmetic
rule at the supplied baseline; it does not establish arbitrary arithmetic rules.
The 2=3, 4=6, 0=1 example exposes how cancellation changes the needed exception.

**Structural changes.** Each admitted table is topologically evaluated;
interventions replace only named equation outputs. Required rows are checked
for the declared current exogenous context and parent domains. The adapter
is not a solver for cyclic equations or a certificate of hidden contexts.
Routing uses a fixed original table, replacement, input/history and mask.
Predictors of the original do not follow a replacement without explicit routing.

## Current coverage map

| Manuscript result | Current support and implementation boundary |
|---|---|
| C04-1, C04-7 | Hand proofs plus independent deletion/violation and definitional-gate checks. One identity means one penalty. S2 composition tests verify the explicit Boolean normality adapter and scalarization preserve all minimizers. |
| C04-2–4 | Ordinary overlap/normality and fixed-frame proofs; paired-support fixtures and exact one-parameter affine-region checks. No arbitrary multi-parameter polytope solver is claimed. |
| C04-5–6 | Selector invariant above; 512 generated small requests, 2,928 stopping prefixes and special seed/tie/early-value cases. Independent point oracle establishes exact optima for those inputs. No general physical-runtime guarantee. |
| CE04-1 | Finite positive-weight/inclusion-minimal proof; 255 attained Boolean-profile families checked. Not equality for an arbitrary one fixed weight vector. |
| CE04-2–5 | Decoder ambiguity, witness existence, no-gap and consequence proofs. Independent set-valued support tables, ordinary overlap, centering, missing frame, bottom infeasibility and a rational-monotony gap countermodel checked. |
| CE04-6–10 | Sourcewise/global distinction, envelope, finite integer scalarization, rank-aware projection and material-MP boundary. Hand proofs plus explicit diagnostic witnesses; no source-probability model inferred. |
| CE04-11 | Least signed-Horn closure proof; 1,280 small cases against independent complete-state enumeration, plus three arithmetic policies. |
| CE04-12–14 | Surviving-minimum and approximate-rank proofs; restriction, correlated-policy and equal-error special cases. No monotone selected-source guarantee after arbitrary new hard constraints. |
| CE04-15, CE04-17 | Algebraic gate proof, global-Lipschitz obstruction, two affine branches with rational witnesses; 162 bounded numeric points and extreme unbounded-graph witnesses tested. These are not executions of the inherited native proof checker. |
| CE04-16 | Independent interval-rank proof; 512 boxed families and simultaneous-winner constructions tested. Correlated scores or score-dependent losses require their joint contract, not that formula. |

General logical implication from finitely many tests is not claimed. Hand proofs
remain hand proofs. Raw counts measure fixture coverage only; they are not
independent discoveries, learner performance or empirical counterpossible truth.

## Concrete scope and repair choices

The CNF compiler rejects arithmetic equality expressions; it does not silently
miscompile normality. The new supplement explicitly rewrites Boolean normality
`t+f=1` to XOR, verifies equality on every four-bit assignment of its 288 requests,
and checks each hard constraint, penalty vector and selected family. That
separate translation is part of the reconstruction evidence, not a new general
compiler feature. No code changes were needed after the first core run.

Pre-run inspection added a quotation-size cap before recursive paired
compilation and a Cartesian-table bound before table expansion. The delivered
core/snapshots contain those guards. Twelve invalid-input cases exercise
selected boundaries, but this is not a hostile remote-input service audit.
The search object and reports are mutable trusted Python objects; exact request
comparison detects ordinary scope changes, not adversarial corruption of live
state or tampering with arbitrary external numerical reports.

Resource counters record frontier pops, expression nodes, reports and seeds.
The cap on an `advance` call is a frontier-pop allowance. Parsing, allocation,
arbitrary-precision arithmetic, Python comparisons and serialization are not
all reduced to one metered primitive. No claim about total CPU/RAM, an optimal
scheduler or a paid-policy advantage is made.

## Disposition

No remaining blocker was found for **the stated finite semantics and current
replacement implementation**. A complete artifact should say so, while leaving
learned anticipation, calibration, BRIA/LI-style reward forecasting, policy
purchase and broader proof reuse to their own tasks. All-method identity
reconstruction rules out an encoding-only advantage; it does not prove that a
future narrowly identified synthesis contribution is impossible.

The source cards make substantial precedents explicit. P3-N01 remains NOT YET
SUPPORTED. P3-05 and P3-B–D were not started or passed here. Historical original
code/results/forecast remain missing; the new evidence closes a current
technical obligation without retrospectively claiming their recovery.
