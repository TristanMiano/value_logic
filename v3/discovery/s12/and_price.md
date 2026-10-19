# Exact price of a conjunction through private computation invoices

Codex (GPT-6), s12 DEVELOPMENT derivation. Same no-repeat private-episode,
positive-coordinate-price and exact-invoice contract as [parity_price.md](parity_price.md).
Source is the full Boolean cube. Query cap 2<=H<=n; each nonempty episode
costs additional f>=0. All conditions are fixed literals on a target set S.
Their signs do not affect the formula. Target is their conjunction; negating
the output gives the corresponding disjunction result.

Write k=|S|, b=sum_(i in S)c_i, q=ceil(k/(H-1)), c_1=min_i c_i,
and c_out=min_(i notin S)c_i. Empty conjunction costs zero. A singleton costs
c_i+c_out+f. For k>=2 the proposed exact optimum is

```math
\Psi(S)=b+
\begin{cases}
c_1+qf,&q\ge2,\\
\min\{c_{out}+f,\ c_1+2f\},&q=1.
\end{cases}
```

## Upper construction: make failed blocks cost the marker

Partition S into q blocks of size at most H-1. Query the whole current block;
if its conjunction is false, purchase a marker outside it. Its two distinct
invoices identify success/failure. The public controller stops at the first
failed block and accepts only when all blocks pass.

For q>=2, arrange the last block to exclude a cheapest coordinate a. If a is
in S, place it in an earlier block and use a cheapest other coordinate as that
block's marker. Every other block uses a. A nonempty last block contains a
coordinate whose price is at least that second-cheapest fee. Therefore an
earlier failure in the block containing a costs no more than the final-failure
bound b+c_1+qf. All other earlier failures also cost no more. A failure in the
last block with all previous blocks passing attains the bound; all-pass cost
is b+qf.

For q=1, either use an outside marker in one episode or split into two
nonempty blocks and apply the preceding construction. A singleton cannot use
the split construction. Its only information-carrying marker must be another
coordinate. This is why that case is stated separately.

## Lower bound

On any all-satisfied input the protocol must purchase every target coordinate:
otherwise flipping an unqueried target literal leaves the entire execution
unchanged and changes the required result. Its transcript is nonempty and
supported on the all-satisfied target subcube. Any nonzero transcript
indicator supported there has a nonzero Fourier coefficient at S, since
chi_S has one fixed sign on that support. Each episode's invoice-event
indicator has degree at most H-1 under the stated no-repeat contract, so the
all-satisfied transcript uses at least q episodes. This imports the established
s11 invoice-degree lemma; it does not infer degree from the realized bill.

If that execution purchases any coordinate beyond the mandatory one purchase
of each target, its bill is at least b+c_1+qf. Otherwise its query bill is
exactly b. Flip the target coordinate purchased last. The alternate execution
has the identical history up to and including that purchase. The invoice
cannot reveal its answer without an additional purchase in that episode or a
later episode: with no later purchase, all public invoices remain identical.
Correctness therefore forces at least one further charge on the flipped
world, after the full b has already been paid. It has at least the original
q episodes. This proves b+c_1+qf whenever q>=2.

For q=1, divide strategies by their all-satisfied transcript. If it uses at
least two episodes, the same argument gives b+c_1+2f, possibly on the flipped
world. If it uses one episode, either it already buys a coordinate outside S,
or its last-target flip must make such a purchase: repeats in an episode are
forbidden and all target coordinates were already read. This gives
b+c_out+f, possibly on the flipped world. Taking the smaller alternative
matches the construction.

For a singleton, any sequence purchasing only that coordinate has constant
invoices, one fixed fee per nonempty episode. Some distinguishing execution
must therefore purchase both it and another coordinate. This gives the
separate singleton lower bound. Randomization under hard worst cost and zero
error is removed by the same finite-world random-tape argument as for parity.

## Consequence and scope

For unit fees, target all n bits, and f=0, conjunction costs exactly n+1 for
every H>=2, while parity costs n+ceil(n/(H-1)). The target functions have the
same ordinary worst-case bit-query complexity n. The invoice-only/reset
interface distinguishes them because a conjunction can stop after the first
reported failure, whereas every parity block must be combined.

With unit fees and overhead f, conjunction costs n+1+qf and parity n+q+qf.
This is a constructed mathematical distinction, not an empirical saving or
a claim that ordinary short-circuit evaluation is new. It identifies which
decision structure can avoid repeated marker charges under the chosen
interface. General Boolean targets, affine-source conjunctions, noisy readout,
expected-only costs and complete controller prices remain outside this formula.

## Finite screen

The separate [and_price_probe.py](and_price_probe.py) reuses the frozen private
program enumerator and implements an arbitrary-truth-table public Bellman
oracle. All 1,040 comparisons passed on three-bit full sources, every nonempty
target and assignment of its literal signs, four price vectors, two caps and
five reset fees. The run visited 57,760 Bellman states and considered
5,892,400 program choices in 2.2601667 seconds on bundled Python 3.12.14.
[Output](and_price_probe.json) includes source and dependency hashes. This is
same-model developmental checking of these panels, not independent review.
