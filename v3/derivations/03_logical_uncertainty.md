# P3-03 — Bounded logical uncertainty

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 7, 2026 UTC.
Status: **IN PROGRESS — finite construction exercised; Research90 and closing assessment pending**.
Source: P3-A at `c573b58165826b30ccbb78107ea752169531c45a`.
[Session and prospective contract](../work_logs/P3_03_2026-10-07_S1.md).

## 1. Target and provisional construction

A bounded reasoner can retain a set of possibilities for deterministic
mathematical answers while computing more evidence. The present construction
makes that process explicit for a finite active fragment. Its loss reports
are conditional bounds over represented possibilities. It assigns no default
point probabilities to unresolved claims.

The starting choice is an **anytime outer cover** of partial Boolean assignments,
with typed assumptions and checked evidence, sound interval evaluation of known rational
losses, and explicitly charged finite operations. An unfinished search keeps
its unexplored cells. A checked exclusion under the active premises can remove
a cell; a fallible estimate alone cannot. Caller assumptions restrict only the
corresponding conditional source. Information withdrawal or a changed interpretation makes the
old current warrant stale and requires a fresh cover or justified repair.

This adapts ordinary finite constraint reasoning and interval/abstract
interpretation to the value-query, evidence and revision interface fixed by
P3-01/P3-A. It must be compared with an ordinary implementation of the same
process. Finite Boolean coherence was already reconstructed in P3-01; the
P3-02 information theorems are inherited at their original scope. No novelty
or learning guarantee follows from their names or from this choice.

## 2. Semantic source, received evidence and displayed state

Fix one episode's finite list of versioned atoms
$Q=(q_1,\ldots,q_k)$. Their intended answers form a deterministic vector
$y\in\{0,1\}^k$. The method has the finite input descriptions and whatever
computations or receipts its access contract admits; it is not given $y$.
An atom may be a bounded execution claim, a selected arithmetic sentence or a
Boolean combination with an explicit translation. The implementation must
identify its smaller actually executable class.

Let $H$ be the active finite set of **typed, received and version-matched**
Boolean constraints on these atoms. The prototype distinguishes caller-supplied
conditional assumptions from signed answers admitted by its bounded VM checker.
An assumption's dependency labels support withdrawal; they do not verify its
truth or prove its consequent. Define, in the metatheory,

$$
F(H)=\{x\in\{0,1\}^k:h(x)=1\text{ for every }h\in H\}.
$$

Writing this set does not grant its enumeration or a membership/consistency
oracle. The interpreted-answer bridge is explicit: **every active constraint
used for that bound must be true of $y$**. Caller assumptions therefore make
the result conditional unless that bridge is established separately. Checked
VM facts use the stated operational semantics and its interpreter-correctness
bridge. A fallible forecast does not become a hard fact by being numerically
precise. The prototype does not supply a learned point-forecast channel.

A finite cube $c\in\{0,1,*\}^k$ denotes all its Boolean completions, written
$[c]$. The current cover $C$ denotes

$$
A(C)=\bigcup_{c\in C}[c].
$$

The central invariant is $F(H)\subseteq A(C)$. In particular, when the hard
premises are sound for the intended interpretation, $y\in A(C)$. The cover
need not be exactly $F(H)$, and its cases need not extend to full models of
arithmetic. It records the received finite information and the work performed.

In particular, a supplied program has a determinate bounded-execution answer
even before this reasoner computes it. The opposite Boolean assessment can
remain in $F(H)$ until the corresponding consequence has been checked. Such
assessments represent bounded unresolved information; they are **not advertised
as complete logically possible worlds** under the full operational theory.
Calling their finite mixture coherent below always means relative to the
received finite constraints, with this restricted scope retained.

Initially $C=\{(*,\ldots,*)\}$, a finite description of every Boolean answer
vector. Splitting and deletion will preserve pairwise disjoint cubes. This
makes coverage accounting explicit; neither disjointness nor compact storage
supplies a probability distribution over the cubes or their completions.

Each displayed numerical report names the atom/source epoch, objective and
unit versions, used evidence, cover version, bound type and resource account.
Historical reports remain immutable. A valid earlier enclosure can be retained
for a stronger same-scope source, although dependent current estimates must be
updated or marked stale when required by their report contract.

## 3. Interrupted search: the first decisive check

