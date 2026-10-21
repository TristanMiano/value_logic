# An edge lower bound for cap-three invoice acquisition

Codex (GPT-6), DEVELOPMENT, October20,2026. A different branch from model
reliance. This revisits an open bound with a simpler potential, not a rerun
of the failed s12 higher-face potentials. Exact all-size finite-n optimality
is not asserted.

## Contract and proposed result

Initially n>=3 independent fair Boolean coordinates. Every private episode
queries distinct coordinates at unit fee, stops after at most3 queries, and
reveals only its total integer invoice. Episodes reset private memory on the
same world. The public controller may adapt the next program to past invoices.
The target is exact full parity. Controller, reset and randomness costs are
excluded from this mathematical query-fee result. Earlier work's prefix
construction recovers the entire vector with expected fee

```math
V_n=\frac{7n}{6}+\frac{2}{9}\left(1-(-1/2)^n\right).
```

Candidate lower bound: every zero-error protocol has expected query fee at
least7n/6. Consequently the existing prefix construction is asymptotically
optimal for parity as well as full recovery, within an additive term at most
1/4 for n>=2. It need not be exactly optimal at each finite n. The useful
delta would be an all-size leading-coefficient guarantee; no new empirical
cost percentage or practical invoice-only application follows.

## Graph potential

For a residual set W of worlds, E(W) counts its internal Boolean-cube edges.
Use unnormalized potential P(W)=(7/3)E(W). A monochromatic parity set has
no internal edge, so its potential is0. If one episode partitions W into
invoice classes W_c, the removed edges are precisely those whose endpoints
have different invoices. It suffices to show

```math
\sum_{x\in W} c(x)\;\ge\;\frac73
 \left(E(W)-\sum_c E(W_c)\right).
```

Unlike a potential containing all higher-dimensional faces, this local
inequality appears to hold for every W, reachable or otherwise. It telescopes
over an adaptive public tree because the conditional source is uniform on
each transcript fiber. Initially E(W)=n*2^(n-1), giving7n/6 after division by
2^n. For randomized zero-error protocols, condition on independent random
tapes: the resulting deterministic protocol is correct for all finitely many
worlds almost surely, and the same bound applies before averaging tapes.
Randomness correlated with the hidden world would be extra information and
is outside this argument.

## Cap-three structural proof

An episode may stop without querying, which removes no edges. Otherwise its
first query is coordinate i. Its final query answer never changes the invoice.

1. If both first-answer branches stop, the invoice is constant1.
2. If exactly one first-answer branch stops, the other either stops after
   one further query (invoice2 constant on that half), or uses its second
   answer to decide between invoice2 and3. In the latter informative case
   the invoice depends only on i and the selected second coordinate j.
   Across these two coordinates the crossed-edge graph is the path on four
   vertices with costs1,2,3,1 in path order. Other coordinates give disjoint
   copies. Every induced subset of this path has total vertex cost at least
   (7/3) times its edge count: the full path is tight (7 versus3); a proper
   connected segment has ratio at least3, and isolated vertices only add cost.
   If the continuing half always stops at2 or always continues to3, crossed
   components are single edges of total cost3 or4. The same bound holds.
3. If neither first-answer branch stops, all invoices are2 or3. In each
   world, only i and that branch's second queried coordinate can change the
   invoice when flipped; hence the crossed-edge graph has maximum degree2.
   It is bipartite between cost2 and cost3 vertices. For every induced subset,
   twice its total vertex cost is at least the sum of endpoint costs over
   its edges, which equals5 times its edge count. This gives the stronger
   factor5/2, and therefore7/3.

Case2 includes the possibility that the third query's coordinate depends on
earlier answers; that choice cannot affect the unit invoice3. No-repeat
prevents the second query from being the first coordinate. Repeated queries
would require a separate statement, though some only waste a fee.

## Prospective cheap screen and limits

Enumerate all cap-three invoice functions on three coordinates using the
unchanged s12 enumerator. Check the inequality on every nonempty subset of
the eight worlds. Three coordinates cover both branches' possibly different
second queries; the third queried answer is irrelevant. A failure rejects the
proposed argument and is retained. This finite screen checks implementation
and the structural cases; it is not an independent all-size proof.

General cap H is only a lead. The prefix coefficient suggests factor
2+1/(2^(H-1)-1) per removed edge, but the cap-three path/degree proof does
not establish that extension. Do not import it into a result without an
argument or an informative counterexample.

## Screen outcome and two consequences

[edge_probe.json](edge_probe.json) checks100 distinct cap-three invoice
functions against all255 nonempty three-bit sources:25,500 inequalities,
72 tight cases, no failure; combined runtime0.0287084 seconds. The minimum
fee/removed-edge ratio is exactly7/3. The enumerator's prior source hash is
bound in the output. This supports the local structural proof, not priority.

The same local inequality extends to arbitrary nonnegative world masses p.
Write p(x)=integral over u>=0 of 1[p(x)>=u]. Apply the subset inequality to
each level set and integrate. Every edge then has weight min(p(x),p(y)).
One can retain only edges on which a target Boolean function f differs;
deleting other edges only weakens the lower bound. A zero-error protocol obeys

```math
\mathbb E[\mathrm{fee}]\ge\frac73
 \sum_{\{x,y\}:x\sim y,\ f(x)\ne f(y)}\min(p(x),p(y)).
```

Conditioning on a deterministic transcript just restricts the unnormalized
masses, so the same telescoping argument works. Under the uniform law this
is (7/6) times the average sensitivity of f. For independent biased bits
and full parity it is (7/3) sum_i min(p_i,1-p_i), which need not be tight.
The layer-set argument is an ordinary weighted extension, not a learned law.

If the protocol has total error probability epsilon, a terminal leaf's
remaining f-bichromatic edges each have an incorrectly labeled endpoint.
Their total weight is at most n times the probability mass of incorrect
worlds, since each vertex has at most n neighbors and each edge weight is
at most its incorrect endpoint's mass. Therefore

```math
\mathbb E[\mathrm{fee}]\ge\frac73\left(
 \sum_{\{x,y\}:x\sim y,\ f(x)\ne f(y)}\min(p(x),p(y))
 -n\epsilon\right).
```

Average over random tapes for randomized protocols, with their actual average
error. For uniform parity, epsilon<=1/2, the bound becomes
(1-2epsilon)*7n/6. A controller that runs the exact prefix protocol with
probability1-2epsilon and otherwise makes a fair free guess has error epsilon
on every world and expected fee (1-2epsilon)*V_n. Thus its leading coefficient
is optimal for this average-fee/error tradeoff too. The random-choice tariff
is0 here; if charged, add it to the upper bill, while the lower query bound
still holds. This is not an empirical error claim.

For a possibly unbounded number of episodes, assume termination almost surely.
If expected fee is infinite the lower bound is trivial. Otherwise telescope
at a finite episode cutoff and let the cutoff grow: residual potential is
bounded by7n/6 in the uniform case (by7n/6 also for any probability law,
using sum min masses <=n/2), so its unterminated part vanishes by bounded
convergence. Nontermination with a guessed output needs to be included in
the declared error/termination contract, not silently counted as success.
