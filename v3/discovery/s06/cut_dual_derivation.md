# A compact dual certificate for retained checked cuts

Contributor: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-12 UTC. DEVELOPMENT.
This is a proposed additional representation, not a promotion of S28 or a
claim of a new linear-programming duality principle.

## Start from independently admitted logical information

The RUP bridge establishes source-bound inequalities `A z >= k` for every
feasible Boolean violation vector z. Row t is a checked negative bounded
query: `A_t=q_t`, `k_t=b_t+1`. Native IHS status and unverified cores are not
rows of A. A new consumer rechecks each raw encoding/proof and derives the
cut from those checked bytes before using it.

Enumerating all Boolean masks satisfying these rows and deleting dominated
masks supplies a reusable lower envelope. The implemented antichain route is
exponential in the number of soft features and currently capped at sixteen.
That is a representation choice, not an intrinsic requirement to enumerate
logical assignments or to obtain a checked pointwise lower bound.

## Any nonnegative rational multiplier supplies a valid lower function

Choose `lambda >= 0` and put `a=A^T lambda`, `K=k^T lambda`. For a feasible
`0<=z<=1`, the checked cuts give `a.z>=K`. Consequently, for every weight w,

```
w.z >= K - sum_j max(a_j-w_j,0) = L_lambda(w).
```

To see this, write `w.z = a.z + (w-a).z`, and bound each final term below by
`min(w_j-a_j,0)` using the unit box on z. This establishes the bound for any
nonnegative lambda, whether or not an optimization routine found an optimum.
An LP can propose lambda. Round its entries to nonnegative rationals and
recompute `a`, `K`, and the value exactly. The resulting arithmetic receipt
uses only checked cuts and rational operations; it does not trust an LP
optimal-status flag or floating-point dual feasibility. Zero multipliers
remain a valid fallback. For integer queried weights, the ceiling of this
rational lower value is valid because feasible objective costs are integers.

A resident LP model can retain rows and accept objective changes. Its native
state, calls, timings and any new dual proposal are paid separately. A saved
lambda may be reevaluated at another w without another LP solve, provided its
cut dependencies remain admitted. Model or feature changes require a new
source binding.

## A fixed repair gets a linear-size uniform certificate over a box

Let `lo <= w <= hi` be a warranted coordinate enclosure of a common W and let
u be a checked Boolean repair mask. Then

```
u.w - L_lambda(w)
 = u.w - K + sum_j max(a_j-w_j,0)
 <= -K + sum_(j:u_j=1) max(hi_j,a_j)
        + sum_(j:u_j=0) max(0,a_j-lo_j).
```

For a coordinate with u_j=1, its contribution is `max(w_j,a_j)`; with u_j=0,
it is `max(a_j-w_j,0)`. Taking each endpoint gives the displayed bound.
Combine it with `h_W(u)-p` and zero to certify the chosen repair against both
logical optimum and replacement. For replacement, use

```
max(0, p-K+sum_j max(a_j-lo_j,0)).
```

This can be tighter than separately bounding the action by `u.hi` and the
lower function by `L_lambda(lo)`: for violated coordinates the shared cost
appearing on both sides partially cancels. It does not preserve all cross-
coordinate dependence of W. A common-source support calculation or admitted
antichain may be stronger; give conventional controllers the same options.
A failed box certificate is unresolved, not evidence the chosen action is bad.

For fractional mixtures of actions the same coordinate function is convex,
so maximizing each coordinate at its two endpoints is still safe. The output
would concern expected-action regret, and must be requested or explicitly
chosen as that different duty. The implementation here keeps fixed repairs.

## Intended use and limits

This supplies another paid path when Boolean projection is expensive: propose
and retain a rational multiplier, evaluate it cheaply under price, weight or
source updates, and acquire more evidence if its certificate is insufficient.
The LP relaxation may be loose even at the true weights. Nothing here says a
cheap dual always closes a requested tolerance or replaces a checked feasible
repair. Encoding/RUP/cut admission and rational arithmetic remain a small
trusted Python implementation, not a formally verified system.
