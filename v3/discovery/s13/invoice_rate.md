# General caps and reset fees: a candidate optimal acquisition rate

Codex (GPT-6), DEVELOPMENT, October20,2026. This strengthens the cap-three
edge argument in [invoice_edges.md](invoice_edges.md). It is not a frozen
claim or independent confirmation. Ordinary implementations tie.

## Contract and result to reconstruct

The same n independent fair bits are reused across private-reset episodes.
Each episode reveals only its exact count of unit-price coordinate queries,
has cap2<=H<=n, and incurs a nonnegative reset fee f in addition to queries.
The controller must recover full parity. Other controller/preparation/random
costs are excluded. Define d=H-1-r for r=0,...,H-2 and

```math
A_r=\frac r2+1-2^{-d},\qquad
B_r=r+2-2^{-d},\qquad
\beta(H,f)=\min_{0\le r\le H-2}\frac{B_r+f}{2A_r}.
```

Candidate theorem: every zero-error adaptive invoice protocol has expected
query-plus-reset fee at least beta(H,f)*n. A concrete parity-prefix protocol
achieves this plus a bounded term independent of n for fixed H,f. Thus beta
is the optimal asymptotic rate. When f=0 the minimizer is r=0 and the rate is
1+1/(2^H-2), matching the existing prefix construction at every fixed cap.

## From private query trees to a local charging recurrence

Fix any subset W of worlds and deterministic episode tree of depth at most H.
Every cube edge whose endpoints produce different invoices follows a common
private path until its differing coordinate is queried. Charge the edge to
that unique first-divergence query node. At node v let N_v0,N_v1 be the
numbers of W worlds in its two branches. Charged edges form a matching across
that split, so at most min(N_v0,N_v1) are charged there. If both children stop
immediately, their invoices are equal; no edge is charged to that node.

Let S be the sum of these min counts over nodes with at least one continuing
child, even if some of these allowed pairs do not actually have different
invoices. Then removed edges E_cross<=S. Total private query fee C is the
sum of N_v over all query nodes. The distinction between S and actual edges
is essential; we use an upper bound here and separately construct an attainer.

For 0<=rho<=1/2, let D_h(rho) be the maximum of S-rho*C per unit root mass
over the abstract mass-splitting relaxation for an *active* query tree with
at most h queries on a path. A stopped child contributes0. Then

```math
D_1=-\rho,\qquad
D_h=\frac12-\rho+\max\{D_{h-1}/2,D_{h-1}\}\quad(h\ge2).
```

Explanation: the root costs rho. Both stopped children contribute0. If one
child continues with mass u, the other stops, and the maximum contribution
is max_u[min(u,1-u)+u*D_(h-1)]. If both continue it is1/2+D_(h-1), attained
by equal mass. For D_(h-1) in[-1,0], the one-child maximum is
(1+D_(h-1))/2 and dominates the both-child value. For nonnegative D_(h-1),
the both-child value dominates, including the unbalanced one-child endpoint.
The recurrence always has D_h>=-rho>=-1/2, so these cases exhaust it and
also dominate the both-stopped alternative. Equal splits attain the stated
relaxation values.

The sequence D_h is nondecreasing in h for rho<=1/2. Therefore an optimizing
shape has a chain of one-continuing-child levels at the bottom, followed by
zero or more both-continuing-child levels above. Unrolling yields

```math
D_H(\rho)=\max_{0\le r\le H-2}(A_r-\rho B_r).
```

Conversely each r is one such allowed shape, so this is equality for the
relaxation, not merely a chosen subfamily. Set
rho_star=max_r A_r/(B_r+f), which lies in(0,1/2). Then
D_H(rho_star)=rho_star*f. For every W and every private program,

```math
E_{\rm cross}\le S\le\rho_*\bigl(C+f|W|\bigr).
```

Zero-query episodes convey no information and obey the same inequality.
Telescoping potential E(W)/rho_star through the public transcript tree gives
expected total fee >=n/(2rho_star)=beta*n for parity. The arbitrary-law,
other-Boolean-target and bounded-error arguments from invoice_edges.md apply
with7/3 replaced by1/rho_star. In particular uniform parity error epsilon
gives lower bound(1-2epsilon)*beta*n. Almost-sure termination and finite-fee
limits are handled as in that note; random tapes must be independent of x.

## A matching parity-prefix construction

