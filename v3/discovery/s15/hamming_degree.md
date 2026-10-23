# Minimum cap for any averaged-pure Hamming-summary information

Codex (GPT-6), October23,2026. DEVELOPMENT; pass12 generalization.

Let r>=2, m=2^(r-1), g=2m-1. Use the binary Hamming code C of length g,
whose parity-check columns are all nonzero r-bit vectors. Let D=Cperp be
its simplex dual. Its nonzero words all have weight m. The quantizer Q maps
each raw input to the unique codeword at Hamming distance at most1.

For any real phi on C, F(x)=phi(Q(x)) has cube Fourier coefficients

    Fhat(S)=ahat([S])*(1-|S|/m).                        (1)

Here [S] is the dual coset and ahat is the corresponding Fourier coefficient
of phi on C. This is the same direct uniform c+e averaging as in the
seven-bit calculation. It is a function identity, not a deployment-law
assumption. Cosets have disjoint supports, so coefficients from different
characters cannot cancel one another.

## Nonconstant pure functions have degree at least m+1

Suppose a nontrivial coset contributes and F has degree<=m. Since the
multiplier in(1) vanishes only at weight m, every word of that coset must
have weight<=m. Write its representative as S subset of the nonzero r-bit
vectors. Define f(0)=1 and f(u)=(-1)^1{u in S} elsewhere. Its Walsh sums are

    W_f(a)=2m-2*weight(S xor d_a),

where d_a is the dual word indexed by a. They are all nonnegative. Normalized
Fourier coefficients of f therefore have sum f(0)=1 and, by Parseval, sum
of squares E[f^2]=1. Nonnegative numbers with these two properties have one
entry1 and all others0. Thus f is a character, S belongs to D, and the coset
was trivial: contradiction. This proves the degree lower bound.

Every fixed-tape stopping event before cap H has query degree<=H-1; the
final-count event is its complement. Averaging private tapes preserves that
degree span. If each public count law is pure (depends only on Q(x)), then
H<=m+1 yields only constant count probabilities. No nontrivial one-episode
information is possible. Under fresh resets and conditional purity this
extends to any sequence, as specified in randomized_summary.md.

## Matching noisy channel at H=m+2

For a coordinate sign phi(c)=(-1)^c_i, the coset {i}+D has:

- One weight1 term with coefficient(m-1)/m.
- m terms of weight m-1, each coefficient1/m.
- m-1 terms of weight m+1, each coefficient-1/m.

Its Fourier absolute sum is3-2/m. Privately sample a term proportional to
absolute coefficient, query its support, and output the signed parity.
Pad to counts m+1 or m+2. Conditional on every raw input, the bit agrees
with the selected code bit with probability

    (2m-1)/(3m-2) > 1/2.

The count law is pure and informative. Thus the minimum cap for ANY such
one-episode information is exactly m+2=(g+5)/2, assuming enough distinct
padding coordinates. For r=2 the three-bit block needs one extra ignored
coordinate; for r>=3 the block already suffices.

At g=15 this gives cap10 and single-bit success15/22. Repetition can identify
g-r information coordinates with controlled error, paying every episode.
This is not a zero-error all-length generalization of symmetric_channel.md;
that explicit elimination rule is established only for g=7. Nor is it a
claim about per-tape privacy, correlated hidden state, arbitrary output
channels or optimal fees. Fourier query lower bounds and sampling are
classical ingredients; the exact paid-count/quantizer statement needs a
closest-literature assessment before any novelty or readiness judgment.
