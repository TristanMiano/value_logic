# F16 principal reconstruction: definitions, quantifiers and revision

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Source commit
`6ef27f20e3ac0920953a27dd84d6c91a021ba58f`. Fresh, **non-blinded**
self-reconstruction. The principal previously saw the F15/ND01 reports and
read TODO, the execution protocol, Gate B's summary and the contribution
review before this derivation. This is not a claim of an externally blinded
proof review. Separate reviewers save their own exposure records.

The first reconstruction below uses the actual F05 semantics and F06 local
rule definitions. Its mathematical implications are derived here before
the principal rereads the old soundness/completeness proof bodies.

## 1. What is assumed and what is concluded

A signature assigns each source coordinate a unit and permits named positive
linear conversion maps. A context contains finitely many named live cases.
Each case is a rational affine polyhedron in one shared coordinate space.
Its supplied rational witness is checked against every source row. Therefore
every admitted case is nonempty. The meaning of the whole context is the
**union** of these cases, not an intersection or an unspecified mixture.

A well-typed term denotes a real-valued continuous piecewise-affine function
on that space. Constants, signed scaling and addition are ordinary arithmetic;
min and max are pointwise; `res(a,b)` means `(b-a)_+`. A `let` evaluates its
right-hand side in the old environment and then evaluates its body in an
extended environment. This is lexical binding, not a simultaneous equation.

For a same-unit pair `(N,O)` and rational budget `b`, the universal comparison
means

\[
  N(z)-O(z)\le b\quad\text{for every }z\in\bigcup_h P_h.
\]

The mathematical use of `for every` and real order is part of the declared
metatheory. It does not give the agent access to an actual deployment state's
membership in the modeled source set. A feasible supplied witness proves
nonemptiness, not that the real deployment is that witness or is in the set.

The resulting implication has four distinct premises/steps:

1. the terms and source set have the stipulated mathematical meanings;
2. a native derivation is sound for its modeled source information;
3. a receiver matches that derivation to the current requested statement;
4. the actual source and deployed criterion satisfy the interpretation contract.

Neither a digest nor a successful syntactic proof check establishes step 4.
Allowing a later model to assess step 4 is legitimate conditional reasoning,
but it introduces that model's assumptions; it is not an automatic closure of
the applicability chain.

### Real models and a rational executable interface

The evaluator's rational input restriction is not a claim that all physical
quantities are rational. Local proof identities below hold over real numbers.
For the admitted rational-polyhedral source and rational CPWA query, a strict
real counterexample also has a rational counterpart: choose its CPWA region,
intersect it with the rational source constraints, and retain the strict
violating half-space. A nonempty rational polyhedron intersected with a
rational strict inequality has a rational point. This can be seen by rational
elimination, or by rational approximation inside the rational affine hull of
the minimal face. Ambient density alone would be insufficient on an arbitrary
lower-dimensional irrational source; that is not the admitted input class.

## 2. Reconstructing the local comparison induction

Write a local judgment as `N-O <= b` on a fixed case. The source-row rule
subtracts the row's constant part and puts its negative on the right; this is
an algebraic restatement of the current row. It does not solve a new problem.

For the constant/rewrite rules, the normalizer must preserve evaluation. Its
affine coefficient collection uses exact rationals, instantiates lexical
bindings, multiplies through declared conversions, and retains nonlinear
min/max children as structured atoms. Residual unfolds its stated max
definition. It never infers a branch sign from sampled points. Structural
identity of the normalized differences is consequently sufficient for
semantic identity. It is deliberately not a complete equality oracle.

The remaining arithmetic steps follow pointwise:

- Transitivity adds `N-M <= a` and `M-O <= b`.
- Addition adds two differences evaluated at the **same** source point.
- Nonnegative scaling multiplies both sides by the same nonnegative factor.
- Negation reverses the expression pair: `(-O)-(-N)=N-O`; it does not negate
  the budget or multiply an inequality by a negative factor without reversal.
- A positive named unit conversion multiplies both the difference and budget.
- Nonnegative slack weakens the conclusion.
- Two proofs of the same difference allow the smaller budget.

Negative budgets are meaningful improvements, rather than malformed data.
For min/max congruence, if `N_i <= O_i+b_i`, let `B=max_i b_i`. Then
`N_i <= O_i+B` for each coordinate, so monotonicity and common translation
give `min_i N_i <= min_i O_i+B`, and likewise for max. This remains valid
when B is negative. Clipping that budget to zero would unnecessarily lose
valid improvement information.

The residual rule has a different bound. Let

\[
  u=N_1-O_0,\quad v=O_1-N_0.
\]

The two premises imply `u-v <= b_0+b_1`. For every real u,v,

\[
  u_+-v_+\le (u-v)_+\le (b_0+b_1)_+.
\]

This is precisely the checked `res_congruence` budget. The positive part is
necessary. For example, `N_0=-1,O_0=0,N_1=-2,O_1=-1` gives two budgets -1,
but both residual outputs are zero. The unclipped proposed budget -2 would
be false. The implemented zero bound is correct.

`max_common` and `min_common` follow the same common-term/translation argument;
lattice injection and projection have zero budget. The finite proof graph
requires strictly backward premise indices, so induction over stored steps is
well-founded. No accepted step can cite its own conclusion as its premise.

### Cases require one common expression pair

If each live case proves the same pair with budget b_h, the union proves that
pair with budget `max_h b_h`. A minimum over case budgets would be unsound.
The checker explicitly requires every live case exactly once and the literal
same expression pair, in addition to equality of normalized differences.

This is a substantive quantifier restriction. With two unobserved source
states and action losses `A=(0,2), B=(2,0)`, each state admits an action of
cost zero, but no single fixed action has worst-case cost zero. Exchanging
`for every state, there exists an action` for `there exists an action, for
every state` would fabricate an operational improvement. The case rule does
not perform that exchange.

The term `min(A,B)` still denotes the pointwise lower envelope. Giving that
term a deployable choice interpretation requires an admissible selector with
the necessary observation. Its algebraic existence alone supplies no such
selector. This is an interpretation boundary to inspect in the application,
not a counterexample to the mathematical min operation.

### Shared uncertainty is retained by composition

For theta in [-1,1], let two component differences be theta and -theta-1/2.
Their sum is identically -1/2. Separately retaining only their upper bounds,
1 and 1/2, yields 3/2, which is valid but much weaker. Conversely, retaining
the convenient values at different source points and treating them as a
joint achievable outcome would be invalid. Native term composition evaluates
one shared assignment, so it retains the cancellation. An ordinary affine
representation with that same shared variable retains it as well.

## 3. Native information access and full-source validity

Consider units U,V, one coordinate x:U, and only the conversion U -> V with
factor 2. Put the row `convert(x) <= 2[V]` in the source. The full modeled
source entails `x <= 1[U]`. There is no authorized path V -> U.

Every rule that uses a row preserves its unit except for a forward named
conversion. Addition, comparison rewriting and lattice rules require common
units. Scaling by zero does not erase the type. Therefore this V-row cannot
supply a native U-conclusion. The U-reduct drops it, and `x=2` is a reduct
countermodel even though it violates the full modeled source.

