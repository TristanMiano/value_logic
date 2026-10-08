# P3-04 — Finite counterfactual semantics

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 8, 2026 UTC.
Status: **IN PROGRESS — Research90 and closing review are not yet complete**.
Base: `688ff3b6c2f10a70d83c58a9ca7610cd32cb5e21`.
[Session](../work_logs/P3_04_2026-10-08_S1.md) ·
[Primary comparisons](../literature/04_source_contracts.md) ·
[Selection and refinement extensions](04_selection_extensions.md).
All executable evidence is DEVELOPMENT. P3-05 and P3-B are not selected.

## 1. Answer and provisional choice

A numerical loss does not determine what a counterfactual changes. We use a
**typed, finitely specified hypothetical request** whose cases, exceptions,
ranking and outcome interpretation are visible. The provisional construction
has ordinary structural and model-repair adapters, plus a deliberately limited
nonclassical adapter for genuinely impossible antecedents. A common ranked
constraint interface handles selection and loss queries. That common interface
does not erase the differences between the adapters.

For the genuine counterpossible adapter, the exact original sentence and its
ordinary interpretation remain fixed. Hypothetical evaluation is explicitly
Belnap–Dunn paired support on a finite propositional fragment. Atomic normality
constraints are relaxed only where permitted by the request; all connectives
retain the specified compositional rules. Atomic exceptions propagate to compound support formulas by those fixed rules.
The selected support states are not ordinary mathematical worlds, and the resulting cost is not the probability
that a contradiction occurs. This is a finite adaptation of familiar machinery,
not a claim that Value Logic has discovered a uniquely correct counterpossible
semantics. The choice remains revisable.

Three distinct tasks must not be conflated:

1. Define which hypothetical cases the question means.
2. Compute enough information about those cases to answer its query.
3. Defend why that question and its relevance preferences are useful.

The first two can have conditional finite proofs. The third is not settled by
a self-consistent implementation or by relabelling a favorable outcome as the
nearest one. P3-N01 remains **NOT YET SUPPORTED**.

## 2. Exact request and response contracts

