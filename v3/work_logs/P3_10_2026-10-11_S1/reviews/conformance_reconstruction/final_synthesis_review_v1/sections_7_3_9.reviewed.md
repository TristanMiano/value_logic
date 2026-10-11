### 7.3 A decision value need not be an expected-loss observation

In the tied structural fixture, `take_p`, `take_r` and fallback have loss rows
`(4,0)`, `(0,4)` and `(3,3)`. Their robust maxima are 4, 4 and 3, so the declared
deterministic minimax menu selects fallback. For any law assigning probability
p to the first state, however, the expected losses are `4p`, `4(1-p)` and 3.
At least one specialized action has expected loss at most 2. Thus fallback is
never a best expected-loss action for any law on those two retained states.
The correct minimax reply cannot be read as an implicit Bayesian estimate.

The robust values themselves also fall outside the Q5 expected-loss map for
these same rows, even with shared positive affine calibration. Under
`v=s Lp+b1`, fallback's value minus the average of the two specialized values
is exactly s, which is positive. The robust vector `(4,4,3)` gives −1 instead.
This is an algebraic separation between the two declared services; it is not
a claim that arbitrary other value encodings cannot contain probability data.

A hypothetical independent fair lottery over the two specialized actions has
worst-over-states expected loss 2, but worst-over-states-and-realized-draw loss
4. It does not give uniform realized non-deterioration against fallback. The
frozen structural menu has no paid lottery implementation, so this calculation
adds no ordinary competitor or empirical saving. It identifies the quantifier
and action-menu limits of the existing optimality claim.

Likewise adding the same state-dependent term to every action preserves each
same-state loss difference and fixed-law expected-loss ordering, but can change
absolute minimax choice. Adding `(100,0)` to the displayed rows gives maxima
104, 100 and 103 and selects `take_r`. A uniform certificate for a fixed loss
difference is unaffected by that common offset. These worked examples show why
absolute risk levels, pairwise guarantees and probabilities require separate
semantic contracts.

The [decision-service interpretation](../work_logs/P3_10_2026-10-11_S1/decision_service_interpretation.md)
and [calibration/rank addendum](../work_logs/P3_10_2026-10-11_S1/decision_service_interpretation_addendum.md)
also explain sourcewise positive affine rank invariance. The general structural
rank can be a lexicographic vector; the deployed current-incumbent receiver has
one scalar tier. Rank transformations preserve their stated mathematical
domains only with the same feasible inputs and admitted encodings. They do not
preserve old request identities, invoices or receipt authority automatically.

## 8. Execution, failure, amendment and resource provenance

### 8.1 The exact stage history

The entry checkout and observed remote `main` both matched commit
`ea3e20dd9889c2ee22141c17390595867d33d8ab`, tree
`3900e2333e1324af72b0b7f51764bfecc79794ba`. The prepared freeze was verified
before final input exposure. Its manifest SHA-256 is
`69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70`;
the machine protocol SHA-256 is
`dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f`.
The 50 source/contract files, 114 method representations, 12 input groups and
500 ordered public units remain bound to that freeze. Initialization and
preparation were not rerun over it.

| Command scope | Observed UTC interval, October 11 | Result | Outer wall seconds |
| --- | --- | --- | --- |
| Original inputs | 14:50:46.554698–14:50:47.131975 | 12/12 sealed; exit 0 | 0.577288758 |
| Original public | 14:51:12.093871–15:20:33.534017 | 440 sealed; first structural unit fails; exit 1 | 1761.440233787 |
| A1 public | 15:33:18.105430–15:33:32.061967 | Remaining 60/60 sealed; exit 0 | 13.956550244 |
| A1 evaluation | 15:34:11.406473–15:34:54.518871 | 500/500 scored; exit 0 | 43.112428671 |
| A1 analysis | 15:35:50.452323–15:35:57.216183 | One complete frozen-endpoint analysis; exit 0 | 6.763867515 |

The original public failure at 15:20:33.505276 UTC is an
`AttributeError: 'NoneType' object has no attribute 'paired_request'` in
`conformance_structural_legacy__counterpossible_tied_minima__candidate`.
The inherited structural module initializes `M = K = None`. Its development
driver calls `_load_legacy()` before running the worker, but the frozen
conformance adapter omitted that prerequisite. Preparation checked a
pre-admission denial and did not exercise this initialized worker path.
Independent source reviews and an initialization-only clean-process probe
confirmed the deterministic omission.

An unchanged infrastructure retry was therefore ineligible and was not used.
The explicit versioned A1 amendment supplied that bootstrap before the
unchanged structural public worker and private verifier. It used the inherited
placement outside the paid meter, openly added and bound the continuation
source, and preserved the old verifier/runtime closure. No frozen source,
method, seed, budget, generator, threshold or scoring formula changed.

The A1 manifest binds all 1,365 original evidence files, totaling 134,825,103
bytes, excluding only the empty writer lock. Its SHA-256 is
`36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359`.
Original inputs and the 440 completed public units are reused through exact
references. The new public stage means 60 amended records; the separate
composite index binds all 500 original schedule positions to the 440 old and
60 new seals. Only after that barrier does private evaluation begin.

