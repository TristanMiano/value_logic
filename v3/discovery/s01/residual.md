# From predictions to checked decision certificates

Codex (GPT-6), October 11, 2026. DEVELOPMENT; principal derivation/self-review.
Candidates S01/S02, with S03/S06 connections. No readiness forecast assigned.

## 1. Generative change in architecture

Prior work retained finite information states and transported certificates,
but complete acquisition/storage/checking bills defeated the proposed savings.
An alternative is to let a fallible model propose *which exact computations
would suffice*, and retain only the checked action certificate. Prediction
can be wrong without making the eventual action wrong. Its usefulness is the
cost of finding a short sufficient proof, not correspondence of every forecast
to truth. This is a standard algorithmic possibility, not a novelty claim.

For a fixed deterministic mathematical request let exact finite computations
return bits x_i. Uncomputed bits are epistemically unresolved, not stochastic
truths. Their paid evaluator is sound and total at its declared horizon. After
a subset Q is evaluated, the information source contains every bit vector
matching those outputs plus any separately checked structural constraints.
A predicted bit vector is never admitted as a constraint.

Compare actions A and B by

    d(x) = loss(A,x) - loss(B,x) = b + sum_i w_i x_i.

The individual losses may contain arbitrarily complicated shared terms which
cancel from d; deriving and checking that cancellation has a cost. For no
additional constraints, the interval for the residual is exact:

    L_Q = b + sum_(i in Q) w_i x_i + sum_(i not in Q) min(0,w_i)
    U_Q = b + sum_(i in Q) w_i x_i + sum_(i not in Q) max(0,w_i).

U_Q <= 0 certifies A weakly dominates B. L_Q >= 0 certifies B weakly dominates
A. At exact zero both are permitted; fix one public tie policy. If neither
bound resolves the comparison, more computation or a declared fallback is
required. These interval facts are elementary and inherited in spirit.

**Why prediction can help:** it can order probes expected to shrink the
*relevant* endpoint rapidly. Truth calibration is neither necessary nor
sufficient for cheap certificates. A uniformly accurate model can be wrong on
the high-weight bit that decides the cost. Conversely, a model can be wrong
about irrelevant bits and still give the cheapest valid proof.

## 2. First constructive certificate calculation

For nonnegative integer weights and a threshold request f(x)=1[sum w_i x_i >= T],
write W=sum w_i. A checked set of one bits of weight at least T certifies f=1.
A checked set of zero bits of weight strictly greater than W-T certifies f=0.
If w_i and T are integers, the latter is at least W-T+1. Other checked bits
may be irrelevant to the final certificate but their acquisition bill remains.

Given a point prediction xhat, compute a predicted sufficient subset by
minimum-cost cover among its predicted winning bits. Exact cover selection
can itself be hard with arbitrary weights/costs. A candidate must price the
optimizer or restrict the problem, not receive the shortest certificate as an
oracle. For equal weights and unit acquisition costs, the proposed subset is
just T predicted ones or n-T+1 predicted zeros; a full prediction scan costs
O(n), while each exact mathematical computation may be much more expensive.

On correct predicted winning bits, verification stops after that subset. On a
wrong proposed bit, use its exact value, update both bounds, and select further
probes. Keep every paid observation for the fallback. The output is correct
because it is supported by L_Q/U_Q, regardless of how probes were proposed.

This is only correctness and a mechanism. To support material usefulness we
need a sharp cost account, strong partial-evaluation controls, and ordinary
antecedents. A comparison solely to computing every bit would manufacture an
uninteresting win on easy threshold cases.

## 3. Cheap objections that improve the candidate

1. **Cheap evaluation kills guidance.** If a bit costs one primitive operation,
   an O(n) forecast pass can exceed the whole exact evaluator. Investigate
   expensive but structured mathematical subcomputations and charge the pass.
2. **The winning certificate can be tiny for ordinary methods too.** Weight-
   ordered and probabilistic evaluation belong in the comparison set. Predictor
   quality must affect ordering beyond what public structure already reveals.
3. **Threshold cover is not a free oracle.** Unit weights give a cheap kernel;
   richer cases need priced DP/greedy bounds or a learned proposal with a
   separately measured search bill.
4. **Incorrect guidance can be arbitrarily bad.** Searching every predicted
   wrong coordinate before a one-query ordinary certificate gives ratio n.
   Interleave a sound baseline or reserve a finite speculative budget.
