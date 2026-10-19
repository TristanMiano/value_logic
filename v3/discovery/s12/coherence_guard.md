# Cross-model cycle checks as a selective error detector

Codex (GPT-6), October 19, 2026. DEVELOPMENT derivation; prior comparison and
a small sharpness check remain to be done. Q1/Q3/Q4/Q5, with counterfactual reuse.

## Contract

Meaningful Boolean claims have values x_v on the vertices of a fixed connected
graph G. For each edge uv, a fallible procedure predicts the relation
b_e=x_u XOR x_v. Its error event has a supplied valid marginal bound epsilon_e
over the stated task population or procedure randomness. No independent errors,
logical truth prior, or conditional calibration after model selection is assumed.
The graph and procedures are selected before these new predictions; their
acquisition, calibration, checking and any exact anchor query are charged.

Check whether all predicted edge labels are cycle-consistent. If so, they
define a vertex labeling xhat up to global complement. Release all pairwise
differences from it, or use one exact vertex anchor to release absolute values.
Otherwise abstain or use a separately priced exact fallback. This is ordinary
error detection: the prediction is not made true by agreement.

The true edge labels are cycle-consistent identically. Therefore an accepted
wrong prediction has error pattern exactly a nonempty graph cut. Conversely
every nonempty cut is a possible accepted error pattern. For any fixed
nonnegative weights lambda with every nontrivial cut of weight at least one,

    Pr(accepted AND wrong) <= sum_e lambda_e * epsilon_e.

The sharp bound using only these marginals is the minimum of this expression
and one. Its primal packs probability mass on cuts subject to the marginal
capacities; all remaining mass can be all-correct. Ordinary linear programming
duality gives equality. A global minimum-cut separation oracle can check the
dual constraints. This is a fractional cut-cover calculation, not a new LP
principle. It differs from the earlier terminal-specific path certificate.

The primal may include every nontrivial cut, not only inclusion-minimal cuts;
moving mass to a contained minimal cut preserves the marginal upper bounds,
so either form gives the same bad-release optimum. This does not assume that
the original prediction errors themselves have minimal support.

## A cycle needs only one relation beyond a spanning path

For an n-cycle with common marginal bound p, every accepted nonzero error
pattern has even weight at least two. Equal weights lambda_e=1/2 give the sharp
bad-release bound min(1,n*p/2). For n*p<=2, assign probability p/(n-1) to each
of the n*(n-1)/2 two-error patterns and the remaining mass to zero errors.
Every edge then has marginal p and bad-release probability n*p/2. Above this
range, a uniform two-error pattern has total mass one and marginals 2/n<=p.

A spanning path releases its relations without a consistency test and has sharp
joint-error bound min(1,(n-1)*p). In the unsaturated range, the cycle's risk-bound
reduction is 1-n/(2*(n-1)), approaching 50%, at the price of one extra relation
prediction and one parity check. For n=10, p=0.01, the bounds are 0.05 versus
0.09: a 44.44% reduction in a guaranteed bound, not measured prediction error
or a runtime gain. An ordinary error-detecting implementation ties exactly.

## Conditional risk requires a separate argument

Write t=sum_e epsilon_e, a=Pr(reject), and b=Pr(accept AND wrong). On a cycle,
rejecting requires at least one edge error, while accepting wrongly requires
at least two. Consequently 2*b+a<=t. When t<=1 and acceptance has positive
probability,

    b/(1-a) <= (t-a)/(2*(1-a)) <= t/2.

Thus this particular guard has a conditional bound t/2 as well, under that
explicit small-total-error premise. It is not the generally invalid inference
from a marginal bound to a post-selection bound. For equal p the all-even
construction above attains it with acceptance probability one.

For 1<t<2 there is no nontrivial uniform conditional guarantee: put mass 2-t
on uniformly chosen one-error patterns and mass t-1 on uniformly chosen
two-error patterns. Every edge has marginal t/n, but every accepted prediction
is wrong. The acceptance probability t-1 can be arbitrarily small. This sharp
boundary prevents advertising unconditional error detection as automatic
conditional confidence at every error level.

## Unequal marginals: exact unconditional and conditional envelopes

For a cycle write S=sum epsilon_e, M=max epsilon_e, q=S-M, with bounds in [0,1].
The exact bad-release envelope is

    R_bad = min(1, S/2, q).

