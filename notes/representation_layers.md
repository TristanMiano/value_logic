# Representation Layers and the Location of Information

Created: 2026-07-10  
Task: TODO Task 3  
Status: Encoding problem and information audit; no final neural architecture selected.

## Executive answer

`Pi(M,D,epsilon)` should not be identified with one vector, one neuron, or one ReLU activation.

At least seven distinguishable objects appear between the original pragmatic judgment and a model's eventual action:

1. a structured, typed license judgment;
2. evidence and records used to evaluate it;
3. vector encodings of models, cases, domains, tasks, and fallbacks;
4. predicted losses or risks;
5. signed adequacy, improvement, and comparative margins;
6. rectified gates or routing weights;
7. licensed predictions, explanations, or actions.

These layers carry different information. A positive ReLU activation can encode both a Boolean fact—“the margin is positive”—and a magnitude—“the candidate has this much positive slack.” But a zero activation merges exact indifference with every degree of failure. Therefore ReLU is naturally a **gate plus positive margin**, not a complete representation of the underlying judgment.

The central encoding problem is best stated loss-first:

> Given a library of models, a bank of cases or domains, observed outcomes, task losses, fallbacks, and tolerances, learn representations that predict the relevant loss/risk profile and preserve the comparisons needed for licensing, routing, abstention, and explanation.

This “works backward” from operational loss or negative utility. It does not assume that hand-written vector coordinates such as “handles strong gravity” are already available. It also does not imply that learned coordinates are a unique ontology: many vector bases can encode exactly the same loss predictions.

The minimum transparency requirement is therefore not that every semantic object be compressed into one vector. It is that the maps between layers be explicit enough to answer:

- which information was used;
- which information was discarded;
- what claim the scalar margin certifies;
- why a gate opened or remained closed;
- which model content was routed downstream;
- on which domains that explanation is licensed.

---

## 1. The structured object comes first

Task 2 recommended factoring the pragmatic use-license into three conditions:

```text
Pi = certified hard adequacy
     + sufficient improvement over a fallback
     + admissibility among retrieved alternatives.
```

Written more explicitly,

```text
Pi_{a,t,b}(M;D,L,epsilon,alpha,B,Delta,K | E_t).
```

The fields have different types:

- `a`: agent or evaluator;
- `t`: evidence/revision stage;
- `b`: search or computation budget;
- `M`: model, theory, or model-building procedure;
- `D`: domain, case set, distribution, or task family;
- `L`: local loss and domain-risk rule;
- `epsilon`: hard loss tolerance;
- `alpha`: calibration, confidence, or coverage level;
- `B`: fallback model or policy;
- `Delta`: required improvement over the fallback;
- `K`: retrieved/evaluated model library;
- `E_t`: evidence, records, or provenance at the current stage.

This is a structured record before it is a vector. Vectorization is a representation map applied to some of these fields. It is not an argument that the fields have the same semantics.

A useful programming analogy is a typed struct:

```text
LicenseRequest {
    model: Model,
    domain: Domain,
    loss: LossSpec,
    hard_tolerance: Tolerance,
    confidence: CalibrationSpec,
    fallback: PolicyOrModel,
    improvement_margin: Cost,
    candidate_library: Set<Model>,
    evidence: RecordSet,
    agent_stage_budget: EpistemicIndex
}
```

A network may encode this record, but the logic should not forget that it was typed.

---

## 2. A representation pipeline

Let `Omega` denote the full structured state relevant to a license request. A generic pipeline is

```text
Omega
  --encode--> z
  --risk predictor--> r_hat
  --compare--> s
  --rectify/route--> g
  --apply licensed content--> y_hat or action.
```

In more detail:

```text
(M,D,L,epsilon,B,Delta,K,E_t,...)
    -> (m,d,l,e,b,k,...)
    -> predicted risk profile R_hat
    -> signed margins s_hard, s_base, s_library
    -> license bit / ReLU slack / abstention / routing weights
    -> model prediction, local rule, explanation, or action.
```

Each arrow is a potential source of compression, invariance, approximation, and information loss.

The project should ask a different question at every arrow:

1. **Encoding:** Does the vector retain the distinctions the downstream task needs?
2. **Risk prediction:** Does the scalar/vector estimate the operational target and generalize?
3. **Comparison:** Is the margin calibrated and monotone in its thresholds?
4. **Rectification:** What negative or boundary information is intentionally discarded?
5. **Routing:** Does the selected content correspond to the model whose license was evaluated?
6. **Action:** Can the final choice be traced back through the relevant comparisons?

