# External Audit VI: Value Logic Repository (Checkpoint E)

Auditor: Claude Opus 5 (Anthropic)
Date: 2026-07-24
Commit audited: `b2869c3` ("Task 31A: audit reader narrative")
Scope: Task 22B and Tasks 26–31A — the entire drafting phase and both internal
publication audits — plus the standing checkpoint charge: alignment with author
goals, trajectory toward the two consumable artifacts, respect for author
guidance, non-fracture of the work, task difficulty versus prediction, and
course corrections to the pending roadmap. This audit is input to Checkpoint E.
Predecessors: [`claude_audit_2026-07-11.md`](claude_audit_2026-07-11.md),
[`claude_audit_2026-07-12.md`](claude_audit_2026-07-12.md),
[`claude_audit_2026-07-14.md`](claude_audit_2026-07-14.md),
[`claude_audit_2026-07-17.md`](claude_audit_2026-07-17.md),
[`claude_audit_2026-07-21.md`](claude_audit_2026-07-21.md).
Item numbering **continues** the series: C26+, S17+, L12+.
Producer of audited work: GPT 5.6 Sol, under project-author direction.
Requested by: Tristan Miano, for placement in `llm_convos/`, as part of the
Checkpoint E protocol.

---

## 1. Scope and method

Two calendar days and seven commits since Audit V. This is the largest single
content window in the project's history: the pre-draft bridge theorem, then the
complete drafting of `paper.md` from an empty file to 19,501 words across
eleven sections and six appendices, then the mathematical/citation audit and the
reader/narrative audit. I did the following.

1. **Ran the verification suite on a fresh Linux clone, with the native kernel.**
   Unlike Audits IV and V, I installed CMake, NumPy, Matplotlib, and PyTorch, so
   this is the first external audit in the series with **zero skipped checks**:
   **177/177 pass**, including the two `NativeKernelTests` that previous audit
   environments skipped. The C++ kernel built and its differential tests against
   the NumPy reference passed.
2. **Reproduced off-pin.** My environment resolved `torch 2.13.0+cu130`, not the
   pinned `2.8.0`, and CMake 4.4.0 on glibc 2.39. Everything still passes. This
   was unintended but is worth recording: the frozen evidence path is not
   brittle to its exact pinned runtime.
3. **Ran the full preflight.** `python -m experiments.run_repaired_experiment
   --preflight` completes end-to-end, verifying frozen hashes, native/Python
   decoder equivalence, the final-data guard, and the deterministic system
   witness.
4. **Independently recomputed the registered hash chain from a clean checkout.**
   `protocol_v1.json` → `3467f5e2…`, `fit_checkpoint_v1_1.json` → `1298e87f…`,
   `calibration_checkpoint_v1_1.json` → `48663fa8…`,
   `selection_checkpoint_v1_1.json` → `84e7456a…`, and the
   `analysis_v1_1.json` self-hash → `dbb17686…`. All five match the registered
   values. The fifth registered digest, `raw_result_sha256`, has no repository
   file by design (gitignored run product). **C20 is fully repaired**: the
   `.gitattributes` CRLF preservation works from a clean Linux clone.
5. **Checked public CI directly through the GitHub REST API.** Green at HEAD
   `b2869c3` and green for the last **ten consecutive runs**, back through
   Checkpoint D. **C23 is fully closed.**
6. **Recomputed every headline empirical value from `analysis_v1_1.json`** —
   `F35a/b/c` point estimates, deltas, percentile intervals, Holm one-sided
   bounds, raw and adjusted p-values, and both `F36` schemas. All match the
   paper and the Task 31 audit exactly.
7. **Re-derived the load-bearing mathematics rather than reading the audit's
   summary of it.** Theorem 11's conservative-decoding soundness and its
   `2ρ_err` completeness band; Proposition 13's `2ρ` argmax bound, its
   tie/flip tightness, and the generic `4ρ` non-abstention condition; and the
   proper-score identity `L_N − L_q = I(R;Y|N) − E·KL`, hence `I ≥ δ`. All
   correct as stated.
8. **Verified the He–Li–Xu–Zheng citation against primary sources** and
   confirmed the `⌈log₂(d+1)⌉` hidden-layer convention is consistent with both
   He et al. 2020 and Arora et al. 2018.
