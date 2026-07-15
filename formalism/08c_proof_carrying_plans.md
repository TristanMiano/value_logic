# Proof-Carrying Recursive Plans and Stratified System Assessment

Status: Task 14C completed

Date: 2026-07-14

Depends on: [`07_core_calculus.md`](07_core_calculus.md), [`08_metatheory.md`](08_metatheory.md), [`08a_transport_routing.md`](08a_transport_routing.md), and the executable witness in [`verification/proof_plans.py`](../verification/proof_plans.py)

## Durable result summary

Finite recursive model use is realizable without identifying computation, evidence, and truth. A finite well-founded plan can carry three synchronized products:

```text
ordinary payload,
typed quantitative grade or bound,
independently checkable composite certificate with provenance.
```

A single topological induction constructs all three and proves that erasing the annotation recovers the ordinary computation. Task 14A's path-sensitivity recurrence is one concrete grade-and-certificate transformer. A valid *root* certificate can then support an ordinary core request; component grants alone still cannot license the composition.

The same discipline permits bounded system assessment. In a finite acyclic support derivation, every supported required atom traces to a typed base source. In a finite-ranked evaluator/request system whose local evaluators are total and deterministic, all diagnostics and assessments are uniquely determined by rank induction. A frozen value-logic implementation may therefore be reified and assessed under an independently fixed meta-context. Its self-endorsement alone is neither a certificate nor a target-world fact.

These are finite composition and stratification results. Direct self-license cycles remain outside the core. No neural encoding is selected here.

## 1. Four different meanings of theorem or proof

The word "theorem" otherwise creates a dangerous equivocation in this project.

| level | canonical form | what it establishes |
|---|---|---|
| object-model result | `[e,q] phi` | plan `e` produces the labelled result `phi` for context `q` |
| internal value-logic derivation | `Gamma ; s |-VL J` | the frozen calculus derives a diagnostic, license, or authorized labelled output from state-indexed premises |
| external metatheorem | `|-meta T(VL)` | ordinary mathematics establishes a property of the calculus or implementation |
| accepted empirical/formal certificate | `s |-m kappa : Claim` | checker and mode `m` accept `kappa` for a typed claim at the current stage |

The first label is not truth detachment. The second is a theorem *of the current formal system relative to `Gamma,s`* and can cease to be derivable after an evidence update. The third is where the proofs in this note live. The fourth is an operational evidence judgment; what it implies about a target world depends on the mode-scoped soundness bridge of [`08_metatheory.md`](08_metatheory.md), Theorem 15.

### 1.1 Exact Curry--Howard boundary

Howard's formulae-as-types construction (`Howard1980`) and Martin-Lof's constructive type-theoretic account of programming (`MartinLof1982`) support a proof-term reading when a term is checked in a named formal theory. Refinement types (`FreemanPfenning1991`) and quantitative type systems (`Atkey2018`) show how programs can carry more precise predicates or resource information. Hoare's program logic (`Hoare1969`), proof-carrying code (`Necula1997`), and certifying algorithms (`McConnellEtAl2011`) supply established precedents for compositional program claims and separately checkable witnesses.

The analogy applies here to:

- a proof term checked against a formal judgment;
- the finite certificate tree constructed from declared local certificate rules; and
- the internal derivation witnessing that the accepted root certificate supports a value-logic atom.

It does **not** by itself identify any of the following with a proof of `Target_w(a)`:

- a neural activation or confidence score;
- a predicted interval before external validation;
- a formally well-typed but empirically unsound loss estimator;
- an empirical certificate accepted under assumptions that fail in `w`; or
- a system's own assertion that its output is adequate.

A formal checker can prove that a certificate inhabits its declared syntactic claim type. A separate theorem must connect that claim and checker to the target world. This preserves the two-sorted `<W,S>` discipline.

### 1.2 Literature and novelty audit

| source | imported precedent | boundary here |
|---|---|---|
| `Howard1980`; `MartinLof1982` | proofs/constructions and programs can share typed term structure | no empirical score-to-truth identification |
| `Hoare1969` | local program specifications compose through inference rules | this note does not claim a new general program logic |
| `FreemanPfenning1991` | types can refine an underlying program language with more precise predicates | value-logic grades are not automatically refinement types |
| `Atkey2018` | type theory can track quantitative resource use | the project's loss bounds and resource dimensions require their own transformers |
| `Necula1997` | a consumer can check supplied code against a safety policy using a proof | project certificates may be empirical and defeasible rather than deductive PCC proofs |
| `McConnellEtAl2011` | an algorithm may return output plus a separately checked witness | the value-logic integration adds profile-indexed licensing, open/refuted states, and world/state separation |

