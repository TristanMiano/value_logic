# Open-Ended Refinement, Stability, and Non-Finality

Status: Task 12 continuation semantics and stability results

Date: 2026-07-12

Depends on: [`05a_integration.md`](05a_integration.md) and the executable [`WF + K_3` reference](../verification/README.md)

> **Task 14B repair notice.** [`08b_audit_repairs.md`](08b_audit_repairs.md) repairs Theorem 3's joint eventual index, states Theorem 4 as an adapted stopping-time regime theorem, and positions the finite-prefix/sequential-decision arguments as classical patterns. The scoped conclusions below now incorporate those repairs.

## Durable result summary

This task adds a meta-level continuation semantics without adding truth or finality predicates to the base license language. A node is a compatible world/stage pair carrying a finite epistemic state. For a fixed substantive query

```text
chi = (e,q,P),
```

the four-valued public assessment is recomputed at every node from well-formedness plus the finite meet of meaningful `K_3` atoms. Changing the evaluated plan `e`, reliance context `q`, or requirement profile `P` creates a different query; it is not evidence that one query changed its status.

The main results are:

1. **Finite-prefix non-certifiability.** If the same finite state has one compatible continuation that preserves the current assessment and another that later changes it, no certificate procedure depending only on that state can soundly certify permanent current stability over both continuations.
2. **Deterministic stability.** A proof-backed atom can be internally certified stable when an enforceable continuation invariant freezes every dependency and the proof-validity rules. The proof alone is insufficient if a premise can later be corrected.
3. **Statistical stabilization without certain arrival.** On a simultaneous-coverage event, shrinking confidence regions stabilize a threshold atom whenever the target risk is separated from the threshold. In a family containing finite-prefix mutually absolutely continuous laws on opposite sides of the threshold, no procedure can both announce the correct side at a finite time with positive probability and have zero error uniformly.
4. **Directional open-library impossibility.** A currently supported relative-undefeated or certified-undominated atom cannot be permanently certified when every current finite library has a history-preserving continuation that adds and validly evaluates a dominator. The polarity-unrestricted version is false: an existing persistent dominator can make a refuted comparison stably refuted.
5. **Extendability underdetermines dynamics.** An indefinitely extendable system may stabilize, change forever, or stabilize under `P_rely` while a comparison profile changes. Query stability, known stability, library completeness, semantic finality, and optional world truth are therefore distinct.

No Löb or GL principle is imported. The project has no arithmetized provability predicate, verified derivability conditions, or diagonal fixed-point translation for empirical licenses. “Final” remains absent from the base syntax; that absence is a design fact, not a non-finality theorem.

## 1. Why a second semantic level is needed

Task 11A defines what a profile-indexed license says at one finite stage. Task 11B verifies those finite assessments. Neither result alone says whether a current grant will persist, whether it eventually stops changing, or whether an agent can know that the last change has occurred.

These are different questions:

```text
current:       what does the finite state assess now?
pathwise:      what eventually happens along one continuation?
modal:         what happens in every compatible continuation?
certificatory: does the finite state contain a sound warrant for that modal claim?
final:         is there any proper continuation relevant to the whole problem?
truth:         what obtains in the target world independently of the finite record?
```

The motivating sequence of physical theories requires only the first four distinctions. It does not require the logic to assert a metaphysical thesis that every theory is false, nor does it require one fixed system to store an actual infinity of later theories.

## 2. Continuation frames over world/stage pairs

### 2.1 Nodes and refinement

A **continuation frame** is

```text
F = (N, ->, root, state, world),
```

where:

- `N` is a countable set of nodes;
- `->` is an acyclic one-step refinement relation;
- `root` is the current node;
- `state(n)` is a finite epistemic state of the Task 11B kind; and
- `world(n)` is a target-world index used only in the semantics or metalanguage.

Write `n <= m` for reflexive-transitive reachability and `n < m` for a proper reachable refinement. The graph may branch and merge. A path is a finite or infinite chain

```text
n_0 -> n_1 -> n_2 -> ... .
```

