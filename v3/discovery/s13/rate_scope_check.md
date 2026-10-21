# Same-model scope reconstruction of the acquisition-rate claim

Codex (GPT-6), DEVELOPMENT, October20,2026. Reliable-lane self-check;
not independent confirmation or novelty assessment.

## The local inequality's actual dependencies

For a deterministic episode at a fixed public history, the private query tree
must be fixed independently of the unresolved world. It may branch on answers
purchased during that episode. Every different-invoice cube edge has a unique
first divergent query, and the pairs crossing one query split form a matching.
The structural charge S overestimates those actual pairs. It is important
that the abstract mass relaxation is only an upper bound; no assertion that
arbitrary relaxed masses are a realizable Boolean source is needed for soundness.

The recurrence maximizes that upper bound. For its nonnegative rho<=1/2,
D_h>=-rho and D_h is nondecreasing. Consequently the change from a one-active
child optimum to a two-active-child optimum occurs at most once as depth grows.
This justifies the H-1 explicit shapes in the rate envelope. The rational
probe checks many values, but the recurrence/crossover argument is the proof.

The upper construction attains the leading rate by removing blocks of bits
whose *parity* the invoice determines. It does not pretend to recover each
prelude bit. Independent fair remaining bits follow because the transcript
depends only on the removed block; the discarded marker answer cannot affect
that transcript. Marker purchases may read a remaining coordinate, but because
its answer is not used or revealed, they do not condition its distribution.

## Interfaces that would invalidate an unqualified statement

- Private answer memory does not persist between episodes except through
  the publicly observed invoice. Retaining a free private cache can change
  later programs without new purchases and defeats the local argument.
- The observer sees no additional answer, branch identity, success/abort flag,
  query identity trace or intermediate timing message. Such an observation
  changes the information interface and requires its own lower bound.
- Unit query fees and a fixed known reset fee are exact. Refunds, hidden
  outcome-dependent prices and an uncalibrated timer are different models.
  uncertain_prices.md gives a separate sufficient interval condition.
- Public/private coins are independent of the hidden source. Free advice
  correlated with that source is additional information, not randomness.
- The exact rate concerns query-plus-reset fees. Source knowledge, control
  arithmetic, storage and compilation have not become free in an application.

No-repeat is used by the upper implementation. The first-divergence lower
argument also tolerates repeated coordinate queries; repetitions cannot add
a matching at a split whose value is already fixed on that private path.
This observation does not grant other free memory operations.

## A sharper zero-reset remainder

At f=0, the old variable-prefix policy shortens its prefix to
min(k,H-1) near the end. Let beta0=1/(2^H-2) and R_k be its marker surcharge.
For1<=k<=H-1, R_k=1/2. For larger k, R_k-beta0*k is a convex combination
of earlier such remainders (s12's exact recurrence). Since the initial
remainders lie in[0,1/2-beta0], for every n>=H>=2,

```math
n(1+\beta_0)\le\mathrm{OPT}_{n,H,0}\le V_{n,H,0}
\le n(1+\beta_0)+\frac12-\beta_0.
```

Thus the construction is within less than half a fee unit of the optimum
for every cap and every n in this contract, not only asymptotically. Exact
finite-n optimality remains open. Cap3's explicit remainder gives the sharper
quarter-unit bound for n>=3. This is a theoretical gap bound, not an observed
algorithm speedup.

As a corollary, choosing H=ceil(log2(n))+1 (when H<=n) yields expected fee
at most n+1 for complete vector recovery. Indeed2^H>=2n and the displayed
upper surcharge is at most1/2+(n-1)/(2^H-2)<=1. A logarithmic private cap is
enough for this average-fee statement; the hard worst bill and episode count
can be much larger. Positive reset fees can remove this consequence.

## A cheap failed finite-remainder repair

Adding a fixed positive surcharge per still edge-incident vertex to the linear
edge potential is unsound. Take a two-dimensional residual cube, cap3, and a
known distinct marker coordinate. A two-bit prefix episode costs7 query units
summed over its four worlds and removes3 cube edges, saturating the7/3 local
edge price. Two worlds become isolated in their invoice cells, while two retain
one edge. Any positive charge for newly isolated vertices would demand extra
cost where the linear inequality has no slack. The final one-bit acquisition
does have slack, but a correct remainder potential must transport that slack
across branches. This counterexample rejects this simple refinement without
launching a larger finite-optimality search.
