# P3-04 — Selection, consequence and payoff boundaries

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 8, 2026 UTC.
Status: **IN PROGRESS**, companion to
[finite counterfactual semantics](04_counterfactual_semantics.md).
These are scoped mathematical reconstructions and adaptations, not an
unrestricted counterpossible theory. All executable evidence is DEVELOPMENT.
Source comparisons: [CF-S5–S7](../literature/04_source_contracts.md).

## 1. Weighted repair and set-minimal abnormality are related but not identical

The predecessor CF-S7 selects models whose sets of abnormal formula assignments
are inclusion-minimal. The main note uses a chosen positive weighted sum, or
lexicographic sums. Those are different contracts. The following exact finite
comparison makes the difference explicit without attributing a new reduction
to Value Logic.

### CE04-1 — the union of positive-weight optima

Fix a nonempty finite case family $`F`$ and Boolean violation indicators
$`b(x)\in\{0,1\}^m`$. Write $`V(x)=\{j:b_j(x)=1\}`$ and let $`M`$ contain
all cases whose violation set is inclusion-minimal among those attained in
$`F`$. For each strictly positive rational vector $`w`$, let
$`S_w=\mathop{\mathrm{argmin}}_{x\in F}w\cdot b(x)`$. Then

```math
M=\bigcup_{w\in\mathbb Q_{>0}^{m}}S_w.
```

**Proof.** If $`V(y)\subsetneq V(x)`$, strict positivity gives
$`w\cdot b(y)<w\cdot b(x)`$ for every admitted weight vector. Thus every
weighted minimizer is in $`M`$.

Conversely fix an inclusion-minimal attained set $`S`$. Choose weight
$`1/(m+1)`$ for indices in $`S`$ and weight 1 elsewhere. A case with violation
set exactly $`S`$ costs $`|S|/(m+1)<1`$. Any other attained violation set
cannot be a proper subset of $`S`$, by minimality. If it is not equal to
$`S`$, it therefore contains an index outside $`S`$ and costs at least 1.
Every case with violation set $`S`$ is optimal, proving the reverse inclusion.
For $`m=0`$, the empty weight vector and zero penalty select all cases.

The construction selects a target violation set, not one case among all cases
with that set. It assumes unrestricted positive rational weights and a fixed
feasible family. It need not hold for a bounded menu of weight ratios, a fixed
lexicographic priority, or real-valued violation magnitudes instead of bits.
For example, the nondominated real vectors $`(0,2),(1,3/2),(2,0)`$ have a
middle point that no positive linear weighting minimizes: it would need both
$`w_1\le w_2/2`$ and $`w_1\ge 3w_2/2`$. Boolean violations are essential to
the converse as stated.

A fixed unit-weight sum can be strictly more selective than set minimality.
If the attained minimal violation sets are $`\{p\}`$ and $`\{q,r\}`$, both
are inclusion-minimal but unit weights select only the first. Giving $`p`$
weight 3 and the other two weight 1 reverses that choice. Treating the union
of all positive-weight choices as the target is therefore a stronger ambiguity
contract than silently selecting unit weights. Ordinary preferential and
multiobjective methods can provide the same comparison.

## 2. A hypothetical support is not automatically an ordinary outcome

### CE04-2 — decoder obstruction and a positive normal-fragment case

Let a selected support state make $`p`$ both-supported:
$`(t_p,f_p)=(1,1)`$. No ordinary Boolean valuation can preserve both support
judgments while also interpreting negation by complementation. Such a valuation
would require $`v(p)=1`$ and $`v(\neg p)=1-v(p)=1`$, a contradiction.

Even requiring agreement on *all ordinary states* does not determine an
extension of an ordinary payoff into this hypothetical state. The two maps

```math
d_+(t,f)=t,\qquad d_-(t,f)=1-f
```

both recover $`v(p)`$ on the normal pairs $`(1,0)`$ and $`(0,1)`$, yet return
1 and 0 respectively on $`(1,1)`$. Hence an ordinary loss equal to the binary
outcome $`p`$ has different hypothetical extensions under two decoders that
agree on every ordinary observation. Additional ordinary data do not distinguish
these decoders on the abnormal state. This is a finite information obstruction,
not a claim that the two maps are equally desirable for every task.

A report can instead declare that its cost is a function of the support labels
themselves. That was the explicit contract in GC01. Or it can carry a specified
nonempty family of decoders and bound the image over both selected states and
decoders. Neither option warrants an unstated ordinary outcome. There is a
simple positive case: if the queried payoff depends only on a subfragment
whose atoms are normal in every selected state, and the hypothetical payoff is
required to remain a function of that same subfragment, its ordinary
truth-functional evaluation is unambiguous. The locality requirement is part
of the payoff contract; ordinary observations alone do not force an extension
to ignore unrelated hypothetical abnormalities. A specified ordinary affine payoff
then transfers directly to its positive coordinates. GC01's cost uses only the
normal $`q`$ coordinate, so its numerical answer does not pick a winner between
$`d_+`$ and $`d_-`$ for the conflicting $`p`$ coordinate.

For a fixed-function counterpossible, both-support for 'returns 0' and 'returns
1' similarly does not tell an ordinary downstream machine which value it
receives. A declared output-port rule or a family of such rules is needed.
Replacing the function by a different, ordinarily executable function avoids
that decoding problem but answers the replacement question, not the unchanged
function's counterpossible. This preserves the type/token distinction in CF-S2.

## 3. Feasible witnesses and the role of relevance

### CE04-3 — a constructive sufficient witness

Every constant-free formula in the admitted $`\neg,\wedge,\vee`$ language is
both-supported when all of its atoms are both-supported. This follows by
structural induction: a swapped pair $`(1,1)`$ is unchanged; conjunction and
disjunction of two such pairs again have both coordinates equal to 1.
Consequently a finite family of positive-support requirements is jointly
satisfied by this assignment if all its atoms permit abnormality and there
are no conflicting hard frame/evaluation constraints. This establishes an
actual feasible witness, not minimum rank and not a useful arbitrary-world
claim. Fixed constants and additional hard Boolean links require separate
checking; in particular the fixed falsity constant blocks this construction.

A local sufficient version starts from the antecedent's atoms and closes that
set $`T`$ under co-occurrence in each retained background formula. At the fixed
point, each background formula either has all its atoms in $`T`$ or none of
them there. Assign both-support to $`T`$, keep the ordinary baseline elsewhere,
and suppose:

- Every formula wholly inside $`T`$ is constant-free.
- All atoms in $`T`$ permit normality exceptions and have no incompatible hard
  frame requirement.
