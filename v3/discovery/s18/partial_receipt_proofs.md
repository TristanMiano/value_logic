# Partial proof acquisition for a conditional value bound

Codex (GPT-6), s18 DEVELOPMENT. Ordinary LP certificates and set-cover
reasoning implement the construction. No new generic proof-search method
or measured fee saving is claimed.

For an upper bound U on the new linear optimum, start with all face options
T provisionally possible for each generator. A checked local certificate
that Q_i(T) is empty or that h dot x<=U throughout Q_i(T) excludes that
option from any source whose new optimum is>U. It also excludes every
superset of T, because those faces are smaller. If the remaining option
families cannot cover all old receipts with one option per generator, U
is certified. The remaining families may be overapproximations: one need
not solve every face LP to certify this nonexistence.

Conversely, explicit points on enough faces to cover all receipts, with
h dot x>U at every generator, give a concrete compatible countermodel.
Between these outcomes, the bound is unresolved. Purchased dual proofs,
infeasibility proofs and primal points can refine the two sides. This is
a concrete setting for the program's ordinary paid proof/cover controls;
their acquisition and checking costs must be charged.

## A small joint-receipt decision consequence

Use two independent hidden generators from the same rational polytope B
in R^3. Its six vertices are e1,e2,e3 and

    a1=(0,2,2), a2=(2,0,2), a3=(2,2,0).

The actual feasible set is their exact two-point hull. Retain three old
coordinate minima, all zero. The new objective is h(x)=x1+x2+x3.
Every point of B has h>=1. Every point of B with any specified two
coordinates zero is the remaining unit vector, hence has h=1.

The three old minima must be attained by two generators. One generator
therefore attains at least two of them and has h=1; the other has h>=1.
Thus the new optimum is exactly1 for every compatible source. A source
such as{e1,e2} attains all three old minima, so this is nonvacuous.

For distinct p,q, the face upper certificate can be written explicitly as

    h(x) <= 1+(3/2)*(x_p+x_q)  for every x in B.

Checking the six vertices proves this linear inequality. On the selected
zero-coordinate face it gives h<=1. The cover obstruction then says two
high-value generators, each able to attain at most one zero coordinate,
cannot cover all three receipts. No one receipt alone gives this result:
either generator can attain any one coordinate minimum at the corresponding
a_i, with h=4. The unconditional sharp upper value is also4.

If a fresh optimizer returns an attaining action for fee1/2 and the fallback
cost is2, the conditional warrant supports the fresh solve with worst cost
3/2; the unconditional upper bound4 would instead choose the fallback.
This is an exact illustrative decision, not an executed service saving.
The ordinary complete covering calculation ties, and retaining a usable
old full optimizer may offer a stronger control depending on its objective.

The value is identified without a guaranteed common feasible action:
the compatible sources{e1,e2},{e1,e3},{e2,e3} have hulls with empty joint
intersection. It is therefore legitimate for the decision to require a
fresh action-producing solve even though its optimum value is known.

Certified attainer identities change that last conclusion. Among the three
old coordinate reports, two must name the same one of the two generators.
If their coordinates are p,q, that generator is exactly the remaining unit
vector, yielding a concrete optimum without a fresh solve. It suffices to
retain a certified colliding pair of coordinates: one of three possibilities,
encodable in two bits apart from the source/certificate bookkeeping. This
does not price that bookkeeping or its original acquisition for free.

Two bits are also necessary for a deterministic fixed-length message that
always identifies an exact optimal action on this example. The three sources
{e_i,a_i} have distinct unique optimum actions e_i, so they need at least
three different messages. This is only a tiny information example, not a
general lower bound for all retention formats. The ordinary metadata-aware
controller has the same capability. It makes explicit when the old full
optimizer control can be replaced by less retained information.

## Arbitrarily large receipt complementarity

For k>=3, take n=k-1 hidden generators in the same polytope in R^k,
with vertices e_j and a_j=M*(1-e_j), where M>1. Retain the k coordinate
minima, each zero, and query the sum of coordinates. Every polytope point
has sum at least1. A point with two specified coordinates zero is in the
convex hull of the remaining unit vectors: each a_j has only one zero,
and nonnegative convex combinations cannot cancel a positive coordinate.
Consequently that point has sum1. The k receipts and k-1 generators force
such a point by the pigeonhole principle. The new optimum is exactly1.
Compatibility is witnessed, for example, by generators including e1,e2.

For every proper subset S of receipts, choose generators from the a_j,
including each j in S, and fill the remaining slots with other a_j.
Every point in their hull has sum M*(k-1), the largest value anywhere in B.
Thus the sharp conditional upper value U(S) is M*(k-1) for every proper S,
but U(all)=1. The bound-improvement set function U(empty)-U(S) has all of
its positive gain at the final receipt. It is not submodular; a greedy
retention rule based only on individual gains can discard every receipt.
This is an explicit instance of familiar complementary information, not a
claim to have discovered non-submodularity of information value.

For distinct p,q, the face certificate generalizes to

    sum_j x_j <= 1+((k-1)-1/M)*(x_p+x_q).

It holds at every defining vertex, so checking the two-zero face is still
elementary. Unlike k=3, a colliding pair of receipts need not identify a
single unit vector when k>3. The two-bit action result above must therefore
remain scoped to its three-dimensional example.

## Approximate receipts in the three-dimensional example

If each old coordinate minimum is only known to lie in [0,epsilon], the
same pigeonhole argument identifies a generator with two coordinates at
most epsilon. The displayed face certificate gives the upper bound
min(4,1+3*epsilon). It is sharp for every epsilon>=0. For 0<=epsilon<=1,
choose generators (epsilon,epsilon,1+epsilon) and a3. The first is the
convex combination (1-epsilon)*e3+epsilon*(a1+a2)/2; the three coordinate
minima lie in the required intervals and the new optimum is1+3*epsilon.
For epsilon>=1, use that construction at epsilon=1 to attain4.

Thus the fee1/2 solve remains strictly preferable to fallback2 whenever
epsilon<1/6 under this worst-case rule. This gives a tolerance for the
worked decision, rather than requiring exact real-valued storage. Approximate
attainer metadata alone no longer justifies the earlier exact unit-vector
action; that separate conclusion still requires the exact zero receipts.
