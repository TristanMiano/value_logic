# An uncertain feasible witness plus a certified interior ball

Codex (GPT-6), DEVELOPMENT, s18. This is an early construction, not a
novelty or independent-confirmation claim. It connects value receipts with
actions: an approximate location of a feasible witness need not itself be
feasible, but known interior slack can convert it into a usable action.

## Exact Euclidean claim

Let d>=2, rho>0, epsilon>0, and suppose an unknown convex feasible set F
contains B(c,rho) and intersects B(a,epsilon). No other constraint on F is
used. Put D=||a-c||. If D<=rho+epsilon, the common feasible core of all such
F is exactly B(c,rho). If D>rho+epsilon, put

    u=(a-c)/D, T=rho*D/(rho+epsilon).
    K=conv(B(c,rho), c+T*u).

This K is exactly the common feasible core. Consequently the point

    y=(rho*a+epsilon*c)/(rho+epsilon)

is always feasible. It is useful outside the known ball precisely when
D>rho+epsilon. The point alone is the familiar interior-slack feasibility
repair; a contribution would require more than this routine observation.

Proof of repair: choose the promised x with ||x-a||<=epsilon and write
y=(1-lambda)*x+lambda*z, lambda=epsilon/(rho+epsilon), where
z=c+(rho/epsilon)*(a-x) belongs to the known ball. Convexity gives y in F.

For exactness translate c to zero. The minimal compatible sets are
conv(rho*B2,x), x in a+epsilon*B2. Their least support in unit direction h is

    g(h)=max(rho, h.a-epsilon)=max(rho,D*s-epsilon), s=h.u.

The common core is the intersection h.y<=g(h) over all unit h. When
D<=rho+epsilon the two balls intersect, and choosing x in their intersection
makes the minimal F just the anchor ball. For the other case put
s*=(rho+epsilon)/D in (0,1). If s<=s*, the constraint is h.y<=rho.
For s>=s*, express h as (s/s*) times a convex combination of unit normals
whose u-component equals s*. Such a combination exists because d>=2 and
the required transverse component has norm at most sqrt(1-s*^2). The
constraints at these normals imply h.y<=rho*s/s*=T*s. Together these
inequalities are the support constraints of conv(rho*B2,T*u). Conversely
its support max(rho,T*s) never exceeds g(h). This proves equality.

Dimension matters. In d=1 the exact extension along a-c is max(rho,D-epsilon),
not max(rho,rho*D/(rho+epsilon)); there are no transverse adverse witnesses.
For epsilon=0 the exact core is simply conv(B(c,rho),a).

## Rational boundary and a decision consequence

Take c=(0,0), rho=1, epsilon=2, a=(5,0). The guaranteed tip is (5/3,0).
The unit normal h=(3/5,4/5) and allowed witness x=(19/5,-8/5) satisfy
||x-a||=2 and h.x=1. Thus conv(B2,x) lies in h.z<=1 and excludes any
larger point on the positive horizontal axis. Reflection supplies the other
tangent plane. This is an exact, short obstruction to a stronger axial claim.

For the new objective f(z)=-z_1, every compatible F has an action of cost
at most -3, since its promised witness has x_1>=3. The best single action
known feasible for all F has cost -5/3. The witness-location receipt gives
a stronger value bound than an executable action; the interior ball still
improves the known action from cost -1 to -5/3. No query or computation saving
has been established, and a direct feasibility or action-returning oracle
is a necessary strong control for any economic comparison.

The action interpretation requires an actual convex action space. A point in
the convex hull of unknown feasible discrete assignments does not reveal a
mixture of those assignments that an agent can implement. Convexification
alone cannot silently supply that missing implementation.

## Status and comparison obligation

The general common-core support formula is prior guaranteed-hull machinery;
the repair is standard Slater-style convex feasibility restoration. The
exact Euclidean common core is a bounded specialization worth retaining,
but should be screened against robust projection, safe interpolation and
interior-point error-bound results before any contribution forecast.
