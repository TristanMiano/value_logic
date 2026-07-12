# Integrated License Profiles and a Finite Witness Model

Status: Task 11A integration and interface resolution  
Date: 2026-07-11  
Depends on: [`01_signature.md`](01_signature.md), [`02_license_semantics.md`](02_license_semantics.md), [`03_consequence_update.md`](03_consequence_update.md), [`04_dominance_retention.md`](04_dominance_retention.md), [`05_atlas.md`](05_atlas.md)  
Checkpoint: [`A_finite_stage_foundations.md`](../notes/checkpoints/A_finite_stage_foundations.md)

> **Checkpoint A1 compactness notice.** This file's atom-level four-status presentation will be compressed in Task 13 to a separate well-formedness judgment plus three-valued meaningful atom assessments. Its named reason codes remain readable displays of indexed witnesses/obstacles, not primitive constructors. Task 11B must verify the legacy witness through that compact kernel rather than reproduce a closed reason-code enum.

## Executive resolution

Task 11A compared three coherent interfaces:

1. separate basic reliance and preferred-use predicates;
2. one license judgment indexed by a finite requirement profile;
3. a strong preferred-use license plus a separately named adequacy/usability judgment.

The selected design is **profile-indexed licensing**:

```text
Lic_P(e;omega)
```

means that use plan `e` is licensed for request `omega` under explicitly named requirement profile `P`. There is no well-formed unqualified `Lic(e;omega)` in the core language.

Named profiles recover the useful vocabulary of the other designs:

```text
P_rely
  = adequacy + fallback improvement + hard constraints + trace

P_pref-rel(g,K,sigma)
  = P_rely + relative undefeated status

P_pref-cert(g,K,sigma)
  = P_rely + certified-undominated status.
```

Thus one may use readable aliases

```text
UseWarrant(e;omega)       := Lic_{P_rely}(e;omega)
PreferredRel(e;omega,g)   := Lic_{P_pref-rel(g)}(e;omega)
PreferredCert(e;omega,g)  := Lic_{P_pref-cert(g)}(e;omega),
```

but these aliases are not independent semantic primitives. A selector names the minimum profile its selected plan must satisfy.

This design does not decree that a comparatively dominated older model must remain in use. It says exactly which conclusions survive a comparison change:

- target/empirical/certified adequacy remain unchanged unless their evidence or scope changes;
- licenses whose profile does not require comparison remain unchanged;
- licenses whose profile requires the defeated comparison atom are refused or withheld as appropriate;
- current selection changes according to the selector's required profile and policy;
- archive history is unaffected absent an explicit removal event.

An older model may therefore remain actually selected under another purpose, profile, subdomain, resource regime, or fallback role; remain usable but unselected; or remain only archived. All three cases occur in the integrated witness below.

The inherited universal closure clause is superseded as a design default. The narrower formal claim that closure is forced by every coherent action-authorizing interface is falsified by the profile-indexed witness. Closure is required by some profiles, not all, and the distinction plus its project impact is recorded in the claim ledger.

## 1. Design alternatives

### 1.1 Alternative A: layered predicates

The layered design uses distinct primitives:

```text
CertAdeq(e)
UseWarrant(e)
CompareStatus(e)
PreferredUse(e)
SelectedNow(e)
ArchiveRetained(e).
```

Its advantage is immediate prose readability. Its costs are:

- every new application-specific strength tends to create another predicate;
- the relation among layers must be separately axiomatized;
- two users can disagree whether a safety, closure, or bridge condition belongs “inside” a layer;
- neural outputs can accidentally hard-code one layer inventory.

It remains a valid presentation of named profiles, but it is not selected as the primitive syntax.

### 1.2 Alternative B: profile-indexed license

The parameterized design uses:

```text
Lic_P(e;omega)
```

with finite, typed `P`. It supports:

- explicit application-specific requirements;
- formal comparison of stronger and weaker profiles;
- one assessment operator and status type;
- readable aliases for common profiles;
- selectors that state their minimum authorization strength;
- new profiles without changing the core grammar.

Its main risk is suppressed notation: writing bare `Lic` could hide which profile was used. The type system therefore makes omission of `P` undefined.

### 1.3 Alternative C: strong preferred-use license

The strong design keeps Task 8's full conjunction as the sole `Lic` and uses separate predicates such as:

```text
Adequate
Usable
Available
FallbackSuitable
Archived.
```

It is coherent if “license” is stipulated to mean current competitively approved use. It is less suitable as the canonical interface because:

- many motivating sentences use “licensed” for scoped usability before unique selection;
- unknown comparisons can erase the main permission even when every noncomparative requirement passes;
- different selection policies require different strong license notions anyway;
- actual use of an older model under another profile becomes awkward to describe.

The strong interpretation survives as `P_pref-rel` or `P_pref-cert`; it is rejected only as the universal unindexed meaning of `Lic`.

### 1.4 Decision matrix

| Criterion | Layered A | Profile-indexed B | Strong C |
|---|---|---|---|
| factors remain inspectable | yes | yes | partly; needs auxiliary statuses |
| adds new requirement without new grammar | weak | strong | weak |
| represents several authorization strengths | yes | yes | only through extra predicates |
| makes comparison scope explicit | yes | yes | yes, but proliferates strong licenses |
| handles older-model actual use under another profile | yes | yes | awkward but possible |
| distinguishes unknown from dominance | yes | yes | yes if auxiliary status retained |
| supports a formal strength preorder | manual axioms | direct set inclusion | manual axioms |
| neural implementation options | multiple heads | multiple heads or profile input | strong head plus auxiliary heads |
| risk of ambiguous bare `Lic` | medium | controlled by type error | high across purposes |
| public readability | high | high with named profiles | high only after strict terminology |

