# P3-01 — where component guarantees need a bridge

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: optional P3-01 comparison analysis, not a selected learner or frozen
experiment. The elementary diagnostics below are not novelty claims.

The [main contract](01_problem_contract.md) combines forecasting, computation
selection and checked revision. These services have different inputs and
different guarantees. Merely placing them in one system does not prove the
interfaces between them correct.

## CB01. Equal access is different from equal realized histories

A paid-reasoning comparison supplies the same initial information, query
process, permitted computations, observation rules, prices and hard budgets.
Each method can then buy different computations and receive different results.
For method `M`, write `H_t^M` for its own acquired history. Its next choice
depends on that history; it has no free access to another method's purchases.

A replay comparison instead supplies an identical recorded history to two
forecasting or decision modules. That can isolate a representation or update
effect. It is a different question from comparing the acquisition policies
which would have generated their histories. Charge common information as a
common input in the replay, and do not attribute its acquisition to a policy
that did not select it.

Replay either attaches the same historical acquisition cost to both modules
or excludes acquisition from both and labels its result conditional on the
supplied information. It does not mix those two accounting conventions.

**Finite diagnostic.** In a stipulated two-case metalevel model, an unknown
bit is equally likely zero or one. Guessing it wrongly costs ten. Both methods
can purchase an exact reveal for one; no other visible input reveals it.
Policy A buys, then guesses correctly. Policy B never buys and guesses zero
unless a label is already available. Their expected total costs are one and
five. If the evaluator gives B the answer purchased by A, but charges B zero
for access, B appears to cost zero. This apparent superiority comes from a
changed information contract, not from B's acquisition policy.

An ordinary optimal controller with the same stipulated law buys too and
matches A. Thus the fixture supplies no advantage for value logic. The law
and reveal are idealized diagnostic inputs; this is not a hardness claim
about a visible program or a learned value-of-computation model.

The later implementation must therefore identify each comparison as one of:

- A common-history representation/update comparison.
- A full policy comparison with equal access rules and separate acquisitions.
- An oracle-information diagnostic, explicitly outside the deployable budget.

Even in a full policy comparison, shared external evidence can arrive to all
methods by the same announced schedule. What is forbidden is silently turning
one method's private paid result into the other's free external evidence.

## CB02. Decision calibration has a consumer and population scope

S19 (Zhao et al., Definitions 1–4) compares the population-average losses
computed from a probability report with actual population-average losses for
a stated loss family and decision rules that use that report. It already
provides an ordinary language for decision-relative calibration. It does not
thereby promise correct probabilities on every individual input, permit every
context-dependent loss, or solve paid acquisition and missing feedback.

**Finite diagnostic.** Let a visible feature `X` be equally likely zero or one
and let the deterministic answer be `Y=X`. A forecast returns `p=1/2` on both
inputs. Every decision rule depending only on this report is constant (or has
the same declared randomization on both inputs). For every fixed loss
`ell(Y,a)`, its predicted average loss equals its actual average loss, because
the marginal distribution of `Y` is fair. This forecast is exactly decision
calibrated for those consumers, even though it ignores a feature which would
predict every answer correctly. Under zero-one guessing loss, its best fixed
action has loss `1/2`, while the rule `a=X` has loss zero.

There is no contradiction in the source's optimality proposition: `a=X` is
not a function of the constant report. The information supplied to the
consumer is part of the comparator. In P3-01, the strong ordinary method may
use every legitimately visible feature and cheap shortcut.

**Stakes can change the estimand.** In the same population, let known stakes
be `kappa(0)=1` and `kappa(1)=9`. The loss of always guessing zero is
`kappa(X)Y`. Using `p=1/2` gives predicted average loss

$$
\frac12\left(1\cdot\frac12+9\cdot\frac12\right)=\frac52,
$$

whereas its actual average loss is

$$
\frac12(1\cdot0+9\cdot1)=\frac92.
$$

