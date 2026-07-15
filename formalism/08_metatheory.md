# Metatheory of the Compact License Calculus

Status: Task 14 proof and countermodel audit

Date: 2026-07-12

Depends on: [`07_core_calculus.md`](07_core_calculus.md), [`06_open_endedness.md`](06_open_endedness.md), and the executable [`WF + K_3` reference](../verification/README.md)

> **Task 14A extension notice.** [`08a_transport_routing.md`](08a_transport_routing.md) supplies the quantitative subdomain, router, bridge/blend, and finite plan-DAG propagation theorems requested by this audit.

> **Task 14B repair notice.** [`08b_audit_repairs.md`](08b_audit_repairs.md) defines typed query/read and event/write footprints, proves complete-diagnostic locality and canonical graph change-completeness for the frozen atom clauses, repairs Theorem 10's base-local statement, and clarifies Theorem 14's decoded normal form and finite discrete-code bound.

## Durable result summary

This file audits the Task 13 calculus rather than adding another ontology. It proves three characterization/separation clusters, with the stricter paper-contribution tally qualified by Checkpoint B.

1. **Robust update persistence is now instantiated for the calculus.** For a declared update class, absence of a canonical event-to-key-to-slot path is sufficient for invariance because Task 14B proves every frozen evaluator local to its typed read footprint and the canonical graph change-complete. Absence is also necessary when every reachable observed coordinate has a realizing allowed status-changing path. Without that path realizability, a spurious dependency edge gives a finite countermodel to necessity. Diagnostic equality, atom-value equality, public-status equality, and continued grant require different observables.
2. **The typed atom and profile refinements are sound.** In the finite independent-atom fragment, they are relatively complete: whenever the syntactic profile refinement fails, a finite down-set model grants the alleged stronger profile and withholds the alleged weaker one. The completeness direction deliberately excludes unrepresented conjunctive interactions among atoms.
3. **The minimal status representation is the quotient induced by the supported profile queries.** If singleton profiles are available, the quotient is equality on the set `V` of realizable atom vectors. Hence the exact number of distinguishable meaningful states is `|V|`. It becomes `3^n`, with worst-case fixed-length cost `ceil(n log_2 3)` bits, only when all `3^n` ternary vectors are realizable. Singleton availability alone does not imply independence; a two-atom refinement countermodel has seven rather than nine realizable vectors.

The audit also proves the `WF + K_3` normal form, scoped four-outcome minimality, exact limits of the safety projections, typed elaboration invariance, label preservation, tolerance monotonicity, raw history heredity, profile-local comparative defeat, and finite acyclic plan reification. It gives countermodels to unqualified world-factivity, target-safe fallback, unrestricted update persistence, global closure from finite search, unconditional component-license composition, and implicit cyclic self-reference.

No primitive core carrier is added. Two Task 13 phrases are narrowed:

- the `3^n` lower bound is a worst-case independent-realizability result, not a consequence of singleton profiles alone; and
- “safe fallback” means no unlicensed expert is used on a certified gap, not that the fallback has low target-world loss without a separate certificate.

The finite cardinality and separation witnesses are executable in [`verification/test_metatheory.py`](../verification/test_metatheory.py).

## 1. Scope and notation

Fix the Task 13 core. A request is

```text
r=(s,e,q,P).
```

For a well-formed request, each required or report slot receives one value in

```text
K_3={-,?,+},     - < ? < +,
```

and required values aggregate by finite meet. `-`, `?`, and `+` mean refuted, open, and supported. They are operational evidence states, not target truth values.

Profiles have stable slot identities even when a slot's instantiated address depends on `s`. This matters for comparison atoms: adding a model may change `Eval_s(q)` and therefore the parameters of the atom occupying the same profile slot. For a fixed `(e,q,P)`, define the slot-indexed value and diagnostic views

```text
Val_s^P(i)  = nu_s(e,q,theta_P(i;s,e,q))
Diag_s^P(i) = diagnostic at theta_P(i;s,e,q).
```

Diagnostics at different states are compared after transporting old provenance identifiers through the history embeddings. This avoids declaring a diagnostic changed merely because an append-only store renamed a node.

The term **realizable** always means realizable by a finite core model satisfying the frozen typing, diagnostic, and atom-semantics conditions. When a theorem uses an abstract independent-atom fragment, that extra hypothesis is stated.

## 2. Status normal form and elementary algebra

### Theorem 1: two-phase normal form

Every core request receives exactly one public outcome:

