# A candidate regret certificate for fallible query/flip controllers

Codex (GPT-6), DEVELOPMENT derivation. Extends the
[compact paid controller](probe_control.md) toward useful reliance on fallible
models. New guarantee proposed here; novelty and computational checks pending.

## Exact uncertainty contract

The masses p_z of the r query-sign cells are known and fixed. For each unqueried
coordinate i, its conditional mean in cell z is only known to lie in
[l_zi,u_zi] within [-1,1]. These intervals are independent constraints across
cells and coordinates; arbitrary within-cell joint dependence is allowed.
Every such mean table is realizable, for example by conditional independent
signs. Interval validity must come from an actual source or justified statistical
event; agreement of fallible models alone does not provide it.

Fix a proposed admissible controller pi, with at most H paid operations. It
may have been generated from a fallible point model. After the earlier
postponement reduction, a full cell z determines its total acquisition/flip
fee C_pi(z) and its terminal coefficients s_pi,i(z) in {-1,0,1}. The zero vector
means terminal action 0; otherwise each sign records a chosen flip. These
coefficients and fees are computable by following pi on the r known signs.

The target is worst-case regret to the best admissible query/flip policy under
the SAME true mean table, same fees and same operation cap:

```math
R(\pi)=\max_{\mu\in[l,u]}\max_\rho
       \{V_\pi(\mu)-V_\rho(\mu)\}.
```

The comparator may know the true table for this retrospective benchmark.
This is a stronger regret reference, not a claim that a learner and an oracle
have equal acquisition information. The two maxima commute. The issue is
whether their joint optimization can avoid enumerating all source corners
and all contingent policies.

## Leaf calculation

At a comparator history h, let Z_h be its compatible full query cells and
P_h their total mass. Define C_h=sum_z p_z C_pi(z). For an unqueried coordinate,

```math
W_i(s;h)=\sum_{z\in Z_h}p_z
   \max_{\mu\in[l_{zi},u_{zi}]}w_i(s_{\pi,i}(z)-s)\mu,
\qquad s\in\{-1,0,1\}.
```

For a coordinate among the r queryable signs, use its exact cell value z_i
instead of maximizing over an interval. The endpoint maximizing a signed
linear term is explicit. If rho stops with action 0, its worst regret is
C_h+sum_i W_i(0;h). If it stops with action 1, start from
C_h+sum_i W_i(1;h). Flipping i changes that objective by

```math
\Delta_i=W_i(-1;h)-W_i(1;h)-f_i P_h.
```

With k operations left, add the k largest positive Delta_i. Thus the maximizing
comparator's terminal flip choice is again a sorted list, although its scores
are now robust regret contributions rather than predicted loss savings.

## Query recursion and why the source is still common

Let B(h,k) be the maximum of these two terminal values and, for each unqueried
query coordinate j when k>0,

```math
-a_j P_h+B(h,j=-1,k-1)+B(h,j=1,k-1).
```

This is a MAXIMUM recursion: it seeks the comparator that makes pi's regret
largest. C_pi and its terminal contributions are charged at leaves, so each
full cell contributes exactly once. The comparator's query fees are subtracted
on the path. Different outcome branches use disjoint cell parameters. Therefore
their maximizing interval endpoints can be combined into one common admissible
mean table. Within a leaf, every chosen coordinate endpoint can also coexist
because the source constraints impose no additional coupling.

Induction then proposes **B(empty,H)=R(pi)**, with an attaining comparator and
an attaining single mean table recoverable by recording maximizing choices.
The proof uses box separability and mutually exclusive query cells, not an
assumption that actual unknown signs are independent. A generic common-source
minimax regret problem need not have this decomposition.

## Useful delta and limits

This would let a bounded reasoner certify how badly a fixed model-guided
computation/revision policy could perform before trusting it, even when most
joint probabilities remain unidentified. It uses a small conditional-value
source and at most 3^r(H+1) comparator states, with explicit moment summation
and sorting costs. It does not solve optimal minimax-regret policy design:
minimizing this certificate over a large proposal family remains a separate
search. Finite candidate selection can use the certificate without asserting
global optimality.

Known fixed cell masses, hidden-outcome-independent prices, the allowed flip
semantics and the conditional-mean box are load-bearing. Unknown masses, global
constraints coupling cells, informative invoices, or changed sensor semantics
require a different derivation. A policy selected from data needs simultaneous
interval coverage. No independence of adaptively selected calibration samples
is inferred from the interval notation.