---

## 3. What “information is preserved” can mean

There is no single notion of information preservation. Let `e:Omega -> Z` be an encoder.

### 3.1 Lossless encoding

The strongest requirement is injectivity:

```text
e(omega_1) = e(omega_2) implies omega_1 = omega_2.
```

Then a decoder can in principle recover the exact structured input. This is rarely necessary and may be impossible or undesirable for large models and domains.

### 3.2 Task sufficiency

An encoding can discard raw details while retaining everything needed to predict a target `Y`. A statistical sufficiency condition is

```text
Y independent of Omega given e(Omega).
```

For this project, possible targets include:

- pointwise loss;
- domain risk;
- whether a hard threshold is met;
- improvement over a baseline;
- action rankings;
- the identity of an undominated model.

An encoding sufficient for one target may be insufficient for another. The mean loss can be sufficient for an expected-risk license while losing the tail information needed for a worst-case license.

### 3.3 Decision sufficiency

An encoding is decision-sufficient for an action rule if using only the encoding yields the same optimal decisions as using the full object, within a stated regret tolerance.

This is weaker than reconstructing the whole loss surface. Two models can differ predictively while remaining decision-equivalent on the available action set.

### 3.4 Approximate sufficiency

Exact preservation is often unnecessary. Let `T(Omega)` be the target and `T_hat(e(Omega))` its reconstruction. An approximate representation can be judged by a distortion bound:

```text
dist(T_hat(e(Omega)), T(Omega)) <= delta.
```

The acceptable `delta` must itself be tied to the downstream license. An embedding error of `delta` is harmless far from a threshold and potentially decisive near it.

### 3.5 Interpretive sufficiency

A representation can predict perfectly but remain opaque. Interpretive sufficiency asks whether the representation supports stable, human-usable descriptions or causal tests. This is not guaranteed by low prediction loss.

---

## 4. What should represent a model?

A “model vector” can be constructed in several non-equivalent ways.

| Representation | Encodes | Advantages | Main losses/ambiguities |
|---|---|---|---|
| Learned model-ID embedding | Identity relative to training records | Small; easy to train | No cold start; coordinates lack direct semantics |
| Flattened parameters | One parameterization of implementation | Contains exact weights | Huge; permutation/scaling symmetries; functionally equivalent weights differ |
| Functional fingerprint | Outputs on a probe set | Invariant to many weight symmetries; behavior-grounded | Only as complete as probes; misses off-probe behavior |
| Loss-profile row | Performance across cases/tasks | Directly aligned with adequacy | Collapses mechanisms producing the same losses |
| Structural/compositional code | Laws, corrections, modules, assumptions | Potentially interpretable and supports recombination | Requires ontology/schema; may be hand-engineered |
| Hidden-representation summary | Internal features/activations | Useful for mechanistic comparison | Basis dependence, superposition, state dependence |
| Source text/equations encoder | Description of theory/model | Can support new models | Meaning depends on learned language representation |

No single representation dominates for every purpose.

For the current project, a loss-profile representation is the cleanest operational starting point because the intended license is about performance. But a loss profile should not be mistaken for the model's ontology or mechanism. Two structurally different theories can produce the same observed loss row on the current record bank.

---

## 5. What should represent a case or domain?

A case `x` and a domain `D` are not the same object.

### 5.1 Case encoding

A case encoder

```text
phi_X: X -> R^p
```

maps one situation to a vector. It may use raw measurements, learned features, dimensionless physical quantities, state histories, or belief states.

### 5.2 Domain encoding

A domain may be:

- a subset of cases;
- a probability distribution;
- an empirical sample;
- a family of interventions;
- a task description plus tolerances;
- a region described by constraints.

Encoding a domain as one vector requires an aggregation or set/distribution encoder:

```text
phi_D(D) in R^q.
```

Possible representations include:

- parameters of a known distribution;
- moments or quantiles;
- an empirical measure;
- a permutation-invariant set encoder;
- a kernel mean embedding;
- a constraint/polytope description;
- learned task metadata;
- log dimensionless physical groups.

### 5.3 A single domain vector can be insufficient