This proves an information-access limitation, not logical inconsistency.
The ordinary comparator must be given the same reduct when comparing native
availability. A separately labeled full-source optimizer may legitimately do
better. Reporting the reduct witness as a full-source counterexample would
be a concrete receiver/reporting error.

Positive conversion factors are material: forward conversion preserves an
upper-bound comparison. They do not automatically assert that all directed
conversion paths represent one coherent physical unit system. Distinct paths
are distinct declared operations; additional path-coherence identities would
need hypotheses. This is compatible with the current arithmetic semantics.

## 4. A fresh route to the finite completeness argument

This section records the principal reconstruction target before comparison
with the existing F08 proof. It identifies the nontrivial native obligation.

After restricting rows to those whose units reach U and expressing them in a
common numerical presentation, an admitted CPWA difference can be represented
as a finite max of finite minima of affine functions. For one minimum branch
`g(z)=min_j l_j(z)`, its upper bound over a nonempty rational polyhedron can
be written as the LP

\[
  \sup t:\quad Az\le d,\quad t\le l_j(z)\ (\text{all }j).
\]

A finite upper bound yields nonnegative dual coefficients for source rows and
nonnegative weights on the l_j whose sum is one. The weighted affine
combination supplies an upper bound on their minimum. Combine the branch
bounds by max, then combine source cases by max. Rational LP alternatives
handle lower-dimensional and unbounded polyhedra; the original source need
not have a vertex.

However, this semantic LP argument is not by itself a native-completeness
proof. Two additional constructions must be checked:

1. the represented max–min expression must be connected to the actual query
   by derivable zero-budget equalities, not an unimplemented CPWA oracle;
2. retyping/forward conversion through nonlinear expressions must be justified
   using existing rules, despite their opaque nonlinear normalization.

Positive scalar homogeneity of min is derivable. Scaling the two projections
of min(a,b) proves `k min(a,b) <= min(ka,kb)`. For k>0, divide the two reverse
projections by k, take their common minimum bound, and scale back. The k=0
case is constant arithmetic. The corresponding max identity is dual.

For a conversion with factor k>0 into U, the terms `(1/k) convert(a)` and
`(1/k) convert(b)` are U-typed numerical copies of a and b. Opaque normal
forms identify `convert(min(a,b))` with k times the minimum of those copies.
The scalar argument then relates this to `min(convert(a),convert(b))` without
requiring a reverse conversion. Checking the full max–min normalization
construction against F08 remains an explicit next step, not a presumed pass.

## 5. Comparison of the noncircular completeness construction

After saving §§1–4, the principal read the pertinent F07/F08 proof sections
and the actual `positive_min`, `disjoint_hinges`, sign-discharge and source
transport constructions. This is a comparison after reconstruction, not a
claim that the old proofs were hidden throughout F16.

The possible cycle is resolved at the small generic lemma. In a row-free
two-coordinate context, set `a=__lemma_a`, `c=__lemma_b`. Under the affine
guard `a-c<=0`, projection and a common minimum bound give
`a<=min(a,c)`. Applying the common max with zero and projecting from
`min(a_+,c_+)` proves

\[
  \min(a_+,c_+)\le (\min(a,c))_+.
\]

The opposite guard `c-a<=0` gives the same literal pair by the symmetric
argument. Both branches are nonempty, including their common boundary.
Discharging the two opposite guards produces source-free upper allowances
`alpha*(a-c)_+` and `beta*(c-a)_+` for the same difference. Their minimum
is zero. The `disjoint_hinges` construction proves that last identity using
only primitive lattice projections, common bounds, scaling and arithmetic.
It does not call `positive_min`, a CPWA optimizer, or U1.

Transport then substitutes **arbitrary closed, same-unit terms** for a,c in
this one finite proof. The generic source has no rows, so no unproved source
implication is introduced by that substitution. This is why a nonlinear
instantiation does not need another affine split of its own. The reverse
positive-min inequality follows from monotonicity and projections.

Translate this identity by z, with a=x-z and c=y-z, to obtain

\[
 \min(\max(x,z),\max(y,z))=\max(\min(x,y),z).
\]

The translation equalities themselves have native projection/common-bound
proofs. Together with signed scaling, addition, and the dual identities,
these supply the finite lattice-distribution route to the max–min affine
normal form used in §4. Thus the order of dependencies is:

**native arithmetic/lattice rules → disjoint hinges → a fixed affine
two-branch lemma → closed typed substitution → distributive normal form →
lifted LP duals → completeness.**

The old F08 route states these dependencies explicitly. The separate fresh
review additionally emitted a 192-node zero-budget nonlinear instance with
zero source-row reads. That finite example tests the implementation route;
the generic substitution argument is the reason it generalizes. Neither
claim says that the bounded practical producer will always find or afford
the complete proof.

### The exact graph condition, including unused bindings

Let A(U) be the units with a directed conversion path to U, including U.
Induction on term meaning shows that a U-term's **denotational dependence**
is confined to source coordinates whose units lie in A(U). This is not a
claim that every syntactic leaf lies there: `let dead=v:V in 0[U]` can contain
an unused foreign right-hand side. The separate review initially overstated
the syntactic version and corrected it; the existing proof already uses
the denotational version.

If A(U) has no outgoing edge, a source row outside A(U) cannot depend on
an A(U) coordinate: a path from such a coordinate to that row's unit would
have a first outgoing edge. Conversely, retained rows depend only on A(U)
coordinates. Therefore each full source case factors into its relevant and
foreign coordinate constraints. Its admitted full witness supplies a
foreign assignment to accompany **any** point in the relevant reduct.
Dropping foreign rows cannot change any U-query's supremum in that case.

If an edge a→v leaves A(U), introduce x:a, put its converted value under an
upper bound in unit v, and ask for the corresponding bound along a path
a→U. The full source entails that bound; the reduct does not. This constructs
failure of graph-uniform full-source completeness. It quantifies over source
declarations and contexts. A particular context with no such coordinate or
only redundant foreign rows may still be complete. The equivalent graph
description is that every unit in U's weakly connected component reaches U.

## 6. Revision: what must remain fixed and what must be retained

For one fixed query clause `min_j(a_j·z+c_j)` and fixed source row matrix A,
the lifted primal from §4 has the dual feasible set

\[
 D=\{(\lambda,\alpha)\ge0:
 A^\top\lambda=\sum_j\alpha_j a_j,\quad\sum_j\alpha_j=1\}.
\]

Its objective is `lambda·theta + sum_j alpha_j c_j`. Only theta, the source
right-hand sides, varies in the U11 family. The dual set is fixed. Because
the source case is feasible, the primal is feasible by taking t sufficiently
small. If D is empty, this clause is unbounded for every admitted theta;
if D is nonempty, every admitted theta has a finite upper bound.

For a finite optimum, select an optimal dual point of minimum positive
support. If its supported equality columns are dependent, a nonzero kernel
direction permits small perturbations of both signs. A nonzero objective
slope contradicts optimality; a zero slope permits a perturbation that sets
one positive coordinate to zero, contradicting minimum support. Therefore
an optimal independent-support point exists. There are only finitely many
supports, so finitely many rational dual vertices suffice for all feasible
theta. This argument does not assume that the primal source polyhedron has
vertices or is bounded.