Alternative B wins because it subsumes the useful cases of A and C while giving their relationship a simple formal structure. This is a design result, not a metaphysical theorem.

## 2. Requirement atoms and profiles

### 2.1 Requirement atoms

Let `ReqAtom` be a tagged family containing at least:

```text
AdeqReq(q,epsilon,alpha)
ImproveReq(F,q,Delta,alpha)
ConstraintReq(c,q)
TraceReq(p)
RelUndefeatedReq(D,g,K,sigma)
CertUndominatedReq(D,g,K,sigma)
BridgeReq(beta,purpose)
CoverageFloorReq(gamma)
ReviewCurrentReq(review_policy).
```

Only the first four and two comparison atoms are needed in the minimal Task 11A interface. Other atoms show extensibility.

Each atom has a typed assessment:

```text
AssessAtom_{a,t}(r,e,omega | S_{a,t}) in Status.
```

The atom assessment stores its certificate, reason, and provenance.

### 2.2 License profile

A profile is:

```text
P : LicenseProfile = <
    profile_id,
    finite_required_atoms Req(P),
    finite_report_only_atoms Report(P),
    aggregation_rule,
    intended_use_role,
    validity/review_conditions,
    provenance
>.
```

`Req(P)` determines the top-level license status. `Report(P)` is always evaluated when possible but cannot by itself block the grant. This lets a reliance profile report current comparison status without requiring it.

The `intended_use_role` field is typed:

```text
UseRole =
    DiagnosticOnly
  + Advisory
  + ActionAuthorizing
  + EmergencyException
  + GovernanceException.
```

A profile is **action-authorizing** exactly when `intended_use_role=ActionAuthorizing`. Emergency and governance exceptions are separately typed so that they cannot silently inherit ordinary authorization semantics.

### 2.3 Well-formedness

`WFProfile(P,omega,e)` requires:

1. every atom is well typed for the same model/use-plan and task context;
2. all required domains/frames are equal or connected by a valid transport;
3. certificate interpretations are not silently mixed;
4. comparison atoms name their profile, evaluated set, and closure strength;
5. no two required atoms impose contradictory type identities;
6. every profile with `intended_use_role=ActionAuthorizing` includes an explicit fallback; `EmergencyException` and `GovernanceException` roles instead name their exceptional rule and trace;
7. the profile is versioned and traceable;
8. `Req(P)` is finite.

### 2.4 Canonical profiles

Let:

```text
A = AdeqReq(q,epsilon,alpha)
B = ImproveReq(F,q,Delta,alpha)
H = ConstraintReq(c,q)
T = TraceReq(p).
```

Define:

```text
P_rely(q,epsilon,alpha,F,Delta,c,p)
  = <required={A,B,H,T},
     report={current comparison status when available},
     intended_use_role=ActionAuthorizing>.
```

For finite comparison profile `g`:

```text
P_pref-rel(...,g,K,sigma)
  = <required={A,B,H,T,
               RelUndefeatedReq(D,g,K,sigma)},
     intended_use_role=ActionAuthorizing>.

P_pref-cert(...,g,K,sigma)
  = <required={A,B,H,T,
               CertUndominatedReq(D,g,K,sigma)},
     intended_use_role=ActionAuthorizing>.
```

These names are defaults, not universal normative mandates. An emergency selector, experiment, exploration policy, or regulated deployment can name another well-formed profile.

### 2.5 Profile strength

For profiles with compatible atom semantics, define:

```text
P preceq_prof Q
iff Req(P) subseteq Req(Q).
```

Then `Q` is at least as demanding as `P`. Report-only atoms do not affect strength.

For the canonical profiles:

```text
P_rely preceq_prof P_pref-rel
P_rely preceq_prof P_pref-cert.
```

`P_pref-rel` and `P_pref-cert` are not ordered by atom inclusion as written; their comparison requirements have different semantics. One can define a refinement map because certified undominated status entails relative undefeated status under the same evaluated set, but this is a theorem about atoms, not literal set inclusion.

## 3. Profile-indexed assessment

### 3.1 Request record

Extend the Task 8 request with a mandatory profile reference:

```text
omega_P = <
    request_id,
    profile_ref P,
    a,t,b,e,q,epsilon,alpha,F,Delta,K,c,sigma,p,R
>.
```

Changing `P` creates a new linked request. It does not mutate or defeat the old request.

### 3.2 Diagnostic vector

Always compute when possible:

```text
Diag(P,e,omega)
  = <(r,AssessAtom(r,e,omega)) :
       r in Req(P) union Report(P)>.
```

This preserves failure identity and optional comparison information.

### 3.3 Top-level assessment

Define:

```text
AssessLic_P(e;omega)
  = AllReq(
      AssessWFProfile(P,e,omega),
      (AssessAtom(r,e,omega))_{r in Req(P)}
    ).
```

Use Task 8 precedence:

```text
Undefined > Refused > Withheld > Granted
```

for the top-level diagnostic tag. Every component result remains in `Diag`.

