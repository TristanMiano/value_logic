# P3-02 — scoring, expectation and information recovery

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
`/root/scoring_sources`. Same-model internal, nonblind reconstruction.
This note owns no clock, time-ledger, gate or publication decision. Concurrent
reviewer time is not additional principal research credit. Its constructions
are development material, not a frozen challenge.

## 1. Selected primary-source contracts

Read first: `v3/literature/01_source_contracts.md` entries S02/S09/S13 and their
selected source notes; the corresponding entries of `00_orientation.md`.
The later source contracts supersede orientation-only descriptions.

### S02 — Gneiting and Raftery (2007)

[*Strictly Proper Scoring Rules, Prediction, and Estimation*](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf),
JASA 102(477), 359–378; inspected 20-page author-hosted PDF.
Locators: §1; §2.1, equations (1)–(2); §2.2, equations (6)–(7); §3.1,
Theorem 2 and Examples 1/3, printed pp.362–363.

The paper uses rewards: a report `q` receives `S(q,i)` when outcome `i`
occurs. Strict propriety means the unique maximizer of the expected reward
under a fixed law `p` is `q=p`. Negation gives our loss convention. Positive
scaling and an outcome-dependent addition common to every report preserve
propriety. The finite Brier and logarithmic examples give squared-Euclidean
and KL excess-risk divergences. Selected definitions, formulas and the short
convex-representation proof were inspected; no statistical estimation or
calibration theorem is imported. The constructions below are elementary
specializations and information-recovery arguments, not new scoring rules.

### S13 — Halpern and Pucella (2007)

