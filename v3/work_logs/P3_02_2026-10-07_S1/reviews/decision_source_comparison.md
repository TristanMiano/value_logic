# P3-02 — ordinary comparisons for finite decision recovery

Contributor: **ChatGPT (GPT-6 Astra Pro)**, `/root/scoring_sources`.
Same-model internal, nonblind source reconstruction and proof critique.
No clock, ledger, status, gate or publication edits. Development evidence only.

Inspected [decision_geometry.md](decision_geometry.md), SHA256
`b6fc9c642e025fd9bc39c889f496d6c09be3685954cce0d652fbdaffa14bc142`.
The reading below is targeted, not a comprehensive novelty search.

## 1. Assessment of the proposed characterization

For a nonempty finite menu of finite real loss rows `c_a`, merge duplicate
rows and let `E` contain those actions uniquely optimal at some strictly
positive probability law. Put `A=[1^T;L]`. The proposed equivalence is sound:

\[
\exists s\quad s(Lp)\in\arg\min_a c_ap\quad\forall p\in\Delta_n
\quad\Longleftrightarrow\quad
c_a-c_b\in\operatorname{row}(A)\quad\forall a,b\in E.
\]

The geometry note's proof handles the critical issue correctly. Discarded
actions can tie on special fibers, so merely showing two different minimizing
**essential** actions would not itself prove that the original menu has no
common optimum. Its strict midpoint kink rules out **every** original action
being optimal at both endpoints, closing that gap.

Other necessary proof components are also present: duplicate rows are merged;
essential cells cover the envelope by closure; adjacency is taken through
interior facets; the full-dimensional cell graph is connected; and dimension
one and a singleton essential menu are covered. I found no counterexample or
missing geometric hypothesis within the finite, full-simplex, fixed-linear,
exact, some-optimal-action scope.

This conclusion does not identify the theorem as historically new. The
immediate ordinary precedents already include Bayes-region geometry, loss
matrix rank constructions and expectation-based surrogate learning.

## 2. Closest selected primary sources

### Ramaswamy and Agarwal (2016)