Suppose one unresolved atom $q$ has loss $f(x)=100x$. A search visits only
$x=0$ and stops. Reporting the visited minimum and maximum, both zero, would
miss the still admissible completion $x=1$. It is therefore invalid as a bound
over the whole source. A visited witness supplies an inner approximation and
cannot by itself certify a universal upper bound.

The proposed cover retains either the unsplit cell `*`, or both children `0`
and `1`. Its correct initial loss interval is $[0,100]$. Visiting the first
child does not discard the second. Only a sound constraint excluding the
second child, or a separately justified loss enclosure there, can improve the
upper endpoint. The same issue appears with a searched list of arithmetic
models, proof candidates or repairs.

This is the first correctness requirement for a bounded implementation:
**every interruption boundary must preserve the unvisited possibilities**.
The method may keep a pending computation, return its last valid source-bound
snapshot, or report an unfinished result. It cannot silently publish the
extrema of only the finished work as exact global extrema.

## 4. Safe refinement operations

For a partial assignment, evaluate Boolean constraints with the usual
three-way partial evaluator: definitely true, definitely false, or unresolved
on the cube. These are properties of a partial computation, not new semantic
truth values for the original deterministic sentence. Negation exchanges true
and false; conjunction is false if a conjunct is false and true only if both
are true; disjunction is dual. Boolean formula nodes and data access cost work.

The intended primitive operations are:

1. **Split:** replace a cube with a free coordinate by its two children with
   that coordinate fixed to zero and one. Their union is exactly the parent.
2. **Prune:** remove a cube only after an admitted constraint has been checked
   definitely false throughout it, or a separately admitted exclusion
   certificate establishes the same fact.
3. **Refine the loss enclosure:** evaluate the declared rational loss on a
   smaller cell using a sound inclusion-monotone interval extension.
4. **Accept evidence:** admit a fully checked, scope-matched hard record;
   incomplete checking changes no hard premise. Direct literal resolution must
   be visible at the next eligible update, while dependent stale calculations
   are marked accordingly.
5. **Revise scope/evidence:** preserve the historical record, invalidate
   unsupported current warrants and restore an outer cover for the new source.

A split/prune commit must be atomic at every observable budget boundary.
Preparing two children in a private work area is allowed; deleting the parent
before their coverage is secured is not. A resource cap may stop progress or
force a safe coarsening; it cannot justify dropping a live branch.

**U03-1 — outer-cover preservation (adapted, proved here).** For fixed $H$, the initial cover contains $F(H)$.
A split preserves its denotation. A certified prune removes no member of
$F(H)$. Thus any finite sequence of completed operations preserves coverage.
An interruption returning a committed snapshot does also. If new sound
constraints are added, their compatible set is a subset of the previous one,
so the previous cover remains an outer cover pending further refinement.

The literal overlay is safe for the same reason. Let $L(H)$ be the set of
assignments satisfying every direct literal in $H$. Each report uses
$A(C)\cap L(H)$, and $F(H)$ is a subset of that intersection. Intersecting the
same literal set with disjoint cubes preserves disjointness. An empty effective
cover certifies finite conflict; it need not wait for the physical queue to
delete all incompatible cells. This is a proof from the maintained invariant,
not authentication of an arbitrary supplied snapshot.

## 5. Loss bounds and native-language scope

Use known rational constants, atom coordinates, addition, known rational
scaling, and the admitted min/max or residual operations. Their exact meanings
are finite piecewise-affine on real coordinate extensions; Boolean inputs are
a finite special case. An interval extension evaluates each cell coordinate
as $[0,0]$, $[1,1]$ or $[0,1]$ and propagates outward bounds through the term.
Negative rational coefficients swap the endpoints. Jointly uncertain products
and general division are not silently added.

If $\ell_f(c)\le f(x)\le u_f(c)$ for all $x\in[c]$, then a nonempty cover
supplies the conditional bound

$$
\min_{c\in C}\ell_f(c)\;\le\; f(y)\;\le\;
\max_{c\in C}u_f(c).
$$

The source, not the use of interval notation, warrants this statement. An
empty exact source means conflict under the admitted constraints; it does not
produce a favorable action value. Failure to find a feasible assignment within
budget is not evidence of that emptiness.

**U03-2 — conditional and nested loss bounds (adapted, proved here).**
The default structural interval evaluator is inclusion-monotone: narrowing
coordinate intervals can only raise a lower endpoint or lower an upper
endpoint for the admitted operations. Accordingly, splitting and pruning at
fixed scope can yield a nested sequence of enclosures. Mere soundness of an
arbitrary evaluator would not prove this numerical monotonicity. Dependency
loss can leave an interval loose until further splitting, even when the exact
function is constant.

