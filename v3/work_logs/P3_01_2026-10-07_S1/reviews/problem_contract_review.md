# P3-01 problem-contract adversarial review

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Date: 2026-10-07 UTC. Nonblind internal review; not an external validation.
Resource time is unmeasured and adds no independent time credit. Scope: the
working versions of `v3/foundations/01_problem_contract.md` and
`v3/foundations/01_desiderata.md`; no canonical edits made.

## 1. Assessment

The draft accurately distinguishes the inherited loss calculus from a future
logical-uncertainty learner. It preserves the already-true scope of the old
proof-search example, acknowledges inherited report-dependent behavior, and
correctly avoids deriving paraconsistency from rejection of an empty deployment
source. Its ordinary comparator is strong and appropriately permits probability,
joint dependence, metareasoning, model coexistence and dependency-aware reuse.

The main remaining issues concern the exact time at which a forecast is saved,
the soundness conditions behind a checked truth coordinate, and the positive
evidence target for the author's third question. These are local contract
clarifications; no redesign or new research task is required.

## 2. Actionable findings

### R1 — distinguish a forecast before paid resolution from the later decision report

**Where:** problem contract §5.2 steps 2–4; desiderata U06.

Step 2 permits paid computations that return a checked answer. Step 3 then
saves the forecast before a later evaluator label is revealed. Consequently,
one possible execution saves its only forecast after it has already bought
the true answer. That is a legitimate resource-priced decision policy, but it
cannot supply anticipatory prediction evidence under U06.

**Suggested repair:** save a forecast before starting the round's paid
computations, then save the final action report separately, or explicitly
timestamp every forecast against the first accepted resolution. Distinguish
pre-resolution predictive scoring from total task loss including paid
resolution. Reports made after resolution may be exactly correct and useful;
they must not be counted as advance prediction of an unresolved claim.

This also clarifies that repeated labels and reissued queries are not genuinely
unresolved merely because a new episode's evaluator has not yet revealed them.
Earlier legitimately observed knowledge is permitted, with its status retained.

### R2 — make the soundness condition local to “checked truth” and forced updates

**Where:** problem contract §§3.1–3.2; desiderata U02–U04.

The prose correctly separates truth in an interpretation, theory-provability
and received proofs, and says soundness is an explicit premise. The matrix
then uses “checked truth” and requires an accepted Boolean answer to fix the
truth coordinate, without repeating the relevant condition. An accepted proof
in an unsound theory need not settle interpreted truth; coexistence of tagged
alternative theories is explicitly allowed elsewhere in the contract.

**Suggested repair:** distinguish a received proof/refutation under a named
theory from an answer accepted as sound for the current interpretation. U04's
coordinate fixing should require that bridge (or a correctly checked bounded
execution trace). Contradictory accepted material should receive an explicit
conflict/stale-scope status rather than silently installing both hard truth
constraints or using an empty source to justify an action.

The intended distinction is already present in the prose, so this is a
consistency repair rather than a demand for a new checker theorem.

### R3 — ordinary probabilistic conditioning needs positive probability

**Where:** problem contract §7, evidence-conditioning row.

A “nonempty conditional event” is insufficient for ordinary probabilistic
conditioning. A nonempty event may have probability zero. Set-based restriction
and probabilistic conditioning have different admissibility conditions.

**Suggested repair:** say that set-based restriction retains a nonempty
admitted set; ordinary finite probabilistic conditioning requires a
positive-probability event; zero-probability cases require an explicit
alternative update/selection rule. This matters particularly for a logical
antecedent currently assigned probability zero.

### R4 — require Q3's positive evidence to reach a logical-uncertainty task

**Where:** problem contract §9 Q3; desiderata M01.

Q3's current target is scoped model selection under task loss and compute
limits. That is useful and tests fallible model coexistence, but a successful
scientific approximation example alone would not answer whether nonfinal
model use improves logical or mathematical uncertainty. The author specifically
asked about that connection.

**Suggested repair:** make the positive target explicit: show how scoped
coexistence of mathematical approximations, proof heuristics or conditional
theories improves a declared prediction/decision service on unresolved logical
queries, compared with the same ordinary model library and evidence. The
fallible-approximation example is a conceptual separation; it does not by
itself count as that improvement. Equivalence remains an acceptable result.

### R5 — ensure rechecking obligations permit budget-limited stale status

**Where:** desiderata R01 versus U04 and problem contract §6.2.

R01 says to recheck every dependent warrant or transport it with a proved
correction. In a bounded implementation this must not require immediate
unlimited recomputation merely to maintain a usable state.

**Suggested repair:** allow the method to invalidate or mark a dependent warrant
stale until it can pay for rechecking. It may then abstain or use an independently
valid fallback. U04 already supplies the appropriate pattern.

