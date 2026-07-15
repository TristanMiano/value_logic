# Scientific Licensed Atlases, Overlaps, Seams, and Bridges

Status: Task 11 formalism  
Date: 2026-07-11  
Depends on: [`01_signature.md`](01_signature.md), [`02_license_semantics.md`](02_license_semantics.md), [`03_consequence_update.md`](03_consequence_update.md), [`04_dominance_retention.md`](04_dominance_retention.md)  
Scope: finite-stage local model charts, partial covers, overlap compatibility, bridge composition, routing, and separation from ReLU activation geometry

> **Task 11A interface notice.** This historical artifact predates mandatory profile indexing. Read chart-use and active-set views as `Charts^use(A,P)` and `Act_A(x,zeta,P)`; archive, comparison, selection, and profile-indexed use remain distinct. See [`05a_integration.md`, §16](05a_integration.md#16-repairs-to-completed-interfaces).

> **Task 14A quantitative notice.** [`08a_transport_routing.md`](08a_transport_routing.md) characterizes subdomain restriction, decomposes deployed hard-router risk with selection/misroute/fallback terms, translates prediction bridges into task-risk bounds under Lipschitz hypotheses, and gives the exact group-valued cycle/potential theorem. The prediction-deviation results below do not by themselves imply those stronger task-risk conclusions.

## Executive definition

The weakest object needed by this project is a **finite licensed model cover**, not a differential-geometric atlas. At agent-stage `(a,t)`, it stores versioned local model/use-plan charts whose certified use domains may overlap, nest, coincide, or leave gaps.

A **scientific licensed atlas** adds:

```text
finite chart registry
+ current hard/use/frontier chart views
+ overlap and active-set records
+ typed bridge and compatibility records
+ routing seams and transition obligations
+ dominance/frontier graphs
+ fallback and abstention behavior
+ provenance and revision links.
```

A chart is not merely `(model,domain)`. It binds a versioned model or use plan to a task, frame, evaluation specification, current license references, local output language, and provenance.

On an overlap, two charts may be:

```text
exactly compatible
approximately predictively compatible
statistically compatible
decision-compatible
asymptotically related
connected only by a translation
certifiably incompatible
unresolved.
```

Compatibility is purpose-relative. Exact equality is neither assumed nor generally required. Approximate bridges retain their error bounds; unresolved bridges remain explicit and can force hard selection, further measurement, fallback, or abstention.

Three geometries remain distinct:

```text
scientific licensed cover       overlapping semantic/evidential scopes
router selection partition     regions where a policy chooses plans
ReLU activation complex        polyhedral cells of one continuous CPWL map.
```

A router over separately meaningful models is not automatically one CPWL predictor. Hard routing can produce discontinuous composed outputs even when every expert is affine. A standard finite ReLU MLP has a continuous real-valued output, so it cannot exactly equal every such hard-routed predictor without seam agreement, soft/continuous mixing, or an external discrete decision operation.

The Newtonian/relativistic example is therefore represented narrowly: two instantiated kinetic-energy predictors share a low-speed overlap and admit an approximate bridge with an explicit error bound. This is not a claim that the full theories are coordinate charts on a common differentiable manifold.

## 1. Terminology and non-goals

### 1.1 Licensed model cover

Let `X_tau` be a typed case universe for task `tau`. A finite licensed model cover of a supported region `S subseteq X_tau` is a finite indexed family

```text
L = {(chi_i,U_i)}_{i=1}^n
```

where `chi_i` is a chart record and `U_i` is its current authorized-use scope, such that

```text
S subseteq union_i U_i.
```

The `U_i` may overlap. Equality with `X_tau` is not required. If `S` is defined as the union itself, the cover condition is tautological; substantive coverage claims must name an independently supplied target region or distribution.

### 1.2 Scientific licensed atlas

A scientific licensed atlas is a licensed model cover equipped with typed overlap relations, bridge status, comparison/frontier data, routing/fallback rules, and provenance. “Atlas” here means an organized family of local model charts, not automatically a mathematical atlas in differential geometry.

### 1.3 Differential-atlas qualification

Define the optional predicate

```text
DifferentialAtlasLike(A)
```

only when all of the following are supplied:

1. the base object is a topological manifold of fixed dimension;
2. chart domains are appropriate open sets covering it;
3. each chart map is a homeomorphism into an open Euclidean set;
4. overlap transition maps are invertible with the declared regularity, such as `C^k` or smooth;
5. identity, inverse, and cocycle conditions hold on double and triple overlaps.

Ordinary scientific model libraries generally fail several of these conditions: domains can be distributions, task families, discrete states, intervention regimes, or history spaces; translations can be lossy or directional; gaps are allowed; and overlaps can be only approximately or decision-compatible.

### 1.4 Non-goals

This chapter does not assert that:

```text
every useful theory is a coordinate chart
every overlap has an invertible transition map
all licensed charts glue to one global theory
agreement establishes truth
disagreement establishes falsity
smooth interpolation resolves ontological mismatch
one ReLU activation cell is one scientific regime.
```

## 2. Chart objects

### 2.1 Chart record

A local scientific chart is:

```text
chi_i : SciChart = <
    chart_id,
    model_or_use_plan e_i,
    model_and_plan_versions,
    task_and_purpose,
    domain D_i,
    evaluation_specs Q_i,
    tolerances_and_certificate_specs,
    license_refs,
    local_language_or_equations,
    input_interface,
    output_interface,
    native_frame f_i,
    comparison_translations,
    cost_and_robustness_profile,
    provenance
>.
```

The chart normally points to an instantiated model/use plan, not an underspecified theory family. Motivating prose may call it “Newtonian theory,” but the formal record must identify the observable, parameter convention, frame, and implementation actually evaluated.

### 2.2 Four chart views

At a stage, distinguish:

```text
Charts^archive(A)    all retained versioned chart records
Charts^hard(A)       charts with current hard adequacy/constraints
Charts^use(A)        charts with current full use authorization
Charts^frontier(A)   competitively retained charts for a named profile.
```

The views need not coincide. A chart defeated for selection can remain hard-adequate and archived. An atlas should not delete the local scientific record merely because a router no longer chooses it.

### 2.3 Domain identity and use scope

The declared domain `D_i` remains the typed evaluation scope from Task 7. Its current use scope is a derived relation:

```text
UseScope_{a,t}(chi_i,zeta)
  = {x in carrier(D_i) :
       CoveredCase(x,D_i,zeta)
       and some current license for chi_i covers zeta}.
```

This does not redefine `D_i` as a neural score region. A learned induced region may estimate `UseScope`, but the supplied domain, certified domain, induced score region, and selection region retain distinct identities.

### 2.4 Local consequence

Object formulas derived inside a chart retain their label:

```text
[chi_i] phi.
```

Application of a current chart license yields `MayRely(a,t,lic_i,chi_i,phi)`, not bare `phi`. A bridge is required to transport the content to another chart/frame; an atlas does not add an implicit truth-detachment rule.

## 3. Finite-stage atlas structure

### 3.1 Atlas record

Define:

```text
A_{a,t} : ScientificAtlas = <
    atlas_id,
    agent_and_stage,
    target_case_task_family X,
    finite_chart_registry,
    current_chart_views,
    active_set_index,
    overlap_records,
    bridge_registry,
    seam_registry,
    compatibility_ledger,
    dominance_and_frontier_graphs,
    router_registry,
    fallback_policy,
    gap_and_unknown_policy,
    provenance
>.
```

Every current atlas is finite or finitely represented. Open-ended theory succession will be a sequence of such atlas versions, not one actually infinite record.

### 3.2 Supported, target, gap, and unknown regions

For request context `zeta`, let

```text
Supp(A,zeta) = union_{chi_i in Charts^use(A)} UseScope(chi_i,zeta).
```

For independently declared target scope `T(zeta)`:

```text
Gap(A,zeta) = T(zeta) \ Supp(A,zeta).
```

Also distinguish

```text
UnknownScope(A,zeta)
```

where membership, frame translation, or current license status cannot be assessed. A certified gap means every relevant chart is off/inapplicable there; an unknown scope means the system cannot decide. Both route conservatively, but they are different diagnoses.

### 3.3 Partiality

The base semantics permits:

```text
Gap(A,zeta) != empty.
```

A complete-cover claim requires a certificate that the independently declared target scope is contained in `Supp(A,zeta)`. Counting only observed cases is not a population coverage proof.

### 3.4 Atlas well-formedness

`WFAtlas(A_{a,t})` requires:

1. every chart and use-plan reference is versioned;
2. every current use chart has a current license and executable fallback;
3. domain/task/frame interfaces are typed;
4. every overlap record points to compatible domain versions or a typed reconciliation;
5. every bridge states direction, purpose, assumptions, error target, certificate mode, and provenance;
6. every router selects only current authorized charts or an explicit fallback;
7. gap and unknown behavior is defined;
8. dominance data uses the exact Task 10 profile and certificate references;
9. no current derived record depends only on its own audit event;
10. all finite-stage collections are finite or finitely indexed.

## 4. Active sets and overlapping domains

### 4.1 Active chart set

For a case `x` and request context `zeta`:

```text
Act_A(x,zeta)
  = {i : x in UseScope(chi_i,zeta)}.
```

This can have zero, one, or several members. Multiple current licenses are not a contradiction.

### 4.2 Boolean active-set cells

When every `UseScope_i` is an ordinary set with decidable membership, define for `S subseteq {1,...,n}`:

```text
C_S(A,zeta)
  = (intersection_{i in S} UseScope_i)
    intersect
    (intersection_{j notin S} (T(zeta) \ UseScope_j)).
```

At every `x in C_S`, exactly the charts in `S` are active.

### 4.3 Two-chart case

For two charts:

```text
C_{1}     = U_1 \ U_2
C_{2}     = U_2 \ U_1
C_{1,2}   = U_1 intersect U_2
C_empty   = T \ (U_1 union U_2).
```

The overlap can have positive measure or volume; it need not be a thin seam. The two domains may also coincide or nest.

### 4.4 Generalized status cells

If chart applicability is four-way, define

```text
AppStatus_i(x,zeta) in {On,Off,Unknown,Undefined}.
```

Then index generalized cells by status vectors in `{On,Off,Unknown,Undefined}^n`. The Boolean active-set decomposition applies only to the all-defined `On/Off` part. This prevents uncertain membership from being mislabeled as a gap.

### 4.5 Active set versus frontier set

On an overlap, also store:

```text
HardSet_A(x,zeta)
UseSet_A(x,zeta)
UFront_A(x,zeta,g)
CFront_A(x,zeta,g)
Selected_A(x,zeta).
```

Adequacy, full authorization, lack of a known dominator, certified undominated status, and current selection remain separate.

## 5. Overlaps and seams

### 5.1 Typed overlap

For charts `chi_i,chi_j`, define

```text
O_ij = IntersectTyped(D_i,D_j,r_ij)
```

only when tasks, conditions, frames, and required domain views agree or reconciliation record `r_ij` makes the intersection meaningful. Equal carrier encodings do not suffice if distributions or interventions differ.

### 5.2 Overlap record

```text
o_ij : OverlapRecord = <
    chart_pair,
    typed_overlap_domain O_ij,
    overlap_extent_or_mass?,
    active/license statuses,
    comparison_profiles_and_edges,
    bridge_refs,
    disagreement_or_anomaly_refs,
    routing_modes,
    evidence_and_provenance
>.
```

An overlap can be stored even when no bridge has been validated. `bridge status = Unknown` is information.

### 5.3 Selection region

For router `pi`:

```text
Sel_i(pi,zeta)
  = {x : select(pi,x,zeta)=Use(chi_i)}.
```

Safety requires

```text
Sel_i(pi,zeta) subseteq UseScope(chi_i,zeta).
```

Selection regions usually refine overlaps but need not equal chart domains.

### 5.4 Routing seam

When the case space has topology, a hard routing seam between charts is:

```text
Sigma_ij(pi)
  = closure(Sel_i(pi)) intersect closure(Sel_j(pi)).
```

In a discrete or relational space, replace closure intersection by a declared adjacency/transition relation.

A seam is where the selected rule changes. An overlap is where multiple rules are available. A seam can lie inside a thick overlap, on its edge, or—if routing is unsafe—across a gap. The terms are not synonyms.

### 5.5 Seam record

```text
s_ij : SeamRecord = <
    source_and_target_selection_regions,
    transition_zone,
    hard_or_soft_mode,
    bridge_requirements,
    switching_costs,
    output_jump_or_disagreement_bound,
    invariant_and_safety_checks,
    unknown/fallback behavior,
    provenance
>.
```

## 6. Bridge objects

### 6.1 Bridge record

A directional bridge is:

```text
beta_ij : Bridge = <
    bridge_id,
    source_chart chi_i,
    target_chart chi_j,
    overlap_or_limit_scope O,
    input_map h_ij?,
    output_or_observable_map T_ij?,
    bridge_kind,
    purpose,
    relation_or_error_object,
    assumptions,
    certificate_spec_and_result,
    directionality_and_inverse_status,
    composition_rule?,
    validity/review_conditions,
    provenance
>.
```

The bridge may be directional, partial, many-to-one, stochastic, or noninvertible. A valid `beta_ij` does not imply a valid `beta_ji`.

### 6.2 Common comparison notation

For a source case representation `x_i`, let

```text
x_j = h_ij(x_i)
y_i = output_i(x_i)
y_j = output_j(x_j).
```

When an output translation exists, compare

```text
T_ij(y_i)
```

with `y_j` in the target observable space. If the models expose only shared observables through separate maps `tau_i,tau_j`, use those instead. Internal ontologies need not be identified.

### 6.3 Exact predictive bridge

```text
ExactPred(beta_ij,O)
```

iff for every case in the certified overlap:

```text
T_ij(y_i(x_i)) = y_j(h_ij(x_i)).
```

Exactness is relative to the chosen observable/interface, not necessarily the full internal theory.

### 6.4 Approximate predictive bridge

Given target metric or loss-like discrepancy `d_j`:

```text
ApproxPred(beta_ij,O,delta)
```

iff:

```text
d_j(T_ij(y_i(x_i)),y_j(h_ij(x_i))) <= delta(x_i)
```

throughout the certified scope or according to the named probabilistic guarantee. `delta` is typed and retained during transport.

### 6.5 Statistical bridge

For predictive distributions `P_i(.|x),P_j(.|h_ij(x))`, define a bridge through a declared divergence, calibration target, test statistic, coupling, or decision distribution:

```text
StatBridge(beta_ij,O,d_P,delta,alpha).
```

Marginal distributional similarity does not imply pointwise agreement, causal equivalence, or calibrated subgroup behavior.

### 6.6 Decision bridge

For decision rule `d` and action/value context:

```text
DecisionBridge(beta_ij,O,eta)
```

may mean:

```text
action_i(x)=action_j(h_ij(x))
```

or a bounded regret/action-value difference. Predictive disagreement can coexist with decision equivalence when it does not cross a decision boundary.

### 6.7 Asymptotic/correspondence bridge

For an indexed family with parameter `lambda` and limit regime `lambda -> lambda_0`:

```text
AsymBridge(beta_ij,lambda_0)
```

requires a typed translation and a convergence statement such as

```text
sup_{x in O_lambda}
  d(T_ij(y_i^lambda(x)),y_j(x))
  <= delta(lambda),

delta(lambda) -> 0.
```

Convergence in a limit does not provide a finite-regime license without a usable bound `delta(lambda)` and a domain on which it holds.

### 6.8 Translation bridge

A translation bridge establishes that inputs/outputs or observables can be mapped into a common interface. It need not establish empirical agreement. Translation is a prerequisite for some comparisons, not a certificate that the translated predictions coincide.

### 6.9 Incompatible and unresolved bridges

```text
Incompatible(beta_ij,reason,countercertificate)
UnknownBridge(chi_i,chi_j,purpose,missing_or_unresolved).
```

Incompatibility requires positive evidence against the requested relation. Unknown means the relation is untested, underpowered, ill-supported, or missing an interface. Neither status automatically revokes the local chart licenses.

## 7. Compatibility ledger and bridge obligations

### 7.1 Compatibility status

For chart pair, overlap, and purpose:

```text
CompatStatus_A(chi_i,chi_j,O,purpose) =
    Exact(beta)
  + Approximate(beta,delta)
  + Statistical(beta,target,delta)
  + DecisionEquivalent(beta,eta)
  + Asymptotic(beta,limit,bound)
  + TranslatableOnly(beta)
  + Incompatible(reason,countercertificate)
  + Unknown(missing_or_unresolved)
  + NotRequired(mode).
```

This is not a single Boolean equivalence relation.

### 7.2 Purpose-specific obligations

The required bridge depends on use:

| Use mode | Minimum bridge obligation |
|---|---|
| archival side-by-side storage | none beyond typed identities and provenance |
| compare risks/predictions | common evaluation interface or valid translation |
| hard select one chart | each selected chart licensed on its region; quantify jumps/switching risk if relevant |
| transport a formula/conclusion | Task 9 `Transport` witness preserving scope/error |
| blend numeric predictions | common convex/affine output meaning, licensed weights, constraint preservation |
| transfer calibration/certificate | statistical transport theorem matching the certificate target |
| claim correspondence/reduction | explicit limit/translation relation with quantified error and assumptions |
| glue into one global model | exact compatibility or a separately justified approximate gluing construction |

An overlap does not universally require a successful bridge. It requires the atlas to record which bridge obligations arise from the operations actually requested.

### 7.3 Disagreement and anomaly

If two hard-adequate charts disagree beyond the expected bridge allowance, derive:

```text
AtlasDisagreement(chi_i,chi_j,O,purpose,observed_gap).
```

This can trigger evaluation, domain refinement, bridge revision, active experimentation, or fallback. It does not by itself identify which chart is wrong.

### 7.4 Compatibility does not imply adequacy

Two charts can agree exactly and both be inaccurate. Conversely, two adequate charts can disagree on particular cases under a nonzero-error task guarantee. Bridge compatibility and adequacy are separately certified components.

## 8. Composition, cycles, and gluing

### 8.1 Exact bridge composition

Suppose compatible directional maps exist:

```text
beta_ij : chi_i -> chi_j
beta_jk : chi_j -> chi_k.
```

Their composition is defined only when target/source frames and interfaces match:

```text
h_ik = h_jk compose h_ij
T_ik = T_jk compose T_ij.
```

Exact composition inherits the intersection of assumptions and validity scopes. Provenance records both paths.

### 8.2 Approximate composition bound

Assume on a triple-compatible scope:

```text
d_j(T_ij y_i,y_j) <= delta_ij
d_k(T_jk y_j,y_k) <= delta_jk
T_jk is L_jk-Lipschitz.
```

Then:

```text
d_k(T_jk(T_ij y_i),y_k)
  <= L_jk delta_ij + delta_jk.
```

Errors compose; they do not vanish by calling the maps transitions.

### 8.3 Cycle/cocycle audit

On a triple overlap, compare the direct and composed paths:

```text
Defect_ijk(y_i)
  = d_k(T_ik y_i, T_jk(T_ij y_i)).
```

An exact atlas-like cocycle requires zero defect on the declared scope. An approximate system stores a certified defect bound. Large or unknown path dependence is a seam anomaly and can make transported conclusions route-dependent.

### 8.4 Exact gluing

If every chart output has been translated into one common set `Y`, the domains cover `S`, and

```text
y_i(x)=y_j(x) for every x in U_i intersect U_j,
```

then define

```text
y(x)=y_i(x) for any i with x in U_i.
```

Pairwise equality makes `y` well defined. Additional topological regularity of `y` follows only from corresponding regularity of the local functions and cover.

### 8.5 Approximate compatibility does not give a unique glue

If charts disagree within `delta>0`, choosing chart `i`, choosing chart `j`, or choosing different admissible blend weights generally yields different global functions. Approximate compatibility can bound disagreement but does not determine a canonical global theory.

### 8.6 Continuous blend

Suppose translated outputs inhabit a common normed vector space. On an overlap choose continuous weights

```text
w_i(x)>=0,
sum_i w_i(x)=1,
w_i(x)>0 only where chi_i is licensed.
```

Define:

```text
y_blend(x)=sum_i w_i(x)y_i(x).
```

Continuity follows from continuous weights and outputs. Semantic authorization additionally requires:

1. convex combinations have a task meaning;
2. hard invariants/constraints are preserved by the convex set or separately checked;
3. the blend itself is evaluated/licensed as a use plan;
4. fallback behavior exists where weights cannot be formed.

Numerical smoothness alone is not a scientific bridge.

## 9. Router semantics

### 9.1 Router output type

For atlas `A`:

```text
route_A(pi,x,zeta) ->
    UseChart(chart_ref,license_ref)
  + UseSet(frontier_or_active_refs)
  + Mixture(weighted_chart_refs,mixture_license)
  + BridgeChart(bridge_model_ref,license_ref)
  + InformationAction(action_ref)
  + FallbackDecision(F)
  + Abstain(reason).
```

The output retains chart/model identity and trace references. It is not merely a prediction vector.

### 9.2 Safe router conditions

`SafeRouter(A,pi)` requires:

1. every selected chart is in the current authorized active set;
2. every mixture uses only licensed supports and has a mixture license;
3. hard constraints and switching costs are enforced;
4. unknown/incompatible seams invoke their declared policy;
5. gaps never trigger raw argmax over unlicensed charts;
6. selection/frontier profiles and provenance are recorded;
7. selection does not erase unselected chart records.

### 9.3 Hard selection

A hard router can choose one chart on each case:

```text
y_route(x)=y_{r(x)}(x).
```

Even when every `y_i` is continuous, `y_route` is continuous at a routing boundary only if the selected outputs approach the same value there or the boundary is handled by a continuous transition construction.

### 9.4 Soft selection

Soft weights can produce a continuous output under Section 8.6, but the weights themselves are a policy and can change coverage, cost, calibration, and deployed risk. The mixture must be assessed as a new use plan; it does not inherit every component certificate automatically.

### 9.5 Disagreement-aware routing

On a thick overlap, the router may:

```text
select a certified scalar winner
return the Pareto frontier
choose a cheaper near-best chart
blend under a valid bridge
defer when disagreement is anomalous
choose information that separates the charts.
```

No one overlap policy is built into the atlas definition.

## 10. The three geometries

### 10.1 Scientific licensed cover

```text
H_A = {UseScope(chi_i,zeta)}_i
```

is model-indexed, typed, evidence-bearing, overlapping, and possibly incomplete.

### 10.2 Router selection partition

```text
P_pi = {Sel_i(pi,zeta), Sel_mix, Sel_fallback, Sel_abstain,...}.
```

For a deterministic hard router these regions are disjoint up to boundary convention. They refine current authorization but need not reproduce chart boundaries.

### 10.3 ReLU activation complex

For finite feed-forward ReLU map `N`, an activation pattern `sigma` defines a polyhedral region `P_sigma` on which `N` is affine. The nonempty activation cells form a finite polyhedral decomposition under the ordinary architecture conventions, and the real-valued network map is continuous CPWL.

### 10.4 Non-identification

In general:

```text
H_A != P_pi != ActivationComplex(N).
```

Possible relations include:

- many activation cells implement one chart score or selection region;
- one activation cell crosses several scientific chart domains;
- several charts are active at one point while only one activation pattern occurs generically;
- a router selects one chart throughout a large overlap;
- a scientific chart has a nonpolyhedral or distributional domain not equal to any input-space cell.

### 10.5 Atlas–network alignment

An alignment is a typed relation

```text
Align : ActivationCellRef x AtlasStateRef -> AlignmentStatus
```

evaluated through:

```text
active-set fidelity
gap/unknown fidelity
selection fidelity
component-margin fidelity
local-law approximation
bridge/disagreement sensitivity
stability under retraining
causal/interventional relevance
provenance recoverability.
```

One-to-one alignment is neither assumed nor generally desirable. A many-to-one refinement can be perfectly faithful at the semantic output layer.

### 10.6 Router versus one CPWL predictor

A system can use a ReLU network to score licenses while storing experts and provenance externally. The overall routed system is then a composite object:

```text
registry + scorer + active-set gate + selector + experts + fallback.
```

It is not identified with the scorer's CPWL map.

If experts are CPWL and hard selection is polyhedral, the composite prediction is piecewise affine on a refinement, but it may be discontinuous across selection seams. Standard ReLU real-valued maps are continuous, so exact representation of the composite by one ordinary ReLU network requires compatible seam values or a different output interpretation. Continuous logits followed by an external `argmax` can produce discrete discontinuous labels without making the logits discontinuous.

Softmax gating and products of gates with experts are not generally CPWL even when the logits/experts are CPWL. They may be approximated by ReLU networks, but exact representation needs separate assumptions.

## 11. Atlas updates

### 11.1 Versioned extension

An atlas update can:

```text
add/version a chart
add/correct/retract a license
revise a domain
add or invalidate a bridge
record disagreement/anomaly
expand a search/frontier graph
split a comparison domain
change a router/fallback
repair provenance.
```

The parent atlas remains reconstructible.

### 11.2 Dependency impact

Bridge changes affect only operations that depend on those bridges unless the atlas policy makes bridge compatibility a standing license condition. Adding a chart can change overlaps, active sets, frontier graphs, selection regions, and declared-library closure even when existing adequacy certificates remain valid.

### 11.3 Split integration

Task 10 `SplitReady` creates child domain/chart requests and relation cells. The atlas records both the original overlapping domains and the operational refinement. It does not rewrite every scientific domain into a permanent disjoint tiling.

### 11.4 Bridge defeat

New evidence can:

- rebut an approximate bound, producing `Incompatible` for that requested tolerance;
- invalidate the bridge certificate without contrary evidence, producing `Unknown`;
- narrow the bridge scope;
- replace a translation/version;
- reveal a triple-overlap cycle defect.

Local chart adequacy survives unless its own requirements are affected.

### 11.5 Router update

Changing the router creates a new use-plan version. Coverage, selection risk, costs, and mixture behavior must be reevaluated. A router update is not merely a presentation-layer change.

## 12. Toy examples

### 12.1 Exact temperature translation

Two sensor charts report the same temperature observable in Celsius and Fahrenheit:

```text
y_C(x) in degrees C
y_F(x) in degrees F
T_CF(y)=9y/5+32.
```

On a shared calibrated range, an exact observable bridge is:

```text
T_CF(y_C(x))=y_F(x).
```

The raw numbers are unequal, but the translated observables agree. This is an exact translation/predictive bridge on one observable; it does not imply the sensor mechanisms or noise models are identical.

### 12.2 Approximate overlapping regressors

Let:

```text
y_1(x)=x
y_2(x)=x+0.05x^2
U_1=[-2,0.5]
U_2=[-0.5,2].
```

On overlap `O=[-0.5,0.5]`:

```text
abs(y_2(x)-y_1(x))=0.05x^2 <= 0.0125.
```

Both charts can remain licensed under their own risk bounds. An identity translation supplies an approximate bridge with `delta=0.0125`. A hard router may select one; a blend is meaningful only if the scalar output admits interpolation and the blended plan passes its own constraints.

### 12.3 Two charts with a gap

Let:

```text
U_1=[-2,-0.25]
U_2=[0.25,2]
T=[-2,2].
```

Then `(-0.25,0.25)` is a gap, not a seam between licensed charts. A safe router falls back or gathers information there; it does not extrapolate whichever chart has the larger neural score.

### 12.4 Same domain, different resource profiles

If `U_1=U_2=D`, both charts are active throughout `D`. A risk-only router may select `chi_2`; a Pareto view may retain both if `chi_1` is cheaper or more robust. The atlas keeps both chart/license records and records one selection region equal to `D`.

### 12.5 Unresolved thick overlap

Suppose two climate-control simulators are hard-adequate for different target components and both apply on a large operating regime, but their outputs lack a validated common-state translation. The atlas records a thick overlap with `TranslatableOnly` or `Unknown`, permits separate task uses, and forbids blending or cross-chart formula transport. Further measurement can target the disagreement.

## 13. Newtonian/relativistic kinetic-energy chart example

### 13.1 Narrow formal scope

Fix one particle mass `m`, inertial-speed magnitude `v`, light speed `c`, dimensionless speed

```text
u=v/c,
```

and normalized kinetic energy

```text
k=K/(mc^2).
```

Define two instantiated predictors:

```text
k_N(u)=u^2/2
k_R(u)=(1-u^2)^(-1/2)-1,
```

for `abs(u)<1` in the relativistic chart. The Newtonian chart is licensed only on a task/tolerance-dependent low-speed domain `abs(u)<=beta_N`; the relativistic chart may have a larger certified domain `abs(u)<=beta_R<1` under the chosen numerical and observational assumptions.

### 13.2 Overlap and bridge

On

```text
O_NR={u : abs(u)<=min(beta_N,beta_R)},
```

both outputs inhabit the same normalized observable space, so the output translation is identity. The bridge is approximate, not exact except at `u=0`.

For any `beta<1` and `abs(u)<=beta`:

```text
0 <= k_R(u)-k_N(u)
  <= u^4/(1-u^2)
  <= beta^4/(1-beta^2).
```

Thus a task whose accepted normalized bridge discrepancy is at least `beta^4/(1-beta^2)` can certify this particular low-speed correspondence, subject to model/numerical/measurement assumptions.

### 13.3 What the example does not show

It does not show that:

```text
full Newtonian mechanics equals special relativity on the overlap
the theories share every ontology or state variable
one theory is a coordinate re-expression of the other
their domains are manifold chart domains
transition maps are diffeomorphisms
gravity or accelerated frames are covered
the relativistic model is final or true.
```

It shows only that two explicitly typed predictors of one observable admit a quantified approximate bridge over a low-speed domain. This is enough for the project's retention/routing example and no more.

## 14. Elementary results

### Theorem 1: active-set decomposition

For finite ordinary use scopes `U_1,...,U_n subseteq T`, the cells `{C_S : S subseteq {1,...,n}}` are pairwise disjoint and their union is `T`.

**Proof.** Every `x in T` has a unique membership index set `S_x={i:x in U_i}` and hence belongs to `C_{S_x}`. If `x` belonged to `C_S` and `C_R`, its membership set would equal both `S` and `R`, so `S=R`. `square`

### Theorem 2: exact chart gluing

Let `{U_i}` cover `S`, and let `y_i:U_i->Y` satisfy `y_i(x)=y_j(x)` on every overlap. Then there exists a unique function `y:S->Y` whose restriction to every `U_i` is `y_i`.

**Proof.** Choose any chart containing `x` and set `y(x)=y_i(x)`. Overlap equality makes the definition independent of the choice. Any function with the stated restrictions must take that value, proving uniqueness. `square`

This is set-theoretic gluing. It does not establish a global scientific theory, smoothness, or truth.

### Theorem 3: approximate blend continuity and deviation

Let translated predictions `y_1,...,y_k` lie in a normed vector space and satisfy

```text
norm(y_i(x)-y_j(x)) <= delta
```

for every active pair on an overlap. For convex weights `w_j>=0`, `sum_j w_j=1`, let `y_b=sum_j w_j y_j`. Then for every active `i`:

```text
norm(y_b-y_i) <= delta.
```

If every `y_j` and `w_j` is continuous on the transition scope, then `y_b` is continuous there.

**Proof.** `y_b-y_i=sum_j w_j(y_j-y_i)`. Apply the triangle inequality and pairwise bound: `norm(y_b-y_i)<=sum_j w_j delta=delta`. Continuity follows because a finite sum of products of continuous scalar weights and vector-valued functions is continuous. `square`

The conclusion bounds deviation from component predictions, not error relative to the world.

### Theorem 4: approximate bridge composition

Under the assumptions of Section 8.2:

```text
d_k(T_jk(T_ij y_i),y_k)
  <= L_jk delta_ij + delta_jk.
```

**Proof.** Insert `T_jk y_j`, apply the triangle inequality, use the `L_jk`-Lipschitz property for the first term, and apply the two bridge bounds. `square`

### Proposition 5: safe routers fall back on atlas gaps

If `SafeRouter(A,pi)`, `x in Gap(A,zeta)`, and no separately licensed fallback model covers `x`, then `route_A(pi,x,zeta)` is an explicit fallback/information/abstention decision, not `UseChart(chi_i)`.

**Proof.** Every `UseChart` output must reference a chart in `Act_A(x,zeta)`. The active set is empty on a certified gap. The safe-router gap clause excludes raw unlicensed argmax. `square`

### Proposition 6: hard routing need not be representable by one standard ReLU output

Let affine experts be

```text
y_1(x)=0,
y_2(x)=1,
```

and hard router select `y_1` for `x<=0` and `y_2` for `x>0`. The composed real-valued output is a step function and cannot be represented exactly by a standard finite feed-forward ReLU network with real-valued output.

**Proof.** A finite composition of affine maps and ReLUs is continuous. The step output is discontinuous at `0`. `square`

An external discrete `argmax` or other discontinuous operation can implement the routing decision; the proposition concerns identification with the ordinary continuous ReLU output map.

### Proposition 7: activation/chart alignment need not be one-to-one

There exist faithful implementations with many activation cells per scientific state, and faithful scientific covers with several simultaneously active charts at a point but one generic activation pattern.

**Proof.** For the first direction, add a hidden ReLU feature whose activation boundary crosses the input while downstream weights cancel it; the computed license/selection state is unchanged but the activation complex is refined. For the second, let two charts be licensed on the same domain by the external semantics while a scorer network is affine with one activation cell and outputs two positive named surplus coordinates. The exact licensed state remains separate from those coordinates. Thus neither mapping is forced to be bijective. `square`

### Proposition 8: low-speed kinetic-energy bridge bound

For `abs(u)<1`:

```text
0 <= (1-u^2)^(-1/2)-1-u^2/2
  <= u^4/(1-u^2).
```

**Proof.** For `x=u^2 in [0,1)`, the binomial series is

```text
(1-x)^(-1/2)=sum_{n>=0} a_n x^n,
a_0=1,
a_1=1/2,
0<a_n<=1.
```

Therefore the nonnegative remainder after the linear term satisfies

```text
sum_{n>=2} a_n x^n
<= sum_{n>=2} x^n
=x^2/(1-x).
```

Substitute `x=u^2`. `square`

### Proposition 9: indexed signed margins recover active sets while argmax does not

Let a finite chart library have indexed signed margins `s_1(x),...,s_n(x)` satisfying the calibrated convention

```text
i in Act_A(x,zeta) iff s_i(x)>=0.
```

Then the signed vector recovers the complete Boolean active set by componentwise thresholding. A winner-only `argmax_i s_i(x)` is not sufficient in general.

**Proof.** The equivalence reconstructs membership for each index, hence the entire set. For insufficiency, with a deterministic first-index tie convention the vectors `(1,1)` and `(1,-1)` have the same argmax but active sets `{1,2}` and `{1}`. Also `(1,-2)` and `(-1,-2)` share the same argmax while their active sets are `{1}` and empty. Therefore the argmax cannot reconstruct simultaneous or empty active sets. `square`

## 15. Claim-ledger adjudications produced by this task

1. **E08:** the project can define a scientific licensed atlas, but “naturally forms an atlas” is a terminology/design choice, and not every overlap requires a successful bridge. Bridge obligations are operation-specific; unresolved status is allowed. The scoped construction is supported, while the stronger naturalness/universal-requirement reading remains unsupported.
2. **E11:** simultaneous, nested, coincident, and positive-extent overlapping licenses are formally representable; adequacy is nonexclusive. Empirical prevalence/usefulness remains for experiments.
3. **E12:** Theorem 1 proves the finite ordinary-set active-cell decomposition, with explicit qualification for unknown/graded membership.
4. **E13:** the bridge taxonomy is now typed, and Theorems 2–4 establish exact gluing and approximate blend/composition properties. Empirical usefulness of each bridge type remains task-specific.
5. **E14:** Proposition 5 formally establishes fallback/abstention behavior for certified gaps under the safe-router definition; empirical risk reduction remains untested.
6. **F27:** Proposition 7 supplies formal counterexamples to forced one-to-one activation/chart alignment.
7. **F28:** Theorem 3 proves the conditional continuity-compatible disagreement bound; semantic meaning and constraint preservation remain separate requirements.
8. **F30:** Proposition 9 proves that, for a finite indexed library, retaining one signed calibrated margin per chart recovers the pointwise active set by componentwise thresholding; an immediate argmax discards simultaneous and empty active sets.

No inherited row is newly marked `X1` in this task. The main correction to E08 is scoped as `I1`, not called falsification: the formal object works, while “naturalness” and universal bridge necessity are not theorem-level consequences.

## 16. Decisions fixed here

1. `Licensed model cover` is the weakest primary mathematical term; `scientific licensed atlas` means a cover plus overlap/bridge/seam/routing/provenance structure.
2. Literal differential-geometric identification requires separate manifold and transition-map axioms and is not assumed.
3. Charts bind versioned use plans to typed domains, evaluation specifications, frames, interfaces, licenses, and provenance.
4. Archive, hard, full-use, frontier, and selected chart views remain distinct.
5. Overlaps may be thick, nested, coincident, or unresolved; seams are routing transitions, not synonyms for overlaps.
6. Bridge status is directional, purpose-relative, typed, and multi-valued rather than one equivalence predicate.
7. Exact, approximate, statistical, decision, asymptotic, translation-only, incompatible, unknown, and not-required bridge statuses are distinct.
8. Approximate bridge errors compose and cycle defects must be audited.
9. Approximate compatibility does not determine a unique global glue or prove truth.
10. Blends are new use plans and require commensurate convex outputs, licensed supports, invariant checks, and their own evaluation.
11. Routers select chart identities/use plans and preserve traces; they are not identified with a single prediction map.
12. Scientific cover, router partition, and ReLU activation complex are three separate geometries with a many-to-many alignment relation.
13. Hard-routed expert compositions may be discontinuous and therefore not exactly one ordinary ReLU output.
14. The Newtonian/relativistic example is restricted to a quantified bridge between two kinetic-energy predictors on a low-speed overlap.

## 17. Questions for Checkpoint A

Checkpoint A should now determine:

- whether the minimal paper should use `licensed model cover` throughout and reserve “atlas” for motivation;
- whether `HardLicense` and competitive `PreferredUse` should be separated in the core predicate, given Tasks 10–11;
- which bridge kinds belong in the minimal calculus versus an extension;
- whether exact gluing and differential-atlas qualifications belong in the main text or a terminology appendix;
- whether the Newtonian kinetic-energy bound is an adequate motivating physics example or needs a second historically grounded case;
- which compatibility/cycle results require stronger proofs or literature support;
- how the Task 15 representation will encode bridge status, uncertainty, relation cells, and provenance without a quadratic explosion in chart pairs;
- how Task 17's explicit continuity/discontinuous-hard-routing obstruction should be operationalized in the matched experiment;
- how Task 19 experiments will create exact, approximate, incompatible, and unknown overlaps without defining domains circularly from the trained network.

**Post-checkpoint resolution.** Task 11A selects profile-indexed `Lic_P`. Read chart-use and active-set views as `Charts^use(A,P)` and `Act_A(x,zeta,P)`. Different selectors may induce different atlas views because each declares its required profile; archive, comparison, and selection information remain jointly displayable.

## Task conclusion

The finite-stage scientific object is now a partial, overlapping licensed model cover equipped with typed chart, overlap, bridge, seam, frontier, router, fallback, and provenance records. Exact equality is one bridge type rather than a universal stitching law; approximate and decision-level compatibility preserve their errors and purposes; unresolved seams remain operationally visible. The router over this atlas is distinct from both a single CPWL predictor and the ReLU activation complex used to score it. The low-speed kinetic-energy example supplies a rigorous but deliberately narrow Newtonian/relativistic bridge without claiming that scientific theories literally form a differential-geometric atlas. The finite-stage foundations are ready for Checkpoint A's roadmap audit.
