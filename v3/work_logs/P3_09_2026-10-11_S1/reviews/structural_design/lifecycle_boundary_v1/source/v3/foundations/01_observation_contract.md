# P3-01 — what an improvement claim must observe

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Scope: requirements for interpreting the five questions. These records do not
select a learner, numerical threshold, evaluation population or P3-09 freeze.
The companion [machine-readable contract](01_contract.v1.json) is an index of
semantic obligations, not an implemented scheduler or a validated software API.

## 1. An event record and an evidence record answer different questions

A report has a request, meaning, information history and creation event. A
mathematical claim additionally needs an evidence contract. A trustworthy
timestamp cannot make an unsupported number a certified bound, while a correct
proof produced later cannot turn an earlier guess into an informed forecast.

Keep the following identifiers separable: theory, interpretation, program,
checker, admitted source, objective, resource model, method and their versions.
Not every operation changes every identifier. A change in stakes can preserve
truth while changing the preferred action; changing the program can invalidate
both the label and its proof; changing a checker can require renewed validation
without changing the underlying mathematical statement.

The core event order is request, initial report, optional computation/receipt
events, decision report, and later feedback. A response received before a
request may legitimately be used if its meaning and dependencies cover that
request. A response retained under a different meaning requires a checked
translation. The resource ledger records this reuse on its actual terms.

For labels, distinguish generation from accessibility. An evaluator may have
computed a hidden answer before the method runs; that alone is not exposure.
Conversely, a label encoded in a visible filename or cache can be accessible
without an explicit feedback event. The contract therefore names visible
metadata and permitted cache access as well as receipt timestamps.

Record whose access occurred: evaluator, method, designer or tuner. An
evaluator-only answer can influence a method indirectly if a designer sees it
and selects parameters, features or advice from it. That history changes the
later held-out claim even when the method never receives a label column.
This is a future exposure requirement; all P3-01 examples are already declared
development data and no final evaluation has been created here.

## 2. Three endpoints for a computation policy

| Endpoint | What it measures | What it cannot establish by itself |
|---|---|---|
| Report before optional acquisition | Quality at the initial report boundary, charging the report algorithm | That the algorithm learned a recurring pattern rather than directly solving the request |
| Report after paid acquisition | Quality after the method's observed computations | Anticipation before those acquired results |
| Final decision with its resource account | Task consequence and expense of the complete policy | Accuracy or calibration on every unresolved statement |

The first row is intentionally operational. An initial reporting algorithm may
itself be a fast exact solver, a lookup in a legitimately acquired cache, an
online predictor or a mixture. All can be admissible. Calling its output a
pre-acquisition forecast does not identify the mechanism. An empirical learning
claim needs a stated training/update history and an appropriate held-out
comparison; a theorem-level learning claim needs its proof and quantifiers.
An algorithmic shortcut claim needs its cost and correctness argument. P3-01
does not infer either mechanism from output accuracy.

For policy comparisons, hold initial access and prices fixed while allowing
the chosen computations to differ. For inference comparisons on a common
history, state who paid to create it and use a common cost convention.
[CB01](01_composition_boundaries.md) gives the explicit purchase/replay
separator. These are distinct questions worth measuring separately; they need
not rank methods in the same order.

## 3. A resolved subset is not the whole question family

Every issued request remains in the cohort record, including abstention,
timeout, execution failure, conflict, stale output and unresolved feedback.
Record whether feedback was exogenous, action-selected, purchased, or supplied
only to the evaluator. A forecast score has a denominator: which reports were
issued, which answers were available for scoring, and which selection rule
formed that scored set.

Repeated requests also require a declared unit. Reusing an old answer to the
same versioned question can be a real efficiency gain. Counting each repeat as
a newly learned theorem would be a different claim. Neither deleting repeats
nor including them silently is justified. The later challenge specifies query
identity, sampling and amortization; this contract only requires their disclosure.

If only a selected action's loss is observed, the losses of unchosen actions
are missing. A supplied simulator may expose them for an evaluator, but the
method still has its announced information interface. Regret to a fixed expert,
an adaptive ordinary policy and a free per-request oracle are separate endpoints.
If the relevant comparator loss is not observed or justified, report that
endpoint as unestablished rather than filling it with a modeled estimate.

## 4. Typed numerical reports and their bridge obligations

An exact loss under a stipulated model, a posterior mean, a learned point
forecast, a conditional deterministic enclosure, and a statistical interval
are distinct report types. A point or interval's numerical shape does not
identify its evidential meaning. Each report names its target family, units,
assumptions and the evidence that would make a stronger reading valid.

