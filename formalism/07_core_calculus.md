# The Core Calculus of Finite-Stage Model-Use Licenses

Status: Task 13 canonical core selection

Date: 2026-07-12

Depends on: [`05a_integration.md`](05a_integration.md), [`06_open_endedness.md`](06_open_endedness.md), the executable [`WF + K_3` reference](../verification/README.md), and the [`core literature supplement`](../notes/literature_core_supplement.md)

## Durable core summary

This file replaces the historical implementation-level signature as the canonical paper-level calculus. It has three principal carriers:

```text
E   evaluated use plans
Q   reliance/evaluation contexts
S   finite epistemic states with refinement ->
```

Target worlds `W` are semantic indices, not another operational input. A profile `P` is a finite syntactic family of parameterized requirement templates, not a fourth semantic carrier. A request is exactly

```text
r = (s,e,q,P) in S x E x Q x Profile.
```

All task/domain/loss/risk/tolerance/fallback/frame data are dependent fields of `q`. All finite record/library/search/certificate/dependency/provenance data are dependent fields of `s`. Theory frameworks, exhaustive event and reason taxonomies, full provenance DAGs, bridges, Pareto frontiers, domain splitting, mixtures, and policy/value reconstruction are elaborations or extensions.

Assessment is canonical and two-phase:

```text
not WF(r)                   -> Undefined
WF(r) and meet = refuted   -> Refused
WF(r) and meet = open      -> Withheld
WF(r) and meet = supported -> Granted.
```

Meaningful atom values form `K_3={refuted,open,supported}` ordered

```text
refuted < open < supported.
```

Required atoms aggregate by finite meet. Diagnostics are atom-indexed support witnesses, counterwitnesses, or obstacles with provenance; no closed reason-code type exists. Safety projections retain the complete diagnostics of refuted or open safety atoms. `NoLicensedModel` is not an atom: it is a selector-level display derived from an empty active set.

The core includes a typed atom-refinement relation and a profile preorder. Under exact scope and parameter side conditions, stricter tolerances, larger required fallback advantages, stronger constraints/trace modes, and certified-undominated comparison can entail weaker atoms. A stronger profile grants only where the weaker profile grants. Task 14 must prove soundness and relative completeness for the frozen rules.

Four finite separating models prove that no coordinate of `(s,e,q,P)` can be dropped while preserving assessment on all core models. This is the main completed result of Task 13. The larger metatheory—robust update persistence, profile relative completeness, diagnostic minimality, and mode-scoped soundness—remains explicitly assigned to Task 14.

## 1. Design criterion: mathematical core versus record schema

The historical Task 7 signature was deliberately explicit enough to prevent type errors. It remains useful for implementations and examples, but it is too large to serve as the mathematical ontology of the paper. The core keeps only objects that participate independently in the central assessment function.

The compression principle is:

> If an object changes what is being evaluated, package it in `e`; if it changes where, for what task, under what loss, tolerance, or fallback the evaluation occurs, package it in `q`; if it changes what the bounded agent currently records, package it in `s`.

Profiles remain syntax because they select and parameterize finite queries over those three objects. Worlds remain semantic indices because target risk and truth need not be available to the bounded state.

## 2. The three carriers and their dependent data

### 2.1 Evaluated use plans `E`

An element `e in E` is a versioned executable object sufficiently fixed to evaluate or use. It can be a predictor, equation set, simulator, solver, controller, policy, or composed deployment plan. Its dependent interface supplies:

```text
In_e(q)        whether e has a denotation under q
Exec_e(q,x)    whether e is executable on case x under q
Out_e(q)       its typed output interface
Frame_e(q)     its declared representation/frame interface.
```

Model identity, version, preprocessing, solver choice, and deployment wrapper belong to `e` whenever changing them can change risk or executable behavior. An underspecified theory family is not normally an element of `E`.

The core treats `e` as atomic only relative to this interface. Its elaboration may be a finite dependency DAG of object/idealization choices, frames, formulations, submodels, solvers, loss/consequence estimators, and action rules. Two plans can return the same extensional answer yet remain different elements of `E` because their computation cost, robustness, trace, or behavior on other cases differs. Conversely, licenses for components do not by themselves license the composition: that requires a typed propagation certificate for errors, costs, interfaces, and interactions.

### 2.2 Reliance/evaluation contexts `Q`

An element `q in Q` packages all data that determine the substantive use question. At minimum it contains:

```text
X_q, D_q       typed cases and evaluation/deployment scope
Task_q         prediction/action/output task
Frame_q        required representation and interface
L_q, rho_q     loss and risk aggregation
R_q, <=_q      risk/value space and its comparison preorder
Acc_q          acceptable region or hard tolerance
F_q            explicit fallback or abstention action when action is authorized
Delta_q        required advantage over F_q, if any
C_q            hard resource/safety/operational constraints
Modes_q        admissible certificate and trace modes.
```

`Acc_q` may be scalar, vector-valued, or partially ordered. It is required to be downward closed when “smaller is better” tolerance monotonicity is invoked. A scalar context may use

```text
Acc_q = {z : z <= epsilon_q}.
```

The fallback is dependent data of `q`, not an element that must belong to `E`: deferring, requesting information, or maintaining the status quo need not be another predictive model.

Changing the domain, loss, risk aggregator, task, tolerance, fallback, required margin, frame, or hard constraints changes `q` and therefore changes the request. It is not merely a new observation about the old request.

`L_q` specifies the target criterion; it is not automatically the procedure used to estimate that criterion. A fallible model that predicts downstream outcomes, regret, computation cost, or `L_q` is part of an evaluated plan `e` or an evidence/certificate procedure recorded in `s`. It may itself be assessed by a higher-order request with another context. This permits finite well-founded nesting. A genuine cycle in which a request's result helps determine the very loss or evidence used to assess that request requires an explicit fixed-point or iterative semantics and is outside the ordinary core.

### 2.3 Finite epistemic states `S`

An element `s in S` is finite and contains:

```text
K_s              finite represented library, K_s subset_fin E
Rec_s            finite observations/evaluations/corrections
Eval_s(q)        finite candidates validly evaluated for q
Cert_s           finite certificate and countercertificate support
Search_s         finite searches, budgets, and unresolved comparisons
Dep_s            dependency relation from requests/atoms to support nodes
Prov_s           abstract provenance labels and history embedding
Current_s        current validity/retraction status of recorded support.
```

These are fields, not paper-level sorts. `Prov_s` may be a full DAG in an implementation, but the core requires only stable node names, dependency queries, and history-preserving embeddings.

States refine through

```text
s -> s'.
```

An edge appends a declared evaluation, certificate, correction, model addition, search result, or other state event. It preserves old events and provenance but may invalidate their current support. Thus raw history is hereditary while current assessment is nonmonotonic.

### 2.4 World indices `W`

A target world `w in W` interprets quantities not identified with the finite record:

```text
Risk_w(e,q)
TargetConstraint_w(e,q)
True_w(phi), if truth is introduced in the metalanguage.
```

Operational assessment is computed from `s`. Two worlds can share the same finite state and therefore the same current assessment. World fields enter atom-specific soundness theorems, countermodels, and the Task 12 continuation semantics; they are not silently readable by the agent.

## 3. Profile syntax: shape separated from parameters

### 3.1 Atom templates and addresses

Let `Kind` be an open family of typed requirement kinds. The compact core needs the following examples, not an exhaustive enum:

```text
Adeq          risk lies in an acceptable region
Improve       candidate beats the named fallback by the required margin
Constraint    a named hard constraint is satisfied
Trace         certificate/provenance mode is adequate
RelUndom      no certified dominator exists in the evaluated set
CertUndom     every relevant evaluated comparison is resolved as non-dominating or ineligible.
```

An **atom template** consists of a kind and typed parameter slots. Instantiating it in `q` and, where required, `s` produces an atom address

```text
a = kind(parameters; exact scope, criterion, mode).
```

Addresses include enough information to prevent accidental comparison across different domains, losses, frames, candidate sets, criteria, or certificate modes.

### 3.2 Finite profile schema

A profile is a finite indexed family

```text
P = (I_P, kind_P, theta_P, role_P, Safe_P),
```

where:

- `I_P` is a finite set of slots;
- `kind_P(i)` is the typed atom template in slot `i`;
- `theta_P(i)` instantiates its parameters from the request base `(s,e,q)`;
- `role_P(i)` is `required` or `report`; and
- `Safe_P` is a subset of required slots whose open/refuted diagnostics must be exposed to action consumers.

The **shape**

```text
shape(P)=(I_P,kind_P,role_P,Safe_P)
```

forgets parameter values. This makes “reliance profile” a reusable finite form while `P@b`, for `b=(s,e,q)`, is its parameterized request instance.

For request base `b=(s,e,q)`, write

```text
Req_b(P)     instantiated required addresses
Report_b(P)  instantiated report-only addresses
Safety_b(P)  instantiated safety addresses.
```

Multiple constraints of the same kind are allowed because slots, not kind names, provide identity.

