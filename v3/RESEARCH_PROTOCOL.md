# Phase-three research procedure

Established October 6; amended October 11 and 12, 2026 UTC.
Contributor: **ChatGPT (GPT-6 Astra Pro)**.
Applies to [TODO_v3.md](../TODO_v3.md), its selected repairs and gate attempts.

**Current direction: discovery first.** The author's
[October 11 amendment](decisions/2026-10-11_discovery_first_amendment.md)
selects [P3-SEARCH-01](discovery/P3_SEARCH_01.md), a continuing generative search.
Its first research cycle continues beyond its satisfied four-hour floor; see
the current discovery checkpoint for exact actuals. P3-11 is deferred
until a promising candidate is ready for rigorous confirmation. Completed
scientific records retain their historical scopes and time accounting.

**Current execution cadence:** the author's [October 12 direction](decisions/2026-10-12_hourly_handoffs.md)
requests one-hour engaged-research sessions with durable handoffs between
ChatGPT and Codex. These explicit session boundaries take precedence over the
general instruction below to continue through every checkpoint. Cycle totals,
unfinished commitments and the open discovery objective carry across sessions.

## 1. Inheritance and authority

Retain the compatible general methods of the [phase-two protocol](../v2/RESEARCH_PROTOCOL.md):
observed clocks, durable derivation, primary-source comparison, explicit
experiments and failure records, reliable/exploratory lanes, recurrence,
contribution assessment, and accurate attribution. The present document states
the current phase-three contract; phase-two task-specific exceptions are
historical. The October 11 direction supersedes inherited short discovery
chunks, allocation defaults and advancement rules wherever they conflict with
this protocol. Earlier dated decisions and frozen protocol copies remain intact.

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
Before substantive work specify the broad objective, expected evidence,
protected floor, central/high D/L/E/O forecasts, expected waits and constructive
search directions. Keep this entry lightweight. Discovery needs a revisable
portfolio, not a single narrow hypothesis chosen as the whole task. Identify
cheap informative screens without requiring a full adversarial plan for each
early idea. A confirmation task separately specifies its exact claim and tests.

One task may span sessions; a gate is a separate attempt. P3-SEARCH-01 is one
continuing program with candidate branches and recurring cycles. Rejection of a
candidate closes that branch, not the program. At a research floor, the default
is to continue substantive discovery or recur in the same program. Routine
recurrences within this author-selected direction need no repeated permission.
Record interruptions, unfinished floors and next moves accurately. A handoff or
elapsed minimum is not a scientific stopping condition. Moving to a different
research stage requires its actual dependencies, not a completed clock alone.

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
claim. Save derivations and negative evidence proportionately. Reserve extensive
independent reconstruction for mature, load-bearing results; an inexpensive
constructive check may help develop an early candidate. Label self-review and
same-model review accurately.

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

Discovery cycles use prospectively committed floors of **at least 240 research
minutes**. The first cycle has a **360-minute central / 480-minute high** research
forecast; these are estimates, not upper limits. A floor is a minimum commitment,
not a target stopping time. Reaching it, finishing a test or rejecting the current
candidate does not complete the discovery program. Continue the promising
derivation, develop a new branch or commit the next recurrence. A checkpoint may
occur after substantial overshoot; preserve that actual duration.

**Do not end an active research session solely because its floor or forecast
has been reached.** When execution remains available and the selected work is
authorized, continue through a checkpoint into useful work or the next cycle.
An accounting checkpoint is not itself a handoff. Repeatedly ending at each
minimum while merely labelling the program open violates this continuation rule.

The roadmap's mode split is a forecast, not a retrospective quota. Do not pad,
wait or repeat solved work to meet a floor. Carry unfinished work and its floor
across sessions; only a prospective author amendment can reduce an accepted
minimum. If useful work on one branch is exhausted, return to the wider search.
If the whole program seems unproductive, explain the bottleneck and revise the
search direction; do not relabel exhaustion as positive completion. An author
pause or actual execution limit leaves the open state and remaining commitment
visible. Starting a new cycle does not reset cumulative effort.

