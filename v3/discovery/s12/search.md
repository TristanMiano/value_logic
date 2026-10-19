# s12 generative portfolio notebook

Codex (GPT-6), DEVELOPMENT. This is a revisable search record. Numbered passes
are not separate families, confirmations or minimum time commitments.

## Opening pass: separate the missing premises from the available mechanisms

The s11 repair and invoice packages already assume a supplied logical source.
Their broadest missing step is an economical reason to use that source on the
current task. Merely attaching a global coverage epsilon to it does not solve
that step. In particular, the source can be false exactly on the receipts that
make its attractive action available. We will distinguish four possibilities:

1. **Logical validity:** derive source constraints from checked premises about
   the same program. Cost is proof/checking work, not statistical sample size.
2. **Population coverage:** measure or assume a distributional failure bound
   for a model on fresh tasks. This needs a population and selection-aware use.
3. **Task-specific sufficiency:** verify only the residual statement needed for
   a chosen action or value contrast. This can be weaker than model validity.
4. **Robustness to known inadequacy:** choose a useful action under an explicit
   model-error set, while charging the information that defines that set.

These are different contracts. A known ordinary proof checker, control variate
or robust optimizer can implement one; a contribution must identify the added
adapter or consequence rather than claim that conventional reasoning lacks it.

### First inexpensive screens

**Per-model confidence plus convenient selection:** already fails. For M
equally likely labels, each model can exclude one label (error 1/M), while
choosing the model that excludes the observed label makes selected error one.
No new confidence learner is warranted without a simultaneous or selection-aware
promise. A union bound is a safe baseline, not an original contribution.

**At most k false premises:** this can produce useful robust actions, but as
stated it is just another checked source with a cardinality constraint. The
earlier source/repair machinery already accepts it. Keep only if a compact
task-specific certificate or source update changes the actual cost.

**Observation as permission:** two roles remain distinct. A receipt can change
which action is preferred among a fixed menu, or certify actions that previously
could not be released. A comparator permitted to query but forced to keep its
old menu isolates the latter capability; an identical contingent planner does
not lose that capability. Greedy information-gain scores may ignore permission
complementarity. Check the uncertainty-query/contingent-planning literature
before building another general optimizer.

**Guarded constraint families:** consider a source and target with one guard c
implying each of m feature bits. If a query reveals c=0, every feature subset
can be flipped safely while leaving c fixed; before that query, flipping any
feature could violate the implication at c=1. One observation thus enables an
exponential menu without revealing individual feature values. This generalizes
the previous three-bit star rather than introducing a new family. It suggests
looking for an economical symbolic permission interface rather than merely
enumerating larger menus. Source truth, mask realization, utility and accounting
still need their own contracts.

**Invoice-limited learning:** a persistent mathematical instance is not a fresh
population sample. Same-instance cost transcripts can reveal a high-order
character unavailable to a single episode, but repeated queries and resetting
cost money. Before extending the sampler, ask whether a useful task needs a
whole character or can be decided from a cheaper, source-aware residual.

## Second pass: task observability rather than full-law reconstruction

The partial-monitoring comparison changes the question. For a finite source F,
let S stack indicators of possible invoices for the available private query
programs. Its row span, not its rank alone, determines which expected task
contrasts are identifiable. The s11 result identifies this span with restricted
degree-(H-1) Boolean polynomials when all permitted depth-H programs are
available. Therefore a loss contrast can be observable even when the law is
not. On affine sources, Fourier characters are identified modulo the dual code;
this is a compact way to check a task contrast, subject to the cost of finding
coset representatives. This is an adapter to established partial monitoring,
not a new general learning theorem.

**Cheap rejection of an overbroad impossibility claim:** if the target loss is
the same invoice that is observed, every program's own loss lies in its own
signal span. A finite supplied menu is an ordinary bandit problem. Failure to
recover parity or the full law does not imply inability to learn the cheapest
available program. Arbitrary unknown utility, a counterfactual beyond the
available cap, and observed execution cost are different tasks. Do not conflate
them. Computational dependence on an enormous policy menu remains unresolved.