In this historical four-chain presentation, the top-level tag is never a sufficient safety report: an `Undefined` atom can dominate the aggregate while another required atom carries a certified safety refusal. Until consolidation, every action consumer must inspect `Diag` (or a lossless safety projection). The Checkpoint A1 compact kernel removes this semantic masking by evaluating atoms only after `WF` succeeds; a malformed request is `Undefined`, while every meaningful atom is refuted, open, or supported.

### 3.4 Satisfaction

```text
S_{a,t} |= Lic_P(e;omega)
iff AssessLic_P(e;omega)=Granted.
```

Bare notation

```text
Lic(e;omega)
```

is ill formed and assesses as:

```text
Undefined(MissingLicenseProfile).
```

In informal prose, “licensed” must be followed by a nearby named profile or a previously fixed document-wide convention.

### 3.5 Readable aliases

Aliases may be used after their profiles are fixed:

```text
UseWarrant(e;omega)
  iff Lic_{P_rely}(e;omega).

PreferredRel(e;omega,g)
  iff Lic_{P_pref-rel(g)}(e;omega).

PreferredCert(e;omega,g)
  iff Lic_{P_pref-cert(g)}(e;omega).
```

The final paper may choose friendlier prose, but formal statements retain `P`.

## 4. Comparison atoms

### 4.1 Relative undefeated status

For evaluated eligible set `E=E^+_{sigma,g}(D)`:

```text
UndefeatedRelative(e;E,D,g)
iff no h in E satisfies CertDominates(h,e;D,g|R).
```

Unknown pairwise comparisons are allowed and reported. This means only:

> no certified dominator was found in the validly evaluated set.

It does not mean every competitor was resolved.

### 4.2 Certified-undominated status

```text
CertifiedUndominated(e;E,D,g)
```

requires every `h in E` to have a valid result establishing:

```text
h does not dominate e
or h is ineligible/inapplicable under g.
```

Unknown required pairs prevent this stronger status.

### 4.3 Atom assessment table

| Evidence state | `RelUndefeatedReq` | `CertUndominatedReq` |
|---|---|---|
| valid certified dominator exists | `Refused(CertifiedDominatorFound)` | `Refused(CertifiedDominatorFound)` |
| no dominator; every pair resolved | `Granted` | `Granted` |
| no dominator; some pair unknown | `Granted` with unknown-pair report | `Withheld(UnresolvedComparison)` |
| search trace invalid/missing | `Withheld(SearchEvidenceMissing)` | `Withheld(SearchEvidenceMissing)` |
| type/frame/profile mismatch | `Undefined` | `Undefined` |

### 4.4 Logical relation

For the same `E,D,g`:

```text
CertifiedUndominated(e;E,D,g)
  => UndefeatedRelative(e;E,D,g).
```

The converse fails when at least one comparison is unknown and no certified dominator exists.

### 4.5 No global optimality

Neither atom quantifies over unknown future models or the full model universe. A profile requiring `GlobalClosed` remains undefined/unavailable absent an independent completeness theorem.

## 5. Selection and actual use

### 5.1 Selector specification

A selector declares:

```text
pi : SelectorSpec = <
    required_profile P_pi,
    candidate_scope,
    ranking/tie/override policy,
    fallback,
    switching and information policy,
    provenance
>.
```

### 5.2 Safe selection rule

```text
SelectedNow_{a,t}(pi,e,x)
```

requires:

1. `x` is covered by the request scope;
2. `AssessLic_{P_pi}(e;omega_{e,x})=Granted`;
3. `e` is selected by `pi` under its declared rule;
4. switching/hard constraints pass;
5. the selection trace names `P_pi` and any unknown comparison.

### 5.3 No universal preferred-use requirement

A selector may require `P_pref-cert`, `P_pref-rel`, `P_rely`, or another justified profile. Therefore:

- a regulated best-resolved selector may refuse to choose under unknown comparisons;
- a bounded relative selector may choose an undefeated candidate while reporting unknown pairs;
- an edge or emergency selector may choose an older `P_rely`-licensed model when stronger competitors are inapplicable;
- an information-gathering selector may choose an experiment rather than any model.

This is not permission for arbitrary selection. The required profile and policy are part of the auditable decision specification.

### 5.4 Retention

Keep distinct records for:

```text
Target/CertAdeq status
Lic_P status for each assessed P
SelectedNow under each selector
ArchiveRetained.
```

They may be fields of one structured record rather than separate primitive predicates. “Distinct” means recoverable and nonconflated, not necessarily separate neural modules.

## 6. Update semantics under profiles

### 6.1 Profile-local impact

Let `Deps(P,e,omega)` be the provenance dependencies of required atoms. An update affects `Lic_P` only if it changes:

- a request/profile field;
- a required atom or its assumptions/certificate;
- a shared dependency of a required atom;
- an explicit standing review condition.

Report-only atom changes update diagnostics but not the top-level status.

### 6.2 Evidence rebuttal and lapse

If adequacy evidence is rebutted or lapses, every profile requiring `AdeqReq` is affected:

```text
countercertificate -> Refused
invalidated support without countercertificate -> Withheld.
```

### 6.3 Comparative update

If a new model creates a certified dominator:

- profiles requiring the relevant comparison atom become `Refused`;
- profiles that only report comparison retain their prior top-level status and update the report;
- unrelated profiles remain unchanged by the frame rule;
- selectors whose required profile fails must reroute;
- archive entries remain.

### 6.4 Profile change

Moving from `P` to `Q` is a new request:

```text
omega_Q = ChangeProfile(omega_P,Q).
```

A refusal under `Q` is not a contradiction with a grant under `P`.

