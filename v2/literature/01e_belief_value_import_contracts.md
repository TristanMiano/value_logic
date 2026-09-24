# F03 — Belief/value summaries, update contexts, and checked arithmetic

Session: 2026-09-24-S5. Source repository commit:
`f9d5ef6485e947eafd13b3983b477d31f7595cb6`.
Status: F03 continuation, not a selected calculus or a readiness-gate review.
This note extends [the belief/KL audit](01d_belief_kl_objectives.md) and
[the Lawvere/value bridge](01c_lawvere_value_bridge.md). It distinguishes an
external statement, a worked mathematical adapter, and a computational check.
The source IDs refer to [the source manifest](F03_sources.json).

## 1. Source audit: what was actually checked

**S07 (Boyd–Vandenberghe).** Rechecked *Convex Optimization*, §3.2.5
(partial minimization), §3.3.2 (biconjugacy), and exercise 3.39(d). The coauthor's
[book PDF](https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf) was used;
printed p.94, PDF index 107, was visually inspected. Partial minimization needs
joint convexity, not just convexity in each argument separately. Proper closed
convex functions are recovered by taking the conjugate twice. Sections 2–4
below give the explicit finite-dimensional project specializations, rather than
identifying all imprecise beliefs with convex functions.

**S02 (quantitative algebra).** A final targeted retry rechecked Definitions
2.1–2.2 in the institutional manuscript: PDF index 1 was visually inspected,
but index 2 again failed to render. The earlier stronger parsed
substitution-reflection sentence remains unused; no new completeness import
or claim of a visually confirmed erratum is made.

**S12 (Rational Lawvere Logic).** Rechecked the official
[publisher text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol363-csl2026/html/LIPIcs.CSL.2026.3/LIPIcs.CSL.2026.3.html),
particularly its grammar, Definition 10, and Theorem 11. Real constants in a
syntax do not constitute a variable logarithm operation or an algorithm for
computing real constants. Section 5 separates an analytic log enclosure from
the finite, guarded arithmetic comparison to which the source theorem applies.
The earlier recorded normalization-text ambiguity is not used as a premise.

