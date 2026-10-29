# Useful Decisions under Unresolved Mathematics

## A phase-three synthesis of Value Logic

Tristan Miano, project author. Research contributions: ChatGPT (GPT-6 Astra Pro) and Codex (GPT-6); synthesis: Codex (GPT-6). October 2026.

<a id="abstract"></a>

## Abstract

A bounded reasoner often needs an action before it has a complete mathematical answer, a fully adequate model, or a reliable estimate of the benefit of further computation. This report synthesizes the third phase of Value Logic around five questions about logical uncertainty, counterfactuals, fallible models, learning usefulness, and probability information in values. The principal assessed contribution is an exact whole-range algorithm for a future minimum of affine responses, conditioned on retained interval-valued optimum receipts over independent rational source polytopes. With $`n`$ source blocks and $`k`$ receipts, it uses at most $`2n2^k`$ local linear programs and $`O(n3^k+n2^k\log(n2^k))`$ further comparisons, returns at most $`n2^k`$ intervals, and supports rational certificates and source witnesses. Preserving gaps enables decisions that an interval hull cannot justify. Selected secondary results provide sharp counterfactual bounds from compressed ridge information, task-relative correction of fallible polynomial models, and exact bounds on the benefit of further computation or observation from partial decision information. Finite forecasting and probability-identification results connect these services to established learning and decision theory. The outcome is a useful mathematical and executable synthesis with a bounded contribution claim, rather than a general learner of mathematical truth. Complete-cost superiority over the strongest conventional alternatives remains unestablished.

<a id="sec-introduction"></a>

## 1. The problem and the contribution

The organizing question is practical: **what can a reasoner safely do with the information it has, and what additional information would be worth acquiring?** An unresolved theorem, a partially executed optimizer, and a fallible predictive model create different kinds of uncertainty. Treating them as interchangeable obscures both useful decisions and failure modes. Phase three instead develops explicit contracts between evidence, retained information, computation, and action.

The original questions are addressed in order: (Q1) how to use unresolved mathematics; (Q2) how to evaluate logical and model counterfactuals; (Q3) whether several useful but fallible models help; (Q4) how to refine usefulness estimates and price reasoning, including the comparison with Logical Induction; and (Q5) which probability information values contain. A restricted answer counts as progress when it supplies a concrete guarantee or capability and makes its remaining obligations visible. It need not solve the broadest interpretation of the question.


<a id="def-contract"></a>

**Definition 1 (Evidence and decision contract).**
A contract specifies a source family $`\mathcal X`$, an observation map and the evidence actually received, a target quantity, a finite action family, losses in declared units, and admissible paid operations. Its compatible source set $`\mathcal X_H`$ contains the sources satisfying the received evidence. A certificate is conditional on this contract. A source witness proves compatibility; it does not prove that the witness is the actual source. An empty compatible set is a conflict to investigate, not permission to infer arbitrary useful conclusions.


Three distinctions recur. A mathematical certificate is different from a forecast; knowing an action is optimal is different from knowing its loss is small; and refining a calculation about a fixed source is different from observing the actual source. The results below make those distinctions operational. They also explain the relation to the phrase *value logic*: losses, computational costs, dependence, and revision determine which information matters. Conventional robust optimization, abstract interpretation, numerical analysis, and decision theory already embody many of these concerns. The scientific question is the explicit additional result, not whether an algorithm has been given an unconventional label.

The principal assessed contribution, called **V19-R/v1**, is a specialized whole-range synthesis. It combines familiar local linear programming and subset dynamic programming into an exact answer to a particular retained-information problem. Its mathematical confirmation and contribution assessment were accepted at that bounded scope. Secondary results were selected here for their relevance to the five questions, not because they passed that same review. In the compact map below, **A** denotes the assessed V19 claim; **D** denotes a development derivation with scoped executable evidence; **S** denotes an established result reconstructed or adapted in the project. These are different evidence categories, not a numerical ranking of scientific importance.

| Result | Questions and useful output | Evidence / contribution level | Remaining obligation |
| --- | --- | --- | --- |
| Sound incomplete-evidence covers | Q1: act without enumerating every answer | S/D; finite abstraction and implementation | Truthful evidence and semantic bridge |
| V19 whole scalar range | Q1, Q3, Q5: retain gaps and recover sources | A; specialized algorithm and useful synthesis | External premises, implementation bridge, specialist novelty judgment |
| Typed counterfactuals and proof transport | Q2: identify what changes and what survives | S/D; semantics and interface | Warrant relevance, routing, and coverage |
| N16 compressed ridge bounds | Q2, Q5: sharp edited-value thresholds | D; analytic information theorem | Remaining novelty comparison; no V19 confirmation transfer |
| Structured model correction | Q1, Q3: exact task outputs from fallible models | S/D; acquired-scope synthesis | Real access costs and structural warrants |
| Finite forecasting and paid feedback | Q1, Q4: checked losses and performance bounds | S/D; established algorithms adapted | Generalization, delayed labels, full costs |
| Sharp stopping and observation bounds | Q1, Q4: distinguish useless refinement from useful evidence | D; finite decision interface | Source compatibility and policy restrictions |
| Probability-information fibers | Q5: recover only what a decision needs | S/D; identification analysis | Known payoff semantics and source family |

Detailed source mappings, implementation boundaries, and the remaining portfolio are in [Appendix A](v3/report/claims.md) and [Appendix B](v3/report/portfolio.md). Those records supplement the arguments below; chronological logs are not prerequisites for reading the paper.

<a id="sec-q1"></a>

## 2. Q1: useful decisions before mathematics is resolved

