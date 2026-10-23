# A summary can be visible in probabilities but expensive to identify

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass23.
Uses the fresh-reset, count-only, averaged-purity contract of
pure_query_criteria.md. Extra ignored padding coordinates are available.

## A strict separation between two duties

Let n=2m>=4, w(x) be Hamming weight, and Q(x)=(w(x)-m)^2. The summary has
m+1 cells. It hides coordinate permutations and global bit complementation.
A degree-one function constant on all Q-cells must be constant: permutation
invariance makes all its linear coefficients equal, and complementation
then makes that common coefficient zero. But Q itself has degree two and
separates every cell. Thus d_any=d_sep=2 and the minimal cap for nonzero
information or arbitrarily accurate identification is3.

An explicit optimal-cap channel chooses two distinct coordinates uniformly,
queries them and returns their sign product Z by counts2 and3. With signs
z_i=(-1)^x_i,

    E[Z|x] = ((sum_i z_i)^2-n)/(n*(n-1))
           = (4*Q(x)-n)/(n*(n-1)).                         (1)

Hence P[count2|Q]=p_Q=(n-2)/(2*(n-1))+2*Q/(n*(n-1)). Different summaries
give different probabilities and nothing else about x is disclosed.

Zero-error identification has a different threshold. Take a=the Q=1 cell
and b=the Q=0 cell. Every partial assignment of fewer than n coordinates
that contains a balanced input also contains an input with weight m-1 or
m+1: flip one unqueried coordinate. A nonnegative literal polynomial of
degree<n that vanishes on all of a must therefore vanish on b as well.
The ordered zero-separation criterion fails below degree n. Reading all
n bits and using n/n+1 padding to report any desired summary bit supplies
the upper bound. Thus

    d_zero=n; minimum zero-error random-time cap=n+1.       (2)

This is an unbounded gap between the cap3 noisy duty and the exact duty.
It includes adaptive public control and almost-sure finite termination,
not just a fixed number of episodes. It does not apply if private queried
values or source-dependent private state survive reset.

## Every pure cap3 channel is a garbling of the pair-agreement channel

Fix a Q-cell and temporarily put the uniform distribution on that cell.
It is invariant under coordinate permutations and complementation. In any
adaptive two-distinct-coordinate query process, the first sign is uniform,
and the second agrees with it with probability p_Q, independently of the
first sign. The labels of the queried coordinates add no information under
this distribution. Simulate the process using an independent fair first
sign and one Bernoulli(p_Q) agreement bit, plus its own private coins.
Stopping before two queries ignores that agreement bit.

For a cap3 episode, the event of its final count is already determined after
at most two queries: reaching the third query fixes the count at3. Thus the
entire count is a source-independent randomized function of this one
agreement bit. Averaged purity makes its law on the uniform cell identical
to its law at EACH fixed input in that cell. Therefore the simulation proves
Blackwell domination for the pointwise interface, not a distributional
weakening of it. Ignored padding coordinates cannot add source information.

The same argument applies at every public history under fresh resets. So
adaptive selection of other pure cap3 count policies cannot produce a more
informative experiment per episode than the explicit channel(1).

## Repetitions are a real cost

The closest summary probabilities are p_0 and p_1, with spacing
Delta=2/(n*(n-1)). Estimating the agreement frequency to less than Delta/2
and selecting the nearest allowed p_Q gives error at most epsilon after

    N >= (n*n*(n-1)*(n-1)/2)*log(2/epsilon)

independent episodes, with a conservative rounding/tie convention.
This is an O(n^4 log(1/epsilon)) upper bound, not an efficient full decoder
relative to a larger permitted cap.

Conversely, any cap3 fresh-reset protocol that distinguishes Q=0 from Q=1
with error<=epsilon<1/2 on both, and has finite expected episode count T
under Q=0, satisfies

    E_0 T >= kl(1-epsilon,epsilon) / kl(p_0,p_1).          (3)

Use relative-entropy chain rule for the stopped transcript, data processing
through each episode's garbling, and data processing to the final binary
decision. Truncation handles unbounded stopping with finite expectation.
If an episode reaches two informative input queries only with probability
q(history), its KL contribution is at most q(history)*kl(p_0,p_1), because
the earlier stopping decision uses only the independent first sign and
coins. Thus the same argument gives a lower bound twice(3) on the expected
number of informative input-coordinate probes. Padding can add more.

Here kl(p_0,p_1)=Theta(n^-4), so the fourth-power repetition order is
unavoidable in this particular interface, even with adaptive tests and
sequential stopping. This is a concrete reason not to treat low-degree
probability information as cheap conclusive knowledge.

The local sample-complexity derivation uses standard Blackwell comparison,
KL data processing and sequential testing. Its exact primary-source and
query-complexity comparison remains to be completed. No priority claim or
independent confirmation is supplied by this same-model derivation.

The [finite probe](balanced_probe.json) passes1360 input/channel equalities,
82 partial-assignment count types and all576 deterministic adaptive depth-two
binary-output trees on four bits. At n=8 and error<=1% per input, the
sequential lower bound is1748.73 expected episodes under Q=0, while a simple
fixed-sample wrapper uses8309 episodes. With cap9 available, three episodes
can instead transmit the five-valued summary exactly. These are different
cap contracts, so the comparison describes a capability/cost tradeoff, not
an unconditional efficiency gain. The lower-bound theorem remains same-model
development; finite enumeration verifies only the listed cases.
