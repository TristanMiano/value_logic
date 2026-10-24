# Threshold-aware receipts: width no longer equals fallback frequency

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass61.
This refines the access contract for receipt_sampling.md and threshold_proofs.md;
it does not invalidate their threshold-independent calculations.

Let F in[0,1] be fixed before U~Uniform[0,1]. A truthful interval [L,R]
containing F resolves the comparison when U lies outside it. If the interval
is independent of U, the unresolved probability equals E[R-L], ignoring
zero-probability endpoints. If the model sees U before selecting queries or
receipts, the equality need not hold even though every interval is valid.

For ANY such threshold-aware truthful interval, write w=R-L and let S be
the unresolved event with probability p. On S, w>=|U-F|. Since
P(|U-F|<=x)<=2*x,

    E w >= E[|U-F|*1_S]
         >= integral_0^(p/2) (p-2*x) dx = p^2/4.

Thus p<=min(1,2*sqrt(E w)). If w<=delta surely, the stronger direct bound
p<=min(1,2*delta) holds. For a fresh threshold density bounded by M, the
corresponding bounds are 2*sqrt(M*E w) and 2*M*delta. These concern a fixed
pre-threshold F; choosing F after seeing U is a different contract.

## A narrow average interval can require more full evaluations

Take F=1/2. If U lies in[.4,.6], return
[min(F,U)-.0005,max(F,U)+.0005]; otherwise return[F,F]. The interval is
always truthful, stays in[0,1], and the comparison is unresolved with
probability .2. Its mean width is .0102. A fixed interval[.475,.525]
has width .05 and unresolved probability .05. The threshold-aware method
has 79.6% smaller MEAN width but FOUR TIMES as many unresolved comparisons.

The construction is a counterexample, not an economical algorithm: it
uses F in producing the interval. That suffices to disprove an unrestricted
conversion from average width into paid full-evaluation frequency. Shrinking
the .0005 padding to zero gives p^2/4 as an attainable infimum for the mean
width when the unresolved set is centered at F=1/2. Hence the square-root
bound cannot be uniformly improved using mean width alone.

## Consequence for precision schedules

Suppose a nested hierarchy is queried until resolution. If the cost of
level j is c_j, expected acquisition work is

    c_0 + sum_(j>=1) c_j*P(unresolved after level j-1).

This identity counts actual invocation events and holds regardless of how
the certificates are selected. For threshold-independent intervals with
mean width O(2^(-beta*j)), it gives finite expected work for geometric
cost c_j=O(2^(gamma*j)) when gamma<beta. With ONLY the same mean-width
bound for threshold-aware intervals, the preceding square-root estimate
guarantees finiteness only when gamma<beta/2. This loss is real in the
information contract: centered nested unresolved sets of probability
proportional to 2^(-beta*j/2), with intervals almost spanning F and U,
have mean widths proportional to 2^(-beta*j).

A uniform width bound O(2^(-beta*j)) restores gamma<beta even with
threshold-aware acquisition. At equality or above, these upper bounds do
not guarantee finite work; examples with matching tails give divergence.
Polynomial bit costs with geometric uniform width decay remain summable.

A model may therefore use the threshold to target useful mathematical
queries, but any claimed saving must measure invocation events or use an
appropriate uniform width/tail guarantee. The earlier >23.4% conditional
full-value-call reduction uses a fixed threshold-independent receipt and
retains that premise. None of these calculations is a new audit-fee or
machine-runtime measurement. The argument is an elementary selection
bound; its contribution is the explicit cost-contract repair.
