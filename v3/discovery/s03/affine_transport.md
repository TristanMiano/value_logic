# S19: explicit transport of decisions and fallible forecasts

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT.

The uniform-source rank/closure values can survive assumption revisions, but
an unchanged scalar value does not identify the new action or probability law.
A stronger explicit correspondence permits reuse even for a nonuniform source.

## Translate the whole decision contract

Consider consistent sources S_b={x:A x=b} and S_b' with the same A. Supply delta
with A delta=b xor b'. Translation T(x)=x xor delta is a bijection between them.
Let the new law be the pushforward P'(T(x))=P(x), with no uniformity requirement.
For a query row c_j, its answer changes by the known bit c_j delta. Costs must
remain the same; translating logical answers alone does not prove equal runtimes.

Given any old policy, wrap each new observation y'_j as y_j=y'_j xor c_j delta
before passing it to the old controller. Translate a terminal full-assignment
guess a to a xor delta; translate each parity-output guess by that target's
parity on delta. Correctness utilities and query sequences are identical on
the paired worlds x,T(x). Their net value is therefore identical pointwise.
Taking expectations preserves every policy value, and the inverse wrapper
shows equality of optimal values over the corresponding policy classes. Worst-
case values transport too. An old valid aggregate value source can consequently
be reused without a new statistical draw when this full correspondence is checked.

Precompute one flip bit per available query and target. The wrapper then costs
one bit flip per observed query and the terminal action transformation; it need
not rewrite or optimize the old policy tree. Source/model acquisition and the
cost of checking A delta are still paid. A controller that uses unmodeled runtime,
mutable caches or external feedback is not covered by a pure observation-tree
argument. The broader ordinary antecedent is decision-process isomorphism.

For a forecast report p on S_b, define p'(x')=p(x' xor delta). Normalization,
pointwise likelihoods and all corresponding log scores are preserved. The
mixture's protected uniform component also transports. This differs from
assuming that an arbitrary new fitted model is the transported old model.

## The correspondence is extra semantic information

There can be many solutions delta=delta_0+N t. They all preserve the uniform
source and the value profiles, yet can send a concentrated old forecast to
different assignments. With one free coordinate and a point forecast at zero,
the choices t=0 and t=1 give opposite new predictions. Values, constraint sets
and worst-case trust budgets do not choose between them. The mapping must come
from a declared program replacement or hypothetical-revision convention;
it is not learned merely by preferring a favorable output.

Likewise a hypothetical source translation does not by itself turn old hard
truth receipts into facts about a real new program. That needs a checked
pointwise program relation. The algebraic scenario and its deployed-world
interpretation remain separate types of claim.

## Relaxation and restriction use different report operations

If a checked premise withdrawal expands S to S' containing S, keep a normalized
model f on S and extend it by zero outside S. The report

    p'(x)=(1-eta)/|S'| + eta f(x),  x in S',

is normalized and retains the same worst-case trust surcharge relative to the
new uniform baseline. It pays the unavoidable baseline increase log_2(|S'|/|S|).
For affine premise withdrawal this cardinality ratio follows from the rank
change. Merely extending the old report by zero would assign zero probability
to newly admitted worlds and lose any finite worst-case log-score guarantee.

If S' is a restriction of S, conditioning p on S' is defined because the
protected uniform component makes p(S')>0. Its uniform mixture weight changes,
as [rank_values.md](rank_values.md) derives. Replacing it with a fresh uniform
mixture of the old eta is a different reporting rule, with a different cumulative
trust bill. For disjoint parallel affine sources, a supported model cannot
simply be retained by zero extension: a transport or a new model is required.

## Primary comparison scope

Ravindran and Barto, [SMDP Homomorphisms](https://all.cs.umass.edu/pubs/2003/ravindran_b_IJCAI03.pdf),
IJCAI 2003, §3 defines state/action maps preserving rewards and aggregated
transition probabilities. That definition and the introduction were read;
the full abstraction/option results were not reconstructed. Our finite bijective
observation wrapper is a simple case of ordinary structural decision reuse,
proved directly above. The earlier 2001 technical-report PDF returned HTTP 502.
No novelty or economic superiority over an identical ordinary wrapper is claimed.

Next check explicit correlated finite laws and adaptive policy trees under
translations, plus source-expansion normalization and incompatible transports.

[transport01.json](transport01.json) supplies 32 correlated finite laws and
their explicit translations. Across 4,652 old/new policy states and 226 paired
worlds, the wrapper preserves query indices, costs, guesses and correctness;
its value matches the independently recomputed finite optimum in each new
source. All 32 expanded reports normalize and satisfy the protected point floor.
The two-fact example preserves distinct transports and opposite new point
forecasts. These are same-model finite checks of the declared correspondence,
not evidence that a real program replacement has that correspondence.