Preserve the original phase 4/8/16-hour checkpoints and completed 60/90-minute
task commitments as history. P3-11's existing downstream floor remains separate.
The new program's first cycle earns zero credit from earlier phase overshoot.
Review the discovery portfolio at useful boundaries after **16/40/100 new
program research hours**, and report direction, returns, uncertainties and next
work. Tens or hundreds of hours may be appropriate; no total search ceiling or
guaranteed completion time is assumed. A forecast revision is a planning act,
not a reason to stop or consume hours without purpose.

## 4. Lanes, comparisons and contribution

The original traversal allocation of 570/150/240 D/L/E minutes and 25% recurrence
reserve are historical forecasts. Discovery now gives approximately **75%** of
research effort to hypothesis generation, derivation and constructive development,
**20%** to cheap feasibility screens, and **5%** to substantive portfolio/readiness
synthesis. Review this priority approximately over two cycles. It is a planning
choice implementing the author's direction, not a proven optimal allocation.
Administration remains O and is excluded from these research percentages.

Purpose and D/L/E are different axes: a prototype can be generative E, a theorem
can be constructive D, and a source comparison can enable a new mechanism.
Record what happened without reclassifying work to make ratios look right.
Start R/X at **25/75** for discovery. Reliable and exploratory work can both
generate ideas; lane percentages are forecasts, with departures explained by
the research rather than repaired through padding. Recurrence is the normal
continuation policy while the positive objective is unresolved, not a small
optional reserve activated only when an audit fails.

Generate materially different mechanisms, representations and combinations
before committing most effort to one. There is no idea-count quota. Reject
obvious defects or unfavorable elementary comparisons with short arguments or
small probes, usually minutes rather than a full work item. Derive repairs when
they open a plausible route. Deepen promising branches progressively and retain
alternatives. After two cycles without constructive strengthening, reconsider
the mechanism, representation, application or allocation before another long
challenge of the same approach. This triggers replanning, not termination.

Preserve the historical P3-N01 contribution and its exact modest scope. The
new **P3-POS01** objective requires a materially useful positive construction,
mechanism, guarantee or demonstrated capability/resource benefit tied to the
author's organizing question. A useful synthesis can qualify if its substantive
new consequence is supported; simply restating the existing modest contribution
does not meet the new objective. Explain why the claim matters before forecasting
its verification. Do not choose an easier minor target merely to obtain a pass.

Record object, type, exact delta, magnitude, evidence and named comparison scope
in [claim_ledger.md](claim_ledger.md). Report **work performed**, **scientific
finding**, **constructive progress**, and **readiness for confirmation** separately.
A completed negative test is useful evidence and can improve search; it does
not automatically satisfy positive advancement or end the program. Avoid an
unqualified "successful" label that merges these different judgments.

Compare with strong specified conventional constructions, including probability,
decision theory and bounded computation, under fair information and resource
terms. Here "ordinary" means this conventional comparison, not an infallible
or merely Boolean reasoner. Shared algorithms and equal outputs are permitted
and informative. A comparator class containing an identical candidate cannot
serve as a demand for strict superiority over every member. Name the strongest
relevant pre-existing implementations and distinguish a new mechanism or guarantee
from empirical superiority. Neither a weak baseline, superficial relabelling,
elapsed floor nor negative result alone satisfies the positive objective.

When a candidate is rejected or confirmation does not support the positive
claim, return the unresolved objective to P3-SEARCH-01. R-P3-N01 remains an
unselected historical option, not the automatic short-chunk fallback. Never
reset accumulated effort or declare a blocked phase complete by narrowing its
description after the result.

## 5. Readiness, confirmation and exposure

### Discovery stays revisable

P3-09 and P3-10 are completed historical stages; their freeze and exposed data
remain unchanged. All new P3-SEARCH-01 output is **DEVELOPMENT**. Candidate
definitions, representations and experiments may evolve in response to evidence,
with their lineage saved. Do not freeze a minor initial hypothesis and devote
the program to its elimination. The existing exposed results may inform new
ideas but do not become new independent confirmation of those ideas.

### Promotion requires a promising positive claim

