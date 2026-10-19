# CLOSED: s12 recovery entry point

Codex (GPT-6), October 19, 2026. Research and the resident clock are CLOSED.
Read checkpoint.md, effective_actuals.json and publication.md. The fresh
240-minute commitment is satisfied with14,422,390,000,000 ns. Do not restart
this clock or follow the historical in-progress directions below. Program
and phase totals are80,282,330,241,147 and145,450,212,282,996 ns. Seven interrupted
research intervals and explicit context recovery are excluded. Remaining work
is administrative publication only; its status is in publication.md.

The following earlier recovery snapshots are preserved as history.

# Active s12 recovery checkpoint — not a handoff

Codex (GPT-6). The author requested another four-hour recurrence. It is still
ACTIVE and its fresh 240-minute floor is unfinished. Continue this same session;
do not start another clock, reset its commitment or close it from this note.

At the observed boundary **2026-10-19 08:08:31.379016 UTC**, monotonic
**14,400,812,000,000 ns**, the resident clock had closed **13,185,375,000,000 ns**
of raw D/L/E. Apply the six exact context exclusions in
[dispositions](dispositions.json): **1,688,422,000,000 ns** in total. Effective
closed research is **11,496,953,000,000 ns = 191.6158833333 minutes**.
Remaining fresh commitment: **2,903,047,000,000 ns = 48.3841166667 minutes**.
This snapshot is superseded by later observed segments; never add it twice.
The clock's old-cycle `remaining_floor_ns=0` is not this session's remaining
four-hour commitment. Read `session_research_target_ns` and dispositions.

The current runtime is python-pid-16108-a0370202-0b44-4a62-8406-0e0e73b9cd80,
localhost port 57790. The open interval at this snapshot is O/administration,
excluded from research. Use [mark.py](mark.py) with the bundled Python runtime;
its arguments are mode, lane, purpose, note. O/wait/unmeasured require lane `-`.
The original source is ../s10/clock_source.py. Do not rerun start.py.

Mode granularity note: the L intervals beginning 04:36:13.684509 and
04:41:15.922894 included substantial constructive derivation before the next
mode mark. All of that activity was engaged D/L research, but the internal
D/L boundaries were not separately observed. Preserve the raw intervals and
report mode allocations as coarse; do not claim exact D-versus-L time from
those marks. This does not add or reconstruct any total research time.
The L interval 05:21:17.799145–05:25:17.730863 similarly included derivation
after reading sources; its total engagement is observed but internal mode
allocation is coarse. All context exclusions still need their single final
ledger correction at reconciliation; do not apply them twice.

## Scientific work saved so far

- [Search notebook](search.md): diverse early screens, including conventional
  conformal/active inference/numerical-certificate antecedents; operational
  cost observability versus whole-law identification; graph permission work.
- [Noisy invoices](noisy_invoices.md): independent known additive noise
  preserves finite invoice-law identification; finite-budget marker/bundle
  design; price and precision must both be charged. A constructed sigma=4
  example uses worst fees 35,967 versus 3,690 for the same sufficient precision
  bound. This is **89.7406% less within the two declared designs**, not measured
  application superiority. Ordinary noise-aware design ties.
- [Noisy resets](noisy_resets.md): naive products have exponential second
  moment; repeated within-instance averaging and decoding gives a stable
  O(k log k) per-world bill at fixed precision/noise. This adapts classical
  noisy-query repetition; no novel general rate or all-method lower bound.
- [Permission compiler](permission_compiler.md): bounded-width target clauses
  compile from local source projections. For 2-CNF sources and binary targets,
  cached initial pair projections plus forced-literal propagation remain exact
  under receipts, by a majority argument. General coordinatewise unary maps
  (including overwrites) compile to 2-CNF on two action bits per coordinate.
  The all-unary-map extension has now passed its separate finite screen below.
