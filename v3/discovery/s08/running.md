> **Closed:** this is the historical in-session notebook. Use [cp01](cp01.md) and [findings](findings.md) for the reconciled closing state. No active clock remains.

# Running s08 recovery note (not an ending checkpoint)

## Newest boundary — October14 03:39:47Z

**Read this section before every older boundary below.** Current resident
PID37724/runtime python-pid-37724-821b39cb-ab91-4b3b-af82-aaba6f1bafb5 is alive.
At2026-10-14T03:39:47.657352Z, mono1041771295857700, raw closed research is
13,867,127,256,300ns. Four dispositions total1,086,165,872,000ns, so effective
closed research is **12,780,961,384,300ns =213.0160230717 minutes**.
**26.9839769283 engaged research minutes remain before the requested240.**
Do not end early. Open mode is O for this checkpoint; resume D/L/E at a fresh
boundary. Any compaction in this O interval never earns research credit.

The fourth disposition excludes the entire mixed D/context interval from
02:50:11.301373Z mono1038794939876000 to02:55:18.137883Z mono1039101776391600,
306,836,515,600ns. No changes to older clock treatment. Raw closed modes at
this boundary: D5414880074900,L1267039357600,E7185207823800,O187248572500,
unmeasured197360591000. No PTY processes are running, and no agents exist.

New work since the preceding checkpoint (all DEVELOPMENT):

- sf02 succeeded after sf01's retained cache-execution failure:29,529 count
  actions,24 strict tolerance improvements over the one-copy restriction,
  and6,078 general-group world checks. shared_findings.md summarizes it.
- nominal_bank.md gives the shared-cost counterexample: z in[0,5], observed
  neighbors(2,3),weights(5,2). Best action optimal under any nominal z has
  regret20, but counts(1,1) have19 and are never nominally optimal. This is
  known robust-optimization geometry; s07/robust_witness.py already supports
  non-nominal proposals. Kasperski/Zielinski survey section2.2.2 was read.
- group_frontier.py/gf01:33 groups,7,293 small action checks,2,125 targets,
  99 mutations rejected;12 group-pair convolutions,1,818 action products,
  726 targets. Second nominal-bank gap54→50 in large1. Local DP keeps min
  right regret per exact left regret; global independent groups convolve.
- partial_star.md/.py ps01 crashes with access violation after six cases;
  ps02 full retry succeeds:2,720 receipt states,180,960 actions,544,800
  world comparisons,67,425 tolerance targets,8 correct cap UNRESOLVEDs.
  Unknown-center DP needs(R_left,R_right)→minimum U; observed center uses
  summed edge regret→minimum U. Exact combined bound=max(R,U+A_hi-price).
- observation_policy.md/.py,op01:24 exact physical-fee minimax policies on
  four stars/six duties each; four actual local mandatory-resolution steps.
  6,144 outputs total,1,536/arm, all96 acquisitions and96 reconstructions
  succeed first attempt. Minimax/ordinary fee6625,audits1682,units319678838;
  cheapest/fullfrontier7847/2486/2848339; narrow8112/2535/13299167.
  Complete optimality diagnostics cover28,312 states and471,764 actions.
- policy_admission.md/.py(op02 code policy_safety.py) removes unnecessary
  optimality-proof burden from service.24 selected DAGs contain268 states,
  extraction392604units,safety29375,original actual search28167394 retained.
  3,072 fresh paid outputs on exposed rows; safe/ordinary each fee6625,
  audits1682,units28932145,setup28596793. All88 negative controls fail;
  all48 acquisitions and48 reconstructions finish first attempt.
- decision_regions.md/region_policy.py dr01: existing HEC/DIRECT prior art
  revisits s01/S04, not a newly discovered general framework. Explicit
  DIRECT passes4500 terminal checks,25875 edge-mass identities,9720 adaptive
  comparisons.24 policies safe,193035927 total construction/check units;
  expected physical fee ties cheapest in23 duties and is worse by1/2 in one.
  **No paid DIRECT service** after the negative screen. Probability masses
  in its product objective are unnormalized prior masses. No old numerical
  approximation ratio imported; later adaptive-cover correction matters.
- policy_tradeoff.md/.py pt01:805158 budget states,23546334 diagnosticunits.
  Exact sum of expected fee per duty:original minimax827/8,mean-optimal at
  same worst caps803/8,unrestricted22501/256,cheapest31539/256,DIRECT31667/256.
  All selected policies evaluated over every supported world; zero new audits.
  Do not charge full budget sweep as unavoidable expected-only planning.
