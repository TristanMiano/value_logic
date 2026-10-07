# P3-02 principal mathematics audit — sections 1–11

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Review type: **internal same-model, nonblind adversarial review**.
The reviewer previously helped reconstruct several of these results and
does not claim independent-model corroboration or additional principal
research credit. No primary text, clocks, ledger, status or gate is changed
by this review.

## 1. Exact version and review boundary

The principal file was hashed before reading:

~~~text
v3/derivations/02_probability_information.md
SHA-256:
e9a2209ead2fcb9c3c8b10bb0cfce91a38322ca608447e92f98462c919478c53
~~~

The reviewed prefix comprises sections 1–11, ending immediately before
the heading “Remaining sections under active investigation.” It contains
1,010 lines, including the blank separator before that heading.

~~~text
SHA-256 of that exact UTF-8 prefix:
dc4058c62f28e2b0dd2333b4c8067fc34542d4c3da96ec30d95ff3b5ad56acd4
~~~

The whole-file hash was unchanged on a second read after the initial
inspection. Later appended sections are outside this audit. External
priority, contribution support and every cited source's historical
interpretation were not independently re-surveyed here.

**Overall disposition:** the load-bearing arguments hold under their
intended assumptions. Two statement-level clarifications should be made:
the finite convex-hull coherence test needs its full-simplex scope, and
PI-12 should explicitly require well-formed payoff intervals. Neither
requires replacing a proof or reversing the intended result.

## 2. Load-bearing proposition dispositions

| Proposition | Disposition on reviewed version | Adversarial finding |
|---|---|---|
| PI-1: arbitrary-target fiber principle | **Accepted** | The statement quantifies over actual admitted pairs in \(P\), and explicitly separates decoder existence from computation. The two-point obstruction defeats an arbitrary decoder and an almost-surely exact randomized decoder. |
| PI-2: full-simplex target and law recovery | **Accepted** | Normalization is correctly included. Every hidden zero-sum direction can be realized by opposite perturbations of an interior law, so necessity is not restricted to affine decoders. The affine-independence and coordinate-count consequences follow. |
| PI-3: convex restricted sources | **Accepted** | The actual affine direction space and a relative-interior point suffice. Compactness, full-dimensionality in the ambient space and polyhedral boundaries are not needed. The nonconvex catalogue correctly defeats the unqualified rank condition. |
| PI-4: local support-sensitive identification | **Accepted** | The union of feasible supports is required and is used. Averaging its witnesses produces a relative-interior law of the fiber's nonnegative support. The supplied \(y=1\) example correctly rejects the support of one arbitrary feasible point. |
| PI-5: LP bounds and certificates | **Accepted** | The inequality orientation, unrestricted equality multipliers and nonnegative inequality multipliers are correct. Feasible bounded finite LPs do not need Slater's condition. “Rational data” must include the target, observation and all bounds, as usual. |
| PI-6: exact worst-compatible regret | **Accepted** | The interchange of maxima is valid for a finite action menu and a nonempty compact source. Including the chosen action gives nonnegative regret. Zero regret is exactly the common-optimum condition. |
| PI-7: full span of strict-score differences | **Accepted** | Both annihilator cases preserve the entire risk ranking under a distinct nearby interior law. The positive coefficient in the nonzero-sum case is essential and is stated. Finite losses, all interior laws as reports, exact unique global minimizers and \(n\geq2\) are correctly exposed. |
| PI-8: shared affine score calibration and sharp count | **Accepted** | Invertible score differences recover \(x=sp\), then scale, law and offset. The hidden-vector argument for too few fixed raw probes changes the normalized law, not merely its scale. The exclusion of adaptive menus and optimized reports is material and present. |
| PI-9: essential-action difference criterion | **Accepted** | Essential rows preserve the envelope. Interior-facet connectivity, the strict midpoint kink and a common baseline give necessity and sufficiency. The kink rules out rescue by an original inactive action, without imposing a chosen tie action. |
| PI-10: unknown-scale/offset linear targets | **Accepted** | The nonconstant-target exclusion, every-positive-scale quantifier, interior normalization perturbation and complete additive-nuisance quotient are correct. The raw-query table uses fixed suitable probes under the earlier strict-score assumptions. |
| PI-11: minimum additional target measurements | **Accepted** | The relevant space is the old hidden space inside the actual source direction space. Its target-image dimension gives the lower bound, and target rows spanning the restricted row space attain it. Freely selectable linear measurements are expressly stipulated. |
| PI-12: independent payoff-box projection | **Needs one explicit input precondition; proof accepted with it** | Require \(\underline L_{ji}\leq\overline L_{ji}\) for every entry. This is conventional for a proper box and is explicit in the separate reconstruction, but is not explicit in the principal statement. Otherwise an empty payoff box can pass the projected bands at zero-probability entries. |

