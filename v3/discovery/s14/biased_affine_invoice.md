# Biased affine posteriors under paid coordinate access

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC.

Let X have n independent Bernoulli(p) coordinates, 0<p<=1/2. Queries
reveal one coordinate privately and cost one; each episode costs f>=0 and
outputs only its count in {1,...,H}. Public stopping is determined by public
history. Condition on independent public randomization. Suppose every
terminal public-transcript fiber is an affine subset of F2^n. The expected
Hamming error is D, expected query count Q, and expected episodes R.

Import Wu (2026), Lemma 1, for entropy of a Bernoulli product measure
conditioned on an affine space. It gives

    I(X;T) >= h(p)*(n-D/p).

The public H-ary prefix tree gives I(X;T)<=H(T)<=R*log2(H).
There is also a representation-independent query argument: condition on the
COMPLETE private coordinate-query history. Every never-read coordinate still
has Bernoulli(p) law, so even the best private estimator has conditional loss
p times the number of distinct unread coordinates. Public estimation cannot
have smaller mean loss. Therefore D>=p*(n-E[distinct Q]) and Q>=n-D/p.
Together,

    Q+f*R >= (n-D/p)*(1+f*h(p)/log2(H)).                 (1)

Use max(0,n-D/p) if the specified error exceeds the zero-information loss.
For randomized protocols the affine-fiber condition is required after fixing
the independent tape, with averaged loss and cost; an affine-looking mixture
posterior is not sufficient. Finite-mean infinite trees follow by truncation
and entropy chain rules. Private stopping cannot create an extra public symbol.

For unrestricted terminal cells, ordinary rate-distortion instead yields
R*log2(H)>=max(0,n*h(p)-n*h(D/n)) for 0<=D/n<=p. The universal query
bound is unchanged. The affine restriction costs public information, rather
than creating a stronger intrinsic coordinate-acquisition lower bound.

## Contribution and scope

This is a direct paid-observation adapter of an imported entropy theorem,
not a new Bernoulli affine-space inequality or a solution to biased parity
acquisition. The fair linear-lossy obstruction predates this session by
decades (Ancheta 1978, as identified and discussed by Wu). Full linear
quantization is NOT the comparison class: choosing the nearest word in a
linear reconstruction code is a nonlinear encoder and can have nonaffine
fibers. Adaptive parity observations with affine terminal fibers are covered;
arbitrary conventional quantizers are not. An identical ordinary construction
ties every proposed invoice procedure.

Primary source: [Wu, arXiv2608.22837](https://arxiv.org/pdf/2608.22837),
Lemma 1 and its proof through Lemmas 2-4. Source theorem is imported;
this development has not independently reconstructed all external proofs.
