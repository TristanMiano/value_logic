# One common dependence model for the entire stopped invoice

Codex (GPT-6), October 15, 2026. DEVELOPMENT derivation; S33 continuation.
This is a distinct branch from relative-value compression. It addresses a
specific looseness retained by the previous session's prefix survival bounds.

## Duty and source

Fix an order of n paid observations. Score X_i is an integer in {0,...,K},
with a supplied marginal distribution p_i(x); dependence is unrestricted.
Stop purchasing after accumulated score reaches Q. Observation i costs c_i
when reached. After n unsuccessful observations, purchase a fallback costing C.
All prices are fixed and nonnegative. The invoice is

```math
B(X)=\sum_{i=1}^n c_i\,1\{S_{i-1}<Q\}+C\,1\{S_n<Q\},
\qquad S_i=\min\{Q,X_1+\cdots+X_i\}.
```

The target is max E[B] over ONE joint distribution with all given marginals.
Adding separate worst-case survival probabilities is valid but can be loose.
The source includes scores that would remain unobserved after early stopping;
this is a marginal-law assumption, not free physical acquisition of those scores.

## Compact flow and attainment

Let f_i(s,x) be the joint mass of S_{i-1}=s and X_i=x, with deterministic
transition T(s,x)=min(Q,s+x). Let d_i(s) be state mass after i observations.
Use nonnegative variables with

```math
d_0(s)=1\{s=0\},\qquad \sum_x f_i(s,x)=d_{i-1}(s),
```
```math
d_i(t)=\sum_{s,x:T(s,x)=t}f_i(s,x),\qquad
\sum_s f_i(s,x)=p_i(x).
```

Maximize sum_i c_i sum_{s<Q,x} f_i(s,x) + C sum_{s<Q} d_n(s).
There are O(n Q K) arcs rather than (K+1)^n full trajectories. Saturated
state Q still has outgoing score-labelled arcs: deleting these would discard
the prescribed marginals of scores after stopping and could invalidate the LP.

Every full joint law induces a feasible flow with the same bill. Conversely,
at any positive-mass state draw X_i with probabilities f_i(s,x)/d_{i-1}(s)
and advance deterministically. Choose anything at zero-mass states. Induction
recovers every state/arc mass and each original marginal. The resulting joint
law attains the LP objective. Markovization preserves this fixed additive
invoice and these single-coordinate marginals; it does not claim that the
unknown actual source is Markov or that arbitrary history-dependent objectives
can use the same state.

Thus a feasible primal flow supplies an attainable lower bound, and a matching
dual supplies an exact worst bill. Heterogeneous marginals need no common-law
weakening. More general finite-state controllers with a fixed observation order
admit the same construction if their complete relevant state is supplied.
Adaptive choices of WHICH coordinate to query generally need a larger state
that tracks identity; unrestricted reuse of a small scalar state is invalid.

## A small, independently checkable upper certificate

Provide rational marginal prices lambda_i(x) and state potentials h_i(s), with
terminal h_n(s) >= C 1{s<Q}, and for every reachable arc,

```math
h_{i-1}(s)+\lambda_i(x)\ge c_i1\{s<Q\}+h_i(T(s,x)).
```

Sum along any trajectory and then take expectations. The bill is at most

```math
h_0(0)+\sum_{i,x}p_i(x)\lambda_i(x).
```

This checks O(n Q K) local inequalities. A numerical solver can propose the
lambda values without being trusted: round them to declared rationals, set the
terminal h exactly, then compute the preceding h by backward maxima. This
repairs any dual infeasibility and yields a valid bound, possibly weaker than
the floating-point optimum. A rational feasible flow with the same objective
would establish exactness. Do not round a primal residual away or claim an
unverified floating-point optimum is a certificate.

## Conservative learning without discarding heterogeneity