### 3.3 Canonical examples

With parameters supplied by `q`:

```text
P_rely      = required {Adeq, Improve, Constraint*, Trace}
              report   {RelUndom when available}

P_pref-rel  = P_rely plus required RelUndom(g,Eval_s(q))

P_pref-cert = P_rely plus required CertUndom(g,Eval_s(q)).
```

`Constraint*` denotes a finite family of named constraints, not one conjunction hidden inside a reason code. None of these profiles expresses global optimality.
The displayed `RelUndom` report is an optional schema variant: a concrete profile either contains that report slot or does not. “When available” never permits a present slot to disappear during instantiation.

## 4. Well-formed requests

A core request is

```text
r=(s,e,q,P).
```

`WF(r)` holds exactly when:

1. `s in S`, `e in E`, `q in Q`, and `P` is a finite typed profile with at least one required slot;
2. `e in K_s` and every referenced entity/version denotes;
3. `e` is executable on every case whose use is requested by `q`;
4. `Out_e(q)` and `Frame_e(q)` match the task/frame interface in `q`;
5. every profile slot instantiates on `(s,e,q)` to a typed atom address;
6. every comparison address names an exact scope, criterion, and finite evaluated set/search view;
7. every action-authorizing profile has an explicit fallback in `q`; and
8. all named certificate modes and constraint units are meaningful under `q`.

Missing evidence is not a `WF` failure. A typed request with insufficient evidence has an open atom and is therefore withheld. An absent executable interface, mismatched frame, unknown profile, or ill-typed comparison is undefined.

Let

```text
WFDiag(r)=(obligation,detail,provenance)
```

be the separate well-formedness diagnostic when `WF` fails.

For a request base `beta=(s,e,q)`, `WF(beta,P)` abbreviates `WF(s,e,q,P)`.

## 5. Meaningful atom semantics and diagnostics

### 5.1 The state algebra

For every `WF(r)`, with request base `b=(s,e,q)`, and every address

```text
a in Req_b(P) union Report_b(P),
```

the operational atom valuation is total:

```text
nu_s(e,q,a) in K_3={-,?,+},
```

where

```text
- = refuted
? = open
+ = supported
```

and `- < ? < +`. This is the Strong-Kleene three-element meet algebra after relabeling. It is an algebra of finite-stage evidential status, not a claim that truth itself has three values.

### 5.2 Operational atom clauses

The common operational clauses are deliberately small. When present, let `U_s(e,q,a)` be the current nonempty certificate region in the ordered value space relevant to `a`, after invalidated records have been removed from current support but retained in history.

**Region atoms.** Adequacy and region-valued constraints use:

```text
U subseteq Accept(a)          -> supported
U intersection Accept(a)=0   -> refuted
missing or boundary-crossing U -> open.
```

Here `0` denotes the empty set. A scalar upper-bound certificate is the special case used by Task 11B.

**Fallback improvement.** For scalar smaller-is-better candidate and fallback regions `U_e,U_F`:

```text
sup(U_e)+Delta <= inf(U_F)  -> supported
inf(U_e)+Delta > sup(U_F)   -> refuted
missing or overlapping comparison -> open.
```

Vector/partial-order contexts replace this clause with their declared acceptable improvement relation.

**Trace.** A trace atom is supported when the named verifier accepts a dependency-complete trace in the required mode. An explicit valid counterwitness to a hard trace obligation refutes it; missing, invalidated, or unresolved trace evidence leaves it open.

**Comparison.** On the exact finite set `Eval_s(q)`:

- `RelUndom` is refuted when a valid certified dominator exists, supported when the declared search trace is valid and none exists, and open when that trace is missing/invalid;
- `CertUndom` is refuted when a valid certified dominator exists, supported when the declared search trace is valid and every relevant pair is resolved as non-dominating or ineligible, and open otherwise.

Unknown pairs can therefore coexist with supported relative-undefeated status but not supported certified-undominated status.
The complete comparison record witnessing `CertUndom` carries the canonical projection to a valid `RelUndom` search trace on that same scope and evaluated set.

If current evidence contains unresolved incompatible certificates and the certificate mode supplies no valid priority or correction rule, the atom is open with an `EvidenceConflict` obstacle. The core does not select a convenient polarity from a live conflict.

### 5.3 Indexed diagnostic sum

The diagnostic at address `a` is exactly one of:

```text
Support(a, nonempty witnesses, provenance)
Open(a,    nonempty obstacles, provenance)
Refute(a,  nonempty counterwitnesses, provenance).
```