### PI-1 through PI-4: specific false necessities rejected

The manuscript correctly resists each of the following stronger assertions:

- A deficient global augmented rank makes every observation ambiguous.
- A point's support is the feasible support of its entire fiber.
- A finite catalogue obeys the full-real-simplex dimension bound.
- A sufficient decision summary must identify the full law.
- The only decoder contemplated by the rank proof is an affine decoder.

The necessity proofs use an interior feasible point only where the source
actually permits it. The local theorem uses its support-relative interior,
and the general convex theorem uses the actual affine hull.

The statement about convexifying an already formed fiber is also correct
for linear extrema and linear constancy. It does not license convexifying
the source before applying the observation. The manuscript gives the right
counterexample to that interchange.

### PI-5 and PI-6: optimization scope

The upper certificate
\[
A^\top\lambda+G^\top\mu\geq c^\top,\quad\mu\geq0
\]
implies \(cp\leq\lambda^\top b+\mu^\top g\) because \(p\geq0\).
Applying the same construction to \(-c\) is a valid lower certificate.
The three-state interval, its attaining laws and the two fallback comparisons
are correct.

For nonconvex compact fibers, the scalar target's attainable set can have
gaps while its extrema and worst-regret calculation remain well defined.
The manuscript explicitly distinguishes the outer interval from the
attainable range. No hidden convexification is used in the regret identity.

### PI-7 and PI-8: scoring and calibration

The strict-score span proof works even when the normalized annihilator
\(z/(\mathbf1^\top z)\) has negative coordinates: a sufficiently small
mixture with a strictly positive law remains an interior law. The proof
does not claim that the signed vector is itself a probability law.

The raw Brier and binary scalar Brier conventions are correctly separated.
The uniform Brier risk, optimum risk, vertex risks, logarithmic risk
differences and shared-offset Brier calibration all have the stated values.
The rational example \((7,10,9,8)\) decodes to
\(p=(1/6,1/3,1/2)\), \(s=3\), \(b=5\).

The argument that \(n-1\) suitable raw score rows suffice with fully known
units is valid: extend the nonzero constant row to a basis using rows from
the full score family. Counting a baseline plus \(n-1\) preselected
differences as \(n\) reports is correctly not called a universal raw-query
lower bound.

For the task-property score \(\|r-C[:,i]\|^2\), the unique minimizer
claim assumes the report domain contains \(Cp\), as is natural for an
unrestricted vector report. Explicitly writing \(r\in\mathbb R^k\)
would remove even that minor implicit domain convention.

### PI-9: geometry and quantitative bridge

The finite-cell proof does not require an inactive action to disappear from
all tie sets. It only removes such actions from the essential representation
of the lower envelope. A hypothetical original action optimal at both
opposite facet endpoints would have an impossibly low affine midpoint
value, which closes the potential hidden-tie loophole.

The phrase that three pieces would have “proportional” differences can
be made more precise: their affine differences on the simplex's affine
hull have the same codimension-one zero hyperplane, so are proportional
as affine functions there. On the facet itself all those differences
vanish, which alone would be an uninformative statement. The linked
reconstruction supplies the intended argument.

