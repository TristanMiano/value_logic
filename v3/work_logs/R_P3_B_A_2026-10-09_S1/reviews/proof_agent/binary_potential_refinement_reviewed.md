# Binary-loss potential refinement: prospective stronger calculation

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
Task R-P3-B-A; principal D/X work. No source or experimental policy changes.

## Why revisit the bound

The admitted uniform service has exactly binary expert losses, not arbitrary
fractional losses. The current proof bounds log(1−eta X) by −eta X−eta²X².
For binary X, its lower-potential contribution is exactly X log(1−eta).
Exploit that identity to tighten the guarantee of the **existing** executed
eta=1/K implementation, with no new randomness, rerun or source version.
This is a standard potential refinement, not a new learning algorithm.
The initial independent block review already records its unrounded alternative
in section 2. This follow-up integrates that alternative into the fixed-state,
source-known and numerical certificates; it does not claim a new discovery
of the potential argument. For nonbinary losses in [0,1], the same coefficient
also follows from the concave-log chord inequality, while the implemented
binary case has equality in the comparator's log term.

## Proposed exact coefficient

For 0<eta<1 and binary selected losses,
S_mix <= log N/eta + [-log(1−eta)/eta] S_i.
With floor-plus-one normalization, add
m log(1/(1−2^(−s)))/eta; the same one-sided logarithmic argument applies.
Uniform block averaging therefore gives

E L_terminal <= [(B−1)/B] [-log(1−eta)/eta] L*
 +(B−1)log N/eta
 +(B−1)m log(1/(1−2^(−s)))/eta +(T−m)2^(−h).

For the executed eta=1/K, the coefficient becomes
alpha_exact=((B−1)/B)*K*log(K/(K−1)), strictly below the conservative
coefficient ((B−1)/B)*(1+1/K). Its logarithm can have a rigorously enclosed
rational upper bound from the positive atanh series with z=1/(2K−1).
No mathematical label is used to compute that coefficient.

## Separate unexecuted learning-rate candidate

The same exact binary argument permits eta>1/2 when eta<1; only the old
quadratic lower-log bound required eta<=1/2. Since
−log(1−eta) <= eta + eta²/[2(1−eta)], choosing eta=2/(B+1)
gives alpha<=1 for every B>=2. Integer multipliers are (B+1)−2X and the
logarithmic terminal allowance is (B²−1)log N/2. Fixed-state error is at most
(B²−1)m/[2(2^s−1)]. This can improve the conservative B>=4 allowance;
for B=2 the old first-order coefficient can still be preferable when L*>0.
No policy is chosen after inspecting the tapes. This candidate remains a
mathematical parameter option, with no measured cost or performance claim.
A new implementation or run would need its own source-bound admission and
prospective selection, not relabeling the existing evidence.

## Planned finite calculation

First request independent reconstruction of the exact coefficient and the
candidate rational rate. Then enclose log N and log(K/(K−1)) by rational
atanh sums, verify the coefficient inequalities for admitted power-of-two B,
and compute tighter retrospective and source-known caps for the existing
20 uniform traces. Preserve all original certificates and add a separate
refinement record. This calculation changes no observed loss, invoice or seed.

## General bounded-loss rational rate (derived before calculation)

The same rational-rate candidate does not actually require selected Z to be
binary. For 0<=u<=eta<1,
−log(1−u)<=u+u²/[2(1−eta)], by the positive power series and 1/n<=1/2
for n>=2. Applying this to eta Z gives
S_Z <= S_Zi+log N/eta + eta/[2(1−eta)]*sum Z_i².
For X=HZ with the remaining-action propensity estimator, the conditional
coefficient of each binary comparator loss is bounded by
1−pi + eta/[2H(1−eta)]*(1−pi)²/pi.
It is <=1 if eta H/[2(1−eta)]<=1, so eta=2/(H+2) suffices.
The resulting allowance is H(H+2)log N/2 plus
H(H+2)m/[2(2^s−1)] and the same action rounding. Uniform H=B−1 recovers
(B²−1)log N/2. This rate is a mathematical candidate, not the executed rule.

For the adaptive ticket selector H=2B−1, favored-loss gamma becomes
2(B−1)/[(B+1)H(H+2)]; other gamma is 2/(H+2). A corresponding exact
integer denominator (B+1)H(H+2) may require 33 bits at B=1024, unlike the
executed extension's <2^32 denominator. Any future implementation must
rederive its own capacities and pay the actual arithmetic; the existing
source-bound cost evidence cannot be relabeled as this rate.

## General probability-floor rate option (mathematical, unexecuted)

A direct scalar bound extends the candidate rate to the adaptive proof.
For 0<=u<=eta<1,
−log(1−u) <= u+u²/[2(1−eta)],
because every coefficient 1/j for j>=2 is at most 1/2. Applying this to
u=eta*Z_i, with X=HZ, gives
S_X_mix <= S_X_i + H log N/eta
 + eta/[2H(1−eta)] sum X_i².
The comparator's conditional coefficient is
1−pi + eta(1−pi)²/[2H(1−eta)pi].
It is at most one whenever eta*H <=2(1−eta), so eta=2/(H+2) is sufficient.
The regret allowance is H(H+2)log N/2; fixed-state error is at most
H(H+2)m/[2(2^s−1)]. For uniform H=B−1 this recovers (B²−1)log N/2.

For tickets with H=2B−1, nonfavorite gamma is 2/(2B+1), and favorite gamma
is 2(B−1)/[(B+1)(2B−1)(2B+1)]. A straightforward common denominator
can exceed 2^32 at B=1024, so the old maximum-denominator bound must not be
reused. No source, allocation run, price or rate was changed to claim this
mathematical possibility as an experimental improvement.
