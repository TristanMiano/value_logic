# A failed larger-cap potential and a different full-recovery menu

Codex (GPT-6), DEVELOPMENT, October22,2026. Preserve this negative result;
it does not refute the cap-three proof in vector_rate.md.

The tempting cap-four coefficient extension is

    a=(16+2f)/7, b=(6f-1)/14,
    F(W)=a E(W)+b |W|log2|W|.

It would give full-vector rate a/2+b=(15+8f)/14, attained by ordinary
prefix decoding. The coefficients make both the prefix shape and one
parity-prelude shape tight. That is not sufficient for all episode trees.

The first cap4_probe.py execution enumerated1,848 legal maps on three
unknown bits plus a distinct fourth padding coordinate, all255 nonempty
sources, and seven reset fees:3,298,680 local comparisons in2.0282981s.
At f2,5,10,100 the proposed inequality fails. The source can already be the
entire three-bit cube. Its invoice map in integer order0,...,7 is

    [2,2,3,4,3,4,4,3].

The cells have sizes2,3,3, separate11 of12 cube edges and have total query
bill25. Their entropy mass is22-6log2(3). At f2 the proposed potential drop
exceeds the actual bill41 by about0.242319639. This failure is exact in sign:
the claimed margin is (66log2(3)-108)/14<0, since log2(3)<18/11
(equivalently3^11<2^18). The other tested small fees had no finite violation;
that is not an all-size theorem. The executed script/results are immutable.

One legal implementation queries bit2 and then bit1. On prefix00 it stops
at2. On01 or10, it reads bit0, stopping at3 on0 and padding to4 on1. On11,
it reads bit0, stopping at3 on1 and padding to4 on0. All queries inside an
episode are distinct. This establishes the witness without trusting the
enumerator's reconstruction.

The failed local potential does not prove that prefix recovery is suboptimal
at cap4, and does not itself supply a better complete protocol. Its residual
cells can be expensive to resolve. Do not turn a failed lower-bound method
into a positive rate claim.

## An actual scope obstruction at cap5

At cap5 a single episode can read two fresh bits, then pad to one of the four
distinct counts2,3,4,5. Each count identifies both bits. Its average query
fee is7/2 and its reset fee is f, giving rate7/4+f/2 per recovered bit.
The pure prefix rate at cap5 is(31+16f)/30. The two-bit block is strictly
cheaper when f>43/2, with asymptotic difference(2f-43)/60 per bit.
It trades more queries for fewer resets. Distinct markers require at least
five ambient coordinates; final incomplete blocks cost only a bounded tail.

More generally, recovering r fair bits completely in one episode requires
at least r queries on every branch and2^r distinct counts. Thus it is possible
exactly when H>=r+2^r-1, and the least average query count in that service is
r+(2^r-1)/2. Read the r bits and pad to consecutive counts to attain it.
This is a one-episode counting argument, not an all-adaptive optimality result.

These observations motivate a broader constructive menu of prefix trees:
each invoice identifies a full leaf, the leaf determines a variable number
of fresh bits, and different leaves receive distinct affordable counts.
Optimizing that small exact menu is useful generation; an all-policy lower
bound and complete controller prices remain separate obligations.