For completeness, its nontrivial endpoint rules are

$$
I_{f+g}=[\ell_f+\ell_g,u_f+u_g],\qquad
I_{\min(f,g)}=[\min(\ell_f,\ell_g),\min(u_f,u_g)],
$$

$$
I_{\max(f,g)}=[\max(\ell_f,\ell_g),\max(u_f,u_g)],\qquad
I_{\max(0,f-g)}=[\max(0,\ell_f-u_g),\max(0,u_f-\ell_g)].
$$

Each rule encloses pointwise evaluation. Raising input lower endpoints and
lowering upper endpoints has the same effect on output endpoints; for a
negative known scale the two input endpoints exchange roles. Structural
induction proves soundness and inclusion monotonicity. On singleton coordinates
the induction gives equality at every node. Splitting replaces each cell by
subcells, so the aggregate lower endpoint cannot fall and the upper endpoint
cannot rise, provided numeric reporting succeeds and the remaining effective
cover is nonempty. A conflict or arithmetic limit has its own status and supplies
no replacement numeric interval.

The evaluator is compositional rather than an affine simplifier. Thus even
$x-x$ can initially receive a loose interval. Canonically combining shared
affine coefficients is an available ordinary improvement; its algebra and
cost must be included if selected. The current proof does not call a loose
structural enclosure an exact affine extremum.

## 6. Coherence, feasibility and the optional probability adapter

The nonempty outer cover need not certify $F(H)$ nonempty: it may still contain
only assignments whose incompatibility has not been processed. The status is
**feasibility unresolved** until a full satisfying assignment is checked or a
valid exhaustive exclusion establishes conflict. A sound empty cover proves
finite conflict only with the initial coverage and valid transition record.
No numeric loss interval is issued from a certified empty cover.

Nor may arbitrary probability weights on an unfinished cover be called coherent
with every accepted constraint. Some covered cases may still violate $H$.
A coherent adapter must retain $H$ intensionally in its admissible support, or
use a completely filtered source. Neither description supplies free inference.
After a nonempty finite source $F$ is established, the ordinary credal adapter
containing all normalized laws on $F$ has

$$
\min_{p\in\Delta(F)}\sum_{x\in F}p_x f(x)=\min_{x\in F}f(x),\qquad
\max_{p\in\Delta(F)}\sum_{x\in F}p_x f(x)=\max_{x\in F}f(x).
$$

Every expectation lies between the extreme table entries; point masses attain
them. This inherited finite identity provides a comparison semantics for the
same bounds, not a chosen subjective weighting or efficient solver.

The native real-box embedding is likewise an enclosure. On Boolean inputs,
$\min(x,1-x)$ is zero, whereas its real-box extension can reach $1/2$ on
$[0,1]$. The ordinary interval evaluator may be looser still until it splits
the cell. These are three different objects: Boolean source, real-box source,
and a compositional interval calculation over the box.

### 6.1 Exact polarity and the phase-two interface

The local notation has an explicit translation to phase two. Here $x_i=1$
means that the answer to $q_i$ is true. Phase two's Boolean formula loss is
zero for true, so its formula for that atom uses $1-x_i$. Negation maps to
one minus the formula loss; conjunction and disjunction map to max and min,
respectively. That is the inherited Boolean embedding with the indicator
coordinate complemented, not a change in what a claim means.

The prototype's `resid(f,g)` means the positive difference $\max(0,f-g)$.
Phase two uses $\mathrm{res}(a,b)=\max(0,b-a)$. Therefore the native
translation is **$\mathrm{res}(g,f)$**, with reversed arguments. Addition,
known rational scaling and pointwise min/max retain their numerical meanings
in compatible units. This convention prevents an apparently harmless operator
name from reversing a claimed bound.

For a cube, fix its declared zero/one coordinates and let each star range over
the real interval $[0,1]$. These are rational affine case constraints, so the
resulting finite union of boxes is a phase-two source description. It contains
the Boolean completions. A correctly received native bound over every such
box therefore bounds the original finite assessments by containment. The
reverse implication need not hold: the Boolean function $\min(x,1-x)$ already
separates the sources. Exact singleton cases remove that particular relaxation.

