# Fallible ordinal feedback when genuine ties are allowed

Codex (GPT-6), s18 DEVELOPMENT. A new bounded branch motivated by the tie
restriction in Oki and Sakaue's corruption result. This note is not a claim
of first publication; comparison with noisy preference learning is required.

## Contract

There are d alternatives with fixed unknown real utilities u_i, possibly
equal. A round supplies any nonempty available subset S. The learner returns
j in S and then receives an asserted best alternative i in S. At most C
rounds return a non-maximizer of the true utility on S. Neither C nor the
utility gaps are known. A true tie may be resolved arbitrarily on every round.
The feedback still names an available action; malformed feedback is separate.

Count a mistake when the chosen j is truly suboptimal. If per-round utility
range is at most M, multiplying the mistake bound by M bounds true regret.
This is a choice/recommendation interface, not an assumption that an unresolved
mathematical feasibility predicate can be queried for free.

## Why naive cycle contraction fails

With two alternatives u1>u2, a first false response2 followed by a truthful
response1 produces both comparison edges. Declaring their cycle to be a
genuine equality can permanently contract the two alternatives. A fixed
tie-break favoring2 then loses forever with only one corrupted round.
Conversely, real equal utilities can produce such a cycle without corruption.
Thus neither permanent contraction nor interpreting every cycle as a fault
is justified without an additional argument.

## Keep only the comparison against the proposed action

Maintain counts c_ab for asserted comparisons a>=b. Initially all are zero.
Choose a total ordering pi maximizing

    score(pi)=sum_(a ranked above b in pi) c_ab.

Return the highest-ranked available alternative j. Upon receiving i, add
one to c_ij if i differs from j. Store no other pair from that response.
This is an ordinary maximum-weight linear ordering (Kemeny-type) update.
An exact subset DP can select an ordering in O(d*2^d) work after subset
weight sums, or brute force suffices for a small development example.
This computational cost is material; no polynomial-time claim is made.

## Finite mistake bound, including unknown corruption and true ties

Let B be the final number of recorded strictly FALSE comparisons: those
a>=b with u_a<u_b. Only a corrupted response can create such a comparison,
and only one comparison is recorded per round, so B<=C. Comparisons within
a true tie group are neither classified false nor charged to B.

At any round, stably sort the chosen maximum-score ordering by decreasing
TRUE utility, preserving its relative order inside each true tie group.
This hypothetical ordering is used only in the proof. Its score cannot be
larger than the selected maximum. Sorting reverses exactly the strictly
misordered pairs. Consequently

    sum_(u_a>u_b, pi ranks b above a) (c_ab-c_ba) <= 0.

The sum of the c_ba on these pairs is at most B, and every c_ab is
nonnegative. Therefore each strictly misordered pair satisfies c_ab<=B
before this round's update.

On an uncorrupted round where j is suboptimal, the response i is truly
better than j, while pi ranks j above i because both were available. The
new comparison increments c_ij. Assign this mistaken round to pair{i,j}.
Each strictly ordered pair can receive at most B+1 such assignments over
the entire stream: after that many increments its count exceeds B and the
maximum-score ordering can never misorder it again. There are at most
binom(d,2) strictly ordered pairs. Corrupted rounds add at most C mistakes.
Thus, without knowing C or any gap,

    mistakes <= binom(d,2)*(C+1)+C,
    true cumulative regret <= M*[binom(d,2)*(C+1)+C].

The bound is independent of the horizon. The key is retaining only one
comparison per response; retaining all winner-versus-available comparisons
would allow up to C*(d-1) false edges and give a weaker immediate bound.
Arbitrarily many tie comparisons do not affect the argument because stable
sorting preserves their contribution exactly.

## Scope and strongest immediate comparison

