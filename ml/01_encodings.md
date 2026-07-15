# Operational Encodings for Atoms, Libraries, and Annotated Plans

Created: 2026-07-14
Task: TODO Task 15
Status: architecture-neutral contract instantiated by Tasks 16–18 and audited at Checkpoint C

## Executive decision

The neural interface should not encode the whole logic in one vector and should not predict a public license directly. Its smallest stable unit is one **addressed atom computation**:

```text
exact atom address + canonical dependency projection
    -> optional learned continuous statistic and error envelope
    -> external, boundary-aware diagnostic decoder.
```

For a request base `b=(s,e,q)` and an already instantiated atom address `a`, define

```text
x(s,e,q,a) = (a, Env(s;e,q)|R_s(b,a)),
```

where `R_s(b,a)` is the address-local part of the Task 14B typed read footprint. The profile `P` normally selects addresses, assigns required/report/safety roles, and aggregates their decoded records. Once two profile slots instantiate to the same address, they receive the same `x` and the same atom value. `P` is therefore a consumer of atom records, not an unexplained input that changes their values.

The contract deliberately keeps three boundaries visible:

1. exact identifiers, units, modes, validity, checker versions, and provenance remain symbolic or externally referenced;
2. a learned module may propose continuous sufficient statistics and calibrated error envelopes, but a prediction is not a certificate; and
3. a plan exposes computational payload, quantitative grade, and certificate/provenance separately, even when a later theorem permits one named scalar to serve both as adequacy surplus and downstream content.

This document fixes inputs, outputs, equivalences, and invariances. Task 16 instantiates them in [`02_relu_architecture.md`](02_relu_architecture.md), and Task 17 proves or delimits the promised results in [`03_representation_theorems.md`](03_representation_theorems.md). Nothing here is a neural-width bound or a proof that the proposed statistics are learnable.

## 1. Scope and mathematical economy

This is a derived interface for the compact `E,Q,S` calculus, not a fourth principal carrier and not a new ontology of record types. The paper-level objects remain:

```text
e in E             evaluated use plan
q in Q             complete reliance/evaluation context
s in S             finite epistemic state
P                  finite profile syntax
a                  instantiated typed atom address.
```

The detailed fields below are projections of these objects or of Task 14C's finite annotated-plan elaboration. They should appear in an implementation schema or appendix, not as a new many-sorted logical foundation.

The contract is **query-family-specific**. Before encoding, declare:

```text
F       finite family of profile/status or diagnostic queries
A_F     finite set or address schema that those queries may instantiate
C       optional finite family of downstream computational consumers.
```

An encoding sufficient for `F` need not preserve answers for a different profile family, a new certificate mode, a different loss functional, or an undeclared downstream computation. “Future-profile information” below always means information for a declared extension family `F+` or address horizon `A+`; no finite code is claimed sufficient for every as-yet-unspecified query.

## 2. From Task 14B footprints to one atom input

### 2.1 Address formation and evaluation reads

For a request `r=(s,e,q,P)` and slot `i`, Task 14B's full footprint can be viewed as two derived pieces:

```text
Read_s(r,i)
  = InstRead_s(s,e,q,P,i) union R_s((s,e,q),a),

a = theta_P(i)(s,e,q).
```

`InstRead` contains the profile/slot information needed to form the exact address and its role. `R_s(b,a)` contains the plan, context, certificate, region, trace, comparison, validity, correction, verifier, and collection-index reads needed to evaluate that address after it has been formed. For comparison atoms, exact evaluated-set and search-view identity are part of the address-local dependency projection. For public assessment, the separate `WF` projection is also retained.

This factorization is an encoding convention, not a change to the locality theorem. The complete footprint remains authoritative. It makes one semantic constraint explicit:

```text
theta_P(i)=theta_Q(j)=a
    implies x(s,e,q,a) is identical for both consumers.
```

A profile may change the atom it asks about by changing its instantiated tolerance, fallback, scope, evaluated set, criterion, or mode. That produces a different address, not a profile-dependent value for the same address.

### 2.2 Canonical raw input

Let

```text
pi_a = Env(s;e,q)|R_s((s,e,q),a).
```

The architecture-neutral atom input is

```text
x(s,e,q,a) = (a,pi_a).
```

`pi_a` is a canonical typed map. Empty collection indices, missing member records, correction closure, current validity, conflict state, and checker/version facts are represented explicitly. Set and map order is canonical but semantically irrelevant.

