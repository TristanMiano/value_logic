# Matching development screen: first-pass findings

Codex (GPT-6), October 28, 2026. The [prospectively frozen probe](matching_freeze.json)
passed on its first execution. Its [complete result](matching_result.json)
retains weights, two kinds of attaining witnesses, rational intervals, ranks
and environment details. Runtime194075400ns is one run, not a benchmark.
Execution time was excluded from engaged research.

All46233 perfect matchings for n=1,...,8 were enumerated across the eight
fixtures. The distinct-value counts were1,2,5,10,17,26,37,50, exactly
(n-1)^2+1. A separate augmenting-path residual matching routine found the
same value set and provided an attaining matching for every included edge
value. For n=8,40320 configurations thus yield50 distinct point values in
this fixture. That is an output-size comparison, not a measured runtime gain.

Exact vertex enumeration checked all30 noisy local slices for n=1,...,4.
Their closed-form endpoints agreed with the independent enumeration; all
images had positive width, and the union had1,2,5,10 components respectively.
The rational-rank calculation also agreed on all20 (n,k) pairs with
1<=n<=4 and0<=k<=4, including the exceptional one/two-block formulas.

These finite results corroborate the implementation of the proposed
construction. They do not establish the general face-chain theorem, a
new matching algorithm, empirical usefulness, or novelty. The general
argument remains in [face_chain.md](face_chain.md), [matching_scalar.md](matching_scalar.md)
and [partition_dimension.md](partition_dimension.md); the limited primary
comparison is in [matching_comparison.md](matching_comparison.md).

The useful distinction is now explicit: source component count and scalar
output component count are different resource quantities. An additive
readout can distinguish source components that a bottleneck readout merges.
V19's ordinary matching specialization should be used when its hypotheses
hold. This extension remains separate from the fixed V19 confirmation.