Every nonzero accepted pattern has at least two errors and at least one error
outside any chosen edge. These give S/2 and q. Conversely two-error patterns
are a fractional matching on a complete graph whose vertices are the cycle's
edges and whose degree capacities are epsilon. Its maximum mass is
min(S/2,q); truncate to one if necessary. A direct fractional construction is
given below, so this need not rely on a black-box matching theorem.

Over distributions with positive acceptance, the sharp conditional envelope is

    R_cond = S/2                         if S<=1 and M<=S/2;
             q/(1-M+q)                 if S<=1 and M>S/2 and q>0;
             0                          if q=0;
             1                          if S>1.

The zero-error case is included in the first line. For S<1, 2*b+a<=S and
b<=q imply b/(1-a)<=b/(1-S+2*b), increasing in b. Substitute the smaller of
S/2 and q. At S=1 the same result is 1/2 whenever q>0; q=0 admits no accepted
wrong pattern. This is an exact marginal-only envelope, not a bound conditional
on every individual transcript or every accepted label vector.

For attainment in the balanced case, arrange arcs of lengths epsilon_e on a
circle of circumference S. Pair each point u in [0,S/2) with u+S/2. No arc
contains both points when its length is at most S/2. The measure of each pair
of arcs supplies a two-error-pattern probability; its incident masses equal
the prescribed marginals. Add zero-error mass 1-S/2. For the dominated case,
put two-error mass epsilon_j on {argmax,j} for every other j, singleton-error
mass M-q on argmax, and zero-error mass 1-M. This gives the displayed
conditional envelope. Omitting the singleton mass gives the unconditional
q envelope. For S>1, reserve a small positive mass b on any two positive-
capacity edges, with b<=S-1. Allocate mass 1-b among singleton patterns within
the remaining capacities; this is possible when b is chosen sufficiently
small. Every accepted output is then wrong.

For unconditional saturation, reduce capacities to total two with each at most
one, then use the same circle construction. This is possible whenever both
S/2 and q are at least one. These constructions establish sharpness for the
abstract error process; they do not claim a trained model realizes the worst
case or that marginal calibration is free.

The same accepted vertex labeling gives any adaptively chosen pair difference,
and known translations preserve its joint error event. New instances do not
share that event. A general counterfactual operator can require information
outside these relative bits, and exact source/operation assumptions remain
separate. A credible application still needs economically obtained marginal
bounds and enough accepted useful predictions to offset the guard and fallback.

The extra relation's accuracy premise is substantive. Computing the closing
edge prediction as the XOR of path predictions makes every output coherent,
but does not give that edge marginal error p. A useful additional predictor or
another justified relation bound must actually be acquired. Repeating the
same model does not manufacture it. An exact anchor resolves global phase only;
it does not validate the remaining relation predictions.

The argument is an error-detecting-code specialization. For a known affine
code with minimum nonzero error weight d, acceptance of a valid codeword gives
d*b+a<=sum epsilon, and the same small-total-error argument yields conditional
risk at most sum epsilon/d when sum epsilon<=1. General code-distance
optimization is a separate cost; graph cut codes provide a minimum-cut
separator. Dietterich–Bakiri's established output-code method and later reject
rules are direct antecedents, so no new coding or ensemble principle is claimed.

The first [rational screen](coherence_probe.json) passes 21,824 cycle semantics
checks and 4,662 extremal-distribution checks over 2,331 marginal panels in
0.2426871 seconds. A heterogeneous example epsilon=(1/2,1/20,1/20) has sharp
bad-release bound 1/10 but conditional bound 1/6. With epsilon=(1/2,1/2,1/100),
conditional error can be one at acceptance probability 1/200. These are exact
constructed distributions, not new measured model error rates.

## Early economic rejection of fresh joint calibration

If all edge truths can be audited together on fresh representative instances,
direct calibration of the entire guarded output is a strong ordinary control.
For example, N joint calibration cases with zero errors give a direct
one-sided upper bound 1-delta^(1/N) on the output error event. Giving each of
n edges a simultaneous zero-error bound using delta/n instead yields the
cycle envelope at most n*(1-(delta/n)^(1/N))/2. In the small-error regime this
is about n*log(n/delta)/(2*N), versus log(1/delta)/N for direct calibration.
The marginal route can therefore be much weaker with exactly that data.

Do not build a benchmark that withholds these joint calibration outcomes from
the ordinary comparator. The retained potential use is existing justified
component bounds, or a setting where the needed joint labels are unavailable
or differently priced. That setting is not supplied here. Marginal confidence
bounds also have an outer calibration-failure event: a high-confidence bound
on conditional risk is not automatically an unconditional conditional-risk
bound after mixing good and failed calibration events.