- anchor_cover.md/.py ac01: for price A=10HW,anchor0/A,tauHW, full stopping
  predicate is ordinary capped weighted endpoint-score cover. Either anchor
  response ends; withoutanchor min original repair upper cost<=HW is exact.
  12000 partial states,98840 submodularity checks. Expectedgreedy fees335/64,
  433/64,1501/256,877/128 vs optimum41/8,433/64,93/16,197/32.
- anchor_service.md/.py ac02: four new development streams128 rows each,
  seeds8141680..83, four arms,2048 outputs. Cover/ordinary each fee3349,
  audits1091,units159334,setup41398. Cheapest4270/1299/1694402/716;
  anchor-only4608/512/150610/716. All16 acquisition+16 reconstruction units
  succeed first attempt. Reuses four old resolution receipts, zero new
  resolution/completeSAT calls. Live anchor_cover.py changed choose() to
  read public support directly and charge it, avoiding uncharged source
  regeneration. ac01 frozen impl remains intact; ac02 rebuilds/checks all
  four policies exactly equal to ac01 choices. Historical invoices unchanged.
- policy_findings.md summarizes all policy/cover outcomes. Againstanchor
  cover saves1259fee and adds8724namedunits, proxy crossover8724/1259.
  This is not a complete economic region; ordinary mirror ties, F01 unchanged.
- **Current newest:** graph_cover.md/.py gc01 generalizes to arbitrary
  paired-component graphs with source-bound clique MaxCut upper K<=W,
  tau=HK, quotaQ=H(2W-K). Balanced action has regretH MaxCut<=HK. Without
  anchor, full duty is min upper cost<=tau; ordinary edge-max cover exact.
  Clique allocation proof K=sum lambda floor(|C|²/4)+residual edge weights.
  gc01 all20 cases n2..6 path/cycle/clique/sparse finish first attempt:
  496cut checks,80 negativecontrols; small4032receiptstates,843840action
  classes,2052900cornerchecks,3568terminalactions; larger66996actual-world
  actionchecks. Eight cases improve K<W; sparse n5K17 vsactual16,n6K23 vs22
  correctly keep loose bounds.20 local resolution steps,zero physicalaudits.
  No general-graph paid service yet. Potential next: efficient ordinary
  greedy on this geometry, or derive its cost/tolerance limits. Do not hide
  exponential action/world expansion or force a paid run after negative work.

Still not done: session final synthesis/forecast reassessment, exactly one
recurrence row+JSON, final clock reconciliation/ledger corrections, active
plan/TODO/candidates/CONTINUE updates, full verification/math/path/evidence
checks, staging, commit,push,PR and attachment. Current branch remains
codex/discovery-20261013-s08 at original base6b79228; no commits/push/PR.
Preserve all failed prefixes/logs and exact frozen bytes. Current live source
changes may deliberately differ from frozen screen implementations; reproduce
historical screens from their saved impl/declaration, not by overwriting them.

Primary sources newly read include Chen et al. DIRECT AAAI2015 pages3512–15
https://ojs.aaai.org/index.php/AAAI/article/download/9694/9553 (extended PDF
failed), Javdani HEC sections2–4 (already s01 prior), Deshpande et al.1303.0726
sections4.1–4.3 (Q-value product construction and limitations), and rechecked
Al-Thani et al.2208.08351v2 Theorem1.5 and related-work correction. Briefly
append exact locators to source_notes.md if useful; full new notes are in
decision_regions.md. Do not import old cover constants without hypotheses.

## Latest boundary — read this before older chronology

At **2026-10-14T02:47:45.067667Z**, the resident is still PID 37724, runtime
python-pid-37724-821b39cb-ab91-4b3b-af82-aaba6f1bafb5. Its closed raw research
is **10,907,074,644,800 ns**. The three dispositions now total
**779,329,356,400 ns**, leaving **10,127,745,288,400 ns =168.7957548067 minutes**
effective research. **About 71.204 research minutes remain before the author's
240-minute target. Do not end early.** The open mode is O for this durable
checkpoint; resume D/L/E at a newly observed boundary. If compaction occurs
while O is open, exclude that mixed O interval from engaged administration too
where practical; it never earns research credit. The new third disposition
excludes D from 02:09:43.236630Z mono1036366875142800 to 02:14:35.315682Z
mono1036658954195000 (292,079,052,200 ns).

The newest completed work, all DEVELOPMENT, is:

- ct01 checks cheap receipt-conditioned circuit contrasts; its expanded
  heuristic menu is pointwise pruned in screen_ct01.py. is01 subsequently
  executes and reconstructs 24,576 paid outputs on 24 streams/four arms.
  Circuit pilots improve on replay on some cases, but own-invoice learning
  pays less physical fee in every nontrivial case. See
  invoice_service_findings.md. Ordinary circuit mirror ties exactly.