For subset choice this is the rank-one matroid case of inverse optimization.
Oki and Sakaue (arXiv:2602.01682v2, Sections3--5 and AppendixD) give stronger
O((C+1)*d*log d) regret for general M-convex sets under distinct utility
components, and handle ties without corruption. Their corrupted theorem
explicitly uses distinctness. The present elementary construction trades
exponential ordering computation and a d^2 mistake factor for allowing both
ties and unknown corruption in this narrower action class.

It does not yet extend to all M-convex sets: the required strict comparison
between a received action and the learner's action is immediate for subset
choice, but an exchange mapping for compound actions needs its own proof.
Do not assume simultaneous basis-exchange bijections for arbitrary matroids.

The contribution question is a potentially useful robust ordinal adapter,
not superiority to the paper on its stated domain. It needs an exact-source
comparison with noisy sorting, contextual recommendation and Kemeny online
learning before a readiness forecast or a larger implementation is justified.

## Pay for a certified additive gap instead of exact ranking

Suppose the selected ordering has score at most A below the true maximum,
where A>=0 is a fixed certified absolute gap. Stable sorting by true utility
can then improve its score by at most A. The same proof gives

    c_ab <= B+A for every strictly misordered pair,
    mistakes <= binom(d,2)*(floor(C+A)+1)+C.                 (T1)

An anytime integer-program solver's valid upper bound on the optimum and
the score of its incumbent can certify such a gap. A guessed solver gap
or an unverified language-model ranking cannot. This offers an explicit
exchange between ordering computation and a horizon-independent decision
bound, with the same information available to an ordinary implementation.
For time-varying gaps, a known finite supremum A suffices; a growing gap
does not yield the fixed bound(T1).

The exact ordering DP is conventional: for subset S, append a final element
b and add sum_(a in S minus{b}) c_ab to the best score for S minus{b}.
Precompute subset sums and store predecessors. There are d*2^(d-1)
transitions. Updating the global order is unnecessary when i=j, although
reading the context and reporting an action still costs work.

## Why a multiplicative score guarantee is different

Raw agreement can be dominated by comparisons inside genuine tie groups.
For u1=u2>u3, balanced counts c12=c21=M and c13=r have optimal score M+r.
The ordering3>1>2 scores M yet chooses the wrong action on context{1,3}.
By making M large relative to r, it is arbitrarily close multiplicatively
while retaining an arbitrarily large additive gap. Thus a multiplicative
score certificate alone cannot imply the count threshold used in(T1).

Subtracting min(c_ab,c_ba) from both directions leaves ordering choices and
additive gaps unchanged, but removes that particular balanced-pair offset.
Even then, a three-way true tie can retain a directed comparison cycle
with counts c12=c23=c31=M. Its unavoidable cyclic disagreement remains:
the best tie-group score is2M. Add a lower fourth item and c14=r. A ranking
placing4 first and a maximum-score ordering of1,2,3 scores2M, compared with
2M+r when1 precedes4. This again permits a poor available-set choice with
an arbitrarily good multiplicative score ratio. These are static information
states demonstrating why the proof cannot use a relative gap. A complete
infinite-stream impossibility for every approximate algorithm is not claimed.

## Bounded storage when a fault ceiling is supplied

If a valid hard ceiling C0>=C and a fixed additive gap A are known, saturate
each pair count at K=floor(C0+A)+1. The total saturated false counts are
still at most C0. The stable-sort argument still applies to these weights.
A strictly misordered correct pair has count at most C0+A<K, so every
uncorrupted mistaken update increments a counter that has not saturated.
Each pair receives at most K such updates. The same bound with C0 therefore
holds with O(d^2*log(K+1)) count-storage bits, independently of the horizon.
The ordering DP's workspace is separate and can be exponential in d.

Without a trusted corruption ceiling the original unsaturated algorithm
needs O(d^2*log(T+1)) count bits after T rounds. Do not infer a ceiling from
observed inconsistencies: genuine ties can create arbitrarily many of them.
No unknown-C constant-memory result is claimed.