**Constructive direction:** add a genuinely unobserved task loss and charge
separate invoice measurements. With strictly positive measurement prices and
free no-measurement actions, observers may be dominated at every outcome law
yet necessary to identify action differences. This produces the familiar
label-efficient/partial-monitoring two-thirds rate when observable, and linear
regret when not. A checked source or same-instance reset may move a concrete
invoice task across that boundary. The possible contribution is the exact
interface-dependent reduction and useful consequence, not the regret exponent.
Before building it, specify why the task loss is not already visible.

**Possible cost question, not yet a result:** for unit fees and a cap H, splitting
an n-bit parity into blocks of at most H-1 bits gives a same-instance transcript
with worst charge n+ceil(n/(H-1)). Each block uses a conditional marker. This
is an upper bound only. A matching lower bound needs to handle adaptive episode
selection and nonuniform stopping: a short invoice can depend on its last
queried answer, so replacing every realized episode length k by degree k-1 is
incorrect. Do not turn the earlier cap-based degree theorem into that false
pathwise argument. Defer a long proof until the measurement setting is useful.

## Third pass: numerical certificates and noisy values

**Numerical model library, early rejection as a new mechanism.** For a symmetric
positive-definite A with checked lower eigenvalue bound mu, approximate primal
u and dual z give residuals r=b-Au and s=c-Az. The corrected output
q=c^T u+z^T r obeys |c^T A^(-1)b-q|<=||r|| ||s||/mu. Independently useful
primal/dual models can therefore be combined. Cached matrix products can be
updated after low-rank changes, subject to a valid new coercivity bound.
This connects model fallibility and counterfactual changes, but the main
mechanism is standard goal-oriented reduced-basis error estimation and
offline/online decomposition. The source search found direct antecedents.
Do not build a new benchmark merely to rediscover that mechanism. Keep it as
a strong ordinary comparison if a genuinely different task adapter appears.

**Noisy invoices, constructive candidate within S05/S11.** Exact integer
invoices have implicitly free readout precision. Add independent measurement
noise with a stated common distribution. The event span may survive even
when finite-sample economics change substantially. For a marker of price d,
the invoice b+d*I plus mean-zero noise has an unbiased event estimator with
noise variance divided by d^2. Thus the cheapest marker need not minimize the
fee needed for a target precision. This gives a small mathematical question
before any large experiment: identify the noise assumptions, derive a valid
finite-budget bound, compare every available marker at the same cost, and
separate population identification from exact single-instance decoding.

**Precision trap to avoid.** A tiny outcome-dependent surcharge can reveal a
bit perfectly under noiseless exact real observation; that is a changed
interface, not a free cure for the last-answer blindness theorem. With noise,
its statistical cost must be included. Quantization alone also does not imply
a universal minimum signalling fee: an arbitrarily small increment can cross
a bin boundary if the fixed invoice is already sufficiently close to it.

## Fourth pass: a compact permission interface for implication models

Return to the query/repair branch with a different computational target.
Instead of another small arbitrary-CNF regret LP, consider a valid but partly
unknown configuration constrained by implications u=>v. An atomic patch toggles
a chosen set of bits. Queries reveal original bits. Can we compile exactly
which patches are safe after a receipt, without enumerating every source world?

On a strict implication DAG, unforced endpoints of an edge admit all of
00,01,11. Their patch bits must therefore both be zero: every nonzero pair
breaks the implication in some compatible world. A forced-zero predecessor
of an unknown node cannot be toggled; a forced-one successor of an unknown
node cannot be toggled. An unknown node with no unknown neighbor can be
toggled freely once those known boundary nodes remain fixed. Fully known
regions can be reconfigured by ordinary implication closure constraints.

This suggests an exact factorization: freeze unknown vertices incident to an
unknown edge; leave isolated unknown vertices freely togglable; optimize a
known-value closure problem with its boundary fixed. Strongly connected
components need to be collapsed first: inside an unknown equality component,
all bits may toggle together, unlike a strict unknown implication edge.

If the objective is a sum of rewards for accepted toggles, the known-region
problem becomes maximum-weight closure (ordinary minimum cut). It is not
general state-dependent utility or a solution of the entire query-planning
problem. The possible contribution is the source/receipt-to-permission adapter
and its cheap witness/checking contract. Next prove necessity and sufficiency,
compare configuration-update literature, and run a small exhaustive screen.

