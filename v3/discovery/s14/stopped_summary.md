# Lossy summaries need not finish an exact majority

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC.

Fix a block of T fair bits, an invoice cap H>=T+1, and an external distinct
padding coordinate. Read the block in a fixed order. Stop at a bounded
stopping time 1<=tau<=T that is invariant under complementing all answers.
Write S_t for the signed sum of the first t answers. Choose sign b=sign(S_tau),
with a complement-equivariant tie rule, and pad once iff tau has the wrong
parity to encode b. The count reveals b, and the public estimate assigns b
to ALL T coordinates. Let h=E|S_tau| and q=E[tau]. Then

    expected queries = q+1/2;
    expected Hamming error = (T-h)/2;
    one-episode fee = q+1/2+f.                            (1)

Proof: complement pairs require exactly one padding query. The unobserved
future signed increments have conditional mean zero at tau, so the expected
correlation of b with the final block sum is E[b*S_tau]=h. Stopping need
not certify the final block majority. This is an intentional lossy task.
No new result is claimed for ordinary optimal stopping or random-walk exits.

## Exact finite policy design in this restricted class

To minimize fee per unit of Hamming improvement, minimize (q+f+1/2)/h.
For a proposed ratio r, let

    V_T(s)=r*|s|;
    V_t(s)=max(r*|s|, -1+(V_{t+1}(s-1)+V_{t+1}(s+1))/2).

Force the first read. The best value of r*h-q is -1+V_1(1).
The optimal ratio is the unique zero of

    -1+V_1(1) - f - 1/2.

A policy maximizing the expression at r supplies its exact q,h, and the
ordinary fractional-programming update r<-(q+f+1/2)/h decreases r from
any feasible starting ratio until optimality. A finite policy set and exact
arithmetic give finite termination when each step strictly improves.
Time and signed count are sufficient statistics because future answers are
iid; the Bellman induction also covers history-dependent stopping in this
homogeneous-reconstruction class. It does not optimize arbitrary transcript
decoders, multiple episodes or adaptive block layouts.

For integer rational r=a/b, store b*V_t(s)*2^(T-t) as integers. Both the
stop and continuation comparisons are then exact. Forward propagation of
prefix counts gives exact q,h without sampling. This is a cheap development
screen, not an independent theorem reconstruction or CPU saving claim.

## Fair comparison

At this estimator's actual error, every affine-terminal-cell invoice
strategy pays at least h*(1+f/log2(H)). The candidate's ratio can be compared
with that coefficient. Identical ordinary stopping and count coding tie.
Comparing two constructions at differing h requires reporting fee per unit
improvement, or time-sharing with free public randomization to equalize
their aggregate error. Raw per-block bills alone are not a fair comparison.

As T grows, an unclipped exit at +/-a has q=a^2 and h=a, giving ratio
a+(f+1/2)/a. The nearest integer to sqrt(f+1/2) suggests a starting design,
but the exit is unbounded and DOES NOT obey a finite invoice cap. Only its
bounded Bellman version above is claimed implementable here.

The exact screen stopping_probe.json passes 795 tiny policy comparisons
and126 direct world checks. At H=256,f=1000 the optimized policy uses
196.497088944 mean queries, has error fraction0.475321068951, and its
fee/improvement ratio is2.519162755% below the early exact-majority policy.
At that actual error its fee is24.552547467% below the ALL-affine lower
bound. The former comparison can be made at equal error by mixing the
stronger-accuracy majority policy with zero-information output. At f=100,
the optimized policy still fails to beat the affine lower bound. These are
exact finite tariff calculations (displayed as decimals), not empirical
runtime or transfer results; the high-error limitation remains.
