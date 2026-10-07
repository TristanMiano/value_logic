# P3-02 — principal source and claim-scope audit

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
**/root/scoring_sources**. Same-model internal, nonblind audit. This note
owns no principal-file edit, clock, ledger, status or gate decision.
Concurrent reviewer effort receives no additional principal research credit.

## 1. Audited snapshot and result

Audited principal sections **8–11** and the whole P3-02 source record, using
the following exact UTF-8 file snapshots:

| File | SHA-256 |
|---|---|
| v3/derivations/02_probability_information.md | 6accff3a68cff660baf17693fd44a0d3b129a750050dbda532ed015bfe07da8e |
| v3/literature/02_probability_sources.md | 3a88c01dc90055d9d02d7066d14b5c2a60b117b949d7f5cfaa82cd3b1a5b29c0 |

The snapshot was read once into the review's working memory with its hashes.
The source record's named primary PDFs were revisited selectively. The
protocol's broad contribution criterion and the existing P3-N01 object were
also read. No historical proof or phase-two experiment was rerun.

**Result:** PI-7's full score-difference span, PI-8's calibration construction,
the four fixed-probe counts, and the mathematical distinctions in sections
9–11 are supported under their stated finite assumptions. The principal
carefully distinguishes exact information from learning, and expected loss
from realized score. The main corrections concern a few source-record
abbreviations and categorical failure wording. There is no identified
mathematical counterexample to the audited propositions within their stated
scope.

The contribution paragraph can be more precise about a **local finite
information-audit object**. Its disposition need not make a judgment about
every possible phase-wide contribution, and ordinary antecedents do not
automatically exclude a useful synthesis or formal adaptation under the
author's criterion. This note recommends language and comparison scope,
not a gate verdict.

## 2. Recommended wording corrections

### A1. Preserve the lower/upper-expectation assumptions

P02-S1 currently abbreviates the imprecise-expectation assumptions as
positive homogeneity plus super/subadditivity. Replace that phrase with:

> On the finite gamble space, superadditivity or subadditivity, positive
> affine homogeneity, and monotonicity characterize lower or upper
> expectations, respectively.

Positive **affine** homogeneity includes the constant-translation law;
ordinary positive homogeneity alone omits it. The constant-zero functional
is monotone, homogeneous and additive but cannot be a normalized expectation
because it sends the constant one to zero. The exact source is Halpern and
Pucella §2.2, Theorem 2.4; see the primary locator in §4 below.

The principal's own precise all-gamble functional argument already includes
normalization and positivity and needs no correction.

### A2. Make scalar-risk nonidentification a lack of guarantee

P02-S2 says strict propriety “does not identify that law from one scalar
achieved risk.” Match the principal's more precise wording:

> Strict propriety identifies the exact optimal report under a fixed law;
> by itself it does not guarantee that one scalar risk identifies the law.

This qualification is substantive. The principal correctly includes the
binary fixed-report Brier positive case. Even an optimal scalar risk can
identify a binary law for a suitable score: the finite loss
```math
\ell(q,Y)=(q-Y)^2+2Y,\qquad Y\in\{0,1\},
```
remains strictly proper, but its optimal risk is $`3p-p^2`$, which is
strictly increasing on $`[0,1]`$. This direct calculation shows why a
universal scalar-risk impossibility would be false. It does not weaken
the principal's nonidentification examples for its specified Brier and
log scores.

### A3. Add the source locator for score-equivalent shifts

P02-S2 should include **Gneiting–Raftery §2.1, equation (2), printed p.360**
among the inspected locators. That is the explicit primary antecedent for
positive scaling and an outcome-dependent addition common to all reports.
The current listing gives §1 and §3.1 but omits this particularly relevant
equation. Abernethy–Frongillo §3, Definition 3 also records the common
outcome-term equivalence in its report convention.

### A4. Scope PI-8's list of failures to the displayed formulas

