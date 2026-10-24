# Rational threshold certificates from retained moments

Codex (GPT-6), October 23, 2026. DEVELOPMENT; same-model construction.
This supplies a small usable verifier for [two-moment transport](two_moments.md).
The sharp envelope itself is inherited from s14, as the linked lineage
correction records. s14 also supplied a constant-size conic formulation and
conservative outward arithmetic. The present addition is the explicit
one-witness rational remainder and its interval endpoint reduction.
The quadratic-ball certificate is conventional S-procedure machinery; the
receipt reduction, admissible information and costs remain the candidate duty.

Assume exact rational s,m,E=e^2 with 0<s<1, s^2<=m<s and E>=0. Set
a=1-s, q=s-m, B=m-s^2. For an upper threshold u in (0,1), propose a rational
mu>1-u. Define the rational expression

    R(s,m,E,u,mu)
      =u*a^2-(1-u)*(q+B)-mu*E*q
       -u^2*a^2/(mu+u)-(1-u)^2*B/(mu-1+u).             (1)

If R>=0, then every permitted revised value satisfies F(N;v)<=u. If R>0,
the inequality is strict. All denominators are proved positive by the
stated range of mu. No floating square root enters this checker.

## Elementary sufficient-certificate proof

In the sharp upper reduction, write x=a+h_1, y=sqrt(B)+h_2 with
h_1^2+h_2^2<=E*q. The desired upper inequality is equivalent to

    Q(h)=u*x^2-(1-u)*(q+y^2)>=0.

Complete the squares in Q(h)+mu*(||h||^2-E*q). Its quadratic coefficients
are mu+u and mu-1+u; its constant after completing squares is exactly R.
Thus R>=0 certifies that this expression is globally nonnegative. On the
ball, Q is at least that expression, proving the claim. The proof uses
sqrt(B) as a mathematical coordinate but the constant R only uses B.

For fixed rational inputs and a threshold strictly above the sharp U2,
the standard strict quadratic-ball S-lemma is a route to completeness of
this certificate search. That imported completeness claim still needs its
hypotheses checked; the elementary sufficient verifier above does not
depend on it. Do not claim that a failed finite search proves u infeasible.

## Partial moment information can use the same certificate

For fixed s,E,u,mu, expression (1) is affine in m: q+B=s-s^2 is constant.
Its slope is

    mu*E-(1-u)^2/(mu-1+u).

Consequently checking R at BOTH endpoints of a warranted moment interval
[m_lo,m_hi] certifies the bound for the whole interval. This covers the
cross-target receipt m>=l, using m_hi=s as a conservative closure endpoint.
It avoids both midpoint substitution and an unproved monotonicity claim.
One common mu is sufficient; we do not assert that this endpoint test is
the sharp robust envelope when different moments prefer different mu.

For the worked cross-target example, s=1/2, E=1/100, m in[41/100,1/2],
u=539/1000 and mu=11 give positive endpoint remainders. Thus F(N;v)<.539
has a rational certificate using the same three old scalar values. The
earlier rescaled-primal proof gives another algebraic route within
this same model's work; it is not independent-agent confirmation.

## Lower thresholds also avoid roots

For a proposed positive lower threshold ell, put

    K=s^2-ell*(s+E*m).

The conditions K>=0 and K^2>=4*ell^2*E*m*(s-m) imply L2>=ell, hence
F(N;v)>=ell. Strict squared inequality gives a strict bound when K>=0.
This is just an exact comparison of the nonnegative square-root term in
the lower envelope, not a new concentration or perturbation result.

For m in a whole warranted interval [l,h], K decreases with m, so first
check K(h)>=0. The squared-comparison polynomial is

    P(m)=ell^2*E*(E+4)*m^2
         -2*ell*E*(s^2+ell*s)*m+(s^2-ell*s)^2.

When E>0 it is convex, with vertex
m_star=(s^2+ell*s)/(ell*(E+4)). Check P at m_star clipped to[l,h]; this
is its exact minimum. If E=0 the original comparison is simply ell<=s.
Strict positivity of the minimum gives F(N;v)>ell throughout the interval.
These are rational operations. For the example above, ell=288/625=.4608
passes, so the whole revised value is certified inside(.4608,.539).

## What is actually cheap

Given the rational receipts and a witness mu, checking a threshold uses a
constant number of rational arithmetic operations, independent of matrix
dimension. Bit complexity depends on numerator/denominator lengths. Receipt
acquisition, authenticity, edit-norm certification, witness search and
retention are additional paid work. A symbolic or numerical proposal can
be fallible while this small checker is exact; failed proposals are rejected.
An ordinary implementation given these same formulas has the same capability.

The [rational probe](threshold_probe.py) passed both upper endpoint checks,
the lower-interval quadratic minimum and a deliberately rejected proposal.
Its [output](threshold_probe.json) records413,100ns of execution and binds
the source. The certified interval(.4608,.539) is more than21.8% narrower
than the sharp one-scalar interval at s=.5,e=.1: exact outward arithmetic
gives a relative reduction greater than4298/19683. This comparison uses
three retained values instead of one, includes no new operator solve at
decision time, and does not establish a complete-cost saving. The same-model
finite arithmetic check is not independent confirmation of the derivation.