### 6.5 Stage stability must be profile-indexed

Task 12 must write:

```text
Stable(e,request_core,P,continuation)
```

rather than unqualified `StableLic(e)`. A model can remain stable under `P_rely` while changing repeatedly under library-relative preference profiles.

## 7. Integrated witness: base universe

### 7.1 Cases and target

Let the finite task case universe be:

```text
X={a,b,c,d,e}.
```

The target deployment scope is `T=X`, with uniform measures on every listed finite subdomain unless stated otherwise.

Case `a` is an edge/offline condition. Cases `b,c,d` are cloud conditions. Case `e` is a deliberately unsupported regime.

### 7.2 Plans and fallback

Initial library at stage `t_0`:

```text
K_0={O,S,Q}
```

where:

- `O` is an older low-resource plan;
- `S` is a higher-accuracy specialist;
- `Q` is a quick plan with a certified robustness violation.

At `t_1`, add successor plan `N`:

```text
K_1=K_0 union {N}.
```

The explicit fallback is:

```text
F=Defer
J_F=0.30.
```

Use hard tolerance and fallback advantage:

```text
epsilon=0.20
Delta=0.02.
```

Thus any scalar upper risk bound at most `0.20` satisfies hard adequacy and automatically beats this fallback by at least `0.02`; the two atoms remain separately recorded.

### 7.3 Declared scopes

```text
D_O={a,b,c}
D_S=D_N=D_cloud={b,c,d}
D_Q={a,b}
Gap={e}.
```

`N` is not executable on edge case `a` under its declared deployment protocol. This is an applicability fact, not poor measured performance.

### 7.4 Recorded representative losses

The early record contains the following representative observed/evaluation losses:

| plan | `a` | `b` | `c` | `d` |
|---|---:|---:|---:|---:|
| `O` | `0.06` | `0.10` | `0.14` | undefined |
| `S` | undefined | `0.04` | `0.05` | `0.03` |
| `Q` | `0.08` | `0.11` | undefined | undefined |
| `N` | undefined | `0.03` | `0.04` | `0.05` |

These are finite-stage observations/estimates, not oracle target risks. They help explain the comparisons and post-hoc split proposal, but only the certificates stated below authorize population/domain judgments. The later rebuttal of `S` is therefore coherent: the early frequentist procedure can be valid in its repeated-sampling sense while this realized early interval misses the fixed target, and later stronger same-scope evidence can certify the miss.

### 7.5 Resource and robustness data

| plan | deployment cost | memory | robustness deficit |
|---|---:|---:|---:|
| `O` | `1.0` | `1` | `[0.04,0.06]` |
| `S` | `3.0` | `3` | `[0.02,0.04]` |
| `Q` | `0.5` | `1` | `[0.21,0.24]` |
| `N` | `2.0` | `4` | `[0.05,0.08]` |

The safety profile requires robustness deficit at most `0.15`. The edge hardware at `a` permits memory at most `2`, independently excluding `S` and `N` there.

### 7.6 Certificates at `t_0`

Valid joint/scalar certificates establish:

```text
Risk_{D_O}(O) in [0.09,0.11]
Risk_{D_S}(S) in [0.035,0.055]
Risk_{D_Q}(Q) in [0.08,0.12]
Robust(Q) in [0.21,0.24].
```

The first three support hard risk adequacy. `Q` nevertheless fails the hard robustness constraint by countercertificate.

A prespecified overlap evaluation—not a free restriction of the whole-domain expected-risk certificates—also establishes:

```text
Risk_{D_overlap}(O) in [0.11,0.13]
Risk_{D_overlap}(S) in [0.040,0.050],
where D_overlap={b,c}.
```

Both entities therefore pass the comparison profile's hard adequacy filter on its own evaluation specification. The same overlap-scope joint comparison then validly certifies:

```text
S scalar-risk dominates O on {b,c}.
```

### 7.7 Certificates added at `t_1`

For `N`:

```text
Risk_{D_N}(N) in [0.035,0.050]
Robust(N) in [0.05,0.08].
```

A prespecified overlap certificate additionally gives:

```text
Risk_{D_overlap}(N) in [0.035,0.045].
```

Thus `N` and `O` both satisfy the comparison-scope adequacy filter, and a valid joint comparison certifies:

```text
N scalar-risk dominates O on {b,c}.
```

For whole-domain cloud scalar score

```text
score(e)=Risk_{D_cloud}(e)+0.005*deployment_cost(e),
```

a valid joint certificate gives:

```text
score(N) in [0.048,0.050]
score(S) in [0.054,0.056],
```

so `N` dominates `S` under this named whole-domain profile.

These are new, tighter joint score certificates; they are not obtained by ordinary interval propagation from the marginal risk certificates above. Marginal propagation alone gives overlapping score regions and would withhold the dominance claim.

Recorded point estimates suggest `N` is better on `{b,c}` while `S` is better on `{d}`. Those cells were chosen after inspecting the new data and lack a simultaneous/selective comparison certificate. Their local target relation is operationally unknown at `t_1`.

## 8. Stage `t_0`: all four statuses and initial routing

### 8.1 Status witnesses

Use canonical `P_rely` unless otherwise noted:

