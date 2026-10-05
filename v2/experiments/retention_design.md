# F14 retention implementation and design notes

Contributor: **GPT-6 Astra Pro, retention sub-agent**, October 4, 2026.
Status: development design and implementation notes. The root
[`protocol.md`](protocol.md) and its frozen configuration govern final execution;
these notes do not independently authorize F15 or establish final outcomes.
No evaluation seed has been generated or evaluated by this contributor.

## 1. The bounded question

For three fixed reset procedures, which information is sufficient after a
declared revision to recover individual mean costs, admit a useful numerical
approximation, choose a low-regret action, and receive a proof for the actual
current request? What do storage, production, ordinary solving, proof checking,
and authorized source repair cost in this finite model?

The source is an arbitrary exact probability law on the eight Boolean failure
worlds. Every old procedure order uses all three procedures, stops after the
first success, and pays terminal penalty 4 if all fail. Old attempt prices are
(1,1,1). The actual fixed reset behavior is connected to the existing
`case_cascade` bounded native attempts in a permanent development test; their
statuses generate exactly these Boolean masks. The price parameters are
declared loss charges, not measurements of Python time or proof-node costs.
The generated law is a stipulated finite population, not a calibrated estimate
of a deployed workload.

The cost vector for each order comes from the independent path interpreter
`case_reference.execute`. A separate test compares its expectation with
`case_cascade.compiled_cost` in moment coordinates. No new native rule, source
meaning, stochastic estimator, or stateful search behavior is introduced.

## 2. Generator and revision strata

`generate_case(seed, variant, config)` uses a local `random.Random` instance
initialized by the versioned string `F14-retention-v1:<seed>`. It draws eight
integer weights uniformly from 1 through 17 and normalizes them exactly.
Every generated law has full support. The same initial law is used across all
revision strata for a seed; source drift uses the next eight draws for its new
scoring law. The output's seed and scoring law belong to the evaluation
harness, not the retained-data decoder.

| Stratum | Current request/source change |
|---|---|
| unchanged | Old prices, penalty and six full orders |
| small_price | Last attempt price rises by 1/40 |
| small_negative_price | Last attempt price falls by 1/40 |
| large_price | Last attempt price rises by 1 |
| large_negative_price | Last attempt price falls by 1/2 |
| proportional | Every attempt price and terminal penalty doubles |
| program_edit | The admissible programs are the six ordered pairs; stop after two attempts |
| known_marginals | Old request plus all three exact current one-coordinate failure probabilities |
| withdrawal | Old facts lose current authority; actual law remains the old law |
| source_drift | Old facts lose current authority and the scoring law changes |

The fallback is a deterministic action of cost 5/2, available to every method.
All current attempt prices remain strictly positive. In withdrawal and drift,
**every method** loses authority to use the old source facts, including methods
that retained the complete old table. Without repair, the current admitted
source is the whole probability simplex. The old proof can remain a sound
theorem of its old source while failing current reception.

Development seeds are 14101 and 14102. The final seed count and evaluation
seeds are supplied only by the root freeze. All F01–C4 examples and all explicit
point, uniform-law, unit-gap, and hostile-receiver fixtures stay permanent
development material. A finite seed list is a sampling plan, not a restricted
source hypothesis class: methods may not enumerate known generator seeds to
recover discarded information. Native source revision labels contain no
generator seed. They are binding metadata, not extra measurements.

## 3. Serious ordinary controls and their information

All methods initially receive the same exact old table. Each independently
produces and pays for its chosen retained representation.

| Method | Retained numerical coordinates | Independent affine information | Current ordinary path |
|---|---:|---:|---|
| fresh | Eight world probabilities | 7 | Direct weighted-world calculation; no LP |
| cached_proof | Same eight probabilities plus an old current-bound proof and its complete source context | 7 | Try old reception; use the same direct ordinary source path and replacement production if needed |
| full_joint | All seven nonempty failure moments | 7 | Boolean moment inversion, then direct weighted-world calculation |
| tailored | One base old mean plus four canonical residuals | 5 | Recover the old mean profile and optimize its compatible-law fiber |
| exact_intervals | All six old order means | 5 | Optimize exactly the same compatible-law fiber as tailored |
| marginal_diagnostic | Three one-procedure failure probabilities | 3 | Optimize the larger compatible-law fiber; explicitly a weaker-information diagnostic |