5. **A fallback proof is not a complete economic theorem.** Wall time, operation
   count, inference, retention and checker cost must use consistent units.

## 4. Bundle complementarity without a truth oracle

For two unrevealed fair model bits X,Y, an action predicting X xor Y has
Bayes error 1/2. Revealing either bit leaves error 1/2; revealing both makes
it zero. At query costs c<1/4 each, buying the pair has positive modeled value,
while each singleton has zero immediate benefit. This is an ordinary finite
metareasoning example, not a new theorem or an established model of actual
mathematical truth. It motivates proposals of computation bundles; it does
not imply a greedy method cannot search bundles or that the acquisition law
can be learned without paying for outcomes.

Possible repair of S02: propose a certificate-shaped bundle rather than one
high-confidence bit. Early checked failures can invalidate the bundle cheaply;
all used partial results remain available. The useful unknown is whether the
bundle can be learned and checked for less than a strong conventional search.

## 5. Next constructive work

Locate primary work on explorable uncertainty with predictions, Boolean
function evaluation and robust learning-augmented search. Derive the actual
consistency/robustness tradeoff under a priced certificate proposal. Then use
a small exact prototype to expose where predictive certificate selection
changes cost against a strong ordinary partial evaluator. Retain a null
family with cheap exact values and an adversarial misleading predictor.

## 6. Full-cost scheduling, not just a query count

Let B be a sound complete ordinary procedure and G a guided sound procedure.
Each has a resumable deterministic machine trace for the same request. Define
B(x), G(x) as their standalone primitive-work costs, including prediction
construction, bookkeeping, evaluated subcomputations and certificate checking.
G may fail to terminate; B must terminate on the intended bounded domain.
Keep each lane's virtual input/history identical to its standalone execution.

For integer r>=1, execute r units of G then one unit of B per cycle, checking
termination after every primitive unit. Let C be actual scheduling overhead,
outside those virtual traces. Then the first accepted output costs at most

    min((r+1) B(x), (r+1) ceil(G(x)/r)) + C.

Proof: after j complete cycles B has received j units and G has received r*j.
By B(x) cycles B terminates; by ceil(G(x)/r) cycles G terminates. Stopping
within a cycle only improves these upper bounds. This is standard dovetailing,
not a new algorithmic theorem. It yields a useful implementation obligation:
the *guidance itself* has to be scheduled. Paying unbounded guidance overhead
before launching B destroys the promised robustness.

If C <= h times the number of virtual units + h0, multiply the displayed
virtual-work bound by (1+h), then add h0. If evaluation calls are indivisible,
either use a proven bounded overrun or abandon this bound. Alternating the
number of queries gives no cost robustness with unequal query costs: a guided
first query costing M and a one-unit baseline already gives unbounded ratio.

Caching may help but must not corrupt the comparison: B receives a cached
answer only when it would request it, and its path remains the same. Lookup,
scope matching, storage and failure handling are charged. Without a bound on
that overhead, a shared cache does not preserve the displayed cost theorem.
The clean initial prototype should use explicit priced jobs or machine steps,
and distinguish scheduler work from saved evaluator work.

## 7. A sharper unit-weight constructive direction

For k-of-n with unit acquisition prices, a smallest certificate has size k
when f(x)=1 and n-k+1 when f(x)=0. Let xhat predict outcome b and list all
predicted b bits first, with a fixed public tie order. Query along that list
until an exact certificate of either outcome is obtained.

If f(xhat)=f(x)=1 and the number of false positive predictions is e_plus,
there are at most e_plus failed probes before collecting k true ones *provided
at least k true ones occur among predicted ones*. Without that proviso the
tail search can be long: predicted ones may contain k-1 true ones and one
false one, while the one necessary false-negative bit lies last in a long
predicted-zero suffix. A bound k+Hamming(x,xhat) is therefore false, even for
two prediction mistakes. The error count does not describe the cost of finding
the correction. This matches the broader motivation for structural error
metrics in DS01, without importing its problem-specific formulas.

Repair direction: allow a predicted *redundant certificate* with k+s predicted
ones. If no more than s of these are false, that fixed bundle certifies the
positive result using at most k+s exact probes. A symmetric redundant zero
bundle works for a negative result. The redundancy has to be selected using
observable training evidence or an explicit speculative budget; it is not an
assumption that predictions are valid constraints. Verification checks every
bit actually used, so correctness remains unconditional.

