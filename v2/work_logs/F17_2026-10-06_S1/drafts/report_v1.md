# Value Logic: Loss Comparisons and Information Retention Under Revision

Tristan Miano

Research report, October 2026. Assembly and current internal review:
**ChatGPT (GPT-6 Astra Pro)**. Detailed attribution appears in the final section.

## Abstract

We study how a reasoner can compare the practical value of fallible
models while keeping the assumptions and information needed for later
revision. The working semantics assigns finite signed loss expressions
to a shared uncertain source. A small rational piecewise-affine calculus
composes loss bounds, supports current-request checking, and has a
constructive completeness theorem for the evidence accessible through
its directed unit conversions.

The main application concerns correlated reset procedures whose
attempt prices change. We evaluate exact retention requirements, show
that a single nonzero price edit can require $k-1$ additional actual
new-order means to repair an old exact summary, and distinguish this
exact fragility from small decision regret. For full exact equal-old-price
summary fibers, we construct one compatible probability law attaining
the unrestricted common minimax error after separately applied
single-price edits.

A frozen revision challenge meets its prospective usefulness criterion
in 68 of 160 episodes; matched ordinary methods reproduce the service,
and general performance superiority is not established. In a separate
ordinary-trained neural probe, all five networks learn the task but
zero meet the complete expected-cost intervention criterion. A later
diagnostic implicates extraction restrictions and capable controls
without establishing a joint causal utility representation. The
contribution is a modest synthesis, formal adaptation and specialized
application, bounded by the declared source contracts and inspected
literature comparisons.

## 1. Introduction

### 1.1 The question

A model can cease to be an adequate unrestricted description and still
serve a bounded task well. Its use may depend on a tolerable error, the
cost of obtaining a more detailed answer, the available fallback, and
the evidence currently supporting those judgments. The motivating
research program treats models and value criteria as revisable, without
assuming that scientific revision must reach a final endpoint. That is
a philosophical motivation for the question, rather than an axiom used
in the mathematical proofs.

The operational question is:

> How can a reasoner represent task-relative value, compose the reasons
> for relying on a model, and preserve the information needed when those
> reasons or the task change?

One scalar score is sometimes sufficient. For other operations it
forgets joint dependence, a relevant error direction or the observation
schedule. The present report therefore begins by comparing semantic
objects, then chooses a finite source-based loss interpretation whose
inferences can be checked exactly. A value expression denotes a
function of modeled quantities; an evaluation answers one query about
that function. Its chosen loss meaning, the source evidence and the
permitted actions remain separate.

