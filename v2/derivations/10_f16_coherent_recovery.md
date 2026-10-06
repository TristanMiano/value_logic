# F16 optional extension: a coherent optimal decoder at equal old prices

**Accepted at F16 scoped mathematical review — October 5, 2026.**
Principal reconstruction and algebra audit: **ChatGPT (GPT-6 Astra Pro)**.
The candidate and a proposed proof came from the separate F16 price review;
the principal checked the algebra and supplied the two envelope arguments
below. This is an optional mathematical extension, not a rerun, an amendment
to the frozen experimental protocol, or a worldwide-priority claim.

## 1. Exact statement and the distinction it resolves

Use C4-A2's reset family, k>=2, unit old attempt prices and M>=0. Retain the
complete exact old numeric mean profile, or its equivalent canonical summary.
The domain consists of every Boolean joint law compatible with that summary.
No additional law restrictions, whether convex or otherwise, changed outcome population or changed
terminal penalty are admitted here.

For every nonempty such fiber, a **single compatible law** attains the minimum
possible maximum absolute error for all revised-order means after one
attempt-price edit epsilon with 1+epsilon>0. Its construction is explicit after reading the canonical
summary. The largest conditional proper-prefix interval width is a singleton
width. Therefore the unrestricted and law-valued minimax radii coincide.

This is weaker than requiring every coordinate's own interval midpoint.
The k=4 example in C4 §11 still has incompatible coordinate midpoints. A common
maximum tolerance leaves room to move narrower coordinates inside their
allowed bands. This theorem concerns that common tolerance.

The same law is optimal for each separately applied single-price edit,
because each uses a proper-prefix moment. For a bounded collection with
supremum magnitude E, its joint worst error is E times the conditional
proper-moment radius. There is no finite unnormalized error guarantee for
an unbounded collection when that radius is positive. It makes no corresponding
optimality claim for simultaneous price edits, arbitrary linear combinations
of moments, changed M, noisy old observations or extra law restrictions.

## 2. Reduction and proposed decoder

Set b=k+M and define

    g_h=(k+1)/(k+1-h) for h<k;  g_k=b;
    f_r(h)=binomial(h,r)/binomial(k,r), 1<=r<=k-1.

The canonical summary determines nonnegative residues rho_w and numbers
R=1-sum rho_w, B_rem. If R=0 the law is already known. For R>0 every
compatible law has the form

    p_w=rho_w + R*q_(|w|)/binomial(k,|w|),
    q_h>=0, sum q_h=1, sum g_h*q_h=mu=B_rem/R.

This is an exact parametrization,
including arbitrary nonexchangeable residue offsets. It follows directly
from the old profile's kernel; no new population observations are needed.

Write X_mu for the displayed level-law polytope and L_r,U_r for the minimum
and maximum of E_q f_r on it. The piecewise linear curve (g_h,h/k) is concave.
Thus

    p=L_1=(mu-1)/(b-1),

with attaining endpoint law q^-=(1-p)e_0+p e_k. Let q^+ be the mixture of
the adjacent g-levels bracketing mu, and write B_r=E_(q^+) f_r. Then B_1=U_1.
Define

    q_c=(q^-+q^+)/2.

We prove, for every r,

    2 U_r <= U_1+B_r,
    2 L_r >= 2p+B_r-U_1.                         (1)

Hence every admissible E_q f_r is within (U_1-p)/2 of the candidate value
(p+B_r)/2. Conversely, the two singleton extrema force error at least that
large. Thus the conditional proper-moment radius is exactly (U_1-p)/2,
and the original law fiber's radius is R times this value. A price edit
epsilon scales it by |epsilon|. The candidate p_c is obtained from q_c by
the displayed residue formula and is a compatible law.

Each upper/lower envelope is a polygonal hull with knots among the g-levels.
Between two consecutive g-levels every term of (1) is affine. It is therefore
enough to prove (1) at mu=g_j. The endpoints j=0,k are immediate. For
1<=j<=k-1 put t=j/k and a=f_r(j). The inequalities become

    2 U_r(g_j) <= t+a,
    2 L_r(g_j) >= 2p+a-t.                        (2)

The coordinate r=1 is immediate from its two extrema. In the remaining proof
r>=2, so k>=3. Binomial coefficients outside their usual lower range are zero.

## 3. An elementary polygonal-envelope lemma

Let x_0<...<x_N and y_0=0, after translating x_0 to zero. Suppose the adjacent
slopes first do not decrease and then do not increase. The upper concave hull
is the line from (0,0) to a point maximizing y_i/x_i over i>=1, followed by the original
polygonal curve. Choose the last maximizer when there are ties.