The unweighted calibration statement did not include this feature-dependent
loss. The source explicitly fixes losses without direct dependence on `X`
and decision rules that see `X` through the report. A valid extension could
specify suitable conditioning, weighting or a richer report, but its theorem
would need those hypotheses. Calling the same number a cost does not supply
them. The example is an exact two-case calculation, not evidence against
the source's stated guarantee.

On actual support `Y=X`, the loss `kappa(X)Y` equals `9Y`. Replacing it by
that fixed loss also changes its extension to the forecast's simulated cases:
the fixed table predicts `9/2`, not `5/2`. Agreement of losses on actual cases
does not establish agreement on every case admitted by a fallible forecast.
This explains precisely why the weighted example does not contradict S19.

S19 also separates sample requirements from the inner optimization required
to find a calibration violation. Its practical search uses a relaxation. A
polynomial sample statement is not, on its own, a cheap exact audit under
the phase-three resource budget. No sample or optimization theorem is imported
into our finite logical problem merely by selecting this comparator.

## CB03. A proof about estimates needs a bridge to actual loss

Suppose a checker correctly certifies

$$
\widehat L(A)\le\widehat L(B).
$$

That is a statement about the typed estimate expressions. If their values are
one and two but the actual target costs are ten and zero, the algebraic proof
can be valid while choosing A is poor. Checking the arithmetic does not check
the forecast's adequacy. This is the inherited separation between a conditional
certificate and the evidence that connects its premises to deployment.

With jointly applicable, justified common-unit bounds
`|L(A)-Lhat(A)|<=epsilon_A` and
`|L(B)-Lhat(B)|<=epsilon_B`, a real bridge is

$$
L(A)-L(B)
\le \widehat L(A)-\widehat L(B)+\epsilon_A+\epsilon_B.
$$

It follows by adding the two error inequalities. A nonpositive right-hand
side warrants the comparison at that scope. If the error premise is a
population-average or high-probability statement, its quantifiers and failure
probability remain part of the conclusion; it cannot silently become a
pointwise guaranteed inequality. A changing interpretation, source, forecast
version or loss unit can also invalidate that premise and trigger lazy
rechecking or transport.

For a fixed compared pair, bounds with failure probabilities `delta_A` and
`delta_B` hold jointly with failure probability at most `delta_A+delta_B`,
by the union bound; independence is unnecessary. If the pair is selected
after inspecting noisy estimates, require uniform or selection-valid bounds
for that procedure. A certificate does not remove this selection condition.

**A finite selection witness.** Let two candidate actions have true cost one
and a fallback have known cost `1/2`. The true candidate costs are fixed for
this argument, not supplied as resolved facts to the choosing procedure.
Independently for each candidate, let its noisy estimate be one with
probability `19/20` and zero with probability `1/20`. The fallback estimate is
exact. Each fixed candidate separately satisfies

$$
\Pr\bigl(|\widehat L_i-L_i|\le1/10\bigr)=19/20.
$$

Choose the action with the smallest estimate, using either announced tie rule
when both candidates report zero. The chooser uses the fallback exactly when
neither candidate underestimates. Consequently its selected-action error
exceeds `1/10` with probability

$$
1-(19/20)^2=39/400,
$$

which exceeds the individual failure probability `1/20`. The four exhaustive
events have masses `361/400`, `19/400`, `19/400` and `1/400`: no bad estimate,
only the first, only the second, or both. Every event except the first selects
a cost-one action instead of the cost-one-half fallback. Expected regret in
this stipulated example is therefore `39/800`.

Nothing is wrong with the two fixed-action coverage statements. They do not
license a 95-percent statement for the selected action. A uniform bound,
an appropriate simultaneous correction, or a selection-specific analysis
could support a valid bridge. The example is an elementary failure witness
for the inference from marginal coverage alone; it is not a proposed learner,
a statistical performance finding or evidence that the method should ignore
legitimately known candidate costs.

This diagnostic is not a new uncertainty bound. Its purpose is to locate the
cross-component obligation a useful phase-three integration must discharge.

## CB04. A fair comparator family is not an oracle-selected winner

