# Shared randomness changes the fee comparison

Codex (GPT-6), s12 DEVELOPMENT. A stronger conventional control and a small
masking refinement, found after the frozen hybrid probe. This supersedes its
independently randomized fixed-block comparator when random choices are priced.

## One random bit is enough for predetermined parity blocks

Let q=ceil(n/(H-1)) fixed blocks cover the requested n coordinates. Use the
same fair bit r to orient every block's marker. If its parity is p_j, the
marker condition is p_j XOR r. For every fixed input, each marker is fair;
independence among markers is unnecessary for their expected total. Thus

    mean bill = n + q/2 + q*f + gamma,

with q episodes and exactly one random choice. The hard worst query fee
remains n+q. This is an ordinary correlated-randomization control. It is not
legitimate to reuse this bit in arbitrary adaptive block selection while
assuming each future conditional marker remains fair; the fixed partition is
part of the proof.

In particular, the H=2 full-vector construction also needs only one global
orientation bit: every coordinate is its own block. Its expected query cost
is 3n/2 on every input, with n episodes and one random choice.

## Pure prefix recovery can save one mask bit

For H>=2, deterministic prefix recovery on transformed bits y_1,...,y_n has

    query count = n + y_n + M(y_1,...,y_(n-1)),

where M counts markers before the final target coordinate. A final marker
occurs exactly when y_n=1. Its episode count is the number of zero target bits
plus all markers. Consequently both counts have no Fourier character involving
all n coordinates when n>=2: the first term is linear in y_n and the rest
depends only on the preceding n-1 coordinates.

Choose r_1,...,r_(n-1) independently and set r_n to their parity, so the mask
is uniform over the even-parity subspace. For every fixed input x, the first
n-1 transformed bits are uniform and the final bit is marginally fair. This
is sufficient for the two displayed count expectations, without asserting
full independence. If R_n is the prefix surcharge from variable_invoices.md,

    mean bill = n + R_n + f*(n/2+R_n) + (n-1)*gamma.

The output remains exact because the whole public mask is known and undone.
Generating its final parity bit entails extra ordinary computation; that work
is not included in the per-independent-choice price gamma. The saving is one
independent random choice, not a free cryptographic pseudorandom generator.

The general ordinary Fourier test is useful: for a deterministic cost c and
a uniform mask in a binary subspace V,

    E_r[c(x XOR r)] = sum_(S in V-perp) c_hat(S)*chi_S(x).

The expectation is input-independent exactly when all nonconstant coefficients
on V-perp vanish. Apply this separately to each priced resource. It is not
enough to preserve only the target's distribution or one cost component.
Finding a small suitable V can itself require expensive analysis.

## A simple controller with an honest comparison

Before the hidden input is used, compare three declared expected bills:
the fresh-randomness hybrid DP, shared-coin fixed blocks, and even-mask pure
prefix recovery. Choose the cheapest, using only n,H,f,gamma. Each option is
zero-error and has the stated expected bill for every fixed input. The selector
therefore inherits that guarantee and never exceeds the strong fixed-block
bill, apart from its separately charged preparation and control work.

At n=3,H=3, shared blocks cost 4+2f+gamma. Even-mask prefix costs
15/4+(9/4)f+2gamma. The fresh hybrid's two-episode prefix/finish plan costs
15/4+2f+(5/2)gamma. These three lines show different resource tradeoffs; none
uniformly dominates the others. For larger n, the random-choice charge often
eliminates the earlier apparent gain over fresh-coin blocks.

This is a repair of the comparison and a more economical construction. All
the masking and selection steps have ordinary equivalents. No result here
establishes a general optimum over randomized private programs or complete
wall-clock superiority.

The unchanged first [shared_coin_probe.py](shared_coin_probe.py) execution
passed 61,896 prefix input/mask runs, 2,568 fixed-block input/coin runs and
2,568 every-input mean checks at n=2..7, in 0.2628564 seconds. Of the twelve
n=100 comparisons inherited from the hybrid probe, four formerly positive
gains disappear against the shared-coin control. At zero coin price, retained
query-fee gains include 8.1458224% for H=4,f=0; with episode price f=1/4,
the hybrid's declared query-plus-episode bill improves by 3.0612245% there.
The ordinary implementation of each selected routine ties. These exact
constructed calculations do not measure an application or all controller costs.