- The baseline satisfies each outside background formula and every other hard
  condition, which depends only on outside coordinates.

The inside formulas are supported by induction; outside formulas and hard
conditions remain satisfied. Thus the proposed assignment is feasible. For
ordinary baseline $`p=q=r=0`$, antecedent $`p\wedge\neg p`$ and background
$`\neg p\vee r`$, this procedure may set both $`p,r`$ to both-support while
preserving $`q`$. It is a witness, although setting only $`p`$ abnormal already
suffices and is cheaper under positive normality penalties.

This closure is a *candidate-construction heuristic*, not an inferred relevance
relation or a definition of the selected domain. A classically tautological
background mentioning $`q`$ can enlarge it, despite not requiring a semantic
change to $`q`$. The full hard-constraint checker must validate the constructed
witness. If the heuristic fails because it crosses a hard frame, the complete
search can still succeed. It must not report global infeasibility from that
heuristic failure. Its work is charged and is equally available to O-COMB.

### CE04-4 — a useful gap-exclusion theorem

Consider the paired-support adapter with the following more specific hard
constraints: positive support of finitely many $`\neg,\wedge,\vee`$ formulas
and the fixed constants; hard normality where exceptions are disallowed;
and ordinary fixed atom pairs for frame facts. Allowed normality exceptions
have strictly positive first-tier weights, and no other penalty enters that
tier. Later-tier preferences are arbitrary.

**Claim.** No minimum-ranked state has a neither-supported atom.

**Proof.** A neither pair $`(0,0)`$ cannot occur at a hard-normal or hard-frame
atom. Change it at an allowed-exception atom to $`(1,0)`$. Positive and negative
support formulas are coordinatewise monotone in the atomic support bits, by
induction over the displayed rules. Every positive-support hard requirement
therefore remains satisfied. Other atoms' normality and frames are untouched.
The changed atom is now normal, so its positive first-tier penalty disappears;
no other first-tier term changes. The rank strictly improves regardless of
later-tier costs, contradicting minimality.

Thus the preferred states of this default adapter in fact use only true-only,
false-only and both, although incomplete search correctly retains the larger
four-pair cover until it can exclude alternatives. This does not collapse the
semantics to ordinary Boolean evaluation: both-supported contradictions remain.
It also does not hold for arbitrary additional hard Boolean constraints on
support bits. A hard requirement $`t_p=f_p=0`$, for instance, forces a gap.
If abnormality penalties have zero weight, or share priority with competing
rewards, the improvement argument also fails. The general ranked kernel admits
those Boolean hard constraints; the theorem is about the named adapter only.

## 4. Consequence laws require a fixed selection contract

Fix a finite hypothetical universe, a background and a rank independent of the
antecedent; only the hard requirement $`t(A)=1`$ changes. Let $`S_A`$ be its
nonempty minimum family. Define $`A\Rightarrow B`$ to mean that every selected
state positively supports $`B`$. Empty $`S_A`$ is a separate infeasibility
status, not a true useful conditional.

**Reflexivity and conjunction.** $`A\Rightarrow A`$ follows from feasibility.
If $`A\Rightarrow B`$ and $`A\Rightarrow C`$, then
$`A\Rightarrow B\wedge C`$ by the positive-support conjunction rule.

**Cautious addition.** If $`A\Rightarrow B`$, then
$`S_{A\wedge B}=S_A`$. Every current minimum meets the additional condition,
so the old optimum remains attainable; no newly admitted case exists and no
more expensive case becomes minimizing. As a result, adding an already
supported antecedent consequence preserves every other selected consequence.

**Disjunction.** If both antecedent families are nonempty and every state in
both $`S_A`$ and $`S_B`$ supports $`C`$, then every state selected for
$`A\vee B`$ supports $`C`$. A minimum of the union belongs to at least one
side and must be a minimum on that side. This is the ordinary finite minimum
argument on support sets, not a new preferential-logic theorem.

**Permitted replacement.** Replacing an antecedent by one with the same
positive-support set in this fixed universe preserves selection. Replacing a
consequent by a Belnap–Dunn consequence preserves support. Arbitrary classical
equivalence outside normal states does not have either property: all classical
contradictions have the empty ordinary extension, while the present semantics
intentionally distinguishes their hypothetical contents.

### CE04-5 — the gap condition behind rational monotony

Suppose selected states for $`A`$ are gap-free on all atoms of $`B`$. If
$`A\Rightarrow C`$ but $`A\not\Rightarrow\neg B`$, then
$`A\wedge B\Rightarrow C`$.

**Proof.** Failure of $`A\Rightarrow\neg B`$ supplies a selected state with
$`f(B)=0`$. The gap-free subalgebra is closed under the admitted connectives,
so that state has $`t(B)=1`$. The old optimum rank remains feasible after
requiring $`B`$; its new minima are precisely the old minima supporting $`B`$.
They all support $`C`$ and form a nonempty set.

Without the gap-free condition, the result can fail. In a finite ranked family,
let the unique rank-0 state support $`A,C`$ but make $`B`$ neither-supported.
Let the rank-1 state support $`A,B`$ but not $`C`$. Then
$`A\Rightarrow C`$ and not $`A\Rightarrow\neg B`$, while the selected
$`A\wedge B`$ state does not support $`C`$. A Boolean meta-condition that
some old minimum positively supports $`B`$ suffices even when gaps are allowed;
object-level failure to support its negation is not always that condition.

CE04-4 establishes the gap-free premise for the default adapter's minima.
Nevertheless all the consequence laws in this section require a common
universe/background/ranking. If the repair permissions, hard frame or ranking
are reselected when the antecedent changes, they do not follow from these
arguments. That is a change of request, not a consequence of adding information.
The development checks of these laws test their finite hypotheses and separate
countermodels; they are not an empirical endorsement of the ranking policy.

## 5. Unknown source facts must not be optimized as repair choices

The main selector fixes its interpretation, context and hard source before
ranking repairs. Integrating P3-03's unresolved information needs an extra
quantifier distinction. A possible source completion is not itself an action
or an admissible edit merely because it is represented by another coordinate.

Let $`U`$ be a finite family of source completions, and $`F_u`$ the admissible
repairs for completion $`u`$. Initially suppose every $`F_u`$ is nonempty.
The source-specific optimum rank and selected family are

```math
r^*(u)=\min_{x\in F_u}\rho(u,x),\qquad
S_u=\{x\in F_u:\rho(u,x)=r^*(u)\}.
```

The uncertain-source counterfactual asks about the family

```math
S^{\mathrm{source}}=\bigcup_{u\in U}\{u\}\times S_u.
```