The sentence beginning “It fails for report-dependent scales/offsets,
zero scale, unknown payoff rows or invalid expectation estimates” is stronger
than necessary. Unknown rows can retain partial or even full identification,
as section 11 itself demonstrates. Structured report-dependent transformations
can also admit a separate calibration argument.

Suggested replacement:

> Equations (17)–(18) require known base score rows, exact expectations and
> one shared nonzero affine transformation. Other payoff, transformation
> or error models require their own identification contract; these formulas
> do not establish recovery for them.

Zero common scale does destroy information under (17) with unrestricted
offset and law. Arbitrary independent report offsets likewise admit the
usual confounding obstruction. These specific failures can still be stated
when their quantifiers are explicit.

### A5. Make the query-count table's local premises explicit

The four counts are correct. Add a short table introduction or caption:

> For $`n\geq2`$, exact fixed raw probes from a sufficiently rich finite-score
> family, and a known scale assumed nonzero when applicable:

The preceding sections already contain most of these assumptions. This
small change makes the table resistant to extraction without its context.
The count remains one for each scalar expectation observation, without a
claim about precision, bits, computational effort or sampling cost.

### A6. Restrict the LP-source summary to polyhedral fibers

P02-S5 says “Our probability fibers are finite nonempty compact polytopes.”
The principal also permits more general convex source families, so that
sentence should identify the cases to which its LP conclusion applies:

> The finite polyhedral fibers used for the LP certificates are nonempty
> compact polytopes. Their linear extrema are attained, and ordinary LP
> duality supplies matching certificates.

This retains the correct finite LP statement without classifying every
allowed source as polyhedral. The principal already distinguishes broader
source geometries elsewhere.

### A7. Keep the ordinary-comparison import boundaries

No change is required to the principal's claim that calibrated-surrogate
geometry anticipates the common-optimum condition. In the source note,
“requires” correctly states a necessary condition. If that sentence is
expanded, call Ramaswamy–Agarwal Theorem 6 a **necessary** condition and
keep the principal's own factorization/regret proof for its finite
sufficiency result. The general source theorem is not an imported
essential-difference iff.

For precision, that source's ignored-action premise occurs at §2.3,
printed p.8: every remaining action must be a unique Bayes optimum at some
law. The principal independently proves the boundary/duplicate-row
reduction appropriate to its own service.

## 3. Mathematical and semantic audit

### 3.1 PI-7: all load-bearing assumptions are present

The current proposition supplies:

- A finite number $`n\geq2`$ of outcomes.
- Finite real loss vectors for every admitted report.
- A common report domain containing every interior law as its own report.
- A fixed law while reports are compared.
- An attained, unique global optimum at the truthful report for every
  interior law.

Both annihilator cases are correct. A zero-sum annihilator gives a constant
shift in risk under a tangent perturbation. An annihilator with nonzero sum
gives a positive affine transformation of the risk surface under a small
move toward its normalized vector. An interior starting law different from
that normalized vector exists when $`n\geq2`$. No differentiability or
uniform score bound is used.

The full difference span is stronger than the normalization-augmented span.
The stated consequence for $`n-1`$ appropriately selected raw rows is
correct. A baseline plus $`n-1`$ additional raw rows computes a particular
difference basis but is not the minimum over raw-row selections.
Finite positive log reports satisfy the premises even though other,
boundary reports of the original log score can contain infinite penalties.

This remains a reconstruction proved in the principal. The primary scoring
sources support its premises and ordinary geometric setting; the source
record appropriately avoids claiming to have imported an independently
located numbered span theorem.

### 3.2 PI-8 and the four counts

The transformation $`v(q)=b+sR_p(q)`$ leads to $`x=sp`$; the independent
score differences recover $`x`$, its sum recovers $`s`$, normalization
recovers $`p`$, and the baseline recovers $`b`$. The $`n+1`$ raw-query
construction and kernel lower bound are sound for the declared fixed menu
and unrestricted $`s>0,b\in\mathbb R`$.

