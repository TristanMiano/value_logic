# Adequacy belongs to the public observation interface

Codex (GPT-6), October 19, 2026. DEVELOPMENT synthesis across the permission,
fallible-model and invoice branches. This is a generalization of the fixed
policy envelope, not a claim of a new abstraction theory.

Let X be a finite world space, F a nonempty proposed source, and o:X->O the
public transcript of a fixed deterministic observation policy. Let g_J:X->Y_J
be the task features needed at transcript o, with a nonempty finite family
J(o). The features may be coordinate projections or specified derived values.
Define

    H_o = {x: for every J in J(o(x)), there exists w in F with
             o(w)=o(x) and g_J(w)=g_J(x)}.

For each public transcript t, the conditional feature sets of H_o and F agree:

    {g_J(x): x in H_o, o(x)=t}
      = {g_J(w): w in F, o(w)=t}, for J in J(t).

F is a subset of H_o, giving one inclusion. Each x on the left has the required
F witness by definition, giving the other. If an H_o-world has transcript t,
the nonempty feature family also provides a compatible F-world. Hence conflict
detection agrees. Conversely, any enlarged source preserving every such
conditional feature set is contained in H_o. This is the maximal envelope for
the declared transcript/feature service. It does not assert that enumerating
the envelope, generating the transcript or testing membership is cheap.

Suppose each permitted action's guarantee at t is a conjunction of predicates,
one on each g_J. If it holds for every source feature pattern, it holds on the
actual x whenever x belongs to H_o. Different J can use different witnesses.
A supplied unconditional bound on x outside H_o therefore transports to this
whole fixed policy. This says nothing automatically about conditional error
among accepted transcripts. It also does not justify changing the policy after
selecting favorable calibration data.

For a deterministic adaptive query/action controller, its complete public
transcript is itself such an o. Its internal source-based choices are fixed
functions in that policy. Earlier releases need their own prefix services;
including each prefix's feature requirements gives their intersection as the
whole-stream adequacy event. A final-leaf guarantee alone must not be silently
used for an action already taken at an earlier prefix.

## Hidden invoice answers are not public receipts

Let the proposed model on bits b,a be b=a. A private program buys b once at
unit cost, stops, and releases only its invoice. Its public observation is
constant, o(b,a)=1, although the private executor saw b. With target feature a,
the conditional feature set is {0,1}; the maximal envelope is every world.
No toggle can be certified to make a zero over that feature set.

If a controller improperly treated private b=1 as a public receipt, it would
reduce the model to a=1 and certify toggling a. At actual b=1,a=0 this fails.
That procedure changed the observation contract: it did not obtain information
from the constant invoice. If b genuinely were public, its stronger envelope
would instead be b=a, excluding that world. The difference is semantic and
remains even with unlimited ordinary computation.

Known public random tapes can be conditioned on explicitly. Hidden random
choices require an augmented world and the actual public transcript relation;
one cannot condition on a private tape for free. If many tapes share a public
transcript, their compatible possibilities remain in its source. A marginal
bound proved separately for a favorable tape is not a bound for the deployed
randomized controller without its distribution and independence assumptions.

## Relation to the retained constructions

Coordinate receipts give the Q-plus-J envelope in task_adequacy.md. A fixed
observation tree gives its leaf envelope. Interval receipts and projected
distance constraints give temporal_adequacy.md. Invoice programs give a public
transcript source whose representation and inference costs are studied in
transcript_sources.md. Each uses an ordinary existential image/preimage
construction, with an explicit observation contract and paid implementation.

The shared lesson is constructive: model details and private computations may
remain unresolved while the required public task features are preserved. A
useful contribution would need a compact service, useful bound or application
that this explicit contract enables beyond the closest existing formulation.
This semantic unification by itself is insufficient to establish novelty or
an economic gain. No additional large harness is justified for this elementary
witness argument.