**Disposition after development:** the compiler and all-map extension passed
small exact screens. A homomorphism interpretation and established conformant
planning machinery substantially narrow the originality claim. Retain the
receipt-update specialization and source-change obligations as a candidate
adapter. Do not spend the rest of the recurrence optimizing its exposed fixtures.

## Fifth pass: resumable proof search and usefulness without truth labels

The earlier runtime work treats cutoff recipes and their purchased outcomes.
An additional interface distinction is whether unfinished computation can be
resumed, shared across strategies, or invalidated by a model edit. A timeout is
neither a false mathematical statement nor necessarily wasted work. Before
building another runtime learner, separate the stochastic distribution of
completion times from a deterministic prefix-preserving work trace. Candidate
questions: can a checked partial proof skeleton provide transferable lower
bounds on remaining effort; can continuation resources be priced without a
memoryless-runtime assumption; and can an advice portfolio retain a meaningful
robust overhead when executions share subproofs? Ordinary universal search,
algorithm portfolios, restart scheduling and online caching are mandatory
comparisons. A generic dovetail bound alone would repeat existing work.

**Early screen:** resumable deterministic dovetailing is already present in
s01/residual.md, and prefix evaluation/reuse in s02. Sharing valid subproofs
can only reduce a monotone scheduler's physical work, but a new claim needs
the shared-state interface and cost of maintaining it. Partial progress alone
cannot imply a generic remaining-runtime bound: two programs can have the
same observed prefix and arbitrarily different remaining delay. No further
generic restart/dovetail harness is justified by this pass.

## Sixth pass: diversity of proof supports with correlated premise errors

Several checked proofs of the same conclusion can be useful even when none
of their fallible premises is independently reliable. The event that all
supports fail is a transversal event in the premise hypergraph. Three pair
supports on three premises give a sharp 3p/2 bound instead of one proof's 2p,
without independence. Reliability LPs already cover the probability claim.
The [new note](proof_risk.md) therefore isolates a narrower operational use:
fix one global nonnegative risk weight vector, then check proposed actions
against it after arbitrary paid audits/proof acquisition. All accepted-action
failures lie in one weighted bad-premise event. This supports adaptive action
choice without treating marginal bounds as conditional guarantees. The
separation problem can be hard; defer implementation pending a useful duty.

## Seventh pass: which action interfaces make information useful?

The [affine edit note](affine_edits.md) gives a clean negative/positive pair.
For an initially valid affine target, no receipt can enable new XOR patches.
For retain/erase operations, a single observation can split the remaining
source into independent support blocks and enable 2^m selective erasures while
m bits remain unresolved. All unary maps compile to linear equations through
the existing code-conductor construction. This is a second structured adapter
alongside the binary-clause compiler. Its value is an explicit operational
distinction; the mathematical ingredients are already in coding theory.

## Eighth pass: exact priced inference through computation invoices

The earlier pathwise-degree attempt fails on arbitrary cheap stopping outcomes.
Following a maximum-invoice public path instead gives accepting cylinders that
stop before their last prospective query. Their Fourier supports must jointly
cover the target parity. Retaining the price of those prospective last queries
gives a lower bound that matches a simple reset-block construction, including
unequal coordinate prices and episode overheads. On a checked affine source,
the optimum is the least priced character representative in the relevant dual
coset. See [the derivation and finite oracle screen](parity_price.md).

This is a narrower mathematical strengthening of the invoice line, not a new
general side-channel or polynomial-method discovery. The three-bit exhaustive
oracle agrees in 14,280 comparisons. Priority and a useful complete-cost duty
remain open. Repeat purchases within an episode, expected rather than hard
cost, and noisy readout change the conclusion. A fallible affine model can be
used through one task-specific relation; calibrating that relation remains a
real obligation. Return to other families after preserving these boundaries.

## Ninth pass: random truncation of unfinished verification

Allow a model to predict an exact computation's eventual answer, then randomly
truncate verification and inverse-weight the observed residual on completion.
The result can be unbiased without assuming model accuracy. However, uniform
finite work over arbitrary completion times forces unbounded residual variance,
and a bounded [0,1] estimate unbiased for each fixed Boolean truth must already
be exact. Progressive partial predictions give the familiar telescoping
debiasing estimator. [The screen](censored_values.md) preserves the finite-trace
variance identity and its assumptions. Prior work already supplies the generic
mechanism, so no new harness is justified without a concrete application.

