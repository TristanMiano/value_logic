# Audit Repairs: Typed Locality and the Concrete Theorem Spine

Status: Task 14B completed

Date: 2026-07-14

Depends on: [`06_open_endedness.md`](06_open_endedness.md), [`07_core_calculus.md`](07_core_calculus.md), [`08_metatheory.md`](08_metatheory.md), and the executable [`WF + K_3` reference](../verification/README.md)

## Durable result summary

This note closes the bounded repair gate created by Checkpoint B. Its positive result is a calculus-specific locality theorem for every frozen operational atom family. The theorem does not promote record keys, event schemas, or footprints to new paper-level carriers. They are a derived interface explaining which finite-state writes can change one instantiated profile slot.

The construction has four parts:

1. a finite typed key projection records every request or store query made while instantiating and evaluating a slot;
2. collection-index keys represent negative reads, so adding the first valid certificate, pair record, or search trace cannot evade dependency tracking;
3. every declared event exposes the keys it may write; and
4. a canonical event-to-key-to-slot graph is therefore change-complete for complete diagnostics, `K_3` values, public assessment, and grant.

Graph-path absence is consequently a sound frame rule for this calculus. The converse remains conditional on observable-specific path realizability: a conservative graph may contain inert paths.

The note also repairs the five accepted statement/reference issues, supplies a concrete seven-vector core witness, and records the executable-kernel repairs. No new truth value, atom kind, reason code, or principal carrier is introduced.

## 1. Typed request/store keys and canonical projections

### 1.1 Why current provenance is not a read footprint

The provenance attached to a diagnostic explains the records used in its present derivation. It need not name absent records whose future insertion could change that derivation. For example, a currently supported comparison atom may cite a completed search, but a later valid dominator certificate can rebut it. If dependency tracking lists only the current search nodes, the insertion is invisible.

We therefore distinguish:

```text
Prov_s(r,i)       current explanatory provenance for slot i
Read_s(r,i)       finite typed keys queried to instantiate and evaluate slot i.
```

The second object is derived from the operational evaluator. It is not another semantic input.

### 1.2 Key forms

For a fixed finite request/store environment, the following notation names source-tagged locations or relation indices. Immutable request-side values are resolved from `(e,q,P)` and mutable store-side values from `s`; the tag prevents an accidental identification of equally named locations from different sources. Arguments carry the exact plan, context, scope, criterion, mode, version, and record identity needed to type the query.

```text
LibIndex                         represented-plan membership index
Plan(e), Interface(e,q)          plan record and executable/frame interface
Profile(P), Slot(P,i)            profile schema and slot instantiation
Context(q), Fallback(q)          context parameters and fallback reference

CertIndex(a,m)                   all certificate/countercertificate ids for a in mode m
Cert(k), Current(k)              certificate payload and current-validity state
CorrIndex(k), PriorityIndex(a,m) correction closure and conflict/priority rules
Verifier(m), ModeRules(m)        accepted verifier version and evidence rules

RegionIndex(a), Region(k,a)      address-indexed quantitative regions
TraceIndex(a,m), Trace(t)        trace collection and trace record

EvalIndex(q), EvalEntry(q,d)     exact evaluated-set membership
SearchIndex(g,q,K,c)             searches for candidate g, set K, criterion c
Search(t), SearchCurrent(t)      search payload and validity/correction state
PairIndex(g,d,q,c)               pair-record collection, including an empty collection
Pair(g,d,q,c,k), Eligible(d,q,c) pair result/certificate and eligibility

WFKey(r,j)                       one of the finite well-formedness obligations.
```

An index key is read even when its collection is empty. Every event that inserts, removes, validates, invalidates, corrects, or reprioritizes a collection member must write the corresponding index key as well as the member key. This convention turns an absence test into an ordinary positive key read.

For a finite key set `R`, write

```text
Env(s;e,q,P) |_R
```

for the canonical typed projection containing the values of all keys in `R`, resolved from the combined request/store environment. Sets and maps are canonically ordered by their typed identifiers. Correction closure, validity, verifier version, and priority resolution are part of the projection rather than hidden procedural state.

### 1.3 Deterministic normalization

For each atom address `a`, let

```text
Norm_s(a,m)
```

be the deterministic normalization of all records named by the relevant indices after applying `Current`, correction closure, verifier version, and the declared priority/conflict rules. It returns the canonical set of current valid witnesses, counterwitnesses, and unresolved obstacles together with their transported provenance. If incompatible live evidence remains and no declared rule resolves it, normalization returns the `EvidenceConflict` obstacle.

