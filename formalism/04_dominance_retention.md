# Certified Dominance, Pareto Retention, and Domain Splitting

Status: Task 10 formalism  
Date: 2026-07-11  
Depends on: [`01_signature.md`](01_signature.md), [`02_license_semantics.md`](02_license_semantics.md), [`03_consequence_update.md`](03_consequence_update.md)  
Scope: scalar and multi-objective comparison, frontier semantics, retention, partial domination, and distribution-aware splits

> **Task 11A interface notice.** This historical artifact predates mandatory profile indexing. Its `UFront` and `CFront` notions now supply comparison atoms to named `Lic_P` profiles; comparison does not universally belong to every license. Read current/frontier/use views as profile-indexed where licensing is involved. See [`05a_integration.md`, §16](05a_integration.md#16-repairs-to-completed-interfaces).

## Executive definition

Dominance is not adequacy. Adequacy asks whether a candidate satisfies a hard task-relative requirement. Dominance asks whether another **eligible** candidate is no worse under every coordinate of a declared comparison profile and better under the profile's strictness rule.

The comparison object is generally a use plan rather than a bare model:

```text
e = <model, gate_or_selector, fallback, purpose>.
```

This is necessary because coverage, abstention, fallback use, and some costs belong to the deployed plan. A bare model is shorthand for an always-use plan only when that is meaningful.

For a profile `g` with normalized smaller-is-better coordinates, define

```text
z_g(e,D) = (
    task risk,
    coverage deficit,
    deployment/resource costs,
    robustness deficit,
    ...
).
```

Two main comparison modes are:

```text
ScalarDom_g(e',e;D)
ParetoDom_g(e',e;D).
```

`ScalarDom` uses an explicit monotone scalarization. `ParetoDom` uses the product preorder and requires at least one strict improvement. Neither is inferred from raw point estimates. Operational defeat uses a joint, mode-correct certificate:

```text
CertDominates_{a,t}(e',e;D,g | R).
```

Unknown coordinates or boundary-straddling comparison regions yield `Unknown`, not dominance in either direction.

Retention is layered:

```text
archive retention
  superset hard-adequacy retention
  superset competitive/frontier retention
  superset selected-now.
```

The inclusions describe typical deployment policy, not identity. A model can be globally superseded for risk-based selection while remaining:

1. the better model on a certified subdomain;
2. Pareto-undominated because it is cheaper, faster, more robust, more interpretable, or covers different cases;
3. adequate but competitively dominated;
4. useful only as an archived comparison, bridge component, or contingency.

Partial domination causes a domain split only under an explicit local-frontier policy and only when the proposed cells, measures/samplers, certificates, fallbacks, boundaries, and provenance can be reconstructed. Otherwise the system keeps the aggregate comparison, withholds the local-optimality request, or gathers more information. Set subtraction alone is not a distributional split.

## 1. Comparison entities

### 1.1 Use plans

Define a comparison entity:

```text
e : UsePlan = <
    entity_id,
    model_ref,
    model_version,
    gate_or_selector,
    fallback,
    task_and_purpose,
    deployment_protocol,
    provenance
>.
```

The gate may select the model on some cases and invoke its fallback otherwise. Write:

```text
Pure(m)
```

for an always-use plan when `m` has full intended coverage and no internal reject behavior. If two systems have different abstention behavior, comparing their “model accuracy” without their gates is ill typed.

### 1.2 Eligibility before comparison

For profile `g` and domain `D`, define:

```text
Eligible_g(e,D | R)
```

iff:

1. the entity is executable for the task, purpose, and frame;
2. its hard adequacy requirement is granted for the profile's evaluation specification;
3. every hard safety/resource/governance constraint is granted;
4. its fallback is explicit and executable where the profile requires one;
5. every coordinate required by `g` is defined or handled by the declared missingness policy;
6. its evaluation and provenance are valid for the comparison stage.

Dominance is evaluated only among eligible entities unless the profile explicitly labels the result as a diagnostic comparison. An unsafe but accurate model does not defeat a safe candidate for authorized use merely by having lower predictive loss.

### 1.3 Comparable scope

```text
Comparable_g(e',e,D)
```

requires the same task, purpose, deployment conditions, and coordinate meanings, plus compatible frames and domain views or a valid bridge/transport witness. Equal numerical values with different units, coverage conventions, perturbation sets, or latency hardware are not comparable.

## 2. Comparison profiles

### 2.1 Profile record

A comparison profile is:

```text
g : CompareProfile = <
    profile_id,
    scope_spec,
    candidate_entity_type,
    finite_coordinate_set I_g,
    coordinate_specs (Q_i,preceq_i)_{i in I_g},
    hard_filter,
    mode,
    strictness_or_margin,
    granularity,
    certificate_spec,
    missingness_policy,
    closure_policy,
    retention_policy,
    provenance
>.
```

Every `preceq_i` is oriented so that

```text
x preceq_i y
```

means `x` is no worse than `y`. Numeric benefit coordinates are converted to deficits or supplied with a reversed order. The values do not have to share units under Pareto comparison.

### 2.2 Modes

The base modes are:

```text
Scalar(s,delta)
Pareto(delta_vector?)
Lexicographic(priority_order,delta_vector?)
```

This task formalizes the first two. Lexicographic comparison is admitted as a later policy specialization; it must not be confused with Pareto order.

### 2.3 Granularity

```text
granularity(g) =
    WholeDomain(q)
  + DeclaredCells(H)
  + UniformPointwise(X,certificate_family).
```

- `WholeDomain(q)` compares aggregated quantities on `D`.
- `DeclaredCells(H)` compares a finite, prespecified family of typed subdomains.
- `UniformPointwise` requires functions and uniform certificates over a declared carrier; individual noisy point estimates do not suffice.

A whole-domain profile does not acquire a local-optimality requirement for free. Conversely, a local-frontier profile must not hide difficult cells inside a favorable aggregate.

### 2.4 Missingness policy

The default is:

```text
RequiredUnknown -> comparison Unknown.
```

Alternatives such as conservative worst-case imputation, interval completion, or coordinate omission must be explicitly justified. Silently dropping the one coordinate on which the incumbent is strong invalidates the comparison profile.

## 3. Performance and resource vectors

### 3.1 General vector

For eligible entity `e`, domain `D`, and profile `g`, define the target vector

```text
z_g(e,D) = (z_i(e,D))_{i in I_g}
          in Product_{i in I_g} Q_i.
```

This is a metalanguage target. An empirical estimate or certificate region must retain its decoration.

### 3.2 Task-risk coordinate

The task-risk coordinate is normally

```text
z_risk(e,D) = Risk_q(e)
```

for `q=EvalSpec(D,L,rho)`. If `e` contains a gate/fallback, the profile must choose among:

```text
selective risk of model uses
unconditional system risk including fallback
regret relative to an external comparator
vector(selective risk,coverage deficit,fallback cost).
```

These quantities answer different questions and cannot be substituted silently.

### 3.3 Coverage deficit

For a plan-level use event:

```text
Cov(e,D) = Pr_{x~mu_D}[e uses its model rather than fallback].
```

With numeric coverage, define the smaller-is-better coordinate

```text
z_cov(e,D) = 1 - Cov(e,D).
```

If `D` has no probability view, coverage may instead be a carrier fraction, lower capacity, verified set inclusion, or another typed object with its own preorder. Selective risk must be reported jointly with coverage: a system can reduce selective risk by abstaining almost everywhere.

### 3.4 Deployment and resource costs

For each declared resource `k`:

```text
z_cost,k(e,D) = Cost_k(e,D,hardware,load,protocol).
```

Coordinates may include latency, memory, energy, money, communication, switching, human-review load, or explanation cost. Measurement conditions are part of the coordinate type.

Expected latency and worst-case latency are different coordinates. A cost measured on one device does not dominate a cost on another without a translation model.

### 3.5 Robustness deficit

There is no unqualified scalar “robustness.” A profile declares a perturbation/shift family `U(D)`, base risk `q`, and aggregation. Examples include:

```text
z_rob,abs(e,D) = sup_{nu in U(D)} Risk_{q_nu}(e)

z_rob,deg(e,D) = sup_{nu in U(D)}
                  positive_part(Risk_{q_nu}(e)-Risk_q(e))

z_rob,rad(e,D) = - certified_safe_radius(e,D)
```

after orienting smaller as better. Adversarial radius, distribution-shift risk, calibration drift, and mechanical fault tolerance are not interchangeable.

### 3.6 Interpretability and other coordinates

An interpretability coordinate is permitted only with an operational measure: rule length, human task time, intervention fidelity, causal sufficiency, explanation error, or another declared target. “More interpretable” without a metric or preorder is an annotation, not a dominance coordinate.

### 3.7 Hard constraints versus soft coordinates

Hard constraints are applied in `Eligible_g` before the vector comparison. Soft coordinates enter `z_g`. This prevents a small gain in accuracy from compensating for a noncompensable safety violation unless the application explicitly chose a scalar policy that allows such compensation.

## 4. Scalar dominance

### 4.1 Scalarization

Let

```text
s_g : Product_i Q_i -> Q_s
```

map the performance vector into a totally preordered scalar space, with smaller values preferred. It must be monotone:

```text
z preceq_product z'  implies  s_g(z) <= s_g(z').
```

Common examples are:

```text
single task risk
normalized positive weighted sum
expected total system cost
application-specific utility transformed to loss.
```

Weights require declared units/normalization and provenance. The motivating question does not determine them.

### 4.2 Target scalar dominance

For comparable eligible entities:

```text
ScalarDom_g(e',e;D)
```

iff

```text
s_g(z_g(e',D)) < s_g(z_g(e,D)).
```

For a required practical margin `delta>0` in the scalar space:

```text
ScalarDom_{g,delta}(e',e;D)
iff s_g(z_g(e',D)) + delta <= s_g(z_g(e,D)).
```

When `delta=0`, strict inequality is still required. Equality is tie/equivalence, not strict dominance.

### 4.3 Scalar dominance is profile-relative

Different monotone scalarizations can rank the same pair differently. Therefore:

```text
ScalarDom_g(e',e;D)
```

does not entail `ScalarDom_{g'}(e',e;D)` when `g` and `g'` differ in weights, units, coordinates, or purpose.

### 4.4 Scalar near-best set

For finite eligible set `E` and slack `eta>=0`, define:

```text
NearBest_{g,eta}(E,D)
  = {e in E : s_g(z_g(e,D))
              <= min_{h in E} s_g(z_g(h,D)) + eta}.
```

Near-best retention is a policy distinct from adequacy and Pareto retention. With uncertain scores, the definition must be certified using a joint or simultaneous comparison region.

## 5. Pareto dominance

### 5.1 Product preorder

Define:

```text
z preceq_g^P z'
iff forall i in I_g, z_i preceq_i z'_i.
```

Coordinate equivalence is:

```text
z equiv_g^P z'
iff z preceq_g^P z' and z' preceq_g^P z.
```

The strict product relation is:

```text
z prec_g^P z'
iff z preceq_g^P z' and not(z' preceq_g^P z).
```

For real-valued component orders this is exactly “no worse on every coordinate and strictly better on at least one.” The preorder definition also handles coordinates with equivalence classes.

### 5.2 Target Pareto dominance

For comparable eligible entities:

```text
ParetoDom_g(e',e;D)
iff z_g(e',D) prec_g^P z_g(e,D).
```

Target incomparability occurs when each entity is better on at least one relevant coordinate or the coordinate order itself is partial.

### 5.3 Margin-certified Pareto dominance

For numeric coordinates and a chosen strict witness coordinate `j`, a stability margin may require:

```text
z_i(e',D) <= z_i(e,D)              for every i
z_j(e',D) + delta_j <= z_j(e,D)     for one declared j,
```

where `delta_j>0`. Other coordinates can have their own no-worse margins if the policy requires them.

The tempting relaxed rule

```text
z_i(e') <= z_i(e) + eta_i
```

can destroy transitivity. It is not called Pareto dominance here unless the tolerances induce a genuine quotient order or the nontransitivity is explicitly accepted as a separate outranking relation.

### 5.4 Pareto frontier

For finite eligible set `E`:

```text
PF_g(E,D)
  = {e in E : no h in E satisfies ParetoDom_g(h,e;D)}.
```

The frontier can contain one, several, or all eligible entities. It is not a unique selector.

### 5.5 Equality, tie, incomparability, and uncertainty

Keep four cases distinct:

```text
Equivalent:     both product weak orders hold
Dominated:      one strict product order holds
Incomparable:   target vectors trade off or use a partial order
Unknown:        evidence cannot certify which target relation holds.
```

Incomparability is a property of specified target values/orders. Unknown is an epistemic status of the finite-stage comparison.

## 6. Certified dominance

### 6.1 Joint comparison certificate

Let a valid comparison procedure produce

```text
kappa_{e',e,g,D}
  = Certify_{a,t}((z_g(e',D),z_g(e,D));alpha_g | R)
```

with joint region

```text
C_{e',e} subseteq Z_g x Z_g.
```

Separate marginal intervals may be combined only with a valid simultaneous-coverage or dependence rule.

### 6.2 Support for scalar dominance

```text
SupportsScalarDom(kappa,e',e,g,delta)
```

iff for every `(z',z) in C_{e',e}`:

```text
s_g(z') + delta <= s_g(z)
```

with a strict separation convention when `delta=0`.

### 6.3 Support for Pareto dominance

```text
SupportsParetoDom(kappa,e',e,g)
```

iff:

1. for every `(z',z) in C_{e',e}` and every coordinate `i`, `z'_i preceq_i z_i`;
2. there is one fixed witness coordinate/order separation certified throughout the region so that the reverse product order is impossible.

The strict witness may not change opportunistically from one point of the uncertainty region to another unless a separate theorem proves that reverse dominance is excluded throughout.

### 6.4 Operational relation

Replace the provisional Task 8 predicate by:

```text
CertDominates_{a,t}(e',e;D,g | R)
```

iff:

1. `Eligible_g(e',D|R)` and `Eligible_g(e,D|R)`;
2. `Comparable_g(e',e,D)`;
3. a valid joint comparison certificate exists;
4. it supports the dominance mode declared by `g`;
5. the certificate and result have complete provenance.

For model-only notation, read `m` as `Pure(m)` when well formed.

### 6.5 Pairwise assessment

```text
AssessCompare_{a,t}(e',e;D,g | R)
```

returns:

- `DominatesForward` if `CertDominates(e',e)`;
- `DominatesReverse` if `CertDominates(e,e')`;
- `CertifiedEquivalent` if a valid region supports equivalence under `g`;
- `CertifiedIncomparable` if a valid region supports opposing coordinate advantages or order incomparability throughout;
- `Unknown` if evidence, compatibility, or joint uncertainty is insufficient;
- `Undefined` if the comparison is ill typed.

### 6.6 No transitive closure of arbitrary certificate edges

Target Pareto dominance is transitive under the stated product preorder. Pairwise certified edges need not be freely composed: they may use different data, confidence interpretations, stages, domains, or dependence assumptions. A derived edge `e_1 -> e_3` requires compatible certificates and a valid composition/simultaneous-error rule.

### 6.7 Statistical interpretation

As in Task 8:

- deterministic proof can establish target dominance outright;
- a frequentist edge inherits joint procedure coverage, not certainty for the realized data;
- a Bayesian edge means posterior support under its prior/model assumptions;
- a conformal edge supports only the declared target;
- empirical-only comparison remains benchmark-relative.

The published theorem statements must preserve these modal qualifications.

## 7. Operational frontiers and search closure

### 7.1 Evaluated eligible set

For search `sigma`:

```text
E^+_{sigma,g}(D)
  = {e in Evaluated(sigma,D,g) : Eligible_g(e,D|R)}.
```

Retrieved but unevaluated, ill-typed, or hard-ineligible entities are recorded but excluded from the competitive frontier.

### 7.2 Undefeated set

```text
UFront_{a,t}(E,D,g|R)
  = {e in E : no h in E has CertDominates(h,e;D,g|R)}.
```

This is the default relative operational frontier. Membership means no certified dominator was found in `E`; it is not a positive certificate of target Pareto optimality.

### 7.3 Certified-undominated set

Define the stronger set:

```text
CFront_{a,t}(E,D,g|R)
```

containing `e` only if every `h in E` is covered by a valid result establishing one of:

```text
h does not dominate e
h is ineligible
h is inapplicable/incomparable under the profile.
```

Unknown required comparisons keep `e` out of `CFront`, although it may remain in `UFront`.

### 7.4 Relation to Task 8 closure

Use:

```text
RelClosed(e;D,g,sigma|R)
iff e in UFront(E^+_{sigma,g}(D),D,g|R).
```

For a declared-library closure policy that requires every comparison resolved, replace `UFront` by `CFront`. Global target-frontier membership remains unavailable without a complete candidate reduction and valid comparisons.

### 7.5 Dominance graph

Store the finite graph:

```text
G_{a,t,D,g} = <
    eligible entity nodes,
    certified dominance edges,
    equivalence edges,
    certified-incomparability edges,
    unknown-pair annotations,
    certificate/provenance references
>.
```

A scalar winner label or frontier bit is not enough for later explanation and revision.

## 8. Four retention layers

### 8.1 Archive retention

```text
ArchiveRetained(m,K,R)
```

means the versioned model entry, evaluations, license events, and provenance remain reachable. Dominance never implies archive deletion. Removal requires an explicit storage, privacy, legal, corruption, or governance event and should preserve whatever tombstone/audit metadata policy permits.

### 8.2 Hard-adequacy retention

```text
HardRetained_{a,t}(e,D)
```

means its adequacy and hard constraints remain granted, independently of comparative admissibility. A certified dominator does not by itself remove this status.

### 8.3 Competitive/frontier retention

```text
FrontierRetained_{a,t}(e,D,g,sigma)
iff HardRetained_{a,t}(e,D)
    and e in UFront(E^+_{sigma,g}(D),D,g|R)
```

for default relative closure. Stronger policies may require `CFront`.

### 8.4 Selection retention

```text
SelectedNow_{a,t}(e,x,g)
```

requires frontier/active eligibility plus the selector's decision. An entity can be frontier-retained but not selected because of stochastic routing, switching costs, load balancing, exploration, or another explicit policy.

### 8.5 Typical inclusions

For a well-formed policy that selects only current frontier entities:

```text
SelectedNow
  subseteq FrontierRetained
  subseteq HardRetained
  subseteq ArchiveRetained.
```

The reverse inclusions fail in general.

### 8.6 When “retained set equals Pareto frontier” is true

That characterization requires all of the following:

1. “retained” means competitive retention, not archive or hard-adequacy retention;
2. the candidate library and domain are fixed and finite;
3. all and only hard-eligible candidates are considered;
4. the full resource vector is correctly specified;
5. every required target comparison is known or soundly certified;
6. the policy retains every undominated eligible entity and no dominated one;
7. no near-best, diversity, bridge, contingency, historical, or exploration exception is active.

Under these axioms the result is true by definition/characterization. Without them, the inherited unrestricted claim is false.

## 9. Whole-domain and local dominance

### 9.1 Whole-domain dominance

```text
CertDomWhole(e',e;D,g|R)
```

uses aggregate coordinates on the exact `D` named by `g`. It can hold even when `e` is better on some subdomain, because an expectation or scalarized aggregate can conceal local reversals.

### 9.2 Cell-relative dominance

For a declared subdomain family `H={H_1,...,H_k}` with valid restricted evaluation specifications:

```text
CertDomCell(e',e;H_j,g|R).
```

Each cell has its own risk, coverage, cost, robustness, certificate, and provenance. A whole-domain certificate does not imply these cell certificates.

### 9.3 Certified pairwise relation cells

For a pair `(e',e)` define unions of certified cells:

```text
W_{e',e} = union {H_j : CertDominates(e',e;H_j,g|R)}
L_{e',e} = union {H_j : CertDominates(e,e';H_j,g|R)}
N_{e',e} = union {H_j : CertifiedEquivalent or CertifiedIncomparable}
U_{e',e} = union {H_j : comparison Unknown or Undefined}.
```

The cells are disjoint under a declared boundary convention, and their union covers the parent scope if `H` is a complete partition. `N` is known non-dominance/tie; `U` is epistemic uncertainty.

### 9.4 Post-selection warning

If `H` is chosen after inspecting the same noisy performance data, ordinary cellwise confidence claims may fail through selection/multiple testing. A split protocol must use prespecified cells, held-out evidence, selective-inference correction, simultaneous uniform bounds, or another valid adjustment.

### 9.5 Multiple models

For more than two entities, cells can be indexed by the certified local frontier:

```text
C_A = {x : local frontier at x is exactly A}
```

for `A subseteq E`, plus unknown cells. This refines the active-set decomposition without requiring a unique winner.

## 10. Distribution-aware domain reconstruction

### 10.1 Split specification

A proposed split is a versioned object:

```text
s : SplitSpec = <
    parent_domain D,
    finite child predicates (P_j),
    boundary/null policy,
    child carriers,
    child measure_or_sampler_rules,
    child task/frame/condition records,
    parent mixture weights?,
    certificate adjustment,
    fallback/selector policy,
    provenance
>.
```

### 10.2 Carrier partition

For ordinary set carriers, require:

```text
carrier(D_i) = {x in carrier(D) : P_i(x)}
carrier(D_i) intersect carrier(D_j) = empty for i != j
union_i carrier(D_i) = carrier(D)
```

up to an explicitly assigned boundary or declared null set. The original overlapping scientific domains need not be destroyed; this disjoint partition is an operational comparison refinement of one parent domain.

### 10.3 Probability reconstruction

If `D` has probability measure `mu` and `P_i` is measurable with

```text
pi_i = mu(D_i) > 0,
```

the canonical conditional measure is:

```text
mu_i(A) = mu(A intersect D_i) / pi_i.
```

Store both `mu_i` and `pi_i`. A child with zero parent probability can still have a carrier/set interpretation, but it has no ordinary conditional probability under `mu`; a new measure is required to make an expected-risk claim there.

### 10.4 Sampler reconstruction

A parent sampler induces a child rejection sampler only when:

1. membership in `D_i` is observable without target leakage;
2. acceptance has positive probability;
3. dependence/time-order assumptions remain valid;
4. weighting or stopping corrections are recorded;
5. the sample size supports the requested certificate.

Otherwise child-domain evaluation needs a new sampling protocol.

### 10.5 Dynamic, causal, and intervention domains

Conditioning a static distribution is not enough for trajectories, interventions, or feedback systems. A split must reconstruct the transition kernel, history condition, intervention semantics, or policy-induced distribution required by `rho`. State-based routing can itself change the future distribution, so pre-routing risk need not equal deployed risk.

### 10.6 Expected-risk decomposition

For an integrable point loss and finite measurable partition:

```text
Risk_D(e) = sum_i pi_i Risk_{D_i}(e).
```

This identity supports reconstruction only when each child risk uses the conditional measure above and the same loss/interface.

### 10.7 Worst-case decomposition

For a finite carrier partition:

```text
Worst_D(e) = max_i Worst_{D_i}(e).
```

This can make restriction safe when an existing uniform bound covers every child. It does not reconstruct expected risks or child coverage.

### 10.8 Quantiles, CVaR, and calibration

Quantiles and CVaR generally do not decompose as weighted averages of child values. Calibration can also fail within subgroups despite holding marginally. These targets must be recomputed from child conditional distributions or supported by an appropriate uniform/conditional theorem.

### 10.9 Coverage reconstruction

For plan `e` and measurable partition:

```text
Cov(e,D) = sum_i pi_i Cov(e,D_i).
```

provided coverage means the same use event on every cell. Selective risk on a child is conditioned jointly on cell membership and model use; it is not obtained by merely restricting the parent numerator without renormalization.

## 11. Split readiness

### 11.1 Exact predicate

```text
SplitReady_{a,t}(s,e',e,g | R)
```

holds iff:

1. `s` is well typed and its children form the declared carrier partition;
2. every predicate/cell is measurable or otherwise valid for the required domain views;
3. the split-search/selection procedure preserves the comparison certificate interpretation;
4. child measures, samplers, dynamics, frames, tasks, and conditions are constructed wherever required;
5. pairwise comparison results on the affected cells are valid under `g`;
6. each proposed selected entity is hard-adequate and constraint-compliant on its child;
7. each child's fallback and gap behavior is explicit;
8. unknown/boundary cells are assigned to fallback, information gathering, or a separately licensed plan;
9. any minimum-mass, complexity, switching, or materiality rule in the retention policy is satisfied;
10. all child licenses, comparison edges, and mixture weights have complete provenance.

### 11.2 Split outcome

When `SplitReady` holds, issue new child requests and record:

```text
RestrictedFrom(lic_e,D,D_keep)
SupersededForSelectionOn(e,e',D_win,g)
RetainedOn(e,D_keep,g)
UnknownOn(D_unknown)
ParentMixtureWeights((D_i,pi_i)_i).
```

The parent license remains historical. Whether a parent aggregate license also remains current depends on its standing policy; the child routing view is a new deployment object.

### 11.3 Failure of readiness

If local dominance is suggested but `SplitReady` fails:

- do not manufacture child guarantees;
- retain the whole-domain result if the policy is purely aggregate and it remains valid;
- withhold a required local-frontier deployment on unresolved cells;
- route affected cells to fallback/information gathering when safely identifiable;
- collect data or repair the domain/certificate specification.

Partial evidence is not permission to subtract a region from a probability distribution.

## 12. Exact retain, split, supersede, and revoke conditions

### 12.1 Retain full competitive status

For successor request `omega'=Succ_u(omega)` on unchanged domain `D`:

```text
RetainFull(lic,omega',D,g)
```

iff:

1. every noncomparative component of the license remains granted;
2. no eligible entity certifiably dominates `e` at `granularity(g)`;
3. the required closure policy is satisfied;
4. the provenance transition is complete.

Unknown comparisons are permitted only under the relative-closure policy and remain in the payload.

### 12.2 Supersede for selection on the whole domain

```text
SupersedeWhole(e,e',D,g)
```

iff:

1. both entities are eligible and comparable on `D`;
2. `CertDominates(e',e;D,g|R)`;
3. `D` is a comparison unit under `g`;
4. the search/closure policy includes `e'`;
5. no higher-priority governance rule retains `e` in the active selector.

Then the full competitive admissibility component for `e` is refused on `D`. Its hard adequacy and archive status are unchanged unless separately defeated.

### 12.3 Split and retain on a residual/local cell

```text
SplitRetain(e,e',s,g)
```

iff:

1. `g` uses local/cell granularity or an explicit refinement update requests it;
2. `e'` certifiably dominates `e` on a nonempty selected cell `D_win`;
3. there is a nonempty cell `D_keep` where `e` is frontier-retained, uniquely required, or otherwise retained by the declared policy;
4. `SplitReady(s,e',e,g|R)`;
5. new child licenses are granted on every region where their use is authorized.

This is restriction plus reissuance, not survival of an unchanged parent request.

### 12.4 Withhold local routing

If the policy requires local frontier selection, partial domination is detected, and either the residual comparison or split reconstruction is unresolved, return:

```text
Withheld(LocalSplitUncertified).
```

Use the explicit fallback on affected cells. Do not interpret withholding as proof that the incumbent or challenger is inadequate.

### 12.5 Revoke full reliance

The current full use-license for `e` is refused or withdrawn when any required component is certifiably violated:

```text
hard adequacy violation
fallback not beaten
hard safety/resource violation
certified dominator under required competitive profile
governance withdrawal.
```

The reason must identify the component. Only the first reason establishes certified inadequacy under the same `q,epsilon`.

### 12.6 Revoke adequacy

```text
RevokeAdequacy(e,D,q,epsilon)
```

requires a valid countercertificate for the same model/use-plan version, evaluation specification, and tolerance, or a correction that reveals the earlier request was ill formed. Dominance, nonselection, expiry, missing evidence, or changed purpose does not suffice.

### 12.7 Archive removal

```text
RemoveArchiveEntry(m,reason)
```

is never a dominance consequence. It requires explicit authorization. Where legally and technically possible, retain a tombstone identifying that a version existed and why it was removed.

### 12.8 Decision table

| Hard status of incumbent | Comparative result | Local split status | Current action | What remains |
|---|---|---|---|---|
| granted | no certified dominator | not needed | retain full status | license, adequacy, archive |
| granted | whole-domain certified dominator | not needed | supersede for selection | adequacy and archive |
| granted | partial/local dominator | ready, useful residual | split and reissue | residual/local license and archive |
| granted | partial/local dominator | not ready under local policy | withhold local routing; fallback | adequacy evidence and archive |
| refused by adequacy countercertificate | any | any | revoke current reliance/adequacy | historical record and archive |
| withheld evidence | any unresolved | any | withhold; fallback | historical record and archive |
| hard safety violation | any | any | refuse use | predictive evidence may remain; archive |

## 13. Retention results

### Theorem 1: Pareto dominance is a strict partial order on product-equivalence classes

Assume every coordinate relation `preceq_i` is a preorder. Quotient vectors by `equiv_g^P`. Then `prec_g^P` is irreflexive and transitive on the quotient classes.

**Proof.** The product of preorders is a preorder. Quotienting by mutual reachability yields a partial order. Its strict part is irreflexive and transitive. Therefore target Pareto dominance cannot contain a directed cycle among distinct equivalence classes. `square`

This theorem concerns the target relation. A graph of pairwise statistical certificates should not be transitively closed without compatible error accounting.

### Theorem 2: a strictly monotone scalar optimum is Pareto-undominated

Let `E` be finite, and let `s_g` be strictly increasing with respect to the strict product order:

```text
z prec_g^P z' implies s_g(z) < s_g(z').
```

If `e*` minimizes `s_g(z_g(e,D))` over `E`, then `e* in PF_g(E,D)`.

**Proof.** If some `h` Pareto-dominated `e*`, strict monotonicity would give `s_g(z(h,D)) < s_g(z(e*,D))`, contradicting minimality. `square`

Zero-weight coordinates can break strict monotonicity; then a scalar minimizer may be Pareto-dominated on ignored coordinates while tying in score.

### Theorem 3: global scalar supersession does not imply subdomain supersession

Let `D=A disjoint_union B` with probability masses `p in (0,1)` and `1-p`. Let the comparison library be `{e_old,e_new}` and use expected task risk. Assume both entities are eligible and comparable on `D` and `A`. Suppose:

```text
Risk_D(e_new) < Risk_D(e_old)
Risk_A(e_old) < Risk_A(e_new)
```

and both entities are hard-eligible on `A`. Then `e_new` scalar-dominates `e_old` on `D`, while `e_old` is the unique risk frontier member on `A` in the two-entity library.

**Proof.** The first strict inequality is exactly scalar dominance on `D`. The second reverses the scalar order on `A`; with only two eligible entities, no candidate dominates `e_old` there. `square`

Thus a globally superseded model can remain undominated on a subdomain. A current residual license still requires a valid cell certificate and `SplitReady`; the target inequality alone is not an operational grant.

### Theorem 4: risk supersession does not imply full-resource Pareto supersession

Let the full vector contain risk and deployment cost, both smaller-is-better, and assume both entities are eligible and comparable on `D` under those coordinate definitions. Suppose:

```text
Risk_D(e_new) < Risk_D(e_old)
Cost_D(e_old) < Cost_D(e_new).
```

Then neither entity Pareto-dominates the other on `(risk,cost)`. In a two-entity eligible library both lie on the Pareto frontier.

**Proof.** `e_new` fails the no-worse condition on cost, and `e_old` fails it on risk. Hence neither product strict order holds. `square`

This is the second route by which a globally risk-superseded model can be rationally retained.

### Theorem 5: conditional split-retention

Let `s` partition `D` into `D_win`, `D_keep`, and optional `D_unknown`. Suppose:

1. `SplitReady(s,e_new,e_old,g|R)`;
2. `CertDominates(e_new,e_old;D_win,g|R)`;
3. `e_old` is hard-eligible and frontier-retained on `D_keep`;
4. child full licenses are granted for the authorized plans;
5. `D_unknown` is routed to an explicit fallback.

Then the updated routing may supersede `e_old` on `D_win` while retaining a current license for it on `D_keep`, without contradiction and without deleting the parent record.

**Proof.** Split readiness constructs distinct typed child requests and valid domain views. Comparative defeat is indexed to `D_win`; it does not entail defeat on `D_keep`. The granted child request supplies current reliance on `D_keep`, while the parent event remains in history. The fallback handles the region with no grant. `square`

### Theorem 6: partial domination alone cannot justify total revocation

There is no valid rule

```text
CertDominates(e_new,e_old;D_win,g|R)
------------------------------------------------
RevokeAdequacy(e_old,D,q,epsilon)
```

when `D_win` is a proper subdomain and no transport/countercertificate covers `D`.

**Proof.** Construct `D=D_win disjoint_union D_keep` where `e_new` dominates on `D_win`, `e_old` dominates and satisfies hard adequacy on `D_keep`, and the parent aggregate still satisfies its hard tolerance. The premise holds while the conclusion is false. Thus the rule has a countermodel. `square`

### Theorem 7: expected-risk reconstruction over a certified partition

Under the probability reconstruction conditions in Section 10 and integrable common loss:

```text
Risk_D(e)=sum_i pi_i Risk_{D_i}(e).
```

**Proof.** Apply the law of total expectation to the finite measurable partition. `square`

This does not imply analogous weighted formulas for quantiles, CVaR, calibration, or dynamically shifted deployment distributions.

### Proposition 8: unknown coordinates do not establish dominance

Under the default missingness policy, if a required coordinate for `(e',e)` lacks a valid comparable certificate, then neither `CertDominates(e',e)` nor `CertDominates(e,e')` follows solely from the remaining coordinates.

**Proof.** Operational certified dominance requires a valid joint certificate covering every required coordinate. The premise fails, so the relation is not derivable. `square`

## 14. Worked examples

### 14.1 Aggregate successor, local predecessor

Let `mu(A)=0.1`, `mu(B)=0.9`, and expected losses be:

| Entity | `Risk_A` | `Risk_B` | `Risk_D` |
|---|---:|---:|---:|
| `e_old` | `0.01` | `0.20` | `0.181` |
| `e_new` | `0.05` | `0.05` | `0.050` |

The new entity is much better in aggregate, but the old one is better on `A`. If both meet the hard tolerance on `A` and cell certificates are valid, a local-frontier router retains `e_old` there. A whole-domain risk-only router selects `e_new` everywhere unless its policy is refined.

### 14.2 Accuracy versus latency

Suppose certified vectors are:

```text
z(e_old,D) = (risk=0.08, latency=2 ms)
z(e_new,D) = (risk=0.04, latency=30 ms).
```

With a hard latency limit of `20 ms`, `e_new` is ineligible despite its accuracy. With no hard limit and a Pareto profile, both are frontier members. With scalar score `risk + 0.001*latency`, the new entity wins; with `risk + 0.01*latency`, the old entity wins. The weights encode policy.

### 14.3 Selective risk and coverage

```text
e_1: selective risk=0.01, coverage=0.10
e_2: selective risk=0.03, coverage=0.95.
```

Using vector `(selective risk,1-coverage)`, neither dominates. Reporting only selective risk would misleadingly declare `e_1` superior by ignoring that it abstains on 90% of cases.

### 14.4 Robustness reversal

On the nominal distribution:

```text
Risk(e_new)=0.03 < Risk(e_old)=0.05.
```

Across declared shift family `U(D)`:

```text
WorstShiftRisk(e_old)=0.08 < WorstShiftRisk(e_new)=0.25.
```

The entities trade off nominal and robustness risk. No Pareto edge exists. Calling the new model “strictly better” is valid only under a nominal-risk scalar profile.

### 14.5 Certified split with an unknown cell

Let declared cells be `{D_low,D_high,D_edge}`. Joint certificates establish:

```text
e_old dominates on D_low
e_new dominates on D_high
comparison unknown on D_edge.
```

If the domains and conditional measures are valid, issue child licenses on the first two cells and route `D_edge` to defer/information gathering. The system does not force a seam decision from an uncertain comparison.

### 14.6 Aggregate evidence cannot create a split

Suppose only whole-domain risks are certified:

```text
Risk_D(e_new)=0.07 < Risk_D(e_old)=0.09.
```

No casewise loss bounds or prespecified subdomain evaluations exist. The result supports whole-domain scalar dominance but does not identify where the advantage occurs. Any induced “new wins here” region learned on the same data needs a new validation protocol.

### 14.7 A dominated model retained only in the archive

If `e_new` is eligible and certifiably no worse on risk, coverage deficit, every resource cost, and robustness deficit, with strict improvement on risk, then `e_old` leaves the competitive frontier. It may still be archived for reproducibility, regression tests, historical explanation, bridge analysis, or future changed profiles. Archive retention is not a claim of current rational selection.

## 15. Consequences for neural representation

A neural implementation should output or preserve more than one scalar winner score. For each candidate/use plan it may need:

```text
hard adequacy margins
coverage and selective-risk estimates
resource/cost coordinates
robustness coordinates
joint uncertainty representation or conservative comparison bounds
pairwise certified-dominance edges
frontier membership and unknown-comparison flags
local relation-cell identifiers
split/fallback status
provenance pointers.
```

### 15.1 Scalar head

For a fixed scalar profile, a ReLU network can represent/approximate a signed pairwise margin

```text
d_{e',e}(x) = score_g(e,x) - score_g(e',x) - delta.
```

Positive margin can gate a scalar dominance claim only after uncertainty calibration and eligibility checks.

### 15.2 Pareto head

Pareto comparison requires component margins:

```text
d_i(e',e,x) = z_i(e,x)-z_i(e',x).
```

A hard Pareto edge requires every no-worse condition and at least one strict witness. One compressed scalar can hide which coordinate failed or which tradeoff preserved the older model.

### 15.3 Coverage belongs to the plan/router

If the gate is learned, coverage is an emergent property of the model-gate-fallback plan. It must be estimated under the deployed routing distribution. Attaching one fixed “coverage embedding” to the base model can be wrong after the router changes.

### 15.4 Split cells versus activation regions

Certified dominance cells are semantic/evidential regions. ReLU activation cells are computational affine regions. A learned dominance boundary may use many activation cells, and one activation cell may cross several comparison cells. Task 11 will connect the former to the atlas without identifying them.

### 15.5 Training targets

Useful multi-label targets include:

```text
eligible / hard-failed / unknown
dominates / reverse-dominated / equivalent / incomparable / unknown
frontier member set
selected entity
fallback or abstain
split-ready / split-withheld and reason.
```

Ordinary single-label cross-entropy cannot express multiple Pareto-frontier members and an empty/unknown frontier without an augmented encoding.

## 16. Claim-ledger adjudications produced by this task

This task supplies formal adjudication for three inherited claims:

1. **A05:** a risk-only scalar can rank `e_new` above `e_old` while the full `(risk,cost)` vectors are Pareto-incomparable. This is a constructive scoped reason that one scalar is sometimes insufficient when the stated policy refuses compensation.
2. **E06:** evidence rebuttal and comparative defeat are distinct, and Theorem 5 supports conditional residual retention. The unconditional statement “partial domination causes a split” is false: Theorem 6 and split-readiness failures are countermodels.
3. **E07:** archive retention, hard-adequacy retention, and operational undefeated retention are not generally the target Pareto frontier. Frontier equality holds only under the seven axioms in Section 8.6.

These are formal, definition-relative results. They do not establish that human or machine agents empirically follow the proposed frontier policy.

## 17. Decisions fixed here

1. Dominance compares eligible use plans; a bare model is an always-use shorthand only when coverage/fallback behavior makes that well formed.
2. Loss, coverage deficit, costs, and robustness are typed coordinates with a declared common profile, not interchangeable scalars.
3. Hard constraints filter candidates before soft dominance comparison.
4. Scalar dominance requires an explicit monotone scalarization; weights and normalizations are policy choices.
5. Pareto dominance is the strict part of the product preorder and does not impose compensation among coordinates.
6. Naive indifference-band Pareto rules are not assumed transitive.
7. Operational defeat requires a valid joint comparison certificate; unresolved coordinates yield `Unknown`.
8. The default relative frontier is the undefeated set, not a positive certificate of target Pareto optimality.
9. Archive, hard-adequacy, frontier, and selection retention are distinct.
10. Whole-domain, cell-relative, and uniform pointwise dominance are distinct granularities.
11. Partial domination triggers a split only under a local/refinement policy and `SplitReady`.
12. Distributional children require conditional measures/samplers and stored mixture weights; dynamics and tail risks require specialized reconstruction.
13. Dominance can supersede competitive use but cannot by itself revoke adequacy or delete a model record.
14. Unknown or boundary regions route to fallback/information gathering unless separately licensed.

## 18. Deferred to Task 11 and the first checkpoint

Task 11 must define how model charts retain these local dominance/frontier relations on overlaps, how bridges make cross-frame comparison well typed, and how unresolved seams interact with fallback.

Checkpoint A should audit:

- whether full `Lic` should always contain comparative admissibility or whether the minimal calculus should separate `HardLicense` from `PreferredUse` more sharply;
- whether the operational default `UFront` is too permissive when many comparisons are unknown;
- which of scalar, Pareto, near-best, lexicographic, or diversity-aware retention belongs in the smallest publishable logic;
- whether the split theorem needs a stronger certificate-composition lemma;
- whether coverage should be a coordinate, a hard floor, or both in the planned experiments;
- how much of the distributional reconstruction belongs in the main paper versus an appendix.

**Post-checkpoint resolution.** Task 11A selects profile-indexed `Lic_P`. `UFront` supplies the relative-undefeated atom used by `P_pref-rel`; `CFront` supplies the certified-undominated atom used by `P_pref-cert`; profiles such as `P_rely` can report comparison without requiring it. Unknown comparisons therefore grant the relative atom with disclosure but withhold the certified-undominated atom.

## Task conclusion

The provisional dominance predicate is now replaced by typed scalar and Pareto relations over eligible use plans, together with mode-correct joint certification and explicit unknown comparisons. The logic distinguishes target frontiers from finite-stage undefeated sets and separates archive, adequacy, competitive, and selection retention. A globally risk-superseded model can remain undominated on a subdomain or on a fuller resource vector. Partial domination supports restriction and retention only when a certified, distribution-aware split can be built; otherwise it does not justify total revocation. This supplies the comparative structure needed for Task 11's overlapping scientific atlas.