This ranks the repairs *inside each still-admitted source*. It does not choose
which unresolved mathematical facts would be convenient. In contrast, one
joint optimization over all feasible $`(u,x)`$ yields

```math
S^{\mathrm{joint}}
=\bigcup_{u:r^*(u)=\min_{v\in U}r^*(v)}\{u\}\times S_u.
```

### CE04-6 — exact scope of the joint-optimization shortcut

**Claim.** Under the nonempty finite assumptions,
$`S^{\mathrm{joint}}=S^{\mathrm{source}}`$ exactly when $`r^*(u)`$ is constant
over the admitted source family.

**Proof.** The displayed joint expression follows by minimizing first within
each source and then over sources. Constancy retains every source. Conversely,
if the minimum rank is not constant, some nonempty $`S_u`$ has larger rank and
is wholly omitted by joint optimization. The tagged families therefore differ.
A particular loss image can nevertheless coincide despite this lost source;
full-family equality is not necessary for every consuming task.

For a concrete separator let each of two source completions have one admissible
repair. At $`u=0`$ its rank is 0 and loss 0; at $`u=1`$ its rank is 1 and
loss 10. Sourcewise analysis gives the loss image $`\{0,10\}`$. Joint
minimization returns only 0, implicitly choosing the favorable unresolved source.
A fallback costing 4 would not be dominated on the full source family despite
appearing worse than that joint optimizer's chosen case. Repair ranking was
not observational evidence that $`u=1`$ is false.

An ordinary combined method can keep separate optimizers, or encode the
sourcewise no-better-repair condition directly. In its bounded implementation,
pruning needs a same-source incumbent or an upper bound valid for each source
in the cell. A globally cheapest witness from a different source is not such
an upper bound. This is a scoped composition condition on the uncertainty and
repair interfaces, not an advantage over ordinary conditional optimization.

**Partial domains.** If some $`F_u`$ are empty, the report records which source
completions lack an admissible hypothetical. A value range over the remaining
ones is explicitly conditional on that domain; nonemptiness of their union
does not establish definedness for every admitted source. A total decision
service must specify a fallback on undefined branches or require and establish
full domain coverage. Unknown feasibility is distinct from certified emptiness.

**A semantic family is not a hidden-information policy.** Even
$`\forall u\,\exists x\in F_u`$ does not imply that a single replacement
works in every source. With $`F_0=\{x_0\}`$ and $`F_1=\{x_1\}`$, the
intersection is empty. If the chooser cannot observe which source is actual,
a deployable common replacement has a different feasibility and information
contract. Defining the counterfactual at each possible source is legitimate;
claiming that it supplies an executable source-dependent choice is not.

## 6. Robust pruning over a declared interval of repair policies

Suppose the feasible family is fixed while a scalar policy parameter varies
over a nonempty closed rational interval $`I=[a,b]`$. A candidate's repair
rank is an affine scalar function of that parameter. This is a separate service
from the multi-tier solver's fixed ranking; the two are not silently combined.

Let a search cell $`C`$ have a valid affine rank lower bound $`L_C(t)`$ for
every candidate in that cell and every $`t\in I`$. Let $`B`$ be a nonempty
finite family of inspected candidates feasible at **every** such parameter,
with their known affine ranks $`r_j(t)`$. Then
$`U(t)=\min_{j\in B}r_j(t)`$ is an upper bound on the global optimum.

### CE04-7 — a finite all-policy discharge certificate

Define $`g_C(t)=L_C(t)-U(t)`$. Take the interval endpoints and every pairwise
intersection of nonparallel incumbent rank lines lying in $`I`$. The minimum
of $`g_C`$ over this finite set equals its minimum over all of $`I`$.

**Proof.** Between consecutive such points the ordering of the incumbent lines
does not change. Their minimum is one affine line there (identical ties do not
matter), so $`g_C`$ is affine on that closed subinterval. An affine function
attains its minimum at an endpoint, or everywhere when constant. Taking the
minimum over all intervals proves the assertion. A singleton $`I`$ is immediate.

If this minimum is strictly positive, every candidate in $`C`$ is worse than
a feasible incumbent at every admitted policy, so the cell contains no
minimizer for any such policy. Equality is insufficient to discard it: an
unseen candidate can tie with a different consequence. A negative computed
gap is also not proof that a cell candidate is ever optimal; the lower bound
can be loose.

For example, take incumbent ranks $`t`$ and $`1-t`$ on $`[0,1]`$, and cell
bound $`3/5`$. The best incumbent never costs more than $`1/2`$, so the cell
is uniformly worse by at least $`1/10`$. Neither incumbent alone uniformly
dominates the bound; collectively they do. A bound of $`1/2`$ touches the
envelope at $`t=1/2`$ and must not be discarded by this strict test.

With nonnegative affine soft weights, summing only the certainly violated
constraints gives a valid affine cell lower bound. Negativity can invalidate
that construction. The helper accepts an already justified lower line and
incumbent lines, and verifies the one-dimensional numeric inequality only.
It does not prove those lines' relation to arbitrary external search cells.
The polynomial number of line intersections is a certificate-size statement
for this finite helper, not a general bound on discovering feasible incumbents
or minimizing over many unknown policy parameters.

## 7. A strong ordinary solver can scalarize the finite tiers exactly

### CE04-8 — rational lexicographic ranks as integer weighted repair

For tier $`k`$, let $`d_k`$ be a common denominator of its positive rational
weights. The integer rank $`I_k(x)=d_k\rho_k(x)`$ lies between 0 and the
integer bound $`B_k=\sum_{j:k_j=k}d_kw_j`$. Define

```math
M_r=1,\qquad M_k=1+\sum_{j>k}M_jB_j,
\qquad R(x)=\sum_k M_k I_k(x).
```

For two candidates with different tier vectors, take the first differing tier
$`k`$. An improvement there decreases $`M_k I_k`$ by at least $`M_k`$.
All later tiers together can oppose it by at most
$`\sum_{j>k}M_jB_j=M_k-1`$. Therefore the sign of the scalar rank difference
agrees with lexicographic order. Identical tier ranks yield identical scalar
ranks. Thus all minimizing candidates, not just one, are preserved.

This uses finite bounds and a positive integer gap after rational scaling.
It does not justify an arbitrary fixed 'very large' coefficient for unbounded
requests. An empty tier has $`d_k=1,B_k=0`$. The converted coefficient for soft
constraint $`j`$ is $`M_{k_j}d_{k_j}w_j`$, a positive integer. Paired with
C04-7's hard equivalence gates, this produces an ordinary weighted partial
MaxSAT problem with the same projected minima and cost image. The integer
encoding may need more bits than the original input; it is not automatically
admitted back through the kernel's 128-bit input-coefficient cap.