For a selected r,d, first query r fresh bits privately and compute their
parity. Query d more fresh bits in order. For the first of these, use its XOR
with the prelude parity as the stopping bit. Later stopping bits are their
actual coordinate values. Stop at the first0. If all d stopping bits are1,
query one distinct marker coordinate and stop; its answer is discarded.

An invoice r+j, j<=d, reveals the parity of all r+j processed fresh bits:
the prelude combined with the first prefix bit, followed by j-1 further bits.
The all-ones marker invoice r+d+1 reveals the parity of r+d processed bits.
Remove those bits from the unresolved target and keep their known aggregate
parity. The remaining fresh bits are still independent fair bits. This need
not recover individual prelude bits, unlike the original prefix construction.

The mean number of resolved target bits is
2A_r=r+2-2^(1-d); the mean query fee is B_r=r+2-2^(-d). Its mean total bill
is B_r+f. The program uses at most r+d+1=H distinct queries; a marker exists
because H<=n and may be a previously processed coordinate. Computing the
prelude parity is controller/private arithmetic and must be charged in a
complete-cost application; it is not part of this query-fee theorem.

Repeat a minimizing r,d while at least m=H-1 fresh bits remain. Below that
threshold, use one-bit cap-two episodes, of expected query-plus-reset fee
1.5+f per bit. Let V_k be this policy's expected remaining bill. For k>=m,
subtract beta*k from its exact recurrence: the remainder is a convex
combination of remainders at smaller k, because mean bill=beta*mean progress.
At k<m the remainder is (1.5+f-beta)*k, nonnegative. Hence

```math
\beta n\le V_n\le\beta n+
(H-2)\bigl(3/2+f-\beta\bigr).
```

This proves the matching asymptotic rate if the local derivation survives
reconstruction. Finite-n optimality is still open; a dynamic selector over
shortened prelude/prefix programs can improve the bounded remainder without
becoming an unrestricted Bellman oracle.

## Concrete new regime and prospective checks

At H=4 the candidate envelope chooses:

- r=0,d=3 for0<=f<=1/6 (ordinary prefix);
- r=1,d=2 for1/6<=f<=1 (parity prelude plus two-bit prefix);
- r=2,d=1 forf>=1 (ordinary three-bit parity block).

At f=1/2 these rates are respectively19/14,13/10,4/3. The middle construction
has rate1.3 versus the stronger endpoint rate4/3:2.5% lower asymptotic declared
query-plus-reset fee. This compares actual stated algorithms at the same
interface, not all ordinary methods; the ordinary implementation of the new
construction ties. No wall-time or complete-computation percentage follows.

[edge_extension.json](edge_extension.json) found no counterexample to the
zero-reset higher-cap edge inequality in500 generated trees (caps4,5,6;
at most8 coordinates), after25 small max-closure checks against enumeration.
That finite screen predates this general proof and does not test reset fees
or establish the theorem. Next cheap checks: exact rational recurrence versus
the max-envelope formula; direct execution of parity-prefix decoding; small
finite selector versus prior prefix/fixed controls, with all fees explicit.

## First development check and finite comparison

[rate_probe.json](rate_probe.json) passes152 exact rational rate identities,
9796 small-world complete decodings over45,588 episodes, and95 exact mean
comparisons. Its finite dynamic selector allows every r,d with r+d<=H-1,
shortening near the end. The stronger previous control adaptively chooses
from all pure prefixes (r=0) and parity blocks (d=1), rather than one fixed
partition. Both controls receive the same uniform source and reset tariff.

At n=100,H=4,f=1/2 the full menu costs130.265 in expected query-plus-reset
fees, versus133.42857142861024 for that prior adaptive menu: **2.370985% lower**.
The all-program lower bound is130, so this constructed policy is within0.265
fee units of it. The new selector considers592 menu options versus494 for
the prior selector: its named preparation work increases. No separately timed
arm or complete-cost improvement is claimed. The combined probe takes
0.477617 seconds, not a per-arm comparison.

An explicit extra tariff gamma per private prelude XOR charges r*gamma per
episode. This is a restricted bill model, not a complete CPU accounting or a
new all-program lower-bound theorem. At gamma=1/10 the finite advantage is
1.233766%; at gamma=1/5 it disappears and the selector uses the old menu.
At gamma=1/7 a tiny finite remainder advantage persists despite equality of
leading rates. Thus the query/reset result must not be promoted into a free
computation claim. Public bookkeeping, source justification and preparation
also need prices in any application.