- ga01 checks ordinary general-graph primal-dual query certificates on 2,544
  worlds. graph_audits.md proves the physical-fee factor two and the compact
  receipt/mandatory-set lower bound. Primary prior art is explicitly read
  and attributed, including Halldorsson/de Lima section 7. receipt_optimum.md
  derives the sharp compatible-world lower bound as mandatory fee plus a
  residual weighted vertex cover. No hidden optimum reaches the controller.
- gs01 executes 1,536 graph actions, gs02 1,152 more on the same exposed rows.
  gs02 adds incremental greedy and adaptive local ratio. Every output is
  reconstructed. graph_findings.md reports aggregate bills and limitations.
  ga02 fails after its small checks with an access violation; ga03 reruns
  successfully, including 384 exact greedy trace comparisons. gs01/gs02
  acquisition processes all complete first attempt. One gs01 reconstruction
  failure remains with a successful retry. Both dual/ordinary mirrors tie.
- tolerance_graph.md/.py and tg01 prove/check paired-component minimax regret
  R=2 MaxCut(unknown induced graph)+middle/unknown boundary weight. Bipartite
  geometry makes this scalar. Worst-case audit planning becomes ordinary
  degree-quota minimum knapsack; a prior-free greedy has ordinary 2H(Q)
  pointwise comparison. tg01 checks 15,328 partial states, 160,128 worlds,
  37,536 actions and 46 Bellman/knapsack comparisons (6,688 Bellman states).
  No paid tolerance-only service was declared or run; see tolerance_findings.
- replacement_frontier.md/.py and rf01 show that a witness with larger
  repair-only regret can lower the absolute upper cost against replacement.
  The frontier is ordinary subset sum on a known-M-center star. rf01 checks
  10,920 states, 111,972 actions, 76,536 tolerances and 3,768 explicit worlds.
- fs01 is the paid version: six actual local resolution steps derive common
  mandatory features; zero complete SAT calls. Four arms each complete 1,632
  outputs, total6,528. Frontier and ordinary mirror: 13,399 audit fee/3,451
  audits/2,205,711 named units. Balanced-only:15,403/4,019/2,208,404. All
  original actions and compatible worlds are reconstructed. Five larger
  checking attempts fail, then checks are split by arm/duty; two small
  attempts also fail and retry. No acquisition attempt fails. Preserve all
  logs, fs01/check_initial.py and part reconstructions. frontier_findings.md.

**Current constructive direction:** shared_frontier.md/.py. A single unknown
cost shared by several incident components requires a joint regret frontier,
not separate edge maxima. For known neighbor costs1 and weights(3,5), counts
(0,2) produce exact R10/U22 at tolerance10; balancing gives R8/U24, and the
previous one-copy positive-bias rule misses the useful signed bias5-3.
Two-copy bounded subset sum is the correct ordinary planner. sf01 fails near
the end with "Executing a cache"; sf02 is its fresh retry (inspect results
before proceeding). This finite screen has 25 degree/weight cases and20
general interval groups, no physical audits. A useful next step is to check
global convolution across independent unknown groups, then prospectively
declare a paid source/receipt service if the small screen warrants it. The
same geometry/grouping/knapsack capability belongs to ordinary controls.

All final publication administration remains undone: effective actuals and
ledger reconciliation, one recurrence append plus numerical F01 reassessment,
active pointers/continuation/plan correction, verification/math/index-path/
evidence/portability gates, commit, push, PR and attachment. Still on branch
codex/discovery-20261013-s08. Do not confuse historical carried F01 metrics
with these different development domains. No F01 event replacement/promotion.

## Earlier chronology

Codex (GPT-6), October 14, 2026 UTC. The author requested **240 minutes of
new engaged research**, followed by publication/handoff. This session is
still active, with most of that commitment remaining. C001 OPEN, P3-POS01
OUTSTANDING, P3-11 deferred. No new forecast event or readiness promotion.

Branch `codex/discovery-20261013-s08`, based on main `6b79228`. Prior effective
program/cycle time is 29,849,134,566,547 ns; prior phase is 95,017,016,608,396 ns.
The old live plan incorrectly still points at s06; it must be repaired during
final administration, using s07's actual effective record as the baseline.