Each vertex gives a native derivation whose budget is affine and monotone
in theta. Retain **every** such alternative, combine them with minimum for
one clause, maximum over query clauses, and maximum over live source cases.
The resulting fixed finite portfolio replays to the exact optimal CPWA
bound throughout the fixed-schema family. It is an existence/retention
result, with no polynomial construction-time or storage bound.

### A selected proof is weaker than a complete portfolio

For the query x, suppose the current rows are `x<=theta_1` and
`x<=theta_2`. At `(theta_1,theta_2)=(0,1)`, select the first row's proof.
After revising to `(2,1)`, that proof correctly replays to bound 2, while
the second row gives the optimum 1. Withdrawing the first row eliminates
that selected derivation, although the second row still supplies a fresh
proof. A complete two-alternative portfolio retains both possibilities.

This is the elementary mechanism behind a sound reconstruction miss.
Transport must not advertise the old tight budget after the revision. It
must emit a newly checked proof at its recomputed budget, and the receiver
must compare that budget to the current requested one. Those are the
behaviors examined by the separate implementation audit.

### Optional consequence: withdrawing rows from a complete portfolio

This consequence is reconstructed here to examine assumption weakening; it
is not promoted as a new contribution. Keep the query, row directions and
case schema fixed, but withdraw rows in S. The new dual is the face

\[
 D'=D\cap\{\lambda_s=0\ \text{for every }s\in S\}.
\]

Every vertex of this face is a vertex of D. Consequently an **actually
complete** vertex portfolio contains all certificates needed after this
withdrawal, if the new problem is bounded. Build each vertex certificate
without zero-coefficient source leaves, retain the lambda_S=0 alternatives,
and recompute the remaining right-hand-side budgets. If the face is empty,
the revised clause is unbounded. This reasoning extends case by case; it
does not cover newly introduced source cases or a changed target query.
It also does not turn a pruned or selected practical cache into a complete
portfolio. The face argument explains exactly why discarded alternatives
can matter after withdrawal.

### Three revision operations are not interchangeable

1. Changing evidence **bounds** with fixed source meanings, row directions,
   query and cases is the uniform replay setting above.
2. Changing a price generally changes the **query coefficients** for expected
   cost. The price-retention application analyzes the needed old information
   and new measurements separately; U11 does not by itself cover it.
3. Changing a program may change the meaning or distribution of outcomes.
   Old-to-new source substitution or an applicability bridge must be supplied
   and checked; unchanged metadata labels do not establish that bridge.

The actual transport code binds scope, observation, units/conversions and
the supplied closed source map, covers every new live case, checks replacement
row directions, and recomputes all budgets. A replacement may be weaker than
the old row, but its actual budget then propagates to the new conclusion.
This is proof-relative transport, not an assertion that the old interpretation
remains empirically correct.

## 7. Adaptive applicability and the expectation boundary

This reconstruction compares the event-inclusion contract in
`contribution_review.md` §2.2 with the almost-sure expectation bridge in
`03f_soundness_acceptance.md` §4. These are different premises. The
following exact countermodels attack stronger readings, not the stated
theorems.

### Selection does not invalidate a genuinely common coverage event

Let E be `{theta in C(D)}` with probability at least `1-delta`. The selected
query, its finite budget and the acceptance decision may depend on all of D.
If reception establishes the chosen inequality at **every** point of the
same C(D), it is true at theta on E. Thus

\[
 \{\text{accepted and selected inequality false}\}\subseteq E^c.
\]

This gives a probability at most delta without independence between the
selector and its data. It requires one jointly valid source set in a common
model, not separate fixed-query statements relabeled after selection.

An exact counterexample to the conditional-on-acceptance upgrade is available
with a fixed true coordinate theta=0. Let B be Bernoulli(delta), and let
C(D) be the singleton {0} when B=0 and {1} when B=1. Each source is a
nonempty rational polyhedron. Coverage is exactly 1-delta. Accept the request
`1/2-theta<=0` only when B=1; it is valid on the current source {1} and false
at the actual theta=0. Then

\[
 P(\text{accepted and false})=\delta,\qquad
 P(\text{false}\mid\text{accepted})=1.
\]

The sharp generic conditional bound is
`min(1, delta/P(accepted))`, when the denominator is positive. A small
unconditional error rate can coexist with an unreliable selected output
stream. No proof checker or request fingerprint can correct this by itself.

### Pointwise time coverage and per-query coverage do not compose for free

Repeat the Bernoulli construction independently at times t with the same
fixed theta=0. At every fixed t, coverage is 1-delta. Stop and issue the
false accepted request at the first B_t=1. By time T, the probability of a
false issued request is `1-(1-delta)^T`; with unlimited attempts it is one.
The stopping decision observes B_t, so there is no hidden-information oracle
in this counterexample. A joint/time-uniform coverage event or an explicit
summable error allocation repairs the inference. Pointwise coverage alone
does not.

For query selection, let R be uniform on {1,...,m}. For each registered query
j, suppose its candidate bound fails exactly on `{R=j}`. Each fixed query
has failure probability 1/m, yet selecting query R fails with probability
one. A simultaneous source guarantee prevents this configuration at its
declared joint error level. Registration plus a union allowance is another
ordinary option; independence is not supplied by distinct query names.

### High probability and integrability alone do not imply expected improvement

The preceding coverage condition also permits all outputs to be accepted
with modeled budget -1 while expected actual change is positive. Keep the
same two singleton sources and theta=0. At B=0 choose the constant query
`Delta_g(z)=-1`. At B=1 choose the affine query

\[
 \Delta_b(z)=K-(K+1)z,\qquad K>0.
\]

Each selected query equals -1 on its current source. Its actual value is -1
with probability 1-delta and K with probability delta. Both values are
finite, so the selected difference is integrable, but

\[
 E\Delta=-(1-\delta)+\delta K.
\]

For delta=1/20 and K=20 this is **+1/20**, despite the accepted modeled
budget -1 in every case. Increasing K makes the expectation arbitrarily
bad at the same coverage probability. This does not contradict the F07
expectation theorem, which additionally requires almost-sure source validity.

There are useful repairs that do not impose a universal value cap. For an
always-issued selection with constant budget b and `Delta<=b` throughout
the coverage event E, it is enough to establish

\[
 E[(\Delta-b)_+1_{E^c}]\le r,
 \quad\text{giving}\quad E\Delta\le b+r
\]

whenever the stated expectations are well defined. A global upper bound
`Delta<=B`, B>=b, yields `r<=(B-b)delta`. Alternatively, a bound
`E[((Delta-b)_+)^2]<=M^2` gives `r<=M sqrt(delta)` by Cauchy–Schwarz.
More generally an Lp bound for p>1 gives `M delta^(1-1/p)` by Hölder.
No uniform vanishing-in-delta rate follows from an L1 norm bound alone over
all admissible distributions. A **fixed** integrable excess does have
qualitative absolute continuity of its integral on rare events; the missing
ingredient is a uniform quantitative tail bound for the class being claimed.

If refusal is allowed and A is the acceptance event, the direct bound is
instead `E[1_A*Delta]<=b*P(A)+E[(Delta-b)_+*1_(A intersection E^c)]`.
A conditional mean among accepted outputs divides the excess allowance by
P(A). Behavior on refusal needs its own deployed-loss description; it is
not silently assigned the favorable accepted budget.