No original public, evaluation or analysis completion marker is manufactured.
The overall lineage remains amended, and all 60 conformance units are
conservatively labeled post-exposure amended inherited regression, including
the information units that did not themselves need the loader. The sealed
broker and certificate acquisitions are unchanged. The final-data observers
were released only after all amended official stages completed, at
15:37:22.120309 UTC. Their exploratory outputs never feed back into a paid run.

Evidence: [entry inventory](../work_logs/P3_10_2026-10-11_S1/entry_inventory.json),
[original and A1 command records](../work_logs/P3_10_2026-10-11_S1/commands),
[amendment selection](../work_logs/P3_10_2026-10-11_S1/amendment_selection.json),
[sealed A1 protocol](amendments/P3_10_A1/protocol.md),
[composite public barrier](final_v1_amended_A1/composite_public.json), and
[observer release](../work_logs/P3_10_2026-10-11_S1/completion_release_A1.json).

### 8.2 Physical observations and declared tariffs answer different questions

Execution used Linux, little-endian CPython 3.12.14, built with Clang 22.1.3,
and the exact frozen runtime/dependency closure. The entry platform identifies
Linux 6.18.44 x86-64 with glibc 2.39. This session's boot ID is
`0aa2a50c-3819-4728-bbd8-b8743f8bc121`. Raw command records include UTC and
same-runtime monotonic boundaries, exact arguments, exit codes, stdout/stderr
sizes and hashes, child user/system CPU and child peak resident memory.

| Outer command | Child user CPU seconds | Child system CPU seconds | Child peak RSS KiB |
| --- | --- | --- | --- |
| Original inputs | 0.553868 | 0.025613 | 26,716 |
| Original public | 1760.901368 | 0.388745 | 40,924 |
| A1 public | 13.324855 | 0.633138 | 588,024 |
| A1 evaluation | 41.372457 | 1.737399 | 607,500 |
| A1 analysis | 6.311963 | 0.453742 | 634,520 |

These outer process observations include verification and orchestration. They
are not invoices for an individual scientific service, a physical timing
comparison of paired algorithms, or additions to the principal research clock.
Concurrent reviewers and filesystem/cache state also prevent a causal speed
interpretation. Peak memory observations are not summed across commands.
All three successful A1 command stderr streams are empty; the original failure's
3,193-byte stderr remains preserved.

Broker terminal word charges, optional reporting charges, certificate observed
events/live-byte-period charges and structural VM charges retain their separate
declared scopes. Within a certificate invoice, producer/consumer coordinates
partition the total, while source/output/storage coordinates overlap other
diagnostics. Only disjoint primitive categories support the primitive-price
comparison; overlapping diagnostics are not added as another total.

### 8.3 What remains identifiable with the missing failed-prefix invoice

The original exception occurs after source/input admission and some worker
execution, but before an invoice is returned. The exact lost prefix and its
primitive-category vector are unknown. A source-only argument conditionally
bounds the structural meter counter between **85,976 and 49,900,000** units:
the already admitted source bytes and positive input charge supply the lower
bound, and the 50,000,000 budget with a 100,000 terminal reserve supplies the
upper bound before a nonterminal charge is admitted. This is not a reconstructed
invoice, a physical resource bound or a broker/certificate exchange rate.

The unknown accounting cannot change already sealed forecasts, true labels,
actions, request-ID coverage sets or exact bound validity. Consequently the
negative coverage findings and the positive finite forecast/action effects
retain their stated evidence. A global positive economic flag made false only
by unknown accounting, however, means that the end-to-end claim is
unestablished; that flag alone is not evidence that a method costs more.
Here the measured adverse comparisons have their own signed invoices and
coverage witnesses, as reported above.

For illustration of the accounting distinction, if two same-tariff completed
totals C and O were both assigned an identical additional nonnegative charge u,
their difference would stay C−O. The 5% saving condition would instead become
`u <= 19O-20C`. A common overhead cannot create a 5% saving that already failed,
and can remove one that previously passed. Unequal unmeasured allocations do
not have that invariance. The actual lost work has no declared common
allocation or cross-tariff conversion, so this conditional algebra never
repairs the frozen global gate or substitutes for its unavailable invoice.

Evidence: [source-only cost bounds and invariance review](../work_logs/P3_10_2026-10-11_S1/reviews/certificate_reconstruction/cost_uncertainty_source_review_v1/review.md),
[preserved original failure](final_v1/stages/public/attempts/attempt_01/failure.json), and
[complete amended analysis with original outer-attempt audit](final_v1_amended_A1/stages/analysis/units/all-frozen-endpoints/attempt_01/result.json).

## 9. Answers to the five questions at the P3-10 boundary

### Q1. How does this system handle logical uncertainty?

