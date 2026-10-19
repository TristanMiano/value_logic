# Paid adaptive premise audits

Contributor: **Codex (GPT-6)**. DEVELOPMENT, extending
[premise_audits.md](premise_audits.md). All truth bits remain fixed; probabilities
describe randomized audit selection. This is likelihood-ratio/robust-inference
machinery adapted to proof supports, not a new martingale principle.

## Unequal and adaptive sampling

At step t choose a predictable distribution p_t over premise indices, draw an
index accordingly, and inspect it exactly. Stop this all-pass procedure when
a false premise is seen. For a hypothetical fixed bad set B, let

    q_t(B) = 1 - sum_(i in B) p_t(i).
    M_t(B) = 1{all t audits passed} / product_(s<=t) q_s(B).

On a still-live path with q_t(B)>0, the next multiplier has conditional mean
one if B is the actual bad set. When q_t(B)=0, the next audit must fail under
that hypothesis; kill the process instead of assigning 0/0. Thus M_t(B) is
a nonnegative supermartingale starting at one (a martingale until such killing).
Sampling may avoid previously observed indices and adapt to their identities,
model suggestions and earlier exact observations; the actual draw must follow
its recorded p_t. Random-number generation and selection cost are additional.

At any live time, propose Q and prove that every receipt-compatible bad set B
under which Q is false satisfies M_t(B)>=1/alpha, or has already been ruled
out by an impossible observed transition. Then false release of any such Q
at any time implies the actual bad set's process crossed 1/alpha. Ville's
inequality bounds that event by alpha, without a union over proposed Q.
Uniform sampling without replacement reduces to the hypergeometric rule.

This is computationally expensive in general: there are 2^N possible B, and
the certificate requires separation over the actual logical failure family.
The displayed formula does not make model-dependent audit design free or
permit reusing a marginal calibration number after arbitrary selection.

## Independent inclusion gives an additive support weight

For a simpler fixed design, include premise i independently with probability
q_i in [0,1), and release only when every included premise passes. Let
w_i=-log(1-q_i). For actual bad set B, all-pass probability is
exp(-sum_(i in B)w_i). If every receipt-compatible bad pattern breaking a
selected conclusion has weight at least L=log(1/alpha), the probability of
any false selected conclusion is at most alpha. Actual B is fixed, so the
shared dominating event avoids a multiple-conclusion penalty here too.

The planned expected audit bill, before early termination, is

    sum_i c_i*(1-exp(-w_i)).

Stopping at the first failure can lower the realized expectation; the formula
is exact on an all-true instance or when all selected audits are run. Choosing
weights minimizes a concave increasing objective over a hitting-set cover
region. It is not a convex optimization merely because the risk constraints
are linear in w. Deterministic inclusion q_i=1 is handled separately as an
exact audited premise, with an infinite formal weight only as notation.

## Exact finite-design optimum for a cardinality certificate

Assume equal unit audit prices and require all-pass probability <=alpha for
every bad set of size at least k, where 1<=k<=N. In the independent-inclusion
class, the minimum planned expected bill is

    min_(r=0,...,k-1) (N-r)*(1-alpha^(1/(k-r))).

Construction: ignore r coordinates, sample each remaining coordinate with
probability 1-alpha^(1/(k-r)). Every k-bad pattern includes at least k-r of
the sampled coordinates and so passes with probability at most alpha.

Proof of the reverse bound: sort finite w increasingly. Feasibility is
sum_(i=1)^k w_i>=L. Decrease w_(k+1),...,w_N to w_k and decrease all weights
proportionally if the constraint is slack. Set y_j=w_j-w_(j-1)>=0 for j<=k.
The tight constraint is sum_(j=1)^k (k-j+1)*y_j=L. The objective is concave
in y on this compact simplex; a minimum occurs at a vertex. A vertex has only
y_(r+1)=L/(k-r) nonzero, giving the stated design. If some q_i=1 but at least
k finite weights remain, reducing the infinite weights to w_k improves cost.
If fewer than k finite weights remain, at least N-k+1 coordinates are audited
deterministically, costing at least N-k+1, which is worse than the r=k-1
candidate (N-k+1)*(1-alpha). This covers the boundary designs.

The result is not the optimum over correlated sampling or adaptive policies.
For N=100,k=50,alpha=.01, uniform independent inclusion costs about 8.80
expected audits; seven uniformly sampled distinct audits already suffice.
For k=N, concentrating on one premise at probability 1-alpha costs 1-alpha,
while uniform inclusion wastes work. A logical failure threshold and the
sampling class both affect the useful design. These calculations are derived,
with no numerical optimization or new empirical claim yet.

## Development decision

The common risk event is a useful interface, but existing confidence sequences,
risk-limiting audits and acceptance sampling are the central machinery. A
moderately novel contribution would need a compact proof/permission family
whose separation and audit design are materially useful after all computation
costs. Generic formulas and a threshold example alone do not establish that.

## A stronger ordinary comparison: randomized certificates

Aaronson's [Quantum Certificate Complexity](https://www.scottaaronson.com/papers/qcc.pdf),
Definition 3 and Lemma 5, already defines a randomized verifier relative to a
claimed input and characterizes independent-coordinate inspection up to
constant factors. The claimed all-true premise vector is precisely such a
reference input. Query complexity excludes all other computation. This is a
closer antecedent than treating the construction as a new theory of logical
probability; the adaptive conclusion interface still needs its shared event.

There are exact elementary comparisons beyond independent inspection. For the
cardinality condition with equal prices, symmetrize any all-pass verifier over
coordinate permutations. Its all-true query set is uniform conditional on size
m; risk against k bad bits is h_m=H(N,k,m). Its optimum is the lower envelope
of mixtures over (h_m,m). The sequence h_m is decreasing and convex:

    h_m-h_(m+1) = k*h_m/(N-m),
    (h_(m+1)-h_(m+2))/(h_m-h_(m+1))
        = (N-k-m)/(N-m-1) <= 1.

Use h_m=0 after m=N-k+1 and handle the final denominator separately. Thus
the optimal correlated design mixes the two adjacent sample sizes bracketing
alpha; no independent-inclusion optimum is a global optimum in this setting.
Before finding a discrepancy, every adaptive verifier follows exactly its
all-true path; completeness on that reference input forces acceptance on a
false input whenever its sampled set misses all bad coordinates. This proves
the same lower bound for adaptive verifiers with that reference completeness.

For graph path supports there is an even sharper early rejection. Let premises
mean that specified graph edges are usable, and Q mean s-t connectivity. On
the all-true reference graph, let d be the cheapest s-t path's total audit fee.
Any verifier accepting that reference surely and rejecting every disconnected
graph with probability at least 1-alpha has all-true expected audit fee at
least (1-alpha)*d. Indeed each s-t cut B must be queried with probability at
least 1-alpha; inclusion probabilities r_e therefore satisfy sum_(e in B)r_e
>=1-alpha. By max-flow/min-cut these capacities support that much s-t flow,
whose fee is at least (1-alpha)*d. Expected fee is at least sum c_e*r_e.
Querying every edge of a cheapest path with independent probability 1-alpha,
or checking the whole path with probability 1-alpha, attains the bound.

This concerns verification of an all-true claimed edge vector, allowing
abstention/rejection on other connected graphs, not solving arbitrary
connectivity with small error on every positive input. It rules out a large
audit benefit from mere path redundancy under this contract. The shared
conclusion interface is retained, while graph-audit benchmarking is parked.