```text
Undefined  iff not WF(r)
Refused    iff WF(r) and mu(r)=-
Withheld   iff WF(r) and mu(r)=?
Granted    iff WF(r) and mu(r)=+.
```

**Proof.** `WF(r)` is Boolean. If it fails, meaningful atom evaluation is not invoked. If it holds, the nonempty finite required family has a unique meet in the total chain `K_3`. That meet is exactly one of `-`, `?`, and `+`, and the displayed cases are disjoint and exhaustive. `square`

### Proposition 2: meaningful conjunction algebra

Finite required-atom aggregation is commutative, associative, idempotent, and monotone in every coordinate.

**Proof.** The meet is minimum on the chain `- < ? < +`. Minimum on a total order has all four properties. Under the relabeling `- -> false`, `? -> undefined`, and `+ -> true`, this is the finite Strong-Kleene conjunction algebra. The result imports no interpretation of evidence and no source completeness theorem. `square`

### Theorem 3: scoped four-outcome minimality

Suppose the observable contract asks for the exact public `Assess` result and the model class realizes:

1. one ill-formed request;
2. one well-formed singleton request with value `-`;
3. one well-formed singleton request with value `?`; and
4. one well-formed singleton request with value `+`.

Then every exact representation of that observable has at least four distinguishable states.

**Proof.** The four requests produce four different required outputs. If any pair shared a representation, a deterministic decoder would have to return two outputs on the same representation. `square`

This is observational minimality, not metaphysical minimality. If callers ask only “may act?” then `Granted` versus non-`Granted` needs two outputs. If `WF` is guaranteed upstream, three outputs suffice. The four-way interface is minimal exactly for clients that must distinguish malformed, countercertified, unresolved, and supported requests.

### Proposition 4: exact scope of safety projections

For a well-formed request, `Alarm(r)` preserves every complete refuted safety diagnostic and `PendingSafety(r)` preserves every complete open safety diagnostic. Given the known safety-address set, their domains also recover the `K_3` value of every safety atom: absence from both projections means supported. They do not recover the witness/provenance payload of a supported safety atom, nor any nonsafety diagnostic.

**Proof.** Both objects are literal restrictions of `Diag(r)`, so records in their selected domains are unchanged. Totality of meaningful atom valuation gives the value reconstruction. Restriction discards the omitted payloads, so no stronger reconstruction follows. `square`

Thus the projections are lossless for actionable safety exceptions, not a lossless compression of the whole diagnostic vector.

## 3. Robust update persistence

### 3.1 Update classes and observables

Fix a starting state `s`, a request skeleton `(e,q,P)`, and a class `U` of allowed finite update paths beginning at `s`. Paths retain `(e,q,P)` but may change finite records, the library, valid support, searches, and slot parameters derived from the state.

An **observable** is a finite-coordinate function `O` on path endpoints. Important cases are:

```text
O_diag    transported slot-indexed diagnostic records
O_val     slot-indexed K_3 values
O_assess  the four-way public status
O_grant   the Boolean predicate Assess=Granted.
```

For coordinate set `C`, write

```text
RobustInv(O,s,U,C)
```

when every allowed path endpoint has the same `O` coordinates in `C` as `s`.

An **impact graph** `G` has vertices for allowed event schemas, support/dependency nodes, profile slots, and, when needed, aggregate output coordinates. Let

```text
Cone_G(U)
```

be the observed coordinates reachable from an event schema that may occur on a path in `U`.

The graph is **change-complete for `O`** when every actual change of an observed coordinate along an allowed path has a graph path from one of that path's update events to that coordinate. It is **path-realizable for `O` over `U`** when every observed coordinate in `Cone_G(U)` is changed by at least one allowed path. Completeness says the graph misses no real influence; realizability says it contains no behaviorally inert influence path for the chosen observable and update class.

These properties are indexed by `O`. A new support witness can change `O_diag` while leaving `O_val`, `O_assess`, and `O_grant` unchanged.

### Theorem 5: robust impact-cone characterization

Let `G` be change-complete for `O` over `U`. Then

```text
Cone_G(U) intersection C = empty
    implies RobustInv(O,s,U,C).
```

If `G` is also path-realizable for `O` over `U`, then

```text
RobustInv(O,s,U,C)
    iff Cone_G(U) intersection C = empty.
```

**Proof.** For sufficiency, suppose some allowed path changes a coordinate in `C`. Change-completeness supplies a graph path from an event on that path to the changed coordinate, putting it in `Cone_G(U) intersection C`, contradiction.