A production comparator may use lexicographic optimization natively, repeated
optimization by tier, or this exact scalarization. No efficiency claim rests
on denying the ordinary method any of those options. The numerical and rank
certificates still need the same candidate, hard-constraint and loss semantics.

## 8. Query projection must preserve ranking information, not only losses

### CE04-9 — exact finite elimination for a task projection

Let $`\pi:F\to Y`$ be a projection with finite image, and suppose every
requested loss factors through it. Define the **minimum rank over each
projection fiber**

```math
\bar\rho(y)=\min\{\rho(x):x\in F,\ \pi(x)=y\},
\qquad y\in\pi(F).
```

Then
$`\pi(S)=\mathop{\mathrm{argmin}}_{y\in\pi(F)}\bar\rho(y)`$.
For a projected minimum there is an attaining completion of that rank;
conversely any full minimum induces a projected minimum. Loss sets therefore
agree when evaluated on those projected minima. This is ordinary finite
minimization over eliminated variables; computing the fiber minima is not free.

Merely dropping variables absent from the task loss is not that operation.
Let the hard fact be $`u=1`$, with soft preference $`x=0`$ of weight 1 and
$`x=u`$ of weight 2. The loss is $`x`$ alone. The full optimum has $`x=1`$
and loss 1. Discarding the hard fact and coupling because the loss omits $`u`$
leaves only the preference $`x=0`$, and incorrectly reports loss 0. The eliminated
coordinate mattered through repair ranking even though not directly through
the consumer payoff. Product factorization as in C04-3 is one sufficient case
where the elimination simplifies legitimately.

## 9. Attainment and output-size limits

An infinite extension with ranks $`\rho(x_n)=1/n`$ has feasible candidates
but no minimum. Empty *minimizer* set then does not mean an impossible antecedent.
The finite implementation avoids this by its explicit finite domain. More
generally a nonempty family with a finite rank image still has an attained
minimum even if its case family is infinite; finite Boolean soft constraints
produce just such a finite image. This observation supplies no search or
membership oracle for that infinite family.

For unrestricted replacement programs, even a finite catalogue can contain a
program whose relevant execution never finishes. Treating an unresolved run as
rejection would wrongly discharge a potentially cheaper candidate. Bounded
execution claims can use P3-03's declared checker and horizon semantics;
unbounded behavioural properties require different evidence. The table adapter
here takes complete finite tables as supplied information, not as free outcomes
of arbitrary program evaluation.

Finally, querying a value or action can demand much less output than listing
all minimizing repairs. With $`k`$ free Boolean coordinates, zero repair rank,
and two losses differing identically by 1, every one of the $`2^k`$ cases is
minimizing but one shared-difference certificate establishes the better action.
A feasible witness plus an outer cover suffices; enumerating all identities is
a different service. This is a mathematical family, while the kernel caps
$`k`$ at 12. A same-access ordinary solver can use exactly the same certificate;
the separation is between requested services, not between Value Logic and
ordinary computation.

## 10. Retaining tautologies is not retaining classical consequence

### CE04-10 — ordinary tautologies on the gap-free fragment

For the admitted propositional language, every classically valid formula is
positively supported at every gap-free paired valuation.

**Proof.** A gap-free valuation gives each atom a true-only, false-only or
both pair. Choose either normal pair below each both pair in coordinatewise
order, leaving the other atoms unchanged. This produces an ordinary valuation
$`v\le h`$ in the knowledge ordering on support bits. A classical tautology
has positive support 1 at $`v`$. The support compilation is coordinatewise
monotone, so its positive support at $`h`$ is also 1. Constants obey the same
argument. No claim is made for formulas with an additional implication whose
support rule is not one of these compiled connectives.

Together with CE04-4 this says that the default normality-prioritized adapter
can preserve all classical propositional tautological formulas at its selected
states while still answering some counterpossibles nonexplosively. It does
**not** preserve the whole classical consequence relation.

To see the distinction, abbreviate material implication as
$`A\to B=\neg A\vee B`$. At $`p=(1,1),q=(0,1)`$, both
$`A=p\wedge\neg p`$ and $`A\to q`$ have positive support, but $`q`$ does
not. Modus ponens for this material abbreviation is therefore not a valid
hypothetical inference rule. In particular the ordinary tautology
$`(p\wedge\neg p)\to q`$ does not license explosion inside the hypothetical.

This is a concrete boundary for later proof transport: a proof cannot be
reused merely because its axiom formulas remain supported. Its inference rules
and interpretation also matter. The broader transport analysis is deferred
to P3-05. Here the response keeps the original classical theorem and the
hypothetical support judgment as different typed claims.

The symbol $`\bot`$ in these notes denotes the **fixed formula falsity
constant**, with pair $`(0,1)`$, not the information-lattice bottom
$`(0,0)`$. They are different objects despite notation shared in parts of the
literature. Consequently $`p\wedge\neg p`$ and this fixed falsity constant
have the same ordinary extension but different hypothetical support behavior.

## 11. A rule-sensitive arithmetic fragment

### CE04-11 — least support is uniquely minimum under retained reference facts

A useful alternative to making every valid material implication into a rule is
an explicit finite **signed Horn policy**. This is a restricted hypothetical
consequence discipline, not a classical consequence oracle.

Let the atoms be exact quoted assertions. For each atom, retain the one support
bit corresponding to its given ordinary reference answer: positive for a true
answer, negative for a false answer. These answers are inputs with an evidence
contract, not magically obtained by the hypothetical solver. Add the hypothetical
seed bits, and a finite set of declared rules of the form

```math
b_1\wedge\cdots\wedge b_k\ \Longrightarrow\ b,
```

where every symbol here is a *positive Boolean variable for a signed support
bit*. The arrow means an operational closure requirement: when all body bits
are 1, the head bit must be 1. It is **not** the paired-support evaluation of
material implication between the original assertions. A negative assertion's
support is a positive variable of the form $`f_p`$, not a test for absence of
$`t_p`$. Empty bodies are permitted as unconditional rules.

Choose a set $`E`$ of atoms allowed to be abnormal. Atoms outside $`E`$ must
remain normal; the ordinary support bits are never removed. Put a strictly
positive normality penalty for each atom in $`E`$ in the first rank tier.
No other penalty competes in that tier. Later rank tiers may be arbitrary.

Start with the reference and seed bits and repeatedly add the head of a rule
whose body is present. Call the fixed point $`T^*`$.

