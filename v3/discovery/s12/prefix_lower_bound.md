# Attempt at a general expected invoice lower bound

Contributor: **Codex (GPT-6)**. DEVELOPMENT. This note distinguishes the proven
prefix construction from a prospective optimality argument.

With unit fees, cap three and zero reset/coin price, the prefix construction
on n fair independent bits costs

    F(n)=n+R_n=(7/6)*n+(2/9)*(1-(-1/2)^n).

The unrestricted oracle agrees for n=3,4. One new bounded n=5 attempt stopped
at its predeclared 60,000-state cap (60,001st state detected), after 23,724,074
program choices among 454 invoice maps, in 13.9335238 seconds. It is inconclusive;
the upper bound is 97/16. The frozen output's `result.cap` was overwritten by
the episode cap 3 when panel metadata was attached; the source and this note
preserve the actual 60,000-state stopping limit. No larger run is authorized
by this observation alone and no all-size optimality claim follows.

## Why two easy lower bounds do not close the question

Every correct parity execution must query every original coordinate somewhere;
otherwise flipping an unqueried bit preserves its transcript and changes the
answer. Thus expected cost is at least n. The hard-worst lower bound does not
automatically lower-bound its average. A fresh uniform private tree's output
entropy also does not settle repeated episodes, since their public receipts
can leave a correlated source. Parity recovery need not reveal the full vector.

## A prospective potential using all cubical faces

For a compatible set W of cube vertices, let f_j(W) count its contained
j-dimensional faces. A parity-monochromatic W has no positive-dimensional
faces. Define a candidate unnormalized lower bound

    P(W)=3*f_1(W)-2*f_2(W)+6*f_3(W)-18*f_4(W)+...,
    a_1=3, a_j=-2*(-3)^(j-2) for j>=2.

On a full n-cube, f_j=choose(n,j)*2^(n-j), and the binomial identity gives
P(W)/|W|=F(n). If for every private cap-three program with invoice cells W_c,

    P(W) <= sum_c c*|W_c| + sum_c P(W_c),

then induction on any terminating public protocol would give the desired
expected lower bound. The coefficients alternate: positivity and monotonicity
are not automatic, and a failure at one correlated source would invalidate
this proposed universal Bellman argument. The full-cube fit alone proves
nothing about those sources.

Prospective cheap check: enumerate all source subsets for n=3,4 against the
already frozen private-program enumerator, stopping on the first counterexample
for each size. This tests a proof route, not a new application benchmark.

The first [face_potential_probe.py](face_potential_probe.py) run completed in
6.3836294 seconds. All 20,952 three-bit checks passed. A four-bit counterexample
appeared after 14,632,490 checks: W={0,...,13}, P(W)=63 while the episode's
cost-plus-child-potential is 61. This rejects the potential over arbitrary
sources. It does not falsify the prefix construction or establish a better
full-cube protocol.

The counterexample is not a reachable cap-three source. The new
[transcript characterization](transcript_sources.md) shows that these sources
are exactly binary-CNF relations, whereas W excludes a minimally forbidden
three-bit pattern. A revised proof route would need the Bellman inequality
only on bijunctive sources. Enumerating that semantic class is justified by
this new restriction, rather than merely increasing the earlier oracle budget.

The frozen [reachable-source screen](reachable_probe.json) rejects that rescue.
It enumerates 166, 4,170 and 224,716 binary-CNF sources (including the empty
source) on three, four and five bits. The first two panels pass 12,504 and
844,428 Bellman comparisons. At five bits a reachable 18-world source has
P=83 but cost-plus-child-potential=81, after 93,752,110 comparisons. Its mask
is 4,144,959; the exact cells are retained in the output. The total run takes
46.1473438 seconds. The proposed cubical potential is now parked, including
its restriction to reachable sources. This still does not refute the prefix
upper bound or establish a better full-cube policy.

## A structurally bounded five-bit oracle extension

The later reachable-source count supplies a new finite state bound, so the
[prospective extension](prefix_complete_plan.md) permits one 225,000-state,
150-second-per-panel screen. The [saved result](prefix_complete.json) completes
both panels exactly: five-bit parity and full-vector recovery each cost
**97/16 = 6.0625**, matching the prefix construction. They visit 223,843 and
224,683 nonterminal states and 93,849,890 / 94,123,490 program choices.
Total runtime is 105.3616012 seconds, concurrent with the principal's separate
entropy-bound derivation; it adds no duplicate research-clock credit.

The wrapper's descriptive `prefix_mean` was mistyped as 95/16. This field never
enters its optimization; [the contemporaneous correction](prefix_complete_disposition.md)
records 97/16 and preserves executed bytes. This is a known metadata defect,
not stochastic hardware failure. All-size expected optimality remains open,
and the failed cubical potential remains rejected. No six-bit extension is
justified merely because this finite computation completed.
