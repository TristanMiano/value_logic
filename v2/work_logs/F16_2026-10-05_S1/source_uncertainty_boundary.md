# F16: small uncertainty in old observations can restore a coherence penalty

**Accepted after principal reconstruction and separate hand audit.**
Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 5, 2026 UTC.
This is optional mathematical analysis within F16, not a new experimental
population, modified F15 analysis, neural recurrence or external-priority claim.
It sharpens the boundary of F16-R01/C1 before recommending future uncertain-source work.

## 1. What exact old data permit at k=3

At k=3, M>0 and exact equal-price old means, every old-summary fiber has
proper-moment shifts of the form delta m_i=u, delta m_ij=v, with terminal
shift -(u+v)/M. Any further nonempty closed convex source restriction gives a
compact convex set in these two coordinates. Its coordinate bounding-box
midpoint belongs to that set by the planar lemma in F16-R01. Therefore all
singleton/pair midpoint predictions are still jointly attainable by a law
satisfying the extra source restriction. Fixed exact old data are essential
to this common-two-direction description. Being a planar source set alone
is not enough when the requested means have three different directions.

## 2. A source with arbitrarily narrow old-mean intervals

Use three reset procedures with unit old attempt costs. Terminal penalty M
may be any nonnegative value; it will never be incurred. The declared source
says exactly one procedure fails. Let world w_i mean that procedure i fails
and the other two succeed, and write its probability p_i. No other world has
positive probability.

Choose 0<delta<=1 and a=(1-delta)/3. The additional source information is

    p_i>=a for i=1,2,3;  sum_i p_i=1.

Equivalently p_i=a+delta*z_i with z in the three-coordinate probability
simplex. Every old order beginning with i costs 1 if i succeeds and 2 if it
fails, so its mean is 1+p_i. The displayed source is exactly the known support
face together with the six old-mean interval constraints

    1+a <= C_old(order) <= 1+a+delta.

The upper bound follows from the other two lower bounds and normalization.
Each old-mean interval has width delta, which can be arbitrarily small.
These are stipulated mathematical source bounds, not a claim of empirical
coverage. The known support face is a substantive hypothesis; this example
is not asserted for the larger unrestricted noisy-summary fiber.

## 3. One revised price and its exact query geometry

Change only procedure 3's attempt price to 1+epsilon>0. If procedure 3 is
first, the revised mean is 1+epsilon+p_3. If i in {1,2} is first and 3 is
second, it is 1+(1+epsilon)*p_i. If i is first and the other unchanged
procedure is second, it is 1+p_i. These cover all six orders. Since exactly
one procedure fails, no third attempt or terminal penalty occurs.

After removing the known affine offsets, the maximum error over all six
means is the weighted coordinate error for z, multiplied by delta. Its
weights are

    alpha=max(1,1+epsilon) for z_1 and z_2;  1 for z_3.

Each z_i ranges over [0,1]. An unrestricted answer vector can place every
query at its own interval midpoint, so its sharp radius is

    r_free = delta*alpha/2.

A compatible decoded law must instead use one z in the simplex. Its radius is

    delta * min_(z_i>=0, sum z_i=1)
                  max_i w_i*max(z_i,1-z_i),
    where w=(alpha,alpha,1).

The endpoint values z_i=0 and z_i=1 are both attained in the source, so this
is equality, not an independent-interval relaxation of the uncertainty.

## 4. Solve the compatible-center problem exactly

Let r denote radius divided by delta. Every coordinate forces r>=w_i/2,
so r>=alpha/2. If 1<=alpha<=2, a value no greater than one also requires

    z_1,z_2 >= 1-r/alpha,   z_3 >= 1-r.

Summing gives r>=2alpha/(alpha+2). This bound is at least alpha/2 in the
stated range. It is attained by

    z_1=z_2=alpha/(alpha+2),
    z_3=(2-alpha)/(alpha+2).

All three coordinates are in [0,1/2], so their worst errors are indeed the
one-minus-coordinate endpoints used above. A purported radius r>1 already
exceeds the displayed optimum, so restricting the lower-bound argument to
r<=1 loses no candidate optimum.