**Claim.** If $`T^*`$ makes an atom outside $`E`$ both-supported, there is no
admissible hypothetical state. Otherwise the valuation with exactly $`T^*`$
as its 1 bits is admissible and is the **unique** minimum-abnormality state,
for every choice of the strictly positive first-tier weights.

**Proof.** Every admissible state contains the initial bits. Inductively it
contains every head added by the procedure, so it contains $`T^*`$. A conflict
outside $`E`$ is therefore fatal for this specific permission policy. In the
other case $`T^*`$ obeys every rule by fixed-point closure and obeys the hard
normality requirements. It includes a reference bit for every atom, so it has
no gaps. Every strictly larger admissible bit set adds an opposite bit at some
previously normal atom in $`E`$. It cannot delete any conflict already in
$`T^*`$. Its first-tier abnormality cost is strictly greater, regardless of
later tiers. Thus $`T^*`$ is the unique minimizer.

The closure terminates after at most $`2n`$ successful new-bit insertions for
$`n`$ atoms. A naive repeated scan makes at most $`2n+1`$ full passes, charging
the actual tested rule bodies; an agenda implementation is an ordinary
alternative. This bound is about a supplied finite rule policy. It includes
neither discovery of the rules nor validation of an arbitrary arithmetic
reference answer. The general weighted solver can reproduce the result by
encoding each rule as an ordinary Boolean hard constraint on support bits.
The special closure algorithm is a familiar least-fixed-point construction,
not a new advantage unavailable to ordinary methods.

The result fails in useful diagnostic ways. If ordinary support bits can be
removed, a competing normal state may replace rather than conflict with a
reference answer. If a seed is a disjunction instead of fixed bits, there can
be several incomparable least completions. If a required normality weight is
zero, strictly larger bit sets may tie. If same-tier outcome preferences or
negative penalties are introduced, a larger completion can win. Nonmonotone
absence tests are not covered by the proof.

### An explicitly quoted arithmetic counterpossible

Let the ordinary interpretation use the usual integers and ordinary addition.
Take three quoted atoms:

```text
p : 2 = 3
q : 2 + 2 = 3 + 3       (equivalently, 4 = 6 in the reference interpretation)
r : 0 = 1
```

All three are false under that unchanged interpretation. Their negative
reference support bits are retained. The antecedent is the exact $`p`$, not
"a report about p says true", and not a change to modular arithmetic or to what
an integer denotes. Its ordinary impossibility is immediate from the given
distinct integer numerals. The hypothetical evaluator exceptionally permits
positive support for this false assertion alongside its retained negative
support. It does not purport to satisfy ordinary equality's reference truth
condition.

First choose a policy with just the signed rule $`t_p\Longrightarrow t_q`$.
Its intended primitive is applying addition to the two sides of the assumed
equality. Permit exceptions for $`p,q`$ and keep $`r`$ normal. CE04-11 gives
$`p,q`$ both-supported and $`r`$ false-only. It supports the particular additive
consequence without making every unrelated query hold by explosion.

Now include the additional signed rule $`t_p\Longrightarrow t_r`$, with its
intended primitive cancellation of the common summand 2. Under the original
exception permissions this request becomes infeasible: it forces a conflict
at the hard-normal $`r`$. With $`r`$ explicitly added to $`E`$, its least state
makes all three atoms both-supported. The reference arithmetic did not change;
the **retained hypothetical rule policy** and/or its exception permissions did.

This does not claim that cancellation is less mathematical than addition, or
that the first policy preserves every rule of ordinary integer arithmetic.
It deliberately does not. The response must list the retained primitive rules,
not say merely "ordinary arithmetic is kept". Both source policies agree on
all three ordinary answers yet give different hypothetical support for $`r`$.
The value representation alone cannot select one policy.

A subtler restriction is essential. The material implication $`p\to r`$ is
classically valid under the reference arithmetic simply because $`p`$ is
false. That extensional fact does not establish that it belongs to the selected
hypothetical rule policy. The policy above names cancellation as its primitive;
a generic proof by contradiction followed by explosion is not interchangeable
with it. In more expressive settings the admission of primitive rules requires
its own evidence or task preference. This finite adapter records that choice
rather than solving the philosophical relevance problem.

Consequent support and numerical evaluation remain distinct. Assigning loss
$`t_r`$ rather than $`1-f_r`$ is an additional payoff interpretation under a
both-supported $`r`$, as CE04-2 shows. Ordinary numerical arithmetic used to
calculate those costs remains classical outside the hypothetical support layer.
The example is therefore a finite rule-sensitive counterpossible interface,
not an arithmetic countermodel and not a forecast about a physically occurring
contradiction.

## 12. Narrowing candidates need not narrow selected consequences

### CE04-12 — surviving-minimum condition

Fix a finite candidate family $`F`$ and its rank, and let $`F'\subseteq F`$ be
a nonempty restriction, for example from newly imposed evidence. If
$`S(F)\cap F'\ne\varnothing`$, then

```math
S(F')=S(F)\cap F'.
```

Indeed a surviving old minimizer attains the old lower bound in the smaller
family, so the minimum rank is unchanged. Conversely every new minimizer then
has that old minimum rank. If no old minimizer survives, every minimizer of
$`F'`$ is outside $`S(F)`$ and has a strictly worse rank.

Consequently nested *feasible* sources do not always give nested *selected*
sources. With candidates $`(\rho,\ell)=(0,0),(1,10)`$, selecting first gives
loss 0. Restricting to the second candidate and then selecting gives loss 10.
The first exact bound does not survive this change. This does not contradict
P3-03's containment theorem: its bound was over a source containing the target,
whereas a bound over $`S(F)`$ is not automatically a bound over all of $`F`$.
A witness that an old minimum survives supplies the stated sufficient condition;
without it the selected-family update needs fresh justification.

This also distinguishes conditioning the already selected family from
recomputing repairs after conditioning the candidate family. In the example
one is empty and the other is nonempty. The request must say which operation
it means. The current implementation deliberately constructs a fresh request
for such changes; it does not offer an incremental mutation that blindly keeps
old rank-pruned cells. General proof reuse is still the later P3-05 task.

Removing some exogenous source possibilities in CE04-6 is a different operation.
If the remaining sources retain their own unchanged feasible repair families,
the union of their minimizing consequences does shrink. Restricting the repairs
*inside* a remaining source can instead trigger the failed-surviving-minimum
case just described.

## 13. Discreteness and the native arithmetic bridge

The Boolean and paired-label domains are part of the semantics. Replacing them
by a continuous interval is not automatically an exact computational shortcut.
Consider one Boolean coordinate and one soft formula $`p\wedge\neg p`$ of
weight 1. Every Boolean case violates it, so both Boolean cases minimize at
rank 1. If the same syntax is continuously relaxed using
$`\min(p,1-p)`$, its violation is minimized at $`p=1/2`$ with rank $`1/2`$.
Reporting $`p=1/2`$ as the uniquely selected hypothetical value would change the
problem, not merely accelerate its solution.

