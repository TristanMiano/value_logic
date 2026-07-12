# Labeled Consequence and Finite-Stage Update

Status: Task 9 formalism  
Date: 2026-07-11  
Depends on: [`01_signature.md`](01_signature.md), [`02_license_semantics.md`](02_license_semantics.md)  
Scope: what follows from licenses, local object-level reasoning, contradiction quarantine, record heredity, and revision

## Executive definition

The logic has three distinct consequence relations:

```text
Gamma |-^obj_chi phi
Gamma |-^lic_S J
Gamma |~_{a,t} J.
```

- `|-^obj_chi` is the object logic declared by one model/theory context `chi`. It may be classical.
- `|-^lic_S` is monotone derivability from explicit, typed premises inside one fixed finite-stage structure `S`.
- `|~_{a,t}` is current defeasible consequence: it first selects the licenses and evidence that remain active at `(a,t)`, then applies `|-^lic_{S_{a,t}}`.

The principal use rule is **labeled detachment**:

```text
current license for m on q
+ a permitted local output or derivation phi
+ a case and purpose covered by that license
------------------------------------------------
MayRely(a,t,chi,phi).
```

It does **not** erase the label and conclude bare `phi`. A license warrants reliance on a model output under a stated scope; it does not turn the output into an unindexed truth of the metalanguage.

Revision is a transition between finite structures:

```text
S_{a,t} --u--> S_{a,t'}.
```

Raw history is normally append-only along a lineage, but admissible evidence, valid certificates, current licenses, and selections are derived views and may change nonmonotonically. Updates are recomputed in strata:

```text
raw events
  -> admissible evidence views
  -> certificates and component assessments
  -> full licenses
  -> active sets, selectors, and fallback.
```

Contradictions are quarantined by model, version, frame, task, domain, purpose, and stage labels. Two models may license incompatible outputs on an overlap without licensing arbitrary conclusions. Cross-label transport requires an explicit restriction, bridge, equivalence, or aggregation witness.

## 1. Judgment contexts and labeled formulas

### 1.1 Object context

An object context is the typed record

```text
chi = <
    model_ref,
    model_version,
    theory_ref,
    frame,
    task,
    domain_ref,
    domain_version,
    purpose,
    admissible_record_view
>.
```

Write

```text
[chi] phi
```

for the statement that `phi` is an object-level formula, prediction, equation, or derived output in context `chi`. The brackets are not a truth modality. They preserve the source and scope of the content.

At minimum, well-formedness requires:

1. `phi` belongs to the language declared by `theory_ref` and `task`;
2. the model version supports the task/output interface;
3. `frame` supplies the units, coordinates, and decoding used by `phi`;
4. `domain_ref` and its version make the intended cases meaningful;
5. the record view and provenance identify the assumptions or inputs used.

### 1.2 License context

A full license request remains the immutable record

```text
omega = <a,t,b,m,q,epsilon,alpha,F,Delta,K,c,sigma,p,R>.
```

Its grant event is referenced by `lic`. The request fields are not silently edited. A changed model version, domain, loss, risk aggregator, tolerance, certificate convention, fallback, cost profile, search, purpose, or provenance creates a new request linked to the old one.

Because `t`, `R`, and normally `K`, `sigma`, and `p` are stage-indexed, current reassessment at a child stage uses a successor request:

```text
omega' = Succ_u(omega).
```

`Succ_u(omega)` has a new request identity, points back to `omega`, replaces the stage-bound references with their child-stage versions, and records exactly which substantive fields were inherited or revised. When this document says that a license “persists,” it means that `Succ_u(omega)` is granted with the same substantive reliance profile; it never means that the old event or request was mutated.

### 1.3 Reliance judgments

The central derived judgment is

```text
MayRely(a,t,lic,chi,phi).
```

It means that the current system authorizes agent `a`, at stage `t`, to use the `chi`-indexed content `phi` for the purpose covered by `lic`. It does not mean:

```text
phi is globally true
phi is error-free on every case
m is a true or final theory
all other licensed models agree with phi.
```

For executable prediction, it is often clearer to use:

```text
LicensedOutput(a,t,lic,x,m(x)).
```

This records the authorized output without asserting that `m(x)` equals the eventual observed outcome.

### 1.4 Status judgments are not Boolean negations

For a well-formed request `omega`, the status facts

```text
Granted(omega)
Refused(omega,r)
Withheld(omega,r)
Undefined(omega,r)
```

are tagged alternatives returned by `AssessLic`. `Withheld(omega,r)` is not `not Granted(omega)` inside a two-valued object theory, and it is not `Refused(omega,r)`. Operational code may test status equality, but logical rules must preserve the tag and reason.

## 2. Three consequence relations

### 2.1 Model-local object consequence

```text
Gamma |-^obj_chi phi
```

means that `phi` follows from object premises `Gamma` according to the proof/evaluation rules declared by context `chi`.

The default paper fragment permits ordinary typed classical reasoning inside a fixed context:

- identity and substitution within one frame and type;
- propositional introduction and elimination rules;
- first-order rules when the model language supplies quantifiers and a domain of interpretation;
- algebraic, probabilistic, or numerical rules supplied by the model;
- model-specific approximation rules whose error terms remain explicit.

