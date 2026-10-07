# P3-03 — Finite stabilization and task-component projection

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, `/root/bounded_sources`.
Same-model internal mathematical review. Request and local references reviewed
on **2026-10-07T16:21:36.159325+00:00**.

**Disposition:** both proposed mathematical adapters are valid with the
qualifications below. In particular, the impossible completion flag must be
both sound and universally eventually issued; local feasibility does not by
itself license an exact global projection. These are elementary finite-set
reconstructions, available equally to ordinary constraint methods. They are
not yet implementation claims.

## 1. Fixed finite domain and monotone received information

Fix an episode's $`k`$ Boolean coordinates $`Q`$ and operational interpretation.
Let $`H_n`$ be a computably produced finite received prefix, with
$`H_n\subseteq H_{n+1}`$. Each constraint is a total Boolean formula over $`Q`$.
Define

```math
F_n=\{x\in\{0,1\}^{Q}:x\models H_n\},\qquad
F_\infty=\bigcap_{n\ge0}F_n.
```

**Finite stabilization.** There exists $`N`$ such that $`F_n=F_\infty`$ for all
$`n\ge N`$. To prove this, each assignment outside $`F_\infty`$ is excluded at
some finite index. There are only finitely many assignments; take the maximum
of those exclusion indices, or zero if none are excluded. Every later set
contains exactly the assignments never excluded. There are at most $`2^k`$
strict decreases, or $`2^k-1`$ if all sets are promised nonempty.

This concerns the represented sets. The received formula stream can remain
infinite, with arbitrarily long gaps between informative constraints. It need
not reach a syntactic end. The argument also gives no bound on the paid work
needed to filter a given prefix.

**Displayed results require a publication condition.** Exact filtering of
every finite prefix, eventually completed, permits convergence of exact
snapshots when their published prefix indices are cofinal and eventually do
not regress below any fixed index. Publishing the newest completed prefix is
one sufficient policy. Fair computation alone does not prevent repeatedly
displaying an old result, evicting progress or resetting an approximate cover.
The theorem about $`F_n`$ does not automatically make every intermediate cover
converge.

The stabilization is of the **received-constraint abstraction**. With no
received constraints, a coordinate for a true arithmetic sentence still has
both Boolean values in every $`F_n`$. Completeness for arithmetic truth or for
full theory models requires separate hypotheses absent here. Withdrawal,
changes of interpretation and unbounded growth of $`Q`$ also fall outside this
fixed monotone statement.

## 2. No universally effective final-stability certificate

The [halting source/proof note](halting_certificate_obstruction.md) reconstructs
the needed undecidability obstruction from Turing's primary §8. Here is its
specialization to one Boolean coordinate, without another source import.

Given a program $`P`$, let the computable stream issue no constraint until its
simulation observes halting, and then issue $`x=1`$ permanently. Thus

```math
F_n=\{0,1\}\text{ before the receipt},\qquad
F_n=\{1\}\text{ after the receipt}.
```

If $`P`$ never halts, $`F_n=\{0,1\}`$ forever. Every stream stabilizes, and all
constraints can be valid under the same intended valuation $`x=1`$.
Suppose a total computable procedure returned, from the stream program, an
index $`N`$ guaranteed to be after its final set change. Compute $`F_N`$: it is
$`\{1\}`$ exactly when $`P`$ eventually halts. This would decide halting.

Likewise, suppose an effective flag is **sound whenever issued** and
**guaranteed to be issued eventually on every computable stream**. Run until
that flag and inspect the certified final set. This again decides halting.
Both properties together are impossible. An always-false flag is sound, and
sound flags for some terminal situations are possible: an empty set cannot
shrink further; a singleton cannot shrink under a justified nonemptiness
promise. The claim must not rule out these weaker flags.

The flag `source_exactly_filtered` can correctly certify the currently named
finite prefix, its evidence version and its performed computation. It does
not say that no later receipt will narrow that source. Similarly, a particular
task's answer can be permanently settled before the source: in this example
the upper bound on $`x`$ is always one, even though its lower bound can change.
No universal need for full-source stabilization follows.

## 3. Syntactic task components

Fix one finite $`H`$ and a total loss expression $`g`$. Its syntactic variable set
must contain every semantic dependency; expressions have no unrecorded state
access. Start $`R`$ with the variables appearing in $`g`$. Repeatedly add all
variables of every constraint touching $`R`$, until no new variable is added.
This finite closure can be computed by charged scans or graph traversal.

