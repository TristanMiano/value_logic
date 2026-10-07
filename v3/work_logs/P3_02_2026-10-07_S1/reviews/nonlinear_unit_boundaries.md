# Nonlinear unit and outcome-stake boundaries

**Status:** Internal same-model targeted hostile review; direct mathematical reconstruction. This note supplies assumptions, proofs, and rational counterexamples for P3-02. It does not assert a new scientific contribution or worldwide priority. The numerical checks below are DEVELOPMENT evidence, not a frozen challenge. Concurrent review time receives no additional principal clock credit.

**Scope:** Finite outcome space; fixed known real loss rows where specified; exact subjective expected losses; declared nuisance transformations. This note distinguishes transformations of an already computed expectation from transformations of its outcome-contingent payoffs. It does not replace the principal artifact, change task status, attempt a gate, or extend to decision learning.

## 1. Unknown common strictly increasing transformation after expectation

Let \(P\subseteq\Delta_n\) be a nonempty source of probability laws and let \(L\in\mathbb R^{m\times n}\) have finitely many fixed queried loss rows. For \(p\in P\), write \(y(p)=Lp\). The recorded numbers have the form

\[
v_j=g(y_j(p)),\qquad j=1,\ldots,m,
\]

where one arbitrary strictly increasing function \(g:\mathbb R\to\mathbb R\) is shared by all coordinates of this record and is unknown.

**Nuisance quantifier.** Global recovery means a single decoder must work for every admissible pair \((p,g)\). Hence a collision may compare \((p,g)\) with \((q,h)\), with different candidate functions \(g,h\). If one instead requires the same fixed function in the two compared hypotheses, its injectivity gives \(g(Lp)=g(Lq)\) iff \(Lp=Lq\); that is a different equivalence question and does not describe uncertainty about the nuisance function.

### M1. Exact observation classes are weak risk orders

Define the complete weak order, including all ties,

\[
i\preceq_p j\quad\Longleftrightarrow\quad (Lp)_i\le (Lp)_j.
\]

For any \(p,q\in P\), the following are equivalent:

1. There are strictly increasing \(g,h:\mathbb R\to\mathbb R\) such that \(g(Lp)=h(Lq)\) coordinatewise.
2. The vectors \(Lp\) and \(Lq\) have exactly the same weak ordering of their labeled coordinates.

**Necessity.** Strictly increasing functions preserve and reflect \(<,=,>\). A common observed vector therefore fixes all risk comparisons and all ties.

**Sufficiency.** Suppose the shared ordered partition has \(k\) distinct levels. Enumerate the levels of \(Lp\) as \(a_1<\cdots<a_k\), the corresponding levels of \(Lq\) as \(b_1<\cdots<b_k\), and choose any common output levels \(z_1<\cdots<z_k\). Interpolate linearly through the points \((a_\ell,z_\ell)\), with positive-slope linear extensions on the two exterior intervals; do the same for \((b_\ell,z_\ell)\). Every intervening slope is positive, so the resulting functions are strictly increasing on the whole real line and give the same labeled output vector. With only one distinct level, a positive-slope affine map suffices. Thus the assertion also covers complete ties.

This proof remains valid if the nuisance class is restricted to strictly increasing continuous bijections of the real line: the constructed exterior extensions make the interpolants onto. It need not remain valid under narrower restrictions such as a known affine family, a prescribed modulus, or a prescribed finite-dimensional parameterization.

### M2. Target recovery and the finite-menu obstruction

For any target \(T:P\to\mathcal T\), with no linearity or continuity restriction on its decoder, exact global recovery from \(v\) is possible **iff \(T\) is constant on each complete weak-order class** of the risks.

Necessity follows from M1's collisions. For sufficiency, compute the weak order of \(v\) and return the common target value assigned to its source class. This is an identification statement; it does not promise an efficient representation or algorithm for an arbitrary target.

If \(P=\operatorname{ri}\Delta_n\) and \(n\ge2\), no finite fixed menu identifies the full law. To see the stronger geometric obstruction, consider the affine risk comparisons

\[
(L_i-L_j)p=0
\]