Its constructor determines `nu`. Provenance is mandatory. Certificate mode, confidence level, comparison scope, and relevant dependency nodes live in the witness/obstacle/provenance payload.

Flat strings are renderings:

```text
render(Refute(Adeq(...),kappa,...)) = HardRiskViolation(...)
```

but `HardRiskViolation` is not a primitive semantic constructor. The open-ended atom family therefore does not require an open-ended global reason enum.

Define the complete diagnostic vector

```text
Diag(r) = {a |-> diagnostic(a) : a in Req_b(P) union Report_b(P)}
```

whenever `WF(r)`. If `WF` fails, return `WFDiag(r)` rather than fabricated atom values.

### 5.4 Safety projections

Safety consumers receive submaps containing complete diagnostic records:

```text
Alarm(r) = Diag(r) restricted to {a in Safety_b(P) : nu(a)=-}
PendingSafety(r) = Diag(r) restricted to {a in Safety_b(P) : nu(a)=?}.
```

These projections are lossless for the selected safety diagnostics because witnesses, obstacles, and provenance are retained. They do not pretend to summarize nonsafety atoms.

## 6. Four public outcomes

For nonempty finite `Req_b(P)`, define

```text
mu(r) = meet {nu_s(e,q,a) : a in Req_b(P)}.
```

Then

```text
Assess(r) = Undefined   if not WF(r)
          = Refused     if WF(r) and mu(r)=-
          = Withheld    if WF(r) and mu(r)=?
          = Granted     if WF(r) and mu(r)=+.
```

The licensed judgment is

```text
<w,s> |= Lic_P(e,q) iff Assess(s,e,q,P)=Granted.
```

The right side is operational and depends on `s`; the world index is retained so later soundness claims can relate certificate modes to target facts. A grant does not by itself entail `True_w(phi)`.

The executable reference in [`verification/kernel.py`](../verification/kernel.py) implements this normal form.

## 7. Typed atom refinement

### 7.1 Semantic and derivable entailment

For well-typed atom addresses `a,b`, define semantic grant entailment

```text
a |=_A b
```

when, in every core model and every request where both addresses are meaningful,

```text
nu(a)=+ implies nu(b)=+.
```

Define a syntactic/refinement relation

```text
a =>_A b
```

by the following typed rules. It is deliberately partial: unmatched scopes, losses, criteria, frames, modes, or candidate sets yield no entailment.
Every derivable edge carries a witness projection from support for its antecedent to support for its consequent. Identity projections are available and projections compose along transitive closure.

### 7.2 Core refinement rules

**Acceptable-region rule.** For the same plan, scope, loss, risk aggregation, and certificate mode:

```text
Acc_1 subseteq Acc_2
--------------------------------
Adeq(Acc_1) =>_A Adeq(Acc_2).
```

For scalar smaller-is-better risk, `epsilon_1<=epsilon_2` gives the familiar stricter-to-weaker direction.

**Fallback-margin rule.** For the same candidate, fallback, scope, scalar objective, and certificate mode:

```text
Delta_1 >= Delta_2
--------------------------------
Improve(F,Delta_1) =>_A Improve(F,Delta_2).
```

Requiring a larger certified advantage is stronger.

**Constraint rule.** If two constraints share units, scope, and measured quantity and their admissible regions satisfy `C_1 subseteq C_2`, then

```text
Constraint(C_1) =>_A Constraint(C_2).
```

Independent constraints do not entail one another merely because both are called “safety.”

**Trace-mode rule.** If mode preorder `m_1 >=_trace m_2` is backed by a verifier/provenance projection under which every `m_1` witness is a valid `m_2` witness, then

```text
Trace(m_1) =>_A Trace(m_2).
```

The side condition is essential; a higher numerical confidence label alone does not establish mode refinement.

**Comparison rule.** For the same candidate, exact scope, criterion, and evaluated set:

```text
CertUndom(g,K) =>_A RelUndom(g,K).
```

This is Task 11A's certified-to-relative implication. No rule exports either atom to a larger candidate universe or future library.

Close `=>_A` under identity and transitivity. Task 14 must prove `=>_A` sound for the frozen atom semantics and determine relative completeness in an independent-atom fragment.

## 8. Profile preorder

At a fixed request base `beta=(s,e,q)` for which both profile instances are well formed, write

```text
P >=_prof^beta Q
```

when every `b in Req_beta(Q)` has some `a in Req_beta(P)` satisfying `a =>_A b`. The derivation supplies the witness projection needed to transport support diagnostics.

At schema level, define

```text
P >=_prof Q
iff for every beta, WF(beta,P) implies
    WF(beta,Q) and P >=_prof^beta Q.
```