**S14/S15 (belief functional and PDG loss).** Revisited the requested
[post](https://www.greaterwrong.com/posts/e7Pd4Q9TF7jFdmPgz/imprecise-beliefs-a-tiny-introduction)
and its LessWrong mirror, and S15's observational penalty and Appendix C.1.3.
The post's extraction still omits formulas: no missing general theorem is
certified from surrounding prose. S15's
[publisher PDF](https://proceedings.mlr.press/v151/richardson22b/richardson22b.pdf)
index 2 was visually inspected; attempts at 8/28 failed. The following finite
belief/context example is derived explicitly, not attributed to missing text.

**S16 (Local Inconsistency Resolution).** The inspected version is
[arXiv:2604.17140v1](https://arxiv.org/html/2604.17140v1). The abstract page showed
only v1 in its submission history when checked on September 24, 2026. Proposition
1 and Appendix D were checked in HTML and visually in the
[PDF](https://arxiv.org/pdf/2604.17140), indices 3, 17, and 18. Its claimed
parameter convexity under unconditional log-concave parameterizations is not
safe to import as stated: section 4 gives an explicit finite counterexample.
The proof infers joint convexity from separate convexity. This is a scoped
source objection, not an author-confirmed erratum or rejection of the paper's
other definitions, examples, or experiments.

No new source is needed to resolve these questions. The bibliography's eight
core sources and ten supplements retain their identities. The observation
penalty in S16 remains usable; its broader parameter-convexity assertion is
separated and withdrawn from the list of available imports.

## 2. A bridge can preserve every current value and still forget a belief

### 2.1 Explicit interface and its dual

Let X be a nonempty finite outcome set and Δ(X) its probability simplex. Let
B:Δ(X)→[0,∞] be proper and lower semicontinuous: B is finite somewhere and never
negative. For a finite signed cost vector f∈R^X define

    T_B(f) = inf_{q∈Δ(X)} { B(q) + q·f }.

This is the loss-oriented transformer already considered in F03-C28. Its
infimum is an evaluation of candidate laws, not permission to choose the
external world. It is
finite, and its infimum is attained: the objective is lsc on a compact set,
bounded below by min f, and finite at a point where B is finite. This permits
unbounded ranges across different vectors f; there is no universal value cap.

Extend B to R^X by +∞ off the simplex. Its convex conjugate is

    B*(u) = sup_q { q·u − B(q) }.

Direct substitution gives

    T_B(f) = −B*(−f).

Thus the function reconstructed from all these numerical questions is

    B_hat(q) = sup_f { T_B(f) − q·f } = B**(q).                 (1)

Every term in the supremum is an affine minorant of B, because
T_B(f)≤B(q)+q·f. Conversely, if a·q+c≤B(q) for every q, then
c≤inf_q[B(q)−a·q]=T_B(−a); the corresponding term in (1) dominates that
minorant. Consequently B_hat retains all affine lower information. It is
convex and lsc, is at most B, and is the greatest closed convex minorant under
the usual proper-function hypotheses. The last characterization uses S07's
closed-convex biconjugacy result: any proper closed convex C≤B satisfies
C=C**≤B**. At least the zero function is a minorant on the simplex, so there
is no improper negative-infinity issue here.

In particular, a proper closed convex B is recovered exactly. A general
nonconvex belief penalty need not be. This is an information boundary of this
specific linear-expectation query interface, not a theorem that value-first
reasoning must be convex or cannot express independence.

### 2.2 Independence versus no restriction

Use X={00,01,10,11}. Define two penalties:

    B_ind(q) = 0 if q is a product of its two binary marginals; +∞ otherwise;
    B_vac(q) = 0 for every q∈Δ(X).

The independent-law subset is closed: in these coordinates it satisfies
q00 q11 = q01 q10. Both penalties are proper and lsc. Every deterministic
vertex δ_x is a product law. Therefore, for every finite signed f,

    q·f ≥ min_x f(x),
    T_ind(f) = min_x f(x) = T_vac(f).                         (2)

The equality is proved for all f, not inferred from a grid of tests. Neither
normalization nor empty feasibility causes it: both penalties have minimum
zero, and both admit deterministic outcomes.

But the beliefs differ. For example, q_diag=(1/2,0,0,1/2) has uniform marginals
and is not independent. B_ind(q_diag)=∞ while B_vac(q_diag)=0. The convex
minorant in (1) cannot distinguish them, because the simplex is the convex hull
of the deterministic vertices already assigned penalty zero.

### 2.3 A later compatible context separates them

Add the same new penalty to both:

    H(q) = 0 if both binary marginals are uniform; +∞ otherwise.

Ask about mismatch cost f=(0,1,1,0). For B_ind+H the only feasible law is the
uniform product (1/4,1/4,1/4,1/4), and its cost is 1/2. For B_vac+H the feasible
laws have the exact form

    q(t) = (t, 1/2−t, 1/2−t, t),   0≤t≤1/2.

Their cost is 1−2t, with attained minimum zero at t=1/2. Hence

    T_(B_ind+H)(f) = 1/2,       T_(B_vac+H)(f) = 0.           (3)

All current value queries agreed in (2), yet the same admissible update creates
a disagreement in (3). Equality under those queries is therefore not a
congruence for arbitrary addition of belief penalties. Convexifying first and
combining first do not generally commute. Both updated beliefs are consistent;
this example does not rely on an empty admissible model class.

### 2.4 A restricted positive repair

Choose in advance an admitted context family Hcal that contains zero and is
closed under pointwise addition. Compare beliefs using the richer interface

    Φ_B(H,f) = inf_q { B(q)+H(q)+q·f },    H∈Hcal.             (4)

If Φ_B=Φ_C on this declared family, then for every K∈Hcal,

    Φ_(B+K)(H,f) = Φ_B(K+H,f) = Φ_C(K+H,f) = Φ_(C+K)(H,f).

This proves stability under the admitted updates. Infeasible cases may return
+∞; no subtraction of infinities is used. Restrict (4) to proper compatible
contexts when an attained finite result is needed.

Including every singleton constraint H_q would recover B(q)=Φ_B(H_q,0), but
that is not an efficiency claim. A smaller operational family can be the right
compromise. F02's transformers are not refuted; an eventual candidate must say
whether future belief combination belongs to its promised interface. Nor is
(4) a selected core: the allowed contexts and their practical representation
remain design questions.

## 3. Keep the variable of optimization explicit

Three different statements can easily be confused:

* For fixed B, the map f↦T_B(f) is concave (an infimum of affine cost maps).
* For fixed reference p, q↦D(q||p) is convex.
* For a parameterized p_θ, θ↦inf_q[B_θ(q)+q·f] need not be convex.

The first two do not imply the third. A change of parameter coordinates can
change convexity without changing any represented probability distribution.
The next example tests an external assertion of the third kind. It does not
contradict F03-C28 or require abandoning the nonnegative-belief/signed-value
bridge.

## 4. Scoped counterexample to S16 Proposition 1

### 4.1 A two-arc finite PDG satisfying the stated conditions

There is one binary variable and two unconditional arcs. One supplied law is
r=(1/2,1/2). The other is parameterized on the ordinary real line by

    p_θ = ( e^θ/(1+e^θ), 1/(1+e^θ) ).

Use observation weights β1=β2=1 and γ=0; α may be any finite nonnegative
vector, for example (1,1). Thus β≥γα holds. The structural term is absent,
and the inconsistency specified by the observational interface is exactly

    I(θ) = min_{q∈Δ({0,1})} [ D(q||p_θ) + D(q||r) ].         (5)

The model uses full support and finite entropies. Both arcs are unconditional;
one parameterization is constant. For the other, writing s=e^θ/(1+e^θ),

    d²/dθ² log p_θ(0) = d²/dθ² log p_θ(1) = −s(1−s) ≤ 0.

It therefore satisfies the source's own definition of log-concavity. The
parameter manifold can simply be R with its usual affine structure and origin.
There is no conditional-distribution or missing-mass complication.

### 4.2 Compute the minimum instead of appealing to numerical optimization

Use natural logarithms; changing to another fixed base greater than one just
multiplies these quantities by a positive constant. Let q denote the probability
of the first outcome. The objective in (5) becomes

    F(q,θ) = 2[q log q+(1−q)log(1−q)] − qθ
             + log(1+e^θ) + log 2.

In the interior, its first q derivative is 2log(q/(1−q))−θ and its second is
2/[q(1−q)]>0. The unique minimum is therefore

    q* = e^(θ/2)/(1+e^(θ/2)),
    I(θ) = log[ 2(1+e^θ)/(1+e^(θ/2))² ].                   (6)

An independent derivation uses the geometric-pool identity: with
w_i=√(p_θ(i)r(i)), Z=∑w_i, and q*_i=w_i/Z,

    D(q||p_θ)+D(q||r) = 2D(q||q*) − 2log Z.

KL nonnegativity proves both the value and its attained optimizer. This is the
same exact finite identity underlying the earlier pooling adapter, not a new
assumption about the theorem under review.

### 4.3 An exact Jensen violation

Set θ0=0, θ1=2log 9, θ2=4log 9, so θ1 is the midpoint. Equivalently put
θ=2log a and use a=1,9,81. Formula (6) gives

    I(θ0) = 0,
    I(θ1) = log(41/25),
    I(θ2) = log(3281/1681).

Convexity would require 2I(θ1)≤I(θ2). Instead,

    (41/25)² > 3281/1681,
    1681² = 2,825,761 > 2,050,625 = 625·3281.                (7)

Strict monotonicity of log turns (7) into the opposite inequality. Thus (5) is
not convex in the stated parameter, although all the advertised conditions
are satisfied. No rounded comparison is needed. Section 5 additionally gives
a rational enclosure of the positive Jensen gap.

The same failure can be diagnosed locally:

    I''(θ) = p_θ(0)(1−p_θ(0))
             − (1/2) q*(1−q*).

At θ=2log9 this is 81/6724−9/200<0. At θ=0 it is positive. The function also
approaches log 2 for large positive θ while increasing from zero; this agrees
with the explicit failure rather than rescuing convexity.

### 4.4 Locate the gap and retain a constructive replacement

For each fixed q, F(q,θ) is convex in θ; for each fixed θ it is convex in q.
That does not establish joint convexity. Its mixed Hessian entry is −1 and
its determinant is

    2 p_θ(0)(1−p_θ(0)) / [q(1−q)] − 1,

which is negative at the same interior optimizer used above. The source's
Appendix D joint-convexity step cannot be justified by separate convexity.

A correct replacement is: if F(q,θ) is **jointly convex** on a convex feasible
set, then inf_q F(q,θ) is convex wherever the infimum defines a proper value
function. To see the finite case, take ε-minimizers q0,q1 at θ0,θ1 and use
joint convexity at their same convex combination. The resulting inequality
has an additive ε, which tends to zero. This is S07 §3.2.5's actual hypothesis.

A useful realizable repair to (5) is to parameterize the unconditional reference
probabilities *affinely*, p_θ=Aθ+b, on a convex valid-probability domain.
The relative-entropy summand g(x,y)=x log(x/y), for x,y>0, has quadratic Hessian
form

    d²g[(u,v),(u,v)] = (u/√x − √x v/y)² ≥ 0.

Hence D(q||p_θ) is jointly convex; summing it with D(q||r) preserves this.
The usual extended lower-semicontinuous convention handles zero coordinates.
Partial minimization then does apply. This repair concerns the finite
unconditional, γ=0 construction. It is not a theorem for every structural PDG.
Alternatively, fixing q retains convexity in log-concave parameters but changes
the optimization question.

**Disposition O-S16-01.** The broad convexity import is rejected as stated in
v1. The source's observational definition and the earlier finite KL identities
survive. The old source record is retained with a dated correction, not silently
rewritten as if this objection had always been known. No author confirmation,
independent peer review, or judgment about unrelated paper results is claimed.
No downstream gate relied on this convexity assertion, so there is no gate to
invalidate. F03 must retain this restriction in its eventual handoff.

## 5. From logarithmic belief penalties to finite arithmetic certificates

### 5.1 What RLL supplies and what it does not

RLL arithmetic can reason about numbers once their relevant constraints are
supplied. It does not provide a variable logarithm constructor just because a
fixed logarithm happens to denote a real constant. The following adapter
supplies finite rational bounds for selected logarithms, and only then forms
a guarded arithmetic comparison. It does not claim complete KL reasoning,
implement the source proof system, or settle a universal optimization problem
by checking one candidate distribution.

### 5.2 Exact rational enclosure for a single logarithm

For rational r>0 define z=(r−1)/(r+1), so |z|<1. For an integer n≥0 put

    S_n(r) = 2∑_{k=0}^n z^(2k+1)/(2k+1),
    R_n(r) = 2|z|^(2n+3) / [(2n+3)(1−z²)].                (8)

Both are exact rational numbers. The finite geometric identity yields

    1/(1−t²) = ∑_{k=0}^n t^(2k) + t^(2n+2)/(1−t²).

Integrating from 0 to z and multiplying by two gives

    log r = S_n(r) + 2∫_0^z t^(2n+2)/(1−t²) dt.

For z≥0 the remainder lies in [0,R_n]; for z<0 its sign reverses and it lies
in [−R_n,0]. Indeed its absolute value is at most the integral obtained by
replacing the denominator with 1−z². Thus define the exact enclosure

    L_n(r),U_n(r) = (S_n, S_n+R_n)       when r≥1,
                   (S_n−R_n, S_n)       when 0<r<1.        (9)

At r=1 both endpoints are zero. The intervals shrink to log r: |z|<1 makes
the explicit tail bound tend to zero. Nestedness also follows from (8): the
old positive tail bound exceeds the next added term plus the new tail bound;
the negative case follows by reflection. These statements are analytically
proved for every rational r>0 and n≥0, not inferred from the regression grid.

For extreme ratios convergence is slow and rational numerators grow. Range
reduction or a better certified transcendental library may be useful later;
neither a complexity improvement nor an optimal enclosure is claimed here.

### 5.3 Enclosing a fixed finite KL value

For rational distributions q,p with matching finite index sets, if some q_i>0
has p_i=0 the KL value is +∞, which is reported separately. Otherwise

    D(q||p) = ∑_{i:q_i>0} q_i log(q_i/p_i).

Multiply the lower and upper endpoints in (9) by the nonnegative q_i and sum.
The resulting rational interval contains D(q||p). Coordinates with q_i=0
contribute zero, including when p_i=0; no ratio 0/0 is evaluated.

The lower endpoint may additionally be replaced by its maximum with zero.
This uses a separate mathematical inequality, not an assumption that every
pointwise log ratio is nonnegative. For q_i>0 and p_i>0,
−log(p_i/q_i)≥1−p_i/q_i, so summing against q gives

    D(q||p) ≥ 1 − ∑_{i:q_i>0} p_i ≥ 0.

The scalar inequality follows from log t≤t−1; its derivative or integral proof
is elementary. The zero-support case is already handled as +∞.

An upper interval endpoint at most a proposed budget certifies that budget
for the supplied distributions. A lower endpoint strictly above it refutes
the budget. Otherwise the checker returns unresolved rather than guessing.
Finer enclosures can decide a strict gap eventually; exact equality may remain
unresolved without a separate symbolic identity. A fixed-q certificate must
not be reported as a bound valid for every q or an exact optimized value.

### 5.4 Relate the enclosure to the guarded nonnegative language

For each rational ratio at least one, introduce a nonnegative quantity
u_r=log r and its rational lower/upper inequalities from (9). A negative
logarithm is represented as −u_(1/r), not as a negative atom in RLL. Collect
positive and negative contributions as finite nonnegative expressions A,C:

    D(q||p) = A−C.

For a finite rational budget b≥0, the intended comparison is

    A≤C+b,

or the sequent `C, b |- A` under the source's antecedent-sum convention.
All coefficients are nonnegative rational numbers. Add the finiteness guards
for every introduced variable, as required by S12 Theorem 11 and the prior
signed-pair adapter. Rational upper bounds already ensure finiteness
semantically, but the exact source theorem's syntactic hypotheses are not
silently omitted.

The analytic enclosure is evidence *outside* this arithmetic translation.
Within the translation, the finite bound implications are polynomial/linear
comparisons. The implementation checks those rational implications directly;
it does not generate an RLL derivation or run a Positivstellensatz prover.
A named, uncertified floating logarithm would not supply the same evidence.

### 5.5 Certify the source objection without floating-point dependence

The Jensen gap in section 4 is

    G = log(41/25) − (1/2)log(3281/1681).

Using (9),

    L_n(41/25) − (1/2)U_n(3281/1681) ≤ G
       ≤ U_n(41/25) − (1/2)L_n(3281/1681).

Already a small fixed n gives a strictly positive rational lower bound.
The executable report records the exact fractions and an easy lower target
1/10. This is an alternative certificate of (7), whose integer comparison
already proves the sign. Decimal display and numerical optimizers are not
needed for the decisive step.

## 6. Consequences for the candidate comparison

These findings support a more precise version of the author's intuition.
Nonnegative belief penalties can be included in a larger value calculation,
and signed costs can coexist with nonnegative inferential loss bounds. But a
claim that belief is recoverable from *all* value evaluations needs the query
and update family specified. Linear expectation probes recover a closed convex
penalty, not every dependence constraint carried by a nonconvex belief.

For S and P, retain which joint laws or belief constraints supplied the score.
For T, distinguish equality as a current continuation map from stability under
future additions to the belief. For G, declare whether the retained feasible
region precedes or follows convexification; the independence/fair-marginal
example has hard contextual requirements, not permission to randomize an
unknown epistemic fact. None of these repairs chooses a permanent carrier.

The scoped S16 objection concerns an optimization assumption, not the existence
of a value-based bridge. Its useful replacement is a stronger checked
hypothesis, or a different coordinate/optimization contract. Existing
F01/F02 results and F03-C25/C28 do not depend on the rejected assertion.

### Evidence and next obligations

The companion module `v2/checks/f03_context_audit.py` supplies constructed
finite fixtures and exact rational certificates. Numerical reference checks
are labeled separately from exact arithmetic. It is not a reasoner for the
future core, a frozen empirical challenge, or independent peer review.

F03 still owes the rest of its protected source-review minimum and a final
consolidated import handoff. The next audit should retain these restrictions
when reviewing source theorem applicability, rather than grow the source list
or call the current numerical demonstrations a completed calculus. The task
status and actual clocks are in the S5 work record; no gate is passed here.


### Frozen local check result

The new standalone suite passes **40 tests**. All four F03 bridge/audit families
and their earlier suites pass **175 tests together** using the repository
`test_v2_f03*.py` discovery bridges. The stored result file is
[the exact certificate report](../checks/F03_context_audit_results.json).
Finite tests corroborate the displayed constructions; they are not a proof of
unrestricted conjugacy or source completeness. Full repository validation and
GitHub Actions were not run for this unpushed package.
