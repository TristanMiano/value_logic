# From optimal repairs to a quantitative tolerance for disagreement

Codex (GPT-6), October 19, 2026. DEVELOPMENT derivation, Q2–5.
Extends [optimal_repair_source.md](optimal_repair_source.md) using ordinary
minimum-cut sensitivity and the local permission compiler. The representation
is an announced model-repair policy, not an empirical probability law.

## A fixed repair budget and its local margins

Let E(x) be the positive weighted implication/unit violation cost, with hard
literal assumptions A. Let e0=min E over A, assumed feasible. For rho>=0,
retain W_rho={x: A(x), E(x)<=e0+rho}. After a maximum flow, the residual cut
capacity of x is exactly E(x)-e0. Thus the entire near-optimal family is a
residual cut-budget set. At rho=0 it is the residual implication source; at
positive rho it generally is not binary-definable.

For scope J and pattern v define mu_J(v)=min(E(x)-e0: A(x), x_J=v), with
infinity for infeasible patterns. Each value is a terminal cut problem with
additional hard units. These are ordinary constrained minima, not free
oracles. The local projection is exactly {v: mu_J(v)<=rho}. A prepared table
therefore serves every tolerance rho without another source inference.

For a CNF target G and toggle mask d, let a_C be the falsifying pattern of
clause C on J_C. Its exact failure margin is

    Gamma(d) = min_C mu_(J_C)(d_(J_C) XOR a_C).

Every retained repair satisfies G after d exactly when rho<Gamma(d).
Equality is unsafe, since the definition retains repairs at the budget
boundary. Infinity means no hard-compatible failure. A finite margin has a
minimum-cut witness whose edit violates the target. This is useful even when
one does not pretend that rho has a calibrated probability interpretation.

Preparation needs at most sum_C 2^|J_C| constrained cuts. For a fixed proposed
mask, only one constrained cut per target clause is necessary. Producing,
checking and storing flow/cut certificates and the original model all cost
work. No end-to-end runtime improvement is measured here.

## Select a mask with the largest tolerance

For binary targets and a supplied 2-CNF constraint B on legal masks, ask whether
some legal mask has Gamma(d)>rho. For every local pattern v with mu_J(v)<=rho,
forbid d_J=v XOR a_C using the earlier width-two mask clause. Conjoin B and
solve 2-SAT. Its yes/no answer decreases monotonically as rho increases.

The finite candidate margins are the prepared mu-values. Binary search of
these breakpoints, retaining the strict comparison, recovers the largest
achievable margin and a mask, or detects that B itself is inconsistent. One
may instead scan increasing breakpoints and retain a satisfying mask before
the first infeasible threshold. If B remains feasible after every finite
breakpoint, some legal mask has infinite margin. A budget rho below the largest
finite margin is warranted; the supremum is not itself a safe closed budget.

This optimizes resistance to the specified repair cost, not a general utility
or physical edit cost. Arbitrary cardinality/weighted mask constraints can
make selection hard; a general cost cap cannot silently be represented by
2-CNF. The max-flow source inference and 2-SAT mask search are ordinary
algorithms. The candidate delta is their task-relative, reusable margin
interface and an explicit rejection of its overextensions.

## Two different kinds of further assumptions

Conditioning W_rho on a new receipt h keeps the OLD threshold e0+rho. It
does not recompute a new optimum and restore the same slack above that optimum.
For example E(x)=x, e0=0 and rho=0. Observing x=1 conflicts with the retained
source. Reoptimizing under x=1 instead returns x=1 at cost one. That is a new
repair policy/version, not an observational update of the old source.

Even ordinary conditioning invalidates the cheap forced-coordinate cache when
rho>0. Take E(x)=x1+x2+x3, supplied by three negative soft units, and rho=2.
Every original pair projection is full. After receipt x1=1, neither x2 nor x3
is forced, but (x2,x3)=11 is impossible. The target clause NOT x2 OR NOT x3
now holds throughout the source. One needs updated constrained minima or other
additional dependence information. The exact optimum case was easier because
its residual implication source is closed under coordinatewise majority.

This counterexample works for arbitrarily small positive rho by scaling all
three unit fees to rho/2. Therefore no universal positive-slack extension of
the binary cache follows merely from closeness to the optimum. Integrality
can leave a safe interval below the first positive residual-cut value, but
that interval is source-specific.

## Closest comparison

These local quantities are min-marginal energies. Kohli and Torr (CVIU 2008,
Section 2.1, equations 5–6) explicitly define both unary and pair min-marginals;
their graph-cut approach is a particularly strong computational antecedent.
The present task margin uses their conventional object as a projection service
for a universally safe edit. It does not introduce min-marginals or turn them
into calibrated probabilities. No source/runtime gain over their dynamic
implementation has been measured.

The [first finite screen](repair_margin_probe.json) passes on 60 weighted
sources with two through six variables: 1,030 residual identities, 60 exact
optimal-world representations, 2,160 constrained min-marginals, 673 mask
margins and 9,634 threshold-permission comparisons. It also checks the
positive-slack cache counterexample. Runtime is 0.0860004 seconds. These are
synthetic mathematical diagnostics, not independent reconstruction or measured
fee savings; the ordinary min-cut/min-marginal realization is identical.