Structural induction, proof erasure, finite-DAG evaluation, and finite-rank recursion are established mathematical patterns. The project-specific contribution is their typed integration with defeasible quantitative license assessment: a composite payload is kept distinct from its grade and certificate, and only the checked composite claim is passed into `WF + K_3`.

## 2. A compact annotated plan interface

The paper does not need a large new inventory of plan constructors. One generic finite-DAG interface is sufficient.

Let a plan node `v` have predecessors `pred(v)` and a declared input/output type, frame, and metric on every edge. Its annotated executor returns

```text
B_v(x) = < y_v, g_v, K_v >,
```

where:

- `y_v` is the ordinary computational payload;
- `g_v=<b_v,R_v>` contains a quantitative error or risk bound `b_v` in a named metric and a finite typed resource map `R_v`; and
- `K_v=<kappa_v,pi_v>` is a certificate term plus provenance.

The erasure map forgets the annotation:

```text
erase(<y,g,K>) = y.
```

For a generic constructor instance `c(v_1,...,v_k)`, the declaration contains exactly four operational pieces:

```text
F_c(y_1,...,y_k;x)       payload transformer
G_c(g_1,...,g_k;x)       typed grade transformer
C_c(K_1,...,K_k;x)       certificate/provenance transformer
Side_c                    interface, scope, frame, and termination conditions.
```

The local certificate rule is a checked implication:

```text
Check(K_i, Claim_i) for every i, and Side_c
-------------------------------------------------
Check(C_c(K_1,...,K_k),
      Claim_c(F_c(y_1,...,y_k), G_c(g_1,...,g_k))).
```

`C_c` is not allowed to mark its own conclusion valid. Its checker, version, assumptions, and accepted local evidence are supplied by the enclosing certificate mode or registry.

### 2.1 Standard constructor instances

The following are instances of the generic interface, not additional paper-level carriers.

| form | payload transformer | grade transformer | certificate obligation |
|---|---|---|---|
| primitive `p` | declared terminating `f_p(x)` | local bound and typed resources | independently accepted primitive evidence |
| sequence `g after f` | `F_g(F_f(x))` | for a tube-valid `L_g`, `b_g + L_g b_f`; declared sequential resource operators | interface/frame match and both local bounds |
| parallel product | tagged tuple `(y_1,...,y_k)` | product-metric rule or retained vector of bounds; resource operators such as energy-sum and latency-max | branch independence is not assumed unless declared |
| frame bridge `T` | `T(y)` | `delta_T + Lip(T)b` on the certified tube | source/target frame, metric, and bridge validity |
| tagged choice/router | `(j,y_j)` | selected-branch bound, plus a certified routing penalty if the target compares against another route | tag, selection scope, fallback, and route certificate |
| loss estimator | estimate or region `U` | estimator error/coverage grade in its own mode | held-out/calibration or formal estimator certificate |
| resource aggregation | unchanged payload | dimension-wise declared operator with units | no addition of unlike dimensions or silent sum/max switch |

Several qualifications are load-bearing:

1. A parallel product remains vector-valued unless a product metric or scalarization is declared.
2. A router certificate for "executed branch `j`" is not a certificate that `j` is oracle-optimal. A regret or misrouting term needs separate evidence.
3. A loss estimator produces data used to evaluate `L_q`; it is not the target criterion itself.
4. Resource aggregation is typed. Energy, memory, latency, and monetary cost do not become one scalar without an explicit context rule.
5. Sharing turns an inductive tree into a finite DAG. The proof below uses a topological order so a shared node is executed and certified once.

## 3. Proof-carrying recursive-plan theorem

### Theorem 1: annotated execution and proof erasure

Let `G` be a finite directed acyclic plan graph with root `o`. Assume:

1. every edge matches declared type, frame, and metric;
2. every payload and grade transformer is total and deterministic on the requested cases;
3. every primitive has an accepted typed local certificate with nonempty provenance;
4. every nonprimitive constructor has the locally sound certificate rule above, including its exact scope and tube conditions; and
5. certificate construction and provenance union are canonical.

Then for every admitted input `x`:

1. the annotated executor constructs a unique bundle `B_o(x)=<y_o,g_o,K_o>`;
2. `K_o` checks the declared composite claim at the root;
3. every certificate premise occurs before its conclusion and provenance is preserved; and
4. erasure commutes with execution:

```text
erase(B_o(x)) = Run_G(x).
```