This deterministic normalization is necessary for complete-diagnostic locality. A nondeterministic choice between two equivalent witnesses could change provenance while every record stayed fixed. Value locality would survive, but diagnostic locality would not.

## 2. Slot-level query/read footprints

Fix a request `r=(s,e,q,P)` and slot `i`. The footprint first includes the keys used by `theta_P(i)` to instantiate its exact address, then the keys read by that address's evaluator. For comparison slots, address formation reads `EvalIndex(q)` and the exact search-view identifier. Thus an evaluated-set change can change the slot address and cannot masquerade as an outside-footprint update.

All footprints below include the address, mode, verifier, current-validity, correction, priority/conflict, and relevant collection-index keys. Member keys are finite because `s` is finite.

### 2.1 Region atoms: `Adeq` and region-valued `Constraint`

For `a=Adeq(e,q,Acc,m)` or a region-valued `Constraint(e,q,C,m)`, `Read_s(r,i)` contains:

```text
Slot(P,i), Context(q), CertIndex(a,m), RegionIndex(a),
Verifier(m), ModeRules(m), PriorityIndex(a,m),
Cert(k), Region(k,a), Current(k), CorrIndex(k)
```

for every `k` named by the two indices. The normalized region is compared with the address's acceptable region. Missing regions, a live conflict, or a boundary-crossing region are open; subset inclusion supports; disjointness refutes.

### 2.2 Fallback improvement

For `a=Improve(e,F_q,Delta_q,q,m)`, the footprint contains the preceding certificate/region keys for both the candidate and the named fallback, plus

```text
Context(q), Fallback(q), Slot(P,i).
```

The scalar clause reads both interval endpoints and `Delta_q`. Vector or partial-order modes read the declared improvement relation and its version through `ModeRules(m)`.

### 2.3 Trace

For `a=Trace(e,q,m)`, the footprint contains

```text
TraceIndex(a,m), Verifier(m), ModeRules(m), PriorityIndex(a,m),
Trace(t), Current(t), CorrIndex(t)
```

for every indexed trace or countertrace `t`. A valid dependency-complete accepted trace supports; a valid hard counterwitness refutes; missing, invalid, expired, conflicted, or unresolved evidence is open.

### 2.4 Relative-undefeated comparison

Let

```text
a=RelUndom(g,q,K,c,m),  where K=Eval_s(q).
```

The footprint contains

```text
EvalIndex(q), EvalEntry(q,d)                         for d in K
SearchIndex(g,q,K,c), Search(t), SearchCurrent(t)    for indexed t
PairIndex(g,d,q,c), Eligible(d,q,c)                  for d in K
Pair(g,d,q,c,k), Cert(k), Current(k), CorrIndex(k)   for indexed k
Verifier(m), ModeRules(m), PriorityIndex(a,m).
```

A valid certified dominator refutes. In its absence, a valid declared search trace supports. A missing, invalid, expired, or conflicted search trace leaves the atom open. Unresolved non-dominator pairs may be reported without blocking relative-undefeated support, but their index keys remain in the footprint because a later valid dominator record can change the value.

### 2.5 Certified-undominated comparison

For `CertUndom(g,q,K,c,m)`, use the relative footprint and additionally read the current resolution of every relevant eligible pair. A valid dominator refutes; a valid exact-set search plus a non-dominating or ineligible resolution for every relevant pair supports; any unresolved relevant pair or invalid search leaves the atom open.

### 2.6 Well-formedness footprint

`WF` is not a meaningful atom, but public assessment also requires its finite footprint:

```text
Profile(P), Slot(P,i), LibIndex, Plan(e), Context(q), Interface(e,q),
the exact comparison-set/search-view identifiers, Fallback(q),
Verifier(m), ModeRules(m), and the referenced entity/version keys.
```

Missing evidence is represented by an open diagnostic *after* `WF`; a missing diagnostic record is not missing evidence but an invalid purported core state, because `Diag(r)` is total on every instantiated required and report slot.

## 3. Event-schema write footprints

For an event occurrence `u`, `Write(u)` is the finite set of keys it may change, including every affected collection index.

