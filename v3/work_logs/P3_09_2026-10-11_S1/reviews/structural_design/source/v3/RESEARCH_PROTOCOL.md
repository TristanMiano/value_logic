# Phase-three research procedure

Effective October 6, 2026 UTC. Contributor: **ChatGPT (GPT-6 Astra Pro)**.
Applies to [TODO_v3.md](../TODO_v3.md), its selected repairs and gate attempts.

## 1. Inheritance and authority

Retain the general methods of the [phase-two protocol](../v2/RESEARCH_PROTOCOL.md):
observed clocks, durable derivation, primary-source comparison, explicit
experiments and failure records, reliable/exploratory lanes, recurrence,
contribution assessment, and accurate attribution. The present document states
the phase-three contract; phase-two task-specific exceptions are historical.

Do not import F-task floors, neural-experiment obligations, old gate decisions,
the POST-B-1 clock or its scope ladder as phase-three requirements. Its records
remain intact. Reusing a theorem requires its hypotheses; reusing an artifact
does not earn its historical time again. A new phase does not make all earlier
results stale, and a passed earlier phase does not prove its extensions.

The author fixes the five questions and a minimum of sixteen engaged research
hours. Local mathematical choices remain revisable. Routine task-internal
choices and targeted repairs do not need repeated permission. Significant
redirection gets a prospective written decision, forecast and updated pointer.
Retain the user's final say at contribution and phase-completion gates.

## 2. One selected work item, durable evidence

At entry inspect repository state, the active pointer, blockers, dependencies,
previous sessions and any attempt/exposure markers. Read the relevant sources,
not the entire archive every time. Use the [work-item template](templates/work_item.md).
Before substantive work specify question, expected artifact, evidence criteria,
protected floor, central/high D/L/E/O forecasts, expected waits, reliable and
exploratory gains, likely failure and first informative check.

One task may span sessions; a gate is a separate attempt. Do not consume the
next task automatically when a selected item ends. A user-authorized batch can
continue across items while respecting dependencies and recording boundaries.
This setup creates the plan; it does not execute a sixteen-hour batch.

**D:** definitions, proofs, worked cases, failed arguments and countermodels.
Save reconstructable intermediate reasoning and assumptions. **L:** primary
literature, exact sections/hypotheses, imported versus adapted claims and
comparison scope. Search snippets are leads; record inaccessible or insufficient
sources honestly. **E:** implementations, finite checks, experiments and their
analysis, with versions, commands, inputs, outcomes and actual failures.
**O:** planning administration, formatting, routine transfers and publication.
Classify work by what was done, not by the artifact's filename.

A computational probe can inform a derivation. State its question and budget,
charge the implementation/run analysis to E and the mathematical interpretation
to D, and count each segment once. Finite tests establish only the enumerated
claim. Prefer a separate reconstruction reviewer for load-bearing results;
label self-review when no distinct reconstruction occurred.

## 3. Clocks, floors and resource reporting

Use `v3/time_ledger.csv` with the inherited columns:

```text
task_id,attempt_id,session_id,mode,lane,start_utc,end_utc,elapsed_seconds,engaged_seconds,tool_wait_seconds,idle_seconds,unmeasured_seconds,forecast_seconds,artifact,status
```

Record UTC and `time.monotonic_ns()` at segment boundaries, runtime identity,
mode/lane switches and at least every fifteen active minutes. Subtract matched
monotonic readings only on the same runtime. Pause for long unattended runs,
interruptions and inactivity. If an interval is unobserved, exclude it; do not
reconstruct a flattering duration from output size or token use. Preserve raw
observations, exact arithmetic and prior ledger bytes. Append corrections with
an explicit disposition rather than silently rewriting history.

Track both **research = D+L+E** and **total engaged = D+L+E+O**. The phase floor
is **research >= 960 minutes**. Waiting, idle, recovery and unknown intervals
count toward neither total. Setup is conservatively O and contributes zero
to the research floor. Keep phase two's final ledger and balance unchanged;
the distinct phase-three clock starts at zero research minutes by design.

Concurrent agents may provide independent work and separate resource records.
Their overlapping time is not added to the principal's engaged interval. Work
done while the principal is absent does not manufacture principal-clock credit.
Report measured resource cost when available; mark unmeasured costs unknown.

Research tasks use prospectively chosen 60/90-minute floors. The roadmap's mode
split is a forecast, not a retrospective quota. A task needs both its floor and
evidence. If a useful core result arrives early, use the remainder for meaningful
assumption checks, stronger constructions, comparisons or failure witnesses.
Do not pad, wait or repeat solved work to meet time. Carry unfinished work/floors
forward; only a prospective author amendment can reduce an accepted minimum.

