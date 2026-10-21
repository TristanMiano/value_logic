# Prior bias changes terminal prices; higher-cap behavior remains open

Codex (GPT-6), DEVELOPMENT, October21,2026. This addresses a limitation of
experiment_frontier.md rather than assuming its uniform-source fee comparison
for an arbitrary prior. Use P_mu(x)=2^-n(1+mu*chi(x)), |mu|<1, and require
exact parity on every world. Marginals of every proper subset of coordinates
are independent fair bits, despite the bias of the final parity.

At cap2, each informative episode count is exactly a readout of one queried
coordinate. A private final query cannot affect a cap2 invoice. Repeated
known-coordinate episodes and uninformative counts only add positive fees.
An exact parity decision tree must acquire all n distinct bits. Until n-1
have been acquired, the next bit is fair conditional on the public history.
The final bit has probabilities(1+|mu|)/2 and(1-|mu|)/2 after orienting its
cheap invoice to the more likely sign. Its expected query fee is
1+min(p,1-p)=3/2-|mu|/2. Therefore the exact optimum is

    (3/2+f)*n - |mu|/2,

including a fixed nonnegative reset fee f per informative episode. This is
an ordinary value-dependent test encoding, with independent randomization
unable to improve a linear expected-cost minimum. The degenerate |mu|=1
case must be specified separately: if off-support correctness is dropped,
the parity is already known and the price collapses to0.

For larger caps, the existing weighted-edge bound gives only
(1-|mu|)*beta*n. The cap2 result suggests that prior bias may change a
bounded terminal term rather than the leading n-rate. That suggestion is
NOT a proved extension: private answer forgetting and public-state reuse
make later conditional sources nontrivial. A full global answer history
cannot be supplied free to the public controller.

Cheap screen: exact cap3 Bellman prices on full cubes n2,3,4 with mu0,1/2,
9/10, using all count maps and integer source weights. Budget under15seconds.
Report the complete table even if it contradicts the bounded-terminal
suggestion. No large optimization run or bias-dependent theorem is selected
on the strength of this small panel alone.

The first probe completed all nine cases in6.0928868s. At mu0,1/2,9/10,
respectively, the returned exact query fees were:

| n | mu0 | mu1/2 | mu9/10 |
| --- | --- | --- | --- |
|2 (repeated-marker extension; see correction below)|5/2|9/4|41/20|
|3|15/4|7/2|33/10|
|4|39/8|37/8|177/40|

Every returned price equals its unbiased price minus mu/2. This is an exposed
finite pattern, not an all-n theorem. The oracle enumerated33,99,231 count
maps and15,165,4169 public states for n2,3,4, respectively. These count maps
retain private-answer forgetting; no free global answer history was used.

**Later scope correction, same session:** the cap-three enumerator permits a
final dummy query after two distinct reads. For n2 this necessarily repeats
a coordinate, violating the main no-repeat contract and H<=n restriction.
The n2 row is valid only for that enlarged repeated-query interface (or an
explicitly supplied third marker coordinate); it is not evidence under the
original contract. For n2 with the original cap2, the proved prices are
3,11/4,51/20. The six n3/n4 entries have enough distinct coordinates for
every final dummy query and retain their stated scope. Preserve the executed
script/output unchanged; this was an interpretation error, not a stochastic
machine failure, and no retry would repair it.

## A proved robust comparison that avoids the open bias extension

Take any exact decoder with uniform-source expected fee K. Independently
choose a fair public bit R and conceptually flip one input coordinate when
running the decoder. A query of that coordinate returns its physical bit
XOR R to the private program; this computational relabelling costs no extra
physical query under the declared interface. Undo R in the final parity.
Conditional on either original parity, the transformed input is uniform
over the entire cube after averaging R. Thus the symmetrized exact decoder
has expected fee K conditional on *each* original parity, and hence at
every P_mu. It uses free independent coins and unpriced relabelling; a priced
coin or controller must be included before using this comparison.

Let an ambiguity set consist of P_mu laws and contain P0. Any experiment T
with worst-case expected fee at most B has C0<=B. Its binary-channel
decomposition coefficient q therefore satisfies q<=B/(beta*n). Buying the
symmetrized decoder with probability q gives a dominating erasure experiment
for every mu, whose worst-case expected fee is qK. Consequently the same
K/(beta*n) comparison factor holds for this *robust budget* formulation.

This differs from a claim about a single known biased predictive law: its
budget must cover an ambiguity set containing the uniform law. The exact
decoder's uniform conditional fee is what makes its replacement cost valid
throughout that set. Information dominance remains Blackwell's ordinary
binary-experiment comparison. The new composition is a valid option for
fallible prior beliefs, while the individual biased-source optimum remains
open for larger caps. No additional price experiment is needed to establish
the algebraic symmetrization identity.

## A cheap failed local repair

To strengthen the weighted lower bound, tried adding half the absolute
parity imbalance to the unweighted edge potential. Its proposed local
endpoint-mass inequality was

    sum_(x in W) c(x)*(1+chi(x))
       >= (7/3)*crossed_edges - (sum_t |imb(W_t)|-|imb(W)|)/2.

The first bias_potential.py screen REFUTED it:50490 comparisons over99
cap3 count maps and255 sources, runtime0.4000868s. A minimal witness is
W={000,001,010} with even parity favored. Query the middle bit, stopping at1
when it is0 and padding otherwise. Its cells on W are{000,001} and{010}.
One cube edge is removed, but total absolute parity imbalance does not
increase. The left side is2 and the required right side is7/3. Both count3
padding and a legal count2 continuation give the same obstruction.

The probe is a successful falsification, not a crashed program or evidence
against invoice_rate.md. Increasing the coefficient on this imbalance term
cannot repair a zero-increment witness. A different potential/history
invariant is needed. Merely saying that all proper input marginals are fair
does not solve the problem: the public transcript need not be a subcube,
and giving it every bit previously seen privately changes the interface.
