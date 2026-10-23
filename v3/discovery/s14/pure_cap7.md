# The seven-bit pure-summary minimum cap is seven: finite evidence

Codex (GPT-6), DEVELOPMENT, October23,2026. This is a finite computational
characterization plus an explicit constructive argument, not an all-size
query theorem or an independently reconstructed confirmation.

pure_functions.py represents all65536 Boolean functions of the16 codewords
at once as bits of a Python integer. For each partial raw-bit assignment,
the zero-depth functions are exactly those constant on its possible
codewords. At depth d, union over choices of the next queried coordinate
the intersection of the two depth-(d-1) child sets. This is the exact
deterministic decision-tree recurrence, with all queries distinct.

The counts at depths0 through7 are

    2, 2, 2, 2, 2, 2, 72, 65536.

Thus only constant pure Boolean summaries have depth<=5. Since every
cap-H count event has depth<=H-1, caps<=6 reveal no first information.
Induction on public history gives impossibility for an exact pure
multi-episode decoder at those caps. Independent randomization is handled
by conditioning on its tape, under the same purity/exactness contract.
Here that contract requires purity for each fixed coin tape. A weaker
privacy condition that holds only after averaging hidden random coins is
not covered by this finite deterministic-depth argument.

At cap7, three even code characters, representatives3,5,9, each have a
depth-six tree. Query that tree and pad with ignored distinct coordinates
to count6 or7 according to the character. These three characters identify
one of eight pairs {c,c+1111111}. Given the pair, query any three raw
coordinates: majority agreement identifies the center because the input
is at distance<=1 from that center. Pad to count3 or4 to reveal which
center. The four public counts identify Q(x) and nothing else.

The v4 executable stores the three trees and checks all128 worlds,
constant transcripts on all16 quantizer cells, distinct transcripts across
cells, and mean total queries23. There are four episodes. The earlier
four-episode cap8 construction uses30 mean queries; this one reduces
that particular query count by7/30, with the same pure summary and four
reset charges. The cap22 one-episode construction still has the smaller
fee when available. No minimum mean-query or episode-count claim follows.

## Retained hypothesis and reporting failures

The initial all-functions screen also refuted the guess that depth-six
functions are exactly the complement-invariant functions. v2 made the
weaker guess that all such functions are complement-invariant; it failed
too. Neither conjecture is used in the cap argument. v3 completed the
construction checks but accidentally reported its final four invoice
counts in the depth-count field because a variable name was reused.
v4 corrects that output field and retains every previous source/output.
The original depth-vector result and v4 agree. No failure is attributed
to host instability. Closest ordinary finite decision-tree enumeration ties.
