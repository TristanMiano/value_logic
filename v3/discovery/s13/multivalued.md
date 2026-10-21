# Multivalued facts: an exact cap-two coding adapter

Codex (GPT-6), s13 DEVELOPMENT. This extends the reduction in
[s12/cap_two.md](../s12/cap_two.md), not the coding literature itself.
Private episodes query at most two distinct coordinates, unit query fees,
reset fee f>=0, only their exact count is public, and private answers reset.
There are at least two physical coordinates, so a distinct marker exists.
Controller computation, source construction and coding preparation are unpaid
by this particular invoice contract and must be reported separately.

## Exact reduction and a product consequence

An informative episode first queries one coordinate i. Its answer selects
whether to stop at count1 or purchase a marker and stop at count2; the
marker's answer cannot affect either public outcome. Thus it asks a binary
subset question about x_i with answer prices 1+f and 2+f. Conversely every
such subset question is implementable. Place the extra query on the branch
with smaller probability when optimizing expected price. Free independent
randomization cannot improve the minimum: revealing its tape only makes
the decoder stronger, and averages cannot beat the best deterministic tape.

For one uniform q-valued coordinate, let C_1=0. Exact recovery is precisely
prefix coding of q equally likely symbols using letters of cost 1+f and 2+f.
An elementary (not fastest known) dynamic program is

```math
q C_q = q(1+f) + \min_{1\le a<q}
\{\min(a,q-a)+aC_a+(q-a)C_{q-a}\}.
```

Its straightforward cost is O(q^2) arithmetic operations, apart from bit
complexity. Known unequal-letter coding methods are stronger preparation
controls. For example C_2=3/2+f and C_3=(7+5f)/3. At q=3, put the singleton
on the expensive first answer and the pair on the cheap answer, then separate
the pair with another binary episode. The three query bills are 2,2,3;
episode counts are 1,2,2. At q=4, C_4=3+2f for f>=0; an unbalanced tree ties
at f=0 but has larger reset coefficient.

Suppose n coordinates are independent uniform q-valued variables and the
goal is their sum modulo q. Every public transcript leaves a Cartesian
product of coordinate subsets: each new episode only restricts one factor.
On any nonempty such product, the sum is constant only if every factor is a
singleton. Exact sum therefore requires full coordinate recovery. The optimal
expected total price is exactly n C_q. To see the lower bound without assuming
that coordinates are processed consecutively, use the sum of their optimal
remaining coding costs as a potential. A test of one factor obeys its Bellman
inequality; the other factors do not change. Telescoping proves the bound.
Separate optimal codes attain it. The same proof works for independent
nonuniform full-support coordinates, using each factor's own optimal code,
and for a target injective in every coordinate when the others are fixed.

The information restriction matters: an ordinary visible query recovers a
q-valued coordinate in one purchase. The ordinary same-interface coding
implementation exactly ties this adapter. No new coding algorithm, broad
ordinary superiority or complete-computation gain is claimed.

## Why a tempting larger-alphabet rate argument fails

For q=3, weight each within-coordinate K3 edge by1/2, giving incident
coordinate load1. A loose private-tree relaxation can count all three
cross-branch pairs when two of three branches continue. At cap2, the two
continuing branches both have invoice2, so their mutual edge is not removed.
The relaxation's apparent attainer is not an invoice attainer. In particular,
plugging the three-way split into the Boolean-style recurrence suggests a
5/3-per-coordinate rate; it does not establish an achievable rate. The exact
cap-two value is7/3 at f=0. Even a sharper one-episode edge bound need not
recover the coding cost. Do not generalize the binary optimal-rate theorem
by changing a split coefficient alone.

For a modest constructive higher-cap bound, privately acquire m fresh q-valued
coordinates and compute their sum. Encode that sum by buying j extra markers,
j=0,...,q-1. Count m+j identifies the sum. This uses cap H>=m+q-1 and has
mean query-plus-reset bill m+(q-1)/2+f under the uniform product source.
Enough distinct marker coordinates are required; H<=n suffices. It is merely
a block construction, not a higher-alphabet optimality theorem. Computation
of the modular sum is an additional cost. Changing H is an interface change,
not an improvement against a control that retains cap2.

## Literature and disposition

Golin and Rote (1998), introduction and the start of sectionII, explicitly
formulate prefix codes with unequal letter prices. Golin and Young,
*Prefix Codes: Equiprobable Words, Unequal Letter Costs*, introduction and
section2 through Lemma2.4, study precisely the equiprobable coding subproblem
and report algorithms faster than the elementary recurrence above. The
contribution here is the private-reset interface reduction and its product
target consequence; its conceptual distance from s12 is small. Keep as a
bounded adapter and early exclusion, not a new numbered family or an excuse
for a large benchmark. No numerical execution has been used for this note.