For implementation, parse `pi_a` without loss into three views:

```text
pi_a <-> (c_a,o_a,h_a)
```

where:

- `c_a` is exact typed content eligible for numerical or categorical feature construction;
- `o_a` is exact observation state, including presence, missingness, currentness, conflict, eligibility, and external checker outcomes; and
- `h_a` is a set of opaque handles to certificates, checkers, assumptions, provenance nodes, registries, loss estimators, and source records.

The learned view may vectorize part of `(a,c_a,o_a)`, and it may use an auxiliary embedding of a handle. The exact handle must still travel beside that embedding whenever identity or version affects decoding or audit. The complete `pi_a` or a content-addressed reference to it is retained for the audit-preserving interface.

### 2.3 Learned statistic, not learned license

For each compatible statistic schema `sigma(a)`, a scorer has the abstract form

```text
T_theta^sigma : Vec_sigma(a,c_a,o_a)
                -> (t_hat_a,eta_hat_a,v_hat_a?).
```

Here:

- `t_hat_a` proposes continuous atom-sufficient statistics;
- `eta_hat_a` is a stated uncertainty, calibration, or approximation envelope with units; and
- `v_hat_a`, when present, is only a learned validity proposal or out-of-distribution score.

The exact validity/missingness facts in `o_a` override neither one another nor the checker. A learned validity proposal may cause conservative abstention or request external review; it cannot validate a missing, expired, conflicted, or checker-rejected certificate.

An external decoder then computes

```text
Dec_a(a,pi_a,t_hat_a,eta_hat_a) ->
    Support(a,...), Open(a,...), or Refute(a,...).
```

The decoder may use a learned statistic as evidence only under a named accepted certificate for that statistic or for its error envelope. Otherwise it remains a prediction to be evaluated. `WF`, profile aggregation, `K_3` meet, public outcome, safety projection, active-set masking, selection, and fallback are deterministic consumers outside the scorer.

Some atom schemas need no learned statistic. A formal trace accepted by a named checker, for example, may use a zero-dimensional `t_hat_a`; its exact diagnostic comes entirely from `pi_a` and the checker registry.

## 3. Field ownership

The following classification is normative. “Exact” means that the decoder or auditor receives the typed value, not that the value cannot also have a learned embedding.

| class | representative fields | owner and rule |
|---|---|---|
| explicit typed inputs | plan/version; domain, task, frame; loss and risk functional; tolerance and units; fallback and improvement requirement; atom kind/scope/criterion/mode; candidate features or functional fingerprints | supplied by `(e,q,a)` or the declared data interface; never reconstructed only from an anonymous latent code |
| mechanically fixed context | profile slot instantiation and role; exact evaluated set; registry membership; correction closure; currentness; conflict resolution; eligibility; `WF`; `K_3` meet; safety projection; active mask; fallback rule | computed by the symbolic layer from exact finite records |
| learned sufficient statistics | risk or certificate-region endpoints; support/refutation margins; pairwise performance statistics; payload approximation; quantitative error/resource grade; calibrated envelope | predicted by one compatible module and decoded only under its stated scope and evidence conditions |
| validity and missingness indicators | record present/absent; collection empty; accepted/rejected/unknown; current/expired/corrected; conflict; in/out of declared support; learned OOD proposal | exact indicators are separate channels; absence is not numeric zero and a proposal is not checker acceptance |
| external pointers | certificate/proof term; checker and version; assumptions; calibration record; provenance graph; source record; loss-estimator identity/version; registry entry | opaque exact identity plus optional embedding; checker/provenance contents stay outside the neural semantic claim |
| forbidden sole compression targets | exact address; loss/risk units; tolerance; mode; checker/version; evaluated-set identity; fallback; role/safety flag; missingness; certificate term; full provenance; plan dependency structure when a consumer asks about grade/cost/explanation | may be embedded for scoring, but the latent value cannot be the only surviving representation |

Two additional prohibitions are important:

- Target-world truth is not an input available merely because a model is trained; it enters only through a named mode-scoped bridge.
- The finite discrete-code lower bound in Task 14 is a cardinality statement about distinguishable decoded states. It is not a lower or upper bound on real-valued neural width, precision, parameters, or sample complexity.

## 4. Atom-family statistic schemas

The scorer contract is a family of compatible schemas, not one mandatory omnibus output.