For necessity under path realizability, suppose `c` lies in the intersection. Realizability supplies an allowed path changing `O_c`, contradicting robust invariance. `square`

The theorem applies independently to complete diagnostics, ternary atom values, exact public assessment, or continued grant. It is not sound to use a diagnostic-level cone as a necessary condition for continued grant: a provenance refresh can replace one valid support witness with another while every required value remains `+`.

[`08b_audit_repairs.md`](08b_audit_repairs.md), Theorem 1 and Corollary 3, discharge this theorem's calculus-specific premise. Each frozen slot evaluator is a deterministic function of its finite typed read projection, negative reads use collection-index keys, and every event writes each index it can affect. The resulting event-to-key-to-slot graph is change-complete for diagnostics, values, assessment, and grant. Path realizability remains an additional observable- and update-class-relative hypothesis.

### Countertheorem 6: path absence is not necessary without realizability

There is a finite change-complete impact graph and update class for which `RobustInv` holds although the impact cone meets the observed coordinate set.

**Countermodel.** Let `U` contain one transition `s -> s'`. One atom `a` is supported by the same still-valid certificate at both states, so `O_val(s,a)=O_val(s',a)=+`. Put an edge from the appended bookkeeping event `u` to `a` in `G`, perhaps because a conservative static analyzer treats every event in the same record table as potentially relevant. The graph is change-complete vacuously: no actual value change is missed. Its cone contains `a`, but the value is invariant on every allowed endpoint. The edge is not path-realizable for `O_val`. `square`

**Project consequence.** Dependency graphs used by the neural or implementation layer may safely overapproximate influence for conservative persistence, but they cannot support an “if and only if” explanation unless their reachable paths are validated as realizable for the exact observable being explained.

### Corollary 7: grant persistence

If the starting request is granted, use `O_grant` with its single output coordinate. Under change-completeness and path realizability,

```text
every U-continuation remains Granted
iff no admissible event reaches the grant coordinate.
```

Using `O_diag` instead yields the stronger claim that all required diagnostic records, including transported provenance payloads, remain identical.

## 4. Atom and profile refinement

### Theorem 8: soundness of the frozen atom rules

Every derivable core refinement

```text
a =>_A b
```

is sound for support:

```text
nu(a)=+ implies nu(b)=+
```

whenever both addresses are meaningful under the stated common-scope side conditions.

**Proof.** Check the generators.

- **Acceptable regions.** If `U subseteq Acc_1` and `Acc_1 subseteq Acc_2`, then `U subseteq Acc_2`.
- **Fallback margins.** If `sup(U_e)+Delta_1 <= inf(U_F)` and `Delta_1>=Delta_2`, then `sup(U_e)+Delta_2 <= inf(U_F)`.
- **Constraints.** If the certified region lies in `C_1` and `C_1 subseteq C_2`, it lies in `C_2`.
- **Trace modes.** The rule exists only when a declared verifier/provenance projection maps every `m_1` support witness to an `m_2` support witness.
- **Comparison.** A supported `CertUndom(g,K)` has a valid search trace and resolves every relevant member of the exact set `K` as non-dominating or ineligible. Therefore no valid certified dominator exists in `K`, and the canonical witness projection supports `RelUndom(g,K)`.

Identity is sound, and sound implications compose under transitivity. `square`

Exact scope, loss, frame, certificate mode, candidate, fallback, and evaluated-set conditions are theorem hypotheses. Dropping them invalidates the proof.

### Corollary 9: profile grant antitonicity

If

```text
P >=_prof^beta Q
```

at `beta=(s,e,q)`, both requests are well formed, and `P` is granted, then `Q` is granted.

**Proof.** Every required `Q` atom has a required `P` witness that entails it. Grant of `P` supports every such witness; Theorem 8 supports every required `Q` atom; their meet is `+`. `square`

The uniform schema result follows from the schema-level well-formedness condition in Task 13.

### 4.1 Base-local independent-atom fragment

Fix a reference well-formed request base `beta=(s,e,q)`, profiles `P,Q`, a finite address set `A` containing their instantiated requirements, and the derivable atom preorder `=>_A`. A base `beta'=(s',e,q)` lies in the **instantiation fiber** `[beta]_(P,Q)` when `P` and `Q` are well formed there, instantiate to the same typed addresses as at `beta`, and use the same atom-refinement rules. A supported set is **downward closed** when

```text
a is supported and a =>_A b  implies b is supported.
```