This relation is local. It does not itself issue a use-license, validate empirical assumptions, certify a risk bound, or transport a formula to a different model, frame, task, or domain.

If a model's declared object logic is nonclassical, `|-^obj_chi` delegates to that logic. If it is classical but locally inconsistent, classical explosion remains confined to `[chi]` formulas. Exporting such derivations through `MayRely` should be refused or withheld whenever the license profile requires a consistency or nontriviality constraint. The core calculus does not pretend every scientific model is a consistent first-order theory.

### 2.2 Fixed-stage license consequence

```text
Gamma |-^lic_S J
```

is the smallest typed relation closed under the rules in Sections 3–5, with structure `S` held fixed. `Gamma` may contain:

- explicit status and grant records;
- labeled object formulas and derivations;
- membership/coverage evidence;
- bridge or transport witnesses;
- selector and fallback specifications;
- provenance facts.

Because `S` is fixed, adding an explicit premise to `Gamma` does not remove an earlier derivation. Thus `|-^lic_S` is monotone in its premise set. It is deliberately weaker than unrestricted classical consequence over untyped, unlabeled formulas.

### 2.3 Current defeasible consequence

Let

```text
Base_{a,t}
  = CurrentLicenses(R_{a,t})
    union CurrentAdmissibleFacts(S_{a,t})
    union CurrentTransportWitnesses(S_{a,t}).
```

Define

```text
Gamma |~_{a,t} J
```

iff

```text
Base_{a,t} union Gamma |-^lic_{S_{a,t}} J.
```

`|~_{a,t}` can lose conclusions when the stage changes because `Base_{a,t}` is recomputed. This is where nonmonotonicity lives. It is not produced by making ordinary deduction capricious.

### 2.4 Historical consequence

Historical evaluation uses the structure stored at the issuance stage:

```text
Gamma |~^{hist}_{a,t,lic} J.
```

This freezes the record view, procedures, library/search scope, and request fields referenced by `lic`. Later defeat does not make a correctly reconstructed historical derivation disappear. It changes current consequence at `t'`.

## 3. What follows from a full license

Let `lic` be a current granted license for request `omega`.

### 3.1 Component projection

The full grant supports:

```text
Lic(omega)
------------------------------ Lic-Elim
CertAdeq(m;q,epsilon,alpha|R)
CertImprove(m;F,q,Delta,alpha|R)
ConstraintOK(m;c,q|R)
SearchAdmissible(m;q,K,sigma,c|R)
TraceOK(omega).
```

Each conclusion retains the exact indices and certificate/provenance references stored in `lic`.

The converse is permitted only when the listed judgments constitute the complete requirement profile for the same well-formed request. Components from different model, domain, loss, stage, or record versions may not be spliced together.

### 3.2 Current eligibility

```text
lic in CurrentLicenses(R_{a,t})
-------------------------------- Current
CurrentlyEligible(a,t,lic).
```

Eligibility means the model may enter the active set for covered cases. It does not mean the selector must choose it.

### 3.3 Case application

Let `q=EvalSpec(D,L,rho)`. Then:

```text
CurrentlyEligible(a,t,lic)
CoveredCase(x,D,purpose)
Executable(m,x,task(q),frame(D))
--------------------------------------------- Lic-Apply
MayUse(a,t,lic,m,x,purpose).
```

`CoveredCase` is stronger than raw set membership when the license depends on distributional, temporal, intervention, or history conditions. It checks the deployment conditions recorded by the request.

This rule applies a domain-level permission to a case in its intended deployment scope. It does not derive a new singleton-domain risk certificate.

### 3.4 Labeled detachment

```text
MayUse(a,t,lic,m,x,purpose)
Gamma |-^obj_chi phi
PermittedContent(lic,chi,phi)
--------------------------------------------- Lic-Detach
MayRely(a,t,lic,chi,phi).
```

`PermittedContent` checks that the task, frame, model version, purpose, and output kind in `chi` match the license. If `phi` depends on inputs outside the certified scope, the rule is undefined or withheld rather than coerced.

There is intentionally no rule:

```text
MayRely(a,t,lic,chi,phi) / phi.
```

### 3.5 Active-set formation

For point request context `zeta_x`, derive:

```text
Active_{a,t}(x,zeta_x)
  = {m : some current lic for m covers zeta_x}.
```

Multiple members are allowed. A set of licenses therefore entails an active set, not a unique winner.

### 3.6 Selection

```text
m in Active_{a,t}(x,zeta_x)
SelectorChooses(pi_sel,m,x,zeta_x)
SelectorConstraintsSatisfied(pi_sel,x,zeta_x)
------------------------------------------------ Select
Selected(a,t,pi_sel,m,x,zeta_x).
```

Selection is not logical proof of superiority unless the selector and the license profile explicitly encode and certify that comparison.

### 3.7 Gap and fallback

```text
Active_{a,t}(x,zeta_x) = empty
Fallback(omega)=F
Executable(F,x,zeta_x)
---------------------------------------------- Gap
MustUseFallbackOrAbstain(a,t,F,x,zeta_x).
```

No rule promotes the highest raw neural score when every candidate is unlicensed.