| request | result | reason |
|---|---|---|
| `omega_G=Lic_{P_rely}(O,D_O)` | `Granted` | adequacy, fallback, hard constraints, and trace pass |
| `Lic_{P_rely}(S,D_S)` | `Granted` | same required atoms pass |
| `omega_R=Lic_{P_rely}(Q,D_Q)` | `Refused` | `HardConstraintViolation(Robustness)` with countercertificate |
| `omega_W=Lic_{P_rely}(S,{b,c,d,e})` | `Withheld` | no valid evidence/certificate covers `e` |
| `omega_U=Lic_{P_rely}(O,D_O,wrong_frame)` | `Undefined` | output/frame interface mismatch |
| bare `Lic(O,D_O)` | `Undefined` | `MissingLicenseProfile` |

Thus `Granted`, `Refused`, `Withheld`, and `Undefined` coexist in one finite structure without treating non-grants as one Boolean negation.

For `omega_W`, `S` has a typed executable interface on `e`; `e` lies outside its certified/evaluated scope rather than outside its executable interface. The missing scope evidence therefore yields `Withheld`. By contrast, an absent or ill-typed interface on `e` would yield `Undefined` under the well-formedness rule.

### 8.2 Simultaneous usable plans

Under `P_rely`:

```text
Act_{P_rely}(b)={O,S}
Act_{P_rely}(c)={O,S}.
```

Under scalar-risk `P_pref-rel` on the prespecified overlap:

```text
S is Granted
O is Refused(CertifiedDominatorFound,S).
```

There is no contradiction: the requests use different profiles.

### 8.3 Initial selector

Let `pi_0` require `P_pref-rel` when more than one candidate is comparable and `P_rely` when only one applies. It routes:

```text
a -> O
b -> S
c -> S
d -> S
e -> F=Defer.
```

`O` is an old model still actually used on `a`; `Q` is retained only in the archive because its action-authorizing profile is refused.

## 9. Stage `t_1`: model addition and comparison changes

### 9.1 Add the successor

Append:

```text
ModelAdded(N)
Evaluation(N,D_N,...)
CertificateIssued(kappa_N)
SearchRun(sigma_1).
```

`Lic_{P_rely}(N,D_N)` is granted.

### 9.2 Consequences by profile

On `{b,c}`:

| plan | `P_rely` | risk `P_pref-rel` |
|---|---|---|
| `O` | remains `Granted` | `Refused`, dominated by `N` |
| `N` | `Granted` | `Granted` relative to evaluated set |

On whole cloud domain `{b,c,d}` under the certified scalar profile:

| plan | `P_rely` | cloud `P_pref-rel` |
|---|---|---|
| `S` | remains `Granted` | `Refused`, dominated by `N` |
| `N` | `Granted` | `Granted` |

The addition does not alter `O` or `S` adequacy evidence. It changes profiles containing the relevant comparison atom.

### 9.3 Continued use versus mere retention

At `t_1` use selector `pi_1`:

```text
a -> O
b -> N
c -> N
d -> N
e -> F=Defer.
```

The two cases are now explicit:

1. **Continued old-model use:** `O` remains actually selected on `a` because `N` is not executable there and the edge profile licenses `O`.
2. **Usable but unselected retention:** `S` remains `Lic_{P_rely}`-granted on `D_S` but is not selected by the cloud scalar profile after `N` arrives.
3. **Archive-only retention:** `Q` remains stored with its refusal/countercertificate but is not action-authorized.

No single word “retained” is allowed to erase these differences.

### 9.4 Unknown comparisons

For the adaptively proposed local comparison of `S` and `N` on cells `{b,c}` and `{d}`:

```text
UndefeatedRelative(S;E,D_S,g_local)
UndefeatedRelative(N;E,D_S,g_local)
```

can both obtain because neither direction has a valid certified edge. Therefore:

```text
Lic_{P_pref-rel(g_local)}(S) = Granted with unknown-pair report
Lic_{P_pref-rel(g_local)}(N) = Granted with unknown-pair report.
```

But:

```text
Lic_{P_pref-cert(g_local)}(S) = Withheld(UnresolvedComparison)
Lic_{P_pref-cert(g_local)}(N) = Withheld(UnresolvedComparison).
```

This is the required countermodel to

```text
UndefeatedRelative => CertifiedUndominated.
```

## 10. Successful and withheld domain splits

### 10.1 Successful split of the old chart

Refine:

```text
D_O={a,b,c}
```

into:

```text
D_edge={a}
D_overlap={b,c}.
```

`SplitReady` holds because:

- the finite cells are prespecified by deployment condition;
- the uniform child measures and parent weights are exact;
- `O` certificates restrict/recompute validly on `D_edge`;
- `N` versus `O` has a valid joint certificate on `D_overlap`;
- `N` is inapplicable on `D_edge`;
- fallbacks and provenance are complete.

Issue linked child results:

```text
Lic_{P_rely}(O,D_edge) = Granted
Lic_{P_pref-rel}(O,D_edge) = Granted
Lic_{P_rely}(O,D_overlap) = Granted
Lic_{P_pref-rel}(O,D_overlap) = Refused(dominated by N)
Lic_{P_pref-rel}(N,D_overlap) = Granted.
```

The split explains continued use on `a` without claiming that `O` remains preferred on `{b,c}`.

### 10.2 Withheld split of the specialist chart

Propose after seeing the data:

```text
D_S -> <{b,c},{d}>.
```

Recorded point estimates suggest a local reversal, but the finite-stage evidence lacks a selection-adjusted/simultaneous cell certificate. Therefore:

```text
SplitReady=false
Assess split = Withheld(LocalSplitUncertified).
```

