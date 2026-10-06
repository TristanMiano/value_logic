# C4 discriminator: how much price revision destroys exact retention?

Contributor: **Codex (GPT-6)**. October 4, 2026.
Status: **accepted at C4's local scope**; worldwide priority unestablished,
F16 fresh reconstruction complete, with the dated F16-R01 clarification below. Ordinary mathematics and statistical applications,
not a new native rule or a completed deployment experiment.
This extends the [F13 fixed-price calculation](06_case_studies.md#51-fixed-positive-attempt-costs-and-full-orders).
It is a candidate small technical extension, not a new general theory of
information, a speed result, or a claim that all applications need these data.

## 1. Model and exact consumer

There are k>=2 reset procedures. A Boolean world F specifies which procedures
would remain unresolved on a fixed request. Their joint law p is arbitrary
on the full 2^k-world simplex. Every permutation pi of all procedures is an
allowed order; stop at the first success, or pay terminal penalty M after all
fail. Attempt prices c_i are fixed, strictly positive rational numbers.

Put m_S=P(all procedures in S fail), m_empty=1. Then

    C_pi(c,M) = sum_(j=1..k) c_(pi_j) m_(prefix(j-1)) + M m_all.

These are means under one fixed law. We distinguish all numeric means,
within-price order differences, and comparisons across price profiles.
Exact linear summaries may use arbitrary decoding; known constants are free.
The simplex direction dimension is n=2^k-1. The moment transform is invertible.
This model excludes stateful search, changed outcomes, a restricted law family,
arbitrary real encodings and free access to the discarded source.
Prices are parameters fixed for each query. Making both prices and moments
unknown object-language variables would introduce products c_i*m_S; this
note does not silently extend the native signed-CPWA fragment to bilinear
arithmetic. A revised price changes the loss expression and its request binding.

## 2. The kernel needed for the calculation

Let v_empty=0 and let v_S be a direction in moment space. Adjacent swaps a,b
after prefix S change the mean in that direction by

    (c_a-c_b)v_S + c_b v_(S+a) - c_a v_(S+b).

All order means have the same directional value precisely when

    v_A = sum_(r=1..|A|) t_r e_r(c_A)          (proper nonempty A),

with k-1 free t_r and a free v_all. Here e_r is the elementary symmetric
polynomial of degree r. The common value is

    S_c(t) + M v_all,
    S_c(t) = sum_(r=1..k-1) t_r e_(r+1)(c_all).

For completeness, the necessity argument starts with the swap at the empty
prefix, which makes v_i/c_i constant. After subtracting the terms fixed at
smaller subset sizes, the swap makes each residual at size r, divided by the
product of its costs, constant across one-element exchanges. The graph of
r-subsets is connected. This determines t_r. Substitution of the elementary
symmetric recurrence proves sufficiency. Each monomial of size r+1 is counted
once, at its last added element, proving the common-value expression.
S_c is a nonzero linear functional because e_2(c_all)>0.

Thus a single numeric profile has rank n-(k-1)=2^k-k, and its within-profile
differences have rank n-k. This is the existing F13 result, reconstructed here.

## 3. Two nonproportional prices identify the full law

**Claim C4-T1.** Let c,d be strictly positive and not proportional. The joint
collection of all numeric means at (c,M) and (d,N), with M,N>=0, has rank

    2^k-1  if at least one of M,N is positive;
    2^k-2  if M=N=0.

The collection of all within-profile order differences has rank 2^k-2,
regardless of M,N. If comparisons across the two profiles are also allowed,
the rank is 2^k-1 when M!=N and 2^k-2 when M=N.

Proof. A direction annihilating all within-profile differences must have both
proper-subset representations

    v_A = sum t_r e_r(c_A) = sum s_r e_r(d_A).

At size one, t_1 c_i=s_1 d_i for every i. Nonproportionality forces both
coefficients to zero. Suppose coefficients below r vanish. At size r,

    t_r product_(i in A)c_i = s_r product_(i in A)d_i.

If one coefficient is zero, positivity forces both to be zero. If neither is,
the products of the ratios d_i/c_i are constant over all r-subsets. For any
two indices i,j choose r-1 indices avoiding both (possible for 1<=r<=k-1),
and compare the two resulting products. Every ratio must be equal, a
contradiction. Induction therefore makes every proper v_A zero. Only v_all
remains, giving the within-profile rank. The directional numeric values are
then M v_all and N v_all. Numeric means detect that direction iff one penalty
is nonzero; their cross-profile differences detect it iff M!=N. This proves
all assertions. Small perturbations of an interior probability law realize
every remaining direction, so the rank is an actual summary lower bound.

The result is stronger than saying that arbitrary price changes require all
moments: two suitably distinct price vectors suffice. Even changing one
attempt price by any nonzero amount, while keeping it positive, is enough.
This is an exact-information statement and does not imply a large decision
change or a well-conditioned reconstruction.

## 4. A complete finite-family classification

Let a range over a nonempty finite family of profiles (c^a,M_a), with strictly
positive attempt prices and nonnegative penalties. If the family contains a
nonproportional pair, all proper directions vanish as above. Its ranks are:

| Consumer | Exact linear rank |
|---|---:|
| All numeric means | n if any M_a>0, otherwise n-1 |
| Order differences within each price profile | n-1 |
| All differences, including across profiles | n if the M_a are not all equal, otherwise n-1 |

If all price vectors are proportional, write c^a=lambda_a c with lambda_a>0.
The proper kernel is unchanged: e_r(lambda_a c_A)=lambda_a^r e_r(c_A).
In common coordinates (t,v_all), profile a has directional value

    lambda_a S_c(t) + M_a v_all.

The map (t,v_all) -> (S_c(t),v_all) has rank two. Let h be the rank of the
two-column matrix with rows (lambda_a,M_a); let h_delta be the rank of its
row differences from any fixed reference profile. Then:

| Consumer | Exact linear rank |
|---|---:|
| All numeric means | n-k+h |
| Order differences within each profile | n-k |
| All differences, including across profiles | n-k+h_delta |

Here h is one or two, and h_delta is zero, one or two. In particular, jointly
scaling every price including M adds no information; scaling attempt prices
while holding a nonzero terminal penalty fixed adds one direction. These
formulae cover redundant profiles and unchanged prices without an exception
hidden behind the word "generic". Zero attempt prices need F13's separate
degenerate analysis and are not covered by this theorem.

## 5. Constructive repair from k-1 new queries

**Claim C4-T2.** Start with a minimum-rank exact summary of all old numeric
means at c>0,M>0. Change only price c_j to c_j+epsilon>0, epsilon!=0, and
leave M fixed. Exactly k-1 additional independent linear measurements suffice
and are necessary to recover the full law. They can be chosen as k-1 actual
new order means, rather than arbitrary invented measurements.

Choose a reference order with j last. Its first r elements form P_r for
1<=r<=k-1. For each r choose an order having P_r immediately before j. The
new-minus-old mean of that order is exactly epsilon*m_(P_r), since only the
attempt at j changed cost. Its old mean is available from the old summary.
Thus k-1 new queries determine the chain moments.

Use the F13 attaining summary with this reference chain: its stored residuals
are r_A=m_A-sum t_r e_r(c_A), with zero residuals on P_r, and it stores the
reference mean B. The recovered chain moments determine t_r successively
through triangular equations with positive diagonal product_(i in P_r)c_i.
All proper moments follow from the residuals. Finally

    m_all = [B-c_first-sum_(l=2..k)c_(pi_l)m_(P_(l-1))] / M.

Any old minimum-rank summary of the exact means determines this canonical
summary, so the existence result does not depend on having stored one special
encoding. The old rank is n-(k-1), while the new combined rank is n; fewer
than k-1 independent added linear measurements cannot suffice.

Deterministic adaptive choice of extra order queries does not evade this
worst-case bound. Follow the algorithm at an interior law and fix its transcript
of q<k-1 responses. The old-summary kernel intersected with those q selected
measurement kernels still contains a nonzero direction. Small opposite
perturbations along it remain feasible and return the same transcript: by
induction every later query selection sees the same earlier responses. The
two different laws cannot both be exactly reconstructed. Query selection may
use the retained data and earlier replies, not an uncharged inspection of the
discarded law. This argument concerns exact linear oracle responses, not the
approximate samples used later in A3.

If M=0, no full-order mean at any price sees m_all. The proper moments can
instead be recovered with k-2 new queries on P_1,...,P_(k-2): the old B
determines the final t_(k-1), whose coefficient e_k(c_all)>0. At k=2 no new
query is needed to recover the already-determined proper moments. This does
not recover the full law, which remains impossible from these means alone.

## 6. Exact fragility does not imply practical fragility

Under the one-price edit, every order's pathwise new-minus-old cost lies in
[min(0,epsilon),max(0,epsilon)]. Therefore every mean, CVaR at a fixed level,
or worst-case version of either over the same law source changes within that
same interval. If pi_old minimizes one of those objectives over a common
policy family, then its regret under the new prices is at most |epsilon|.
Proof: compare the new value of pi_old to its old value plus the upper endpoint,
use old optimality, then compare the old value of pi_new to its new value
minus the lower endpoint. The interval width is |epsilon|.

Thus arbitrarily small nonuniform edits can require maximal exact numeric
information while allowing a small-regret unchanged policy. The lower bound
does not force maximal memory for approximate or action-only consumers.
Likewise, reconstructing m_(P_r) divides a mean difference by epsilon. If
each of the two observed means has error at most eta, that coordinate's
error can be as large as 2eta/|epsilon| before probability-range clipping.
This concerns separately perturbed aggregate means. If both prices are
evaluated on the **same retained world traces**, their pathwise difference
is epsilon times the indicator that j is reached; dividing its sample mean
by epsilon estimates that reach probability directly. There is then no
intrinsic 1/|epsilon| statistical amplification (apart from arithmetic
precision). Such paired traces are additional retained information, not
something available from the old compressed aggregate by assumption.
Exact ranks are not sample complexity, byte budgets or stable estimation.

## 7. A separate robust-choice warning

For any fixed law, changing only M adds the same Delta_M*m_all to every
full-order mean, so order differences do not change. This does not imply
invariance of the order minimizing the worst **absolute** mean over a source
of laws: the common addition depends on the law inside the supremum.

For k=2 and c=(1,1), let source P have (m_1,m_2,m_12)=(2/5,1/2,2/5), and
source Q have (4/5,1/10,0). Both are feasible joint laws. The order (1,2)
costs 7/5+2M/5 at P and 9/5 at Q; order (2,1) costs 3/2+2M/5 at P and
11/10 at Q. At M=0 the minimax choice is (2,1), with 3/2 versus 9/5.
At M=1 it is (1,2), with 9/5 versus 19/10. On each law the relative
comparison is unchanged. A common law-dependent offset preserves pointwise
preferences but can change worst-absolute-value choice. A mean-difference
consumer and a robust absolute-cost optimizer therefore have different
retention contracts. This is an ordinary robust-decision distinction, not
a counterexample to native loss-comparison soundness.

The positive counterpart is **minimax regret**. Subtracting the best order
within each law removes the common law-dependent offset, so changing only M
preserves every pointwise regret and its worst value over a fixed source.
In the example, the worst regrets of (1,2) and (2,1) are 7/10 and 1/10 for
every M. Thus an absolute minimax cost and a minimax regret are different
consumers even when both are informally called robust choice.

## 8. Known lower-order marginals change the incremental requirement

**Claim C4-T3.** Suppose every m_A with 1<=|A|<=s is fixed and available,
where 0<=s<=k-1. Assume the resulting probability-law fiber contains a law
with strictly positive mass on every world. Let

    N_s = sum_(r=s+1..k) binomial(k,r).

This is its affine dimension: the Boolean moment transform is invertible,
and a full-support law leaves a relatively open neighborhood in the fiber.
The following ranks count **additional linear coordinates**, beyond the
already known moments. They are not counts for a summary that must also
store those moments afresh for each request.

For one fixed profile c>0,M>=0, the numeric and within-profile ranks are

    numeric = N_s-(k-s-1),               if s<=k-2;
    numeric = 1 if M>0, else 0,          if s=k-1;
    within  = N_s-k+s,                  for every s.

For any two nonproportional positive attempt-price vectors, the combined
ranks are

    numeric = N_s if at least one penalty is positive, else N_s-1;
    within  = N_s-1;
    cross   = N_s if the penalties differ, else N_s-1.

Proof. A direction in this fiber satisfies v_A=0 through size s. In the
single-profile kernel, size-one equations force t_1=0 when s>=1. Inductively,
at size r<=s the remaining expression is t_r product_(i in A)c_i, forcing
t_r=0. Thus the within-profile kernel has k-s free coordinates:
t_(s+1),...,t_(k-1),v_all. If s<=k-2, the common numeric value is the nonzero
functional sum_(r=s+1..k-1)t_r e_(r+1)(c_all)+M v_all, removing one kernel
dimension even when M=0. If s=k-1, only M v_all remains. This proves the
single-profile assertions. Intersecting the two representations at sizes
r>s uses the same product-ratio argument as C4-T1 and leaves only v_all,
giving the combined ranks. Interior feasibility makes the rank lower bounds
attainable on the law fiber, not merely on an enlarged vector space.

Consequently, after a one-coordinate nonzero price edit, a minimum old
numeric summary plus the known low-order moments needs exactly **k-s-1**
additional measurements for full recovery when M>0. Choose the chain probes
at prefix sizes s+1,...,k-1. The earlier chain moments are already known;
the remaining triangular equations determine the coefficients. When M=0,
exactly max(k-s-2,0) such probes recover all unknown **proper** moments, with
the old base mean supplying the last coefficient when one remains. The
all-failure moment is still invisible. At s=k-1, no new probe is needed in
either case: M>0 already identifies the only remaining coordinate, and M=0
has no unknown proper coordinate to recover.

For example, k=3,s=1 leaves four unknown moments. One old positive-penalty
price profile has rank three; one extra new mean, with j reached after two
specified failures, completes the law. Fixing all proper marginals (s=k-1),
as in the original higher-order parity family, leaves a single parameter
that an old mean with M>0 already identifies. C4-T1's unconditioned n-rank
must not be restated as an additional n-coordinate requirement in that case.

Full support matters. If a fixed singleton failure probability is zero,
every larger moment containing it is also zero; the fiber can be smaller
than N_s and the displayed rank can overcount. More generally, for any
declared affine source restrictions Hm=h, the additional rank of query
matrix Q is rank([H;Q])-rank(H) when the feasible source is relatively open
in that affine slice. If it is confined to a smaller face, first compute its
actual affine hull. This is standard restricted linear algebra, not a new
generic source-identifiability theorem.
Small nonzero uncertainty intervals usually retain the full affine dimension;
they are not exact known-moment equalities. Their practical effect belongs in
an approximation or uncertainty-width analysis, not a fictitious rank drop.

## 9. An explicit collision at the old prices

For k=3,c=(1,2,3),M=4, list worlds lexicographically as 000,...,111. The two
full-support laws with numerator weights

    p+ : (105,35,35,101,35,97,93,59) / 560;
    p- : (35,105,105,39,105,43,47,81) / 560

have identical complete old numeric mean profiles and identical F13 attaining
summaries. Change only the third price by epsilon!=0, preserving positivity.
For order (1,2,3), the new means lie at

    13/4 + epsilon/4 +/- 3 epsilon/140.

For epsilon>0 they lie on opposite sides of the displayed midpoint. Thus an
old summary cannot decide every revised numeric threshold even for this one
edited price. This witnesses information loss; it does not assert that the
two laws require different optimal order labels. The laws differ in lower
marginals, so this witness must not be used for a fixed-singleton source.

## 10. Sharp approximation from an old summary: an optional extension

Exact failure to recover is not enough to choose a useful research target.
Here is a quantitative version with an attainable error, not just a rank.
Let k=3, c=(1,1,1), M>0, and allow every law on the eight worlds. Retain every
old numeric mean (or any equivalent minimal summary), then change only c_3
to 1+epsilon>0. The decoder must predict all six revised numeric means, with
worst absolute error over laws and orders. It may output arbitrary real
predictions; a common coherent decoded law is not required.

**Claim C4-A1.** The minimum possible uniform error without any extra data is

    |epsilon| (2M+1) / [6(M+2)].

In particular, M=4 gives |epsilon|/4. This is an information-theoretic
minimax radius for the specified consumer, not a runtime or statistical rate.

To prove it, take two laws p,q with identical old profiles. Their moment
differences have v_i=a, v_ij=2a+b and v_123=-(3a+b)/M by the old kernel.
Each world difference depends only on its Hamming weight h; write it w_h.
Boolean inversion gives

    M w_0 = (3M+3)a+(3M+1)b,
    M w_1 = -(3M+3)a-(2M+1)b,
    M w_2 = (2M+3)a+(M+1)b,
    M w_3 = -3a-b.

These signed masses sum to zero with multiplicities 1,3,3,1. They arise as
differences of probability laws iff

    |w_0|+3|w_1|+3|w_2|+|w_3| <= 2.

Necessity is total variation. For sufficiency the positive and negative
parts have the same mass at most one; add the same remaining probability
mass to both. This proves feasibility of the signed-law optimization without
assuming that p and q themselves are exchangeable.

The largest possible singleton difference is

    A(M) = (2M+1) / [3(M+2)].

For fixed a=1, minimizing the numerator of the displayed L1 expression over
b is a weighted absolute-deviation problem. Its ordered breakpoints are
-3, -(2M+3)/(M+1), -(3M+3)/(2M+1), -(3M+3)/(3M+1), with weights
1, 3(M+1), 3(2M+1), 3M+1. The third is their weighted median. At that b,
the minimum numerator is 6M(M+2)/(2M+1). Scaling to L1=2 gives A(M).
The case a=0 is harmless; changing signs handles negative a.

For completeness, the analogous largest pair-moment difference is

    B(M) = 1/[3(M+2)]                  for 0<M<=1;
           1/9                        for 1<=M<=4/3;
           (3M-1)/[3(3M+5)]            for M>=4/3.

Set 2a+b=1. The numerator to minimize becomes

    |3M+1+(1-3M)a| + 3|2M+1+(1-M)a|
      + 3|M+1+a| + |1+a|.

Its weighted medians are respectively a=-(M+1), a=-1, and
a=(3M+1)/(3M-1) in those three regions. At endpoints a whole interval may
minimize; the formulas agree. Substitution yields B(M), and B(M)<=A(M).

For an order whose edited procedure is reached after prefix S, the revised
mean is its known old mean plus epsilon*m_S. Prefix sizes are zero, one or
two. On each old-summary fiber, minimize and maximize m_S over the finite
probability simplex intersected with the old-mean equalities. These compact
linear programs have endpoints, and their widths are at most A(M). Predict
the midpoint for each order. Its worst error is at most |epsilon|A(M)/2.

The bound is attained. Let p be uniform on the three worlds with exactly
two failures, and let q put (M+1)/(M+2) on 000 and 1/(M+2) on 111. Every
old order has mean two under both laws. Their singleton failure probabilities
are 2/3 and 1/(M+2), differing by A(M). For any revised order with the edited
procedure second, the two new means differ by |epsilon|A(M); one common
prediction incurs at least half that error. This matches the upper bound.

This is a genuine numeric consequence of retaining only the old means, but
even this worst-error witness does not force an incorrect optimal-order
label: for epsilon>0, putting the edited procedure last is optimal for both
laws. A1 must not be recast as a policy-regret lower bound. The midpoint
decoder may require solving new linear programs. For this exact k=3,
single-attempt-price-edit consumer, its midpoint predictions are jointly
realizable by one compatible law, as established in the dated clarification
below. Returning exact intervals is also a sound retention contract.
The particular formulas are a small worked extension of ordinary partial
identification and linear-summary methods, not a new minimax principle.

### F16-R01 clarification: the A1 midpoint decoder can be coherent

**October 5, 2026; signed ChatGPT (GPT-6 Astra Pro).** The original sentence
immediately above said the midpoint decoder "may be incoherent across
orders." F16 found that warning overbroad for the exact A1 setting. The
radius, hypotheses, extremal witnesses and frozen experimental analysis are
unchanged. The following proof strengthens the allowed output contract.
The [F16 adversarial review](07_adversarial_review.md) records the correction,
its separate checks and the disposition of already exposed experimental data.

Fix a law p0 in any nonempty exact old-summary fiber. Equality of old means
`1 + m_i + m_ij + M*m_123` implies that every singleton moment difference
equals one scalar u, every pair moment difference equals one scalar v, and
the terminal moment difference is `-(u+v)/M`. Conversely these conditions
preserve every old mean. Boolean inversion therefore gives an injective
affine parametrization `p=p0+L(u,v)` of the entire fiber. Its admissible
coordinate set K is a nonempty compact convex subset of the plane. All
world-mass nonnegativity constraints remain in K; p0 need not be exchangeable.

Every nonempty compact convex planar set contains the midpoint of its
coordinatewise bounding box. For positive widths, normalize both coordinate
intervals to [-1,1]. If the origin were outside, strict separation and axis
reflections would give `a*x+b*y>=gamma>0` with a,b>=0. An attained x=-1
point implies b>a; an attained y=-1 point implies a>b, a contradiction.
Degenerate coordinate intervals reduce to a segment or a point.

Apply this lemma to K. Its bounding-box midpoint supplies a compatible law
p_star realizing every singleton and pair moment midpoint simultaneously.
After one attempt-price edit, each revised order mean is a known old mean
plus epsilon times a constant, a singleton moment or a pair moment. Hence
the same p_star realizes all six revised-order interval midpoints, for either
sign of epsilon. The A1 lower bound still applies to law-valued decoders, so
the stated sharp radius is also attained under this stronger coherence
requirement. Computing the decoder can still require linear optimization.

This does not require the terminal moment to be at its own interval
midpoint. For M=4 and old mean two in every order, the proper-moment midpoint
law has singleton moment 5/12, pair moment 23/102 and terminal moment 73/816;
the terminal interval midpoint is instead 1/12. Its exchangeable level masses
are `(275,135,333,73)/816`. Thus changed terminal penalties, arbitrary
combinations of query directions, nonconvex additional restrictions and k>=4
need separate analysis. The existing higher-dimensional incoherence example
is unaffected. This proof makes no new empirical or worldwide-priority claim.

## 11. Arbitrary k at equal prices: a small residual moment problem

The three-procedure closed form extends to an exact finite calculation for
every k>=2 when old attempt prices are all one. This is an application of
ordinary moment geometry; the symmetry reduction and its interpretation for
the specified summary are the added calculation. Allow M>=0 here.

Put h=number of failed procedures and define

    g_h = (k+1)/(k-h+1) for h<k;    g_k = k+M;
    f_r(h) = binomial(h,r)/binomial(k,r),   0<=r<=k-1.

The first expression is the average old full-order cost on a uniformly
random h-failure world. To check it directly, sum the probabilities of
reaching each attempt: sum_(r=0..h) binomial(h,r)/binomial(k,r)
=(k+1)/(k-h+1) by the binomial summation identity. Exhaustion costs k+M.
The second expression is the failure probability of a specified r-prefix.
The g_h increase strictly, including at h=k.

**Claim C4-A2.** Let D_r be the largest possible difference of an r-prefix
failure probability between any two laws with the same complete old numeric
mean profile. Then

    D_r = max_(0<=i<j<l<=k)
      | f_r(j) - [(g_l-g_j)f_r(i)+(g_j-g_i)f_r(l)]/(g_l-g_i) |.

The best uniform absolute prediction error for all revised means after a
one-coordinate edit epsilon is

    (|epsilon|/2) max_(r=0..k-1) D_r.

This gives an O(k^4) exact arithmetic calculation of the **global error
radius** from k,M. It is not a claim that every arbitrary encoded old summary
can be read or decoded in polynomial time. Its input already has exponential
dimension when no other restrictions hold.

Proof. The equal-price kernel makes each moment difference depend only on
subset size. Boolean inversion therefore makes the difference of world
probabilities constant on each Hamming level, even when the two original
laws are not exchangeable. Write d_h for its total signed mass at that level.
Identical old profiles are equivalent to

    sum d_h=0,    sum g_h*d_h=0,    sum |d_h|<=2.

The L1 condition is precisely feasibility as a difference of two laws, as
in A1. Conversely, any such d is realized by two exchangeable laws, adding
equal common mass if needed. The target difference is sum f_r(h)*d_h.

Equivalently maximize the difference of two expected f_r values over
probability distributions on {0,...,k} having the same expected g. There
are three independent equality constraints (two normalizations and a common
g-mean). A vertex has at most three positive masses in total across the two
distributions: with more, a nonzero null direction gives two feasible nearby
points, contradicting extremality. Each distribution needs one mass. A
nonzero optimum is therefore a single level j against a mixture of two
levels i,l bracketing g_j. Solving its common-mean equation gives the displayed
weights. Reversing the two laws accounts for the absolute value. Pure equal
levels give zero. Compactness ensures attainment.

Each old-summary fiber's r-prefix interval has width at most D_r. Coordinate
midpoints attain half the largest width for unconstrained numeric outputs.
The extremal triple witnesses the matching worst-case lower bound. The
argument applies to every subset of size r; it does not require the original
law itself to be symmetric. The finite calculation recovers A1 and its
piecewise pair-moment formula at k=3. No universal assertion that r=1 always
maximizes the radius is needed or claimed.

### A canonical summary gives exact conditional intervals too

Choose one reference world w_h in each Hamming level and retain the contrasts
p_w-p_(w_h) for all other worlds, plus the old mean averaged over full orders,
B=sum_w g_(|w|) p_w. This has 2^k-(k+1)+1=2^k-k linear coordinates.
It attains the old numeric rank: equality of these values is exactly the
equal-price kernel just characterized.

From the contrasts, form nonnegative residues rho_w by subtracting the
minimum contrast in each level, treating the reference contrast as zero.
Every compatible law has the unique form

    p_w = rho_w + z_(|w|)/binomial(k,|w|),
    z_h>=0,    sum z_h=R=1-sum rho_w,
    sum g_h*z_h = B_rem=B-sum_w g_(|w|)*rho_w.

If R=0 the law is known. Otherwise the remaining uncertainty is only a
distribution on k+1 levels with mean B_rem/R. For any proper subset S,

    m_S = sum_(w contains S) rho_w + sum_h f_(|S|)(h)*z_h.

Its endpoints occur on at most two residual levels. Enumerate i<=j with
g_i<=B_rem/R<=g_j and use the unique two-point weights (or one level at
equality). This computes sharp conditional intervals and actual attaining
laws, with no access to the original population after retention. Reading
the contrasts and summing the subset residues still costs work proportional
to their size; neither the ordinary control nor its source storage is free.
The implementation is a development control on valid generated summaries,
not an untrusted-data parser or a native proof rule.

### Individual midpoint answers need not form a reusable law

For k=4,M=1/10, take zero contrasts and B=9/8. This is feasible, for example
by mixing equal masses on h=0 and uniformly on h=1. The midpoint of each
proper-prefix interval gives

    m_1=41/496,    m_2=1/48,    m_3=5/248.

Here the subscript denotes size, not one selected index. If these midpoints
were one joint law, its full-failure moment would be forced by the old mean:
m_4=(B-1-m_1-m_2-m_3)/M=5/372. Inclusion-exclusion then assigns **-3/496**
to each specified world with exactly two failures. No such law exists.
Every separate interval and midpoint-error guarantee is nevertheless valid.
Return intervals or an explicitly feasible source representation when later
composition needs a joint law. This witness does not show that enforcing
coherence increases the optimum maximum error; it only refutes treating
separate midpoint outputs as automatically coherent evidence.

## 12. A consequential tolerance and threshold contract

Let R be the exact global prediction radius in A1 or A2 for the old-summary
interface and the specified price edit. The consumer must be declared:

- Numeric predictions of all new means with absolute tolerance tau are
  possible uniformly iff tau>=R, with arbitrary decoding and no extra data.
- For a positive margin gamma, require a binary answer to every query
  `C_pi(new)<=b` whenever the actual value is at least gamma away from b.
  Uniform correct answering is possible when gamma>R and impossible when
  0<gamma<=R. The requirement here forbids refusal on margin-qualified cases.
- Sound answers with permitted refusal need only return the sharp interval:
  certify when its upper endpoint is at most b, refute when its lower endpoint
  exceeds b, and otherwise report insufficient information. The preceding
  impossibility does not forbid this useful partial interface.

For the second statement, a midpoint prediction has error at most R<gamma,
so its comparison with b is correct. Conversely the diameter-attaining pair
has the same old summary and a revised query difference of 2R. Choose b as
their midpoint. Both cases have margin R but require opposite answers; one
summary-based binary answer cannot satisfy both. The weak/strict inequalities
are intentional: equality at gamma=R is already obstructed. This is the
standard indistinguishability argument applied to the computed radius, not
a new general classification theorem.

For k=3,M=4 and epsilon=1/10, R=1/40. The A1 witness laws have old mean two
for every order. When the edited procedure is second, their revised means
are 31/15 and 121/60. At b=49/24 both have margin 1/40 and opposite labels.
A tolerance above that radius permits approximate numeric use of the old
summary; a uniform forced answer at that smaller margin needs more information
or a changed contract. This supplies a concrete discriminator without claiming
that the best execution-order label must change.

If the old policy is only eta-optimal for its declared old objective, its new
regret is at most eta+|epsilon| by the same pathwise argument as section 6.
If every old objective estimate has error at most a, minimizing those
estimates supplies eta<=2a, hence regret at most 2a+|epsilon|. Uniform errors
must themselves be justified; estimates for a single preselected order do
not support this statement after searching many orders. These are ordinary
decision controls that can make recovering every exact mean unnecessary.

## 13. An explicit ordinary capacity representation

Set mu(S)=P(at least one procedure in S succeeds)=1-m_S, including
mu(empty)=0. This is a monotone coverage set function. For an order pi define

    x_(pi_j) = M + sum_(l=j+1..k) c_(pi_l).

These scores decrease along pi. The finite Choquet sum in descending order
therefore gives

    Choquet_mu(x) = sum_(j=1..k-1) c_(pi_(j+1))*mu(prefix(j)) + M*mu(all),
    C_pi(c,M) = sum_i c_i + M - Choquet_mu(x).

Substitution of mu=1-m proves the identity directly. This makes capacity
identification another ordinary formulation of the observation problem.
Here mu(all) need not equal one: forcing the usual normalization would erase
the unresolved mass. The elementary finite sum extends to nonnormalized
capacities and nonnegative scores; that extension, rather than a normalized
learning theorem, is all that is used. Not every monotone capacity is a
coverage function of a Boolean outcome law. Our nonnegative joint-probability
constraints must therefore remain in the identification model.

This representation reinforces the narrow novelty assessment. Generic
interaction-sensitive aggregation and identifying it by a design-matrix rank
are established methods. The candidate addition is the explicit structure
of this price-generated matrix, its revision repair and approximation
consequences. See the [primary comparison](../literature/06_c4_contribution_comparison.md).

## 14. Two optional refinements of the equal-price calculation

### A singleton diameter without triple enumeration

For the geometry in A2, the points `(g_h,h/k)` form a concave polygonal
curve. The slopes before the last interval are
`(k-h)(k-h+1)/(k(k+1))`, decreasing with h. The final slope is
`2/(k(k+2M-1))`, no larger than the preceding slope for k>=2,M>=0.
Consequently the endpoint chord lies below every other chord on its domain.
The singleton diameter is therefore

    D_1 = max_(1<=j<=k-1) [j/k - j/((k-j+1)(k+M-1))].

The witnesses are a uniform j-failure law versus a mixture of the all-success
and all-failure laws with the same old mean. This is a direct corollary of
A2 and elementary concavity. It computes one diameter in O(k) arithmetic;
it does not establish that singletons dominate every other prefix size.

### Coherence need not cost more in the displayed counterexample

The incompatible midpoint example in section 11 has largest half-width
21/496. An exchangeable law with total masses on levels h=0,...,4 equal to

    (11081/13144, 0, 63/424, 0, 55/6572)

has old mean 9/8 and lies within 21/496 of every feasible value of every
proper-prefix moment. Thus it attains the same maximum error as unconstrained
answers, although it does not attain every coordinate's own smaller
half-width. The distinction is between a common maximum tolerance and separate
coordinate-optimal tolerances. Exact vertex searches found no coherence
penalty in 54 specified fibers (k=3..6, M=0,1/10,4, adjacent g-level midpoints).
This is finite negative evidence, **not a universal coherent-center theorem**.

## 15. Nested-prefix samples give a bounded empirical repair

**Claim C4-A3 (application of established DKW concentration).** Assume the
old unit-price numeric summary is exact for the same fixed population p.
The population need not be exchangeable. Fix a canonical chain
P_r={1,...,r}, r=0,...,k-1, before collecting new observations. For each of
n independent requests from p, execute that chain until success or k-1
failures and retain the number J of initial failures, capped at k-1.
The observation uses at most k-1 procedure executions per request; it does
not reveal outcomes after the first success.

From the exact old summary obtain the residues rho in A2. For |S|=r, put

    kappa_S = sum_(w contains S) rho_w - sum_(w contains P_r) rho_w,
    hat_m_S = (1/n) sum_(i=1..n) 1{J_i>=r} + kappa_S.

The residual level contribution is identical for S and P_r. Therefore
`m_S-m_(P_r)=kappa_S`, and, deterministically,

    hat_m_S-m_S = empirical_P(J>=r)-P(J>=r).

One empirical distribution function controls all these errors, rather than
one independent estimate for each of exponentially many subsets. The ordinary
Dvoretzky–Kiefer–Wolfowitz–Massart inequality gives, for fixed n and eta>0,

    P(max_(proper S) |hat_m_S-m_S| > eta) <= 2 exp(-2 n eta^2).

For any single-coordinate attempt-price edit epsilon preserving positivity,
with terminal penalty M unchanged, predict
each revised mean as its exact old mean plus epsilon*hat_m_S, where S is the
prefix before the edited procedure. Simultaneously for all orders, all edited
indices and all edits with |epsilon|<=E, the error is at most E*eta on that
same event. Data-dependent selection among those queries is allowed. For
E>0, tolerance tau>0 and failure probability delta in (0,1), it suffices to
take

    n >= E^2 log(2/delta) / (2 tau^2).

More generally, multiple attempt-price edits with total absolute size at most
E have the same error bound: expand the new mean around its exact old mean
and apply the triangle inequality to the reach errors. This still keeps the
old prices equal to one, the penalty fixed and the population unchanged.

There is no division by a small price edit. This is possible because the
new observations directly measure nested reach events. It does not contradict
ill-conditioning of subtracting two independently noisy means and dividing
by epsilon. With E=1/10, tau=1/200 and delta=1/20, the displayed bound requires
738 independent requests, each using at most k-1 executions. These are
prospective mathematical sample counts, not a performed calibration study.

The exact old summary is a substantial prior-information assumption: it
already contains exponentially many population constraints. This does not
learn an unrestricted joint law from dimension-free data. If the old mean
and offset have separately justified simultaneous errors at most b and
a, the corresponding bound becomes `b+E*(a+eta)` on their joint validity
event; acquiring those old guarantees is not free. Combining failures uses
an explicit probability bound. An arbitrary stopping rule for n, source
drift, changed procedure outcomes or dependence across requests is outside
the stated guarantee. The estimates also need not describe a feasible common
law; intervals or a compatible source set remain the appropriate interface
when later composition requires one.

The concentration theorem is established mathematics, not a C4 discovery.
The added application is the exact-summary offset identity that lets one
stopped canonical trace family control this revision consumer. See the
[primary-source comparison](../literature/06_c4_contribution_comparison.md#7-sampling-extension-established-uniform-empirical-control).
No claim of optimal sample complexity or superiority to strong ordinary
methods is made; those methods can use the same construction.

### How the statistical statement can enter the existing proof contract

Form a source set from nonnegative world masses summing to one, the retained
old linear equalities, and the k-1 canonical reach intervals
`empirical_P(J>=r) +/- eta`. On the DKW event it contains the fixed true law p.
Every interval is about a population probability; an accepted conclusion
concerns a population mean, not the realized cost of the next request.
Selection of the revised order and threshold after observing the sample is
covered by the same simultaneous source event.

When these constants and the query parameters are rational, the source is a
closed rational polytope. Check nonemptiness and supply its feasible rational
witness; an empty fitted source requires refusal, not a vacuous proof. Put
the needed premise rows in units reachable by the target unit. F08's existing
characterization then supplies a finite native proof for each rational bound
valid on the target reduct. The actual receipt still needs the current
sample/source revision, loss expression, scope and requested budget. This
is a mathematical admission argument, not a newly executed native producer.

The rank and statistical results allow real-valued population summaries.
An irrational exact summary is not itself an admitted rational F05 context.
Use justified rational enclosures and carry their errors, or restrict this
native-admission bridge to rational inputs. Neither a fingerprint nor an
accepted proof certifies iid sampling, an unchanged population or the truth
of old exact-summary assumptions. Conditional on the stated modeling setup,
the probability of a false accepted mean conclusion is at most delta over
the new sample; this is not generally a delta bound conditional on acceptance.

## 16. Review and relevance

T1–T3 and A1–A3 have explicit arguments, direct-execution checks and a
[same-assistant reconstruction](../work_logs/C4_2026-10-04_S1/derivation_review.md).
The literature comparison names the established chain, identification,
optimal-recovery and concentration tools. The results add narrowly specified
consumer-revision consequences; they do not establish a new universal
calculus, a new concentration inequality or practical superiority.
F16's [fresh reconstruction](07_adversarial_review.md) is complete at its scoped
review, including the dated F16-R01 correction. The later
[coherent-recovery theorem](10_f16_coherent_recovery.md) supplies singleton
dominance and a compatible common-radius decoder on the full exact equal-price
fiber, resolving that former optional question. The original C4 finite evidence
and the k4 incompatible-individual-midpoint example remain valid. F16's bounded
primary comparison does not establish worldwide priority.