The request also records the consumer's decision criterion and commitment
timing, including information available at choice and permission to reoptimize.
A pure value query can mark the consumer decision service inapplicable.
Minimizing expected loss, worst-case expected loss and worst-case
regret can disagree on the same numerical family. A root commitment and a
fresh choice after an observation are different policy services. The shared
tree example [CB05](01_composition_boundaries.md#cb05-a-tree-recursion-can-discard-shared-constraints)
shows why neither criterion nor timing can be inferred from the word
“robust.” Later comparisons hold the announced service fixed.

For example, the Gaussian scale calculation linked in S21 produces a posterior
variance under a model. It does not supply an absolute error bound for the
particular deterministic answer. A checked inequality between two posterior
means remains an inequality between those estimates. To warrant their ordering
as actual task costs, supply the additional error/adequacy bridge described in
[CB03](01_composition_boundaries.md). If the compared actions were selected
using the data, that bridge must cover the selection.

For counterfactuals, the selection domain is equally material. A point can be
the value of a chosen repair while other equally ranked repairs disagree.
An exact optimum rank, a complete characterization of tied consequences and
empirical identification of the supplied dependency model need different
evidence. The [response contract](../work_logs/P3_01_2026-10-07_S1/reviews/counterfactual_status_stress.md)
gives the cross-field conditions. Do not use numerical agreement to erase
those distinctions.

## 5. How this constrains the five questions

| Question | Minimum discriminating record |
|---|---|
| Q1 | Query meaning, visible information, resolution bridge, update order and status before/after the computation |
| Q2 | Original antecedent, operation, preserved interpretation, selected family, coverage and consequence meaning |
| Q3 | Shared initial library/access, each policy's acquisitions, model applicability, action loss and actual resource use |
| Q4 | Immutable reports, delayed/selected feedback, exact scoring or decision comparator, duty-specific assumptions and any source theorem imported |
| Q5 | Known loss functions and units, retained information, requested decoder service and the admissible family over which recovery is claimed |

These fields make improvement, equivalence and failure claims reviewable.
They do not require every later method to solve the unrestricted problem.
A method may return a useful restricted answer or an honest failure status;
the report must state the service it actually supplied. The contribution
obligation still requires evidence beyond combining these records by name.

## 6. Revision changes which refinement question is being asked

Use version changes to identify the affected object, rather than treating
every update as a new truth value or every changing number as failed learning.

| Change | What may remain valid? | What must be reconsidered? |
|---|---|---|
| Additional sound evidence for the same query | Query meaning, earlier reports as historical objects, and correctly retained premises | Newly eligible hard conclusions and dependent current estimates |
| Withdrawal of an admitted premise | The old conditional proof and its original meaning | Whether its assumptions still warrant current use; no automatic refutation of its conclusion follows |
| New task loss or resource price | The interpreted mathematical answer and appropriately retained probability/dependence information | Cost expressions, action ordering, feasibility and the value of another computation |
| Changed program or interpretation | Historical claims about the old version | New query identity and any proof/forecast transport; unchanged display text is insufficient |
| Changed forecasting procedure | Previously saved reports and labels | The self-model, resource/performance profile and guarantees for the new procedure |

### Perfect tracking need not be a convergent numerical sequence

Consider versions of a trivial program that alternately return zero and one.
For each version, the request asks whether **that version** returns one. An
exact forecaster returns `0,1,0,1,...`; its error is zero but its numerical
reports do not converge. These are different versioned queries. Neither
fixed-query convergence nor a theorem about a fixed deductive process is
violated. The example is a direct trace calculation, not a new learning result
or a claim that any difficult program is easy to inspect.

Similarly, hold a forecast `p=7/10` fixed and alternate the known failure stake
between ten and one hundred. The corresponding expected costs are three and
thirty. A changing value can correctly track the changing task while the
epistemic forecast remains unchanged. Comparing unnormalized numerical costs
across these objectives as if they were estimates of one fixed quantity would
test the wrong proposition.

A later convergence claim therefore specifies an eventually fixed query,
meaning, objective and process, or supplies a different tracking statement
with its own changing-target comparator. An empirical sequence of favorable
updates alone supplies neither. Changes in what the method has computed also
remain separate from a change in what a fixed mathematical query means.

### Current warrant and old conditional truth are different statuses

Suppose an old certificate proves `Gamma_A |- phi` and cites an assumption
that is no longer admitted. The certificate remains evidence for the old
conditional judgment. It need not warrant `Gamma_B |- phi`, and removing its
support does not establish `Gamma_B |- not phi`. A sound current-use interface
can mark it stale, search for another support, or transport it under an explicit
bridge. Treating all three outcomes as a new probability of zero would lose
their meanings.

This is why the fixed-theory LI comparison and the source-revision extension
remain separate in the main contract. The numerical carrier alone does not
choose a prior after withdrawal, establish a corrected conditional-market
theorem, or decide which assumptions are appropriate for deployment. P3-03,
P3-05 and P3-06 own those restricted procedures and guarantees.
