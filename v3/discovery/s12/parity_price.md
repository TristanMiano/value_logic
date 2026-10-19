# Exact worst invoice price of parity with private resets

Codex (GPT-6), s12. DEVELOPMENT theorem derivation, not independent review.
Extends [s11 composition](../s11/invoice_composition.md) and resolves the
pathwise-cost obstacle recorded earlier in [search](search.md).

## Contract

There are n>=2 hidden Boolean coordinates on one fixed instance, initially
with unrestricted source. Coordinate i has fixed positive fee c_i. Each
private episode may adapt its queries to answers, buy at most H coordinates
(2<=H<=n), purchase each coordinate at most once in that episode, and stop at
will. Only its exact total invoice is public.
The next episode starts with no private answer memory, although the public
controller may use all previous invoices. Repeated purchases across episodes
are charged. Each nonempty episode also has a fixed overhead f>=0. There is
no additional answer-dependent terminal signal or price.

Recover chi_S exactly on every world, for a specified nonempty S of size k.
Minimize the worst total query bill plus these episode overheads, over all
finite adaptive public/private strategies. Internal planning, checking and
source preparation are outside this particular bill; they are not free in a
complete service comparison. Noise, positive error probability, expected-only
budgets and private state persistence are outside the theorem.

Let b(S)=sum_(i in S)c_i; q=ceil(k/(H-1)). Choose one cheapest coordinate a,
write c_1=c_a, c_2=min_(i!=a)c_i, and c_out=min_(i notin S)c_i (infinity if
none). The exact optimum Phi(S), with Phi(empty)=0, is:

```math
\Phi(S)=b(S)+
\begin{cases}
q(c_1+f), & a\notin S,\\
(q-1)c_1+c_2+qf, & a\in S,\ q\ge2,\\
\min\{c_{out}+f,\ c_1+c_2+2f\}, & a\in S,\ q=1.
\end{cases}
```

For k=1 in the final case, the first alternative always wins because
c_out=c_2. No infeasible two-block construction is needed. The result does
not depend on how ties for cheapest coordinate are broken.

## Constructive upper bound

Partition S into q nonempty blocks of size at most H-1. In each episode,
query its block and buy a marker outside the block iff its parity has one
specified sign. Its invoice reveals the block parity. Multiply signs across
blocks. The worst bill is the sum of block fees, marker fees and overheads;
all costly parity signs can occur together because the blocks are disjoint.

If a is outside S, use it as every marker. If a is inside S and q>=2, put a
and a second-cheapest coordinate in different blocks when the latter is in S.
The block containing a uses that second coordinate as marker; every other
block uses a. Such a partition exists because q>=2 and the total block
capacity is at least k. If the second-cheapest coordinate is outside S, no
special placement is required. This attains the first two cases.

When q=1, either use one block S with its cheapest outside marker, or (for
k>=2) split into two nonempty blocks and use the two-marker construction.
Both blocks still fit the cap. The minimum gives the third case.

## Lower bound: choose a maximum-invoice public path

The earlier tempting assertion "an invoice of k queries has degree k-1" is
false for an arbitrary short stopping outcome. Instead construct one public
path by repeatedly selecting the **largest attainable invoice among worlds
still compatible with that path**. Each selected branch is nonempty.
For a finite exact strategy the path ends with one parity answer. Zero-cost
episodes convey no information and can be removed.

For selected episode j let Gamma_j be that maximum invoice, excluding f.
Build a Boolean predicate R_j on the full cube by simulating its fixed private
query tree as follows. If it stops before reaching Gamma_j, return zero. Before
each next purchase, compare accumulated fee plus that coordinate's fee with
Gamma_j: return one at equality, zero if it would exceed Gamma_j, otherwise
buy the coordinate and continue. Thus every accepting path stops BEFORE the
answer to its final prospective purchase is seen. If Q_j is its already-read
coordinate set and ell_j its prospective last coordinate, then

```math
|Q_j|\le H-1,\quad \ell_j\notin Q_j,\quad
\sum_{i\in Q_j}c_i+c_{\ell_j}=\Gamma_j.
```

On the still-compatible worlds, R_j is exactly the event that this episode's
invoice is Gamma_j. It may behave differently outside that source, which is
harmless. Strict positivity of fees is essential: no compatible execution can
continue spending after reaching its maximum invoice.

Consequently the product P=product_j R_j is a nonzero Boolean indicator of
the constructed final public transcript on the initial source. It is supported
on one sign of chi_S, so its Fourier coefficient at S is nonzero:
E[P*chi_S]=+/-E[P] !=0 under the uniform full cube.

Expand each R_j into its accepting-path cylinder indicators. Each cylinder's
Fourier support consists of subsets of its Q_j. Expanding their product, a
nonzero coefficient at S implies there is a choice of accepting paths and
Fourier terms T_j subset Q_j whose symmetric difference is S. In particular,
their union covers S, and if t is the number of selected episodes,

```math
k\le\sum_j|Q_j|\le t(H-1),\qquad
\sum_j\Gamma_j\ge b(S)+\sum_j c_{\ell_j}.
```

