# Two Atlas Claims: Scientific Model Covers and ReLU Activation Complexes

Created: 2026-07-10  
Task: TODO Task 4  
Status: Conceptual and mathematical audit; cited external theorems remain unverified until Task 6/17.

## Executive answer

The project currently uses “atlas” for two different structures.

1. **Intrinsic ReLU atlas:** a fixed finite ReLU network partitions its input space into activation-pattern regions. On each region the network computes an affine map. Adjacent affine pieces agree exactly on their common boundary because they are restrictions of one continuous function.

2. **Scientific-model atlas:** a library of separately meaningful models has domains on which each model is licensed. These domains may overlap substantially, nest, coincide, or leave gaps. On overlaps the models may agree exactly, agree only within task tolerance, support the same decisions despite predictive differences, or disagree enough to require routing, further testing, or abstention.

The first is a structural fact about one function class. The second is the epistemic/computational object needed by the project. They should not be identified without an alignment argument.

The user's overlap observation improves the scientific picture. If models `M_1` and `M_2` are both licensed on the same domain `D`, the atlas need not discard `M_1` merely because `M_2` has lower error. It can retain:

- both adequacy records;
- their comparative risk/cost relation;
- a router's current preference;
- the possibility that the ranking changes on a subdomain, under another loss, or after new evidence.

If licensed domains `D_1` and `D_2` overlap, the system can distinguish

```text
D_1 \ D_2,
D_1 ∩ D_2,
D_2 \ D_1,
X \ (D_1 ∪ D_2).
```

The middle region is not merely a seam. It can have positive volume and can be the best place to compare, calibrate, blend, or test the two models. The final region is an explicit gap in which the system should fall back or abstain.

The recommended terminology is therefore:

- **activation complex** for the intrinsic polyhedral decomposition of one ReLU network;
- **licensed model cover** or **scientific model atlas** for model-indexed adequacy domains;
- **selection partition** for the regions on which a router chooses a particular model or model set.

These three objects can interact without being identical.

---

## 1. The motivating scientific structure

Let `X` be a space of cases. Let

```text
K_t = {M_1,...,M_n}
```

be the finite model library currently represented at stage `t`.

For each model `M_i`, suppose the system has:

- a prediction or local law `f_i`;
- a risk profile `J_i(x)` or domain risk `J_i(D)`;
- one or more signed margins `s_i`;
- a licensed domain `D_i`;
- evidence/provenance supporting the domain;
- output translations needed to compare it with other models.

A pointwise licensed domain can be defined extensionally as

```text
D_i = {x in X : s_i(x) >= 0}.
```

If domain-level certification is primary, `D_i` can instead be a declared set or distribution for which a risk guarantee has been established. These two meanings must remain distinct:

- **induced domain:** the set where a learned score is nonnegative;
- **certified domain:** a set/distribution over which a bound has been proved or calibrated.

The atlas should retain the relationship between them. An induced domain may approximate a certified domain, overgeneralize beyond it, or fail to cover all of it.

---

## 2. A scientific chart

A minimal scientific chart is not just a pair `(M,D)`. Define provisionally

```text
C_i = (M_i, D_i, f_i, L_i, epsilon_i, E_i, tau_i),
```

where:

- `M_i` identifies the model or model-building procedure;
- `D_i` is its licensed domain;
- `f_i` is its prediction/local-law interface;
- `L_i,epsilon_i` specify adequacy;
- `E_i` records evidence and provenance;
- `tau_i` translates model-specific output into a comparison interface when possible.

The translation `tau_i` matters because separately developed theories may not use the same variables or ontology. Their raw internal objects cannot always be averaged or compared directly. The atlas operates on shared observables or decisions only after an explicit translation.

A scientific atlas at stage `t` is then a finite family

```text
A_t = {C_i : M_i in K_t}
```

plus overlap, bridge, dominance, routing, and fallback data.

This is closer to an indexed database of locally licensed models than to a single global theory.

---

## 3. Covers may overlap and may be incomplete

