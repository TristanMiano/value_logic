# Value Logic Phase Four: Recursive Value

**Status:** proposed plan, not started. Drafted by **Claude (Opus 5.5)** on
November 7, 2026, at Tristan Miano's request. The author's approval of
[the charter](v4/CHARTER.md) (M0) is required before any task begins.

Phase four is governed by [`v4/CHARTER.md`](v4/CHARTER.md) and its binding
companion [`v4/AIM_BALANCE.md`](v4/AIM_BALANCE.md). Read the charter's
**Drift** section before starting any task. Each task below names the charter
theses it serves; a task that serves none is out of scope unless the author
authorizes it as toolkit work.

For every task:

1. Begin by recording the candidate readings of the thesis, the most
   defensible one chosen, and why ([AIM_BALANCE §2](v4/AIM_BALANCE.md#2-find-the-most-defensible-interpretation-then-defend-it)).
2. Seek the construction and the obstruction with equal seriousness. A
   counterexample is followed by a characterization attempt: what does imply
   the conclusion, and where does the claim hold?
3. End with the [end-of-task review](v4/AIM_BALANCE.md#6-end-of-task-review),
   recorded in the task record or PR, and a closing de-biasing paragraph.

## Organizing question

> Can value, applied to itself over time, recover factual structure? Within
> that same recursion, can truth, theory succession and ontology change each
> be expressed as a derived structure?

Phases one to three are a toolkit to draw on, not a foundation phase four
must extend. Useful carried-over pieces: the five-way license distinction
(adequacy, permission to rely, preference, selection, retention), the Boolean
fragment of the phase-two calculus, the finite-prefix and open-library
theorems, composition and routing results, and the habit of naming the
closest conventional comparison.

**Deprioritized:** extending V19 or N16, retention economics, full-cost
comparisons against conventional methods, and further random numerical
panels. These may be used when a workstream needs them.

## Running example

Choose one world and carry it through every workstream. Default proposal: a
**physics-task world**. Performers are models and agents, tasks are physics
problems across regimes (Newtonian, relativistic, with and without drag), and
judges score predictions.

- W1 recovers the regime partition from judgments alone.
- W2 states what is limit-true in that world.
- W3 organizes the regimes as a sheaf of licenses.
- W4 has the agent judge its own judging.
- W5 trains a network on the same world.

If these connect in one example, that connection is the phase's main
contribution.

## Milestones

### M0 — Charter and example (author)

- [ ] **M0.1** Author rewrites or approves [`v4/CHARTER.md`](v4/CHARTER.md).
- [ ] **M0.2** Author confirms the running example or chooses another.
- [ ] **M0.3** Set up `v4/notebook/` (informal exploration) and `v4/results/`
      (stated, proved, checked results). Bulk outputs go to releases or LFS,
      not git history.

### M1 — Core feasibility (C1, C2, C4)

- [ ] **W1.1 Toy model of recursive judgment** (C1, C2). Performers i with
      skills θᵢ ∈ ℝᴷ; task instances t with latent type z(t) ∈ {1…K};
      performance yᵢₜ ~ f(θᵢ, z(t)); judges emit approvals aⱼᵢₜ, noisy in y with
      judge-specific reliability. Approvals are scored against *later*
      performances. Define J¹ (predictive validity of approvals), J² (judges
      weighted by how well their judgments predict later judgments and
      outcomes) and T (a partition or soft kernel over task instances).
- [ ] **W1.2 Identifiability (W1-T1)** (C1). Under separation of skill
      profiles, enough performers and better-than-chance judges, the
      J²-optimal partition equals the true type partition up to relabeling.
      Give rates in performers, judges and time steps. Check the closest
      literature first: Dawid–Skene, multidimensional IRT, co-clustering, peer
      prediction.
- [ ] **W1.3 When recursion adds information (W1-T3)** (C1, C5). Sharpen the
      phase-one J_m = J₀ countermodel into a necessary and sufficient
      condition. Conjecture: level m+1 adds conditional information exactly
      when it accesses outcomes later in time than level m's evidence.
- [ ] **W3.1 Toy sheaf of licenses** (C4). Domain space: (v/c, GM/rc²,
      ħ-relevance, drag). Licenses as a presheaf over open domains; bridge
      maps between carriers (special relativity to Newton as c → ∞; drag to
      no-drag). Check whether gluing failures carry real information or only
      notation.

**M1 checkpoint.** Start with the charter's alignment review.

- If W1 identifiability holds in the toy model, state the result as a positive
  conditional theorem, test its consequential perturbations (fewer judges,
  correlated judge errors, no temporal recurrence), and pursue the widest
  class it extends to. If it fails in every natural variant, state the
  repaired thesis the failure reveals and redirect C1 toward it. Do not
  narrow scope silently, and do not widen a claim beyond its proof.
- If gluing failures in the W3 sheaf carry real information, characterize
  what they detect and carry that into W3.2. If the sheaf adds nothing beyond
  notation, say so and redesign W3 before M2.

### M2 — Fixed points, limits and self-trust (C2, C3, C5)

- [ ] **W1.4 T = J² as a fixed point (W1-T2)** (C2). Alternate a T-step
      (repartition to maximize judge validity) and a J-step (reweight judges
      given the partition). Show the true structure is a stable fixed point;
      characterize spurious fixed points.
- [ ] **W1.5 Excellence centroids (W1-T4)** (C1). Heterogeneous "best X"
      selections as argmaxes of different weightings over latent quality
      dimensions concentrate on extreme points of the attainable quality set.
      Broad good judges cover the frontier; correlated excellences appear as
      low-rank frontier structure.
- [ ] **W2.1 Limit truth** (C3). In the phase-one stage semantics, φ is
      limit-true iff every eventually-undominated theory agrees on φ. Give
      conditions for consistency and closure under consequence.
- [ ] **W2.2 Classical fragment** (C3). Generalize the phase-two Boolean
      fragment: limit truth is classical where the eventual frontier agrees.
- [ ] **W2.3 The Newton case** (C3, C4). Show "Newton holds on regime R"
      survives in the limit while unrestricted Newton does not. Compare with
      Peirce, Kelly's limiting learnability and Logical Induction.
- [ ] **W4.1 Löb-type obstruction for self-licensing** (C5). Conjecture: a
      procedure that uniformly licenses "if I license φ, then φ is adequate"
      licenses everything or loses error control; self-trust is consistent
      only when stratified by a strictly smaller budget or domain. Include at
      least one genuinely cyclic case with stated fixed-point semantics.

**M2 checkpoint.** Alignment review first. Then the unification question: is
the W1 excellence frontier the same object as the W2 eventual frontier,
applied to theories instead of trees?

### M3 — Ontologies, drift and networks (C4, C5, C6, C7)

- [ ] **W3.2 Global sections** (C4). A final theory exists iff a global
      section exists; supersession is refinement of the cover. Explore
      whether an obstruction class appears when no global section exists.
- [ ] **W3.3 Ranking ontologies** (C4). Compare theories with different
      carriers by pulling licenses back along bridge maps.
- [ ] **W4.2 Value drift** (C5). Values over values, updated by counts:
      conditions under which recursive value updates converge rather than run
      away.
- [ ] **W5.1 Neural atlas experiment** (C6). Train ReLU networks on the
      running example. One preregistered primary metric: alignment between
      activation-pattern regions and true regime boundaries, against controls
      matched for size and depth. Secondary: does alignment require depth?
- [ ] **W5.2 Distributed value (optional)** (C7). Probe whether value-like
      structure reconstructed from a policy is distributed rather than
      localized, as the policy/value essay predicts. Connect to phase three's
      probability-information results on what behavior does and does not
      identify.
- [ ] **W1.6 Real data (optional)** (C1). Test W1 on one dataset of judged
      performances across task types, for example peer grading or chess
      ratings split by game phase.

### M4 — Integrated report

- [ ] **R.1** Essay-first report in the author's voice, built around the
      running example, with formal appendices. Each result opens with what it
      shows about a thesis, then its conditions.
- [ ] **R.2** Final alignment review against the charter: for each thesis,
      advanced, unchanged or refuted-with-repair.

## Approximate effort weights

| Workstream | Theses | Share |
|---|---|---|
| W1 Recursive judgment | C1, C2 | ~40% |
| W3 Sheaf of licenses and ontology change | C4 | ~20% |
| W2 Truth as limit of value | C3 | ~15% |
| W4 Reflection and self-licensing | C5 | ~15% |
| W5 Neural atlas | C6, C7 | ~10% |

These are guidance for allocation, not clocks. Track milestones, not minutes.

## Risks and opportunities

Each limiting risk is paired with the constructive possibility it sits
beside.

- **W1 and existing identifiability results.** Risk: W1 may reduce to known
  latent-variable identifiability. Opportunity: those results may supply most
  of the proof, leaving the reflexive fixed-point characterization (W1.4) as
  the new content; that is a good outcome, not a lesser one. Check
  Dawid–Skene and peer-prediction work at the start of W1.2, searching for
  enabling theorems as explicitly as for prior art.
- **W3's sheaf.** Risk: it may be decorative. Opportunity: gluing failures
  may give the first precise formal statement of "no final theory." The M1
  checkpoint tests both.
- **W4.** Risk: it is the most speculative workstream. Opportunity: a
  stratified self-trust result would connect C5 to C1 directly. Bound W4 to
  one theorem, an obstruction or a positive stratified self-licensing result,
  before extending it.
- **Drift and its reciprocal.** The charter's warning signs apply to this
  plan too: if the plan starts pulling away from the theses, amend the plan,
  not the charter. Equally, do not present a restricted success as broader
  than it is.