The regret bound in equation (24) is valid for any decoded report \(u\):
compare the selected essential action to an essential true optimum,
subtract their nonpositive predicted difference, and use the dual norm.
The common hidden expected baseline cancels. The result neither needs
that baseline's value nor establishes that a learning procedure achieves
a small feature-surrogate excess risk.

The ordinal absolute-loss example is correctly scoped. Its adjacent
differences span all \(n-1\) prefix coordinates modulo constants, while
an optimized median is a nonlinear report. Exact adaptive prefix search
for the first cumulative probability at least \(1/2\) can use at most
\(\lceil\log_2 n\rceil\) queries. This does not contradict a fixed-linear
measurement lower bound.

### PI-10 and PI-11: nuisance and repair quantifiers

The scale obstruction is global over \((p,s)\). Selecting an interior law
with \(ch-(\mathbf1^\top h)cp\ne0\) is legitimate for every nonconstant
target. The perturbation remains a normalized law at a positive scale.
When the constant row is retained, hidden kernel vectors are automatically
zero-sum and the ordinary target obstruction applies.

For an unrestricted common offset, a collision of differenced observations
can always be lifted to a collision of complete observations by adjusting
the offset. The reference coordinate therefore contains no omitted
probability information under that nuisance contract. A complete left
annihilator is correctly required for the general additive nuisance.

The positive column-sum normalization premises ensure that equal normalized
reports are exactly positive-ray collisions. The decision-only rational
example has strictly positive column sums and no undefined normalized report.
It does not generalize the nonconstant-target obstruction to all nonlinear
probability properties or to every individual fiber.

The additional-measurement dimension identity follows from rank-nullity
on \(V\), and the restricted-menu example correctly requires two available
queries even though one freely chosen query would suffice. A small nonzero
price coefficient can change exact identifiability while its target-width
effect tends to zero; the distinction is mathematically valid.

## 3. Two precise statement changes

### A1 — scope the convex-hull coherence criterion

Section 8 states that a finite record is compatible with some law exactly
when it lies in the convex hull of the loss columns. This is true for
some law on the **full simplex**, or when additional source restrictions
are deliberately ignored. It is not the criterion for nonemptiness of
the earlier \(F_P(y)\) under an arbitrary admitted family \(P\).

Counterexample:
\[
P=\{e_1\},\qquad L=(0,1),\qquad y=1.
\]
The value \(1\) lies in the convex hull of the loss columns, but no law
in \(P\) gives it. The sure-gain separation argument likewise describes
unrestricted finite-state probability compatibility, not every additional
constraint on admissible laws.

Recommended local change: begin the criterion with “When \(P=\Delta_n\)”
or “Ignoring any additional restrictions on \(P\).” This preserves the
intended coherent-expectation comparison.

### A2 — require valid payoff intervals in PI-12

Explicitly state
\[
\underline L_{ji}\leq\overline L_{ji}\qquad\text{for every }j,i.
\]
Otherwise the formal implication fails at zero-probability coordinates.
For example, take one row with
\[
\underline L=(0,1),\quad \overline L=(0,0),\quad p=e_1,\quad y=0.
\]
The projected inequalities hold, but no admissible payoff row exists
because its second entry would have to lie between \(1\) and \(0\).

Under the ordinary valid-box assumption, PI-12's row-segment construction
is correct, including zero weights and zero-width weighted intervals.
Its affine lift is a lift **of the existential projection, with the
unknown payoff table eliminated**. It is not the exact joint bilinear
graph with \(L\) still retained. Adding that short phrase would also
make the existing scope warning maximally explicit.

The independent error-box extension requires nonnegative error radii
and availability independent of the payoff choices. This is already
conveyed by “independent box error”; the separate reconstruction spells it
out. Shared stakes, correlated entries or one table shared across several
law records cannot be replaced by independent candidate-specific witnesses.
The principal text correctly includes these counterexamples and caveats.

