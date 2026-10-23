# A compact stopping model for a symmetric protected summary

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 27.
Contract: n=2m, Q=(weight-m)^2, fresh private randomness, only counts public,
unit-cost distinct input queries, ignored padding allowed, cap H<=n+1.

Every permitted count channel can be implemented by a randomized stopping
rule on state (t,k): t queries so far and k ones among them, after uniformly
permuting and possibly complementing the input. The count law is unchanged
by this symmetrization because it was already constant on each Q-cell.
Under a uniform weight-w input, every ordered t-bit prefix with k ones has
probability (w)_k*(n-w)_(t-k)/(n)_t. Conditional on (t,k), the distribution
of internal histories and private coins is therefore independent of w.
Markovizing the stop decision at that state preserves every count law.
Complement symmetrization makes the stop rates at (t,k) and (t,t-k) equal.

Uninformative padding before the last decision can be replaced by fresh
input reads whose values are ignored; if a later simulated query asks for
one of those coordinates, use its cached value and spend that physical read
on another unused coordinate. There are enough distinct coordinates through
time H-1. The final query, if reached, can be ignored padding. This argument
uses unit prices and a private episode workspace; it is not valid for
arbitrary heterogeneous coordinate prices or private memory across resets.

## A finite flow polytope

Under a reference sequence of independent fair bits, let o_tk be occupation
mass, a_tk stopping mass and c_tk continuation mass. Then

    o_00=1,  a_tk+c_tk=o_tk,  a_tk,c_tk>=0,
    o_(t+1,k)=(c_tk+c_(t,k-1))/2.

Use this through t=H-1. Remaining mass produces count H. Enforce symmetry
under k<->t-k. The likelihood ratio for a weight-w input is

    L_w(t,k)=2^t*(w)_k*(n-w)_(t-k)/(n)_t.

For t<H, its probability of count t is sum_k a_tk*L_w(t,k); count H has
probability sum_k c_(H-1,k)*L_w(H-1,k). Conversely these flows implement
the channel by stopping with probability a_tk/o_tk at each nonzero state.
Thus any fixed linear score of the count probabilities, including a declared
decoder's Bayes loss plus query price, is a linear program of O(H^2) size.
If an empty episode is disallowed, set a_00=0. Query indices, randomization,
flow construction and arithmetic still have a computation bill.

This is an ordinary sufficient-statistic/sequential-decision reduction.
The candidate contribution is the exact paid count interface, not new
dynamic programming or a new generic LP method.

## Binary decisions are cheaper duties than identifying all summaries

For a fixed binary decision and prior on Q, the most informative folded
sample of H-1 bits can be reduced privately to its Bayes-optimal binary
answer. Counts H-1 and H transmit that answer. Hence the full folded
experiment's optimal one-episode Bayes accuracy is attainable under cap H,
even though its entire multi-valued observation need not fit that cap.
Early stopping may reduce mean query count without changing that accuracy.

An exact dynamic program can optimize the stopping policy for each fixed
mapping from counts to binary answers. Its state posterior is determined
by (t,k); compare stopping with continuing one query. At t=H the answer is
fixed by the decoder, so the last bit cannot improve it. Enumerating the
2^H count decoders is exponential in H, despite the polynomial state model.
Lexicographically maximizing accuracy and then minimizing expected queries
gives a clean small-instance strong control. This is a binary-prior duty,
not a worst-case all-summary decoder or a universal efficiency claim.

## Exact small-instance screen and a reusable stopping rule

`stopping_probe.py` enumerated count decoders and used rational dynamic
programming for n=4,6,8 and every cap from 2 through n+1 (18 cases).
The optimum accuracy equals the folded experiment in every case. All 288
four-bit permutation checks passed. Source SHA-256:
`ae7e8f6a4b8d930df31ac563895207250b924f081bbfb542d0944ee1c41be062`.
The measured run took 313,327,100 ns; that is the probe's runtime, not an
operational CPU improvement. Its evidence compares prior 1/2 on Q=0 and
1/2 on Q=1, the latter split equally over the two complementary weights.

At n=8, cap8, maximal binary-prior accuracy is 11/16. Mean queries fall
from 115/16 for fixed-depth sampling plus binary padding to 375/56 under
optimal stopping: 55/805, about 6.83%, fewer queries. There is one reset
either way. At reset price 100 the fee saving is only 55/12005, about 0.46%.
An ordinary implementation of this same stopping rule ties exactly.

For arbitrary n=2m>=4, a simple cap-n policy obtains the same binary
experiment as n-1 complete reads: return Q=1 early when m+1 equal bits
have appeared at a time t<=n-3; return Q=0 at time n-2 if the prefix is
balanced; otherwise read through n-1 and use counts n-1/n for the binary
decision. Earlier count labels are Q=1 where that early witness is possible.
The n-2 and n-1 count labels are Q=0, and count n is Q=1.

The fixed-depth wrapper costs n-1+(m-1)/(4m). This policy saves exactly

    Delta = (3m+1)/(4*(2m-1))
            + sum_(t=m+1)^(n-3) (n-t)*C(t-1,m)/(2*C(n,m+1)).

The first term is the probability of a balanced n-2 prefix; the second
counts earlier conclusive majority witnesses. The policy matches the
small-instance optima for n=4,6,8; no all-n optimality claim is made.
Counts n-2 and n-1 have the same likelihood ratio between Q=0 and Q=1,
and the other observed counts certify Q=1. Thus the extra stopping count
detail is ancillary for that binary experiment. The expected savings tend
to 5/8 of one query as m increases, so the relative query saving vanishes.
This asymptotic screen limits the practical lead rather than amplifying a
small-instance percentage into a scalable efficiency claim.
