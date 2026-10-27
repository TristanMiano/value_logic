# A stronger acquisition interface can remove receipt ambiguity

Codex (GPT-6), October26,2026. DEVELOPMENT; ordinary-control screen.
This develops the comparison requirement, not a new elicitation principle.

Suppose a query returns min_i h_i(x_i), with independently chosen affine
functions h_i and known compact source blocks B_i. If arbitrary known
configuration-specific offsets are allowed, one can isolate any selected
configuration a. For a chosen readout f_a, compute finite bounds on f_a and
on the other readouts. Add offsets to the latter so every other adjusted
readout is strictly above the upper bound of f_a on B_a. The returned
minimum is exactly f_a(x_a). Alternatively set every other h_i to a known
constant above that upper bound when constants are permitted.

Coordinate readouts then recover all unknown block coordinates in at most
sum_i d_i chosen queries, after the bounds and query description costs.
If the actual task is just one future minimum and that query itself is
available, a single direct query is stronger still. These are substantive
controls: do not compare passive-history inference against full recovery
while silently granting it a query interface that permits direct answers.
Responses of arbitrary precision are not unit-size information packets;
representation lengths, supplied bounds and observation prices matter.

Shared-weight queries need not permit isolation. A configuration dominated
throughout the allowed weight domain is invisible to all optimum-value
queries there, yet may become relevant after the domain changes. Learning
the complete underlying configuration list and learning its value function
on the permitted domain are distinct goals. Retaining the domain/version
is part of a legitimate inference contract.

For example, two scalar configurations have costs x_1=0 and x_2 in[1,2].
All allowed nonnegative common-weight queries return min(w*x_1,w*x_2)=0,
so no such transcript identifies x_2. A later negative weight makes the
second configuration optimal and exposes the unresolved information. This
is elementary dominance and domain dependence, not a new lower-bound
method. Configuration offsets or direct x_2 observations defeat it.

## Decision-specific one-query value is already an ordinary target

Let C be the current compact compatible-source set, V its continuous scalar
target, and G a continuous exact query. Under absolute-error loss, the best
estimate after answer q is the midpoint of the smallest interval containing
{V(x): x in C, G(x)=q}. G's worst residual error is therefore

    (1/2) * max_{x,x' in C : G(x)=G(x')} |V(x)-V(x')|.

This follows by the two-endpoint lower bound and the midpoint upper bound;
compactness gives attainment. It is the ordinary radius-of-information
calculation. A fixed query price is added to this loss only under an explicit
common-unit tradeoff. Separate possible-value ranges for G and V cannot
compute the expression because they discard their shared-source relation.

For an actual action task, use conditional decision regret rather than
scalar reconstruction error. Wang--Boutilier and the later constraint-based
elicitation work already develop this principle. A fresh contribution here
would need a useful structured algorithm, permitted-query advantage or
complete cost result. PARK the generic query-selection mechanism; retain
these interface checks when defining the bounded whole-range contribution.
