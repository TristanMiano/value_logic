# P3-08 ordinary controls and a more discriminating development family

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated ordinary-control reviewer,
October 10, 2026 UTC. **DEVELOPMENT proposal and same-model nonblind source
review.** No implementation, population generation, policy execution, final
freeze, commit or publication occurred in this review. Agent effort is
unmeasured and contributes **zero** additional principal-clock credit.

## 1. Recommendation

Use a small **bounded-CNF decision-program family** as a substantive new
development arm, while retaining the inherited Euler-table obstruction. The
public question is whether the fully specified finite search program returns
SAT on its input formula. The proposed scope is 4–16 variables, at most 64
clauses and at most four literals per clause. These are engineering starting
bounds, not final challenge choices or a claim that every admissible instance
is computationally difficult.

This family has three useful properties. Its mathematical answers are
deterministic; cheap syntactic evidence and general exact algorithms coexist;
and source edits support concrete, checkable reuse and invalidation cases.
There is no inherited 248-entry universal table. A declared finite development
pool still admits a pool-specific exact table, and that table must remain a
control if its construction is affordable. No unproved hardness premise is
needed for the comparison.

The ordinary combined method should share every useful component with the
candidate: exact shortcuts, paid computation, probability forecasts, blocked
online mixture, task-cost action choice, current hard state and dependency-aware
reuse. If these implementations coincide, their equality is the appropriate
result. The contribution hypothesis in problem-contract §10 permits a precise
interface or cross-component guarantee; it does not require manufactured
predictive superiority.

**Lower-engineering alternative:** use mixed bounded natural-register programs
already admitted by P3-03. Public countdown, parity and nested-loop templates
would require little new checking machinery. They also invite exact template
summarizers, which ordinary methods must receive. This alternative is good for
integration witnesses but weaker as a new comparative challenge. Merely
increasing the Euler modulus is also weak: efficient direct modular arithmetic
continues to be an obvious ordinary control even when a complete table grows.

## 2. Exact question and public information

The proposed query record contains the full clause list, variable count,
source version, semantics/checker version and unique request identifier.
Variable names and literal signs are public. Formula satisfaction means the
ordinary Boolean conjunction of disjunctions, including the explicit empty
formula/empty-clause boundary convention if those boundaries are admitted.

A reference program enumerates all assignments in a declared order, returns 1
when an assignment satisfies every clause, and returns 0 after the complete
finite enumeration if none does. This is a bounded finite program instance of
the L_math contract. Its full execution bound is part of the semantic bridge;
an agent budget that ends before completion does not make the answer false.
The bound can conservatively account for at most 2^n assignments and at most
the input literal count inspected per assignment, plus loop/control work.

Population construction must be specified without hidden controller advice.
Candidate public cohorts include short clauses, disconnected formulas, fixed
width clauses at several clause counts, and mixed clause widths. Random public
task selection leaves each formula's mathematical truth fixed. Do not quietly
condition generation on SAT/UNSAT balance and then give one method the generator
tag or seed. If a public construction deliberately guarantees a witness or
contradiction, its guarantee and the shortcut belong to every method.

Use at least a repeated-pool cohort and an unseen-formula cohort. The former
tests honest amortization and permits a cold exact table; the latter tests
whether a table built only from paid prior cases generalizes. A stream order,
hash, identifier or program template that encodes the answer is public advice,
not evidence of learning. Formula and method source bytes should be registered
before each development run; all later edits require new version labels.

## 3. Ordinary exact and analytic controls

The following are a credible minimum portfolio, subject to the actual selected
family. Their costs must be counted using common primitives.