There is a mathematical native piecewise-affine encoding of the domain guard.
For $`x\in[0,1]`$,

```math
\min(x,1-x)\le 0\quad\Longleftrightarrow\quad x\in\{0,1\}.
```

On those guarded bits, conjunction and disjunction use minimum and maximum,
negation uses $`1-x`$, and a paired normality penalty can be written as
$`|t+f-1|`$. With known rational weights these remain finite piecewise-affine
expressions; no product of uncertain quantities is needed. CE04-8 supplies a
finite lexicographic scalarization when a single score is required, with its
coefficient-growth qualification. The alternative is to retain the rank vector.

This is an expression-level bridge, not a claim that the existing native checker
was run on these new compiled obligations. Its actual proof interface still
needs the domain, source, hypothesis and unit premises. Treating an unguarded
continuous box as an *outer bound* can be sound for some services, but solving
the rank-selection problem over that enlarged box can change the minimizers.
The primary counterfactual semantics therefore retains the discrete domain;
any relaxation needs a separately stated inclusion/selection argument.

## 14. A tie set is not a probability law

All-minimizer images and interval hulls are insensitive to making an exact copy
of a candidate with the same rank and the same full queried semantics. A uniform
probability on **candidate identifiers** is not. With equally ranked losses 0
and 2 it gives mean 1. Duplicating the loss-0 candidate gives identifier-uniform
mean $`2/3`$, without introducing any new semantic consequence.

Thus a default average over ties would add a representation-dependent probability
choice. A caller may intentionally use that policy, but must identify what is
sampled and how duplicates are treated. A prior on semantic alternatives,
weights on program identities, a uniform distribution on finite tables and an
all-ties robust query are different services. Equality of observable outputs
alone does not justify merging programs when their runtime or intervention
structure is part of the requested semantics. No arbitrary duplicate-elimination
oracle is supplied here.

## 15. Centering depends on the adapter, not on numeric ranks alone

CF-S4 supplies useful comparison conditions rather than a blanket theorem for
this implementation. The following checks are direct finite arguments about
our own selectors. A normal reference valuation is denoted by $`b`$.

### CE04-13 — conditional weak and strong centering

Assume $`b`$ satisfies the declared hard background and frame as well as the
antecedent. In the default paired adapter, normality is the only scored property.
Then $`b`$ has rank zero, every rank is nonnegative, and $`b`$ is selected.
This is **weak centering** on that restricted request family. If the adapter's
`preserve_baseline` option is enabled, its second tier is the positive bitwise
distance from $`b`$. The reference has distance zero and every distinct case
has positive distance. Thus it is the unique selected state: **strong
centering** for this family.

Arbitrary additional repair penalties can defeat this argument. So can a hard
frame not satisfied by the stated reference. The generic `Request` type does
not promise centering; it is a general finite ranked selector. Nor may an agent
replace an unresolved actual state by a guessed complete reference and then
claim a theorem about that actual state. Sourcewise conditional references
require the separate source contract of CE04-6.

The signed-Horn adapter has a related special case. If its ordinary reference
satisfies every primitive rule and already contains all hypothesis seeds, its
least closure is the reference itself. CE04-11 then gives strong centering.
Its `reference_satisfies_rule_policy` output checks this finite compatibility;
it does not validate the quoted assertions against a full arithmetic theory.

Define an external counterfactual judgment $`A\Rightarrow_R B`$ to mean that
the selected family for $`A`$ is nonempty and every selected state positively
supports $`B`$. If the centering condition holds and $`b\models A`$, then

```math
A\Rightarrow_R B\quad\Longrightarrow\quad b\models B.
```

The proof is simply that the normal $`b`$ is one of the selected cases and its
positive support agrees with ordinary truth. Consequently the external
classical metatheory may infer $`b\models\neg A`$ from a warranted
$`A\Rightarrow_R B`$ and $`b\models\neg B`$, under the same conditions.
This is an external reductio argument. It does not restore the failed
*internal* material modus ponens of CE04-10. In particular a premise about a
counterfactual judgment is not interchangeable with a material-implication
formula positively supported inside an impossible case.

These results establish neither a complete modal counterfactual logic nor a
semantics for nested hypothetical operators. The finite grammar includes only
the displayed Boolean connectives; an external request is not itself a new
unrestricted connective in that grammar.

## 16. Consequence reports need two support channels

For a nonempty selected family $`S`$, the questions

```math
\text{Does every }h\in S\text{ support }B?
\qquad
\text{Does every }h\in S\text{ support }\neg B?
```

are separate. Both can receive yes; both can receive no; and a bounded search
may settle only one. Failure of universal positive support is not the same
thing as universal negative support. The latter must be checked on the
negative-support coordinate.

A cover of all selected cases gives bounds for the two compiled support
expressions. A lower bound of 1 certifies universal support once nonemptiness
is established. An upper bound of 0 refutes universal support on a nonempty
family. A checked *optimal* witness lacking that support also refutes it.
A merely best-found but not certified-optimal witness does not: a better rank
may exclude it. A loose outer bound containing zero is not by itself a selected
counterexample.

The finite consequence adapter uses these criteria. It keeps an empty target,
a still-unproved nonempty target and an unsettled consequence distinct. The
ordinary Boolean kernel checks the compiled bit expressions, while the chosen
front-end policy supplies their hypothetical meaning. This preserves the
harder counterpossible request without using its numerical costs as a hidden
substitute for a consequence relation.

## 17. Uncertain repair ranks require a wider target

### CE04-14 — exact possible-minimizer family for an independent error box

Let a nonempty finite family $`F`$ have estimated scalar ranks $`\widehat r(x)`$
and a certified or explicitly assumed uniform error bound $`\delta\ge0`$.
For each admitted true rank table $`r`$, suppose
$`|r(x)-\widehat r(x)|\le\delta`$ for every $`x\in F`$. Then

```math
\bigcup_r\mathop{\mathrm{argmin}}_{x\in F}r(x)
\ \subseteq\
N_{2\delta}
=\{x\in F:\widehat r(x)\le\min_{y\in F}\widehat r(y)+2\delta\}.
```