| atom family | exact dependency content | possible learned statistic | exact decoder/checker responsibility |
|---|---|---|---|
| `Adeq` or region-valued `Constraint` | address, acceptable region, current normalized evidence, mode, units, verifier/version | certificate-region parameters or dual support/refutation margins with an envelope | check certificate/envelope validity; apply subset/disjoint/boundary rules; preserve witnesses or obstacles |
| `Improve` | candidate and fallback regions, `Delta`, common criterion/units, both evidence states | paired regions or the two comparison margins | verify both scopes; decode support/refutation/open; retain fallback identity |
| `Trace` | trace index and records, completeness requirement, mode, checker/version, corrections | normally none; optionally a proposal for where a trace may be incomplete | the named checker alone accepts a trace or countertrace; missing/invalid/conflicted remains open |
| `RelUndom` | candidate, exact `K`, criterion, eligibility, valid search view, pair/certificate indices | on-demand candidate-pair statistics or dominator proposals | a valid dominator refutes; only a valid declared exact-set search supports; no global closure |
| `CertUndom` | the relative footprint plus resolution of every relevant eligible pair | pair statistics and envelopes for unresolved pairs | require a valid search and checked resolution/ineligibility for every relevant pair |
| `WF` | profile, slots, library membership, plan/interface/context, exact comparison view, fallback, modes and referenced versions | none in the core | compute deterministically before atom decoding; return `WFDiag` on failure |

For the scalar upper-risk special case with certificate interval `U=[l,u]` and acceptable region `(-infinity,epsilon]`, a useful statistic pair is

```text
m_support = epsilon-u,
m_refute  = l-epsilon.
```

The exact decoder gives support when `m_support>=0`, refutation when `m_refute>0`, and open otherwise. Thus boundary support at a singleton `U={epsilon}` is not confused with strict refutation. For scalar improvement,

```text
m_support = inf(U_F) - (sup(U_e)+Delta),
m_refute  = (inf(U_e)+Delta) - sup(U_F),
```

with the same inclusive-support/strict-refutation convention. Task 16 adopts these as the scalar reference statistics; this is not a demand that every ordered risk space be scalarized.

## 5. Profile consumption and two representation strengths

### 5.1 Status-minimal code

Fix a declared profile-query family `F`. Let `WFObs_F(omega)` collect exactly the well-formedness observations needed by its requests, let `V(omega)` be the realizable meaningful atom-state vector on its declared address base, and define

```text
v ~_F v'  iff every P in F returns the same requested status on v and v'.
```

The status-minimal semantic code is

```text
c_min^F(omega) = (WFObs_F(omega), [V(omega)]_~F),
```

with the meaningful-vector component used only on the relevant well-formed branches. `Ill/Well` is a convenient external normal form for rendering those branches, not a required internal tag. `c_min^F` intentionally discards atom identity, witness choice, negative magnitude, diagnostics, provenance, and distinctions no query in `F` can observe.

This code is appropriate only for a frozen status consumer. It must not be called globally lossless or audit-preserving.

### 5.2 Audit-preserving code

Fix a declared audit/future address horizon `A+` containing the present addresses and those instantiable by a named future profile family `F+`. An audit code retains

```text
c_audit^(F+)(omega) =
  (WFDiag/observations,
   {a -> (diagnostic_a, statistic_a, envelope_a,
          safety projections, h_a) : a in A+},
   exact profile-role maps,
   exact plan/candidate registries and dependency references).
```

The statistic and envelope may be omitted for an exactly checked symbolic atom; the atom address and diagnostic may not. Safety consumers receive the complete selected diagnostic records, not only alarm bits. Retaining unqueried records in `A+` permits later profiles in `F+` to reuse them without retraining, but no claim is made for an address whose task, mode, loss, candidate, or evidence schema was never represented.

The two codes answer different questions:

| consumer | sufficient interface |
|---|---|
| one frozen public-status family | `WFObs_F + V/~_F` |
| atom explanation or safety audit | address-indexed complete diagnostics and safety roles |
| update impact or evidential review | diagnostics plus exact read/provenance references and validity history |
| named future profiles | unquotiented atom records over their declared address horizon |
| arbitrary future query | no finite sufficiency claim |

## 6. Fixed and expandable model libraries

### 6.1 Fixed finite model-indexed baseline

For a frozen registry `K={e_1,...,e_n}`, a simple baseline has model-indexed outputs:

```text
T_theta(q,s) = (t_1,...,t_n),
```

with a fixed coordinate schema per registered plan. Exact registry identities remain external. This baseline makes simultaneous and empty active sets easy to decode, but it has three limits:

1. a new independent plan has no output coordinate without expanding or replacing the interface;
2. a coordinate permutation requires the registry map and outputs to be permuted together; and
3. a dense ordered comparison table uses `n(n-1)` cells, or `n(n-1)/2` only when a proved symmetric representation is sufficient.

The fixed baseline is a finite-stage witness, not a model of literal indefinite storage.

### 6.2 Candidate-conditioned shared scorer

An expandable library instead uses shared functions such as

```text
f_theta(phi_E(e_i),phi_Q(q),x_i) -> t_i,
g_theta(phi_E(e_i),phi_E(e_j),phi_Q(q),x_ij) -> t_ij.
```

`f_theta` is applied equivariantly to each candidate. `g_theta` is evaluated only on requested pairs. A permutation-invariant reducer may summarize a set, while any selected candidate identity is returned through the external registry and therefore permutes equivariantly. Cold-start quality depends on the candidate representation and evidence; shared parameters do not guarantee correct scoring of an arbitrary new theory.

This design separates **parameter sharing** from **explicit memory**. The registry, candidate features, evidence, and evaluated-set identity may grow while scorer parameters remain fixed, but a fixed-dimensional summary can still lose independent distinctions. External memory or a sequence of systems remains necessary when the declared access problem grows beyond the representation's capacity.

### 6.3 Sparse versus quadratic comparison

Let `E_K` be the directed candidate pairs actually queried or certified.

```text
dense storage/evaluation:  Theta(n^2)
sparse/on-demand form:     Theta(n+|E_K|).
```

Sparse evaluation is exact for the pair questions it actually contains. It does not silently prove all missing pairs irrelevant.

- A `RelUndom(g,q,K,...)` decoder may stop after finding one valid dominator. To support non-domination it additionally needs the declared valid search trace over exact `K`; sparse pair records alone do not certify search completeness.
- A `CertUndom(g,q,K,...)` support requires every relevant eligible pair to be resolved or ineligible. This is `Theta(n)` evidence for one candidate and can become `Theta(n^2)` for all candidates unless a separate, proved certificate compresses the comparisons.
- Adding a candidate changes `K`, its address, and its search footprint. Neither shared scoring nor sparse storage converts a finite-library result into global optimality.

## 7. Annotated plan encoding

### 7.1 Node contract

For a finite Task 14C plan DAG `G=(N,E_G,o)`, every node `v` exposes four groups:

```text
payload:
  input/output type, frame, metric, transformer identity, y_v or y_hat_v

quantitative grade:
  bound values, units, validity tube/scope, typed resource map,
  grade transformer identity, g_v or g_hat_v and envelope

certificate/checking:
  certificate or evidence handle, checker and version, assumptions,
  accepted/rejected/open state

provenance/stratification:
  predecessor ports, source handles, local rule record, dependency rank.
```

The loss estimator is a named node or exact external handle. Its output estimates or bounds the target criterion `L_q`; it is not identified with `L_q`. Checker identity and version remain exact whether the plan is represented by a flat model embedding or by its graph.

The architecture-neutral learned plan output, when requested, is

```text
PlanStat_theta(G,x) = (y_hat_o,g_hat_o,eta_o),
```

or the corresponding node-equivariant family. The certificate term, accepted checker result, and provenance graph are not predicted by this tuple. Task 14C's composite license consumes a checked root certificate, not merely an acceptable predicted grade.

### 7.2 Flattened identity baseline

A flat baseline uses

```text
(exact plan ID/version, plan feature vector, q, evidence summary)
    -> (payload statistic, grade statistic).
```

It is adequate if the declared consumer distinguishes plans only through those retained features. It is deliberately tested on pairs with the same observed output but different:

- sharing versus duplicate computation and hence cost;
- solver/formulation or reference-frame path and hence robustness bound;
- grade propagation rule or resource aggregation;
- certificate assumptions/checker version; or
- explanatory dependency trace.

If the flattened vector omits one of these while the consumer asks for it, equal codes form an immediate insufficiency witness.

### 7.3 Explicit DAG hypothesis

