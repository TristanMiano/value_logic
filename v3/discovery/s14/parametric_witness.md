# A reusable algebraic witness: useful, but directly anticipated

Codex (GPT-6), DEVELOPMENT, October22,2026. Early literature screen found
a close existing construction before implementation. Keep the application
contract and limitations; do not start a new benchmark under a novelty claim.

## Exact adapter

Let U be a known rational n-by-r matrix, b a known rational vector,
c=U^T b, and Y(t)=b^T(I+tUU^T)^(-1)b for t>=0. An untrusted provider commits
rational polynomials P,Q of degree at most r. Require Q(0)>0 and all Q
coefficients nonnegative, so Q(t)>0 throughout the service domain.

After commitment, the verifier samples T uniformly from a fixed set S of
positive rationals. The provider returns a rational r-vector z. Check exactly

    z+T*U^T(Uz)=c,
    Q(T)*(b^T b-T*c^T z)=P(T).

The first equation has a unique solution because I+T U^T U is SPD.
Woodbury therefore makes the checked scalar the true Y(T). Also Y has
a numerator and denominator of degree at most r, by adjugate/determinant
expansion of the r-by-r system. If P/Q is not that same rational function,
cross multiplication gives a nonzero polynomial of degree at most2r.
Consequently false acceptance has probability at most min(1,2r/|S|).
With k independent challenges against the SAME fixed commitment, the bound
is min(1,2r/|S|)^k. Responses may depend on challenges; uniqueness prevents
that dependence from changing the scalar being checked.

On the single global identity event, every later t>=0 query is correct,
including adaptively selected t values. There is no extra union bound over
those uses. New P,Q commitments, changed U or changed b need a new soundness
budget. Revealing challenges before commitment defeats the polynomial root
argument. Reusing a public fixed seed is not independent randomized checking.

The soundness bound concerns accepting a false committed function; it is not
a posterior probability of correctness conditional on acceptance. Repeated
new attempts until one passes can exhaust it. A service allowing adaptive
new commitments must assign per-attempt error allowances whose sum fits its
declared overall budget, using fresh challenges after each commitment.

Verifier cost is one U and one U^T application plus O(r) field operations
per challenge, after computing c and b^T b. Communication is O(r) field
elements per commitment and response. Future scalar evaluation takes O(r)
field operations. These are arithmetic counts: coefficient bit lengths,
exact arithmetic, random sampling, input reading, provider computation,
communication and rejection/fallback are additional costs. A local provider
can erase the verification saving; trusted Woodbury/Krylov preprocessing is
a strong comparator. Matrix access is stronger than the scalar-only receipt
service and must not be silently granted to just one side.

## Prior match and disposition

[Dumas, Kaltofen, Thome and Villard](https://arxiv.org/pdf/1602.00810),
Section4/Figure2, already commit a rational generating function, challenge
at a random resolvent point, verify a returned linear-system solution and
check its scalar projection. Their certificate also proves minimality.
The present positive-parameter response adapter drops minimality and uses
SPD to rule out singular challenges. The core verification mechanism is
directly anticipated. Retain this as an ordinary implementation option for
fallible model proposals, not as a new program contribution by itself.

## Why approximate checking is a separate problem

Exact polynomial root counting does not justify replacing equality by a
floating tolerance. For example, p_D(t)=(1-t)^D on[0,1] has supremum one,
but a uniform random T satisfies p_D(T)<=epsilon with probability
epsilon^(1/D). Thus k independent tolerance checks all pass with probability
epsilon^(k/D), despite a unit uniform error. For D=100, epsilon=10^(-3),
k=10, this is10^(-0.3)>1/2.

This example is a general polynomial-checking obstruction, not necessarily
a realizable difference of the restricted positive response functions.
Additional coefficient, positivity, smoothness or spectral premises can
help, but then their verification and precision costs are part of the
construction. The earlier partial Stieltjes receipt bands provide a direct
ordinary alternative. Do not use this exact algebraic adapter to claim a
cheap finite-precision uniform certificate without further analysis.