Suppose two domains have the same mean case vector but different tails. They may have identical mean embeddings and radically different worst-case risk. Therefore a domain encoding is adequate only relative to the risk functional it must support.

If the license uses expected risk, a particular summary may suffice. If it uses worst-case or tail risk, the encoding must preserve more of the distribution or set geometry.

### 5.4 A pointwise score does not yet license a domain

A neuron applied to `phi_X(x)` evaluates one case. To obtain

```text
Pi(M,D,epsilon),
```

the system must aggregate or certify scores over `D`:

```text
R_hat(M,D) = rho_D(x -> ell_hat(M,x)).
```

The domain may then be induced extensionally as

```text
D_M(epsilon) = {x : R_or_local_loss(M,x) <= epsilon},
```

but this induced set is different from a prior domain descriptor supplied to the request. Later tasks must distinguish:

- a domain given as input;
- a domain inferred from cases;
- the acceptance region induced by a learned score.

---

## 6. Loss-first encoding

The loss-first strategy begins with operational records rather than semantic coordinate labels.

Let

- `M_1,...,M_n` be candidate models;
- `x_1,...,x_m` be cases;
- `L_1,...,L_r` be evaluation rules.

Construct a loss tensor

```text
T[i,j,k] = ell_{L_k}(M_i,x_j).
```

If domains rather than individual cases are the primitive evaluation units, use

```text
T[i,d,k] = R_{D_d,L_k}(M_i).
```

The representation problem is to learn encoders and a scorer such that

```text
R_hat_{i,d,k}
    = g(m_i, d_d, l_k, context)
    approx T[i,d,k].
```

Here:

```text
m_i = e_M(M_i),
d_d = e_D(D_d),
l_k = e_L(L_k).
```

A simple bilinear special case is

```text
log R_hat_{i,d}
    = c_i + r_d - <m_i,d_d>.
```

This can be read as a learned compatibility between a model's performance profile and a domain's demands. The semantics of the coordinates is relational: they are whatever latent factors help reconstruct the observed loss matrix.

### 6.1 What the loss tensor contains

It contains information about:

- which models work on which recorded cases/domains;
- relative and cardinal loss differences, if the loss scale supports them;
- correlations that can reveal latent capability/demand axes;
- gaps in record coverage.

### 6.2 What the loss tensor omits

It does not by itself contain:

- why a model succeeds;
- its internal mechanism or ontology;
- behavior on unrecorded cases;
- the provenance/reliability of measurements unless separately encoded;
- causal effects of changing a latent feature;
- a unique coordinate system.

This is why loss-first representation is operationally grounded but not automatically mechanistically interpretable.

---

## 7. Loss, inverse utility, and preference

The user-proposed “work backward from loss or inverse utility” can be stated precisely.

If lower loss is better and the loss is cardinal, define a utility-like score

```text
U(M,D) = -R(M,D)
```

or, relative to a fallback,

```text
U_B(M,D) = J(B,D) - J(M,D).
```

Then maximizing utility is equivalent to minimizing the chosen loss.

But this is a representation choice, not a discovery that all utility is negative loss. Several cautions apply:

1. An ordinal preference determines only rankings, not unique cardinal differences.
2. Positive affine transformations of utility can preserve choices while changing raw margins.
3. Multi-objective preferences may not admit a justified scalar utility.
4. Behavior alone does not identify reward/utility without environmental and rationality assumptions.
5. A learned loss predictor describes performance under the selected evaluation rule, not necessarily what the original agent “really values.”

The safe claim is:

> Once a task loss or utility convention is fixed, one may encode the same comparisons in loss-minimizing or utility-maximizing form.

The unsafe claim is:

> Any learned negative-loss score is the agent's uniquely recovered utility.

---

## 8. From predicted risk to signed margins

Suppose the representation produces a predicted task loss

```text
J_hat(M,D).
```

Task 2 identified three distinct comparisons.

### 8.1 Hard-adequacy margin

```text
s_hard(M,D) = epsilon_hard - J_hat(M,D).
```

### 8.2 Fallback-improvement margin

```text
s_base(M,D) = J_hat(B,D) - J_hat(M,D) - Delta.
```

### 8.3 Near-best margin

Let

```text
J_hat_star(K,D) = min_{M' in K} J_hat(M',D).
```

Then

```text
s_lib(M,D) = eta - (J_hat(M,D) - J_hat_star(K,D)).
```

