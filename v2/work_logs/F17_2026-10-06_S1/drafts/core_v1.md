# Value Logic: Loss Comparisons and Information Retention Under Revision

Tristan Miano

Research report, October 2026. Assembly and current internal review:
**ChatGPT (GPT-6 Astra Pro)**. Detailed attribution appears in the final section.

## Abstract

<!-- F17: abstract is assembled after the checked body. -->

## 1. Introduction

<!-- F17: introduction is assembled after the checked body. -->

## 2. Choosing what a value expression means

A numerical score answers a particular question about a plan. It need not
retain the information needed for the next question. Suppose a fair binary
variable $`X`$ is paired either with $`Y=X`$ or with $`Y=1-X`$. Both pairs have
the same marginal means. Nevertheless, their expected maxima are $`1/2`$ and
$`1`$, respectively. Their expected minima are $`1/2`$ and $`0`$. Thus two
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

```math
\mathrm{res}(a,b)=\max(b-a,0).
```

A term has a finite real value at every assignment. Its range over possible
assignments can still be unbounded. Variable multiplication, literal
infinities and recursive term bindings are outside this fragment. In
particular, an application parameter fixed when a query is issued is not
silently promoted to a second unknown multiplied by a source variable.

At a fixed visible observation, the context $`\mathcal C`$ supplies a
nonempty finite family of cases,

```math
D_{\mathcal C}
 =\bigcup_{h\in H}\{(h,x):A_hx\le \eta_h\}.
```

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

Let $`t`$ denote the new loss and $`s`$ the old loss, in the same unit $`u`$.
For a rational budget $`b`$, define

```math
\mathcal C\models t\le_b s:u
\quad\Longleftrightarrow\quad
\forall(h,x)\in D_{\mathcal C},\quad t_h(x)-s_h(x)\le b.
\tag{1}
```

The executable fragment uses one literal expression pair across its cases.
A negative budget is a guaranteed modeled improvement, zero is
non-deterioration, and a positive budget allows an increase. Absolute
adequacy is a separate comparison with zero; relative improvement alone
does not supply it.

The best semantic upper bound is the metalevel quantity

```math
B_{\mathcal C}(t,s)
 =\sup_{(h,x)\in D_{\mathcal C}}\bigl(t_h(x)-s_h(x)\bigr)
 \in\mathbb R\cup\{+\infty\}.
\tag{2}
```

It is not an expression-language primitive or an oracle available to a
proof. A feasible case and assignment with difference greater than $`b`$
is a countermodel within the declared source. Failure of a bounded search
to find a proof is a different outcome.

Clipping to nonnegative deterioration loses useful information:

```math
\sup_{D_{\mathcal C}}\mathrm{res}(s,t)
 =\max\bigl(B_{\mathcal C}(t,s),0\bigr).
\tag{3}
```

For $`b\ge0`$, bounding this shortfall is equivalent to (1). For $`b<0`$
the equivalence fails. Even a strict improvement has nonnegative shortfall,
so its improvement margin must remain in the signed comparison.

### 3.3 Permitted actions and observations

A loss formula can depend on an unknown source coordinate without making
that coordinate available to a policy. At one visible observation, the
same permitted policy must be used across every compatible hidden case.
The relevant order of quantifiers is

```math
\exists\ \text{permitted policy }\pi\;
\forall\ (h,x)\text{ compatible with the observation}.
\tag{4}
```

For example, consider two hidden cases in which the costs of two actions
are $`(0,2)`$ and $`(2,0)`$. The pointwise minimum is zero. A fixed policy
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

Write $`\mathcal C;h\vdash t\le_b s`$ for a finite derivation in a named
case. Every premise in a rule refers to the same context and compatible
units unless an explicit conversion is applied. The table groups the
sixteen implemented instruction tags by their mathematical role.

| Role | Rule or condition |
|---|---|
| Constant and source | Prove an exactly normalized constant difference, or use an actual source row with its offset and budget. |
| Exact rewriting | Replace a pair only when its normalized difference is unchanged. |
| Transitivity | From $`t\le_b s`$ and $`s\le_c r`$, derive $`t\le_{b+c}r`$. |
| Addition | From $`t_i\le_{b_i}s_i`$, derive $`t_1+t_2\le_{b_1+b_2}s_1+s_2`$. |
| Scaling and conversion | Multiply expressions and budget by a nonnegative rational or the declared positive conversion factor. |
| Polarity reversal | From $`t\le_b s`$, derive $`-s\le_b -t`$. |
| Slack | Add only a fixed nonnegative allowance to the budget. |
| Combining proofs | Two proofs of the same difference at $`b,c`$ give the budget $`\min(b,c)`$. |
| Lattice rules | Use the min projections, max injections, and common-target min/max comparisons. |
| Min/max congruence | Two component bounds $`b,c`$ give the bound $`\max(b,c)`$ for either pointwise min or max. |
| Residual congruence | Reverse the first argument's comparison and clip the summed allowance at zero. |
| All cases | Prove the same literal pair in every live case and take the maximum case budget. |