Classical atlas language already suggests overlapping charts, but this project needs an even weaker object because complete coverage is not guaranteed.

Define the supported region

```text
X_supported = union_i D_i.
```

The uncovered region is

```text
G = X \ X_supported.
```

`G` is an epistemic/model gap. The appropriate response may be:

- abstain;
- retain the status quo;
- request measurements;
- use a verified fallback;
- search or construct another model;
- proceed under an explicitly degraded license.

Therefore “atlas” should not imply that current knowledge covers all possible cases. At a finite stage it is more accurate to speak of a **partial atlas** or **licensed cover of the supported region**.

---

## 4. Active-set decomposition of overlaps

Given licensed domains `D_1,...,D_n`, define for every subset `S` of `{1,...,n}` the active-set cell

```text
C_S = (intersection_{i in S} D_i)
      ∩ (intersection_{j not in S} (X \ D_j)).
```

At a point `x in C_S`, exactly the models indexed by `S` are licensed.

The nonempty cells partition `X` up to whatever boundary convention is adopted. There can be as many as `2^n` active sets, although typically far fewer occur.

### Two-model case

For two domains, the possible cells are:

```text
C_{1}   = D_1 \ D_2,
C_{2}   = D_2 \ D_1,
C_{1,2} = D_1 ∩ D_2,
C_empty = X \ (D_1 ∪ D_2).
```

This formalizes the user's proposed three-domain division, with a fourth gap cell when coverage is incomplete.

The overlap `C_{1,2}` is not automatically a thin boundary. It can be a large region on which both models remain licensed.

### Exact same-domain case

If

```text
D_1 = D_2 = D,
```

then the active set on `D` is `{1,2}`. Adequacy alone does not choose between them. A separate comparative relation is required.

---

## 5. Adequacy, dominance, and storage are different

Suppose on the same domain

```text
J_2(D) < J_1(D) <= epsilon.
```

Then:

- both models are adequate;
- `M_2` has lower risk under `J`;
- a risk-minimizing router prefers `M_2`;
- the atlas can still retain `M_1` and its domain.

This separates three questions:

### 5.1 License question

```text
Is M_i adequate on D?
```

Several models can answer yes.

### 5.2 Selection question

```text
Which licensed model should be used now?
```

The answer may depend on accuracy, cost, robustness, interpretability, latency, or risk.

### 5.3 Memory question

```text
Which learned model/domain records should the system retain?
```

Retention can be broader than the active selection frontier. A dominated model may remain useful as:

- a cheaper fallback;
- a diagnostic comparison;
- a local approximation under a changed tolerance;
- a component of a bridge model;
- historical evidence about domain structure;
- a source of interpretable rules;
- protection against catastrophic forgetting.

The logic should therefore avoid equating “not selected” with “forgotten” or “false.”

---

## 6. Dominance inside an overlap

At each case `x`, let the performance vector of model `M_i` be

```text
v_i(x) = (
    predictive risk,
    decision regret,
    computational cost,
    robustness deficit,
    explanation cost,
    ...
).
```

Lower is better componentwise for this convention.

Model `M_i` Pareto-dominates `M_j` at `x` if

```text
v_i,k(x) <= v_j,k(x) for every k,
```

with strict inequality for at least one component.

This induces several possible subdivisions of an overlap:

- region where `M_1` dominates;
- region where `M_2` dominates;
- region where neither dominates;
- region where both are effectively tied within uncertainty/tolerance.

Thus an overlap domain can be refined not only by which models are licensed, but by their comparative relationship.

For a finite library, a point can carry a full record:

```text
State(x) = {
    licensed model set,
    signed margin vector per model,
    pairwise dominance graph,
    selected model(s),
    fallback,
    provenance
}.
```

This is richer than a single winner label.

---

## 7. Why overlaps are useful

Overlap is not merely tolerated. It performs several epistemic and computational functions.

### 7.1 Comparison

If both models apply to the same cases, their losses and predictions can be compared directly.

### 7.2 Calibration

A trusted model can help calibrate a newer model in the shared regime.