This creates a concrete target for S06: learn which small *bundles* yield
certificates cheaply, not which model predicts every mathematical bit. A
failed bundle is fully observable once purchased, even if the whole truth
vector remains unresolved. That feedback can support learning without charging
for uncomputed labels; the selector still needs bandit or explicitly purchased
cross-strategy feedback. Next derive the regret and full-cost comparison for
a finite bundle library with a baseline completion policy.

## 8. Learning usefulness from completion cost, not every hidden label

Freeze K deterministic certificate policies at the beginning of a round. A
policy includes its cheap forecast/proposal, probe selection, early-stop
checker and ordinary completion fallback. With bounded deterministic requests
each policy j has a well-defined complete cost C_tj in [0,M_t], even though
only the selected policy is executed. The cost vector is fixed before the
policy lottery; an adversary reacting to the chosen policy's private random
draw would require a different comparator. Requests may otherwise be adaptive.

The chosen policy's cost is observed from its execution and its output is
checked. It is unnecessary to learn the unqueried bits merely to obtain this
cost feedback. Applying an ordinary adversarial bandit algorithm to normalized
costs therefore selects useful proof policies without a statistical truth
model. The exact regret statement and normalization for variable M_t must be
specified; we do not import one from an unspecified algorithm. A fixed public
cap M permits the usual bandit reduction. Training/selection/update overhead
adds to total cost and is outside C_tj unless explicitly included in each
comparator. This reduction is established bandit reasoning, not new by itself.

**Information advantage to develop:** a completed certificate often exposes
enough exact outputs to evaluate several *unchosen* policies' costs by cheap
virtual replay. Stop a replay at its first unavailable observation. Its paid
prefix is a lower bound; a declared complete runtime cap supplies an upper
bound. If replay terminates, it supplies the exact counterfactual cost. Charge
the replay work, keep the original policy version and initial receipt scope,
and do not fabricate missing answers. A replay cost is evidence about what
the alternate procedure would cost on this request; it is not a new paid
physical execution nor a free oracle for every policy.

This differs from observing prediction losses only at acquired truth labels:
the target is completion cost of a sound computation policy, including failed
predicted certificates. Relevant ancestors include ordinary algorithm
selection, feedback graphs and partial-information online learning. A useful
new integration would have to earn its replay overhead.

## 9. A provisional evidence-width bound

Here is a direct constructive lemma for the partially replayed costs; it is
not yet a material positive claim. Assume fixed M, and normalize all costs to
c_tj in [0,1]. At round t use exponential weights p_t over K policies,
select I_t~p_t and observe the chosen actual cost. After execution construct
sound intervals [l_tj,u_tj] for every c_tj. Update weights with **lower**
endpoints: w_(t+1),j = w_tj exp(-eta l_tj), starting uniform.

The ordinary bounded-loss potential inequality gives pathwise

    sum_t p_t dot l_t - min_j sum_t l_tj
        <= log(K)/eta + eta*T/8.

Since l_tj <= c_tj <= u_tj, it follows for every realized interval sequence

    sum_t p_t dot c_t - min_j sum_t c_tj
        <= log(K)/eta + eta*T/8
           + sum_t sum_j p_tj (u_tj-l_tj).

Proof: add p_t dot (c_t-l_t) on the left; replace this by the width term,
and use min_j sum l_tj <= min_j sum c_tj. The potential inequality is algebraic
even when intervals depend on the selected policy. Conditional on the
pre-lottery cost vector, E[c_t,I_t]=p_t dot c_t. Thus the same bound holds
in expectation with the expected width term, also for an adaptive
nonanticipating environment and its realized best fixed comparator. The
comparator's hindsight minimum is inside the expectation in this statement.

This is deliberately not a claim of sublinear regret without informative
replay: widths may sum linearly. The intervals themselves yield the simpler
fully observable, deterministic upper certificate

    realized selected total - min_j sum_t l_tj

for actual regret against the fixed policy catalogue. Neither certificate
identifies the true regret when unchosen procedures remain unresolved.

A runtime implementation must also address finite arithmetic, cap validity,
policy versioning, randomized-policy replay and the fee for producing bounds.
The next small prototype will measure exact replay coverage and cost on a
finite shared-computation family before this branch receives further theory.