## 4. What does not follow from licenses

Even a nonempty set `Lambda` of full grants does not by itself entail:

```text
TrueTheory(m)
Final(m)
BestPossible(m)
Correct(m,x)
Lic(m;q',...) for q' != q
Lic(m;union(D,E),...)
Lic(m;intersect(D,E),...)
Lic(m;PointDomain(x),...)
not Lic(m';q,...) for m' != m
a unique selected model
agreement among all licensed models.
```

The domain non-inferences are important. Expected adequacy on `D` need not survive conditioning on a difficult subset; adequacy on two domains need not survive their union under a different mixture; a worst-case claim may restrict safely only when the carrier and assumptions genuinely nest. Each such transport requires a rule appropriate to `rho`.

## 5. Scope transport and contradiction quarantine

### 5.1 Transport witness

A transport witness is a typed record

```text
w : Transport(chi,chi') = <
    source_context,
    target_context,
    kind,
    assumptions,
    formula_map,
    risk_or_error_map?,
    validity_certificate,
    provenance
>.
```

Kinds include:

```text
SameContext
ModelEquivalence
FrameTranslation
DomainRestriction
DomainExtension
BridgeTransport
DecisionEquivalence
ApproximateTransport(delta).
```

The transport rule is:

```text
[chi] phi
w : Transport(chi,chi')
ValidTransport(w,phi,S)
---------------------------------------------- Transport
[chi'] map_w(phi).
```

Approximate transport preserves its error term. It cannot silently produce an exact formula.

### 5.2 Domain restriction is risk-specific

Set inclusion alone does not validate a license restriction:

```text
D' subseteq D
not sufficient for
Lic(m;Eval(D,L,ExpectedRisk),epsilon) ->
Lic(m;Eval(D',L,ExpectedRisk),epsilon).
```

The conditional distribution on `D'` may concentrate failures. A valid `DomainRestriction` witness must reconstruct every view required by `rho` and certify the transported risk claim.

For a uniform worst-case certificate over carrier `D`, restriction to a compatible `D' subseteq D` may be valid because

```text
sup_{x in D'} L(m,x) <= sup_{x in D} L(m,x),
```

provided frames, tasks, conditions, and certificate assumptions are preserved. The witness records that theorem.

### 5.3 Labeled contradiction

Suppose:

```text
[chi_1] phi
[chi_2] not phi.
```

They are a direct contradiction only if a certified equivalence identifies the model language, version, frame, task, domain conditions, referents, and relevant stage of `chi_1` and `chi_2`. Ordinary overlap of domain carriers is insufficient.

Without such equivalence, record:

```text
Disagreement(chi_1,chi_2,phi,overlap).
```

Disagreement is useful diagnostic information, not an explosion rule.

### 5.4 Quarantined explosion

The license language has no rule

```text
[chi_1] phi, [chi_2] not phi |-^lic_S J
```

for arbitrary `J`. If `chi_1=chi_2` and the local logic is classical, object-level explosion is possible only inside `[chi_1]`. Stripping the label still requires a forbidden truth-detachment rule; exporting a local derivation requires `PermittedContent` and any required nontriviality constraint.

### 5.5 Decision conflict on an overlap

Two current licenses can recommend incompatible actions on a common case. Then derive:

```text
DecisionConflict(x,lic_1,lic_2,actions).
```

The conflict must be resolved by an explicit selector, dominance rule, arbitration policy, information-gathering action, or fallback. The logic does not obtain every action, and it does not revoke either license merely because both are active.

### 5.6 Status consistency

Because `AssessLic_S(omega)` is a function, one fixed well-formed request in one fixed structure has exactly one top-level status. Thus the system cannot currently derive both

```text
Granted(omega)
Refused(omega,r)
```

for the same `S` and exact request identity. Apparent examples almost always differ by stage, domain version, tolerance, record view, or requirement profile.

## 6. Structural properties of consequence

### 6.1 Properties retained at a fixed stage

For well-typed premises and fixed `S`, `|-^lic_S` satisfies:

1. **Typed reflexivity:** if `J in Gamma`, then `Gamma |-^lic_S J`.
2. **Premise monotonicity:** if `Gamma subseteq Delta` and `Gamma |-^lic_S J`, then `Delta |-^lic_S J`.
3. **Cut:** if `Gamma |-^lic_S J` and `Gamma union {J} |-^lic_S H`, then `Gamma |-^lic_S H`.
4. **Label-preserving right weakening:** if `phi |-^obj_chi psi`, a licensed reliance on `[chi]phi` supports reliance on `[chi]psi` only when the license permits that inference/output kind.
5. **Typed left equivalence:** interchangeable premises require a proved equivalence preserving types, context labels, and provenance-relevant content.

These are properties of the explicit closure rules, not claims that any new observation can be added without changing current licenses.

### 6.2 Failure of unrestricted monotonicity across stages

In general:

```text
Gamma |~_{a,t} J
and Raw(R_{a,t}) subseteq Raw(R_{a,t'})
```

does not imply

```text
Gamma |~_{a,t'} J.
```

The later raw record may contain a correction, countercertificate, domain-shift event, or dominator that changes the admissible base.

### 6.3 Conservative cautious monotony