An explicit encoding retains the finite typed labeled graph: node operators and interfaces, ordered input ports where order matters, edges/sharing, root, grade schemas, certificate/checker handles, and ranks. A graph/set architecture is now a legitimate *experimental comparator* for this hypothesis:

> When structurally distinct plans are extensionally equal on observed payloads but differ in cost, robustness, grade propagation, or explanation, an explicit isomorphism-aware DAG representation should preserve and generalize those distinctions better than a matched flattened plan-ID baseline.

This is falsifiable and not yet supported. Checkpoint C defers the trained
graph/set comparison until a study has many independent typed plan families and
true structural separators; the deferral is not an empirical verdict. Nothing
here shows that graph structure helps a payload-only task.

## 8. Required invariances and non-invariances

### 8.1 Provenance identifier renaming

Let `alpha` be a bijection on opaque provenance/certificate node identifiers that preserves node type, content hash, checker/version, assumption labels, and graph incidence. Then diagnostics and public outcomes must be invariant up to the same renaming:

```text
Dec(alpha . x) = alpha . Dec(x),
Assess(alpha . x) = Assess(x).
```

Display names may change. Deleting a source, changing a checker version, changing an assumption, merging distinct nodes, or altering incidence is not a harmless renaming.

### 8.2 Candidate permutation

For a permutation `pi` of an exact candidate set:

- a candidate-conditioned scorer is equivariant: scores and returned identities permute by `pi`;
- set-level status summaries are invariant after exact identities are restored;
- pair outputs transform by `(i,j)->(pi(i),pi(j))`; and
- a tie breaker is invariant only if it is itself set-defined or its external stable ordering is declared as part of `q`.

A fixed indexed baseline satisfies this condition only when its registry map, input coordinates, output coordinates, and pair axes are permuted together.

### 8.3 Finite plan-DAG isomorphism

Two plan DAGs are encoding-isomorphic only when a root-preserving bijection preserves:

- node operator/version and typed payload interface;
- input-port labels or declared commutativity;
- edge incidence and sharing;
- frame, metric, grade schema, units, resource aggregation, and validity scope;
- checker/version/assumption labels up to opaque-ID renaming; and
- provenance rank and typed-base status.

Node-level encodings must be equivariant and root outputs invariant under such a bijection. Graph rewrites that duplicate a shared computation, change aggregation, alter a validity tube, or replace a checker are not isomorphisms merely because the final numerical payload happens to match.

## 9. Mandatory outputs and theorem-indexed extensions

No single network is required to predict every formal extension.

| layer | mandatory when in scope | not part of the mandatory learned head |
|---|---|---|
| atom scorer | named continuous statistic; units/schema; uncertainty or approximation envelope; learned validity proposal if used | atom address, exact missingness/currentness, checker acceptance, certificate, provenance, `K_3`, public status |
| symbolic atom/profile layer | exact address and roles; `WF`; boundary-aware diagnostic; `K_3` meet; safety projection; active mask and fallback | no learned aggregate-status override |
| annotated-plan scorer | payload and quantitative grade as separate outputs, plus envelope, for the declared plan consumer | proof term, certificate acceptance, assumptions, provenance, root grant |
| external audit layer | registry identities; certificate/checker/version; loss-estimator identity; read/provenance references | no requirement to embed all raw artifacts in one finite vector |

The following are separate, theorem-indexed modules and appear only when queried:

- router cell and misrouting/fallback statistics from Task 14A;
- bridge disagreement, Lipschitz/scope certificates, and cycle-defect data;
- pairwise dominance statistics for the requested comparison edges;
- path sensitivities, local error bounds, and typed resource aggregators for an explicitly composed plan; and
- system-audit statistics for a separately ranked meta-request.

An absent extension head means “not modeled by this module,” not a negative atom or zero-valued quantity.

## 10. Identifiability and interpretation tests

### 10.1 What is identifiable

For a declared consumer family `H`, codes are observationally equivalent when

```text
z equiv_H z'  iff h(z)=h(z') for every h in H.
```

Training can at most identify an equivalence class under transformations that preserve its scorer and consumers. Candidate embeddings may permute; hidden coordinates may change basis; bilinear model/domain factors admit paired invertible transformations; redundant units may split or merge; and graph node order may change. None of those symmetries establishes one coordinate as “the real domain,” “person,” or “Newtonian adequacy.”

Semantic interpretation therefore attaches first to the declared output statistic and exact address, not to an arbitrary latent axis. A hidden coordinate receives a stronger interpretation only after independent alignment and intervention evidence.