The original resident PID 27120 crashed after an invalid client mark. Its
closed raw totals were retained; its last unclosed interval earns no credit.
The current resumed resident is **PID 37724**, with a fresh runtime identity,
running clock_resume.py. See crash01.md and the preserved original actuals.
Use `python v3/discovery/clock.py
mark v3/discovery/s08 MODE LANE PURPOSE NOTE`, report and end. Preserve raw
ledger and observations. Apply [dispositions](dispositions.json) later: the
mixed context-refresh intervals (196,931,799,100 and 290,318,505,100 ns) receive
no credit, in addition to raw unmeasured gaps. At the last research mark,
2026-10-14T01:51:11.392293Z, raw research was 7,611,495,199,700 ns; subtract
487,250,304,200 ns for those two dispositions. **About 118.74 credited minutes
were closed then; more than two research hours remain in this session.**
If a later refresh lands inside a research segment, exclude that entire mixed
interval conservatively. Current raw totals are not final effective totals.
Do not mistake the already satisfied **cycle** floor for this session's
separate 240-minute commitment. Publication/maintenance earns no research time.

Completed DEVELOPMENT evidence and interpretation:

- [G01](g01_findings.md): actually acquired geometry and residual proofs,
  complete threshold/audit routes; strong ordinary controls tie or cost less.
- [Improving maps](maps_findings.md): optimum-preserving reduction even when
  the full feasible set has no affine equation. Larger uncertainty-set work
  outweighs reduced audit count; ordinary star control ties. Preserve maps01
  failed source/record and maps02 completed run.
- [Joint guards](guard_findings.md): exact tree upper/attainment certificates;
  the general guard contains maximum cut. Zero physical audits in guard01.
- [Action-adaptive audits](aa_findings.md): residual minimax regret equals
  maximum cut of the unaudited induced graph. On forests the observation task
  is weighted partial vertex cover. aa01 has 1,028 outputs per arm; ordinary
  residual-axis DP can tie the candidate. Do not infer novelty from a slower
  cost-axis implementation. The aa01 declaration was preserved byte-exactly
  after later math formatting corrections in the live derivation.
- [Star development](star_audits.md): three-level costs break binary coverage;
  exact adaptive star fee reduces to inherited S21 optional AND ordering.
  star01 checks 26 cases/27,652 Bellman states and binary minimax separately.
- [Receipt learning](learning_findings.md): learn01 completes 30,720 outputs
  across three environments/five arms, learner and ordinary control tie.
  learn02 failed before acquisition (rational hash encoding); learn03 fixes
  encoding and uses 12 confidence epochs per arm, completing 12,288 additional
  outputs on the same exposed development rows. Favorable fee savings survive
  some compute prices; unpriced costs remain explicit, no complete-cost win.
- [Path planner](path_findings.md): path01 checks 24 cases, 86,352 full-history
  states, 13,104 conditional source outcomes, 1,008 probability-box endpoints.
  Exact interval DP is ordinary and supplied-parameter; zero physical audits.

The [compact path-policy certificates](pc_findings.md) are now executed in
pc01: 72 small supplied policies match 3,624 full-history rectangular-adversary
states, six large certificates check, and four tampering controls reject.
The explicit monotonicity counterexample is a correct invoice bound 13 versus
an invalid lower-probability-only bound 3. All are conditional calculations,
with zero physical audits. A ratio proposer rescans intervals and is cubic;
certificate production/checking are quadratic. Preserve that limitation.

The following was the first recovery note's next derivation and is now
completed; use the later entries below for current direction:
[correlation-model learning](correlated_models.md).
The marginal-only guarantee fails even with exact one-half marginals: a
five-node complementary-pair source costs 4 against the independent forecast
15/4; n=6/7 also fail. All finite pairs were screened and saved. Develop exact
partial-pattern likelihoods for a finite symmetric Markov menu rho=
{1/10,3/10,1/2,7/10,9/10}, then boundary-conditioned path policy evaluation,
then an actual paid receipt-learning service. Use predictable query likelihoods,
not unconditional marginal frequencies. The common mixture-likelihood set
retains the true model with probability 1-alpha over all observation times
under finite-menu membership; this premise is not learned for free. Retain
unknown model identity across components or use an explicitly conservative
relaxation. Source admission, inference, proposals, checks and retention all
belong in the bill. See the prospective document for exact first-step scope.

The independent product law at the lower probabilities supplies a lower
bound for the optimal path policy; the explicit-policy upper proof separately
uses conditional bounds, avoiding an unnecessary interchange assumption for
all history-dependent laws. Primary-source boundaries are in source_notes.md.

At the eventual authorized boundary: close/reconcile the clock; append one
recurrence row to the existing single chronological table, with measured vs
carried metrics and numerical F01 reassessment; update active pointers and
portable CONTINUE (future default remains 60 minutes unless overridden);
run complete suite/math/path/evidence/portability gates, commit and publish PR.
Attach any created PR to this chat. Preserve all historical scientific bytes.

