# Checkpoint C1: Empirical Adjudication, Coverage Cost, and Artifact Integrity

Date: 2026-07-18
Status: completed; Task 22 is next
Scope: the ReLU-semantics clarifications after Checkpoint C, Tasks 19--21,
Task 20R, the required pre-checkpoint interpretation, External Audit IV, and
the complete pending publication roadmap

## Durable decision summary

1. **The frozen experiment remains internally valid and final.** The one v1.1
   confirmation run, its world-first analysis, and its registered decision
   rules are unchanged. No outcome-selected rerun, relabeling, threshold
   adjustment, or calibration repair is authorized.
2. **The aggregate `F35/H18.1` disposition remains `I1`, but the word
   “inconclusive” is insufficient by itself.** The result is mixed with
   decisive opposing effects: structured learning strongly wins tolerance
   transfer and strongly loses the registered boundary and in-regime
   comparisons. The aggregate rule and reverse-falsification rule each fail.
3. **The registered components receive separate, non-retroactive rows.**
   `F35a` tolerance-transfer superiority is `S1`; `F35b` boundary superiority
   and `F35c` in-regime noninferiority are each `X1` at their registered
   margins under the registered interval procedure. The observed superiority
   of direct cross-entropy on the latter two metrics is descriptive, not a
   newly invented confirmatory hypothesis.
4. **`F36/H18.2` remains `S1` only at its exact registered scope.** It supports
   marginal target-in-proposal coverage in the frozen `J` and `T`
   exchangeable groups. It does not establish conditional, profile, selected,
   routed, deployed-task, finite-system, or world-truth coverage.
5. **No architecture or empirical system claim was tested.** Hard MoE was
   prospectively omitted before learner implementation and receives no
   empirical disposition. The certificate/system tier is a successful
   deterministic integration witness for the already scoped formal interface,
   not powered evidence of system adequacy.
6. **The empirical lesson is information reuse with a large operational
   coverage cost.** The structured arm retained numerical information that
   transferred under changed tolerances, but its accepted conservative regions
   produced many open states, large support/refutation miss rates, and
   `0.9962` fallback mass. Information preservation, marginal calibration,
   cautious withholding, and useful decision coverage are different
   objectives.
7. **External Audit IV found a real preregistration weakness but overstated
   its derivation.** Conservative dead-band geometry is the leading
   post-result explanation and should guide future design. It was not proved
   at freeze time that every `.25 sigma` boundary case had to become Open, and
   `F36` does not force pointwise overshoot of the oracle endpoint. The durable
   process correction is nevertheless accepted: before freezing a future
   directional alternative, derive it against the generator constants and
   applicable project theorems, and record any unresolved mismatch.
8. **The public hash failure was an artifact-transport erratum.** Git had
   normalized seven frozen CRLF JSON artifacts to LF, breaking their public
   raw-byte hashes while leaving the run's internal chain and scientific
   content unchanged. Their exact registered bytes are restored, future JSON
   versions have an LF-stable writer, and completion now includes local checks
   plus a green-or-explained public CI result once a commit is pushed.
9. **The roadmap remains ordered and finite.** Tasks 22 and 22A remain
   independent of `F35`; no immediate repair experiment is inserted. Tasks
   23--34 are retained with targeted empirical-narrative, limitation,
   trace-schema, and audit obligations. Task 22 is next.

## 1. Evidence considered

This checkpoint applied the protocol in `TODO.md` and rechecked the project
question, required public artifacts, living specification, claim ledger, and
decision log. It read the artifacts produced since Checkpoint C, including the
three ReLU-semantics clarifications; the Task 19 preregistration; Task 19A's
generator, pilot, manifests, protocol, and prospective extension decisions;
Task 20's matched learners, exact decoder boundary, trace schema, and
deterministic system witness; the v1 failure/interruption records and runtime
diagnosis; Task 20R's versioned execution-only repair and differential gates;
and Task 21's compact checkpoints, machine analysis, figures, results,
deviations `21-D1` through `21-D5`, and unavailable secondaries.

The required
[`C1_precheckpoint_F35_interpretation.md`](C1_precheckpoint_F35_interpretation.md)
was read as human-facing evidence and questions, not as the adjudication
itself. External Audit IV in
[`claude_audit_2026-07-17.md`](../../llm_convos/claude_audit_2026-07-17.md)
was checked against the code, contracts, hashes, generator constants, Task 17
recovery theorem, and frozen analysis rather than accepted by authority. The
founding conversations were used only to trace which motivation the result
bears on; they are not empirical evidence.