### 10.2 Required tests

| test | success condition | failure exposed |
|---|---|---|
| footprint sufficiency | changing a record outside `R_s(b,a)` leaves the complete atom output unchanged; a declared relevant change is detectable | hidden dependence or omitted input |
| missingness separation | missing, zero, boundary, expired, conflict, and checker rejection remain distinguishable | zero-imputation and ReLU collapse |
| profile reuse | two slots instantiating the same address share one diagnostic; changing only role changes aggregation/exposure, not atom value | `P` as hidden causal input |
| rename/permutation/isomorphism | outputs obey the three invariance laws above | ID memorization or order leakage |
| boundary/calibration | held-out envelope coverage is measured; inside the propagated uncertainty band the decoder opens rather than guesses | predicted margin treated as certainty |
| consumer separator | search for equal codes with unequal required status, payload, cost, trace, or grade | insufficient quotient or dual-use scalar |
| counterfactual address test | changing loss, tolerance, fallback, mode, checker, frame, or exact `K` changes the address/eligible decoder in the specified way | latent conflation of typed requests |
| provenance reconstruction | every supported required atom resolves to checked typed bases in the declared DAG/rank fragment | post-hoc or circular explanation |
| latent stability probe | align coordinates across seeds, bases, and equivalent parameterizations before naming a feature | latent coordinate treated as ontology |

Passing functional tests supports the interface on the tested distribution. It does not by itself establish mechanistic faithfulness, human interpretability, or target-world soundness.

[`verification/encodings.py`](../verification/encodings.py) and [`verification/test_encodings.py`](../verification/test_encodings.py) make selected finite contracts executable: dependency projections ignore outside records while exposing missing reads, shared candidate scoring is permutation-equivariant, sparse comparison counts remain distinct from dense resolution, typed plan isomorphism preserves checker-sensitive structure, and an equal-margin/different-payload pair defeats scalar joint sufficiency. These are regression witnesses, not neural results or proof-assistant proofs.

## 11. Joint license/computation consumers and dual-use activations

Let `Omega` be the declared exact input class. Define independently of the learned code:

```text
F = {f:Omega -> license status or diagnostic answer}
C = {c:Omega -> required downstream payload, decision, grade, cost, or trace answer}.
```

Examples of `C` include a named classifier output, a plan continuation's numeric input, a selected payload, or an error/resource quantity used by a later constructor. “Whatever the network happens to compute from its activation” is not an independently declared consumer.

Define

```text
omega ~_(F,C) omega'
  iff [for every f in F, f(omega)=f(omega')]
      and [for every c in C, c(omega)=c(omega')].
```

A code `z` is jointly sufficient exactly when

```text
ker(z) subseteq ~_(F,C),
```

equivalently when every member of `F union C` factors through `z`. The minimal abstract joint code is the quotient `Omega/~_(F,C)`. Task 17 goes beyond this definition-level condition by proving minimality for the explicit coordinate-complete state-plus-normalized-surplus family and giving scalar, boundary, and scale obstructions.

For named margins `m_i` and `z_i=ReLU(m_i)`, a dual-use interpretation additionally requires:

1. channel `i` names an exact hypothesis/address and unit-bearing statistic;
2. `m_i` is certificate-valid or has a verified error envelope with sufficient boundary separation;
3. inclusive boundary support, negative/open status, validity, and missingness remain recoverable outside the rectified scalar;
4. magnitudes are commensurate or normalized for the declared downstream operation;
5. `z` is jointly sufficient for the independently declared `F` and `C`; and
6. the certificate/checker remains external to `z`.

The author's classifier example is therefore coherent as a conditional construction. Channels named `flower`, `dog`, `cat`, `person`, and so on may carry positive normalized certificate-relative surplus and feed a later layer. A vector such as `(0,0.2,0.2,0,5,3,0.1,...)` says that `person` has the largest displayed surplus only under the common scale and channel contract. It does not by itself say that `person` is the highest posterior probability, the global best theory, or a proved world fact.

An immediate obstruction remains: two plans may have equal adequacy margin and different predictions, costs, or traces. Then the scalar adequacy code identifies two points not equivalent under `C` and is not jointly sufficient. Likewise, a positive rescaling of loss, tolerance, and certificate bounds can preserve license status while changing margin magnitude. A downstream consumer must be covariant under that rescaling or consume a declared normalization. Multiplying a payload by an adequacy margin defines a new plan and requires its own evaluation.