For data-dependent budgets the corresponding inequality involves
`E[b(D)]` and the selected excess, with their measurability/integrability
conditions. One must not silently replace that expectation by a favorable
realized budget. These are ordinary probabilistic consequences, not added
native proof rules or new claimed concentration results.

### Fixed policy laws and bounded self-assessment

For the stated branch law
`J(r)=(1-r)p+rs+r/4+z`, comparing the **fixed rational policies** r=1/2 and
r=3/4 gives

\[
 \Delta=\tfrac14(s-p)+\tfrac1{16}+e
       =\tfrac14(s-p+\tfrac12)-\tfrac1{16}+e.
\]

With e<=1/32 and `s-p+1/2<=1/16`, the bound is -1/64. The independent
attainer `p=7/16,s=0,e=1/32` gives old cost `11/32+z`, revised cost
including e `21/64+z`, and difference -1/64. The common finite baseline
cancels and needs no moment assumption for this paired difference.

The mixture formula requires branch rates **conditional on the deployed
selection law**, or a justified independence/causal bridge from marginal
potential branch rates. A fair bit U, potential failures `Y0=U,Y1=1-U`,
and choosing branch 0 at U=1 and branch 1 at U=0 give marginal rates 1/2
and selection frequency 1/2 but actual failure one. Conditional branch
rates are both one, which restores the mixture identity. This example is
already explicit in `03a_soundness_scope_and_use.md` §21.

Changing a report that controls the policy also changes the object whose
failure rate must be bounded. From p<=1,s<=1/4 the fixed-policy bound
`h(3/4)<=7/16` does not authorize substituting 7/16 for the policy's report.
At p=1,s=1/4 the substituted policy has `h(7/16)=43/64`, exceeding its
report by 15/64. The reconstructed self-consistent fixed report 4/7 instead
solves `1-(3/4)r<=r`. This is a finite staged fixed-point calculation under
stated component bounds, not unrestricted self-endorsement.

Finally, allowing r and p,s to vary continuously together introduces the
products rp and rs. Those are not generally CPWA terms in the S1 fragment.
The worked result fixes rational policies; a finite policy family remains
within the fragment. A continuously varying policy would require a separate
modeling reduction or extension, rather than silently treating multiplication
of source coordinates as an existing native operation.

## 8. Price-family reconstruction and the ordinary comparison

This section is a non-blinded principal reconstruction: the C4 theorem
statements and some proof text, plus the separate review, are visible.
The separate price reviewer saved its earlier, partially exposed initial
derivation before its full comparison. No new F15 population is generated.

### Adjacent swaps expose the exact missing information

For one fixed law, write m_S for the probability that every procedure in S
fails. A complete order pi, stopping at its first success, has mean

\[
 C_\pi(c,M)=\sum_{j=1}^k c_{\pi_j}m_{S_{j-1}}+Mm_{[k]},
 \qquad S_j=\{\pi_1,\ldots,\pi_j\},\quad m_\varnothing=1.
\]

Consider a direction v with v_empty=0. Swapping a,b immediately after S
changes its directional cost by

\[
 (c_a-c_b)v_S+c_bv_{S+a}-c_av_{S+b}.
\]

At the empty prefix, vanishing swaps force `v_i=t_1*c_i`. Inductively
subtract the elementary-symmetric terms determined at smaller subset sizes.
At size r, the residuals satisfy
`c_b*u_(S+a)=c_a*u_(S+b)` for |S|=r-1. Divide by the nonzero product of
prices in each r-subset. One-element exchanges connect all such subsets,
so their normalized residual is one scalar t_r. Conversely the elementary
symmetric recurrence verifies every swap. Thus

\[
 v_A=\sum_{r=1}^{|A|}t_r e_r(c_A)\quad
 (\varnothing\ne A\subsetneq[k])
\]

describes the entire proper-subset kernel, and v_[k] is free. There are k
kernel dimensions for within-profile differences. Each size-(r+1) price
monomial is counted once in the ordered mean sum, at its last element, so
every order has the common directional value

\[
 \sum_{r=1}^{k-1} t_r e_{r+1}(c_{[k]})+M v_{[k]}.
\]

This functional is nonzero. Therefore one numeric profile removes one
kernel dimension. On the normalized-law tangent of dimension n=2^k-1,
the within-profile and numeric ranks are respectively n-k and n-k+1.

Strictly positive prices are the task's intended cost model. The algebra
only needs nonzero coordinates: the final coefficient e_k is their nonzero
product, even when lower symmetric sums cancel. The separate signed-price
addendum proves this optional weakening, including mixed signs. It changes
neither the frozen model nor the theorem's advertised positive-price scope.

For a nonproportional second profile d, choose a,b with
`c_a*d_b-c_b*d_a != 0`. If t_1,...,t_(r-1) vanish, a second-profile swap
after any (r-1)-subset avoiding a,b gives

\[
 t_r\Bigl(\prod_{i\in S}c_i\Bigr)(d_b c_a-d_a c_b)=0.
\]

Hence t_r=0 at every proper size. Only v_[k] survives. A nonzero terminal
penalty sees it in numeric means; unequal penalties see it in cross-profile
differences; within-profile differences never do. This recovers C4-T1 and
explains its zero-penalty exceptions. The proportional-family classification
then reduces to the two-dimensional map `(t,v_all) -> (S_c(t),v_all)` and
the ranks of the rows `(lambda_a,M_a)` or their differences.

These ranks become lower bounds for linear retention because small opposite
perturbations of a strictly positive law realize every tangent direction.
If a linear summary identifies every demanded query, its kernel must lie
inside the query kernel. Arbitrary decoding cannot separate equal summaries.
The argument does not apply unchanged to a restricted finite grid that lacks
a relatively open neighborhood, or to arbitrary nonlinear real encodings.
Nor does a worst-case rank imply that every boundary law has a nontrivial
fiber. The code's finite frozen examples are evidence about their specified
instances; they do not replace this general lower-bound argument.

### Actual new means attain the repair rank

Editing c_j by epsilon changes one order's mean by
`epsilon*m_S`, where S is exactly the prefix preceding j. Choose nested
prefixes of sizes 1,...,k-1 among the other procedures and put j after each.
The new actual order mean, minus its known old mean, gives that chain moment
after division by epsilon. The equations for t_r are triangular with
nonzero diagonal products of old prefix prices. Recover all proper moments,
then use the old reference mean and M>0 to recover m_[k].

The old numeric kernel has dimension k-1, so fewer independent extra linear
measurements cannot identify the full law. Adaptivity does not remove this
worst-case deficit: follow a deterministic query algorithm at an interior
law, intersect the old kernel with its fewer-than-(k-1) chosen measurement
kernels, and perturb in a remaining direction. All earlier replies, and
therefore all later query choices, agree along the two perturbed laws.
This is an exact-response oracle argument, not a sample-complexity theorem.

Known lower-order moments remove the corresponding early t_r coordinates;
their information is already paid for. A face forced by a zero marginal can
reduce the dimension further. The actual affine hull, rather than the
unrestricted simplex dimension, controls the applicable rank.

The reconstruction also needs profile and population binding. The separate
review supplies a concrete example in which a wrong old penalty reconstructs
a **different feasible law** from the supplied numbers. Probability feasibility
therefore does not verify that the old summary and new means concern the
same declared profile and population.