on the normalization hyperplane \(H=\{p:\mathbf1^\top p=1\}\). Ignore differences that are identically zero; differences that are constant and nonzero on \(H\) give no tie locus. The remaining finitely many proper affine hyperplanes cannot cover the open set \(\operatorname{ri}\Delta_n\). At a point avoiding them there is a nonempty relative open ball with an unchanged weak order. That ball contains distinct laws.

Moreover, **no nonconstant scalar linear expectation \(cp\) is globally identifiable** on this full interior source under this nuisance class. A nonconstant affine function on \(H\) varies on every relative open ball. It therefore varies within the weak-order class just constructed. Constant targets are the explicit exception. This stronger obstruction concerns finite fixed queries with arbitrary unknown monotone calibration; it is not a lower bound for all value representations or all information-access services.

Finite known reference values can constrain order intervals and exact threshold equalities, but do not remove this obstruction. For example, consider binary laws and three queried rows

\[
L_0=(0,0),\qquad L_1=(1,1),\qquad L_E=(1,0).
\]

At \(p=(1/4,3/4)\), take \(g(t)=t\). The observations are \((0,1,1/4)\). At \(q=(3/4,1/4)\), take the globally strictly increasing function

\[
h(t)=
\begin{cases}
t/3,&t\le3/4,\\
3t-2,&t\ge3/4.
\end{cases}
\]

The two branches agree at \(3/4\), and \(h(0)=0\), \(h(1)=1\), \(h(3/4)=1/4\). The same observations arise although the event probabilities are \(1/4\) and \(3/4\). Even exact zero and one anchors do not calibrate an otherwise arbitrary monotone function between them.

### M3. Exactly preserved decisions and access distinctions

If the queried rows are exactly the losses of the finite action menu to be chosen, then

\[
\operatorname*{argmin}_{j}v_j
=\operatorname*{argmin}_{j}(Lp)_j.
\]

The entire optimal-action set, its ties, and the complete preference ordering within that queried menu are identified. Any fixed tie-breaking rule therefore returns a Bayes-optimal action. This conclusion requires no full probability law and no recovery of absolute expected losses.

The following distinct services must not be conflated:

| Information service | What follows |
|---|---|
| Finite fixed risk queries through an arbitrary unknown common strictly increasing function | Exactly their complete weak order is invariant information. |
| The same queries through a known invertible function | Applying its inverse on the observed range restores the original \(Lp\); ordinary finite-matrix and source-fiber conditions apply. |
| The same queries through a restricted unknown positive affine function | More than order can survive; suitable fixed references can calibrate that restricted nuisance family. M1's unrestricted equivalence does not apply. |
| The entire exact ordering of expected scores over every admissible report of a strictly proper score | The unique minimizing report is \(p\), if \(p\) is admitted and strict propriety holds there. A common strictly increasing transformation after expectation preserves that unique minimum. |
| A service returning the exact optimizing proper report | Its returned report can directly identify \(p\); this is a different optimization/access contract from finitely many fixed score queries. |

The full report-order statement treats the entire order relation as available. It does not give an algorithm that extracts an arbitrary real law using finitely many pairwise oracle calls. A finite report menu also need not contain the true law.

Strict increase matters: a merely nondecreasing function can merge distinct risk levels and create spurious ties; a constant function can erase all distinctions. Unknown monotone calibration also supplies no uniform conversion from a small gap in transformed risks to a small gap in the original risks, since admissible functions can flatten a selected interval arbitrarily.

Finally, one function shared across several observed records imposes cross-record comparisons if all transformed numbers are available together. Those comparisons belong to the information contract and must be included. M1 applies directly to the resulting finite combined vector; a per-record analysis may discard such shared-function information.

## 2. Nonlinear transformation before and after expectation

Let the two outcome-contingent action losses and law be

\[
\ell_A=(0,4),\qquad
\ell_B=(5/2,5/2),\qquad
p=(1/2,1/2).
\]

Then

\[
\mathbb E_p[\ell_A]=2<5/2=\mathbb E_p[\ell_B].
\]

Using \(g(t)=t^2\) on the nonnegative domain:

| Operation | Action A | Action B | Preferred action |
|---|---:|---:|---|
| Original expected loss \(\mathbb E_p[\ell]\) | \(2\) | \(5/2\) | A |
| Transform the expected loss, \(g(\mathbb E_p[\ell])\) | \(4\) | \(25/4\) | A |
| Transform each payoff, then average, \(\mathbb E_p[g(\ell)]\) | \(8\) | \(25/4\) | B |

