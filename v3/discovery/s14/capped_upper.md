# Matching upper endpoint with an old-operator norm cap

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. Completes the one-value
plus norm-cap interval alongside capped_response.md.

Let l=1/(1+K^2)<=s<=1, ||M||<=K and ||N-M||<=e. For0<s<1 define

    a=(sqrt(e^2+4)+e)/2,
    m_max=(1+l)*s-l,
    m_opt=clamp(s/(1+a^2), s^2, m_max).

The exact upper endpoint is

    U_cap(s,K,e)=U_e(s,m_opt),                            (1)

where U_e is the convex scalar formula in two_scalar_upper.md. The cap
one and e=0 cases retain their immediate interpretations. This reduces
the extra norm premise to one selected worst-case old moment.

## Concavity argument

Every feasible old moment lies in[s^2,m_max], and its sharp U_e(s,m)
is attained with the minimum-norm rank-one old operator. Thus maximizing
U_e over this interval is necessary AND sufficient for the upper endpoint.

For fixed alpha>=0, expand its defining objective as

    1-(2*alpha-alpha^2)*(1-s) + alpha^2*e^2*(s-m)
      +2*alpha*e*sqrt(A*(s-m)),
    A=1-2*alpha*(1-s)+alpha^2*(1-2*s+m).

A and s-m are nonnegative affine functions of(s,m) on the moment domain.
Their geometric mean is concave. Therefore each fixed-alpha objective is
concave in(s,m), and its pointwise infimum U_e is concave too. For the
uncapped linear-upper regime s<=1/(1+a^2), the finite extremizer has
m=s/(1+a^2) and realizes the global upper maximum. Concavity implies
that clipping this maximizer to the feasible interval gives a maximizer
there. For larger s the scalar old operator, with m=s^2, already attains
the uncapped upper endpoint. This proves (1).

Equivalently, a cap changes the upper bound only when

    s < 1/(1+a^2) and
    s < (1+a^(-2))/(K^2+2+a^(-2)).

In that region the worst old moment is m_max, so the old rank-one
operator saturates its norm cap. Outside it, the uncapped endpoint is
attained within the cap. This is an exact information restriction, not
a claim that matrix perturbations commute or remain scalar.

## Partial value receipts

Both capped endpoints are nondecreasing in s. For the upper endpoint,
mix any old/new pair with a zero-operator row and mix the unit right-hand
side accordingly. Both values move toward one, preserving both norm
bounds. This raises old s to any larger feasible value without reducing
the achieved new value. For the lower endpoint, mix with the scalar pair
M=K, N=K+e. Its values are l and1/(1+(K+e)^2), and the latter is a
universal lower bound for every feasible new matrix. This lowers old s
to any smaller feasible value without increasing the new value.

Hence an old truthful interval[s_lo,s_hi] transports sharply to
[L_cap(s_lo,K,e), U_cap(s_hi,K,e)], after intersection with[l,1].
Increasing the allowed K can only widen the interval. An uncertain
norm receipt uses its certified upper endpoint. Outward arithmetic and
acquisition of the norm premise remain paid work.
