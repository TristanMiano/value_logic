# F04 prospective neural discriminator

Status: **design only**. No training, alignment search, held-out result, or F15
challenge has been run. This is an OPP-02 output required by F04, not a frozen
F14 benchmark. Any later change must be recorded before collecting its test data.

## Question and falsifiable hypothesis

Does an ordinarily trained ReLU MLP use representations of the two task-specific
expected action costs in a way that predicts interventions, rather than merely
having activations from which those costs can be decoded?

The strongest claim sought in this small probe is a **partial causal abstraction
on a declared distribution**, up to function-preserving positive neuron rescaling
and permutation. It is not unique identification of a utility function, discovery
of RLL proof search, or evidence about arbitrary networks.

## Ordinary outcome-learning task

Stipulate x=(x1,x2) uniform on [-1,1]^2 and

    eta(x)=1/2+(x1+x2)/8,
    Y|x ~ Bernoulli(eta(x)).

Draw positive false-negative and false-positive costs c_FN,c_FP in [1/2,2].
The network receives (x1,x2,c_FN,c_FP), has one standard unconstrained ReLU hidden
layer and a scalar affine logit followed by a sigmoid. A proposed initial width
is 32; later F14 must freeze initialization, optimizer, training count and compute
budget. Train only on ordinary outcome labels Y using weighted cross-entropy:

    -c_FN Y log p - c_FP(1-Y) log(1-p).

There are no logical labels, hidden-unit targets, positivity constraints on
weights, residual regularizers, or compiled architectural modules. The weighted
loss is a conventional task loss; selecting a task that admits an interpretable
solution does not establish that training finds that solution.

Independently of the network, the task model defines

    J0=c_FN eta(x), J1=c_FP(1-eta(x)),
    p*=J0/(J0+J1), decision*=1 iff J0>=J1.

To derive p*, differentiate -J0 log p-J1 log(1-p): the derivative vanishes at
-J0/p+J1/(1-p)=0, hence p=J0/(J0+J1). Its second derivative is positive for
p in (0,1). Both costs stay positive under the stipulated domain. These costs
are available to post-hoc interpretation development, not as extra network
training labels. Squared/Brier and cost-sensitive 0-1 loss are separate criteria;
W1 prevents inferring one improves solely because another does.

## High-level intervention prediction

For base b and donor d, intervention on J0 alone predicts

    p_H = J0(d)/(J0(d)+J1(b)).

The J1 intervention has the symmetric prediction. Both expressions retain the
untouched cost. Unlike a whole-output transplant, they can predict an outcome
that is neither the base output nor donor output.

Search for a small proper hidden-coordinate subset for each cost, initially
at most 8 of the 32 units; record overlap rather than silently accepting one
representation for both roles. Allow scalar affine decoders fitted on development
data. If no axis subset works, record that result before comparing a distributed
representation under a new prospective budget. Restricting the initial search is
an efficiency decision, not an assumption that concepts must be individual neurons.

For each proposed alignment, replace only the chosen hidden coordinates of the
base with donor activations. Compare both intervened probabilities and decisions
with the declared high-level prediction. Record original prediction error to
separate failure to learn the task from failure of its internal explanation.
A pass threshold, sample sizes, search budget and multiplicity correction must
be set in F14, not chosen after observing held-out effects.

## Discriminating pairs and controls

1. Use donor/base pairs that change J0 while preserving J1, and the converse.
   Positive costs permit such controlled pairs on an interior subdomain.
   Also use equal-J0 donors with different underlying eta/c_FN factors. This
   distinguishes a cost representation from a proxy for only one input factor.
2. Fit candidate alignments on a development split. Freeze them before evaluating
   new factor combinations and intervention pairs. Test both near and away from
   the decision boundary; do not keep only pairs that already agree.
3. Compare with equal-size random subsets, concept-label permutations, shuffled
   donor choices, and the same procedures on an untrained network. Match decoder
   capacity and search effort. An output-only or whole-layer swap is a trivial
   baseline, not an eligible intermediate explanation.
4. Include the constructed duplicated-but-unused neuron witness from the F04
   fixture. A decoder should succeed there while a causal-use test fails.
   This checks methodology; it is not evidence from a learned network.
5. Apply exact positive rescaling/permutation, adjusting incoming biases/weights
   and outgoing weights. Transport the candidate alignment and decoder rather
   than fitting it anew. The scalar-output one-hidden-layer network has an exact
   algebraic invariance (F04 main note §5). Numerical experiments must separately
   account for floating-point tolerance. Replacing raw activation magnitudes by
   a new threshold after rescaling is not an invariant interpretation.

## Possible results

A useful positive result predicts held-out interventional effects better than
matched controls and survives transported gauges. Decodability alone supports
only a correlation claim. Good task predictions with poor intervention agreement
refute this particular mechanistic hypothesis, not the broad value-first program.
A circuit that is only found after logical supervision belongs to a different,
explicitly enforced-structure experiment. A negative result is retained rather
than reformulating the criterion on the same held-out data.

## Relation to existing work and remaining scope

Geiger et al., *Causal Abstractions of Neural Networks* (NeurIPS 2021; arXiv
2106.02997v2), §3 and equations (1)–(3), provide the interchange-intervention
precedent. Our proposed variables are independently defined action costs, not
arbitrary labels assigned to convenient activations. The ReLU gauge control is
proved here for the simple architecture. Neither ingredient establishes novelty
by itself; compare with the original causal-abstraction baseline before a claim.

F04 supplies this design and analytical controls only. F14 must freeze the
experiment and F15 run it. No task boundary is bypassed because the design is
small enough to execute earlier.


## S2 prospective competing explanation: high-level cost scale

[The continuation](../derivations/01a_nonlinear_and_reflective_reconstruction.md),
Section 5, adds a control *before* any training, alignment or held-out testing.
For a positive input-dependent g, the descriptions (J0,J1) and (g J0,g J1)
have the same unrestricted pointwise optimal probability. Their J0-only donor
interchanges generally differ: g(d)J0(d)/(g(d)J0(d)+g(b)J1(b)) need not equal the
original prediction. A fixed global scale is an invariant positive control.

At experiment freeze, declare a small bounded-complexity family of positive g
functions, its fitting budget and the base/donor distribution. Fit competing
alignments only on development data and match capacity/search effort. Do not
choose g or intervention pairs after seeing held-out results. Report if both
hypotheses fail or cannot be discriminated; observational prediction alone
cannot establish an absolute internal cost scale. This is not a claim that
both descriptions are low-level realizable in the given network.

Do not conflate this with S1's neuron rescaling/permutation: transporting a
low-level intervention under that gauge preserves the same high-level question.
Here the competing *high-level* decomposition changes the counterfactual query.
Input-dependent training reweighting may also change a finite-capacity fit even
though its unconstrained pointwise optimum is unchanged. No new experiment has
been executed and no baseline architecture is restricted by this amendment.
