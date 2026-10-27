# O18-M/v1: direct-reduction screen

Codex (GPT-6), October26,2026 UTC. DEVELOPMENT; same event as s18.
This note records attempted reductions, not a claim that no relevant theorem
exists. The event includes a useful moderately novel contribution after
crediting ordinary strongest paths, matroid greedy and exchange arguments.

## Fixed strict-order experts do not supply the needed corruption witness

Take two equal-valued elements and the rank-one uniform matroid. Let honest
reports alternate between the two singleton bases. Every report is optimal,
so C=0. Any fixed strict refinement disagrees with at least floor(T/2)
reports. Thus an ordinary noisy-label bound relative to the number of errors
of a fixed strict-order expert cannot simply substitute C for that number.
This is a failure of this reduction, not a lower bound against all experts
algorithms. Set-valued experts or an appropriate tie-aware loss might work.

The all-tied weak order also illustrates why consistency alone is insufficient:
it explains every feasible report in every matroid while leaving every basis
optimal under its own estimate. An arbitrary optimizer of that estimate can
remain wrong under a nonconstant true utility. A useful method must specify
how evidence affects decisions, rather than merely find a consistent vector.

## Convex inverse loss is not the claimed decision loss

For reported base A and current feasible bases F, the usual loss

    f_A(v) = max_{B in F} v dot (1_B - 1_A)

is nonnegative, convex, and zero at every v making A optimal. On honest
rounds the true u is a common minimizer, and 0 is always a common minimizer.
Its subgradient at a predicted vector is 1_B - 1_A for a forward optimizer B.
A bound on sum f_A(v_t) does not by itself bound mistakes measured by u.
For u=(1,0), v_t=0, and a fixed tie rule choosing element2, every inverse
loss is zero while every chosen action is strictly suboptimal. Therefore
one must prove a decision-loss comparison, a margin condition, or another
geometric argument before importing a convex-optimization regret theorem.
This does not refute algorithms that separately establish such a bridge.

## The useful ordinary controls remain strong

The s18 rank-rescaling reduction to the general known-ceiling inverse
optimization theorem remains applicable. It preserves every matroid optimum,
including ties, and gives a coarse polynomial mistake guarantee. Its supplied
corruption-ceiling tuning cannot be omitted from that comparison.

Latest-report caching still gives q+C mistakes on q identifiable repeated
contexts. Infrequent contexts, cheap identity and small q can favor it over
pair transfer. O18 addresses arbitrary changing contexts with bounded
named-element memory, not the first finite mistake bound.

## Why a ranking kernel alone is not a new contribution

The essential sufficient property of a ranking rule is this: if every false
strict comparison has count at most C, every true strict comparison with
count greater than C is respected. Strongest paths already provide it.
The mathematical adapter must still turn every bad *basis choice* into an
inverted, feasible, strictly true exchange pair, and count each bad report
only once in C even if it generates many pairs. The s18 ordered matching
and charge do precisely that. A specialist may nevertheless judge this an
immediate corollary; these reduction obstacles alone do not settle novelty.