For a true minimizer $`x`$ and an estimated minimizer $`y`$,
$`\widehat r(x)\le r(x)+\delta\le r(y)+\delta
\le\widehat r(y)+2\delta`$. This proves inclusion. If the admitted family is
**every independent per-case choice** in the indicated error intervals, the
inclusion is equality. For $`x\in N_{2\delta}`$, set
$`r(x)=\widehat r(x)-\delta`$ and every other rank to its upper endpoint.
Then $`x`$ is a minimizer; ties at the boundary are retained.

A unique estimated winner with a gap strictly exceeding $`2\delta`$ is therefore
stable throughout this box. Equality of the gap does not justify removing the
tied competitor. If rank errors arise from shared uncertain weights or other
structural constraints, the independent-box converse need not hold. The bound
still gives a possibly loose outer family.

This is an elementary finite information-recovery result, not a learning theorem.
A model's asserted confidence does not establish the error bound. Nor does an
error bound in *repair rank* control the downstream *task loss* without another
relation between them. Two cases can have estimated ranks 1 and $`1+\delta`$,
true ranks $`1+\delta`$ and 1, and task losses 0 and an arbitrarily large $`M`$.
They arise, for example, from two distinct one-element violation sets and two
positive weights. Arbitrarily small rank uncertainty can then conceal a change
of task loss by $`M`$.

A robust report bounds task costs on the union of possible true minimizers;
a policy may instead intentionally choose a favorable near-minimal repair.
Those can use the same set $`N_{2\delta}`$ but mean different things. The latter
is preference-guided planning, not an identified explanatory counterfactual.
No probability over the rank tables follows from this construction.

For a fixed Boolean violation profile and a positive closed weight box,
$`\rho_w(x)-\rho_w(y)=\sum_jw_j(b_j(x)-b_j(y))`$ is affine in the weights.
Shared violations cancel. Its exact upper bound is obtained by choosing the
upper endpoint where the difference is positive and the lower endpoint where
it is negative. A candidate is a possible minimizer precisely when the weight
box intersects all of its comparison half-spaces. This is an ordinary finite
linear-feasibility comparison. The current executable policy helper solves the
specified one-parameter version, not arbitrary-dimensional linear programs.

The ordinary branch-and-bound implication is also precise: if $`B`$ is a
feasible incumbent's estimated rank, a cell can be discarded from the possible-
true-minimizer cover when its estimated lower bound is **strictly greater**
than $`B+2\delta`$. A visited candidate cannot be thrown away merely because
its estimated rank is worse than the best found. The current exact-weight
kernel uses threshold $`B`$ and stores exact-best candidates. It must **not**
be reinterpreted as this error-aware algorithm without changing those rules.

## 18. A bounded Boolean gate inside finite affine/min/max syntax

### CE04-15 — a special uncertain product and its unbounded limit

The ban on silently multiplying two uncertain quantities has a useful scoped
exception. For known rational $`L\le U`$, a value $`w\in[L,U]`$ and a Boolean
indicator $`b\in\{0,1\}`$, define

```math
G_{L,U}(w,b)=Lb+\min\bigl(w-L,(U-L)b\bigr).
```

Then $`G_{L,U}(w,b)=wb`$. At $`b=0`$, the nonnegative $`w-L`$ makes the minimum
zero. At $`b=1`$, the bound $`w-L\le U-L`$ makes it $`w-L`$, giving $`w`$.
Only addition, minimum and multiplication by **known rational constants** were
used in the expression. Neither the Boolean condition nor the interval premise can be dropped
in general: with $`L=0,U=1,w=b=1/2`$, the expression is $`1/2`$ rather than
$`1/4`$; with $`w=2,b=1`$ it incorrectly clips to 1 if the interval premise is
ignored.

Thus a bounded uncertain repair weight gated by a discrete violation can have
an exact expression-level representation without granting arbitrary products
of two continuous uncertain variables. A known interval and the genuine
Boolean domain must accompany the representation. Its equivalence is an
algebraic reconstruction; this task does not assert priority or a native
proof-certificate execution for it. It does not change the implemented kernel's
requirement of fixed rational weights.

There is a complementary obstruction for the fixed finite syntax made solely
from affine functions and finite min/max operations. Every such real function
is globally Lipschitz under an ordinary finite-dimensional norm: affine inputs
have finite constants, addition adds constants, fixed scaling multiplies them,
and min/max preserve a finite bound. Therefore a single such expression cannot
agree with $`wb`$ on **all** pairs $`w\in\mathbb R,b\in\{0,1\}`$.
The distance between $`(w,0)`$ and $`(w,1)`$ is 1 in the sup norm, while the
required output difference is $`|w|`$, contradicting any finite Lipschitz
constant.

This obstruction is for that continuous finite min/max-affine syntax. An
explicit branch on a discrete type can represent the unbounded gate; so can
using a separately justified bounded expression for each finite request.
It is not a reason to postulate a globally bounded value range. A richer
carrier or operation remains a revisable design option. The inspected [provisional core, sections 2–3](../../v2/foundations/03_provisional_core.md)
uses exactly finite rational CPWA terms: affine operations, min/max, residual,
nonrecursive lets and fixed rational conversions. Residual is itself a maximum
of an affine difference and zero, so it does not defeat the Lipschitz argument.
This is an expression-level restriction, not a restriction on the richer source
representation or on all future languages.

For typed use, the indicator is dimensionless while the gate and weight have
the weight unit. Its numeric bit must first receive a declared valuation bridge
into that unit with numeric factor 1; the coefficients in the displayed
equation are the known rational coordinates of the interval endpoints in that
unit. For a different known positive bridge factor, divide the coefficients
on the converted bit by that factor instead. All sums and
minima then occur in one unit. Matching numbers is not itself such a bridge.
Neither a CPWA denotation nor these finite arithmetic checks supplies an
automatically accepted native proof certificate. A conditional gate term
must carry the interval, Boolean-source and valuation-bridge premises.

Pointwise expression equivalence is not a license to minimize jointly over
uncertain weights and repairs. With shared unknown weights, the possible
counterfactual family is the union of per-weight minimizing repairs. Treating
weights as freely chosen repair variables can discard an unfavorable admitted
weight case, just as in CE04-6. The gate supplies rank evaluation and uniform
comparison expressions; it does not by itself supply the sourcewise selection
quantifiers. Likewise a native inequality certificate would need to quantify
over the correct discrete source, not just a continuous relaxation of its bits.

## 19. Heterogeneous rank intervals and joint tie realizability

### CE04-16 — exact scalar interval recovery

There is a sharper ordinary interval formulation of CE04-14. Fix a finite
nonempty candidate family $`F`$, finite real intervals
$`[l_x,u_x]`$ with $`l_x\le u_x`$, and admit **every independent scalar rank
choice** $`r(x)\in[l_x,u_x]`$. Define