Define `u` to be **conservative for request `omega`** when:

1. it does not change any request field;
2. it does not add, correct, retract, or invalidate a dependency of `omega`;
3. it does not change a certificate procedure or assumption used by `omega`;
4. it does not expand a comparison/search scope relevant to `omega`;
5. it does not invalidate a transport or provenance edge used by `omega`.

Then current consequences of `omega` persist across `u`. Adding a consequence already derivable from `omega` as a non-authoritative annotation is conservative and therefore supports a restricted cautious-monotony principle.

### 6.4 Rational monotony is not valid in general

An update can leave `not J` uncertified while still removing `J`: invalidating the only sampling assumption supporting `J` yields `Withheld`, not a certified negation. Likewise, a newly found competitor can remove admissibility without refuting adequacy. Therefore the unqualified KLM-style inference “retain `J` whenever its negation is not derived” is invalid for this calculus.

### 6.5 Why the calculus is not simply AGM

The state is not one deductively closed belief set. It contains raw history, admissible evidence views, model-local theories, certificates, libraries, searches, licenses, and selections. Retraction can remove an event from an admissible view while retaining it in history; a model can lose selection while remaining adequate and archived. AGM-style revision remains a useful comparison, but identifying record inclusion with belief inclusion would erase the project's main distinctions.

## 7. Stage transitions

### 7.1 Update object

An update is a typed record

```text
u : Update = <
    update_id,
    actor,
    parent_stage_refs,
    kind,
    payload,
    declared_targets,
    validation_protocol,
    provenance
>.
```

Update kinds include:

```text
Observe
Evaluate
Correct
Retract
AddModel
VersionModel
RunSearch
ReviseDomain
ReviseTolerance
ReviseCertSpec
ReviseFallback
ReviseCostOrPurpose
RepairProvenance
MergeBranches
IssueOrWithdrawLicense.
```

Derived license events are recorded for audit, but their status is determined by the semantic assessment rather than by an unchecked assertion in the payload.

### 7.2 Transition relation

```text
S_{a,t} --u--> S_{a,t'}
```

holds only if:

1. `u` is well typed and authorized under the declared protocol;
2. every parent stage exists and its record identity is preserved;
3. primary events are appended or linked, not silently overwritten;
4. corrections/retractions target existing versioned events;
5. affected derived objects are recomputed by the stratified procedure below;
6. the new provenance graph records the transition and all status changes.

The relation may branch: two agents or protocols can produce different children of one stage.

### 7.3 Raw record lineage

For a non-merge child, define:

```text
R <=_raw R'
```

iff every event identifier and dependency edge in `Raw(R)` remains reachable in `Raw(R')`, with the same payload and identity. A correction adds a new event and a correction link; it does not mutate the target event.

For merges, both parents embed into the child raw history:

```text
R_1 <=_raw R'
and R_2 <=_raw R'.
```

Raw heredity is a lineage property, not a claim that all old events remain admissible.

### 7.4 Admissible-view revision

For protocol `alpha` and evaluation specification `q`, the derived view

```text
Adm(R,alpha,q) = Admissible(R,alpha,q)
```

may grow or shrink:

```text
Adm(R,alpha,q) not subseteq Adm(R',alpha,q)
Adm(R',alpha,q) not subseteq Adm(R,alpha,q).
```

A correction can exclude an old evaluation and include its replacement. A newly verified source can make an old raw event newly admissible. Both occur while `R <=_raw R'`.

## 8. Stratified recomputation

### 8.1 Dependency strata

The derived state is stratified:

```text
Stratum 0: versioned primary events and registry objects
Stratum 1: admissible evidence views and valid provenance paths
Stratum 2: empirical results, certificates, comparisons, and constraints
Stratum 3: component statuses and full license statuses
Stratum 4: active sets, selection, abstention, and fallback decisions.
```

Edges point from lower to higher strata. Audit events describing a derived result do not feed back as substantive evidence merely because they were logged. This prevents self-supporting license cycles.

### 8.2 Impact cone

Let `Targets(u)` contain the primary objects changed by `u`. Define:

```text
Impact(u,S)
  = Targets(u)
    union Descendants_{ProvGraph_S}(Targets(u))
    union GlobalComparativeImpact(u,S).
```

`GlobalComparativeImpact` widens the cone when an update changes a library, search scope, dominance coordinate, or selector shared by many requests. For example, adding one newly evaluable model can affect the admissibility of every comparable current model even if it does not affect their adequacy certificates.

### 8.3 Transaction

`Apply(S,u)` performs:

1. **Normalize:** resolve exact versioned targets and request identities.
2. **Type-check:** reject malformed payloads without changing the current stage.
3. **Append:** construct the child raw record and registry versions.
4. **Resolve views:** recompute correction, retraction, authorization, and admissibility policies at Stratum 1.
5. **Compute impact:** form `Impact(u,S)` and include all dependent requests.
6. **Invalidate:** mark affected derived objects stale before reuse.
7. **Recompute:** evaluate affected strata in order, using unchanged cached objects only outside the impact cone.
8. **Emit transitions:** append typed grant, refusal, withholding, lapse, restriction, and supersession audit events.
9. **Validate trace:** ensure each current result points only to current or explicitly frozen historical dependencies.
10. **Publish view:** compute `CurrentLicenses`, active sets, selections, and fallbacks.