Thus the schema relation is the uniform lifting of all request-local refinements, including transfer of well-formedness. A base on which `P` is not well formed creates no authorization claim.

Only required atoms determine authorization refinement. Report-only coverage can be compared separately by ordinary inclusion/refinement.

**Preorder fact.** Both the request-local relation (on profiles well formed at the fixed base) and its uniform schema lifting are reflexive and transitive. Reflexivity chooses the same slot and the identity atom derivation. For transitivity, compose each `P`-to-`Q` atom derivation with the selected `Q`-to-`R` derivation; witness projections and schema-level well-formedness implications compose. Thus `>=_prof` is a preorder, although distinct profile schemas can be equivalent in both directions.

The intended chain, under identical base parameters and comparison scope, is

```text
P_pref-cert >=_prof P_pref-rel >=_prof P_rely.
```

### Lemma 1: grant antitonicity under profile strengthening

Assuming `WF(beta,Q)` and soundness of every atom-refinement edge used in `P >=_prof^beta Q`:

```text
Assess(s,e,q,P)=Granted implies Assess(s,e,q,Q)=Granted.
```

**Proof.** Grant under `P` supports every required `a`. Each required `b` of `Q` has a supported entailing witness `a`, so sound atom refinement supports `b`. The explicit side condition supplies well-formedness. Every required `Q` atom is supported, hence its meet is supported. For the schema relation, the side condition follows by definition. `square`

The converse fails whenever `Q` omits a requirement that is open or refuted under `P`. This lemma is a finite order consequence; the paper-carrying Task 14 result is the exact soundness/relative-completeness characterization of the derivable preorder.

## 9. Labelled, output-producing consequence

Let

```text
Gamma |-_(e,q) phi
```

be the internal consequence/evaluation relation supplied by plan `e` under the interface in `q`. The core does not require every model to use the same object logic.

Licensed output production is written

```text
Gamma =>_[s,e,q,P] [e,q]phi.
```

The label cannot be erased by ordinary detachment.

### Core rule `USE`

```text
Assess(s,e,q,P)=Granted
Gamma |-_(e,q) phi
phi has the output type and scope required by q
------------------------------------------------ USE
Gamma =>_[s,e,q,P] [e,q]phi.
```

This produces an authorized scoped output. It does not derive `True_w(phi)`. Transport to another context `q'`, combination with another model, or removal of the label requires a separately validated bridge/transport rule.

### Core rule `WEAKEN-PROFILE`

Here `beta=(s,e,q)`.

```text
P >=_prof^beta Q
Assess(s,e,q,P)=Granted
-------------------------------- WEAKEN-PROFILE
Assess(s,e,q,Q)=Granted.
```

Its semantic justification is Lemma 1; Task 14 audits the exact side conditions.

### Core rule `FALLBACK`

For case `x`, define the active set

```text
Act(s,q,P,x)={e in K_s : x in D_q, Exec_e(q,x), Assess(s,e,q,P)=Granted}.
```

If `Act(s,q,P,x)` is empty, an action-authorizing selector may output only `F_q` or a declared information/abstention action. The display label `NoLicensedModel` is derived from this empty set; it is not an atom diagnostic.

Selection among a nonempty active set is q-dependent policy data. Being active, being preferred, being selected, and being archived remain different properties.

## 10. Update dynamics

### 10.1 History-preserving transitions

For `s -> s'`, there is an injective history/provenance embedding

```text
iota : Hist_s -> Hist_s'.
```

Old events remain addressable. Their current validity may change through appended corrections or countercertificates. Every standing request is recomputed from `WF`, current atom diagnostics, and finite meet.

### 10.2 Dependency interface

For meaningful atom `a` in request `r`, let

```text
Dep_s(r,a) subseteq_fin Hist_s
```

name the support, assumptions, verifier versions, and comparison/search nodes on which its diagnostic depends. The core exposes only this abstract dependency query and reachability/impact projection; a full DAG is an elaboration.

### 10.3 Core update principles

1. **Raw heredity:** events and prior assessments persist as historical records through `iota`.
2. **Current recomputation:** historical support does not force current support.
3. **Report locality:** if only report-only diagnostics change, top-level assessment is unchanged.
4. **Lapse/rebuttal:** invalidated support without a counterwitness yields open; a valid counterwitness yields refuted.
5. **Comparison locality:** `AddModel` can change profiles requiring/reporting the affected comparison atom while leaving `P_rely` unchanged when its dependencies are untouched.
6. **Query identity:** changing `e`, `q`, or `P` creates another linked request; it is not a state update of the same request.