### 7.3 Correspondence testing

An overlap can test whether a successor recovers a predecessor's successful predictions under limiting conditions.

### 7.4 Uncertainty estimation

Agreement among differently structured models can provide evidence of robustness; disagreement can reveal model uncertainty or missing variables.

### 7.5 Smooth routing

Overlaps allow routing weights to change gradually instead of switching at a single hard boundary.

### 7.6 Bridge construction

A dedicated bridge/correction model can be trained using records from the overlap.

### 7.7 Anomaly discovery

Unexpected disagreement inside a region where both models claim adequacy can defeat one or both licenses or motivate a domain split.

For these reasons the project should not aim to force model domains into disjoint tiles prematurely.

---

## 8. Bridges need not be exact

Let `O_ij = D_i ∩ D_j` be an overlap. Suppose both models can be translated into a common observable space `Y`:

```text
y_i(x) = tau_i(f_i(x)),
y_j(x) = tau_j(f_j(x)).
```

Several bridge relations are possible.

### 8.1 Exact predictive bridge

```text
y_i(x) = y_j(x) for every x in O_ij.
```

This is strongest and often unnecessary.

### 8.2 Approximate predictive bridge

```text
dist_Y(y_i(x),y_j(x)) <= delta_ij(x)
```

throughout a certified overlap. The allowance can reflect both models' error bars and the task tolerance.

### 8.3 Statistical bridge

The predictive distributions are close under a divergence or calibration criterion over the overlap distribution.

### 8.4 Decision bridge

The models may disagree predictively while inducing the same action or action ranking. For an acting system this can be sufficient.

### 8.5 Asymptotic/correspondence bridge

One model approaches the other's predictions in a limit or after a correction/coordinate transformation.

### 8.6 Translation bridge

The models use different internal objects, but maps `tau_i,tau_j` connect them to shared observables or intervention predictions.

### 8.7 Unresolved bridge

Both models are locally licensed by their own criteria but disagree beyond the accepted bridge tolerance. The atlas retains the disagreement as an anomaly rather than manufacturing continuity.

The bridge type should be stored as data. “Stitching” is not one universal equality condition.

---

## 9. Seams versus overlaps

A **seam** is a boundary across which the selected local rule changes. An **overlap** is a region where multiple local rules are simultaneously available.

They should not be treated as synonyms.

### Hard seam

A hard router chooses model `M_1` on one side and `M_2` on the other:

```text
F(x) = f_1(x) if r(x) <= 0,
       f_2(x) if r(x) > 0.
```

Unless the predictions agree on `r(x)=0`, the routed output can be discontinuous.

### Overlap transition

On an overlap, weights can vary continuously:

```text
F(x) = w_1(x)y_1(x) + w_2(x)y_2(x),
w_1(x)+w_2(x)=1,
w_i(x)>=0.
```

If the translated outputs and weights are continuous, then `F` is continuous even when `y_1` and `y_2` are not exactly equal. Exact seam agreement is therefore not necessary for continuous blending.

However, continuous blending is semantically justified only if:

- outputs inhabit a common affine/convex space;
- interpolation has a meaningful interpretation;
- the mixture respects hard constraints;
- weights are supported only where the corresponding models are licensed.

Averaging incompatible ontologies or mutually exclusive decisions can be meaningless even when it is numerically smooth.

---

## 10. An elementary blending bound

Suppose on an overlap `O`, two translated predictions satisfy

```text
norm(y_1(x)-y_2(x)) <= delta.
```

Let

```text
F(x)=w(x)y_1(x)+(1-w(x))y_2(x),
```

where `0<=w(x)<=1`. Then

```text
norm(F(x)-y_1(x)) <= delta,
norm(F(x)-y_2(x)) <= delta.
```

**Proof.**

```text
F-y_1 = (1-w)(y_2-y_1),
F-y_2 = w(y_1-y_2).
```

Taking norms and using `w,1-w<=1` gives the bounds.

Thus an approximate bridge can support a blend that remains within the pairwise disagreement tolerance of each model. This does not prove that the blend is closer to reality; it only bounds its deviation from the component predictions.