Review research totals at 4/8/16-hour chunk boundaries and report overshoot,
new scope, stronger evidence, forecast error and the next useful chunk. Sixteen
hours is a floor, not an automatic finish. Additional time may be warranted by
remaining criteria or promising ambitions; choose it explicitly at a boundary.

## 4. Lanes, comparisons and contribution

Nominal traversal D/L/E allocation is 570/150/240 minutes, near the inherited
60/15/25 guideline; this is a planning distribution. Start R/X at 60/40 and
preserve at least 25% each over two consecutive cycles unless a documented
repair emergency intervenes. Assign lanes prospectively to substantive work,
not to desired result labels. Reserve about 25% additional research for
recurrence in the forecast; unused reserve need not be consumed.

The reliable route delivers precise interfaces, reconstructions and tested
restricted cases. The exploratory route tests stronger uncertainty/refinement,
counterfactual transport and information requirements. An unsuccessful
exploration can narrow a question without proving its opposite.

Carry forward the author's broad contribution criterion: a modest synthesis,
formal adaptation, application or useful combination can qualify. Record
object, type, exact delta, magnitude, evidence and named comparison scope in
[claim_ledger.md](claim_ledger.md). Assess technical task completion separately
from **SUPPORTED / NOT YET SUPPORTED / DISPLACED** contribution status.

Compare with the strongest credible ordinary combination, including probability,
decision theory and bounded computation. Shared algorithms and equal outputs
are permitted and informative. Neither superiority on every benchmark nor
worldwide priority is mandatory. A superficial relabelling, unsourced novelty
claim, elapsed floor or negative result alone cannot satisfy contribution support.

If support is missing at the relevant advancement gate, open a named 60/90-minute
evidence/recurrence chunk with an exact target. P3-N01 is the continuing initial
obligation; R-P3-N01 names its recurrence when selected. After two failed chunks,
compare at least two alternatives before proceeding. Never reset accumulated
effort or declare a blocked phase complete by changing its description.

## 5. Experimental and exposure contract

Until P3-09, all executable output is development. P3-09 chooses the concrete
environment and freezes dependency closure, methods, observations, task families,
prices, all controls, seeds, budgets, endpoints, thresholds and analysis.
No phase-two runtime or seed schedule is imposed on this new experiment.

Before execution inspect stage markers and verify the freeze. **Prepare,
durably save, hash and validate every tuned method and selected representation
before generating or revealing any final evaluation population**, including
transfer/secondary arms. Separate setup, development, preparation and evaluation.
Store versions and complete units so an interruption can resume without hiding
exposure. Freeze any alignment/search selection that a chosen method requires;
do not invent neural machinery solely to imitate F15's preparation layout.

Each frozen stage permits at most one unchanged retry for an unexplained
failure, with reason recorded and completed units preserved. Changing seeds,
methods, output paths or counts to obtain another attempt is not permitted.
A deterministic defect needs an explicit versioned amendment and disposition
of exposed data; preserve the old freeze and failed output. The final protocol
must define stage/unit boundaries, retry mechanics and conditions for loss of
confirmatory status when changes are made after exposure. Any amended run has
the label its data history warrants.

Save machine-readable results, commands, actual environment, hashes, resource
costs, failures, exposures and completion records. Include ordinary methods and
null/negative findings. Positive finite results do not establish an unrestricted
theorem; failure of support does not automatically establish falsification.

## 6. Gates and publication

P3-A and P3-B are technical readiness assessments under the selected work item;
record PASS/BLOCKED with evidence, hashes, timing, open objections and next
pointer. P3-C and P3-D require a reasoned evaluator recommendation followed by
the author's advancement/completion decision. Do all authorized review work
before presenting that decision. Preserve dated pre-decision snapshots; record
later acceptance separately. A new defect reopens the earliest affected
dependency and marks dependent claims stale without erasing past assessments.

At a task boundary synchronize TODO, claims, actuals, work log and affected
source/dependency records. Verification should resolve concrete remaining risks;
do not build an administrative test programme around minor prose edits. Keep
the root README polished and project-facing; operational status belongs here.

Sign new work with the actual contributor/model; preserve prior attribution.
Use the existing authorization to commit and publish this repository, verify
the resulting branch head, and report actual publication status. If transport
is unavailable, use the authorized ZIP/PowerShell handoff. Transport and
packaging do not satisfy research floors.