Because every finite stage has finitely represented records and dependencies, this transaction is finite provided each declared certificate/search procedure terminates or returns a recorded timeout. A timeout yields `Withheld` where required; it is not evidence of failure.

### 8.4 Frame rule for unaffected licenses

If request `omega` and every dependency of its grant lie outside `Impact(u,S)`, and `u` does not change any shared comparative scope or selector required by `omega`, then the child reuses the same component certificates and derives the same license status with a provenance link:

```text
omega' = Succ_u(omega)
UnchangedBy(lic,omega',u).
```

This is the update analogue of a separation/frame rule. It prevents irrelevant evidence from defeating unrelated licenses.

## 9. Evidence updates

### 9.1 New observation or evaluation

Appending new compatible data does not automatically preserve or defeat a license. The result depends on the certificate protocol:

- a sequentially valid procedure may update its bound directly;
- a fixed-sample certificate may remain a frozen historical certificate but require a new request/procedure to incorporate the data;
- optional stopping or adaptive reuse can invalidate a procedure if its assumptions did not permit them;
- evidence outside the domain is retained but irrelevant unless a transport or domain-revision rule connects it.

After recomputation:

```text
supporting certificate valid and all components pass -> Granted
valid countercertificate violates a requirement       -> Refused
support invalid/straddling and no countercertificate  -> Withheld
typing/frame failure                                  -> Undefined.
```

### 9.2 Correction and retraction

For

```text
Correction(e,e')
```

the raw view contains both events. The admissible view applies the declared conflict policy, normally excluding `e` as authoritative and admitting `e'` if validated. All certificates and licenses descending from `e` enter the impact cone.

For

```text
Retraction(e,reason)
```

the default result is loss of support, not evidence for the opposite claim. Hence descendants usually lapse to `Withheld`. They become `Refused` only if remaining or replacement evidence supplies a valid countercertificate.

### 9.3 Evidence conflict without a resolution policy

If two admissible sources conflict and the certificate procedure has no declared robust combination or priority rule, the system returns `Withheld(UnresolvedEvidenceConflict)`. It must not choose whichever source favors the current model.

### 9.4 Distribution or condition shift

A detected shift can have three effects:

1. the old license remains current for its unchanged historical deployment scope;
2. applying it to the shifted scope is `Undefined` or `Withheld` pending a new domain/request;
3. if the old request explicitly required stationarity and the shift invalidates that requirement for ongoing use, the current old license lapses.

Shift alone does not certify the model inadequate on either the old or new domain.

## 10. Library and search updates

### 10.1 Adding a model

`AddModel(m')` changes the registry but does not by itself defeat anything. `m'` must be retrieved, validly evaluated on a comparable specification, and included in the relevant search closure.

The update can therefore progress through:

```text
known but unevaluated
-> evaluated but incomparable
-> comparable and nondominating
-> certified dominator.
```

Only the last state refuses the older model's admissibility component under the corresponding order.

### 10.2 Search expansion

When `sigma'` extends the evaluated scope of `sigma`, old relative closure remains a correct historical claim about `Evaluated(sigma,q)`. The current admissibility request is reassessed against `sigma'` only if its request or standing review policy names the expanded scope.

Failures and timeouts produce diagnostic events and may withhold declared-library closure. They never count as comparisons won by the incumbent.

### 10.3 Comparative versus evidential impact

A new dominator normally changes:

```text
SearchAdmissible
CurrentLicenses under a full profile
selection and routing.
```

It does not automatically change:

```text
Adeq
CertAdeq
the older model's stored evaluation
historical grant validity
registry retention.
```

Exact Pareto, cost, robustness, and partial-domain rules are deferred to Task 10.

## 11. Domain updates

### 11.1 Immutable domain versions

```text
DomainRevised(D_v,D_{v+1},reason)
```

creates a new domain record. Licenses referring to `D_v` retain that identity. A current deployment configured to follow “latest domain version” must generate and assess a new request for `D_{v+1}`.

### 11.2 Restriction

From a license on `D`, a license on `D'` is derivable only with a valid risk-specific `DomainRestriction` witness. If the witness reconstructs the necessary carrier, measure/sampler, conditions, frame, certificate, fallback comparison, and provenance, the new request can reuse transported components. Otherwise it is withheld pending evaluation.

### 11.3 Expansion

Domain expansion is never inferred merely from good performance on `D`. A new region can change expected, tail, or worst-case risk. Expansion requires new evidence or a certified structural transport theorem.

### 11.4 Split

A proposed split

```text
D -> <D_keep,D_defeated,D_overlap_or_boundary?>
```

creates candidate domain versions and dependency links. No child license is current until each child's required domain views, measures, certificates, fallbacks, and provenance are constructed. Task 10 will specify when partial domination justifies the split and which pieces retain a model.

### 11.5 Overlap

Adding an overlapping domain does not modify either domain into a disjoint tile. It creates additional contexts and possibly an active-set cell. Conflicting outputs on the overlap invoke disagreement or decision-conflict rules, not set subtraction by default.