It implements a finite, source-bound information process: six public advice
coordinates produce a before-purchase forecast, owned paid computations return
sound receipts, current matching hard evidence can change future forecasts and
actions, and earlier issuance records remain immutable. The 336 broker
episodes give exact evidence for that bounded service and for some improved
anticipation on the mixed and cheap-null families. The gate-transfer failure
shows that these gains do not extend uniformly even across the frozen families.
The advice-collision and moment analyses explain this particular limitation
without claiming that mathematical truth is probabilistic or unknowable.

The learned point forecasts are not a coherent joint law over all represented
claims. The separate current-bound receiver has not been composed with the
learner, and finite successful hardening supplies neither general eventual
correctness nor Logical Induction. The accepted integration remains the finite
owned CNF broker under its existing information and timing premises.

### Q2. What logical counterfactual and counterpossible semantics are supplied?

The inherited finite semantics distinguishes conditioning, occurrence and actor
changes, shared-code replacement, stored copies, predictors and exceptional
repair. Complete tied minima and unresolved source alternatives remain in the
declared quantifiers. A fixed deterministic minimax consumer gives an
implementable reply; an action chosen after observing the hidden retained state
would be a different, inadmissible oracle. The current-bound histories add
checked nonempty incumbent sublevels, including the nonoptimal cutoff and
changed loss scope.

The known contradictory antecedent is still classically infeasible under
conditioning. Its paired-support evaluation depends on an explicit exceptional
policy, whose replay does not justify that policy generally. The final
conformance is amended inherited regression, not unseen counterpossible
transfer, identified causal structure or a theory of topic-preserving exception
choice. That subsystem also remains separate from selective feedback.

### Q3. Does retaining useful models beat a strong ordinary combination?

This experiment supports constructive service equivalence and consequential
finite limitations. The identity mirror reconstructs the same kernel; distinct
ordinary broker witnesses beat all four numerical candidates on both realized
terminal loss and cost per request within each family. Direct ordinary checking
delivers the same full current-bound service at lower complete cost, and covers
more actual capped request IDs. The inherited ordinary structural implementation
matches all nine outputs at lower declared charges.

These results leave **affirmative advantage over the strongest ordinary
combination OPEN**. They do not establish that useful model plurality is
impossible. In particular, the complementary transported warrants here are
sound conditional facts, not learned fallible empirical models. The evidence
retains P3-N01's accepted **modest formal-adaptation and implementation-synthesis
support**; it does not add an exclusive general algorithmic advantage or make
an author contribution decision. The ordinary terminal-objective witnesses
also have worse issued Brier scores than the candidates, so the particular
dominance statement is not silently extended to every predictive objective.

### Q4. Do usefulness estimates improve, and in what sense is this like learning?

There are genuine finite improvements against named before-resolution advice
and hardening baselines: three of six distinct A2 cells and four of six paired
hardening action cells meet their declared practical conventions. Known
asymmetric stakes produce different readout effects, and the full frozen
transfer suffix is adverse. Learning score, action gain and priced usefulness
are distinct outcomes. Caching costs more on all selected-receipt pairs, and
the strongest ordinary economic comparison remains unfavorable on the recorded
terminal objective.

The exact original-expert reductions retain their existing feedback, weighting,
propensity and randomness assumptions. This fixed cohort supplies no new
calibration, adaptive-policy regret, non-exploitation or Logical Induction
guarantee. Paid fixed-end reports deliver useful typed intervals, but mostly
null practical narrowing, while the later geometry and fitted decompositions
are external interpretation rather than deployed learning or reporting wins.

### Q5. When can values contain probability information?

Under the admitted exact expected-loss map, recovery depends on the source
simplex, loss-row span, shared scale/offset and requested target. The 36 exact
conformance certificates exhibit full-law recovery, partial target recovery,
collisions and minimum query repairs; the six rejection controls enforce the
declared interface. Constant targets and one-state laws keep their trivial
status, and hypothetical repair queries are not counted as acquired evidence.

The theorem's premises are essential. Realized scores are not expectations;
unshared stakes do not become shared nuisance calibration; a minimax decision
or positive uniform bound is not a probability observation. The tied fixture
gives an explicit robust value vector outside all four expected-loss
calibration conventions. This precisely qualified information result remains
the most mature answer to Q5, with no claim that arbitrary external reports
meet its hypotheses merely because a schema accepts their numbers.

### 9.1 All 21 duties retain their accepted statuses and residual obligations

The [additive duty interpretation](../work_logs/P3_10_2026-10-11_S1/duty_evidence_attachment.md)
and [complete machine attachment](../work_logs/P3_10_2026-10-11_S1/duty_evidence_attachment.json)
map every U01–U09, V01–V04, M01, R01, C01–C04, I01 and F01 duty to this evidence.
All 21 full accepted records, status strings and residual obligations are
retained verbatim, with independent broker and conformance attachments.
No accepted checkpoint is overwritten or silently strengthened. P3-A/B retain
their restricted PASS; P3-C/D are unattempted. Option C and R-P3-N01 remain
unselected. P3-11 is unstarted and no author decision gate is attempted here.