To see the shape, before the slope peak the secant y_i/x_i is a weighted
average of earlier adjacent slopes, and cannot decrease. A last maximizing
secant therefore lies at or after the peak, unless the whole remaining
curve is a tie; the last choice handles that case. Subsequent adjacent slopes
do not increase. The first slope after the chosen point is at most the
maximizing secant, since otherwise the next secant would be larger. The
line-then-curve construction is consequently concave and majorizes every
earlier point by maximality of the secant. Any concave majorant must lie
above that initial chord, and must majorize the later original points. This
proves minimality. A wholly convex or wholly concave sequence is included.

The same assertion holds when the second differences of y on an equally
spaced x-grid have one nonnegative-to-nonpositive turn. Initial zero values
and zero curvature cause only ties. We use these two equivalent forms below.

## 4. Upper inequality for distributions below the terminal level

Fix mu=g_j and temporarily allow only h<k. Tilt a level law x by

    y_h=x_h*g_h/g_j.

Then y is a probability law with E_y h=j. Conversely every such y determines
an admitted x. Put H_r(h)=(k+1-h)f_r(h); the objective becomes

    E_x f_r = E_y H_r / (k+1-j).

For n=r-1 and h>=1, set

    P(h)=binomial(h-1,n)/binomial(k-1,n),
    C(h)=(k+1-h)P(h),
    H_r(h)=h*C(h)/k.

The second differences are

    Delta^2 H_r(h) =
      [(k+1-r)binomial(h,r-2)-(r+1)binomial(h,r-1)]/binomial(k,r).

After the initial zero terms, their signs change at most once, from positive
to negative: the ratio binomial(h,r-1)/binomial(h,r-2)=(h-r+2)/(r-1)
increases with h. By §3 the upper envelope of H_r is a line from zero to a
last maximizer h_* of H_r(h)/h=C(h)/k, followed by H_r itself.

Furthermore

    Delta C(h) =
      [(k-h)binomial(h-1,n-1)-binomial(h-1,n)]/binomial(k-1,n) <= 1.

The first numerator term counts n-subsets with n-1 elements in a specified
block of size h-1 and one in its complement of size k-h, within a universe
of size k-1. It is at most the denominator; the subtracted term is nonnegative.
Thus F(h)=k+1-h+C(h) is nonincreasing. Also C(h)<=k+1-h since P(h)<=1.

If j<=h_*, then F(j)>=F(h_*)>=2C(h_*), and the envelope gives

    2 E_x f_r <= (j/k)*2C(h_*)/(k+1-j)
               <= (j/k)*[k+1-j+C(j)]/(k+1-j)
                = t+a.

If j>=h_*, the envelope equals H_r(j), giving E_x f_r<=a<=t, so the same
inequality follows. This proves the upper part of (2) for interior-supported
laws, without using a finite search.

## 5. Upper inequality after adjoining the terminal level

First take M=0. The adjacent slopes of f_r as a function of g below k are

    s_(r,h)=binomial(h,r-1)(k-h)(k-h+1)/[(k+1)binomial(k,r)],
    0<=h<=k-2.

After initial zeros their successive ratio is

    [(h+1)/(h-r+2)]*[(k-h-1)/(k-h+1)].

It is at least one exactly when
`(r-1)(k+1)-(r+1)h-2>=0`. Thus these slopes have one increase-to-decrease
turn. The terminal slope is s_T=2r/[k(k-1)].

If r<=k/2, apply §3 to the interior curve. Its last hull slope is either
the endpoint secant from g_0,

    2(k-r)/[k(k-1)],

or the last actual interior slope,

    6r(k-r)/[k(k-1)(k+1)].

Both are at least s_T. The first inequality is r<=k/2; the second follows
from 3(k-r)>=k+1, which follows from r<=k/2 and k>=2. Appending the terminal
point by its segment therefore preserves concavity and leaves the interior
upper hull unchanged. Section 4 bounds all its interior node values.

If r>=k/2, C(h) is nondecreasing for h<k. Indeed its nonzero successive ratio
is `h(k-h)/[(h-r+1)(k+1-h)]`, at least one when
`(r-1)(k+1)-rh>=0`; at h=k-2 this follows from 3r>=k+1. Hence

    max_(0<h<k) f_r(h)/(g_h-1)
      = 2(k-r)/[k(k-1)] <= 1/(k-1).