Next screen: exact small corner enumeration using the original unrestricted
planner as comparator; reconstruct an attaining mean table and policy. Test
zero-width intervals, asymmetric boxes, and a deliberately coupled source to
demonstrate the boundary. Compare robust POMDP and interval-data regret methods
before calling this a new theorem rather than a useful specialization.

## Constructive proof and first screen

The postponement lemma reduces every competing policy to queries followed by
one terminal choice and a subset of flips. Repeated queries have no new
information; positive fees and operation accounting permit deleting them.
For a fixed terminal leaf, the regret expression is affine separately in every
conditional mean. Maximizing over the box gives the displayed W terms, and a
flip changes exactly one term plus its known fee. A cardinality limit therefore
selects the largest positive changes. At a query node, its two outcome sets
partition the full cells. Their choices of means have disjoint coordinates,
so the independently attaining endpoints define one common table. Induction
over the remaining query/flip budget proves the recursion's upper bound and
attainment simultaneously. The attaining mean table is realizable by a sign
law with the prescribed cell masses. This proves the proposed equality under
the stated contract; it is a same-model DEVELOPMENT proof, not confirmation.

The first immutable implementation is `robust_flip.py`, SHA256
`7a7041f3097496971945893ad9bc7d8a4979541d8bf1fce9228f6d877222bab9`.
Outputs in `rf01` passed all nine cases on their first attempts. Eight small
cases enumerate 353 corners in total; 48 also compare to unrestricted
interleaved query/flip planning. All nine reconstruct an attaining source and
check that interval refinement cannot increase regret of the unchanged policy.
Five cases satisfy the ordinary induced-scenario shortcut and tie it exactly.
The 101-coordinate, four-query case visits 81 contexts, with 77,568 counted
support terms and 8,181 sorted flip keys. Its all-zero proposal has regret
6713/96; halving each interval toward its nominal mean reduces this to 3049/72.
These are certificate values for a deliberately weak proposal, not performance
gains of a deployed reasoner. The large full-source corner problem was not run.

### Strong conventional shortcut

If pi selects terminal action 1 in every cell, each coefficient is extremal:
s_pi,i(z) is -1 or +1. For any comparator coefficient in {-1,0,1}, the sign
of w_i(s_pi,i(z)-s_rho,i(z)) is fixed or zero. Thus set each uncertain mean to
its upper endpoint when w_i s_pi,i(z)>0 and to its lower endpoint otherwise.
This one induced source maximizes every pairwise regret simultaneously.
Evaluate pi there and subtract an ordinary optimum. This is the signed version
of the established induced-scenario argument for binary interval optimization.
Do not claim that the new recursion is necessary or faster in these cases.

When pi selects terminal action 0, its coefficients are interior, so the sign
can depend on the competing policy. The direct shortcut no longer follows.
Our recursion handles this through support values for each competing terminal
choice. It remains a specialization of conventional support-function and
dynamic-programming machinery; a useful synthesis needs this restricted
capability and its cost made explicit, not a claim to a new regret criterion.

### Sharpness boundary

Take two unqueryable signs, equal weights, no operations and proposed terminal
action 0. If both means lie in [-1,1], the box certificate is 2, attained by
means (-1,-1) and competing terminal action 1. Add the justified coupling
mu_1+mu_2=0: both terminal costs are now zero, so actual regret is zero.
Ignoring the coupling still gives a valid upper bound, but the claimed witness
is infeasible and the bound is not sharp. Common-source validity is not the
same as box separability. Unknown cell masses also cannot be optimized
independently, since their sum must remain one.

### A cheaper implementation route

The first implementation scans compatible cells for each context. Over all
partial histories this takes O(m 4^r) scalar support work: each full cell is
compatible with 2^r histories. Instead precompute the three per-coordinate
support vectors in every full cell and aggregate them recursively along a
fixed missing coordinate. Each partial-history vector is the sum of its two
children. Memoization gives O(m 3^r) arithmetic after O(m 2^r) endpoint work.
Sorting flip gains costs O(m log(m)) per history; selection can reduce this
if only the summed top k is needed. Starting at budget H, a history with j
queries always has H-j remaining, so the present policy recursion needs one
budget per history, not H+1 copies. These are mathematical operation bounds;
exact rational bit complexity and source acquisition remain separate.
