# Checking useful cost forecasts through their drift

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; broad early screen.
Ranking supermartingales, additive drift, Bellman supersolutions and direct
mean inference are established comparators, not proposed new principles.

Consider a finite-state randomized reasoning procedure with absorbing
completion set T. A fallible model proposes a nonnegative potential V with
V=0 on T. For each nonterminal state s, suppose a truthful local receipt gives

    E[V(S_next) | S_now=s] <= V(s)-epsilon_s,
    epsilon_s>0.                                             (D1)

Then epsilon=min_s epsilon_s>0. The stopped process
V(S_(t wedge tau))+epsilon*(t wedge tau) is a nonnegative supermartingale,
so E[tau]<=V(s0)/epsilon and completion occurs almost surely. The finite
state assumption makes the positive minimum meaningful. More generally,
if a nonnegative per-step price c(s) replaces epsilon_s in(D1), stopping
and monotone convergence give E[sum_(t<tau)c(S_t)]<=V(s0), with a separate
termination condition if zero prices are allowed. These are standard
supermartingale cost bounds.

The model's transition probabilities need not be close to the true ones.
For instance V(a)=2,V(b)=1,V(t)=0. At a, either a deterministic transition
to b or the mixture .4*a+.6*t has next-potential expectation at most1.
At b, transition to t. The kernels disagree substantially at a, yet V
certifies unit-price expected cost at most2 for both. The useful object is
the projected drift, not a claim that either whole model is true.

## A sampling route has a different contract from a complete verifier

If a simulator permits independent successor samples from every declared
state, fix V before a validation batch. A bounded-mean upper confidence
bound for each E[V(S_next)] can establish(D1). Union-bound the declared
states and the candidate-validation error budgets, or use a simultaneous
confidence source for a predeclared family. A predictor fitted to the same
validation data requires that simultaneous guarantee or fresh data.

No known positive lower bound on every transition probability is needed
for this one-sided, possibly abstaining, margin-dependent check. This is
not a size-only sample bound, a complete yes/no verifier, or learning from
reset-only trajectories. A tiny drift can require arbitrarily many samples;
unvisited states cannot be silently treated as checked. Direct generation
from every state is a substantial access assumption and its cost is paid.

The recent unknown-MDP source in the literature log rules out a budget
depending only on state/action counts and error probability. Its statement
does not rule out this ordinary candidate-range/margin-dependent validation.
We do not claim to refute its theorem, or to have audited its entire proof.

## Counterfactual reuse question

Suppose a common source certifies a set of possible row-wise expectations
of several potentials V_1,...,V_r. A later nonnegative combination V=V beta
can inherit a checked drift bound by linear optimization over that source.
Prices or policy choices may then change inside the certified inequalities.
The source must cover the selected policy's actual transitions. A new action
with no receipt is not justified by algebraic recombination.

This is ordinary robust Bellman verification and finite-dimensional moment
retention. The potential contribution would need a concrete reasoning
workflow in which direct projected-drift purchases and reuse save enough
work relative to an equally informed ordinary verifier. Full-kernel learning
alone is too weak a baseline. No such saving or moderate novelty is yet
established; retain the direction, reject the generic principle as new.

## A bounded fallback replaces unchecked global dynamics

Let R be a finite region of states in which a proposed reasoning policy will
continue. Outside R it immediately invokes a terminating fallback whose
conditional expected cost is bounded by B(s). Let V be nonnegative on R,
and define W=V on R and W=B outside R (zero at completed states). A checked
inequality at every s in R is

    c(s)+E[W(S_next)|s] <= V(s),  c(s)>=epsilon>0.             (D2)

Stop at first exit from R or completion. The same stopped-supermartingale
argument bounds expected in-region cost plus expected B at exit by V(s0),
and epsilon proves finite expected exit/completion time. Conditional on the
exit state, the fallback adds at most B. Thus total expected cost is at most
V(s0). A global model outside R need not be learned. A bounded-mean sampling
check still needs a known bound on W over possible successors, including
rare exits; excluding unobserved successors would be unsound.

An unchecked estimate V below the fallback price cannot simply be used until
its local check fails. At a failing state, switching to a fallback with B>V
can exceed the very potential used to justify the preceding step. Either
check the whole admitted region with its boundary prices, reserve the possible
fallback cost, or obtain a new valid continuation bound before making that
step. This is a concrete obstruction to naive speculative cost certification.

## Combining locally useful models

Suppose each potential V_i is a nonnegative certified cost bound for its
own policy pi_i on the same state space, with actual positive step prices:

    c(s,pi_i(s))+P_(s,pi_i(s)) V_i <= V_i(s).

Set U(s)=min_i V_i(s) and choose an attaining i at the current state. Since
P U<=P V_i, this switching policy satisfies

    c(s,pi_i(s))+P_(s,pi_i(s)) U <= U(s).

Consequently U is a valid bound even though the whole transition model that
suggested V_i may be false. A common source or separate valid error budgets
must justify all the selected local inequalities. This is ordinary Bellman
supersolution composition/generalized policy improvement, not a new logic.

If the expectation of U is also known for every admitted action, define

    (T U)(s)=min_a [c(s,a)+P_(s,a) U].

The certified associated actions imply TU<=U. Monotonicity then gives
T(TU)<=TU, so one backup yields another supersolution; positive prices and
a nonnegative finite bound give the same stopping argument. Computing TU
from each policy's *own* scalar drift receipt is generally not possible.
The cross-potential expectations need receipts, source support information,
or newly paid evaluation. The model's unvalidated cross predictions do not
supply them.

For a small illustration, a start state pays1 and moves to a or b. Each of
a,b has a fast terminating action of cost1 and a slow action of cost3.
Policy1 uses fast at a and slow at b; policy2 reverses this. With equal
branch probabilities, both fixed policies cost3 from the start. Their
pointwise minimum is1 at a,b and3 at the start; one backup reduces the
start bound to2, attained by switching to the fast action after observing
the branch. The branch probability is unnecessary for that backup because
U(a)=U(b)=1. The two models can be wrong about it while this certificate
remains sound. Ordinary policy improvement produces exactly the same result;
this is an algebraic example, not an empirical33% saving or a novelty claim.

The bounded reasoner gains an explicit distinction between a model's global
truth, the validity of its selected drift receipts, and which recombinations
those receipts actually support. A natural implementation must still pay
for region discovery, potential evaluation, verification and fallback.