Every interior point lies below the endpoint chord, so U_r(g_j)=p.
For j<=k-2, `2p<=j/k` because `(k-j+1)(k-1)>=3(k-1)>=2k`.
For j=k-1, use `a>=f_(k-1)(k-1)=1/k` to obtain t+a>=1=2p.
This proves the upper inequality in both cases, including their overlap.

For M>0, a coordinate extremum is attained on at most two levels. At the
fixed interior mean g_j, an interior-supported pair is unchanged. For a pair
{h,k}, h<=j, the expectation is

    f_r(h) + [1-f_r(h)]*(g_j-g_h)/(k+M-g_h),

which does not increase with M. The M=0 upper inequality therefore covers
every M>=0.

## 6. A lower affine envelope and reduction to M=0

For each h, the sequence f_s(h), s=0,...,k, is nonincreasing and convex in s.
For h<k its second difference is

    f_s(h)*(k-h)(k-h-1)/[(k-s)(k-s-1)] >= 0

where the expression is needed; the remaining endpoints follow directly.
For h=k it is constant. Bound f_s(h), 0<=s<r, above by the chord from
(0,1) to (r,f_r(h)), and bound later terms by f_r(h). Then

    g_h = sum_(s=0..k-1) f_s(h) + M*1{h=k}
        <= (r+1)/2 + [b-(r+1)/2] f_r(h).

Thus

    L_r(mu) >= ell_r(mu)
      := max(0, [2mu-r-1]/[2b-r-1]).             (3)

At an interior node mu<= (k+1)/2, the deficit p-ell_r(mu) does not increase
as b grows from k. On the positive branch it equals

    (r-1)(b-mu)/[(b-1)(2b-r-1)].

The derivative numerator, after removing positive factors, is

    N(b)=-2b^2+4mu*b-(r+3)mu+r+1.

For b>=2mu-1, N is nonincreasing and
`N(2mu-1)=-(r-1)(mu-1)<=0`. On the zero branch the deficit is simply
(mu-1)/(b-1), also nonincreasing. Equivalently the deficit is the minimum
of these two nonincreasing functions. Since k>=2mu-1, M=0 is the worst
case. It remains to show at M=0 that ell_r(g_j)>=p-(t-a)/2.

## 7. Exact lower-node comparison

Write m=j, s=k-m>=1, n=r-1>=1. Then

    g_m=(k+1)/(s+1),
    d=t-a=m/k-f_r(m).

The required comparison is exactly

    d >= [2/(k-1)] * min(
           g_m-1, n*(k-g_m)/(2k-n-2)).          (4)

The two branches switch at n_0=2m/(s+1): the first is the minimum for
n>=n_0, the second for n<=n_0.

If m<r, then a=0 and s>=2. The proposed target p-t/2 is nonpositive,
because `(s+1)(k-1)>=3(k-1)>=2k`; so the nonnegative lower bound suffices.
Hence assume m>=r, in particular m>=2 and 1<=n<=m-1.

The product representation gives

    P=binomial(m-1,n)/binomial(k-1,n) <= (m-n)/(k-1).

For a direct proof, bound its first n-1 factors `(m-l)/(k-l)` by
`(k-1-l)/(k-l)`, since s>=1. Their product telescopes to (k-n)/(k-1).
Multiplying the last factor (m-n)/(k-n) proves the displayed inequality,
also for n=1. It follows that

    d >= m(n+s-1)/[k(k-1)].                    (5)

### Case s>=3

If n>=n_0, (5) proves the first branch of (4), since

    (n+s-1)(s+1) >= 2m+s^2-1 >= 2(m+s)=2k.

For 1<=n<=n_0, the second branch follows from

    F(n)=m(s+1)(n+s-1)(2k-n-2)-2kn(ks-1) >= 0.

This is a concave quadratic in n. If n_0<1 there is no such case. Otherwise
it suffices to check 1 and n_0. Direct substitution gives

    F(n_0)=2m(ks-1)(s^2-2s-1)/(s+1) >= 0,
    F(1)=2s^2 m^2+(2s^3-5s^2-3s+2)m-2s^3+2s.

For s>=3, the last polynomial increases with m>=2: its derivative there is
at least `2s^3+3s^2-3s+2>0`. At m=2 it is
`2(s-1)(s^2-2)>=0`. This closes both branches.

### Case s=2

Here m=k-2, 1<=n<=k-3, and the exact value is

    d=n(2k-n-3)/[k(k-1)],  n_0=2(k-2)/3.

For n>=n_0, the first branch requires
`3n(2k-n-3)>=2k(k-2)`. The left side increases throughout the allowed n
range. At n_0 its excess is `2(k-2)(k-5)/3`, nonnegative for k>=5.
For n<=n_0, the second branch requires

    (2k-n-3)(2k-n-2) >= 2k(2k-1)/3.