If worlds are complete target worlds, an actual continuation preserves the world coordinate. Different compatible frames may nevertheless have different worlds while exposing the same finite state. If worlds are partial structures, an edge may replace `w` by an extension `w'`; every formula already fixed by `w` must retain its interpretation. This convention keeps metaphysical change separate from epistemic refinement.

### 2.2 Compatible continuation

An edge `n -> m` is **compatible** with the project when all of the following hold:

1. `state(m)` contains a provenance-preserving embedding of the event history of `state(n)`;
2. new evaluations, certificates, corrections, model additions, searches, profile requests, or routing decisions are appended through a declared update operation;
3. a correction may invalidate an old certificate but does not delete the certificate or its historical status;
4. every retained request is re-evaluated from its current valid dependencies rather than inheriting its old top-level label by fiat;
5. the world coordinate is preserved or refined as described above; and
6. substantive query identity is preserved whenever a stability claim is being tested.

The last clause needs emphasis. Fix

```text
chi = (e,q,P).
```

The stage, evidence record, evaluated library, search budget, certificates, and diagnostics may change. The evaluated plan `e`, reliance/evaluation context `q`, and profile `P` do not. Replacing any of them forms `chi' != chi`. A profile change is a linked new request, not instability of the old request.

Compatibility does not imply status monotonicity. Append-only history permits both rebuttal and lapse because validity is recomputed over the enlarged provenance graph.

### 2.3 Observational indistinguishability

Two nodes are **stage-indistinguishable**, written

```text
n ~_fin m,
```

when their finite epistemic states, accepted verifier rules, and exposed query data are isomorphic. Their target worlds or later continuations may differ. Any stage-local procedure must return the same result at stage-indistinguishable nodes.

This is the exact sense in which two possible inquiries can share every observation so far but diverge later. It is weaker than saying that their complete worlds are identical.

## 3. Fixed-query assessments

For node `n` and fixed `chi=(e,q,P)`, let

```text
A_chi(n) in {Undefined, Refused, Withheld, Granted}
```

be the Task 11B public outcome:

```text
A_chi(n) = Undefined                         if not WF(chi,state(n));
A_chi(n) = lift(meet required K_3 atoms)    otherwise.
```

Here `lift(refuted)=Refused`, `lift(open)=Withheld`, and `lift(supported)=Granted`. `Undefined` remains a well-formedness failure, not a fourth evidential degree.

For a required atom `a`, write

```text
v_a(n) in K_3 = {refuted,open,supported}
```

whenever `WF` holds. Atom-level results below presuppose well-formedness throughout the relevant continuation. Outcome-level results permit all four public values.

The **current grant** predicate is only

```text
Grant_chi(n) iff A_chi(n)=Granted.
```

It quantifies over no future node.

## 4. Four notions that must not collapse

### 4.1 Eventual stability along a path

For an infinite path `pi=(n_i)`, define

```text
EventuallyStable_chi(pi)
iff exists N exists z forall i>=N: A_chi(n_i)=z.
```

The index `N` is an external witness. The agent at `n_N` need not know it. The stable value may be any public outcome; eventual grant is the special case `z=Granted`.

A frame is **branchwise eventually stable** for `chi` when every maximal infinite path is eventually stable. This allows different branches to stabilize at different times or values. A stronger uniform notion would require one depth and one value for all sufficiently deep nodes; no result below assumes it.

### 4.2 Permanent current stability

Define

```text
StableNow_chi(n)
iff forall m>=n: A_chi(m)=A_chi(n).
```

This is a semantic property of the continuation class. It is stronger than eventual stability along the actual path: it says the present value never changes in any compatible future represented by the frame.

A descendant `m>=n` is a **live alternative for `chi` at `n`** when

```text
A_chi(m) != A_chi(n).
```

Thus a node is permanently stable exactly when it has no live alternative in the declared frame. The definition is useful, but the paper-carrying work lies in establishing when domain assumptions construct or exclude live alternatives.

### 4.3 Known or certified stability

A stability-certificate scheme consists of a finite certificate language, a stage-local verifier