The four cases can be checked by their remaining hidden spaces:

| Nuisance knowledge | Information that must determine the law | Sharp raw count |
|---|---|---:|
| Both known | Raw rows modulo the known normalization | $`n-1`$ |
| Only scale known | Report differences modulo normalization | $`n`$ |
| Only offset known | Raw rows must recover a positive vector up to its normalized law | $`n`$ |
| Neither known | Report differences must recover a positive vector up to its normalized law | $`n+1`$ |

In the last two cases, a nonzero hidden direction can perturb some positive
$`x`$ without staying proportional to it, changing its normalized law.
This justifies the stronger rank requirement rather than relying on a
count of formal parameters. With unknown unrestricted offset, adjusting
that offset preserves the baseline observation, so it supplies no extra
law distinction after differencing.

The rational Brier formulas (19) check: the $`n`$ differences sum to
$`s(n-1)`$, and the three-outcome numeric example decodes to the stated
$`s=3,b=5,p=(1/6,1/3,1/2)`$.

The principal expressly scopes the lower bound to fixed probes and
excludes a general claim about optimized reports or adaptive policies.
That scope should be retained. If a later document counts a “direct
difference query,” it must mean observing $`v(q)-v(q_0)`$, rather than
applying an unknown offset afresh to a newly constructed difference gamble.

### 3.3 Report, objective value and realization remain distinct

The principal correctly separates the score vector, its exact expectation,
the exact optimal report, the scalar attained risk and a realized score.
Its Brier excess-risk implication is conditional on a certified excess
risk, and its binary single-risk positive case prevents overstatement.
The log probes use finite rows, with their nonrational-coefficient boundary
stated separately from mathematical recoverability.

A possible additional short hostile example, already recorded in the
scoring-span review, is that evaluating all selected reports on the same
realized outcome $`Y`$ causes the calibration algebra to decode $`e_Y`$.
An invertible score matrix and a normalized answer do not certify that
the original observations were subjective expectations. The principal's
current distinctions are correct without this additional example.

### 3.4 State-dependent additions preserve the stated service only

Adding one finite outcome vector $`h`$ to every action changes each
expected cost by the same $`hp`$ at a fixed law. It preserves pointwise
action comparisons and regret. Across a law family, $`hp`$ varies with
the law, so absolute minimax decisions need not be preserved. The two-state
example in section 10 correctly changes the minimax choice from $`B`$ to
$`A`$, while keeping all pointwise differences and minimax regret unchanged.

This also resolves a minor source-domain difference: Ramaswamy–Agarwal and
Ramaswamy–Agarwal–Tewari use nonnegative finite loss tables. A finite real
action-loss table can be made nonnegative by adding
$`h_i=-\min_a c_{ai}`$ at each outcome. That transports their pointwise
Bayes-action/excess-risk comparison, with the absolute-minimax qualification
just described. It does not justify discarding baselines for every service.

### 3.5 Sections 9–11 retain their required boundaries

PI-9 uses a finite menu, the full simplex, exact fixed linear observations
and permission to return some minimizing action. Its necessity argument
excludes a common optimum from the original menu using the strict midpoint
inequality, including a discarded action that merely ties. The connection
to ordinary feature-surrogate fibers and the norm regret bound are accurate.
The ordinal-median and adaptive-prefix examples properly distinguish
different information interfaces.

PI-10 correctly excludes constant targets from its nonconstant-target
necessity claim. PI-11 states a freely chosen linear-measurement repair
rank, and separately handles restricted query availability and smaller
decision services. This is consistent with the inherited phase-two rank,
repair and small-edit distinction.

PI-12 correctly specifies a complete payoff box and existential projection.
Its independent-row interpolation, zero-probability handling, shared-stake
counterexample and independent box-error extension are sound. It does not
claim to eliminate arbitrary shared-parameter products or provide a
general robust bilinear solver.