Each score has a different meaning:

- `s_hard`: slack relative to an external ceiling;
- `s_base`: surplus relative to the outside option;
- `s_lib`: slack relative to the best retrieved model.

A scalar combined license could use

```text
s_all(M,D) = min(s_hard, s_base, s_lib),
```

because all requirements hold exactly when their minimum is nonnegative. This minimum is valid only if the conditions have been normalized into comparable signed margins. Otherwise the system should retain a margin vector and use componentwise gates.

### 8.4 Why one score can hide useful information

If `s_all=-2`, the number does not say whether the model failed safety, lost to the baseline, or was merely noncompetitive. A transparent system should preserve the individual margin vector

```text
s(M,D) = (s_hard, s_base, s_lib, ...)
```

even if a downstream gate uses `min(s)`.

This is an example of deliberate compression: the minimum is sufficient for conjunction but insufficient for diagnosis.

---

## 9. What ReLU represents

Let

```text
a = ReLU(s) = max(0,s).
```

### 9.1 Information retained for positive scores

When `s>0`, the activation retains:

- the fact that the strict threshold was passed;
- the positive margin magnitude;
- ordering among positive margins, subject to scale.

### 9.2 Information lost for nonpositive scores

For every `s<=0`,

```text
ReLU(s)=0.
```

Thus the output alone cannot distinguish:

- exact indifference `s=0`;
- a tiny failure `s=-0.001`;
- a catastrophic failure `s=-10^6`.

This can silence that one nonpositive channel, which is useful inside an
already authorized multiplicative content interface, but it does not
quarantine a whole downstream network: biases and bypass paths can remain
active. It is also harmful for diagnosis, learning, and transparency.

### 9.3 A two-channel signed representation

Define

```text
s_plus  = ReLU(s),
s_minus = ReLU(-s).
```

Then

```text
s = s_plus - s_minus,
abs(s) = s_plus + s_minus.
```

The pair is an exact representation of the signed scalar. A transparent architecture can:

- route licensed content only through `s_plus`;
- retain `s_minus` for diagnostics, defeat explanations, or learning;
- treat `(0,0)` as exact boundary/indifference.

Together with an exact symbolic active mask, this can preserve quarantine at a
declared content interface without destroying negative-margin information
globally. The ReLU pair alone does not authorize the route or prove
non-explosion; Task 16's `F18` counterexample is the controlling correction.

### 9.4 The scale problem remains

Even when ReLU preserves positive magnitude, that magnitude is meaningful only relative to the scale of `s`. Rescaling loss and tolerance rescales the margin. Downstream layers should not compare margins across tasks unless they are calibrated or normalized.

### 9.5 ReLU is not a probability

An activation of `2` is not twice as true as an activation of `1`, nor is it a 200% probability. It is a margin in whatever units the comparison defines. A probability interpretation requires an additional calibrated link function and statistical semantics.

---

## 10. Five elementary representation results

### Proposition 1: ReLU is non-injective on the failure region

For any `s_1,s_2<=0`,

```text
ReLU(s_1)=ReLU(s_2)=0.
```

Therefore the rectified scalar is insufficient to recover degree of failure.

### Proposition 2: paired ReLUs exactly encode a signed scalar

For every real `s`,

```text
s = ReLU(s) - ReLU(-s).
```

**Proof.** If `s>=0`, the right side is `s-0`. If `s<0`, it is `0-(-s)=s`.

### Proposition 3: a calibrated prediction buffer can certify adequacy

Suppose

```text
abs(J_hat(M,D)-J(M,D)) <= delta.
```

If

```text
J_hat(M,D) <= epsilon-delta,
```

then

```text
J(M,D) <= epsilon.
```

**Proof.** `J <= J_hat+delta <= epsilon`.

This shows how representation error should reduce the usable margin rather than disappear from the license.

### Proposition 4: bilinear embeddings are not uniquely identified

Suppose a score uses

```text
<m,d>.
```

For any invertible matrix `A`, define

```text
m' = A m,
d' = A^{-T} d.
```

Then

```text
<m',d'> = <m,d>.
```

Therefore identical loss predictions can arise in infinitely many latent coordinate systems. Coordinate-level semantic claims require additional constraints, probes, or interventions.

### Proposition 5: conjunction compression loses failure identity

Let