The base-local model class is **independently realizable** when every downward-closed subset `D` of `A` occurs in some finite well-formed core model at a base `beta_D` in `[beta]_(P,Q)` whose supported addresses are exactly `D`; unsupported addresses may all be open. This is an explicit fragment hypothesis, not a claim about every family of operational atoms. It excludes extra semantic laws in which a conjunction of incomparable atoms entails a third atom.

Define semantic profile grant entailment on this fragment by

```text
P |=_prof^[beta] Q
```

iff every model in this base-instantiation fiber that grants `P` grants `Q`.

### Theorem 10: relative completeness and finite separation

On the finite independently realizable fragment in the instantiation fiber of `beta`,

```text
P |=_prof^[beta] Q  iff  P >=_prof^beta Q.
```

When the syntactic relation fails, a finite separating model grants `P` and withholds `Q`.

**Proof.** The right-to-left direction is Corollary 9.

For the converse, suppose `P >=_prof^beta Q` fails. Then some `b in Req_beta(Q)` has no `a in Req_beta(P)` with `a =>_A b`. Let

```text
D = {c in A : some a in Req_beta(P) satisfies a =>_A c}.
```

`D` is downward closed, contains every required `P` atom by identity, and omits `b`. Independent realizability supplies a finite model supporting exactly `D`; assign `?` with an explicit `IndependentOpen` obstacle to every address outside `D`. The model grants `P`. It leaves required `b` open and has no refuted required `Q` atom, so it withholds `Q`. Hence semantic entailment fails. `square`

The result is relative rather than absolute and base-local rather than automatically schema-uniform. The fiber is essential: valuations vary with `s_D` while the instantiated addresses and rules being compared remain fixed. A schema-level completeness theorem would require this hypothesis at every relevant base plus the `WF`-transfer condition in the definition of `>=_prof`. If the semantics contains a genuine conjunctive rule such as `a_1 and a_2 |= b` but the syntax contains only unary atom refinements, `P={a_1,a_2}` can semantically entail `{b}` without a matching antecedent. The remedy would be a typed conjunctive rule, not a false claim that unary matching is complete everywhere.

## 5. Minimal status representation

### 5.1 Query-induced quotient

Fix a well-formed base and a finite meaningful address universe

```text
A={a_1,...,a_n}.
```

Let

```text
V subseteq K_3^n
```

be the set of atom-state vectors realizable by the intended core-model class. Let `F` be the supported finite profile-query family. Each `P in F` induces a public-status query `Q_P:V -> {Refused,Withheld,Granted}` by finite meet.

Define

```text
v ~_F v'
iff Q_P(v)=Q_P(v') for every P in F.
```

### Theorem 11: coarsest sufficient quotient

`V / ~_F` is the unique coarsest deterministic representation, up to bijective renaming, sufficient to answer every query in `F` exactly.

**Proof.** The quotient is sufficient because every `Q_P` is constant on each equivalence class by definition. If a sufficient representation identifies `v` and `v'` from different classes, some `P` gives different answers on them, so its decoder cannot be correct on both. Therefore every sufficient representation refines `~_F`. `square`

This is the exact answer to “where the status information must live” for a declared query family. A smaller family permits more compression. For example, if `F` contains only one profile requiring all atoms, every vector is summarized by its three-valued meet.

### Theorem 12: singleton separation and the corrected bit bound

Suppose `F` contains a well-formed singleton profile `P_i` requiring only `a_i` for every `i`. Then

```text
v ~_F v' iff v=v'
```

on `V`. Consequently every exact code has at least `|V|` distinguishable meaningful codewords and worst-case fixed-length binary size

```text
ceil(log_2 |V|).
```

If, in addition, the atoms are fully ternary-independent so that `V=K_3^n`, then

```text
|V|=3^n
ceil(log_2 |V|)=ceil(n log_2 3).
```

**Proof.** A singleton query returns `Refused`, `Withheld`, or `Granted` exactly according to whether its coordinate is `-`, `?`, or `+`. If two vectors differ, the singleton at a differing coordinate separates them. The counting and binary-code bound follow from injectivity. `square`

The real-valued quantity `n log_2 3` is the information logarithm; a fixed-length bit string has the displayed ceiling.

### Countermodel 13: singleton profiles do not imply `3^n`

Let `n=2` and take the finite abstract support-only fragment whose model class realizes every ternary assignment consistent with one sound atom refinement

```text
a =>_A b.
```

Semantic soundness forbids the two vectors

```text
(a,b)=(+,?) and (+,-).
```

