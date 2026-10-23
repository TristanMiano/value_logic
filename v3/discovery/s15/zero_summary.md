# Exact summaries at cap6 with averaged privacy and random termination

Codex (GPT-6), October23,2026. DEVELOPMENT; pass12 extension.

The literal-cone screen found a nonzero pure acceptance probability p(Q(x))
that is zero at codeword0 and strictly positive at every other codeword.
The exposed floating solution initially failed independent small-denominator
rounding. zero_repair.py reconstructed its105-variable support by exact
Gaussian elimination and checked primal feasibility, dual feasibility and
zero gap. Both failed output and raw solver result remain preserved. This
was a rational-reconstruction defect, not evidence of hardware failure.

The protocol chooses a partial assignment with its saved nonnegative weight,
queries those at most five coordinates, and accepts iff they match. Weights
sum to1. Pad acceptance to count5 and rejection to count6. The acceptance
probability is exactly constant on each eight-element quantizer cell.

## A useful symmetry of the receipt

Average this protocol over the168 invertible linear transformations of the
three-bit parity-check column labels. They permute raw coordinates, preserve
the Hamming code and error balls, and are transitive on codewords of each
weight3 and4. The only nonconstant degree<=5 pure Fourier characters are
the seven coordinate characters. Averaging makes their coefficients equal.
The zero at0 therefore forces

    p(c)=a*weight(c).

Uniform-codeword mean acceptance is1/26 and mean weight is7/2, so a=1/91.
The all-ones codeword has acceptance1/13, agreeing with the exposed policy.
This symmetry is a mathematical consequence, not an extra solver result.
The random transformation is private and discarded with the episode.

## Las Vegas identification

Maintain the public set of possible codewords, initially all16. To test
candidate c0, virtually XOR every queried raw bit with c0 and apply the
channel. Translation by a codeword commutes with Q. An acceptance has
probability weight(c+c0)/91, so it eliminates c0 with no possibility of
eliminating the actual center c. Rejecting carries no elimination duty.

Cycle through all remaining candidates with fresh independent private
coins. Each incorrect candidate has a positive chance to be eliminated
on each visit. Almost surely all15 wrong candidates are eventually removed;
then deliver the remaining codeword exactly. Every conditional public count
law depends only on c and the public history. Therefore the complete
random-length transcript is pure after averaging the private tapes.

This gives zero answer error, cap6 in EACH episode, and finite expected total
work. It has no finite worst-case episode bound. A bounded-round version can
abstain when multiple candidates remain; it still never releases a wrong
center. It differs from s14's per-tape purity and deterministic four-episode
cap7 construction, so it does not invalidate that lower bound.

Let G_j be the visits needed to eliminate wrong candidate j. Each is
geometric with its specified parameter; independent local tapes can realize
them independently. The number of visits to the true candidate is at most
max_j G_j, so total episodes T<=sum_j G_j+max_j G_j<=2*sum_j G_j. Consequently

    E[T] <= 2*91*(7/3+7/4+1/7) = 4615/6.

This conservative bound is hundreds of resets, not an economic improvement.
It is nevertheless a constructive exact-decoding capability at the smaller
cap. After r full rounds, failure to finish is bounded by

    7*(88/91)^r + 7*(87/91)^r + (12/13)^r.

## Stronger-control question

The literal mixture's normalization is restrictive. A complete adaptive
depth-five decision tree may implement p(c)=a*weight(c) with a much larger
a. Query-probability feasibility only gives a<=1/7. A small extension of
the earlier flow LP can check this before any expensive decoder benchmark.
The present1/91 construction is retained even if a stronger control wins.