9. **Parsed `paper.md` mechanically** for Markdown/math publication hazards:
   all 1,699 inline `$` delimiters outside display and code blocks, table-cell
   math, display-block placement, and figure path resolution.
10. **Read the paper end to end as a reader**, plus both internal audits, the
    claim ledger, the TODO diff, and Checkpoint D's decision record.

---

## 2. Overall assessment

The drafting phase is a success, and by a wider margin than I expected going in.
`paper.md` is a real paper. It opens on a human question, answers it before it
introduces machinery, carries one synthetic succession through eleven sections,
gives every headline result a significance paragraph, and reports a partly
negative empirical result without either burying it or performing contrition
about it. The four formal clusters survive. The claim ledger has 108 adjudicated
rows — 71 `S1`, 17 `X1`, 14 `O1`, 6 `I1` — and no live `U0/C0/L0/R0/T0` cells.
The work is not fractured: Tasks 26–30 each own a section, and the sections
compose into one argument rather than an inventory of repository artifacts.

Checkpoint D's correction of my Audit V stands and I reaffirm the concession.
My claim that the bridge theorem was the existing conservative-decoding theorem
under renaming did skip the second certification error step; the `2ρ`/`4ρ`
separation as implemented in Task 22B is correct and my compression of it was
not. The adjudication contract has now fired in both directions twice. That
remains the healthiest process signal this repository produces.

My findings this round are of three kinds, and none of them is a mathematical
error in a theorem.

**One is a rendering defect that would ship into the Gist** (C26). It is the
sole unbalanced math span in the document and it sits inside an Appendix B proof
paragraph.

**Two are missing denominators in the empirical narrative** (C27, C28). The
paper reports its abstention and fidelity figures without the reference base
rates that make them interpretable — and the needed reference values are already
frozen in `protocol_v1.json` and `analysis_v1_1.json`. Supplying them makes the
paper's own finding sharper, not weaker, and forecloses a reviewer computing
them independently and asking why they were omitted.

**Two are narrative gaps against the project's own lead question** (S17, S18).
The motivating question has two halves. The paper answers the first half well
and does not answer the second half at all; and the paper is titled after a term
it never defines. Both are cheap, and both make the artifact more consumable
rather than more hedged.

No finding requires returning to proof, experiment, or interpretation work.

---

## 3. Corrections

### C26 — One malformed formula survived the mathematical audit (blocks Task 32)

`paper.md` line 1912 reads:

```text
The $.06+$.06$ separator is a complete countermodel to unconditional
```

It should read `$.06+.06$`. I parsed every inline `$` delimiter in the document
outside display-math and fenced-code regions: 1,699 of them, and this is the
**only parity break**. Ten further lines carry an odd `$` count, but they pair
into five intentional line-wrapped spans (see S20); line 1912 is unpaired.

On GitHub this renders `$.06+$` as math, then `.06` as literal text, then leaves
an open delimiter that the next `$` on line 1913 closes — turning most of a proof
paragraph in Appendix B into a spurious math span. Task 31's completion note
records that it "corrected three malformed formulas"; this is a fourth, and it is
the one that damages a whole paragraph rather than a single symbol.

### C27 — Fallback mass is reported without its denominator

Section 7.3 reports target-weighted fallback mass `.9962` (structured) and
`.9139` (cross-entropy). Neither the main text nor Appendix E states the
**reference** fallback mass. That value is a registered design constant, not new
analysis:

```text
experiments/protocol_v1.json → /sampling/outcome_target_mass/Granted = 0.35
```

I confirmed `request_target_weight` in `experiments/implementation.py` is the
joint outcome/context target-to-design ratio, so the target-weighted metrics are
computed under exactly that declared target distribution. Therefore the
reference target-weighted fallback mass is **`.65`**, and:

| arm | licensed target mass | share of the available `.35` |
|---|---:|---:|
| reference | `.3500` | — |
| structured | `.0038` | **≈ 1.1%** |
| direct cross-entropy | `.0861` | **≈ 24.6%** |

Without `.65` on the page, `.9962` cannot be read. A reader cannot distinguish
"this pipeline is pathologically cautious" from "this generator rarely grants
anything in the first place." One sentence supplies the denominator, and it
strengthens the paper's thesis: the structured arm captured roughly one part in
ninety of the licensing that was actually available.