---

## 11. Router choices on overlaps

The atlas should support several policies rather than building one into the definition.

### 11.1 Best risk

Choose the licensed model with smallest estimated task risk.

### 11.2 Best positive margin

Choose the model with the largest hard/baseline/comparative slack.

### 11.3 Near-best set

Retain every model within `eta` of the best, then select by cost or robustness.

### 11.4 Pareto frontier

Return the undominated model set when no scalarization is justified.

### 11.5 Model averaging or mixture

Blend predictions when outputs are commensurate and mixture semantics is justified.

### 11.6 Bridge model

Use a separate correction or transition model in the overlap.

### 11.7 Conservative fallback

Select the safest model or abstain when disagreement exceeds tolerance.

### 11.8 Information-gathering action

Choose a measurement or experiment that best distinguishes the active models.

This last policy turns overlap disagreement into an active-learning signal.

---

## 12. The intrinsic ReLU activation complex

Now consider a fixed feed-forward ReLU network

```text
F = A_L ∘ ReLU ∘ A_{L-1} ∘ ... ∘ ReLU ∘ A_1,
```

where every `A_k` is affine.

For an input `x`, record the sign/activation state of every hidden preactivation. An activation pattern `sigma` identifies a region

```text
P_sigma = {x : network activation pattern is sigma}.
```

Once the activation states are fixed, every ReLU is either the identity or zero. Therefore the network reduces to an affine map on `P_sigma`.

The standard structural claims inherited from Fable are:

1. each nonempty activation region is polyhedral under the ordinary finite ReLU-MLP assumptions;
2. the regions cover input space;
3. their interiors are disjoint by activation pattern;
4. the network is affine on each region;
5. adjacent affine restrictions agree on their shared boundary because the global network is continuous;
6. derivatives/Jacobians can change across boundaries;
7. depth can represent many more or more efficiently arranged regions than one affine threshold.

Tasks 6 and 17 must verify the exact theorem statements, boundary conventions, converse results, and quantitative depth claims against primary sources. The current task treats them as a precise research target, not as already audited literature.

---

## 13. What Fable gets structurally right

Fable's strongest useful observation is:

> The local-affine chart structure is native to a ReLU network; it is not added after training as a visualization.

This matters because a network does not merely output a score. It already computes through a collection of local affine laws selected by activation patterns.

Several parts of the analogy are mathematically well motivated:

- activation pattern ↔ intrinsic chart index;
- activation region ↔ domain of one affine restriction;
- affine restriction ↔ local computational law;
- shared facet ↔ intrinsic seam;
- gradient/Jacobian change ↔ change of local law;
- depth ↔ hierarchical construction of complex regions.

This supports a representation theorem of the form:

```text
finite ReLU function
    -> finite polyhedral complex with compatible affine restrictions.
```

It does not yet support the semantic claim that those restrictions are scientific theories.

---

## 14. Where Fable's identification is too strong

### 14.1 A linear region is not automatically a scientific model

An activation region is defined by hidden sign patterns. It may split one scientifically meaningful domain into thousands of computational pieces, or one piece may cut across several human domain categories.

### 14.2 Exact boundary agreement is weaker than scientific correspondence

Two affine restrictions of one continuous network agree on their common facet because they are the same function there. Newtonian and relativistic models are separately defined theories whose correspondence is normally approximate or asymptotic over a region, not identity on one codimension-one boundary.

### 14.3 An intrinsic complex has essentially disjoint interiors

The scientific atlas can have large overlaps with several simultaneously valid models. One activation pattern is active at each generic point of a deterministic network, even though many hidden units are active. Thus an intrinsic region partition does not directly encode a set of overlapping model licenses.

### 14.4 A unit need not be a model or license

The one-unit/one-license interpretation can fail under superposition, cancellation, and basis symmetries.

### 14.5 Depth supplies expressivity, not semantics

A deep network can form bounded and disconnected acceptance regions, but this does not determine what those regions mean.

