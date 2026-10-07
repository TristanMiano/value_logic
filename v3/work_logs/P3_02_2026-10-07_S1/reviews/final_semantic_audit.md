# P3-02 — final semantic and comparison audit

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
**/root/scoring_sources**, October 7, 2026 UTC. Same-model internal, nonblind
development review. This is neither an independent external evaluation nor
a gate attempt. It changes no principal artifact, scientific support status,
clock, time ledger or phase pointer. Concurrent review supplies no additional
principal research credit.

## 1. Snapshots and actual coverage

The principal remained under revision during the review. The following
content snapshots, rather than an unspecified eventual version, were read.

| Record | File | SHA-256 | Coverage |
|---|---|---|---|
| S1 | v3/derivations/02_probability_information.md | 6bc510681051b34eb4fc1e21a7ab04ab4c4b2fac993016cb29a8d1105479e9a9 | Scientific-boundary read across sections 1–14; new ratio optimization, error and scoring claims checked directly |
| S2 | v3/derivations/02_probability_information.md | c7473eab541abd6c9a9d12f0d4943fd387795d36b11a92000d6f3163028aea45 | New section 15 and randomized-decision subsection; current noise/native wording |
| S3 | v3/derivations/02_probability_information.md | 1c16171d3b2ad266ca1b1c1ca502cd3a11128ec0535c1a97e6d42b4ea35e0e71 | All intervening changed paragraphs, new section 16, corrected conditional report domain, shared-table quantifiers, numbering and named affine-recovery ancestry |
| L3 | v3/literature/02_probability_sources.md | bbb913a63c2b25ca1ad620e07ff729aa33bd2416d8c9cf645494da521365d841 | Source/comparison wording, including new linear-fractional and optimal-recovery entries and disposition |
| A | v3/work_logs/P3_02_2026-10-07_S1/reviews/affine_scalar_recovery.md | 9d1d725bebdaf1ed83261ed1a63cc996deebb92ce168526541dbc57aebe23e30 | Supporting affine proof and its implementation boundaries |
| C | v3/work_logs/P3_02_2026-10-07_S1/reviews/conditional_probability_review.md | 4f9356798daff0f7c3e92ee62ab5c8890b9582c9c0d69d8c7fa33b2aac19d02e | Recorded sibling proof dependency; its closed base ratio theorem was not independently re-proved in this audit |

The earlier mathematical checks of PI-2 through PI-13 were not rerun.
Reading their surrounding claims here checks semantic consistency and
comparison scope, not new independent validation of each proof. No code,
development receipt count, clock calculation, final challenge or publication
state was checked.

The requested ratio LP and error equations were numbered (42) and (43)
in S1. They are **(43) and (44)** in S3 after correction of a duplicated
equation number. PI-15 is (45) in S3. Equation labels in this audit therefore
refer to S3 unless the earlier snapshot is named.

**Finding:** the newly examined mathematics and ordinary comparisons are
sound within their declared interfaces. The principal consistently separates
exact expectation information from its acquisition, estimation and application
accuracy. One newly added sentence in S3 section 16 still requires a semantic
wording correction: a population connection needs a justified sampling or
error model, not necessarily an iid model. This is identified precisely in
section 5 below. No other material unsupported learning, population-truth,
novelty or resource-advantage inference was found in the covered text.

## 2. Conditional ratios: transform, inverse and accuracy

### 2.1 The positive-margin LP is exact

The source is a nonempty compact polytope
```math
F=\{p\geq0:Bp=d,\ Gp\leq g\},
```
with normalization among the equality rows and a justified bound
$`bp\geq\beta>0`$. The construction
```math
t=(bp)^{-1},\qquad x=tp
```
maps every law in $`F`$ to a feasible point of (43):
```math
Bx=dt,\quad Gx\leq gt,\quad bx=1,\quad
x\geq0,\quad 0\leq t\leq1/\beta.
```
Its target value is $`ax=ap/(bp)`$.

Conversely, normalization in $`Bx=dt`$ gives
$`\mathbf1^\top x=t`$. If $`t=0`$, nonnegativity forces $`x=0`$,
contradicting $`bx=1`$. Hence every transformed feasible point has
$`t>0`$, and $`p=x/t`$ satisfies the original normalization, equalities,
inequalities and denominator condition. It also inverts the objective.
Thus both minimization and maximization are preserved; there are no spurious
zero-$`t`$ feasible points in this normalized problem.