| event schema | mandatory writes |
|---|---|
| add evaluation/certificate/countercertificate | `CertIndex` or `RegionIndex`, new record, `Current`, correction/priority index if applicable |
| validate, invalidate, expire, retract, or correct evidence | `Current`, `CorrIndex`, affected collection index, successor record when present |
| change verifier or certificate convention | `Verifier` or `ModeRules` and the indices whose current normalization is invalidated |
| append, validate, invalidate, or correct a trace | `TraceIndex`, `Trace`, `Current`, `CorrIndex` |
| add a represented plan | `LibIndex`, `Plan`; no comparison key unless the plan is also evaluated for that exact context |
| add/remove/reevaluate a candidate for `q` | `EvalIndex(q)`, affected `EvalEntry`, exact-set search indices invalidated or replaced |
| append/invalidate/correct a search | `SearchIndex`, `Search`, `SearchCurrent`, `CorrIndex` |
| append/invalidate/correct a pair result or eligibility fact | `PairIndex`, `Pair` or `Eligible`, `Current`, `CorrIndex`, affected exact-set search index |
| change plan interface, context, profile, or slot parameters | the corresponding `Plan`/`Interface`/`Context`/`Profile`/`Slot` and `WFKey`; this forms a new request unless the declared update class permits it |
| archive-only or unrelated bookkeeping | only its own archive/bookkeeping keys |

The fixed-query update class in Task 14 retains `(e,q,P)`. The final two rows are included to make the boundary explicit, not to silently treat a changed substantive request as persistence of the old one.

## 4. The calculus-specific locality theorem

### Theorem 1: complete diagnostic locality

Fix a profile slot `i`, its declared evaluator/rule versions, fixed request-side inputs `(e,q,P)`, and two finite store states `s,s'` for which that request skeleton is meaningful. If

```text
Env(s;e,q,P) |_(Read_s(r,i)) = Env(s';e,q,P) |_(Read_s(r,i)),
```

including equality of the slot-instantiation keys, collection indices, member records, correction closure, current-validity state, verifier versions, and conflict rules, then the slot instantiates to the same address and

```text
Diag_s(r,i)=Diag_s'(r,i)
nu_s(r,i)=nu_s'(r,i).
```

For `WF`, equality on its footprint preserves either the same success or the same `WFDiag`.

**Proof.** Address equality follows from agreement on the instantiation keys. The atom cases then follow from the frozen clauses.

- **Region.** The certificate and region indices name the same finite records. Validity, correction, verifier, and priority agreement make `Norm_s=Norm_s'`. The same canonical region is therefore missing, conflicting, contained, disjoint, or boundary-crossing in both states, with the same witness/obstacle/counterwitness and provenance.
- **Improvement.** The same argument gives identical candidate and fallback regions; the fallback identity, margin, order, and mode version are equal, so the endpoint/relation comparison and complete diagnostic agree.
- **Trace.** Equal trace indices, trace records, validity/correction closure, and verifier rules produce the same accepted trace, hard counterwitness, or open obstacle.
- **Relative comparison.** `EvalIndex` agreement gives the same exact `K`. Search and pair indices include both extant and absent possibilities. Normalization therefore finds the same valid dominators and the same search validity. The precedence `valid dominator -> refuted`, otherwise `valid search -> supported`, otherwise open produces the same complete diagnostic.
- **Certified comparison.** In addition, every relevant pair has the same eligibility and current resolution, so the all-resolved test agrees.
- **Well formedness.** Each of the eight frozen obligations is a deterministic query of its listed keys, so the first failed canonical obligation—or success—is the same.

The diagnostic constructors are disjoint and normalization is deterministic, hence equality includes payload and transported provenance, not only the `K_3` constructor. `square`

### Corollary 2: disjoint-write frame rule

For an event `u:s->s'`, if

```text
Write(u) intersection Read_s(r,i) = empty,
```

then slot `i` retains its complete diagnostic and value. For a finite update path

```text
s_0 -u_0-> s_1 -u_1-> ... -u_(n-1)-> s_n,
```

the sufficient condition is state-indexed:

```text
Write(u_j) intersection Read_(s_j)(r,i) = empty
```

at every step. This formulation permits a footprint to grow after an evaluated-set or certificate-index update; such growth cannot evade the rule because the update changing the index intersects the pre-state footprint.

**Proof.** By the event contract, a key outside `Write(u)` has the same value before and after the event. Disjointness therefore gives the projection equality required by Theorem 1. Induct over a finite path. `square`

### Corollary 3: canonical graph change-completeness

For an update class `U`, construct `G_can(U)` using every reachable pre-state `t` and admitted event occurrence `u:t->t'`, with edges