### 14.6 A fixed network is finite-stage

A fixed finite ReLU network has finitely many parameters and finitely many activation patterns. It cannot literally store an indefinitely growing explicit library without expansion, retraining, compression, or external memory.

### 14.7 One network's continuity may be the wrong obligation

Scientific models can disagree in an overlap while both remain useful for different purposes. Forcing them into one continuous output may hide rather than represent the disagreement.

The safe conclusion is structural equivalence at the function level, followed by a separate alignment problem.

---

## 15. The router has its own activation complex

An explicit model-library architecture can separate scientific charts from neural computation:

```text
for each model i:
    score_i(x) = signed license margins
    content_i(x) = model prediction/local law

router(x) = choose/blend/abstain from licensed models.
```

Here:

- `{D_i}` is the scientific licensed cover;
- the vector of active model licenses is an active set `S(x)`;
- the router may itself be a ReLU network;
- the router's activation regions form an intrinsic activation complex;
- the selected-model regions form a selection partition.

Thus there can be three nested geometries:

```text
scientific licensed domains
    -> overlap active-set cells
    -> router activation regions / selection cells.
```

The router's complex may refine the scientific overlap cells. Many intrinsic regions can map to the same active model set or selected model. A one-to-one correspondence is neither necessary nor likely.

---

## 16. A formal alignment target

Let

- `P_sigma` be intrinsic activation regions of the neural scorer/router;
- `C_S` be active-set cells of the scientific licensed cover;
- `Q_r` be final selection regions of the router.

An alignment map might assign each intrinsic region a scientific state:

```text
lambda(P_sigma) = (
    active model set S,
    component margin signs/order,
    selected model set r,
    bridge status
).
```

The desired relation need not be bijective. A realistic target is a refinement:

```text
each P_sigma lies mostly within one scientifically labeled C_S,
```

while several `P_sigma` may share the same label.

Alignment should be evaluated through:

### 16.1 License fidelity

Do neural score signs match the intended licensed domains?

### 16.2 Overlap fidelity

Does the network preserve multiple simultaneous licenses rather than collapse immediately to one label?

### 16.3 Gap fidelity

Does it abstain where the scientific cover has no licensed model?

### 16.4 Comparative fidelity

Are risk/dominance relations inside overlaps preserved?

### 16.5 Bridge fidelity

Are exact, approximate, decision, and unresolved bridges represented distinctly?

### 16.6 Local-law fidelity

Does routed content match the model whose license was evaluated?

### 16.7 Stability

Do the labels/relations persist across random seeds, retraining, and mild distribution shifts?

### 16.8 Minimality/compression

Can many activation regions be summarized by a smaller scientifically meaningful cover without losing predictive or license fidelity?

This is the central empirical/theoretical bridge between the two atlas claims.

---

## 17. Capacity and “remember every model/domain”

The user's intuition can be made precise at a finite stage.

For a finite library of `n` models, an architecture with one indexed score/margin head per model can retain:

```text
(s_1(x),...,s_n(x))
```

and hence the complete licensed active set at `x`. With sufficient representational capacity and training coverage, it can approximate complicated `D_i` and their overlaps.

But four qualifications are necessary.

### 17.1 Finite capacity

A fixed finite network cannot explicitly distinguish arbitrarily many independent model/domain records. “Enough capacity” must scale with library complexity.

### 17.2 Continual addition

Adding `M_{n+1}` may require a new head, parameters, external memory, or retraining. Ordinary training can alter old domains and cause forgetting.

### 17.3 Compression and interference

A shared representation can compress recurring structure across models, but superposition can also cause interference. Exact retention and efficient compression are separate goals.

### 17.4 Evidence/provenance storage

Margins alone do not store why each model/domain license was granted. A registry or memory should retain model identity, domain definition, evidence, and revision history.

The most natural open-ended architecture may therefore be hybrid:

```text
external/expandable model registry
    + learned encoders and score predictors
    + ReLU router with finite current computation.
```

At each stage the active neural system is finite; over time the registry and network sequence can grow. This matches the project's open-ended epistemology better than claiming one fixed MLP contains every future theory.