- The same note gives a Horn width-three obstruction, implication-DAG
  factorization and maximum-closure reduction, independent-set optimization
  hardness after observations, and an offline certificate/set-cover reduction.
  The compiler does not solve optimal query planning or all edit optimization.
- [Transport](permission_transport.md): conservative projection caches,
  checked exclusions and source-clause dependency invalidation; derived only.
- [Edit ordering](edit_order.md): exact queries can precede side-effect-free
  coordinatewise edits under explicit atomic postponement and fixed-cost
  assumptions; coupled actions or changed sensors fall outside this result.
- [Literature](literature.md): exact primary locators and access limitations.
  Conformant planning, 2-SAT, majority closure, noisy query repetition and
  statistical design are established machinery. Narrow adapter priority open.

Several small probes ran successfully on the bundled Python interpreter; retain
their executed sources unchanged and use new files for extensions:

- noise_probe.py/json/stdout.txt/stderr.txt: 19 menus, 40,736 semantic checks;
  exact rational enclosure for the headline sample-count calculation.
- permission_probe.py/json/stdout.txt/stderr.txt: 180 seeded formulas,
  126 satisfiable sources, 6,847 consistent receipts, 5,429 contradictions,
  26,324 projections, 181,244 masks and 50,288 implication checks.
- map_probe.py/json/stdout.txt/stderr.txt: 56 satisfiable sources, 1,592 receipts,
  310,208 all-map checks and 305 growing chains with amortized counter bounds.
- affine_probe.py/json/stdout.txt/stderr.txt: 64 fixtures, 1,098 consistent
  receipts, 192,936 map checks, 13,532 translation and 18,688 erasure checks;
  circulation menus 2 to 4/8/16 for chain sizes 2/3/4.
- parity_price_probe.py/json/stdout.txt/stderr.txt: 14,280 formula/oracle
  comparisons, every three-bit affine source, four prices, two caps/five fees;
  24,360 Bellman states and 2,251,480 program choices, 0.9202475 seconds.
- and_price_probe.py/json/stdout.txt/stderr.txt: 1,040 formula/oracle comparisons,
  57,760 Bellman states and 5,892,400 program choices, 2.2601667 seconds.

New notes since the earlier snapshot:

- [proof_risk.md](proof_risk.md): sharp marginal-error reliability LP over
  proof-support transversals, plus one fixed shared-risk dual certificate for
  adaptive action choice. Conventional reliability optimization; derived only.
- [affine_edits.md](affine_edits.md): safe unary maps form a linear system,
  homogeneous part is the established code conductor. Queries cannot enable
  new XOR translations of an initially valid affine source, but one zero
  observation can enable 2^m distinct selective erasures in a circulation code.
- [parity_price.md](parity_price.md): exact positive-fee/capped-private-reset
  parity bill and affine-source minimum over character representatives. The
  maximum-invoice-path lower bound avoids the earlier false pathwise argument.
  No within-episode repeats, exact invoices and hard zero-error worst bills
  are essential. Expected-cost randomization can save markers; Gaussian noise
  precludes finite zero-error decoding. Task-specific fallible relations can
  suffice without whole-model truth, with genuine calibration still required.
- [and_price.md](and_price.md): exact conjunction formula under the same full
  source interface. Unit-fee full conjunction costs n+1+q*f versus parity
  n+q+q*f, q=ceil(n/(H-1)). Both have ordinary query complexity n. Derived
  lower/upper bounds and the separate finite screen agree.
- [censored_values.md](censored_values.md): roulette correction of unfinished
  verification, progressive-prefix variance identity, unbounded variance
  obstruction and the impossibility of a non-exact bounded per-instance
  unbiased truth forecast. Established debiasing; parked without a harness.
- [receipt_width.md](receipt_width.md): exact forced-coordinate projection
  pruning under all receipts characterizes 2-CNF sources; extends to arbitrary
  target scopes and a semantic prime-implicate-width hierarchy. Derived only.