```text
Accept(c,chi,state(n)),
```

and a declared frame class `C`. It is **sound** when

```text
Accept(c,chi,state(n))
=> StableNow_chi(n)
```

for every pointed frame in `C` containing that finite state. Define

```text
CertifiedStable_chi(n)
iff exists c: Accept(c,chi,state(n)).
```

This is intentionally scheme-relative. A string saying “nothing will change” is not a certificate unless a trusted verifier connects it to continuation invariants. “Known” in this document means an accepted certificate under a stated sound scheme, not an unanalysed epistemic modality.

Sound certified stability implies semantic permanent stability. The converse need not hold: a path or even a whole frame can stabilize without the finite state containing a certificate that rules out every live alternative.

### 4.4 Semantic finality

Query stability is not finality. To express a stronger external notion, choose a **problem projection** `Omega_q(n)` containing the target facts, admissible plan universe, comparison obligations, and other information declared relevant to the whole inquiry under `q`. Then define

```text
SemFinal_q(n)
iff there is no m>n with Omega_q(m) != Omega_q(n).
```

This is semantic finality relative to `q` and the declared possibility class. It is stronger than `StableNow_chi(n)` for one `e` and `P`. Irrelevant models may be added without changing either projection; a new relevant model may defeat finality while leaving `P_rely` for `e` unchanged.

`SemFinal` is metalanguage notation. It is not added to the base object language and supplies no license rule.

### 4.5 Optional target truth

If a later argument needs truth, write externally

```text
True_w(phi)
```

for satisfaction in target world `w`. No general rule

```text
Grant_chi(n) => True_w(phi)
```

is valid. Such a rule requires an atom-specific soundness theorem connecting the certificate mode, loss, tolerance, and target proposition. A statistical grant may instead carry a stated error guarantee. Conversely, a true target claim can remain withheld when evidence is insufficient.

## 5. A general finite-prefix barrier

### Theorem 1: indistinguishable-continuation non-certifiability

Let `C` contain two pointed continuation frames with roots `n` and `n'` such that:

1. `n ~_fin n'`;
2. `A_chi(n)=A_chi(n')=z`;
3. `StableNow_chi(n)`; and
4. some descendant `m'>=n'` has `A_chi(m') != z`.

Then no stage-local certificate scheme sound over `C` can accept a permanent-current-stability certificate for `chi` at the common finite state.

**Proof.** A stage-local verifier receives isomorphic finite inputs at `n` and `n'`, so it accepts the same certificates at both or neither. If it accepts some `c`, soundness requires `StableNow_chi(n')`. Clause 4 contradicts that requirement. Therefore no sound scheme accepts at either root. `square`

The theorem is conditional, not a metaphysical ban on knowledge. It identifies the exact obstruction: an observation-preserving live alternative inside the claimed scope of soundness.

### Corollary 1: finite state does not reveal that the last change has occurred

If every finite prefix of an actually stabilizing path is stage-indistinguishable from the root of some compatible path that changes later, then no sound stage-local procedure announces permanent current stability at any finite point of the actual path.

The assessment may nevertheless be eventually constant. Eventual stability and certified arrival are therefore non-equivalent.

## 6. Stability regime I: deterministic proof-backed atoms

Let a meaningful atom have a finite dependency projection

```text
dep_a(state(n))
```

and a deterministic evaluator `f_a` such that

```text
v_a(n)=f_a(dep_a(state(n)), Rules_a(n)).
```

Examples include a resource inequality over immutable hardware constants, a type judgment, or a proof-backed algebraic property. Let `Dep(a)` be the finite set of record locations and rule versions read by `f_a`. A **local freeze certificate** names the allowed future event schemas `U` and verifies, for every `u in U`, that either `u` is disabled or its transition preserves the values and denotations in `Dep(a)`. It also locks the evaluator/proof-rule version. By induction over edges this local effect condition implies the global invariant `Freeze_a(n)`: every descendant preserves

1. the denotation and values of every dependency read by `f_a`;
2. the evaluator and proof-validity rules;
3. the relevant interface and frame; and
4. the validity of the supplied proof or counterproof.