Addition uses a common assignment before taking a bound; it needs no
independence assumption. If both losses contain the same source term
$`z`$, exact rewriting can cancel $`z`$ from their difference even when
$`z`$ is unbounded. It cannot cancel distinct coordinates merely because
they happen to have similar values.

For min/max congruence, put $`d=\max(b,c)`$. Both component inequalities
imply bounds with the same additive allowance $`d`$. Monotonicity and
translation invariance give

```math
F(t_1,t_2)
 \le F(s_1+d,s_2+d)
 =F(s_1,s_2)+d,\qquad F\in\{\min,\max\}.
\tag{5}
```

This argument also applies to negative budgets. If one argument remains
unchanged, the common budget is $`\max(b,0)`$: saturation can erase a
strict component improvement.

Residual polarity requires particular care. From

```math
a_{\rm old}\le_p a_{\rm new},
\qquad
b_{\rm new}\le_q b_{\rm old},
```

one obtains

```math
\mathrm{res}(a_{\rm new},b_{\rm new})
 \le_{\max(p+q,0)}
\mathrm{res}(a_{\rm old},b_{\rm old}).
\tag{6}
```

The preactivation changes by
$`(b_{\rm new}-b_{\rm old})+(a_{\rm old}-a_{\rm new})`$; the unchanged
zero branch then contributes the clipping. Using the opposite comparison
in the first argument would be unsound.

### 4.2 Reuse after source revision

An old proof is a conditional argument, not an unconditional stored answer.
To reuse it under a new source, substitute source terms in a type-correct
way and prove the substituted old row directions in every current case.
The receiver checks the resulting current request. Matching an old
fingerprint or copying an old numerical budget is insufficient.

A related construction makes the cost of withdrawing assumptions explicit.
For an old localized proof, replace a withdrawn row allowance $`\eta_i`$
by

```math
\eta_i+\max(a_i(x)-\eta_i,0).
```

Replaying the proof's monotone budget operations produces a pointwise
allowance $`E_P(x)`$. On the retained domain,

```math
t(x)-s(x)\le E_P(x)=b_P+R_P(x),\qquad R_P(x)\ge0.
\tag{7}
```

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
given request. A root budget $`b_{\rm out}\le B`$ discharges an inclusive
request at $`B`$; a strict request requires $`b_{\rm out}<B`$.
The bound consequently applies to the actual requested pair and domain.
$`\square`$

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

Let $`A(u)`$ contain the units with a directed conversion path to $`u`$,
including the path of length zero. The **target-unit reduct**
$`\mathcal C|u`$ retains exactly the rows whose unit lies in $`A(u)`$.
It keeps the signature, case identities and feasible witnesses. Removing
rows preserves each case's nonemptiness.

Let $`K_{\mathcal C}(t,s;b)`$ mean that a finite native proof exists with
exactly the global pair $`t,s`$, in unit $`u`$, and root budget at most
the rational number $`b`$. This is mathematical proof existence, without
an implementation's search or size caps.

**Theorem 2 (unit-directed completeness).** For the finite rational typed
fragment and contexts of §3, and one common literal query pair,

```math
K_{\mathcal C}(t,s;b)
\quad\Longleftrightarrow\quad
\mathcal C|u\models t-s\le b.
\tag{8}
```

If the optimal reduct bound is finite, it is rational and is attained by
both a finite native proof and a rational reduct model. If the bound is
$`+\infty`$, no finite native budget exists.

**Proof structure.** Trace the root's ancestors. Every premise edge
preserves the inequality unit or follows a declared conversion. Hence
every used source row survives in the reduct. Apply the soundness
induction in the separate reduct cases, then aggregate their union.
This proves the forward implication.