## Tenth pass: does decision structure change invoice price?

It does. Under the same private-reset contract, a conjunction can stop at its
first reported failure and needs only one marker charge on a worst-case path.
Parity must combine every block. The [conjunction derivation](and_price.md)
gives an exact unequal-price/reset-fee formula; its separate unrestricted
three-bit oracle passes 1,040 comparisons. With unit fees and no overhead,
full conjunction costs n+1 while full parity costs n+ceil(n/(H-1)), despite
both having ordinary worst-case query complexity n. This is an interface
consequence, not an assertion of a new short-circuit evaluation principle.

## Eleventh pass: characterize the cheap-update boundary

The binary-source projection lemma extends to arbitrary target scopes. A
minimal-forbidden-pattern argument also supplies its converse: exact pruning
by forced coordinates under every receipt and pair scope characterizes
2-CNF-definable sources. [receipt_width.md](receipt_width.md) records a broader
semantic hierarchy and the obstruction to substituting raw input clause width.
This sharpens the adapter contract using established prime-implicate structure;
it is a derivation, not a measured solver advantage or a new general logic.

## Twelfth pass: changed stakes and a concrete graphic inference adapter

Reconsidered active payoff/price interventions, but generic affine anchors and
unknown-stake nonidentification are already treated in P3-02 and s11. No new
mechanism was obtained from merely repeating that proposal.

A different constructive connection is the [graphic invoice adapter](graph_invoices.md).
At cap two, the parity price is additive in adjusted coordinate weights. On an
affine circulation source, one unknown edge can therefore be recovered at the
minimum of its direct invoice price and a separating-cut price. This supplies
short cut/flow certificates and remains exact after known receipts. General
parity targets encode MaxCut, so this is a scoped tractable duty. A small exact
screen passed; the underlying local-repair and cut-code methods are established.

If the graph equations are fallible, one cut relation has a sharp marginal-risk
bound using both cut sides. A precommitted trusted vertex region supports
adaptive cut choice with a shared unconditional error guarantee. Calibration,
source acquisition and full computation bills remain real obligations. This
connects task-specific model use to the price theorem without treating the
entire model as true or assigning a novelty claim to min-cut itself.

## Thirteenth pass: learn the useful relation and transport its error

[Paid relation calibration](relation_calibration.md) separates one-answer
marginal risk, confidence in an accepted rule, and any-error risk across many
uses. Its explicit graph law can have a perfectly useful cut relation while
the full model is wrong on every case. The mean-invoice formula includes the
calibration surcharge and preserves a corrected worst-versus-actual-cost draft
error. A small rational screen passes; the statistical ingredients are ordinary
binomial testing and selective prediction. [Error transport](error_transport.md)
then records why checked translations can share this error event across
adaptive counterfactual requests on one base instance, whereas arbitrary
overwrites can require a full-rank error check. Existing S17/S18/S19 machinery
already supplies much of this connection; no further harness is warranted yet.

## Fourteenth pass: compile the two-query observation interface

At private cap two, the second answer cannot affect the invoice. Every
informative episode is therefore dominated by a coordinate query with a
cheapest marker on one chosen answer. [cap_two.md](cap_two.md) reduces arbitrary
finite source/output tasks to ordinary outcome-dependent-cost decision trees,
including separate hard-worst and expected-cost recursions. An unrestricted
small oracle agrees. The reduction replaces private-program choices by a
smaller action menu; the remaining decision-tree search may still be expensive.
This strengthens the interface account rather than introducing another learner.

## Fifteenth pass: coupled sensing and structured model errors

Coupled reversible edits followed by sensing can expose a linear combination
that coordinatewise edits cannot. The pullback of a sensor through a linear
edit is simply a new measurement row. Generic proposals here reduce to active
sensing, circuit synthesis or the direct-contrast queries already in S01/S18;
no distinct useful contribution emerged, so no harness is built.