Before the first freeze, the retained wire format was revised to
**`F14-retained-v2`**. The tailored payload is the fixed five-value array
`[B, r_(1), r_(2), r_(0,2), r_(1,2)]`. Its four residual subset labels are public
schema metadata rather than repeated data fields. The public schema also
declares the full-joint moment order, marginal order, worlds and old orders,
and its bytes are charged identically to every method. This removes avoidable
format overhead from the tailored storage control while preserving all
measurements, equations and repair behavior. The old development artifacts
remain unchanged and do not supply final wire-v2 storage or timing evidence;
the generator, seeds and numerical cutoffs are unchanged. Old wire-v1 payloads
are rejected rather than silently decoded under the new layout.

The cached initial proof targets the old selected order when an order is
selected. It is not assumed to survive a changed query, source, or program.
The complete old context is counted alongside the proof. Neither source
inspection nor a source-backed native proof is free.

`fresh`, `cached_proof`, and `full_joint` use `Fiber.point`: exact direct dot
products on the known law, with decision regret equal to each action's cost
minus the minimum. They do not perform pointless vertex enumeration. The
ordinary numeric path is timed separately from the optional common native
receipt wrapper, so the wrapper cannot hide the strength of a direct solver.

The five-versus-six coordinate distinction is not a claim about encoded-byte
savings. Rational numerators, denominators, field names, provenance, and source
contexts all appear in the separately measured byte counts. Likewise, seven
independent law coordinates and eight transmitted probability fields are
different quantities.

## 4. Exact intervals and coherent action choice

For a retained source, write

    P = {p >= 0 : A p = b, sum(p) = 1}.

`Fiber` reduces these equalities by rational elimination, then enumerates
basic feasible solutions. At eight worlds, at most C(8,4)=70 candidate bases
are needed. Bounds are the exact minima and maxima of the requested pathwise
cost vector over these vertices. Every upper bound also has an ordinary dual
certificate; primal and dual agreement is checked exactly.

The numerical tolerance is **tau=1/20** declared cost units. An interval [l,u]
is exact when l=u. Its midpoint is an admitted approximation only when
u-l<=2 tau; otherwise the method refuses that numerical answer. Individual
midpoints are not represented as a jointly realizable probability law.

Action choice uses the entire same-law fiber, not arithmetic on independent
interval endpoints. For the six current orders and fallback, compute

    rho(a) = max_b max_(p in P) [C_a(p) - C_b(p)].

Choose the smallest rho, then the smallest upper absolute mean, then the
declared order index. If rho<=**epsilon=1/20**, the action is admitted. A
selected fallback can therefore be a certified fallback. If the smallest rho
exceeds epsilon, the method explicitly refuses and actually executes the
fallback. This second outcome is `refusal_to_fallback`, earns no useful-choice
credit, and still incurs fallback cost and its realized regret. Exact scoring
under the hidden law checks every numerical admission and useful decision.

The small edit of 1/40 is chosen prospectively because the C4 bound makes
small one-price changes compatible with low decision regret despite exact
information loss. Large edits and the program change challenge that account.
No positive empirical rate is obtained by adjusting these cutoffs after
evaluation.

## 5. Equal acquisition capabilities and useful repair

Two access panels are frozen:

1. **No reacquisition.** The decoder gets only the retained payload, current
   public query metadata, and newly declared source facts. It never receives
   the original or current scoring law.
2. **Adaptive reacquisition.** Every method has the same authorized source
   archive capability. It first performs the same retained-data calculation.
   It asks for source information only if any requested numerical answer is
   refused or the decision is refused. This preliminary computation is charged.

On a stable one-price edit, a retained complete old mean profile can acquire
the two actual current order means for (0,2,1) and (0,1,2). The C4 constructive
repair recovers all moments from those two means and the old summary.
`exact_intervals` obtains the canonical minimal summary from a vertex derived
from its retained equations; it does not inspect the scoring law. Independent
generic elimination on the old and new observation equations is tested to
produce the identical singleton law.

