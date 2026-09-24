# F03 continuation — belief penalties, KL, and task value

Research date: September 23, 2026. Published source revision:
`3b5846099ad0ffb6194a5a259b3a0f369d9a9fee`; the saved S3 value-bridge
package is a cumulative prerequisite of this continuation. F03 remains an
external-source audit, not a selected calculus. The author's proposed connection
between belief functionals and multi-term losses is treated as a useful lead,
not an assumption that every belief or value must be a KL divergence.

## 1. Source checks and attribution boundaries

**S14 — davidad, “Imprecise beliefs: a tiny introduction” (July 29, 2026).**
The requested [post](https://www.greaterwrong.com/posts/e7Pd4Q9TF7jFdmPgz/imprecise-beliefs-a-tiny-introduction)
defines beliefs using lower-semicontinuous inconsistency functionals on
probability distributions, combines beliefs additively, and distinguishes its
Bayesian subcase from the larger class. The discussion with Oliver Richardson
also distinguishes observational penalties from structural terms and records
that some PDG parameter regimes permit negative scores. These are the author's
proposals and subsequent discussion, not a metatheorem imported here.
**Inspection limitation:** the accessible post and LessWrong mirror omitted
most displayed formulas during extraction. No exact formula numbering or broad
subcategory theorem is certified from that incomplete rendering. Sections 2–4
below are explicitly reconstructed finite models, with KL orientation checked
against S15/S16's legible primary equations. The comment discussion about lost
provenance motivates section 7, but is not its proof.

**S15 — Oliver E. Richardson, “Loss as the Inconsistency of a Probabilistic
Dependency Graph: Choose Your Model, Not Your Loss Function” (AISTATS 2022,
PMLR 151:2706–2735).** Inspected the [publisher PDF](https://proceedings.mlr.press/v151/richardson22b/richardson22b.pdf),
§2 equation (1), §3 Propositions 2–5, §4 Proposition 8, and §5 Proposition 9
and Lemma 10; PDF pages 1–4 (zero-based), printed pp.2707–2710, were visually
checked. Observational incompatibility is a weighted conditional-KL functional;
inconsistency is its infimum over compatible joint distributions. These are
different quantities. The source derives log-loss, cross-entropy and regularizer
relationships under explicit fixed-data/confidence assumptions. We use those
interfaces, not a universal theorem that pragmatics uniquely selects a loss.
The general structural score can require a separate sign/parameter audit.
The parsed Appendix C proofs of Propositions 2–5 and Lemma 10 (PDF indices
13–14 and 20–21) were also inspected. The conditioning proof continuing on
PDF index 16 was visually checked. Screenshots of indices 13, 20 and 21 failed;
no visual verification of those pages is claimed. The usable pooled-KL case
requires positive weights and a nonzero normalizer; our statement keeps both.

**S16 — Richardson et al., “Local Inconsistency Resolution: The Interplay
between Attention and Control in Probabilistic Models”, arXiv:2604.17140v1
(April 18, 2026).** Inspected [§§2–3](https://arxiv.org/html/2604.17140v1),
equations (1)–(4), Definition 1 and Proposition 1. Equation (1) writes each
conditional penalty as a joint KL against a candidate marginal times a supplied
conditional. Attention weights and control over parameters are separate;
reducing a locally visible inconsistency is not stated as guaranteed global
success. We use the observational, nonnegative-confidence interface, not all
signed structural regimes, all dynamical claims, or the experimental results.
This matters when a distribution represents an external-world hypothesis rather
than an outcome law the agent can choose.

**S17 — Ouyang et al., “Training language models to follow instructions with
human feedback”, arXiv:2203.02155v1 (2022).** Inspected [§3.5, equation (2)](https://arxiv.org/html/2203.02155v1)
and its PPO/PPO-ptx explanation. The specific PPO-ptx objective combines a reward,
a policy-to-reference log-ratio penalty, and an expected pretraining log
likelihood. The expectation of the on-policy log ratio is a conditional KL.
This is a concrete example supporting the author's intuition about multiple
objective terms, not a claim about every present-day post-training recipe.
A single sampled log ratio need not be nonnegative; its expected KL is.

**S18 — Rafailov et al., “Direct Preference Optimization: Your Language Model
is Secretly a Reward Model”, arXiv:2305.18290v3 (July 29, 2024; originally submitted May 29, 2023).** Inspected
[§§3–4 and Appendix A.1](https://arxiv.org/html/2305.18290v3), especially equations
(3)–(5) and (11)–(15). The reference-weighted exponential optimum supplies a
useful finite adapter between a reward and a KL-regularized objective. The
optimizer uses the full nonparametric policy class, appropriate support, and a
finite partition function. The displayed max/min chain is an optimizer
re-expression, not preservation of optimum numerical values after dropping a
negative factor; section 5 below retains the exact value identity. No DPO
training algorithm or convergence claim is imported.

These five checks answer the new author-supplied lead. The eight original core
sources and five earlier supplements remain in the source manifest. All new
sources are targeted supplements, not five full-paper independent reviews.

## 2. A belief functional is an object; a KL value is one evaluation

Fix a nonempty **finite** scenario set X. Its probability simplex Δ(X) is a
mathematical space of candidate models, not direct access to a true distribution.
For this adapter take a belief object to be a lower-semicontinuous function

$$B:\Delta(X)\longrightarrow[0,\infty].$$

A precise-reference example, with p a declared probability law, is

$$B_p(q)=D(q\Vert p)=\sum_{i:q_i>0}q_i\log(q_i/p_i).$$

Use natural logs throughout. A positive q_i with p_i=0 gives infinity;
zero q_i contributes zero. Nonnegativity follows from the log inequality,
and equality holds exactly at q=p. Here p specifies the reference and q is the
candidate being assessed. Neither is an unqualified metaphysical truth.
The fixed-p functional, its value at one q, and its minimum zero are distinct.

General B need not be one KL functional. For a nonempty closed set C of
candidate distributions, the extended indicator I_C is zero on C and infinity
outside. It is lower semicontinuous. A set with two distinct distributions has
two zeros, so its indicator cannot equal D(q||p) for any fixed p. This is a
finite direct witness, not a verification of the post's broader embeddings.

For finitely many such B_j and nonnegative **finite** weights λ_j, define

$$B(q)=\sum_{j:\lambda_j>0}\lambda_j B_j(q).$$

Writing only positive-weight terms avoids ambiguous zero-times-infinity
bookkeeping. Finite sums of nonnegative lsc functions are lsc; prove this by
applying liminf to each nonnegative summand. On the finite simplex they attain
a minimum, but it may be infinity if there is no common finite point. The
existence of a minimizer is not a proof that the assertions are correct.
Duplicating a finite penalty changes its weight: B+B is generally not B.

For conditional claims K(y|x), the well-defined joint form is

$$B_K(q)=D(q_{XY}\Vert q_XK)
=\sum_{x:q_X(x)>0}q_X(x)D(q_{Y|x}\Vert K_{\cdot|x}).$$

Rows with q_X(x)=0 impose no realized penalty. Requiring correctness at such
unvisited inputs is an additional, different contract. This definition matches
S15's equation (1) and S16's equation (1) at their observational interface.

### 2.1 Combining assertions is not adding their separately optimized scores

Let p=(9/10,1/10), r=(1/10,9/10), and let q range over the binary simplex.
Both individual KL functionals have minimum zero, but their minima occur at
different q. Set Z=Σ_i sqrt(p_i r_i)=3/5 and m_i=sqrt(p_i r_i)/Z=1/2.
Expanding the logs gives the exact identity

$$D(q\Vert p)+D(q\Vert r)=2D(q\Vert m)-2\log(3/5).$$

Thus the minimum of their sum is -2 log(3/5), approximately 1.02165 nats,
not the sum of their minima. The shared candidate q is indispensable.
More generally, with positive finite a,b, s=a+b and overlapping positive
support, put Z=Σ_i p_i^(a/s) r_i^(b/s) and m_i=p_i^(a/s)r_i^(b/s)/Z.
Then aD(q||p)+bD(q||r)=sD(q||m)-s log Z. This is the finite specialization
of S15 Lemma 10, not a new claimed representation theorem.

### 2.2 Matching marginal beliefs does not assert independence

For two finite variables and fixed positive references p_X,p_Y, the lifted
marginal sum B(q)=D(q_X||p_X)+D(q_Y||p_Y) leaves the coupling open. Directly
splitting the log ratio gives

$$D(q_{XY}\Vert p_Xp_Y)=B(q)+I_q(X;Y),$$

where I_q(X;Y)=D(q_XY||q_Xq_Y). Zero marginal rows cause no problem because
q_XY is zero there. When both references are fair binary laws and q puts one
half on each of (0,0) and (1,1), B(q)=0 but I_q(X;Y)=log2. Under the product
law both are zero. Marginal fit cannot silently be replaced with a joint-product
claim. This is a concrete connection to F01's dependence examples.

Independence itself gives a nonnegative continuous belief penalty on a finite
simplex: I_q=H(q_X)+H(q_Y)-H(q_XY), with 0log0 extended by zero. It is not
convex: both point masses δ_(0,0) and δ_(1,1) have penalty zero, but their
midpoint has penalty log2. Thus even a smooth-looking information-theoretic
belief object need not be a fixed-reference KL or a convex function of q.
This is a finite reconstruction of the blog's independence example and the
PDG structural-entropy interface, not a claim about all parameter regimes.

### 2.3 Belief strength is not the desirability of a candidate

There are two distinct comparisons. A stronger constraint can assign a greater
inconsistency penalty to every candidate: write B ⊒ C when B(q)≥C(q) for all q.
Then for every finite tolerance τ, {q:B(q)≤τ} is a subset of {q:C(q)≤τ}.
Adding a nonnegative assertion strengthens this order. By contrast, when B is
fixed, a candidate q with a *smaller* B(q) fits it better. The post's reverse
numeric order for implication should not be silently treated as the ordinary
larger-is-better ordering of utilities on candidates.

For precise positive-reference KL beliefs, B_p ⊒ B_r already forces p=r:
evaluate the inequality at q=p to get 0≥D(p||r)≥0. This reconstructs the
finite content of the post's statement that distinct normalized Bayesian
beliefs have no nontrivial pointwise implication. Additional functional
structure, rather than merely the shared range, enables imprecise beliefs.

Penalties measured in nats require an explicit coefficient with units of
cost per nat before addition to a task cost. A change from natural to base-two
logs rescales that coefficient. This is a requirement on this proposed adapter,
not a privileged physical or metaphysical unit of value.

## 3. Bayesian updating retains an evidence offset

For an event E with p(E)>0, let p_E be p conditioned on E. On the whole simplex,
using extended values where necessary,

$$D(q\Vert p)+I_{\{q:q(E)=1\}}(q)
=D(q\Vert p_E)-\log p(E).$$

On E, substitute p_E(i)=p_i/p(E) into the log sum; off E, both sides are
infinity. This includes q concentrated on an originally zero-probability point:
both sides remain infinity. The minimum is -log p(E), attained at p_E.
An impossible event p(E)=0 yields an identically infinite left-hand side, not a
normalized posterior. No subtraction of infinity is performed.

The nonnegative evidence offset can affect later model comparisons although
it does not affect this one posterior argmin. For example p=(1/2,1/2) and
r=(1/4,3/4) both condition on E={first outcome} to the same point mass,
yet their offsets are log 2 and log 4. Retaining only the posterior loses this
distinction. This finite derivation supports the post's normalization concern
without claiming its general categorical update theorem.

For a likelihood ℓ_i∈[0,1] with Z=Σ_i p_iℓ_i>0, define L_i=-log ℓ_i.
On positive support, the corresponding identity is

$$D(q\Vert p)+\mathbb E_q L
=D(q\Vert p\ell/Z)-\log Z.$$

Zero likelihood is handled as an impossible outcome for q, not by computing
0 times infinity naively. A continuous probability **density** can exceed one;
its negative log need not be nonnegative. The finite probability/likelihood
scope is part of this bridge to RLL's nonnegative range.

## 4. What the multi-term training example actually supports

For a fixed empirical target law d and candidate predictor p_θ,

$$H(d,p_\theta)=H(d)+D(d\Vert p_\theta).$$

Subtract the entropy definition from cross-entropy to obtain the identity.
Only when d and its scope/weighting are held fixed is H(d) ignorable for
optimizing θ. This is the finite content of S15 Propositions 3 and 5.
It does not say that predicting text establishes the truth of that text.
Nor is KL interchangeable with cross-entropy when the first argument is being
optimized: for p=(1/2,1/2), H(q,p)=log2 for every q, whereas D(q||p) has a
unique minimum at p. This counterexample fixes a common argument-order error.

A finite version of S17's objective, written as a minimized loss, is

$$J(\pi)=-\mathbb E_{x\sim\rho,y\sim\pi}r(x,y)
+\beta\mathbb E_{x\sim\rho}D(\pi(\cdot|x)\Vert\pi_0(\cdot|x))
+\gamma H(d,\pi),$$

where ρ is the declared prompt law, π_0 the fixed reference policy, and d the
separate pretraining-sequence law. The last two terms may live on different
sample spaces before being evaluated; a common symbol π refers to the same
parameterized model, not identical integration measures. The KL expectations
and the data-fitting term require their own supports and weights.

This illustrates a wider **proposed** value objective: a sum of epistemic-fit,
task-performance and resource terms, with declared scales. Epistemic fit can be
one contribution rather than the entire value. It does not follow that every
value must admit this decomposition, that the weights are known, or that the
negative of a training loss already provides a sound operational calculus.

For a sequence of fixed finite length, the joint KL has the conditional chain
rule, weighted by prefixes from its **first** argument. This gives an additive
per-token interpretation only with the same sequence law and information
schedule. Uniformly averaging conditional terms over unrelated prefixes is a
different quantity. A sampled log ratio may be negative even though its full
on-policy expectation is nonnegative.

### 4.1 A primary source already gives a cost-to-belief construction

S15 section9, Proposition15 and AppendixC.1.3 explicitly encode a nonnegative
cost c(x) by a binary auxiliary variable T with K(T=1|x)=exp(-c(x)). Fix the
input law p and require T=1. The remaining conditional-KL penalty is

$$\sum_xp_xD(\delta_1\Vert K(\cdot|x))
=\sum_xp_x[-\log e^{-c(x)}]=\mathbb E_p c.$$

Finite c suffices for this identity; +infinity can encode an impossible success
outcome with the usual support convention. In the source, fixing p is an
infinite-confidence constraint. Replacing that constraint with the finite
penalty D(q||p) lets q tilt and changes the result to -log E_p exp(-c).
Its AppendixC.1.3 derives this change; it is not merely a qualitative warning.

This is a representability bridge, not evidence that the artificial success
observation is an independently justified belief. Source section9 itself
questions the modeling choices. For finite signed costs on a finite support,
subtracting a lower bound permits the same encoding; the discarded offset must
be retained for absolute comparisons. No common bound across every future
value is required. Parsed section9 and the AppendixC.1.3 argument were checked;
screenshots of their PDF pages8 and28 failed, so their diagrams are not used.

## 5. A constructive bridge to continuation values

Let β>0, p a finite probability law, and f a finite real cost on its support.
No universal magnitude bound is imposed across tasks. Set

$$Z_f=\sum_i p_i e^{-f_i/\beta},\qquad
q_f(i)=p_i e^{-f_i/\beta}/Z_f.$$

On p's support, expanding log(q_i/q_f(i)) proves

$$\beta D(q\Vert p)+\mathbb E_q f
=\beta D(q\Vert q_f)-\beta\log Z_f.$$

Outside that support the KL penalty is infinite; finite costs cannot offset it.
Consequently the minimum over q is -β log Z_f, attained uniquely by q_f.
S15 Appendix C.1.3 gives the unit-coefficient cost case, and
S18 Appendix A.1 gives the reward-sign version; this proof keeps the value
constant and support assumptions explicit. A restricted policy family might
not contain q_f and need not attain this optimum.

Define T_p^-(f)=-β log E_p exp(-f/β). It is monotone and preserves common
shifts: T_p^-(f+c)=T_p^-(f)+c. Monotonicity and these identities imply
|T_p^-(f)-T_p^-(g)|≤||f-g||∞. Thus KL regularization supplies a concrete
nonlinear instance of F02's monotone shift-preserving transformer interface.
It is concave in f, as an infimum of affine functions of f, and is not normally
linear. This is a scoped connection, not a choice of the permanent T calculus.

Minimizing over an **external-world candidate** q selects a favorable tilted
model. It is not a robust guarantee about that world. The different worst-case
penalized cost is

$$T_p^+(f)=\sup_q\{\mathbb E_q f-\beta D(q\Vert p)\}
=\beta\log\mathbb E_p e^{f/\beta}.$$

For p=(1/2,1/2), β=1 and f=(0,log3), these give log(3/2) and log2,
respectively. The first optimizer is (3/4,1/4), the second (1/4,3/4).
The signs and who controls q determine different decisions even though both
use the same KL and the same nonnegative penalty range.

### 5.1 Signed, unbounded values require no single global shift

Each finite signed f works in the formula above. Adding any finite constant c
changes T by c and leaves q_f unchanged. There is no need to shift every
possible future task into one fixed positive interval.

On a countably infinite space, however, individual integrability is weaker than
the exponential-moment premise. Take p_n=2^-n and reward r_n=β n log2,
n≥1. Its mean is finite, but Σ_n p_n exp(r_n/β)=Σ_n1 diverges. The uniform
law on {1,...,N} has reward-minus-KL value β log N, which grows without bound.
This is a concrete scope boundary, not a reason to prohibit unbounded values:
finite-state use or an explicitly finite exponential moment is a constructive
restriction when a finite soft value is requested.

### 5.2 The functional bridge does not require KL in every term

For any proper nonnegative lsc B on the finite simplex (proper means B is
finite somewhere), define the loss transformer

$$T_B(f)=\min_{q\in\Delta(X)}\{B(q)+\mathbb E_q f\},\qquad f\in\mathbb R^X.$$

The objective is lsc on a compact simplex, so the minimum exists. It is finite:
the minimum of f is a lower bound, and any point where B is finite supplies a
finite upper bound. Addition of a constant c to f changes every feasible
objective by c; ordering of f is preserved in every expectation. Therefore
T_B is monotone, shift-preserving and sup-norm nonexpansive. As the infimum of
affine maps of f it is concave. These are proofs for this adapter, not a claim
that every F02 transformer has a belief representation. Importantly,
T_B(0)=min B need not be zero: normalizing B changes every returned value.

This organizes the four candidates without prematurely choosing one. An
*evaluated scalar* S keeps B(q) or T_B(f) for one query. A *profile* P can keep
the jointly indexed map q↦(B(q),E_q f), retaining a common candidate during
aggregation. The map f↦T_B(f) is an explicit T. For a **declared controlled**
set of available laws A⊆Δ(X), an achievable budget image is

$$G=\{(b,\tau):\exists q\in A,\ B(q)\le b,\ \mathbb E_q f\le\tau\}.$$

If q instead indexes uncertain external models, the existential quantifier is
not a policy witness. Universal bounds over {q:B(q)≤b}, an outer policy choice,
or an information-dependent policy require a different specification. Empty
sublevel sets must not be mistaken for an available action. This is the same
existence-versus-guarantee boundary already identified in F01/F02.

## 6. Sharing a range does not transfer every Lawvere rule

### 6.1 KL is not the directed distance from the earlier bridge

Let p=(1,0), q=(1/2,1/2), r=(1/4,3/4). Then

$$D(p\Vert r)=\log4>
D(p\Vert q)+D(q\Vert r)=\log2+\tfrac12\log(4/3).$$

So nonnegativity, asymmetry and range [0,∞] do not make KL a Lawvere distance:
the triangle law fails. Its valid composition interfaces include the chain rule
and contraction under a common channel, not arbitrary intermediate-model
triangles. This does not affect S3's separately proved supremum-of-positive-
value-loss distance, whose triangle follows from ordinary inequalities.

For a common finite stochastic channel K, the joint laws q_i K_ij and p_i K_ij
have KL D(q||p). Marginalizing their output and splitting the log ratio yields
that same KL as D(qK||pK) plus a nonnegative conditional KL. Therefore
D(qK||pK)≤D(q||p). Shared channel and KL direction are essential. This is a
finite source-adapter proof of data processing, not a free theorem for an
arbitrary changed representation or independently chosen channel. A general
relation-based framework such as S10 need not assume a triangle law, but its
own substitution and context conditions would still have to be established.

### 6.2 Lower semicontinuity is not closure under truncated subtraction

Parametrize the binary simplex by t∈[0,1]. Let B(t)=0 at t=0 and B(t)=1
elsewhere, and let C(t)=1 everywhere. Both are nonnegative lsc functionals.
But the pointwise RLL-style residual (C-B)+ equals one at zero and zero at
every positive t. Along t=1/n its liminf is zero, below its value at zero.
It is not lsc. The source post's additive category of beliefs does not thereby
supply an internally closed model of every RLL connective; it does not claim
that stronger closure in the inspected prose.

A positive restricted repair is to use finite **continuous** functionals on a
common finite simplex. They are closed under finite sums, products, min, max,
and truncated subtraction. Fixed strictly positive reference laws make
q↦D(q||p) continuous, since q log q extends continuously by zero. A zero
reference entry requires a support-face restriction for this repair. The
statement concerns this finite connective fragment, not division at zero,
actual infinity constants, or a full inherited completeness theorem.

### 6.3 Logarithmic content is not already polynomial deduction

Once a nonnegative KL penalty has been evaluated or bounded, its numerical
allowance may enter the nonnegative arithmetic bridge. Deriving that bound
from probabilities still involves logs and support conditions. S12's polynomial
completeness theorem is not a completeness theorem for those additional
logarithmic constraints, contextual probability variables, or policy witnesses.
Sound arithmetic on supplied bounds is useful without claiming that transfer.

## 7. What aggregation preserves and what it forgets

A sum of labeled penalties can be a useful value object, but retaining only its
unlabeled total can obstruct revision. The decompositions (B,0) and (0,B)
have the same sum; removing the first source leaves zero in the first case
and B in the second. This proves why source identity may matter to a revision
query even when totals suffice for current evaluation. Duplicate reports also
change weights; algebraic addition alone does not establish independent evidence.

There is a further finite non-identifiability. For p positive, β>0, and a finite
function h, put p'_i=p_i exp(h_i/β)/Z_h and f'_i=f_i+h_i. Direct expansion gives

$$\beta D(q\Vert p')+\mathbb E_q f'
=\beta D(q\Vert p)+\mathbb E_q f+\beta\log Z_h.$$

All q comparisons and minimizers are the same, although the belief reference
and cost term have changed. For f=(0,log3), p uniform and β=1, choosing h=-f
absorbs the cost into p'=(3/4,1/4). The new cost is zero and the old objective
is D(q||p')+log(3/2). This is a concrete limited belief/value reallocation,
not unique extraction of an agent's true beliefs or values. Preserving absolute
allowances additionally requires retaining the additive offset.

## 8. Disposition for F03 and later work

The author's intuition has a useful precise form: nonnegative epistemic
inconsistency penalties can participate in a broader value objective, and a
finite KL-regularized version yields a nonlinear continuation-value transformer.
The four earlier candidate representations remain alternatives. No universal
KL primitive, probabilistic semantics, decision rule or additional permanent
axiom is adopted.

The most consequential import checks are: fixed versus controlled probability
arguments; support and normalization; label-preserving aggregation; soft
optimistic evaluation versus robust guarantee; and closure of the selected
function space under the actual connective. The RLL and KL occurrences of
[0,∞] are a conceptual bridge, not by themselves an equivalence of calculi.

Source cards, the bibliography, the finite checks and the session record keep
literature inspection, independent adapter derivation and computation separate.
No F04 work, readiness-gate pass, complete theorem prover or novelty claim is
introduced. Task completion still depends on F03's recorded L60 and evidence
requirements, not this note's length or the number of passing fixtures.


## S5 source-audit correction (September 24, 2026)

[The next audit](01e_belief_value_import_contracts.md), section 4, gives a finite
counterexample to S16 Proposition 1's parameter-convexity statement as written
in arXiv v1, and a constructive joint-convexity repair. The observational KL
definitions used here survive. This correction does not retract the earlier
penalty-to-continuation result: its concavity is in the continuation cost f,
not convexity in a learned model parameter. The old inspection record remains
historical; the source manifest now marks the rejected import explicitly.
