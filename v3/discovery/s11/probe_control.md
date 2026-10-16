# Informative probes and paid counterfactual flips

Codex (GPT-6), DEVELOPMENT. Candidate extension of S11L/M and the
[canonical policy-difference space](potential.md), not a new family count.

## A compact but nontrivial source

Let X be m binary signs with an arbitrary joint law. The terminal options cost
0 and sum_i w_i X_i. A paid flip changes one sign at a known nonnegative price
f_i. A paid probe reveals one of r specified original signs at price a_j.
The agent observes its own flips, so a probe of a flipped sign can be decoded
to the original sign. Prices do not depend on hidden signs. At most H purchased
operations are allowed. This is a declared finite counterfactual interface:
the validity of flips and observations is supplied, not inferred from natural
model agreement.

Let Z=(X_1,...,X_r). The following unnormalized values suffice:

```math
p_z=\Pr(Z=z),\qquad t_{zi}=\mathbb E[X_i\mathbf1\{Z=z\}]
\quad (i>r).
```

There are 2^r(m-r+1) stored entries, with one normalization identity. Queried
coordinates need no extra entries because their cell means are z_i p_z.
For any partially observed query assignment, summing compatible cells gives
its mass and every signed first moment. No joint information among the
unqueried signs is needed. Several models can disagree on those correlations
and still give exactly the same controller at this interface.

These are ordinary conditional moment tables, not a new probabilistic object.
Their useful role here is to connect direct value retention to the exact
counterfactual/computation contract and its representation lower bound.

## Postpone flips, then solve a small query problem

Because probe prices and original outcomes are unaffected by known flips, any
policy can postpone each flip until after its last probe. Removing pairs of
identical flips cannot increase cost. At a posterior with means mu_i and k
operations remaining, ending with action 1 has best expected cost

```math
\sum_i w_i\mu_i-
 \sum_{\text{largest }k\text{ positive }i}(2w_i\mu_i-f_i).
```

Compare this with zero for immediate action 0. Flips for a path ending with
action 0 are unnecessary. This supplies the exact stopping value G_k.
For a partial query assignment h, dynamic programming compares G_k with

```math
a_j+\sum_{o\in\{-1,1\}}\Pr(X_j=o\mid h)V_{k-1}(h,j=o)
```

for each unqueried j. Use unnormalized cell sums to avoid division on empty
branches. There are at most 3^r partial assignments and H+1 budget levels.
Terminal flip selection and relevant moment aggregation are charged work.
The method still becomes expensive as r grows; it is parameterized by the
number of permitted informative probes, not generally tractable reasoning.

Postponement argument: simulate the original policy's flip mask internally
without applying its flips. Decode each actual probe through this virtual mask
before feeding it to the simulated policy. The observed history therefore has
the same law. At the stopping leaf, apply only the odd-parity flips if terminal
action 1 was selected; use none for terminal action 0. The terminal loss matches
in the former case, while nonnegative flip charges and operation count cannot
increase. This simulation is a dominance proof, not the implementation used by
the compact planner. Once probes finish, minimizing the linear conditional
expectation chooses the largest positive flip savings directly.

## Candidate exact dimension for the all-horizon interface

For w_i=1, positive constant flip/probe costs and all coordinate flips, Walsh
characters give the canonical space explicitly. Flips isolate each character
in the terminal sum. Observing coordinate j multiplies a function by
(1+o X_j)/2, adding the symmetric-difference shift of its character index.
Thus the space consists exactly of characters whose support is either a subset
of the r queried coordinates, or that subset plus one unqueried coordinate.
It has dimension **2^r(m-r+1)**. Constant costs supply the empty character.
Independence of Walsh characters proves this is the minimal linear space of
all policy-cost differences, under the earlier branch-splicing theorem.

For odd m, a pointwise-minimum potential in the old signed-flip construction
contains every even character. With at least one coordinate observation its
local invariant closure becomes all 2^m characters; at r=0 its dimension is
2^(m-1)+m. This contrasts representation contracts, not the intrinsic difficulty
of planning: ordinary shaping followed by the same relative-value compression
gets the smaller space too. Complete transformed policy values can cancel to
at most one additional feature, as explained in potential.md.

For example, m=31 and r=3 gives 232 canonical feature functions instead of a
full 2,147,483,648-state distribution. This is presently a symbolic dimension
calculation, not an executed large-scale economic measurement. Feature
acquisition must itself be supported without enumerating that distribution.

## Limits and next discriminating step

Prove the postponement transformation carefully under an adaptive stopping
policy. It fails if a probe price or sensor law depends on a flip, or if observing
the actual flip charge reveals hidden information. Check the small controller
against an unrestricted finite POMDP action search. Produce the moment table
from a compact admitted source and count preparation, query and decision work.
Compare ordinary conditional-moment dynamic programming, which should tie,
as well as a full-joint implementation. A resource saving against avoidable
full enumeration is useful but is not superiority over the strongest ordinary
method or proof of moderate novelty by itself.

## Executed developmental result

[query_flip.py](query_flip.py) completed all twelve declared cases. The ten
small cases agree exactly with unrestricted interleaved query/flip planning
under both conditionally independent and common-uniform couplings: **20 exact
comparisons**. Those laws have the same supplied conditional values but can
disagree on the unqueried joint outcomes. Both large compact cases also ran:
m=31,r=3 uses **232 source entries**, and m=101,r=4 uses **1,568**. Full-joint
slot counts are conceptual comparisons only; no enormous allocation was run.
The identical ordinary conditional-moment controller matches value, chosen
plan and all counted work in every case.

These runs compute optimal expected cost under declared tariffs. They are not
new physical audit purchases or a learned-source evaluation. Acquisition costs
of the source values, source validity, unknown real-world tariffs and the cost
of searching over which r probes to permit remain outside the demonstrated
service. A full-joint comparison is weaker than the required strong ordinary
counterpart and does not establish a superiority claim.

Evidence: [first case](qf00.json), [remaining attempt ledger](qf01/attempts.jsonl),
[31-fact case](qf01/c10.json), [101-fact case](qf01/c11.json). All case hashes
bind the same executed source. No retry was needed in this controller panel.