## 4. Optional convex-source extension of PI-9

This extension is **proved in this audit only**. It is not needed to make
the currently narrower full-simplex principal statement correct.

Let \(P\subseteq\Delta_n\) be any nonempty convex set and let
\(V=\operatorname{span}(P-P)\). Merge action losses that define the same
affine function on \(\operatorname{aff}(P)\). Define \(E_P\) by unique
optimality at some point of \(\operatorname{ri}(P)\). Then a globally
valid some-optimal selector from \(Lp\) exists on \(P\) iff
\[
(c_a-c_b)h=0
\quad\text{for every }a,b\in E_P
\text{ and every }h\in V\cap\ker L.
\]

The justification is the same finite affine argument:

1. The relative interior is nonempty, convex and open in the actual affine
   hull. Avoiding finitely many proper tie hyperplanes gives essential
   unique cells. Approaching any source point by such points shows that
   essential rows preserve the envelope on all of \(P\).
2. A generic polygonal path inside that relative interior connects strict
   cells through flat interior interfaces. Curvature or nonpolyhedral
   structure of the outer boundary of \(P\) does not affect these local
   interfaces. The hidden-direction midpoint obstruction applies using
   \(h\in V\cap\ker L\).
3. Conversely, annihilation of this kernel factors each essential difference
   on the affine hull as
   \((c_a-c_{a_0})p=\alpha_a+\beta_a Lp\). Minimize these recovered
   differences.

No closedness or compactness premise is needed for this exact finite-menu
selector statement. With a zero-dimensional source the selector is constant.
If an implementation is required, access to the actual affine hull and
essential cells must still be supplied or charged.

### Why separate convex components cannot be checked independently

Let
\[
P_1=\operatorname{conv}\{e_1,e_2\},\qquad
P_2=\operatorname{conv}\{e_3,e_4\},\qquad P=P_1\cup P_2,
\]
with
\[
L=(0,1,0,1),\qquad
c_A=(0,0,1,1),\quad c_B=(1,1,0,0).
\]
Each component has a constant unique optimum: \(A\) on \(P_1\), \(B\)
on \(P_2\). Its componentwise essential-difference test is vacuous.
Nevertheless, for every \(y\in[0,1]\),
\[
p_y=(1-y,y,0,0),\qquad q_y=(0,0,1-y,y)
\]
have the same observation \(y\) and opposite unique optimal actions.
The union therefore has no summary-only optimal selector at any observation.

Known case identity would make the observation \((\text{case},y)\)
and permit componentwise selection. Without that identity, the literal
fiber-intersection condition must also compare laws from different source
components. This does not expose an error in PI-9 as currently scoped.

## 5. What the existing executable evidence actually checks

The following artifacts were inspected without rerunning or changing them.
Their recorded direct script hashes match the current script bytes.

| Check | Actual supported scope | What it does not establish |
|---|---|---|
| \(02\_probability\_checks.py\) | Exact rational partial-identification fixtures, joint-dependence and random-stake intervals, one three-outcome Brier scale/offset calibration, realized-score semantic counterexamples, and a noisy scale-ratio fixture. Every claimed LP extremum carries a feasible witness and arithmetic multiplier certificate. | It is not a generic LP solver or a test of all loss matrices, all proper scores, all nuisance dimensions or all payoff boxes. |
| \(02\_decision\_geometry\_check.py\) | 351 two-action and 2,925 three-action menus on \(\Delta_3\), with entries in \(\{-1,0,1\}\), fixed summary \(p_1\), exact tie crossings and intervening intervals, plus five focused rational exceptions. | It does not establish PI-9 for arbitrary state count, summaries, real coefficients or convex source geometry. The proof supplies that scope. |
| \(02\_native\_probability\_check.py\) | Five declared rational groups, thirteen accepted native target receipts, three expected rejections, and an explicit target-unit reduct countermodel. | It does not add general division, arbitrary bilinear semantics, a probability learner or broad production validation. |
| \(02\_noise\_modulus\_check.py\) | Fourteen rational conditioning regimes and selected coherence/source checks, using exact certificates. Its source incompatibility and negative-multiplier cases support the earlier distinctions. | The later noise and coherent-center theorems are outside this sections-1–11 audit. |