No child preferred-use license is manufactured. The whole-domain cloud profile may still prefer `N`; the possible local value of `S` on `d` remains an open empirical question.

This realizes the Task 10 result that partial-looking advantage does not automatically cause a split.

## 11. Bridge statuses in one overlap

At `t_1`, store purpose-specific bridge records:

1. **Exact observable bridge:** after a unit translation, `O` and `S` agree on a shared diagnostic observable at `b`.
2. **Approximate predictive bridge:** translated `O` and `N` outputs on `{b,c}` satisfy a certified discrepancy bound `delta_ON=0.03`.
3. **Decision bridge:** `S` and `N` induce the same action on `{b,c}` under decision rule `d`, despite unequal predictions.
4. **Predictive incompatibility at a tighter tolerance:** a valid countercertificate shows `S` and `N` do not satisfy requested predictive bridge `delta=0.005` on the same overlap.
5. **Unknown translation bridge:** `Q` uses a native categorical output with no validated translation to `N`'s scalar observable.

These statuses coexist because bridge kind, purpose, direction, and tolerance are indexed. Decision compatibility does not imply tight predictive compatibility.

## 12. Stage `t_2`: lapse versus rebuttal

### 12.1 Lapse of `O`

Append a validated correction showing leakage in the only risk certificate supporting `O`:

```text
Correction(eval_O,SampleLeakage)
```

with no countercertificate against target adequacy. Then every current profile requiring `AdeqReq(O)` becomes:

```text
Withheld(BrokenAssumption).
```

But:

```text
not CertInadeq(O).
```

`O` ceases actual use at `a`; fallback is required there. Its earlier grants and archive entry remain.

### 12.2 Rebuttal of `S`

Append a valid same-scope certificate:

```text
Risk_{D_S}(S) in [0.24,0.27].
```

Since the entire region exceeds `epsilon=0.20`:

```text
CertInadeq(S,D_S)
Assess Lic_P(S,D_S)=Refused(HardRiskViolation)
```

for every action profile `P` requiring that adequacy atom.

### 12.3 Updated routing

At `t_2`:

```text
a -> F=Defer        O withheld
b -> N
c -> N
d -> N
e -> F=Defer        certified gap.
```

This stage distinguishes evidence defeat from comparative defeat and from archive retention.

## 13. Provenance and event history

### 13.1 Primary nodes

The witness uses versioned nodes:

```text
models:       m_O^0,m_S^0,m_Q^0,m_N^0
domains:      D_O^0,D_S^0,D_Q^0,D_N^0,D_overlap^0,D_cloud^1,
              D_edge^1,D_overlap^1
data:         d_O^0,d_S^0,d_Q^0,d_N^1,d_O_leak^2,d_S_rebut^2
procedures:   cert_risk^0,cert_compare^0,cert_split^1
certificates: k_O^0,k_S^0,k_Q^0,
              k_O_overlap^0,k_S_overlap^0,
              k_N^1,k_N_overlap^1,k_NO^1,k_NS_cloud^1,k_S_bad^2
searches:     sigma_0,sigma_1
profiles:     P_rely^0,P_pref-rel^0,P_pref-cert^0
requests:     omega_*^{stage,profile}
decisions:    route_0,route_1,route_2
bridges:      beta_OS,beta_ON,beta_SN^decision,beta_SN^tight,beta_QN.
```

### 13.2 Dependency edges

Every current grant/refusal/withholding has a path of the form:

```text
model version
domain/evaluation spec
data or proof event
certificate procedure
certificate/comparison result
required atom assessment
profile-indexed request
top-level status
selector decision
stage event.
```

Comparison profiles additionally point to `K`, `sigma`, `g`, eligible-set computation, and every certified/unknown pair report.

### 13.3 Correction and rebuttal edges

At `t_2`:

```text
d_O_leak^2 corrects d_O^0
  -> invalidates k_O^0
  -> lapses O requests
  -> reroutes a.

d_S_rebut^2 supports k_S_bad^2
  -> refutes AdeqReq(S)
  -> refuses S requests.
```

No event deletes its predecessor. Historical reconstruction remains possible.

### 13.4 Provenance completeness audit

Every result used by the witness has:

- exact object/version identity;
- task/domain/frame identity;
- certificate interpretation;
- evidence and correction links;
- profile and required-atom list;
- comparison/search scope where relevant;
- status reason;
- selector/fallback consequence.

The witness therefore satisfies the requested complete finite provenance at the formal-record level. It does not claim cryptographic integrity or reproduce executable datasets; those are implementation extensions.

## 14. Witness requirement audit

| Task 11A requirement | Realization |
|---|---|
| at least three plans | `O,S,Q`, later `N` |
| explicit fallback | `F=Defer`, risk `0.30` |
| overlap | `O/S` on `{b,c}`; later `O/S/N` overlap |
| certified gap | `{e}` |
| simultaneous usable models | `O,S` under `P_rely` at `b,c` |
| comparison change without evidence erasure | arrival of `N` changes preferred profiles only |
| continued old-model use | `O` remains selected on edge case `a` at `t_1` |
| mere usable retention | `S` remains `P_rely`-granted but unselected at `t_1` |
| archive-only retention | `Q`; later historical `O,S` events |
| four statuses | table in Section 8.1 |
| lapse | leaked `O` certificate at `t_2` |
| rebuttal | countercertificate against `S` at `t_2` |
| model-addition supersession | `N` at `t_1` |
| unresolved comparison | adaptive local `S/N` cells |
| successful split | `D_O -> {a}+{b,c}` |
| withheld split | post-selected `D_S -> {b,c}+{d}` |
| multiple bridge statuses | exact, approximate, decision, incompatible, unknown |
| complete provenance | Section 13 graph schema and event links |