For the converse, transport accessible rows along positive conversion
paths and certify the retyping of the query in unit $`u`$. Conversion
through min/max needs derived equalities, not an assumed inverse map.
Refine the finite expression into affine sign cells. Rational linear
elimination supplies feasible witnesses or strict infeasibility rays,
and exact nonnegative row multipliers for affine upper bounds. A finite
optimum is rational and attained, even when nuisance coordinates are
unbounded or the source has no vertex.

The temporary sign assumptions can be removed using the existing
withdrawal construction and a source-free disjoint-hinge identity.
Opposite guards give allowances proportional to
$`\max(g,0)`$ and $`\max(-g,0)`$; their suitably weighted minimum vanishes.
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
$`\square`$

**Why full-source completeness can fail.** Take units $`U,V`$, one
factor-one conversion $`U\to V`$, and a source $`x:U`$. The single case
has the $`V`$-row $`\mathrm{convert}(x)\le-1_V`$, with witness
$`x=-1`$. The $`U`$-request $`x\le_{-1}0_U`$ is valid in the full real
semantics. Its $`U`$-reduct has no rows; $`x=0`$ refutes the request
there. Equation (8) proves native nonderivability. This is a structural
boundary, not merely a failed search.

For a fixed conversion graph, full-source completeness uniformly over
source declarations and $`u`$-queries holds exactly when every unit in
$`u`$'s weak component reaches $`u`$. For all target units, each weak
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
| $`\top,\bot`$ | $`0,1`$ |
| $`\neg A`$ | $`1-L(A)`$ |
| $`A\land B`$ | $`\max(L(A),L(B))`$ |
| $`A\lor B`$ | $`\min(L(A),L(B))`$ |
| $`A\Rightarrow B`$ | $`\mathrm{res}(L(A),L(B))`$ |

Let $`P_\Gamma=\max_{A\in\Gamma}L(A)`$, taking zero for no premises,
and let $`\mathcal C_B`$ consist of all Boolean valuations as finite
point cases in one unit. Then

```math
\Gamma\models_{\rm CL}B
\quad\Longleftrightarrow\quad
\mathcal C_B\models L(B)\le P_\Gamma
\quad\Longleftrightarrow\quad
K_{\mathcal C_B}(L(B),P_\Gamma;0).
\tag{9}
```

If all premises hold, $`P_\Gamma=0`$, so the comparison requires $`B`$.
Otherwise $`P_\Gamma=1`$, and the comparison is automatically true.
Theorem 2 supplies the last equivalence. Premises are encoded in the
query, so inconsistent premises retain classical entailment without an
inadmissible empty source.

This is an exact fragment, not an identification of arbitrary numerical
loss with truth. On the interval $`[0,1]`$, the excluded-middle
expression has loss $`\min(x,1-x)=1/2`$ at $`x=1/2`$. Addition also
leaves the Boolean carrier.

### 6.2 Relation to the first-stage reliance calculus

The earlier report concerned present permission to rely on a fallible
model under a domain, task loss, tolerance, fallback, profile and
provenance. Its assessment states were refuted, open and supported.
Their meet algebra embeds as the constant losses $`1,1/2,0`$, with
maximum combining requirements. The value $`1/2`$ here is a status
code, not the probability that a claim is true or the expected cost
of acting on an open claim.

The stronger connection is through explicit evidence consumers. For
an admitted interval $`[l,u]`$ and threshold $`\tau`$, the original
consumer supports the requirement when $`u\le\tau`$, refutes it when
$`l>\tau`$, and otherwise leaves it open. Finite rectangles and
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
expression pair. Preserving all rational difference-budget tests is
stronger than preserving order and forces an affine numerical map
with positive scale. A bounded monotone recoding alone does not
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

There are $`k\ge2`$ reset procedures. A world $`w\subseteq[k]`$ records
which procedures would fail on one fixed request. Its law $`p`$ is arbitrary
on the full $`2^k`$-world simplex. An order $`\pi`$ tries each procedure
until the first success, paying strictly positive rational attempt
prices $`c_i`$, and terminal penalty $`M\ge0`$ if all fail. Write

```math
m_S=\Pr(S\subseteq w),\qquad m_\varnothing=1.
```

Then the mean cost is

```math
C_\pi(c,M)
 =\sum_{j=1}^k c_{\pi_j}
     m_{\{\pi_1,\ldots,\pi_{j-1}\}}
   +M m_{[k]}.
\tag{10}
```

All permutations are allowed. The outcome law is unchanged when prices
change; stateful procedures or edits that change outcomes require a
different source contract. Prices are fixed parameters of each query, so
(10) is affine in the moment coordinates admitted by the native language.