### Exact fragility and a cheap stable decision can coexist

Pathwise, a single price edit changes an order's cost by
`epsilon*1{edited procedure is reached}`. Put
`l=min(0,epsilon), u=max(0,epsilon)`. For every fixed action and law the
new-minus-old mean lies in [l,u]. An unchanged fixed fallback has shift zero
and lies in the same interval. Exact old means therefore give a prediction
at the old mean plus `(l+u)/2`, with error at most `|epsilon|/2`.

If a_0 minimizes the old means over the same action family, including
fallback, then for any law p and its new optimizer a_1(p),

\[
 C^1_{a_0}(p)\le C^0_{a_0}+u
 \le C^0_{a_1(p)}+u
 \le C^1_{a_1(p)}(p)+u-l.
\]

Thus the old optimizer has same-law regret at most |epsilon| throughout
the old-summary fiber. An eta-optimal old action gives eta+|epsilon|.
The same interval argument works for any monotone, translation-equivariant
objective on the fixed finite losses, including a fixed-level CVaR or its
worst value over the same law source, **provided the old action is optimal
for that corresponding old objective**. An optimizer of old means alone
does not have this CVaR guarantee. For example, loss A equal to 0 with
probability 9/10 and 10 with probability 1/10 has mean 1, below constant
loss B=2, but its upper-tail CVaR at level 9/10 is 10. Its CVaR regret is
8 even at zero price change. The proper-objective interval proof remains
valid. It cannot carry old source authority,
new program meanings or a changed action family along for free.

At F15's |epsilon|=1/40 and numeric/regret tolerance 1/20, the generic
numeric error bound 1/80 and old-policy regret bound 1/40 already suffice.
The sharper A1 radius is 1/160. Consequently these small-edit tolerance
arms do not discriminate the sharper radius from these ordinary controls.
This derivation does **not** establish the separate native 1/20 fallback
improvement margin or the availability of its premises, and does not claim
to reproduce all 28 useful small-edit episodes with the coarse method.

## 9. Approximation, coherence and a direct capacity comparison

### An independent upper certificate for the three-procedure radius

With k=3 and old unit prices, an equal-old-profile law difference is constant
within each failure-count level. The level cost and reach functions are

| h | g_h | f_1(h) | f_2(h) |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 |
| 1 | 4/3 | 1/3 | 0 |
| 2 | 2 | 2/3 | 1/3 |
| 3 | 3+M | 1 | 1 |

Two compatible laws have the same expected g. Subtract the affine function
`ell_h=(g_h-1)/(M+2)` from each reach function without changing a difference
between those laws. The singleton residuals are

`(0, (M+1)/(3(M+2)), (2M+1)/(3(M+2)), 0)`.

Their range has width A=(2M+1)/(3(M+2)). The pair residuals have range
width `max(1,M)/(3(M+2))<=A`. Differences of expectations cannot exceed
these ranges, so every relevant reach interval has width at most A. This
upper argument does not require solving the old weighted-median calculation.

For attainment, compare a uniform two-failure law with the mixture assigning
`(M+1)/(M+2)` to all-success and `1/(M+2)` to all-failure. Every old order
has mean two. Their singleton reaches differ by A. A revised order placing
the edited procedure second has means separated by |epsilon|A, so any one
prediction errs by at least half that separation on one law. Midpoints of
the exact intervals attain the matching upper bound:

\[
 R=\frac{|\epsilon|(2M+1)}{6(M+2)}.
\]

At M=4, |epsilon|=1/40, this is 1/160. It is a global worst-fiber statement;
it does not assert that the actual frozen F15 fiber attains the witness.
The two witness laws can have the same best execution-order label, so this
numeric obstruction is not a policy-regret lower bound.

### Why the general level calculation is exact

At k unit-price procedures, uniform h-failure worlds have
`g_h=(k+1)/(k-h+1)` for h<k, and `g_k=k+M`. For a particular r-subset,
the reach probability is `f_r(h)=binom(h,r)/binom(k,r)`.

Equal-profile law differences are exchangeable even when the original laws
are not. The global diameter problem therefore reduces to two probability
vectors on h=0,...,k with equal expected g, maximizing their f_r difference.
There are three independent equality constraints: two normalizations and
one common mean. At a vertex at most three masses in total are positive,
since a larger support has a two-sided feasible kernel perturbation. A
nonzero optimum is one level against two levels bracketing it. Solving the
one mean equation gives the three-level chord formula in A2.

The reduction is exact for the **global radius**. For a particular summary,
its retained within-level contrasts must still be read. Subtracting the
minimum contrast at each level gives nonnegative residues rho_w. Every
compatible law is those residues plus an unknown uniform mass at each level,
with one residual mass and one residual g-mean constraint. Conditional
moment endpoints then use at most two residual levels. The number of these
levels is small, but acquiring and reading the original contrasts is not.

### An answer vector and a reusable law have different contracts

Unrestricted sup-norm answers can use separate coordinate interval centers.
A law-valued answer must satisfy all joint-law constraints. In the saved
k=4 example, the coordinate midpoints force negative world mass -3/496.
That rejects their interpretation as one law. The same example nevertheless
has another coherent answer attaining the same **largest** coordinate error,
21/496. It does not prove a strict coherence penalty.

To see why no general convexity shortcut resolves this issue, consider the
ordinary convex set
`conv{(1,1,0),(1,0,1),(0,1,1)}`. Its unconstrained sup-norm radius is 1/2,
at `(1/2,1/2,1/2)`. Every point in the set has coordinate sum two, so at
least one coordinate is at least 2/3; another vertex has that coordinate
zero. A center constrained to the set therefore has radius at least 2/3,
attained by `(2/3,2/3,2/3)`. This is an exact generic counterexample to
automatic coherent-center optimality. It is **not** claimed to be an old
reset-summary fiber. The special family needs its own argument; finite
no-gap searches do not supply a universal theorem.

### The reset mean is an ordinary Choquet observation

Set rho(S)=1-m_S, the probability of at least one success in S. For order pi
put `x_(pi_j)=M+sum_(l=j+1..k)c_(pi_l)`. In descending score order, consecutive
differences are c_(pi_(j+1)), and the final difference is M. Therefore

\[
 \operatorname{Ch}_\rho(x)
   =\sum_{j=1}^{k-1}c_{\pi_{j+1}}\rho(S_j)+M\rho([k]),
 \qquad
 C_\pi=\sum_i c_i+M-\operatorname{Ch}_\rho(x).
\]

The principal derived this from the inspected ordered-difference definition,
then found the same identity already explicit in C4 §13. It is a
reconstruction, not a new identity attributed to F16.

Normalization is not an expressiveness obstacle. Add an always-successful
dummy d with score zero, and define rho'(A)=1 when d is in A and rho(A)
otherwise. It is the normalized coverage capacity of the original random
success set with d adjoined. Positive superlevel sets exclude d, so the
Choquet value is unchanged. At M=0, the last original score ties with d at
zero and the associated increments vanish; the all-failure moment remains
invisible. The separate reviewer checked this construction independently.

An application of a normalized-capacity identification theorem must retain
the deterministic-dummy face, all fixed d-containing capacity entries, the
coverage constraints, and the original k! observation family. It must not
silently substitute a free (k+1)-procedure model. The direct representation
removes a possible artificial novelty distinction; it does not decide whether
an unread earlier theorem already evaluates this special matrix or radius.
The surviving C4-S claim remains modest formal adaptation/application.