## 12. Tolerance, confidence, fallback, cost, and purpose updates

### 12.1 Tolerance revision

Changing `epsilon` creates a new request. Let acceptable regions satisfy

```text
A_q(epsilon) subseteq A_q(epsilon').
```

Then any valid certificate region that supported adequacy at `epsilon` also supports adequacy at the looser `epsilon'`. The adequacy component may be transported with a provenance link. The full new license still rechecks fallback improvement, constraints, search admissibility, and trace requirements.

Tightening the tolerance has no analogous preservation rule. It may grant, withhold, or refuse depending on the existing certificate.

### 12.2 Confidence/certification revision

A change from `alpha` to `alpha'` is meaningful only within a named certificate family. A bound at 95% confidence does not become a 99% bound by relabeling. Reuse requires a nesting or conversion theorem supplied by the procedure. Frequentist, Bayesian, and conformal interpretations cannot be converted by numerical comparison alone.

### 12.3 Fallback revision

A new fallback changes both the comparison target and often the induced tolerance. The old hard adequacy certificate may remain reusable if `q` and `epsilon` are unchanged, but `CertImprove` must be recomputed. “Do nothing” and “status quo” remain explicit executable policies with costs and outcomes.

### 12.4 Cost or purpose revision

Changing latency, resource, safety, interpretability, or purpose coordinates can revive a retained model or defeat a selected one without changing predictive risk. These are new admissibility requests, not new facts about the old model's truth.

### 12.5 Expiry

Expiry is derived from explicit validity/review conditions, such as:

```text
valid_until_time
valid_until_n_uses
valid_while_stationary(test)
review_on_library_change
review_on_domain_version_change.
```

Crossing a declared condition invalidates the current certificate or license and normally yields `Withheld(Expired)` pending renewal. There is no unexplained primitive “become false with age” operator.

## 13. Provenance updates

### 13.1 Broken provenance

If a required provenance node or edge is shown to refer to the wrong model version, data, code, domain, or procedure, every dependent certificate enters the impact cone. Lack of a replacement trace yields `Withheld(BrokenProvenance)`; a substantive countercertificate is still required for `Refused`.

### 13.2 Repair

`RepairProvenance(p,p')` may reconnect an unchanged substantive result to its actual dependencies. Reinstatement is allowed only after:

1. the repaired graph is valid and acyclic under the chosen representation;
2. the artifacts match the request versions;
3. certificate assumptions remain satisfied;
4. no intervening evidence or competitor defeats another component.

The new grant points to the repair and the former lapse. It does not rewrite the historical gap as though it never occurred.

### 13.3 Model and code version changes

A code fix or parameter change creates a new model/evaluator version. Results are not inherited unless a reproducibility or behavioral-equivalence certificate establishes the relevant equivalence. A filename staying the same is not version identity.

## 14. Branches and merges

### 14.1 Branching inquiry

Two child stages can apply different admissibility protocols, domain hypotheses, or corrections to the same parent:

```text
             S_t
            /   \
       S_{t+1}^A S_{t+1}^B.
```

Each branch has its own current consequences. Neither branch is silently treated as the unique true continuation.

### 14.2 Merge is not union of beliefs

A merge stage retains both raw histories but recomputes admissible views under an explicit merge protocol:

```text
Merge(S^A,S^B,mu) = S^M.
```

The current licenses of `S^M` are not generally

```text
CurrentLicenses(S^A) union CurrentLicenses(S^B).
```

The branches may contain incompatible corrections, duplicate data, dependent samples, different model versions, or certificate conventions. `mu` must resolve identity, duplication, authority, and conflict before certificates are rebuilt.

### 14.3 Unresolved merge

If the merge protocol cannot resolve a dependency needed by a request, that request is withheld in the merged stage. Other requests outside the conflict cone may survive by the frame rule.

## 15. License lifecycle

### 15.1 Immutable events, changing current view

A license event can have the lifecycle links

```text
issued
-> renewed
-> restricted
-> lapsed
-> rebutted
-> superseded_for_selection
-> reinstated.
```

These are not mutually exclusive historical descriptions. For example, a license can be adequate, superseded for selection, later relevant under a new cost profile, and reissued for a restricted domain.

### 15.2 Status transition table

| Update result | Later operational status | Historical grant retained? | Certified inadequacy? |
|---|---|---:|---:|
| supporting evidence remains valid | `Granted` | yes | no |
| valid countercertificate violates a required condition | `Refused` | yes | possibly, if adequacy is the violated component |
| support invalid or expired, no countercertificate | `Withheld` | yes | no |
| request becomes ill typed for attempted new scope | `Undefined` | yes | no |
| certified dominator defeats full-profile admissibility | `Refused(CertifiedDominatorFound)` | yes | no |
| irrelevant update outside dependency/comparison cone | unchanged | yes | no |

### 15.3 Withdrawal versus semantic defeat

An authorized human or governance process may append `LicenseWithdrawn(lic,reason)`. This removes current authorization under that governance protocol. It is distinct from a semantic countercertificate. The trace must say whether withdrawal was evidential, comparative, precautionary, legal, or administrative.

## 16. Worked examples

### 16.1 Correction without certified falsification