Put every constant constraint in the local collection $`H_R`$. Each remaining
constraint belongs to $`H_R`$ if it touches $`R`$, and to $`H_{\mathrm{rest}}`$
otherwise. At closure, every local constraint uses only $`R`$, and every
remaining constraint uses only $`Q\setminus R`$. Let $`F_R`$ and
$`F_{\mathrm{rest}}`$ be their respective satisfying-assignment sets.

**Factorization.** Identifying an assignment with its two restrictions,

```math
F(H)=F_R\times F_{\mathrm{rest}}.
```

Indeed, satisfaction of the local conjunction depends only on the first
restriction; satisfaction of the other conjunction depends only on the
second. Their conjunction is exactly $`H`$. This proof includes the empty
variable set, whose unconstrained assignment domain has one empty tuple.

**Projection.** The exact statement is

```math
\pi_R F(H)=
\begin{cases}
F_R,&F_{\mathrm{rest}}\ne\varnothing,\\
\varnothing,&F_{\mathrm{rest}}=\varnothing.
\end{cases}
```

Consequently projection equals $`F_R`$ if and only if $`F_R`$ is empty **or**
$`F_{\mathrm{rest}}`$ is nonempty. Exterior nonemptiness is necessary for the
intended useful case of nonempty local extrema. Since $`g`$ depends only on
$`R`$, nonempty factors imply that its global minimum and maximum equal its
local minimum and maximum.

## 4. Counterexamples and service boundaries

**Disjoint contradiction.** Take $`g(q,r)=q`$ and constraints $`r=0`$, $`r=1`$.
Then $`R=\{q\}`$, $`F_R=\{0,1\}`$, but $`F_{\mathrm{rest}}=\varnothing`$.
The local interval $`[0,1]`$ does not establish global feasibility, a global
attainable range, or existence of a normalized law on the global source.
There is no global valuation at all.

**Universal bounds survive dropping constraints.** Forgetting the exterior
constraints widens the global domain to
$`F_R\times\{0,1\}^{Q\setminus R}`$. A computed local enclosure therefore
holds for every full assignment satisfying $`H`$. If global nonemptiness is
unknown, it remains a conditional universal bound; if global conflict is
established, it is not a meaningful numeric feasible-source answer. If
$`F_R`$ itself is empty, factorization already proves global conflict.

The missing nonemptiness bridge can be a checked exterior satisfying
assignment or another valid nonemptiness theorem/semantic premise. Requiring
explicit global assignment recovery would be stronger than necessary.
Without such a bridge, nonempty local computation alone leaves global
feasibility conditional or unresolved.

**Constant constraints.** A false constant conjunct makes the entire source
empty. Placing constants in $`H_R`$ exposes that obstruction even when the
loss is constant or its component has no variables. Silently dropping a
constant false constraint and calling the local source globally feasible is
unsound.

**Closure can overinclude.** The syntactic losses $`q+0r`$ and $`q-q`$ mention
variables irrelevant to their values. A constraint supplied as one formula
$`(q=1)\land(r=1)`$ also couples two variables syntactically even though it can
be split. Closure remains sound but need not be the smallest or cheapest
component. Any simplification or finer decomposition needs its own checked
semantic identity and charged processing; no minimal-relevance oracle is
supplied.

Dropping constraints disjoint from the *initial* loss variables still widens
the source, but does not justify the factorization theorem. For example,
$`q\leftrightarrow r`$ together with $`r=1`$ forces loss $`q`$ to one. Closing
from $`q`$ includes $`r`$ and both constraints. Dropping $`r=1`$ too early loses
that exact conclusion and yields only a looser bound.

## 5. Scientific disposition

The finite descending-chain argument, halting specialization and component
factorization are elementary reconstructions. Their value here is a precise
separation of received-prefix completion, final stability, conditional loss
bounds and feasibility. They do not establish a new learning theory or a
performance advantage. The ordinary comparator receives the same decomposition,
constraints, witnesses, simplifications and resource limits.

This is a mathematical adapter review only. No code, scientific execution,
clock, ledger, status or principal edit was made; there is no additional
concurrent time credit. **P3-N01 remains NOT YET SUPPORTED.**