### C28 — The frozen trace already contains the most decision-relevant number, and the paper omits it

`analysis_v1_1.json → trace_secondary_summaries` contains:

```text
request.structured.unweighted_accuracy.outcome_granted = .0124
request.ce.unweighted_accuracy.outcome_granted         = .1811
```

Conditional on a grant being the correct outcome, the structured arm grants
1.2% of the time; cross-entropy grants 18.1%. I verified these reconstruct the
paper's own headline four-outcome fidelity almost exactly, using the registered
target masses and the per-outcome conditional accuracies:

```text
structured: .05(1.0) + .30(.6944) + .30(.7872) + .35(.0124) = .4987   [paper: .4976]
CE:         .05(1.0) + .30(.8430) + .30(.7247) + .35(.1811) = .5837   [paper: .5866]
```

Two consequences follow, and both belong in §7.3.

First, the `.4976` figure is earned almost entirely on **Withheld and Refused**.
The Granted column contributes about 0.4 points out of a possible 35. The
paper's prose ("withholding many correct ones") is directionally right but
understates by roughly an order of magnitude what the frozen numbers show.

Second, this yields a baseline the paper currently lacks. A trivial predictor —
"Undefined if ill-formed, else Withheld" — scores `.05 + .30 = .35`
target-weighted, because well-formedness is exact and external in both arms.
Structured's margin over trivial is `.148`; cross-entropy's is `.237`. Reporting
four-outcome fidelity without that reference point invites a reviewer to compute
it and wonder why it was not stated.

None of C27 or C28 requires a rerun, a regrade, an outcome-selected analysis, or
a new disposition. Every number is already frozen and registered.

---

## 4. Structural findings

### S17 — The lead question's second half is never answered affirmatively

This is the most important finding in the audit.

The project's motivating question, carried in `TODO.md` and in every prior
checkpoint charge, is:

> Why did we choose this "value logic" design, **and why are we hoping this
> serves as a nice fit for neural networks?**

The paper answers the first half, and answers it well: §1 and §2 are the best
prose the project has produced. It does not answer the second half.

The word "hope" does not appear in `paper.md`. Nor does any equivalent
affirmative construction — I searched for "natural fit," "good fit,"
"attractive," "appealing," "suggestive," and "why ReLU," and found nothing but
one database-analogy reference in §4.3 and one warning about "attractive traces"
in Appendix F. What §6 answers is a different and more defensive question: *what
must a learned implementation preserve, and can ReLU do it?* Theorem 12 is a
sufficiency result. It is not a reason for expecting a good fit, and a reader
reaches it without ever learning why anyone thought ReLU was special for *this*
logic rather than for function approximation generally.

The material for the affirmative answer exists across the repository —
`notes/atlas_questions.md`, `notes/representation_layers.md`, the founding
transcripts, `llm_convos/claude.txt` — and has never been assembled. There were
four distinguishable hopes, and their honest current dispositions are:

| original hope | disposition after the drafted paper |
|---|---|
| `ReLU(ε − u)` is not an analogy for a license margin — it is the same operation | **Survives, delimited.** §6.3's five-way zero collision (supported equality, crossing, refuted, missing, invalid) is a precise correction, not a refutation. The margin is real; rectification alone cannot carry the logic |
| the intrinsic activation atlas aligns with the scientific-model atlas | **Not established, and not tested.** §2.3 states no correspondence is assumed; the frozen experiment did not probe activation alignment at all |
| depth corresponds to nested licensing | **Not addressed anywhere in the paper** |
| a reusable numerical statistic transfers under a changed threshold without retraining | **Supported.** `F35a`, `+.1866`, `[.1860,.1873]`, sign shared by all eight fits |

That table *is* the answer to the lead question, and it is a more interesting
answer than a compatibility theorem: two hopes survive in modified form, one is
open, one was quietly dropped. It costs roughly 300 words as a §6.0 lead-in or as
an addition to §10.1. It converts §6 from "here is a compatibility result" into
"here is what we expected, and here is what happened," which is the register the
author has asked for since Checkpoint C.