[*Characterizing and Reasoning about Probabilistic and Non-Probabilistic Expectation*](https://www.cs.cornell.edu/home/halpern/papers/expectation.pdf),
49-page author manuscript. Locators: §2.1, Proposition 2.1/Theorem 2.2 and
its displayed proof; §2.2, Theorem 2.4 and the following paragraph; Example
2.11. These are the same finite interfaces already inspected for P3-01.

On all gambles measurable for a fixed finite event algebra, an additive,
affinely homogeneous, monotone expectation determines a unique probability
measure on that algebra. Lower expectations use superadditivity and positive
affine homogeneity; their full functionals determine a closed convex credal
set, rather than an arbitrary generating list of laws. Individual event bounds
can leave different expectations of general gambles possible. Consequently,
recovering probabilities from a full coherent linear functional, or recovering
a closed convex set from a full lower functional, is established comparison
material. The finite original argument and selected statements were inspected;
the paper's general axiomatization and appendix proofs were not re-audited.

### S09 — de Cooman and Hermans (2008)

[*Imprecise Probability Trees: Bridging Two Theories of Imprecise Probability*](https://arxiv.org/pdf/0801.1196),
30-page PDF displaying `arXiv:0801.1196v1`, January 8, 2008.
The version-suffixed URL returned an error; the unsuffixed primary URL
succeeded. Locators newly revisited: §§3.1–3.2, D1–D4, equations (4)–(5),
Proposition 2 and the concluding linear-prevision paragraph, printed pp.8–10.

Lower and upper previsions have supremum-buying/infimum-selling-price
interpretations for known gambles. When they coincide, the common functional
is a linear prevision; its restriction to event indicators is a finitely
additive probability. On a finite algebra this is the ordinary finite law.
The source's acceptance-cone conventions and its distinction between present
conditional prices and later dynamic beliefs matter. No theorem about
arbitrary bounded-stakes, fee-paying controllers is imported. The finite
signed-portfolio argument in §8 below is our direct reconstruction with its
own stated sure-gain convention; it is not identified wholesale with D1–D4.

### Additional comparator — Frongillo and Kash (2015)

[*On Elicitation Complexity*](https://raf.prof/media/papers/elic-complex.pdf),
12-page author-hosted version;
[NIPS 2015 primary proceedings record](https://papers.nips.cc/paper_files/paper/2015/hash/f0bbac6fa079f1e00b2c14c1d3c6ccf0-Abstract.html).
Locators: §2, Definitions 1–7, Proposition 1/2, vector-moment example and the
paragraph following Definition 7; §2.1, Lemma 1 on linear properties.

A property is a function of a distribution, possibly vector-valued. Eliciting
it means arranging for that property to minimize expected loss. Identification
uses an expected equation instead. An indirect link can recover a desired
property from another elicited property. Their dimension comparisons restrict
the admissible intermediate properties; the paper explicitly warns that
unrestricted real encodings collapse such dimension counts. This is an
especially strong ordinary comparator for retaining only task-relevant
expectations. We import the selected interfaces and warning, not its general
lower-bound or Bayes-risk theorems. The paper's terminology must not be
confused with unique recovery from an already observed finite vector `Lp`.
Lemma 1's affine-hull dimension formula was inspected as a close comparison
lead under its identifiable-elicitation definition, not an unrestricted
dimension theorem for arbitrary representations.

### Additional orientation — Lambert, Pennock and Shoham (2008)

[*Eliciting Properties of Probability Distributions*](https://ai.stanford.edu/~nlambert/papers/EC2008-elicitability.pdf),
10-page author-hosted EC 2008 paper. Inspected §§2.1–2.3, Definitions 1–3,
and the beginning of §4. The score is an outcome-contingent contract for a
reported property; its optimal report supplies that property under the stated
expected-utility interpretation. The paper restricts its main scalar-property
analysis to convex probability domains and continuous, not locally constant
properties. No unrestricted elicitation-complexity lower bound is imported.
This earlier source is attribution/context; the P3-02 constructions need no
additional theorem from it.

## 2. Six objects that must not share one untyped name

Let `Omega={1,...,n}`, `p` be the law, `q` a report, and
`ell(q,i)` a known semantic loss. Put

\[
R_p(q)=\sum_i p_i\ell(q,i).
\]

| Object retained | What it supplies |
|---|---|
| Known loss vector `ell(q,.)` | The contract for every possible outcome. For Brier/log scores it can encode the **report** `q`; it supplies no additional fact equating `q` with `p`. |
| One exact subjective expectation `R_p(q)` | One known linear measurement of `p`, in the declared payoff units. |
| Several expectations or the whole surface `q -> R_p(q)` | More measurements of the same fixed `p`; full-law recovery depends on their span. Strict propriety makes the full surface informative through its minimizer. |
| An exact optimal report `q*` | Under strict propriety, the full allowed report class and exact expected-loss optimization, `q*=p`. This is a report/optimizer, not the scalar value of its objective. |
| A learned estimate `Rhat(q)` or report `qhat` | A prediction about one of the preceding objects. Coherence, error control and outcome accuracy each need evidence or assumptions. |
| One realized loss `ell(q,Y)` | An observation generated by an outcome. It may encode that outcome, a coarsening of it, or no distinction at all; one realization generally does not identify its generating law. |

If `p` is subjective, every recovery statement identifies that subjective
law. It does not prove that this law predicts the external process correctly.
If the outcome law changes with the report, the fixed-law propriety hypothesis
has changed. P3-01 already supplies a separating example for this boundary.

## 3. Brier score: constructive recovery and destructive compression

Use the multiclass loss convention

\[
\ell_B(q,i)=\|q-e_i\|_2^2,
\qquad R_p(q)=1+\|q\|_2^2-2q^\top p.
\]

Expansion and completing the square give

\[
R_p(q)=1-\|p\|_2^2+\|q-p\|_2^2.
\]

Thus the optimal report is `p`, while the scalar optimal risk
`1-||p||^2` usually loses probability information. For instance,
`p=(1/2,1/2,0)` and `p'=(1/2,0,1/2)` have identical optimal risk `1/2`.
The labels matter, so these are different laws.

At a fixed uniform report `u=(1/n,...,1/n)`,

\[
\ell_B(u,i)=R_p(u)=1-1/n
\]

for every outcome and every law. This score observation has no information
about even the realized category. More generally, one fixed report gives
only the row `ell_B(q,.)`; for `n>=3` no such single row identifies every law
on the full simplex. Two independent affine constraints at most—normalization
and this expected loss—leave a nonzero tangent direction through an interior
law. This is a linear-measurement statement, not a prohibition on arbitrary
scalar encodings.

There are simple positive cases:

\[
R_p(e_i)=2(1-p_i),\qquad
p_i=1-\tfrac12R_p(e_i).
\]

The `n-1` vertex reports for `i<n`, together with normalization, recover the
whole law. These rows are just known event-contingent losses. For arbitrary
fixed reports `q,r`,

\[
R_p(q)-R_p(r)=\|q\|^2-\|r\|^2-2(q-r)^\top p.
\]

Independent report differences spanning the simplex's tangent space therefore
also recover it. Each underlying evaluation or direct difference query needs
the same information-access/cost accounting as any other retained row.

For binary outcomes, the often-used scalar convention `(r-Y)^2` is half the
multiclass loss above. Its expected value is `r^2+p(1-2r)`; one exact value
does recover `p` if the known report satisfies `r != 1/2`. The central
nonidentification claim must therefore be scoped rather than universal.

## 4. Log score: finite positive probes

For reports with `q_i>0`, use

\[
\ell_{\log}(q,i)=-\log q_i,\qquad
R_p(q)=-\sum_i p_i\log q_i.
\]

For a true law in the report class, the excess risk is
`D_KL(p||q)` and the exact optimum is `q=p`. The scalar optimum is entropy;
the two permuted laws in §3 have the same entropy as well. At the uniform
report, both the realized and expected losses are the constant `log n`.

For each `j<n`, choose the positive rational report

\[
q^{(j)}_i=\frac{2^{\mathbf1\{i=j\}}}{n+1}.
\]

Its known loss vector and expected loss are

\[
\ell_{\log}(q^{(j)},i)=\log(n+1)-\mathbf1\{i=j\}\log2,
\quad
R_p(q^{(j)})=\log(n+1)-p_j\log2.
\]

Hence `n-1` exact values identify `p`, including boundary laws, without ever
issuing a zero-probability report. These probes again reduce to indicator
measurements with specified offsets/stakes. With an added unknown common
outcome-dependent baseline, report-risk differences cancel that baseline.

The displayed natural-log coefficients are not automatically native rational
coefficients. Special log bases and dyadic reports can produce rational rows
(for example base 2 and `(1/2,1/4,1/4)`), so the limitation is not a universal
obstruction to using any finite log-score probe. Fixed rational Brier probes
give a simpler uniform rational construction.

## 5. Finite difference-span lemma for strict propriety

**Our elementary reconstruction.** Let the report set `Q` contain the entire
open simplex `Delta_n^o`. Assume every loss vector for `q in Q` is finite
and, for each interior law `p`, the unique global minimizer over `Q` of its
expected loss is `q=p`. Fix `q0 in Q`. Then

\[
\operatorname{span}\bigl(\{\mathbf1\}\cup
\{\ell(q,\cdot)-\ell(q_0,\cdot):q\in Q\}\bigr)
=\mathbb R^n.
\]

**Proof.** Otherwise take nonzero `z` orthogonal to this span. Since
`1^T z=0`, choose sufficiently small `t>0` so `p+=u+tz` and `p-=u-tz`
are distinct interior laws. For every report `q`,

\[
R_{p_+}(q)-R_{p_-}(q)
=2t z^\top\ell(q,\cdot)
=2t z^\top\ell(q_0,\cdot).
\]

The surfaces differ by a constant and have exactly the same minimizers.
Strict propriety requires the two different laws as their unique minimizers,
a contradiction. Finite-dimensional linear algebra then selects `n-1`
difference rows independent modulo constants. Their expectations and
normalization identify every normalized law. End of proof.

This gives existence of a finite separating subset of a full strict score
surface. It does not give a cheap method to locate a well-conditioned subset
for an arbitrary score, nor certify the values used. With raw evaluations,
one baseline plus `n-1` additional reports suffices; with a direct difference
operation, there are `n-1` difference measurements. The Brier/log constructions
avoid an additional measured baseline because their constant pieces are known.

The hypothesis covers interior log reports with finite loss vectors. Allowing
a restricted law/report family can change the number of measurements required.
This lemma is proved here as a finite consequence of strict propriety and
linear algebra. It is not offered as a novel theorem relative to the scoring
or information-recovery literature.

A targeted antecedent check found the immediate convex/Savage representation
in S02, Theorem 2, and the restricted affine-dimension comparison in Frongillo
and Kash, §2.1, Lemma 1. No exact separately numbered difference-span result
was located in the selected reading; this is not a priority finding.
Also inspected:
[Abernethy and Frongillo (2012), *A Characterization of Scoring Rules for Linear Properties*](https://proceedings.mlr.press/v23/abernethy12/abernethy12.pdf),
13-page COLT primary PDF, §4, equations (6)–(7) and Lemma 7, printed p.27.7.
Its Bregman construction elicits a vector expectation. The PDF prints an
`argmin` in Definition 2 but uses reward maximization in §1 and equations
(6)–(7); our comparison follows the displayed construction's reward sign.
Its full characterization and market-equivalence theorems were not imported.

## 6. Task-specific expected losses are already elicitable

Let `C[:,i]` be a known vector of losses useful for the actual task. Its mean
`mu=Cp` can be learned/reported directly using

\[
\ell_C(r,i)=\|r-C[:,i]\|_2^2.
\]

Writing `X=C[:,Y]`, expansion gives

\[
\mathbb E\|r-X\|^2=\|r-\mu\|^2+
\mathbb E\|X-\mu\|^2.
\]

Thus the unique optimal report is `mu`; recovering the whole law is
unnecessary. Finite outcomes make all required second moments finite. This
is the ordinary vector-mean elicitation comparator described by Frongillo
and Kash, reconstructed explicitly for this task's loss rows. Expected-loss
inversion, elicitation, empirical estimation and decision preservation remain
different operations. A correct expectation report can suffice even when
many laws produce it.

The phase-two native-language distinction is exact: a **fixed** rational
Brier report produces a known rational loss row and an expectation affine in
uncertain `p`. Optimizing a variable report contains products such as
`q_i^2` and `q_i p_i`; that full optimization is not automatically a native
finite piecewise-affine expression. It can be an ordinary external comparator,
or require a declared finite report set, extension or justified enclosure.

## 7. Learned estimates and observed scores require another bridge

For Brier risk, suppose an estimated surface satisfies the independently
certified uniform error bound

\[
|\widehat R(q)-R_p(q)|\le\eta
\]

on a report domain containing `p`. If
`Rhat(qhat) <= inf_q Rhat(q)+delta`, two applications of the error bound give

\[
\|\widehat q-p\|_2^2
=R_p(\widehat q)-R_p(p)\le2\eta+\delta.
\]

This is a conditional deterministic bound. Propriety does not produce the
error certificate, observational feedback, sample count or optimization
accuracy for free. A perfectly coherent Brier surface under the wrong law
can still produce the wrong forecast of the external process. With certified
errors only at finite probes, use their simplex feasibility set and certified
linear bounds instead of asserting a uniform surface estimate.

If the **distribution** of a realized score at fixed report `q` is known,
then it identifies the total probability of each level set of
`i -> ell(q,i)`. It identifies `p` on the unrestricted finite class exactly
when that map is injective. This is different from being given one realized
score, or only its expectation. At nonuniform reports with distinct
components, Brier and log scores can encode the realized category; at uniform
reports they encode none. Repeated observations can support estimation under
a declared sampling model, but are not the exact expectation oracle assumed
in §§3–5.

## 8. Coherent expectations: the finite signed-portfolio check

For known payoff columns `L[:,i]` and proposed fair prices `v`, allow every
finite signed position vector `a` and define the trader's net payoff

\[
g_a(i)=a^\top(L[:,i]-v).
\]

There is no `a` with `g_a(i)>0` **for every** state exactly when

\[
v\in\operatorname{conv}\{L[:,1],\ldots,L[:,n]\}
\iff (\exists p\in\Delta_n)\ Lp=v.
\]

If `Lp=v`, every such payoff has expectation zero and cannot be strictly
positive everywhere. If `v` lies outside the finite closed convex hull,
strict separation supplies the required signed position (reverse its sign
if needed). This is the usual finite convex-separation/coherence comparison,
reconstructed here without invoking a stronger behavioral theorem.

Do not replace the stated sure-gain condition by “nonnegative everywhere and
positive somewhere” without another assumption. Example: one payoff
`L=(0,1)` priced at `v=0` is consistent with `p=(1,0)`, while buying it has a
nonnegative payoff that is positive in the second state. Full support or the
appropriate relative-interior condition gives a stronger comparison.
Restricted positions and fees can also change the criterion. Existence of
a coherent law is not uniqueness, and neither asserts empirical correctness.

## 9. Units, common baselines and nonlinear transforms

For a common positive scale `a` and outcome-dependent baseline `b_i`
independent of the report, put

\[
\ell'(q,i)=a\ell(q,i)+b_i.
\]

Then `R'_p(q)=aR_p(q)+p^T b`: report preferences and strict propriety are
preserved. Risk differences remove the common baseline and scale by `a`.
With known scale, the same difference probes recover the law. Unknown
scales/stakes require their own identifying information; an unchanged optimal
report alone does not reveal numerical payoffs. A rich whole surface can
sometimes identify a scale, so unknown scale is not an unconditional
nonidentification theorem.

A nonlinear increasing transform applied **to each realized loss** need not
preserve propriety. For binary loss `(r-Y)^2`, squaring the loss gives
`(r-Y)^4`. Its expected-loss minimizer obeys

\[
\frac{r}{1-r}=\left(\frac{p}{1-p}\right)^{1/3}.
\]

At `p=1/9`, it is `r=1/3`, not the law. In contrast, an increasing transform
applied after the expectation preserves its report ordering but is generally
not the expectation of that transformed realized payoff. These are different
operations. The numerical example is our own direct derivative calculation;
it is not a new scoring-rule obstruction.

## 10. Disposition for P3-02

The strong ordinary comparisons already contain: coherent full expectation
representations; nonunique laws compatible with finite queries; proper full-law
elicitation; task-specific vector-mean elicitation; and explicit restrictions
needed to make real-valued dimension counts meaningful. A cost notation or
the recovery identities alone establish no contribution delta.

Useful project-facing content can instead state exactly what survives a
restricted retained row set, certified error, units change or semantic repair,
and what operations and evidence are required to transport it. The present
note supplies finite positive constructions, deliberate score-compression
failures and a precise ordinary baseline. It does not establish priority,
P3-N01 support, a phase gate, induction duties or a counterfactual semantics.

Retrieval limit: the first broad author-name search was noisy; exact-title
queries found the additional primary PDFs. No originality inference follows
from those retrieval results. No original de Finetti monograph was inspected;
the finite behavioral connection is sourced through S09/S13 and independently
reconstructed above. All mathematical checks in this note are finite algebraic
arguments; no randomized experiment or external replication is claimed.
