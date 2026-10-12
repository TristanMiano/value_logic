# S13A: adaptive acquisition bounds from a common value baseline

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; no promotion forecast.

## A polynomial-size upper certificate for every observation tree

Fix independent uniform unresolved bits, pure coordinate observations, finite
terminal actions, and additive nonnegative fixed query prices q_i. Substitute
already known bits and combine coefficients before entry. Terminal utilities are

    y_a(x)=c_a+sum_e a_{a,e}*chi_e(x),    c_star=max_a c_a.

Any finite adaptive policy produces a terminal transcript H, revealed set B_H,
and conditional action values M_a(H)=c_a+sum_{e subset B_H} a_{a,e}*chi_e.
Conditional unobserved bits remain independent uniform: each transcript is a
cylinder determined only by values actually queried. Randomization independent
of the world can be conditioned on first. Repeated queries can be omitted.

Choose any fixed common polynomial g(x)=sum_e b_e*chi_e(x), with mean zero.
Its conditional projection M_g(H) has expectation zero by the tower property.
Consequently the policy's expected net improvement over immediate action is

    E[max_a M_a(H)-c_star-M_g(H)-q(B_H)].

For each realized terminal action and transcript, bound every remaining signed
term by its absolute coefficient. This gives the all-policy upper certificate

    Gamma(b)=max_a { -gap_a + max_B[
                        sum_{e subset B}|a_{a,e}-b_e| - q(B)] },
    gap_a=c_star-c_a >=0.

Each inner maximization is the ordinary closure problem already implemented.
Exact flow/cut witnesses therefore verify Gamma(b) without enumerating adaptive
trees. Gamma(b)>=0 because the best immediate action admits empty B. If Gamma
is zero, **no finite adaptive observation policy can have positive expected net
gain in the stated model**. A positive value is only an upper bound. Any fixed
or numerically proposed b yields a valid certificate; searching b does not
change the model or require trusting an optimizer.

A particularly cheap common baseline uses midpoint coefficients
b_e=(max_a a_{a,e}+min_a a_{a,e})/2 and radii
r_e=(max_a a_{a,e}-min_a a_{a,e})/2. One closure problem with r_e upper-bounds
Gamma and hence all adaptive gains. For two actions this is the earlier
|contrast coefficient|/2 construction: its zero test extends to adaptive trees,
even though the exact support-union planner itself remains nonadaptive.
Common value terms cancel automatically. Picking the incumbent's coefficients
can additionally exploit large action gaps and prove sign-dominance cases.

Gamma is convex in b: it is a maximum of sums of absolute affine functions.
Projection of each b_e into the range of that coefficient across actions cannot
increase Gamma. These facts support bounded convex numerical advice, with
exact rational checking afterward. They do not show this restricted penalty
family is complete or that a small upper bound always exists.

## An adaptive example with a sharp simple baseline

For independent fair x1,x2, take three utilities x1+x2, -x1+x2, and -x2.
All initial means are zero. With q1=q2=2/5, observe x2 first. If x2=-1,
choose the third action immediately; if x2=+1, observe x1 and select one of
the first two actions. Expected utility is 3/2 and expected observation cost
is 3/5, giving net 9/10. Midpoint coefficient baseline zero gives a looser bound.
The common baseline g=(3/10)*x2 yields closure values 9/10 for all three actions,
so it certifies this policy's exact optimum without a general tree search.
This is a small constructive example; it does not establish broad economics.

## A tighter rank-sensitive information relaxation

Instead of replacing all signed terms by absolute values, allow an anticipatory
choice of action and acquired batch after seeing the full world, and then average:

    U(b)=E_x max_{a,B} [c_a-c_star
                 +sum_{e subset B}(a_{a,e}-b_e)*chi_e(x)-q(B)].

The same zero-mean projection argument gives actual adaptive gain <=U(b)<=Gamma(b).
For sparse supports, enumerate unions and use the GF(2) rank of all involved
characters to average over at most 2^r parity outcomes. An optimal B can omit
bits that complete no nonzero term, so support unions suffice. Costs of this
enumeration must be counted; it is not a polynomial-time general algorithm.
Dropping negative completed terms gives another safe but weaker closure-based
upper approximation. No claim is made that optimizing b closes the relaxation.

