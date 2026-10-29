# What partial ranges can justify for decisions

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT extension, not part of A1.

## Fixed-model decision bracket

Let the nonempty true feasible scalar set be R, with checked inner/outer
sets I subset R subset O. Fix a finite nonempty action set A and specified
bounded real losses L_a(q) on O. These are the decision maker's loss functions,
not a probability model or values inferred from compatibility. Define

    l_a = sup_{q in I} L_a(q),   W_a = sup_{q in R} L_a(q),
    u_a = sup_{q in O} L_a(q).

If I is empty, a known common loss lower bound can replace l_a; otherwise
use -infinity and accept that the result may be uninformative. Then
l_a <= W_a <= u_a. Choose a_hat minimizing u_a, and put

    epsilon = u_a_hat - min_b l_b.

For the exact fixed-model minimax value W*=min_b W_b,

    0 <= W_a_hat-W* <= epsilon.                                (D1)

Proof: W_a_hat <= u_a_hat and W* >= min_b l_b. Nonnegativity follows from
the definition of W*. A certificate epsilon=0 proves minimax optimality.
An epsilon below a specified tolerance proves that tolerance without full
range recovery. Supremum bounds need their own exact calculation or certificate;
they are not free merely because R has a finite interval description.

For minimax regret, first replace L_a(q) by

    G_a(q)=L_a(q)-min_b L_b(q),

using the same q in both terms. Apply(D1) to G. Separate extrema of different
losses are generally insufficient, and minimax loss and minimax regret must
not be conflated. These are familiar robust-decision constructions; the
adaptation is the checked receipt-specific I/O interface.

## A limited, sound computation stopping rule

Suppose a proposed computation only reveals more about this fixed R and
fixed losses, costs a deterministic amount c in the same loss units, and has
no reuse, future-information or other benefit. It may choose a different action
after its result, but cannot change R. Its final selection is restricted to the
specified action class: randomizing over that class is not silently allowed
unless those randomized policies were already included in the optimization.
Even an exact optimizer can improve the
incumbent's true worst-case loss by at most epsilon. Thus if c>=epsilon,
the proposed computation cannot strictly improve that criterion net of cost.
For an already certified incumbent, computing more precision may still be
interesting research, but is not justified by this particular single-use duty.

This is an upper bound on value of computational refinement, not a general
value-of-information formula or a claim that any query below epsilon is worth
buying. The probability of improvement and actual computation cost remain
separate questions. It is also not a competitive guarantee against an oracle
that learns the actual state.

**Observation counterexample.** Let R={-1,1}. Action A has losses0 and1,
respectively; B has losses1 and0. The exact minimax loss is1 and both actions
are optimal, so a complete computational certificate has epsilon=0. A new
perfect observation of the actual state permits loss0. A measurement costing
less than1 improves the contingent policy in every state. Thus(D1) cannot
bound the value of observations that shrink R, even though it bounds further
optimization over the already fixed R. This distinguishes reasoning cost
from evidence acquisition without treating either as automatically useful.

## A concrete band-loss duty

Let a fast action have loss M*1_H(q), and a fallback have constant loss c,
where0<c<M and H is a specified hazardous band. These assumptions define a
small mathematical decision problem; they are not claims about a deployed
application or measured economic benefit.

* If the outer range misses H, the fast action has worst loss0 and is optimal.
* If the inner range meets H, a compatible source realizes loss M for the
  fast action, so fallback with worst loss c is minimax optimal.
* If neither is certified, fallback guarantees c, and the most that resolving
  this one fixed-model duty can save is c.

The noisy-envelope example in partial_findings.md supplies the first case
for H=[-5/4,-6/5]. The interval hull includes H and therefore cannot support
that certificate. A tailored ordinary bounds calculation does support it.
If H is just a conjectured hazard region, the decision guarantee is conditional
on that loss model; compatibility calculations do not verify the hazard model.

For convex scalar losses, supremum over a compact R is attained at one of its
two extreme endpoints. Then holes add no minimax-loss information. For affine
scalar losses and their finite-action regret functions (maxima of affine
differences), the same endpoint sufficiency holds. The whole nonconvex image
is useful for nonmonotone properties such as band avoidance, not for every
possible decision downstream of an uncertain scalar.

## Statistical interpretation requires a separate coverage event

Suppose the source x* is fixed but receipt bands are data-dependent. If an
upstream procedure proves joint coverage

    P(x* belongs to the complete retained source set S) >= 1-alpha,

then on that event every sound outer range for every adaptively chosen readout
contains its actual value. Therefore all checked band exclusions are correct
simultaneously on that event, even if queries are chosen after seeing earlier
answers. No additional query-count penalty arises from deterministic logical
consequences of the same covered source set. Existence of an inner witness
still means possible, not actual or probable.

If source sets change as more observations arrive, one needs time-uniform
joint coverage of the relevant source, or an explicit finite error allocation.
Marginal95% coverage for each separately selected receipt does not supply
95% joint coverage after arbitrary selection. A union bound for fixed bands
is a valid conservative option; model assumptions and adaptive sampling must
also be justified. Rounding real-valued confidence limits to rational limits
outward preserves coverage, while inward rounding need not. No confidence-
sequence constructor or statistical calibration is implemented in this work.

An empty checked outer range diagnoses incompatibility of the supplied model
and receipts. It does not identify which premise failed, prove that reality is
impossible, or license arbitrary subsequent actions. Under valid joint coverage,
such a false incompatibility conclusion can occur only off the coverage event.

## Literature and exact scope of reading

[Manski, revised April2026](https://arxiv.org/pdf/2602.00355), sections5.1--5.2.3
(PDF pages35--39) separates feasible actions, credible states, and welfare;
defines maximin and minimax regret; and distinguishes decisions with sample
data. This is a direct conceptual antecedent for useful action despite
underdetermined theories. The contribution here is not that idea. Other
sections and the broad philosophical claims have not been audited.

[Howard, Ramdas, McAuliffe and Sekhon](https://arxiv.org/pdf/1810.08240),
v9(2022), introduction, section6 and Lemma3 with its AppendixC.4 proof,
give the simultaneous confidence-sequence contract and its equivalence to
validity at arbitrary random times. The proof uses inclusion in the union
of failure events and the first-failure stopping time. That established
contract, rather than an ordinary fixed-time interval, is what the preceding
time-uniform interpretation would require. No boundary-rate theorem is imported.

[Aradillas Fernandez et al., December2025](https://arxiv.org/pdf/2408.11621),
section2 and LemmaC.1 with proof, separates ex-ante and ex-post robust Bayes
criteria in a Gaussian partially identified treatment problem. Its assumptions
include a fixed two-point prior for identified parameters and unrestricted
conditional priors for unidentified parameters. The piecewise-linear posterior
regret calculation shows why randomized actions can matter. Those statistical
optimality results do not transfer to the present deterministic receipt model;
the relevant lesson is to state the actual criterion and information timing.

Disposition: useful conditional interface and stopping consequence; established
decision and coverage machinery credited. Standalone novelty UNASSESSED.
No increase to V19 readiness and no new empirical cost percentage.