The remaining seven vectors are realizable by construction. A concrete core instance uses same-scope address-indexed region certificates for `a=Adeq([0,0.05])` and `b=Adeq([0,0.20])`; [`08b_audit_repairs.md`](08b_audit_repairs.md), Section 6.2, gives all seven pairs of regions and explicit missing-evidence cases. Singleton profiles distinguish all seven, but there are not nine realizable states. Thus the unconditional inference

```text
singletons available  implies  3^n realizable states
```

is false. `square`

**Project impact.** Task 17's factorization theorem uses the actual query quotient and preserves this restriction. A `3^n` worst case requires `n` independently realizable atoms; finite discrete-bit counts are not converted into real neural-width bounds.

### Theorem 14: canonical decoded well-formedness separation

To answer the four-way public query over both well-formed and ill-formed requests, the following is a canonical decoded normal form:

```text
Ill(WFDiag(r))
or
Well([v]_F).
```

Any exact representation must decode to this form or refine its observational equivalence; it need not literally store a tag or use this datatype internally. If all well-formedness failures are intentionally collapsed to one public `Undefined`, the coarse state count is

```text
1 + |V / ~_F|.
```

If callers require the failed obligation, detail, and provenance, the `Ill` branch must additionally preserve the corresponding quotient of `WFDiag` records.

**Proof.** `K_3` is defined only after `WF`; no meaningful ternary vector can determine which typing/denotation/executability obligation failed. Conversely the canonical decoder's branch and payload answer the requested observation. Any exact code identifying observations from different branches, or different required classes inside a branch, would make exact decoding impossible. The counting result follows. `square`

Full diagnostic explanation is larger than this status quotient. Witnesses, counterwitnesses, obstacles, certificate modes, and provenance can vary while `v` is fixed. The theorem is not a bit bound for complete audit records. Moreover, `ceil(log_2(1+|V/~_F|))` is only a fixed-length finite discrete-code bound. It is not a lower bound on real-valued neural output width without additional precision, robustness, noise, decoder, or regularity restrictions.

## 6. World/state separation and soundness

Let `Target_w(a)` be the world-level property associated with a meaningful atom, such as `Risk_w(e,q) in Acc_q`. A certificate mode `m` declares a class `C_m` of admissible `<w,s>` pairs and an exact bridge condition, deterministic or probabilistic.

### Theorem 15: mode-scoped soundness schema

If mode `m` satisfies

```text
for every <w,s> in C_m,
Support_m(s,a) implies Target_w(a),
```

then a supported `m`-atom in any pair in `C_m` has its target property. A statistical mode obtains only its stated probability/coverage conclusion on its declared sampling law.

**Proof.** Immediate instantiation of the mode bridge. `square`

This is a theorem schema whose substance lies in proving the certificate-mode premise. Deterministic proof checking, confidence bounds, Bayesian posterior claims, and conformal guarantees do not share one unqualified premise.

### Countertheorem 16: operational support is not universally factive

The unqualified rule

```text
nu_s(a)=+  implies Target_w(a)
```

is invalid on the core model class.

**Countermodel.** Take one finite state `s` containing a currently valid certificate that operationally supports `Adeq(e,q,m)`. Put two worlds `w_0,w_1` over that same state. Let `Risk_{w_0}(e,q)` lie in `Acc_q` and `Risk_{w_1}(e,q)` lie outside it. Operational assessment is computed from `s`, so the atom is supported in both pairs; the target property holds only in the first. Excluding the second pair requires a mode-specific soundness assumption. `square`

**Project impact.** The paper must call `Lic_P` a finite-stage warrant, not truth. Neural targets may reproduce or calibrate operational status, but target-world adequacy requires a separately validated certificate bridge and distributional assumptions.

## 7. Label preservation and scoped non-explosion

### Theorem 17: licensed-output label preservation

In the core proof system generated by `USE`, `WEAKEN-PROFILE`, and `FALLBACK`, every model-produced conclusion retains an `[e,q]` label and a request authorization label. No derivation concludes an unqualified `True_w(phi)` unless a new bridge or truth-detachment rule is added.

**Proof.** Induct on derivation length. `USE` introduces both labels. `WEAKEN-PROFILE` changes only the authorization profile and preserves `(e,q)`. `FALLBACK` returns an action rather than an unqualified proposition. No core rule erases the labels or introduces `True_w`. `square`

### Corollary 18: cross-label disagreement does not globally explode

From authorized outputs