A more precise retained connection is [cycle-constrained errors](cycle_errors.md).
When truth and forecast satisfy the same checked graph equations, their error
vector is an even subgraph. A target edge's sharp risk under marginal error
caps is a min-cut capacity, witnessed by a distribution over cycles. This is
the cycle-space counterpart of s05's cut-space/T-join bound. It also exposes a
comparison trap: any cheap exact cut used in calibration is available to the
ordinary exact-answer baseline. Source constraints, risk caps and acquisition
prices must remain separate.

## Sixteenth pass: variable stopping and procedure randomness

[variable_invoices.md](variable_invoices.md) replaces fixed blocks by a prefix
stopping code. With unit query fees and no episode overhead it recovers every
hidden bit with expected surcharge n/(2^H-2)+O_H(1), while retaining the
optimal parity hard-worst bill n+ceil(n/(H-1)). The small unrestricted oracle
matches its mean at n=3 and 4, cap three. Parity-specific finishing reduces
episode costs further; a restricted hybrid DP is derived but not yet run.

A public random mask makes the same expected fees hold for every fixed input,
with exact answers on every tape. Thus no probabilistic belief about unresolved
mathematical truth is needed for this cost guarantee. The conventional masking
and variable-cost coding antecedents are explicit. Extra random bits and
controller work remain unpriced, and general expected optimality is open.

## Seventeenth pass: scores for randomized truth forecasts

Ben-David–Blais's forecasting-algorithm framework is directly relevant to
bounded deterministic truth questions. [forecast_scores.md](forecast_scores.md)
records a conditional contract for paid repeated procedures and a counterexample
to substituting population-average model performance: mean hs score 1/8 falls
to -3/16 when the same fallible forecast is sharpened twice. Independent
per-input experiments would instead give 15/64. The remaining obligation is
obtaining the relevant conditional score floor; confidence reports alone do
not provide it. Existing amplification and supermartingale machinery cover
the generic proposal, so a new harness is deferred.

## Eighteenth pass: information resolution changes the price

[quantized_invoices.md](quantized_invoices.md) replaces exact invoice readout
by known cost buckets. Visible thresholds give information capacities and a
matching padded-query construction. The equal-width case has a closed parity
price; the general monotone case is an ordinary integer capacity-cover DP.
A small unrestricted oracle passes while retaining actual hidden within-bucket
costs in its per-world budgets. Increasing the cap without crossing a new
visible threshold can be useless. This is a new interface-specific extension,
not a new coding principle or a measured complete-cost application gain.

## Nineteenth pass: combining counterfactual changes safely

[edit_consensus.md](edit_consensus.md) identifies the compiler's Horn form in
change-bit coordinates and an initial disjoint-block representation for safe
reversible edits of a binary source. Receipts can enlarge the menu while
destroying that group structure; additive exploitation can include independent
set optimization. A conservative intersection of certified edits is safe for
binary targets, but its exact single-world characterization was found already
in Schaefer's change-set theorem. This is useful imported structure for the
adapter, not a newly discovered consensus principle; no harness is built.

## Twentieth pass: exact labels versus economical statistical information

[information_price.md](information_price.md) tests whether partial transcripts
can beat the expected exact-answer fee per unit Fisher information in a parity-
tilted population. All 72 small finite panels tie the exact decoder; this does
not establish an all-size optimality theorem. The prefix's fresh-bit entropy
rate is explicit, but conditioning on earlier invoices can change the source.
An ordinary channel-capacity relaxation is therefore not automatically a
realizable private-query protocol. No statistical or regret benchmark is added.

## Twenty-first pass: pay for procedure randomness too

[hybrid_invoices.md](hybrid_invoices.md) supplies a finite DP mixing prefix
and parity-block episodes, with every-input expected bills and separate prices
for independent random choices and resets. A stronger control then changed the
comparison: fixed blocks can share one fair orientation coin. Four positive
n=100 gains against fresh-coin blocks disappear. [randomness_price.md](randomness_price.md)
preserves that correction and adds a limited-randomness prefix mask and an
outer selector. Query-only and some query-plus-reset gains survive; all are
constructed exact calculations and the ordinary realizations tie.

## Twenty-second pass: combine exact and fallible graphic answers

