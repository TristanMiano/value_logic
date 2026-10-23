# Private reset state is a substantive resource assumption

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass24.
Two early counterexamples delimiting the pure-query threshold claims.

## Retaining queried values

If the private worker retains its input-dependent scratch state across
episodes, it can read one new input bit per episode and always return count1
for the first n episodes. It then knows the whole input. On later episodes
it can reveal any summary bit by count1 or2 using ignored padding reads.
All public outputs depend only on the summary, but cap2 now suffices for
any finite summary. Reading, storage and subsequent computation are paid.
The fresh-reset theorem's low-degree bound cannot apply to a worker whose
initial state already depends on all the input bits.

## Retaining only correlated random coins

Even if no queried values survive, shared private randomness can matter.
For Q(x)=x1 XOR x2, privately retain one fair bit R. In episode i=1,2,
query xi and use count1 or2 to report Zi=xi XOR R, with the second query
ignored padding. The pair(Z1,Z2) is uniform on the two strings with xor Q.
Its entire distribution depends only on Q; the second conditional count
law given the first also depends only on Q. Yet cap2 suffices, whereas the
fresh-independent-reset degree criterion requires cap3 for parity.

This is ordinary one-time-pad sharing. The retained coin acquires an
input-dependent posterior after the first public count, even though the
implementation does not retain the first queried bit. Thus erasing only
input values is not equivalent to refreshing all private randomness.
For a uniformly distributed parity, the two-episode construction averages
three queries and two resets. A single cap3 exact parity episode averages
2.5 queries and one reset; the lower cap is a different feasible interface,
not a total-cost improvement.

These examples do not refute the s15 thresholds, whose reset contract is
explicit. They do reject applying those thresholds to ordinary persistent
processes merely because an API calls each request a reset. Any application
must justify what memory and correlated state survive and charge them.