Suppose a valid past-history event supplies lower tails L_i(j) <= Pr(X_i>=j).
Make these tails monotone by replacing L_i(j) with max_{k>=j} L_i(k), keeping
them in [0,1]. They define a minimal discrete law G_i dominated by the actual
marginal. Conditional coordinatewise couplings produce Y_i<=X_i with marginal
G_i under any actual dependence. Since B is coordinatewise nonincreasing,
E[B(X)]<=E[B(Y)]<=max_{Y_i~G_i} E[B(Y)]. Apply the flow to these individual laws.
There is no need to replace all of them by the weakest shared law. The existing
predictable first-purchase calibration restriction still matters; adaptively
selected within-request scores are not automatically unbiased samples.

This is a construction to screen, not a learned-service cost result. Choosing
an order or truncation from past data is permitted by a simultaneous valid
source; solving many flows, storing/checking certificates and acquiring the
source all cost resources. A useful policy must repay those costs.

## Closest literature and proposed cheap screen

Padmanabhan, Ahipasaoglu, Ramachandra and Natarajan, *Extremal Probability
Bounds in Combinatorial Optimization*, arXiv:2109.01591v1, section 2.2,
Corollary 2.2, gives a compact partial-sum flow and an attaining conditional
construction for a single sum tail. Section 2.2.2 handles weighted functions
of the final sum. The present use of intermediate-state invoice costs and
absorbing thresholds is a direct adaptation of that machinery. Do not describe
compact marginal coupling or its extremal-law construction as newly invented.
The proposed local delta is an exact stopped-invoice certificate, with the
heterogeneous learned-source interface and explicit checking/planning costs.

Screen prospectively: compare flow and full-trajectory LP on short sources,
retain rational primal and repaired dual values, and seek a strict gap against
the sum of separately sharp prefix bounds. Start with n<=6, K=2, varied rational
marginals and fees; use larger n only after the formulation passes. A positive
gap is informative about the earlier bound, not proof of novelty or economic
advantage over an ordinary flow implementation.

## First exact and numerical evidence

`invoice_flow.py` SHA256
`b1abe608032930b6709a3ef6bb0ce336795599c7eafbcad681977593f49fdd5c`
implements the formulation. The twelve prospective small cases all match a
full-trajectory LP through an exactly feasible rational witness and matching
repaired dual; no numerical tolerance substitutes for those equalities.
Eleven have a strictly smaller invoice bound than the sum of separately sharp
prefix bounds. For example, case 7 has n=6, Q=3, heterogeneous marginals:
the bound falls from 1483/104 to 1523/117 (difference 1163/936, about 8.71%).
Its compact LP has 60 arc variables versus 729 full trajectories. These are
size/bound improvements against named representations, not service savings.

A 24-coordinate case has 912 variables and exact bound 1204/17. An
80-coordinate case has 3,648 variables, but its proposed rational primal fails
the marginal/flow equalities in three unchanged attempts. The retained repaired
dual is nevertheless exactly valid, with bound 183037861351/1745944200, about
104.836, against fallback fee 157. `flow_failure.py` checks all 3,648 arcs from
the retained log without solving again. For this instance report a valid upper
bound only; the near-equal floating-point optimum does not prove sharpness.
An ordinary implementation of the same coupling LP has the same bound.

### A transparent incompatibility example

Case 0 has three identical score laws (3/8,3/8,1/4), Q=2, fees (1,3,1),
and fallback fee 5. The sharp failure probabilities after one and two scores
are both 3/4, while the sharp three-score failure probability is 9/16.
If the first two failure events both have mass 3/4, monotonicity forces them
to agree almost surely. The first two scores must then have probabilities
3/8 on (0,1), 3/8 on (1,0), and 1/4 on (2,2). Remaining failure requires the
third score to be zero, whose mass is only 3/8. Hence the separately sharp
9/16 final failure cannot coexist with both earlier optima.

The exact joint optimum instead uses probability 3/16 on each of (0,0,1),
(0,1,0), (1,0,0), (1,1,1), and probability 1/4 on (2,2,2). It has first,
second and third failure probabilities 3/4, 9/16, 9/16. Its invoice is
1+3(3/4)+1(9/16)+5(9/16)=53/8. The independently summed bound is 109/16.
The checked dual proves the exhibited law is optimal. The example shows why
one common distribution matters even with identical marginals and a fixed order.