## 10. Source coordinates, characteristic probes and penalties

The principal next read `04c_information_and_withdrawal.md`,
`04f_source_substitution_and_penalties.md`, and
`04h_geometry_and_transfer.md`. The row-withdrawal consequence independently
derived in §6 is already U13 in 04c. The new derivation and separate check
confirm it; F16 does not claim to have added that theorem.

### The direction of source strength

For each case h, let V_h be the largest positive part of its accessible,
converted row violations; an empty row list gives zero. Let V_C be the
minimum of these case violations. V_C is nonnegative, and V_C(x)=0 exactly
when x belongs to at least one reduct case. Finiteness matters: outside the
union every V_h is strictly positive, so their finite minimum is positive.

In its own context, native row, conversion, max-common, min-projection and
all-cases rules directly prove V_C<=0. Thus `P_C subset P_D` is equivalent
to the native claim `V_D<=0` in C. A smaller domain permits at least as many
valid inequalities. A weakening to a larger source domain can lose warrants;
it cannot create an old-domain falsehood merely by proving less.

For a closed typed CPWA source map F, its image of the new projected reduct
is a finite union of rational polyhedra. Expand F into affine cells, intersect
each cell with each source polyhedron, then project the affine graph. This
uses closure of **polyhedral** projections, not a false general statement
about continuous images of closed sets.

Every old-query meaning after substitution is evaluation on this image.
Consequently old consequences are preserved iff the image lies in the old
domain; new translated consequences reflect back iff the old domain lies
in the image. Characteristic CPWA probes witness either failed inclusion.
Both directions hold exactly at equality of the two sets. The theorem is
about translated current requests, not replaying an unchanged fingerprint.

For an affine map `x=M*z+d` with exactly the substituted old rows, being
onto is sufficient for faithful full-query transport. The dual balance
equation after substitution is the old equation multiplied by M-transpose;
injectivity of M-transpose makes the feasible dual sets identical. The
objective's offset terms cancel by that same balance equation. In contrast,
the injective map `z -> (z,z)` introduces x=y into an old row-free two-source
model. The old query x-y is unbounded, while its translation is zero. The
onto map `(z,w)->z` harmlessly forgets a new nuisance coordinate.

An old domain with d-dimensional interior cannot be covered by a finite
CPWA map from fewer than d coordinates. Each affine image piece lies in a
proper affine subspace; finitely many such pieces contain no open set.
This is a finite-CPWA representation boundary, not a dimension bound for
arbitrary discontinuous real encodings or a restricted set of consumers.

### Affine observations can lose nonconvex source information

Let Q be `{(0,0)} union {(x,y):x>=1}`. Its convex hull is
`{x>0, any y} union {(0,0)}`, and its closed convex hull is `{x>=0}`.
An affine upper bound is finite on Q only when its y coefficient is zero
and its x coefficient is nonpositive, and then its optimum is its constant
part. Exactly the same affine upper bounds hold on the closed halfspace.

But the finite CPWA term
`min(max(|x|,|y|), max(1-x,0))` vanishes precisely on Q and equals one
at (0,1). The full query language distinguishes the sources. An ordinary
comparator that keeps the same disjunctions can do so as well; restricting
it to affine probes or independent intervals would be an unequal comparison.

### Why a finite numerical withdrawal penalty exists

For a fixed native query f<=b, its max–min normal form has a finite dual
certificate in every source case and every minimum clause. Replace each
row `a_r*x<=theta_r` by the unconditional inequality
`a_r*x<=theta_r+(a_r*x-theta_r)_+`. Nonnegative dual weights then bound
the clause by its old budget plus a weighted sum of violations. Increase
the finite gains to a common K and constants to b. This gives
`f<=b+K*V_h` **everywhere** for each case h. Only after those proofs are
unconditional may their minimum produce `f<=b+K*min_h V_h`.

This avoids mixing a minimum of bounds that each hold only on a different
hidden case. It also keeps signed b: moving a constant between an expression
and the external budget uses an explicit constant comparison, not a rewrite
that silently changes a parent's budget.

The least gain can be found by splitting f-b and V_C into common affine
cells. On each cell, Farkas multipliers impose linear equalities and
inequalities in those multipliers and K. Their finite rational feasible
system has a closed projection onto K>=0 and a rational minimum. A ratio
need not attain its supremum: `(x-1)_+/x_+` approaches one as x grows,
but never equals one where x>1. The least coefficient K=1 nevertheless
exists and gives the valid source-free inequality `(x-1)_+<=x_+`.

Given a current checked bound `sigma(V_C)<=epsilon`, this penalty transfers
the old request at budget `b+K*epsilon`. A nonempty source cannot validly
give a negative epsilon for the nonnegative violation term. The least
global K does not ensure the sharpest result for one revised source:
with old x<=0 and f=(x-1)_+, K=1; new x<=1/2 yields transferred bound 1/2
while fresh reasoning gives zero. No query-independent error tolerance is
possible for the unnormalized language, since scaling the query by any
positive M scales the required correction by M.

## 11. Geometry and shared-source composition

### Distance dual and the source of the sensitivity factor

Fix one nonempty polyhedron `P={y:A*y<=theta}` and a numerical coordinate
gauge. Its L1 distance from x is the optimum of

\[
 \min_{y,z}\sum_i z_i:quad Ay\le\theta,
 \quad y-z\le x,\quad-y-z\le-x.
\]

The last two constraints already imply z_i>=|y_i-x_i|. Lagrange coefficient
balance gives nonnegative multipliers lambda,mu,nu with
`A^T lambda+mu-nu=0` and `mu+nu=1`. Eliminating mu,nu gives

\[
 d(x,P)=\max_{\lambda\ge0,\ \|A^\top\lambda\|_\infty\le1}
              \lambda^\top(Ax-\theta).
\]

The dual can be unbounded as a set. Its recession directions r satisfy
`r>=0,A^T r=0`; feasibility of P gives `r^T theta>=0`, so such directions
cannot increase this objective. A vertex optimizer exists by the finite
standard-form argument, and finitely many rational vertices give an exact
CPWA distance formula. It does not assume bounded P or primal vertices.

Let H be the largest sum of coordinates of a dual vertex. Each row residual
is at most the maximum positive violation V, so d<=H*V. With finitely many
source cases, use their maximum H and the minimum of their violations to
bound distance to the union. For an L-Lipschitz paired query with old bound
b, a closest point yields `f(x)<=b+L*d(x,P)<=b+L*H*V(x)`.

The one-matrix H is sharp over freely varying feasible right-hand sides.
For a maximizing vertex lambda*, its positive-support rows are independent:
a supported null direction would permit two opposite feasible perturbations
of that vertex. On this support solve the distance problem to `A_S*y<=-1`.
Its optimum is H. Negate a rational minimizing y to obtain delta with
`A_S*delta>=1` and `||delta||_1=H`. Equality in the dual bound forces every
positive-support residual to be one. Put theta=0 on S and
`theta_r=max(0,A_r*delta)` elsewhere. The origin is feasible, V(delta)=1,
and both the dual and the origin show distance H. No smaller coefficient
works uniformly for that matrix's admitted RHS family.