```text
event u -> key k       iff k in Write(u)
key k -> slot i        iff k in Read_t(r,i) for some reachable pre-state t
slot i -> assessment   iff i is required
assessment -> grant.
```

Add the corresponding `WF` edges. Then `G_can` is change-complete for complete slot diagnostics, slot values, exact public assessment, and grant over every update class generated by the declared event contracts.

**Proof.** If a slot diagnostic changes along a finite path, some first step changes it. At that step, the contrapositive of Theorem 1 gives a changed pre-state footprint key. The event contract says that step's event wrote the key, yielding an event-to-key-to-slot path in the reachable-state union. Value change is a diagnostic-constructor change and uses the same path. Public assessment is a deterministic function of `WF` and required values, while grant is a deterministic projection of assessment, so any change in either has an extended path. `square`

Combining Corollary 3 with [`08_metatheory.md`](08_metatheory.md), Theorem 5, yields the promised calculus-specific persistence theorem:

```text
no allowed event reaches an observed coordinate
    => that diagnostic/value/assessment/grant coordinate is robustly invariant.
```

The converse still requires path realizability for that exact observable and update class. An archive insertion can be conservatively connected to a reliance request and yet be incapable of changing its grant.

## 5. Repairs to the stability package

### 5.1 Statistical stabilization uses a joint eventual index

In [`06_open_endedness.md`](06_open_endedness.md), Theorem 3 has two eventual hypotheses: eventual coverage and eventual diameter below the fixed margin. The proof must choose

```text
N=max(N_coverage,N_diameter),
```

not an index supplied by the diameter condition alone. The theorem and conclusion are otherwise unchanged.

### 5.2 The finite-announcement theorem is a regime theorem

The repaired Theorem 4 declares:

- a filtration `(F_n)`;
- a stopping time `tau`;
- a declaration `delta in {-,+}` that is `F_tau`-measurable, equivalently `{tau=n,delta=d} in F_n`; and
- error relative to the parameter regime `theta(P)<epsilon` versus `theta(P)>epsilon`.

It does not call the opposite declaration wrong merely because a possibly invalid interval process displays the opposite trajectory. A trajectory-level corollary requires the additional almost-sure coverage and shrinkage hypotheses of Theorem 3 under each law.

The countable-union/local absolute-continuity proof is elementary. Its stopping-time framing belongs to classical sequential analysis, represented here by Wald's foundational formulation of sequential tests (`Wald1945`). Confidence sequences and time-uniform coverage likewise have direct classical precedents (`DarlingRobbins1967`; `Robbins1970`). Bahadur and Savage's nonexistence result (`BahadurSavage1956`) is a related but stronger source-specific nonparametric impossibility and is not imported as this theorem. Kelly's convergence-in-inquiry framework (`Kelly1996`) is the closest existing project source for the distinction between convergence and knowing that convergence has arrived.

Accordingly, the finite-prefix and zero-error stopping arguments are classified as classical patterns restated in the project's continuation language. The project-specific contribution is their integration with profile-indexed licenses, the directional open-library result, and the separation of positive non-finality from stable refutation.

## 6. Repairs to profile completeness and representation

### 6.1 Base-local relative completeness

The independently realizable fragment in [`08_metatheory.md`](08_metatheory.md), Theorem 10, fixes a reference well-formed request base

```text
beta=(s,e,q)
```

and a finite address set containing `Req_beta(P) union Req_beta(Q)`. Realizing models vary the finite state but remain in the instantiation fiber `[beta]_(P,Q)`: both profiles stay well formed, instantiate to the same addresses, and use the same atom-refinement rules. Its semantic relation is therefore `P |=_prof^[beta] Q`, while the syntactic relation is `P >=_prof^beta Q`. The proof does not establish the uniform schema relation merely from one fiber. Schema-level completeness would need the base-local hypothesis uniformly at every base together with the existing `WF`-transfer condition.

“Independently realizable” is an explicit model-class hypothesis: for every support-downward-closed `D`, some finite well-formed model in the same instantiation fiber supports exactly `D` and may make every other address open. It is not asserted of arbitrary interacting atom families.

### 6.2 A concrete seven-vector core realization

Countermodel 13 can be instantiated with two same-scope region atoms

```text
a = Adeq(Acc_a=[0,0.05])
b = Adeq(Acc_b=[0,0.20]),
```

so `a =>_A b`. Address-indexed certificate regions realize the seven support-sound pairs as follows; `missing` produces an explicit open obstacle.

