# S06/S08: learn proof-production effort from paid partial outcomes

Codex (GPT-6), October 11, 2026. DEVELOPMENT; no cost guarantee or promotion.

## 1. Why simple reordering is insufficient for the first bounded policy

Fix the prepared per-instance state and a deterministic bounded proof-search
recipe B. Let a_i(B)=1 exactly when that recipe produces an accepted proof on
instance i, and zero otherwise. This is an observable computational outcome,
not the mathematical truth y_i. Sound checking gives a_i(B)<=y_i. A bounded
positive-only sampling service can be viewed as conservatively observing this
proof-production population, while unproved truths remain possible.

If b+sum_i a_i(B)<T, a valid label-only lower-count test supplied only that
recipe cannot have high probability of warranting b+sum_i y_i>=T: its observed
one/unknown sequence is also compatible with the fixed truth population
y_i=a_i(B). On that comparison population the warrant would be false, so its
probability is at most alpha. This is an information-interface/power argument,
not a lower bound on arbitrary solvers that exploit additional formula
structure. It assumes each sampled instance follows the same fixed recipe;
adaptive budgets require the outer-set argument, not a fixed a(B) population.

Seven of eight n=100 bounded-statistical requests in proof_values01 reached a
complete first-pass prefix and then resumed computations. At the first resumed
observation, b+k was respectively 491,476,473,480,496,485,492, all below 512.
The preceding first-pass proof total was no larger. Thus their initial budget
had an observed proof-production ceiling below the target. A cost-based
reordering alone cannot turn that initial recipe into a reliable positive
warrant. More proof-production effort or additional sound information is
needed. The n=60 requests did not need a resumed round.

## 2. Paid pilot for a computation recipe, not free truth feedback

Use the first 16 uniformly selected instances as a pilot. On each, try the
nested recipes: 32 conflicts; then another 128; then another 512; then an
unbounded completed call if still needed. Retain each accepted proof forever.
An unsupported native negative may deprioritize further proposals, but it
remains unknown in the mathematical evidence count. Each recipe's measured
cost includes all earlier unsuccessful steps in its sequence. Do not report
the last call's time as the cost of the cumulative recipe.

The pilot supplies, for each recipe j, its accepted-proof fraction r_j and
mean cumulative elapsed cost c_j. These are paid computational observations.
They do not label every unresolved mathematical question or reveal the cost
of an unexecuted strategy. All pilot work contributes to the controller bill,
and its accepted witnesses remain usable in the final sampling prefix.

Let q=(T-b)/R be the required remaining-group proof fraction. A heuristic
score is KL(r_j||q)/c_j for r_j>q, and zero otherwise. It approximates
likelihood evidence growth per cost in a large-population binary model.
Use a small smoothing rule to avoid numerical boundary accidents; its
forecasting interpretation is revisable. Exact finite-population stopping
still uses the previously derived sound test. No iid truth assumption or
calibration guarantee is needed for the warrant itself.

Choose the highest pilot score and apply that cumulative recipe to later
uniformly drawn indices. If every score is zero, use the complete recipe.
If the chosen recipe exhausts the sample population without a warrant, a
separately charged complete-call fallback may deepen unresolved instances.
This can waste work if the pilot is unrepresentative. Compare the full-call
statistical rule and the bounded rule, and retain negative selection outcomes.
The identical ordinary metareasoning controller is an admissible comparison.

## 3. Why adaptive effort does not invalidate this lower warrant

The population and sampling permutation are fixed before adaptive effort
choices; any accepted proof count k is at most the prefix's actual true count.
At a fixed threshold, rejection is monotone in that count. Therefore every
wrong warrant by the adaptive producer also lies in the original full-label
test's wrong-warrant event. Choosing effort using the pilot, later proof
failures or measured costs cannot enlarge that event beyond alpha. It may
change cost and power. Each distinct source/request still follows its declared
stream risk allocation; later retargeting of the fixed test is not automatic.

## 4. Keep the margin-investment question separate

For future local edits, a stronger initial bound L can survive up to L-T
arbitrarily changed coordinates under uniform weights. Purchasing that margin
may cost much more than acquiring the immediate action. A cheap model may
forecast edit sizes and prices to select a prospective margin, but it cannot
guarantee that enough true positives exist to buy the proposed certificate.
Ordinary exact witness repair is the necessary comparator. The two-endpoint
censored confidence construction can support adaptive precision targets;
separately testing repeatedly chosen fixed thresholds cannot substitute for it.

Next implement this one pilot rule at the already exposed development scope,
including its complete failed-work bill. This is a constructive probe, not a
parameter search or independent confirmation.

## 5. First paid-pilot outcome

[proof_pilot01.json](proof_pilot01.json) preserves the single selected rule,
source closure, cumulative pilot profiles and 48 request units. All 48
returned warrants agree with the exposed reference values. For n=60, total
request times were 55.892 ms full, 72.025 ms bounded and 56.946 ms pilot. For
n=100 they were 151.427 ms full, 552.898 ms bounded and 207.570 ms pilot.
The pilot selected mainly the cumulative 128/512 recipes on n=100 and reduced
the weak bounded rule's cost substantially, but did **not** beat the direct
full-call control. It also paid more proof attempts: 978 versus 508 at n=100.

Native timings and some native-driven query paths varied across runs; arm
orders also differ across prototypes. Do not treat these repeated exposed
cohorts as clean replicates or stable timing estimates. The paid profiles
demonstrate an implementable, fallible computation-selection mechanism with
sound warrants. They do not establish an economic advantage over the strongest
observed ordinary rule. Deprioritize additional pilot tuning here.