[risk_priced_cuts.md](risk_priced_cuts.md) turns each edge into a choice between
an exact answer and priced fallible predictors with supplied marginal risk
bounds. A Lagrange multiplier gives ordinary min-cut separation and a compact
cut/flow certificate for the declared fee/risk mixture class. A small example
attains a 1% error certificate for four acquisition/evaluation fee units, with
the matching dual bound checked. Calibration and controller costs remain open;
the example is not a complete-cost application or a new min-cut principle.

Next question: a prediction can also orient the marker so that an exact answer
costs c+m only when the prediction is wrong, and c otherwise. This could turn
ordinary online prediction guarantees directly into paid acquisition guarantees
while preserving zero error. Advice collection and computation must be charged;
free counterfactual feedback from unrun predictors would invalidate the claim.

[predicted_invoices.md](predicted_invoices.md) now supplies that adapter and an
ordinary exponential-weights transfer with all-advice overhead explicit. A
vector forecast also orients the prefix decoder, where mistakes' arrangement
and reset prices affect usefulness. No further learner harness is justified by
this elementary composition; accuracy alone cannot rank its total bill.

## Twenty-third pass: multiple sources without erasing their identities

[model_unions.md](model_unions.md) extends the permission interface to a
disjunction of binary models. Branch-aware receipt updates are exact; merging
their pair tables first loses constraints, as a three-bit parity example shows.
The exact disjunctive-closure antecedent was found immediately in knowledge
compilation. Retain the adapter and counterexample, without a new harness.

## Twenty-fourth pass: audit randomness instead of a prior on mathematics

[premise_audits.md](premise_audits.md) converts a bound on the number of false
premises into a shared release certificate for adaptive conclusions. A uniform
all-pass audit has a direct anytime proof; a small exact screen passes. General
confidence sequences for fixed populations are prior work. Disjoint-support
applications lose to checking one exact proof, so the next development question
is overlapping supports and the price of choosing which premises to audit.

## Twenty-fifth pass: price the verifier and discard weak proof routes

[weighted_audits.md](weighted_audits.md) gives a predictable weighted audit
martingale and exact independent-inclusion threshold formula. Correlated
sampling is stronger; its threshold optimum mixes adjacent sample sizes.
For graph path supports, a max-flow lower bound collapses reference-input
verification to randomized inspection of a cheapest path. Mere redundant paths
do not produce a large audit saving, so that application is parked early.

The attempted invoice lower bound failed first on an arbitrary source, then
on a reachable five-bit binary source. Preserve both counterexamples. The
surviving [transcript representation](transcript_sources.md) instead motivates
[binary-source parity inference and ordered search](binary_parity.md), a
different consequence rather than another attempt to rescue the potential.

## Twenty-sixth pass: choose an observation interface that preserves inference

[source_threshold.md](source_threshold.md) derives a tractability boundary.
Cap-three invoices preserve a binary logical source and polynomial local
permission compilation; cap four already makes forced-bit inference coNP-hard,
even with a known compatible witness. This combines the transcript adapter
with ordinary 2-SAT and a guarded 3-SAT reduction. It is retained as a small
mathematical synthesis, without another large experiment or a novelty claim
for the underlying complexity classification.

## Twenty-seventh pass: reject a tempting but weak composition

[audit_margin.md](audit_margin.md) checks whether broad random audits can
cheaply justify the binary permission source. Without additional logical
restrictions, an unprotected width-two clause has error distance at most two;
a 1% uniform-audit rule then needs roughly 90% of the premise population (99%
for distance one). A task-directed exact support check can be much cheaper.
Retain large-margin aggregate releases, but reject this generic source-admission
application before implementing it.

## Twenty-eighth pass: stable evidence through a changing current state

[lineage.md](lineage.md) composes original-source receipts with constants,
copies and complements. Current local permissions use the initial pair cache;
there is no expanding action history in this restricted representation. The
finite direct-world screen passes. Logical filtering and lazy regression are
close established antecedents, now explicitly recorded. The retained candidate
delta is the restricted cache composition and its charged operation bound.

## Twenty-ninth pass: cross-model consistency as error detection

[coherence_guard.md](coherence_guard.md) gives sharp cycle-guard error envelopes
from marginal component bounds, including the conditional-risk distinction.
A rational sharpness screen passes. One extra cycle relation can lower the
guaranteed joint-error bound by nearly half compared with a spanning path;
the underlying error-detecting-code principle is established. Fresh joint
calibration can make direct output calibration much stronger, so the generic
new-calibration application is rejected before benchmarking.

