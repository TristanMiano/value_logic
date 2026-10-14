# Prospective paid Markov-model service

**Codex (GPT-6), October 14, 2026 UTC. DEVELOPMENT.**
The [correlation-model derivation](correlated_models.md) and
[mk01 reconstruction](mk01/results.json) now support an actual service test.
Mk01 matched 5,460 partial-pattern likelihoods, 2,508 boundary probabilities,
24 optimal path cases/13,080 Bellman states and 120 cross-model policy values.
Its terminal adaptive observation patterns partition the source with total
likelihood one under every candidate model. Those were conditional calculations
and acquired no physical source receipts.

## Frozen development source

Use path sizes n=6,10,16, with positive audit fees sampled uniformly from
integers 1..9 using one Python random generator at seed 8141440, in that order.
For each size use true repeat probability rho=1/10,1/2,9/10, for nine cases.
Each case supplies 256 fresh requests. Hidden row seeds are 8141450 through
8141458 in size-major, true-rho-minor order. This is a fixed development matrix,
not a selected favorable set or a calibration/transfer study.

The public source has the independently checked exactly-one path factors,
positive unit edge scales, ternary costs and the fixed unknown parameter menu
{1/10,3/10,1/2,7/10,9/10}. The actual parameter is withheld from service
controllers except the labelled oracle diagnostic. Initial extreme/middle
indicator is fair; each subsequent indicator repeats with the true probability;
extreme labels are 0/2 with equal probability. All rows are fresh under one
fixed model per case. Freeze source, code, seeds and arm definitions before
generating any hidden row.

## Paid arms and prepared policies

Compare full identification, a fixed independence-model policy, a fixed robust
menu policy, a receipt-likelihood learner, the identical ordinary learner, and
a known-model oracle diagnostic. Independence-only is a misspecified resource
forecast when true rho differs; its outputs still require exact action checks.
It is not used as the sole strong comparison.

Each robust/learning arm separately prepares one optimal root policy under
each of the five menu models. It evaluates every policy under every model and
checks the resulting upper tables. A separate checker computes two-state
transition powers by matrix recurrence, not the producer's closed power
formula, then verifies the selected-policy Bellman inequalities. This checks
upper invoices, not optimality. The full planner's finite optimality evidence
is mk01; every admitted menu policy remains a valid fallback even if suboptimal.

The static robust arm selects the candidate minimizing its largest full-row
fee over the whole menu. The learner selects the candidate minimizing its
largest fee over the current retained confidence set. Selection, preparation,
all cross-evaluations, source admission, checking and retention are charged.
An identical ordinary controller receives all of these capabilities.

## Observation and learning order

Freeze the selected policy and confidence set for each request. Execute its
ordinary/forced interval tasks with a stack; buy each receipt once and flush
the prefix before the next query. Construct an original-source satisfying
action only when every edge has a known extreme endpoint or both endpoints
are known. Independently check its local dominance for all compatible values.
Save the checked output before reading hidden unqueried values in diagnostics.

After output, compute each menu model's exact likelihood of the observed
indicator pattern. Multiply the previous rows' integer likelihood weights by
these row numerators and normalize by their common gcd. Keep alpha=1/20 and
the uniform prior. Intersect the retained model set with
{k:100*weight_k >= sum_j weight_j}. Save every pattern and confidence-set
change; exact weights need only be checkpointed at powers of two and set
changes, because the receipt log reconstructs every update. Record integer
bit growth and hash the complete weight state. If the set becomes empty,
fall back to the whole source menu and label the performance confidence
failure; do not emit an unjustified narrower-model certificate.

The common likelihood event covers the true menu member over all request
boundaries. It does not establish menu adequacy. An outside-menu source can
remain close to a retained member, and a nonempty set is not evidence that
the family is correct. A separate future goodness-of-fit alternative would
need its own predictable likelihood and acquisition/inference bill.

## Cost reporting

Report physical audit count and fee separately. Record source, planning,
cross-model inference/checking, selection, receipt processing, action checking,
likelihood update and exported trace work in named units; retain exact trace
bytes and whole-arm CPU/wall resource observations. Integer-weight growth,
host/serialization work not captured by named units, code admission and
retention byte-time remain explicit duties. A physical-fee improvement alone
does not establish a complete economic win. Oracle parameters are diagnostic
free information, not learned performance. No promotion event is created.
