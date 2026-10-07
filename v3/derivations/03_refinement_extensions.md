# P3-03 — Refinement, finite tasks and retained evidence

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Companion to [bounded logical uncertainty](03_logical_uncertainty.md).
These are scoped mathematical reconstructions and adapters. The current
executable kernel implements the finite source and bounded VM described in
the principal note; it does not implement the general proof-stream adapter
or the component projection below. All executable evidence remains DEVELOPMENT.

## 1. A finite source can stabilize without announcing that it has finished

Fix one finite, versioned Boolean query list $`Q`$, with $`k`$ coordinates.
Suppose an effective received stream supplies increasing finite sets of total
Boolean constraints $`H_n`$. Here $`n`$ names a finite computational stage,
and $`H_n`$ contains the constraints accepted by that stage; repeated prefixes
are allowed. There need not be a next receipt. Generating, checking, retaining
and filtering that prefix all require work. Define

```math
F_n=\{x\in\{0,1\}^Q:x\models H_n\},\qquad
F_\infty=\bigcap_{n\geq0}F_n.
```

**U03-7 — finite stabilization.** There is a finite index $`N`$ such that
$`F_n=F_\infty`$ for every $`n\geq N`$. For each assignment outside
$`F_\infty`$, choose a finite prefix that excludes it. There are finitely
many assignments, so the largest of these finitely many indices suffices;
use zero if no assignment is ever excluded. Equivalently, there are at most
$`2^k`$ strict decreases, and at most $`2^k-1`$ under a nonemptiness premise.

This elementary descending-chain argument bounds the **number of changes**,
not the time between them. A receipt stream can run forever and contain an
arbitrarily late informative constraint. Stabilization also does not mean
identification of the intended truth vector: an unconstrained true sentence
has both assessment values in every $`F_n`$.

The theorem becomes a convergence statement about displayed exact bounds
only with a processing and publication condition. Suppose every finite
prefix eventually receives sufficient paid filtering work, and published
exact snapshots have indices eventually at least every fixed index. Then
every fixed total rational loss has eventually constant displayed extrema
on $`F_\infty`$, if that source is nonempty and the required arithmetic is
admitted. Publish the newest completed prefix, for example. Fair work alone
does not stop a display policy from repeatedly showing an old prefix or
discarding the only useful retained state. Intermediate loose covers need
their own refinement guarantee.

### An effective universal completion signal is a stronger request

Given a program $`P`$, simulate it. Supply no constraint on one bit $`x`$
until the simulation observes halting, then supply $`x=1`$. All constraints
can be sound for the same intended valuation $`x=1`$. Before the receipt the
source is $`\{0,1\}`$; afterwards it is $`\{1\}`$.

