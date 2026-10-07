# P3-01: admissible Logical Induction desiderata imports

Reviewer: **GPT-6 Astra Pro**, `/root/p301_induction_sources`.
Date: **2026-10-07 UTC**. Same-model internal, nonblind review.
Scope: primary definitions, selected theorem statements and proof interfaces;
pinned formalization declarations as correction leads. No canonical edits,
later-task execution, full Lean build, publication or principal time credit.

**Disposition:** the current duty matrix correctly describes prospective
comparisons. None of the inspected LI results automatically supplies its finite
implementation guarantees. The main qualifications concern value admission,
the meaning of expectation, the strength and timing of calibration, and the
representation of self-reference. Known corrections remain attributed to their
prior source.

## 1. Primary source locators

Sources: [author PDF](https://intelligence.org/files/LogicalInduction.pdf),
[arXiv v5 PDF](https://arxiv.org/pdf/1609.03543v5), and
[v5 TeX source](https://arxiv.org/src/1609.03543v5), dated December 7, 2020.
Use PDF numbering: Gamma-complete is Definition 3.2.4; HTML numbering differs.

| Contract | Exact source locator |
|---|---|
| Common domain / efficiency | §§3.1–3.5; §4 standing assumptions; v5 TeX 753–754 |
| Unique existing value / range | Definition 4.8.1, p. 39; v5 TeX 1638 |
| Threshold average / asymptotic properties | Definition 4.8.2, p. 40; Theorems 4.8.3–4.8.6 |
| Calibration / feedback | Theorems 4.3.3, 4.3.6, 4.3.8; Definition 4.3.7; Appendices D.2–D.5 |
| Introspection / diagonal family | Theorems 4.11.1–4.11.2; Appendices F.1–F.2; v5 TeX 1969–1981 |

Common assumption tuple:
`Gamma consistent c.e.; D computable, nested, finite, Gamma-complete;
assessment worlds PC(D_n); P satisfies LI(D)`.
`EC` below means polynomial-time emission of the object on unary input `n`.
The following mathematical reconstructions and operational deductions are
import restrictions, not new results asserted on the paper's authority.

## 2. LUVs require an existing value, and a declared encoding

The weaker convention in §2 is

$$
\Gamma\vdash\exists x\,\forall y\,(X(y)\Rightarrow y=x).
$$

The actual admission formula is stronger:

$$
\Gamma\vdash\exists x\,[X(x)\land\forall y\,(X(y)\Rightarrow y=x)],
\qquad\Gamma\vdash\forall x\,(X(x)\Rightarrow 0\le x\le1).
$$

For the
empty predicate `X(y) := (y != y)` in ordinary nonempty equality semantics,
the weaker §2 condition holds vacuously, while an existing satisfying value
does not. A statement that every satisfying value lies in `[0,1]` is equally
vacuous for this predicate. Therefore any project object called a LUV must
carry the actual existence, uniqueness and range obligations, not merely the
§2 shorthand. This is a distinction between two source formulas, not a claim
that Definition 4.8.1 lacks existence.

The input and output code must also be declared. A representation convention
for a total natural-number-valued program cannot be applied literally to a
real-valued program without an encoding or approximation interface. For
rationals, exact pair codes and quotient equivalence are distinct choices.
For more general reals, a cut or approximation program is a different object
from one finite numeral. These choices affect equality, threshold queries,
serialization cost and the scope of a theorem. The pinned PE9 correction
addresses this issue; it is not a project novelty claim.

## 3. The expectation notation does not supply a finite coherent law

Definition 4.8.2:

$$
E_k^V(X)=\frac1k\sum_{i=0}^{k-1}
V(\text{“}X>i/k\text{”}),\qquad E_n=E_n^{P_n}.
$$

This average is bounded in `[0,1]`. That fact alone supplies neither exact
normalization nor linearity under the actual finite quotes. Consider a
provably constant-one LUV at day one. Its displayed expectation is the price
of the single threshold sentence `X > 0`. Giving that sentence price zero
makes `E_1(X)=0`, whereas a normalized finite probability law gives the
constant-one payoff expectation one. Even LI does not prohibit that single
exceptional dated quote: the direct finite-coordinate preservation proof in
[finite_perturbation_scope.md](finite_perturbation_scope.md) suffices. The
corrected restricted proof is all this witness needs.

Consequently, the exact sum in the main contract §6.1 is appropriately an
**ordinary-model bridge with a supplied coherent law**. Its finite identities
must not be attributed to the notation `E_n`. In particular, defining a
failure-cost quote `v = 1-p` constructs a complementary numerical quote; it
does not prove `v = p(not phi)` at that date. An exact payoff recoding and an
asymptotic coherence result have different premises and conclusions.

For a later expectation import, record the LUV admission certificates, the
efficiently emitted family, allowed coefficient generation, uniform bounds,
and the precise Gamma-provable payoff relation. An identity available only in
the intended interpretation need not satisfy its provability premise. No
finite rate or exact finite identity follows from a limit assertion alone.

## 4. Calibration imports must preserve the selection and feedback contract

Use `r_n = 1{Gamma proves phi_n}` with
`(phi_n) in EC` and `forall n: Gamma proves phi_n or Gamma proves not phi_n`.
The latter quantified disjunction supplies no polynomial-time deciding
program. Consistency makes the alternatives exclusive. Identification with an
externally executed label or intended arithmetic truth requires the separate
soundness/execution bridge. Pending proof search is not the label zero.

The import distinctions are:

| Result | Assumption schema | Conclusion schema |
|---|---|---|
| 4.3.3 | `a,b in Q; delta in EC(Q>0); w_n=I_delta_n(a<P_n(phi_n)<b); sum w_n=infinity` | `LimPts(sum_(n<=N) w_n r_n / sum_(n<=N) w_n) intersects [a,b]` |
| 4.3.6 | `w in P-generable([0,1]); sum w_n=infinity` | `0 in LimPts(B_N)` |
| 4.3.8 | `w` as above; `f` a strictly increasing deferral; `supp(w) subset image(f)`; `r_(f(n))` computable in `O(f(n+1))` | `B_N -> 0` |

$$
B_N=\frac{\sum_{n\le N}w_n\bigl(P_n(\phi_n)-r_n\bigr)}
{\sum_{n\le N}w_n}.
$$

Definition 4.3.7: `f(n)>n; runtime(f(n)) <= poly(f(n))`.
Notice the different quantifiers: a limit point does not force convergence;
and convergence alone provides no finite rate. If either recurring statistic
converges, its limit must satisfy the displayed constraint. Nothing in the
4.3.3 schema requires `delta_n -> 0`. Strict increase is present in 4.3.8 but
absent from the bare deferral definition. Mere eventual disclosure supplies
no bound of the displayed timely-feedback form. A round count is not a
runtime certificate. Generating a price-dependent rational feature expression
is not necessarily efficient evaluation or emission of its value as a numeral.

For P3-01, a finite resolved-cohort statistic may be reported under its own
sampling contract, but it does not establish these asymptotic duties. A
passive delayed-feedback wrapper, an actively chosen paid proof schedule,
and LI's selected deferral theorem likewise need distinct hypotheses. No
replacement of one by another is licensed merely by the word “feedback.”

## 5. Pinned correction/code scope

Primary correction source: A. M. Berns, **Formalized Agent Foundations**,
commit `367d1e42bf104706ff28d8a40492b9ce95c98da0`, tree
`397e61e644547031ee90b58a20849358ed4b48df`, pinned by the principal reviewer.
[Pinned errata](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/notes/paper-errata.md).
The following declarations were inspected, **not independently built**.

| Pinned file and exact declaration | Scope that can safely be recorded |
|---|---|
| [LUV/PaperLUV.lean](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/Construction/LUV/PaperLUV.lean), `PaperLUV`, lines 87–90; threshold/world interface, lines 251–290 | Admission contains theory proofs of unique existence and a rational unit-code bound. The code uses a selected numerator/positive-denominator pair; equivalent rational pairs are not identical codes. The world-value bridge introduces arithmetic-strength assumptions beyond the admission structure. |
| [Statistics/HistoricalMaturity.lean](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/Construction/Statistics/HistoricalMaturity.lean), `BoundedSequence.recurringunbiasednessexp`, lines 1556–1567 | Bounded, world-valued combinations determined via the theory; generable divergent weights; nonempty finite-stage worlds. The conclusion is a limit point, with no deferral hypothesis. |
| [Statistics/FeedbackTruth.lean](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/Construction/Statistics/FeedbackTruth.lean), `FeedbackTruthComputation`, lines 108–120, and `luv_wubexp_ofComputation`, lines 916–931 | The feedback route retains strict deferral and support conditions, a rational share-norm bound, and certified computation of a specified normalized mesh truth. It is not a certificate for arbitrary exact-real feedback. |
| [Statistics/Endpoints.lean](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/Construction/Statistics/Endpoints.lean), `luv_wubexp_ofComputation_unconditional`, lines 128–147 | The closed route uses the constructed market and explicit theory/code/feedback assumptions. “Unconditional” in a declaration name does not remove those hypotheses. |
| [Paper/Market.lean](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/Construction/Paper/Market.lean), `paperIntervalQuoteCode`, lines 394–443, and `lic_introspection_closed`, lines 452–477; [Quotation/Packages.lean](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/Construction/Quotation/Packages.lean), lines 269–314 | The endpoint concerns the constructed market, a machine-coded sentence sequence, generated rational bounds and machine-coded shrinking margins. The quote emitter names a fixed program and index. It does not emit the current bound values as literal numerals. No same-day price identity between those encodings was established in this review. |

PE2 identifies misplaced/omitted feedback hypotheses and a variable error in
the printed expectation unbiasedness pair, Theorems 4.8.15–4.8.16. Therefore
do not import those statements verbatim. Choose a corrected route and check
its exact indices, combination-level determined value and precision contract.
The inspected declarations are useful evidence about that route's stated
scope, not a substitute for auditing its proof dependencies.

PE6 distinguishes the introspection proof-interface problem from a false
theorem. Independently inspected v5 TeX lines 1969–1981 explicitly place
encoded **values** `a_n,b_n` inside the interval sentence, while the hypothesis
only makes their feature sequences P-generable. Appendix F.1 needs an
efficiently emitted sentence family. This leaves a serialization gap unless
efficient literal numerals or a suitable code-indexed alternative and its
bridge are supplied. The current pinned endpoint uses the latter style. Its
location is `Paper/Market.lean`; the erratum's older endpoint locator is stale.

Neither route yields exact finite introspective correctness. The comparison
has shrinking margins and an existential error sequence tending to zero,
without an efficient error certificate or rate in the inspected statement.
Paradox resistance likewise requires the particular efficient diagonal
family and its Gamma-proved fixed-point relation; it is not blanket semantic
resolution of every self-referential sentence. F01 appropriately remains a
later comparison, not an inherited guarantee of neural transparency or
self-certification.

Finally, author-PDF Appendix G.8, pp. 127–128, invokes G.7's early-price
correction before conditional-market replay. The unrestricted correction is
the known PE1 issue. This review does not establish whether every downstream
conditioning argument survives its repair. The project needs no closure
theorem to distinguish consistent conditioning from evidence withdrawal or
counterpossible evaluation, so no such theorem is imported here and no FAF
conditioning endpoint was audited.

## 6. Recommended P3-01 dispositions

| Current duty | Admissible status after this audit |
|---|---|
| U03 / V01 and main contract §6.1 | Exact finite expectation algebra belongs to the declared ordinary coherent model. LI bounded-expectation properties remain asymptotic theoretical comparisons with admission/provability/efficiency assumptions. |
| U05 / U06 | Retain prospective status. Separate pointwise convergence, Gamma-relative correctness and anticipation along an efficient family; none means correctness for all intended arithmetic truths. |
| U07 / U09 | Preserve the exact selected sequence, weighting, divergence, limit-point/convergence and feedback-time obligations. Finite calibration summaries and ordinary delayed regret receive their own labels. |
| F01 | Retain the bounded inherited case and open broader duty. Any later import must name the self-code, quotation convention, precision, arithmetic assumptions and exact scope of the statement. |
| Source record | Record PE1/PE2/PE6/PE9 where relevant, the immutable pin, stale prose/locator distinctions and source-inspection-only scope. No full formalization verification or new LI theorem is claimed. |

## 7. Verification and resource observation

The current canonical problem contract §6.1 and duty matrix were read without
editing them. This reviewer inspected the original/v5 PDF text, retrieved the
v5 TeX source for the actual quantifiers and numeral encodings, and inspected
selected pinned errata/statistics declarations. The same-model helper
`/root/p301_induction_sources/luv_code_scope` independently inspected the
PaperLUV and quotation/introspection declarations at the pin. This was an
internal nonblind check, not external peer review; no Lean build was run.

Raw start: `2026-10-07T01:32:16.698670+00:00`,
`time.monotonic_ns() = 29906005882551`.
The completion observation records elapsed span only, including tool waits,
orchestration and context-recovery gaps. It is not an audited engaged-work
measurement and adds **no principal ledger credit**.

Raw completion: `2026-10-07T01:42:44.954906+00:00`,
`time.monotonic_ns() = 30534262047683`.
Observed elapsed span: `628.256165132` seconds; no principal credit.