**Strongest supported answer.** A bounded reasoner can maintain sound outer information about unresolved answers, sometimes certify an action before resolving them, and distinguish uncertainty from inconsistency. It can also recover exact nonconvex numerical ranges from retained computations in the V19 class. These are finite conditional services. They do not provide probabilities for arbitrary unresolved mathematical sentences or the broad learning properties of Logical Induction [1](#ref-li).

<a id="sec-covers"></a>

### 2.1. Interrupted reasoning must preserve unvisited possibilities

For a finite list of versioned Boolean questions, let $`y\in\{0,1\}^m`$ denote their intended answers. Received hard constraints define a finite feasible set $`F(H)`$. An implementation maintains a cover $`A(H)\supseteq F(H)`$, for example a union of cubes whose coordinates are $`0`$, $`1`$, or unresolved. If every hard receipt is true of $`y`$, then $`y\in A(H)`$. Evaluating a loss by sound interval operations on this cover yields a conditional bound on its actual value.

The invariant survives a split that replaces one cube by both children and a pruning step justified by a checked contradiction. It does not survive silently discarding an unfinished branch. For example, visiting only $`x=0`$ for loss $`100x`$ does not establish the range $`[0,0]`$ while $`x=1`$ remains possible. Likewise, withdrawing a premise requires restoring an appropriate cover or marking the dependent result stale. These are applications of the established abstraction principle [2](#ref-abstract); the project supplies typed evidence, finite operations, and versioned decision use.

Finite shrinking feasible sets eventually stabilize, but stabilization time is not generally observable. A computable rule that always recognized completion of arbitrary computable future receipt streams would decide whether a further constraint encoding a halting event will ever arrive. This obstruction does not prevent a decision certificate from becoming stable earlier: if every remaining answer supports the same action, later truthful narrowing preserves that action's warrant. [The finite construction](v3/derivations/03_logical_uncertainty.md) and its [refinement extension](v3/derivations/03_refinement_extensions.md) keep these claims separate from a general theory of arithmetic belief.

<a id="sec-range"></a>

### 2.2. Retained optimum values can constrain a new computation

Suppose earlier computations returned intervals for optimum values, while the underlying numerical parameters were not retained exactly. Reusing each interval independently discards the fact that the same hidden parameters generated all the receipts. V19 asks for the complete future scalar range under that shared-source condition.

Let $`n\geq1`$. Independently uncertain vectors $`x_i`$ lie in supplied nonempty compact rational polytopes $`B_i`$, with possibly different positive dimensions. Independence here means a product uncertainty set, not probabilistic independence. Let $`g_{ji}`$ and $`f_i`$ be rational affine forms. The $`k`$ retained receipts and future readout are


<a id="eq-source"></a>

```math
a_j\leq\min_{1\leq i\leq n}g_{ji}(x_i)\leq b_j
 \quad(j\in K=\{1,\ldots,k\}),\qquad
 V(x)=\min_i f_i(x_i).
 \tag{1}
```

Every old lower bound applies to every block; each old upper bound needs at least one witnessing block. For a receipt subset $`T\subseteq K`$, form


<a id="eq-slice"></a>

```math
Q_i(T)=B_i\cap\bigcap_{j\in K}\{g_{ji}\geq a_j\}
              \cap\bigcap_{j\in T}\{g_{ji}\leq b_j\}.
 \tag{2}
```

If this slice is nonempty, let $`\ell_i(T)`$ and $`u_i(T)`$ be the minimum and maximum of $`f_i`$ on it, with attaining points. Its affine image is the entire interval between them. Empty slices are unavailable, rather than assigned invented endpoints.

For a block index set $`I`$ and receipt subset $`S`$, define the bottleneck


<a id="eq-bottleneck"></a>

```math
U_I(S)=\max_{\bigsqcup_{i\in I}T_i=S}\ \min_{i\in I}u_i(T_i),
 \tag{3}
```

where partitions with an empty slice are omitted. Set $`U_I(S)=-\infty`$ when no feasible partition exists; $`U_\varnothing(\varnothing)=+\infty`$ and $`U_\varnothing(S)=-\infty`$ for nonempty $`S`$.


<a id="thm-range"></a>

**Theorem 2 (Exact anchored range, V19-R/v1).**
Under [Equation 1](#eq-source), the entire attainable set is


<a id="eq-range"></a>

```math
V(\mathcal X_H)=
 \bigcup_{i,T}
 \left[\ell_i(T),\ \min\{u_i(T),U_{[n]\setminus\{i\}}(K\setminus T)\}\right],
 \tag{4}
```

omitting unavailable slices and intervals with upper endpoint below lower endpoint. The set has at most $`n2^k`$ closed intervals before merging. It can be computed using at most $`2n2^k`$ local rational LP solves and $`O(n3^k+n2^k\log(n2^k))`$ additional comparisons, with $`O(n2^k)`$ scalar table entries plus input, backpointers, and local certificates. Every requested attainable rational value has a reconstructable rational source. An empty union certifies inconsistency of the supplied premises.



**Proof.** Take a compatible source. Assign each receipt to one block witnessing its upper bound, obtaining a partition $`(T_i)`$. Choose an anchor $`i`$ attaining the future minimum $`q`$. Then $`\ell_i(T_i)\leq q\leq u_i(T_i)`$. Every other block has future value at least $`q`$, so the bottleneck of this outside partition is at least $`q`$. Thus $`q`$ belongs to the displayed interval.

Conversely, take $`q`$ in a displayed interval. Recover an outside partition attaining its bottleneck and put every outside block at a local maximum. Their future values are at least $`q`$. In the anchor slice, interpolate its minimum and maximum points to attain exactly $`q`$. Convexity preserves the slice constraints. Every old lower bound holds, every upper bound has its assigned witness, and the new minimum is $`q`$. Rational interpolation preserves rationality. Compactness supplies attainment, including singleton images. The empty-set conventions handle $`n=1`$ and $`k=0`$.

Prefix and suffix tables compute [Equation 3](#eq-bottleneck) by splitting each subset: $`P_i(S)=\max_{T\subseteq S}\min\{P_{i-1}(S\setminus T),u_i(T)\}`$. The sum of the numbers of splits is $`\sum_{S\subseteq K}2^{|S|}=3^k`$ per layer. Combining a prefix and suffix gives each outside table in another $`3^k`$ scan. Sorting and merging the at most $`n2^k`$ intervals gives the remaining term. LP bit complexity, rational number lengths, certificate bytes, and source reconstruction arithmetic are additional costs, not unit-cost consequences of this comparison count. $\square$

The certificate covers **every indexed local slice**. For a bounded slice it supplies feasible extremizers and matching nonnegative dual multipliers; for an empty slice it supplies a Farkas witness. The verifier reconstructs constraints from the original input, checks the rational identities, and recomputes the union. Omission of a slice is not evidence of emptiness. This division makes the optimizer an untrusted producer while retaining explicit trust in input interpretation and checker implementation.

The principal proof and certificate contract were reconstructed in the bounded confirmation. Twelve Lean units checked selected finite-set, order, recurrence, and witness-combination lemmas. They do not formalize all rational LP existence, bit complexity, parsing, Python execution, or semantic premises. The development audit in Section 8 supplies additional finite implementation evidence; it is not an exhaustive program-correctness proof.

<a id="sec-gap"></a>

### 2.3. Why the whole range can matter

A positive-cost example uses independent local variables and two response vectors


<a id="eq-positive-example"></a>

```math
x_1=(10+2t+u,\ 11-t+v),\qquad
 x_2=(10+s+u',\ 12-2s+v'),
 \tag{5}
```

with $`0\leq t,s\leq1`$ and $`0\leq u,v,u',v'\leq1/10`$. Each coordinate-minimum receipt lies in $`[10,10.1]`$. Neither block can witness both upper bounds: before thickening, the least possible maximum of its two excess coordinates is $`2/3>1/10`$. The two split assignments give, for the future minimum total response,


<a id="eq-positive-range"></a>

```math
R=[21,21.2]\ \cup\ [21.9,22.2].
 \tag{6}
```

For the first assignment the excess total ranges from $`1`$ to $`1.2`$; for the reverse it ranges from $`1.9`$ to $`2.2`$. Independence permits both local extrema and interpolation. Hence a later band $`[21.4,21.6]`$ contradicts the retained model, while its interval hull admits that band. The same gap certifies $`|1/(V-21.5)|\leq10/3`$. This is a model-criticism and numerical-stability consequence, not a probability claim.

Whole-range computation is most relevant to repeated or nonmonotone queries. For a single forbidden band, direct feasibility can be cheaper. For a convex scalar loss, the worst loss on a compact scalar set occurs at an extreme endpoint; internal holes add nothing to that particular minimax duty. Further, an explicit range may itself be exponentially large: the preserved hypersimplex construction produces $`\binom{k}{\lfloor k/2\rfloor}`$ isolated values with two blocks and growing local dimension. This limits explicit output, not all succinct representations or single-value queries.

<a id="sec-range-prior"></a>

### 2.4. Relationship to the strongest alternatives

Inverse optimal-value inference is established [3](#ref-inverse). Mixed-integer formulations already encode active pieces of piecewise-affine models [4](#ref-mip). Berger and Sankaranarayanan combine compatible-subset search, covering, and LP infeasibility certificates to fit piecewise-affine models [5](#ref-berger). Goodman supplies general semiring outside recurrences [6](#ref-goodman). V19's outside bottlenecks are a specialization of that machinery. The proposed contribution is the **anchored continuous scalar image with its receipt-parameter bound, complete certificate, and source recovery**, not a new LP theorem, convolution primitive, or generic inference principle.

A substantive distinction from fitting one model is preserving all value-bearing slices. With $`x_1,x_2\in[0,1]`$, receipt $`\min(x_1,x_2)=0`$, and future $`\min(-x_1,-x_2)`$, the correct image is $`[-1,0]`$. Keeping only each block's maximally constrained receipt slice retains $`\{0\}`$ and loses valid values. The empty-subset slice matters. A conventional solver can retain it and perform the same synthesis; an identical implementation necessarily ties. A distinct MIP solver, direct band-feasibility algorithm, or structural shortcut is instead a genuine competitor whose resources can differ.

The [close-comparison map](v3/report/claims.md) includes inverse interval LP, bounded-error identification, max-plus set estimation, and exact set propagation. Some potentially close full texts remained inaccessible in the assessed review; their abstract-level scope is recorded rather than treated as a novelty clearance. The accepted claim is a useful moderately novel synthesis under that explicit uncertainty. It supplies neither universal superiority nor a new physical model-identification method.

<a id="sec-q2"></a>

## 3. Q2: counterfactual meaning and retained information

**Strongest supported answer.** Counterfactual questions become tractable when the changed object, unchanged commitments, dependency routing, and selection rule are explicit. Old evidence can then be transported under a numerical and domain-coverage bridge. N16 gives a stronger analytic answer for one numerical edit problem: the sharp edited ridge value compatible with a retained response block. None of these results determines a uniquely correct semantics for every false mathematical antecedent.

<a id="sec-semantics"></a>

### 3.1. A numerical value does not define an intervention

Consider a fixed function with $`f_0(h_0)=0`$, calls $`A=f_0(h_0)`$ and $`B=f_0(h_0)`$, and loss $`2+A-2B`$. Conditioning on $`A=1`$ has an empty ordinary target. Intervening only on the occurrence $`A`$ gives loss $`3`$. Replacing the function by an explicitly chosen $`f_1`$ with $`f_1(h_0)=1`$, and redirecting both calls, gives loss $`1`$. Redirecting only the actor's call again gives $`3`$. A predictor of the old function does not automatically become a predictor of its replacement.

The finite request interface therefore records an operation tag, original antecedent, candidate grammar, hard commitments, permitted exceptions, ranking, tie policy, interpretation map, and consumer loss. Structural interventions follow familiar modified-equation semantics [7](#ref-halpern). Ranked repairs select all minimum-ranked alternatives unless an explicit policy breaks ties. The finite counterpossible adapter instead uses paired positive/negative support in a Belnap--Dunn propositional fragment, allowing named atomic normality exceptions while preserving connective rules. Its states are not ordinary arithmetic worlds. Nonvacuous counterpossible semantics has substantial prior literature [8](#ref-counterpossible); this adapter is an explicit limited choice, not a philosophical settlement.


<a id="prop-transport"></a>

**Proposition 3 (Domain coverage plus a numerical bridge).**
Let $`S_1`$ be the nonempty family of currently selected alternatives. For every $`y\in S_1`$, suppose some valid old proof gives $`d_{0,i}(x)\leq B_i(x)`$ and a warranted interpretation gives $`d_1(y)\leq\alpha_i d_{0,i}(x)+\delta_i(x,y)`$, with $`\alpha_i>0`$. If $`I(y)`$ lists all applicable pairs, then


<a id="eq-transport"></a>

```math
\max_{y\in S_1}d_1(y)
 \leq\max_{y\in S_1}\min_{(i,x)\in I(y)}
       \{\alpha_iB_i(x)+\delta_i(x,y)\}.
 \tag{7}
```




**Proof.** Apply the bridge to each valid old inequality at its actual domain point, take the best valid upper bound for that point, and then maximize over the currently selected family. Positivity preserves the inequality. Coverage of every current alternative is indispensable; preserving the old proof file alone does not provide it. $\square$

The minimum selects a proof, not an action allowed to observe hidden $`y`$. For instance, proof allowances $`(0,10)`$ and $`(10,0)`$ on two cases combine to a uniform allowance $`0`$, while choosing a proof after first taking its worst case yields $`10`$. This is an established dependency-aware operation with a useful retention consequence. Ordinary proof systems can preserve the same support information.

<a id="sec-n16"></a>

### 3.2. N16: what a compressed solve tells us about an edited solve

Let $`M`$ be an unretained finite real matrix, $`W`$ an isometry with $`k`$ columns, and $`c`$ a unit vector. Retain the strict response block $`C=W^T(I+MM^T)^{-1}W`$, where $`0\prec C\prec I`$. An edit $`N`$ has the same shape as its source $`M`$ and satisfies $`\|N-M\|_{\mathrm{op}}\leq e`$, with $`e>0`$. The target is the reoptimized ridge value


<a id="eq-ridge"></a>

```math
F(N;Wc)=\min_z\{\|Wc-Nz\|^2+\|z\|^2\}
        =c^TW^T(I+NN^T)^{-1}Wc.
 \tag{8}
```

The information class ranges over **all finite compatible sources and edits**, with unrestricted finite source dimensions. This differs from choosing one robust solution before an edit of a completely known matrix. Acquisition of $`C`$, the isometry interface, and the edit warrant are substantive inputs.

Put $`E=e^2`$, $`h=(E+\sqrt{E^2+4E})/2`$, $`a=1+t`$, and $`d=t-E-E/t`$. Define $`L_t(C)=C(aI-dC)^{-1}`$ and $`U_t(C)=aC(I+dC)^{-1}`$.


<a id="thm-n16"></a>

**Theorem 4 (Sharp retained-block endpoints, developmental N16-C/v1).**
The infimum and supremum of [Equation 8](#eq-ridge) over the stated information class are


<a id="eq-n16"></a>

```math
\underline F=\max_{t\geq h}c^TL_t(C)c,
 \qquad
 \overline F=\inf_{t\geq h}c^TU_t(C)c,
 \tag{9}
```

where the upper family includes its limit $`1`$ at infinity. Each endpoint is attained by a finite compatible source and edit; the sources may differ. A construction uses at most $`2k`$ input and output coordinates. Sharpness is for the specified scalar direction $`c`$, not a simultaneous least or greatest matrix envelope.



<a id="lem-compression"></a>

**Lemma 5 (Inverse compression).**
For every positive definite real matrix $`A`$ and isometry $`W`$, $`W^TA^{-1}W\succeq(W^TAW)^{-1}`$.



**Proof.** For any vector $`c`$, maximize $`2(Wc)^Tz-z^TAz`$ over all $`z`$ to obtain $`c^TW^TA^{-1}Wc`$. Restricting $`z`$ to $`Wu`$ gives the maximum $`c^T(W^TAW)^{-1}c`$. Restriction cannot increase the maximum; validity in every direction gives the matrix order. $\square$

**Proof explanation for [Theorem 4](#thm-n16).** The ridge normal equations give [Equation 8](#eq-ridge) and the quadratic dual $`F(N;v)=\max_w(2v^Tw-w^T(I+NN^T)w)`$. [Lemma 5](#lem-compression) supplies the required compression inequality. Young's inequality applied in both directions to $`N=M+(N-M)`$ gives


<a id="eq-young"></a>

```math
NN^T\preceq aMM^T+(1+1/t)EI,
 \qquad MM^T\preceq aNN^T+(1+1/t)EI.
 \tag{10}
```

Invert the positive expressions and compress them using the dual inequality. Because $`d\geq0`$ and $`a-d>0`$, the resulting bounds are precisely $`L_t(C)`$ and $`U_t(C)`$. This proves validity for every compatible source, rather than only for a tested matrix.

Sharpness needs more. At an interior optimum, choose the canonical source $`M=(C^{-1}-I)^{1/2}`$ and a rank-one edit in the old residual/solution directions. Differentiating the scalar endpoint makes Young's equality condition agree with the new normal equations. At the cap $`t=h`$, a hidden second moment may be required. With $`H=I-C`$, $`s=c^TCc`$, and $`m_0=c^TC^2c`$, a block contraction


<a id="eq-dilation"></a>

```math
S_\tau=\begin{pmatrix}C&\sqrt{\tau CH}\\\sqrt{\tau CH}&H\end{pmatrix},
 \quad 0\leq\tau<1,
 \quad c^TW^TS_\tau^2Wc=m_0+\tau(s-m_0)
 \tag{11}
```

realizes the needed moment while preserving $`C`$. Each eigenvalue block has positive determinant $`(1-\tau)\lambda(1-\lambda)`$ and trace $`1`$, so $`0\prec S_\tau\prec I`$ and it corresponds to a finite source. The endpoint derivative conditions select moments $`s(1+h)/(2+h)`$ for the lower cap and $`s/(2+h)`$ for the upper cap, each in $`[m_0,s)`$ when that branch applies. The corresponding rank-one edits satisfy the new normal equations. The remaining upper branch is cancellation, giving value $`1`$. [Appendix A's N16 entry](v3/report/claims.md#n16) links the complete branch calculations, including boundary equality and the later smaller-witness construction. This is a reconstructed developmental theorem, not a consequence of V19's review.

The pointwise bounds are already useful without optimizing $`t`$ or proving sharpness. Their operator monotonicity permits truthful rational brackets $`C_-\preceq C\preceq C_+`$: evaluate $`c^TL_t(C_-)c`$ and $`c^TU_t(C_+)c`$ exactly. The rational checker verifies these finite algebraic conditions and a strict threshold. It does not authenticate the source, isometry, bracket truth, or norm warrant. Its finite bit limits also prevent an unconditional completeness promise for arbitrarily tiny strict gaps.

For a concrete decision, take $`C=\mathrm{diag}(1/1601,9/10)`$, $`c=(1,1)/\sqrt2`$, and $`e=3`$. Brackets $`C\pm10^{-4}I`$ with rational parameter $`t=100`$ certify an upper value approximately $`0.58311909<0.6`$. The exact calculation can use the rational matrix $`cc^T`$. A different source preserving the entire compared old optimizer and residual admits an edit with value $`1`$; the extra block information excludes it. This establishes a capability from retained information. Three scalar polarization queries suffice to acquire the displayed block, but one suitably targeted scalar query can settle this particular threshold too. Thus the example supplies no minimal-acquisition or speed claim.

Robust least squares already supplies the worst-residual machinery [9](#ref-robustls), and operator interpolation supplies a strong exact finite SDP comparator [10](#ref-operator). The project's Gram reduction uses two positive semidefinite matrices to express the same unknown-source and edit constraints; it attains the same endpoint values. N16's possible increment is an explicit one-parameter solution and finite equality construction. A subsequent ordinary hidden-moment/minimax derivation made that increment easier to reconstruct and potentially more routine. The last scoped contribution estimate remained 55--80%, central 65%, with novelty as the principal blocker. This historical subjective assessment is not a probability that the displayed inequality is true, nor a calibrated confidence interval. N16 remains a worthwhile extracted result without being promoted to V19's status.

<a id="sec-q3"></a>

## 4. Q3: task-relative use and correction of fallible models

**Strongest supported answer.** A model can fail as a complete account while supplying correct, useful consequences for particular tasks. Multiple models can supply complementary predictions, proof domains, or correction structure. The investigation provides exact restricted mechanisms for doing so. It does not establish a general advantage of a Value Logic ensemble over equally informed model averaging, robust selection, or correction methods. Bayesian model averaging already treats model uncertainty explicitly [11](#ref-bma); task-relative permission and repair are additional contracts, not exclusive ideas.

<a id="sec-correction"></a>

### 4.1. Correct the requested output instead of requiring the whole model to be true

Let $`A(x)`$ be an expensive true vector output and $`B(x)`$ a cheap fallible model, with residual $`F(x)=A(x)-B(x)`$ over a field. Suppose a full-column-rank matrix $`U\in\mathbb K^{n\times d}`$ spans every residual. Choose $`d`$ linearly independent rows $`J`$.


<a id="prop-correction"></a>

**Proposition 6 (Exact correction from a retained error space).**
For every input in the warranted domain,


<a id="eq-correction"></a>

```math
A(x)=B(x)+U(U_J)^{-1}\bigl(A_J(x)-B_J(x)\bigr).
 \tag{12}
```

Thus $`d`$ paid true coordinates, together with model evaluation and matrix arithmetic, suffice for the complete corrected output. A contrast $`w^TB(x)`$ is already exact whenever $`w^TU=0`$.



**Proof.** Write $`F(x)=Uz`$. Restriction to $`J`$ gives $`F_J=U_Jz`$; invert this equation and substitute. The contrast assertion follows by annihilating the residual space. $\square$

The algebra is ordinary skeleton/cross reconstruction, with low-rank approximation as a strong ancestor [12](#ref-cross). The difficult operational premise is acquiring a warranted residual space without making every future true evaluation. For fixed polynomial residuals of known total degree at most $`D`$, sample from a grid of $`q>D`$ field elements per coordinate. At any incomplete observed span $`S`$, a linear functional annihilating $`S`$ but not the full residual range produces a nonzero polynomial. The Schwartz--Zippel bound gives $`\Pr(F(X)\in S)\leq D/q`$. Stopping after $`h`$ consecutive nonexpanding probes at a rank stage gives a false-completion bound at most $`n(D/q)^h`$, by a union bound over at most $`n`$ incomplete stages. On the single success event, **all future inputs and all later chosen annihilating contrasts** are protected. This is structural scope, not a posterior probability that the model is true.

If the residual also has a declared feature representation $`F(x)=E\phi(x)`$, keep feature/error pairs $`\Phi`$ and $`Y`$. A new feature in the old span has error $`Y\alpha`$ when $`\Phi\alpha=\phi(x)`$, so it needs no new truth query. Otherwise acquire the $`d`$ anchors in [Equation 12](#eq-correction) and enlarge the feature span. Starting at rank $`r`$, at most $`M-r`$ such purchases determine an $`M`$-dimensional feature map. Under only these coefficient and output-space constraints, fewer than $`d`$ independent anchor coordinates cannot identify an arbitrary new direction: an unobserved perturbation $`Uz\lambda`$ can preserve the old pairs and queried coordinates while changing the answer.

The constructed $`n=128`$, $`M=35`$, $`d=4`$ example starts from seven full samples of feature rank seven. Its total is $`128\cdot7+4(35-7)=1008`$ true-coordinate outputs, compared with $`128\cdot35=4480`$ for full-output interpolation, a **77.5% reduction in that oracle component**. The model, feature evaluation, factorization, storage, numerical conditioning, and shared batch operations still need pricing. A conventional two-sided interpolation implementation matches the count. Exact finite-field tests support the algebra; they do not validate a real application's access tariff or turn a probabilistic polynomial-scope event into zero-error certainty.

<a id="sec-model-revision"></a>

### 4.2. Revision preserves only warranted scope

A useful repair rule is explicit: if a new residual satisfies $`F'(x)=LF(x)+G(x)`$ and a separately warranted subspace $`T`$ contains every $`G(x)`$, then $`\mathrm{image}(LU)+T`$ contains every new residual. The correction construction can be rebuilt on that space while retaining the original common event. Arbitrarily retraining $`B`$ supplies no such guarantee. Similarly, partial mathematical labels may support a restricted equation or action even while the whole feature model remains inadequate, but the population, selection procedure, and confidence event must remain the ones actually justified.

The wider portfolio includes joint incomplete-evidence certificates, nonlinear approximate summaries, query-guided proof selection, and protected model scopes. Their strongest comparisons sometimes removed an apparent gain: established scenario bounds beat one proposed elementary envelope; per-task selection matched a marginal ensemble guarantee; and interpolation defeated an overly favorable private-validation probe count. These outcomes favor **task-relative adequacy with explicit correction costs** as the useful synthesis. They do not support the claim that maintaining several fallible models is inherently better than all conventional methods. [Appendix B](v3/report/portfolio.md) preserves these directions and their blockers.

<a id="sec-q4"></a>

## 5. Q4: learning usefulness, stopping computation, and buying observations

**Strongest supported answer.** Finite loss forecasts can improve under checked feedback, and partial evidence can bound what more computation or an observation might buy. The project gives executable adaptations and sharp restricted decision bounds. It does not match Logical Induction's general language-wide guarantees or demonstrate a generally efficient metareasoner.

<a id="sec-forecast"></a>

### 5.1. A cost forecast is a forecast, with an explicit error allowance

For a versioned binary answer $`y_t`$, a known affine loss $`b_t(a)+d_t(a)y_t`$ has forecast $`b_t(a)+d_t(a)p_t`$. The scalar $`p_t`$ is learned, not admitted as a hard receipt. The finite implementation adapts Vovk's K29-star defensive forecasting [13](#ref-vovk). With continuous predictable features $`\Phi_t(p)`$, put


<a id="eq-forecast"></a>

```math
\begin{aligned}
 R_{t-1}&=\sum_{s<t}(y_s-p_s)\Phi_s(p_s),\\[0pt]
 S_t(p)&=\langle R_{t-1},\Phi_t(p)\rangle
             +\tfrac{1-2p}{2}\|\Phi_t(p)\|^2,\\[0pt]
 A_t&=2\max\{0,(1-p_t)S_t(p_t),-p_tS_t(p_t)\}.
 \end{aligned}
 \tag{13}
```

Choose a favorable endpoint or search for a root; an interrupted root search retains the actual allowance $`A_t`$. For binary $`y`$, the identity $`(y-p)^2=p(1-p)+(1-2p)(y-p)`$ proves


<a id="eq-potential"></a>

```math
\|R_T\|^2\leq
 B_T:=\sum_{t\leq T}p_t(1-p_t)\|\Phi_t(p_t)\|^2+\sum_{t\leq T}A_t.
 \tag{14}
```

It follows by expanding one potential increment and telescoping. Here $`p_t,q_{t,i}\in[0,1]`$, the finite weights $`w_t\geq0`$ and expert values are available before the current answer, and $`\alpha,\beta>0`$ are fixed feature scales. Expert features $`\alpha w_t(q_{t,i}-p)`$ yield weighted Brier regret at most $`2\sqrt{B_T}/\alpha`$ to each supplied expert. Calibration features $`\beta w_tb_j(p)`$ yield residuals at most $`\sqrt{B_T}/\beta`$ in the declared continuous bins. These are meaningful finite guarantees with charged computation and truthful feedback. They neither discover arbitrary mathematical structure absent from the experts nor supply a universal convergence rate. Zero-allowance potential control and concatenated features are established machinery; the adaptation is the bounded rational calculation, versioning, feedback, and loss interface.

Paid selective feedback adds observable performance estimates: only issued forecasts, purchased checked labels, and actual selection probabilities enter the reports. In the binary setting, Brier loss and prospective action-error probability differ by the public term $`p_t(1-p_t)`$. This lets appropriately centered estimators share one unknown residual. Conditional bounded-moment arguments then yield scoped horizon-specific bounds. The fixed query tape, positive purchase probabilities, frozen block state, and fresh-bit assumptions matter. Deterministic pseudorandom test paths check formulas, not coverage frequencies. The [supporting derivations](v3/derivations/07_observable_performance.md) retain the exact sampling contract.

<a id="sec-stopping"></a>

### 5.2. A sharp bound can make further calculation unnecessary

Fix bounded losses for a finite action family. Partition a scalar outer range into finitely many cells on which every loss is constant, denoting the loss of action $`a`$ in cell $`j`$ by $`v_{ja}`$. Let $`K`$ be the known attainable cells and $`P`$ the possible cells. The true nonempty support $`J`$ satisfies $`K\subseteq J\subseteq P`$. Its robust loss is $`W_a(J)=\max_{j\in J}v_{ja}`$. Define $`l_b=\max_{j\in K}v_{jb}`$, or $`-\infty`$ when $`K`$ is empty.


<a id="thm-gap"></a>

**Theorem 7 (Sharp computational gap from a partial cell signature).**
For at least two actions, the largest possible robust suboptimality of incumbent $`a`$ under this information is


<a id="eq-gap"></a>

```math
\Gamma_a=\max\left\{0,\ \max_{b\ne a}\max_{j\in P}
          \bigl[v_{ja}-\max\{l_b,v_{jb}\}\bigr]\right\}.
 \tag{15}
```

For one action it is zero. Direct computation uses $`O(|P|\,|\mathcal A|^2)`$ scalar work. The bound is sharp for the signature, whose permitted supports may be more numerous than those realizable by the original source model.



**Proof.** For any admissible support choose a cell $`j`$ attaining $`W_a(J)`$. Every competitor satisfies $`W_b(J)\geq\max(l_b,v_{jb})`$, giving the upper bound. Conversely, for a maximizing pair $`(b,j)`$ choose $`J=K\cup\{j\}`$. Then $`W_b(J)=\max(l_b,v_{jb})`$ and $`W_a(J)\geq v_{ja}`$, attaining a positive maximum; if the bound is zero every admissible support has zero suboptimality. No enumeration of all possible supports is needed. $\square$

For known cell losses $`(9,0)`$ and $`(0,10)`$, and one possible additional cell $`(12,13)`$, separate worst-loss intervals give a suboptimality upper bound of $`2`$ for action A. [Equation 15](#eq-gap) gives $`0`$: the actual worst-loss vector is either $`(9,10)`$ or $`(12,13)`$, both favoring A. B is better in the first known cell, so statewise dominance alone does not explain the result. Retaining joint information about the losses makes the decision complete before the values are complete.

If a computation only refines knowledge of this fixed source and fixed action class, has no reuse or other benefit, and costs $`c`$ in the same loss units, then $`c\geq\Gamma_a`$ rules out a strict net improvement in this robust criterion. A positive $`\Gamma_a`$ only bounds possible benefit; it does not recommend purchase. Optimality also does not imply safety: losses $`(0,10)`$ and $`(10,0)`$ make both actions minimax-optimal on the known two-cell support, while either can incur actual loss $`10`$.

The continuous analogue replaces the cell maximum by a supremum over an outer set and retains known inner-set maxima. For piecewise-linear losses, endpoints and original knots alone can miss a maximum: additional intersections where a competitor crosses its known lower maximum are required. The preserved example has a missed maximum $`13/4`$ at $`q=3/4`$, versus $`1`$ on the insufficient candidate set. This refinement is separately developed, not imported into the finite theorem without its compactness and continuity assumptions.

<a id="sec-observation"></a>

### 5.3. Observation value needs a different policy class and a named baseline

Computation selection is an established metalevel decision problem [14](#ref-hay). A new truthful observation can change which action is taken in the actual state; it is therefore not bounded by a fixed-model optimization gap. If actions have losses $`(0,1)`$ and $`(1,0)`$ on two known states, both have minimax loss $`1`$ and computational gap zero. A perfect signal permits loss zero. Robust information discovery studies exactly this distinction [15](#ref-paradiso).

For a deterministic truthful signal $`s(j)`$ and unrestricted deterministic action choice on each signal branch, define


<a id="eq-observation"></a>

```math
B(J)=\min_a W_a(J),\qquad
 Q(J)=\max_{s:J_s\ne\varnothing}\min_a\max_{j\in J_s}v_{ja}.
 \tag{16}
```

$`B(J)-Q(J)`$ is the ideal information value relative to the **best constant action**. Relative to an arbitrary incumbent, the relevant total improvement is instead


<a id="eq-incumbent"></a>

```math
U_a=\max_{K\subseteq J\subseteq P,\ J\ne\varnothing}
             \{W_a(J)-Q(J)\}.
 \tag{17}
```

This includes improvement from selecting a better constant action. For each threshold $`t`$ among the finite loss entries, a branch action $`h`$ is legal when it has loss at most $`t`$ on every known cell in that branch. Its allowed set is $`A_{sh}(t)=\{j\in P_s:v_{jh}\leq t\}`$. Discard a threshold if a branch has no legal action or all allowed sets are empty. Put $`M_a(t)=\max_{s,h\text{ legal},j\in A_{sh}(t)}v_{ja}`$.


<a id="prop-observation"></a>

**Proposition 8 (Exact incumbent-aware observation bound).**
Under the preceding signal and policy contract,


<a id="eq-observation-threshold"></a>

```math
U_a=\max_t\{M_a(t)-t\}.
 \tag{18}
```

It takes $`O(|V|\,|P|\,|\mathcal A|)`$ scalar work for one incumbent, where $`|V|`$ is the number of distinct loss entries. An observation and its required policy calculation costing at least $`U_a`$ cannot strictly improve this single-use robust criterion net of the fee.



**Proof.** For any support use $`t=Q(J)`$ and its optimal action in each nonempty branch; known cells in empty branches are absent. Every cell of $`J`$ lies in an allowed set, so $`W_a(J)\leq M_a(t)`$. Conversely choose a legal branch option and cell attaining $`M_a(t)`$, choose a legal option in every other branch, and take the union of these options' allowed sets. It contains $`K`$, is nonempty, and permits a contingent policy with worst loss at most $`t`$. Its incumbent loss is at least $`M_a(t)`$. The two inequalities establish equality. $\square$

The baseline distinction is substantive. With safe/hazardous losses $`(0,1)`$ and $`(10,1)`$ for fast/fallback, and no known attainable cell, the ideal value $`\max_J(B-Q)`$ is zero for every nonempty possible support. Yet the incumbent fallback can improve by $`1`$ if only the safe cell is attainable. Rejecting every positive-fee observation using the ideal bound would therefore be wrong. The implemented wrapper uses [Equation 17](#eq-incumbent) and reports the ideal baseline separately.

<a id="sec-accounting"></a>

### 5.4. Root accounting and statistical warrants

For a complete policy $`\pi`$ compared with a fallback $`b`$, retain paired expected task/resource savings $`d_{\pi,b}`$. Simultaneous coordinate bounds $`l_j\leq\mathbb E d_j\leq u_j`$ give, at price vector $`\lambda`$, the lower saving $`L=\sum_{\lambda_j\geq0}\lambda_jl_j+\sum_{\lambda_j<0}\lambda_ju_j`$. For $`H`$ future uses, subtract still-unpaid policy overhead from $`HL`$ to choose a continuation. Already incurred acquisition and selection costs remain in the root bill even though they should not distort the continuation choice. An unsuccessful assessment branch still paid them. Complete policies retain shared uncertainty across branches; independently minimizing every branch requires an additional rectangularity assumption.

Statistical source bands require their own coverage guarantee. If a single simultaneous event of probability at least $`1-\delta`$ contains the actual source in every selected version, all sound deterministic consequences of it inherit that event. With absolute loss bounded by $`\gamma`$ on that event and always in $`[0,M]`$, one obtains $`\Pr(\text{loss}>\gamma)\leq\delta`$ and $`\mathbb E[\text{loss}]\leq\gamma+\delta(M-\gamma)`$. Here $`\gamma`$ is an absolute bound, not the suboptimality $`\Gamma_a`$. Fixed-time confidence intervals do not justify arbitrary adaptive stopping; confidence-sequence methods provide the appropriate established contract [16](#ref-howard). This project does not implement a general statistical source-calibration layer.

<a id="sec-q5"></a>

## 6. Q5: probability information in values

**Strongest supported answer.** Known expected-loss values can encode all, some, or none of a probability law. The amount depends on payoff semantics and the admitted source family. A decision can be identifiable when the full law and even its absolute action costs are not. Conversely, optimization values and computational invoices need not be probabilities at all.

Let $`p\in\mathcal P\subseteq\Delta_n`$ be an admitted law and observe $`y=Lp`$, where the loss rows of $`L`$ are known. The fiber $`\mathcal F(y)=\{p\in\mathcal P:Lp=y\}`$ expresses the unresolved information. A target is recoverable precisely when it is constant on every relevant fiber; an empty fiber signals incompatible premises.


<a id="thm-identification"></a>

**Theorem 9 (Expected-loss identification on the full simplex).**
Put $`A=[\mathbf1^T;L]`$. A linear target $`Cp`$ is determined by $`Lp`$ for every $`p\in\Delta_n`$ if and only if $`\ker A\subseteq\ker C`$, equivalently every row of $`C`$ is in the row span of $`A`$. In that case $`C=a\mathbf1^T+BL`$ and the decoder is $`Cp=a+By`$. Full-law recovery requires and is implied by $`\mathrm{rank}A=n`$.



**Proof.** The row-space identity supplies the displayed decoder. Conversely, if $`Ad=0`$ but $`Cd\ne0`$, sufficiently small opposite perturbations of the strictly positive uniform law, $`p_\pm=\mathbf1/n\pm td`$, remain in the simplex. They have identical observations and different targets, defeating any decoder, linear or otherwise. The normalization row is essential. $\square$

On a convex restricted family, replace the ambient space by its actual affine direction space. On a nonconvex catalogue the literal fiber criterion remains valid but the ambient rank condition need not be necessary: one linear measurement can distinguish finitely many known candidate laws. Convexifying the family before conditioning can introduce false ambiguities. This is the same structural reason that V19 keeps a nonconvex image rather than automatically replacing it by its hull.

For a binary event with probability $`p`$, a known expected cost $`v=c_0+(c_1-c_0)p`$ recovers $`p`$ whenever $`c_1\ne c_0`$. If the stakes are unknown, the same number need not identify a probability. A realized cost is also not an expected cost. Proper scoring rules give an established loss-based incentive to report distributions [17](#ref-scoring); they do not make every utility or receipt a probability.

For an explicit task-only result, retain $`y=p_1`$ on three states and losses $`c_A=(0,1,2)`$, $`c_B=(1,0,1)`$. Their expected costs are $`1-y+p_3`$ and $`y+p_3`$. Their difference $`1-2y`$ is known, so A is optimal for $`y>1/2`$ and B for $`y<1/2`$, although neither absolute cost nor the full law is identified. More generally, a guaranteed Bayes action exists on a fiber exactly when the intersection of its pointwise optimal-action sets is nonempty. A minimax action can exist without this common Bayes optimum; the consumer must name the intended criterion.

The discovery portfolio also studied information carried by query counts and invoices. Exact parity rates and approximate nonlinear summaries show that the permitted observation channel can matter as much as the scalar's name. Their private-read, reset, and public-count restrictions are load-bearing; direct transmission of a summary or shared randomness can erase a separation. They are retained as interface results with application and novelty obligations, not generalized into a claim that money or computation time always encodes useful probabilities.

<a id="sec-episode"></a>

## 7. A worked reasoning episode: partial evidence, action, and revision

The following example connects the numerical source, partial computation, stopping decision, and evidence reuse. **The source-to-action portion is already implemented** in the developmental `DecisionService`. The final model-edit step below is a mathematical composition with a separately proved transport rule; the current wrapper does not implement automatic cross-version transport.

There are two blocks $`(x_i,y_i)\in[0,1]^2`$. Their sums lie in $`[1.19,1.21]`$ and $`[1.79,1.81]`$, respectively. Receipts require $`\max_i x_i\geq.99`$ and $`\max_i y_i\geq.99`$. Equivalently, the minimum of the corresponding negative coordinates lies in $`[-1,-.99]`$, fitting [Equation 1](#eq-source). The future scalar is $`q=\min_i(.5x_i-1.5y_i)`$. A fast action loses $`10`$ when $`q`$ is in the hazard band $`H=[-5/4,-6/5]`$ and zero otherwise; fallback loses $`1`$ everywhere. These are declared mathematical losses, not measured deployment outcomes.

**Partial evidence.** Initially the implementation has outer range $`[-3/2,1/2]`$ and no known source. It reports a decision conditional on nonemptiness, conservatively choosing fallback. Fallback's sharp possible improvement is $`1`$; the best-constant-action information bound is nevertheless zero, illustrating the baseline distinction in Section 5.3. A new observation costing at least $`1`$ cannot improve this incumbent net of that fee under the stated single-use policy contract. A cheaper observation is not automatically worth buying.

**A computation choice.** The controller performs two passes of exact box propagation over the eight indexed local slices. Neither block can witness both receipts because its sum would be at least $`1.98`$. Only two split assignments survive. Assigning the $`x`$ receipt to the first block gives its $`y`$ coordinate in $`[.19,.22]`$; assigning the $`y`$ receipt gives its $`x`$ coordinate in the same interval. The second block's free coordinate is in $`[.79,.82]`$. The resulting outer range is


<a id="eq-episode-range"></a>

```math
O=[-281/200,-11/8]\ \cup\ [-221/200,-43/40],
 \tag{19}
```

which misses $`H`$. The saved run records 134 row visits, 28 coordinate-bound updates, and zero optimizer calls. A tailored ordinary calculation derives the same answer. The chosen propagation route is a demonstrated operation, not a claim that it was the optimal computation to purchase. A later complete range certificate agrees with this union, but the partial service correctly does not label its current state exact without corresponding inner coverage.

**An action before completion.** An original-source witness $`((1/5,1),(1,4/5))`$ passes the base and receipt checks and gives $`q=-7/5`$. It establishes nonemptiness. The outer exclusion then certifies fast with worst loss zero and $`\Gamma_{\mathrm{fast}}=0`$. The action needs neither every local LP optimum nor an exact identification of $`q`$. Under the fixed-model, single-use stopping contract, further paid calculation cannot improve its robust action loss. A second witness $`((1,1/5),(4/5,1))`$ gives $`q=-11/10`$ and preserves additional attainable information for later questions. The implementation binds evidence to a copied problem digest, rejects a wrong digest and an infeasible source without changing state, and binds the loss/signal request separately. These checks prevent a valid bound from being silently applied to a different problem.

**A subsequent model edit.** Suppose a later version changes a local slice from $`Ax\leq b`$ and readout $`c^Tx+d`$ to $`A'x\leq b'`$ and $`c'^Tx+d'`$, with the same indexed coordinates and a warranted new finite box $`l\leq x\leq u`$. An old nonnegative multiplier $`z`$ remains useful even if it is no longer dual-feasible for the new objective:


<a id="eq-dual-reuse"></a>

```math
c'^Tx+d'\leq d'+z^Tb'
       +\sum_r\max\{(c'-A'^Tz)_r l_r,(c'-A'^Tz)_r u_r\}.
 \tag{20}
```

Insert and subtract $`z^TA'x`$, use the new inequalities, and maximize the remaining linear residual on the new box to prove it. A corresponding lower bound follows with a nonnegative lower multiplier. Rebuilding all indexed outer slices from these corrected bounds preserves a sound range enclosure. An old empty slice must be reconsidered unless its infeasibility certificate still works. An added source block, changed coordinate identity, unwarranted new box, or changed loss semantics is outside this reuse step and requires a new binding or proof.

Thus the fast action may be retained only if the rebuilt outer range still misses $`H`$ and the new nonempty source duty is met. Otherwise the old action certificate becomes stale and fallback or new acquisition is appropriate. This last paragraph is a **conditional mathematical composition** of established dual-residual bounding with the range interface. The repository tests the transport component separately; it has not executed this exact revision as one end-to-end controller episode. No statistical coverage layer, N16 solve, or automatic model-learning loop is silently attached to the implemented example.

<a id="sec-evidence"></a>

## 8. Evidence, adverse comparisons, and reproducibility

The investigation contains both the original five-question traversal and a long discovery portfolio. Their results have different evidential roles. The principal V19 confirmation reconstructed the frozen mathematical claim and assessed its useful moderate synthesis. It was conducted by the same model, with access to the source, and is not independent expert peer review. Other mechanisms retain their developmental status. The author accepted the bounded contribution and authorized this synthesis; final phase completion remains a separate decision.

**Table 1. Selected executable evidence.** Counts refer to saved exact finite controls or exposed constructed examples. Support uses may repeat the same support under several brackets; they are not independent observations. These are validity and mechanism checks, not confidence intervals or estimates of deployment success.

| Service | Unit and denominator | Recorded result | Evidence scope |
| --- | --- | --- | --- |
| Range certificate audit | 13 problems; 143 bounded and 24 empty slices | 37 source witnesses; 114 rejected mutations | Development; local checker, not end-to-end proof |
| Partial range service | 6 problems; 538 answers | 86 checked attainable answers | Development; exposed examples |
| Sharp stopping gap | 2,904 brackets; 11,904 support uses | 728 tighter bounds; 118 new optimality certificates | Development; exhaustive finite controls |
| Incumbent observation bound | 7,260 brackets; 930 distinct support controls | 2,435 tighter bounds than sum of separate maxima | Development; finite controls |
| Structured model correction | 729 maps over the three-element field | 19,683 repaired vectors | Development; exact finite-field scope |
| Greatest-point shortcut | 9 restricted cases | 34 versus 266 LP calls | Structural shortcut; not general speedup |
| Bound source-to-action service | 3 source checks; 2 invalid inputs rejected | 0 optimizer calls | Implemented composition on exposed example |

**Table 2. A matched historical resource comparison.** The four 128-request streams have 512 outputs per arm and the same supplied-source duties. Audit fees and instrumented counted work are separate components; setup is included in the reported counted-work convention. Unmeasured host, retention, and other costs are not assigned zero. The figures are extracted from all 16 original stream/arm records.

| Method | Outputs | Audit fees | Counted work |
| --- | --- | --- | --- |
| Selective controller | 512 | 2,886 | 137,310 |
| Same controller, ordinary label | 512 | 2,886 | 137,310 |
| Distinct greedy-cover control | 512 | 2,937 | 157,452 |
| Always-fallback control | 512 | 4,608 | 152,022 |

The selective controller saves **37.37% in audit fees and 9.68% in counted work relative to fallback** on this panel. The identical ordinary implementation ties exactly. Against the genuinely different greedy-cover control, the fee and counted-work totals are also lower, but this is a bounded developmental comparison, not a universal optimality or complete economic result. A later source-specific panel had larger savings against its full-audit control under a different duty; it is not pooled with Table 2 or presented as continued improvement on the same benchmark.

The earlier frozen phase-three execution is equally relevant. Its original public stage preserved 440 completed units, then hit a deterministic initialization defect. An explicitly versioned amendment reused those records and completed the remaining 60 public units and 500 private scores. The original failed-prefix invoice remains unknown. The recorded complete-path comparisons are adverse: selected caching increased every paired broker bill, and direct ordinary certificate checking was cheaper in all eight full group/recipient cells and delivered more coverage under actual caps. The global positive economic gate remained false. Those findings rule out a broad full-cost headline; they do not invalidate the conditional mathematics or erase the bounded component gains in Table 2. The [execution appendix](v3/experiments/results.md) preserves the exact amended status and denominators.

The scope of novelty is therefore differentiated. V19 is the principal assessed algorithmic and representational synthesis. N16 offers an analytic information theorem with an unresolved contribution comparison. Error-space correction and finite forecasting explicitly reuse classical results. The stopping/observation formulas expose useful dependency and baseline information in a small exact service, with standalone novelty unassessed. Counterfactual typing and probability fibers clarify the required interfaces. The phrase “ordinary methods tie” settles only an identity comparison; it does not decide whether a specialized theorem, useful representation, or application is worth contributing. Conversely, a gain against a weaker information set does not establish an algorithmic advantage at equal information.

All displayed results are traced in [Appendix A](v3/report/claims.md). [Appendix B](v3/report/portfolio.md) retains the alternatives, adverse screens, and excluded extensions. [The build guide](v3/report/README.md) gives exact commands. One canonical scientific source generates both editions, their numbered results and equations, and the bibliography. The table extractor reads preserved JSON evidence and records hashes without reacquiring old experiments. A separate narrow episode check verifies the displayed rational arithmetic and the implemented interface without replacing the historical run. Original phase-three derivations retain their attribution to ChatGPT (GPT-6 Astra Pro); later discovery, confirmation, and this synthesis are attributed to Codex (GPT-6). Neither model-generated analysis nor the author's project role is represented as third-party endorsement.

<a id="sec-conclusion"></a>

## 9. Accomplishment, remaining gaps, and next direction

Phase three produced a concrete positive contribution and a connected set of mechanisms for acting with incomplete mathematics. Its strongest result makes retained optimum receipts into an exact, certifiable future-range service with explicit parameter dependence. The wider synthesis shows how incomplete ranges can settle actions, how a stopping bound differs from observation value, how numerical information survives warranted edits, how a globally fallible model can be corrected for a task, and when values identify probabilities or only decisions. These are useful restricted answers to all five questions. They advance the organizing goal without requiring a new foundation for every form of mathematical uncertainty.

The largest gaps are now specific. First, the mechanisms assume truthful structural or statistical warrants whose acquisition can be expensive. Second, the strongest conventional methods often supply the same mathematics, leaving the contribution at the level of a specialized theorem or synthesis rather than an exclusive computational capability. Third, full-service economics and external transfer are unresolved. Finally, general learning of unresolved mathematical truth, automatic selection of counterfactual semantics, and a complete adaptive model-revision controller remain beyond what was established.

The priority is **one concrete repeated-decision application of retained partial results**, with real source access, changing readouts, and prices. It should compare direct queries, generic MIP/disjunctive methods, structural shortcuts, and the specialized range service under identical information and full accounting. This tests whether the useful information structure survives a natural acquisition regime. In parallel, a tightly bounded specialist comparison could resolve N16's remaining analytic novelty question; another large random numerical panel would be less informative. The preserved portfolio offers alternatives if either access economics or novelty fails.

The recommendation is **ready to proceed to P3-D's final audit and author decision at the stated bounded scope**. This is a readiness recommendation for a completed synthesis, not a declaration that phase three is complete, that every secondary result is confirmed, or that the broadest five questions have been solved.

## References

<a id="ref-li"></a>

1. S. Garrabrant, T. Benson-Tilsen, A. Critch, N. Soares, and J. Taylor. *[Logical Induction](https://intelligence.org/files/LogicalInduction.pdf)*. arXiv:1609.03543; full project paper, 2016.

<a id="ref-abstract"></a>

2. P. Cousot and R. Cousot. *[Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml)*. POPL, pp. 238--252, 1977.

<a id="ref-inverse"></a>

3. S. Ahmed and Y. Guan. *[The Inverse Optimal Value Problem](https://www.isye.gatech.edu/~sahmed/invlp.pdf)*. Author version of the inverse optimization study, 2005.

<a id="ref-mip"></a>

4. D. Teichrib and M. Schulze Darup. *[Piecewise Regression via Mixed-Integer Programming for MPC](https://proceedings.mlr.press/v242/teichrib24a.html)*. PMLR 242, pp. 337--348, 2024.

<a id="ref-berger"></a>

5. G. O. Berger and S. Sankaranarayanan. *[Template-Based Piecewise Affine Regression](https://www.cambridge.org/core/journals/research-directions-cyber-physical-systems/article/templatebased-piecewise-affine-regression/9CC69E94D4F222CA4741ADA0181D5471)*. Research Directions: Cyber-Physical Systems, 2024.

<a id="ref-goodman"></a>

6. J. Goodman. *[Semiring Parsing](https://aclanthology.org/J99-4004/)*. Computational Linguistics 25(4), pp. 573--606, 1999.

<a id="ref-halpern"></a>

7. J. Y. Halpern. *[Axiomatizing Causal Reasoning](https://arxiv.org/abs/cs/0005030)*. Journal of Artificial Intelligence Research 12, pp. 317--337, 2000.

<a id="ref-counterpossible"></a>

8. F. Berto, R. French, G. Priest, and D. Ripley. *[Williamson on Counterpossibles](https://doi.org/10.1007/s10992-017-9446-x)*. Journal of Philosophical Logic 47, pp. 693--713, 2018.

<a id="ref-robustls"></a>

9. L. El Ghaoui and H. Lebret. *[Robust Solutions to Least-Squares Problems with Uncertain Data](https://people.eecs.berkeley.edu/~elghaoui/Pubs/rob-ls.pdf)*. SIAM Journal on Matrix Analysis and Applications 18(4), pp. 1035--1064, 1997.

<a id="ref-operator"></a>

10. N. Bousselmi, J. M. Hendrickx, and F. Glineur. *[Interpolation Conditions for Linear Operators and Applications to Performance Estimation Problems](https://arxiv.org/abs/2302.08781v3)*. arXiv:2302.08781v3, 2024.

<a id="ref-bma"></a>

11. J. A. Hoeting, D. Madigan, A. E. Raftery, and C. T. Volinsky. *[Bayesian Model Averaging: A Tutorial](https://sites.stat.washington.edu/www/research/online/hoeting1999.pdf)*. Statistical Science 14(4), pp. 382--417; corrected author version, 1999.

<a id="ref-cross"></a>

12. I. V. Oseledets and E. E. Tyrtyshnikov. *[TT-Cross Approximation for Multidimensional Arrays](https://doi.org/10.1016/j.laa.2009.07.024)*. Linear Algebra and its Applications 432(1), pp. 70--88, 2010.

<a id="ref-vovk"></a>

13. V. Vovk. *[Non-asymptotic Calibration and Resolution](https://arxiv.org/abs/cs/0506004v4)*. arXiv:cs/0506004v4, 2006.

<a id="ref-hay"></a>

14. N. Hay, S. Russell, D. Tolpin, and S. E. Shimony. *[Selecting Computations: Theory and Applications](https://arxiv.org/abs/1207.5879)*. UAI; arXiv:1207.5879, 2012.

<a id="ref-paradiso"></a>

15. R. Paradiso, A. Georghiou, S. Dabia, and D. Tönissen. *[Exact and Approximate Schemes for Robust Optimization Problems with Decision Dependent Information Discovery](https://arxiv.org/abs/2208.04115v1)*. arXiv:2208.04115v1, 2022.

<a id="ref-howard"></a>

16. S. R. Howard, A. Ramdas, J. McAuliffe, and J. Sekhon. *[Time-uniform, Nonparametric, Nonasymptotic Confidence Sequences](https://arxiv.org/abs/1810.08240v9)*. Annals of Statistics 49(2), pp. 1055--1080; arXiv v9 (2022), 2021.

<a id="ref-scoring"></a>

17. T. Gneiting and A. E. Raftery. *[Strictly Proper Scoring Rules, Prediction, and Estimation](https://doi.org/10.1198/016214506000001437)*. Journal of the American Statistical Association 102(477), pp. 359--378, 2007.