### Theorem 2: deterministic freeze certification

Suppose compatible continuations from `n` are generated by the declared event schemas `U`, and `WF` holds for `chi` at every descendant. If a checkable certificate establishes both

```text
v_a(n)=k
```

and the local freeze condition for every `u in U`, then

```text
forall m>=n: v_a(m)=k.
```

If this holds for every required atom of `P`, then `StableNow_chi(n)`.

**Proof.** Induct on the length of a path from `n`. The base node has the certified dependency projection. At an induction step, the edge is generated by some declared `u`; the local freeze check preserves every location and rule version read by `f_a`. Thus every reachable node has the base dependency projection and evaluator. Determinism gives

```text
v_a(m)=f_a(dep_a(state(m)),Rules_a(m))
      =f_a(dep_a(state(n)),Rules_a(n))
      =k.
```

If every required atom is fixed, their finite meet is fixed. `WF` is fixed by hypothesis, so the lifted public outcome is fixed. `square`

For a finite event-schema language and finite `Dep(a)`, the disjoint-write/effect checks are finite. This is genuine internal certification only when the transition system can verify or enforce that declared event language. A proof of the current atom value does not by itself prove that its premises will never be corrected.

### Countermodel 1: proof without frozen premises

At `n_0`, a deterministic check proves `cost(e)<=B` from signed premise `B=10` and record `cost(e)=9`, so the constraint atom is supported. At `n_1`, an authenticated correction records that the earlier unit conversion was invalid and the normalized cost is `12`. The old proof remains in provenance but its premise lapses; the atom becomes open pending recertification or refuted if `12` is certified.

Thus proof-backed does not imply stable. The missing hypothesis is continuation invariance of the proof dependencies, not more confidence in the original derivation.

## 7. Stability regime II: statistical threshold atoms

### 7.1 Region semantics

Fix target risk `theta=Risk_w(e,q)` and threshold `epsilon`. Let `C_n=[L_n,U_n]` be the valid uncertainty region stored at node `n` along one path. Use the Task 11B three-valued assessment:

```text
supported    if U_n <= epsilon;
refuted      if L_n > epsilon;
open         otherwise.
```

Let `diam(C_n)=U_n-L_n`. A **simultaneous-coverage event** is

```text
G = {forall n: theta in C_n}.
```

The event may have probability at least `1-alpha` under a confidence-sequence construction. That probability is an assumption supplied by the statistical method, not a theorem of this logic.

### Theorem 3: margin-separated statistical stabilization

Along a path, assume:

1. `theta in C_n` for every sufficiently late `n`;
2. `diam(C_n) -> 0`; and
3. `gamma=|theta-epsilon|>0`.

Then the adequacy atom is eventually stable. It is eventually supported when `theta<epsilon` and eventually refuted when `theta>epsilon`.

**Proof.** Choose `N_coverage` beyond which coverage holds and `N_diameter` beyond which `diam(C_n)<gamma`. Set `N=max(N_coverage,N_diameter)`. If `theta<epsilon`, coverage implies for every `n>=N`

```text
U_n <= theta + diam(C_n) < theta+gamma=epsilon,
```

so every late atom is supported. If `theta>epsilon`, coverage implies

```text
L_n >= theta - diam(C_n) > theta-gamma=epsilon,
```

so every late atom is refuted. `square`

If simultaneous coverage holds with probability at least `1-alpha`, the conclusion holds on that event and therefore with at least that probability. This is not a zero-error claim.

The margin assumption matters. At `theta=epsilon`, shrinking regions can straddle the boundary forever, approach from the supported side, or change repeatedly if coverage is not nested. Convergence in diameter alone does not choose one behavior.

### Corollary 2: finite-profile lifting

Let `P` have finitely many required atoms. Along a path, suppose `WF(chi)` is eventually constant and every required atom is eventually constant. Then `A_chi` is eventually constant. If sound certificates establish permanent stability of `WF` and every required atom, they jointly certify permanent profile stability.

