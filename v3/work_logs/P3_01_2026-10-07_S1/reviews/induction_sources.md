# P3-01: induction and ordinary comparison source reconstruction

Research date: 2026-10-07 UTC. Researcher: GPT-6 Astra Pro,
`/root/p301_induction_sources`. Same-model internal reconstruction, not a blind
independent review. This note proposes problem-contract ingredients only; it does
not execute P3-02, establish phase-three novelty, or certify a practical logical
inductor.

## 1. Selected primary definitions

### LI — Garrabrant et al., Logical Induction (2016)

[Primary PDF](https://intelligence.org/files/LogicalInduction.pdf).
Selected reconstruction, not a complete paper summary:

\[
P_n:S\to\mathbb{Q}\cap[0,1],\qquad
D_1\subseteq D_2\subseteq\cdots,\quad |D_n|<\infty.
\]

The sequences are computable. Worlds assign Boolean sentence values;
\(PC(D_n)\) enforces Boolean compositionality and the available sentences.
Completeness means \(PC(\bigcup_n D_n)=PC(\Gamma)\).
An efficient trader generates each continuous, expressible, finite portfolio
in polynomial time in unary \(n\). Its holdings are

\[
H_n=\sum_{i\le n}\sum_j \xi_{ij}(P)
\bigl(\phi_{ij}-P_i(\phi_{ij})\bigr).
\]

Exploitation means
\(\{W(H_n):n\ge1, W\in PC(D_n)\}\) is bounded below and unbounded above.
The criterion excludes every such efficient trader.
Property theorems assume consistent, computably enumerable \(\Gamma\).
Expectations additionally use computable-function representability and
provably unique, bounded variables:

\[
E_n(X)=\frac1n\sum_{i=0}^{n-1}P_n(X>i/n).
\]

Locators: Definitions 3.0.1, 3.1.1–3, 3.2.1–4, 3.3.1, 3.4.3–5,
3.5.1; Section 4 assumptions; Definitions 4.8.1–2.
Theorems 4.1.1–2: convergence/coherence; 4.2.1: efficient provable sequences;
4.3.8: feedback-conditioned unbiasedness; 4.4.2: relative pseudorandomness;
4.8.4: asymptotic linearity; 4.8.6: indicators; 4.8.10: expectation provability.
Section 5.5 and Proposition 5.5.1 distinguish computability from practical runtime
and computable general convergence rates.

### H — Freund and Schapire, Hedge (1997)

[Author-hosted primary PDF](https://cseweb.ucsd.edu/~yfreund/papers/adaboost.pdf).
Full paper title: *A Decision-Theoretic Generalization of On-Line Learning and an
Application to Boosting*, JCSS 55(1), 119–139.

Section 2, Figure 1 (printed page 4), and Theorem 2/Corollary 3 (page 5)
specify bounded full-feedback losses and a finite collection of alternatives.
For \(N\) alternatives, uniform initial weights, and \(0<\beta<1\):

\[
\pi_{i,t}=\frac{w_{i,t}}{\sum_jw_{j,t}},\qquad
w_{i,t+1}=w_{i,t}\beta^{\ell_{i,t}},\qquad 0\le\ell_{i,t}\le1.
\]

The complete loss vector arrives after the allocation. With
\(L_H=\sum_t\sum_i\pi_{i,t}\ell_{i,t}\) and
\(L_i=\sum_t\ell_{i,t}\), Corollary 3 gives

\[
L_H\le\frac{\ln(1/\beta)}{1-\beta}\min_i L_i
       +\frac{\ln N}{1-\beta}.
\]

This is a finite comparison with the supplied alternatives, not a guarantee
against every efficient logical trading strategy. The PDF's extracted text is
poorly encoded; the algorithm and bound were checked visually on the page images.
The 1997 JCSS citation is verified on
[Freund's publication list](https://cseweb.ucsd.edu/~yfreund/papers/index.html),
entry 39.

### DF — Joulani, György and Szepesvári, delayed feedback (2013)

[Primary PDF](https://proceedings.mlr.press/v28/joulani13.pdf);
[publication record](https://proceedings.mlr.press/v28/joulani13.html),
PMLR 28(3), 1453–1461.

Figure 1 separates decision time from timestamped feedback at \(t+\tau_t\).
Section 3.1, Algorithm 1, runs a free base-learner instance while other instances
await feedback. Theorem 1 transfers a nondecreasing concave base regret bound
\(f\), with \(f(0)=0\), under its underlying base-algorithm assumptions and
delays independent of the forecaster's prediction. Writing \(G_T^*\) for the
maximum outstanding feedback count, its first bound is

\[
\mathbb E R_T\le
\mathbb E\!\left[(G_T^*+1)f\!\left(\frac{T}{G_T^*+1}\right)\right].
\]

This is a route to an ordinary passive delayed-feedback comparator. A learner
that chooses proof searches changes its own feedback schedule; that new setting
needs a separate contract and analysis.

### A — Fagin and Halpern, awareness (1988)

[Author-hosted primary PDF](https://www.cs.cornell.edu/info/people/halpern/papers/awareness.pdf).
The printed title page identifies *Artificial Intelligence* 34 (1988), 39–76.
The DOI is `10.1016/0004-3702(87)90003-8`; the embedded 87 is not the
publication-year field.

Section 5 (printed pages 52–54) uses classical two-valued truth with a syntactic
awareness set \(\mathcal A_i(s)\), implicit belief \(L_i\), and explicit belief
\(B_i\):

\[
B_i\phi\quad\Longleftrightarrow\quad L_i\phi\land A_i\phi,
\qquad A_i\phi\quad\Longleftrightarrow\quad\phi\in\mathcal A_i(s).
\]

Explicit beliefs need not include all valid formulas or be deductively closed.
Section 6 separates local belief clusters; Section 7 (pages 61–63) adds temporal
structure. These are precise representational alternatives, not automatically
efficient predictors or decision algorithms.

### AK — Halpern and Pucella, probabilistic algorithmic knowledge (2005)

[Author-hosted primary PDF](https://www.cs.cornell.edu/home/halpern/papers/probalgk.pdf).
The [publisher record](https://lmcs.episciences.org/2261) verifies LMCS 1(3:1),
20 December 2005, DOI `10.2168/LMCS-1(3:1)2005`; the fetched manuscript's
placeholder header is not used for the year.

Section 2 (PDF pages 3–4) interprets explicit algorithmic knowledge through a
terminating procedure \(A_i\) returning Yes, No, or unknown:

\[
(M,s)\models X_i\phi
\quad\Longleftrightarrow\quad
A_i(\phi,L_i(s),s)=\text{Yes}.
\]

Section 3 explicitly represents algorithm randomization. Section 4's discussion
of state access (PDF page 10) requires the modeler to avoid giving procedures
unavailable information. Section 5.3 defines reliability using conditional
answer probabilities. Procedure reliability, evidence about a proposition, and
posterior belief are distinct objects.

## 2. Proposed finite comparison contract — our reconstruction

Use fixed encoded sentences or total program-output claims \(\phi_t\), not a
hidden random coin substituted for the computation. Ground truth, eventual
proof/refutation, and what the learner has observed are separate records.
The learner receives the encoded query and timestamped prior feedback; all
feature extraction, inference, checking, prediction and update work consumes the
same declared computation budget as the value-first candidate. Final labels
cannot enter features or weights before their reveal times.

Choose a finite, prespecified family of bounded forecasting procedures
\(q_{i,t}\in[0,1]\). In the immediate-feedback panel, take
\(\ell_{i,t}=(q_{i,t}-y_t)^2\) and
\(q_t=\sum_i\pi_{i,t}q_{i,t}\). Convexity gives

\[
(q_t-y_t)^2\le\sum_i\pi_{i,t}(q_{i,t}-y_t)^2,
\]

so H's bound also bounds the mixture's cumulative squared error. This is our
direct specialization of H. A known task-loss table then converts each forecast
to a decision by ordinary expected-cost minimization. Report prediction loss and
task loss separately; do not transfer the Brier regret statement to arbitrary
downstream action regret without another argument.

For passive delayed feedback, use a declared adaptation such as DF and retain
its delay assumptions. For paid search, the comparable ordinary method can
choose the same searches and abstentions as the value-first method. Its
feedback acquisition policy must be scored as part of the decision system; no
passive-feedback theorem is imported automatically. Count actual algorithm
steps or another specified resource independently from the number of prediction
rounds.

### A bounded Boolean constraint kernel

This is an elementary proposed comparator, not a new theorem claim. Select at
most \(k\) prime sentence-atoms and retain a finite set \(C_t\) of verified
Boolean constraints drawn from available proof records. Parse their Boolean
connectives compositionally. Enumerate

\[
V_t=\{v\in\{0,1\}^k:v\models C_t\}.
\]

For any nonnegative normalized weights \(\mu_t\) on nonempty \(V_t\), define

\[
p_t(\psi)=\sum_{v\in V_t}\mu_t(v)\,1[v\models\psi].
\]

Every returned distribution respects all constraints in \(C_t\), and all their
Boolean consequences within this selected fragment. Proof: each surviving
assignment satisfies them; a convex average preserves probability one. This
does not require deciding which assignments extend to a model of the full
arithmetical theory. Enumeration uses at most \(2^k\) assignments; checking their
clauses, constructing weights, and answering queries are charged operations.
An implementation must cap \(k\), track actual cost, and return a typed
over-budget or inconsistent-context result if it cannot complete or if
\(V_t\) is empty. A cap is not a license to conceal omitted constraints.

The learned weights may combine bounded predictors of assignments, with an
explicit fallback when a predictor gives all surviving assignments zero mass.
This supplies a stronger ordinary comparator than a bare Boolean prover while
remaining less than full theory-wide logical closure.

## 3. Separating examples and duties — our analysis

1. **Finite coherence versus theory-wide closure.** Treat two unexpanded
   arithmetic sentences as atoms \(u,v\). The observed checked constraints are
   \(C=\{u\}\); the full theory proves \(v\), but its proof has not arrived.
   The finite kernel admits \((u,v)=(1,0),(1,1)\), so a uniform mixture gives
   \(p(v)=1/2\). This is Boolean coherence in the observed fragment alongside
   uncertainty about an unprocessed logical consequence. If the verified
   constraint \(u\to v\) arrives, only \((1,1)\) survives. No change from
   two-valued semantic truth was needed to represent this change of knowledge.

2. **Finite expert regret versus calibrated logical belief.** With the sole
   expert \(q_t=1/2\) and a sequence of eventually verified true claims,
   regret relative to that expert is exactly zero, but squared error is
   \(T/4\) and average signed error is \(-1/2\). Thus a practical regret
   result over a restricted pool does not establish LI's broader duties.

3. **Task stakes versus prediction quality.** Let two forecasts for a true
   binary claim be 0.49 and 0.51. Their squared errors differ by only 0.02.
   With symmetric error cost \(K\), ordinary expected-cost decisions cross the
   threshold at 0.5, and their realized decision losses differ by \(K\).
   The comparison should expose decision margins and costs. This example
   illustrates why usefulness is a separate scoring target; it supplies no
   representational advantage for value logic, since ordinary forecasts support
   the same cost-sensitive decisions.

The proposed contract should test at least these distinct duties: forecasting
before proof arrival; respecting discovered relationships; learning across
repeated structured queries; retaining information useful under changed task
costs; and selecting computations whose decision benefit exceeds their cost.
For every duty, specify the query family, available facts, allowed computation,
feedback/revision schedule, objective and ordinary comparator. A finite positive
result supports the tested duty only. A cheap counterexample can refute an
overbroad proposed duty without refuting every possible value-first system.

## 4. Limits of this review

Selected definition/theorem statements and the indicated source sections were
read; full proofs of the LI construction were not independently reconstructed.
No literature-priority claim is made. No source says that choosing a numerical
carrier alone solves bounded reasoning. LI's monotone deductive-process property
assumptions do not directly govern retractable model adequacy claims; those need
an explicitly indexed theory/model layer and revised contract.

Bibliographic retrieval correction: a guessed Schapire `FreundSc97.pdf` URL
opened the authors' *Arcing Classifiers* discussion, rather than the requested
Hedge paper. Its content was not used for the Hedge reconstruction; the correct
PDF was located through Freund's publication index. Several broad searches were
noisy; substantive imports above use the identified primary texts.

Raw start observation: `2026-10-07T00:42:42.336633+00:00`,
`time.monotonic_ns() = 26931643784454`. Resource completion observations are
recorded below. Subagent elapsed time is not added to the principal research
clock; token and billed compute totals are unavailable.

Raw completion observation: `2026-10-07T00:48:35.686799+00:00`,
`time.monotonic_ns() = 27284993941264`. Observed subagent session elapsed:
`353.35015681` seconds. This is elapsed resource information, not a separately
measured engaged-mode total and not additive ledger credit.