This is a mathematical adapter. The present prototype does not emit native
proof bytecode or invoke the phase-two receiver. Such a path must construct
the actual current cases, terms, units, proof and request, and charge their
creation/checking. A stored scalar or matching old label supplies none of
those receiving obligations. Phase two's proof-relative withdrawal penalty
is also richer than the reset implemented here; its hypotheses and actual
proof must be available before it can replace that reset.

The relevant inherited rules are [paper_v2 §§4.1–4.2 and 6.1–6.3](../../paper_v2.md).
The specialized reset-policy probability ranks and new-mean repair counts in
its §7 retain their original probabilistic/reset assumptions. They are not
rank or optimal-repair theorems for this finite logical assessment state.

## 7. Concrete bounded-query and operation contract

The executable investigation selects finite register-machine programs with
nonnegative integer registers and instructions for increment, zero-test/decrement,
unconditional jump and Boolean halt. A query asks whether a specified program,
on its stated input, halts with its requested bit within its specified horizon
$b$. Executing a halt instruction consumes one VM transition. A horizon of zero
therefore returns false in this chosen semantics. Invalid programs are rejected
as invalid inputs, not assigned false mathematical answers.

The reasoner's budget $B$ is different: it bounds the number of scheduled kernel
transactions in one call. Producer and checking VM states are retained between
calls. A stopped VM job yields no answer. Completing the query horizon without
the requested halt refutes this bounded proposition. An unbounded halting
question is outside this executable family and retains an unsupported/unresolved
status rather than borrowing the bounded refutation rule.

A candidate receipt is bound to the original query's program, registers,
horizon, target and versions. A checker replays that original computation before
admitting the signed answer. Candidate production precedes acceptance;
acceptance is part of the final checking transaction. Checking has its own
retained phase, which can span several calls. The replay and producer share the stipulated VM
interpreter; that does not make them independent implementations or prove the
interpreter's real-world correctness. Development checks use a separate
reference calculation for the finite examples.

### 7.1 A finite resource model, not unit-cost arbitrary arithmetic

Each kernel transaction performs one of a finite set of operations: one VM
transition, one checker transition, one cell inspection/split/prune, one
bounded input or evidence update, or one bounded report calculation. A declared
finite cap on atoms, cells, formula nodes, program size, horizon and rational
bit lengths bounds its semantic data and arithmetic. Cumulative event, cell-ID,
scheduling and diagnostic counters can grow with the run; their bit lengths
and the host's bookkeeping costs are not fixed-width constants. The work is generally
larger for a report or cell scan than for a VM instruction.

The implementation must record those operations and their Boolean/loss-node,
coordinate, rational-arithmetic and storage work separately. A budget measured
in kernel transactions is not an equal-CPU-cost or equal-priced-loss claim.
Host elapsed/CPU observations and any task-loss price vector remain separate.
There is no constant-CPU or fixed-total-memory theorem. The finite operations
also do not establish useful performance as the semantic caps grow. The ordinary comparator has the same
limits, state representation, operations and reported costs.

Input parsing, validation, initial cell construction, snapshot writing and
loading are charged at their actual boundary or reported as setup/serialization
outside the call's kernel allowance. They are never treated as free when a
total resource claim is made. Reports are requested work, not a free scan of an
arbitrarily large source after budget exhaustion. Oversize or failed arithmetic
returns a typed limit/failure and preserves the last committed cover.

At every observable boundary a cube replacement is committed only after both
children have been built. Refusing a split at a cell cap preserves the parent.
The cell cap bounds the **committed frontier**; temporary workspace holds the
parent and its prepared children. The call-boundary guarantee excludes a
process crash inside a transaction. Audit snapshots do not implement authenticated
restoration, and a historical journal is the caller's storage responsibility.
The implementation's completeness claim explicitly requires sufficient
capacity; soundness can survive a cap even when exactness cannot.

| Executed limit or convention | Prototype value |
|---|---|
| Active coordinates; committed cells | At most 12; configurable from 1 to 4,096 |
| Active constraints; named losses | At most 128; at most 16 |
| Expression nodes; recursive depth | At most 256; at most 48 |
| Program instructions; registers | At most 64; at most 4 |
| Proposition horizon | At most 100,000 VM instructions |
| Initial integer/rational input magnitude | At most 64 bits in each admitted component |
| Rational syntax | Bounded signed integer or integer/positive-integer; no exponent notation |
| Rational intermediate guard | Conservative unreduced result bound at most 4,096 bits, checked before the next arithmetic allocation |
| Input boundary | At most 1,000,000 encoded bytes, 100,000 traversal nodes, depth 64; caller construction is outside the method |
| One scheduling call | At most its requested allowance, itself at most 1,000,000 transactions; partial states persist across calls |