O-COMB specifies credible ordinary ingredients and concrete implementations
to compare. It does not mean selecting the best ordinary program after seeing
evaluation answers, or requiring value logic to outperform every classical
program. Concrete choices and any tuning belong to development and the later
freeze. An ordinary implementation may reproduce the candidate's algorithm;
that is informative equivalence evidence.

A state translation with matching actions, observations, costs and transition
rules supports a direct operational argument. If initial states correspond
and every paired step preserves correspondence, induction over the finite
history gives equal observable reports and total costs. Matching only the
numerical output on a few fixtures is much weaker. Changing input privileges,
decoding costs, allowed operations or future query services breaks the stated
translation contract and must be analyzed explicitly.

Equivalence can coexist with a modest useful synthesis, formal adaptation or
application. Such a contribution must identify the concrete added service or
guarantee and the closest prior construction. It is neither granted by shared
terminology nor ruled out merely because ordinary software can implement it.
The [composition review](../work_logs/P3_01_2026-10-07_S1/reviews/composition_and_contribution_boundary.md)
records the already proposed LI/controller combination and established
incremental checking. P3-N01 remains **NOT YET SUPPORTED**.

## CB05. A tree recursion can discard shared constraints

S09 already relates imprecise expectations to sequential prediction and local
tree models. Its concatenation theorem concerns the natural extension of its
stated local assessments. It does not promise that separate branchwise bounds
retain every constraint in a richer global model. The
[source reconstruction](../work_logs/P3_01_2026-10-07_S1/reviews/imprecise_tree_source.md)
and [independent check](../work_logs/P3_01_2026-10-07_S1/reviews/imprecise_tree_review.md)
give the precise import boundary.

In the finite diagnostic, `X` is fair, and a single unknown parameter
`theta` in `[0,1]` determines both conditional probabilities:

```
P(Y=1 | X=0) = 1-theta,
P(Y=1 | X=1) = theta.
```

For every admissible parameter, the root expectation of the cost `Y` is
`1/2`. Each conditional probability separately ranges over `[0,1]`, but their
sum is constrained to one. Independent branchwise upper expectations discard
this coupling:

$$
\max_{0\leq\theta\leq1}
  \left[\frac12(1-\theta)+\frac12\theta\right]=\frac12,
\qquad
\frac12\max_{0\leq\theta\leq1}(1-\theta)
 +\frac12\max_{0\leq\theta\leq1}\theta=1.
$$

With a constant fallback cost of `3/4`, minimizing worst-case expected loss
at the root chooses the `Y` action under the shared family and the fallback
under the larger independent local family. This decision comparison fixes
both its criterion and commitment timing. After observing a particular `X`,
the original conditional family also admits every probability in `[0,1]`;
a newly made conditional upper-loss choice can therefore prefer the fallback.
Changing that decision service is different from preserving the original
root commitment. Minimax regret is another distinct criterion.

The ordinary comparison can retain variables `a,b` with `0<=a,b<=1` and
`a+b=1`, then evaluate `(a+b)/2`. This instance is affine in the retained
coordinates, so the inherited numerical language can also express its
constraint and cost comparison. Neither implementation obtains a distinctive
advantage from the notation alone. A claimed efficient recursive interface
must retain the coupling, or declare its larger family and the resulting
conservatism. This is not a claim that every shared family has a cheap exact
recursive representation.

These are abstract finite Boolean-event assessments, conditional on the
specified family. They do not assert that two complete interpretations of a
fixed arithmetical sentence are both true possibilities, or supply a way to
compute an unresolved answer. The logical-information and resource contracts
remain necessary when applying this example to bounded reasoning.

## Verification scope

CB01–03 and CB05 are direct finite/arithmetic derivations written here, not outputs of
the earlier `finite_checks_1.json` run. The latter checks only its recorded
eleven groups. CB04 is a conditional simulation argument, not an implemented
compiler. These distinctions prevent the numerical assertion count from being
used as evidence for claims it did not test.