**Proof.** Take the maximum of the finitely many atom stabilization indices and the `WF` index. Beyond it, the required vector and therefore its deterministic finite meet are constant. The permanent version applies the same argument at every descendant. `square`

### Theorem 4: no uniform zero-error finite regime declaration in a rich family

Let `(F_n)` be the observation filtration. Let a statistical family contain laws `P_-` and `P_+` such that:

```text
theta(P_-) < epsilon < theta(P_+),
```

and their restrictions to every finite observation sigma-field `F_n` are mutually absolutely continuous. Let `tau` be a possibly infinite stopping time and let the declaration `delta in {below,above}` on `{tau<infinity}` be `F_tau`-measurable, so

```text
{tau=n and delta=d} in F_n
```

for every finite `n` and declaration `d`. Interpret `below` as the regime claim `theta(P)<epsilon` and `above` as `theta(P)>epsilon`.

If the procedure declares `below` at a finite time with positive probability under `P_-`, then it makes that same, wrong-regime declaration with positive probability under `P_+`. Symmetrically, a finite `above` declaration that has positive probability under `P_+` has positive probability under `P_-`. Hence no such procedure is both zero-error over `{P_-,P_+}` and finite with positive probability on the corresponding correct side; in particular, no zero-error procedure stops almost surely under both laws.

**Proof.** Suppose

```text
P_-(tau<infinity and delta=below)>0.
```

This event is the countable union of the `F_n`-measurable events

```text
E_n={tau=n and delta=below}.
```

Some `E_n` has positive `P_-` probability. Stopping-time adaptedness makes `E_n` an `F_n` event, and mutual absolute continuity on `F_n` gives `P_+(E_n)>0`. On `E_n`, `delta=below` is the wrong parameter-regime declaration under `P_+`. The opposite direction is identical. `square`

This theorem does not deny high-confidence sequential certification, almost-sure eventual correctness under stronger assumptions, or practical stopping rules. It denies a particular conjunction: finite positive-probability regime declaration, uniform zero error, and a family whose opposite regimes cannot be excluded from any finite prefix.

It is deliberately not phrased as a claim that the displayed atom trajectory is already “supported forever” or “refuted forever.” If, under each law, eventual coverage and shrinking diameter hold almost surely, Theorem 3 makes the atom eventually match the parameter regime; under those additional assumptions the same argument yields the corresponding trajectory-level corollary.

### Countermodel 2: stabilization with no knowable arrival time

Consider an actual path whose intervals are open-valued until some finite but externally unknown `N`, after which all regions lie strictly below `epsilon`. The atom is eventually supported. Require the continuation class to contain, for every finite prefix, another path with the same prefix and a later valid region that again straddles or exceeds the boundary. Theorem 1 then prohibits permanent-stability certification at every finite prefix even though the actual path stabilizes.

## 8. Stability regime III: open-library comparison

Fix a comparison profile and scope inside `q`. Let `Comp_e(n)` be either the relative-undefeated or certified-undominated atom for `e`, evaluated against the eligible library at `state(n)`.

Define the **history-preserving dominator extension property** at `n`:

```text
AddDom(e,q,n)
```

when there exists `m>=n` and a newly added plan `d` such that:

1. the history and old assessments remain in provenance;
2. `d` is executable and eligible on the exact comparison scope in `q`;
3. a valid joint comparison certificate establishes `d` dominates `e` under the named criterion;
4. the relevant search/evaluation trace is valid; and
5. `Comp_e(m)=refuted`.

The library is **positively open for `e,q`** when `AddDom(e,q,n)` holds at every node at which `Comp_e` is supported.

### Theorem 5: no permanent positive comparison certificate in a positively open library

If `Comp_e(n)=supported` and `AddDom(e,q,n)`, then the comparison atom is not permanently stable at `n`. No sound stability-certificate scheme over frames satisfying this property can certify its current support as permanent.

**Proof.** The `AddDom` witness supplies a descendant `m` with `Comp_e(m)=refuted`, so `m` is a live alternative and permanent stability fails. Sound certified stability implies permanent stability, so no sound scheme accepts a permanent-support certificate at `n`. `square`