For $m$ current cells, $h$ constraints, at most $s$ nodes per constraint/loss,
and $k$ coordinates, a source inspection visits at most $hs$ Boolean nodes
and a report visits at most $ms$ loss nodes, plus overlay, coordinate and
identity work. The naive withdrawal closure may require up to $h$ passes over
the dependency records. These finite envelopes are deliberately heterogeneous.
The instrumented counters describe selected work units; they are not a full
machine-instruction account. Embedded report/snapshot counters end before that
object's own serialization, whose bytes are recorded in subsequent kernel state.

### 7.2 Literal uptake and stale calculations

An accepted signed answer is available as a direct coordinate fact at the next
eligible report. Other loss calculations use a literal overlay on the current
cover, or retain an explicitly identified earlier valid conservative enclosure
while recomputation is pending. They cannot continue to advertise a contradictory
point estimate as a current hard result. A fallible point predictor, if later
added, is a separate report type and must follow the same receipt/version order.

An added hard constraint shrinks the intended source; the old cover can remain
sound while its work queue is refreshed. Scope withdrawal instead can enlarge
the source. This asymmetry determines the repair policy below.

## 8. Withdrawal, changed objectives and finite growth

The basic constructive revision policy is **reset to the outer top for the new
active source**, retaining only independently valid facts for their original
versioned query identities. Any proof records remain historical conditional
objects. Resetting can discard useful refinement work; its safety does not
make it the optimal repair. A more selective method needs accessible exclusion
records and dependency information, with their storage and checking costs.

For one bit, a source restricted by $q=1$ can yield $[1,1]$ for loss $q$.
After that premise is withdrawn, the compatible source includes zero. Keeping
the old survivor alone is unsound; a reset yields $[0,1]$. Withdrawal of a
premise does not prove its negation. If another retained independent receipt
still establishes $q=1$, that particular resolution may survive.

Changing only a loss function or its unit does not require forgetting valid
truth receipts. It does require a newly bound loss report and resource account.
Changing a program/horizon/interpretation creates a different query identity;
its old answer is not inherited by matching the displayed name. The conservative
implementation may start a new episode, with historical records preserved.

Appending a genuinely new atom extends each existing cube by a star. Projection
onto the old coordinates returns the old represented set. An old objective
that ignores the new atom therefore has the same semantic extrema. Adding a
new cross-constraint is another evidence update; its computational processing
and any changed report scope must be charged.

This append construction is a mathematical extension, not an implemented
in-place API. The executable keeps its query list fixed and starts a new kernel
for a changed query/program/interpretation. Likewise arbitrary theory proof
enumeration and selective exclusion repair are possible adapter obligations,
not services supplied by this VM prototype.

A one-cube cap cannot represent exactly the XOR source $\{01,10\}$ by an
ordinary cube: its smallest covering cube is `**` and also includes `00,11`.
It may keep the XOR constraint intensionally, return a wider enclosure, or use
another representation with declared costs. Silently deleting one alternative
would sacrifice soundness. Thus bounded storage and universal eventual exactness
are separate obligations.

## 9. Fixed-query resolution and the quantifier boundary

**U03-3 — retained fixed-query resolution (proved conditional statement).**
For one eventually fixed versioned query, suppose a correct signed receipt has
a finite admitted production and checking computation. Suppose the scheduler
supplies every required finite prefix of that computation, keeps its partial
state, and retains the eventual accepted result for subsequent reports. Then
there is a finite eligible report event after which that query is resolved
correctly. The argument covers true and false bounded claims alike: finite
work completes, its signed result is checked, and later reports use it.

There is a concrete bound for the fixed finite VM scheduler. If the query's
execution stops after $r$ instructions, production and replay each use
$\max(1,r)$ scheduled transactions; the extra convention handles a zero
horizon. In `all` scheduling mode, at most $k+1$ eligible transactions occur
between services to that job. With retained state, no request corruption or
source withdrawal, and sufficient evidence capacity throughout, acceptance
occurs within

$$
2(k+1)\max(1,r)
$$

scheduled transactions from initial service scheduling. A requested report is
additional charged work. This is a coarse operation bound for an explicitly
bounded query, not anticipatory success before its own production/replay cost.
Using a mode that deliberately omits the job does not meet the premise.