| Ordinary component | Information/service | Required cost or boundary |
|---|---|---|
| Direct complete enumeration | Exact SAT/UNSAT answer | Formula reads, assignment/literal work, stopping, output; a premature stop is unresolved |
| Unit propagation and contradictory-unit check | Sound deductions or a sound contradiction | Clause scans and the retained assignment; an unresolved propagation result is not a false label |
| Pure-literal elimination | Satisfiability-preserving simplification | Scan and transformation costs; retained proof/scope if used as hard evidence |
| Connected-component factorization | Independent subproblem reduction | Graph construction, component identity and solving/checking every necessary component |
| DPLL with a public branch rule | General complete exact method | All visited branches and simplification work, including failed search |
| Exact formula cache | Current previously solved formulas | Cold acquisition once, canonicalization, key comparisons, eviction, storage and lookup |
| Component cache | Previously solved repeated components | Paid factorization and exact component identity; no free symbolic equivalence oracle |
| Cold finite-pool table | All formulas in a known pool | Full construction, binding, retention and lookup under an announced reuse horizon |
| Fixed visible-feature forecasts | Cheap fallible prior/model | Feature extraction and supplied/learned parameter acquisition; same library for both sides |

Further ordinary solvers are allowed. A conventional optimized library solver
would be an especially strong implementation control if available, but its
opaque physical runtime should not silently share a primitive-count scale
defined for a hand-coded interpreter. Report it under a separate measured-time
comparison or instrument a declared equivalent cost interface. Absence of such
a library does not license a claim about the best possible ordinary solver.

A formula with many independent components can look expensive to naive
enumeration and cheap to factorization. Likewise, a large formula with an
obvious contradictory unit pair is easy. These cases must be identified rather
than used as apparent forecast victories over a deliberately naive exact
baseline. A complete shortcut sweep on every known template is the first useful
family audit. If it removes all meaningful uncertainty at lower cost, retain
that negative result and use the family only for integration.

## 4. Common output and resource service

The primary endpoint should be **terminal decision plus immutable issued
forecast**, with a separate current hard-answer record. The checker here is an
internal trusted service. It does not implicitly select optional recurrence B
or require independently exported certificates for every method.

Every arm receives the same full public query and may invoke the same exact
services before issuing its report or after issuance at the declared feedback
time. Purchased answers alone may enter a selected-feedback learner. A forecast
can be fallible; a reported hard true/false coordinate must have completed its
declared check. A true witness can be checked by evaluating every clause under
that assignment. A false claim needs complete search evidence or an independent
complete check; failure to find a witness within budget is insufficient. A new
checker/receipt scheme requires its own source-versioned correctness argument.

To avoid a service mismatch, do not charge one method for redundant independent
checking while allowing another to claim the same hard-evidence service using
unpaid trust. Either share the same checked operations or explicitly separate a
trusted terminal-only comparator from a stronger evidence-delivery endpoint.
When all methods use the same internal trusted implementation, it may be shared
and charged identically. Expensive proof export is not required by this
proposal.

Record resource vectors for input reads, integer/bit operations, solving,
checking, acquisition, forecasts, mixture arithmetic, selection, dependency
search, retention, lookup and output. Variable-size bitsets must pay for their
word length. Whole-formula canonicalization and hashing are not constant-time
metadata. File serialization for private audit can remain evaluator-only if
no policy reads its contents and it is excluded on both sides. Store peak
retained bytes and numeric operand bounds separately from transaction counts.

The source registry, model library and cache begin from the same declared
initial state. Cold cost and warm cost are separate comparisons. Acquisitions
used to train a model or populate a table are paid once and amortized over the
same horizon. They cannot be charged every time to the ordinary method, waived
only for the candidate or moved into a free feature extractor.

## 5. Matched methods and discriminating comparisons

The candidate and O-COMB may share a single correct mechanism with distinct
representation/readout wrappers. A useful explicit comparison is a probability
state q versus the exact known-loss pair

~~~text
cost(guess 0) = false_negative_price * q
cost(guess 1) = false_positive_price * (1-q).
~~~

With the same q, prices, tie rule and resource schedule, these actions must
coincide. A retained direct cost at one price does not automatically answer a
new-stakes query unless its encoding permits the needed recovery. Keep that
information issue separate from any learning effect.

Recommended distinct arms are:

1. Proof/evaluation only with sound timeout and the common fallback.
2. Fixed ordinary forecasts with expected task-cost action choice.
3. Ordinary finite blocked predictor mixture with actual paid feedback.
4. Integrated candidate with a separately bound current hard state.
5. O-COMB with exactly those capabilities plus the strongest implemented
   exact/cache portfolio.
6. Charged exact computation, including the cheapest implemented shortcut path.
7. A visibly labeled free oracle used only as an unattainable diagnostic.

The report should answer specific mechanism questions:

| Comparison | What it can establish |
|---|---|
| Mixture versus each fixed public expert and constant-half forecast | Whether purchased feedback improves issued forecasts on this cohort |
| Candidate versus O-COMB | Distinct behavior/cost or an exact reconstruction/equality result |
| Forecast-action method versus charged exact | Whether residual error reduction repays additional computation under declared prices |
| With and without a current hard overlay | Pointwise terminal-error improvement and its additional bill, with the base purchase/update path held fixed |
| Cold versus warm, repeated versus unseen formulas | Actual amortization and cache reuse, without conflating prior label exposure with generalization |
| Direct cost versus coherent probability under changed prices | The retained representation's actual query service |
| Version-aware versus deliberately stale cache diagnostic | Why source identity matters; the stale arm is an invalidity witness, not the principal ordinary comparator |
| Learned versus explicitly supplied analytic profile | Whether learning acquisition is necessary, provided both have the same public law and shortcuts |

Sweep a modest declared development grid of resource prices, asymmetric error
prices and hard budgets. Save task loss and resource vectors before adding
prices. A replay under new prices is valid only when the actual policy path is
unchanged; a new price that changes acquisition/selection requires a new labeled
development execution. A retrospectively best fixed method and a best-instance
oracle are analysis comparators, not deployable O-COMB selectors.

For example, a successful cheap forecast is useful only when its expected error
cost plus its acquisition/forecast expense beats the exact alternative. The
simple decision inequality does not supply its own conditional error law.
Report whether the law was supplied, learned from paid labels or only estimated
after private scoring. If constant-half or a cheap structural rule is as good,
the result does not support a special fallible-model benefit.

## 6. Version and edit comparisons

A source-version edit can change a label while leaving a request's printed
identifier unchanged. Full claim identity must include the actual formula and
semantic version; request identity additionally binds the delivery event.
Changing only the task prices leaves mathematical truth intact but invalidates
old price-specific action warrants. Previously issued reports remain historical
reports with their original prices and meaning.

Ordinary reuse need not discard everything after an edit. A checked satisfying
assignment remains a witness after clause deletion. After clause addition, it
can be rechecked against the added clauses. A proved UNSAT formula stays UNSAT
after adding clauses; deleting clauses need not preserve UNSAT. These facts
support cheap sound transfer when their exact hypotheses are checked and paid.
Candidate and ordinary controls receive the same transfer rules. Clause
reordering/duplicate removal can preserve semantics with paid normalization;
changing a literal's sign generally cannot reuse a cached scalar answer without
new evidence.

For the accepted selective-feedback theorem, an exogenous version schedule is
compatible with a fixed tape of versioned questions. A theorem about learning
under one stable population law does not automatically imply predictive quality
after a distribution change. Existing predictor weights may be retained as
fallible state under an explicit rule, but a stale exact coordinate is never
made current merely because its probability is high.

## 7. Reuse of existing APIs and concrete integration risks