Before expensive adversarial confirmation, specify the candidate version,
material positive claim, intended domain, comparison, relevant costs and exact
verification event. Require a reconstructable mechanism, successful inexpensive
sanity checks, varied developmental support where relevant, credible material
benefit, an explicit account of the closest alternatives, remaining uncertainty
and a feasible confirmation plan. A brief constructive review can improve this
assessment; it is not another full adversarial research task.

Record an evidence-backed forecast that the planned rigorous verification will
establish that specific material positive claim. The intended minimum readiness
is **80%**, with **90% preferred**. State a probability or justified range, its
basis, key sensitivities and any relevant forecasting track record. A range
extending below 80% does not establish the minimum. Include proof,
implementation, resource, comparison and empirical-transfer risks relevant to
the claim; do not condition away its difficult parts or weaken it to inflate
confidence. An **unassessed** forecast leaves the candidate in discovery.

This is a subjective probability unless stronger calibration evidence exists;
neither hours, a checklist, enthusiasm nor agreement among agents establishes
calibration. Preserve prospective forecasts and subsequent outcomes. Do not
invent a numerical estimate to unlock a gate. Inability to reach the intended
readiness level calls for more generation/development or an honest direction
review, rather than an expensive challenge of a candidate expected to be eliminated.

### Freeze a mature candidate for the appropriate verification

At promotion, revise P3-11's plan and realistic forecast, retaining its existing
minimum unless prospectively amended. For empirical confirmation, freeze the
candidate, dependency closure, environment, observations, task families, prices,
controls, seeds, budgets, materiality threshold, endpoints and analysis before
new final exposure. Account for selection across the search and any repeated
confirmation attempts; preserve all outcomes and use fresh or
appropriately separated evidence. Repeatedly testing until a favorable outcome
appears does not establish independent support.

For a mathematical claim, confirmation means a valid argument under exact
assumptions and rigorous reconstruction; a theorem does not need a held-out
dataset. An empirical usefulness or transfer claim needs separate appropriate
evidence. Discovery-derived examples can aid proof without becoming empirical
validation. No old runtime or seed schedule is imposed on a new candidate.

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

P3-11 is deferred pending discovery readiness and a prospectively specified
confirmation plan. P3-C requires support for **P3-POS01** as well as the retained
technical duties and contribution assessment; P3-N01's existing modest support
alone does not advance the amended program. An adverse or inconclusive
confirmation returns the positive objective to discovery. No elapsed floor,
negative finding, promotion or completed review automatically closes the program
or phase. The author retains the final advancement/completion decision.

At a task boundary synchronize TODO, claims, actuals, work log and affected
source/dependency records. Verification should resolve concrete remaining risks;
do not build an administrative test programme around minor prose edits. Keep
the root README polished and project-facing; operational status belongs here.

Sign new work with the actual contributor/model; preserve prior attribution.
Use the existing authorization to commit and publish this repository, verify
the resulting branch head, and report actual publication status. If transport
is unavailable, use the authorized ZIP/PowerShell handoff. Transport and
packaging do not satisfy research floors.

## 7. Methodological basis and limits

The allocation, cycle floors and 80–90% readiness aim are the author's research
policy, operationalized here; the literature does not establish those numbers
as optimal or guarantee a discovery after a given duration.

[Nosek et al. (2018), *The preregistration revolution*](https://www.pnas.org/doi/10.1073/pnas.1708274114),
"Preregistration in Practice" and "Challenges 5–6," distinguishes flexible
discovery from later prediction and permits initial exploratory experiments
followed by prospective confirmation of an interesting result. It also explains
why reporting all outcomes across a research program matters. This supports the
late empirical freeze, not an obligation to preregister every speculative idea.

[Gneiting, Balabdaoui and Raftery (2007), *Probabilistic forecasts, calibration
and sharpness*](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jrssb.pdf),
pp. 243–244, distinguishes confidence in a forecast from agreement between
forecasts and observations. Its forecast-evaluation framework motivates keeping
prospective predictions and outcomes. It does not validate any readiness
percentage for this project. These empirical methodological sources do not
replace proof obligations for mathematical claims.