---

## 18. Updating the atlas when a new model arrives

Suppose stage `t` has atlas `A_t` and a new model `M_{n+1}` is learned.

A disciplined update is:

1. Preserve prior model/domain/evidence records.
2. Estimate or certify the new model's signed margins.
3. Construct its licensed domain `D_{n+1}`.
4. Compute new active-set overlaps with existing domains.
5. Evaluate pairwise predictions, losses, costs, and bridge types on overlaps.
6. Update dominance/frontier relations.
7. Update routing while retaining fallback and abstention.
8. Recheck old licenses on stored records to detect forgetting.
9. Store unresolved disagreements as anomalies, not forced seams.

The addition of a better model does not automatically delete an old chart. It changes the comparative structure and selection policy.

This yields a clear distinction:

```text
library growth is monotone in stored records,
current selection is nonmonotone,
empirical licenses remain defeasible.
```

---

## 19. A two-model worked example

Let

```text
D_1 = {x : s_1(x) >= 0},
D_2 = {x : s_2(x) >= 0}.
```

Assume all outputs are translated to a common scalar observable.

### Region A: only `M_1` licensed

```text
x in D_1 \ D_2.
```

Use `M_1` if it also beats the fallback; otherwise abstain.

### Region B: overlap

```text
x in D_1 ∩ D_2.
```

Both are adequate. Record:

```text
s_1(x), s_2(x),
J_1(x), J_2(x),
dist(y_1(x),y_2(x)),
cost_1(x), cost_2(x).
```

Possible actions:

- choose the lower-risk model;
- choose the cheaper near-best model;
- keep both as a Pareto set;
- blend if translation/interpolation is meaningful;
- abstain or gather information if disagreement is anomalous.

### Region C: only `M_2` licensed

```text
x in D_2 \ D_1.
```

Use `M_2` subject to fallback/hard constraints.

### Region D: gap

```text
x outside D_1 ∪ D_2.
```

Use the fallback or abstain.

### Same-domain variant

If `D_1=D_2=D` and `J_2<J_1` everywhere, both licenses remain stored. A risk-only router always selects `M_2`, but `M_1` may remain on the archive/fallback layer. If `M_1` is cheaper, the models may both remain Pareto-undominated.

This example captures the intended “keep track of every learned model and domain” behavior without claiming every stored model must be active.

---

## 20. Recommended provisional definitions

### Definition 1: licensed model cover

A licensed model cover of a supported region `S subseteq X` is a finite family

```text
{(M_i,D_i,s_i,E_i)}_{i=1}^n
```

such that

```text
S subseteq union_i D_i.
```

The domains may overlap. Equality with `X` is not required.

### Definition 2: overlap relation

For each nonempty `O_ij=D_i∩D_j`, store comparison and bridge data

```text
R_ij = (
    risk/dominance relation,
    output translation,
    bridge type and tolerance,
    disagreement/anomaly status
).
```

### Definition 3: active-set cell

`C_S` is the set of points at which exactly the model indices in `S` are licensed.

### Definition 4: selection policy

A selection policy maps

```text
(x, active models, margins, costs, bridge data)
```

to a model, model set, mixture, information-gathering action, fallback, or abstention.

### Definition 5: intrinsic activation complex

The activation complex of a finite ReLU network is the collection of activation-pattern polyhedra together with the affine restriction of the network to each cell and their shared-face relations.

### Definition 6: atlas alignment

An alignment relates intrinsic activation cells to scientific active-set/selection states and is evaluated by license, overlap, gap, comparative, bridge, local-law, and stability fidelity.

These definitions will be typed and refined in Tasks 7, 8, and 11.

---

## 21. Audit of the main inherited atlas statements