## 12. Task 17 result audit

The contract stated each result frozen at Checkpoint B without assuming it; Task 17 now closes the corresponding burden:

| Task 17 target | interface supplied here | Task 17 result |
|---|---|---|
| 1. architecture-neutral exact factorization | `WFObs_F`, `V/~_F`, diagnostic-preserving `c_audit`, and deterministic consumers | exact kernel characterization and minimal public/audit quotients |
| 2. margin-robust approximation | typed statistics, envelopes, exact boundary rules, and conservative open state | sound interval decoder; exact ideal recovery outside the explicit `2r` band |
| 3. exact finite ReLU for CPWL statistics | fixed finite numerical view and external decoder; no direct `K_3` output | exact global finite CPWL construction with audited depth/size/domain conventions |
| 4. polyhedral hard seams | router/bridge quantities are a separate optional module with exact cell/scope metadata | trace-agreement iff, rank-one facet corollary, and discontinuity obstruction |
| 5. finite versus expandable library | fixed indexed and candidate-conditioned designs plus exact sparse/dense obligations | interface limitation, shared-score equivariance, and extension non-closure counterexample |
| 6. dual-use joint sufficiency | independently declared `F,C`, joint quotient, scalar separator, boundary and scale obligations | minimal named coordinate-complete construction plus scalar/boundary/scale obstructions |
| 7. annotated finite-plan realization | explicit payload/grade channels, finite DAG, seam/interface fields, external certificate/checker | CPWL closure and exact proof-erased payload/grade realization; certificates remain external |

In particular, this document does **not** assume that a learned target is CPWL, that every seam matches, that a fixed scorer handles an unbounded registry, that a margin scalar preserves payload, or that a predicted grade proves its own validity. Task 17's results apply only when their explicit hypotheses settle those points.

## 13. Decisions carried forward

1. `x(s,e,q,a)` is the exact address plus its dependency-scoped canonical projection; the learned vector is only a view of it.
2. `P` forms addresses and consumes diagnostics. It does not change the value of an already fixed address.
3. Exact typed metadata, validity/missingness, checker/certificate/provenance handles, `WF`, `K_3`, masking, selection, and fallback stay symbolic or external by default.
4. Learned outputs are continuous sufficient-statistic proposals with envelopes, not direct proofs or public grants.
5. Status-minimal and audit-preserving codes are different products for different consumer families.
6. Future-profile reuse is bounded by a declared address horizon; arbitrary future sufficiency is not claimed.
7. Fixed indexed and candidate-conditioned expandable libraries are both retained. Sparse pair evaluation saves work only for questions whose evidence is actually sparse.
8. Annotated plan encoding keeps payload, grade, certificate/checker/assumptions, and provenance/rank separate and retains loss-estimator identity.
9. Candidate order, opaque provenance names, and plan node names are semantic symmetries only under the exact invariance conditions above.
10. An explicit DAG model is an operationalized comparator hypothesis, not a selected architecture.
11. Latent coordinates are identifiable only modulo consumer-preserving equivalence and receive no automatic ontological interpretation.
12. Dual-use adequacy activations remain possible under declared joint sufficiency, certification/envelope, boundary, and scale conditions; the scalar is never its own proof.

## Task conclusion

Task 15 supplies a compact neural/symbolic boundary for the surviving logic. It can encode ordinary model/domain cases, variable libraries, and recursively structured plans without making the profile a hidden cause, flattening evidence into reason labels, or treating neural output as proof. It also gives the graph/set comparator a concrete structural hypothesis while leaving architecture choice open.

Task 16 derives the ReLU reference architecture in [`02_relu_architecture.md`](02_relu_architecture.md), preserving the exact metadata and decoder boundary fixed here, exposing separate plan payload/grade/validity/evidence channels, and treating dual-use activations only as a hypothesis-indexed construction. Task 17's [`03_representation_theorems.md`](03_representation_theorems.md) proves the scoped positive construction and exact limitations, and Task 18's [`04_losses.md`](04_losses.md) fixes the structured statistic objective, held-out calibration proposal, symbolic decoder, atom-classification baseline, and separate router loss. Checkpoint C retains this architecture-neutral interface and makes its leakage, certificate-binding, and split requirements explicit for the experiment.