An exact linear summary stores linear measurements of the law, with
arbitrary decoding allowed afterward and known constants free. Its
dimension is a linear-information requirement. It is not a number of
bits, a finite-sample guarantee, or a lower bound for arbitrary
nonlinear real encodings.

### 7.2 Two price profiles and minimal repair

Put $`n=2^k-1`$, the simplex direction dimension. The following results
evaluate the rank of the requested family of linear functionals.

**Theorem 3 (retention under price revision).** For one strictly positive
price profile and any $`M\ge0`$, all order means have exact linear rank
$`2^k-k`$; all within-profile order differences have rank $`n-k`$.
For two nonproportional strictly positive profiles $`(c,M),(d,N)`$,
with $`M,N\ge0`$, the ranks are:

| Requested values | Rank |
|---|---:|
| All numerical means at both profiles | $`n`$ if $`M>0`$ or $`N>0`$; otherwise $`n-1`$ |
| All within-profile order differences | $`n-1`$ |
| All differences, also allowing cross-profile comparisons | $`n`$ if $`M\ne N`$; otherwise $`n-1`$ |

**Proof.** Work in moment directions $`v`$, with $`v_\varnothing=0`$.
An adjacent swap of $`a,b`$ after prefix $`S`$ changes the directional
mean by

```math
(c_a-c_b)v_S+c_bv_{S\cup\{a\}}-c_av_{S\cup\{b\}}.
\tag{11}
```

These swaps connect all orders. Their simultaneous zero set on proper
subsets has the form

```math
v_A=\sum_{r=1}^{|A|}t_r e_r(c_A),
\qquad \varnothing\ne A\subsetneq[k],
\tag{12}
```

where $`e_r`$ is the elementary symmetric polynomial and
$`t_1,\ldots,t_{k-1}`$ are free. To obtain (12), the empty-prefix
swap first makes $`v_i/c_i`$ constant. At each next subset size,
subtract the already determined lower-degree terms. The residual,
divided by the product of that subset's prices, is constant across
one-element exchanges; the graph of subsets of fixed size is
connected. The elementary-symmetric recurrence verifies the converse.

The full-set direction is separately free. The common directional
mean equals

```math
\sum_{r=1}^{k-1}t_r e_{r+1}(c_{[k]})+Mv_{[k]}.
\tag{13}
```

Its proper-coordinate functional is nonzero because $`e_2(c)>0`$.
Thus differences have a $`k`$-dimensional kernel, and numerical
means impose one additional independent constraint. This proves the
single-profile ranks.

Now require (12) for both $`c`$ and $`d`$. At subset size one,
nonproportionality forces both leading coefficients to vanish.
Inductively, if a nonzero coefficient first survived at size $`r`$,
the products $`\prod_{i\in A}(d_i/c_i)`$ would be constant over all
$`r`$-subsets. Comparing two subsets that differ in only one member
forces every ratio $`d_i/c_i`$ to agree, a contradiction. All proper
directions therefore vanish. The remaining full-set direction has
numerical values $`Mv_{[k]}`$ and $`Nv_{[k]}`$, and cross-profile
difference $`(M-N)v_{[k]}`$, giving the table.

Finally, small opposite perturbations of an interior law realize
the surviving null directions as feasible indistinguishable laws.
A lower-dimensional retained linear map cannot distinguish their
different requested values, even with an arbitrary decoder.
$`\square`$

