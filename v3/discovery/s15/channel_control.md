# A stronger ordinary randomized channel control

Codex (GPT-6), October23,2026. DEVELOPMENT; follows randomized_summary.md.

The signed-Fourier construction's70% bit accuracy is not optimal. A finite
randomized decision-tree LP gives a symmetric binary channel with accuracy
5/6 using at most five raw queries. Padding its two outputs to counts5/6
preserves the cap6 averaged-purity interface. Both a rational feasible
policy and matching rational dual are saved in channel_lp.json; all linear
equalities, nonnegativity, dual inequalities and zero gap were checked in
exact Fraction arithmetic after the floating solver returned.

## Optimization scope

States are partial assignments (mask,value), with at most five known bits.
For each state s there are nonnegative flow weights for accept, reject and
querying any still-unknown coordinate j. At the root the outgoing total is1.
At another state the outgoing total equals the sum of query weights from
its compatible parents. A query weight appears in BOTH answer children:
each fixed full input follows only the compatible child. This is not a
probability transition averaging the source distribution.

For each of the128 full inputs x, the sum of accept weights over compatible
states equals (1+beta*F_i(x))/2. Maximize beta. The result is beta=2/3.

Every randomized query tree gives such flows. Conversely, at each reached
state normalize its outgoing weights by total incoming flow to choose an
action. Incoming probabilities depend only on the revealed assignment,
not on the unqueried bits. Induction on depth reproduces the flows for
every compatible input. Merging query orders therefore loses no policy
in this finite memoryless representation. This establishes the optimization
scope; the exact certificate verifies its particular optimum.

This is optimal for a symmetric binary channel estimating a selected code
coordinate with five queries. It is NOT an optimal complete invoice decoder,
all-output channel, reset schedule or expected query bill. All earlier
construction outputs remain retained. The solver is an ordinary exact-
certificate control, not evidence of superiority over ordinary algorithms.

## Repetition consequence and costs

Four information coordinates identify the16 codewords. Thirteen independent
episodes per coordinate suffice for the union bound

    4*P[Bin(13,5/6)<=6] <= .01.

Eleven repetitions fail this particular bound. Thus the same simple majority
wrapper uses52 episodes instead of180 for the first channel:71.1% fewer
reset charges in THIS wrapper, with the same1% upper on codeword error.
Every episode can be padded to5/6 queries. Under a uniform codeword, its mean
is5.5; expected totals are286 queries+52*f versus990 queries+180*f. This
comparison excludes policy construction, lookup and random-number costs,
and is not a new audit-stream or CPU result. The cap7 exact four-episode
construction still dominates when that different cap is available.

The program has1611 states,6534 variables and1739 equalities. Only244 primal
entries are nonzero in the saved solution. Ordinary expectation-query
literature motivates the control; no generic LP or Fourier novelty claim.

## A remaining information question

At cap6, counts below5 have constant pure probabilities because their degree
is at most4. Only the probabilities of5 and6 can depend on the codeword.
This does not immediately settle zero-error decoding with an unbounded
number of episodes: output probabilities might have zeros that eliminate
some codewords. The all-positive symmetric channel above does not do that.
The next cheap screen is whether a nonzero pure depth-five acceptance
probability can vanish on one quantizer cell. If it can, examine the actual
separations; if not, finite zero-error decoding under fresh resets is blocked.