For general theory-based proof enumeration, the corresponding premise is an
admissible proof or refutation that the effective checker can eventually process.
Merely having an interpreted truth value is insufficient. A particular external
decidable family instead needs its supplied total decision procedure. No
consistency oracle or decision procedure for arbitrary arithmetic is obtained.

Unbounded total budget alone does not imply the needed fairness: a scheduler
can starve a particular job, restart its checker on every visit, or repeatedly
evict its only accepted receipt. Retained progress and information are part
of the theorem, not implicit consequences of a round counter.

**U03-4 — finite-source completion (adapted, proved here).**
For a fixed finite active fragment and fixed $H$, fair full splitting and
constraint checking eventually reach all its Boolean leaves when the storage
cap permits the required frontier and every required checking, arithmetic and
report operation fits its declared limits and is eventually scheduled. There are at most $2^k-1$ splits and
$2^{k+1}-1$ processed nodes in the full binary tree. Strong-Kleene evaluation
is exact on complete assignments, and the rational loss evaluator is exact
on singleton cells. Hence this process eventually computes the exact extrema
on the **received finite assessment source** when it is nonempty; an empty
source instead yields finite conflict. It need not discover constraints
that were never admitted.

These are fixed-query/finite-fragment statements. Requesting a fresh unresolved
query at every round can leave every initial report at its default even though
each old query is eventually resolved. A default midpoint forecast $1/2$ on a
sequence of true queries has squared error $1/4$ at every initial report.
This is a counterexample to that inference about the stipulated process,
not a complexity lower bound against an ordinary solver with a valid shortcut.
Enumeration, total lookup/defaults, fixed-query eventual resolution and
anticipatory refinement remain different services.

### 9.1 Eventual guesses do not supply universally complete finite certificates

**U03-6 — obstruction for an unbounded extension (classical reduction,
reconstructed here).** Fix an effective universal program encoding and one
operational semantics. Suppose a computable process eventually accepts a finite
signed answer to the unbounded halting question for every program, and every
accepted sign is correct. Running it until its first accepted sign would be a
total halting decider. Such a decider would decide whether a Turing machine
ever prints a specified symbol: simulate that machine and halt exactly on the
designated printing event, continuing to idle if the simulation stops without
it. This contradicts Turing's §8 result.

The primary anchor is [Turing 1936, §8, printed p. 248](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf),
whose stated problem is eventual symbol printing. The modern halting reduction
and this accepted-certificate interface are reconstructed here; Turing's
circle-free predicate is not silently equated with halting. The
[source/proof addendum](../work_logs/P3_03_2026-10-07_S1/reviews/halting_certificate_obstruction.md)
records the exact import and independently checked reasoning.

No common deadline was assumed: completion could take an arbitrary finite
time depending on the program. Earlier explicitly fallible guesses do not
defeat the argument, because the decider waits for accepted evidence. A
noncomputable external oracle, or a theory-relative derivation lacking the
semantic soundness bridge, does not satisfy these premises. Particular
unbounded programs can still have sound negative certificates, and restricted
decidable families can still have complete procedures.

A weaker service is possible. Let $H(P)$ be the unbounded halting bit and set
$h_t(P)=1$ if simulation observes a halt within $t$ transitions, and zero
otherwise. Every finite output is computable with its simulation work charged.
If $P$ halts after $T$ steps, then $h_t(P)=1$ for every $t\geq T$; if it
never halts, every estimate is zero. Thus $h_t(P)$ converges to $H(P)$ for
every fixed program. Its provisional zero is an estimate, **not a finite
certificate of nonhalting**. An effective universal signal that the zero had
become permanently correct would restore the forbidden decider.

For a growing family, let $P_n$ execute $n$ increments and then a halt
instruction. Its true unbounded halting bit is one, but $h_n(P_n)=0$ for
every $n$. A structural shortcut can recognize this simple family earlier;
the example attacks the claimed implication from pointwise convergence for
the stipulated estimator, not every ordinary reasoning method. This explains
why the finite VM's sound negative answer about a **stated horizon** must not
be advertised as either unbounded refutation or learned anticipation.

## 10. Primary comparison and an informative value-only case