Squaring is strictly increasing on the relevant nonnegative values. If a function strictly increasing on all of \(\mathbb R\) is required, \(g(t)=t|t|\) agrees with this example on those values and supplies a global extension.

The two transformed quantities are different even though the same formula is used for \(g\). A strictly increasing transformation of an already computed expectation preserves its ranking. Applying a nonlinear transformation to the semantic payoff changes the expectation being evaluated and can reverse the action choice.

A common positive affine transformation is the constructive commuting case. For \(g(t)=\alpha t+\beta\), \(\alpha>0\), normalization gives

\[
\mathbb E_p[g(\ell)]
=\alpha\mathbb E_p[\ell]+\beta
=g(\mathbb E_p[\ell]).
\]

It preserves all expected-loss comparisons. The counterexample establishes the needed obstruction for general nonlinear transformations without invoking a broader utility-representation theorem. Replacing semantic payoffs by their squares is therefore not merely relabeling the numerical units of an existing linear expectation.

## 3. Outcome-dependent stakes and proper scoring

Let \(\ell(q,i)\) be a loss score for report \(q\) and outcome \(i\), with the expected risks below well defined. Let \(s_i>0\) be outcome-dependent stakes that are fixed across reports. For a normalized law \(p\), define

\[
S=\sum_i p_i s_i>0,\qquad
r_i=\frac{p_i s_i}{S}.
\]

Then for every report \(q\),

\[
R'_p(q)
=\sum_i p_i s_i\ell(q,i)
=S\sum_i r_i\ell(q,i)
=S R_r(q).
\tag{S1}
\]

This is a direct reweighting identity. No probability-recovery or propriety theorem is needed to establish it.

### S2. Incentives, support, and report-domain assumptions

If the base score is strictly proper at \(r\), and \(r\) is an admissible report, then the unique minimizer of the staked risk is **\(q=r\)**. It need not be \(q=p\).

The domain qualification is substantive. For a positive interior law and strictly positive finite stakes, \(r\) remains interior; an interior-domain strictly proper score can then be applied. A score strictly proper on the full closed simplex, such as the usual Brier loss, also covers boundary laws. If a score permits only strictly positive reports but \(r\) is on the boundary, its admitted report set may contain only an infimum approaching \(r\), so one must not assert an attained unique minimizer \(q=r\).

Common outcome-independent positive stakes are the incentive-preserving case: if every \(s_i=s\), then \(S=s\) and \(r=p\). For a fixed law \(p\), \(r=p\) iff the stakes are constant on the support of \(p\). Indeed, for every \(i\) with \(p_i>0\), the identity \(r_i=p_i\) is equivalent to \(s_i=S\). Stakes on zero-probability outcomes are irrelevant to that law. Consequently, preserving truthfulness for every strictly positive law requires equal stakes across all outcomes.

Strictly positive stakes preserve the support of the reweighted law. Zero stakes can delete support; if every outcome in the support has zero stake, the whole objective becomes zero. Negative stakes do not admit this reweighted-probability interpretation. These excluded cases are not covered by S1's strictly positive normalized-law conclusion.

### S3. Known stakes can be removed; unknown independent stakes confound

Given \(r\) and known positive stakes, the original law is reconstructed by

\[
p_i=
\frac{r_i/s_i}{\sum_k r_k/s_k}.
\tag{S2}
\]

Only relative stakes are needed, since a common unknown positive multiplier cancels in this formula.

The same distinction appears for event-contingent values. The expected value of the staked event indicator for outcome \(i\) is \(v_i=s_i p_i\), and normalizing these values gives \(r_i=v_i/\sum_k v_k\), not necessarily \(p_i\).

If the stakes are independently unknown positive nuisance parameters, even the entire raw vector \(v\) need not identify probability weights. It identifies support exactly:

\[
v_i=0\quad\Longleftrightarrow\quad p_i=0.
\]

For any candidate law \(q\) with that same support, set \(t_i=v_i/q_i>0\) on its support and choose arbitrary positive \(t_i\) off the support. Then \(v_i=t_i q_i\) for every coordinate. Thus every law with the observed support is compatible. When the support consists of one outcome, its law is already forced; this local exception must not be described as nonidentification. For a strictly positive event-value vector on \(n\ge2\) outcomes, all strictly positive laws are compatible.