```text
s_all = min(s_1,...,s_k).
```

The condition `s_all>=0` is equivalent to every `s_i>=0`, so the minimum is sufficient for the Boolean conjunction. But `s_all` alone generally does not identify all failed conditions or their margins. Distinct margin vectors can have the same minimum.

This justifies retaining the full margin vector alongside any combined gate.

---

## 11. Identifiability and equivalence classes

A learned representation is usually identifiable only up to transformations that preserve its outputs.

### 11.1 Weight symmetries

Hidden units can often be permuted without changing the network function. Positive rescalings can also move magnitude between adjacent ReLU layers. A particular neuron index is therefore not automatically a stable semantic object.

### 11.2 Embedding basis symmetries

As Proposition 4 shows, model and domain embeddings can rotate or shear together while preserving bilinear scores.

### 11.3 Behavioral equivalence

Two models may agree on all recorded cases while diverging elsewhere. Relative to the record bank they belong to the same observational equivalence class.

### 11.4 Loss equivalence

Two mechanisms may have the same loss profile but different predictions, explanations, or failure modes. Loss-factor embeddings collapse them unless additional targets are included.

### 11.5 Preference equivalence

Different utilities can induce the same policy on the observed feasible sets. Policy reconstruction identifies at most an equivalence class without stronger assumptions.

The project should therefore prefer claims of the form

```text
the representation is sufficient for target T on domain D up to equivalence E
```

over claims that the representation uniquely recovers “the true ontology” or “the true utility.”

---

## 12. Incoming tests and outgoing content

Fable's commentary suggests that a neuron contains two roles:

- incoming weights implement a test;
- outgoing weights specify what content the activated unit contributes.

This is a useful idealized decomposition. For a hidden unit

```text
h_i(x) = ReLU(<w_i,x>+b_i),
```

the incoming parameters `(w_i,b_i)` determine the activation region and margin. Its outgoing column contributes

```text
v_i h_i(x)
```

to the next layer. One can read this as:

```text
if test_i passes with margin h_i, transmit content direction v_i with that strength.
```

But a standard dense MLP does not guarantee that one unit corresponds to one human-interpretable license:

- content is distributed across many paths;
- units may be polysemantic;
- basis changes can alter unit meanings;
- later layers can cancel or repurpose a contribution;
- outgoing content may not be independently identifiable.

A modular gating architecture makes the distinction more explicit:

```text
gate_i(x) = license margin for model i,
expert_i(x) = prediction/content of model i,
output(x) = Route({gate_i, expert_i}).
```

The present task does not select modular routing over a plain MLP. It records the trade-off: a monolithic MLP may be compact and expressive, while an explicit gate/expert separation is easier to interpret and verify.

---

## 13. Nested representations and multilayer recursion

A first layer can compute local scores:

```text
h_1 = ReLU(W_1 z+b_1).
```

A second layer can compute tests over the first layer's margin profile:

```text
h_2 = ReLU(W_2 h_1+b_2).
```

This makes nested computation possible:

- first-order features: local correction sizes, state properties, or constraint margins;
- second-order features: adequacy of a model configuration;
- third-order features: adequacy of a router, policy, or whole modeling strategy.

However, depth alone does not establish this semantic hierarchy. The same network can be described purely as a function composition. To claim that layer 2 represents “adequacy of adequacy,” the project needs one or more of:

- supervised intermediate targets;
- architectural modularity;
- monotonicity or sign constraints;
- causal interventions;
- verified correspondence to known latent factors;
- stable decoding across seeds and distributions.

Recursion is representationally available; semantic recursion must be demonstrated.

---

## 14. Provenance and evidence do not fit inside a scalar margin

A margin says how far a comparison lies from a threshold. It does not say why the risk estimate should be trusted.

Two identical margins may be supported by:

- one observation or a million observations;
- direct measurement or simulation;
- in-domain tests or extrapolation;
- a verified solver or a noisy learned predictor;
- fresh evidence or a stale benchmark.

Therefore provenance should remain a side channel or structured object:

```text
LicenseOutput {
    signed_margins,
    gates,
    selected_content,
    domain,
    calibration_guarantee,
    evidence_trace,
    model_library_and_search_scope,
    expiry_or_revision_stage
}
```

Compressing provenance into the activation may improve predictive performance but undermines auditability. The final paper should treat provenance erasure as an explicit limitation of ordinary inference-time activations.

