# Whole-vector failure has a different optimal invoice rate from parity error

Codex (GPT-6), DEVELOPMENT, October20,2026. Uses the local charging lemma in
invoice_rate.md and the classical cube edge-isoperimetric inequality. The
random-mask minimax conversion already appears in s12/variable_invoices.md;
it is retained machinery, not new here.

Use the same private-reset exact-invoice contract, n independent fair bits,
2<=H<=n, and expected query-plus-reset fee. Every run returns a complete vector.
Let epsilon be its probability of any wrong coordinate. Write beta=beta(H,f)
from invoice_rate.md and q=max(0,1-epsilon/(1-2^(-n))). The proposed bound is

```math
\mathbb E[\mathrm{fee}]\ \ge\ q\,\beta n.
```

For f=0, exact prefix recovery from rate_scope_check.md yields the matching
upper bound q*[beta*n+1/2-1/(2^H-2)] by mixing exact recovery with a uniform
independent guessed vector. The guess fails with probability1-2^(-n).
Thus, for fixed H and epsilon<1, the optimal leading coefficient for whole-
vector recovery is (1-epsilon)*beta(H,0). This differs from parity's
(1-2epsilon)*beta(H,0). A positive reset fee retains the lower bound, but the
optimal parity prelude can hide individual bits, so no matching full-vector
upper rate is asserted there.

## Terminal edges and wrong-vector mass

Condition on a full independent random tape. Each final transcript has a
fiber W of m equally weighted worlds and one returned vector. At most one
world in that fiber can be correct, so its wrong-world count is at least m-1.
For an induced cube subgraph,

```math
E(W)\le\frac{m\log_2m}{2}
 \le\frac{n\,2^{n-1}}{2^n-1}(m-1).
```

The first inequality follows by induction: splitting on a coordinate gives
edge counts bounded by m0*log2(m0)/2+m1*log2(m1)/2+min(m0,m1). Concavity of
binary entropy gives H2(p)>=2min(p,1-p), proving the inductive step. The second
uses that m*log(m)/(m-1) increases for m>=2; its derivative has the sign of
m-1-log(m). For m=0 or1 there are no internal edges.

Consequently expected terminal edge mass is at most
[n*2^(n-1)/(2^n-1)]*epsilon, whereas initial edge mass is n/2. The local
invoice charging lemma prices each removed edge at2beta in expectation.
Telescoping gives the displayed lower bound, truncated below by zero.
As before, use bounded convergence for residual edge potential when protocols
terminate almost surely; random tapes are independent of the hidden world.

## Distinguish the loss functions

For expected Hamming loss d, charge an internal cube edge in dimension i to
an endpoint whose returned coordinate i is wrong. This bounds terminal edge
mass by d and gives fee>=beta*(n-2d). It is a different error contract from
probability of any vector error. At f0, learning a chosen fraction of bits and
guessing the rest attains the Hamming leading coefficient, with ordinary
rounding and terminal overhead. All-or-nothing randomization attains the
whole-vector probability bound's leading coefficient.

The guarantees are average losses under the stipulated source. They are not
conditional accuracy guarantees for a selected subset of apparently successful
runs. If public fair masking and its processing are free, the earlier ordinary
symmetrization converts the expected-price constructions to every fixed input
with the same error probabilities. Nonzero random-generation or controller
prices require a new bill; the result concerns acquisition fees only.

The later partial_probe.py screen checks this inequality on360 generated
adaptive public protocols as well as the stronger intermediate edge bound.
This is a finite same-model check; see partial_information.md for its scope.