The equal-price rank has a direct maximal-chain-span antecedent:
Gasanova and Nicklasson's Theorem 3.4 supplies the corresponding
$`|L|-|P|`$ dimension for a finite distributive lattice
([Gasanova–Nicklasson](#ref-chain)). The price-dependent kernel and
its intersection, evaluated here for the reset consumer, are the
relevant extension.

**Theorem 4 (repair by actual new means).** Start with a minimum-rank
exact summary of all old numerical means with $`c_i>0`$ and $`M>0`$.
Change one price to $`c_j+\varepsilon>0`$, where
$`\varepsilon\ne0`$, keeping $`M`$ and the law fixed. Exactly
$`k-1`$ additional independent linear measurements suffice and are
necessary in the worst case to recover the full law. They can be
$`k-1`$ actual new-order means.

**Proof.** Choose nested prefixes
$`P_1\subset\cdots\subset P_{k-1}=[k]\setminus\{j\}`$. An order
placing exactly $`P_r`$ before $`j`$ has new-minus-old mean

```math
C_{\pi_r}(c+\varepsilon e_j,M)-C_{\pi_r}(c,M)
 =\varepsilon m_{P_r}.
\tag{14}
```

Its old mean is available from the summary. The new measurements
therefore recover the $`k-1`$ chain moments. In the canonical
summary associated with this chain, equation (12) gives triangular
equations for the missing coefficients $`t_r`$, with positive
diagonal $`\prod_{i\in P_r}c_i`$. The retained residuals recover all
proper moments, and an old mean recovers $`m_{[k]}`$ by division
by $`M`$. Any exact summary of all old means also determines this
canonical summary.

Conversely, the old-summary kernel has dimension $`k-1`$. Fewer
than $`k-1`$ additional linear responses leave a nonzero direction.
At an interior law, small opposite perturbations remain feasible.
For deterministic adaptive queries, fix the transcript at that law:
the perturbations preserve each answer, so induction preserves
every subsequent query choice. The two laws remain indistinguishable.
$`\square`$

If $`M=0`$, no full-order mean sees $`m_{[k]}`$, whatever the prices.
The proper moments can instead be recovered with $`k-2`$ new means.
Proportional price families and additional known marginals have
separate classifications in the
[full retention derivation, §§4–8](v2/derivations/09_c4_price_revision.md).

### 7.3 Exact fragility and decision stability

An arbitrarily small nonproportional price edit can require the
maximal exact numerical information. This does not imply a large
practical change. Pathwise, a one-price edit changes every order's
cost by a number in

```math
[\min(0,\varepsilon),\max(0,\varepsilon)].
\tag{15}
```

An old-optimal policy therefore has new-price regret at most
$`|\varepsilon|`$ for the stated common mean, fixed-level CVaR or
worst-source objective. Compare its new value with its old value
plus the upper endpoint, use old optimality, and compare the
new-optimal policy's old value with its new value minus the lower
endpoint. The interval width is the regret bound.

Likewise, the old mean plus $`\varepsilon/2`$ has a universal
absolute error bound $`|\varepsilon|/2`$ for a revised mean.
An exact information lower bound consequently does not force
maximal memory for an approximate or action-only request.

Equation (14) also clarifies a statistical distinction. Dividing
two separately perturbed aggregate means by a small
$`\varepsilon`$ can amplify their errors. If both prices are
evaluated on the same retained world traces, their pathwise
difference is $`\varepsilon`$ times a reach indicator, so the
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
means, with fixed $`k\ge2`$ and $`M\ge0`$. The source is the full
nonempty set of Boolean laws compatible with that summary, without
additional law restrictions.

For $`h<k`$, set
$`g_h=(k+1)/(k+1-h)`$, and set $`g_k=k+M`$.
These are the old costs averaged over all orders on a world with
$`h`$ failures. A canonical summary retains the probability
contrasts within each Hamming level and

```math
B=\sum_w g_{|w|}p_w.
```

There are $`2^k-k`$ such coordinates. In each level subtract the
minimum contrast, including the reference world's zero contrast,
to obtain fixed nonnegative residues $`\rho_w`$. Put

```math
R=1-\sum_w\rho_w,\qquad
B_{\rm rem}=B-\sum_w g_{|w|}\rho_w.
```

If $`R=0`$, the law is already determined. If $`R>0`$, every
compatible law has exactly the representation

```math
p_w=\rho_w+\frac{R q_{|w|}}{\binom{k}{|w|}},
\qquad
q_h\ge0,\quad \sum_hq_h=1,\quad
\sum_h g_hq_h=\mu=\frac{B_{\rm rem}}R.
\tag{16}
```

This allows nonexchangeable residue offsets. Only the remaining
uncertainty is expressed by a distribution on the $`k+1`$
failure-count levels. For $`1\le r\le k-1`$, define
$`f_r(h)=\binom hr/\binom kr`$; a proper-prefix moment has a fixed
residue contribution plus $`R\mathbb E_qf_r`$.

**Theorem 5 (compatible common-radius recovery).** Under these
assumptions, define

```math
\alpha=\frac{\mu-1}{k+M-1},\qquad
q^-=(1-\alpha)e_0+\alpha e_k.
```

Let $`q^+`$ be the mixture on adjacent $`g`$-levels bracketing
$`\mu`$, with mean $`\mu`$, and put
$`\beta=\mathbb E_{q^+}f_1`$. The law obtained from

```math
q^*=\tfrac12(q^-+q^+)
\tag{17}
```

through (16) attains the unrestricted minimum common maximum
absolute error over all proper-prefix moments. The conditional
radius is

```math
r(\mathcal C)=\frac R2(\beta-\alpha).
\tag{18}
```

For any separately applied single-price edit
$`\varepsilon`$ with $`1+\varepsilon>0`$, the revised-order mean
radius is $`|\varepsilon|r(\mathcal C)`$. The same decoded law
works for each such edit. A bounded collection whose supremum
edit magnitude is $`E`$ has common worst error $`Er(\mathcal C)`$.

**Proof and its nontrivial step.** The endpoint law $`q^-`$
minimizes the singleton expectation, giving $`\alpha`$. The
polygonal curve $`(g_h,h/k)`$ is concave, so the adjacent-level
law $`q^+`$ maximizes it, giving $`\beta`$. These two extremes
force error at least $`(\beta-\alpha)/2`$ before scaling by $`R`$.

For every $`r`$, let $`L_r,U_r`$ be the extrema of
$`\mathbb E_qf_r`$ under the constraints in (16), and write
$`B_r=\mathbb E_{q^+}f_r`$. The family-specific envelope argument
establishes both inequalities

```math
2U_r\le\beta+B_r,\qquad
2L_r\ge2\alpha+B_r-\beta.
\tag{19}
```

The candidate coordinate is $`(\alpha+B_r)/2`$. Equation (19)
puts its distance to both endpoints at most
$`(\beta-\alpha)/2`$, simultaneously for all $`r`$.
The residues add fixed constants and $`R`$ scales the uncertainty.
Thus one compatible law attains the lower bound. Equation (14)
then scales the bound for every revised-order mean; all proper
prefixes occur among the available orders.

The substantive proof of (19) is retained in
[the complete envelope derivation, §§3–7](v2/derivations/10_f16_coherent_recovery.md).
It reduces the inequalities to the knots $`g_j`$, proves the
upper bounds using the polygonal concave envelope, and proves
the lower bounds through an affine envelope and the separate
$`M=0`$, $`M>0`$ cases. Equation (19) is not a consequence of
generic convexity alone. This paragraph gives the construction
and reduction; the linked note supplies the full binomial
inequality proof.
$`\square`$

Taking the worst case over all exact old-summary fibers gives
the sharp global revised-mean radius

```math
\frac{|\varepsilon|}{2}
\max_{1\le j\le k-1}
\left[
\frac jk-\frac{j}{(k-j+1)(k+M-1)}
\right].
\tag{20}
```

The maximum requires $`O(k)`$ scalar arithmetic operations.
This excludes reading the generally exponential-size summary,
computing its residues, materializing a law, and generating or
checking a native certificate. At $`k=3,M=4`$, the radius is
$`|\varepsilon|/4`$. For the frozen small edit
$`|\varepsilon|=1/40`$, it is $`1/160`$, compared with the
ordinary universal bound $`1/80`$. Both already satisfy the
experiment's numerical tolerance $`1/20`$. The factor-two
improvement here is an exact bound, not evidence of a new
successful decision or a speed advantage.

**The limit of the theorem matters.** One common radius does not
require every coordinate to be its own interval midpoint.
At $`k=4,M=1/10`$, zero contrasts and $`B=9/8`$ yield individual
midpoints

```math
m_1=41/496,\qquad m_2=1/48,\qquad m_3=5/248,
```

where subscripts indicate subset size. Together with the old
mean they force a negative probability $`-3/496`$ for each
two-failure world. Yet a compatible common-radius optimum still
exists by Theorem 5. The earlier three-procedure midpoint
warning was corrected: in that exact equal-price family with
$`M>0`$, the proper-coordinate midpoints are compatible.

Additional source restrictions can change the result. The
[explicit convex-source triangle](v2/derivations/10_f16_coherent_recovery.md#10-additional-convex-source-restrictions-can-create-a-coherence-penalty)
has unrestricted moment radius $`1/400`$ and compatible radius
$`1/300`$. Noisy old observations, simultaneous price edits,
changed terminal penalty and arbitrary new moment combinations
are also outside Theorem 5. A compatible decoded law is an
estimate with a stated query error; it is not new exact source
knowledge.

*Complete retention, repair and interval proofs:*
[price-revision analysis](v2/derivations/09_c4_price_revision.md).
*Compatible-law construction, sharp bound and adverse cases:*
[coherent recovery](v2/derivations/10_f16_coherent_recovery.md).