The external audit initially found one genuine scope inconsistency: the first version used overlap dominance without overlap-scope adequacy certificates, despite rejecting free restriction of expected-risk certificates. The repaired witness now includes the prespecified overlap certificates in Sections 7.6–7.7 and their provenance nodes in Section 13. After that repair, no contradiction remains in this finite witness; the other apparent conflicts come from comparing different profiles, scopes, stages, or evidence views as if they were one judgment.

## 15. Elementary results

### Theorem 1: profile functionality

For fixed `S,e,omega,P`, `AssessLic_P(e;omega)` has exactly one top-level status tag.

**Proof.** Every required atom has one tagged assessment, and `AllReq` is a deterministic function with fixed precedence. `square`

### Theorem 2: profile weakening

Let `P preceq_prof Q`, with identical assessments for every atom in `Req(P)`. If

```text
AssessLic_Q(e;omega_Q)=Granted,
```

then

```text
AssessLic_P(e;omega_P)=Granted.
```

**Proof.** Grant under `Q` means every atom in `Req(Q)` is granted. Since `Req(P) subseteq Req(Q)`, every atom required by `P` is granted; `AllReq` returns granted. `square`

### Proposition 3: the converse of profile weakening fails

There are requests with `Lic_{P_rely}` granted and `Lic_{P_pref-rel}` refused.

**Witness.** At `t_1`, `O` remains `P_rely`-granted on `{b,c}` while `N` certifiably dominates it under the risk comparison atom, refusing `P_pref-rel`. `square`

### Theorem 4: comparative-update locality

Suppose update `u` changes only comparison/search atoms and their report descendants, while every noncomparative required atom of profile `P` remains valid. If `Req(P)` contains no affected comparison atom, the top-level `Lic_P` status persists.

**Proof.** `P` lies outside the required-atom impact cone. Its required assessment vector is unchanged, so deterministic aggregation returns the prior status. Report-only comparison fields may change. `square`

### Proposition 5: certified undominated implies relative undefeated

For the same evaluated set and comparison profile:

```text
CertifiedUndominated(e) => UndefeatedRelative(e).
```

**Proof.** Certified-undominated status resolves every competitor as non-dominating, ineligible, or inapplicable. Hence no certified dominator exists. `square`

### Proposition 6: relative undefeated does not imply certified undominated

**Witness.** At `t_1`, the adaptive local `S/N` comparison has no certified dominance edge in either direction, so both are relatively undefeated. The unresolved pair prevents either from being certified undominated. `square`

### Proposition 7: comparison defeat does not entail evidence defeat

There are stages satisfying:

```text
Lic_{P_rely}(e)=Granted
Lic_{P_pref-rel}(e)=Refused(CertifiedDominatorFound)
not CertInadeq(e).
```

**Witness.** Use `O` or `S` at `t_1`. Their adequacy certificates remain valid while `N` defeats their named comparison profiles. `square`

### Proposition 8: safe selection is profile-relative

If `SelectedNow(pi,e,x)`, then `Lic_{P_pi}(e;omega_{e,x})` is granted. It need not follow that `Lic_Q` is granted for every stronger or incomparable profile `Q`.

**Proof.** The first result is a selector rule premise. For the second, select `O` on `a` under the edge profile while a cloud preferred-use profile is inapplicable or stronger. `square`

### Proposition 9: no unqualified closure clause

There exists a well-formed action-authorizing license profile with no comparison/closure atom.

**Witness.** `P_rely` requires adequacy, fallback improvement, hard constraints, and trace, and reports comparison when available without requiring it. `O` and `S` receive well-formed grants under it at `t_0`. `square`

This proposition shows that closure is not forced by action authorization plus the retained project requirements. It supersedes E05 as a universal design default and supplies a countermodel only to the narrower formal claim that every coherent action-authorizing profile must contain closure. It does not “falsify” a stipulative definition merely by choosing another definition. The supported replacement is that `P_pref-rel` and `P_pref-cert` contain explicit finite closure requirements.

## 16. Repairs to completed interfaces

Completed files remain historical artifacts. The following integration mappings supersede their ambiguous shorthand.

### 16.1 Task 8 mapping

Task 8's full conjunction is reinterpreted as the named profile:

```text
P_full^8
  = {AdeqReq,
     ImproveReq,
     ConstraintReq,
     RelUndefeatedReq,
     TraceReq}.
```

Thus:

```text
Task8-Lic(omega)
  = Lic_{P_full^8}(omega),
```

not the universal form of every license.

### 16.2 Task 9 mapping

Replace:

```text
CurrentLicenses(R_{a,t})
```

with:

```text
CurrentLicenses(R_{a,t},P)
```

or a structured map from profiles to current grants. Consequence and active-set rules must name the profile required for reliance.

`Succ_u(omega_P)` retains or explicitly changes `P`; a profile change is not a silent successor.

### 16.3 Task 10 mapping

`UFront` supplies `RelUndefeatedReq`. `CFront` supplies `CertUndominatedReq`. Dominance defeat automatically affects only profiles requiring those atoms. Archive, adequacy, and other profiles are separately updated.

### 16.4 Task 11 mapping

Replace one ambiguous chart-use set with profile-indexed views:

