# Reference-relative sparse feedback

Codex (GPT-6), DEVELOPMENT. Connects [potential-relative values](potential.md)
to [local counterfactual information](banded_feedback.md). All values and fees
remain fixed within a request; Stop is monotone in true receipts and
order-independent. This is a candidate algorithmic adaptation, not a priority
claim or an empirical complete-cost result.

## Only a short band of reduced edge losses is needed

Suppose the reference stops after L0 receipts. Set a=max(0,L0-d) and let C0 be
its query bill (the common fallback, if any, cancels separately). For acquired
set S, define Phi(S)=sum_{i in S} c_i when |S|<=a and Phi(S)=C0 otherwise.
An edge from S to S+j has the reduced loss

```math
\widetilde\ell(S,j)=c_j\mathbf1\{\neg\mathrm{Stop}(S)\}
                    -\Phi(S\cup\{j\})+\Phi(S).
```

Telescoping gives total C_sigma-C0 on every full permutation path. Before
layer a no candidate can have stopped, so each edge loss is exactly its fee
and the potential cancels it. At and after layer L0+d every candidate has
stopped and Phi is constant, so reduced loss is zero. Thus only the at-most
2d layers a,...,L0+d-1 need updates, independent of n. At layer a, S is a
subset of the reference prefix (if a>0); the negative potential jump accounts
for the missing reference fees. Signed edge losses are intended.

If there is no full-set certificate, every policy buys all values and has
the same fallback and total bill: the whole difference vector is zero.
Stop(empty) likewise gives zero. Do not treat sparse updates as free planning:
maintaining weighted path sums after edge changes still costs work.

This adapts ordinary potential shaping to the counterfactual cost interface.
The representation can now update O(d^2*4^d) edges per audited request rather
than every O(n*d*4^d) edge. Those are loose frontier bounds. A matrix-product
data structure could update aggregate path weights in logarithmic n time for
fixed d; the matrix dimension and arithmetic costs must also be included.

## Exact specialization to disjoint adjacent swaps

For d=1, every allowed permutation is a matching M of the path with n vertices:
an edge j swaps neighboring reference positions j,j+1. Its cost obeys

```math
C_M=C_0+\sum_{j\in M}\delta_j,\qquad
\delta_j=C_{\{j\}}-C_0.
```

Proof: partition the reference into swapped pairs and unswapped singletons.
Every block has the same acquired set after completion in either order. The
first block with a certificate is invariant under its internal order; earlier
blocks pay their full fees and later blocks pay zero. Summing the individual
pair differences therefore reproduces the matching difference exactly.

With one-based L0, only j=L0-1 and j=L0 can have nonzero delta. Earlier pairs
are contained in the non-stopping prefix, so neither ordering can stop there;
later pairs start after the reference certificate. The adjacent identity gives

```math
\delta_j=c_{j+1}\mathrm{Stop}(R_j\cup\{j\})
          -c_j\mathrm{Stop}(R_j\cup\{j+1\}),
```

where R_j is the reference prefix strictly before j, and the indicators are
interpreted only for pairs before the reference has already stopped. For a
pair after stopping, delta is zero. The last observed pair and the next value
are enough when the reference executes; an arbitrary matching's execution can
require two additional values, as the preceding lower construction establishes.

## Ordinary weighted-matching data structure

Exponential weights on matchings with cumulative estimated local deltas has
weight proportional to product_{j in M} w_j, w_j=exp(-eta*sum delta_hat_j).
For suffix partition functions, Z_i=Z_{i+1}+w_i*Z_{i+2}, with appropriate
terminal values. This is an ordinary weighted matching recurrence. Write each
step as a 2-by-2 transfer matrix [[1,w_i],[1,0]]. A balanced product tree
supports point updates and suffix partition queries in O(log n) matrix
products. There are at most two point updates per informative request.

At the next unused identity i, sample a swap with conditional probability
w_i*Z_{i+2}/Z_i; otherwise leave i alone. After a swap advance two identities.
Generate only as much of the permutation as execution needs. This lazy
sampling has the same prefix distribution as a complete permutation sampled
before observing current values. The data structure does not inspect hidden
values. Log-domain arithmetic prevents ordinary overflow, but is numerical
advice; finite implementation checking is still needed.

Expected computation per executed prefix is O(L*log n), with O(log n) work
per sparse update and O(n) retained tree size. A naive full-family updater is
exponential, but the relevant ordinary control is this same matching dynamic
program or an existing path learner, not only enumeration. The prospective
gain is the justified sparse feedback/update interface under a paid query
model; standard matrix products and exponential weights are imported machinery.

Next cheap step: independently enumerate small matching families, verify the
sparse delta decomposition and transfer products, then implement a modest
priced simulation including no-extra-query learning controls. This remains
discovery and should not displace broader candidate generation for the rest
of the recurrence.

Executed [mf01](mf01/attempts.jsonl): four n=5,7,8,9 binary panels passed on
their first attempts. The [screen](matching_probe.py) checks 156,544 exact
matching cost decompositions, 80 numerical partition functions and 500
conditional swap probabilities against enumeration. The largest small family
has 55 policies. The separate scaling construction reaches n=4096, where two
point updates perform 24 log-domain 2-by-2 matrix products after 4095 setup
products; a fresh scalar suffix recurrence has 4095 steps. A matrix product
is more expensive than one scalar recurrence step: these different operation
counts are not a 99% runtime or complete-cost claim. Sampling and predicate
costs remain to be measured in a service comparison. Executed core and screen
hashes are in each output; preserve their bytes.