## Thirtieth pass: preserve counterfactual ties symbolically

[optimal_repair_source.md](optimal_repair_source.md) reduces implication/unit
repair to a minimum cut, then represents every optimum by residual-graph
implications. This supplies a compact source for all tied hypothetical
consequences. General binary repair remains hard. Compare the exact residual
source with the established minimum-cut lattice before developing further.

## Thirty-first pass: preserve near-optimal uncertainty without fake probabilities

[repair_margins.md](repair_margins.md) uses ordinary constrained min-marginals
to give each edit an exact model-repair tolerance. Binary targets and binary
mask constraints permit threshold feasibility by 2-SAT. A small cut-versus-
world screen passes. Positive slack immediately destroys the optimal-source
forced-coordinate update rule, even at arbitrarily small scales. This is a
restricted adapter to established min-marginals, not a new inference method.

## Thirty-second pass: rule out an attractive audit application early

[audit_integrality.md](audit_integrality.md) shows why randomized audit
selection cannot improve on randomly purchasing the cheapest complete
certificate when the relevant fractional hitting problem is integral. The
graph-coded one-target case has that property. A three-coordinate code shows
the boundary, with a small gain at stringent risk. Larger fingerprint-style
gains require a genuinely cheap structured query interface; do not hide that
computation price. No additional generic benchmark was built.

## Thirty-third pass: rely only on the part of a model the interface can use

[task_adequacy.md](task_adequacy.md) gives a maximal enlarged source preserving
all target projections after every permitted receipt: intersect the projections
on each target scope together with the observable coordinates. This can warrant
actions when the full model is false. Omitting the observable coordinates is
unsound; a three-variable example makes the difference explicit. A fixed-policy
leaf version can weaken the required event further. Forgetting and feature-model
slicing are close established antecedents. Retain the operational/adequacy
composition, without a claim of new forgetting machinery or free calibration.

## Thirty-fourth pass: use the source theorem to close one finite uncertainty

The exact 224,716-state binary-source count justifies one bounded continuation
of the earlier capped five-bit oracle. Both parity and full recovery finish at
97/16, equal to the prefix upper bound. This extends finite support through
five bits without rescuing the failed all-size proof. The stronger information
question now has a correctly scoped [cost-alphabet lower bound](invoice_entropy.md)
for full recovery, which remains below the prefix construction. It is ordinary
unequal-duration coding and cannot be applied to parity as though parity had
n bits of output entropy. No further oracle escalation is selected.

## Thirty-fifth pass: compose the service while exposing its real obligations

[scoped_service.md](scoped_service.md) joins local permission compilation,
binary receipt reuse, original-coordinate lineage and task-scoped model
adequacy. It leaves source preparation, physical observations and calibration
priced explicitly. [verification_targets.md](verification_targets.md) separates
elementary theorem confidence from the full useful-contribution event. No
complete-service or independent confirmation count is claimed.

## Thirty-sixth pass: move beyond Boolean worlds

[ordered_sources.md](ordered_sources.md) derives exact projection pruning for
median-closed sources under interval receipts and gives a nonconvex failure
example. [temporal_receipts.md](temporal_receipts.md) specializes this to
prepared difference constraints, O(n) per bound and O(1) requested difference
queries. A finite world/closure screen passes. [temporal_adequacy.md](temporal_adequacy.md)
then permits an endpoint edit despite false intermediate timing claims, while
ordinary endpoint modeling remains an equal or cheaper strong comparator.

## Thirty-seventh pass: joint model adequacy and the public observation boundary

[union_adequacy.md](union_adequacy.md) shows that several models can be jointly
adequate without any one being adequate, and checks the strict distinction on
a small finite panel. A cheap argument then rejects an easy superiority claim:
per-task model selection matches the bound available from marginal warrants.
[observable_adequacy.md](observable_adequacy.md) gives the shared public
transcript/feature envelope and an explicit private-invoice-answer pitfall.
Abstract interpretation and disjunctive representations are close established
antecedents. These are connections within the portfolio, not new families per
note or a mandate for another large benchmark.