**Proof.** Choose a topological order. At a source node, totality gives `y_v`; the declared local transformer gives `g_v`; and the independently accepted primitive evidence gives `K_v`. Erasure is immediate.

For the induction step, suppose every predecessor has its unique checked bundle. Interface agreement makes `F_v` defined. Determinism gives one `y_v` and one `g_v=G_v(...)`. The local certificate rule accepts the canonical `K_v=C_v(...)` and unions predecessor provenance with the local evidence. Because `F_v` is the same payload transformer used by the ordinary executor, erasing the new bundle produces the ordinary node output. The root case proves all four clauses. `square`

This theorem shows realizability of computation-plus-certificate for the finite recursive fragment. Its induction pattern is standard; its role is to prevent the later neural interface from collapsing payload, quantitative grade, and evidence into one uninterpreted number.

### Corollary 2: Task 14A path-sensitivity certificate

Instantiate each local grade transformer by

```text
b_v = delta_v + sum_(u in pred(v)) L_(u,v) b_u,
```

where each `delta_v` and `L_(u,v)` is certified on the full reachable perturbation tube. Let `C_v` record the local tube certificate, interface facts, predecessor certificates, and this arithmetic step. Then Theorem 1 yields a checked root certificate for

```text
b_o <= sum_(u in V) W_(u,o) delta_u,
```

with `W` the path weights of [`08a_transport_routing.md`](08a_transport_routing.md), Theorem 15. If the outer task loss is `K`-Lipschitz on the reached range, one final checked bridge gives

```text
abs(R(Fhat_G)-R(F_G)) <= K b_o.
```

**Proof.** The node recurrence is exactly the grade induction in Theorem 1. Expanding it along the finite topological order gives the path sum. Apply the certified outer Lipschitz bridge. `square`

Resources propagate in parallel but remain typed. The error proof does not justify any particular energy, latency, or memory aggregation rule.

### Corollary 3: license lifting from a composite certificate

Reify the annotated root as the core plan `e_G`. Fix a request `r=(s,e_G,q,P)`. Suppose:

1. `WF(P,e_G,q,s)`;
2. the root certificate is accepted under the exact certificate mode named by the instantiated atoms;
3. the certified root grade lies in the acceptable region of `q` and satisfies any required resource/bridge constraints; and
4. every other required slot of `P` has a supported diagnostic.

Then

```text
Assess(r)=Granted.
```

**Proof.** Conditions 2--3 make the *composite* certificate support its instantiated adequacy and constraint atoms. Condition 4 supports the remaining required atoms. Their finite `K_3` meet is supported, and condition 1 excludes `Undefined`. Apply the core assessment rule. `square`

This is not the invalid rule

```text
Granted(component 1) AND ... AND Granted(component k)
    => Granted(composition).
```

It is a lifting rule from a checked root claim whose derivation explicitly transforms the component bounds and evidence.

### Countertheorem 4: checked leaves without a constructor rule do not suffice

There are checked primitive certificates whose payload composition has no valid certificate at the parent tolerance.

**Countermodel.** Let two sequential scalar components have same-direction error bounds `0.06` under separate tolerances `0.10`. Both local certificates check. Let the composite error be their sum and retain outer tolerance `0.10`. The root error is `0.12`; the composite adequacy atom is refuted. Merely pairing the two certificate identifiers cannot establish a false root claim. `square`

**Project impact.** A learned or symbolic system may expose component statuses for explanation, but it must receive or construct a valid grade/certificate transformer before licensing the composite. "Proof-carrying" cannot mean attaching unrelated successful certificates to an ordinary program.

## 4. Grounded support rather than circular endorsement

Let `H_r` be the finite support derivation used for one request. Its nodes are either:

- **typed bases**: formal axioms in a named theory, accepted empirical records under a named mode, externally supplied inputs, or independently checked primitive certificates; or
- **derived support nodes**: applications of declared rules with a nonempty finite premise set.

Edges point from premises to conclusions. A derivation is *grounded* when every supported required atom has a directed path from a typed base. Each derived diagnostic's provenance transformer must contain the union of its premise provenance plus its local rule/checker record.

### Theorem 5: grounded provenance in the DAG fragment

If `H_r` is finite and acyclic, every indegree-zero support node is a typed base, and every derived support rule preserves premise provenance, then every supported required atom is grounded. Its diagnostic contains at least one typed base source and a finite derivation path from that source.

**Proof.** Topologically order `H_r`. An indegree-zero node is a typed base by hypothesis. At a derived node, every premise occurs earlier. By induction each premise is reachable from a typed base; adding the rule edges gives a base-to-conclusion path, and provenance union preserves the corresponding source. Apply this at each supported required atom. `square`