---

## 15. Information audit by layer

| Layer | Candidate representation | Information preserved | Information commonly lost | Transparency requirement |
|---|---|---|---|---|
| Structured request | Typed record | Full declared semantics and provenance | Undeclared background assumptions | Make hidden defaults explicit |
| Case encoder | `phi_X(x)` | Task-relevant features | Raw details, history, rare factors | Test sufficiency and OOD behavior |
| Domain encoder | `phi_D(D)` | Selected distribution/set summaries | Tails, geometry, interventions | Match encoder to risk functional |
| Model encoder | `m(M)` | Identity, behavior, loss profile, or structure | Mechanism or off-probe behavior | State equivalence class represented |
| Risk predictor | `J_hat(M,D)` | Expected target loss | Loss decomposition and uncertainty | Calibrate and retain component risks |
| Margin vector | `(s_hard,s_base,s_lib,...)` | Reasons for passing/failing | Raw observations and mechanisms | Preserve components and units |
| Combined margin | `min_i s_i` | Conjunctive pass/fail and weakest slack | Identity of other failures | Keep component vector for diagnosis |
| ReLU gate | `max(0,s)` | Positive grant and slack | Equality and all negative magnitudes | Retain signed score or negative channel |
| Router | model index/weights | Selected alternative or mixture | Rejected alternatives and near ties | Log candidate scores and abstention |
| Expert output | prediction/action | Task result | Why the expert was licensed | Attach model/domain/trace |
| Final action | discrete choice | Executed behavior | Almost all counterfactual structure | Preserve action rankings and margins |

This table is the core answer to “where is the information?” It is distributed across the pipeline; later layers usually contain less diagnostic information than earlier ones.

---

## 16. Candidate architectural families, without selecting one

### 16.1 Monolithic score MLP

```text
z = Encode(M,D,task,...)
s = MLP(z)
gate = ReLU(s)
```

**Strength:** simplest fit to a basic MLP.  
**Risk:** model/domain semantics, risk estimation, and comparison are entangled.

### 16.2 Factorized risk predictor

```text
m = e_M(M)
d = e_D(D)
J_hat = g(m,d,task)
s = Compare(J_hat, epsilon, baseline, library)
```

**Strength:** separates empirical prediction from normative/pragmatic comparison.  
**Risk:** latent factors remain non-identifiable and aggregation may be complex.

### 16.3 Explicit gate plus expert library

```text
gate_i = LicenseScore(M_i,D)
content_i = Expert_i(x)
output = route(gate_i,content_i)
```

**Strength:** clean model identity, abstention, and traces.  
**Risk:** less like one ordinary homogeneous MLP; routing discontinuities or expert mismatch.

### 16.4 Multi-margin transparent head

```text
s = (s_hard,s_base,s_cost,s_robust,s_library)
gate = all(s_i >= 0)
diagnostic = (ReLU(s), ReLU(-s))
```

**Strength:** preserves reasons and defeat modes.  
**Risk:** requires labeled/interpretable intermediate targets.

### 16.5 Shared policy/value representation

```text
h = shared_encoder(state)
policy = policy_head(h)
value/license = value_or_license_head(h)
```

**Strength:** relevant to policy-to-value interpretability; enables alignment tests.  
**Risk:** shared representation can encourage but does not prove causal identity.

Task 16 now chooses a hybrid ReLU statistic scorer plus exact symbolic decoder in [`ml/02_relu_architecture.md`](../ml/02_relu_architecture.md), using separate plan content/grade/evidence channels and exact active masking.

---

## 17. The central encoding problem

The project can now state its main representation problem without choosing an architecture.

### Given

- a model library `K={M_i}`;
- cases or domains `{D_j}`;
- evidence records and outcomes `E_t`;
- one or more losses `{L_k}`;
- fallbacks `{B_j}`;
- hard tolerances and required improvements;
- observed or simulated model losses;
- optional structural information about models/domains.

### Learn or construct

- model encoders `e_M`;
- case/domain encoders `e_X,e_D`;
- a calibrated risk predictor `g`;
- signed comparison margins;
- a gate/router with explicit abstention;
- a trace connecting selected content to the margins and evidence.

### Such that