The numerical record is coherent. The audit independently reproduced the
Task 21 estimates, multiplicity mechanics, and frozen aggregate rules. This
checkpoint also reproduced the reported public-verification failure before
repair: 158 of 161 checks passed, with the remaining failure and two errors all
arising from the same newline/hash mismatch.

## 2. Artifact-transport erratum and verification contract

### 2.1 What failed

The frozen experiment ran on Windows, where the historical JSON writers used
text-mode newline translation. They wrote CRLF bytes and the runners hashed
those bytes. Git later normalized the committed files to LF. On Linux, the
committed `protocol_v1.json`, `manifests_v1.json`, and
`pilot_results_v1.json` therefore failed the preregistration chain; the three
committed v1.1 stage checkpoints and `analysis_v1_1.json` likewise failed the
hashes recorded by their consumers.

Converting exactly those seven files back to CRLF recovers every registered
digest exactly:

| artifact class | recovered registered hashes |
|---|---|
| protocol, manifests, pilot | `3467f5e2...`, `0819522e...`, `91ac7195...` |
| selection, fit, calibration | `84e7456a...`, `1298e87f...`, `48663fa8...` |
| analysis | `dbb17686...` |

The LF `implementation_v1_1.json`, by contrast, is already the byte sequence
bound by every stage as `603dcceb...`; it was deliberately not converted.
This selective restoration is evidence preservation, not re-freezing.

### 2.2 Classification and repair

This is an **execution-environment artifact-transport erratum**. Its severity
was high for public auditability and public trust: the advertised one-command
verification failed in a clean Linux checkout, and public CI was red while
several local completion notes said tests passed. No evidence indicates any
change to a scientific endpoint, world, seed, fit, calibrator, trace value,
analysis rule, or internal provenance binding. It is therefore neither a
scientific-protocol deviation nor a reason to change the Task 21 result.

The repair has three parts:

1. `.gitattributes` marks `experiments/*.json` as byte-preserved so Git does
   not normalize any committed experiment JSON.
2. The seven affected files contain their original registered CRLF bytes.
3. New experiment versions use `experiments/artifact_io.py`, whose atomic
   writer explicitly opens UTF-8 text with `newline="\n"`; a regression checks
   the exact bytes.

The historical `run_pilot.py`, `run_experiment.py`, and
`run_repaired_experiment.py` writers are source-hashed frozen evidence. Editing
them merely to adopt the new helper would break the very provenance chain this
repair restores. They remain unchanged; the LF helper is a prospective
contract for new versions. RFC 8785/JCS remains a reasonable optional
canonicalization convention for a future protocol, but it is not adopted
retroactively and no v1/v1.1 raw-byte digest changes.

After the repair, all 162 local repository checks pass, including link checks,
the original protocol and v1/v1.1 source guards, the restored cross-artifact
hash chain, native/Python decoder equivalence, and the new transport
regression. The C1 commit is local because the project rule forbids automatic
push and the author did not request one. Public CI for this commit is therefore
not yet observable; it must be checked when an authorized push occurs rather
than silently described as green.

### 2.3 Standing completion and preregistration rules

A task or checkpoint now requires a passing local verification command. Once
its commit is pushed, the corresponding public CI run must also pass, or the
completion note must state why it did not and what remains unresolved. This
does not authorize an automatic push.

For future generated artifacts, raw-byte hashing requires an explicit
serialization and newline convention. For future empirical protocols, every
registered directional alternative must be checked on paper against the
frozen generator constants and applicable theorem bounds before freeze.
Failure to derive a direction is not automatically fatal, but the protocol
must either revise the endpoint or state that the direction is an empirical
conjecture rather than a theorem-predicted effect.

## 3. Registered empirical adjudication