| Inherited statement | Current disposition | What remains to establish |
|---|---|---|
| A ReLU network is piecewise affine on activation regions. | Precise structural claim; formally checkable and literature-addressable. | Verify exact theorem and conventions. |
| Activation regions form an atlas of local affine laws. | Useful terminology if called an intrinsic activation complex/atlas. | Avoid importing scientific semantics. |
| Adjacent pieces have exact bridges. | Correct in the sense of equality of one continuous network's restrictions on a shared boundary, conditional on ordinary ReLU assumptions. | Verify statement; do not equate it with physical-theory overlap. |
| Jacobian change is rank one when one unit switches. | Scoped generic algebraic claim. | Verify assumptions and counterexamples with multiple switches. |
| Depth is forced by realistic domains. | Too strong without qualifications. | Show necessity/efficiency only relative to primitive half-space tests, target family, width, and approximation metric. |
| Every scientific regime is a ReLU chart. | Unestablished semantic claim. | Define and test alignment. |
| ReLU exact seams model Newton/Einstein correspondence. | Suggestive analogy, not established. | Use approximate/asymptotic bridge definitions and real examples. |
| Smooth blending solves atlas stitching. | Conditional. | Require common output space, meaningful interpolation, licensed supports, and constraint preservation. |
| A sufficiently large fixed network remembers every model/domain. | Valid only for a finite scoped library and representation target. | Give capacity/continual-learning bounds or use expandable memory. |

No row is labeled true or false here beyond elementary conditional derivations. Literature claims remain `L0` until verified.

---

## 22. What Task 4 establishes

Task 4 establishes a clean separation:

```text
Scientific atlas:
    overlapping, partial, model-indexed, evidence-bearing,
    possibly inconsistent, with approximate or unresolved bridges.

ReLU activation complex:
    finite, polyhedral, activation-indexed,
    exactly compatible as pieces of one continuous CPWL function.

Selection partition:
    induced by the router over licensed models,
    possibly hard, soft, set-valued, or abstaining.
```

The scientific atlas can be implemented with help from ReLU networks without being reduced to one network's activation partition.

The central research question becomes:

> Can a loss-grounded, trace-preserving ReLU scorer/router represent the active licensed model sets, overlap relations, gaps, and selection rules of a scientific atlas, while retaining enough capacity and provenance to add new model/domain records without erasing old ones?

This question is formally and empirically testable in finite settings. The indefinite version requires a sequence of finite systems or expandable external memory.

---

## 23. Handoff to later tasks

Task 5 should decide whether “scientific atlas” or “licensed model cover” is the primary term and state the non-goal of literal differential-geometric identification.

Task 7 should type cases, domains, translations, models, risks, evidence, and active-set cells.

Task 8 should define licenses and gaps, including the distinction between induced and certified domains.

Task 10 should define pointwise/domain Pareto dominance and archive versus active frontier.

Task 11 should turn the provisional definitions into the formal atlas chapter.

Task 15 should choose representations for model/domain/overlap records and external memory.

Task 16 now chooses a hybrid ReLU statistic scorer plus symbolic decoder/mask, preserving all simultaneous licenses before a separate active-set-restricted selector; hard MoE remains a seam-specific comparator in [`ml/02_relu_architecture.md`](../ml/02_relu_architecture.md).

Task 17 should verify the CPWL, continuity, converse, rank-change, and depth results from primary sources.

Tasks 19–21 should use synthetic overlapping domains with a known gap and measure active-set, selection, bridge, and abstention fidelity.

Task 23's [`policy_value_interpretability.md`](policy_value_interpretability.md) makes this a seven-axis companion/future-work test rather than a positive result: domain/trace structure must improve declared usefulness or human audit performance, and router complexity alone is not transparency.

## Task conclusion

Atlases need not be perfectly stitched only at thin seams. The scientific object should admit large overlaps, nested domains, coincident domains, unresolved disagreements, and uncovered gaps. Overlaps are where comparison, correspondence, calibration, blending, and anomaly discovery become possible.

The exact seam compatibility of a ReLU network is still valuable, but it belongs to a different object: the intrinsic activation complex of one continuous piecewise-affine function. A scientific model library should normally be represented as an overlapping licensed cover, with a router whose own neural activation complex may refine—but need not equal—the scientific domains.
