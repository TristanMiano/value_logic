# A priced menu of full-information prefix episodes

Codex (GPT-6), DEVELOPMENT, October22,2026. This construction extends the
ordinary prefix decoder to different leaf shapes; it is not yet an optimum
over arbitrary public/private adaptive protocols.

For cap H, choose a complete binary prefix tree. A leaf at depth d has
probability2^(-d) under fresh independent fair input bits. Assign each leaf
a distinct public count t in{1,...,H}, with t>=d. Privately read the d fresh
bits along that leaf, then query arbitrary distinct unused coordinates until
count t. Ignore the marker answers. Observing t reveals that entire prefix,
so all unprocessed bits remain independent fair bits. Ambient dimension at
least H makes distinct markers available, including already decoded bits.

For leaf depths d_i and assigned counts t_i, define

    D=sum_i 2^(-d_i)d_i, Q=sum_i 2^(-d_i)t_i.

The asymptotic fee per recovered bit is (Q+f)/D. For n at least the maximum
leaf depth, the exact expected fee recurrence is

    V_n=Q+f+sum_i 2^(-d_i)V_(n-d_i).

Use the cap-two one-bit decoder at the finitely many boundary n values.
Subtracting rho*n, rho=(Q+f)/D, makes the recurrence a convex average.
Hence V_n-rho*n lies between the smallest and largest boundary differences:
an explicit O_(H,f)(1) remainder. Markers do not alter the posterior because
their answers never affect the observable count or later retained state.

## Exhaust the small menu without an arbitrary tree search

A finite full binary tree with L leaves has maximum depth at most L-1.
Since counts are distinct, L<=H. Generate all depth multisets recursively
by merging two smaller full-tree multisets and increasing depths by1.
These finite profiles cover every tree in this declared class.

For a fixed profile sort d_1<=...<=d_L. An optimal count assignment is

    t_1=d_1, t_i=max(d_i,t_(i-1)+1).

If two counts are inverted relative to depths, swapping them is feasible
and does not increase cost: the shallower leaf has larger probability, and
the formerly smaller count was already large enough for the deeper leaf.
Thus a monotone assignment exists, and the greedy counts are coordinatewise
smallest among monotone feasible assignments. The profile is feasible iff
t_L<=H. This is a small exact construction using ordinary prefix coding and
scheduling; a novelty claim would need closer constrained-coding comparison.

Each feasible profile gives an affine function Q/D+f/D. Its lower envelope
is the best member of this menu for a given reset price. Equal D profiles
retain the smallest Q. An exact rational line-envelope computation can list
all price phases. Prospective screen: caps2 through12 only, retain exact
profiles, fees and transition prices, and verify the envelope independently
at every transition and interval midpoint. No larger all-policy harness.

The distinct-output requirement is substantive. A general invoice can merge
several private leaves at the same count and leave correlated residual worlds.
Those protocols may beat this menu. The cap-four failed potential already
shows why this possibility cannot be dismissed by simple extrapolation.

## Executed small menu and interpretation

The immutable prefix_menu.py/json screen passed 5,106 exact envelope
comparisons in 69,193,500 ns. It enumerated caps2 through12. Source SHA256:
8188840d805ea9841a6c5b7abf51e49c1b2670c0ac387b0398c5c8a637bc1fcd.
This verifies the finite arithmetic/menu calculation, not an all-policy claim.

At cap12 there are197 feasible profiles and five optimal price phases:

| Reset price at phase start | Mean bits D | Mean queries Q | Sorted leaf depths |
|---|---|---|---|
| 0 | 2047/1024 | 4095/2048 | 1,2,3,4,5,6,7,8,9,10,11,11 |
| 48593/14864 | 93/32 | 281/64 | 2,2,3,3,4,4,5,5,5,6,6 |
| 415/112 | 25/8 | 5 | 2,3,3,3,3,4,4,5,5,5,5 |
| 95/16 | 51/16 | 167/32 | 2,3,3,3,4,4,4,4,4,5,5 |
| 31/2 | 13/4 | 45/8 | 2,3,3,4,4,4,4,4,4,4,4 |

The first profile uses counts1 through12; each other profile uses2 through12.
At reset10 the leading fee falls from24575/4094 to487/102 per recovered bit,
a reduction256436/1253325 =20.460455...%. At reset100 it falls from208895/4094
to65/2, a reduction15168/41779 =36.305320...%. Both comparisons are against
the simple prefix strategy on full-vector recovery under this tariff. They
are not gains on the earlier parity task, measured CPU gains, or superiority
over the strongest ordinary coding method. Queries increase to reduce resets.
At reset10, for example, the new query rate is167/102 rather than4095/4094,
while episodes per bit fall to16/51 rather than1024/2047.

The closest-source screen found a particularly direct antecedent:
[Aviran, Siegel and Wolf, ISIT2006](https://cmrr-star.ucsd.edu/static/pubs/optimal_parsing_trees.pdf),
SectionsII-B and III-A/B. Their variable-length parsing construction optimizes
mean output cost divided by mean source length, with ordered assignments and
a finite search over parsing trees. Our extra feasibility condition is that
the observable count cannot precede the paid acquisitions: t_i>=d_i. Reset
price adds a common cost. Treat this as a causally constrained adaptation
of that ordinary construction, not a new coding principle. A nonredundant
contribution would need the acquisition constraint or arbitrary-policy bound
to do substantive work. This screen rejects a standalone novelty claim for
the menu or its percentages.
