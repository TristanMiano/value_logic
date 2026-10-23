# A simple five-query channel reaches the maximum weight scale

Codex (GPT-6), October23,2026. DEVELOPMENT; extends zero_summary.md.

The full flow LP numerically returned a=1/7 but its independently rounded
primal was not exact. weight_channel_raw.json and the failed stderr are
retained. The following explicit construction replaces reliance on that
unverified numerical policy. It is a new declared derivation and screen,
not an unchanged retry or a claim of hardware instability.

## Rule

Label the seven raw coordinates by nonzero three-bit vectors1,...,7.
Privately choose an unordered pair O of omitted coordinates uniformly from
the21 pairs and query the other five, M. Let w be their number of ones.

- If w<=1, reject. If w>=4, accept.
- If w=2, let t be the XOR of the labels of the two observed ones.
  Accept with probability3/4 if t is in O, otherwise accept surely.
- If w=3, let t be the XOR of the labels of the two observed zeros.
  Accept with probability1/4 if t is in O, otherwise reject surely.

Pad acceptance to count5 and rejection to count6. The extra queried
coordinate is distinct and its value ignored. Only the count is public.

## Exact probability identity

For every raw input x,

    P[accept|x]=weight(Q(x))/7.                        (1)

An elementary orbit count proves this. Weights0 and1 always reject.
Complementing every bit complements acceptance, and Q commutes with
complement because1111111 is a codeword, so only weights2 and3 remain.

For a weight-two x, ten omitted pairs avoid both ones. Four give the
ordinary two-one branch, two another ordinary branch, and four the3/4
branch: weighted accept count4+2+4*(3/4)=9 of21. The other11 pairs give
at most one observed one. Q(x) has weight3.

For a weight-three codeword (a Fano line), three omitted pairs leave one
one;12 leave two ones whose XOR is an omitted label; six leave three ones
whose two observed zero labels do not trigger acceptance. Total9 of21.

For a weight-three noncodeword, the12 pairs omitting one one and one zero
contribute9+3*(3/4)=45/4. Among six pairs omitting only zeros, three trigger
the1/4 branch and three reject. Total12 of21. Q(x) has weight4.
This establishes(1), including all complements, without a floating policy.

The scale1/7 is the largest possible for a channel of the form
a*weight(Q(x)), since at the all-ones codeword probabilities cannot exceed1.
This does not optimize all pure channels or whole decoder schedules.

## Exact-decoding resource consequence

Insert(1) into the candidate-elimination procedure in zero_summary.md.
Each wrong codeword is eliminated on a visit with probability3/7,4/7 or1,
according to its distance from the true center. All15 wrong centers are
eventually removed almost surely; the true center is never removed.
The previous geometric bound becomes

    E[episodes] <= 2*7*(7/3+7/4+1/7) = 355/6.

There are exactly15 acceptances on completion, so total raw queries equal
6*episodes-15. Hence expected queries are at most340, and the tariff bound
including reset fee f is (6+f)*355/6-15. Construction, public candidate
updates and random-bit costs remain outside that inherited tariff.

The literal-mixture predecessor gave the looser bound4615/6 episodes.
The13-fold improvement here is in a proved upper bound and in each wrong
candidate's elimination probability, not an observed runtime ratio.
The cap7 deterministic decoder remains a much cheaper available control
when that cap and its stronger per-tape privacy contract are permitted.

After r full rounds, the probability of not yet finishing is at most
7*(4/7)^r+7*(3/7)^r for r>=1. A bounded-round service may abstain; it cannot
return an incorrect codeword. The next finite screen will check(1), exact
round thresholds, and a sharper conservative expected-round calculation.

The exact screen passed128 inputs with21 omitted pairs and four private
coin outcomes, plus2048 translated-channel checks. Summing40 terms of the
maximum-geometric tail and bounding its remainder gives conservative
expected-episode upper35.091542562 and expected-query upper195.549255371.
The omitted tail is less than1.78e-9 rounds. Twelve full rounds suffice for
completion probability above99%; cap the service at192 episodes and abstain
if unfinished. These are analytic resource bounds, not observed timings.
