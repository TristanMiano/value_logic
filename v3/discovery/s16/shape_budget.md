# Shape metadata can rule out a counterfactual design target

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass30.

Let the retained covariance/response block be C=diag(1,c), 0<c<1,
target v=e1, and allow exactly one input column. Additional output
directions are unretained and unrestricted. Put b=(1-c)/c>0.
The minimum-column result gives the sharp lower value1-tmin, where

    e^2 = tmin/(1-tmin)+b*tmin.                        (1)

This follows by substituting g=0 in minrank_envelope.md. The right side
increases strictly on0<tmin<1. A target value tau in(0,1) is therefore
impossible for EVERY compatible one-column source and allowed edit when

    e^2 < (1-tau)*(b+1/tau).                         (2)

At equality the canonical source M=(0,sqrt(b))^T and its hard-case edit
attain tau. Above equality the information contract permits such a source;
it does not guarantee attainability for the particular unretained source.

With an additional allowed input column, the dimension-unrestricted lower
value is1/(1+e^2), achieved by a compatible source with a spare zero column.
Its corresponding possible-target threshold is

    e^2 >= (1-tau)/tau.                              (3)

For c=1/2, tau=1/2, one column requires e^2>=3/2, whereas two columns
permit e^2=1. The one-column squared-edit requirement is50% larger; using
the second column lowers this particular requirement by one third. This
does not price the additional observation or claim a total-cost saving.
For e=1, the target tau=.55 is ruled out by the one-column receipt but
is not ruled out by the column-unrestricted receipt.

In the Gaussian interpretation, columns count observations. Reorienting
one existing observation and allowing another observation are different
counterfactual duties, even when zero padding preserves the old covariance.
A bounded design-search procedure can use (2) to decline an impossible
target before paying for a full optimization. The need for the actual
design budget, shape and uncertainty warrant remains explicit.

This is a consequence of the candidate sharp-envelope theorem, not a
measured search-speed experiment or a new general experimental-design
algorithm. An ordinary method with the same information and theorem ties.

## Do not transfer one metric's percentage to another use

The earlier two-target example's>23.4% interval-width reduction is relevant
to its retrospective full-value-call rule. A posterior upper-variance-only
use instead compares the scalar upper100/181 to the retained-block upper
867127945275459/1611861132384100. That is about2.63% less upper variance,
and about1.32% less standard-deviation/radius contribution. It is not23.4%.
The model-mixture inflation and old-solve residual can further dominate
that difference. Report the metric actually used by an application.