### Corollary 3: comparison-profile grants are non-final under model-addition openness

Suppose every other required atom of `P_pref-rel` or `P_pref-cert` is supported at `n`, the required comparison atom is supported, and an `AddDom` continuation preserves the other atoms. Then

```text
A_(e,q,P)(n)=Granted
```

but some descendant assesses the same fixed query as `Refused`. A finite best-in-evaluated-library result does not entail permanent preferred use.

### Proposition 6: the polarity-unrestricted comparison claim is false

It is not true that every comparison atom in an open library is unstable or uncertifiable. Suppose a valid persistent certificate already establishes that `d_0` dominates `e`, and every continuation preserves that certificate. Then `Comp_e=refuted` at every descendant. New models may be added indefinitely, yet the refutation of `e` remains stable and may be certified by the frozen `d_0` witness.

**Proof.** Relative-undefeated and certified-undominated are both refuted whenever at least one valid dominator exists. The persistent `d_0` certificate supplies such a dominator at every descendant. `square`

The correct impossibility result is therefore directional: **presently positive finite-library non-domination cannot be certified as permanent under guaranteed dominator extensions**. This is enough for the theory-succession motivation and is mathematically stronger than an imprecise slogan because it identifies the exact polarity, update, and certificate assumptions.

### Corollary 4: conditional library incompleteness

If every finite stage admits a proper relevant `AddModel` continuation, then `SemFinal_q(n)` is false at every finite node for a problem projection that includes the relevant candidate universe. Consequently, no sound certificate can establish `Complete(Library,q)` at such a node.

This is conditional on the declared continuation class. It is not a universal metaphysical proof that no inquiry can ever have a complete finite candidate set.

## 9. Countermodels separating the notions

### 9.1 Extendable but stable

Let `P_rely` for `e` have frozen supported adequacy, fallback, constraint, and trace atoms. At every stage add a new archived plan `z_n` that is inapplicable to `q`. The sequence is indefinitely extendable and its archive grows without bound, but

```text
A_(e,q,P_rely)(n)=Granted
```

at every node. Extendability does not imply query instability.

### 9.2 Extendable and changing forever

Start with a supported certificate for an evidence atom. Append a valid correction that lapses it, producing `open`; append a new independent valid certificate, producing `supported`; later correct that certificate; and repeat. Every historical certificate and correction remains in the provenance graph. The fixed atom follows

```text
supported, open, supported, open, ...
```

and never stabilizes. Append-only history does not imply monotone current warrant.

The construction can alternate `supported` and `refuted` as well if each later experiment validly rebuts the currently governing target claim under a changing but fixed-in-advance evidence rule. The simpler lapse construction suffices to separate extendability from convergence.

### 9.3 One finite prefix, two futures

Take a finite node at which `e` is granted. One continuation adds only irrelevant records and preserves the grant forever. A second, stage-indistinguishable through that node, later corrects the adequacy certificate or adds a dominator required by `P`. The common prefix determines current assessment but not permanent stability. This is the finite witness pattern required by Theorem 1.

### 9.4 Different profiles, different dynamics

Fix the same `e` and `q`. Let all `P_rely` atoms be frozen supported. Let `P_pref-rel` add the relative-undefeated atom. At stage `n_0`, both profiles grant. At `n_1`, add and validly evaluate dominator `d` while preserving all adequacy evidence:

```text
A_(e,q,P_rely)(n_1)      = Granted,
A_(e,q,P_pref-rel)(n_1)  = Refused.
```

The reliance profile is stable while the preferred-use profile changes. There is no unqualified fact `StableLic(e)`.

### 9.5 Stable assessment without semantic finality

In Countermodel 9.1, the one query is stable, yet the full problem projection changes whenever another relevant but non-dominating plan is discovered. Thus `StableNow_chi` does not imply `SemFinal_q`. Even stability for every currently stored query need not imply that the candidate universe is complete, because a later query may be newly expressible.

## 10. Stability trichotomy: exact adjudication