| claim | frozen evidence | C1 disposition | consequence |
|---|---|---|---|
| aggregate `F35/H18.1` | only transfer passes; the reverse rule also fails | `I1`: mixed with decisive opposing effects | no general preference for the tested structured objective |
| `F35a`, transfer superiority | delta `+0.1866`, interval `[0.1860,0.1873]`, Holm-adjusted `p=0.00019998` | `S1` at the registered synthetic scope | supports reusable statistic information under changed tolerances |
| `F35b`, boundary superiority | delta `-0.2612`, interval `[-0.2636,-0.2587]`; its upper endpoint is below the registered `+0.05` alternative margin | `X1` at the registered margin and interval procedure | the tested structured pipeline does not deliver the predicted boundary advantage |
| `F35c`, in-regime noninferiority | delta `-0.1009`, interval `[-0.1022,-0.0997]`; its upper endpoint is below the registered `-0.02` guard | `X1` at the registered margin and interval procedure | the tested structured pipeline incurs operational degradation in ordinary cases |
| `F36`, loss `J` | coverage `0.9098`; Holm lower bound `0.9085 >= 0.88` | `S1`, registered marginal target-in-proposal scope | no extension to conditional or downstream coverage |
| `F36`, latency `T` | coverage `0.9044`; Holm lower bound `0.9033 >= 0.88` | `S1`, registered marginal target-in-proposal scope | same scope boundary |
| hard-MoE seam comparison | prospective feasibility/power gate failed; no implementation or final endpoint | no empirical disposition | Task 17's seam theorem remains formal; no architecture comparison exists |
| empirical system audit | only the deterministic adapter/certificate/rank witness ran | illustrated and implemented, not empirically tested | `E34`'s finite theorem and integration witness survive; empirical system adequacy remains unsupported |

The component rows are legitimate because transfer, boundary, and in-regime
were frozen endpoints with frozen margins, intervals, and roles inside the
registered conjunction. Recording their evidential grades does not change
what counted as aggregate support. Conversely, `F35b` and `F35c` refute the
registered structured-arm claims; they do not turn the opposite statement
“CE is superior” into a confirmatory claim that was never registered. The
narrow intervals and eight-seed directional stability make the observed CE
advantages strong descriptive findings.

`F36` supports a procedure-level marginal proposal statement. All expansions
happened to be finite and binding rejection happened to be zero, but these are
descriptive properties of this run. They do not license selection, profile
conjunction, routing, deployment, a frozen system, or a target-world fact.

## 4. What the opposing effects mean

### 4.1 Information retention survived; operational dominance did not

The tolerance-transfer result directly tests a central motivation for
retaining a numerical adequacy statistic rather than only its current label.
Without retraining, the structured arm reached `0.9436` on changed-tolerance
queries versus `0.7570` for direct CE. This supports a scoped empirical claim
that the learned numerical interface preserved useful threshold-relative
information. The tolerance is itself a scorer input and the scorer is
re-evaluated for each query, so this is strong no-retraining generalization by
a statistic-output interface, not evidence that one invariant numerical
region was literally reused. It does not prove semantic alignment, causal
faithfulness, or a universal advantage over classifiers that also receive the
tolerance.

The operational result is equally real. At the frozen current-threshold
queries, accepted structured regions nearly eliminate false positive
assertions but miss many correct support/refutation decisions. Unweighted
false-support and false-refutation rates are `0.0087` and `0.0146`, while
support and refutation misses are `0.4611` and `0.3248`. The resulting
target-weighted fallback mass is `0.9962`, compared with `0.9139` for CE.
Calibrated and cautious is not the same as discriminating and useful.

### 4.2 Conservative dead-band geometry: leading explanation, not proved cause

The project already proves that a conservative accepted region opens an
uncertainty band around a decision boundary. The boundary panel deliberately
places queries at near support, inclusive support equality, a crossing, and
near refutation. In particular, its equality reference uses
`epsilon=u*`, whereas the structured decoder supports only when
`upper(U_safe)<=epsilon`; any learned-envelope overshoot turns that reference
support into Open. The observed accepted `J` width is about `0.04006`, compared
with an average oracle width of about `0.03290`, and the miss/fallback pattern
is consistent with a widened dead band.

External Audit IV correctly identifies that this geometry should have been
analyzed before the directional alternative froze. Two stronger statements in
its C21 derivation do not follow, however:

1. `F36` covers sampled targets marginally. It does not imply, case by case,
   that `upper(U_safe)>u*`, so it does not mechanically forfeit every equality
   cell.
2. If one temporarily ignores information carried by the declared threshold,
   a hidden loss intercept with standard deviation `.006` would add a
   visible-feature-only 90% half-width of
   `k(sqrt(sigma^2+.006^2)-sigma)`. In units of `sigma`, that increment is
   about `.681` at `sigma=.006`, `.273` at the typical `sigma=.010`, and
   `.145` at `sigma=.014`. It is not uniformly larger than the `.25 sigma`
   near-boundary offset. Moreover, the scorer is given the declared threshold,
   which the generator constructs from `U*`; the intercept is therefore not
   wholly absent from every permitted input.