The transformed source is closed and bounded: $`0\leq x_i\leq t\leq1/\beta`$.
Its extrema therefore exist. The stated bound is a sufficient known margin,
not an imported assertion that all fractional programs require this precise
compact formulation. If one wants rational LP witnesses or native rational
syntax, the target and denominator rows and the chosen margin must also
have the required rational encodings. A rational law polytope alone does
not make arbitrary real coefficients rational.

The attribution to ordinary linear-fractional programming is accurate.
Charnes and Cooper's positive-denominator transformation and inverse appear
in “General Linear Fractional Models,” printed pp.182–184, equations
(2.1)–(3), Lemma 1, Theorem 1 and the positive branch (4.1).
The principal specializes the transformation and proves its inverse directly;
it does not import their complete treatment of vanishing or changing-sign
denominators. The archive scan was reopened and those portions inspected;
its OCR is imperfect. [Author-archive scan](https://iiif.library.cmu.edu/file/Cooper_box00010_fld00009_bdl0001_doc0001/Cooper_box00010_fld00009_bdl0001_doc0001.pdf).

### 2.2 The error bound uses the correct denominator premise

With $`u=\Pr(A\cap B)`$, $`v=\Pr(B)\geq\beta`$, and the stated coordinate
errors, $`\widehat v\geq\beta-\eta_v>0`$. Writing the difference as
```math
\frac{\widehat u}{\widehat v}-\frac uv
=
\frac{(\widehat u-u)-(u/v)(\widehat v-v)}{\widehat v}
```
gives
```math
\left|\frac{\widehat u}{\widehat v}-\frac uv\right|
\leq
\frac{\eta_u+(u/v)\eta_v}{\beta-\eta_v}
\leq
\frac{\eta_u+\eta_v}{\beta-\eta_v}.
```
This proves (44). It requires neither that the estimated pair itself be a
coherent event-probability pair nor that its ratio already lie in $`[0,1]`$.
Clipping to that interval cannot increase distance from the true target
in the interval.

The two rare-event laws supplied in section 14 demonstrate the absence
of a uniform stable conditional decoder as the event mass approaches zero.
They do not establish a lower bound for every statistical estimation protocol
or imply large unconditional decision loss. The text states those boundaries.
Joint source optimization can improve on the displayed separate-coordinate
bound without contradicting it.

### 2.3 Conditional Brier elicits the specified property

The corrected report domain $`q\in[0,1]`$ includes the conditional law.
For a fixed outcome distribution with $`v=\Pr(B)>0`$ and
$`r=\Pr(A\mid B)`$,
```math
\mathbb E[\mathbf1_B(q-\mathbf1_A)^2]
=v\bigl[(q-r)^2+r(1-r)\bigr].
```
Thus its unique minimizer is $`q=r`$, and its excess expected loss is
$`v(q-r)^2`$. If a separate procedure certifies excess at most $`\xi`$
and $`v\geq\beta>0`$, then
```math
|q-r|\leq\sqrt{\xi/\beta}.
```
Without a positive event-mass control, small unconditional excess need not
give small conditional error. At $`v=0`$, every report has zero loss and
the conditional target is outside this service.

The principal correctly calls this property elicitation, distinguishes it
from eliciting the entire unrestricted law, and supplies no exact optimization
oracle or sample guarantee by definition. Known fixed rational report rows
and optimization over a variable report remain different operational inputs.

## 3. PI-15: the strong ordinary recovery comparison

The claimed endpoint is the **global worst-case absolute error** of an
unrestricted scalar answer, for a known linear target and observation map
on one nonempty compact convex finite-dimensional source. The affine
constant is allowed. Output compatibility and a pointwise error budget
are additional requirements.

The finite proof has the appropriate dual constraints. Free radius and
intercept variables require the two nonnegative dual weight families to
have totals $`1/2`$; the observation coefficients require equal observation
barycenters. Convexity makes those barycenters admissible source points.
Their objective is half a same-observation target separation. This matches
the unrestricted scalar information bound. For general compact convex
sources, the stated affine-spanning anchor construction and compact finite
intersection argument give attainment without pretending that an unspecified
source oracle is an executable finite LP.

A compact convex joint source of objects and errors is covered by the
enlarged linear observation map. No statistical independence follows or
is needed. Coordinatewise stacking is valid for unrestricted finite-vector
recovery in the maximum-coordinate norm. It does not impose a common
compatible law or establish the analogous assertion for every norm.
The text preserves each of these distinctions.

### 3.1 Named ordinary ancestry is now explicit

Osipenko's introduction states the centrally symmetric scalar recovery
theorem as Theorem 1, printed p.461, attributed there to Smolyak. For the
principal's $`K`$, take
```math
W=\mathrm{conv}\{\pm(x,1):x\in K\},\qquad
I(u,t)=(Nu,t),\qquad \widetilde c(u,t)=cu.
```
This is a compact convex centrally symmetric source. At zero information,
$`t=0`$ forces $`u=(x-x')/2`$ with $`Nx=Nx'`$. The stated theorem's
radius is therefore the required pair half-width; its linear rule restricts
on $`t=1`$ to an affine rule on $`Nx`$. This confirms the principal's
direct ancestry route. Only the statement in Osipenko was inspected;
Smolyak's original 1965 paper was not retrieved.

The same source's section 3, printed pp.466–468, supplies multivalued
observation relations and local/global information radii. The corrected
full page span 459–482 agrees with the displayed final page.
[Osipenko paper](https://www.rstu.ru/proc/pdf/paperOs.pdf).

Foucart and Liao's inspected Theorem 1 concerns the stated Hilbert-space
two-centered-hyperellipsoid model. Section 3.2 equations (22)–(25) use the
joint object/error variable. Those provide relevant ordinary context; their
specialized theorem is not applied to a general simplex or a different
target norm here. The principal now gives both its own proof and the
closer scalar ancestry, with no new general estimation claim.
[Foucart–Liao author manuscript](https://foucart.github.io/publi/OR_L1Noise_v3.pdf).

### 3.2 The conditioning example no longer relies on a weak baseline

The three displayed affine decoders have the stated worst errors.
For the non-inversion decoder,
```math
\frac{z_2-1/2}{1+\delta}-p_3
=\frac{p_2-1/2+e_2}{1+\delta}.
```
The source endpoints attain its bound. Selecting the best of the three
known regimes before observing $`z`$ attains the earlier sharp global
radius. Thus the sharper radius improves on the simpler inversion bound,
but supplies no improvement over the best stated ordinary affine baseline.
Selecting a decoder by its proved risk bound is correctly distinguished
from taking a numerical minimum of its output and another decoder's output.

The three-state example also correctly separates global error from pointwise
quality and compatible output. A globally optimal affine estimate can be
incompatible on a singleton fiber. The piecewise-affine midpoint is compatible
and achieves the same global radius; an affine rule required to be compatible
everywhere has a worse radius in that example. An ordinary piecewise-affine
solver is explicitly allowed the same midpoint construction. Removing
convexity gives the stated distinct-observation lookup counterexample.

These examples identify different services. They do not establish a resource
advantage, a special native capability, or a universal need for nonlinear
recovery merely because a pointwise midpoint is nonlinear.

## 4. Randomized-action integration

Section 6 preserves the finite, nonempty-fiber scope of the earlier regret
discussion and states the private-draw timing. Expected regret is a sum of
nonnegative original-action regrets. Consequently it vanishes exactly when
every positive-weight original action is optimal at every compatible law.
Randomization leaves the zero-regret common-optimum obstruction intact.

The opposing two-state action example correctly lowers positive minimax
expected regret from one to one-half. Letting nature observe the realized
action before choosing a law is a different contract and removes that
specific improvement. The text neither turns this into a randomized
acquisition policy nor treats randomization as an uncharged operation.

## 5. New finite-storage and observation boundaries

The added section 16 makes several helpful distinctions explicit:

- The finite-code interval-covering bound concerns a deterministic encoder
  with finitely many outputs. Its ideal encoder is not presumed to possess
  an unavailable exact law. A decision label and a reusable probability
  record have different future-query duties.
- In the stated iid Bernoulli example, every finite transcript has positive
  likelihood under every interior parameter. Strict positive-likelihood
  compatibility therefore differs from statistical identifiability, a
  confidence statement with nonzero failure allowance, or consistency.
  The likelihood-ratio example makes clear that the sample still carries
  statistical information.
- The law of a realized loss, its one realized draw, and its mean are three
  different inputs. Distinct statewise loss values can make the first
  identifying even when the mean is not.
- A common finite batch produces $`L\widehat p`$. When the stipulated
  exact law inverse is available, it returns the empirical law. Common
  varying trial weights can instead yield a weighted empirical law;
  different probe batches need not yield any one exact coherent law.
- The binary shifted-Brier positive case and the higher-simplex continuous
  scalar obstruction preserve their different dimensions and exact input
  premises. They do not prohibit arbitrary discontinuous encodings or
  identify an approximate achieved score with the Bayes-risk oracle.

### One correction still open in S3

Immediately after the empirical-law identity, S3 says:

> This algebra needs no iid assumption; connecting it to a population law does.

The second clause is too strong. An iid assumption is one possible sufficient
part of a statistical bridge, not a necessary premise of every population
interpretation. Different dependent or designed sampling models can support
their own conclusions. The needed correction is:

> This algebra needs no iid assumption; connecting the empirical law to a
> population law requires a separately justified sampling or error model.

This is a scientific-boundary wording correction, not a defect in the
empirical identity or the separately stated iid Bernoulli example. The
principal was notified. Its application to a later snapshot is not presumed
by this review.

## 6. Cross-principal scientific boundary findings

| Potential inference | What the inspected principal actually warrants |
|---|---|
| Known statewise loss implies a belief | The loss table is semantic input; a law is a separate input |
| Exact loss inversion establishes an accurate population or mathematical belief | Recovery is relative to the stipulated law and source family; application adequacy remains unproved |
| Exact decoder existence supplies a bounded reasoning algorithm | PI-1, rank results, PI-7/8 and PI-15 separately identify access, precision, optimization and computation requirements |
| Strict propriety means a learner has found the correct report | Risk optimization, reported optimizer, realized score, empirical score and learned estimate remain explicitly distinct |
| Coherence verifies accuracy | Coherence is compatibility; projecting an estimate or selecting a compatible law supplies no accuracy or coverage guarantee |
| An error box is a statistical confidence result | Error and source premises are conditional inputs; simultaneous statistical coverage needs an external justification |
| Conditional coverage after selecting a conclusion is automatic | Section 12 explicitly distinguishes an unconditional selected-error bound from coverage conditioned on acceptance |
| Full-law recovery is necessary for useful decisions | Task-loss, preference, common-optimum, conditional-property and threshold services supply stated smaller alternatives |
| A change of prices automatically preserves the same law | Same statewise semantics and fixed-source law are required; behavior changes and counterfactual dependencies remain separate |
| Native acceptance validates empirical probability inputs | Section 13 treats those inputs as stipulated premises and separates directed conversions, rational syntax and external semantic adapters |
| A smaller number of exact coordinates establishes lower memory, sample or acquisition cost | Measurement dimension, finite codes, optimized reports, adaptive queries, sample evidence and resource costs are separately scoped |
| A reconstructed numerical characterization is automatically a new contribution | Strong ordinary expectation, elicitation, LP, fractional-programming and optimal-recovery methods are named; priority and advantage are not inferred |

Two earlier wording refinements are visibly resolved in S3. Section 5 now
uses a “particular unobserved law” rather than potentially implying a
metaphysically true probability. Section 11 correctly quantifies a shared
payoff table over each simultaneous candidate tuple: one table must satisfy
every record within that tuple, while different alternative tuples may have
different witnesses. That avoids an unintended requirement for one table
across every alternative hypothesis.

The finite-score calibration assumptions remain explicit: known finite
base rows, sufficiently rich accessible probes, exact expected scores,
common affine nuisance parameters and the stated source domain. Numerical
success does not verify those types; the shared-realization example makes
that obstruction concrete. No new reproof of the four closed query counts
was needed for this semantic finding.

## 7. Contribution and comparison disposition

The source record names a strong ordinary combination that can implement
the numerical services. Section 15 strengthens that comparison further:
the sharp global scalar noise radius already has an ordinary affine
implementation, while pointwise or compatible outputs have their own
ordinary constructions. This prevents a numerical improvement over one
simple inverse from becoming an unsupported general advantage claim.

The narrower finite information-audit interface can still be assessed as
a proposed synthesis or formal adaptation under the author's stated
criterion. Its assessment is not identical to the broader phase-wide
obligation concerning uncertain logical forecasts, paid computations and
revisable comparisons. Ordinary ancestry alone neither proves nor refutes
the usefulness of that narrower adaptation. Merely assembling familiar
ingredients also does not establish its significance.

Appropriate reporting language, without deciding either obligation, is:

> P3-02 reconstructs a finite information-audit contract with explicit
> decoders, ambiguity witnesses, service-specific recovery conditions and
> certificate interfaces. Its numerical operations have named ordinary
> implementations. No distinct learning guarantee, data-efficiency result
> or paid-resource advantage follows from those characterizations. The
> usefulness of the adapted interface and the wider phase contribution
> require their separately scoped assessments.

No support status or gate verdict follows from this audit. Source/contribution
closure and final development reconciliation were still listed as active
in S3. Later additions to those sections, changes to the inspected premises,
or publication claims require their own review.