For rows `x<=0` and `-x+e*y<=0`, e>0 rational, the dual vertex
`(1+1/e,1/e)` gives H=1+2/e. At `(x,y)=(1,2/e)`, both violations are one
and the nearest source point in L1 is the origin, at distance H. The query
f=x+y has Lipschitz factor one. Relaxing both bounds to R>=0 gives the
exact attained bound `(1+2/e)R`, at `(R,2R/e)`. For e=R=1/100, the loss
can be 201/100. Small row violations alone do not mean small loss change.

At e=0 the old source instead has x=0 and y free. Distance has coefficient
one, while x+y is unbounded. Taking the supremum of the multiplier sum over
the entire unbounded dual would wrongly give infinity for the distance
constant. Changing the row direction also lies outside fixed-matrix replay.

Coordinate sensitivities can avoid extra slack. With envelope
`|f(x)-f(y)|<=sum_i L_i*|x_i-y_i|`, use the weighted distance dual
`lambda>=0, |(A^T lambda)_i|<=L_i`. Zero L_i are allowed, but its distance
is then a seminorm distance and no longer characterizes the whole source
by its zero set. The query is independent of those zero-weight coordinates,
which is exactly why its particular transfer remains sound.

### Faulty arguments and faulty shared sources are different models

For n proofs of the same current difference d, with bounds sorted as b_(i),
an assumption that at most k<n **arguments** are inapplicable implies
`d<=b_(k+1)`: among the first k+1 arguments at least one must apply. The
bound is sharp under only that assumption by taking d=b_(k+1) and making
only the arguments with smaller bounds inapplicable.

Now suppose the actual fault allowance concerns **source identities**.
Let proof i depend on support S_i. For an allowed faulty-source set F, the
strongest surviving stored bound is

\[
 B(F)=\min_{i:S_i\cap F=\varnothing}b_i.
\]

When every allowed F has a survivor, the common family bound is max_F B(F).
If one F has no survivor, the stored family is unavailable there; neither
unboundedness nor falsity of d follows. Three proofs with supports
`{a},{a},{b}` and bounds `(0,0,1)` illustrate the distinction. One faulty
source a invalidates both zero-bound proofs. d=1 is permitted, so the median
zero is false, whereas the source-aware bound one is correct and attained.

This also exposes construction cost. At a proposed threshold tau, consider
only stored proofs with b_i<=tau. Surviving at most k arbitrary source faults
means that **no** set of at most k source identities intersects all those
supports. The receiving operation can check a particular selected proof
cheaply while selecting/retaining a robust collection involves this separate
combinatorial problem. Duplicating a proof with the same support changes
neither the condition nor the evidence.

All these proofs concern one fixed claim and interpretation. They do not
let a deployed policy observe the unknown fault set, assign independent
probabilities to reused sources, or validate an asserted fault budget.
The existing source-dependence and all-case rules preserve those distinctions.

## 12. Canonical traces, simultaneous inference and coherent empirical repair

The sampling extension is an application of an established empirical-CDF
bound. Its nontrivial information condition is worth reconstructing separately
from the probability theorem. Under exact unit-price old means, every compatible
law can be written as fixed residues rho_w plus a common per-level remainder.
For two subsets S and P_r of size r, the remainder contributes the same
`sum_h f_r(h) z_h` to both failure moments. Therefore

    m_S-m_(P_r)=sum_(w contains S)rho_w-sum_(w contains P_r)rho_w=kappa_S.

The offset is determined by the exact old summary, even if the true law is
not exchangeable. It is not a newly observed statistic or permission to read
the discarded law. Computing all requested offsets still requires reading
the retained contrasts and doing their subset sums.

Fix the canonical chain before new requests. On one request, run it until
success or k-1 failures and record J, the initial-failure count capped at k-1.
Then `1{J>=r}` is exactly the observed event that its first r procedures all
failed. Outcomes after the first success are unnecessary. Independence is
assumed **across requests**, while arbitrary dependence among procedures within
one request is retained by its Boolean world. A changed population or an
adaptively changing chain need not yield identically distributed J values.

The empirical tail estimate of the canonical event, plus kappa_S, has error
equal to the canonical empirical-tail error. Thus a single uniform empirical
CDF event controls every proper subset, all orders and all edited indices.
There is no exponential union bound because the remaining statistical
uncertainty is the same nested threshold family. The established fixed-n
DKW–Massart result supplies probability at least `1-2 exp(-2n eta^2)` for the
uniform error eta. It does not certify the old summary itself.

For one price edit the error is epsilon times the appropriate moment error.
For several edits, expand the fixed-world stopped cost as a linear function
of attempt prices and apply the triangle inequality. Any selected edit vector
with total absolute magnitude at most E has error at most E eta on that same
event. The parameter choices may be made after observing the new data because
the event already controls every allowed query. At receipt the chosen prices
are concrete coefficients; treating both prices and moments as unconstrained
object-language variables would be a different, bilinear fragment.

For E=1/10, tau=1/200 and delta=1/20, eta=1/20 and

    n >= log(40)/(2*(1/20)^2)=200 log(40),

so n=738 suffices. The sampling statement counts requests. The worst-case
procedure executions are 738(k-1), and the old retained source still has
exponential information dimension. The bound is not dimension-free learning
of an unrestricted joint law, a performed empirical calibration, or a
demonstrated advantage over an ordinary method using the same chain.

If the old mean and offsets have already justified simultaneous errors b
and a, respectively, the price-edit error becomes `b+E(a+eta)` on the joint
good event. Obtaining those old guarantees may be difficult or ill-conditioned.
A bound on a few original rows is not automatically a bound a on every derived
offset. Independent old and new data are one way to justify a conditional
new-sample guarantee, but a union bound for separately established events does
not itself require independence. What matters is that their actual scopes
cover the data-dependent construction being used.

### Source admission and what an accepted statistical result says

Intersect the old exact probability-law source with the canonical reach
intervals. On the simultaneous event the true law lies in the intersection.
For rational observations, parameters and interval endpoints, this is a
rational polytope. Nonemptiness must be checked and a feasible witness supplied;
an empty fitted source is a refusal, not a vacuous context. A real feasible
point in a nonempty rational polytope implies a rational feasible point, but
an irrational exact old summary is not thereby turned into rational input.
It needs justified rational enclosures or a separately declared rational-data
scope.

Every currently received inequality valid throughout that same source holds
on the good event, even if the action, budget or whether to accept is selected
after seeing the sample. The conclusion is about a population mean. It is not
a guarantee for each realized request, a conditional-on-acceptance delta
bound, or a guarantee for an optional stopping rule justified only by this
fixed-n concentration statement.

### Why a new coherent decoder does not silently repair every statistical output

The general F16 coherent-center theorem applies to the **full exact old-summary
fiber**. Intersecting it with additional empirical intervals changes that
geometry. Membership of a selected law in the fitted source alone does not
give each empirical midpoint's smaller individual error guarantee.

A simple safe consequence remains available. If every source law has proper
moments within eta of the same offset-adjusted empirical vector, then any
selected compatible law differs from the true law by at most 2eta in each
proper moment on the good event. It gives error at most 2E eta for separate
single-price edits of magnitude at most E. This is an elementary conservative
bound, not an optimality theorem. Tighter coherent centers can be obtained
by an ordinary optimization over that current source.

