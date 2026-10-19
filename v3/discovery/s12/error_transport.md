# Counterfactual reuse of a task-specific error event

Codex (GPT-6), s12 DEVELOPMENT early screen. Related to S17/S19 and this
session's paid relation calibration; not a new numbered family.

Suppose a fixed cheap parity relation predicts x_s from x_T with offset b.
Its error bit is E(x)=x_s xor parity_T(x) xor b. A declared translation
y=x xor delta has the transported relation offset
b'=b xor delta_s xor parity_T(delta). Its error is exactly E(x), pointwise.
Therefore any number of translations, even chosen adaptively from the same
instance's observations, share one failure event. If Pr(E=1)<=epsilon, the
probability that any of those transported predictions is wrong is at most
epsilon. No independence or union factor across these translations is needed.
The map and its offset must actually be checked; choosing a convenient
counterfactual correspondence does not establish its semantics.

An accepted calibration rule's marginal guarantee transports with the same
qualification: calibration randomness and the new base instance are averaged
over. Infinitely many counterfactual queries about that one base instance do
not create independent new instances. Across new base instances, the earlier
familywise limitation remains. Nor does translation establish that runtimes,
invoice orientations or acquisition bills are unchanged.

For a more general linear error vector e=xhat xor x, a family of requested
linear outputs has simultaneous correctness exactly when R e=0, where the
rows of R span the requested output rows. Thus task-relative model adequacy
can require only a syndrome, not correctness of every model coordinate.
Translations change known offsets and keep R. Arbitrary coordinate overwrites
before a full parity request can produce every singleton row, making R full
rank on that target scope. The compact shared error event then becomes full
correctness on that scope. Weighted acquisition of a linear syndrome reuses
the ordinary rank/basis machinery already explored in S18; no new calibration
or matroid theorem is claimed.

**Disposition:** retain this as an explicit calibration/revision interface
boundary, not a new harness. Earlier [affine transport](../s03/affine_transport.md)
already proves pointwise policy correspondence under stronger whole-contract
conditions. This note only isolates the weaker error-event statement useful
when the complete source model is fallible. A separate application would be
needed to establish a material new contribution.