```math
u_* = \min_{y\in F}u_y,
\qquad
I = \{x\in F:l_x\le u_*\}.
```

Then the union of all possible minimizing families is exactly $`I`$.
Necessity follows from $`l_x\le r(x)\le r(y)\le u_y`$ for every competitor
$`y`$ whenever $`x`$ minimizes. For sufficiency, choose $`r(x)=l_x`$ and every
other candidate at its upper endpoint. The case $`x`$ then minimizes.
The independent uniform error box of CE04-14 is the special case
$`l_x=\widehat r(x)-\delta`$, $`u_x=\widehat r(x)+\delta`$.

A stronger constructive fact holds: **all and only the possible winners can
be tied in one admitted rank table**. Assign

```math
r^*(x)=
\begin{cases}
u_* & x\in I,\\
l_x & x\notin I.
\end{cases}
```

For $`x\in I`$, $`l_x\le u_*\le u_x`$; outside $`I`$ the lower endpoint is
strictly above $`u_*`$. Thus the assignment is admitted and has minimizing
family exactly $`I`$. Nonemptiness follows, for example, by taking a candidate
whose upper endpoint is $`u_*`$. No generic consistency or optimization oracle
is needed once this complete independent interval table is actually supplied.
It takes finitely many endpoint comparisons to construct the family; obtaining
and validating the rank intervals is an additional information cost.

For a **fixed** task loss $`c_a(x)`$ independent of the rank table, the exact
possible selected-loss image is consequently $`\{c_a(x):x\in I\}`$. Uniform
pairwise action comparisons can be made directly on $`I`$. This is the same
ordinary finite information service as unioning the families; the simultaneous
witness shows it is not merely a list of individually incompatible winners
under this particular interval contract.

Three limits are important. First, correlated ranks need not admit that
simultaneous witness. With a shared $`t\in[0,1]`$ and three ranks
$`(0,t,1-t)`$, each candidate can minimize somewhere, but all three can never
tie: the second needs $`t=0`$ and the third $`t=1`$. Such a dependency cannot
be discarded merely because individual intervals are known.

Second, the joint-tie statement is specifically scalar. For lexicographic
ranks $`r_A=(a,5)`$ and $`r_B=(b,0)`$ with independently variable
$`a,b\in[0,1]`$, either candidate can win, but they cannot tie at any admissible
rank vectors. The exact-weight multi-tier kernel and CE04-8 scalarization do
not automatically provide an uncertain-rank extension satisfying this scalar
interval theorem.

Third, if the task loss itself depends on the uncertain rank table, retain
that coupling. For $`c(x,r)=r(x)`$, the attained optimum ranges over

```math
\left[\min_x l_x,\ \min_x u_x\right],
```

not generally over the union of candidate intervals. Both endpoints are
attained by setting all ranks to their lower or upper endpoints, and the
continuous minimum along their linear interpolation attains the intervening
values. For intervals $`[0,0]`$ and $`[0,10]`$, both candidates are possible
winners but the selected rank is always zero. The unconditioned interval for
the second candidate is not its possible loss **when selected**. This is
another reason to preserve selection dependencies in a cost representation.

The characterization is a direct finite reconstruction, not a priority claim.
Its input contract is stronger than mere marginal bounds without independent
attainability. It does not establish how to learn reliable rank intervals or
which repair preferences are philosophically appropriate.

## 20. The unbounded gate is representable by a disjunctive source

### CE04-17 — exact graph lifting without an unbounded arithmetic product

The term obstruction in CE04-15 does **not** prohibit every representation in
the inherited framework. Section 4 of the inspected provisional core permits
finite unions of closed rational polyhedra, including unbounded ones. Introduce
a new coordinate $`g`$ in the same unit as $`w`$ and retain a dimensionless
Boolean coordinate $`b`$. The graph of the desired gate is exactly

```math
\{(w,b,g):b=0,\ g=0\}
\ \cup\
\{(w,b,g):b=1,\ g=w\}.
```

Each branch uses only affine equalities (two inequalities per equality),
with rational coefficients. Neither branch bounds $`w`$. The rational points
$`(0,0,0)`$ and $`(0,1,0)`$ witness the two live branches. All equalities are
within their respective units, so this construction does not multiply or
coerce a dimensionless quantity into a cost unit. The equality $`g=w`$
relates two coordinates already in the same unit.

Projection to $`(w,b)`$ is a bijection between this lifted graph and the
original Boolean-gated source. For every such original point, exactly one
$`g`$ is admitted and equals $`wb`$. A query may use the ordinary source term
$`g`$ after receiving this **explicit graph interpretation**, rather than
silently treating a newly named free variable as the product. Affine losses
using the gate are preserved by the bijection. This is an ordinary disjunctive
linear representation, not an extension of the term grammar or a new
multiplication rule.

If further source constraints are present, intersect both branches with those
constraints. The same mathematical graph equivalence holds. Native admission
still requires the inherited conditions: a feasible witness for each retained
live polyhedral case and an explicit justification for any empty case removed.
A parent case's one witness need not witness both children. The construction
therefore does not provide a free feasibility oracle or an unperformed native
proof-acceptance test. The unrestricted two-branch example above has its
witnesses explicitly; a general source must supply the additional evidence.

Several gates can require many combinations of branch choices if flattened
into the inherited union-of-polyhedra representation. Building, storing and
checking those cases is a resource cost, not eliminated by the algebraic
bijection. A richer symbolic source representation could retain sharing, but
its implementation and checking would need their own account.

Finally, lifting changes representation, not the quantifier meaning of unknown
weights. In uncertain-rank problems, choose minimum repairs **within each
admitted weight/source assignment** before unioning consequences. Allowing the
solver to optimize over the weight coordinate itself would reintroduce the
CE04-6 source-selection error. CE04-15's finite-term limitation and this positive
source-level construction are compatible: they concern different interfaces.
No globally bounded value range is required by either result.

There is also no automatic uniform scalarization of a *continuously uncertain*
lexicographic rank family. Consider two candidates with ranks $`(w_1,0)`$ and
$`(w_2,1)`$, where $`w_1,w_2\in[1,2]`$. For any fixed positive finite first-tier
multiplier $`M`$ (and second-tier coefficient 1), choose
$`w_2=1`$ and $`0<w_1-1<\min(1,1/M)`$. Lexicographic order selects the second
candidate, while the weighted scalar score selects the first. Positive bounds
on the weights do not bound away from zero the difference of two first-tier
ranks. CE04-8 instead scalarizes a **fixed finite rational request**, whose
attainable rank increments can be scaled to integers. Its multiplier must not
be imported unchanged as a uniform solution of this different input family.