[*Convex Calibration Dimension for Multiclass Loss Matrices*](https://jmlr.org/papers/volume17/14-316/14-316.pdf),
JMLR 17(14):1–45, primary 45-page PDF.

Inspected locators: §2.3, Definition 1; §2.4, Definition 4;
§3.1, Theorems 6–7 and their displayed arguments; §3.3, Example 8;
§4, Definition 10; §4.1, Theorem 12 and proof; §4.2, Theorem 16 statement;
§4.3 opening ordinal-loss comparison.

Their loss matrix has **outcomes as rows and actions as columns**, the
transpose of our action-row convention. Trigger probability sets are the
laws under which an action is Bayes optimal. Theorem 6 requires each
surrogate positive-normal set to lie in a single trigger set. Their
calibration definition concerns a positive expected-surrogate-risk gap for
wrongly decoded actions; it is stronger than correctness only at one exact
optimizer. Convex calibration dimension minimizes the dimension of the
surrogate report domain. Theorem 12 supplies an affine-dimension upper bound;
ordinal absolute loss has a one-dimensional convex calibrated surrogate.
No exact essential-action/fixed-linear-summary iff was located in these
selected passages. The longer lower-bound proof and ranking applications
were not imported.

### Ramaswamy, Agarwal and Tewari (2013)

[*Convex Calibrated Surrogates for Low-Rank Loss Matrices with Applications to Subset Ranking Losses*](https://proceedings.neurips.cc/paper_files/paper/2013/file/a5cdd4aa0048b187f7182f1b9ce7a6a7-Paper.pdf),
NIPS 2013, primary nine-page PDF.

Inspected: §2 setup/calibration interface; §3, Theorem 3 and its proof,
printed pp.3–4. Given a finite target factorization
`ell(i,a)=alpha_i^T beta_a+c`, the construction uses the squared loss
`||u-alpha_i||^2`, whose optimal report is `E_p alpha_Y`, and decodes with
`argmin_a u^T beta_a`. The displayed argument proves calibration from this
factorization. This directly anticipates learning a task-sufficient vector
of expected features instead of the full law. It is a sufficient low-rank
construction, not the proposed necessity characterization for a fixed
observed summary after discarding nonessential actions. Known constants and
common outcome-dependent baselines must be handled explicitly when adapting
its exact factorization and dimension count.

### Property-elicitation context already inspected

[Frongillo and Kash (2015), *On Elicitation Complexity*](https://raf.prof/media/papers/elic-complex.pdf),
§2, Definitions 1–7 and §2.1, Lemma 1, is recorded in
[scoring_sources.md](scoring_sources.md). Its link-function viewpoint permits
a desired property to be obtained from another elicited report. Its
dimension count depends on the allowed intermediate property class. A fixed
linear expectation vector is one such class, and is substantially more
restrictive than all nonlinear elicited reports. No general elicitation
lower bound is substituted for the present geometry argument.

## 3. Direct relation to the source's Bayes-region condition

This paragraph is our specialization of the 2016 source's definitions.
For a fixed summary matrix `L`, consider the ordinary squared surrogate

\[
\psi_i(u)=\|u-L[:,i]\|_2^2.
\]

Its population risk is uniquely minimized at `u=Lp`. Consequently, the
probability set making a fixed report `u` optimal is precisely

\[
\{p\in\Delta_n:Lp=u\}.
\]

The source's necessary containment of such a set in one Bayes action region
therefore becomes the existing common-optimum fiber condition. The proposed
essential-difference theorem characterizes that condition for this fixed
linear family using elementary finite polyhedral geometry. It is a precise
adaptation within a mature ordinary comparison framework, rather than a new
kind of probabilistic or utility representation.

The converse quantitative bridge is also elementary. If for essential actions

\[
c_a=c_{a_0}+\alpha_a\mathbf1^T+\beta_a L,
\qquad q_a(u)=\alpha_a+\beta_a u,
\]

decode `u` by minimizing `q_a(u)`. Write `y=Lp`, let `a` be the decoded
action, and choose `b` minimizing `q_b(y)`. Since `q_a(u)<=q_b(u)`,

\[
0\le c_ap-\min_b c_bp
\le(\beta_a-\beta_b)(y-u)
\le M\|u-y\|,
\]

where `M=max_(a,b in E)||beta_a-beta_b||_*` for the dual norm. In Euclidean
norm, the squared surrogate excess risk is `||u-y||_2^2`, giving a
square-root target-regret bound. This reconstructs the familiar
least-squares/linear-decoder mechanism. It supplies no data, uniform learning
guarantee, acquisition policy or new convergence theorem.

## 4. A decisive distinction: fixed expectations versus a median report

Take ordered outcomes and actions `1,...,n`, with `n>=2`, and semantic loss

\[
c_a(i)=|a-i|.
\]

Every action is essential: put sufficiently high probability on outcome `a`
while keeping all coordinates positive. Adjacent rows satisfy

\[
c_{a+1}-c_a=2\mathbf1_{\{i\le a\}}-\mathbf1,
\qquad a=1,\ldots,n-1.
\]

Together with the normalization row these differences span `R^n`, since
successive prefix indicators recover singleton indicators. The theorem
therefore requires **n-1 independent fixed expectation coordinates** for
global exact decision recovery. In this particular representation class,
the decision service forces full-law identifiability.

Nevertheless, an optimal action is any median. The ordinary convex loss
`|u-Y|`, on one real report coordinate `u`, has median reports as its
minimizers. Decoding by a nearest permitted integer gives an optimal action.
This is the ordinal surrogate covered by the 2016 source; its reported
dimension is one. The population optimizer is a nonlinear property of `p`,
so it is outside the fixed `Lp` class.

For three states the target rows are

\[
C=\begin{pmatrix}0&1&2\\1&0&1\\2&1&0\end{pmatrix}.
\]

All three actions are essential and two differences are independent modulo
constants. Thus no single fixed affine expectation determines a Bayes action
for every law, although a single nonlinear scalar median report does. The
linear-summary lower bound is therefore **not** a lower bound on convex
calibration dimension, arbitrary nonlinear representation dimension, or
storage of an already computed action label.

An action label among `n` choices itself uses only `ceil(log2 n)` bits once
computed. That storage fact pays none of the cost of finding or learning it.

## 5. Adaptive expectation queries are another different service

The same ordinal example shows why “fixed” must remain explicit. Suppose
the information interface allows exact queries

\[
F(j)=P(Y\le j),
\]

each a known linear indicator expectation. Binary search for the first
`j` with `F(j)>=1/2` returns a lower median using at most
`ceil(log2 n)` adaptively selected queries. Ties cause no problem: that
chosen lower median is Bayes optimal. The union of available prefix queries
still has `n-1` members, but a single path need not ask them all.

This is our elementary query construction, not a claim imported from the
surrogate papers. The adaptive transcript is not one fixed matrix `Lp`, so
it does not contradict the rank theorem. Each query must actually be
available at its charged cost; noisy or merely learned prefix estimates
require an additional error/decision-margin argument. The theorem supplies
no lower bound against such adaptive paid-acquisition policies.

## 6. Qualifications to preserve in canonical wording

- Duplicate loss rows must be merged before defining unique interior optima.
  Otherwise several copies of every useful row could make `E` empty while
  the decision still varies.
- Discarding nonessential actions preserves existence of some optimum,
  including on the boundary, but need not preserve every original tie or an
  externally prescribed tie rule.
- The universal source is the full simplex. Restricting it to a finite
  catalogue or a smaller affine/convex family changes the information test.
- The menu and its semantic losses are fixed and known. A later new action
  can introduce a previously irrelevant direction; that is a retention/repair
  question rather than a consequence of current decision sufficiency.
- The observations are exact and linear with one fixed matrix. Noise,
  adaptive queries, nonlinear encodings and unknown loss parameters change
  the service. Near an action boundary, arbitrarily small error can affect
  the exact optimal label even when regret is small.

Finite real-valued losses can be shifted by a common outcome-dependent vector
to make every loss nonnegative for the surrogate papers' convention; that
shift preserves all action comparisons. It can change a raw matrix rank, so
the source rank formulas should not be transplanted without tracking the
shift and deterministic constants. Essential loss differences are invariant
under the common baseline shift.

## 7. Attribution and scientific disposition

The inspected primary literature already supplies the Bayes-region and
normal-set framework, low-rank expectation codes with calibrated decoders,
and smaller nonlinear elicited reports. The present fixed-linear
essential-action characterization is proved in the accompanying geometry
note and survived this separate same-model critique. I did not locate its
exact iff wording as a numbered result in the selected sources. That narrow
reading limit supports neither an originality claim nor a priority claim.

A suitable disposition is **finite reconstruction/adaptation with explicit
service and comparison boundaries**. Any contribution claim must point to
additional concrete project integration or transport guarantees and name its
comparison scope. This review does not decide P3-N01 or attempt a gate.
