# Checkpoint D: Pre-Draft Coherence and Policy/Value Rigor Gate

Date: 2026-07-21
Status: completed; Task 22B is next
Scope: Tasks 22--25, Checkpoint C1 propagation into the frozen publication
contract, External Audit V, the current public-verification signal, and every
unfinished item through Task 34

## Durable decision summary

1. **The proposed paper is coherent at its present core scope.** It answers one
   human question: how a bounded agent can represent justified reliance on
   useful models during open-ended, domain-sensitive theory succession without
   asserting that its current model is final. The profile-indexed calculus,
   stability/update results, typed locality, neural representation boundary,
   and mixed experiment form a connected argument rather than a list of
   unrelated repository artifacts.
2. **One bounded formal bridge task is required before drafting.** Task 22B will
   state and prove an oracle action-gap behavioral bound, derive its certified
   corollaries only under accepted error/gap evidence, give finite executable
   witnesses, and delimit the result's semantic and distributional scope. This
   closes the precise gap between Task 22's abstract representation-existence
   result and Task 23's unrun interpretability program.
3. **The finite “isomorphism” existence claim remains supported at its declared
   objects.** For an injective encoder `E` and a decoder satisfying
   `D(E(pi))=pi`, policies correspond exactly to the encoder image. Checkpoint D
   does not infer that standard return-based value functions are unique or
   policy-only inverse representations. It also does not infer that the
   existence construction is natural, readily learned, or semantically rich.
4. **Raw recovery and conservative certification are different guarantees.**
   If every action score is approximated within `rho`, raw `argmax` recovery is
   stable where the intended action gap exceeds `2 rho`. A conservative decoder
   that must also certify its estimated winner can require a true gap exceeding
   `4 rho` to guarantee both recovery and non-abstention when its pairwise-gap
   error radius is obtained by the generic `2 rho` triangle bound. Task 22B must
   state these separately and may use a tighter pairwise certificate when one
   is actually available.
5. **Return semantics adds a real assumption.** The same action-gap geometry
   applies to a learned `Q^pi`, but decoding reconstructs `pi` only on states
   where `pi` is greedy for its own declared `Q^pi`, with compatible ties,
   perspective, state, and horizon/discount conventions. Elsewhere the decoder
   performs policy improvement. A scalar `V^pi` additionally needs a declared
   decision harness containing the environment and reward/return rule.
6. **Training agreement supplies no automatic generalization result.** Task 22B
   will distinguish pointwise/training-set recovery, held-out agreement under a
   named distribution, and trajectory-level behavior. “Generalizes the same
   way” remains a future empirical conjecture until a prospective companion
   study supplies the needed distribution, learner, and sequential assumptions.
7. **No bridge experiment is inserted before the paper.** The companion remains
   an implementation witness at pinned commit `097ea889...`. Future empirical
   work waits for its open PyTorch-migration tasks, records a fresh pin, and
   freezes thresholds and evidence roles before outcomes. Checkpoint D neither
   runs nor modifies that repository.
8. **The author's semantics-backward motivation is now durable.** A licensed
   value-like output is proposed as a first semantic foothold from which future
   work might investigate stable semantic structure deeper in a network. Work
   on an independently trained surrogate's layers concerns that surrogate; an
   inward claim about the original policy additionally needs an explicit
   alignment/readout link and policy-side interventions. This is attributed
   motivation, with representation and intervention evidence as gates.
9. **External Audit V's concrete maintenance findings are accepted with one
   factual precision.** The workflow omitted NumPy, Matplotlib, and PyTorch
   installation; the audit manifest omitted three audits; `Afriat1967` lacked
   a bibliography entry; and the Task 22A handoff blurred a true Bayes baseline
   with a merely declared comparator. These are repaired. The public run at the
   audited head actually stopped first on three missing-NumPy collection
   errors; the audit's two missing-Torch errors came from a differently
   provisioned environment.