```text
[e_1,q_1]phi
[e_2,q_2]not-phi
```

the core does not derive an arbitrary unlabelled `psi`, or an arbitrary output under a third label, absent a bridge rule with such a conclusion.

This is label conservativity, not a claim that every object logic is paraconsistent. If one local model's own premises are inconsistent and its object logic is classical, it may derive every formula under its own `[e,q]` label. The core prevents that local explosion from becoming unqualified global truth.

## 8. Tolerance, fallback, heredity, and comparative defeat

### Theorem 19: tolerance monotonicity

Fix the plan, scope, loss, aggregation, certificate mode, and certificate region. If

```text
Acc_1 subseteq Acc_2,
```

then support for `Adeq(Acc_1)` entails support for `Adeq(Acc_2)`. In scalar smaller-is-better contexts, `epsilon_1<=epsilon_2` gives this inclusion.

If a granted profile request changes only this adequacy parameter and all other required slots remain well formed with identical supported diagnostics, the looser request is granted.

**Proof.** The atom claim is Theorem 8. The profile claim follows because every required atom of the new request is supported. `square`

Changing fallback, margin, frame, sampling scope, certificate mode, or constraints at the same time creates no monotonicity theorem.

### Theorem 20: operational gap fallback

For an action-authorizing request, if

```text
Act(s,q,P,x)=empty,
```

then the core selector cannot return `Use(e,x)` for any library plan. It may return only the explicit `F_q` or a declared abstention/information action.

**Proof.** This is the `FALLBACK` rule and the absence of any other action-producing rule on an empty active set. `square`

### Countermodel 21: fallback is not automatically target-safe

Let the active set be empty and let `F_q` be “maintain status quo.” Choose a world in which maintaining the status quo has catastrophic loss. The selector obeys Theorem 20 but the fallback is not target-safe.

Thus “safe fallback” means safe with respect to the operational no-unlicensed-use policy unless `F_q` itself carries a world-linked safety certificate. This is why fallback identity, expected cost, and evidence remain explicit.

### Theorem 22: raw heredity without current-status monotonicity

For every transition `s -> s'`, old history/provenance nodes remain addressable through the injective embedding `iota`. Nevertheless neither atom value nor public assessment is monotone along `->`.

**Proof.** Raw heredity is a transition axiom. For nonmonotonicity, append a correction invalidating the only support witness for an atom: `+ -> ?` while the old witness remains historically present. Alternatively append a valid countercertificate: `+ -> -`. A profile requiring the atom changes from Granted to Withheld or Refused. `square`

### Theorem 23: comparative defeat is profile-local

Suppose an `AddModel` update adds and validly evaluates `d`, certifying that `d` dominates `e` on the exact comparison scope, while preserving adequacy, fallback, constraints, and trace support for `e`. Then:

- a profile requiring `RelUndom` or `CertUndom` for `e` is refused;
- a profile that reports but does not require that comparison records the refusal without changing its top-level assessment; and
- a reliance profile with no comparison slot is unchanged.

**Proof.** The dominator is a valid counterwitness for both comparison atoms. Finite meet changes only when the atom is required. Report-only slots do not enter the meet. `square`

This settles the earlier basic-warrant/preferred-use subtlety without requiring one interpretation for every application: the requesting profile determines whether comparative defeat affects authorization.

## 9. Failure of unrestricted update persistence and global closure

KLM rational monotony is a postulate about premise-indexed nonmonotonic consequence. The core's principal nonmonotonicity is instead indexed by epistemic-state transition. No literal KLM theorem is asserted. The relevant structural analogue is the following unrestricted persistence principle:

```text
if a request is Granted at s,
then every history-preserving extension consistent with old records
keeps it Granted.
```

### Countertheorem 24: unrestricted rational-style persistence fails

The displayed principle is false.

**Countermodel.** At `s`, let `P_pref-rel` be granted for `e`. Extend the history by adding a newly evaluated `d` that dominates `e`, without retracting or contradicting any old observation. By Theorem 23, the preferred-use request becomes Refused. The update is consistent with the old finite claim “no certified dominator was present in the old evaluated set”; it enlarges the relevant evaluated set. `square`

**Project impact.** State expansion and premise enrichment must not be conflated. Persistence requires the Task 14 impact conditions or a narrower frozen update class; neither append-only history nor absence of contradiction with old records suffices.

### Countertheorem 25: finite search does not yield global closure

No core rule validly derives

```text
GlobalUndominated(e)
```