Other failed admissions use a full eight-field law response. Source withdrawal
or drift always requires current information; the old two-mean repair is not
used after its old-law premise loses authority. The known-marginal stratum
keeps old prices, so the complete old profiles already answer the requested
means exactly and acquire nothing. There is no claim that this policy solves
the general optimal experimental-design problem, or that two measurements
are always minimal when additional lower-order moments are already known.

The archive stores the full current source and is charged even when a method
makes zero queries. Both full and mean-query capabilities exist for every
method. The full response transmits eight scalar fields; the two-mean response
transmits two scalar values plus its order/price metadata. Eight is a wire
convention, not an information lower bound: an optimized full-law encoding
could omit one normalized coordinate. Source production for the two means
actually executes the path interpreter on 16 world/order pairs and is timed.

Sensitivity prices **0, 1/20, 1/2 per exact scalar measurement** are synthetic
decision-cost scenarios. Record API query count, scalar count, transferred
bytes, source path executions, archive storage and measured production time
separately. These prices do not convert nanoseconds or storage bytes into loss.
The common initial eight-field source input is charged once; the
known-marginal stratum also charges its three newly delivered exact scalars
equally to every method. The sensitivity output exposes common initial,
common current and method-specific source charges separately.
The fixed admission-then-repair policy is not asserted to be utility-optimal
at every sensitivity price.

## 6. Native validity, availability, reception and usefulness

The adapter uses only the existing K row, nonnegative scale, addition,
constant, declared conversion, rewrite and all-cases constructors. It translates an ordinary exact
dual certificate into a native proof. Its source-context witness is a canonical
fiber vertex computed from the retained information, never the hidden scoring
law. Probability coordinates carry source unit P; the declared positive
`probability_to_declared_loss` conversion maps P to U with factor one after the
known numeric task-cost coefficients are combined. This makes the normalization
per declared loss unit explicit; it changes no calculus rule. The maximum
emitted proof size is 128 steps. A bound that exceeds the
requested budget is checked as the weaker theorem it actually proves and
reported as insufficient for the current request.

When the decision selects and executes an admitted order, the native request
is that order's expected cost minus fallback cost, with budget zero. A useful
derivation candidate must concern an actual price/program revision, receive a
current proof with upper bound at most -1/20, use at least two distinct nonzero
source-row premises, and concern this selected order. Unchanged and merely
proportionally rescaled old means cannot meet that extra contribution-facing
criterion. For certified fallback or refusal, a fixed first-order comparison
is retained only as a validity/reception diagnostic and never earns useful
derivation credit.

The frozen application criterion additionally requires a useful
no-reacquisition `tailored` or `exact_intervals` row whose selected numerical
answer is **approximate**. A multiple-vertex law fiber alone is insufficient:
putting the price-edited procedure first can give a known constant offset of
an old mean, leaving that selected cost exact despite uncertainty elsewhere.
The additional condition requires a nonzero conditional interval for the
executed order while its regret and received fallback-improvement bounds
remain admitted. It does not imply that a strong ordinary perturbation bound
could not establish the same result.

This native comparison establishes improvement against fallback. The stronger
all-alternative regret criterion comes from the independently stated ordinary
fiber calculation; a single fallback proof is not described as a proof of
global optimality. The hidden-law scoring oracle also has no native proof and
is labeled as a different-information reference where appropriate.
Each method row separately records the same candidate comparison's value and
validity under the exact stipulated current scoring law
(`scoring.full_source_semantic_valid`) and its robust validity over the actual
retained or repaired information fiber (`native.semantic_valid`, with an
explicit scope label). The former is not silently supplied to a restricted
solver or substituted for current receipt.

Permanent development sentinels distinguish three additional boundaries:

- A valid old proof fails a changed source revision or changed current pair.
- A zero producer-output budget can leave a semantically valid request without
  an available emitted proof.
- In the directed-unit fixture, a foreign audit-unit row makes the full-source
  maximum zero, while the target-unit reduct still permits maximum one. This
  uses the already established F08 interpretation; it is not a new kernel
  incompleteness claim or an evaluation fixture.