The safe conclusion is narrower and stronger methodologically: conservative
region width and exact decoding are a plausible, quantitatively consistent
mechanism for much of the deficit, but the completed experiment did not
identify the separate causal contributions of the loss, fit, calibration
expansion, decoder, threshold construction, generator, or their interaction.
The experiment supplies the effect sizes; a new prospective study would have
to establish the decomposition. This correction preserves the aggregate
`I1` disposition and prevents a post-result explanation from becoming a
retroactive theorem or rescue.

### 4.3 The matched-coverage drift

Checkpoint C required boundary risk “at matched coverage.” The frozen Task 19
primary instead compares raw boundary macro accuracy. With fallback masses of
`0.9962` and `0.9139`, the two arms answer at materially different rates, so
raw accuracy mixes information quality with abstention policy. The frozen
endpoint still governs; this traceable design drift neither invalidates it nor
authorizes a post-hoc matched-coverage result.

Any separately versioned follow-up must make matched coverage or full
risk--coverage curves primary, preferably alongside per-stratum/asymmetric
calibration or decision-cost-weighted decoding. Accuracy, false assertions,
misses, and fallback mass must be reported together. Deviation `21-D3` means
target-weighted trace errors, polarity/mode/diagnostic breakdowns,
selected/deployed loss, and misroute severity cannot be reconstructed from the
committed compact traces. Their absence cannot rescue or overturn the core.
A future trace schema must prospectively retain target/design weights,
polarity, evidence mode, and compact diagnostic fields sufficient for these
registered analyses.

## 5. Project and paper impact

The result does not threaten the finite-stage motivation, profile-indexed
license calculus, `WF + K_3` semantics, evidence/checker boundary, atlas and
update results, proof-carrying plans, or finite ReLU/CPWL representation
theorems. Those objects never entailed that one learned objective would be
operationally superior.

The tolerance-sensitive information-retention claim and the exact marginal
calibration claim receive scoped empirical support. The selected
center--radius/calibration/conservative-decoder pipeline as a generally
preferred classifier is seriously weakened: one registered component is
supported and two are refuted at their margins. Architecture superiority,
activation alignment, scientific-domain alignment, mechanistic
interpretability, human inspectability, and empirical system adequacy remain
untested.

The founding intuition therefore has an asymmetric result. The margin or
statistic as reusable tolerance-sensitive content survived its first
adversarial comparison. The later Task 18 engineering default that the same
certificate pipeline would also be the better current-threshold classifier
did not. Public prose such as “gradient descent built the license calculus”
must be qualified: it built a calibratable and highly withholding interface,
not an operationally competitive complete license system.

The paper-facing empirical sentence is now frozen for Task 25:

> Structured learning preserved numerical information that transferred
> strongly across changed tolerances, but the tested conservative pipeline
> paid a large price in boundary fidelity, ordinary-case fidelity, and usable
> coverage. Information preservation, marginal calibration, cautious
> withholding, and operational decision quality are distinct objectives.

Fallback mass and miss rates must remain physically adjacent to accuracy and
coverage numbers wherever the paper describes safety or calibration.

## 6. Disposition of External Audit IV

| item | disposition | checkpoint action |
|---|---|---|
| C20, newline/hash transport | accept | restore exact registered bytes, preserve them with `.gitattributes`, add a prospective LF writer and regression, record this erratum |
| C21, conservative geometry | accept the design lesson and leading mechanism; correct the claimed pointwise implication and uniform `.27 sigma` bound | adopt pre-freeze direction derivation; present the causal decomposition as future work, not theorem or rescue |
| C22, unmatched boundary coverage | accept | record the checkpoint-to-protocol drift and require matched coverage/risk--coverage in any follow-up |
| S13, public CI contract | accept | require local green and pushed-CI green or an explicit exception; do not auto-push |
| S14, propagation checklist | accept as corrected above | split ledger components, carry C21/C22 and `21-D3`, preserve Task 22 independence, repair C20 |
| L10, RFC 8785/JCS | defer as optional prospective convention | do not alter frozen raw-byte hashes; revisit only when a new protocol version is designed |