from a supported `RelUndom(e;g,K)` or `CertUndom(e;g,K)` over finite `K`.

**Countermodel.** Keep the same finite state, evaluated set `K`, and supported finite comparison atom. Consider a compatible world or continuation containing an unrepresented plan `d` that dominates `e`. Every finite diagnostic remains the same before `d` is represented, but the global conclusion is false. `square`

**Project impact.** The neural system must preserve evaluated-set/search scope and may predict only profile-indexed finite comparison status. An external registry can expand; no output bit may silently mean “globally best possible.”

## 10. Typed elaboration and recursive plan structure

> **Task 14C extension notice.** The results below establish finite reification, conditional quantitative propagation, and failure of unconditional license composition. [`08c_proof_carrying_plans.md`](08c_proof_carrying_plans.md) now supplies the stronger positive result: typed plan constructors transform payloads, quantitative grades, and certificate/provenance terms by topological induction; a checked root certificate lifts into an ordinary core request; and a frozen value-logic implementation has a unique grounded assessment under finite-rank evidence dependencies.

### Theorem 26: typed elaboration invariance

Let detailed records `D_1,D_2` compress to the same core request:

```text
C(D_1)=C(D_2)=(s,e,q,P).
```

Suppose detailed and core `WF` agree, and every required/report atom maps to the same address, `K_3` value, and transported diagnostic payload. Then the detailed and core public assessments agree. The canonical elaboration `J` therefore satisfies

```text
Assess(C(J(r)))=Assess(r)
```

for every core request, up to identifier renaming.

**Proof.** On `WF` failure both sides return `Undefined`. Otherwise they have the same finite required value vector, hence the same meet and public result. Diagnostic agreement gives the stated audit preservation. Task 13 already gives `C(J(r))=r` up to renaming. `square`

Extension fields not read by `C` need not be reconstructible; the theorem is assessment invariance, not record isomorphism.

### Theorem 27: finite acyclic plan reification

Let `G_e` be a finite directed acyclic graph of typed executable components. Suppose every edge has a matching output/input interface, all leaves denote, every node operation terminates on the requested cases, and the graph supplies a defined composite output, cost/resource record, frame, and provenance trace. Then the composite can be reified as one core use plan `e_G in E` and assessed by an ordinary request.

**Proof.** Topologically order the finite DAG. Inductively execute each node after its predecessors; interface matching supplies a typed input, and termination supplies an output. The root output, accumulated declared cost/resource data, composite frame map, and concatenated provenance define the dependent interface of one versioned executable plan. The core is indifferent to whether that interface was primitive or elaborated. `square`

This is a closure property of the carrier interface, not of licenses.

### Countertheorem 28: component grants do not compose unconditionally

There are two individually adequate components whose composition is inadequate under the outer task.

**Countermodel.** On a scalar quantity, let component `f` introduce error `0.06` and component `g` introduce another same-direction error `0.06`. Give each component its own well-formed adequacy request with tolerance `0.10`; both are supported. Under the composite request, the output error is `0.12`, so adequacy at `0.10` is refuted. All nonadequacy requirements can be held supported. `square`

Correlated errors, unit/frame mismatch, nonlinear amplification, and combined computation cost give further separators. [`08a_transport_routing.md`](08a_transport_routing.md), Theorem 15, supplies a positive finite-DAG composition bound under tube-valid local errors and downstream Lipschitz sensitivities.

**Project impact.** A plan-DAG encoder may expose component statuses for explanation, but the symbolic decoder must consume an independently certified composite atom or a proven propagation certificate. It must not compute composite grant by simply meeting component grants.

### Proposition 29: higher-order evaluation is typed without internal cycles

A fallible loss or consequence estimator can be represented as a plan `e_L` and assessed by another request `(s,e_L,q_L,P_L)`. The original context still names its target criterion `L_q`; the estimator and its evidence remain separate. Any finite well-founded tower of such requests is admitted by repeated application of Theorem 27.

### Counterexample 30: implicit cyclic self-reference is underdetermined

If a Boolean grant variable `g` is stipulated to satisfy `g=not g`, it has no Boolean fixed point. If it is stipulated to satisfy `g=g`, it has two. A three-valued extension may add an open fixed point but still changes the semantics and does not choose a unique operational result. Therefore a cycle in which a request determines the loss/evidence used to determine itself requires an explicit fixed-point space, operator, existence/uniqueness conditions, and selection rule. It is not an ordinary core request.