The left side decreases in the relevant range; at n_0 its excess is
`2(2k-1)(k-5)/9`, again nonnegative for k>=5. The remaining k=4 case
has only n=1, and gives `20>=56/3`. For k=3, m<r was already handled.

### Case s=1

Now d=n/k and n<=k-2<n_0=k-1. The second-branch target in (4) is
`n/(2k-n-2)`, at most n/k. This closes the last case.

Equations (3)–(5) prove the lower part of (2), first at M=0 and then at
every M>=0. The endpoint and interpolation argument in §2 proves (1).

## 8. Global formula and computational scope

Every conditional coordinate width is at most its singleton width. Taking
the supremum over exact old-summary fibers therefore gives

    max_(1<=r<=k-1) D_r = D_1
      = max_(1<=j<=k-1) [j/k-j/((k-j+1)(k+M-1))].

The sharp global revised-mean radius is |epsilon|D_1/2. Its attaining pair
is the singleton-extremizing uniform law on Hamming level j and endpoint
mixture from C4. Here 0<=R<=1, and zero residues with R=1 realize every
residual mean mu in [1,k+M], so taking the supremum loses no available fiber.
This replaces the need for triple enumeration when only that common radius
is wanted. It does not remove the input cost of reading an arbitrary old
summary or the work of computing its canonical residues.

The maximizing j can even be located by adjacent differences. Put
s=k+1-j, C=k+M-1, so 2<=s<=k. The objective is

    (k+1)/k+1/C-s/k-(k+1)/(Cs).

Its difference from s to s+1 is `-1/k+(k+1)/(C*s*(s+1))`.
Choose the smallest s in [2,k] with `C*s*(s+1)>=k*(k+1)`; if none exists
choose k. Equality gives a tie with s+1 when that lies in the interval.
Exact comparisons or integer binary search avoid an unverified floating
square root. This is an arithmetic-operation consequence, not a complete
bit-complexity or practical-speed comparison.

### Magnitude of the improvement

The sharp formula does not promise a uniform large improvement over the
ordinary interval bound |epsilon|/2. For fixed k, taking M to infinity in
the finite maximum gives D_1 -> (k-1)/k. For fixed M and increasing k,
choose j=k-ceil(sqrt(k)). Then j/k tends to one while
`j/[(k-j+1)(k+M-1)]` tends to zero. Since every moment interval has width at
most one, D_1 tends to one. The sharp radius consequently approaches
|epsilon|/2 for long chains. These are limits of the proved formula, not
new measured experiments.

At the frozen three-procedure setting M=4 the exact value is D_1=1/2,
so the radius is |epsilon|/4. For the small edit |epsilon|=1/40 this is
1/160, versus the ordinary universal bound 1/80. Both already meet the
frozen numeric tolerance 1/20. The factor-two numerical improvement there
does not establish a new successful decision, a regret separation or an
experimental advantage. Ordinary methods can use the same sharp formula.

## 9. Check against the existing k=4 midpoint counterexample

For k=4,M=1/10,mu=9/8 and zero residues, the canonical candidate has level
masses

    q_c=(181/248, 1/4, 0, 0, 5/248).

It has old mean 9/8 and proper moments `(41/496,5/248,5/248)`. The singleton
is at its own midpoint, but the pair moment differs from its individual
midpoint 1/48 by -1/1488. The common optimal radius remains 21/496. Thus
the negative world mass in the old coordinate-midpoint construction and
this coherent optimum are fully compatible statements.

## 10. Additional convex source restrictions can create a coherence penalty

The restriction to the full compatible old-summary fiber is substantive.
Here is a counterexample within the same reset model, rather than an unrelated
abstract query set. Take k=4,M=1, an exchangeable law with initial level masses
(1/5,...,1/5), and delta=1/200. Its proper moments are (1/2,1/3,1/4), terminal
moment 1/5, and every old order has mean B=137/60.

Add source restrictions saying that the level law lies in the convex hull of

    q_A=(40,40,34,48,38)/200,
    q_B=(30,64,16,52,38)/200,
    q_C=(40,48,22,52,38)/200.

All three laws are nonnegative, normalized and have that same old mean.
Their proper-moment vectors are respectively

    (1/2,1/3,1/4) + delta*(1,1,0),
    (1/2,1/3,1/4) + delta*(1,0,1),
    (1/2,1/3,1/4) + delta*(0,1,1).