### Corollary 6: closed mutual support is syntactically inadmissible

A finite component in which every support node depends only on another node in the same component contains a directed cycle. It is therefore not a derivation in the DAG fragment. In particular,

```text
Grant(A) because Grant(B),
Grant(B) because Grant(A)
```

cannot be used as a core certificate tree.

The theorem does not prove that every base source is target-world sound. It establishes audit grounding. Empirical bases still need mode assumptions, and formal bases establish only their formal claims unless a world bridge is proved.

### Counterexample 7: acyclicity without a typed-base condition is insufficient

Take a one-node acyclic graph marked "supported" with no premises and no source type. It is not reachable from typed evidence. Thus finiteness and acyclicity alone do not establish grounding; every zero-premise support must be declared and checked as a base rule. `square`

**Project impact.** Provenance checks must reject both closed support cycles and untyped zero-premise successes. A missing evidence record should yield an open diagnostic, not manufacture an axiom.

## 5. Licensing the value-logic implementation

Freeze a versioned implementation of the value-logic checker/decoder as a use plan `e_VL`. Its independently fixed context `q_VL` must state what is measured. Possible targets include:

- agreement with a reference evaluator on held-out requests;
- false-grant and false-refusal risk;
- calibration or coverage of predicted certificate statistics;
- proof-term checking fidelity;
- routed task risk; and
- typed computation, memory, or latency bounds.

The meta-request is ordinary:

```text
r_VL = (s_meta,e_VL,q_VL,P_VL).
```

Nothing about this syntax grants `e_VL`. Its diagnostics must be built from held-out records, formal verification, independently checked traces, or other sources named by `q_VL`.

### 5.1 Finite-rank semantics

Let `N` be a finite set of evaluator/request nodes with a rank

```text
rho:N -> {0,...,h}.
```

An internal dependency `v -> u` means that evaluator `v` reads the completed output of `u`. Require

```text
rho(u) < rho(v).
```

Each node also reads fixed exogenous inputs. Let its local evaluator be a total deterministic function of exactly those lower-rank outputs and inputs. The rank is attached to semantic evidence dependence, not to whether a payload happens to contain source code or a quotation of the system.

### Theorem 8: unique stratified system assessment

Under the finite-rank conditions above, there is exactly one global assignment of outputs, diagnostics, and assessments to all nodes. If each local support derivation satisfies Theorem 5 and its provenance transformer preserves lower-rank sources, then every supported required atom in the global assignment is grounded.

**Proof.** At rank zero, every evaluator reads only fixed exogenous inputs, so totality and determinism give a unique output. Assume uniqueness below rank `k`. Every rank-`k` node reads only those already unique values and fixed inputs, hence has one output. Finite induction reaches `h`. The provenance conclusion follows simultaneously: rank-zero support is grounded in typed exogenous bases, and each higher rank unions already grounded lower-rank provenance with its local sources. `square`

### Corollary 9: stratified reification of `e_VL`

Adding the frozen computation `e_VL` as a plan does not create reflection by itself. If its observed run records occur below a meta-evaluator, and `r_VL` consumes only those records and independently supplied meta-evidence at a higher rank, Theorem 8 gives a unique assessment of `e_VL`. That assessment may be `Granted`, `Withheld`, `Refused`, or `Undefined` exactly as for any other plan.

It is also legitimate to evaluate a previous version or prior-run output of the system at a later rank. Version and time indices must remain explicit; a previous certificate can expire or be rebutted. The same-run grant cannot be its own sole premise.

### Countertheorem 10: system self-endorsement is not target-factive

No rule from

```text
Assess(s_meta,e_VL,q_VL,P_VL)=Granted
```

to an unqualified target-world statement about `e_VL` is valid without a mode-scoped soundness bridge.

**Countermodel.** Fix one finite meta-state containing the same implementation, self-report, accepted operational certificate, and resulting grant. Pair it with two target worlds. In `w_0`, the held-out sample and assumptions transfer and the target false-grant rate is acceptable. In `w_1`, an unrecorded distribution shift makes the target false-grant rate unacceptable. Because assessment reads the same finite state, it grants in both pairs; the target property differs. `square`

**Project impact.** System-level adequacy is a defeasible, context-indexed license. The experiment must compare externally audited system evidence with self-confidence-only pseudo-evidence. A self-grant head cannot certify its own target reliability.

### Counterexample 11: unranked self-dependence is underdetermined

If a same-rank grant is its own only evidence, the equation `g=g` has at least two Boolean solutions. The equation `g=not g` has none. Moving to `K_3` changes the space but does not choose an operator or fixed point. Thus an unranked cycle has no inherited core meaning. `square`