At `t`, classifier `m` has a valid upper risk bound `0.08`, tolerance `0.10`, and a granted license. At `t+1`, an audit finds train/test leakage in the evaluation event. The raw record retains the original evaluation and appends the audit/correction.

The original certificate is now invalid, but suppose no valid lower bound exceeds `0.10`. Then:

```text
Raw(R_t) subset Raw(R_{t+1})
Lic_t(m) was historically granted
CurrentStatus_{t+1}(m) = Withheld(BrokenAssumption)
not CertInadeq_{t+1}(m).
```

This is record heredity without belief/license monotonicity.

### 16.2 New evidence strongly rebuts adequacy

If the corrected evaluation instead yields a valid risk region `[0.13,0.16]`, entirely outside `(-infinity,0.10]`, the later request is `Refused(HardRiskViolation)`. The historical grant remains reconstructible from its old stage, but current reliance is defeated by a countercertificate.

### 16.3 Contradictory licensed outputs on an overlap

Models `m_1` and `m_2` are both adequate for a noisy classification task on overlapping domains. At case `x` both licenses cover the deployment conditions, but:

```text
[chi_1] class(x)=A
[chi_2] class(x)=B.
```

The calculus derives two `LicensedOutput` judgments and `DecisionConflict`. It does not derive both bare class facts, revoke both models, or permit an arbitrary class. A selector may use certified comparative margins, gather more information, or defer.

### 16.4 Expected-risk restriction failure

Model `m` has expected loss `0.02` on a population where a rare subgroup `D_bad` has loss `0.40`. A license on the population does not entail a license on the subgroup even though `D_bad subset D`. Conditioning changes the measure and risk. A request for `D_bad` is refused or withheld according to its own certificate.

### 16.5 Looser tolerance

A valid certificate region `[0.06,0.08]` supports tolerance `0.10`. It also supports the looser tolerance `0.12` under the same risk order. The system issues a linked new adequacy judgment rather than mutating the old request. If the fallback or safety constraints changed at the same time, those components are reassessed independently.

### 16.6 Newly discovered cheaper model

An older model remains below the hard error tolerance. A new model has indistinguishable certified risk but much lower deployment cost and certifiably dominates under the current full resource order. The older full use-license loses admissibility, but its adequacy certificate and registry entry survive. A later offline or low-data purpose may license it again under a different cost/purpose profile.

### 16.7 Branch merge with duplicated data

Branches `A` and `B` each evaluate models on datasets that partially share examples. Simply pooling the certificates would double-count evidence. The merge retains both raw event histories, detects shared sample provenance, and withholds the merged certificate until a dependence-aware procedure is applied. Licenses for an unrelated simulator remain current by the frame rule.

This does not automatically invalidate either branch certificate considered under its frozen branch record. It blocks only an unsupported merged certificate or any merged-stage request whose protocol requires pooling the two sources.

## 17. Elementary results

### Proposition 1: fixed-stage status functionality

For a fixed structure `S` and exact request `omega`, there do not exist reasons `r_1,r_2` such that both

```text
AssessLic_S(omega)=Granted
and AssessLic_S(omega)=Refused(r_1)
```

or any other two distinct top-level status tags obtain.

**Proof.** `AssessLic_S` is defined as a function into the tagged sum `Status`, and `AllReq` uses a deterministic precedence rule. Distinct tags are disjoint constructors. Apparent counterexamples use different request identities or structures. `square`

### Proposition 2: raw heredity does not imply current-license monotonicity

There exist `S --u--> S'` with `R <=_raw R'` and a request `omega` such that

```text
S |= Lic(omega)
but S' not|= Lic(omega_current_view).
```

**Proof.** Append a validated retraction of the only event supporting the adequacy certificate. Raw heredity holds because both the original event and retraction remain. The admissible view excludes the original event as authoritative; without replacement support, `AssessCertAdeq` is withheld, so the full license is not current. `square`

### Proposition 3: labeled disagreement is non-explosive

Let `chi_1` and `chi_2` be non-equivalent contexts. For arbitrary well-formed `J` not otherwise derivable,

```text
{[chi_1]phi, [chi_2]not phi} not|-^lic_S J.
```

**Proof.** No license-consequence rule has differently labeled disagreement as premises and arbitrary `J` as conclusion. The only applicable rule records `Disagreement` or, with action incompatibility, `DecisionConflict`. Object-level explosion, if available, requires one fixed context and cannot erase its label. `square`

### Proposition 4: conservative-update persistence

If `S --u--> S'`, `u` is conservative for request `omega`, and `S |= Lic(omega)`, then `S' |= Lic(Succ_u(omega))` for the successor request with the same substantive reliance profile.

**Proof.** Conservativeness excludes changes to every substantive request field, supporting dependency, certificate assumption, comparative scope, transport, and provenance edge. Hence the old grant's dependencies lie outside `Impact(u,S)`. The frame rule reuses every component result for `Succ_u(omega)`, updates only the required stage-bound references, and deterministic `AllReq` returns a grant with a transition provenance link. `square`

### Proposition 5: adequacy transports to a looser acceptable region

Suppose a valid certificate `kappa` satisfies