These statements follow from the exchangeable Boolean inversion:

    q_4=m_4,
    q_3=4(m_3-m_4),
    q_2=6(m_2-2m_3+m_4),
    q_1=4(m_1-3m_2+3m_3-m_4),
    q_0=1-4m_1+6m_2-4m_3+m_4,

with m_4=B-1-m_1-m_2-m_3. Each added proper-moment sum is 2delta and
each terminal moment is 1/5-2delta=19/100. The extra information is an
ordinary nonempty rational convex source restriction; it is stronger than
merely retaining the old summary.

In normalized proper coordinates the query image is the triangle
`conv{(1,1,0),(1,0,1),(0,1,1)}`. Every coordinate ranges over [0,1], so
unrestricted midpoint predictions have sharp maximum error delta/2=1/400.
Every compatible decoded law instead has coordinates z in that triangle,
with sum z_i=2. Its worst coordinate error is
`delta*max_i max(z_i,1-z_i)`, at least 2delta/3 because some z_i>=2/3.
The centroid z=(2/3,2/3,2/3) attains this lower bound. The law-valued
radius is therefore 1/300, a factor 4/3 larger than the unrestricted radius.
Its centroid level law is `(55,76,36,76,57)/300`.

One fixed edited procedure can be preceded by prefixes of sizes one, two
and three, so its revised-order means realize all three coordinates. For an
edit epsilon these radii scale by |epsilon|. This example establishes an
actual coherence penalty after extra convex information is imposed. It does
not contradict the theorem: the canonical endpoint/adjacent mixture need not
satisfy those additional restrictions. It also explains why the theorem must
not be applied automatically to sources intersected with new empirical
confidence intervals.

Requiring the output to satisfy the **augmented source** is essential to this
gap. The unrestricted proper-coordinate midpoint is realized by the level law
`(75,96,56,96,77)/400`, which belongs to the original old-summary fiber but
violates the added triangle restriction. Both augmented-source radii are below
the original larger fiber's common radius 437/2400. This example concerns a
relative premium for the stronger output contract, not a claim that the new
information increased unconstrained uncertainty.

The compatible-output objective itself need not be monotone under source
restriction. To see this within the example, let Q be the convex hull of
q_A,q_B,q_C and the displayed unrestricted-midpoint law. Its coordinate
ranges are unchanged, but its midpoint law is now admitted, so its compatible
radius is 1/400. Restricting Q to the original triangle P removes that law
and gives radius 1/300. Thus P is a subset of Q while the optimal compatible
radius increases. The unrestricted radius stays 1/400: the feasible output
contract has also narrowed. Multiply both radii by |epsilon| for the revised means.

A compatible prediction law is still an estimate. Its membership in a source
does not establish that it is the true law. Reusing it requires carrying the
proved error guarantee for the declared query family, or verifying subsequent
claims over the full source. Inserting it as exact source authority would
silently discard the remaining uncertainty.

This exact additional-source example was derived after the predeclared finite
checks. It is a proof calculation, not an added case in their saved attempt or
a modified experimental result. Its separate proof review is recorded in the
F16 work log.

## 11. Review status and evidence discipline

Separate upper and lower proof reviewers found the envelope and lower-bound
arguments sound, subject to the statement clarifications incorporated above.
The additional-source counterexample was separately reconstructed and checked
in `../work_logs/F16_2026-10-05_S1/reviews/core/additional_source_coherence_gap.md`.
The previously predeclared finite search checked 735 rational level fibers
once, with all cases preserved; it motivated the candidate but is not used
in this proof. No new F15 or ND01 population, alignment, model or evaluation
was created. The frozen neural endpoint and retention counts do not change.

The principal accepts the mathematical reconstruction after those separate
checks. The required F16-R01 k=3 correction also has its own planar proof and
does not depend on this general extension. This acceptance is a scoped proof
review. F16 completed D60 and Research90; its principal review and work log
record the separate contribution, attempt and accounting dispositions.

### Further checked boundaries at k=3

The [source-uncertainty note](../work_logs/F16_2026-10-05_S1/source_uncertainty_boundary.md)
shows that the exact k3 midpoint argument survives further nonempty closed
convex restrictions, but can fail with uncertain old observations even on a
known support face. Its arbitrarily narrow interval construction gives an
explicit strict compatible-center premium. A compact nonconvex two-law source
attains the generic factor-two premium even with exact old observations.
The [separate audit](../work_logs/F16_2026-10-05_S1/reviews/core/source_uncertainty_boundary_audit.md)
also checks the nested-source corollary in §10. These additions do not change
C1's hypotheses, frozen results, or any claim of external priority.