A future cyclic extension would have to declare:

1. a complete order or other fixed-point space;
2. an immediate-consequence operator;
3. monotonicity or another existence condition;
4. a selected fixed point, such as the least one; and
5. a soundness theorem connecting that fixed point to accepted evidence.

No such extension is assumed here. Consequently, this task makes no claim that an ungrounded positive cycle can or cannot create a grant under every possible cyclic semantics.

## 6. What the result says about adequacy values

The annotated bundle answers the project author's recursive-model concern constructively. A component can compute a prediction, coordinate transformation, object decomposition, route, or loss estimate while also emitting the quantitative information and certificate used by later components. The downstream node can process both the payload and the grade.

The safe general interface keeps them separate:

```text
payload channel != quantitative grade != certificate/provenance.
```

A scalar may serve both as adequacy surplus and downstream content only in the special jointly sufficient construction already scoped at Checkpoint B: the value has a named hypothesis, units/normalization, boundary rule, and independently valid certificate or approximation envelope. Even there, the scalar is not the certificate term. Task 15 encodes this interface, and Task 17's [`ml/03_representation_theorems.md`](../ml/03_representation_theorems.md) proves the minimal coordinate-complete state-plus-surplus realization and its limitations. This note stops before choosing an architecture.

## 7. Result classification

| result | classification | role |
|---|---|---|
| annotated execution and erasure | standard structural/topological induction instantiated to the project bundle | positive realizability of recursive computation-plus-certificate |
| path-sensitivity certificate | integration of Task 14A's proved bound with the annotated executor | concrete quantitative composition witness |
| composite license lifting | core consequence under a checked root certificate | exact bridge into `WF + K_3` |
| failure of certificate/license pairing | finite countermodel | blocks unconditional component composition |
| grounded provenance | elementary finite-DAG invariant with necessary base condition | auditability theorem |
| unique stratified assessment | elementary finite-rank recursion theorem | bounded system self-assessment |
| self-endorsement nonfactivity | two-world countertheorem specializing the core world/state separation | central reflection limit |
| unranked-cycle underdetermination | finite fixed-point counterexamples | boundary of the core |

The package is theorem-heavier than mere record specification, but its mathematical mechanisms are deliberately classical. The publishable claim is the coherent integration: recursive executable plans can carry checked quantitative evidence into a defeasible license calculus, while grounded/ranked assessment prevents the system's license from becoming its own warrant.

## 8. Executable witness

[`verification/proof_plans.py`](../verification/proof_plans.py) implements the generic finite-DAG contract using only the Python standard library. Its tests construct a parallel computation followed by a frame bridge, verify proof erasure, reproduce the path-sensitivity recurrence, keep energy and latency aggregation typed, lift a valid root certificate through the actual assessment kernel, reject an unregistered local certificate, reject a plan cycle, trace a required atom to empirical and formal bases, reject mutual support, and show rank-order independence plus same-rank rejection.

These tests are finite regression witnesses, not a proof-assistant formalization.

## Decisions carried forward

1. "Theorem" is always tagged as object output, internal derivation, external metatheorem, or accepted certificate judgment.
2. Proof erasure establishes computational agreement, not target-world truth.
3. Every composite constructor transforms payload, typed grade, certificate, and provenance under explicit conditions.
4. Root licensing consumes a checked composite certificate; it never meets component grants as a substitute.
5. Every zero-premise support node must be a typed accepted base.
6. Finite acyclic provenance excludes closed mutual support.
7. Finite-rank evaluator dependencies give unique system assessment when local evaluators are total and deterministic.
8. Reifying `e_VL` is permitted; using its same-run grant as its sole evidence is not.
9. Cyclic semantics, fixed-point selection, and reflection principles remain outside the core.
10. Payload, quantitative grade, and certificate are separate by default; a dual-use scalar is a later conditional representation theorem, never a proof term by itself.

## Task conclusion

Task 14C establishes the positive finite result requested by the project author. Programs in the plan library can both compute and carry checked claims about their quantitative behavior. The recursion is structural rather than self-justifying: every composite proof is assembled from accepted bases through declared transformers, and every value-logic self-assessment sits at a higher evidential rank than the records it evaluates.

This is enough structure for Task 15 to encode recursive plans. Task 17 subsequently proves that fixed finite annotated CPWL plans with conforming hard branches admit exact ReLU payload/grade realization with an external certificate checker. It is not a theorem that neural activations are proofs, that empirical certificates are infallible, or that the system can license itself from nothing.