A total computable function that returned, from the stream program, an index
after the final source change would decide halting: compute that prefix and
check which of the two sources remains. Similarly, a computable completion
flag that is always sound when issued **and eventually issued for every
computable stream** would decide halting by waiting for the flag and inspecting
its certified final source. This specializes the classical obstruction in
[U03-6 and its primary-source reconstruction](03_logical_uncertainty.md#91-eventual-guesses-do-not-supply-universally-complete-finite-certificates).

Both conditions on the flag matter. A flag that never fires is sound. Some
terminal situations can be certified: an empty source cannot shrink again,
and a singleton cannot shrink under a separately justified nonemptiness
promise. A certificate for the currently received prefix is also computable.
The kernel's `source_exactly_filtered` has this last, finite-prefix meaning;
it makes no assertion about all future receipts.

A particular task can be settled sooner. In the example, the upper bound on
$`x`$ is always one, while its lower bound may change. More generally, a
current uniform regret certificate survives later source narrowing with the
same objective. Useful stopping for that task does not require a universal
source-completion signal.

### The current storage caps do not implement an infinite stream for free

The executable kernel has at most 128 active constraints and fixed expression
and input caps. An arbitrary infinite stream is outside that interface.
Rejecting its 129th needed constraint does not meet the hypothesis that every
received prefix is eventually processed. An extension must supply an explicit
retention or compression policy and account for its work.

For monotone additions on fixed $`Q`$, an exact Boolean membership table has
only $`2^k`$ entries and can be filtered by each new admitted constraint. That
is a finite semantic representation, not a fixed-total-memory implementation
claim: receipt provenance, counters and histories can grow. In particular,
discarding a premise after incorporating its exclusion can prevent later
withdrawal. Section 4 gives a two-bit obstruction.

## 2. A constructive proof-stream adapter for a fixed logical fragment

The distinction between enumeration and useful refinement can be made precise
without assuming a logical-model oracle. This section specifies a mathematical
adapter beyond the implemented VM, using the type of computable deductive
process compared in [P03-S1](../literature/03_bounded_sources.md).

Let $`\Gamma`$ be a fixed classical theory with a decidable finite-proof
checking relation that completely presents its derivability:
$`\Gamma\vdash\psi`$ exactly when some finite certificate is accepted for
$`\psi`$. Checker soundness here means validity of a derivation, distinct
from truth in the intended interpretation. If its axioms are only effectively enumerable, include
finite enumeration witnesses in proof records; do not assume free axiom-set
membership. Require the usual sound checking and closure under finite
classical propositional reasoning. Fix sentences
$`Q=(\varphi_1,\ldots,\varphi_k)`$ and their explicit syntactic encodings.

Enumerate pairs consisting of a finite Boolean template $`B`$ over these
$`k`$ placeholders and a finite proposed proof of
$`B(\varphi_1,\ldots,\varphi_k)`$. Generation, substitution and proof checking
are computable work. Dovetail the jobs so every finite candidate and every
needed checker prefix eventually receives service, retaining its progress.
Admit $`B`$ only after its proof is checked. The method starts with every
Boolean assessment; it never asks which assessments extend to a full model
of $`\Gamma`$.

Define in the metatheory

```math
F_\Gamma(Q)=\{x\in\{0,1\}^k:
 B(x)=1\text{ whenever }\Gamma\vdash B(\varphi_1,\ldots,\varphi_k)\}.
```

**U03-8 — eventual exactness for the represented proof consequences.**
If every genuine finite proof in the enumeration eventually passes through
the checker, the received source intersection equals $`F_\Gamma(Q)`$.
Sound admission proves one inclusion. For the other, an assignment violating
a provable template is excluded when a proof of that template is processed.
U03-7 then gives eventual finite-source stabilization. Paid exact filtering
and the publication condition in section 1 give eventual exact extrema of
each fixed admitted loss when that source is nonempty. Otherwise exact
filtering eventually reports conflict.

This conclusion is about **provable Boolean relations in the fixed fragment**.
It does not assert an effective stopping index, a rate, or convergence to the
actual truth assignment. If $`\Gamma`$ is consistent, the represented source
is nonempty: otherwise finitely many provable templates would have no Boolean
assignment, and their conjunction would yield a propositional contradiction
inside $`\Gamma`$. This uses a consistency premise, not a consistency test
available to the algorithm. Soundness of $`\Gamma`$ for the intended
interpretation supplies the separate bridge that its actual answer vector
belongs to the source. Consistency alone does not supply that bridge.

If $`\Gamma`$ is consistent and proves each $`\varphi_i`$ or its negation, every coordinate
eventually has its corresponding checked sign and the source is a singleton.
Without that completeness condition, some coordinates may remain unresolved
forever. Provable relations can still settle a loss or an action comparison;
for example, the relation $`x\ne y`$ determines the loss $`x+y=1`$ without
choosing either bit. A detected contradictory source produces conflict,
not arbitrary feasible-source numerical answers.

The logical strength assumptions are substantive. A mere enumeration of all
sentences with a default number attached provides neither the checked
constraint stream nor its narrowing invariant. A complete but unfair proof
enumeration, a checker repeatedly restarted before completion, a receipt
capacity limit that blocks the decisive proof, or a publication policy that
keeps returning the original broad source can each defeat the displayed
conclusion. With a growing active query list, completion of every fixed finite
fragment also does not imply accurate initial reports on the newly requested
sentences.

This supplies a constructive route to a scoped refinement duty. It does not
supply Logical Induction's anticipation, calibration or expert-comparison
theorems, a point forecast, an efficient implementation, or a paid-computation
selection policy. An ordinary proof enumerator plus finite constraint engine
can implement precisely the same adapter with the same accesses and costs.

### 2.1 A task predicate can be provable before its coordinates are decided

There is a useful converse at this fixed finite scope. For any finite Boolean
template $`T`$ over $`Q`$,

```math
F_\Gamma(Q)\subseteq\{x:T(x)=1\}
\quad\Longleftrightarrow\quad
\Gamma\vdash T(\varphi_1,\ldots,\varphi_k).
```

**U03-8a — finite task proof equivalence.** The right-to-left implication
is the definition of $`F_\Gamma(Q)`$. Conversely, for each assignment
$`x`$ with $`T(x)=0`$, membership fails in $`F_\Gamma(Q)`$. Choose a
provable Boolean template $`B_x`$ that this assignment violates. There are
finitely many such assignments. The conjunction of their chosen templates
propositionally implies $`T`$: each assignment falsifying $`T`$ falsifies
its own conjunct. Closure under finite classical propositional consequence
therefore gives a proof of $`T(\varphi_1,\ldots,\varphi_k)`$. If $`T`$
is a tautology, the empty conjunction suffices.

Consistency is not needed for this equivalence; an inconsistent theory gives
an empty source and proves every such template. A useful nonempty-source
certificate retains the consistency/nonemptiness obligation. Interpreted
truth again needs its separate soundness bridge. This finite argument uses
no algorithm for selecting the excluding proofs from an arbitrary input;
the fair proof stream eventually finds the needed finite proofs if they exist.

For a fixed total rational loss $`f`$ on the Boolean domain and a fixed
rational threshold $`t`$, exact finite evaluation can construct the template
$`T(x)=[f(x)\leq t]`$. A fixed finite action catalogue similarly gives
$`T(x)=[R_a(x)\leq\varepsilon]`$. One explicit construction disjoins the
complete assignment clauses for the satisfying rows. This can have
exponential size, and constructing and checking the loss-to-template
translation requires paid evaluation and exact threshold comparisons. It
may exceed the current prototype's expression caps. Propositional proof
checking does not by itself validate an arithmetic encoding or its payoff
interpretation.

Subject to that bridge, the equivalence says precisely when a theory proof
can certify the finite task predicate. The fair adapter eventually supplies
such a proof if it exists, without requiring a separate sign for every
coordinate. For example, a proved $`x\ne y`$ certifies $`x+y=1`$ while
both individual bits can remain undecided. This is ordinary finite theorem
proving applied to the consumer's task. It establishes neither a short-proof
bound nor an advantage over the same task-directed ordinary solver.

The positive-certification statement is not a total decision procedure for
certifiability. A counterexample in the current finite prefix may be excluded
by a later proof. For example, let a stream emit $`x=1`$ only if a program
halts, and ask for the uniform task predicate $`x=1`$. The initial assessment
$`x=0`$ is a current-prefix counterexample; it need not survive the stream.
The eventual source entails the predicate exactly when the program halts.
A sound process that also always finished certifying permanent failure of this
predicate would recover the forbidden total halting decision. In contrast,
a positive uniform bound on a current outer source already remains valid on
all later same-scope narrowed sources. This is why an actionable positive
certificate and a complete answer about every future task have different
stopping requirements.

## 3. Projecting to the consumer's component needs a feasibility bridge

Fix one finite current set $`H`$ of total Boolean constraints and a loss
expression $`g`$ whose syntactic variables include every semantic dependency.
There is no hidden state access. Begin with its variable set $`R`$ and
repeatedly include every variable of every constraint touching $`R`$.
The closure terminates because $`Q`$ is finite. Scanning the expression trees
and their incidence graph is charged work, not a relevance oracle.

Put all constant constraints in $`H_R`$. At closure, put a nonconstant
constraint in $`H_R`$ if it touches $`R`$ and in $`H_S`$ otherwise, where
$`S=Q\setminus R`$. The first collection mentions only $`R`$ and the second
only $`S`$. Let $`F_R`$ and $`F_S`$ be their respective satisfying sets.

**U03-9 — component factorization and projection.** Under the natural split
of an assignment into its two coordinate restrictions,

```math
F(H)=F_R\times F_S,\qquad
\pi_R F(H)=
\begin{cases}
 F_R,&F_S\ne\varnothing,\\
 \varnothing,&F_S=\varnothing.
\end{cases}
```

Each local constraint depends only on its respective restriction, so satisfying
both collections is exactly satisfying $`H`$. This proves the factorization
and the projection formula, including empty coordinate sets. An unconstrained
empty coordinate domain has the single empty assignment.

Consequently the projection equals $`F_R`$ exactly when $`F_R`$ is empty or
$`F_S`$ is nonempty. For a useful nonempty local range, **exterior nonemptiness**
licenses equality of local and global extrema of $`g`$. A checked exterior
witness can supply that premise, but is not necessary: another valid
nonemptiness theorem or explicit semantic bridge can suffice. Demanding
recovery of every exterior truth coordinate would be a stronger service.

Without that premise, a local enclosure is still sound for every full
assignment satisfying $`H`$: dropping exterior constraints widens the domain.
Its global feasibility remains conditional or unresolved. It cannot be
advertised as an attained global range, a complete consistent model, or a
normalized probability law over a known nonempty source.

**Disjoint contradiction.** For loss $`g(q,r)=q`$, take the two constraints
$`r=0`$ and $`r=1`$. The local component has range $`[0,1]`$, while the full
source is empty. A false constant constraint must likewise remain visible;
putting constants in $`H_R`$ catches it even for a constant loss. If the local
source is empty, the factorization itself establishes global conflict.

**Closure and syntax matter.** With $`q\leftrightarrow r`$ and $`r=1`$,
the loss $`q`$ is one on the full source. Closing from $`q`$ includes $`r`$
and both constraints. Discarding constraints disjoint from the initial variable
list too early may still produce a sound wider bound, but loses the exact
factorization. Conversely, $`q+0r`$ syntactically mentions $`r`$ and
$`q-q`$ mentions $`q`$ despite their cancellations. A single supplied
conjunction can also connect otherwise separable factors. The syntactic
closure is safe and computable; it is not generally minimal. A justified
simplification can reduce it, with its own work and proof obligations.

If the component has $`r`$ coordinates, its explicit Boolean enumeration uses
$`2^r`$ local assignments rather than $`2^k`$ full assignments. That is a
conditional count for this enumeration method. It omits neither the component
scan nor any separately required exterior-feasibility work. Ordinary SAT,
constraint and interval methods receive the same decomposition and shortcuts.

This is a present-source semantic adapter. Operational dependency labels can
cross the syntactic components; dropping them can break proof admission or
withdrawal even when the present numerical bound survives. A genuine reduced
implementation must retain an original-source binding and adequate revision
metadata. It does not follow from this projection theorem that all operations,
positions, information access and costs have been recoded identically.

## 4. The exact present source can still forget how to withdraw evidence

**U03-10 — a two-bit retention obstruction.** Compare these active histories,
with no dependency edges and with the same removable identifier `h0`:

| History | `h0` | `h1` | Current exact source |
|---|---|---|---|
| A | $`x=1`$ | $`y=1`$ | $`\{11\}`$ |
| B | $`x=1`$ | $`x\leftrightarrow y`$ | $`\{11\}`$ |

Both have the same exact current source and the same current value $`y=1`$.
After withdrawing `h0`, history A admits $`\{01,11\}`$, with $`y`$ still
one; history B admits $`\{00,11\}`$, with range $`[0,1]`$ for $`y`$.
Thus a record containing only the current feasible set, even if exact, cannot
determine the revised source or this revised loss range for both histories.
The same-record/different-target pair is a complete obstruction to that
decoder. The original premise decomposition distinguishes the histories.

This specializes phase two's [retention principle](../../paper_v2.md#7-what-must-survive-a-cost-revision)
and the dependency role of [assumption-based truth maintenance](../literature/03_bounded_sources.md).
It concerns actual receipt withdrawal, without supplying counterfactual
semantics. The current kernel keeps the active constraint records and resets
the cover after withdrawal; it therefore retains the needed distinction.

The example does not prove that every past byte must be kept. For a restricted
future revision menu, a smaller record might retain exactly the resulting
task ranges or a sufficient dependency certificate. What is insufficient is
the specified present-source-only record. Source compression, task compression
and revision support are different consumers, as in P3-02's recovery contract.

## 5. A frontier that can describe the answer may still be unable to reach it

**U03-11 — parity capacity obstruction for the stated refinement strategy.**
Let the source be odd parity on $`k\geq2`$ Boolean coordinates. Every exact
cover by Boolean cubes uses at least $`C=2^{k-1}`$ cells: a cube with any free
coordinate contains assignments of both parities, so every exact cell must
be a singleton. There are exactly $`C`$ odd assignments, and these singletons
attain the representation minimum.

The present first-free-coordinate, FIFO, split-only-at-commit kernel can stall
with this same cap $`C`$. It reaches $`C`$ partial cells, each with one free
coordinate. None is Strong-Kleene-false for parity, and none is a singleton.
Every attempted split would temporarily increase the committed count to
$`C+1`$, so it is refused and the parent is requeued. Fairly trying every
parent cannot change the state. A full unchanged queue cycle of these
capacity stops establishes this fixed-input stall; an arbitrary timeout is
unnecessary.

Cap $`C+1`$ suffices for this particular FIFO case. One final-level parent can
split. Its two singleton children contain one false parity case, eventually
pruned, which restores the spare slot. The next pending parent can then split.
Continuing source service finishes all parents and checks all leaves.

For the direct recursive XOR expression and no other evidence, the FIFO
counts are $`2C-1`$ successful splits, $`2C`$ singleton visits and
$`C(C-1)/2`$ capacity-stop revisits. The last term counts the successively
smaller groups of waiting parents before each false child frees a slot.
Consequently distinct tree-node counts alone do not bound the number of
transactions under a restricted cap. Reports and scheduler scans are separate
work again. The companion development probe checks this claim against the
actual queue; it does not alter the kernel's strategy.

A constructive alternative shows that the extra slot is algorithmic. Prepare
both children, check the source on each, remove only checked-false children,
and atomically commit **all** survivors if they fit; otherwise retain the
parent. The cover invariant survives because every removed child is certified
infeasible and all other completions are retained. At the final parity split
there is exactly one survivor, so the minimum $`C`$ cells suffice. This is an
ordinary lookahead-pruning transition with additional charged child checks.
It is not implemented by the current kernel or equivalent to its operation
budget merely because both are called one step.

There is no lower bound here against arbitrary ordinary methods. A symbolic
parity calculation can avoid the cube representation entirely. Likewise,
consider $`g(x)=\min(x_k,1-x_k)`$ with no constraints. Under the kernel's
coordinate order, all $`2^k-1`$ successful splits are needed to fix the last
coordinate in every cell and reduce its compositional upper bound to zero.
If the relevant coordinate is scheduled first, one split suffices, though
other coordinates and the entire source remain unresolved. Renaming the
coordinates while changing this schedule is not a cost-preserving identity
recoding unless the priority rule is transported too. A direct Boolean
identity can settle the loss without either enumeration.

### A cap need not admit one least enclosing cover

A further small obstruction explains why the direct containment proof does
not assume a best bounded abstraction. Let
$`S=\{000,011,101\}`$ and permit unions of at most two disjoint Boolean
cubes. Both covers

```math
A=[0**]\cup\{101\},\qquad B=[*0*]\cup\{011\}
```

contain $`S`$. These are members of the mathematical representation class;
no claim is made that the current splitter reaches them with that same cap.
Their intersection is
$`K=\{000,001,011,101\}`$. No union of two cubes contained in $`K`$
can cover $`S`$: any cube containing two of the three points of $`S`$
contains their two-dimensional coordinate rectangle, including a point
outside $`K`$. Thus each such cube can contain at most one of those three
points. A least enclosing two-cube denotation would have to lie inside both
$`A`$ and $`B`$, and hence inside $`K`$, which is impossible.

The two covers can serve different cost queries. The Boolean indicator of
`010` is a min of the appropriately complemented coordinates; its exact
upper value on $`A`$ is one and on $`B`$ is zero. The indicator of `100`
reverses those answers. Both indicators are zero throughout $`S`$ and use
the admitted piecewise-affine grammar. Choosing a bounded cover can therefore
favor one consumer's bound over another without identifying a universally
least enclosing cover in that representation class.

The obstruction also applies to a uniformly best set of upper-loss reports
obtained as exact extrema of denotations in this cover class. Include all
eight Boolean point indicators among
the requested losses. A cover whose exact upper bounds were no greater than
both A's and B's on every such indicator would have to be contained in both
denotations: any extra point would have indicator upper bound one where the
other cover gives zero. It would therefore be a forbidden two-cube enclosure
inside K. This is a fixed finite loss family; it does not rule out a different
representation, a separate proof using the original constraints, or a
smaller sufficient family for one consumer.

This is a hand-derived finite limitation of the declared cap, not another
executed probe or a model-plurality performance result. The current kernel
uses its specified safe transitions and can keep a broader cover; it does
not search for a universally best capped representation. Established abstract
interpretation motivates the containment comparison, but no lattice or
optimal-abstraction hypothesis for this capped class is silently imported.

## 6. Exact loss extrema can encode the finite assessment source

This is another recovery target, distinct from identifying the actual answer
vector or its probability law. Let $`F`$ be a nonempty subset of the known
Boolean domain $`\{0,1\}^k`$. For each known assignment $`z`$, define the
unit-stake Hamming loss

```math
d_z(x)=\sum_{i:z_i=0}x_i+\sum_{i:z_i=1}(1-x_i).
```

It is an affine rational loss, requires only a linear-size expression in
$`k`$, and uses no product of uncertain coordinates.

**U03-12 — a finite source-recovery family.** The exact minima
$`m_z=\min_{x\in F}d_z(x)`$ determine $`F`$ through

```math
z\in F\quad\Longleftrightarrow\quad m_z=0.
```

Each summand is a nonnegative integer on Boolean inputs, and their sum is zero
exactly at $`x=z`$. If $`z`$ is absent from the nonempty finite source, the
minimum is therefore at least one. This proves the equivalence and gives a
constructive family of $`2^k`$ source-recovery queries. It is a sufficient
family, not a minimum query-count or bit-complexity theorem. Computing exact
minima is part of the service and can require the source processing being
investigated; this identity provides no free minimization oracle.

Separate coordinate minima and maxima need not suffice. The two sources
$`\{00,11\}`$ and $`\{01,10\}`$ both give range $`[0,1]`$ for each bit.
But $`d_{00}=x_1+x_2`$ has respective minima zero and one. The already
established XOR example is thus also a concrete distinction between marginal
value information and information about the present joint assessment source.

The exactness premise cannot be dropped. An unfinished structural lower bound
of zero for $`d_{00}`$ does not prove that `00` is feasible: the XOR source's
root cover gives that very loose bound. A positive certified lower bound
does exclude `00`; inclusion needs additional information forcing the minimum to zero, such
as a valid witness, an exact attained minimum, or a gap-resolving error bound.
For example, under nonemptiness a certified upper bound on the true minimum
strictly below one forces membership. A zero lower bound alone does not. The prototype labels these different
source and report statuses explicitly.

If a separately justified estimate of each **minimum** has error strictly
less than $`1/2`$, comparison with $`1/2`$ still recovers membership. Equality
at that error level can be ambiguous: on one bit, minima zero and one can
both produce the estimated value $`1/2`$. Multiplying the known stake by
$`s>0`$ scales the separating gap to $`s`$ and requires error below $`s/2`$.
This is a conditional discrete-gap calculation, not a learned-error guarantee.
It concerns estimates of minima, not an arbitrary interval enclosing all
point losses or an expected-loss estimate.

Interpreting these same loss rows as **expectations under one supplied law**
changes their information content. In that case

```math
E_p[d_z]=\sum_{i:z_i=0}E_p[x_i]+
        \sum_{i:z_i=1}(1-E_p[x_i]),
```

so every such expectation depends only on the coordinate marginals. Equal
mixtures on $`\{00,11\}`$ and $`\{01,10\}`$ give the identical value one
for all four Hamming-loss expectations, although their support sets differ
and their exact minimum families distinguish them. Thus the minimum-family
result is not a probability-recovery theorem in disguised notation. It uses
a different supplied information service. The Boolean unit gap is also
essential to the approximate-membership claim: arbitrary real-valued sources
need not have any positive gap from an absent vertex.

### Why the Boolean domain and the loss family matter

There is an ordinary affine-information boundary behind this positive case.
On the known non-Boolean candidate domain $`Z=\{0,1/2,1\}`$, the two sources
$`F_1=\{0,1\}`$ and $`F_2=\{0,1/2,1\}`$ have the same minimum and maximum
for **every affine loss**. Its value at the middle point is the average of
its endpoint values, so adding that point changes neither extremum. Affine
extrema cannot distinguish the presence of this interior candidate. The
Boolean Hamming family succeeds because each named Boolean vertex has a
known affine nonnegative loss that vanishes only there on the entire domain.
This is the finite convex-hull limitation of affine comparisons in a directly
checkable example, not a special advantage of value notation.

A richer supplied loss family gives a constructive finite extension. Let
$`Z\subset\mathbb{Q}^d`$ be a known finite candidate domain with distinct
points, and let $`F\subseteq Z`$ be nonempty. For each candidate $`z`$, use

```math
D_z(x)=\sum_{j=1}^d\max(x_j-z_j,z_j-x_j).
```

This is the sum of coordinate absolute differences. It is a rational
piecewise-affine expression using known constants, rational scaling, max
and addition; no product of uncertain quantities is needed. It vanishes
exactly at $`z`$. Hence exact minima of this specified family again recover
membership in $`F`$, including interior candidates. If $`Z`$ has another
point, its known finite separation

```math
\delta_z=\min_{w\in Z\setminus\{z\}}D_z(w)>0
```

permits the same argument with certified minimum error strictly below
$`\delta_z/2`$. Constructing the domain, finding this gap and computing the
requested extrema are charged information and work; the expression must
also fit any chosen implementation limits. A singleton candidate domain
needs no separation query under the nonemptiness premise.

The expectation comparison must be recomputed for the richer loss family.
Expected absolute deviations depend on coordinate distributions, not only
their means. On $`Z=\{0,1/2,1\}`$, let $`a=E[X]`$ and
$`b=E[|X-1/2|]`$ under one supplied normalized law. Then
$`p_{1/2}=1-2b`$, $`p_1=a-p_{1/2}/2`$ and
$`p_0=1-p_{1/2}-p_1`$. These richer rows recover that three-point law.
This is a direct instance of [P3-02's finite loss-matrix criterion](02_probability_information.md),
not a general claim that distance expectations recover a joint law in higher
dimensions. The Hamming marginal-means obstruction had its own specified rows.

This is a mathematical extension, not a change to the current Boolean VM.
It makes the choice of loss family substantive. Nor does it make full-source
recovery necessary for a particular decision. For unrestricted nonclosed
real sources, replacing minima by infima can lose actual membership: at
$`z=0`$, both $`F=(0,1]`$ and $`F=[0,1]`$ have infimum distance zero. The
finite attained-source and known-gap assumptions therefore cannot disappear
when the representation is extended.

No normalized probabilities are assigned by these extrema. The same source
may support many subjective laws. The optional ordinary credal family of all
laws supported on $`F`$ has these minima as its lower expectations, but no
single law is selected. Moreover, even recovering this entire present source
does not recover its premise decomposition for withdrawal, as U03-10 shows.
The consumer's requested information remains essential.

## 7. What these extensions add

The contribution is a set of precise boundaries and constructive finite
adapters: received-prefix exactness versus final stability, provable-fragment
refinement versus truth prediction, conditional task projection versus global
feasibility, present-source recovery versus withdrawal support, and storage
representability versus reachable refinement. Their ingredients are ordinary
finite-set, proof-enumeration, constraint and dependency methods.

The current prototype implements a narrower finite operational instance.
These proofs neither establish an efficient general logical learner nor show
an advantage over the strong ordinary combination allowed by P3-01. They
make the remaining obligations more explicit and identify concrete ways a
value query can improve while underlying truth coordinates remain unresolved.
**P3-N01 remains NOT YET SUPPORTED.** No gate or P3-04 task is attempted here.
