# Shared costs can require a non-nominal repair

**DEVELOPMENT derivation — Codex (GPT-6), October 14, 2026 UTC.**

One unknown cost z lies in [0,5]. Two observed neighbors have costs (2,3),
and their incident edge weights are (5,2). Each edge has two independent
exactly-one components. Count k_i in {0,1,2} says how many components choose
the known neighbor. With the original pair constraints, the exact endpoint
regrets and absolute upper cost are

```math
R_L=10k_1+6k_2,\qquad R_U=38-15k_1-4k_2,
\qquad R=\max(R_L,R_U),\qquad U=32+R_U.
```

The complete menu of actions optimal at **some** z in the entire interval
has counts (0,0), (1,0), (2,0), (2,1), (2,2), including all tied counts at
z=2 and z=3. Its best regret is 20, attained by (2,0). The full action set
contains (1,1), with endpoint regrets (16,19), hence uniform regret 19.
It is never nominally optimal: splitting both pairs would require z=2 and
z=3 simultaneously. A tolerance of 19 separates the two menus before any
query of z. This is a deterministic action guarantee. A randomized mixture
with a small expected regret does not establish that bound for each realized
action, which is the service duty used here.

This is **not new robust-optimization methodology**. Kasperski and Zielinski,
*Robust discrete optimization under discrete and interval uncertainty: a survey*,
section 2.2.2, pages 11–12, distinguish independent Cartesian item intervals
from correlated/discrete scenarios. Their possibly-optimal property for the
former does not apply to our single shared parameter. The affine scenario
curve imposes equality/correlation between several feature costs. See the
[author-hosted survey](https://ki.pwr.edu.pl/zielinski/publications/papers/survey16.pdf).

More directly, the repository's [s07 proposer](../s07/robust_witness.py) already
searches feasible actions against admitted scenario-anchor lower bounds and
absolute upper costs. Its MIP epigraph does not restrict proposals to nominal
optima. The example therefore diagnoses a restricted baseline; it does not
establish an advantage against the strongest existing ordinary controller.
Any new cheap structured proposer must also be supplied to that controller.

## Cheap structured proposal

For a group with one unknown z in [L,H], known neighbors c_i in that interval,
and integral weights w_i, put a_i=w_i(c_i-L), b_i=w_i(H-c_i). A dynamic program
retains the smallest right-end regret y at each exact left-end regret x.
Initialize T_0(0)=0. For each edge and count k in {0,1,2}, transition

```math
T_i(x+k a_i)\ \leftarrow\
\min\{T_i(x+k a_i),\ T_{i-1}(x)+(2-k)b_i\}.
```

Keep a concrete count witness, breaking equal y ties lexicographically.
There are at most 2 sum a_i+1 states per row. At completion transform each
state into (R,U)=(max(x,y), 2 sum w_i c_i+y), and remove dominated pairs.
For fixed x, discarding a larger y is safe for both coordinates. The recurrence
therefore retains every nondominated attainable pair, though not every action.
This is a pseudopolynomial multiobjective knapsack calculation, not a
polynomial-in-input-bitlength algorithm.

If separate unknown vertices have independently varying compatible intervals
and all their neighbors are observed, their groups have disjoint unknown
coordinates. The worst regret and upper cost each add across groups. Convolve
the local nondominated menus: retain the minimum sum U for every exact sum R,
then remove dominated totals. This yields the minimum upper cost under a
global regret tolerance. Source correlation between different unknown groups
would invalidate this equality; a box relaxation remains an upper bound.

Only the returned concrete action and its endpoint bounds need admission for
service safety. Claiming frontier completeness needs the recurrence checked
as well. The planned finite screen records every table and independently
reconstructs transitions, plus exhaustive actions for small groups and products.
Wrong source, changed interval, and understated endpoint bounds must fail.

**Prospective gf01:** use the 20 already exposed sf02 general groups, the
(2,3)/(5,2) boundary, and 12 new seeded groups of degree 6–12 (seed 8141640).
Exhaustively compare all count actions through degree 7; for larger groups
check every DP transition and every returned witness endpoint. Convolve 12
pairs of groups of degree at most 3 and compare the complete action products.
There are no physical audits or confirmation claims in this screen.