| `(nu(a),nu(b))` | `U(a)` | `U(b)` |
|---|---:|---:|
| `(-,-)` | `[0.21,0.22]` | `[0.21,0.22]` |
| `(-,?)` | `[0.06,0.07]` | `[0.19,0.21]` |
| `(-,+)` | `[0.15,0.18]` | `[0.15,0.18]` |
| `(?,-)` | `missing` | `[0.21,0.22]` |
| `(?,?)` | `missing` | `missing` |
| `(?,+)` | `[0.04,0.06]` | `[0.04,0.06]` |
| `(+,+)` | `[0.04,0.05]` | `[0.04,0.05]` |

The two forbidden vectors `(+,-)` and `(+,?)` violate the support projection. The construction uses the core's address-indexed regions `U_s(e,q,a)`; it does not claim that one shared physical confidence interval can take two values at once. If a certificate mode requires one shared region for both tolerances, additional refutation/open dependencies reduce the realizable set below seven, exactly as the relative-completeness caveat permits.

### 6.3 Canonical decoded normal form, not a literal datatype

Theorem 14's

```text
Ill(WFDiag) or Well([v]_F)
```

is a canonical decoded normal form. An exact representation need only admit a deterministic decoder to that form—or refine its observational equivalence. It need not literally contain a tag field or use that datatype internally.

The count

```text
1 + |V / ~_F|
```

is the number of distinguishable coarse public states. `ceil(log_2(1+|V/~_F|))` is a fixed-length **finite discrete-code** lower bound. It is not a lower bound on the width of a real-valued neural output: without precision, robustness, noise, decoder, or regularity restrictions, one real coordinate can name finitely many states.

## 7. Executable-kernel contract

The reference implementation now mirrors the repaired semantics:

1. `Diagnostic` enforces an actual disjoint sum: exactly one of support, obstacle, or counterwitness payloads is nonempty and agrees with `K_3`.
2. Relative and certified comparison helpers return open on a missing or invalid search trace when no valid dominator is present.
3. A well-formed request must have a diagnostic for every instantiated required and report slot. Missing evidence is encoded by an open diagnostic; a missing diagnostic record raises `DiagnosticCompletenessError` because the purported finite model violates totality.
4. The spurious-impact regression uses two real `EpistemicState` assessments plus a conservative provenance path rather than hardcoded booleans.
5. The component-composition regression constructs component and composite requests whose actual assessments are respectively granted and refused; it is no longer only arithmetic.
6. The executable typed-footprint witness checks negative collection-index reads, disjoint-write invariance, and evaluated-set/search/pair invalidation keys. These are regression witnesses for the definitions and case proof, not proof-assistant verification.

## 8. Result classification and project impact

| result | classification | project role |
|---|---|---|
| typed complete-diagnostic locality | calculus-specific case theorem | closes the main Task 14B proof gate |
| disjoint-write frame rule | direct corollary | implementation/neural dependency contract |
| canonical graph change-completeness | calculus-specific corollary | makes Task 14's abstract persistence result applicable |
| necessity under path realizability | previously proved abstract characterization | remains instance- and observable-relative |
| statistical index and stopping-time repairs | correctness repairs | preserve the scoped Task 12 results |
| Wald/Darling–Robbins/Robbins positioning | primary-source classification | removes novelty overstatement |
| base-local completeness notation | statement repair | prevents an invalid schema-level reading |
| seven-vector table | concrete finite witness | makes the representation correction self-contained |
| decoded-tag and discrete-code clarification | scope repair | prevents a false neural-width inference |
| kernel/test changes | executable conformance | protects the formal interface; not an independent theorem |

No inherited claim is newly falsified here. The accepted claims were already mathematically sound at their intended scope; this task closes statement, attribution, applicability, and executable-conformance gaps. The main project impact is positive: the update cluster now counts as a theorem of the actual license calculus, and Task 15 may use typed dependency-scoped atom inputs without assuming that current provenance is a complete future-influence map.

## Task conclusion

The focused repair succeeds. Every frozen atom clause now has a finite typed query/read footprint with explicit negative reads; every declared event exposes its writes; agreement on the footprint preserves the complete diagnostic; and the canonical graph is change-complete. The abstract impact-cone theorem is therefore connected to the actual calculus, while the necessity direction remains honestly conditional.

The stability, profile, and representation repairs remove the remaining local overstatements without enlarging the ontology. Task 14C may now build proof-carrying recursive plans on a theorem spine whose update contract is both mathematically stated and executable.
