# F16 addendum: exact normalized Choquet embedding

**Signed:** ChatGPT (GPT-6 Astra Pro), separate delegated contribution reviewer.
**Date:** October 5, 2026 UTC.
**Scope:** proof-only check requested by the principal; no new retrieval,
experiment, or edit to existing derivations. A nested reviewer separately
checked the dummy/tie case and agreed. Concurrent principal-clock credit:
**zero**.

## Disposition

**The proposed bridge is exact, including `M=0` and its zero-score tie.**
An always-successful zero-score dummy embeds the original nonnormalized
coverage capacity in a normalized coverage capacity without changing any
Choquet evaluation in the stated query family. This removes normalization
as an expressiveness obstacle. It does not itself evaluate the special
observation-matrix kernel, recovery radius, or their literature priority.

## 1. Cost identity

Let `S_j={pi_1,...,pi_j}`, `m_S=P(all procedures in S fail)`, and
`rho(S)=1-m_S`. Set

`x_pi_j = M + sum_(l=j+1..k) c_pi_l`,
`x_pi_(k+1) = 0` (a virtual endpoint).

For `c_i>0` and `M>=0`, the original scores are nonnegative and strictly
decrease along `pi`. Their successive differences are `c_pi_(j+1)` for
`j<k`, while the final difference is `M`. Thus

`Choquet_rho(x)`
`  = sum_(j=1..k-1) c_pi_(j+1) (1-m_S_j) + M(1-m_[k])`.

Subtracting this expression from `sum_i c_i + M` gives

`c_pi_1 + sum_(j=1..k-1) c_pi_(j+1) m_S_j + M m_[k]`,

which is exactly the expected reset cost: the first attempt is always paid,
each later attempt is paid when its predecessors fail, and the terminal
penalty is paid when all original procedures fail.

A second pathwise check makes the same identity transparent. In a world
whose first successful procedure is `pi_t`, the largest score among its
successful procedures is `x_pi_t`; subtracting it from `sum_i c_i+M` leaves
`sum_(l=1..t)c_pi_l`. If no procedure succeeds, use maximum zero, leaving
the complete cost plus terminal penalty. Taking expectation gives the same
formula.

## 2. Normalized dummy and the tie

Add an element `d` with `x_d=0`, and define for every augmented subset `A`

`rho'(A)=rho(A)` if `d not in A`, and `rho'(A)=1` otherwise.

If `R` is the random set of successful original procedures, put
`R'=R union {d}`. Then

`rho'(A)=P(R' intersects A)`.

Consequently `rho'` is a monotone coverage capacity, with empty-set value
zero and full augmented-set value one. This proves the proposed definition
is probabilistically coherent, including when the original `rho([k])<1`.

When `M>0`, append `d` after all original coordinates in descending order.
All old prefix terms are unchanged; the added dummy's increment is zero.
When `M=0`, both `pi_k` and `d` have score zero. They may appear in either
order. Prefixes preceding that zero block are identical, and all increments
inside or after it are zero, so the value is independent of the tie order.
Equivalently, every strictly positive threshold set excludes `d`; the
nonnegative Choquet layer-cake integrals therefore coincide.

At `M=0`, normalization does **not** make the original full-failure moment
observable: `rho([k])` still has a zero coefficient. The full augmented
capacity is fixed at one but also receives zero score increment.

## 3. What the embedding does and does not import

The augmented model is a **constrained normalized-capacity family**. All
capacities of sets containing `d` equal one; the augmented outcome law has
deterministic dummy success and therefore lies on a face of the augmented
simplex. The original coverage/joint-probability constraints remain necessary.
Replacing this family by every normalized monotone capacity would enlarge
the feasible set and can change ranks and sharp recovery bounds.
The dummy is a zero-score representation device: the observations remain
the original `k!` price-generated score vectors with an appended zero, not
all queries of a new `(k+1)`-procedure reset problem.

There are no additional free source parameters. The old law maps into this
family injectively, and original moments are recovered as `m_S=1-rho'(S)`
for subsets excluding `d`. Relative-interior arguments must be made in that
constrained family, not in the full augmented simplex.

Hence established normalized Choquet evaluation and design-matrix machinery
can represent the application exactly, with its constraints and restricted
score queries made explicit. Nonnormalization alone is not a substantive
novelty claim. The remaining comparison target is still the evaluated
price-generated matrix, explicit repair construction and specialized
approximation consequences; this embedding does not settle their priority.