### Proposition 2: extensional persistence

If `WF(r)` and every required diagnostic of `r` are identical at `s` and `s'`, then `Assess(r)` is identical.

**Proof.** The same finite required value vector has the same meet. `square`

This is only an extensional sufficient condition. Task 14 seeks the stronger characterization of which update classes guarantee diagnostic invariance from dependency-complete impact cones, and why path absence is not necessary without path realizability.

## 11. Two-sorted model semantics

A core model is

```text
M=(W,E,Q,S,->,I,nu,Diag,Dep),
```

where:

- `I_w` interprets target/world quantities;
- `nu_s` and `Diag_s` are the finite operational assessment maps;
- `Dep_s` records abstract support dependence; and
- `->` is compatible finite-state refinement.

The semantic interface imposes:

1. diagnostic/value agreement;
2. total `K_3` valuation after `WF`;
3. nonempty indexed witness, counterwitness, or obstacle payloads;
4. provenance membership in `s`;
5. finite profile and state support; and
6. history-preserving transitions.

An atom-specific certificate mode may add a soundness statement such as

```text
Pr_{w,s}[nu_s(Adeq(e,q,m))=+ implies Risk_w(e,q) in Acc_q] >= 1-alpha_m,
```

or a deterministic implication under frozen premises. There is no unqualified core axiom `supported -> target true`. Conformal miscoverage, statistical confidence failure, task tolerance, and fallback margin remain separately typed parameters.

## 12. Coordinate-indispensability theorem

Say assessment **factors through omission of coordinate `z`** when a function of the other three coordinates returns `Assess(s,e,q,P)` for every core model. To show that a coordinate is indispensable, it suffices to give two well-formed requests agreeing on the other three coordinates but receiving different outcomes.

### Theorem 3: `s,e,q,P` are independently indispensable

On the class of finite core models, `Assess` does not factor through omission of any one coordinate of `(s,e,q,P)`.

**Proof by four finite separators.** Use one scalar smaller-is-better adequacy setting and add only the listed diagnostics.

**Plan coordinate `e`.** Fix `s,q,P_rely`. Let `K_s={e_1,e_2}` and make both requests well formed. All required atoms for `e_1` are supported. For `e_2`, adequacy is refuted by a valid upper/lower risk countercertificate; its other required atoms are supported. Then

```text
Assess(s,e_1,q,P_rely)=Granted
Assess(s,e_2,q,P_rely)=Refused.
```

Any representation omitting `e` receives identical remaining inputs but would need two outputs.

**Context coordinate `q`.** Fix `s,e,P_rely`. Let one certificate locate scalar risk in `[0.09,0.11]`. Contexts `q_loose` and `q_strict` agree except

```text
epsilon_loose=0.20
epsilon_strict=0.05.
```

All other required atoms are supported. Adequacy is supported under `q_loose` and refuted under `q_strict`, so the outcomes are Granted and Refused.

**State coordinate `s`.** Fix `e,q,P_rely`. States `s_0,s_1` share the same library and interfaces. In `s_0`, a valid adequacy certificate is present; in `s_1`, the relevant evaluation has not occurred, so adequacy has obstacle `InsufficientEvidence`. Other required atoms are supported. The outcomes are Granted and Withheld.

**Profile coordinate `P`.** Fix `s,e,q`. All `P_rely` atoms are supported. The finite evaluated set also contains `d` with a valid certificate that `d` dominates `e` under the exact comparison scope. Then

```text
Assess(s,e,q,P_rely)=Granted
Assess(s,e,q,P_pref-rel)=Refused.
```

Thus each coordinate admits a pair with the other three fixed and different assessment. No coordinate can be omitted on all finite core models. `square`

The theorem establishes extensional necessity, not that each coordinate requires a separate neural module. A representation may encode coordinates jointly, provided it preserves all distinctions required by the assessment family.

## 13. Typed compression and elaboration

### 13.1 Compression from historical detailed records

Let `D` be a well-typed Task 7–11A record. Define compression `C(D)` by:

| detailed data | core destination |
|---|---|
| model version, solver, preprocessing, output/execution interface | `e in E` |
| task, cases/domain/distribution, frame, loss, risk aggregator, tolerance/acceptable set, fallback, margin, constraints | fields of `q in Q` |
| agent/stage record, library, evaluations, certificates, searches/budget, current validity, provenance | fields of `s in S` |
| required/report-only atom list, safety flags, parameter bindings | finite profile `P` |
| target population risk, target facts, optional truth interpretation | world index `w` |
| bridge, split, Pareto, mixture, theory-framework, policy/value records | extension data linked to the core tuple |