```text
Region(kappa) subseteq A_q(epsilon)
and A_q(epsilon) subseteq A_q(epsilon').
```

Then `kappa` supports `CertAdeq(m;q,epsilon',alpha|R)`.

**Proof.** Set inclusion is transitive, so `Region(kappa) subseteq A_q(epsilon')`. Certificate validity and interpretation are unchanged. This proves only the adequacy component; a full license at `epsilon'` still requires reassessment of all other components. `square`

### Proposition 6: merge licenses are not generally the union of branch licenses

There are branches `S^A,S^B` and merge protocol `mu` such that the same substantive request profile is granted in both branches but its merged-stage successor is withheld in `Merge(S^A,S^B,mu)`.

**Proof.** Let the parent contain two conflicting calibration events `e_1,e_2`. Branch `A` validates a correction establishing `e_1` as authoritative and grants from it; branch `B` validates a different correction establishing `e_2` as authoritative and grants the same profile from that source. Let `mu` retain both corrections but have no rule for resolving their incompatible authority claims. The merged admissible view cannot validate either supporting certificate for the merged-stage successor, so it withholds the request. Unrelated licenses can still persist by the frame rule. `square`

### Proposition 7: dominator defeat does not entail certified inadequacy

There are updates in which

```text
DefeatedByDominator(lic,m',q,K',sigma',R')
and CertAdeq(m;q,epsilon,alpha|R').
```

**Proof.** Choose two models whose certified risks both lie inside the acceptable region, with `m'` strictly better on the declared dominance coordinates. The new model defeats the older admissibility component, while the older adequacy certificate remains valid. `square`

## 18. Consequences for a neural implementation

A finite neural scorer/router may approximate Strata 2–4, but it must not be the sole raw record or provenance store. The update semantics requires stable identifiers and dependency edges that permit selective invalidation.

At minimum, a neural interface should distinguish:

```text
current request/version identifiers
component signed margins
certificate-validity indicators
four-way operational status
active-set membership
selected model or fallback
impact/dependency references
reason and provenance pointers.
```

Training examples must also distinguish update transitions:

```text
grant -> grant       conservative persistence
grant -> withheld    support lapse
grant -> refused     countercertificate or dominator
grant -> undefined   attempted ill-typed new scope
withheld -> grant    new support or provenance repair.
```

A binary “license/not license” label collapses the very update structure the logic is meant to expose. A learned cache may accelerate reassessment, but the authoritative status remains a typed assessment tied to the current structured record.

## 19. Decisions fixed here

1. Consequence is separated into model-local object consequence, fixed-stage typed license consequence, and current defeasible consequence.
2. The default object logic may be classical inside a fixed typed context; cross-context reasoning is never automatic.
3. The conclusion of applying a license is `MayUse`, `LicensedOutput`, or `MayRely`, not an unindexed truth claim.
4. Context labels include model/version, theory, frame, task, domain/version, purpose, and record view.
5. Contradictions across non-equivalent labels produce disagreement or decision conflict, not explosion.
6. Domain restriction, extension, union, and intersection require risk-specific transport; set inclusion alone is insufficient.
7. Fixed-stage derivability is monotone, while current consequence is nonmonotone across stage updates.
8. Raw records are hereditary along a lineage; admissible views, certificates, licenses, and selections are not.
9. Updates are dependency-directed and evaluated in strata to prevent self-support and unnecessary global recomputation.
10. Changed request fields create linked new requests rather than mutating historical license records.
11. Retraction or broken provenance normally yields withholding; refusal requires a valid countercertificate or another certified component failure.
12. A model/library addition affects admissibility only after valid comparable evaluation and inclusion in the relevant search scope.
13. Expiry is derived from explicit validity/review conditions.
14. Branch merges retain raw histories but recompute current licenses; they do not union branch belief/license sets.

## 20. Deferred questions

Task 10 must provide:

- the exact scalar and Pareto dominance relations;
- the global comparative impact rule for each dominance profile;
- when partial domination warrants a domain split;
- measure reconstruction for distributional residual domains;
- exact retain, restrict, supersede, and revoke conditions.

Task 11 must provide:

- typed bridge validity and error composition;
- compatibility conditions on overlapping scientific charts;
- when disagreement can be translated across frames;
- atlas coverage and seam obligations.

Tasks 12–14 must decide whether the minimal core calculus needs a dedicated proof system and establish the strongest soundness, non-explosion, update-persistence, retention, or non-finality results that survive audit. The KLM and AGM comparisons remain scoped structural analogies unless a later representation theorem proves a tighter correspondence.

Task 11A subsequently requires every current-license, active-set, consequence, and stability reference to carry a license profile `P`. Read this file's unindexed `CurrentLicenses` as historical shorthand pending the canonical Task 13 consolidation.

## Task conclusion

The logic now states what a license permits one to infer without converting usefulness into truth. Classical reasoning remains available inside a fixed model context; license application produces labeled reliance judgments; transport across models, frames, or domains requires a witness; and conflicting local conclusions remain quarantined. Finite-stage revision preserves raw history while recomputing admissible evidence, certificates, licenses, and routing through a dependency-directed stratified update. This supplies the dynamic foundation required for Task 10's dominance, retention, and domain-splitting rules.
