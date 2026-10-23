# Optimal one-episode majority readout through an invoice

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. Strengthens the
explicit construction in nonlinear_invoice.md; the earlier full-read
probe remains immutable evidence for its weaker construction.

Let g=2m+1 fresh fair bits, cap H=g+1, and enough ambient coordinates
for one distinct padding query. An episode must reveal the exact block
majority through its count, with no other private output. Define G_g
as in nonlinear_invoice.md. The optimal expected count is

    Q_g=g+3/2-2*G_g.                                    (1)

This is an exact one-episode majority duty, not an all-task coding optimum.

## Construction and cost

Read distinct block coordinates until one value has appeared m+1 times.
Let tau be that stopping time and b the now-certified majority. If tau
has parity b, stop. Otherwise make one distinct padding query and stop.
The count's parity reveals b, and the count never exceeds g+1.

Under complementation of the block, tau is unchanged and b flips, so
exactly one of each paired worlds needs padding. Its expected cost is1/2.
At time tau the signed vote margin is g+1-tau, in favor of the final
majority. Remaining independent fair votes have conditional mean zero.
Therefore E[|final signed margin|]=g+1-E[tau]=2*G_g, proving (1).

## Lower bound, including arbitrary adaptive query orders

Before m+1 equal block answers have been seen, both majority values remain
possible. An exact algorithm must therefore acquire at least tau block
answers. Reading new fair coordinates in any adaptive order produces the
same iid answer sequence; unrelated marker bits provide no information
about this block. Conditional on tau, the majority is balanced by
complement symmetry of that answer sequence.

Every usable public count must decode to one majority value. For each
integer t, at most one sign may stop at count t. On the events tau=t,
the two signs are equally likely; at least one must use total count at
least t+1, and the other at least t. Thus E[count | tau=t]>=t+1/2.
Interspersed markers or queries after the majority is already known can
only increase the count relative to this constraint. Averaging gives
the matching lower bound. Independent randomization cannot improve it;
condition on its tape. This argument concerns a fresh fair block, not
arbitrary correlated posteriors.

## Stronger same-error separation

Substitute Q_g for g+1/2 in nonlinear_invoice.md. At the SAME expected
Hamming error, the optimized construction beats every affine-terminal-cell
protocol whenever

    f > [g+3/2-4*G_g]/[2*G_g/log2(H)-1],

provided 2*G_g>log2(H). Both public/private decoding and all queried
padding coordinates obey the existing invoice contract. No new accuracy
claim is obtained from the lower query count.

The public count may reveal more than the majority, but guessing every
coordinate as the majority remains the same valid estimator. Retaining
that fixed estimator avoids claiming an uncomputed extra distortion gain.

The nearest-codeword quantizer using the two antipodal reconstruction
vectors is also optimal among unrestricted one-bit Hamming quantizers of
g fair bits: two reconstruction vectors differing on k coordinates give
best mean error g/2-G_k, and G_k is nondecreasing in k. This conventional
quantization fact does not establish optimality among multi-output invoice
codes. The possible contribution is its paid readout composition.

For large g, G_g is asymptotic to sqrt(g/(2*pi)). The cost per unit of
Hamming improvement is approximately sqrt(2*pi)*(sqrt(g)+f/sqrt(g)),
up to lower-order terms. This suggests block size near f when the cap
permits it. It is an asymptotic design guide, not a new measured optimum;
the associated distortion approaches chance level as g increases.

The exact small screen in majority_probe.json passes 5,460 count colorings
and 2,730 world cases. At H=256, g=255, f=1000, its derived fee is
22.60278567% below the all-affine lower bound at error fraction
0.474992760503. This is a tariff calculation, not a measured stream or CPU
improvement. At f=100 the construction loses. Threshold query optimization
has a direct conventional ancestor in Acharya, Jafarpour and Orlitsky (2011),
Sections II-IV and Theorem 2; the claimed adapter includes invoice readout.