Historical reason tags compress to the atom address, polarity-specific payload, and provenance. They are not retained as independent semantic constructors.

### 13.2 Canonical elaboration

Conversely, a core tuple has a canonical minimal elaboration `J(s,e,q,P)` that materializes:

- one versioned model/use-plan record for `e`;
- one evaluation/request record containing the dependent fields of `q`;
- finite library, evidence, search, and abstract provenance records from `s`; and
- one profile record with instantiated required/report/safety slots.

Up to identifier renaming,

```text
C(J(s,e,q,P))=(s,e,q,P).
```

For a rich historical record `D`, `J(C(D))` need not reconstruct extension fields. Compression is intentionally lossy outside the core.

### 13.3 Assessment-preservation obligation

If detailed and core well-formedness agree and every detailed atom diagnostic maps to the same core address, `K_3` value, and provenance payload, then the two assessments agree by finite-meet functionality. Task 14 must state and prove the precise typed-elaboration invariance theorem; Task 11B supplies the executable regression witness.

## 14. Boundary between core and extensions

| layer | included objects | reason |
|---|---|---|
| minimal core | `E,Q,S,->,W` index, finite profiles, `WF`, `K_3`, indexed diagnostics, active set/fallback, labelled use, abstract dependencies | required to type and assess scoped reliance and update |
| canonical elaboration | detailed task/model/domain/certificate/search/provenance records, finite component DAGs, and selector traces | implementation, audit, and witness construction |
| formal extensions | bridges, transport, Pareto/frontier machinery, domain splits, mixtures, theory-framework relations, cyclic fixed-point evaluators | useful but not necessary for every license request |
| neural layer | encodings, margins, learned scoring heads, routers, external registry; ReLU is the reference construction | representation/learning of the calculus, not its semantics |
| policy/value case study | policy reconstruction, value surrogates, causal interpretability probes | optional application to transparency |
| metalanguage | eventual/certified stability, semantic finality, target truth | reasoning about sequences/worlds, not ordinary license derivation |

The term “atlas” names the richer licensed-cover extension. The core needs only profile-indexed active sets and gaps.

## 15. Central notation and glossary

| symbol/term | canonical meaning |
|---|---|
| `W`, `w` | target-world class and semantic index |
| `E`, `e` | evaluated use-plan carrier and one versioned executable plan |
| `Elab(e)` | optional finite well-founded component DAG hidden behind the core interface for `e` |
| `Q`, `q` | context carrier and one domain/task/loss/tolerance/fallback/frame package |
| `S`, `s`, `->` | finite epistemic-state carrier, one state, and refinement transition |
| `K_s` | finite library represented in `s` |
| `Eval_s(q)` | candidates validly evaluated for the exact comparison context |
| `P`, `shape(P)` | finite parameterized profile and its parameter-free slot/role shape |
| `Req`, `Report`, `Safety` | instantiated required, report-only, and safety atom addresses |
| `r=(s,e,q,P)` | complete core license request |
| `WF`, `WFDiag` | request well-formedness and its separate failure diagnostic |
| `K_3={-,?,+}` | refuted, open, supported meaningful atom states |
| `nu_s(e,q,a)` | operational value of atom address `a` |
| `Diag(r)` | complete atom-indexed diagnostics for a well-formed request |
| `Alarm`, `PendingSafety` | full refuted/open safety diagnostic submaps |
| `mu(r)` | finite meet of required atom values |
| `Assess(r)` | `Undefined`, `Refused`, `Withheld`, or `Granted` |
| `Lic_P(e,q)` | grant judgment at the named state/context/profile |
| `a =>_A b` | derivable typed atom refinement from stronger `a` to weaker `b` |
| `P >=_prof^beta Q`, `P >=_prof Q` | request-local and uniform schema forms of “`P` is at least as authorization-demanding as `Q`” |
| `Act(s,q,P,x)` | all plans granted under the same profile at case `x` |
| `F_q` | explicit fallback/abstention/information action |
| `Dep_s(r,a)` | finite abstract provenance dependencies of one atom diagnostic |
| `[e,q]phi` | labelled model output whose scope/context is not erased |
| `EventuallyStable`, `StableNow`, `CertifiedStable` | Task 12 metalanguage notions; always query/profile indexed |

This table is the canonical notation index. Later artifacts must record any deliberate deviation.

## 16. Metatheory dependency and novelty audit