A request records the following fields, building on
[P3-01 section 7](../foundations/01_problem_contract.md#7-a-typed-counterfactual-request):

| Field | Meaning |
|---|---|
| Base scope | Fixed language, interpretation, theory, actual history and program versions |
| Quoted antecedent | The original formula or program assertion, not a revised paraphrase |
| Operation tag | Conditioning, occurrence intervention, actor-only or shared replacement, model repair, or counterpossible evaluation |
| Candidate grammar | Finite domains, structural equations or formula support rules, and its construction cost |
| Hard commitments | Inalterable structure, history, frame facts and evaluation rules |
| Permitted exceptions | Named replaceable components or defeasible semantic constraints |
| Ranking | A specified comparison rule for changes; this is not task loss or computation expense |
| Tie semantics | All minimizers by default; an explicit policy may choose among them |
| Interpretation map | How a hypothetical label, variable, cost or action relates to the original query |
| Consumer service | A loss set, outer interval, uniform comparison, or explicitly chosen action policy |
| Search contract | Available operations, budget, coverage, witnesses and checked bounds |

The mathematical specification below permits a finite known rational loss
profile; no global bound on all future requests is assumed. The executable
fragment is narrower and reports that difference. A numerical carrier is not
chosen as the metaphysical type of every possible value.

A response separates **domain feasibility**, **search coverage**, **optimal rank**,
**coverage of minimizing alternatives**, and **query certainty**. For example:

- A feasible candidate can prove that the finite optimum family exists without
  proving that this particular candidate is optimal.
- A candidate attaining a global rank lower bound can prove optimum rank without
  exhausting the other minimizers.
- A certified singleton loss bound over a cover of all minimizers can identify
  the requested value without identifying a unique repair or even the optimum rank.
- Exhausted search with no admissible case proves infeasibility of the declared
  finite domain. A timeout without a witness does not.

A response with no established nonempty target gives no useful-action warrant.
An exact policy-selected value and a uniquely implied value have different tags.
A wide outer interval does not establish that both endpoints are attainable.
The program or theory identifiers alone do not certify the numeric contents of
a supplied response; a computed result still needs the declared evaluator.

## 3. Ordinary operations and their interpretation transport

### 3.1 Conditioning keeps the process

For a finite set of admitted cases $`W`$, conditioning on $`A`$ restricts it to
$`W_A=\{w\in W:w\models A\}`$. No equation is changed. If $`W_A`$ is empty,
ordinary set conditioning has no nonempty target. With a supplied probability
law, the usual normalized conditional additionally requires a positive event
mass. A rank on existing cases cannot make an empty event nonempty [CF-S3].

### 3.2 Occurrence intervention changes a named equation

Take a finite acyclic structural graph with total finite-table equations and
an explicit exogenous context. A token intervention replaces one designated
equation by a constant. Evaluate the remaining equations in their declared
dependency order [CF-S1]. Acyclicity gives a unique output for each context;
we do not give a general cyclic solver. The modified graph is a new ordinary
model. Its coordinate map back to the old graph identifies unchanged variables,
replaced equations and recalculated descendants, not an equality of all values.

### 3.3 Replacing a function needs a routing map

Let the complete input history be $`h_0`$, and let a known table satisfy
$`f_0(h_0)=0`$. The table may have other inputs. A replacement table $`f_1`$
must meet the stated history/behavior requirements, including $`f_1(h_0)=1`$.
The permitted table family and its distance from $`f_0`$ are explicit inputs.
A finite input/output table is not an unrestricted program-similarity solver.
A syntactic distance on real program text requires additional presentation
commitments; none is silently supplied here.

Each call has an exact target identity and a routing bit saying whether it
continues to call $`f_0`$ or instead calls $`f_1`$. An actor-only replacement
redirects only the actor's call. A shared replacement redirects all calls
specified as tracking the new version. A stored prediction of $`f_0`$, or a
separate predictor whose meaning is to predict $`f_0`$, does not follow merely
because the actor changed [CF-S2].

The inherited four-operation example remains a diagnostic, not a new result:
$`Z=f_0(h_0)`$, $`A=Z`$, $`B=Z`$, and $`\ell=2+A-2B`$.
Conditioning on $`A=1`$ is empty; intervening only on $`A`$ gives loss 3;
redirecting both calls to an explicitly chosen $`f_1`$ gives loss 1;
redirecting only the actor gives loss 3. A predictor of the old function
continues to return 0 even in the shared-replacement graph unless a separate
rule says otherwise. Same history does not fix this external dependency.

This respects the author's nearest-agent proposal: the replacement is a
specified nearby agent with the required history and different output. It does
not misdescribe that nearby agent as the unchanged original function taking a
mathematically different output at exactly the same argument.

### 3.4 Model or axiom repair

A finite repair changes declared defeasible assumptions while retaining the
hard model and interpretation constraints. A changed arithmetic domain or a
changed meaning of 'integer' belongs here, with an explicit translation.
It is not an ordinary solution of the original statement about usual integers.
Nor does a finite list of ground constraints constitute a complete arithmetic
model or a free theory-consistency oracle.

## 4. A finite ranked-constraint selector

Let $`X`$ be an explicitly finite, nonempty product domain. Its construction is
charged, not supplied as a list of all possible arithmetic worlds. Let
$`H(x)`$ conjoin hard requirements, including the antecedent evaluated according
to the operation's declared adapter. Write

```math
F=\{x\in X:H(x)=1\}.
```

There are $`m`$ named defeasible constraints $`E_1,\ldots,E_m`$. Each has a
strictly positive rational weight $`w_j`$ and a tier
$`k_j\in\{1,\ldots,r\}`$. The vector of violation penalties is

```math
\rho_k(x)=\sum_{j:k_j=k}w_j\bigl(1-E_j(x)\bigr),
\qquad \rho(x)=(\rho_1(x),\ldots,\rho_r(x)).
```

We minimize in lexicographic order. This is a task-specific ordering of
repairs, not an expectation or a probability distribution. The default target is

```math
S=\{x\in F:\rho(x)\le_{\mathrm{lex}}\rho(y)\text{ for every }y\in F\}.
```

If $`F`$ is empty, return **INFEASIBLE**, with a certificate appropriate to this
finite domain. If $`F`$ is nonempty, finiteness ensures $`S`$ is nonempty.
Different weights, tiers, exception permissions or hard frames define different
requests. Rank, task loss and computational resource cost are three independent
quantities; adding one to another requires an additional conversion policy.

For a known rational loss $`\ell_a`$ of hypothetical action $`a`$, the exact
answer can be the image $`\{\ell_a(x):x\in S\}`$ or its interval hull.
A uniform comparison uses the paired quantity $`\ell_a(x)-\ell_b(x)`$ on the
same selected case. Optimistically choosing the minimum loss among ties or
robustly choosing the maximum is a consumer rule, not a fact forced by the
counterfactual. Selecting a repair by inspecting the queried loss must be
labelled preference-guided planning; it is not independent structural evidence.

### C04-1 — exact deletion correspondence

A deletion repair is a set $`R\subseteq\{1,\ldots,m\}`$ together with a
witness $`x\in F`$ satisfying every $`E_j`$ whose index is outside $`R`$.
Its penalty vector sums the weights of the deleted indices in each tier.
Let $`V(x)=\{j:E_j(x)=0\}`$.

**Claim.** If $`F\ne\varnothing`$, the minimum deletion penalty equals the
minimum violation penalty, and the projections of all minimum deletion pairs
onto $`X`$ are exactly $`S`$. Every minimizing pair satisfies $`R=V(x)`$.

**Proof.** Any feasible pair has $`V(x)\subseteq R`$. Deleting just $`V(x)`$
remains feasible with the same witness. If the inclusion is strict, dropping
one surplus deletion lowers its tier by a positive amount and leaves earlier
tiers unchanged, so strictly improves the lexicographic vector. Thus a minimum
pair has equality. Conversely, $`(V(x),x)`$ is feasible for every $`x\in F`$
with penalty exactly $`\rho(x)`$. Minimize in both directions. The same argument
preserves the full union of minimizing completions, not just the minimum number.

This is a direct finite reconstruction of ordinary weighted constraint repair,
not a novel belief-revision theorem. Strictly positive weights are used for
the equality of deletion sets: zero weights allow surplus deletions at the
same rank. Negative weights invalidate the stated dominance argument. Distinct
soft identities may intentionally have the same formula; their multiplicity
then counts. Repeating the same identity as a logging accident must not create
a new penalty.

## 5. A genuine counterpossible adapter

### 5.1 What stays fixed, and what is exceptional

The base language is finite propositional syntax built from atoms, negation,
conjunction, disjunction, and specified truth/falsity constants. The ordinary
interpretation is the usual Boolean one. A quoted formula such as
$`\theta=p\wedge\neg p`$ has no ordinary satisfying valuation, independently
of the actual facts about $`p`$ or $`q`$. That remains a classical theorem.

Inside the hypothetical evaluation only, atom $`p_i`$ has two independent
bits $`(t_i,f_i)`$, positive and negative support. The original atom occurs with
the same identity wherever it is repeated; splitting its occurrences into
unrelated variables is not permitted by this adapter. The inherited paired
Belnap–Dunn rules [CF-S5, CF-S7] are

```math
\begin{aligned}
t(\neg\phi)&=f(\phi),&f(\neg\phi)&=t(\phi),\\
t(\phi\wedge\psi)&=\min(t(\phi),t(\psi)),&
f(\phi\wedge\psi)&=\max(f(\phi),f(\psi)),\\
t(\phi\vee\psi)&=\max(t(\phi),t(\psi)),&
f(\phi\vee\psi)&=\min(f(\phi),f(\psi)).
\end{aligned}
```

The constants are fixed at $`(t(\top),f(\top))=(1,0)`$ and
$`(t(\bot),f(\bot))=(0,1)`$. These constant conventions are part of this
adapter. The antecedent is imposed by $`t(\theta)=1`$. A retained finite
background formula can likewise be imposed by its positive support; this is
not a claim that its full classical consequence closure survives hypothetically.

An atom's normality constraint is $`N_i:t_i+f_i=1`$. Where normality is hard,
its pair remains ordinary. Where a normality exception is expressly allowed,
$`N_i`$ may be a soft constraint with a positive first-tier penalty. The four
possible pairs are true only, false only, both and neither. The labels are
hypothetical supports, not frequencies, proof-checker verdicts or probabilities.
Ordinary mathematical truth is not changed into those labels.

The exception is therefore precise: hypothetical negation need not be Boolean
complementation at abnormal atoms or at the compound formulas they affect,
but conjunction/disjunction and their
support propagation remain compositional. We do not introduce unrestricted
explosion, arbitrary independent formula labels or a general first-order
counterpossible evaluator. A scalar loss can still be ordinary rational
arithmetic on these explicitly scoped labels.

### C04-2 — conditional return to ordinary evaluation

If every atom is normal, induction on a formula's construction gives
$`(t(\phi),f(\phi))=(v(\phi),1-v(\phi))`$, where $`v`$ is the ordinary
Boolean valuation defined by the positive bits. The atomic case is normality;
negation swaps the complementary bits; the min/max rules yield the usual
Boolean truth tables and complementary negative values. Constants satisfy the
same claim.

Suppose every allowed normality exception has positive penalty in the first
tier, no other first-tier penalty is used, and the hard constraints and
antecedent admit an all-normal case. Its first-tier cost is zero. Every
abnormal case violates at least one normality constraint and has strictly
positive first-tier cost; it cannot minimize, regardless of later tiers.
Thus all selected cases are ordinary, and their selection is exactly the
later-tier ordinary ranking on the hard-conditioned classical cases.

This is a relative ordinary-overlap result. If a user adds a hard frame that
excludes all normal antecedent cases, the hypothesis fails even when the
antecedent alone is satisfiable. It is not the unrestricted possible-world
selection condition from [CF-S4]. Without later-tier costs the ordinary target
is just the conditioned feasible set. With them it is a ranked selection.
Weak centering additionally needs the baseline to be hard-admissible and
minimum-ranked when the antecedent is already true; it is not automatic for
an arbitrary ranking.

### 5.2 GC01: a nonexplosive answer to the unchanged contradiction

This reproduces the [inherited GC01 target](../work_logs/P3_01_2026-10-07_S1/reviews/genuine_counterpossible_target.md)
inside the more general compositional adapter. Let the ordinary actual values
be $`p=q=0`$. Retain the exact quoted antecedent $`p\wedge\neg p`$, permit a
normality exception only for $`p`$, and hold the frame $`(t_q,f_q)=(0,1)`$
hard. Then $`t(\theta)=1`$ requires $`t_p=f_p=1`$. The selected family is the
single support state

```math
(t_p,f_p,t_q,f_q)=(1,1,0,1).
```

It positively supports the antecedent, $`p`$, $`\neg p`$ and $`\neg q`$,
but does not positively support $`q`$. Hence the construction is nonvacuous
and nonexplosive on this fragment. It did not replace the antecedent by another
sentence or turn it into an ordinary satisfiable proposition.

For hypothetical costs $`\ell_{\mathrm{continue}}=4t_q`$ and
$`\ell_{\mathrm{fallback}}=1`$, continuing costs 0 and the fallback costs 1.
This conditional answer depends on the declared frame and evaluator. Removing
the hard frame and adding no replacement preference allows both ordinary
$`q`$ values, so the continuing-loss image is $`\{0,4\}`$. A default point
answer of 0 would then conceal a real ambiguity. No distribution over the
support states is implied by their number or by their ranks.

### 5.3 More than one way to sustain a contradiction

For ordinary-false atoms $`p,r`$, consider the unchanged classical contradiction

```math
\theta=(p\wedge\neg p)\vee(r\wedge\neg r).
```

With normality costs $`\alpha>0`$ for $`p`$ and $`\beta>0`$ for $`r`$, an
admissible state must make at least one atom both-supported. If $`\alpha<\beta`$,
a minimum has only $`p`$ abnormal; if $`\beta<\alpha`$, only $`r`$ is abnormal;
if equal, both types are minimizing alternatives. Making both abnormal costs
more and is never minimal. A later-tier baseline preference can fix the
unaffected atom to its original false-only value without changing that result.

Thus the same antecedent and ordinary background need not identify a unique
counterpossible cost. Which relation is most important to retain is additional
question-specific information. Comparing all admitted weight policies exposes
this dependence rather than treating one unannounced policy as necessity.
A family of conjunctions of such contradiction demands gives an ordinary finite
weighted constraint problem; a full search still has to pay for its candidates.

### 5.4 Limits and why this choice is defensible at finite scope

The choice preserves atomic identity, conjunction elimination, double negation
and the displayed support rules, and it agrees with ordinary evaluation when
normality is possible and prioritized. These are concrete reasons to try it:
it does not acquire nonvacuity merely by setting the root formula to true and
ignoring its constituents. A direct formula-label impossible-world model is
more expressive but needs more exceptional rules and relevance commitments.
The present restricted model is not superior by definition.

It deliberately cannot support the fixed falsity constant: $`t(\bot)=0`$ in
every admitted support state. An antecedent requiring $`t(\bot)=1`$ is therefore
infeasible. Some impossible antecedents are handled, not all of them. Nor does
this propositional adapter decide what follows arithmetically from the usual
integers allegedly making $`\sqrt{2}`$ rational. A ground arithmetic atom would
need a declared bridge and propagation rules; treating it as an opaque support
bit does not import substitution, induction or field identities. The classical
irrationality proof remains valid in its original scope.

Ordinary classical equivalence of two contradictions gives the same empty
possible extension, but does not require them to have the same hypothetical
support consequences. That unrestricted requirement would undo the content
sensitivity sought here [CF-S4]. Specific meaning-preserving presentations can
still be tested. Their larger invariance and proof-reuse theory belongs to P3-05.

## 6. Frame preferences, tiers and admitted uncertainty

### C04-3 — a sufficient local-frame condition

Partition the representation into targeted coordinates $`x`$ and untargeted
coordinates $`u`$. Suppose the hard-feasible set is the nonempty product
$`F_T\times F_U`$ and $`\rho(x,u)=\rho_T(x)+\rho_U(u)`$, with the same
lexicographic vector order. Then

```math
\mathop{\mathrm{argmin}}_{(x,u)\in F_T\times F_U}\rho(x,u)
=
\mathop{\mathrm{argmin}}_{x\in F_T}\rho_T(x)
\times
\mathop{\mathrm{argmin}}_{u\in F_U}\rho_U(u).
```

**Proof.** If a component is not minimizing, replacing it by a smaller one
strictly decreases the total by translation invariance of lexicographic order.
Conversely, each component's excess above its minimum is lexicographically
nonnegative, and so is their sum. Therefore the pair of minima is minimizing.
If $`u_0`$ is the unique minimum on $`F_U`$, every selected pair retains $`u_0`$.

This gives a reason for a ceteris-paribus answer when the question really has
an independent frame and a baseline preference. Independence is an input to
verify, not a conclusion from the word 'untargeted'. A hard link $`t_p=t_q`$
destroys the factorization; imposing $`t_p=1`$ with a hard frame $`t_q=0`$
then makes the domain empty. No ranking repairs a conflict between two hard
requirements. Likewise, a coupled rank can make an unrelated variable change
because the declared policy rewards that change.

### 6.1 A priority tier is not an arbitrarily large finite penalty

With actual $`p=0`$ and antecedent $`t_p=1`$, compare normal $`(1,0)`$ with
abnormal $`(1,1)`$. Penalize each changed support bit relative to actual
$`(0,1)`$ by $`B>0`$. The normal case changes two bits; the abnormal case
changes one. A single scalar objective giving abnormality penalty $`M`$
selects the abnormal case whenever $`M+B<2B`$, or $`M<B`$.

Lexicographically prioritizing normality always selects the normal case here.
There is no universal finite $`M`$ that simulates this priority for an unbounded
family of secondary stakes $`B`$. For one finite request a sufficient bound
can be computed from the admitted secondary range and minimum positive
first-tier gap, or rational tiers can be converted to bounded integers and
scalarized with explicit place values. That construction and its increased
bit precision are costs, not a free universal constant.

### C04-4 — which weight policies can select a case?

Sometimes the user has not fixed one tradeoff between two kinds of allowed
change. Let $`F`$ be finite and nonempty and let a declared compact rational
interval $`I=[a,b]`$ index scalar ranks

```math
r_x(t)=\alpha_x t+\beta_x,\qquad t\in I.
```

This includes two positive normalized repair weights by taking
$`t\in[\epsilon,1-\epsilon]`$ and using $`t`$ and $`1-t`$. The parameter
interval describes permitted policies, not probability uncertainty.
For each case define

```math
I_x=I\cap\bigcap_{y\in F}
\{t:(\alpha_x-\alpha_y)t+(\beta_x-\beta_y)\le 0\}.
```

**Claim.** $`I_x`$ is a possibly empty closed rational interval, and $`x`$
is selected by some policy in $`I`$ exactly when $`I_x`$ is nonempty.

**Proof.** A nonconstant affine inequality in one variable gives a closed half
line with a rational endpoint; a constant one is either vacuous or impossible.
Intersecting with $`I`$ gives the claimed interval. Membership says exactly that
$`r_x(t)\le r_y(t)`$ for every competitor, which is the minimizing condition.
Finiteness and nonemptiness of $`F`$ ensure at least one minimizing case for
any admitted $`t`$. The same reasoning in higher dimension gives a polyhedral
feasibility problem, but no higher-dimensional solver is implemented here.

Thus the union of possibly selected cases is
$`U=\{x\in F:I_x\ne\varnothing\}`$. A loss or paired action inequality that
is constant/valid over $`U`$ is stable across every admitted policy. A failure
of constancy gives a policy/case witness to non-identification, not evidence
that all weights are equally reasonable. The computation needs the full
candidate comparisons or a sound substitute; old minimizers from only one
parameter value are insufficient input.

For section 5.3, use $`\alpha=t`$ and $`\beta=1-t`$ with
$`t\in[1/4,3/4]`$. The $`p`$-abnormal repair is selected on
$`[1/4,1/2]`$, and the $`r`$-abnormal repair on $`[1/2,3/4]`$, including
the tie. With an ordinary-false baseline preference for the other atom,
$`2t_r`$ has possible selected values 0 and 2. A fallback of 1 changes which
action is preferable across the weight regions. In contrast, costs
$`t_p+2t_r`$ and $`t_p+2t_r+1`$ leave the first action better by one across
all policies, even though its absolute cost is not identified. This is a
concrete task-relative robustness distinction, not a discovered causal law.

## 7. Interrupted search must cover every possibly optimal case

The selected set $`S`$ is a mathematical target, not information a bounded
reasoner receives for free. We now adapt the
[P3-03 outer-cover principle](03_logical_uncertainty.md) to that target.
Fix the complete request throughout the search, including its hard constraints,
ranking and loss interpretation.

A cell denotes a subset of the finite domain. Its hard-constraint evaluation
must conservatively indicate possible feasibility. Its rank lower bound
$`L(C)`$ satisfies $`L(C)\le_{\mathrm{lex}}\rho(x)`$ for every feasible
$`x\in C`$. A loss enclosure covers every feasible value in the cell.
These bounds may be loose; they need not prove that any feasible point exists.

Maintain a feasible incumbent with rank $`u`$ when one has been found, a set
$`B`$ of all best-ranked assignments examined so far, and a frontier of
unresolved cells. Initially the frontier covers the entire domain. An operation
may split a cell into an exhaustive cover, discharge an infeasible cell,
evaluate a singleton, or discard a cell with $`L(C)>_{\mathrm{lex}}u`$.
Rank equality is **not** a reason to discard a cell when the service concerns
all minimizing consequences. Worse previously examined assignments may be
removed from $`B`$ when a better feasible incumbent arrives.

### C04-5 — optimal-family outer coverage

At any stage with a feasible incumbent, let $`C_*`$ be the union of its
best-found assignments and all frontier cells that remain potentially
feasible and do not have a lower bound strictly above the incumbent rank.
Then

```math
\varnothing\ne S\subseteq C_*.
```

**Proof.** A feasible incumbent makes $`F`$ nonempty, so its finite global
minimum exists. Every true minimizer was in the initial domain. A sound
infeasibility discharge cannot remove it. A rank discharge cannot remove it,
because its actual rank is at least the discarded cell's lower bound, strictly
greater than an already feasible incumbent; that contradicts global minimality.
An exhaustive split preserves membership. An examined global minimum cannot
be dropped from $`B`$ in favor of a strictly smaller feasible point, since
that would contradict its minimality. Thus every operation preserves coverage.
This reasoning does not suppose the incumbent already is a global minimum.

A known nonnegative rank and a found rank-zero case certify the optimum rank,
but an unexamined rank-zero cell can contain a different loss. For example,
two equally ranked cases with losses 0 and 4 do not justify returning only 0.
Pruning with $`L(C)\ge u`$ would lose that information. It is appropriate only
for a different service, such as finding some optimal assignment, and cannot
be silently reused for all-optima loss queries.

### C04-6 — task certainty without repair certainty

Let a sound evaluation of $`\ell_a`$ over $`C_*`$ lie in $`[l_a,u_a]`$.
By C04-5 this encloses the true selected loss set. If the interval is a singleton,
its value is exact even if optimum rank and minimizing identities remain unknown.
For several actions, a sound upper bound on $`\ell_a-\ell_b`$ not exceeding
zero for every competing $`b`$ certifies that $`a`$ is optimal in every selected
case. It need not identify their absolute costs.

These are one-sided guarantees: an inconclusive bound does not prove that the
value is nonunique or that no uniformly optimal action exists. A pointwise
best action that depends on an unseen case is not an available common action.
The certificate requires a feasible witness and covers all true minimizers;
a sample of found good cases does not suffice.

If optimum rank is certified and best-found optimal witnesses attain both
endpoints of the outer loss interval, the interval is the **exact hull** without
exhausting every minimizing identity. This does not identify every interior
attainable value. An exact finite image is a stronger service.

### 7.1 Ordinary multi-pass comparison

A strong ordinary solver can first optimize the rank, then constrain it to its
certified optimum and minimize/maximize the requested loss. Lexicographic
rank can be optimized tier by tier, retaining earlier optimum values. This
computes an exact hull without enumerating all minimizing identities. Each
solve, optimum certificate and constraint construction must be counted.
It is not an extra oracle permitted only to Value Logic.

The outer-cover method instead permits early task certificates before the
rank optimum is known. Ordinary branch-and-bound can use the same stopping
condition. This is a scoped integration of selection and query evidence, not
a numerical performance advantage over that ordinary combination.

### 7.2 What changes invalidate the search question?

Changing the antecedent, ranking, permitted exceptions or structural routing
can make a formerly discarded candidate relevant. Even a new hard condition
can do so: a rank-zero case may be excluded while a previously inferior case
becomes the unique optimum. Restricting the already selected set to the new
condition then gives the wrong answer. Bind search results to the entire exact
request and begin a new search or justify an appropriate repair. The later
P3-05 task owns the general proof-reuse and change-transport analysis.

## 8. Compilation into an ordinary Boolean solver

Each hypothetical paired-support coordinate is an ordinary Boolean bit in the
metatheory. Negation, min and max on these bits are explicit Boolean gates;
the exceptional meaning lies in the front-end support interpretation, not in
the arithmetic backend. A solver over these bit constraints therefore does not
implicitly impose $`f_i=1-t_i`$ where normality has been made defeasible.
Nor does merely encoding two bits prove that this interpretation is appropriate.
The use of a classical signed-Boolean encoding for preferred paraconsistent
reasoning has a direct predecessor in Arieli [CF-S7]. Its inclusion-minimal
abnormality relation and this fixed weighted selector must be distinguished;
CE04-1 characterizes their finite Boolean-profile overlap rather than claiming
that the classical reduction itself is new.

### C04-7 — cost- and all-minimizer-preserving encoding

For each Boolean subformula introduce a fresh root bit and enforce its complete
truth-table equivalence by hard clauses. In particular, for $`y\leftrightarrow
(a\wedge b)`$, use $`(\neg y\vee a)`$, $`(\neg y\vee b)`$ and
$`(y\vee\neg a\vee\neg b)`$. For $`y\leftrightarrow\neg a`$, use
$`(\neg y\vee\neg a)`$ and $`(y\vee a)`$. The disjunction gate is dual.
Assert hard formula roots, and give each named soft formula exactly one weighted
soft root assertion. Reusing a formula root does not collapse intentionally
distinct soft identities or multiply a single one.

**Proof.** Every assignment to the original bits has exactly one extension
satisfying all gate definitions: evaluate subformulas in dependency order.
Conversely, induction on that order forces every satisfying extended assignment
to take those values. The root of each hard/soft formula therefore equals its
original value. Hard feasibility, each tier's total violation penalty and any
loss decoded from the original bits are preserved pointwise. The bijection
then preserves all minimizing assignments and their loss image, not just the
optimum number. Rational positive weights can be scaled to integers per tier;
lexicographic optimization still needs its declared tier handling.

This is a reconstruction of standard definitional encoding and weighted partial
MaxSAT [CF-S6], with the particular all-selected-case query contract made explicit.
It does not import possibly mistyped displayed gate clauses from a source.

### 8.1 A genuine objective-preservation failure

Let hard constraints admit only $`(p,q)=(0,0)`$ and $`(1,1)`$. A single soft
assumption $`p\wedge q`$ has weight 3, and $`\neg p`$ has weight 4.
The original penalties are 3 and 4 respectively, so the first case is preferred.
Incorrectly replacing the conjunction by two separately weighted clauses of
weight 3 gives penalties 6 and 4, reversing the preferred case. Satisfiability
is preserved, but the counterfactual selection is not. One soft root with hard
conjunction definitions preserves the intended penalty and both query meanings.
This is a worked instance of the known MaxSAT encoding issue, not a new general
observation. It also explains why a record's identity and penalty unit matter.

## 9. Relationship to the existing Value Logic calculus

The new front end supplies a finite, nonempty, explicitly hypothetical source,
known rational loss terms and a declared consumer query. The ordinary numerical
backend can check inequalities conditional on that source. It does not prove
the philosophical aptness of the selected relevance rules or discover its
structural equations. Native Boolean entailment and old theorems retain their
original interpretations and assumptions.

The support rules use min/max on Boolean source coordinates and known rational
coefficients. An affine loss difference likewise stays inside the inherited
piecewise-affine language. Arbitrary products of two continuous uncertain quantities remain outside that
fragment. There is a useful narrower construction: a weight in a known rational
interval multiplied by a genuinely Boolean indicator has the exact CPWA gate
of CE04-15, with explicit unit, interval and Boolean-source premises. No single
finite CPWA expression uniformly gates an unbounded weight by such an indicator.
CE04-17 also gives an unbounded gate as an explicit two-branch affine source
graph with witnesses, without introducing a product term. The distinction is
between term syntax and source representation, not bounded versus unlimited
Value Logic ambition.
The mathematical weight-region results are a separate finite comparison
analysis; the executable rank kernel still requires fixed rational weights,
and no native proof-acceptance claim is made for the new gate.

A model replacement changes scope and requires an interpretation map. The
counterpossible adapter instead leaves the original formula and classical
impossibility claim intact and declares a new hypothetical consequence relation.
Those are different operations even if their eventual numerical costs agree.
This session does not establish a native checker integration test, a full
first-order logical counterfactual calculus, or a proof-reuse theorem.

## 10. Ordinary comparison and contribution disposition

The relevant ordinary combination is supplied structural equations and routing,
finite weighted constraint repair or MaxSAT, paired-support semantics where
requested, sound branch-and-bound bounds, and explicit loss optimization. It
may use the very same efficient shortcuts, input identities, query service,
precision and computation budget. Classical Boolean bookkeeping alone is not
the strongest comparator.

C04-1/2/3/7 are finite reconstructions or direct specializations of familiar
selection, support and compilation machinery. C04-4 is a finite affine
optimality-region calculation. C04-5/6 adapt the P3-03 outer-cover contract to
all minimizing counterfactual consequences and task-dependent stopping. The
combined object is a concrete provisional interface, not merely a cost number;
its wider usefulness needs the later named comparisons. No worldwide-priority,
universal superiority or learned counterfactual-dependence claim is supported.
P3-N01 remains **NOT YET SUPPORTED**.

## 11. Evidence and current limits

The proposed proofs are subject to the declared finite-domain, sound evaluator,
positive-weight, fixed-request and nonempty-witness premises. The executable
adapter and its development checks are being prepared separately. No test
count, Research90 completion or publication claim is inferred from this draft.
P3-04 remains the active task until both evidence and its measured floor close.