## Closest comparison and an operational limitation to test

This is an information-relaxation argument: a common zero-mean conditional
projection penalizes an anticipatory acquisition plan. Brown, Smith and Sun
(2010), *Information Relaxations and Duality in Stochastic Dynamic Programs*,
is the relevant general framework. Its [Duke abstract](https://scholars.duke.edu/publication/762575)
and author-submitted abstract were read; the full PDF attempt was forbidden.
The specific argument above is reconstructed here, with no claim to a new
duality principle or to having checked their full strong-duality hypotheses.

Bilgic and Getoor (2011), [VOILA](https://arxiv.org/pdf/1401.3881), sections 2
and 3.1, already treat paid feature sets, complementarity, shared inference,
and reduced subset search under a supplied joint model. Their XOR example
already defeats singleton greedy. Our intended delta is the explicit sparse
value/martingale-to-closure certificate, not the discovery of nonmyopic value
or an advantage over optimal ordinary Bayesian acquisition.

Not all collections of valid terminal information cells form a realizable
sequential query tree. Kothari, Racicot-Desloges and Santha (2015), section 1
of the [primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol040-approx-random2015/LIPIcs.APPROX-RANDOM.2015.915/LIPIcs.APPROX-RANDOM.2015.915.pdf),
explicitly distinguish subcube partitions from decision trees and establish
stronger asymptotic separations. Only the introduction and definitions were
read here. A small multi-output matching partition can test how this known
obstruction affects our restricted common-baseline certificate, without
importing their full Boolean-function theorem as a new result.

## First finite screen and a concrete gap

[adaptive01.json](adaptive01.json) compares 36 random small problems against
an exact adaptive Bellman oracle. Every tested common baseline obeyed
adaptive gain <= rank-averaged U <= closure Gamma. The three-action example
has exact oracle and checked closure value 9/10. This same-model finite screen
does not confirm the general proof or establish timing superiority.

The following perfect matching of the four-bit cube supplies eight distinct
output labels, one for each pair (binary integers use bit 0 as the low bit):

    (0,1), (2,3), (4,6), (5,13),
    (7,15), (8,12), (9,11), (10,14).

Each pair is a one-dimensional subcube; fixing the other three bits identifies
its label. Each of the four unqueried edge directions occurs twice. Therefore
there is no coordinate common to all eight certificates. A real tree must
query some root coordinate. On the four worlds whose matching edge varies in
that coordinate, the already paid root query is unnecessary for the three-bit
certificate, and all four coordinates must be queried to identify that label.
All other worlds require at least three queries. Hence expected query cost is
at least (4*4+12*3)/16=13/4. The exact Bellman recurrence attains 13/4.

Assign utility one for the correct label and zero otherwise, and query price
q=1/100. At any ambiguous transcript, error probability is at least 1/2, while
all remaining queries cost at most 4/100; optimal stopping therefore never
accepts ambiguity. The true adaptive value is 1-(13/4)/100=387/400.

An anticipatory selector can instead choose the appropriate matching cell,
query its three fixed coordinates, and get value 97/100. For **any** function
g on the sixteen worlds, the expectation of its conditional projection on
these matching cells equals E[g]: the cells partition the world space. Thus
every mean-zero terminal common-baseline penalty has expectation zero even
for this nonsequential selector. Every U(b), even with unrestricted terminal
g, is at least 97/100, exceeding the actual optimum by at least 1/400. The
probe checks all fifteen nonconstant Fourier basis projections exactly; their
linearity covers every such g. This is a limitation of this restricted penalty
family, not a refutation of general information-relaxation strong duality.

The constructive repair is to condition penalties or upper potentials on the
actual sequential state, preserving which coordinate can be acquired next.
The next derivation is [sequential_bounds.md](sequential_bounds.md).