## 4. Exact primary-source import record for this audit

These are targeted re-inspections, not a broad literature search:

| Primary source | Locators actually revisited and audit conclusion |
|---|---|
| [Halpern–Pucella, Characterizing and Reasoning about Probabilistic and Non-Probabilistic Expectation](https://www.cs.cornell.edu/home/halpern/papers/expectation.pdf) | §2 finite-domain qualification; §2.1 Proposition 2.1; §2.2 Theorem 2.4 and its following canonical-set paragraph. The normalized functional/closed convex set comparison is sound; A1 restores the exact imprecise-expectation assumptions. |
| [Gneiting–Raftery, Strictly Proper Scoring Rules, Prediction, and Estimation](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf) | §2.1 equation (2); §3.1 Definition 2/Theorem 2 and Brier/log examples. The loss sign, finite-interior report restriction and source attribution are correct. A2–A3 improve the source record's wording and locator coverage. |
| [Frongillo–Kash, On Elicitation Complexity](https://raf.prof/media/papers/elic-complex.pdf) | §2 definitions and the paragraph following Definition 7; §2.1 Proposition 2/Lemma 1; Appendix A's proof of Lemma 1. The principal keeps their identifiable-elicitation dimension distinct from fixed-query cost and unrestricted encoding dimension. |
| [Abernethy–Frongillo, A Characterization of Scoring Rules for Linear Properties](https://proceedings.mlr.press/v23/abernethy12/abernethy12.pdf) | §3 Definitions 2–3; §4 equations (6)–(7), Lemma 7. The minimization wording in Definition 2 and maximized displayed Bregman construction are both visible. The source note accurately records this local sign-reading qualification and independently derives the squared-loss case. |
| [Boyd–Vandenberghe, original Convex Optimization lecture slides](https://web.stanford.edu/~boyd/cvxbook/bv_cvxslides_original.pdf) | Slide 2–19, PDF p.34, and slides 5–9 through 5–12, PDF pp.125–128. They support the separation and finite LP duality comparisons. The linear-inequality refinement does not require a strictly positive probability vector. A6 scopes the polytope sentence. This audit did not retry or claim to read the unavailable full-book PDF. |
| [Ramaswamy–Agarwal, Convex Calibration Dimension for Multiclass Loss Matrices](https://jmlr.org/papers/volume17/14-316/14-316.pdf) | §2.3's unique-optimum action premise and Definition 1; §2.4 Definitions 4–5; Theorem 6 and adjacent Theorem 7 qualification. These verify the ignored-action and common-optimum comparison. The earlier targeted review already inspected the ordinal example and dimension discussion; their derivations were not rerun here. |
| [Ramaswamy–Agarwal–Tewari, Convex Calibrated Surrogates for Low-Rank Loss Matrices](https://proceedings.neurips.cc/paper_files/paper/2013/file/a5cdd4aa0048b187f7182f1b9ce7a6a7-Paper.pdf) | Theorem 3 and proof, printed pp.3–4. Its factorization, squared feature estimator and linear argmin are direct ordinary antecedents. Its displayed added constant is scalar; the principal identifies the state-dependent baseline extension through its own cancellation argument. |

The inherited comparison was checked selectively against paper_v2.md
§§7.2–7.3 and the exact theorem scope at the start of
v2/derivations/10_f16_coherent_recovery.md, with the existing retention
review's locators. These support the inheritance statements in P02-I1.
The detailed F16 envelope proof was not re-audited.

The internal-reading list in the source record can additionally link
scoring_span_review.md, decision_source_comparison.md and
payoff_uncertainty_projection.md, since those later notes carry qualifications
not all present in the initial scoring_sources.md.

## 5. Credible ordinary comparison

A minimal adequate ordinary comparator for the basic recovery claims is a
finite normalized probability vector, a matrix of known contingent losses,
kernel/rowspace tests and linear programming over compatible laws. Merely
showing an advantage over one marginal probability or one scalar expected
loss would be weaker than this established baseline.

The strongest credible combination for the **audited finite service** also
permits task-property scoring, low-rank expectation codes, action-region
geometry, nuisance variables and their declared dependence, and a nonlinear
median report when that is the requested decision. It can retain the same
information and use the same algebra as the proposed value representation.
The principal allows these strong comparisons and does not require the
ordinary method to reconstruct a full law unnecessarily.

This comparison does not make exact expectations, rich report access,
statistical accuracy or a successful optimizer free. If later work compares
learned implementations, both sides need the same initial evidence and an
explicit access, acquisition, precision and computational-cost contract.
Neither a rank identity nor elicitation of the correct population optimizer
supplies that learning contract.

The result is a precise ordinary-method comparison, rather than a source
claim that one paper already states every PI-7–PI-12 formulation verbatim.
Conversely, failure to locate those exact formulations in the inspected
papers is insufficient to establish originality.

## 6. A narrower contribution record without inventing novelty

The existing phase-wide P3-N01 object links uncertain logical forecasts,
paid computation and comparisons under changes of evidence, objective or
program. The audited artifact establishes a substantially narrower object:

> A finite information-audit interface for retained expected-loss records,
> separating exact law recovery, selected expected losses, identified
> intervals and optimal-action service, with explicit score calibration,
> unknown-unit and bounded-payoff assumptions.

Its currently visible mathematical content includes the full score
affine-span proof and calibration counts, essential-action information
criterion, nuisance-specific obstructions, exact box-payoff projection, and
their links to inherited retention/repair. These are concrete contents that
can be assessed as a modest formal synthesis or adaptation. Describing them
that way does not require a new general probability or learning theory.

A local record can therefore separate the following fields:

| Field | Precise candidate wording |
|---|---|
| Object | The finite information-audit interface just stated. |
| Type | Formal reconstruction and scoped synthesis/adaptation. |
| Delta to be assessed | An explicit, reusable service contract connecting the reconstructed results and nuisance assumptions to retention, repair and affine certification; not exclusive numerical capability. |
| Magnitude established | Mathematical scope and constructive examples under finite exact or explicitly bounded uncertainty premises. |
| Ordinary comparator | Finite probability/credal models plus linear algebra/LP, property scoring and calibrated expectation-code decisions. |
| Further claims not established by this audit | A learning/refinement duty, an acquisition or resource advantage, or priority for the component formulations; implementation/runtime claims are not assessed here. |

This wording names a possible contribution **object**, not a support verdict.
Its value as a useful synthesis must be assessed from its concrete
integration and intended use. An ordinary combination reproducing its
outputs is compatible with the author's contribution criterion, but a
list of familiar ingredients or a relabeling is insufficient on its own.

Suggested replacement for the source record's closing contribution paragraph:

> The sources provide strong ordinary implementations of the finite
> expectation, property and decision services studied here. P3-02 records
> a scoped reconstruction and synthesis of their information requirements,
> including explicit calibration and payoff-uncertainty cases. No exclusive
> capability, learning duty or resource advantage over the named combination
> has been established. The finite information-audit interface is a narrower
> candidate for assessment under the author's synthesis/adaptation criterion.
> This source audit supplies no change to the existing phase-wide P3-N01
> disposition or to any gate.

This preserves the continuing obligation while avoiding an unsupported
conclusion that ordinary ancestry rules out every local adaptation.
Mathematical task completion, local attribution, contribution support and
phase advancement remain separate assessments.

## 7. Limits of this audit

This is an internal source and reasoning check of the recorded snapshot.
It does not establish independent peer review, empirical generalization,
worldwide priority, a final challenge result or an advancement decision.
Any edits made after the recorded hashes are outside this snapshot unless
subsequently checked. The requested principal/status/clock/ledger files
were not edited by this reviewer.