## 7. Resources, comparisons and interpretation

Assessment output `f14-retention-assessment-v2` attaches a complete quality
vector to each method/fresh resource comparison: all six intervals,
dispositions, estimates and actual errors; certified/refused decision,
selected/executed indices, coherent and actual regret; and the native
candidate, semantic bounds and receipt status. Literal quality equality may
include two refusals. It is therefore separate from the flags requiring all
numerical answers and both ordinary decisions to be admitted, or additionally
requiring a received selected-order proof. Certified fallback is an admitted
ordinary decision; its diagnostic alternative-order proof is not relabeled a
proof about an executed order. There is no aggregate quality score that hides
precision differences or forgone answers.

Within every case and access panel, assessment requires equal exact numerical
outputs, deterministic decisions/coherent regret, native semantic target and
fixed-policy acquisition output from `fresh`, `full_joint` and `cached_proof`.
The same requirement separately applies to `tailored` and `exact_intervals`.
This checks the two declared information-equivalence classes, not all arms
indiscriminately. Native receipt equality is reported separately: equal
information need not imply equal proof availability under a producer budget.
Proof bytes, premise counts, cache behavior and measured computation can differ.
The guard is a consistency check between controls, not an independent proof of
their shared numerical correctness; the separate exact/moment tests and
ordinary reference challenge supply additional evidence.

Disjoint timing stages include initial retained-payload production and
serialization, cached initial source/proof production and checking, source
archive production, acquisition, source update and arithmetic solving,
decision calculation, current source-context production/serialization, and the
entire native request/production/checking/serialization path. The latter also
has diagnostic internal stage timers, which are not added a second time.
Scoring, report writing and benchmark-case generation are outside method timing.
`run_generated_case(seed, variant, config)` separately measures the common
generator/source-input production and serialization, including the exact new
marginal facts and query metadata. It records those input bytes and charges
this common production equally to every arm. Method-plus-common totals and
the peak initial state while the full source is supplied are also reported.
For `run_case` invoked with an already supplied fixture, unobserved generation
time remains `None`; it is not guessed or recorded as a measured zero.
The common generator measures synthetic input construction, not real sampling
or a deployed workload-estimation process.

Reported storage includes retained payload, cached source and proof, active
current source and proof, current update metadata, public schema and external
archive. `resident_bytes` explicitly means the durable initial cache;
`active_serialized_upper_bytes` and `total_stored_serialized_upper_bytes`
include current components and possible duplicated encodings. These are
serialized-size measures, not Python RSS. Basis/vertex counts, inverse matrix
sizes, source row counts and probability-coordinate counts provide bounded
transient-work measures.

For horizons 1,4,16,64 the implementation reports the algebraic model

    T(h) = measured initial production + h * measured one-update cost.

The break-even field solves the strict inequality against fresh solving in
that model. This is **not observed repeated-update performance**. In particular,
a real adaptive cache might retain a replacement proof after its first update;
the one-event model does not establish its later behavior. Native-inclusive and
arithmetic-only projections remain separate. F15 must not turn a projected
crossing or a one-event wall-time difference into a general speed claim.

Positive results can support a bounded integration/application contribution:
valid current reception, informative conditional intervals, useful changed
decisions, and charged repair of the declared lost information. Strong ordinary
controls can match every conclusion. Failure to beat them in speed or bytes
does not by itself defeat the methodological synthesis. False admission, stale
premises, a free hidden-source read, incoherent regret, or failure to charge
repair would displace the claimed integration. Finite generated checks do not
establish universal theorems or worldwide priority; the scoped C4 contribution
assessment and F16 reconstruction remain separate.

## 8. Development evidence and auxiliary timing

The source files are `retention.py`,
`verification/test_v2_f14_retention.py`, and the result-contract tests in
`verification/test_v2_f14_retention_contract.py`. Focused tests cover the exact path/moment
bridge, full-information direct controls, matching minimal/redundant fibers,
C4 specialized interval agreement, primal/dual/native agreement, coherent
regret, source-capability poisoning, withdrawal, adaptive zero-query sufficiency,
two-mean repair without a full-law read, resource accounting and receiver
sentinels. The root work log owns the final combined run and frozen evidence.