For alpha>=2, use z=(1/2,1/2,0). Its weighted errors are alpha/2,alpha/2,1,
so the universal lower bound alpha/2 is attained. Consequently

    r_compatible/delta =
        2alpha/(alpha+2)  if 1<=alpha<=2,
        alpha/2          if alpha>=2.

The ratio to the free radius is 4/(alpha+2) in the first range and one in
the second. For -1<epsilon<=0 it is 4/3; for 0<epsilon<1 it is strictly
between one and 4/3. At epsilon>=1 the common largest tolerance leaves
enough room for compatibility. These are exact mathematical consequences,
not outcomes selected from a parameter search.

## 5. A small rational example and the implication

Take delta=1/100 and epsilon=1/10, so a=33/100 and alpha=11/10.
Every old mean lies in [133/100,134/100]. The optimal normalized center is
z=(11,11,9)/31, giving the compatible law

    p=(1034,1034,1032)/3100

on (w_1,w_2,w_3). The radii are

    r_free=11/2000,
    r_compatible=11/1550,
    ratio=40/31.

The component probabilities sum to one and meet the lower bound 33/100.
The coordinate midpoint z=(1/2,1/2,1/2) cannot be a law because its sum is
3/2. The best compatible center realizes the larger radius derived above.

This shows why even k3's exact-data coherence correction cannot simply be
promoted to uncertain old observations, even on a fixed known closed convex support
face. Arbitrarily small interval width can leave a strict *relative* gap;
the absolute radii both tend to zero with delta. It is not a discontinuity,
an assertion that more information worsens uncertainty, or a counterexample
to F16-C1's full exact old-summary theorem. Future confidence-set work must
state both the source and the decoded-law contract and check its own geometry.

No existing mathematical check or saved experiment was rerun for this result.
The proof and rational example passed the separate
[hand audit](reviews/core/source_uncertainty_boundary_audit.md).

## 6. Dropping convexity can attain the generic factor-two ceiling

For comparison keep exact old means, k=3 and M=4. Let q_A be the uniform
law on Hamming level 2 (exactly two failures), and let q_B put probability
5/6 on no failures and 1/6 on three failures. Both are exchangeable and have
every old order mean equal to 2: g_2=2 and (5/6)*1+(1/6)*7=2.
Declare the source to be the two-point set {q_A,q_B}, excluding mixtures.
This source is compact but nonconvex; it is not the full old-summary fiber.

The singleton moments are 2/3 and 1/6, with difference 1/2. The pair moments
are 1/3 and 1/6, with difference 1/6. After any fixed admissible single-price
edit epsilon, all revised-order means differ by at most |epsilon|/2, and an
order putting the edited procedure second realizes that difference. Thus an
unrestricted midpoint answer has exact common radius |epsilon|/4. A decoded
law required to be in the two-point source must pick an endpoint, whose
worst error is |epsilon|/2. For nonzero epsilon the ratio is exactly two.

This is the sharp generic ceiling from the ordinary-center argument, realized
inside the reset family. It illustrates why convexity in the positive k3
statement is substantive. Allowing the output mixture would change its
contract: the mixture is a law in the full old-summary fiber but not in the
stated two-point source. No claim about the F15 convex-source experiment or
about randomized expected-error criteria is made.

### Draft correction from the separate review

The initial §1 sentence omitted the word 'closed' when asserting compactness
of an added convex restriction. The separate reviewer identified this before
acceptance. The intended finite closed-polyhedral source scope is now
explicit. A nonclosed triangle such as x,y>=0, x+y<1 need not contain its
bounding-box midpoint. The original F16-R01 full-fiber proof and F16-C1
compact-polytope theorem do not require repair.

### Relation between the two uncertainty sources

At fixed delta>0 the revised-answer radius need not vanish as epsilon tends
to zero: the old answers themselves remain uncertain. This is why the exact
old-summary theorem's |epsilon| prefactor cannot be used as the entire error
budget in a future noisy-observation application. By contrast, at fixed
admissible epsilon both radii in this example vanish linearly with delta.
No discontinuity or unbounded amplification is present. A practical study
would have to distinguish old-observation error, additional price-query
uncertainty, and the constraint that the output satisfy its current source.