## Additional completed work through the mid-session checkpoint

All entries below remain DEVELOPMENT, attributed to Codex (GPT-6).

- mk01 checks finite Markov likelihoods and interval planning. ms01 executes
  13,824 outputs across finite-model learners and controls. pl01 executes
  13,824 more on the same exposed rows, using only a compulsory first-pair
  statistic and stopping on a common acceptable-policy region. Ordinary
  mirrors tie; see pair_findings.md and forced_calibration.md.
- cont01 checks continuous-parameter expected-fee polynomial certificates.
  cs01 executes 46,080 outputs on nine off-menu development streams; mi02
  adds 18,432 on those same exposed streams with an exact Bernoulli mixture
  confidence interval. Independent reconstructions complete for every case.
  See continuum_findings.md and mixture_findings.md; no complete-cost win.
  mi01 checks the mixture interval arithmetic separately.
- aq01 constructs identical compulsory-receipt laws with reversed policy
  ranking, proving that calibration does not establish model-family adequacy.
  ic01 checks exact source-free completion intervals for another policy's
  invoice: 32,760 partial states, 218,400 completion comparisons and 2,520
  own-policy collapses. Its interrupted prefix is preserved and remaining
  five cases are resumed in ic01_finish.py. See invoice_completion.md.
- ib01 executes 9,216 ordinary on-policy invoice-bandit outputs without a
  Markov assumption, then reconstructs every receipt/action/learning update.
  Its bill is much cheaper than whole polynomial admission, with greater
  exploration cost. Three interrupted attempts remain; ib_findings.md.
- pi01 checks paired invoice ADDs for 82 pairs, 18,313 partial patterns,
  12,321 strict contractions and 6,735 extra exact contrasts. Four failed
  attempts are retained. ia01 compiles policy ADDs compositionally; n=32/64
  hit the 250,000-node cap. ev01 uses ordinary edge-valued diagrams and
  checks pair identities; n=16 improves substantially but all four n=32/64
  units still cap. ev02 applies the same representation to actual service
  fee vectors. See diagram_findings.md, paired_invoices.md, edge_invoices.md.
- sy01 implements a much cheaper ordinary normalized invoice circuit.
  Its separate checker validates every recurrence for 25 fee vectors and
  five policies each, including n=64. It matches all completed ADD/EVBDD
  invoice-equivalence groups. Service n=6/10 have two invoice classes, n=16
  five. See invoice_syntax.md and check_invoice_syntax.py. Small truth-table
  checks and larger finite-world checks are distinct from the later local
  proof checks; do not conflate their evidence dates.
- ib02 executes and reconstructs 9,216 source-free ordinary bandit outputs
  with checked syntax-equivalence pruning. It has mixed finite-horizon
  effects: n=10 physical fees rise on all exposed streams; n=16 outputs/fees
  exactly match ib01 while preparation increases 48,297 named units.
- cq01/cq02 implement and check minimum worst-case **contrast-only** audit
  planning on normalized residual functions. All 128/2,048 world/logger
  cases are conditional, not physical acquisitions. At n=6 direct target
  ties ordinary replay (156 total added fee). At n=10 it is worse on eight
  worlds (1,852 versus 1,788 total). Do not execute a paid experiment merely
  to repeat that negative screen. See contrast_findings.md and the separate
  target_counterexample.json, which proves a small off-menu target saving.

**Current constructive direction:** use the cheap checked normalized invoice
circuit for direct fee-contrast evaluation, cancelling shared sums before
buying values. Whole EVBDD minimax planning did not repay its overhead on
the exposed pair. A source-free paired statistical estimator needs every
row's missing contrast completed or an explicit probability correction;
naively taking only naturally complete cases is biased. Review the existing
partial_contrasts.md derivation and the ordinary control-variate literature
boundaries before choosing another bounded experiment. No new paid service
design for this direction has been frozen yet.

The author explicitly permits rerunning apparent stochastic program failures
on this unstable CPU. Preserve every prefix and log and reconstruct durable
outputs in a fresh process. Python 3.13 and bundled 3.12 have both crashed.
Fresh cold processes generally fare better: python -B -X
pycache_prefix=v3/discovery/s08/unused_cache -X faulthandler. This does not
prove hardware causation or license hiding deterministic errors. No timings
from this host support a robust performance claim. Unknown failed cost is
never zero. All final repository gates, clock reconciliation, recurrence
append, handoff, commit, push and PR publication remain outstanding.