For k=3,M>0, the planar proof is stronger: any additional **convex** law
restrictions preserve the compact convex (u,v) image, so proper coordinate
midpoints still have one compatible realization. Their widths can be smaller
than the original A1 width. The original globally sharp A1 formula need not
remain sharp on a restricted source. For k>=4 the extra-source triangle in
the new F16 derivation gives a real coherence gap. It does not assert that
that exact triangle is always generated by A3's interval-only sampling scheme.

These distinctions are relevant to a later empirical repair study, but no
new sampling study or revised F15 endpoint was executed in this review.

## 13. Coherence correction and the optional general proof

F16-R01 arose by expressing the exact k=3 old fiber in common singleton/pair
shifts and applying the compact planar bounding-box lemma. Two separate
reviewers confirmed that proof, including arbitrary nonexchangeable offsets.
The affected old §10 warning was corrected transparently; the frozen protocol
never promised that its output vector was a law, and its broader source/query
settings make its generic warning still appropriate. None of its registered
files, thresholds, hypotheses or result bytes was changed.

The subsequent general proof is saved in
`v2/derivations/10_f16_coherent_recovery.md`. I independently checked the proposed
lower comparison, including its convexity identity, monotonicity reduction,
branch threshold and all polynomial cases. I supplied explicit proofs of
the two envelope steps flagged by the initial delegate. Separate upper/lower
reviewers then derived those steps again and found no defect; their requested
scope clarifications were incorporated. The 735 bounded candidate checks and
the 1,439-record exact verification were supporting finite evidence, not the
source of its universal quantifier.

The endpoint/adjacent mixture shows that the largest conditional proper-moment
width is the singleton width and that a compatible law attains the common
radius. This yields the scalar global singleton formula and its monotone
adjacent-difference maximizer. It does not require every proper coordinate
midpoint to be feasible for k>=4. I also derived a rational triangle source
within the k=4 reset model: extra convex information makes the free radius
1/400 and the radius with an output constrained to that source 1/300.
A separate proof check verified the three laws, the common old mean and the
realization by one edited procedure.

The decoded law remains a prediction object with a proved error contract.
Treating it as known source truth would erase uncertainty. This is unrelated
to whether the original neural networks causally use a utility representation.

## Reconstruction coverage and process corrections

Review correction record: the separate core reviewer identified the need
to make the acceptance-event condition, fixed-variable versus uniform L1
distinction, and matching old objective explicit in §§7–8. These conditions
were clarified during F16 before acceptance. They correct the principal's
new explanatory wording, not the frozen theorems or scientific data. The
signed check is retained under `reviews/core/principal_notes_check.md`.

The planned reconstruction targets above are now covered: completeness and
its producer boundary, revision/withdrawal/substitution, self-assessment and
applicability, price-family retention and approximation, and the strong
ordinary combined control. The principal adversarial report assigns explicit
objection dispositions and a separate contribution finding. Final timing and
task acceptance remain pending until the protected floors and handoff are
verified; these notes do not grant a later gate pass.

## 14. Sharpness does not imply a uniformly large practical gain

Fresh principal deduction after the envelope audits: the global formula has
D_1 -> (k-1)/k as M -> infinity at fixed k, by taking the limit of its finite
maximum. At fixed M and k -> infinity, use j=k-ceil(sqrt(k)). The first term
j/k tends to one and the second term j/[(k-j+1)(k+M-1)] tends to zero;
D_1<=1 supplies the reverse bound. Thus the sharp radius can approach the
ordinary universal |epsilon|/2 bound. This is an analytic consequence, with no
additional finite search or experiment.

For k=3,M=4 the two interior values are 5/18 and 1/2. Hence D_1=1/2,
and |epsilon|=1/40 gives radius 1/160. The ordinary bound 1/80 also meets
the frozen numeric tolerance 1/20; the generic pairwise decision bound
|epsilon|=1/40 meets the frozen regret tolerance 1/20. Specialized sharpness
is informative mathematics but this frozen small-edit arm does not discriminate
it through a new threshold pass. No performance, learned representation or
worldwide-priority disposition changes.

## 15. Explicit equally informed compatible-center solver

Let P be the nonempty compact polytope of laws under the actual available
source, including normalization and every current authorized row. Let C_i p
be the demanded finite family of means. Compute L_i=min_P C_i p and
U_i=max_P C_i p by exact ordinary LPs. For an unrestricted answer vector z,

    sup_(p in P) max_i |C_i p-z_i|
      = max_i max(U_i-z_i, z_i-L_i).

Both directions follow by bounding every component and then taking each
attained endpoint in turn; no independence of the coordinates is assumed.
Hence r_free=max_i(U_i-L_i)/2. Requiring one compatible law q changes the
problem to the exact LP

    minimize r over q in P, r>=0,
    subject to U_i-C_i q <= r and C_i q-L_i <= r for every i.

This gives r_compatible>=r_free. Any q in P gives error at most
max_i(U_i-L_i)=2r_free, including the zero-radius case, so the generic
compatible-center ratio is bounded by two. F16-C1 proves equality at factor
one for its full old-summary fiber, while its augmented-source triangle has
factor four-thirds. Generic convexity alone cannot provide C1's equality.
The preceding LP formulation is established optimal-recovery methodology;
the special family construction and evaluated constant are the local delta.

The ordinary method may retain the same five-dimensional old information in
F15, reuse the same exact source fiber, calculate same-law pairwise regret,
compile the same native derivations, and use the same current-request receiver.
The scalar interval relaxation intentionally discards dependencies; it is not
the strongest ordinary method. Counts of linear measurements concern the
specified open source domain, not arbitrary coding, bits, costs or runtime.
For finite unions and general signed piecewise-affine expressions the ordinary
route branches over the same live cases and expression cells, with unit
eligibility imposed identically. No finite-resource completeness or cheap
proof-construction conclusion is inferred.

This explicit reduction defeats an exclusive inference-power or general-method
claim. It leaves a bounded, checked application contribution if the specialized
rank, repair, sharpness and compatible-decoder consequences remain substantive
relative to the named comparisons. The six-field disposition in the principal
report ties support to those consequences, not to an absent external match.

## 16. Closing boundary analysis and disposition

The final protected derivation examined uncertain old observations and the
output-law constraint in [source_uncertainty_boundary.md](source_uncertainty_boundary.md).
The separate [hand audit](reviews/core/source_uncertainty_boundary_audit.md)
checked the complete construction, found and resolved the draft's missing
closedness qualification, and checked the tight two-point ceiling. Derivation10
also records the exact nested-source P subset Q example: compatible radius
increases 1/400 to 1/300 while the free radius is unchanged, because the output
contract shrinks too. These are proof calculations outside the earlier finite
attempt, with no fresh population or experiment.

All earlier 'next', 'pending' and provisional-review sentences in these
chronological reconstruction notes describe their writing-stage status. They
are resolved by the principal review and its linked final audits. The protected
research clock closed at 2026-10-05T23:53:18.425936+00:00: D67.483485 and
Research90.249178 minutes, after conservative report/administration transfers
to O. No concurrent reviewer time is counted. Final accounting and Git handling
are separate overhead, with the exact cut-off and final handoff in the work log.