1. predicted risk generalizes to held-out cases/domains;
2. tolerance monotonicity holds by construction;
3. baseline improvement is correctly represented;
4. licensing remains conservative under prediction uncertainty;
5. multiple adequate or Pareto-undominated models can coexist;
6. no model is selected when none is licensed;
7. the representation exposes component margins and near alternatives;
8. semantic interpretations are stable enough to test across seeds and shifts;
9. representation error is charged against license slack;
10. provenance and scope remain recoverable.

This is more precise than “encode models and domains as vectors.” It says what the vectors must be sufficient for and what information must remain outside them.

---

## 18. Evaluation criteria for representations

A candidate representation should be evaluated along separate axes.

### Predictive sufficiency

- held-out pointwise loss prediction;
- held-out domain-risk prediction;
- calibration of risk bounds.

### License fidelity

- false-license and false-rejection rates;
- monotonicity in hard tolerances;
- correct improvement over baselines;
- correct abstention in uncovered domains.

### Comparative fidelity

- preservation of pairwise model rankings;
- Pareto-front recovery;
- stability under library expansion.

### Information preservation

- reconstructability of signed margins;
- retention of component failure reasons;
- sensitivity to tails and rare cases;
- provenance accessibility.

### Interpretability

- feature/domain stability across seeds;
- sparse or compositional descriptions;
- correspondence to known physical/task axes;
- causal response to interventions;
- human ability to predict the system from its trace.

### Efficiency

- embedding dimension;
- sample complexity;
- inference and routing cost;
- complexity of certificates.

No single metric should stand in for all six categories.

---

## 19. Consequences for the eventual paper

The paper should introduce the neural mapping in this order:

1. Define the structured license and its separate comparisons.
2. Explain that cases, domains, and models require different encoders.
3. Ground the embeddings in observed/simulated loss profiles.
4. Predict risk before thresholding it.
5. Construct signed margins with explicit units and meanings.
6. Use ReLU to propagate positive slack, not to represent the whole judgment.
7. Retain negative/component margins and provenance for transparency.
8. Distinguish a pointwise gate from a domain-level certificate.
9. Treat semantic alignment of hidden regions as an empirical target.

This order prevents a tempting but circular story:

```text
neuron activates -> therefore it encoded adequacy -> therefore its region is a scientific domain.
```

The justified direction is:

```text
operational records and losses
    -> calibrated risk representation
    -> signed adequacy comparisons
    -> constrained gate/router
    -> tests of whether internal regions align with the intended semantics.
```

---

## 20. Open questions handed to later tasks

Task 4 must determine whether scientific model charts should be represented by explicit experts, activation regions of one network, or both.

Task 5 must decide which information is part of the logic's syntax and which is implementation metadata.

Task 7 must define typed model, case, domain, loss, evidence, and provenance objects.

Task 8 must define how statistical calibration turns predicted risk into a license.

Task 10 must define scalar versus Pareto admissibility.

Task 15 compares model-ID, functional, loss-profile, and structural encodings at the interface level in [`ml/01_encodings.md`](../ml/01_encodings.md). Empirical comparison remains for the later experiment; hidden-state interpretation additionally requires the alignment tests fixed there.

Task 16 now selects the hybrid architecture, signed and paired-score access, inclusive-support/strict-refutation boundary convention, and active-mask fallback mechanism in [`ml/02_relu_architecture.md`](../ml/02_relu_architecture.md).

Task 18's [`../ml/04_losses.md`](../ml/04_losses.md) selects standardized center–radius statistic/interval training, disjoint held-out residual calibration, independent atom cross-entropy as the baseline, separate exact-mask router ranking, and optional representation-alignment probes outside authorization.

Task 23 must test whether a recovered value/license representation aligns with the internal representations of the companion policy network rather than merely matching its actions.

## Task conclusion

The information in `Pi(M,D,epsilon)` is not located in one activation. It begins in a structured, evidence-relative request; is compressed into model/domain/task encodings; becomes operational in predicted loss; becomes decision-relevant in signed margins; is partially erased by ReLU; and is further compressed by routing and action selection.

The most defensible representation program is therefore loss-first and trace-preserving:

- derive vectors from their role in predicting operational loss or negative utility;
- preserve separate hard, baseline, and library margins;
- retain signed scores even when only positive slack routes content;
- state the equivalence class identified by the embeddings;
- keep provenance and domain scope accessible;
- test, rather than assume, that internal neural regions correspond to meaningful licenses.