| result or target | dependency | classification | status / task |
|---|---|---|---|
| two-phase status normal form | `WF`, `K_3`, finite meet | definition plus standard algebra | implemented Task 11B; audit Task 14 |
| meet commutative/associative/idempotent | Strong-Kleene chain | standard imported algebra | supported E16 |
| profile grant antitonicity | atom-refinement soundness | elementary lemma | stated here; audit Task 14 |
| coordinate indispensability | complete request interface | finite separating theorem/countermodels | proved here |
| indistinguishable-prefix non-certifiability | continuation semantics | paper-carrying impossibility | proved Task 12 |
| statistical stabilization / zero-error barrier | coverage, shrinkage, finite-prefix equivalence | convergence plus impossibility | proved Task 12 |
| positive open-library non-finality | valid `AddModel` dominator continuation | paper-carrying impossibility | proved Task 12 |
| robust update persistence | `Dep`, update class, path realizability | new characterization target | Task 14 |
| profile refinement relative completeness | typed atom rules, independent-atom models | new characterization target | Task 14 |
| minimal diagnostic quotient and bit bound | all supported profile queries, singleton profiles | new representation lower bound | Task 14 |
| mode-scoped soundness | `<W,S>`, certificate-specific assumptions | theorem family, not one universal theorem | Task 14 |
| finite plan-composition closure | typed component interfaces, propagation certificates, interaction assumptions | standard/extension lemma or countermodel family | Tasks 14–14A |
| unrestricted rational monotony/global closure | state transitions/open library | negative/countermodel targets | Task 14 |
| subdomain/routed/bridge risk bounds | measure, router, loss, bridge hypotheses | cross-layer extension theorems | Task 14A |
| finite ReLU reference representation and hard-seam characterization | diagnostic quotient, CPWL assumptions | representation/impossibility cluster for one architecture class, not an optimality claim | Task 17 |
| semantic/activation alignment | synthetic and later real examples | empirical hypothesis | Tasks 19–25 |

Definitions and imported three-element lattice facts do not count as the project's paper-carrying theorem contribution. Coordinate indispensability protects the interface but is a finite separation result; the principal theorem spine remains the Task 12 impossibilities plus the Task 14 characterization, Task 14A transport bounds, and Task 17 representation/seam results if they survive audit.

## 17. Decisions frozen for Task 14

1. The core has three principal carriers `E,Q,S`; `W` is a semantic index and profiles are finite syntax.
2. A request is exactly `(s,e,q,P)`, and each coordinate is extensionally indispensable.
3. Domain, task, loss, risk, tolerance, fallback, constraints, and frame are fields of `q`.
4. Record, finite library/evaluated set, search/budget, certificates, dependencies, validity, and provenance are fields of `s`.
5. `WF` precedes meaningful evaluation; `Undefined` is not in `K_3`.
6. Meaningful atoms use Strong-Kleene finite meet with an evidential interpretation.
7. Diagnostics are atom-indexed sum records with mandatory provenance, not flat reason constructors.
8. Safety projections retain full selected diagnostics.
9. Profile shape and parameters are distinct; profiles are finite indexed families so repeated kinds remain addressable.
10. Atom/profile refinement is typed and scope-sensitive; no rule silently enlarges a domain, candidate set, or future library.
11. Consequence produces labelled authorized outputs and has no unqualified truth-detachment rule.
12. Empty active sets derive fallback behavior and the display `NoLicensedModel`; they do not create an atom reason.
13. Raw history is hereditary while current diagnostics are recomputed and may lapse or be rebutted.
14. Bridges, Pareto/splitting, full atlases, mixtures, and policy/value work are extensions.
15. Task 14 may repair a frozen rule only by proving a countermodel and propagating its project impact.
16. A core plan may elaborate into a finite well-founded component DAG, and evaluators may receive higher-order requests; cyclic evaluator/license dependence remains a fixed-point extension rather than an implicit core feature.

## Task conclusion

The project now has one compact calculus rather than a stack of partially overlapping record schemas. It says what a bounded agent may currently rely on without turning usefulness into truth: choose a versioned use plan `e`, state the complete reliance context `q`, evaluate it in finite state `s`, and name the finite requirement profile `P`. Well-formedness is checked first; meaningful requirements are then refuted, open, or supported with explicit diagnostics; their finite meet yields the public outcome.

This core is small enough to support real metatheory and explicit neural representation. It is also rich enough to preserve the project's central distinctions: absolute versus fallback-relative adequacy, basic reliance versus preferred use, unknown versus refuted requirements, simultaneous active models versus selection, historical retention versus current warrant, and finite evidence versus target-world truth. Task 14 can now test the calculus rather than another implementation inventory.