The requested “trichotomy” is not a partition of all atoms into three exhaustive syntactic species. It is a three-regime theorem package with different sufficient assumptions and obstructions:

| regime | positive result | obstruction or limitation |
|---|---|---|
| deterministic proof-backed | current value and profile can be internally certified stable under a checkable freeze invariant | a current proof without frozen dependencies can lapse or be rebutted |
| statistical threshold | shrinking, simultaneously covering regions stabilize away from the threshold | finite-prefix overlap across opposite regimes blocks uniform zero-error finite announcements |
| open-library comparison | a persistent certified dominator can stabilize a refutation | current positive non-domination cannot be permanently certified when a valid dominator can always be added |

The asymmetry is substantive. Deterministic stability is controlled by dependency invariance; statistical stability is pathwise and mode-probabilistic; open-library positive comparison is defeated by candidate-space expansion. The profile layer then transports atom behavior through finite meet.

These results also explain why an error tolerance `epsilon` is not itself a truth threshold. Statistical stabilization concerns a fixed task-relative risk boundary. A future model may change comparative preference without changing the stable adequacy side of that boundary.

## 11. Why Löb and GL are not used

The continuation operator

```text
[C] phi  iff phi holds at every compatible descendant
```

is a semantic necessity over a declared refinement relation. The certificate predicate `Accept(c,chi,s)` is a typed finite verifier. Neither is currently an arithmetized provability predicate.

No project artifact establishes:

1. a formal theory capable of representing its own syntax and proof predicate;
2. the Hilbert-Bernays-Löb derivability conditions for the empirical license operator;
3. a diagonal or fixed-point lemma for license formulas; or
4. a translation under which empirical certification is formal provability.

Therefore Löb's theorem and GL supply no theorem here. Calling open-ended refinement “anti-Löbian” would obscure the actual proof, which is the elementary but exact indistinguishable-continuation argument of Theorem 1 plus domain-specific constructions of live alternatives.

This is a scoped rejection of transfer by analogy, not a claim that no future enriched formal system could contain a genuine provability fragment.

## 12. Base-language non-expressibility

The current base grammar contains profile-indexed license requests, atom diagnostics, updates, and selectors. It contains no formula constructor

```text
Final(e), Complete(K), or True(phi).
```

Hence such strings are not well-formed base formulas. This is **syntactic non-expressibility by design**. It does not prove that finality is impossible in every world, that no external observer can establish completeness, or that every present theory is false.

The substantive negative results require semantic hypotheses:

- a stage-indistinguishable changing continuation for Theorem 1;
- finite-prefix mutually absolutely continuous opposite statistical laws for Theorem 4; or
- a history-preserving valid dominator extension for Theorem 5.

Keeping the syntax fact separate from these theorems prevents a design omission from masquerading as a discovery about inquiry.

## 13. Consequences for the integrated witness and later core

The Task 11A stages are one finite prefix, not evidence that the sequence must continue in a particular way. They instantiate:

- `O`: grant, then lapse (`supported -> open`) under `P_rely`;
- `S`: stable adequacy through `t_1`, comparative defeat under a stronger profile, then rebuttal (`supported -> refuted`) at `t_2`;
- `N`: addition-driven supersession without deletion of older evidence; and
- profile-local dynamics: comparison changes do not automatically change basic reliance.

Task 13 should import only the following compact meta-interface:

```text
node n=(w,s)
compatible reachability <=
fixed query chi=(e,q,P)
current assessment A_chi(n)
pathwise EventuallyStable
modal StableNow
scheme-relative CertifiedStable
optional external SemFinal and True_w.
```

Full branching graphs, confidence regions, dominator events, and freeze certificates can remain semantic constructions or extensions rather than primitive paper-level sorts.

Task 14 consequently did not infer unconditional stability from append-only records; Tasks 14 and 14B instead characterize update classes and typed read/write conditions that preserve required diagnostics. Theorem 2 supplies the deterministic special case, while Theorem 5 supplies a countertheorem for comparison profiles under candidate expansion.

### 13.1 Classical-pattern positioning