Hence t>=q. If a is outside S, the last sum is at least t*c_1. If a is in S,
some Q_j contains a, and that episode's ell_j differs from a; the sum is at
least (t-1)c_1+c_2. For t=1, every target coordinate lies in Q_1, so the last
coordinate is outside S and the stronger bound b(S)+c_out applies. Adding
t*f and minimizing the t=1 / t>=max(2,q) alternatives gives exactly Phi(S).

The accepting paths chosen in this algebraic expansion need not be the same
private branches realized by the final compatible world. Each has the SAME
selected episode invoice Gamma_j, so the price identity used in the bound
still holds. This is why the argument survives adaptive hidden query order.

Private or public randomization cannot improve a hard worst-bill, zero-error
guarantee: with finitely many worlds, fix a random tape on which correctness,
termination and the stipulated hard bill hold simultaneously for all worlds.
This does not cover bounded-error or expected-cost randomized strategies.

## Consequences

For unit fees, f=0 and the parity of all n bits, this becomes
n+ceil(n/(H-1)), matching the block construction. For fees (1,1,100), target
the first two bits, H=3 and episode overhead f, the exact optimum is
2+min(100+f,2+2f). Thus the earlier 102+f versus 4+2f comparison is optimal
over all allowed adaptive protocols, not only those two displayed procedures.
At f=98 they tie. This remains a constructed query-price comparison.

## Checked affine sources: optimize a character representative

For source F=x_0+V, a target character chi_S is constant if S belongs to
V-perp; it then needs no purchase. Otherwise its exact optimal worst bill is

```math
\min_{T\in S+V^\perp}\Phi(T).
```

Upper bound: query the cheaper representative T and apply the known offset
sign. Lower bound: follow the same maximum-invoice path over F. The product
P has E_F[P*chi_S]=+/-E_F[P] !=0. Expanding P into full-cube characters, at
least one nonzero coefficient has index T in S+V-perp, by character
orthogonality on the affine source. The accepting-path cost argument applies
to that T and gives a bill at least Phi(T), hence at least the displayed
minimum. P only needs to agree with the selected transcript on F.

This reduces arbitrary adaptive invoice strategies to an explicit priced
representative problem for this task and interface. It does not make weighted
coset optimization efficient. A fallible adviser may supply a representative
with a cheaply checked linear-code witness, giving an upper bound; proving
global optimality still requires the minimization or a valid lower certificate.
Source acquisition, arithmetic bit complexity and the actual controller cost
remain separate. Ordinary procedures given the same interface attain the same
optimum. Literature priority and a useful complete-cost application are open.

## Finite developmental screen

[parity_price_probe.py](parity_price_probe.py) enumerates every distinct invoice
function of the permitted private query trees on three bits. A separate Bellman
recursion minimizes worst cost over public adaptive strategies on compatible
world sets. It does not assume parity blocks or affine representatives.

All 14,280 comparisons with the formula passed: 51 nonempty affine sources,
seven nonempty targets, four fee vectors, two episode caps and five reset fees.
The oracle visited 24,360 Bellman states and considered 2,251,480 private-program
choices. Bundled Python 3.12.14 took 0.9202475 seconds for the recorded run.
See [the frozen output](parity_price_probe.json). This is an exhaustive screen
of the stated three-bit panels, not independent confirmation or a performance
comparison against a production controller.

## Boundaries that change the result

1. **A repeat purchase within one episode is a new signaling operation.**
   If permitted, query all of S and conditionally repurchase its cheapest
   coordinate. The final repeated charge reveals parity. In particular, full
   n-bit parity can then be recovered in one episode with n distinct queried
   coordinates and n+1 purchases. The no-repeat hypothesis above is essential;
   a cap on distinct coordinates alone would not suffice.
2. **Expected cost is a different objective.** For two bits with unit fees,
   cap two and no overhead, the hard worst bill is four. In each of two
   single-target episodes, use a public fair random bit to choose which target
   sign triggers the marker. The decoder knows that orientation. Correctness
   is exact, while every world's expected bill is three. More generally this
   construction halves expected marker charges, not base purchases or reset
   fees. No optimal expected-cost formula is claimed.
3. **Full-support readout noise prevents finite zero-error decoding.** With
   independent nondegenerate Gaussian noise on each invoice, every finite
   adaptive observation history has mutually absolutely continuous laws under
   any two worlds. A decision event at a finite stopping time cannot have
   positive probability in one world and zero in an opposite-parity world.
   Thus almost-sure finite, zero-error decoding is impossible in that model.
   This does not preclude bounded-error recovery or population estimation.

## A task-specific use of fallible affine information

The representative construction needs only the particular relation
chi_(S symmetric-difference T)(x)=chi_(S symmetric-difference T)(x_0),
not the truth of every equation defining the proposed affine source. Its
block-query bill bound remains valid on the full cube even when that source
is wrong. If this one relation has a justified failure bound epsilon, the
decoded target has error probability at most epsilon, with the same hard
invoice bill. A checked linear-combination witness establishes the logical
implication from the listed source equations; it does not establish their
empirical reliability.

This gives a concrete reason to evaluate the reliability of a decision-relevant
relation instead of requiring an entire model to be correct. Selecting among
relations after observing the current instance needs a simultaneous or
selection-valid guarantee; separate marginal bounds do not suffice. See
[proof_risk.md](proof_risk.md) for one deliberately conservative shared-risk
certificate. No distributional assumption or free reliability oracle is added.