```text
Charts^use(A,P)
Act_A(x,zeta,P).
```

An atlas can display several profiles simultaneously. A routing seam is relative to the selector and therefore to `P_pi`.

### 16.5 Neural mapping

A transparent implementation must either:

1. expose component atom statuses/margins and compute arbitrary finite profiles outside the MLP; or
2. take a profile encoding as input and return profile-indexed status while preserving component diagnostics.

One hard-coded “license” bit is insufficient.

## 17. Handoff to Tasks 12–14

### 17.1 Task 12 repairs

Open-endedness must index stability by:

```text
request core + profile + selector where selection is discussed.
```

It must permit:

- stable `P_rely` status with changing preferred profile status;
- stable adequacy with changing selection;
- eventual selection stability without known arrival;
- profile changes that create new requests rather than mind changes about one request.

### 17.2 Task 13 repairs

The minimal core should include:

- `ReqAtom`, finite `LicenseProfile`, and mandatory profile reference;
- `AssessAtom`, `Diag`, and `AssessLic_P`;
- canonical `P_rely`, `P_pref-rel`, and `P_pref-cert` examples;
- profile-indexed current consequence and active sets;
- selector-required profiles;
- profile-indexed stage semantics.

It may omit bridge, Pareto, and split atoms from the minimal grammar while explaining how extensions add them.

### 17.3 Task 14 proof obligations

Task 14 should settle:

1. soundness of profile-indexed inference rules;
2. profile functionality;
3. profile weakening and its exact side conditions;
4. comparative-update locality;
5. `CertifiedUndominated => UndefeatedRelative` and nonconverse;
6. profile-indexed non-explosion/status consistency;
7. selector safety relative to `P_pi`;
8. stability of report-only changes;
9. countermodels to bare/universal `Lic`, universal closure, and profile-independent stability.

### 17.4 Inconsistencies found

The integration audit found no inconsistency in the underlying component semantics. It found four interface defects:

1. bare `Lic` hid a variable requirement set;
2. `CurrentLicenses` and active sets lacked a profile index;
3. comparative defeat was described as if it affected every license strength;
4. stability/non-finality plans did not yet index the judgment whose stability was studied.

The selected interface repairs each defect without rewriting historical events.

## 18. Claim-ledger adjudication

### 18.1 E05

Inherited claim E05 states:

> An agent-level license includes a closure clause: no better model was found in the retrieved/searched library under the available budget.

As a proposed definition, the universal reading is superseded (`D1`) by the profile-indexed design rather than falsified. As the narrower formal claim that closure is forced by every coherent action-authorizing interface satisfying the retained requirements, it is falsified (`X1`) by Proposition 9 and the integrated witness: `P_rely` is coherent and action-authorizing without required comparison closure. The scoped replacement is:

> A profile that authorizes comparative preferred use must state its finite search/closure requirement; `P_pref-rel` records no certified dominator in the evaluated set, while `P_pref-cert` additionally requires every relevant comparison resolved.

### 18.2 Project impact

The design replacement and narrower falsification do not threaten the central goal. They change the core interface and improve the theory-succession account:

- the paper must not claim every license is a best-known-model certificate;
- Task 8's full license becomes one named strong profile;
- current-license sets, neural labels, experiments, and stability claims become profile-indexed;
- comparison status remains required for selectors/profiles that demand preferred use;
- older models can remain usable under one profile while losing another;
- no new repair task is needed because Task 11A is the repair;
- the result should be presented as a central limitation/reconstruction, not a footnote.

E06's comparative defeat clause is correspondingly profile-local: discovering a dominator defeats profiles requiring that comparison atom, not every possible `Lic_P`.

## 19. Decisions fixed here

1. The primitive license judgment is `Lic_P`; the profile reference is mandatory.
2. Bare `Lic` is undefined rather than assigned a hidden default.
3. A profile is a finite set of required atoms plus report-only atoms and provenance.
4. Common layered terms are aliases for named profiles, not additional primitives.
5. `P_rely` omits required comparison closure but may report it.
6. `P_pref-rel` requires no certified dominator in the evaluated set and permits unknown pairs with disclosure.
7. `P_pref-cert` requires resolved non-domination/ineligibility for every relevant evaluated candidate; unknown pairs withhold it.
8. Neither preferred profile establishes global optimality.
9. Selectors declare the minimum profile they require.
10. Continued use, usability without selection, and archive-only retention are distinct structured outcomes.
11. Comparative updates affect only profiles requiring/reporting the changed atoms.
12. Evidence rebuttal and lapse propagate to every profile requiring the affected adequacy/certificate atom.
13. Current license sets, active sets, and future stability claims are profile-indexed.
14. Task 8's full conjunction remains valid as one named strong profile rather than the universal meaning of licensing.

## Task conclusion

The finite-stage foundations now have one integrated interface. Licensing is parameterized by an explicit finite requirement profile, allowing the project to express basic pragmatic reliance, relative preferred use, resolved preferred use, emergency or regulated variants, and diagnostic reports without multiplying primitive predicates or hiding comparison assumptions. The integrated witness realizes all four statuses, overlaps, a gap, continued old-model use, unselected usability, archive-only retention, model-addition supersession, unknown comparison, successful and withheld splits, several bridge kinds, lapse, rebuttal, and complete provenance. The only conflicts were missing profile indices in earlier shorthand. Task 12 can now ask coherent questions about which profile-indexed judgments stabilize or remain non-final.