The decision-geometry oracle is stronger than sampling a few laws. For
each tested menu, its candidate checks cover every exact endpoint-order
breakpoint and one point in each intervening interval. A positive conclusion
requires all those checks; a negative conclusion can stop at the first
actual pair with no common optimum. It therefore decides the continuous
\(p_1\)-fiber service for each menu. However, the menu family and summary
remain deliberately finite and fixed.

The agent and principal decision-result files are byte-identical, as
expected for the deterministic script. This is consistent with a matching
rerun; their bytes alone do not establish independent execution timing
or independent-model verification. Both are labeled development.

The rational vertex enumerator explicitly assumes independent equality
rows in its supplied compact fixtures. It would, for example, fail to
enumerate a source supplied with redundant equality rows
\(p_1+p_2=1\), \(2p_1+2p_2=2\) without preprocessing. This does not
invalidate its passed extremum certificates, which independently prove
the bound for their actual constraints. It does mean that its fixture
coverage must not be used as evidence of a general LP implementation.

No current executable file specifically exhausts PI-12's payoff-box
projection, PI-11's arbitrary repair dimension or PI-10's general additive
nuisance. Those are proof-based claims with scoped hand constructions.
Additional broad tests are not needed merely to restate the proofs, but
they must not be described as already executed.

### Inspected direct script hashes

~~~text
02_probability_checks.py
11d63d38a2d77398b5f67d3db882dffb2d9dfd26f07fa83c1a4cbee8a51d1ca4

02_decision_geometry_check.py
1d61ee1b6e4b49ebce00fc9d07183f0fce5ca87249a8add51a787f09d2f8391c

02_noise_modulus_check.py
77e15a46966640e80364908e877a2e697b679996b0338911504cbdbec1531930

02_native_probability_check.py
dcfc32c51000ff7b3ed4ff95fd309bdb360dd8f78f25e1c048ddc8e1ee56236a
~~~

The inspected result records are the existing development files
probability_checks_1.json, decision_geometry_agent.json,
decision_geometry_principal.json, noise_modulus_1.json and
native_probability_agent.json. All report successful completion within
their declared scope.

## 6. Final mathematical disposition

No counterexample was found to PI-1 through PI-11 under their declared
premises. PI-12 is accepted under the standard nonempty componentwise-box
premise, which should be made explicit. The separate convex-hull coherence
sentence should state that it concerns full-simplex compatibility.

The current manuscript consistently distinguishes full-law, target-loss,
interval, preference and some-optimal-action services. Its mathematical
conclusions do not need a stronger claim that probabilities are always
necessary, that a scalar can never contain them, or that exact
information recovery itself establishes learning, computation costs or
source adequacy. This audit makes no contribution-gate or task-completion
determination.

## 7. Targeted resolution check after principal edits

A later read found both requested wording changes in place:

- **A1 closed:** the convex-hull criterion now explicitly uses the full
  simplex with no additional law restrictions.
- **A2 closed:** PI-12 now explicitly requires
  \(\underline L\leq\overline L\) entrywise.

The exact bytes inspected for this limited resolution check had:

~~~text
Whole-file SHA-256:
0b2324d25329ea25c45bad5b2e5a5e998854debe6f1b5e840971dacab19df2b1

Sections 1–11 prefix SHA-256, before the new section 12:
6f9d054449c0d5f1919ccb393601fa6c3714c3f12c307d31b753e2bc67b3d0e8
~~~

PI-12's disposition is therefore **accepted with its now explicit
well-formed-box premise**. No required mathematical change from this
audit remains open. This targeted reread verifies those two resolutions;
it does not extend the audit to the newly appended section 12 or other
later material.