It also hands Task 33 its spine. "Here is what we hoped rectified linear units
would give us, and here is what they actually gave us" is a far better Substack
essay than the current planned order, which leads with the empirical trade-off.

### S18 — The title term is never defined

"Value logic" occurs five times in `paper.md`: once in the title, once in a
passing sentence in §9.1, and twice inside protocol version strings quoted in
Appendix E. Section 3 introduces the calculus as `𝔯 = (s,e,q,P)` and never names
it. The abstract makes the connection in a single clause — "Their continued use
exhibits pragmatic value… We formalize such value as a… license" — and the
connection is never made again, and never made to the formal object.

For a paper whose title is the term, a reader should not finish it unable to say
why "value" is in the name. Two options:

- **(a)** one sentence in §3.1 naming the calculus and grounding the name in the
  §1 definition of pragmatic value as task-relative reliance worth; or
- **(b)** retitle to match what the paper actually defends.

I lean strongly toward (a). The connection is genuine and §1 already makes it —
it simply never lands on the formal object, so the title reads as inherited
project vocabulary rather than as a claim the paper defends.

### S19 — §1 overattributes abstention to the conservative wrapper

The introduction reports `.9962` without `.9139`, and its mnemonic reads:

> *wrapping that statistic in a conservative uncertainty-and-decoding pipeline
> often turned informative predictions into abstentions*

But the cross-entropy arm has no conservative interval machinery at all and
still forfeits roughly 75% of the available grants (C27). The conservative
wrapper accounts for the increment from `.914` to `.996` — large in relative
terms, and the paper is entitled to say so — but not for the bulk of the
abstention. §7.3 places the CE column adjacent and is fine. §1 does not, and §1
is what most readers will retain. One clause fixes it: both arms abstained
heavily; the conservative pipeline made it near-total.

### S20 — Multi-line inline math is a Gist risk (Task 32)

Five inline `$…$` spans wrap across a line break: lines 601/602, 2112/2113,
2178/2179, 2295/2296, and 2885/2886. These are intentional wraps, not defects,
but GitHub's inline-math handling across a soft break is inconsistent and
version-dependent. Task 32 should **render-test on an actual Gist** rather than
reason about it.

Two things I checked and found clean, so Task 32 need not spend time on them:
there are **no** pipe characters inside math spans in table cells (an initial
regex pass produced 35 false positives; a proper span-parse yields zero), every
`$$` display block sits on its own line, and both referenced figure paths
resolve.

---

## 5. Literature

### L12 — Prefer the DOI over the CAS journal host

`paper.md` §9.4 links He et al. 2020 to
`https://computmath.cjoe.ac.cn/jcm/EN/10.4208/jcm.1901-m2018-0160`.
`references.bib` already carries the DOI `10.4208/jcm.1901-m2018-0160`. For a
publicly published artifact the DOI is the durable destination; the `cjoe.ac.cn`
mirror is the more fragile one, and its English-language path is not the
canonical landing page.

The citation itself is correct. I verified authorship (He, Li, Xu, Zheng), venue
(*Journal of Computational Mathematics*), volume/issue/pages (38(3):502–527),
and year against multiple independent primary and secondary sources, and
confirmed that the paper's depth convention — total depth at most
`⌈log₂(d+1)⌉ + 1`, hence at most `⌈log₂(d+1)⌉` hidden layers — is consistent with
both He et al. and Arora et al. 2018, and that He et al.'s own lower-bound result
(at least two hidden layers for `d ≥ 2`) is not contradicted by the stated upper
bound at `d = 2, 3`.

---

## 6. Task difficulty versus prediction

**Drafting was dramatically faster than predicted, and this is the window's most
interesting process discovery.** Tasks 27 through 31A all landed on 2026-07-24
between 10:57 and 13:09 — six tasks, comprising the theorem spine and Appendices
A–C, the neural representation sections and Appendices D and F, the full
empirical narrative and Appendix E, and both internal publication audits — in
roughly two hours of commit wall-clock. Checkpoint D treated drafting as the
substantial remaining phase and allocated five tasks plus two audits to it. The
formal groundwork through Task 25 evidently did the real work; prose turned out
to be largely an allocation problem, not a construction problem.