The auxiliary pre-wire-v2 [development run](../work_logs/F14_2026-10-04_S1/retention_agent/f14_retention_development_v2.json)
and [assessment](../work_logs/F14_2026-10-04_S1/retention_agent/f14_retention_assessment_v2.json)
contain 20 cases and 240 method rows. Numerical dispositions were 1,072 exact,
88 approximate and 280 refused. Decisions were 165 certified orders,
35 certified fallbacks and 40 refusals to fallback. There were 165 current
native receipts, 75 insufficient bounds and 27 rows where exact full-law truth
was valid but retained-fiber validity did not hold. The application-facing
criterion was exercised on nine distinct development cases across both seeds;
it remains formally false as a final-evaluation conclusion because these are
development data. Six rows used the two-mean repair, 44 used an eight-scalar
full response, and 190 made no source query. This run plus assessment and
sentinels took 23.084 measured seconds.
Its unchanged numerical records contain four useful no-reacquisition
selective rows with an approximate selected cost: development seed 14102's
small positive and negative price edits under both `tailored` and
`exact_intervals`. The wire-format revision changes their serialized storage
accounting, not their numerical information or conclusions.

Earlier auxiliary runs are preserved in the root's
`v2/work_logs/F14_2026-10-04_S1/retention_agent/` record:
an initial subset smoke omitted the `fresh` baseline and exposed a deterministic
`StopIteration` in the comparison reporter; the subset reporter was corrected.
The first complete development run had 20 cases and 240 method records and
took 14.136 seconds, before adaptive repair and complete timing accounting were
added. Its correctness checks remain development evidence; its method timing
is superseded. Subsequent focused runs passed 13 tests in 0.977 seconds and
15 tests in 1.113 seconds. The final root run supersedes these counts after the
additional reset-execution bridge and common-accounting tests. The latest
auxiliary focused run passed 17 tests in 1.442 seconds.
After the typed P-to-U adapter change, 17 tests passed in 1.770 seconds.
The result-contract challenge then exposed five deterministic validation gaps
in the initial assessment: unchecked truth flags, negative/understated coherent
regret, duplicated numerical query identities and an unbound selected index.
The principal corrected those checks; all 29 retention and contract tests then
passed together in 8.134 seconds. The failed challenge log is preserved and
is not characterized as a native crash or an unexplained host failure.
After the wire-v2 revision, 30 core/contract tests passed in 8.371 seconds.
A focused regression then distinguishes the exact selected-cost,
multiple-vertex development counterexample from the approximate selected-cost
witness; all 31 core/contract tests passed in 7.809 seconds.
The ordinary-control assessment challenge subsequently widened one reported
exact interval conservatively while preserving its midpoint, error,
disposition and decision. This exposed a missing control-equivalence guard:
the initial targeted contract failed because assessment admitted the mutant.
After adding the explicit quality vectors and equivalence checks, all 32
core/contract tests passed in 8.239 seconds. Reassessing the existing 20-case
development records checked 120 information-equivalent control pairs;
arithmetic, decision, acquisition and native semantic targets agreed in all
120, as did separately reported native receipt statuses. No new source cases
were generated for that reassessment, and its old storage/timing records were
not promoted to wire-v2 evidence.

The sub-agent did not establish an independent engaged-time timer at entry and
does **not** claim any additional D/L/E minutes toward the principal floor.
The first observed auxiliary UTC clock was 2026-10-04 23:19:16; a later observed
clock was 23:41:41. This is an observation span, not an engaged-time estimate.
All sub-agent work overlaps the principal task and must not be added to its
POST-B-1 clock. Test wall times above are measured execution times only.

### Local references

- [C4 price-revision derivation](../derivations/09_c4_price_revision.md), especially
  sections 1–6 and the known-marginal restrictions in section 8.
- [C4 contribution selection](../contribution_review.md#6-selected-next-work-f14-not-another-unrestricted-n01-loop).
- [F13 case-study derivation](../derivations/06_case_studies.md).
- [F14 task obligations](../../TODO_v2.md).