Audit IV also verified the prior audit corrections and the cumulative chain
from preregistration through analysis. No completed theorem or semantic task
is reopened.

## 7. Rejected changes and future-study boundary

This checkpoint rejects:

- another final-confirmation run selected after seeing `F35`;
- retrospective changes to labels, endpoints, margins, weights, tolerances,
  losses, calibration, or decoder rules;
- aggregate relabeling of `F35` as supported or globally falsified;
- confirmatory language for CE superiority on boundary/in-regime metrics;
- claims that CE is universally better or structured learning universally
  worse;
- any empirical conclusion about hard MoE or another architecture;
- any interpretability upgrade from named structured channels alone;
- weakening a representation theorem merely because its implementation did
  not dominate empirically;
- re-freezing or canonicalizing v1/v1.1 hashes under a new digest convention;
- inserting a repair experiment before Task 22; and
- changing Tasks 22 or 22A because `F35` was deliberately not their premise.

A future conservatism study is legitimate only as a separately versioned,
prospectively frozen experiment against a declared generator. It should test a
causal mechanism, not repair the original confirmation, and should retain the
trace fields needed for matched-coverage and deployed-risk analysis. The
current publication path can report the trade-off honestly without waiting
for that study.

## 8. Prospective roadmap review

Every unfinished work item was reconsidered.

| item | C1 decision |
|---|---|
| Task 22 | retain unchanged and make next; its identifiability/literature audit is independent of `F35` |
| Task 22A | retain unchanged; recursive-judgment information and system licensing remain separate |
| Task 23 | retain; explicitly deny any interpretability upgrade from `F35` and include licensed-coverage/fallback feasibility |
| Task 24 | retain and amend with conservatism/coverage cost, C22 drift, `21-D3`, and future trace obligations |
| Task 25 | retain and amend the lead answer with the component grades, founding-intuition asymmetry, dead-band hypothesis, and frozen empirical sentence above |
| Checkpoint D | retain; require an audit that the C1 claim grades and limitations actually reached the outline |
| Task 26 | retain; inherit Task 25's post-result answer instead of saying learnability simply remains untested |
| Task 27 | retain unchanged; the empirical result does not alter the compact semantics |
| Task 28 | retain unchanged; representation and recovery theorems remain explicitly non-dominance results |
| Task 29 | retain with the objective-comparison evidence at its component grades; no architecture comparator exists |
| Task 30 | retain; require negative components first, matched-coverage drift, adjacent fallback/miss rates, and the corrected mechanism status |
| Task 31 | retain; audit aggregate/component inference, `F36` scope, transport erratum, unavailable secondaries, and absence of CE/architecture confirmation |
| Task 31A | retain; ensure “mixed” is not rendered as low power and a plausible mechanism is not narrated as proved geometry |
| Checkpoint E | retain unchanged as the post-audit publication gate |
| Task 32 | retain; include clean-checkout artifact-hash verification in publication readiness |
| Task 33 | retain; carry transfer versus coverage and safety versus usefulness into plain prose |
| Task 34 | retain; crosswalk both public artifacts against `F35`, `F35a--c`, `F36`, and the no-claim boundaries |

No reorder, merge, new gate, or immediate empirical follow-up is justified.

## 9. Remaining risks and unresolved obligations

1. The local repair is not yet visible in public CI because this checkpoint is
   not authorized to push; the first authorized push must verify and record
   the run.
2. “Mixed” can still be misread as underpowered unless every use includes
   “decisive opposing effects” or the three component results.
3. Marginal calibration or low false-assertion rates may be marketed as useful
   system safety while the `0.9962` fallback mass is omitted.
4. Descriptive CE advantages may drift into confirmatory or universal
   architecture language.
5. Conservative dead-band geometry may be narrated either as a mystery or as
   a proved causal account; the warranted middle position is a mechanism
   consistent with theory and the observed traces, pending a prospective
   decomposition.
6. A later conservatism study may be mistaken for a repair unless its version,
   hypothesis, endpoints, and no-rescue relation to v1/v1.1 are explicit.
7. The final paper may inherit ledger/audit register rather than turn this
   result into a human argument. Task 25, Checkpoint D, and Task 31A remain the
   guards.

## 10. Next task

Proceed to **Task 22 -- Audit the policy--value and recursive-judgment
claims**. Do not begin Task 22 during this checkpoint.
