# Core Signature and Notation

Status: Task 7 formal specification, version 0.1  
Date: 2026-07-11  
Scope: syntax and typing only; license truth conditions begin in Task 8

> **Task 11A interface notice.** This historical signature predates mandatory profile indexing. Read its full bare `Lic` constructor as the strong named profile `Lic_{P_full^8}`, not as the universal meaning of licensing. Current-license and active-set views are profile-indexed. See [`05a_integration.md`, §16](05a_integration.md#16-repairs-to-completed-interfaces); Task 13 will consolidate the notation.

> **Checkpoint A1 compactness notice.** The inventory below is a typed elaboration and implementation schema, not the intended primitive signature of the paper. Task 13 must compress the mathematical core to use plans, reliance/evaluation contexts, and finite epistemic states, with target worlds as a semantic index; the remaining types survive as dependent fields, witnesses, derived objects, or extensions. Do not reproduce the 28-sort table as the paper's core ontology.

## Executive decision

This Task 7 elaboration uses a **many-sorted, finite-stage language with typed records and dependent task interfaces** to prevent invalid combinations. Its objects are not truth degrees. It names agents, stages, versioned models, typed cases and domains, evaluation specifications, evidence records, libraries, search traces, costs, fallbacks, and provenance—but Checkpoint A1 no longer treats every named record type as primitive in the paper-level calculus.

A domain is neither always a set nor always a probability distribution. It is a typed **evaluation scope** that can expose several compatible views:

```text
carrier of admissible cases
+ optional distribution or sampling process
+ one task or a task family
+ environmental/measurement conditions
+ representation/frame
+ domain provenance.
```

Loss and risk aggregation are deliberately not built into domain identity. They are combined with a domain in an evaluation specification:

```text
q = Eval(D, L, rho).
```

The same domain can therefore be evaluated by expected loss, worst-case loss, tail risk, regret, or a vector of criteria without pretending that these are the same judgment. A tolerance `epsilon` lives in the ordered risk space selected by `q`; it need not be a scalar.

The canonical full judgment will eventually have the form

```text
Lic_{a,t,b}(m; q, epsilon, alpha, F, Delta, K, c, sigma, p | R).
```

Task 7 fixes the types and well-formedness conditions of this expression. Task 8 will say when it obtains.

## 1. Metalanguage and conventions

### 1.1 Kind of formal language

The intended foundation is a many-sorted first-order signature augmented by:

- finite records;
- partial functions whose domains of definition are explicit;
- dependent sorts such as `Case(tau)` and `Pred(tau)`;
- preordered value spaces rather than an assumed global real line;
- finite stage-indexed structures.

This is a specification language, not a commitment to a particular theorem prover. It can later be encoded in dependent type theory, many-sorted first-order logic, a proof assistant, or typed code.

### 1.2 Typographic conventions

- Roman lowercase letters denote elements: `a,t,m,x,D,q,R,K`.
- Sans-serif names denote sorts: `Agent`, `Stage`, `Model`, `Domain`.
- Calligraphic capitals normally denote finite collections or structured spaces: `K`, `R`, `Q`.
- Bold lowercase values may denote vectors: `epsilon`, `c`, and `r` are written in bold when necessary.
- `?` marks an optional record field, not logical uncertainty.
- `perp` denotes absence/undefined, not falsehood.
- `preceq_Q` denotes the preorder in a typed value space `Q`.
- `id(o)` and `ver(o)` denote an object's stable identifier and version.

### 1.3 Three equality notions

The calculus must not use one equality sign for every purpose.

1. `o_1 = o_2`: identical typed records, including identity/version where relevant.
2. `o_1 equiv_ext o_2`: extensionally equivalent for a stated interface and case scope.
3. `o_1 equiv_q o_2`: indistinguishable under evaluation specification `q` and a stated record.

Two differently derived or versioned models can be extensionally equivalent while remaining different library entries. Two domains can have equal carriers while differing in distributions, tasks, frames, or provenance.

## 2. Typed elaboration inventory

The elaborated schema names the following sorts. Task 13 must recover the compact `E,Q,S` reduct described in the notice above and justify any type retained as primitive:

| Sort | Notation | Informal role |
|---|---|---|
| agent | `a in Agent` | evaluator, reasoner, or certifying system |
| stage | `t in Stage` | finite evidential/revision state |
| budget | `b in Budget` | bounded search, compute, data, time, or attention resources |
| task | `tau in Task` | typed predictive or decision problem |
| case | `x in Case(tau)` | one evaluable input/history/situation for task `tau` |
| outcome | `y in Out(tau)` | observed or target outcome |
| prediction | `yhat in Pred(tau)` | model output to be scored or acted upon |
| action | `u in Act(tau)` | available action, when the task is decisional |
| theory framework | `Theta in Theory` | vocabulary and family of admissible model structures |
| model | `m in Model` | versioned evaluable predictor, simulator, or policy |
| frame | `f in Frame` | coordinates, units, idealizations, and encodings |
| domain | `D in Domain` | typed evaluation scope over cases/tasks |
| loss specification | `L in LossSpec` | pointwise discrepancy or decision loss family |
| risk specification | `rho in RiskSpec` | aggregation/certification target over a domain |
| evaluation specification | `q in EvalSpec` | compatible triple `(D,L,rho)` |
| risk value | `r in RiskVal(q)` | result in `q`'s ordered risk space |
| tolerance | `epsilon in Tol(q)` | admissible risk boundary typed by `q` |
| confidence/calibration spec | `alpha in CertSpec` | statistical meaning and required guarantee |
| fallback | `F in Fallback` | status quo, reject, defer, model, policy, or information action |
| improvement requirement | `Delta in Improve(q,F)` | required advantage over fallback |
| cost profile | `c in Cost` | resource, safety, latency, or interpretability criteria |
| evidence event | `e in EvidenceEvent` | observation, evaluation, correction, or decision event |
| record | `R in Record` | finite versioned event structure available at a stage |
| library | `K in Library` | finite stage-local collection of model entries |
| search request/trace | `sigma in Search` | bounded retrieval/evaluation history |
| provenance object | `p in Provenance` | auditable dependency graph and source references |
| selection policy | `pi_sel in Selector` | choice/mixing/abstention rule after licensing |
| bridge | `beta in Bridge` | typed relation between model outputs or frames on overlap |

Not every sort appears in every compressed formula. Omission is permitted only after the missing object is fixed by an explicit context.

## 3. Agents, stages, and budgets

### 3.1 Agents

`Agent` is a nonempty sort. An agent can be a person, institution, algorithm, or composite evaluation process. No rationality axiom is built into membership in `Agent`.

Each license judgment is indexed by its certifier:

```text
a : Agent.
```

Different agents may possess different records, libraries, budgets, losses, and tolerances while evaluating the same model/domain pair.

### 3.2 Stages

`Stage` carries a preorder

```text
preceq_Stage : Stage x Stage -> Bool.
```

`t preceq_Stage t'` means that `t'` is an admissible later or informationally extended stage relative to `t`. Antisymmetry and linearity are not assumed: concurrent or differently branched inquiry states may exist.

For each agent-stage pair there are partial accessors:

```text
record   : Agent x Stage -> Record
library  : Agent x Stage -> Library
budget   : Agent x Stage -> Budget
```

When convenient:

```text
R_{a,t} = record(a,t)
K_{a,t} = library(a,t)
b_{a,t} = budget(a,t).
```

Every object actually available at a stage is finite or finitely represented. The stage order does not imply that current licenses are monotone.

### 3.3 Budgets

A budget is a typed resource vector:

```text
b = <time?, compute?, memory?, samples?, queries?, money?, attention?>.
```

`Budget` carries a componentwise or application-defined preorder `preceq_Budget`. A missing component is not infinity; it means that the component is outside the current budget schema.

Budget is distinct from realized cost. `b` limits a search or evaluation; `c` records properties/costs of using a model or fallback.

## 4. Tasks, cases, histories, outcomes, and actions

### 4.1 Task records

A task is a typed record:

```text
TaskSpec tau = <
    id,
    input_type,
    prediction_type,
    outcome_type,
    action_type?,
    environment_type?,
    horizon?,
    perspective?,
    provenance
>.
```

It determines dependent sorts:

```text
Case(tau), Pred(tau), Out(tau), Act(tau).
```

For a purely predictive task, `Act(tau)` may be absent. For a decision task, predictions and actions remain different types even if the implementation uses one vector for both.

### 4.2 Cases

A case is the smallest object on which the relevant model interface can be evaluated:

```text
x : Case(tau).
```

A case may be a current state, a state-action pair, a trajectory prefix, an experimental configuration, a query with measurement conditions, or a structured history. “Point” always means one element of `Case(tau)`, not necessarily one Euclidean coordinate vector.

### 4.3 Histories and information states

Histories form a distinguished dependent sort:

```text
h : Hist(tau).
```

There may be typed maps

```text
observe_tau : Hist(tau) -> Case(tau)
compress_eta : Hist(tau) -> InfoState_eta(tau).
```

No compression is assumed sufficient by definition. If a task is partially observable, a belief state or other information state becomes a case only after its sufficiency conditions are stated. The full history is always representationally available in principle but may be computationally unusable.

### 4.4 Targets and predictions

An evidence record may partially supply targets:

```text
target_R : Case(tau) ⇀ Out(tau).
```

`⇀` denotes a partial function. A case can be evaluable by simulation, bounds, pairwise preferences, or decision outcomes even when no single target outcome is recorded.

Predictions are task-typed:

```text
yhat : Pred(tau).
```

The signature does not assume that `Pred(tau) = Out(tau)` or that either is a real vector.

## 5. Theory frameworks, models, frames, and model identity

### 5.1 Theory frameworks

A theory framework is an intensional record:

```text
Theta : Theory = <
    id,
    vocabulary,
    state_variables,
    structural_principles,
    admissible_model_family,
    admissible_frames,
    provenance
>.
```

It is normally too underspecified to receive an empirical loss directly.

### 5.2 Instantiated models

A model is a versioned evaluable record:

```text
m : Model = <
    model_id,
    version,
    theory_ref?,
    supported_tasks,
    prediction_interfaces,
    native_frame,
    parameters_or_rules,
    resource_profile,
    construction_record,
    provenance
>.
```

For each supported task `tau`, a model provides a partial interface

```text
predict_{m,tau} : Case_m(tau) ⇀ Pred_m(tau).
```

Translations may be required to connect the case and prediction types of the task to the native types of the model.

The core empirical license applies to `m : Model`, not directly to `Theta : Theory`. A prose reference to “Newtonian theory” must be refined in formal examples into an instantiated model, frame, parameter convention, and output interface.

### 5.3 Frames and translations

A frame records representational choices:

```text
f : Frame = <
    id,
    coordinates,
    units,
    idealizations,
    case_encoder,
    prediction_decoder,
    validity_conditions,
    provenance
>.
```

Typed partial maps include:

```text
enc_f : Case(tau) ⇀ Case_m(tau)
dec_f : Pred_m(tau) ⇀ Pred(tau).
```

The externally scorable prediction is

```text
pred(m,f,x) = dec_f(predict_{m,tau}(enc_f(x)))
```

when every component is defined.

### 5.4 Identity is versioned and intensional

Model identity is not quotienting by behavior. In general:

```text
id(m_1) != id(m_2)
```

can coexist with

```text
m_1 equiv_ext m_2 on D.
```

This preserves differences in derivation, ontology, version, cost, robustness, and provenance. Behavioral equivalence may be defined later relative to a task/domain/evaluation specification.

## 6. Domains as typed evaluation scopes

### 6.1 Canonical domain record

A domain is:

```text
D : Domain = <
    domain_id,
    version,
    tasks,
    carrier,
    measure_or_sampler?,
    conditions,
    frame,
    membership_procedure?,
    coverage_evidence?,
    provenance
>.
```

The fields have the following types.

#### Task family

```text
tasks(D) : nonempty finite/indexed subset of Task.
```

A single-task domain is the ordinary and preferred initial case. A multi-task domain is permitted through a dependent disjoint union.

#### Carrier

```text
carrier(D) subseteq Sum_{tau in tasks(D)} Case(tau).
```

`Sum` is a dependent disjoint union, so the task tag is never lost. Membership is written

```text
(tau,x) in D
```

or simply `x in D` when `tau` is fixed.

#### Measure or sampler

The optional field is either a probability measure or a sampling process:

```text
mu_D : Probability(carrier(D))
```

or

```text
samp_D : Seed -> Stream(carrier(D)).
```

A sampler does not automatically define an i.i.d. distribution; its stochastic assumptions belong in its provenance/evidence.

#### Conditions

```text
conditions(D) : ContextPredicate.
```

This can state environmental, measurement, intervention, horizon, resource, or idealization conditions not carried by the raw case.

#### Frame

```text
frame(D) : Frame.
```

The frame makes domain membership and model outputs comparable. Domains with different ontologies or coordinate systems require a bridge/translation before set operations or risk comparison are meaningful.

### 6.2 The four main domain views

One record supports four distinct views:

1. **Set view:** `SetView(D) = carrier(D)`.
2. **Distribution view:** `DistView(D) = mu_D` when defined.
3. **Sampling view:** `SampleView(D) = samp_D` and its recorded sample/evidence protocol.
4. **Task-family view:** `TaskView(D) = tasks(D)` plus task-tagged cases.

No view is privileged universally. A risk specification declares which views it requires.

### 6.3 Supplied, certified, and induced domains

These are distinct constructors/statuses:

```text
Supplied(D,p)
CertifiedDomain_{a,t}(m,D,q,alpha | R)
InducedRegion_{a,t}(m,q,epsilon | R)
```

- `Supplied` means the scope is fixed independently of the current model score.
- `CertifiedDomain` is a later judgment backed by evidence.
- `InducedRegion` is a derived set such as `{x : s_m(x) >= 0}`.

The latter two are not primitive domain identity conditions. Treating an induced neural region as the domain would otherwise make domain adequacy circular.

### 6.4 Domain operations are partial and typed

Possible constructors include:

```text
restrict(D,P)
intersect(D_1,D_2)
union(D_1,D_2)
pushforward(D,f)
condition(D,C)
pointDomain(tau,x)
```

They are defined only when task tags, frames, conditions, and measure conventions are compatible or an explicit translation/reconciliation is supplied.

For example, equal carrier sets do not determine the distribution of `intersect(D_1,D_2)`. A union of distributions requires mixture weights or a different sampling rule. The set operation and measure operation must be recorded separately.

### 6.5 Domain equality and overlap

Define:

```text
D_1 equiv_car D_2 iff carrier(D_1) = carrier(D_2)
D_1 equiv_dist D_2 iff equiv_car and mu_{D_1} = mu_{D_2}
D_1 equiv_scope D_2 iff all task/frame/condition/carrier fields agree
```

An overlap is initially a carrier relation:

```text
Overlap(D_1,D_2) iff carrier(D_1) intersect carrier(D_2) != empty
```

but bridge and comparison claims additionally require compatible task and output interfaces.

## 7. Loss, risk, evaluation specifications, and tolerance

### 7.1 Loss specifications

A loss specification is a task-indexed family:

```text
L : LossSpec = <
    id,
    tasks,
    local_loss_family,
    local_value_spaces,
    orientation,
    scaling,
    provenance
>.
```

For each task `tau`:

```text
ell_{L,tau} : Pred(tau) x Out(tau) x Case(tau) -> Q_{L,tau}.
```

For decision loss, the inputs may include actions, transitions, or a comparator policy. This is represented by a specialized `LossSpec`, not by pretending that every loss is prediction error.

`orientation(L)` records whether smaller or larger is better. The canonical convention converts all risk comparisons to **smaller is better**. Utility-like quantities must be transformed explicitly, for example by regret or negative utility.

### 7.2 Risk specifications

A risk specification states how pointwise quantities become a domain-level object:

```text
rho : RiskSpec = <
    id,
    required_domain_views,
    aggregation_rule,
    risk_space,
    preorder,
    estimation_protocol?,
    provenance
>.
```

Examples include:

```text
Expected(mu_D)
WorstCase(carrier(D))
Quantile(mu_D,gamma)
CVaR(mu_D,gamma)
Empirical(sample,weights)
Regret(comparator,dynamics)
Vector(rho_1,...,rho_k).
```

The associated value space is

```text
Q_q = RiskVal(q)
```

with preorder `preceq_q` oriented so that `r_1 preceq_q r_2` means “`r_1` is no worse than `r_2`.” It may be `R_bar`, `R_bar^k` under Pareto order, intervals, or another ordered set.

### 7.3 Evaluation specifications

An evaluation specification is a compatible triple:

```text
q : EvalSpec = <D,L,rho>.
```

Well-formedness requires:

```text
tasks(D) subseteq tasks(L)
required_domain_views(rho) are defined on D
outputs of L match predictions/outcomes of tasks(D)
rho accepts the local value spaces produced by L.
```

Use accessors:

```text
dom(q), loss(q), risk(q), Q_q, preceq_q.
```

The population/target risk term is written

```text
Risk_q(m)
```

or fully

```text
Risk_{rho,L}(m,D).
```

An evidence-derived estimate and a certified bound are separately written

```text
RiskHat_{a,t,q}(m | R)
RiskBound_{a,t,q,alpha}(m | R).
```

Task 8 will define the relation among target risk, estimates, and certificates. The undecorated `Risk_q(m)` must not be used for an empirical estimate.

### 7.4 Tolerances

A tolerance is typed by its evaluation specification:

```text
epsilon : Tol(q) = Q_q.
```

The basic admissible down-set is

```text
Down_q(epsilon) = { r in Q_q : r preceq_q epsilon }.
```

Therefore adequacy will later compare

```text
Risk_q(m) preceq_q epsilon.
```

This covers:

- scalar `Risk <= epsilon`;
- componentwise vector thresholds;
- interval upper-bound comparisons;
- partial-order/Pareto admissibility.

If the application uses a more general acceptable set than a principal down-set, replace `epsilon` by

```text
A_q : AdmissibleSet(Q_q)
```

and write `Risk_q(m) in A_q`. The paper should introduce scalar `epsilon` first, then state this generalization.

`epsilon` is never typed as a probability that the model is false.

## 8. Confidence, calibration, and statistical specifications

`alpha` is not always one real number. Use:

```text
alpha : CertSpec = <
    interpretation,
    level?,
    sidedness?,
    target?,
    sampling_assumptions?,
    calibration_scope?,
    estimator_or_bound?,
    provenance
>.
```

Possible interpretations include:

- frequentist confidence/coverage;
- Bayesian posterior probability;
- conformal marginal or conditional coverage;
- deterministic certified bound;
- empirical calibration criterion;
- no statistical certificate (`NoneCert`).

The symbol `alpha` may denote the level only when the rest of `CertSpec` is fixed. A statement such as “confidence 0.95” is ill-typed without its interpretation and target.

## 9. Fallbacks, improvement requirements, costs, and selectors

### 9.1 Fallbacks

A fallback is a tagged sum:

```text
Fallback =
    ModelFallback(Model)
  + PolicyFallback(Policy)
  + ActionFallback(Act(tau))
  + Reject
  + Defer(AgentOrSystem)
  + InformationAction(Act(tau))
  + StatusQuo(PolicyOrProcess)
  + NoFallback.
```

The tag is semantically important. Rejecting a prediction, doing nothing, preserving a status quo, and gathering information can have different outcome distributions and costs.

### 9.2 Improvement requirements

`Delta` is typed by a common comparison protocol between candidate and fallback:

```text
Delta : Improve(q,F).
```

Its value may be additive, multiplicative, vector-valued, or a down-set requirement. It is not automatically measured in the same space as hard risk tolerance unless the comparison protocol establishes that fact.

The fallback-induced scalar threshold

```text
epsilon_F = J_q(F) - Delta
```

is well-typed only for an additive scalar cost `J_q` with smaller values preferred.

### 9.3 Cost profiles

A cost profile is:

```text
c : Cost = <
    predictive_or_decision_cost?,
    compute?,
    latency?,
    memory?,
    monetary?,
    safety?,
    robustness?,
    interpretability?,
    provenance
>.
```

Costs carry an application-specific preorder. The calculus does not assume a universal scalarization of accuracy, safety, speed, and interpretability.

### 9.4 Selection policies

A selector acts only after license information is available:

```text
pi_sel : Selector
select(pi_sel, ActiveSet, q, c, F, R) ->
    SelectedModel
  + Mixture
  + FallbackDecision
  + Abstain.
```

Selection is not part of model identity and does not erase unselected licenses.

## 10. Evidence events and finite-stage records

### 10.1 Evidence events

`EvidenceEvent` is a tagged sum including:

```text
Observation(case,outcome,method)
Evaluation(model,eval_spec,result,uncertainty)
ModelAdded(model_ref)
ModelVersioned(old_ref,new_ref)
DomainProposed(domain_ref)
DomainRevised(old_ref,new_ref)
SearchRun(search_ref)
LicenseIssued(license_ref)
LicenseWithdrawn(license_ref,reason)
SelectionMade(selection_ref)
Correction(target_event,replacement_or_note)
Retraction(target_event,reason)
ExternalClaim(content,source).
```

An event is not automatically trustworthy evidence merely because it is recorded.

### 10.2 Records

A record is a finite versioned event structure:

```text
R : Record = <
    record_id,
    version,
    finite_events,
    temporal_or_dependency_order,
    correction_links,
    admissibility_annotations,
    provenance
>.
```

Corrections and retractions do not silently delete old events. They add typed links that change which event views are admissible for a later judgment while retaining the audit trail.

Define partial views:

```text
Raw(R)       : all recorded events
Admissible(R,alpha,q) : events permitted by a stated protocol
Data(R,q)    : evaluation data relevant to q
History(R,o) : provenance/history of object o.
```

`R_{a,t}` is finite at every stage. A later record can extend, correct, branch from, or merge earlier records. Record extension does not imply monotonicity of licenses.

## 11. Libraries and model entries

### 11.1 Library entries

A library entry is:

```text
k : LibraryEntry = <
    model_ref,
    version,
    availability_status,
    supported_tasks,
    known_domain_refs,
    evaluation_refs,
    cost_profile,
    provenance
>.
```

Availability statuses include at least:

```text
active, archived, deprecated, unavailable, quarantined.
```

Archived and deprecated do not mean false or useless.

### 11.2 Libraries

A library is a finite versioned map:

```text
K : Library = <library_id,version,finite_entries,provenance>.
```

Membership is intensional:

```text
m in K
```

means that a versioned entry referring to `m` exists. It does not imply that `m` was evaluated on the current domain, is licensed, or is selectable.

Use:

```text
Active(K), Archived(K), Retrieved(sigma), Evaluated(sigma,q).
```

The full model universe `Model` is never identified with a finite library `K`.

## 12. Search requests and traces

A search object records both a request and what happened:

```text
sigma : Search = <
    search_id,
    agent,
    stage,
    query,
    source_libraries,
    retrieval_procedure,
    evaluation_procedure?,
    budget,
    scanned_or_generated_set,
    retrieved_set,
    evaluated_set,
    stopping_reason,
    failures_or_timeouts,
    provenance
>.
```

Typed accessors include:

```text
Scanned(sigma) subseteq K
Retrieved(sigma) subseteq Scanned(sigma)
Evaluated(sigma,q) subseteq Retrieved(sigma).
```

For generative search, `Scanned(sigma)` may contain newly constructed models not previously in the source library; successful additions must be versioned into a resulting library.

The strongest immediate closure statement a trace can support is relative:

```text
NoRecordedDominator(m,q,Evaluated(sigma,q)).
```

It cannot support

```text
NoPossibleDominator(m,q,Model)
```

without an independently proved completeness theorem.

## 13. Provenance

A provenance object is a finite labeled directed acyclic graph unless cycles are explicitly represented through higher-level references:

```text
p : Provenance = <
    nodes,
    edges,
    source_ids,
    transformations,
    timestamps_or_stage_refs,
    signatures_or_checksums?,
    trust_annotations?,
    version
>.
```

Node types include data, models, frames, domains, code, evaluations, searches, claims, certificates, and decisions. Edge labels include:

```text
derived_from
measured_by
transformed_by
trained_on
evaluated_on
corrects
supersedes
selected_because
licensed_because.
```

Provenance is not compressed into a scalar license margin. A margin can point to provenance; it cannot replace it.

## 14. Bridge objects

A bridge is a typed record:

```text
beta : Bridge = <
    source_model_and_frame,
    target_model_and_frame,
    overlap_domain,
    translation_maps?,
    relation_type,
    discrepancy_spec?,
    bound_or_test?,
    direction,
    evidence,
    provenance
>.
```

`relation_type` may be:

```text
ExactPredictive
ApproxPredictive
Statistical
DecisionEquivalent
Asymptotic
Translated
Unresolved.
```

Bridge composition is partial. It requires matching intermediate frames/interfaces and a rule for composing errors or guarantees.

## 15. Formula constructors and judgments

Task 7 declares the following well-formed formula families without yet assigning truth conditions.

### 15.1 Performance and certification

```text
Adeq(m;q,epsilon)
CertAdeq_{a,t}(m;q,epsilon,alpha | R)
```

`Adeq` is a target/population-level relation. `CertAdeq` is an evidence-relative judgment. Task 8 will specify whether and how either is observable.

### 15.2 Baseline improvement

```text
Improves_{a,t}(m;F,q,Delta | R)
```

This is distinct from hard adequacy.

### 15.3 Library-relative admissibility

```text
Admissible_{a,t,b}(m;q,K,sigma,c | R)
Dominates_{a,t}(m_2,m_1;q,c | R)
```

The search trace appears explicitly so “no better retrieved model” cannot be confused with global optimality.

### 15.4 Full use-license

The canonical full constructor is:

```text
Lic_{a,t,b}(
    m;
    q,
    epsilon,
    alpha,
    F,
    Delta,
    K,
    c,
    sigma,
    p
    | R
).
```

where:

```text
a       : Agent
t       : Stage
b       : Budget
m       : Model
q       : EvalSpec
epsilon : Tol(q)
alpha   : CertSpec
F       : Fallback
Delta   : Improve(q,F)
K       : Library
c       : Cost
sigma   : Search
p       : Provenance
R       : Record.
```

For update semantics, partition these request positions into:

```text
Substantive(omega)
  = <a,b,m,q,epsilon,alpha,F,Delta,c>

StageBound(omega)
  = <t,R,K,sigma,p>.
```

`Substantive` records what reliance question is being asked. `StageBound` records the finite-stage versions of the evidence, library/search, and provenance objects against which it is currently reassessed. A successor request may rebind `StageBound` positions to child-stage versions without claiming that the old request was mutated. Changing a substantive position creates a different reliance question. If an application treats a library, search protocol, or provenance requirement as a fixed substantive constraint, that constraint belongs inside `q`, `c`, or the later license profile; the reference to its current version remains stage-bound.

When the context is fixed, write:

```text
Lic(m;q,epsilon)
```

or, only in motivational prose,

```text
Pi(M,D,epsilon).
```

`Pi(M,D,epsilon)` is not the canonical formal signature.

### 15.5 Active sets, selection, and abstention

```text
Active_{a,t,b}(x;q,K | R)
Selected_{a,t,b}(m,x;pi_sel,q,K | R)
Abstain_{a,t,b}(x;pi_sel,q,K,F | R).
```

The active set returns model references; selection returns a decision. Their semantics are deferred.

### 15.6 Update and defeat placeholders

```text
DefeatedByEvidence(lic_ref,R,R')
DefeatedByDominator(lic_ref,m',q,K',sigma',R')
RestrictedTo(lic_ref,D')
Retained(entry,K,K')
Supersedes(m',m,D,q).
```

Task 9 will define update rules, and Task 10 will formalize dominance and domain splitting.

## 16. Point judgments versus domain judgments

### 16.1 Point domains

For `x : Case(tau)`, distinguish:

```text
delta_x : point-mass distribution
{x}     : singleton carrier set.
```

The constructor

```text
pointDomain(tau,x,mode)
```

records which is intended. Expected risk under `delta_x` and worst-case risk over `{x}` may coincide numerically for a deterministic loss, but they remain different evaluation specifications.

### 16.2 Point license notation

A pointwise request is shorthand for a domain request:

```text
LicPoint_{a,t,b}(m;x,q_x,epsilon,...|R)
  := Lic_{a,t,b}(m;q_x,epsilon,...|R)
```

where `dom(q_x)=pointDomain(tau,x,mode)`.

### 16.3 Why pointwise adequacy is not domain adequacy

The following inferences are not signature-level identities:

```text
forall x in carrier(D), Adeq(m;q_x,epsilon)
    => CertAdeq(m;q_D,epsilon,alpha|R)
```

and

```text
Adeq(m;q_D,epsilon)
    => forall x in carrier(D), Adeq(m;q_x,epsilon).
```

They can fail or become ill-typed because:

- expected risk does not imply a worst-case point guarantee;
- domain certification includes finite-sample uncertainty and coverage;
- point and domain tolerances may live in different spaces;
- the domain may include a distribution or task family absent from a point scope;
- the risk aggregator may not commute with universal quantification.

Later propositions must state the aggregator and assumptions under which a point/domain inference is valid.

## 17. Well-formedness of a full license request

Write

```text
WF(a,t,b,m,q,epsilon,alpha,F,Delta,K,c,sigma,p,R).
```

At minimum, `WF` requires:

1. `R = R_{a,t}`, `K = K_{a,t}`, or an explicit reason that an external record/library is being evaluated.
2. `b preceq_Budget b_{a,t}` for the process represented by `sigma`.
3. `m` has a versioned entry in `K` or is explicitly marked as a newly proposed candidate.
4. `m` supports every task in `dom(q)` through a defined model/frame interface on the evaluated cases.
5. `loss(q)` accepts the decoded predictions and available outcomes/decision traces.
6. `risk(q)` has every required domain view: set, measure, sampler, dynamics, or comparator.
7. `epsilon : Tol(q)` and uses the same orientation/order as `RiskVal(q)`.
8. `alpha : CertSpec` names a target, interpretation, assumptions, and estimator/bound compatible with `q` and `R`.
9. `F` is executable/evaluable on the comparison scope, or its absence is explicitly represented by `NoFallback` in a semantics that permits it.
10. `Delta : Improve(q,F)` and the candidate/fallback quantities are commensurable.
11. `c` supplies every cost coordinate required by the chosen admissibility/dominance relation.
12. `sigma` identifies its searched/evaluated subset and respects `b`; timeouts and failures are not silently treated as negative evaluations.
13. `p` connects the model, domain, loss, evidence, search, and requested decision through auditable references.
14. Every collection quantified internally at the current stage is finite or finitely represented.

An ill-formed request is not false. It is rejected by the type system or returned as `Undefined(reason)`.

## 18. What is intentionally absent from the base signature

The base object language does not contain primitive predicates

```text
TrueTheory(m)
FalseTheory(m)
Final(m)
Complete(K)
BestPossible(m).
```

Their absence does not assert that truth or final theories are impossible. It prevents the finite-stage license calculus from obtaining such claims for free.

Model-local satisfaction is permitted:

```text
m,x |=_Theta phi
```

when the theory framework supplies a formal object language. This says that a formula holds in/under a model, not that the model is the final true theory of the world.

Meta-level predicates about convergence, stability, completeness, or truth may be introduced in Tasks 12–13 with explicit semantics. They are not inputs to ordinary license derivations unless a later theorem justifies the connection.

## 19. Neural representation interface placeholders

The structured signature precedes vectorization. Later neural tasks may introduce encoders:

```text
e_M : ModelRef -> R^{d_M}
e_D : DomainDescriptor -> R^{d_D}
e_q : EvalSpecDescriptor -> R^{d_q}
e_R : EvidenceSummary -> R^{d_R}
e_c : Cost -> R^{d_c}.
```

These are representations of typed records, not identifications of the records with vectors.

A future scorer may have type

```text
RiskNet_theta : EncodedRequest -> PredictedRisk(q)
```

and a comparison head may return

```text
Margins_theta : EncodedRequest ->
    <s_hard,s_fallback,s_library,s_cost,...>.
```

The signature requires outputs to retain model references, task/domain scope, risk units/order, and provenance pointers. A bare real number without those indices is not a complete license representation.

## 20. Three well-typed examples

### 20.1 Projectile prediction under two domain views

Let `tau_proj` predict landing position. Define one carrier:

```text
X = {launch configurations satisfying stated speed/field conditions}.
```

Construct:

```text
D_set  = <tau_proj,X,no measure,...>
D_dist = <tau_proj,X,mu_operational,...>.
```

Then:

```text
q_worst = Eval(D_set,L_distance,WorstCase)
q_mean  = Eval(D_dist,L_distance,Expected(mu_operational)).
```

`epsilon_worst : Tol(q_worst)` and `epsilon_mean : Tol(q_mean)` can both be measured in meters while licensing different claims. Equality of units does not make the judgments identical.

### 20.2 Classifier with defer fallback

Let `tau_cls` have class predictions and classification outcomes. Let `F=Defer(human_reviewer)` with a time and monetary cost. Define:

```text
q = Eval(D_deployment,L_misclassification,Expected(mu_deployment)).
```

A full request can ask whether model `m` meets a hard error threshold, beats deferral by `Delta` after costs, and remains admissible among the models actually evaluated by `sigma`. Reject/defer is a typed alternative, not another class label.

### 20.3 Policy/value reconstruction with history

Let `tau_game` be action selection in a game. A raw visible board `x` may be sufficient in a Markov game; in a partially observable variant, a history `h` or belief state `b(h)` may be required. The two domains

```text
D_board   subseteq Case_board(tau_game)
D_belief  subseteq Case_belief(tau_game)
```

are different typed scopes even if their neural encodings share a dimension. A value-reconstruction license must name the environment dynamics, return convention, perspective, and evaluated state/history distribution through `tau_game`, `q`, and `R`.

## 21. Canonical abbreviations

The following abbreviations are approved:

| Abbreviation | Expansion | Permitted when |
|---|---|---|
| `q` | `Eval(D,L,rho)` | domain, loss, and risk rule are stated nearby |
| `R_t` | `R_{a,t}` | agent fixed |
| `K_t` | `K_{a,t}` | agent fixed |
| `Adeq(m;q,epsilon)` | target adequacy formula | risk meaning fixed |
| `CertAdeq_{a,t}(m;q,epsilon,alpha)` | evidence-relative certification | record understood as `R_{a,t}` |
| `Lic(m;q,epsilon)` | full license | all fallback/library/cost/search fields fixed by a displayed context |
| `Pi(M,D,epsilon)` | motivational compression | informal opening only; immediately unpacked |
| `A(x)` | active licensed model set | agent, stage, library, and evaluation context fixed |

Forbidden silent compressions include:

- using `D` for both a case set and a probability distribution without declaring the view;
- folding `rho` into `L` in one section but not another;
- using the same `epsilon` across differently scaled losses;
- using `M` for a theory framework, instantiated model, and library entry in one proof;
- using `K` to mean all possible models;
- treating `alpha` as self-explanatory;
- replacing a search trace with the phrase “best available.”

## 22. Decisions fixed here

1. The core language is many-sorted and task-typed.
2. Licenses apply primarily to versioned instantiated models, not underspecified theory frameworks.
3. Model identity remains intensional; behavioral equivalence is a derived, scoped relation.
4. Domains are typed evaluation scopes supporting set, distribution/sampler, and task-family views.
5. Loss and risk aggregation remain separate from domain identity.
6. `EvalSpec(D,L,rho)` is the canonical bundle that types risk and tolerance.
7. Tolerances live in preordered risk spaces and need not be scalar.
8. Point judgments are singleton/point-mass domain judgments but do not automatically entail domain guarantees.
9. Evidence records are finite, versioned event structures with explicit corrections rather than destructive overwrites.
10. Libraries are finite stage-local maps and are never the universe of possible models.
11. Search traces record evaluated scope, stopping reasons, and failures; closure is always relative unless separately proved complete.
12. Provenance is a graph-valued first-class object, not a scalar score.
13. Fallback, hard adequacy, comparative improvement, cost admissibility, and selection have separate types.
14. Global truth/finality/completeness predicates are absent from the base object language.

## 23. Open gates handed to later tasks

Task 8 must decide:

- the target/population semantics of `Adeq`;
- the evidence-relative semantics of `CertAdeq`;
- how each `CertSpec` interprets uncertainty;
- the exact conjunction/factorization defining `Lic`;
- whether `NoFallback` is ever admissible;
- how empty active sets trigger fallback or abstention.

Task 9 must decide:

- the KLM/AGM-style structural properties of consequence and update;
- how record corrections change admissible evidence views;
- which object-level conclusions may be exported from a license.

Task 10 must decide:

- the cost/risk product order for dominance;
- how partial domination constructs domain restrictions/splits;
- when old licenses survive on residual domains.

Tasks 12–13 must decide whether any convergence, stability, or provability modalities are added at the meta level. No GL/Löb principle is inherited by default.

Task 15's [`ml/01_encodings.md`](../ml/01_encodings.md) decides which record fields are explicit neural inputs, fixed context, learned statistics, external handles, or forbidden sole compression targets. Task 16's [`ml/02_relu_architecture.md`](../ml/02_relu_architecture.md) preserves that boundary in the hybrid reference, Task 17's [`ml/03_representation_theorems.md`](../ml/03_representation_theorems.md) preserves it through the exact/robust proofs, and Task 18's [`ml/04_losses.md`](../ml/04_losses.md) preserves it through structured training, calibration, baseline, and routing losses.

## Task conclusion

The signature now has a stable type boundary. A model is a versioned evaluable object; a domain is a typed evaluation scope; a loss scores task-typed outputs; a risk specification aggregates those scores using declared domain views; and a tolerance is an element of the resulting ordered risk space. Evidence, library scope, bounded search, fallback, costs, and provenance remain first-class indices of the eventual license. This is sufficient for Task 8 to define finite-stage semantics without conflating a point with a domain, a set with a distribution, a theory with a model, a risk threshold with falsity, or a finite library with the universe of possible theories.