In fact, the obstruction is stronger than a finite-query limitation. Equation S1 says the **entire report-indexed expected-risk function** is \(S R_r(q)\). Two pairs of laws and stakes with the same vector \(s_i p_i\) give identical expected risks for every report. An oracle exposing every report risk or the exact optimizer cannot separate those pairs without additional stake information.

This contrasts with the common unknown increasing function applied after expectation in Section 1: that operation preserves the base score's true-law optimizer \(p\); multiplying outcome payoffs first generally changes the optimizer to \(r\).

### S4. Rational proper-score example

Take a binary law and stakes

\[
p=(1/2,1/2),\qquad s=(1,3).
\]

Then \(S=2\), \(r=(1/4,3/4)\), and the raw event-value vector is

\[
v=(1/2,3/2).
\]

The same raw vector arises from \(q=(1/4,3/4)\) with common stakes \(t=(2,2)\). The underlying laws differ, but all report risks in S1 coincide.

For a report \(u\in[0,1]\) giving the probability of the first outcome, use the binary squared-error score

\[
\ell(u,1)=(u-1)^2,\qquad \ell(u,2)=u^2.
\]

The staked expected risk is

\[
R'_p(u)
=\tfrac12(u-1)^2+\tfrac32u^2
=2u^2-u+\tfrac12
=2(u-\tfrac14)^2+\tfrac38.
\]

Its unique minimizing report is \(u=1/4\), with risk \(3/8\); reporting the actual first-outcome probability \(u=1/2\) gives risk \(1/2\). This convention is the scalar binary squared-error score; a two-coordinate Brier convention would multiply both losses by two and leave the optimizer unchanged.

### S5. Report-independent outcome additions preserve incentives

For a common positive scalar \(\alpha\) and any finite outcome-dependent additions \(h_i\) that do not depend on the report, let

\[
\widetilde\ell(q,i)=\alpha\ell(q,i)+h_i.
\]

Then

\[
\widetilde R_p(q)
=\alpha R_p(q)+\sum_i p_i h_i.
\]

The second term can depend on \(p\), but is the same for every report at that law. Thus it preserves the exact minimizing report and strictness of propriety. Unknown \(h_i\) may obstruct recovery of absolute expected loss while leaving these fixed-law incentives unchanged.

If the multipliers depend on outcome as well,

\[
\widetilde\ell(q,i)=s_i\ell(q,i)+h_i,
\]

then

\[
\widetilde R_p(q)=S R_r(q)+\sum_i p_i h_i.
\]

The additions still do not affect the optimizer, but the optimizer is the tilted law \(r\), subject to S2's domain assumptions. Report-dependent additions or multipliers fall outside these invariances.

This is a statement about minimizing expected loss at a fixed law. It does not automatically preserve absolute cost, an uncertainty-set minimax criterion, a budget constraint, or a paid-acquisition service. Those services can respond to law-dependent baselines or scales and require their own comparison contract.

## 4. Review disposition and development evidence

All three proposed boundaries are **accepted with the stated quantifiers**:

1. Arbitrary unknown common strictly increasing transformations of finitely many expected risks leave exactly the complete weak order. They preserve decisions within that queried menu but fail to identify the full interior law, or any nonconstant linear expectation, globally.
2. A nonlinear transformation after expectation and the same transformation of outcome-contingent payoffs before expectation can choose different actions.
3. Positive outcome-dependent stakes tilt the effective law for a strictly proper score; common positive scale preserves the original law's optimizer. Known relative stakes permit debiasing, while unknown independent stakes can confound the original law even with all report risks.

An inline exact-rational Python DEVELOPMENT check verified the zero/one-anchor monotone collision, both transformed-payoff expectation values, the binary stake tilt, the raw event-vector collision, the two squared-score risks, and the known-stake inverse formula. It used rational arithmetic and direct substitution. It did not enumerate arbitrary functions or prove the general propositions; the proofs above carry those claims.

The results are elementary reconstructions and targeted semantic obstructions under a named finite-expectation comparison scope. No novelty is inferred from the change of variables, interpolation argument, or squared-error example. In particular, none establishes a new induction theory or a general lower bound on the dimension of useful value representations.
