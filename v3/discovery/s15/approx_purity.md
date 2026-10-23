# Approximate count purity: a discontinuous cap, a growing resource price

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 37.

Use the [fresh-reset contract](reset_contract.md): inputs x in {0,1}^n,
at least one primitive bit query per episode, cap two, only the count C in
{1,2} observed, and no retained input-dependent private state. Let Q be
complement-invariant, including Q(x)=(weight(x)-n/2)^2. Replace exact purity
by the condition that, at every public history, distributions for inputs in
the same Q-cell have total variation distance at most eta, 0<eta<1.

Every cap-two channel has p(x)=P(C=2|x)=a+sum_i b_i x_i: its first queried
coordinate is chosen before seeing the input. Since Q(x)=Q(1-x), the
approximate-purity condition gives

    max_x |p(x)-p(1-x)| = sum_i |b_i| <= eta.

Consequently the count distributions for ANY two inputs have TV<=eta.
This characterization is exact at cap two: an affine attainable channel
with coefficient l1-norm <=eta satisfies the requested cellwise bound.

## Finite horizon and information price

Coupling episode by episode gives TV between any two T-episode transcripts
at most 1-(1-eta)^T, even with adaptive public choices. Distinguishing two
different Q-values with error at most epsilon on each therefore requires

    T >= log(2 epsilon)/log(1-eta).                         (1)

For eta<1, zero error is impossible at any finite fixed horizon.

A sharper information currency is available. Any binary-output channel
whose output probabilities occupy an interval of width at most eta has
capacity at most

    C_eta = log[1+eta (1-eta)^((1-eta)/eta)] nats.            (2)

For a fixed interval, only its endpoints are needed; introducing their
randomized interpolation can only lose information. Capacity is convex in
the left endpoint, so the largest interval capacity is attained at [0,eta]
or its reflection. Optimizing the Bernoulli input prior for that Z-channel
gives (2). In particular C_eta is asymptotic to eta/e as eta tends to zero.

By the conditional chain rule, I(Q;transcript)<=C_eta T for fixed T.
For a uniform prior on K possible Q-values, Fano yields the necessary bound

    T C_eta >= log K-h(epsilon)-epsilon log(K-1).

For an almost-surely finite zero-error procedure with finite expected length,
the stopped-transcript chain rule instead gives E T>=H(Q)/C_eta. Query
choices and stopping must depend only on the past and independent coins;
otherwise they can carry an uncharged input channel.

## Any positive eta nevertheless permits eventual exact recovery

For one input bit, choose a public sign uniformly each episode. If the sign
is positive, output count two with probability eta*x_i; if negative, use
eta*(1-x_i). Otherwise output one. Count two certifies the bit from the
known sign. Each episode meets the eta-purity condition. Success probability
is eta/2, so the expected number of episodes is 2/eta. Repeat for all n bits.
This recovers the entire input, hence Q, with zero error and expected at most
2n/eta episodes and (2/eta+1)n primitive queries. Random-bit generation,
padding and internal computation remain separate costs.

Thus exact purity's cap-two impossibility disappears for every positive
per-episode tolerance, while the required acquisition price diverges as
eta goes to zero. The transcript eventually reveals distinctions INSIDE a
Q-cell: per-episode approximate purity is not a global privacy guarantee.
This is a changed duty, not an improvement to the exact-purity cap theorem.
Identical ordinary channels tie. General composition, channel capacity and
query-complexity methods are the relevant prior art; novelty is unassessed.
The [numerical screen](purity_probe.py) passes20,705 binary-channel grid cases
and405 affine complement checks. At eta=.01, identifying five equally likely
summary values at error .01 requires at least418 fixed-horizon episodes by
the information bound. Almost-sure zero-error identification needs mean at
least436.11; the eight-bit construction gives mean at most1600. These are
different termination duties, not competing estimates of one optimum.
Runtime23,932,900 ns, Python3.12.14, and source hash are in
[the result](purity_probe.json). No query-fee or CPU benchmark was run.
