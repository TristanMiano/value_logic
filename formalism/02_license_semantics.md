# Finite-Stage License Semantics

Status: Task 8 formal specification, version 0.1  
Date: 2026-07-11  
Depends on: [`01_signature.md`](01_signature.md)  
Scope: finite-stage adequacy, certification, reliance, search closure, abstention, and defeat; consequence and update rules begin in Task 9

> **Task 11A interface notice.** This historical artifact predates mandatory profile indexing. Read its full bare `Lic` conjunction as the strong named profile `Lic_{P_full^8}`, not as the universal meaning of licensing. Read current-license and active-set views as profile-indexed. See [`05a_integration.md`, §16](05a_integration.md#16-repairs-to-completed-interfaces); Task 13 will consolidate the notation.

> **Checkpoint A1 compactness notice.** The four public outcomes remain, but the flat reason-code list in §2 is illustrative implementation vocabulary rather than primitive logical syntax. The planned core first checks well-formedness (`Undefined` on failure), then assesses each meaningful requirement atom in `K_3={refuted,open,supported}` and aggregates by finite meet. Reasons factor through atom identity plus counterwitness, obstacle, and provenance. Task 13 will state the canonical algebra and prove its information properties.

## Executive definition

A finite-stage license is an evidence-relative permission to rely on a versioned model for a typed evaluation scope. It is not a truth value assigned to the model.

At agent `a`, stage `t`, and budget `b`, the full license

```text
Lic_{a,t,b}(m;q,epsilon,alpha,F,Delta,K,c,sigma,p | R)
```

is granted exactly when the request is well formed and all of the following are certified:

1. `m` satisfies the hard adequacy requirement for `q` and `epsilon`;
2. `m` improves sufficiently over the explicit fallback `F` under `Delta`;
3. `m` satisfies the hard cost/safety/resource constraints in `c`;
4. no certified dominator occurs in the search scope declared by `sigma` under the current admissibility rule;
5. the evidence, comparison, search, and decision are connected by valid provenance `p`.

In schematic form:

```text
Lic = CertAdeq
      AND CertImprove
      AND ConstraintOK
      AND SearchAdmissible
      AND TraceOK.
```

The operational evaluator does not return only yes/no. It returns one of:

```text
Granted
Refused(reason)      -- contrary evidence certifies a required condition fails
Withheld(reason)     -- evidence/search/comparison is insufficient or unresolved
Undefined(reason).   -- the request is ill-typed or non-executable
```

Only `Granted` makes the formula `Lic(...)` obtain. The other outcomes remain distinct. In particular, `Withheld` is not evidence that the model is inadequate, and `Undefined` is not negation.

## 1. Finite-stage semantic structures

### 1.1 Stage structure

For each agent-stage pair `(a,t)`, define a finite semantic structure

```text
S_{a,t} = <
    R_{a,t},
    K_{a,t},
    b_{a,t},
    AdmView_{a,t},
    CertProcedures_{a,t},
    Selectors_{a,t},
    ProvGraph_{a,t}
>.
```

where:

- `R_{a,t}` is the finite versioned record;
- `K_{a,t}` is the finite stage-local library;
- `b_{a,t}` is the available budget;
- `AdmView_{a,t}` supplies the evidence events currently admissible under stated protocols;
- `CertProcedures_{a,t}` contains the certificate-generating procedures the agent is entitled to use;
- `Selectors_{a,t}` contains available routing/decision rules;
- `ProvGraph_{a,t}` connects the relevant artifacts and decisions.

The structure does not contain an oracle saying which current theory is finally true. For formal analysis, the metalanguage may refer to target risks and data-generating states that the agent does not observe.

### 1.2 World/stage models, satisfaction, and assessment

The semantic model is a pair:

```text
M_{W,a,t} = <W,S_{a,t}>.
```

`W` is a metalanguage world/environment structure containing the population or data-generating objects needed to determine target risks. It is not assumed to be observed by the agent. `S_{a,t}` is the finite stage structure above. This gives three deliberately distinct judgment levels:

```text
W |=_world Adeq(m;q,epsilon)          -- target/world-level
S_{a,t} |=_stage CertAdeq(...)        -- finite-stage evidential
M_{W,a,t} |=_mixed J                  -- explicitly mixed, when needed.
```

For a stage-level judgment `J`, use two related notions:

```text
S_{a,t} |=_stage J
```

means that judgment `J` obtains at the stage, while

```text
Assess_{a,t}(J) in Status
```

returns its operational status and reasons.

The connection is:

```text
S_{a,t} |=_stage J  iff  Assess_{a,t}(J) = Granted.
```

This keeps a classical meta-level satisfaction relation available while preventing all non-grants from collapsing into one operational state. When an older section uses undecorated `|=`, its formula family determines the sort; Task 13 must make the annotation explicit in the core grammar. A soundness claim must therefore name a class of pairs `<W,S>` and the certificate-mode relation connecting stage evidence to world facts.

### 1.3 Stage locality

Every license is stage-local:

```text
ValidAt(lic_ref,a,t).
```

A later withdrawal does not rewrite the historical claim as

```text
NeverValid(lic_ref).
```

It records that a later structure no longer grants the same request or grants a defeat judgment. Whether the earlier grant was procedurally warranted is evaluated against the earlier record, protocol, and search scope.

## 2. The four-way operational status

### 2.1 Status type

```text
Status =
    Granted(payload,trace)
  + Refused(reason,countercertificate?,trace)
  + Withheld(reason,missing_or_unresolved,trace)
  + Undefined(type_or_execution_error,trace?).
```

Typical **derived display labels** include:

```text
HardRiskViolation
FallbackNotBeaten
HardConstraintViolation
CertifiedDominatorFound
InsufficientEvidence
CertificateStraddlesBoundary
UnsupportedDomainView
UnknownComparison
SearchScopeTooWeak
NoLicensedModel
FrameMismatch
LossMismatch
UnavailableFallback
BrokenProvenance.
```

These labels abbreviate the requirement being assessed plus its witness, counterwitness, obstacle, or failed well-formedness derivation. They are not intended to form a closed exhaustive enum; the Checkpoint A1 compact core factors them through `WF + K_3`.

### 2.2 Conjunctive aggregation

For required component statuses `z_1,...,z_n`, define `AllReq(z_1,...,z_n)` by precedence:

1. if any component is `Undefined`, return `Undefined`;
2. otherwise, if any component is `Refused`, return `Refused` with every certified failure reason;
3. otherwise, if any component is `Withheld`, return `Withheld` with every unresolved requirement;
4. otherwise return `Granted`.

The precedence is diagnostic, not metaphysical. A request with a frame mismatch is not made meaningful merely because another component has evidence against it.

### 2.3 Negation warning

The object-level formula `Lic(...)` obtains only in the granted case. Nevertheless, the operational system must not infer any of the following from a non-grant alone:

```text
not Lic(m;...)  => FalseTheory(m)
not Lic(m;...)  => CertInadequate(m;q,epsilon)
not Lic(m;...)  => Lic(F;...)
not Lic(m;...)  => another candidate is licensed.
```

Those require separate evidence and well-formed judgments.

## 3. Population or target adequacy

### 3.1 Acceptable risk region

For `q : EvalSpec` and `epsilon : Tol(q)`, define

```text
A_q(epsilon) = Down_q(epsilon)
             = { r in Q_q : r preceq_q epsilon }.
```

If an application supplies a general admissible down-set `A_q` instead of a principal threshold, replace `A_q(epsilon)` by that set.

### 3.2 Defined risk

`Risk_q(m)` is defined only if:

- `m` has a complete interface for the task(s) and frame in `q`;
- the population/data-generating object required by `risk(q)` exists;
- the loss is measurable/evaluable as required;
- the aggregation rule produces an element of `Q_q`.

Write

```text
RiskDefined(m,q).
```

Undefined risk makes `Adeq` undefined rather than false.

### 3.3 Adequacy semantics

```text
W |=_world Adeq(m;q,epsilon)
```

iff

```text
RiskDefined(m,q)
and Risk_q(m) in A_q(epsilon).
```

Target adequacy is determined by `W` and is stage-invariant when `m`, `q`, `epsilon`, and the underlying population are unchanged. Its observability and certification are stage-relative properties of `S_{a,t}`. The pair notation prevents a target fact unavailable to the agent from being smuggled through a stage-only satisfaction symbol.

### 3.4 Certified inadequacy

Define target inadequacy only relative to the same acceptable region:

```text
Inadeq(m;q,epsilon)
  iff RiskDefined(m,q)
      and Risk_q(m) notin A_q(epsilon).
```

In a partial order, failure of `r preceq_q epsilon` can include incomparability. If the application wants “strictly worse than the tolerance” to exclude incomparability, it must define a typed rejection region `Bad_q(epsilon)` disjoint from `A_q(epsilon)`. The project will not assume total order merely for convenience.

## 4. Empirical adequacy

### 4.1 Empirical evaluation event

Let an admissible evaluation event in `R` contain

```text
e = Evaluation(m,q,S,w,result,protocol,p_e)
```

where `S=(z_1,...,z_n)` is a finite task-typed sample and `w` contains any declared weights.

For an empirical aggregator:

```text
RiskHat_{e,q}(m)
  = rho_emp(ell(m,z_1),...,ell(m,z_n);w).
```

### 4.2 Empirical adequacy semantics

```text
EmpAdeq_e(m;q,epsilon)
```

iff

```text
e is admissible for q in R
and RiskHat_{e,q}(m) in A_q(epsilon).
```

`EmpAdeq` says exactly that the recorded empirical quantity meets the recorded threshold. It does not imply `Adeq` unless a valid generalization/certification rule connects the sample to the target risk.

### 4.3 Sample-relative honesty

If the sample was selected after examining failures, drawn from a different distribution, adaptively reused, or produced by a simulator whose relation to the target domain is unknown, `EmpAdeq` may still be a correct statement about that sample. The problem appears in any attempted certification or domain extrapolation, which must name those conditions.

### 4.4 Empirical-only licenses

An application may intentionally request

```text
alpha.interpretation = EmpiricalOnly.
```

Such a judgment can support a license only if the license is explicitly labeled

```text
EmpiricalLicense
```

and its scope is the recorded sample or benchmark. It must not be restated as a population guarantee.

## 5. Certificate objects

### 5.1 Certificate result

A certificate procedure produces

```text
kappa = Certify_{a,t}(target;alpha | R)
      : CertResult
```

with record

```text
CertResult = <
    cert_id,
    mode,
    target,
    eval_spec,
    evidence_view,
    assumptions,
    payload,
    validity_obligation,
    diagnostics,
    provenance
>.
```

Possible payloads include:

```text
Region(C subseteq Q_q)
UpperBound(u in Q_q)
LowerBound(l in Q_q)
JointRegion(C subseteq Q_q x Q_q)
Posterior(nu on Q_q)
CoverageStatement(statement,level)
DeterministicProof(proof_ref)
EmpiricalResult(value).
```

### 5.2 Validity of a certificate

```text
ValidCert_{a,t}(kappa;alpha,q,R)
```

requires:

1. the procedure is authorized and versioned in `S_{a,t}`;
2. `kappa.target`, `q`, and the evidence view have matching types;
3. the data/sampling/structural assumptions required by `alpha` are recorded and not defeated in the admissible record view;
4. the promised validity obligation is appropriate for `risk(q)`;
5. the payload and its units/order match `Q_q`;
6. the provenance trace reaches the data, model version, domain version, code/proof, and procedure version used.

A certificate can be computed yet invalid for the requested target. For example, a concentration bound assuming i.i.d. samples is not a valid certificate for a dependent sample unless an appropriate replacement theorem is supplied.

### 5.3 Validity is itself defeasible at the evidence layer

`ValidCert` is a finite-stage procedural/evidential judgment. Discovery that a sampler was biased, an implementation was incorrect, or an assumption failed can invalidate the certificate at a later stage without changing the target risk.

## 6. Calibration and confidence modes

No single probability expression covers every `CertSpec`. Define support and refutation mode by mode.

### 6.1 Deterministic region or proof

For a valid deterministic certificate with payload `Region(C)` and a guarantee

```text
Risk_q(m) in C,
```

define:

```text
SupportsAdeq(kappa,epsilon) iff C subseteq A_q(epsilon)
RefutesAdeq(kappa,epsilon)  iff C subseteq Q_q \ A_q(epsilon).
```

If `C` intersects both regions, the result is withheld.

### 6.2 Scalar frequentist upper confidence bound

For `Q_q subseteq R_bar` and smaller risk preferred, let a procedure output `U_alpha(R)` satisfying a repeated-sampling coverage statement such as

```text
Pr_R[ Risk_q(m) <= U_alpha(R) ] >= alpha
```

under its declared data-generating assumptions.

Then:

```text
SupportsAdeq(kappa,epsilon) iff U_alpha(R) <= epsilon.
```

A lower confidence bound `L_alpha(R)>epsilon` can support refusal. An upper bound exceeding `epsilon` does **not** itself refute adequacy; it may merely withhold certification.

The statement above is a property of the procedure under repeated sampling. It is not the posterior statement

```text
Pr(Risk_q(m) <= epsilon | R) >= alpha.
```

### 6.3 Bayesian posterior support

For payload `Posterior(nu_R)`:

```text
SupportsAdeq(kappa,epsilon)
  iff nu_R(A_q(epsilon)) >= alpha.level.
```

If a symmetric refusal threshold is requested:

```text
RefutesAdeq(kappa,epsilon)
  iff nu_R(A_q(epsilon)) <= 1 - alpha.level.
```

The prior, likelihood, model class, and posterior computation are part of the certificate provenance. This is posterior support conditional on those assumptions, not assumption-free knowledge.

### 6.4 Conformal/selective guarantees

A conformal or selective certificate must state its target exactly: marginal prediction-set coverage, selective risk at a coverage level, or another guarantee. It supports `CertAdeq` only when a proved map turns that target into membership of `Risk_q(m)` in `A_q(epsilon)`.

Prediction coverage alone does not automatically certify expected loss, worst-case risk, calibration, or safety.

### 6.5 Vector or partial-order certificates

For a valid joint region `C subseteq Q_q`:

```text
SupportsAdeq(kappa,epsilon) iff
    forall r in C, r preceq_q epsilon.
```

For componentwise scalar bounds, this becomes

```text
U_j <= epsilon_j for every required coordinate j.
```

If the coordinates are statistically dependent, separate marginal intervals need a declared simultaneous-coverage rule before their Cartesian product is treated as one joint certificate.

### 6.6 Calibration-test-only payloads

Passing an empirical calibration test supports only the calibration statement the test was designed to assess. It becomes a risk certificate only if `alpha.validity_obligation` supplies that implication. This prevents “well calibrated” from serving as an untyped synonym for “safe” or “accurate.”

## 7. Certified adequacy

### 7.1 Assessment

Let

```text
kappa_m = Certify_{a,t}(Risk_q(m);alpha | R).
```

Define:

```text
AssessCertAdeq_{a,t}(m;q,epsilon,alpha | R)
```

as follows:

1. if the adequacy request is ill formed, return `Undefined`;
2. if no valid certificate can be produced, return `Withheld(InsufficientEvidence)`;
3. if `SupportsAdeq(kappa_m,epsilon)`, return `Granted(kappa_m)`;
4. if `RefutesAdeq(kappa_m,epsilon)`, return `Refused(HardRiskViolation,kappa_m)`;
5. otherwise return `Withheld(CertificateStraddlesBoundary,kappa_m)`.

### 7.2 Satisfaction

```text
S_{a,t} |= CertAdeq_{a,t}(m;q,epsilon,alpha | R)
```

iff

```text
AssessCertAdeq_{a,t}(m;q,epsilon,alpha | R) = Granted.
```

### 7.3 Relation to target adequacy

The logical relation depends on certificate mode:

- a sound deterministic proof can imply target `Adeq` outright;
- a frequentist grant inherits the procedure's coverage guarantee, not certainty at this realized record;
- a Bayesian grant means posterior support at the stated level;
- an empirical-only grant remains sample-relative.

The final paper must attach the appropriate modal qualifier rather than write one unqualified theorem `CertAdeq => Adeq` for every mode.

### 7.4 Certified inadequacy

The corresponding stage-relative negative judgment is:

```text
S_{a,t} |= CertInadeq_{a,t}(m;q,epsilon,alpha | R)
```

iff

```text
AssessCertAdeq_{a,t}(m;q,epsilon,alpha | R)
  = Refused(HardRiskViolation,kappa_m).
```

Thus `CertInadeq` requires a valid countercertificate establishing non-membership in the acceptable region. A withheld or undefined adequacy request does not satisfy it. `CertInadequate` is treated as a readable alias for `CertInadeq`, not as a second predicate.

## 8. Fallback-relative improvement

### 8.1 Explicit fallback requirement

Every full use-license requires

```text
F != NoFallback.
```

`NoFallback` remains permitted in `Adeq` and `CertAdeq` requests, which can describe model performance without authorizing reliance. A practical reliance decision must name what happens otherwise.

### 8.2 Comparison specification

`Delta : Improve(q,F)` contains or references:

```text
<
    candidate_value_map,
    fallback_value_map,
    common_comparison_space,
    advantage_relation,
    required_margin,
    uncertainty_protocol,
    provenance
>.
```

Let the target comparative values be

```text
J_m = J_{q,Delta}(m)
J_F = J_{q,Delta}(F)
```

in a common ordered space `Q_Improve`.

Define the required advantage relation

```text
Adv_Delta(J_m,J_F).
```

For scalar costs with smaller values preferred:

```text
Adv_Delta(J_m,J_F) iff J_m + Delta <= J_F.
```

### 8.3 Joint uncertainty

The preferred certificate is a joint certificate

```text
kappa_{m,F} = Certify_{a,t}((J_m,J_F);alpha | R)
```

with payload `JointRegion(C_{m,F})`. Then

```text
SupportsImprove(kappa_{m,F},Delta)
  iff forall (r_m,r_F) in C_{m,F}, Adv_Delta(r_m,r_F).
```

For scalar marginal bounds, the sufficient conservative condition is

```text
U_m + Delta <= L_F.
```

where `U_m` is a valid upper cost/risk bound for the candidate and `L_F` is a valid lower bound for the fallback under a simultaneous or otherwise justified comparison protocol.

### 8.4 Assessment

`AssessImprove` returns:

- `Undefined` if the fallback is unavailable, non-executable, or incommensurable;
- `Withheld` if no valid comparison certificate exists or it straddles the advantage boundary;
- `Refused(FallbackNotBeaten)` if the certificate supports failure of `Adv_Delta`;
- `Granted` if the certificate supports `Adv_Delta` throughout its uncertainty region or under the specified posterior/coverage rule.

### 8.5 External and fallback-induced thresholds

Hard adequacy and fallback improvement remain separate even when both are scalar. If

```text
epsilon_F = J_F - Delta,
```

then the full effective threshold may be

```text
epsilon_eff = min(epsilon_hard,epsilon_F)
```

only when every term shares a scalar space, orientation, and uncertainty treatment. With estimated `J_F`, `epsilon_F` is itself uncertain; conservative certification uses the fallback lower bound, not a plug-in estimate presented as known.

## 9. Hard constraints and cost admissibility

### 9.1 Constraint profile

Let `Hard(c)` be the set of hard constraints in the cost profile and `Soft(c)` the coordinates used for ranking or Pareto comparison.

Examples of hard constraints include:

```text
latency <= 20 ms
memory <= budgeted memory
safety_risk <= threshold
required provenance complete
forbidden data source absent.
```

### 9.2 Assessment

```text
AssessConstraintOK_{a,t}(m;c,q | R)
```

is:

- `Granted` if every hard constraint is certified;
- `Refused(HardConstraintViolation)` if a valid countercertificate establishes a violation;
- `Withheld` if a required coordinate is unknown or its certificate straddles the bound;
- `Undefined` if the constraint is ill-typed for the model/task.

Soft cost coordinates do not independently refuse a license; they enter dominance or selection.

## 10. Search scope and closure

### 10.1 Evaluated search scope

For a search trace `sigma`, define

```text
E_sigma(q) = Evaluated(sigma,q).
```

Only models with valid comparable evaluations belong to `E_sigma(q)`. Retrieved-but-unevaluated models, timeouts, frame mismatches, and failed runs remain in diagnostics but do not count as defeated alternatives.

### 10.2 Three closure strengths

#### Relative evaluated closure

```text
RelClosed(m;q,sigma,c | R)
```

means no model in `E_sigma(q)` is a certified dominator of `m` under the current relation.

This is the default and weakest admissibility clause. It means:

> no certified dominator was found among the models actually evaluated in this trace.

#### Declared-library closure

```text
LibClosed(m;q,K,sigma,c | R)
```

requires:

1. every relevant active entry in the declared finite library `K` is either validly evaluated on `q` or accompanied by a proved inapplicability reason;
2. no evaluated entry certifiably dominates `m`;
3. unknown comparisons required by the chosen order are resolved or explicitly permitted by the closure policy.

Timeouts and unexamined candidates prevent this stronger closure claim.

#### Global closure

```text
GlobalClosed(m;q)
```

would quantify over the entire model universe. It is unavailable in the base finite-stage semantics unless an independent completeness theorem supplies a finitely checkable reduction. No ordinary search trace establishes it.

### 10.3 Closure requested by the search

`sigma.query` must declare one of:

```text
RelativeEvaluated
DeclaredLibrary
ProvedComplete(class_ref,proof_ref).
```

If absent, the default is `RelativeEvaluated`.

### 10.4 Search failures

Failures have asymmetric meaning:

- a successful evaluation may certify domination;
- a failed evaluation does not certify non-domination;
- under relative closure it narrows the reported scope;
- under declared-library closure it normally causes `Withheld(SearchIncomplete)`.

## 11. Library-relative admissibility

### 11.1 Provisional certified dominance

Until Task 10 fixes scalar and Pareto dominance, let

```text
CertDominates_{a,t}(m',m;q,c | R)
```

be a typed relation supplied by the admissibility profile. At minimum it requires valid comparative certificates over every coordinate used and strict improvement on the coordinate(s) required by the selected rule.

Unknown or incomparable pairs do not satisfy `CertDominates`.

### 11.2 Default relative admissibility

```text
AdmissibleRel_{a,t,b}(m;q,K,sigma,c | R)
```

iff:

1. `sigma.agent=a`, `sigma.stage=t`, and `sigma.budget preceq b`;
2. `m in E_sigma(q)` or `m` is the designated candidate with an equivalent valid evaluation;
3. every alleged comparator is a versioned member/new candidate connected to `K` by the trace;
4. there is no `m' in E_sigma(q)` such that `CertDominates_{a,t}(m',m;q,c|R)`;
5. the provenance of the relative closure statement is complete.

### 11.3 Assessment

For relative closure:

- return `Refused(CertifiedDominatorFound,m')` if such `m'` exists;
- return `Granted(scope=E_sigma(q))` if no certified dominator exists;
- return `Undefined` for type/provenance mismatch.

Unresolved comparisons are reported in the grant payload. They do not become evidence of non-domination. If the application requires every comparison resolved, it must request declared-library closure, which returns `Withheld` instead.

### 11.4 Meaning of the grant

An admissibility grant never entails:

```text
m is globally optimal
m is uniquely best
every model in K was evaluated
no future model can dominate m
unexamined models are worse.
```

It entails only the closure strength and evaluated scope recorded in `sigma`.

## 12. Provenance sufficiency

### 12.1 Trace predicate

```text
TraceOK_{a,t}(m,q,epsilon,alpha,F,Delta,K,c,sigma,p | R)
```

holds iff `p` contains directed, version-consistent paths from the requested license to:

- the exact model and frame versions;
- domain, loss, risk, tolerance, and certificate specifications;
- admissible data/evidence events and corrections;
- fallback and comparison protocol;
- cost constraints;
- library and search trace;
- certificate code/proof and assumptions;
- selector or intended action interface.

### 12.2 Broken or partial traces

A broken required path returns `Undefined(BrokenProvenance)` when identity or typing cannot be established. A nonessential missing annotation may return `Withheld(IncompleteTrace)` if the application permits repair.

Provenance does not prove substantive correctness by itself. It makes the asserted grounds inspectable and permits later correction or defeat.

## 13. Full use-license semantics

### 13.1 Full assessment

Let the request record be

```text
omega = <a,t,b,m,q,epsilon,alpha,F,Delta,K,c,sigma,p,R>.
```

Define:

```text
AssessLic(omega) = AllReq(
    AssessWF(omega),
    AssessCertAdeq_{a,t}(m;q,epsilon,alpha | R),
    AssessImprove_{a,t}(m;F,q,Delta,alpha | R),
    AssessConstraintOK_{a,t}(m;c,q | R),
    AssessAdmissible_{a,t,b}(m;q,K,sigma,c | R),
    AssessTraceOK(omega)
).
```

For a full use-license, `AssessWF(omega)` returns `Undefined(MissingExplicitFallback)` when `F=NoFallback`. This is a malformed decision request, not evidence that the model is inadequate. (`NoFallback` remains well formed for adequacy-only judgments.)

### 13.2 Satisfaction

```text
S_{a,t} |= Lic_{a,t,b}(m;q,epsilon,alpha,F,Delta,K,c,sigma,p | R)
```

iff

```text
AssessLic(omega) = Granted.
```

### 13.3 Grant payload

A granted license stores at least:

```text
LicenseGrant = <
    license_id,
    agent,
    stage,
    model_ref,
    eval_spec_ref,
    hard_tolerance,
    cert_result_ref,
    fallback_ref,
    improvement_certificate_ref,
    hard_constraint_results,
    closure_strength,
    evaluated_search_scope,
    unresolved_comparisons,
    selector_or_action_scope,
    provenance_ref,
    expiry_or_review_condition?,
    status=active
>.
```

This record is the structured object that later neural outputs must approximate or point toward.

### 13.4 Optional conjuncts

The project may define narrower judgments such as `SafetyLicense`, `BenchmarkLicense`, or `AdequacyOnly`. They must use different names or an explicit `RequirementProfile`. The unqualified `Lic` in this project means the full factored use-license above.

## 14. Pointwise active sets

### 14.1 Point request context

For `x : Case(tau)`, construct a point evaluation specification `q_x` as defined in Task 7, while keeping agent, stage, fallback, costs, and closure policy fixed.

### 14.2 Active licensed model set

```text
Active_{a,t,b}(x;q_x,K | R)
  = { m in Active(K) : AssessLic(omega_{m,x}) = Granted }.
```

This is set-valued. Multiple models may be active, and no model may be active.

### 14.3 Diagnostic partition

Also retain:

```text
RefusedSet(x)  = {m : AssessLic(omega_{m,x}) is Refused}
WithheldSet(x) = {m : AssessLic(omega_{m,x}) is Withheld}
UndefinedSet(x)= {m : AssessLic(omega_{m,x}) is Undefined}.
```

An empty active set does not reveal which of these three explanations applies.

## 15. Selection, fallback, and abstention

### 15.1 Selector constraint

A valid selector must satisfy:

```text
if select(pi_sel,x)=Use(m), then m in Active_{a,t,b}(x;q_x,K|R).
```

It may select among multiple active models by certified risk, cost, robustness, interpretability, a Pareto policy, mixture rule, or information value. Selection semantics will be expanded in Tasks 9–10.

### 15.2 Mandatory gap rule

Define:

```text
MustFallback_{a,t,b}(x;q_x,K | R)
  iff Active_{a,t,b}(x;q_x,K | R) = empty.
```

A safe selector obeys:

```text
MustFallback(x) =>
    select(pi_sel,x) in {
        Reject,
        Defer,
        StatusQuo,
        InformationAction,
        LicensedFallbackModel
    }.
```

It must not choose the highest-scoring unlicensed model merely because the active set is empty.

### 15.3 Abstention judgment

```text
S_{a,t} |= Abstain_{a,t,b}(x;pi_sel,q_x,K,F | R)
```

iff the selector returns `Reject`, `Defer`, or an explicitly designated abstention action. A status-quo action and information-gathering action are fallback decisions but may be reported separately from abstention.

### 15.4 Voluntary fallback

Even with a nonempty active set, the selector may choose a fallback if the selection policy legitimately accounts for switching cost, information value, deference rules, or other criteria not already required by candidate licensing. This must be traceable and must not be reported as evidence that the active models are inadequate.

### 15.5 Selective risk and coverage

For deployment distribution `mu_D`, define the selector's coverage

```text
Coverage(pi_sel,D) = Pr_{x~mu_D}[select(pi_sel,x)=Use(m) for some m].
```

and selective risk

```text
SelRisk(pi_sel,D)
  = E[loss of selected model | a model is used]
```

when the conditional event has positive probability. Coverage, selective risk, and fallback cost must be reported together. Lower selective risk can be purchased by abstaining almost everywhere.

## 16. Evidence-based defeat

### 16.1 Later-stage setup

Let `lic` be granted at `(a,t)` from `R`, and let `t preceq_Stage t'` with later record `R'` referring to the same request fields unless a changed field is explicitly identified.

### 16.2 Strong empirical rebuttal

```text
DefeatedByEvidence(lic,R,R')
```

holds in the strong sense iff:

1. `lic` was granted from `R`;
2. `R'` contains or validates a certificate `kappa'` for the same versioned model and evaluation specification;
3. `RefutesAdeq(kappa',epsilon)` or another required component is certifiably violated;
4. the defeat trace identifies the new/corrected evidence and affected requirement.

This supports `Refused` at `t'`.

### 16.3 Evidential lapse without rebuttal

Define:

```text
LapsedByEvidence(lic,R,R')
```

iff the former supporting certificate becomes invalid, inapplicable, expired, or boundary-straddling under `R'`, but no valid countercertificate establishes the requirement's failure.

This changes the later status to `Withheld`, not `Refused`.

Examples include discovery of sample leakage, a broken sensor, distribution shift outside the certified scope, or expiration of a calibration guarantee.

### 16.4 Scope change is not automatically defeat

If `D`, `L`, `rho`, `epsilon`, or the fallback changes, the result is normally a new request. A model can remain licensed for the old `q` while being refused or withheld for the new one. Provenance should link the requests without calling every scope change a contradiction.

## 17. Defeat by a newly retrieved dominator

### 17.1 Comparative defeat

Let later library/search objects be `K'` and `sigma'`, and let `m'` be newly retrieved or newly evaluable. Then

```text
DefeatedByDominator(lic,m',q,K',sigma',R')
```

holds iff:

1. `lic` was granted at `t` under an admissibility component;
2. `m'` is validly evaluated on the same `q` or a typed comparable restriction;
3. `CertDominates_{a,t'}(m',m;q,c | R')`;
4. the later search closure includes `m'`;
5. the later `AssessAdmissible(m;...)` returns `Refused(CertifiedDominatorFound,m')`.

### 17.2 What comparative defeat does not imply

It does not by itself imply:

```text
Inadeq(m;q,epsilon)
not CertAdeq(m;q,epsilon,alpha|R')
delete m from K'
m' is finally optimal
m' dominates m on every subdomain or cost vector.
```

It removes or narrows the **admissibility/use** component under the stated order. Hard adequacy and archival retention are separate.

### 17.3 Partial domination

If `m'` dominates only on `D' subset D`, the semantics records a proposed restriction/split:

```text
RestrictedTo(lic,D \ D')
```

only after the residual domain, measures, frames, and certificates are reconstructed. Task 10 will supply exact conditions; set subtraction alone is insufficient for distributional domains.

## 18. Historical retention and current status

### 18.1 License event history

Every grant, refusal, withholding, lapse, and defeat is an evidence event. A later stage retains links:

```text
issued_at
supported_by
lapsed_because
defeated_by
restricted_to
superseded_for_selection_by.
```

### 18.2 Current license view

The current active license set is a derived view over the event record, not the raw event collection:

```text
CurrentLicenses(R_{a,t})
  = grants not withdrawn, lapsed, expired, or defeated
    under the current admissible event view.
```

Removing a grant from `CurrentLicenses` does not delete its historical event or supporting trace.

### 18.3 No retroactive truth claim

A properly issued earlier license can be defeated later because the finite-stage warrant changed. The semantics does not infer that the earlier model changed metaphysical truth value at the update time.

## 19. Small examples

### 19.1 Classifier, hard threshold, and defer fallback

Let `q` measure expected classification error on a deployment distribution, with

```text
epsilon = 0.10
F = Defer(human_reviewer)
Delta = 0.02
```

under a common scalar cost convention. Suppose valid joint certificates imply:

```text
candidate risk r_m in [0.06,0.09]
fallback cost r_F in [0.14,0.18].
```

Then:

```text
0.09 <= 0.10
0.09 + 0.02 <= 0.14.
```

So hard adequacy and fallback improvement are certified. If hard constraints, relative search admissibility, and provenance pass, the model receives a license.

If later evidence yields a valid risk region `[0.11,0.14]` for the same `q`, the new region lies entirely outside the scalar acceptable set `(-infinity,0.10]`. This is strong evidence defeat. If instead the original bound is invalidated by sample leakage and no replacement bound exists, the license lapses to `Withheld`; the model is not certified inadequate.

### 19.2 Two adequate models on the same domain

Let `m_1` and `m_2` both be certifiably adequate on `D`, and suppose `m_2` has lower certified predictive risk while `m_1` is cheaper and faster. Under prediction-only scalar dominance, `m_2` may defeat `m_1` for selection. Under a Pareto order over risk, latency, and cost, neither may dominate.

The active set can therefore be

```text
Active(x) = {m_1,m_2}
```

even if the selector chooses `m_2`. The library retains both model entries and both licenses. This is not inconsistency; adequacy is nonexclusive.

### 19.3 Overlap and gap

Suppose licensed point domains satisfy:

```text
x_A: Active(x_A) = {m_1}
x_B: Active(x_B) = {m_1,m_2}
x_C: Active(x_C) = {m_2}
x_D: Active(x_D) = empty.
```

At `x_B`, the selector applies its comparison rule without deleting either license. At `x_D`, `MustFallback(x_D)` holds. Choosing the larger raw neural score at `x_D` would violate the selector constraint because no model is licensed.

### 19.4 No explicit fallback

Suppose every adequacy and search certificate for `m` is favorable but the request uses

```text
F = NoFallback.
```

Then `CertAdeq(m;...)` may be granted, but the full `Lic(m;...)` request is `Undefined(MissingExplicitFallback)`. Replacing `NoFallback` with `Reject`, `Defer`, or a specified status quo makes the decision comparison inspectable.

### 19.5 Worst-case claim from an ordinary sample

Let `q_worst` require `WorstCase(carrier(D))`, but the record contains only a random sample and an empirical mean. `EmpAdeq` for the sample may obtain. `CertAdeq` for `q_worst` is withheld unless structural assumptions, exhaustive verification, or a valid bound connects the observed sample to worst-case risk. The mismatch is not repaired by increasing `alpha` numerically.

## 20. Elementary semantic consequences

### Proposition 1: tolerance monotonicity of target adequacy

If

```text
epsilon preceq_q epsilon'
```

then

```text
Adeq(m;q,epsilon) => Adeq(m;q,epsilon').
```

**Reason.** Since `preceq_q` is transitive and `A_q(epsilon)=Down_q(epsilon)`, `epsilon preceq_q epsilon'` already entails `A_q(epsilon) subseteq A_q(epsilon')`. Membership in the smaller acceptable down-set therefore implies membership in the larger one. For non-principal application-supplied acceptable sets, the inclusion must instead be stated explicitly.

Certificate monotonicity also holds for a fixed valid certificate and nested acceptable regions. It can fail operationally if changing `epsilon` triggers a different certificate protocol, fallback, or requirement profile.

### Proposition 2: nonexclusive adequacy

For distinct models `m_1` and `m_2`,

```text
Adeq(m_1;q,epsilon)
and Adeq(m_2;q,epsilon)
```

is satisfiable whenever both risks lie in the acceptable region. Therefore

```text
Adeq(m_1;q,epsilon) does not imply not Adeq(m_2;q,epsilon).
```

### Proposition 3: a full grant implies each component grant

By definition of `AllReq`,

```text
Lic(omega) =>
    CertAdeq(omega)
    and Improves(omega)
    and ConstraintOK(omega)
    and Admissible(omega)
    and TraceOK(omega).
```

The converse holds when every listed judgment is the required profile and the request is well formed.

### Proposition 4: comparative defeat need not defeat adequacy

There are finite-stage structures satisfying

```text
CertAdeq(m;q,epsilon,alpha|R')
and DefeatedByDominator(lic,m',q,K',sigma',R').
```

**Witness.** Let both models have certified risk below `epsilon`, with `m'` strictly better on every coordinate used by the admissibility order. The old model remains adequate while losing admissibility.

### Proposition 5: evidence invalidation need not certify inadequacy

There are updates satisfying

```text
LapsedByEvidence(lic,R,R')
and not CertInadeq(m;q,epsilon,alpha|R').
```

**Witness.** Invalidate the only supporting certificate because its sampling assumption fails, without introducing a valid lower bound or countercertificate outside the acceptable region.

### Proposition 6: safe selection abstains or falls back on gaps

For a selector satisfying the selector constraint and mandatory gap rule:

```text
Active(x)=empty => select(pi_sel,x) is not Use(m) for any m.
```

This follows immediately because `Use(m)` requires `m in Active(x)`.

## 21. What the semantics does not yet settle

Task 8 intentionally leaves the following to later tasks:

- the object-level consequence relation and quarantine of contradictory local conclusions (Task 9);
- exact update algorithms over records, domains, and license events (Task 9);
- the formal scalar/Pareto dominance relation, retention theorem, and distribution-aware domain splitting (Task 10);
- bridge composition and atlas coverage (Task 11);
- long-run stability, convergence, and non-finality (Tasks 12–14);
- representation proofs and objectives for the Task 16 hybrid approximation of certificate-relative statistics, margins, and routing components under the Task 15 external-checker boundary (Tasks 17–18).

Task 10 replaces the provisional `CertDominates` relation with typed scalar and Pareto definitions over eligible use plans. Task 11A then selects mandatory profile-indexed licensing: the full conjunction defined in this file is the named strong profile `P_full^8`, while other `Lic_P` profiles may omit required comparison closure. The core calculus must import the scoped dominance atom and the profile mapping rather than retain the placeholder or bare `Lic`.

## 22. Implications for neural representation

The finite-stage semantic target is not one Boolean label. At minimum a transparent implementation should expose:

```text
hard-adequacy status and certificate/margin
fallback-improvement status and certificate/margin
hard-constraint statuses
closure strength and evaluated search scope
certified dominator, if any
unresolved comparisons
provenance pointer
final operational status
selected or fallback action.
```

For a scalar hard-risk condition with valid upper bound `U`, the signed margin

```text
s_hard = epsilon - U
```

is positive exactly when the sufficient certificate condition is strict. At equality, inclusive certification obtains but `ReLU(s_hard)>0` does not. The signed comparison remains authoritative.

For fallback improvement:

```text
s_F = L_F - U_m - Delta.
```

For library admissibility, a family of pairwise or Pareto margins may be required; one scalar can hide which competitor or coordinate caused defeat. The final ReLU license gate must not erase the four operational statuses or their reasons.

## 23. Decisions fixed here

1. Target adequacy, empirical adequacy, and certified adequacy are different judgments.
2. Certification is mode-specific; frequentist confidence, Bayesian posterior support, deterministic proof, conformal coverage, and empirical-only assessment are not interchangeable.
3. A valid certificate must name its target, assumptions, evidence view, procedure, and provenance.
4. Non-grants are operationally divided into `Refused`, `Withheld`, and `Undefined`.
5. The full license form defined in this Task 8 artifact requires hard adequacy, explicit fallback improvement, hard-constraint compliance, search-relative admissibility, and provenance. Task 11A reindexes it as named profile `P_full^8`; it is not the universal meaning of every `Lic_P`.
6. Every full use-license requires an explicit fallback; `NoFallback` is allowed only for adequacy-only judgments.
7. The default search closure is relative to the models actually and validly evaluated; stronger declared-library closure must resolve omissions and failures.
8. No finite ordinary search trace licenses a global best-model claim.
9. Empty active sets force a fallback/abstention route rather than an argmax among unlicensed models.
10. New evidence can strongly rebut a requirement or merely invalidate its certificate; refusal and lapse are different.
11. A newly found dominator defeats library admissibility without automatically defeating hard adequacy or archival retention.
12. License history is retained as versioned events; current licenses are a derived view.

## 24. Open questions recorded for Tasks 9–10

1. Which nonmonotonic consequence properties should license consequence satisfy: cautious monotony, cut, rational monotony, or weaker labeled variants?
2. Should unknown pairwise comparisons permit a relative admissibility grant by default, as specified here, or should the core calculus offer both permissive and conservative profiles?
3. What evidence relation is sufficient for a later record to count as an extension rather than a new branch or corrected history?
4. How should conflicting valid certificates from different protocols be compared or retained?
5. Which hard constraints belong inside `CertAdeq` versus the separate `ConstraintOK` component?
6. Under what measure-reconstruction rule can a distributional domain be split after partial domination?
7. Which fallback decisions themselves require a license, especially an automated status-quo model that can also fail?
8. Should expiry be primitive, or derived from explicit review conditions and changed records?

## Task conclusion

The finite-stage semantics now separates the world-level performance target from what a bounded agent can establish. Empirical adequacy concerns a recorded finite evaluation; certified adequacy concerns a valid mode-specific certificate; and the full use-license additionally requires an explicit fallback comparison, hard constraints, bounded search-relative admissibility, and provenance. A non-grant can be a certified refusal, an evidential withholding, or an ill-typed request. New evidence can rebut or merely invalidate a license, while a newly retrieved dominator can defeat current admissibility without making the older model inadequate. This supplies the semantic object needed for Task 9's consequence and update rules without asserting that the licensed model is true or final.