### R6 — distinguish completion of the proposition's horizon from investigator timeout

**Where:** problem contract §3.1.

The separation between the proposition's execution bound `b` and the reasoner's
budget `B_t` is correct. One small addition would prevent the inverse mistake:
completing all `b` stipulated VM steps without the claimed termination is a
negative answer to that *bounded* proposition, whereas an investigator stopping
before resolving the `b`-step condition is unresolved. A halt with the wrong
output also refutes the specified output claim.

**Suggested repair:** add these explicit outcomes and require any negative
receipt to identify which bounded condition was checked. This does not supply
an answer about unbounded halting.

### R7 — clarify certificate checking for a computably enumerable axiom specification

**Where:** problem contract §3.1.

A computably enumerable axiom set need not have a decidable membership test.
The stipulated “concrete proof checker” is a sufficient parameter only if its
admission rules make finite checking operational.

**Suggested repair:** specify a decidable axiom schema or require a finite
enumeration/admission witness for each cited axiom, with its checking cost
charged. Alternatively, explicitly allow axiom checking to time out and accept
only fully checked receipts. Do not implicitly grant instantaneous axiom
membership from the phrase “computably enumerable.”

### R8 — minor editorial and completion checks

- The last sentence of the desiderata file currently contains
  `refuted,+narrowed`; remove the accidental plus sign.
- During this review, the linked `01_separating_examples.md` and
  `01_source_contracts.md` were not yet present. This is consistent with the
  working status; verify those links, EX identifiers and source locators before
  completion. Their mathematics and source imports were not independently
  checked in this review.
- Duty S01 and source S01 are disambiguated by the explanatory paragraph. The
  explicit `duty:`/`source:` prefixes should be used in machine-readable records
  as promised, to avoid an accidental provenance collision.

## 3. Five-question coverage

| Author question | Operational target present? | Improvement/equivalence/failure criteria | Assessment |
|---|---|---|---|
| Q1 logical uncertainty | Yes: bounded information, true/false/unresolved outcomes and paid updates. | Restricted guarantee or matched advantage; preserved translation; counterexample to update or guarantee. | Adequate after R1/R2/R6 clarify timing and truth statuses. |
| Q2 logical counterfactuals | Yes: distinct conditioning, intervention, replacement, repair and genuine-counterpossible service. | Nonvacuous declared semantics/transport; ordinary reconstruction; twins/ties refute unsupported uniqueness. | Adequate after R3; the task need not manufacture a positive answer for every impossible antecedent. |
| Q3 fallible models and logical uncertainty | Partly: scoped model selection is explicit, but the logical-uncertainty connection is not yet required in the positive target. | Equal-information comparison is strong; ordinary reproduction and disappearance of an advantage are explicit. | Apply R4 so a generic approximation example cannot be mistaken for the requested logical improvement. |
| Q4 usefulness refinement comparable to LI duties | Yes: the matrix separates finite coherence, convergence, anticipation, calibration, regret, delayed feedback and computation value. | Each claimed duty needs its own proof or valid finite evidence; expectation recoding or an adverse process narrows the claim. | Adequate as a prospective menu; no unrestricted property is falsely imported. R1 matters for anticipatory evidence. |
| Q5 probability information in costs | Yes: known payoff, recovery objective and indistinguishable-input obstruction. | Scoped characterization/retention consequence; decoder equivalence; collision proves insufficiency. | Adequate at P3-01 scope; full characterization remains P3-02. |

## 4. Comparator fairness and overclaim checks that pass

- O-COMB may use the same algorithm and obtain the same outputs; the draft does
  not require a contrived numerical advantage.
- The ordinary baseline receives joint information and provenance, avoiding
  a comparison only against independent marginals or uncached arithmetic.
- Visible shortcuts are permitted for both methods, directly addressing the
  phase-two proof-procedure example's strongest ordinary control.
- Full feedback, passive delay, selected-action feedback and paid proof discovery
  are separate; a finite-expert regret statement is not called Logical Induction.
- Unresolved-label coverage and selection bias are explicitly recorded.
- The finite assignment baseline does not require every assignment to extend to
  a full model of the theory. Its soundness claim is conditional on the checked
  constraints being sound, and enumeration is charged.
- The inherited finite feedback example is retained, while the matrix does not
  infer correct self-report from an ordinary proper score under changed outcomes.
- P3-N01 remains NOT YET SUPPORTED, and no gate or downstream task is completed
  by the document.

## 5. Recommendation

Keep the current contract and incorporate the local corrections above. The
architecture and comparison scope are appropriate for P3-01. The most valuable
change is to make prediction-before-resolution and decision-after-paid-reasoning
two explicit evaluation records; that distinction will prevent a subtle but
material success inflation in the eventual challenge.