10. **Drafting remains the next phase after Task 22B.** Tasks 26--30 receive
    clearer section ownership, Tasks 31/31A and Checkpoint E remain the two
    publication audits, and Tasks 32--34 remain appropriate. No new experiment,
    broad literature survey, architecture comparison, or Lean formalization is
    required before drafting.

## 1. Evidence considered

This checkpoint applied the protocol in [`TODO.md`](../../TODO.md). It read the
current project specification and claim ledger, the completed Task 22
policy/value judgment, Task 22A judgment-information theorem, Task 23
interpretability design, Task 24 limitations synthesis, and Task 25 publication
contract. It checked the founding conversations under `llm_convos/` and the
four posts as provenance for the author's intended arc. Those sources inform
the motivation; they do not substitute for proofs, literature, or experiment.

External Audit V,
[`claude_audit_2026-07-21.md`](../../llm_convos/claude_audit_2026-07-21.md),
was independently checked rather than adopted wholesale. The local repository
was clean at audited commit `59ae3cc` apart from the new audit file. The current
remote head of the companion was separately checked as
[`097ea8897fb203b9b3a6ceafcb29e11bdc6cdd6c`](https://github.com/TristanMiano/policy_value_isomorph/commit/097ea8897fb203b9b3a6ceafcb29e11bdc6cdd6c),
the same pin recorded by Task 22. Its README, design, reproducibility note,
migration audit, and TODO show a useful small deterministic-game scaffold and
an unfinished PyTorch migration. No companion code was executed.

The public workflow was also inspected at the exact audited head. GitHub run
[`29675939364`](https://github.com/TristanMiano/value_logic/actions/runs/29675939364)
is red. Its actual first failure is collection of three experiment test modules
because NumPy was not installed. Two of those modules import the learner and
will also require PyTorch after NumPy is available; the analysis module imports
Matplotlib at collection time. The workflow now installs the experiment's
pinned NumPy and CPU-only PyTorch versions plus prospective Matplotlib 3.10.8
for analysis imports. The original analysis contract did not record its
Matplotlib version, so this clean-checkout pin is not presented as a recovered
run-environment fact. Because this checkpoint is committed locally and the
standing rule forbids an automatic push, a repaired public result cannot yet be
observed; the first authorized push must be followed by a CI check.

## 2. Does the frozen outline form one argument?

Yes. The outline's strongest connective tissue is the running succession
example, not the number of formal objects. A reader first sees an old model, a
successor, a fallback, and a task whose tolerated loss is derived from what the
fallback already achieves. That makes `epsilon` a decision-relevant threshold
rather than a probability of falsehood. The finite profile then states which
adequacy, improvement, constraint, and trace conditions authorize reliance.
Four-way assessment permits refusal, withholding, and ill-formedness without
pretending that every unavailable license is a false scientific theory.

The open-endedness results answer the temporal part of the lead question: a
finite agent can state current, eventual, or certified stability under explicit
conditions while leaving semantic finality outside the object language. The
locality and update results answer how revision can be auditable without
recomputing an unspecified worldview. The representation results then show how
the finite assessment interface can be realized by a hybrid symbolic/neural
system, and exactly which semantics are external to arbitrary activations. The
experiment tests one learning implementation of that boundary. Its mixed result
is narratively useful because it demonstrates why representational information,
calibrated caution, and usable decision coverage must remain distinct.

The paper therefore does not need every theorem to be a headline. Its four
formal clusters are a defensible upper bound, and three would still carry the
argument if drafting folds typed locality/update persistence into the
open-ended stability cluster. Transport, routing, finite certified composition, and the
Task 22A information result remain support structure. The optional policy/value
section has a different role: it explains why obtaining a semantically named
statistic from a black-box policy could matter beyond the synthetic example.
Task 22B is warranted because it connects that role to the same margin geometry
as the core rather than enlarging the paper with another empirical program.

## 3. Checkpoint C1 propagation audit

Every required component is present in the frozen claim set and section plan.
No result needs to be rerun or regraded.

| required item | frozen public treatment | Checkpoint D disposition |
|---|---|---|
| aggregate `F35` | `I1`, explicitly “mixed with decisive opposing effects” | retained; “mixed” must never imply low power |
| `F35a` | `S1`, tolerance-transfer difference `+0.1866` | retained as no-retraining changed-tolerance generalization, without literal invariant-region language |
| `F35b` | `X1`, boundary difference `-0.2612` at the registered superiority margin | retained beside `F35a`, with direct-CE advantage descriptive rather than retroactively confirmatory |
| `F35c` | `X1`, in-regime difference `-0.1009` at the registered noninferiority margin | retained beside `F35a`, with the same registration boundary |
| `F36` | `S1`, marginal coverage `0.9098` for `J` and `0.9044` for `T` | retained only as marginal target-in-proposal coverage |
| miss/fallback companions | unweighted misses `0.4611/0.3248`; target-weighted fallback `0.9962` | kept physically adjacent to coverage and low false-assertion rates |
| matched-coverage drift | Checkpoint C asked for matched coverage; the frozen primary used raw boundary accuracy | disclosed as design drift; a matched-coverage study would be new prospective work |
| hard MoE / architecture | prospectively omitted; no empirical disposition | no architecture-superiority claim |
| system tier | deterministic integration witness only | no powered empirical system-adequacy claim |
| mechanism language | conservative dead-band geometry is consistent with the result | plausible explanation, without identified causal decomposition |

This propagation is sufficient for drafting. A new confirmatory run would not
repair the original registered result and would distract from the paper's more
interesting asymmetry.

## 4. The missing bridge result

### 4.1 The objects must be fixed before the word “isomorphism” is used

Let `S` be a state domain, `A(s)` a finite nonempty legal-action set, and `pi` a
deterministic policy. For forced states with `A(s)={pi(s)}`, use the convention
that the action gap is `+infinity`. A fixed score encoder `E` may assign an action-score
vector `W_pi(s,.)`, and a fixed transparent decoder `D` may select its unique or
tie-broken winner. Then

```text
pi -> E(pi) -> D(E(pi)) = pi
```

is exact on the encoder image. On that image, `E` and `D` are inverse maps; this
is the finite existence result Task 22 preserved. Starting from an arbitrary
score function, however,

```text
W -> D(W) -> E(D(W))
```

generally discards score magnitudes and all structure outside the canonical
encoder image. The exact existence statement should remain available when its
policy class, score class/image, decoder, tie convention, and preserved
structure are stated. Checkpoint D therefore does not adopt Audit V's categorical
recommendation to retire the word from public prose. Public prose should use the
more informative phrase **behavioral reconstruction** for the practical learned
claim and reserve “isomorphism” for the exact declared correspondence.

The decision harness is part of the represented system. It must be fixed,
transparent, and included in fidelity and complexity accounting. A harness that
contains a hidden lookup table for `pi` makes reconstruction vacuous; Task 22B
will include that countermodel.

### 4.2 Raw action-gap stability

For intended scores `W`, learned scores `W_hat`, a radius `rho>=0`, and an
intended policy action `pi(s)` that wins under `W`, define

```text
e(s) = max_a |W_hat(s,a) - W(s,a)|,
g(s) = W(s,pi(s)) - max_(a != pi(s)) W(s,a).
```

The second maximum is omitted at a forced singleton-action state, where
`g(s)=+infinity`. For an evaluation distribution `mu`, define
`D_mu(pi,pi_hat)=mu{pi_hat!=pi}`.

The Task 22B target is the pointwise implication

```text
e(s) <= rho and g(s) > 2 rho
    => argmax_a W_hat(s,a) = pi(s),
```

under compatible deterministic tie handling. Equivalently, for an evaluation
distribution `mu`, the disagreement risk obeys

```text
D_mu(pi,pi_hat)
  <= mu{e > rho} + mu{g <= 2 rho}.               (D.1)
```

This is the appropriate constructive formulation: score error and action gap
specify a region where reconstruction is guaranteed, and the bound
exposes the unresolved mass. A two-action tie/flip fixture will show that the
factor `2` cannot generally be improved under coordinatewise sup-norm error.
For Task 22's indicator-score encoder, the intended gap is one, so any uniform
error below one half gives exact raw decoding throughout any domain on which
that uniform bound is accepted. That representation remains semantically thin;
its strength is arbitrary-policy behavioral encoding.

Equation (D.1) itself is an **oracle inequality** because `e` and `g` are true
quantities. It becomes an operational certificate only when accepted evidence
supplies pointwise envelopes or valid upper bounds on the two masses. If a
jointly valid record gives `mu{e>rho}<=eta_e` and
`mu{g<=2rho}<=eta_g`, then it certifies
`D_mu(pi,pi_hat)<=eta_e+eta_g` at that record's stated mode and coverage. For a
learned `Q^pi`, neither true score error nor true action-gap mass is known merely
because the network emits scores.

### 4.3 Conservative certification is a second layer

Equation (D.1) concerns the behavior of a raw decoder. The value-logic interface
may demand a sound certificate before authorizing the decoded action. From
coordinate errors of radius `rho`, `r_gap:=2 rho` is a valid generic certified
pairwise-gap error radius. An estimated winner gap greater than this `r_gap`
soundly certifies the winner. A separately accepted direct gap-error certificate
may supply a smaller valid `r_gap`; an unverified smaller number may not be
substituted. To guarantee in advance that the conservative decoder both selects
and does not abstain, the existing generic recovery argument can require

```text
g(s) > 2 r_gap,
```

which becomes `g(s) > 4 rho` under the generic coordinate-to-gap bound. A
directly certified pairwise gap can be tighter. Task 22B must therefore keep
three objects visible: the true action gap, the learned estimated gap, and the
accepted error radius. It must not call the gap alone a full `Adeq` or
`P_surrogate-rely` license. At most it supplies a `DecodeStable`/behavioral
fidelity atom or an agreement-risk bound; value/ranking fidelity, support,
trace, and any selected profile requirements remain additional atoms.

### 4.4 Semantic variants

The one inequality supports several variants with different meanings:

- **Arbitrary-policy score encoding.** Indicator or canonical logits make the
  policy recoverable for any deterministic policy. They prove behavioral
  representation and margin robustness, while leaving return semantics open.
- **Return-semantic `Q^pi`.** Approximation of a declared environment-relative
  `Q^pi` yields the same raw stability result for its greedy decoder. Agreement
  with the original policy also requires self-greediness on the claimed states
  and compatible tie and perspective conventions. Global self-greediness is a
  policy-improvement fixed-point/optimality condition under the usual finite
  discounted assumptions; distribution-local self-greediness is weaker.
  Without the relevant condition the composite is policy improvement, which can
  be useful but is a different claim.
- **Scalar `V^pi`.** An action cannot be decoded from a state value alone. The
  harness must expose legal successor states, dynamics, immediate reward,
  perspective, and horizon/discount, and Task 22B must propagate value error to
  action-score error before applying the gap result.
- **Stochastic policies.** An `argmax` decoder recovers only a modal action.
  Distributional reconstruction needs normalized probabilities or a sampling
  harness and a fidelity measure such as total variation or KL. It is a scoped
  extension, not something the deterministic theorem silently covers.

These variants preserve the author's motivating possibility while preventing a
practical learned reconstruction from being mistaken for unique internal
utility recovery.

### 4.5 Generalization and trajectory scope

Agreement on a finite training set has no implication for states outside that
set: two score functions can agree on every training state and choose opposite
actions everywhere else. Task 22B will include this finite countermodel. A
held-out IID estimate can support disagreement under its named sampling
distribution with an ordinary concentration statement. It does not establish
the same generalization mechanism, shared inductive bias, or agreement after
the reconstructed policy changes the state distribution. Sequential claims
also require a horizon, visitation distribution, and coupling or imitation
analysis because small action disagreement can alter later states.

The phrase “might generalize the same way a trained model generalizes” is kept
as the author's bounded research hope. It will be restated as an empirical
question about two named learners and distributions. Task 22B will verify the
relevant primary literature on distillation, action gaps, imitation error, and
underspecification before allocating that question to future work.

## 5. Why this one task improves the paper

Task 22 currently supplies a clean exact existence proposition and clean
boundaries around standard return semantics and identification. Task 23 supplies
a seven-axis experimental design. What is missing is the intermediate statement
the author actually cares about: when an approximate semantic surrogate plus a
decision harness recovers the policy's behavior, and how much unresolved mass
remains. Equation (D.1), the certification distinction, and the semantic
variants provide that statement without pretending to answer whether true
utility exists.

This also explains why the policy/value section belongs in a value-logic paper.
The same margin-and-abstention pattern used for model reliance supplies a
transparent condition for behavioral reconstruction. The connection is not
that every action gap is already a complete use license. The connection is that
a certified gap can become one named, checkable requirement inside a profile
whose other semantic and evidential obligations remain explicit.

The author's longer-term motivation is then intelligible. If a value-like output
can receive stable declared semantics and a scoped license, it may become an
anchor for investigating whether related structure can be recovered further
inside a network. Probing the independently trained surrogate would establish
only surrogate-side structure. Reaching the black-box policy needs an explicit
alignment/readout link to policy hidden states, cross-seed and symmetry-aware
tests, and policy-side interventions. The present project records the direction
and the gates; it supplies no hidden-layer recovery claim.

## 6. External Audit V dispositions

| audit item | disposition | Checkpoint action |
|---|---|---|
| `C23`, red public CI | accepted with environment precision and import-closure repair | install pinned NumPy, Matplotlib, and CPU PyTorch; record the existing red run and require post-push observation |
| `C24.i`, stale audit manifest | accepted | add Audit III, IV, and V rows with target commits and adjudication links |
| `C24.ii`, missing `Afriat1967` | accepted | add the verified journal entry and DOI to `references.bib` |
| `C25`, “best declared” baseline | accepted | restore “true nuisance-conditioned Bayes baseline” and add the arbitrary-comparator regret identity |
| `S15`, one bridge theorem | accepted with corrected certificate geometry | insert Task 22B before Task 26; distinguish raw `2 rho` recovery from generic conservative `4 rho` non-abstention |
| `S16`, companion readiness/pin gate | accepted | add the migration, fresh-pin, and prospective-threshold condition to Task 23 and the roadmap |
| `L11`, targeted bridge literature | routed | Task 22B verifies and adds only sources actually used; no unreviewed bibliography batch at this checkpoint |
| retire “isomorphism” publicly | not adopted categorically | preserve the exact existence term with its objects/image/decoder; prefer behavioral reconstruction for practical learned claims |
| no bridge experiment before drafting | accepted | keep all empirical bridge measurements in prospective companion/future work |
| semantics-backward paragraph | accepted as attributed motivation | record it in Task 23, the ledger/specification, and the outline's future-work path |

The audit's proposed `2 rho` action-gap result is correct for raw argmax
stability. Its claim that this is simply the existing conservative theorem under
renaming skips the second certification error step. The corrected Task 22B brief
retains the useful unification while preventing a factor-of-two and scope error.

## 7. Revised pending roadmap

| item | decision and dependency |
|---|---|
| **Task 22B** | **new immediate gate**: write `formalism/10_policy_value_reconstruction.md` and a small pure-Python verification module; prove the oracle bound and evidence-certified corollaries, give tight witnesses/countermodels, distinguish score, `Q`, `V`, and stochastic cases, audit targeted literature, and propagate the result |
| **Task 26** | retained after 22B; owns title, abstract, introduction, motivation, contribution framing, and related work only; it may foreshadow the optional bridge but does not draft its technical result |
| **Task 27** | retained; owns the compact definitions/semantics and certificate-carrying plan interface, with the running example; it does not absorb H4 representation proofs |
| **Task 28** | retained; owns the H1--H3 theorem spine, open-endedness, update locality, composition/routing integration, and formal appendices for those results; it does not duplicate the H4 neural cluster or empirical section |
| **Task 29** | retained; owns H4's architecture-neutral contract, ReLU witness, learning contract, interpretability grades, and the optional Task 22B bridge proposition/Appendix F if it survives audit; numerical C1 adjudication remains in Task 30 |
| **Task 30** | retained; owns §7 empirical results and the discussion, limitations, future work, and conclusion; it reports every C1 component and no-claim boundary together |
| **Task 31** | retained and extended; audits Task 22B's factor, ties, harness, generalization language, literature, and exact CI status, in addition to all existing mathematics/citations |
| **Task 31A** | retained; checks that the optional §8 supports the single question “what semantic structure can a surrogate preserve?” and does not interrupt the main reliance argument |
| **Checkpoint E** | retained; publication readiness remains a real decision after both audits |
| **Tasks 32--34** | retained; Gist formatting, Substack adaptation, and final crosswalk remain correctly ordered |

No pending item is removed. The new formal task is narrow enough to improve the
optional section without turning the paper into a companion-project report.

## 8. Rejected additions and current risks

### No pre-draft empirical bridge run

A credible companion result would require the migration to finish, a new pin,
new split and provenance roles, preregistered fidelity and usefulness margins,
off-support and trajectory tests, and possibly human or causal arms. That is a
substantial study rather than a quick check. Its absence does not block the
current paper because Task 22B is a formal conditional result and the empirical
interpretability grades remain visibly unmeasured.

### No matched-coverage or architecture rescue experiment

Checkpoint C1's frozen result is informative as it stands. Adding a
matched-coverage analysis or alternative architecture after observing the
outcome would create a new study. The paper should state that need in future
work and retain the original design drift.

### No Lean formalization before drafting

Checkpoint B deferred proof-assistant work until a concrete ambiguity or proof
risk justified it. The candidate action-gap proof is finite and elementary;
its main risks are interface and scope distinctions that are better exposed in
the mathematical note and executable fixtures. Lean would not resolve whether
the score carries return semantics, whether the harness is nonvacuous, or which
distribution supports a generalization claim. Reconsider formalization after
the mathematical audit or as post-publication hardening.

### Remaining risks

1. **Register inversion.** Drafting can still lead with machinery rather than
   the human reliance question. Task 26 and Task 31A keep this explicit.
2. **Bridge overstatement.** “Isomorphism,” “value,” “reconstruction,” and
   “generalization” can each slide between exact, semantic, empirical, and
   mechanistic readings. Task 22B must type every arrow and Task 31 must audit
   every use.
3. **Certification conflation.** A raw action-stability bound can be mistaken
   for a full profile license. The `2 rho`/`4 rho` distinction and separate
   `DecodeStable` atom are mandatory safeguards.
4. **Optional-section bloat.** The main §8 budget remains about 500 words. Full
   proofs, stochastic extensions, countermodels, and literature details belong
   in Appendix F or the repository note.
5. **Public verification.** The workflow repair is locally reviewable but has
   no public green run until an authorized push. That pending observation must
   not be forgotten at Task 31 or the next push.

## 9. Completion and next task

Checkpoint D confirms the four-cluster publication contract with one scoped
amendment: Task 22B must finish the operational policy/value reconstruction
bridge before prose drafting begins. Maintenance repairs are applied without
changing any scientific artifact or empirical disposition. The local
repository verification and link suite passes after these changes. Public CI
for the repaired workflow is pending an authorized push.

**Next task:** Task 22B — prove policy/value behavioral round-trip stability and
delimit its semantic scope.