**One risk follows directly from that speed.** Tasks 31 and 31A audited, within
the same working session, prose that Tasks 28–30 had written hours earlier.
Both are self-audits with no temporal or authorial distance. The findings in this
audit are exactly the class of miss that pattern produces: C26 is a malformed
formula that the mathematical audit reports having swept for and repaired three
instances of; C27 and C28 are frozen numbers that the reader audit reviewed
without noticing the absent denominators. This is not an indictment of the audit
protocol — the two internal audits are genuinely good, and the reader audit's
compression of 1,673 words while retaining all thirteen results and every
registered endpoint is a real achievement. It is an argument for continuing to
place an external checkpoint after the internal ones, which is what the roadmap
already does.

**Task 22B landed clean.** Checkpoint D's gate was correctly scoped, correctly
executed, and correctly propagated into §8 and Appendix F, including the
correction to my own Audit V compression.

**Word budget behaved.** 13,078 → 11,405 main-text words in one pass, 2.7% over
the planning target, with all thirteen public results and every registered
endpoint retained. That is a good outcome and I would not cut further; the
remaining excess in §§3 and 5 carries load-bearing definitions.

**Nothing was harder than predicted.** No task in this window recorded a failure,
a runtime stop, or a time-budget abort — a marked contrast with the Task 20/21
experiment window.

---

## 7. Recommended course corrections

### Insert Task 31B — Narrow publication repair, before Task 32

Every item draws on already-frozen artifacts or is purely expository. No rerun,
no regrade, no new disposition, no new literature.

1. Repair C26 (`$.06+.06$` at line 1912).
2. Add the reference target-weighted fallback mass `.65` from
   `outcome_target_mass`, and the derived share-of-available-licensing figures
   (C27).
3. Add the grant-recall values `.0124` / `.1811` and the trivial-baseline `.35`
   to §7.3 (C28).
4. Add the four-hopes subsection and its disposition table (S17).
5. Resolve the title/term gap in §3.1 (S18).
6. Add the cross-entropy fallback clause to §1 (S19).

### Task 32

Add an explicit Gist render test covering the five multi-line inline math spans
(S20). Re-verify the hash chain from a clean checkout — I have now confirmed this
path works, so it should be a confirmation rather than an investigation. Switch
the He et al. destination to its DOI (L12).

### Task 33

Build the Substack spine on the S17 four-hopes structure rather than the current
planned order. The essay's natural arc is: Newtonian retention → pragmatic value
→ the `0.35 − 0.05 = 0.30` calculation → what we hoped ReLU would give us → what
it actually gave us → the transfer-versus-coverage mnemonic. The `.9962` figure
should travel with both its `.9139` companion and its `.65` reference.

### Task 34

Unchanged, and correctly ordered.

---

## 8. Checkpoint E disposition

**Publication-ready, conditional on a single narrow repair task.**

The four formal clusters survive independent re-derivation. The empirical record
is frozen, honestly graded, hash-verified from a clean checkout, and — as this
audit incidentally established — reproducible off its pinned runtime. Public CI
is green at HEAD and has been for ten consecutive runs. The claim ledger has no
unadjudicated cells. The paper reads as one argument and answers a stated human
question in every section.

The gap that matters is not mathematical and not empirical. It is that a project
whose motivating question has two halves has drafted a paper answering one of
them, and has titled that paper after a term it never defines. Both are cheap to
fix, and fixing them makes the deliverable more consumable rather than more
hedged — which has been the standing direction since Checkpoint C.

I recommend Checkpoint E authorize Task 31B, then proceed to Task 32. I do not
recommend returning to proof, experiment, or interpretation work.

---

## 9. Erratum against my own prior audits

Audit V (`claude_audit_2026-07-21.md`) claimed that the proposed policy/value
action-gap result was "simply the existing conservative decoding theorem under
renaming, with the margin renamed as the action gap." Checkpoint D §6 rejected
this as skipping the second certification error step, and it was right. Raw
argmax stability requires a true gap above `2ρ`; a conservative decoder that must
also certify its estimated winner can require a true gap above `4ρ` under the
generic coordinate-to-gap bound. I reaffirm the concession here so the record is
not split across two documents.

This is the second occasion on which the project has corrected the external
auditor with verified work — the first being Checkpoint C1's arithmetic
correction of Audit IV's item C21. Both corrections were right.
