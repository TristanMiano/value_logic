# Repair receipts as a partial convex coverage set

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT source bridge and constructive derivations. No solver installation,
new workload experiment, or completeness claim is made. The two primary readings
below identify concrete algorithmic comparisons for the retained
[repair witness/proof bank](maxsat_reprice_findings.md) and its
[compact representation](reprice_compact_findings.md).

## Two primary algorithms and their actual inputs

**S1. Roijers, Whiteson and Oliehoek (ADT 2013), Computing Convex Coverage Sets
for Multi-Objective Coordination Graphs.**
[Author PDF](https://www.cs.ox.ac.uk/people/shimon.whiteson/pubs/roijersadt13.pdf).
Read Sections 2–6, especially Algorithms 1–4, Theorems 1–3 and Section 6.4,
PDF pp. 2–11. The model has finite joint actions and explicitly available local
vector-payoff factors, combined additively. Linear nonnegative preferences make
a convex coverage set sufficient. CPrune combines Pareto pre-pruning with LP
tests for useful weights. CMOVE applies such pruning during variable elimination,
retaining action tags. This is factor-table processing, not an opaque scalar
solver oracle. Its cost depends on induced width and the intermediate vector
sets/pruning work. The paper explicitly distinguishes its unconstrained model
from weighted constraint satisfaction (Section 2, footnote 4). It does not grant
free handling of arbitrary CNF feasibility.

**S2. Roijers, Scharpff, Spaan, Oliehoek, de Weerdt and Whiteson (ICAPS 2014),
Bounded Approximations for Linear Multi-Objective Planning under Uncertainty.**
[Author PDF](https://roijers.info/pub/roijers2014icaps.pdf).
Read Sections 2.2–3.2, Algorithms 1–2 and Theorems 1–2, PDF pp. 2–5. AOLS
calls a scalarized optimizer and separately evaluates the returned policy's
complete objective vector. It maintains optimistic objective bounds, recomputes
corner weights as its action set changes, and prioritizes possible improvement.
The stated coverage guarantee assumes a known per-call approximation guarantee;
Section 3.2 explicitly weakens the conclusion for an unbounded heuristic solver.
The planning model is finite-horizon, with known dynamics for policy evaluation.
The guarantee uses multiplicative reward accuracy, which should not be copied
unchanged after negating costs. The useful imported mechanism is the oracle,
vector-evaluation, optimistic-bound and acquisition loop; our additive checked
receipts require their own explicit bound algebra.

These are existing strong coverage/pruning and acquisition methods. Their
scalar calls, policy/vector evaluations, LPs and state retention belong in the
comparison bill. Neither method's source gives our provider a free calibrated
law for the cost of its next call.

## Exact correspondence for one fixed repair source

Let F contain the violation vectors a(x) of all hard-feasible repairs. Let S be
the vectors of the checked retained witnesses. Write

```text
P = conv(F),     Q = conv(S),
O = {z in [0,1]^m : q_j dot z >= ell_j for every checked lower cut j}.
```

Every feasible repair satisfies each admitted lower cut, so `Q subset P subset O`.
For a requested nonnegative preference vector w,

```text
L_O(w) = min_(z in O) w dot z
C*(w)  = min_(z in P) w dot z
U_S(w) = min_(z in Q) w dot z = min_(a in S) w dot a.
```

Hence `L_O(w) <= C*(w) <= U_S(w)`. The inner bank supplies executable actions;
the outer bank supplies constraints on what an unknown better action could
achieve. Convexification does not require executing a randomized repair: for
any fixed linear preference, one of the constituent deterministic repairs
attains the minimum. Convex hull and convex coverage set are related objects,
not interchangeable names. A coverage set only needs enough actions to attain
the optimal linear value throughout the declared preference domain.

The current bank is a **partial** coverage set until its residual gap is
certified. An additive certificate over a domain W is

```text
sup_(w in W) [U_S(w) - L_O(w)] <= epsilon.
```

This certifies the bank's optimization loss, not just agreement between two
implementations. Computing that supremum and checking the outer cuts are paid
operations. A few tested weight vectors do not establish it on a continuum.
For replacement price p, the more directly useful certificate is
`min(U_S(w),p)-min(L_O(w),p) <= tau`; it can hold while optimization error remains
large. This supplies the concrete action target for the next acquisition loop.

Normalize nonzero w as `w=s*theta`, `sum(theta)=1`. Exact action rankings are
unchanged, but additive cost gaps scale by s; normalized price/tolerance become
p/s and tau/s. A fixed additive optimization error over the entire unbounded
weight cone is generally impossible without exact coverage. Declare a bounded
weight domain, a normalized tolerance, or the actual price-clipped target.
At w=0 any checked feasible witness has zero repair cost.

## A special feature of Boolean violation vectors

For the complete nonnegative weight cone, ordinary convex pruning cannot remove
more of the current binary witness bank than exact subset pruning already does.
Here is an elementary source-specific argument, independent of either paper.

Take any distinct subset-minimal mask a in the bank. Assign weight 1 to every
coordinate outside a and weight eta, with `0<eta<1/m`, to coordinates inside a.
Then `w dot a<1`. Every other bank mask b has a coordinate outside a: otherwise
b would be a strict subset of a. Consequently `w dot b>=1`. Thus a is uniquely
optimal for these strictly positive preferences. Each subset-minimal mask is
needed for exact coverage of this bank over the unrestricted cone.

This does not prove that it belongs to the unknown true frontier: a new feasible
repair whose mask is a strict subset could replace it. It does explain why
running a more expensive generic convex-pruning LP on the already reduced
binary bank cannot by itself yield another exact compression win.

A constructive route to richer compression is to declare fewer actual preference
objectives. Fix a nonnegative feature map G, such as grouped counts of violated
service, disruption and resource clauses, and use `v(x)=G*a(x)` with group weights
theta. These vectors need not be binary. For illustration, grouped costs
`(0,4), (3,3), (4,0)` are all pairwise nondominated, but the middle action is never
best for a nonnegative linear preference: the cheaper endpoint always beats it.
This is a proposed objective representation, not an observed new benchmark gain.
It must reflect the requested preferences rather than hide inconvenient weights.

## A finite local-factor bridge to the exact CMOVE control

The hard-constraint mismatch has a concrete repair. With normalized clause
weights theta, every feasible binary-mask cost is at most 1. Let h(x) count
violated hard clauses and give the unconstrained factor model vector cost

```text
g(x) = a(x) + 2*h(x)*1.
```

An infeasible assignment costs at least 2 for every normalized preference;
the public feasible witness costs at most 1. Therefore no infeasible assignment
can be optimal. Each penalty is a local factor on that hard clause's variables;
negate these costs to use the source paper's payoff-maximization convention.
For grouped objectives bounded componentwise by B, use `(B+1)*h(x)*1` instead.
The factor tables, induced-width computation, vector joins and pruning must be
constructed and charged. The bridge is a derivation here; no CMOVE execution
or favorable width claim has been made.

## Constructive implication for the next generation

Use an AOLS-style coverage loop with the same persistent IHS scalar provider,
checked witness vectors, scalar lower cuts and compact evaluator available to
every control. Compare its established possible-improvement rule with an
action-value rule that targets the remaining replacement-regret gap, while
charging weight selection, proof acquisition and reusable representation costs.
Choose one explicit low-dimensional preference domain if the application
supports it. Include the factorized exact-coverage control when the declared
source's induced width makes it a credible alternative.

The developmental opportunity is a paid, interruptible coverage service whose
receipts remain usable when preferences change. The guarantee comes from the
checked inner/outer gap; a time-capped optimizer without a warranted residual
bound does not supply the approximation assumption required by AOLS. This is
a focused integration path, not a claim that convex coverage or optimistic
outer approximation is new.