| Source API | What can be reused | Boundary |
|---|---|---|
| P3-03 Kernel | Finite source cover, distinct true/false/unresolved states, withdrawal, objective versioning and nonempty-source rules | Its executable grammar is nat-register-v1; an opaque CNF atom is not automatically backed by a checked SAT solver |
| P3-03 TaskCertificate | Named-action catalogue and exact binding of query, loss, tolerance and unit | Changing a query or catalogue requires a new request; report currency is not arbitrary JSON authentication |
| P3-06 Evidence | Register/prepare/admit separation, retained current answers, immutable issued event identities | Its Query, residue semantics and receipt checks are modular-specific; its audit counters are not a new complete common tariff |
| P3-07 computation Adapter/Meter | Paid primitive admission, solve/check/acquire, actual failed spending, bounded jobs/cache and scoped keys | Input caps, key structure and completion caps are modular-specific |
| P3-07 FrozenProd/AllocatedProd | Finite blocked update, exact finite action randomness, meter/reservation mechanics and actual-selector binding | Current receipt type/provider checks explicitly require the Euler modular service; a new family is a new version, not an unnoticed monkey-patch |
| P3-07 ServiceResult/ResourceRecord pattern | Immutable answer/status/provider/resource payload, common invoice absorption | Type/identity equality only authenticates the trusted local broker; external hostile receipt authentication is outside scope |

The minimum new query API needs query_id, claim_key and key_words. The receipt
needs query_id, claim_key, answer, checked, status, provider/provider_version and
an immutable resource record. The broker must reserve the announced worst-case
cap before executing a child operation, absorb failed as well as successful
charges, and disclose no answer before successful checking/acquisition. The
allocation path must bind the actual selection probability, not an arbitrary
caller-provided number.

Reusing P3-07's blocked theorem also retains fixed exogenous queries, fixed
within-block expert advice, the specified prospective action randomization and
the exact checked-feedback quota. A hard overlay may correct terminal actions
by pointwise domination with unchanged base purchases/updates. Updating later
within-block forecasts from the first bought answer needs the separately
accepted predictable construction; the old theorem does not transfer simply
because the result looks better. Failed receipts must suspend the successful
purchase guarantee while preserving actual costs and explicit unresolved
outcomes.

## 8. Disposition

This report proposes a stronger family and exposes implementation risks; it
does not certify an implementation or choose the P3-09 final challenge. The
first decisive experiment is a tiny public shortcut audit with exact/cache
controls and genuine failure/version witnesses. A positive learner result,
negative result or complete O-COMB equality are all acceptable evidence. The
same-source Euler obstruction should remain visible as an inherited adverse
result, regardless of the new development family's outcome.

## Source hashes inspected

SHA-256 values bind the sources reviewed here, before later P3-08 changes.

| Repository-relative source | SHA-256 |
|---|---|
| v3/RESEARCH_PROTOCOL.md | ef57593ce23cbe06b1683fc3609526f700b6ab5c395befacbbcd01bd48f3aa52 |
| v3/work_logs/P3_08_2026-10-10_S1/forecast.json | cce049260f0d9245ffa211403b1d57397794510d849456459b4930e02ed3bd3a |
| v3/foundations/01_problem_contract.md | e67905f9d182abcc52bd2cbdc5d6817208201e2b8a89ac074450600994ffe4c7 |
| v3/checkpoints/B_1_R_P3_B_A.md | 4425c19ad9f64dbdee2b6cff4307594472c22534c20e26dcb4c2bdb26e19c2c9 |
| v3/checks/03_bounded_logic.py | 841df6c5223844d2131642adcbb136855e054aa8833036506bb32c91aaf8afe6 |
| v3/checks/03_task_certificate.py | 5e7d7d669f4243dac0a0df77e429b86ac2439b7351dab70965702ccdc71b1e15 |
| v3/checks/06_mathematical_forecast_development.py | 7e19e1e0930cbcdea3637af16c1ade4e1f2099b615a3600821196c2c8c5cecd4 |
| v3/checks/07_computation_adapter.py | 06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615 |
| v3/checks/07_selective_feedback.py | f872ec2eb07df4722720763730932c33055e380f0ab76ddc3c848d79a5e70f48 |
| v3/checks/07_selective_feedback_allocation.py | eaf79ecb0c4b297ffeec3de4026a025fabc23058ec3c119abe5fdd23434da070 |
| v3/checks/07_selective_feedback_service.py | 68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32 |
| v3/derivations/07_ordinary_analytic_profile.md | 46db6cb249c5e0bb0066685c438132a1bfcf7551d834612cc752a8239e90cfb7 |