Theorems 1 and 4 use classical patterns rather than claiming new general impossibility principles. Theorem 1 is a finite-observation indistinguishability argument in the convergence-versus-known-arrival tradition represented in this project's literature by Kelly (`Kelly1996`). Theorem 4 is an elementary stopping-time/local-change-of-measure argument in the sequential-testing setting initiated by Wald (`Wald1945`). The simultaneous-coverage premise used around Theorem 3 has classical confidence-sequence precedents in Darling and Robbins (`DarlingRobbins1967`) and Robbins (`Robbins1970`). Bahadur and Savage (`BahadurSavage1956`) prove a different, source-specific nonexistence result for broad nonparametric problems; it is related context, not a theorem imported here.

The project-specific content lies in the typed continuation semantics, profile lifting, and especially the polarity-sensitive open-library result: supported finite-library non-domination remains defeasible under valid dominator extension, while a persistent dominator can stabilize refutation. [`08b_audit_repairs.md`](08b_audit_repairs.md) records the exact transfer boundary and verified metadata.

## 14. Theorem and countermodel audit

| item | classification | principal assumptions | contribution |
|---|---|---|---|
| Theorem 1 | classical-pattern impossibility restated in the license setting | same finite state; one live alternative; stage-local verifier | separates present evidence from certifiable permanent stability |
| Theorem 2 | sufficient-condition theorem | deterministic evaluator; complete frozen dependencies and rules | identifies when internal stability certification is legitimate |
| Theorem 3 | convergence theorem | eventual coverage; shrinking regions; nonzero margin | establishes pathwise statistical stabilization |
| Theorem 4 | classical sequential-decision pattern restated in the license setting | adapted stopping rule; opposite regimes; finite-prefix mutual absolute continuity | rules out uniform zero-error finite regime declarations |
| Theorem 5 | impossibility theorem | supported comparison; valid history-preserving dominator extension | establishes positive open-library non-finality |
| Proposition 6 | counterexample to overstatement | persistent existing dominator | refutes polarity-unrestricted comparison instability |
| Countermodels 9.1–9.5 | separation results | explicit continuation patterns | separate extendability, convergence, profiles, and finality |

Definitions such as `StableNow` and the observation that a live alternative negates it do not count by themselves as theorem weight. The classical-pattern results receive no novelty credit by renaming. The package's project contribution is the integration with typed licenses, profile transport, and the directional comparison construction.

## 15. Decisions fixed by Task 12

1. Stability always fixes `(e,q,P)`; selection stability additionally fixes the selector.
2. Eventual pathwise constancy, permanent current stability, certified stability, semantic finality, and truth are distinct.
3. A sound stability certificate must verify continuation invariants or exclude live alternatives; a current atom witness alone is insufficient.
4. Deterministic proof-backed atoms admit positive certification only under frozen dependencies and rules.
5. Statistical atoms may stabilize with high probability away from a boundary without admitting a zero-error finite announcement over a rich family.
6. Open-library non-finality is directional: supported finite-library non-domination is defeasible by valid model addition; persistent refutation may be stable.
7. Mere extendability entails neither convergence nor endless change.
8. Query stability does not imply complete-library or semantic finality.
9. `Final`, `Complete`, and `True` remain metalanguage notions, not base license operators.
10. No Löb/GL or “anti-Löbian” theorem is part of the core.

## Task conclusion

Open-endedness is now represented by a class of compatible finite-state continuations, not by a fifth truth value or an infinitely large current model. The logic can grant present reliance while remaining explicit about what would change that grant. Some atoms can be certified stable because their dependencies are institutionally frozen; statistical atoms can converge without a zero-error signal that convergence has arrived; and positive finite-library comparison claims remain non-final when the admissible candidate space can always produce a valid dominator. These facts coexist with stable older-model reliance under another profile and with indefinite growth of the archive.

The resulting position is deliberately modest but rigorous: the project does not prove that final truth is impossible. It proves conditional limits on what a finite stage can soundly certify, gives positive conditions for stability where they exist, and shows exactly why profile-relative reliance can remain useful inside an inquiry that has not certified its own end.
