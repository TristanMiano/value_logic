# Exact-quota allocation using current disagreement: prospective extension

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
Task: R-P3-B-A; same selected service, DEVELOPMENT.

## Question and intended evidence

The stable first implementation buys uniformly within each block. Can the
current expert state influence which answer is bought without losing the
all-issued decision guarantee or exact quota? Explore a block-adaptive
distribution with an explicit positive probability floor. The public inputs
for the whole block must be available before selection, and all prediction
weights remain frozen until its end. No adaptation after the current block's
purchase history is observed is licensed.

Expected result: a directly reconstructed propensity-corrected bound, a finite
ticket implementation if useful, and a concrete failure when propensities are
ignored. Keep the stable uniform code and its planned batch unchanged. This
is an optional strengthening inside option A, not a new task, P3-08 activity
or a change to its protected Research90 floor. A separate source/proof review
has been assigned. No additional principal time is credited for that review.

## Candidate derivation

Before block k's selector is drawn, choose probabilities pi[k,t]>0 from prior
settled history, the frozen mixture and the full public query block. Require
sum_t pi[k,t]=1 and pi[k,t]>=1/(H+1), for a fixed finite H. Draw exactly one
position J. Define the selected objective estimate

```math
X_{k,i}=(\pi_{k,J}^{-1}-1)\ell_{J,i},\qquad
Z_{k,i}=X_{k,i}/H\in[0,1].
```

Its conditional expectation equals the all-unbought objective:

```math
\mathbb E\left[\sum_{t\ne J}\langle p_k,\ell_t\rangle
                   \mid\mathcal F_{k-1},\pi_k\right]
=\mathbb E[\langle p_k,X_k\rangle\mid\mathcal F_{k-1},\pi_k].
```

Apply product weights to Z, with eta=1/K and K>=max(2,H), and multiply its
potential bound by H. For binary expert losses, the coefficient of each
all-issued expert loss after conditional averaging is

```math
(1-\pi)+\frac{(1-\pi)^2}{KH\pi}\le1.
```

Indeed (1-pi)/pi<=H and K>=H, so the added second-order term is at most pi.
On a fixed exogenous loss table this suggests

```math
\mathbb E L_{\rm terminal}\le L_*+HK\log N
 +\frac{HmK}{2^s-1}+(T-m)2^{-h},
```

where the fixed-state term is omitted for exact weights. Each selected update
must use the actual propensity through

```math
\gamma_J=\frac{\pi_J^{-1}-1}{HK},\qquad
w_i\longleftarrow w_i(1-\gamma_J\ell_{J,i}).
```

The correct probability may depend on the earlier learned state. The finite
conditional calculation does not require it to be constant across blocks.
For fixed per-query costs c_t, the fee term becomes E sum_t pi_t c_t rather
than (1/B)sum_t c_t. The hard bill still reserves one completion per block
plus the actual allocation, buffer, integer and output work.

An exact finite selector is available when B is a power of two: give one
ticket to every position, then give B extra tickets to one position favored
by a source-fixed disagreement/public-cost score. There are 2B tickets,
so exactly log2(2B) bits suffice, pi_min=1/(2B), H=2B-1. This pays for
adaptivity with a larger worst-case regret constant and allocation overhead.
The score is a heuristic, not a theorem that a selected label has maximal
information value. An ordinary implementation receives the identical rule.

## Prospective failure witness

Use B=4, pi=(5/8,1/8,1/8,1/8), repeated label blocks (0,1,1,1), constant
experts 0 and 1, H=K=7 and target m=64. The best full-tape expert loses m.
An unweighted update with factor 1/K sees label zero with probability 5/8
and tends to favor the wrong expert for the mostly-one all-issued tape.
If a_k is its action-zero probability in block k, expected terminal block
loss is 3/8+(9/4)a_k. The number of previously selected zeros is binomial,
so exact O(m^2) rational summation can inspect the proposed finite violation
without enumerating exponentially many selector sequences.

The propensity-aware factors are gamma_zero=3/245 and gamma_one=1/7.
Use real queries from the existing family to realize the two labels if an
executable witness is needed; evaluator-only correctness checks remain separate.
This target and parameters are stated before the new witness is executed.