The [targeted source contracts](../literature/03_bounded_sources.md) make
the ordinary comparison concrete. Logical Induction's computable deductive
process and provability induction have different hypotheses and quantifiers
from a finite VM scheduler. Abstract interpretation supplies the established
containment/refinement perspective. Assumption-based truth maintenance supplies
dependency and withdrawal mechanisms. Algorithmic knowledge separates the
procedure's accessible answer from consequences implicit in its visible input.
The primary passages were rechecked by the principal as well as the internal
source reviewer; this is selective inspection, not replication of every proof.

A source refinement can help a value query while leaving the individual truth
coordinates unresolved. Take received constraint $x\ne y$ on two Boolean
atoms and loss $f=x+y$. Both atoms remain individually unresolved on the
compatible source $\{01,10\}$, but the loss is exactly one. Processing the
finite source can tighten an initial interval $[0,2]$ to $[1,1]$ without finding
which actual atom is true. The ordinary constraint method obtains the same
answer, including any available symbolic shortcut from the XOR relation.

An even smaller computational example is $f(x)=\min(x,1-x)$. On the unchanged
Boolean source $\{0,1\}$ its exact value is zero. The root-cell compositional
interval is $[0,1]$; splitting into the two Boolean leaves makes both leaf
intervals $[0,0]$. No new truth receipt has arrived and the answer to $x$ remains
unresolved. The intervening work improves a bound on the consumer's loss.
This distinguishes processing existing information from receiving new evidence.
It is an elementary finite case exercised in development attempt 1;
it does not establish learned anticipation or an advantage over ordinary code.

For the exact ordinary reconstruction, use the identity map on query bytes,
accepted constraints, frontier cells, pending producer/checker work, known
loss terms, scope versions, event order and resource charges. Execute the same
operations and tie rules. Induction on the common transcript gives identical
states, reports and costs. No probability conversion is necessary for this
reference; the optional credal adapter is a separate supplied interpretation.

### 10.1 A terminal task certificate

**U03-5 — named-action certificate (ordinary reconstruction, adapted here).**
Fix a finite supplied action catalogue $B$, common declared loss units,
a selected action $a\in B$ and tolerance $\varepsilon\geq0$. Its regret at
one shared assessment $x$ is

$$
R_a(x)=\ell_a(x)-\min_{b\in B}\ell_b(x)
      =\max\bigl(0,\max_{b\in B\setminus\{a\}}
           (\ell_a(x)-\ell_b(x))\bigr).
$$

For a one-action catalogue the final expression is defined to be zero.
Subtraction by a common number reverses the ordering of the compared losses,
which proves the identity. The finite maximum and positive differences use the
existing rational loss language when their constructed expression fits its
size and arithmetic limits.

If a sound current-source upper bound $u_a$ on $R_a$ satisfies
$u_a\leq\varepsilon$, then

$$
\ell_a(x)\leq\min_{b\in B}\ell_b(x)+\varepsilon
\quad\text{for every }x\in F(H).
$$

The guarantee concerns every action in the **supplied** catalogue, not every
possible real-world option. It transfers to the interpreted truth vector only
through the same premise bridge as the loss bounds. A finite conflict does
not produce an action certificate. Otherwise an unresolved feasibility status
retains the guarantee's conditional status. For a nonempty exactly evaluated
finite source, such a uniform certificate exists precisely when
$\max_{x\in F(H)}R_a(x)\leq\varepsilon$. A loose upper bound above the
threshold does not itself prove the certificate impossible.

At fixed source and objective, the existing interval refinement makes $u_a$
nonincreasing. Thus the threshold, once certified, survives further such work.
The request must bind the chosen action, complete supplied catalogue, original
losses, shared unit, tolerance and active-source identity. Giving an unrelated
term the name `regret_A` does not check that construction. Compilation and its
checks cost work; a later objective change requires a newly validated request.

This is a terminal action-quality service. It neither assigns a probability
law nor chooses which future computation to buy, and introduces no learning
rate or sequential forecast claim.

### 10.2 Shared uncertainty can cancel from the consumer's comparison

Let $x$ remain unresolved on $\{0,1\}$ and take

$$
\ell_A(x)=10x,\qquad \ell_B(x)=10x+1.
$$

Their exact marginal loss ranges remain $[0,10]$ and $[1,11]$. Neither loss
level is identified, and the ranges overlap. Yet $R_A(x)=0$ everywhere.
The current structural evaluator initially gives the uncancelled positive
difference an upper bound of nine; splitting into the two Boolean cells
gives zero on both. This certifies A without learning the actual value of
$x$ or either actual cost. An ordinary symbolic cancellation rule can reach
the conclusion earlier; that permitted shortcut belongs to O-COMB too.