**Project impact.** Recurrent or self-evaluating neural implementations must expose their update operator and stopping/fixed-point convention. A converged activation is not automatically a licensed self-justification, and the finite core decoder must not be applied to an unresolved cycle as though it were an acyclic request.

## 11. Result classification and surviving theorem spine

| result | classification | paper role |
|---|---|---|
| `WF + K_3` normal form and meet algebra | definition plus standard finite-lattice fact | supporting infrastructure |
| scoped four-outcome minimality | finite observation-separation lemma | interface justification |
| safety projection scope | exact restriction lemma and limitation | audit/safety interface |
| typed locality plus robust impact-cone iff under realizability | calculus-specific case theorem, change-complete graph corollary, abstract necessity characterization, and finite countertheorem | paper-carrying update/frame-rule cluster; necessity remains instance-relative |
| atom/profile soundness | core soundness theorem | necessary metatheory |
| independent-fragment relative completeness | new finite separating characterization | paper-carrying core result |
| query-induced diagnostic quotient | new sufficient-statistic characterization | paper-carrying core result |
| conditional `3^n` / bit bound | worst-case corollary plus countermodel to overstatement | representation bridge |
| mode-scoped soundness | conditional theorem schema | certificate-family obligation |
| unqualified factivity failure | two-world countermodel | central philosophical limit |
| label preservation/non-explosion | syntactic conservativity theorem | logic qualification |
| tolerance, fallback, heredity, profile-local defeat | elementary conditional results | sanity/interface checks |
| unrestricted persistence/global closure failures | finite continuation countermodels | open-endedness qualifications |
| elaboration invariance and DAG reification | structural induction | core/elaboration bridge |
| component-grant and cyclic-self-reference failures | finite counterexamples | recursive-modeling limits |
| proof-carrying plans and stratified system assessment | standard finite inductions plus project-specific license integration | Task 14C positive recursive-computation bridge |

Checkpoint B applies a stricter tally than theorem count alone. Task 14B has now repaired and classically positioned the stability package, and its typed locality/change-completeness theorem makes the update cluster a result about the actual atom clauses. Together with profile relative completeness, the three-cluster pre-neural theorem bar is cleared. The diagnostic quotient remains a representation bridge, while Task 14A is load-bearing integration of mostly standard machinery rather than a novelty headline. Task 17 subsequently establishes the scoped positive/negative neural representation cluster in [`ml/03_representation_theorems.md`](../ml/03_representation_theorems.md) rather than relying on this formal minimum.

## 12. Decisions carried forward

1. No Task 13 core carrier is added or removed.
2. Impact/dependency claims are always indexed by update class and observable.
3. Graph path absence is conservative; necessity requires path realizability.
4. Atom refinement is support-preserving, not a complete three-valued implication calculus.
5. Profile refinement is relatively complete only for the declared independent-atom fragment.
6. The minimal representation is the query-induced quotient of the realizable vector set.
7. `3^n` and `ceil(n log_2 3)` require full ternary independence; singleton profiles alone yield `|V|`.
8. `WF` and its derivation remain outside the meaningful ternary channel.
9. Operational support is not target truth without a certificate-mode bridge.
10. Label preservation gives scoped non-explosion but does not make every local object logic paraconsistent.
11. Gap fallback prevents unlicensed expert use; target safety of the fallback is separately certified.
12. Append-only history does not imply monotone status.
13. Comparative updates affect authorization according to the named profile.
14. Finite search never entails global closure.
15. Finite acyclic plan composition is reifiable; component grants do not compose without a propagation theorem.
16. Higher-order evaluation is allowed through new typed requests; cycles require an explicit fixed-point extension.
17. Finite plans may carry payload, typed grade, and checked composite evidence; root licenses consume the composite certificate, and system assessment must be grounded and ranked.

## Task conclusion

The compact calculus survives its first metatheory audit with a narrower and stronger publication contract. It supports exact finite-stage authorization, update-sensitive diagnostics, typed refinement, labelled use, and recursive plan elaboration without turning any of them into final truth. Its principal exact results are conditional where they must be: persistence depends on a complete and realizable influence abstraction; profile completeness depends on independent atom realizability; and the ternary information bound depends on the actual realizable state space.

Those qualifications are not cosmetic. They prevent three tempting overclaims: that every dependency edge can actually change a decision, that singleton queries manufacture independent evidence states, and that a successful component or certificate automatically transfers to the world or to a composition. The resulting logic is better suited to the later neural work because it states exactly which information a representation must preserve and exactly which assumptions must remain outside the learned score.
