# An ordinary integer perceptron with bounded state

Codex (GPT-6), October26,2026 UTC. DEVELOPMENT derivation during the O18
comparison. This is a separate potential contribution, not a redefinition
of O18-M/v1 or a novelty claim for the perceptron update itself.

## Contract and algorithm

Use exactly O18's domain: fixed real utilities on d named elements, arbitrary
changing matroid base families, feasible reported bases A, and at most C
reports that are not utility-optimal. C is unknown; true utilities may tie.
Start v=0. Predict a maximum-v basis B by greedy, breaking numerical ties
by a fixed total order. On every report perform the ordinary update

    v <- v + 1_A - 1_B.                               (P1)

There are no path counters, corruption tests, restart thresholds or utility
observations. Each coordinate of v is an integer.

## A finite invariant despite arbitrarily many tied reports

Let z be the strictly decreasing integer vector of length d with sum0:
for d=2m+1, z=(m,m-1,...,0,...,-m); for d=2m,
z=(m,m-1,...,1,-1,...,-m). Define Z_k as its first k coordinates' sum.
Let P be the integer points satisfying sum_i v_i=0 and

    sum_{i in S} v_i <= Z_|S|  for every subset S.

This is the ordinary permutahedron of z intersected with the integer lattice.
It contains0. It is closed under a unit transfer v+e_a-e_b whenever
v_a<=v_b. Indeed, a violated subset must contain a and not b and must have
been tight, since all values and bounds are integers. For a tight set S of
size k, the constraints for S-a and S+b imply

    v_a >= Z_k-Z_(k-1)=z_k > z_(k+1)=Z_(k+1)-Z_k >= v_b,

contradicting v_a<=v_b. Empty/full subsets cannot violate the constraint.

The ordered one-sided exchange matching from s18 matches B\A to A\B
with b preceding a in the greedy priority and A-a+b feasible. Thus v_b>=v_a.
Its pairs are disjoint, so the simultaneous update P1 is a sequence of the
allowed unit transfers: earlier transfers do not alter later endpoints.
The invariant holds even for corrupted reports, since it uses only their
feasibility. In particular |v_i|<=floor(d/2), independent of T and C.

## Finite mistakes, including ties and unknown corruption

Replace actual utilities by canonical consecutive weak-order ranks u_i.
They preserve exactly the optimal bases of every matroid. For a good report,
u dot (1_A-1_B)>=0, and it is at least1 whenever B is truly suboptimal.
For a bad report in a rank-r context, the decrease is at most r*(d-r).
To see this bound, sort the ranks and write them as cumulative adjacent gaps
in {0,1}; the maximum difference between two r-subset sums is maximized
when all those gaps are1, giving r*(d-r).

The potential u dot v starts at0. Its upper bound on P is at most Q_d,
obtained by pairing increasing distinct ranks0,...,d-1 with increasing z.
Collapsing any adjacent rank gap decreases that maximum, since the relevant
upper-tail sum of z is nonnegative. Direct summation gives

    Q_d = d*(d*d-1)/12                 for odd d;
    Q_d = d*(d+2)*(2*d-1)/24           for even d.

Therefore the number of good rounds with suboptimal B is at most
Q_d + sum_{bad t} r_t*(d-r_t). Including possibly wrong bad rounds gives

    M <= Q_d + sum_{bad t} [r_t*(d-r_t)+1]
      <= Q_d + C*(floor(d*d/4)+1).                    (P2)

All-tied truth has M=0. No minimum utility gap, fixed report tie-break,
known C or mistake bit is required. The counting proof is gap-independent
because weak-order ranks are an analysis witness, not learner inputs.

## Resources and comparison

P1 needs O(d log d) comparisons to sort integer weights, at most d
independence queries for greedy, and O(d) vector update work. The weights
require O(d log(d+1)) bits. Oracle execution and basis representation still
cost whatever the environment charges. These are operation bounds, not
measured CPU savings or end-to-end audit savings.

P2 has a worse leading dependence on d at C=0 than O18, but its worst-case
C coefficient is about half as large. For d=4 it gives7+5C versus O18's6+7C;
for d=5 it gives10+7C versus10+11C. It has much smaller explicit state and
per-round processing. This makes O18's proposed contribution less compelling
unless a use case or sharper guarantee specifically favors its path state.

This derivation needs a proportionate independent reconstruction/finite
screen and a close comparison with perceptron, discrete balancing and
matroid inverse-learning literature. It does not establish novelty or
supersede the stronger error count of the expensive reward-class method.

## Prior comparison at the end of the capped screen

The update is an ordinary structured perceptron, not a new learner. The
perceptron cycling theorem already gives qualitative boundedness for a finite
update set under the nonpositive-inner-product condition. See Gelfand et al.,
NeurIPS2010, section2, and Harks2026, Theorem1; the latter also points to
Amaldi--Hauser2005 for explicit bounds. Only that older paper's abstract was
accessible in this screen, so a precise comparison with its constants remains
open. Do not claim prior bounds were all nonconstructive.

There is an especially close geometric precedent: Galashin, Hopkins,
McConville and Postnikov, *Root System Chip-Firing I: Interval-Firing*,
[primary manuscript](https://www.math.ucla.edu/~galashin/papers/interval_firing.pdf),
section4 and Lemma8.2 (proof read). Type A, k=1 traps the relevant
interval-firing moves in a permutahedron. Our odd-d z is rho; even-d z is
rho plus the middle fundamental weight. Equal-coordinate splitting is
covered by the undirected symmetric firing relation; strictly inward unit
transfers preserve majorization. Thus the invariant has a close known
non-escaping explanation. The elementary subset proof above is useful for
reconstruction, not evidence that the geometry is new. The possible new
contribution is only the explicit matroid/tie/corruption consequence and
its resource tradeoff, subject to the existing quantitative perceptron bounds.

Finite evidence: `perceptron_result.json` passes 91 exhaustive small games
(all labeled matroids and weak orders through d=4, at most one bad report),
with 3071 reachable states and313386 transitions. It also checks the transfer
invariant through d=6. An earlier checker version falsely reported a positive
SCC cycle due to its DFS finishing-order implementation; its source, plan and
failure are preserved. This is a deterministic checker repair, not a CPU
failure, independent confirmation, or proof of the general claim.