The relationship really matters. Replacing B's loss by $11-10x$ leaves both
marginal ranges unchanged, but A's regret becomes nine at $x=1$. Separate
ranges do not retain the shared-assignment comparison. This is a range-level
adaptation of P3-02's dependence warning, now tied to a bounded certificate
that the consumer can request.

More generally, a shared unknown component $g(x)$ cancels when
$\ell_b(x)=g(x)+d_b(x)$ for every supplied action. Recovering the absolute
cost levels can require information that the comparison does not require.
A common change $\ell'_b(x)=\alpha\ell_b(x)+\beta(x)$ with known
$\alpha>0$ gives $R'_a(x)=\alpha R_a(x)$. A certificate therefore transports
with tolerance $\alpha\varepsilon$ under that declared relationship. This
is a mathematical transport rule, not an implemented arbitrary rewrite checker.

Action-specific price changes need more information. In the example, doubling
only A's loss gives $20x$ versus $10x+1$: A is best at zero but has regret
nine at one. The earlier zero-regret number alone does not warrant the new
comparison. Retaining the original source and loss expressions allows a fresh
calculation, consistent with the phase-two retention interface and P3-02's
task-specific information distinctions.

### 10.3 A precise obstruction for this certificate service

On the same unresolved source let $\ell_A(x)=x$ and $\ell_B(x)=1-x$.
A is uniquely best at zero and B at one. Each fixed pure action has worst-case
regret one. Hence neither can have a sound uniform certificate with tolerance
below one on this source, however thoroughly the source is enumerated.
This is a limitation of the stated information and requested service.
An allowed computation that resolves $x$, a different action catalogue, or a
separately supplied subjective-law objective can change the question.

Randomized actions are another distinct service. If A is selected with a
known probability $r$, independently of the unresolved bit, its loss averaged
over that internal randomization is $rx+(1-r)(1-x)$. Its worst expected regret
over the two assessments is $\max(r,1-r)$, minimized at $r=1/2$ with value
$1/2$. Realized worst-case regret remains one. A known rational mixture can
be admitted as another explicitly interpreted action; this averages the
action's coin, not a supplied probability law for mathematical truth.

Similarly, the pointwise minimum in the regret benchmark is not automatically
an executable plan that sees $x$. The selected named action is fixed before
the hidden assessment is known. This preserves phase two's distinction between
an expression's pointwise minimum and a policy with the required information.

It does not prove a general computational lower bound: the original query
may have a cheap proof available to an ordinary method. Conversely, merely
improving an enclosure until it equals the correct worst-case regret cannot
manufacture a uniformly good pure action where none exists.

## 11. Development evidence and remaining work

The [kernel](../checks/03_bounded_logic.py) and
[independent finite evaluator](../checks/03_bounded_logic_check.py) have completed
[development attempt 1](../work_logs/P3_03_2026-10-07_S1/development/attempt_1/summary.json):
22 source cases, 162 interruption boundaries, 306 partial-cube visits, nine
bounded VM queries and the named revision, binding and resource-limit checks.
All twelve suites passed, with 10,840 explicit assertions. These are small
finite correctness diagnostics, not independent samples, a blind anticipation
test or a final challenge. The source/evaluator/code versions and complete
traces are bound in that attempt's prospective manifest.

The [terminal task wrapper](../checks/03_task_certificate.py) subsequently
passed its [separate development attempt](../work_logs/P3_03_2026-10-07_S1/development/task_certificate_attempt_1/summary.json),
with nine targeted suites and 64 assertions. The principal's final inspection
and current dependency audit remain pending. Its compilation, binding and
threshold work are recorded separately from the core transaction allowance.

The [mathematical](../work_logs/P3_03_2026-10-07_S1/reviews/bounded_reconstruction.md),
[implementation](../work_logs/P3_03_2026-10-07_S1/reviews/implementation_review.md)
and [harness](../work_logs/P3_03_2026-10-07_S1/reviews/harness_review.md) reviews
are same-model internal, nonblind reviews. They add no concurrent research
minutes. Source/code hashes in earlier review and execution records identify
their historical snapshots; later text additions do not rewrite those records.

Remaining work: check the growing-deduction/fixed-fragment boundary and
task-specific projection conditions; finish current-request binding review,
the duty/contribution disposition and the protected Research90 remainder;
then synchronize exact actuals, claims and status. The rendering repair is
separate administrative work. P3-04 remains unstarted.