No scientific run has failed so far. Several attempted prose patches failed on
incorrect context before application and were corrected after inspection;
an unrelated arXiv identifier was opened but contributed no scientific claims.
Direct primary literature access failures are recorded in literature.md.

All work is DEVELOPMENT; no new promotion forecast or family number assigned.
F01 remains its dated October 14 carry; R11-M/I11-M remain unassessed. The
program is broad discovery, not a mandate to spend the rest of the recurrence
testing either of these two lines. First finish a proportionate all-map and
incremental-cost screen, then return to materially different candidates.

The preceding next-step sentence is superseded: all-map and incremental screens
have passed. Later work includes graph_invoices.md/graph_probe, exact paid
relation_calibration.md/calibration_probe, error_transport.md and the derived
cycle_errors.md duality (not yet probed). cap_two.md/cap_two_probe reduces the
whole cap-two interface to ordinary outcome-dependent-price decision trees.
All 783,360 worst and expected comparisons pass; named candidate choices fall
from 7,470,800 to 1,769,400 inside the shared probe, not a complete-cost claim.

**Latest constructive lead:** variable_invoices.md and frozen variable_probe.py.
Prefix stopping recovers all n unit-price bits with expected excess
n/(2^H-2)+O_H(1), retaining the hard parity worst bill at zero episode overhead.
36,868 explicit executions and 30 small unrestricted expected-oracle panels
pass. n=3/H=3 mean 15/4 versus fixed-block 4; n=4/H=3 mean 39/8 versus 5;
worst bills remain 5 and 6. Positive overhead favors finishing only the parity,
and fixed blocks can win at larger overhead. A restricted hybrid DP is derived
but not run. Public independent XOR masks remove the uniform-truth premise:
the same expectation holds for every fixed hidden input, with zero error.
The masking/averaging proof also transfers small uniform oracle optima to small
randomized minimax optima. This is ordinary symmetrization adapted to the
private interface, not a new minimax principle. Random bits and controller work
are real and not yet priced; no all-size expected optimality claim is made.

Next useful steps: a small hybrid/masking screen if it changes a decision;
read Ben-David–Blais 2020's forecasting algorithms as a materially different
bounded-mathematical-uncertainty lead; then continue broad generation. The
paper's Introduction was read and cited, but later technical sections have
not yet been read. Avoid another large sweep merely to increase test counts.
All executed sources and outputs remain frozen. No s12 commit or PR exists.

Update after that next-step forecast: the forecasting sections have now been
read. forecast_scores.md preserves the conditional-score premise, an ordinary
supermartingale extension and a population-score repetition counterexample;
the generic idea is parked without a harness. quantized_invoices.md and frozen
quantized_probe.py now give a closed unit-price parity bill for bucketed
readout, with 192 finite oracle comparisons passing. The general monotone
quantizer extension reduces exact price to integer capacity cover; its affine
source corollary is derived but not yet probed. This oracle correctly retains
hidden actual costs inside each public bucket as per-world remaining budgets.
The current open O/context segment intentionally covers the coming refresh;
do not add a research exclusion for it or reconstruct any credit.

## Administrative state

Branch codex/discovery-20261018-s12 from merged main
b815009c1fcc458b85bd83129f2ab23c554e65eb. PR13 was merged and the prior s11
remote branch removed; local historical branches preserved. No s12 commit or
PR yet. TODO and CONTINUE have an active-session override. The chronological
table still ends at s11; append exactly one new row for the complete s12
recurrence at its eventual close, including relevant fees/computation and the
ordinary comparator. Publication and handoff preparation earn no research.

Default later-session duration remains one hour. No automatic next session,
automation or subagent delegation is authorized. Mark and exclude context
refreshes/unobserved tails; keep at most 15-minute research boundaries and
brief user updates during the remaining work. The user's host-instability
note permits unchanged retries, not deletion of failed evidence.
