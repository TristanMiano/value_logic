# F16 proof check — coherent midpoint decoding in the exact A1 fiber

**Signed: ChatGPT (GPT-6 Astra Pro), delegated independent proof check.**
2026-10-05 UTC. Principal clock credit: **zero**.

**Disposition: confirmed.** For C4-A1's exact k=3 model, unit old attempt
prices, M>0, a nonempty old-numeric-summary fiber, and one edited attempt
price, the coordinatewise exact interval-midpoint predictions for all six
new order means always come from one compatible law. This holds for arbitrary
nonexchangeable fibers, not only symmetric examples.

Consequently the statement in `09_c4_price_revision.md` §10, lines 401–403,
that this midpoint decoder “may be incoherent across orders” is overbroad
for its immediate A1 scope. The numerical radius theorem is unchanged. Its
same radius is attainable even when the decoder must return a law in the
old fiber. This is a mathematical clarification/strengthening of the output
contract, not a new experiment or novelty assessment.

The proof below was reconstructed from the proposed claim, then compared
with the exact C4 §10 wording. No experiment, saved search, frozen source,
or principal note was rerun or edited.

## 1. Derive the entire fiber in two coordinates

Fix any compatible reference law p0. Write m_S for its failure moments and
write delta m_S for the difference to another law in the same old fiber.
For an order (i,j,l), the old unit-price mean is

`1 + m_i + m_{ij} + M m_{123}`.

Subtract the equal-mean equations for orders (i,j,l) and (j,i,l). They give
`delta m_i=delta m_j`. Hence every singleton shift is one common u.
Subtract equations with the same first procedure and different second
procedures; then every pair shift is one common v. Finally each order's
equal-mean equation gives

`delta m_{123}=-(u+v)/M`.

Conversely these three relations make every old-order mean difference zero.
Together with delta m_empty=0 they specify every moment difference. Boolean
inversion therefore specifies one unique signed law difference L(u,v).

Define

`K = {(u,v): p0 + L(u,v) is a probability law}`.

K is exactly the old fiber in this coordinate chart. It is nonempty, compact
and convex: the original fiber is a closed affine section of the finite
probability simplex, and the chart is an injective affine parametrization.
Equivalently, its eight nonnegative world-mass conditions are affine
inequalities. No original law is presumed exchangeable; all its fixed
within-level contrasts are retained in the offsets supplied by p0.

For example, the world-mass shifts, grouped only to display their common
coefficients, are

| Exact number of failed procedures | Shift of each specified world's mass |
|---|---|
| 0 | `-3u+3v+(u+v)/M` |
| 1 | `u-2v-(u+v)/M` |
| 2 | `v+(u+v)/M` |
| 3 | `-(u+v)/M` |

The actual starting masses within one row can differ. Their individual
nonnegativity constraints all remain in K.

## 2. Planar bounding-box midpoint lemma

**Lemma.** Every nonempty compact convex K in R² contains the midpoint of
its coordinatewise bounding box.

If one coordinate interval is degenerate, K lies on a line and its other
coordinate projection is a compact interval. Convexity puts that interval's
midpoint in K. If both are degenerate, K is the single midpoint.

Otherwise translate and independently rescale the coordinates so that both
projection intervals are [-1,1]. Suppose the origin is outside K. Compactness
and convexity give a strict separating linear functional: there are a,b
and gamma>0 such that `ax+by>=gamma` throughout K. One may obtain this
directly from a closest point to the origin and the first-order inequality
for squared distance. Reflect coordinate axes according to the signs of
a,b; the projection intervals are still [-1,1], and now a,b>=0.

Because the x minimum is attained, some (-1,y) belongs to K with y<=1.
Thus `-a+b>=gamma`, so b>a. Similarly an attained point (x,-1), x<=1,
gives `a-b>=gamma`, so a>b. Contradiction. The origin, hence the original
bounding-box midpoint, belongs to K. No strict convexity or positive-area
assumption is used.

## 3. Apply the lemma to every proper moment and revised order

Let the projection intervals of K be [u_minus,u_plus] and [v_minus,v_plus],
and let `(u_bar,v_bar)` be their midpoint. The lemma supplies a compatible
law `p_star=p0+L(u_bar,v_bar)`.

Each singleton interval is its own fixed reference offset m_i(p0) plus the
same u interval. Each pair interval is m_ij(p0) plus the same v interval.
Therefore p_star realizes the exact midpoint of **every singleton and
every pair interval simultaneously**. Changing the reference law only
translates this chart; it does not change the resulting law.

If procedure 3's price changes by epsilon, each revised order mean is its
known old mean plus epsilon times its preceding-prefix failure moment:

- first position uses m_empty=1, a constant;
- second position uses m_1 or m_2, both fixed offsets plus u;
- third position uses m_12, a fixed offset plus v.

The midpoint of an affine image of an interval is the affine image of its
midpoint, including negative or zero epsilon. Thus the one law p_star
produces the midpoint prediction for every one of the six revised orders.
The unused singleton m_3 and pairs m_13,m_23 are also at their respective
midpoints; they create no omitted constraints because K retained the full
law and old-summary requirements from the outset.

The information-theoretic lower bound from two compatible witness laws still
applies to law-valued decoders. This coherent midpoint decoder attains the
same upper bound as the unrestricted decoder. Hence A1's radius

`|epsilon|(2M+1)/[6(M+2)]`

is also the minimax radius for a decoder constrained to return one law in
the current old-summary fiber. This is an existence result; calculating the
interval endpoints can still require work.

## 4. The terminal moment is a distinct output direction

The terminal moment is fixed **affinely** by u+v. It is feasible at p_star,
but need not be the midpoint of its own interval. This does not affect A1:
M is unchanged, its old contribution is already in the known old mean, and
a single attempt-price edit reads only an empty or proper prefix moment.

An exact boundary example has M=4 and every old-order mean equal to 2.
The exchangeable level laws have level costs `(1,4/3,2,7)`. Their fiber in
the absolute singleton/pair coordinates has vertices

`(2/3,1/3)`, `(1/6,1/6)`, `(7/17,2/17)`.

The coordinate midpoints are m1=5/12 and m2=23/102. The old mean then forces
m123=73/816. They are realized by the nonnegative level masses

`(275,135,333,73)/816`,

which sum to one and have old mean two. But the terminal moment's own
interval is [0,1/6], with midpoint 1/12=68/816, not 73/816. Thus one must
not extend this result to midpoints of **all seven** moment coordinates or
to arbitrary additional affine query directions. Merely saying a fiber has
dimension two would not justify that extension: the A1 outputs use only
the two aligned coordinate directions and constants.

The argument also does not establish universal coherence for k>=4, noisy
or incomplete old profiles, changed outcome laws, or arbitrary simultaneous
price/penalty queries. The previously reviewed k=4 incoherent-midpoint
witness remains consistent with this k=3 result.

## 5. Earliest dependency and scoped repair

The earliest affected assertion is the interpretive sentence following the
C4-A1 proof, not its radius formula, feasible witnesses, native kernel, or
soundness/completeness theorem. A suitable scoped correction is:

> For this exact three-procedure, single-price-edit consumer, the interval
> midpoint predictions are jointly realizable by one law in the old fiber.
> Computing their endpoints may still require linear optimization. Coherence
> for additional output directions or higher-dimensional fibers needs a
> separate argument.

No frozen file was changed by this review.