This approach connects to established utility-oriented logic,
quantitative reasoning, abstract interpretation and checked program
analysis. The closest practical combination is an ordinary quantitative
model with polyhedral optimization and incrementally checked evidence
([Albert et al.](#ref-acc); [Fouilhé et al.](#ref-polyhedra)).
Our contribution is the particular adaptation and its evaluated
retention/recovery consequences, not the general existence of those
ingredients.

### 1.2 Main results and their significance

The core compares a new modeled loss $t$ with an old loss $s$
through the signed assertion $t-s\le b$ over every retained source
case. Its rules preserve shared dependence, combine improvement and
error budgets, and record how withdrawn assumptions affect a proof.
Theorem 1 establishes soundness when the actual proof conclusion is
checked against the current request. Theorem 2 gives an exact
constructive characterization: native derivability is validity on the
target-unit reduct. It also explains why a directed conversion can
make a semantically relevant premise inaccessible to a proof.

The main mathematical application asks what an old summary of
expected procedure costs preserves after prices change. With arbitrary
correlation among $k$ reset procedures, one complete old numerical
profile has linear rank $2^k-k$. Two nonproportional positive price
profiles recover the full law when at least one terminal penalty is
positive. A single admissible nonzero price edit can consequently
require exactly $k-1$ additional independent linear responses, and
Theorem 4 constructs them as actual new expected costs. This is an
exact-information result: an old-optimal action can still have regret
at most the edit magnitude.

Theorem 5 addresses a different obstacle. Separate interval midpoints
can be mutually incompatible, so a collection of accurate numbers
need not constitute a reusable probability model. For the full exact
equal-old-price family, an explicit mixture of an endpoint law and an
adjacent-level law attains the best common error while remaining
compatible with the old evidence. Generic optimal recovery supplies
the solver framework ([Ettehad–Foucart](#ref-recovery)); the
compatible-radius equality is a further property of this family.
The theorem's adverse source examples show where that property ends.

The resulting distinction is practical: **predicting a cost, choosing
a good action, and justifying the current choice can require different
information**. The scientific example derives a cheaper-rule
replacement from separate source premises, while the staged
self-assessment example chooses between actual bounded proof
procedures. Strong ordinary controls are retained in both cases.
The frozen revision study then tests an explicit useful-derivation
criterion, rather than treating every accepted inequality as a
meaningful success.

The neural probe asks a separate empirical question: whether a
particular expected-cost intervention correspondence can be extracted
from networks trained only on ordinary outcomes. Its negative
complete-support result is part of the report. Ordinary prediction
training gives no special reason for each cost to occupy a clean
eight-neuron block, and the later diagnostic shows that both extraction
choice and control discrimination matter. The mathematical
application does not depend on a positive neural result.

### 1.3 Reading the report

Sections 2–6 develop the semantic choice, rules, proofs and exact
interfaces with Boolean reasoning and the earlier reliance calculus.
Section 7 contains the retention, repair and compatible-recovery
results, with explicit links to the complete technical derivations.
Sections 8–10 give the worked applications, implementation and frozen
findings, including adverse controls. Sections 11–14 state the precise
contribution, open questions, reproducibility contract and attribution.
Definitions, mathematical theorems, empirical findings and motivating
choices are identified separately.

## 2. Choosing what a value expression means

A numerical score answers a particular question about a plan. It need not
retain the information needed for the next question. Suppose a fair binary
variable $X$ is paired either with $Y=X$ or with $Y=1-X$. Both pairs have
the same marginal means. Nevertheless, their expected maxima are $1/2$ and
$1$, respectively. Their expected minima are $1/2$ and $0$. Thus two
evaluated means suffice for an expected sum, but not for these nonlinear
compositions. Repeated observations of one quantity must also remain the same
quantity when an expression is revised.

The preliminary comparison therefore examined four semantic objects, each
with a declared operational fragment.

| Candidate | Object retained | Natural operation | Consequential limitation |
|---|---|---|---|
| Evaluated scalar | A task-relative real value | Addition and an externally chosen mixture | A mean loses dependence needed by nonlinear or sequential questions. |
| Aligned profile | Values on a common set of scenarios | Pointwise arithmetic before evaluation | Its scenarios, alignment and information-access rules must remain explicit. |
| Continuation transformer | A map from later value functions to present values | Composition of transformations | Evaluation can discard information about how a later decision depends on an observation. |
| Guarantee front | The resource/error budgets achievable by permitted plans | Composition of feasible guarantees | A hard requirement, an attainable optimum and a scalar preference are different questions. |

These are different mathematical meanings, not merely different numeral
systems. An arbitrary encoding of an entire profile into one real number,
equipped with a special decoder, is not the ordinary scalar-value algebra
being tested. Conversely, a richer representation receives no credit for
consulting discarded data through an uncharged identifier.

The chosen working core retains shared source coordinates and compares
finite signed loss expressions built from rational continuous
piecewise-affine arithmetic. This fragment permits exact rational checks,
explicit dependence and finite proofs. It also has useful connections to
piecewise-linear networks, but choosing it does not establish that an
ordinarily trained network uses the proposed semantic organization.
Continuation and guarantee semantics remain possible alternatives.

The choice is provisional. Cost is a declared proxy for practical value; an
intended objective and its accessible proxy may themselves be uncertain.
The framework does not identify utility with truth, assume that every
quantity is observable, or prove that this is the unique suitable meaning
of value.

*Detailed selection evidence:* [candidate semantics](v2/foundations/02_candidate_semantics.md),
[candidate reconstruction](v2/foundations/02a_candidate_reconstruction.md),
[separating examples](v2/foundations/01_requirements_and_separating_examples.md),
and [selected core](v2/foundations/03_provisional_core.md).

## 3. A semantics for conditional loss comparisons

### 3.1 Sources, terms and contexts

A finite signature declares source keys, their units, and named directed
conversions with strictly positive rational factors. Two occurrences of the
same source key denote the same unknown quantity. Different program,
population or criterion meanings require distinct identities or an explicit
relation; equality of a display name is insufficient. A revision can tighten
evidence about the same quantity without changing that quantity's identity.

For each unit, terms use rational literals, source coordinates, addition,
rational scaling, minimum, maximum, a residual, nonrecursive lexical
bindings, and the declared conversions. Negative scaling is permitted.
The residual is

$$
\operatorname{res}(a,b)=\max(b-a,0).
$$

A term has a finite real value at every assignment. Its range over possible
assignments can still be unbounded. Variable multiplication, literal
infinities and recursive term bindings are outside this fragment. In
particular, an application parameter fixed when a query is issued is not
silently promoted to a second unknown multiplied by a source variable.

At a fixed visible observation, the context $\mathcal C$ supplies a
nonempty finite family of cases,

$$
D_{\mathcal C}
 =\bigcup_{h\in H}\{(h,x):A_hx\le \eta_h\}.
$$

Every case is a closed rational polyhedron with a supplied rational feasible
witness. Source rows are typed affine inequalities. They may relate several
coordinates and retain correlations that separate intervals would discard.
The witness establishes mathematical nonemptiness; it does not establish
that the modeled source describes deployment. An empty context is rejected
as inconsistent evidence rather than used to warrant every action by
vacuity.

Structural induction evaluates every closed typed term uniquely. The
induction carries a lexical environment: a binding's right side is
evaluated in the old environment before its body receives the new binding.
Refining the finitely many min/max branches shows that the denotation is a
rational continuous piecewise-affine function. An implementation may share
subexpressions, provided its cache respects bindings and source identity.

### 3.2 Signed budgets

Let $t$ denote the new loss and $s$ the old loss, in the same unit $u$.
For a rational budget $b$, define

$$
\mathcal C\models t\le_b s:u
\quad\Longleftrightarrow\quad
\forall(h,x)\in D_{\mathcal C},\quad t_h(x)-s_h(x)\le b.
\tag{1}
$$

The executable fragment uses one literal expression pair across its cases.
A negative budget is a guaranteed modeled improvement, zero is
non-deterioration, and a positive budget allows an increase. Absolute
adequacy is a separate comparison with zero; relative improvement alone
does not supply it.

The best semantic upper bound is the metalevel quantity

$$
B_{\mathcal C}(t,s)
 =\sup_{(h,x)\in D_{\mathcal C}}\bigl(t_h(x)-s_h(x)\bigr)
 \in\mathbb R\cup\{+\infty\}.
\tag{2}
$$

It is not an expression-language primitive or an oracle available to a
proof. A feasible case and assignment with difference greater than $b$
is a countermodel within the declared source. Failure of a bounded search
to find a proof is a different outcome.

Clipping to nonnegative deterioration loses useful information:

$$
\sup_{D_{\mathcal C}}\operatorname{res}(s,t)
 =\max\bigl(B_{\mathcal C}(t,s),0\bigr).
\tag{3}
$$

For $b\ge0$, bounding this shortfall is equivalent to (1). For $b<0$
the equivalence fails. Even a strict improvement has nonnegative shortfall,
so its improvement margin must remain in the signed comparison.

### 3.3 Permitted actions and observations

A loss formula can depend on an unknown source coordinate without making
that coordinate available to a policy. At one visible observation, the
same permitted policy must be used across every compatible hidden case.
The relevant order of quantifiers is

$$
\exists\ \text{permitted policy }\pi\;
\forall\ (h,x)\text{ compatible with the observation}.
\tag{4}
$$

For example, consider two hidden cases in which the costs of two actions
are $(0,2)$ and $(2,0)$. The pointwise minimum is zero. A fixed policy
cannot choose the cheaper action in each case without observing the case;
even its best fixed randomization has worst cost one. Different proof
witnesses in different cases do not change that information constraint.

The semantics accordingly separates an expression, an executable plan,
the loss assigned to that plan, and the observations permitted before
selection. This distinction makes the calculus useful for conditional
reasoning without treating every mathematical minimum as an available
action.

*Definitions and evaluation proof:* [provisional core, §§2–6](v2/foundations/03_provisional_core.md).

## 4. Composing and revising proofs

### 4.1 Native rules

Write $\mathcal C;h\vdash t\le_b s$ for a finite derivation in a named
case. Every premise in a rule refers to the same context and compatible
units unless an explicit conversion is applied. The table groups the
sixteen implemented instruction tags by their mathematical role.

| Role | Rule or condition |
|---|---|
| Constant and source | Prove an exactly normalized constant difference, or use an actual source row with its offset and budget. |
| Exact rewriting | Replace a pair only when its normalized difference is unchanged. |
| Transitivity | From $t\le_b s$ and $s\le_c r$, derive $t\le_{b+c}r$. |
| Addition | From $t_i\le_{b_i}s_i$, derive $t_1+t_2\le_{b_1+b_2}s_1+s_2$. |
| Scaling and conversion | Multiply expressions and budget by a nonnegative rational or the declared positive conversion factor. |
| Polarity reversal | From $t\le_b s$, derive $-s\le_b -t$. |
| Slack | Add only a fixed nonnegative allowance to the budget. |
| Combining proofs | Two proofs of the same difference at $b,c$ give the budget $\min(b,c)$. |
| Lattice rules | Use the min projections, max injections, and common-target min/max comparisons. |
| Min/max congruence | Two component bounds $b,c$ give the bound $\max(b,c)$ for either pointwise min or max. |
| Residual congruence | Reverse the first argument's comparison and clip the summed allowance at zero. |
| All cases | Prove the same literal pair in every live case and take the maximum case budget. |

Addition uses a common assignment before taking a bound; it needs no
independence assumption. If both losses contain the same source term
$z$, exact rewriting can cancel $z$ from their difference even when
$z$ is unbounded. It cannot cancel distinct coordinates merely because
they happen to have similar values.

For min/max congruence, put $d=\max(b,c)$. Both component inequalities
imply bounds with the same additive allowance $d$. Monotonicity and
translation invariance give

$$
F(t_1,t_2)
 \le F(s_1+d,s_2+d)
 =F(s_1,s_2)+d,\qquad F\in\{\min,\max\}.
\tag{5}
$$

This argument also applies to negative budgets. If one argument remains
unchanged, the common budget is $\max(b,0)$: saturation can erase a
strict component improvement.

Residual polarity requires particular care. From

$$
a_{\rm old}\le_p a_{\rm new},
\qquad
b_{\rm new}\le_q b_{\rm old},
$$

one obtains

$$
\operatorname{res}(a_{\rm new},b_{\rm new})
 \le_{\max(p+q,0)}
\operatorname{res}(a_{\rm old},b_{\rm old}).
\tag{6}
$$

The preactivation changes by
$(b_{\rm new}-b_{\rm old})+(a_{\rm old}-a_{\rm new})$; the unchanged
zero branch then contributes the clipping. Using the opposite comparison
in the first argument would be unsound.

### 4.2 Reuse after source revision

An old proof is a conditional argument, not an unconditional stored answer.
To reuse it under a new source, substitute source terms in a type-correct
way and prove the substituted old row directions in every current case.
The receiver checks the resulting current request. Matching an old
fingerprint or copying an old numerical budget is insufficient.

A related construction makes the cost of withdrawing assumptions explicit.
For an old localized proof, replace a withdrawn row allowance $\eta_i$
by

$$
\eta_i+\max(a_i(x)-\eta_i,0).
$$

Replaying the proof's monotone budget operations produces a pointwise
allowance $E_P(x)$. On the retained domain,

$$
t(x)-s(x)\le E_P(x)=b_P+R_P(x),\qquad R_P(x)\ge0.
\tag{7}
$$

The penalty is zero wherever the used withdrawn rows still hold. It is
relative to the chosen proof and need not be small, observable or minimal.
A separate receiving check reconstructs the promised penalty and request;
an otherwise valid proof does not authenticate arbitrary attached metadata.

Alternative supports matter under revision. Discarding a currently
inferior proof can lose the best surviving argument after one of its
competitors' assumptions is withdrawn. This is a reason to track
dependencies and useful alternatives, with explicit storage and checking
costs, rather than identify a current best scalar bound with all reusable
evidence.

*Rules and full constructions:* [inference rules](v2/derivations/02_inference_rules.md),
[source transport and withdrawal](v2/derivations/02b_source_transport_and_withdrawal.md),
and [producer/receiver reconstruction](v2/derivations/03f_soundness_acceptance.md#3-producer-contracts-and-the-interface-repair).

## 5. What the calculus proves

### 5.1 Current-request soundness

**Theorem 1 (soundness).** Fix an admitted context and an independently
specified request. On finite immutable supported data and exact rational
arithmetic, suppose the native checker accepts a finite proof and a
receiving check binds its actual root to the request's current context,
domain, unit, expression pair and adequate budget. Then the request holds
in the finite-real semantics (1). Every additional producer field used by
the caller requires its stated input contract and proved transformation,
or an independent receiving check of that field.

**Proof.** First verify that normalization preserves denotation.
Structural induction carries the captured local environment, collects a
binding's right side before extending that environment, and preserves
source/local distinctions. The original term is type-checked before zero
coefficients are erased. Residuals unfold their definition and conversions
multiply by their declared factors. Thus equal collected differences
denote equal functions, including on unbounded domains.

Next check each stored instruction. Constant and row instructions are
valid by exact arithmetic and the case assumptions. Addition,
transitivity, nonnegative scaling, polarity reversal and slack preserve
their pointwise inequalities. The minimum of two valid bounds bounds the
same difference. Equation (5) proves min/max congruence and the
common-target variants; equation (6) proves the residual rule. The
lattice projections and injections hold pointwise. Finally, the all-cases
instruction covers each live case once and takes the maximum of their
bounds.

Parents point strictly backward, and each instruction checks its scope.
Induction over the finite sequence therefore proves every instruction and
its designated root. The receiver compares that root with the separately
given request. A root budget $b_{\rm out}\le B$ discharges an inclusive
request at $B$; a strict request requires $b_{\rm out}<B$.
The bound consequently applies to the actual requested pair and domain.
$\square$

This is correctness conditional on successful return. It does not promise
that bounded search returns a proof, that a reported bound is optimal, or
that a source assumption is empirically applicable. Program identity,
proxy adequacy and observation availability are additional modeling
premises. Context hashes identify recorded data; they do not establish
physical provenance.

The full rule proof and the implementation correspondence are in the
[soundness derivation](v2/derivations/03_soundness.md) and its
[acceptance reconstruction](v2/derivations/03f_soundness_acceptance.md).

### 5.2 Constructive completeness for accessible evidence

A directed conversion can move a proof into a different unit. The rules
do not invent a reverse conversion. This makes the available source
information part of the exact completeness statement.

Let $A(u)$ contain the units with a directed conversion path to $u$,
including the path of length zero. The **target-unit reduct**
$\mathcal C|u$ retains exactly the rows whose unit lies in $A(u)$.
It keeps the signature, case identities and feasible witnesses. Removing
rows preserves each case's nonemptiness.

Let $K_{\mathcal C}(t,s;b)$ mean that a finite native proof exists with
exactly the global pair $t,s$, in unit $u$, and root budget at most
the rational number $b$. This is mathematical proof existence, without
an implementation's search or size caps.

**Theorem 2 (unit-directed completeness).** For the finite rational typed
fragment and contexts of §3, and one common literal query pair,

$$
K_{\mathcal C}(t,s;b)
\quad\Longleftrightarrow\quad
\mathcal C|u\models t-s\le b.
\tag{8}
$$

If the optimal reduct bound is finite, it is rational and is attained by
both a finite native proof and a rational reduct model. If the bound is
$+\infty$, no finite native budget exists.

**Proof structure.** Trace the root's ancestors. Every premise edge
preserves the inequality unit or follows a declared conversion. Hence
every used source row survives in the reduct. Apply the soundness
induction in the separate reduct cases, then aggregate their union.
This proves the forward implication.

For the converse, transport accessible rows along positive conversion
paths and certify the retyping of the query in unit $u$. Conversion
through min/max needs derived equalities, not an assumed inverse map.
Refine the finite expression into affine sign cells. Rational linear
elimination supplies feasible witnesses or strict infeasibility rays,
and exact nonnegative row multipliers for affine upper bounds. A finite
optimum is rational and attained, even when nuisance coordinates are
unbounded or the source has no vertex.

The temporary sign assumptions can be removed using the existing
withdrawal construction and a source-free disjoint-hinge identity.
Opposite guards give allowances proportional to
$\max(g,0)$ and $\max(-g,0)$; their suitably weighted minimum vanishes.
Strict rays discharge empty children. Graft the original converted-row
proofs into each surviving local proof and check the literal query pair.
Only then aggregate all original live cases. The resulting finite native
proof contains neither an optimizer oracle nor temporary unverified rows.

These are the three reductions of the complete constructive proof.
The exact retyping, affine-certificate and guard-elimination arguments
are given in [the characterization, §§9–14](v2/derivations/04_characterization.md)
and [its reconstruction, §§2–3](v2/derivations/04g_characterization_acceptance.md).
An alternative max-min construction is also given there; its normal-form
identities are proved independently of (8), avoiding circularity.
$\square$

**Why full-source completeness can fail.** Take units $U,V$, one
factor-one conversion $U\to V$, and a source $x:U$. The single case
has the $V$-row $\operatorname{convert}(x)\le-1_V$, with witness
$x=-1$. The $U$-request $x\le_{-1}0_U$ is valid in the full real
semantics. Its $U$-reduct has no rows; $x=0$ refutes the request
there. Equation (8) proves native nonderivability. This is a structural
boundary, not merely a failed search.

For a fixed conversion graph, full-source completeness uniformly over
source declarations and $u$-queries holds exactly when every unit in
$u$'s weak component reaches $u$. For all target units, each weak
component must be strongly connected. A fixed signature can have a
weaker criterion because only actually declared source keys matter.
The exact distinctions are in [characterization results U7–U10](v2/derivations/04_characterization.md).

## 6. Boolean reasoning, earlier licenses and numerical scales

### 6.1 A genuine Boolean fragment

On Boolean source assignments, encode truth as loss zero and falsity
as loss one. The following translation preserves truth by structural
induction:

| Formula | Loss expression |
|---|---|
| $\top,\bot$ | $0,1$ |
| $\neg A$ | $1-L(A)$ |
| $A\land B$ | $\max(L(A),L(B))$ |
| $A\lor B$ | $\min(L(A),L(B))$ |
| $A\Rightarrow B$ | $\operatorname{res}(L(A),L(B))$ |

For a finite premise family $\Gamma$ over finitely many atoms,
let $P_\Gamma=\max_{A\in\Gamma}L(A)$, taking zero for no premises,
and let $\mathcal C_B$ consist of all Boolean valuations as finite
point cases in one unit. Then

$$
\Gamma\models_{\rm CL}B
\quad\Longleftrightarrow\quad
\mathcal C_B\models L(B)\le P_\Gamma
\quad\Longleftrightarrow\quad
K_{\mathcal C_B}(L(B),P_\Gamma;0).
\tag{9}
$$

If all premises hold, $P_\Gamma=0$, so the comparison requires $B$.
Otherwise $P_\Gamma=1$, and the comparison is automatically true.
Theorem 2 supplies the last equivalence. Premises are encoded in the
query, so inconsistent premises retain classical entailment without an
inadmissible empty source.

This is an exact fragment, not an identification of arbitrary numerical
loss with truth. On the interval $[0,1]$, the excluded-middle
expression has loss $\min(x,1-x)=1/2$ at $x=1/2$. Addition also
leaves the Boolean carrier.

### 6.2 Relation to the first-stage reliance calculus

The earlier report concerned present permission to rely on a fallible
model under a domain, task loss, tolerance, fallback, profile and
provenance. Its assessment states were refuted, open and supported.
Their meet algebra embeds as the constant losses $1,1/2,0$, with
maximum combining requirements. The value $1/2$ here is a status
code, not the probability that a claim is true or the expected cost
of acting on an open claim.

The stronger connection is through explicit evidence consumers. For
an admitted interval $[l,u]$ and threshold $\tau$, the original
consumer supports the requirement when $u\le\tau$, refutes it when
$l>\tau$, and otherwise leaves it open. Finite rectangles and
specified polyhedral acceptable regions have corresponding
quantitative adapters. Joint feasibility matters: individually
possible requirements need not be jointly possible.

These adapters preserve the defined consumers. They do not reconstruct
missing evidence, an invalid frame, provenance or every possible
acceptable region from a status number. The earlier license system and
the present loss semantics therefore have a precise interface, rather
than a claimed unrestricted embedding.

### 6.3 Meaning-preserving numerical presentation

Changing the numerical presentation of a loss requires transporting
the operations, source rows, conversions and budgets consistently.
Positive affine presentations preserve the stated comparison
structure under these conditions; a negative scale reverses the
expression pair. Preserving all rational difference-budget tests through
one common budget map, for all real baselines, is stronger than preserving
order and forces an affine numerical map with positive scale.
A bounded monotone recoding alone does not
preserve unrestricted additive comparisons or exact unbounded
information.

The general unit-specific affine certificate reconstruction is proved
on paper. Its implemented compiler covers the common-positive-scale
special case. This difference between a mathematical construction and
current executable coverage is retained throughout the report.

*Detailed interfaces and proofs:* [Boolean and phase-one adapters](v2/derivations/05a_boolean_and_phase_one.md),
[presentation laws](v2/derivations/05b_scaling_and_bounded_domains.md),
and [general affine certificate construction](v2/derivations/05h_affine_certificate_transport.md).

## 7. What must survive a cost revision?

The application asks which features of a joint outcome law must be retained
to answer later cost questions. It separates three services: reconstructing
all numerical means, preserving comparisons between plans, and selecting
an action within a tolerance. They need not have the same information
requirement.

### 7.1 Reset procedures and exact summaries

There are $k\ge2$ reset procedures. A world $w\subseteq[k]$ records
which procedures would fail on one fixed request. Its law $p$ is arbitrary
on the full $2^k$-world simplex. An order $\pi$ tries each procedure
until the first success, paying strictly positive rational attempt
prices $c_i$, and terminal penalty $M\ge0$ if all fail. Write

$$
m_S=\Pr(S\subseteq w),\qquad m_\varnothing=1.
$$

Then the mean cost is

$$
C_\pi(c,M)
 =\sum_{j=1}^k c_{\pi_j}
     m_{\{\pi_1,\ldots,\pi_{j-1}\}}
   +M m_{[k]}.
\tag{10}
$$

All permutations are allowed. The outcome law is unchanged when prices
change; stateful procedures or edits that change outcomes require a
different source contract. Prices are fixed parameters of each query, so
(10) is affine in the moment coordinates. Its native instances take all
fixed price and penalty parameters to be rational.

An exact linear summary stores linear measurements of the law, with
arbitrary decoding allowed afterward and known constants free. Its
dimension is a linear-information requirement. It is not a number of
bits, a finite-sample guarantee, or a lower bound for arbitrary
nonlinear real encodings.

### 7.2 Two price profiles and minimal repair

Put $n=2^k-1$, the simplex direction dimension. The following results
evaluate the rank of the requested family of linear functionals.

**Theorem 3 (retention under price revision).** For one strictly positive
price profile and any $M\ge0$, all order means have exact linear rank
$2^k-k$; all within-profile order differences have rank $n-k$.
For two nonproportional strictly positive profiles $(c,M),(d,N)$,
with $M,N\ge0$, the ranks are:

| Requested values | Rank |
|---|---:|
| All numerical means at both profiles | $n$ if $M>0$ or $N>0$; otherwise $n-1$ |
| All within-profile order differences | $n-1$ |
| All differences, also allowing cross-profile comparisons | $n$ if $M\ne N$; otherwise $n-1$ |

**Proof.** Work in moment directions $v$, with $v_\varnothing=0$.
An adjacent swap of $a,b$ after prefix $S$ changes the directional
mean by

$$
(c_a-c_b)v_S+c_bv_{S\cup\{a\}}-c_av_{S\cup\{b\}}.
\tag{11}
$$

These swaps connect all orders. Their simultaneous zero set on proper
subsets has the form

$$
v_A=\sum_{r=1}^{|A|}t_r e_r(c_A),
\qquad \varnothing\ne A\subsetneq[k],
\tag{12}
$$

where $e_r$ is the elementary symmetric polynomial and
$t_1,\ldots,t_{k-1}$ are free. To obtain (12), the empty-prefix
swap first makes $v_i/c_i$ constant. At each next subset size,
subtract the already determined lower-degree terms. The residual,
divided by the product of that subset's prices, is constant across
one-element exchanges; the graph of subsets of fixed size is
connected. The elementary-symmetric recurrence verifies the converse.

The full-set direction is separately free. The common directional
mean equals

$$
\sum_{r=1}^{k-1}t_r e_{r+1}(c_{[k]})+Mv_{[k]}.
\tag{13}
$$

Its proper-coordinate functional is nonzero because $e_2(c)>0$.
Thus differences have a $k$-dimensional kernel, and numerical
means impose one additional independent constraint. This proves the
single-profile ranks.

Now require (12) for both $c$ and $d$. At subset size one,
nonproportionality forces both leading coefficients to vanish.
Inductively, if a nonzero coefficient first survived at size $r$,
the products $\prod_{i\in A}(d_i/c_i)$ would be constant over all
$r$-subsets. Comparing two subsets that differ in only one member
forces every ratio $d_i/c_i$ to agree, a contradiction. All proper
directions therefore vanish. The remaining full-set direction has
numerical values $Mv_{[k]}$ and $Nv_{[k]}$, and cross-profile
difference $(M-N)v_{[k]}$, giving the table.

Finally, let $Q$ be the requested linear map on the simplex direction
space, and $T$ a proposed retained map with
$\operatorname{rank}T<\operatorname{rank}Q$. There is a direction
$v\in\ker T\setminus\ker Q$. Small opposite perturbations of an
interior law along $v$ have identical retained data and different
requested values. No decoder from that retained map can answer both.
$\square$

The equal-price rank has a direct maximal-chain-span antecedent:
Gasanova and Nicklasson's Theorem 3.4 supplies the corresponding
$|L|-|P|$ dimension for the finite distributive lattice
$L=\mathcal J(P)$ of ideals of a finite poset $P$
([Gasanova–Nicklasson](#ref-chain)). The price-dependent kernel and
its intersection, evaluated here for the reset consumer, are the
relevant extension.

**Theorem 4 (repair by actual new means).** Start with a minimum-rank
exact summary of all old numerical means with $c_i>0$ and $M>0$.
Change one price to $c_j+\varepsilon>0$, where
$\varepsilon\ne0$, keeping $M$ and the law fixed. Exactly
$k-1$ additional independent linear measurements suffice and are
necessary in the worst case to recover the full law. They can be
$k-1$ actual new-order means.

**Proof.** Choose a reference order with $j$ last and let $P_r$
be its first $r$ procedures, so
$P_1\subset\cdots\subset P_{k-1}=[k]\setminus\{j\}$ and
$|P_r|=r$. An order
placing exactly $P_r$ before $j$ has new-minus-old mean

$$
C_{\pi_r}(c+\varepsilon e_j,M)-C_{\pi_r}(c,M)
 =\varepsilon m_{P_r}.
\tag{14}
$$

Its old mean is available from the summary. The new measurements
therefore recover the $k-1$ chain moments. Define $t_r$
recursively by

$$
m_{P_s}=\sum_{r=1}^s t_r e_r(c_{P_s}),
\qquad
r_A=m_A-\sum_{r=1}^{|A|}t_r e_r(c_A).
$$

The canonical old summary stores the $r_A$ off the reference
chain and one reference old mean; on the chain, $r_{P_s}=0$.
These are linear coordinates whose common kernel is the old
numeric kernel, so the given exact summary determines them.
The recovered chain moments solve the triangular equations,
whose diagonal is $\prod_{i\in P_s}c_i>0$. The residuals then
recover all proper moments. Equation (10) for the reference
old mean recovers $m_{[k]}$ by division by $M$.

Conversely, the old-summary kernel has dimension $k-1$. Fewer
than $k-1$ additional linear responses leave a nonzero direction.
At an interior law, small opposite perturbations remain feasible.
For deterministic adaptive queries, fix the transcript at that law:
the perturbations preserve each answer, so induction preserves
every subsequent query choice. The two laws remain indistinguishable.
$\square$

If $M=0$, no full-order mean sees $m_{[k]}$, whatever the prices.
The proper moments can instead be recovered with $k-2$ new means.
Proportional price families and additional known marginals have
separate classifications in the
[full retention derivation, §§4–8](v2/derivations/09_c4_price_revision.md).

### 7.3 Exact fragility and decision stability

An arbitrarily small nonproportional price edit can require the
maximal exact numerical information. This does not imply a large
practical change. Pathwise, a one-price edit changes every order's
cost by a number in

$$
[\min(0,\varepsilon),\max(0,\varepsilon)].
\tag{15}
$$

An old-optimal policy therefore has new-price regret at most
$|\varepsilon|$ for the stated common mean, fixed-level CVaR or
worst-source objective. Compare its new value with its old value
plus the upper endpoint, use old optimality, and compare the
new-optimal policy's old value with its new value minus the lower
endpoint. The interval width is the regret bound.

Likewise, the old mean plus $\varepsilon/2$ has a universal
absolute error bound $|\varepsilon|/2$ for a revised mean.
An exact information lower bound consequently does not force
maximal memory for an approximate or action-only request.

Equation (14) also clarifies a statistical distinction. Dividing
two separately perturbed aggregate means by a small
$\varepsilon$ can amplify their errors. If both prices are
evaluated on the same retained world traces, their pathwise
difference is $\varepsilon$ times a reach indicator, so the
corresponding paired estimator does not have that intrinsic
statistical amplification. Those traces are additional retained
information; they are not present for free in an old aggregate.

### 7.4 A compatible estimate at the sharp common error

Separate coordinate intervals need not have midpoints realizable
by one law. Subsequent composition then needs either the original
uncertainty set or a compatible estimate with a valid error
contract. On the following full-fiber family, compatibility costs
nothing at the best **common** maximum error.

Assume unit old attempt prices and retain all exact old order
means, with fixed $k\ge2$ and $M\ge0$. The source is the full
nonempty set of Boolean laws compatible with that summary, without
additional law restrictions.

For $h<k$, set
$g_h=(k+1)/(k+1-h)$, and set $g_k=k+M$.
These are the old costs averaged over all orders on a world with
$h$ failures. A canonical summary retains the probability
contrasts within each Hamming level and

$$
B=\sum_w g_{|w|}p_w.
$$

There are $2^k-k$ such coordinates. In each level subtract the
minimum contrast, including the reference world's zero contrast,
to obtain fixed nonnegative residues $\rho_w$. Put

$$
R=1-\sum_w\rho_w,\qquad
B_{\rm rem}=B-\sum_w g_{|w|}\rho_w.
$$

If $R=0$, the law is already determined. If $R>0$, every
compatible law has exactly the representation

$$
p_w=\rho_w+\frac{R q_{|w|}}{\binom{k}{|w|}},
\qquad
q_h\ge0,\quad \sum_hq_h=1,\quad
\sum_h g_hq_h=\mu=\frac{B_{\rm rem}}R.
\tag{16}
$$

This allows nonexchangeable residue offsets. Only the remaining
uncertainty is expressed by a distribution on the $k+1$
failure-count levels. For $1\le r\le k-1$, define
$f_r(h)=\binom hr/\binom kr$; a proper-prefix moment has a fixed
residue contribution plus $R\mathbb E_qf_r$.

**Theorem 5 (compatible common-radius recovery).** For $R>0$,
under these assumptions, define

$$
\alpha=\frac{\mu-1}{k+M-1},\qquad
q^-=(1-\alpha)e_0+\alpha e_k.
$$

Let $q^+$ be the mixture on adjacent $g$-levels bracketing
$\mu$, with mean $\mu$, and put
$\beta=\mathbb E_{q^+}f_1$. The law obtained from

$$
q^*=\tfrac12(q^-+q^+)
\tag{17}
$$

through (16) attains the unrestricted minimum common maximum
absolute error over all proper-prefix moments. The conditional
radius is

$$
r(\mathcal C)=\frac R2(\beta-\alpha).
\tag{18}
$$

For any separately applied single-price edit
$\varepsilon$ with $1+\varepsilon>0$, the revised-order mean
radius is $|\varepsilon|r(\mathcal C)$. The same decoded law
works for each such edit. A bounded collection whose supremum
edit magnitude is $E$ has common worst error $Er(\mathcal C)$.

**Proof and its nontrivial step.** The endpoint law $q^-$
minimizes the singleton expectation, giving $\alpha$. The
polygonal curve $(g_h,h/k)$ is concave, so the adjacent-level
law $q^+$ maximizes it, giving $\beta$. These two extremes
force error at least $(\beta-\alpha)/2$ before scaling by $R$.

For every $r$, let $L_r,U_r$ be the extrema of
$\mathbb E_qf_r$ under the constraints in (16), and write
$B_r=\mathbb E_{q^+}f_r$. The family-specific envelope argument
establishes both inequalities

$$
2U_r\le\beta+B_r,\qquad
2L_r\ge2\alpha+B_r-\beta.
\tag{19}
$$

The candidate coordinate is $(\alpha+B_r)/2$. Equation (19)
puts its distance to both endpoints at most
$(\beta-\alpha)/2$, simultaneously for all $r$.
The residues add fixed constants and $R$ scales the uncertainty.
Thus one compatible law attains the lower bound. For a fixed
edited procedure $j$, every subset of $[k]\setminus\{j\}$
can precede it, so every prefix size from zero through $k-1$
occurs. Equation (16)'s varying contribution depends only on
that size; the residue offset is fixed. Since $k\ge2$, an
available singleton excluding $j$ gives the same lower
bound. Equation (14) therefore yields the exact radius for
that fixed edit. When $R=0$, the known law has radius zero.

The substantive proof of (19) is retained in
[the complete envelope derivation, §§3–7](v2/derivations/10_f16_coherent_recovery.md).
It reduces the inequalities to the knots $g_j$, proves the
upper bounds using the polygonal concave envelope, and proves
the lower bounds through an affine envelope and the separate
$M=0$, $M>0$ cases. Equation (19) is not a consequence of
generic convexity alone. This paragraph gives the construction
and reduction; the linked note supplies the full binomial
inequality proof.
$\square$

Taking the worst case over all exact old-summary fibers gives
the sharp global revised-mean radius

$$
\frac{|\varepsilon|}{2}
\max_{1\le j\le k-1}
\left[
\frac jk-\frac{j}{(k-j+1)(k+M-1)}
\right].
\tag{20}
$$

The maximum requires $O(k)$ scalar arithmetic operations.
This excludes reading the generally exponential-size summary,
computing its residues, materializing a law, and generating or
checking a native certificate. At $k=3,M=4$, the radius is
$|\varepsilon|/4$. For the frozen small edit
$|\varepsilon|=1/40$, it is $1/160$, compared with the
ordinary universal bound $1/80$. Both already satisfy the
experiment's numerical tolerance $1/20$. The factor-two
improvement here is an exact bound, not evidence of a new
successful decision or a speed advantage.

**The limit of the theorem matters.** One common radius does not
require every coordinate to be its own interval midpoint.
At $k=4,M=1/10$, zero contrasts and $B=9/8$ yield individual
midpoints

$$
m_1=41/496,\qquad m_2=1/48,\qquad m_3=5/248,
$$

where subscripts indicate subset size. Together with the old
mean they force a negative probability $-3/496$ for each
two-failure world. Yet a compatible common-radius optimum still
exists by Theorem 5. The earlier three-procedure midpoint
warning was corrected: in that exact equal-price family with
$M>0$, the proper-coordinate midpoints are compatible.

Additional source restrictions can change the result. The
[explicit convex-source triangle](v2/derivations/10_f16_coherent_recovery.md#10-additional-convex-source-restrictions-can-create-a-coherence-penalty)
has unrestricted moment radius $1/400$ and compatible radius
$1/300$. Noisy old observations, simultaneous price edits,
changed terminal penalty and arbitrary new moment combinations
are also outside Theorem 5. A compatible decoded law is an
estimate with a stated query error; it is not new exact source
knowledge.

*Complete retention, repair and interval proofs:*
[price-revision analysis](v2/derivations/09_c4_price_revision.md).
*Compatible-law construction, sharp bound and adverse cases:*
[coherent recovery](v2/derivations/10_f16_coherent_recovery.md).

## 8. Worked uses of the inference rules

### 8.1 Replacing a scientific calculation

Consider the declared degree-six polynomial family in the
[scientific case study](v2/derivations/06_case_studies.md).
A Simpson rule $S$ uses three samples. A rule $Q$, constructed
to be exact on this family, uses four, including an additional node
at $1/12$. Their error interpretations share a target discrepancy
$J$:

$$
E_Q=J+\sum_j Q_j(r_j+e_j),\qquad
E_S=J+d+\sum_j S_j(r_j+e_j).
\tag{21}
$$

The source supplies a joint coefficient strip
$|d|=|u/4-v|\le1/64$, node discrepancies $|r_j|\le1/100$,
measurement errors $|e_j|\le1/200$, and sample price $c=1/32$.
The coefficients satisfy
$\sum_j|S_j-Q_j|=28633/46200$. The common discrepancy $J$
may be unbounded.

Define total loss as absolute error plus sample cost. Subtracting
(21) cancels $J$. The triangle inequality, established with signed
scaling, addition and the max rules, gives

$$
\begin{aligned}
L_S-L_Q
&\le |E_S-E_Q|-c\\
&\le \frac1{64}
  +\frac3{200}\frac{28633}{46200}
  -\frac1{32}\\
&=-\frac{4873}{770000}<0.
\end{aligned}
\tag{22}
$$

The cheaper deployment is consequently preferable under the admitted
relative-loss request. No final comparison was supplied as a source
premise: the proof combines the coefficient, discrepancy, error and
price facts.

The result depends on the requested comparison. Absolute accuracy
remains unbounded through $J$. Withdrawing the joint coefficient
strip removes the stated replacement guarantee. Ordinary
support-function arithmetic obtains the same bound; ordinary
interpolation supplies $Q$, and a general four-point Gaussian
quadrature also integrates the declared degree-six family exactly.
The contribution is the explicit composition and its source
boundary, not a new quadrature advantage.

The family, weights, native derivation, adverse variants and ordinary
references are specified in
[case-study §§2.1–2.9](v2/derivations/06_case_studies.md).

### 8.2 A reasoner comparing its own bounded procedures

The self-assessment example uses actual proof procedures. The source
contains short chains $x\le y_i\le b_i$, with $b_i\in\{0,1\}$,
and a longer chain $x\le z_0\le z_1\le z_2\le0$. The current
request is $x\le0$. Short procedure $i$ attempts its two-row
chain and succeeds at current reception exactly when $b_i=0$.
The long procedure always resolves this source family.

Every request is already a theorem of its supplied source.
“Unresolved” therefore means that a particular bounded procedure
failed to produce a received proof, not that the request is false.
Calibration executes those procedures; a separate declared model
relates their failure patterns to later requests.

In the chosen emitted-node cost proxy, a short trace costs five,
the complete fallback costs nine, and exhaustion carries penalty
twenty. A three-procedure cascade has mean

$$
C=5+5m_1+5m_{12}+20m_{123}.
$$

From the separate premises
$m_1=1/2$, $m_{12}=1/4$, and $0\le m_{123}\le q$,
the calculus derives

$$
C-9\le-\frac14+20q.
\tag{23}
$$

Thus $q\le1/80$ establishes non-deterioration relative to the
fallback. The cascade is then used on later requests under the
declared same-population assumption.

| Failure population | Cascade mean | Cascade unresolved probability | Selected policy mean | Strong ordinary source-visible control |
|---|---:|---:|---:|---:|
| Even parity | $35/4$ | $0$ | Cascade, $35/4$ | $5$ emitted nodes |
| Odd parity | $55/4$ | $1/4$ | Complete fallback, $9$ | $6$ expected emitted nodes |

The ordinary control inspects the visible $b_i$, chooses a
successful short chain when available, and otherwise uses the
long chain. It is stronger on this node-count objective.
Inspection, construction and runtime would need their own costs
before making a total-performance comparison.

This is finite staged self-assessment: the reasoner uses evidence
about its procedures to choose a later procedure and checks the
returned proof against the current request. It is neither a general
self-certification theorem nor a difficult theorem-proving benchmark.
[The complete executable construction](v2/derivations/06_case_studies.md#4-actual-bounded-native-procedures-and-later-reasoning)
records the observations, policies and limits.

## 9. Implementation and the frozen retention challenge

### 9.1 What is implemented

The implementation separates a small exact rational native checker,
bounded proof producers, and a receiver that binds the actual
conclusion to a current request. The integrated revision layer
compares retained sources, transports usable evidence, checks
alternative supports and reports acquisition and checking costs.
An ordinary reference reconstructs the same requested numerical
and decision services from the same information.

A proof is stored as a finite sequence with strictly backward
references. Admission checks source feasibility witnesses and
typing. Reception rejects stale, mismatched or insufficient
outputs; it does not treat a field called a certificate as its own
validation. Named expansion limits bound selected operations, not
every possible process allocation. The implementation is Python
with rational arithmetic, not a proof-assistant formalization.

The most recent pre-report Linux regression passed **288 distinct
tests on its first attempt**, covering the mathematical core,
producer/receiver contracts, revision integration and both
case-study modules. This is the named focused suite, not an
all-repository or cross-platform result. The source versions and
actual command are preserved in the
[technical regression record](v2/work_logs/C_2026-10-06_S1/reviews/technical/regression_attempt1/result.json).

### 9.2 Prospective protocol and population

The experiment was frozen before final evaluation in protocol
**F14-v1**, covering 34 files. Its two questions were whether the
revision application met a specified usefulness criterion and
whether a specified expected-cost intervention correspondence
could be extracted from ordinary-trained networks.

All five neural model artifacts, including every discovery-selected
alignment, were prepared, saved, hashed and separately reloaded for
validation **before any final evaluation population was generated**.
This order also applied to the retention population. Preparation
and evaluation each completed on attempt one. No discovery
alignment was refitted using final data.

The retention study used three reset procedures, unit old attempt
prices and terminal penalty four. Sixteen initial exact synthetic
laws were generated from positive integer weights on the eight
worlds. Each supplied ten registered revision variants: unchanged;
small and large positive and negative one-price edits;
proportional scaling; program edit; known marginals; withdrawal;
and source drift. The small edit magnitude was $1/40$;
the large changes were $+1$ and $-1/2$. Numerical and decision
regret tolerances were both $1/20$.

Each of the resulting **160 episodes** was assessed under six
methods and two acquisition regimes, yielding **1,920 method rows**
and **11,520 scalar outputs**. Variants share their initial law,
and methods share episodes. These counts are not independent
replications.

The six methods were fresh reconstruction, a cached-proof route,
full-joint retention, a tailored summary, ordinary exact intervals,
and a marginal diagnostic. The latter is deliberately
information-limited; it is not the strongest ordinary comparator.
Adaptive acquisition requested additional information when any
numerical or decision refusal required it, under the unchanged
registered policy.

### 9.3 Retention outcomes and ordinary controls

In the table, numerical counts are **exact / approximate / refused**
out of 960 scalar outputs per arm. Decision counts are
**certified order / certified fallback / refused** out of 160
episodes per arm. A received native comparison is recorded
separately from the selected-action outcome.

| Acquisition | Method | Numerical counts | Decision counts | Received native comparisons |
|---|---|---:|---:|---:|
| None | Fresh | 768 / 0 / 192 | 98 / 30 / 32 | 98 |
| None | Cached proof | 768 / 0 / 192 | 98 / 30 / 32 | 98 |
| None | Full joint | 768 / 0 / 192 | 98 / 30 / 32 | 98 |
| None | Tailored | 416 / 172 / 372 | 85 / 29 / 46 | 88 |
| None | Ordinary exact intervals | 416 / 172 / 372 | 85 / 29 / 46 | 88 |
| None | Marginal diagnostic | 0 / 0 / 960 | 0 / 16 / 144 | 0 |
| Adaptive | Fresh | 960 / 0 / 0 | 126 / 34 / 0 | 126 |
| Adaptive | Cached proof | 960 / 0 / 0 | 126 / 34 / 0 | 126 |
| Adaptive | Full joint | 960 / 0 / 0 | 126 / 34 / 0 | 126 |
| Adaptive | Tailored | 824 / 136 / 0 | 126 / 34 / 0 | 126 |
| Adaptive | Ordinary exact intervals | 824 / 136 / 0 | 126 / 34 / 0 | 126 |
| Adaptive | Marginal diagnostic | 960 / 0 / 0 | 126 / 34 / 0 | 126 |

All **960 saved equal-information comparisons** agreed on ordinary
results, native targets and acquisition behavior. The ordinary
interval method reproduced the tailored results. The application
therefore demonstrates a workable conditional reasoning service
and informative refusal boundaries, without establishing an
exclusive numerical capability.

The prospective useful-derivation criterion required direct price
or program revision, an executed nonfallback choice, a current
native bound at most $-1/20$, at least two distinct nonzero source
premises, and coherent regret at most $1/20$. At least four
distinct episodes from two seeds had to qualify, covering both
price and program edits, with at least one genuinely uncertain
selective no-acquisition case whose selected cost remained
approximate.

The study met that criterion:

| Useful result | Distinct episodes |
|---|---:|
| Small positive price edit | 14 of 16 |
| Small negative price edit | 14 of 16 |
| Large positive price edit | 9 of 16 |
| Large negative price edit | 16 of 16 |
| Program edit | 15 of 16 |
| Total | **68 of 160**, covering all **16** initial seeds |
| Uncertain selective cases with approximate selected cost and no acquisition | **15 episodes across 8 seeds** |

The last category appears in 30 paired-method rows. Across all
methods and regimes there are 718 useful rows, which repeat the
68 episodes rather than adding independent successes.

### 9.4 Resource costs and the scope of usefulness

The strongest ordinary arithmetic baseline is often much cheaper.
In the no-acquisition arm, fresh numerical arithmetic averaged
$1.005003$ ms per episode, while its native-inclusive update
averaged $72.134739$ ms. The tailored route averaged
$5.984763$ ms for arithmetic and $81.452699$ ms including
the native service. Cached proof handling was slower than fresh
handling in all 98 matched admitted-service no-acquisition cases,
with mean difference $81.113254$ ms.

The tailored payload had median 125 serialized bytes versus
143 for ordinary intervals, an 18-byte encoding difference at
the same information rank. Its median total serialized stored
upper measure was 21,503 bytes, versus 20,527 for fresh handling.
These payload and stored-artifact measures are not process memory
and do not establish overall compression superiority.

Of 960 adaptive rows, 412 performed repairs: 60 used two new
means and 352 used eight-field repairs. The remaining 548 needed
none. The full report retains acquisition prices, amortization
horizons and all cost components; a selective summary does not
receive free observation or checking.

Thus the supported empirical result is the frozen application
criterion under exact stipulated sources. It is not a deployment
calibration result, a general speed advantage, or evidence that
the sharp bound of §7 creates decisions unavailable to ordinary
methods. The easy small-edit bounds already met the registered
tolerances.

*Protocol and complete outputs:*
[frozen protocol](v2/experiments/protocol.md),
[configuration](v2/experiments/config.v1.json),
[full F15 report](v2/experiments/results.md),
[method-level machine summary](v2/experiments/F15_v1_analysis/retention_by_method.json),
and [saved-row recount](v2/work_logs/C_2026-10-06_S1/saved_results_attempt1/summary.json).

## 10. The ordinary-trained neural intervention probe

### 10.1 The task and what the probe asks

Each network receives
$(x_1,x_2,c_{\rm FN},c_{\rm FP})$, with
$x_i\in[-1,1]$, prices in $[1/2,2]$, and binary outcome
probability

$$
\eta=\frac12+\frac{x_1+x_2}{8}.
$$

Ordinary weighted binary cross-entropy training has optimal output

$$
p^*=\frac{J_0}{J_0+J_1},\qquad
J_0=c_{\rm FN}\eta,\quad
J_1=c_{\rm FP}(1-\eta).
\tag{24}
$$

The networks have 32 ReLU hidden units and 193 parameters.
Each receives 768,000 binary labels over 3,000 training steps:
3,840,000 labels across five models, and **zero expected-cost
training labels**. Expected-cost counterfactual targets are
subsequently used in alignment discovery; they are not absent
from the entire experiment.

The intervention asks whether replacing an identified hidden
subset's state with a donor's state changes the output as if one
of the expected costs had been replaced at the high level.
Discovery searches 128 candidate eight-coordinate subsets for
each role, hypothesis and arm. It uses four fixed scales:
identity, multiplication by $1/\eta$,
$1/(1-\eta)$, or $1/(J_0+J_1)$.
These scales preserve ordinary prediction when applied to both
costs, but can predict different mixed interventions.

Controls include equally budgeted random search, permuted-concept
search, incorrect donors and untrained networks, alongside the
aligned arm. The five evaluation strata test mixed near- and
far-decision pairs, preservation of the other cost, equal target
cost and scale separation. All hypotheses and controls retain
their original rows; none was substituted after evaluation.

The original simultaneous analysis has 560 intervals at familywise
level $0.05$, using the frozen two-sided Hoeffding union bound
([Hoeffding](#ref-hoeffding)). A model supports the complete
identity claim only when the registered accuracy, decision,
control and scale requirements all pass; at least four of five
models are required for the overall support claim. This is
stronger than ordinary task success or a low average
intervention error.

### 10.2 The frozen result

**All five models met ordinary task readiness. None met complete
identity intervention support.**

| Registered assessment | Result |
|---|---:|
| Ordinary task readiness | **5/5 models** |
| Conditional ordinary base accuracy | 50/50 cells supported |
| Complete identity intervention support | **0/5 models** |
| Identity intervention MAE | 2 supported / 48 inconclusive / 0 violated cells |
| Identity near-decision disagreement | 3 supported / 6 inconclusive / 1 violated |
| Identity far-decision disagreement | 10/10 supported |
| Identity $0.01$ advantage over random-search control | 0 supported / 9 inconclusive / 1 violated |
| Identity $0.01$ advantage over permuted-concept search | 1/10 supported |
| Identity advantage over incorrect donors and untrained networks | 10/10 supported for each control |
| Complete support for each rival scale | 0/5 models |

For an 8,192-row $[0,1]$ mean, the simultaneous radius is
$0.0247260580$. An observed MAE must therefore be at most
$0.0252739420$ to establish the registered $0.05$ upper
tolerance. The absence of that support does not imply a lower
confidence bound exceeding the tolerance. This explains many
inconclusive cells, but the near-decision violation and failed
material advantage over random search also provide specifically
adverse evidence.

The rival-scale MAE supported/inconclusive/violated counts were
$0/46/4$ for inverse-$\eta$, $0/39/11$ for
inverse-$(1-\eta)$, and $9/41/0$ for inverse-total-cost.
No rival achieved complete support. These correlated criteria
are not independent votes for or against an absolute utility
representation.

The full preparation contains 25,600 candidate evaluations or
decoder fits. Final evaluation includes 409,600 intended pairs,
409,600 separately generated incorrect-donor records, 40,960
ordinary task examples and 8,192,000 alignment/role/pair
evaluations. These nested work counts should not be mistaken
for that many independently trained models.

### 10.3 Why a negative extraction result is plausible

**Ordinary prediction training gives the network no particular
reason to organize each expected cost into one clean
eight-neuron block.** Its loss constrains the output while
leaving many internal decompositions compatible with success.
The probe therefore tests whether a useful representation is
accessible to a particular extraction method, as well as whether
the network learned the task.

For example, (24) also gives

$$
\operatorname{logit}(p^*)
 =\log c_{\rm FN}-\log c_{\rm FP}
  +\log\eta-\log(1-\eta).
\tag{25}
$$

A computation organized around prices and probability odds need
not contain two separately swappable expected-cost blocks.
This is an available decomposition, not a finding that these
networks implement it. Mixed or distributed features, another
basis, and limits of the alignment search are plausible causes.
Technical superposition ([Elhage et al.](#ref-superposition)) is a relevant
research hypothesis, but
was not demonstrated in these four-input, 32-hidden-unit models.

The method belongs to the literature on interchange
interventions and distributed alignment
([Geiger et al., 2021](#ref-causal);
[Geiger et al., 2024](#ref-das)).
Probe controls help distinguish accessible information from
what the original computation uses
([Hewitt–Liang](#ref-probes)). The interpretation of successful
patching is itself a subject of technical disagreement
([Makelov et al.](#ref-illusion);
[Wu et al.](#ref-reply)).
Neither decodability nor a useful isolated intervention is,
by itself, a unique or jointly composable causal utility model.

### 10.4 What the later diagnostic adds

The separately frozen **F15-ND01** diagnostic used the same
five ordinary networks as development data. It tested
constructed known-structure calibration, search scope and
intervention masks. It neither reran the F15 confirmatory
challenge nor changed its endpoint.

In the constructed calibration, searched identity adequacy
passed for **5/5 layouts**: all 50 MAE upper-bound cells and
all 20 near/far decision cells were supported. Yet complete
identity support remained **0/5**, because the required
control-superiority conjunction still failed. Random and
permuted-concept controls could themselves find effective
interventions. Thus a known accessible structure does not
guarantee success on this particular complete endpoint.

On ordinary-network diagnostic validation, broader searches
and fractional masks improved intervention accuracy:

| Intervention family | Mean MAE | Near disagreement | Far disagreement | Point-adequate roles | Models with both roles point-adequate |
|---|---:|---:|---:|---:|---:|
| Original F15 subsets | .039626 | .354932 | .001062 | 3/10 | 0/5 |
| Exhaustive size-eight binary masks | .028251 | .291992 | .000085 | 9/10 | 4/5 |
| Rounded top eight from fractional masks | .029993 | .308508 | .000134 | 9/10 | 4/5 |
| Fractional masks with total mass eight | .025032 | .257288 | 0 | 10/10 | 5/5 |

These are development point criteria, not the simultaneous
confidence-and-control conjunction of F15. The favorable
fractional-mask row consequently does not replace the
original **0/5 complete-support** result.

The combined evidence makes a mundane interpretation plausible:
task learning succeeded, the original extraction restriction
was demanding, and the full endpoint also demanded separation
from capable optimized controls. More data might narrow
intervals; a richer extraction family might improve
interventions. Neither remedy alone establishes one joint
causal representation. The optional **F15-ND02** direction
would test joint two-cost assignments and their composition
under one fixed geometry, with calibration and matched
controls, using a new prospective protocol. It remains
deferred and unstarted.

*Original findings and every arm:*
[F15 neural assessment](v2/work_logs/F15_v1_run1/evaluation_attempt_1/neural_assessment.json)
and [complete report](v2/experiments/results.md).
*Diagnostic protocol, full tables and interpretation:*
[ND01 report](v2/experiments/F15_ND01_results.md)
and [diagnostic analysis](v2/experiments/F15_ND01_analysis/core_summary.json).

## 11. Contribution and relation to established work

### 11.1 The closest combined approach

The closest established approach combines quantitative program
reasoning, polyhedral optimization and incremental checked
abstractions. Incremental abstraction-carrying code already
retains analysis information and dependencies across updates
([Albert–Arenas–Puebla](#ref-acc)); polyhedral certificate
generation supplies a serious checked-arithmetic comparator
([Fouilhé–Monniaux–Périn](#ref-polyhedra)).
These are architectural antecedents, rather than capabilities
first established by the present implementation.

The contribution is a **modest synthesis and formal adaptation
with a specialized mathematical application**. For the stated
reset family, the report evaluates how price revision changes
exact information requirements, shows how actual new-order
means repair the missing information, and supplies sharp
uncertainty bounds with feasible witnesses. The explicit
endpoint/adjacent-level construction in Theorem 5 then returns
a compatible law at the unrestricted common minimax radius.
The resulting consequences for numerical prediction, action
choice and current-request justification are worked through
under the same source contract.

This is substantive local mathematical content beyond posing a
generic optimization problem. It remains available to an ordinary
implementation using the same information. Reproduction by that
implementation defeats an exclusive-capability or general-speed
claim; it does not remove the demonstrated application result.

### 11.2 Ingredients, adaptations and boundaries

| Area | Checked antecedent | What this report contributes or establishes |
|---|---|---|
| Value-oriented motivation | Ruspini's utility-relative logic; nonlinear desirability [Ruspini](#ref-ruspini), [Miranda–Zaffalon](#ref-desirability) | A chosen finite signed-loss interpretation with explicit source and action access; the motivation itself is inherited. |
| Candidate semantics | Abstract interpretation, probabilistic semantics and soft constraints [Cousot–Cousot](#ref-ai), [Kozen](#ref-kozen), [Bistarelli et al.](#ref-semiring) | Separating examples on a common information contract and a provisional fragment choice. |
| Quantitative consequence | Quantitative algebraic reasoning and Rational Lawvere Logic [Mardare et al.](#ref-qar), [Bacci et al.](#ref-rll) | Native signed budgets, successful-return soundness and the exact directed-unit characterization for the declared restricted calculus. |
| Retaining information for a language | Generalized strong preservation [Ranzato–Tapparo](#ref-preservation) | Evaluated information requirements for specified later cost requests, rather than a new general preservation principle. |
| Ordering and action selection | Min-sum ordering and minimax utility elicitation [Happach et al.](#ref-ordering), [Boutilier et al.](#ref-decision) | Revision sensitivity and source-conditioned acceptance; first fallback-relative certification is not claimed to solve a new ordering or minimax-regret problem. |
| Equal-price rank | Maximal-chain span, Theorem 3.4 [Gasanova–Nicklasson](#ref-chain) | Unequal-price kernel intersection, minimal new-mean repair and the following recovery calculation. |
| Recovering uncertain values | Polyhedral optimal recovery and relative Chebyshev centers [Ettehad–Foucart](#ref-recovery), [Paruchuri–Chatterjee](#ref-center) | The full-fiber compatible-radius equality, explicit law and source restrictions of Theorem 5. |
| Capacity identification | Linear Choquet parameter observations [Oliveira et al., 2017](#ref-choquet17) | A specified reset-cost translation; the close 2022 identifiability comparison remains incomplete. |
| Neural interpretation | Causal abstraction, distributed alignment and controlled probes [Geiger et al.](#ref-causal), [DAS](#ref-das), [Hewitt–Liang](#ref-probes) | A frozen expected-cost extraction challenge and a later diagnostic, with no complete support established. |

Full Rational Lawvere Logic has richer syntax and different
theorem assumptions. Its completeness results are not imported
as guarantees for the present Python checker. Likewise, the
mathematical rank of a retained observation map is not a lower
bound for every possible encoding, proof graph or program.

Generic optimal recovery already formulates the minimum worst
error for target values over a compatible polytope. Requiring
the returned values to come from one compatible source law
adds a constraint; a relative-center formulation can express
it. Theorem 5 proves an equality between those two optima for
a particular family and gives the attaining law. The
additional-source triangle shows why a separate proof is
needed.

### 11.3 Magnitude and comparison scope

The contribution is bounded by the stated fragment and inspected
comparisons. Its magnitude is a modest project-level application
and formal adaptation, with a concrete local recovery theorem.
The old exact summary generally has exponential dimension,
ordinary arithmetic reproduces the service, and the frozen
experiment does not demonstrate a deployment advantage.
These facts limit practical claims even where the mathematics
is sharp.

The comparison is not a claim of worldwide priority.
The technical identifiability theorem in the close 2022 Choquet
paper ([de Oliveira–Duarte–Romano](#ref-choquet22)) was not
obtained in the earlier comparison. Its accessible metadata,
abstract and partial introduction do not establish that it
contains or lacks the present delta. The accessible 2017
precursor and the inspected recovery statements also do not
prove absence from every related source.

The bounded synthesis/application claim is supported by the
specific construction and its consequences, not by failed
searches or the neural null. A later theorem-level displacement
would require revising that claim and comparing the surviving
question directly. The project’s
[comparison record](v2/literature/06_c4_contribution_comparison.md),
[adversarial reconstruction](v2/derivations/07_adversarial_review.md)
and [current source map](v2/work_logs/F17_2026-10-06_S1/reviews/literature_source_map.md)
preserve the exact inspected scope.

## 12. Claim dispositions and later questions

The evidence supports a conditional calculus and a specialized
application. The claims have different kinds of support:

| Claim | Kind of evidence | Disposition |
|---|---|---|
| Finite signed source semantics and permitted observations | Explicit definitions and countermodels | Chosen, revisable design |
| Accepted current-request proofs establish their declared comparison | Mathematical proof and bounded implementation correspondence | Supported at Theorem 1's contract |
| Every reduct-valid finite-budget query has a native proof | Constructive mathematical proof | Supported at Theorem 2's contract; bounded search need not find it |
| Boolean reasoning and specified earlier evidence consumers are represented | Exact translations and boundary witnesses | Supported for the stated fragments |
| Price revision has the ranks and minimal repair in §7 | Mathematical proofs under exact linear information | Supported under the stated reset assumptions |
| A compatible law attains the sharp common error | Explicit construction and complete linked envelope proof | Supported only for Theorem 5's full exact fibers |
| Revision usefulness meets the prospective criterion | Frozen exact-source challenge and saved-output audits | Supported on the stipulated population |
| General numerical, speed or total-memory superiority | Matched ordinary controls and cost records | Not established |
| Complete neural identity intervention support | Frozen simultaneous endpoint | Not established: 0/5 complete |
| Extracted expected-cost variables are a unique joint causal utility model | Individual interventions and later development diagnostics | Not established |
| Modest specialized synthesis/application | Explicit local consequences and bounded prior-work comparison | Supported at the stated comparison scope |
| Worldwide priority or broad real-world benefit | Incomplete worldwide/deployment evidence | Unestablished |

Three later questions would purchase different kinds of evidence.

**Practical acquisition under uncertain sources.** A design chunk
could replace exact old summaries with jointly uncertain old
observations and newly acquired information. The useful question
is whether selective retention changes decisions after charging
observation, state, repair and checking costs. The deferred
**F15-EXT-01** is a 90-minute research design target, balanced
between the new application and a serious ordinary comparator
with a prospective error/cost contract. It is not a promised
positive experiment.

**A closer theorem-level comparison.** If a concrete antecedent
displaces the stated difference, the named
**R-N01-01/F16-COMP60** comparison targets the exact translation of
the retention, repair and recovery statements into the closest
identification/recovery work. Its protected D30/L30 split
requires both mathematical and primary-source evidence. An
unread source does not count as a completed comparison.

**Joint neural semantics.** Optional **F15-ND02**, a separately
scoped 90-minute research chunk, could test two-cost
interventions with a common fixed geometry, two donors and
repeated assignments, alongside known-structure calibration and
matched controls. Its purpose would be to discriminate a
joint semantic explanation from effective individual output
edits. It is deferred, has not begun, and would need its own
prospective freeze. A richer representation search could also
be useful; success is a question for that study, not a conclusion
of this report.

The immediate next project step is a separate final report
audit. Completing this assembly does not preempt that audit or
turn any optional branch into a completed contribution.

## 13. Reproducibility and evidence provenance

### 13.1 Versions, environment and exposure

The accepted source baseline for this report is repository
commit `2e44ed1b711508d7ad451e1ca6272ff989deef81`.
Earlier scientific commits are:

| Artifact | Preservation commit |
|---|---|
| F14 prospective protocol | `5388a3f9b0f18ad4f4e33d7e0cd04ea38f03e43e` |
| Original F15 challenge | `9f42a047126618b0364cf334002f846e5839d726` |
| F15-ND01 diagnostic | `6ef27f20e3ac0920953a27dd84d6c91a021ba58f` |
| F16 reconstruction and compatible recovery | `de7b456d08f383e72dfcabd278c183db324fdf16` |

The experiments used Linux, CPython 3.12.14, NumPy 2.3.5,
binary64 neural computation and exact rational retention
arithmetic, with single-thread numerical libraries. No PyTorch
is required. The registered environment is CPython 3.12.x and
NumPy 2.3.5; the exact run record includes the observed
OpenBLAS version and thread count.

| Binding | SHA256 |
|---|---|
| F14-v1 manifest, 34 files | `b860021d3cb26705196b75d6b13277135d0c9220c266b21e05d7d11e719b2f9c` |
| F14-v1 configuration | `ea76f361eb1f2f055e6fa09096ba87fc5558bfe679982466e6de9543541d1918` |
| ND01 manifest, 47 files with five source-model bindings | `9c15af55b83d7edf134542a9c70bcc0f087c6f4f6491f993361a27493b5cf24c` |

Original F15 preparation completed at
**2026-10-05 03:46:15.790579 UTC**. All-five artifact validation
completed at **03:47:06.149535**, before the exposure marker
at **03:47:20.675387**. Evaluation completed at
**03:50:24.452339**. The original F14 runs, including full-count
development runs, remain development data.

The protocol allowed at most one unchanged retry per stage for
an unexplained failure, preserving completed units. F15 and
ND01 each completed their registered preparation and evaluation
stages on attempt one. Report assembly generated no final
population and did not train, select or evaluate another model.

### 13.2 Costs and recorded limitations

| Original F15 process | External wall seconds | Child CPU seconds | Peak child RSS, KiB |
|---|---:|---:|---:|
| Preparation | 7.628116 | 7.621769 | 44,020 |
| Evaluation | 184.274726 | 184.249148 | 248,364 |

These are process measurements, distinct from engaged research
time. Inner stage timers have narrower scope and are not added
to the external totals. The
[command records](v2/work_logs/F15_2026-10-04_S1/commands)
and [environment](v2/work_logs/F15_2026-10-04_S1/environment.json)
retain the full details.

One original aggregate is zero bytes although its sidecar names
a nonempty hash. All 160 individual retention units remain
intact. A separately preserved canonical recovery of
15,833,616 bytes matches the original SHA256
`0b0d9f79a7e74ddecef52bf5d20654eb433a5472d66cc3df63f84ae27dd04691`.
The damaged file was not overwritten. Original F15 sidecars
therefore match 180/181 with this explicit exception; ND01
sidecars match 103/103. See the
[storage-exception disposition](v2/experiments/results.md).

Historical Windows limitations also remain explicit: six older
dependency files had CRLF differences, three focused-suite
attempts ended in native access violations, and one frozen
dependency-path test has a separate deterministic
backslash/forward-slash portability defect. These were not
resolved by changing registered hashes or editing the frozen
test. Native crashes were not diagnosed as hardware failure.
The unchanged Linux F14-focused suite passed 78 tests; the
later Gate C focused regression passed 288. Neither is a
whole-repository or Windows certification.

### 13.3 Verifying saved results

From a clean Linux checkout with the recorded dependencies,
the following commands check existing artifacts without
generating a population or refitting an alignment:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1

python -m v2.experiments.freeze verify
python -m v2.experiments.summarize_f15 --check
python -m v2.experiments.neural_diagnostic_v1.runner verify
python v2/experiments/F15_ND01_analysis/summarize.py --check
python v2/reporting/build_f17_tables.py --check
```

The historical preparation/evaluation commands are retained in
the original results report. Completed attempt directories are
exposed data, so rerunning those stages is not a fresh
confirmatory experiment.

The [report table export](v2/reporting/F17_v1/tables.json) binds
its source files by SHA256 and distinguishes original
confidence outcomes from diagnostic point criteria.
The [claim map](v2/reporting/F17_v1/claim_map.json) identifies
the precise source and support type for each report claim.
The [F17 work record](v2/work_logs/F17_2026-10-06_S1.md) supplies
the actual assembly checks, review findings and timing;
the [claim ledger](v2/claim_ledger.md) remains the project-wide
record.

## 14. Attribution and writing method

Tristan Miano initiated and directs the Value Logic research
program. The source notes preserve the contributors and
assistant identities responsible for each research stage.
This report was assembled by **ChatGPT (GPT-6 Astra Pro)**,
with separately assigned mathematical, empirical and
literature reviewers of the same model. Their review is
internal and non-blind, not external peer review or
proof-assistant verification. Concurrent reviewer work is not
double-counted in the principal engaged-time ledger.

At the author's suggestion, the exposition draws on Scott
Armstrong and Amélie Loher's
[Mathematics Paper Skills](https://github.com/amelieloher/math-paper-skills/),
at revision `a542dbe5a70e6441b651bd659d93041558110136`,
licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The advice was adapted to this repository's Markdown report:
explain mechanisms before technical detail, keep theorem
contracts stable, use one canonical editor, and compare
important statements and proofs with their source notes.
No theorem or empirical criterion was changed to improve
the story.

## References

The separate [BibTeX file](v2/reporting/F17_v1/references.bib)
contains the bibliographic metadata. The
[source-access record](v2/work_logs/F17_2026-10-06_S1/reviews/source_access.json)
distinguishes current primary reads, earlier attributed reads
and unavailable technical material.

<a id="ref-ruspini"></a>

**Ruspini (1991).** Enrique H. Ruspini.
*Truth as Utility: A Conceptual Synthesis.* UAI, 316–322.
[Archival manuscript](https://arxiv.org/abs/1303.5744).

<a id="ref-ai"></a>

**Cousot and Cousot (1977).** Patrick Cousot and Radhia Cousot.
*Abstract Interpretation: A Unified Lattice Model for Static Analysis
of Programs by Construction or Approximation of Fixpoints.*
POPL, 238–252.
[Author record](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml).

<a id="ref-kozen"></a>

**Kozen (1981).** Dexter Kozen.
*Semantics of Probabilistic Programs.*
Journal of Computer and System Sciences 22(3), 328–350.
[Author manuscript](https://www.cs.cornell.edu/kozen/Papers/ProbSem.pdf).
DOI: 10.1016/0022-0000(81)90036-2.

<a id="ref-semiring"></a>

**Bistarelli, Montanari and Rossi (1997).** Stefano Bistarelli,
Ugo Montanari and Francesca Rossi.
*Semiring-Based Constraint Satisfaction and Optimization.*
Journal of the ACM 44(2), 201–236.
[DOI](https://doi.org/10.1145/256303.256306).

<a id="ref-qar"></a>

**Mardare, Panangaden and Plotkin (2016).** Radu Mardare,
Prakash Panangaden and Gordon Plotkin.
*Quantitative Algebraic Reasoning.* LICS, 700–709.
[Accepted manuscript record](https://strathprints.strath.ac.uk/70265/).
DOI: 10.1145/2933575.2934518.

<a id="ref-rll"></a>

**Bacci et al. (2026).** Giorgio Bacci, Radu Mardare,
Prakash Panangaden and Gordon Plotkin.
*Rational Lawvere Logic (Invited Paper).* CSL,
LIPIcs 363, 3:1–3:21.
[Official publication](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CSL.2026.3).

<a id="ref-desirability"></a>

**Miranda and Zaffalon (2022, v2).** Enrique Miranda and Marco Zaffalon.
*Nonlinear Desirability Theory.* arXiv:2209.00686v2,
18 November 2022.
[Inspected manuscript](https://arxiv.org/pdf/2209.00686).

<a id="ref-polyhedra"></a>

**Fouilhé, Monniaux and Périn (2013).** Alexis Fouilhé,
David Monniaux and Michaël Périn.
*Efficient Generation of Correctness Certificates for the Abstract
Domain of Polyhedra.* SAS, LNCS 7935, 345–365.
[Official chapter](https://link.springer.com/chapter/10.1007/978-3-642-38856-9_19).

<a id="ref-acc"></a>

**Albert, Arenas and Puebla (2006).** Elvira Albert,
Puri Arenas and Germán Puebla.
*An Incremental Approach to Abstraction-Carrying Code.*
LPAR, LNCS 4246, 377–391.
[Author manuscript](https://cliplab.org/papers/inc-acc-lpar06.pdf).
DOI: 10.1007/11916277_26.

<a id="ref-preservation"></a>

**Ranzato and Tapparo (2006, v3).** Francesco Ranzato
and Francesco Tapparo.
*Generalized Strong Preservation by Abstract Interpretation.*
arXiv:cs/0401016v3, 14 March 2006.
[Inspected manuscript](https://arxiv.org/pdf/cs/0401016v3).

<a id="ref-decision"></a>

**Boutilier et al. (2006).** Craig Boutilier, Relu Patrascu,
Pascal Poupart and Dale Schuurmans.
*Constraint-based optimization and utility elicitation using the
minimax decision criterion.* Artificial Intelligence 170, 686–713.
[Author manuscript](https://cs.uwaterloo.ca/~ppoupart/publications/elicConstraints/sdarticle.pdf).

<a id="ref-chain"></a>

**Gasanova and Nicklasson (2024).** Oleksandra Gasanova
and Lisa Nicklasson.
*Chain algebras of finite distributive lattices.*
Journal of Algebraic Combinatorics 59, 473–494.
[Official article, Theorem 3.4](https://link.springer.com/article/10.1007/s10801-023-01294-8).

<a id="ref-ordering"></a>

**Happach, Hellerstein and Lidbetter (2022).** Felix Happach,
Lisa Hellerstein and Thomas Lidbetter.
*A General Framework for Approximating Min Sum Ordering Problems.*
INFORMS Journal on Computing 34(3), 1437–1452.
[Author manuscript](https://arxiv.org/html/2004.05954v2).
DOI: 10.1287/ijoc.2021.1124.

<a id="ref-recovery"></a>

**Ettehad and Foucart (2021).** Mahmood Ettehad and Simon Foucart.
*Instances of Computational Optimal Recovery: Dealing with
Observation Errors.*
SIAM/ASA Journal on Uncertainty Quantification 9(4), 1438–1456.
[Author manuscript, §2.1 and Theorem 1](https://foucart.github.io/publi/OR_Uncertainty_v2.pdf).
DOI: 10.1137/20M1328476.

<a id="ref-center"></a>

**Paruchuri and Chatterjee (2023, v1).** Pradyumna Paruchuri
and Debasish Chatterjee.
*A numerical algorithm for attaining the Chebyshev bound
in optimal learning.* arXiv:2307.01304v1, 3 July 2023.
[Inspected version](https://arxiv.org/html/2307.01304v1).

<a id="ref-choquet17"></a>

**Oliveira, Romano and Duarte (2017).** Henrique E. Oliveira,
João M. T. Romano and Leonardo T. Duarte.
*Identificação dos Parâmetros da Integral de Choquet via uma
Abordagem baseada em Processamento de Sinais Esparsos.*
SBrT, 692–696.
[Proceedings paper](https://www.sbrt.org.br/sbrt2017/anais/1570362091.pdf).

<a id="ref-choquet22"></a>

**de Oliveira, Duarte and Romano (2022).** Henrique Evangelista
de Oliveira, Leonardo Tomazeli Duarte and João Marcos
Travassos Romano.
*Identification of the Choquet integral parameters in the
interaction index domain by means of sparse modeling.*
Expert Systems with Applications 187, 115874.
[Publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0957417421012331).
The substantive identifiability theorem was unavailable in
the recorded comparison.

<a id="ref-causal"></a>

**Geiger et al. (2021).** Atticus Geiger, Hanson Lu,
Thomas Icard and Christopher Potts.
*Causal Abstractions of Neural Networks.* NeurIPS 34.
[Official proceedings](https://proceedings.neurips.cc/paper/2021/hash/4f5c422f4d49a5a807eda27434231040-Abstract.html).

<a id="ref-das"></a>

**Geiger et al. (2024).** Atticus Geiger, Zhengxuan Wu,
Christopher Potts, Thomas Icard and Noah Goodman.
*Finding Alignments Between Interpretable Causal Variables
and Distributed Neural Representations.*
CLeaR, PMLR 236, 160–187.
[Official proceedings](https://proceedings.mlr.press/v236/geiger24a.html).

<a id="ref-probes"></a>

**Hewitt and Liang (2019).** John Hewitt and Percy Liang.
*Designing and Interpreting Probes with Control Tasks.*
EMNLP-IJCNLP, 2733–2743.
[Official proceedings](https://aclanthology.org/D19-1275/).

<a id="ref-superposition"></a>

**Elhage et al. (2022).** Nelson Elhage and collaborators.
*Toy Models of Superposition.* Transformer Circuits,
14 September 2022.
[Author manuscript](https://transformer-circuits.pub/2022/toy_model/toy_model.pdf).

<a id="ref-illusion"></a>

**Makelov et al. (2024).** Aleksandar Makelov, Georg Lange,
Atticus Geiger and Neel Nanda.
*Is This the Subspace You Are Looking For? An Interpretability
Illusion for Subspace Activation Patching.* ICLR.
[Final conference paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/70b8505ac79e3e131756f793cd80eb8d-Paper-Conference.pdf).

<a id="ref-reply"></a>

**Wu et al. (2024, v1).** Zhengxuan Wu, Atticus Geiger,
Jing Huang, Aryaman Arora, Thomas Icard, Christopher Potts
and Noah D. Goodman.
*A Reply to Makelov et al. (2023)'s “Interpretability Illusion”
Arguments.* arXiv:2401.12631v1, 23 January 2024.
[Inspected version](https://arxiv.org/html/2401.12631v1).

<a id="ref-hoeffding"></a>

**Hoeffding (1963).** Wassily Hoeffding.
*Probability Inequalities for Sums of Bounded Random Variables.*
Journal of the American Statistical Association 58(301), 13–30.
[Paper, Theorem 2](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).
DOI: 10.1080/01621459.1963.10500830.
