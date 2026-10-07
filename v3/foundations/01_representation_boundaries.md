# P3-01 — representation and information boundaries

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Scope: inherited-language and comparison assumptions. These arguments do not
choose a new carrier or establish the P3-02 representation theorem.

## 1. Known coefficients and uncertain quantities are different inputs

The phase-two native term language has rational literals, source coordinates,
fixed rational scaling, min/max/residual, finite lexical bindings and named
fixed rational conversions. Its terms are finite continuous piecewise-affine
functions. Source domains are finite unions of rational polyhedra. Variable
multiplication and division are explicitly outside that fragment
([paper §3.1](../../paper_v2.md#31-sources-terms-and-contexts),
[core §§2–4](../../v2/foundations/03_provisional_core.md)).

For known rational stake `c`, expected failure cost `c(1-p)` is affine in the
uncertain probability coordinate `p`. A new request can supply another known
rational `c`, after which a native term and its current request are constructed
and checked. The fact that coefficients change between requests does not make
them unknown within each request. Construction, arithmetic and checking still
have their declared costs. An arbitrary exact-real coefficient would need an
encoding or approximation contract beyond rational literals.

If both `c` and `p` vary independently over nondegenerate intervals, the exact
function `c(1-p)` is generally outside the native fragment. For a concrete
normalized rectangle `[0,1]^2`, restrict to the diagonal `c=p=t`. Every finite
piecewise-affine term restricts to a finite piecewise-affine function of `t`.
The desired restriction is `t-t^2`, which is not affine on any interval of
positive length: its second derivative is the nonzero constant `-2`. Finitely
many affine pieces therefore cannot equal it on the whole interval.

This is an elementary inherited-closure obstruction, not a theorem that values
cannot express such costs. The first-order reference language can describe
arithmetic multiplication while the native loss kernel has a smaller exact
term language. Expressibility of a relation in the reference theory does not
automatically supply a native term, certificate rule or efficient evaluator.

### A fresh coordinate does not prove its intended relationship

Introducing a cost source `z` makes `z` a legal native term. The equation
`z=c(1-p)` is nevertheless not an affine source constraint. Nor can an exact
finite linear auxiliary encoding repair this graph automatically: projection
of each finite-dimensional polyhedron is polyhedral. Intersect a proposed
finite-union representation with `c=p`; its projection onto `(p,z)` would be
a finite union of polyhedra contained in the strictly curved graph
`z=p-p^2`. A convex polyhedron in that graph has at most one point, since any
segment between distinct points leaves the graph. Finitely many such pieces
cannot cover the interval. This argument concerns the whole continuous graph;
a supplied finite list of parameter cases has different scope.

One valid **outer** relation on this rectangle is

```math
0\le z,\qquad c-p\le z,\qquad z\le c,\qquad z\le1-p.
```

For the true product, the lower nontrivial slack is
`c(1-p)-(c-p)=p(1-c)>=0`; the upper slacks are `cp>=0` and
`(1-c)(1-p)>=0`. Thus every exact product lies in the displayed polyhedron.
The relation is not its exact graph: at `c=p=1/2` it permits every
`z` in `[0,1/2]`, while the exact product is `1/4`. We claim containment only,
not that this derivation is a new relaxation method or an optimal enclosure.

A valid bound over that larger source can transfer to the exact product through
the containment proof. A counterexample found only in the larger source need
not refute the exact computation. Phase two already demonstrates this adapter
pattern for a quadratic continuation
([core §12](../../v2/foundations/03_provisional_core.md#12-complete-interpretation-iii--nonlinear-continuation-with-a-local-enclosure)).
Its use here remains a candidate adaptation. A later task may instead fix a
coefficient, enumerate supplied finite cases, justify tighter enclosures, or
extend the kernel and prove the new rules. No choice is made in P3-01.

## 2. Reading a program is not the same as cheaply knowing its answer

The word “information” has a computational meaning in this project. It must
not silently grant closure under every consequence of a visible string.
Consider a finite random query index `Q` and a fixed Boolean-valued deterministic answer
function `f`, with `Y=f(Q)`. Under the fully specified joint law,

```math
\Pr(Y=1\mid Q=q)=f(q)
```

whenever `q` has positive probability. Equivalently, `Y` is measurable with
respect to the full mathematical information in `Q`. This identity says
nothing about the cost of computing `f(q)`. Even a huge lookup table can define
a perfectly ordinary conditional law whose answer is expensive to produce
under the permitted access model.

A bounded forecast `p(q)` strictly between zero and one can be useful without
being this omniscient conditional probability. It may be an approximate
forecast, a probability model over an explicitly retained abstraction, or a
distribution over unchecked Boolean assessment cases. Which interpretation
is intended must be stated. A score over a randomized query cohort can assess
such a predictor without making one fixed program's output physically random.

In particular, the finite `D_t` construction in the main contract gives
Boolean coherence with **received and represented constraints**. It does not
give all semantic consequences of the program text or all models of the full
arithmetic theory. Those additional consequences require discovery or an
explicitly supplied oracle. S01's assessment-world interface and S11/S12's
distinctions between implicit, explicit and algorithmically available belief
are pertinent comparisons; this is not a new objection to classical logic.

### What a conditional improvement calculation assumes

The squared-loss decomposition in [criterion probes §4](01_criterion_probes.md#4-refinement-has-several-non-equivalent-meanings)
assumes exact conditional expectations under a stated model and nested modeled
information. A metalevel probability model such as S03 also supplies a joint
law of action utilities and computation outcomes. Neither gives a bounded
reasoner free access to those conditional expectations, nor proves that a
chosen abstraction represents uncertainty about its actual code adequately.

For a fully known deterministic query family, buying a computation changes
what the procedure has computed; it does not change the mathematical function
from full input to answer. A useful practical model can represent computation
outcomes as uncertain relative to its retained state. That model needs its
own adequacy, approximation and acquisition contract. Do not describe its
coarse state as all information mathematically implied by visible code.

The ordinary comparator may use the same partial computational model, explicit
belief state, approximate inference and permitted shortcuts. It is neither
forced to be omniscient nor artificially denied visible syntax. P3-03 must
choose a bounded information/update procedure; P3-06/07 must identify which
learning and decision guarantees survive the approximation and its cost.
These are open tasks, not capabilities established by changing probability
notation to value notation.
