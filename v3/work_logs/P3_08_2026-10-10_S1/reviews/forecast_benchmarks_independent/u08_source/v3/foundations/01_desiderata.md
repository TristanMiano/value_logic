# P3-01 — exact duties and comparison matrix

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: **prospective comparison contract**, not a list of guarantees already
obtained. Read the [problem contract](01_problem_contract.md) first.

All statements below quantify over the declared fragment, versions, budgets and
feedback process. “Finite diagnostic” and “theorem target” are distinct evidence
types. The final challenge's families, numerical thresholds and statistical
analysis belong to P3-09; none are frozen by these development examples.

Cited theorems describe their source systems under their stated hypotheses.
This table does not instantiate those systems or transfer their guarantees to
the candidate. A later claim must identify its actual algorithm, encoding,
information/feedback process and the proof or reduction licensing the import.

## 1. Common notation

- `phi_t` is a query issued before its own new feedback; `y_t` is its eventual
  Boolean answer if available in the fixed interpretation.
- `p_t` is an explicitly labeled forecast, not truth or a proof-status code.
- `C_t` contains only constraints actually received/checked for the current
  version. `W_t` is the finite set of bit assignments satisfying the selected
  Boolean fragment of those constraints, if fully constructed.
- `ell_t(a)` is realized task loss; `L_t(a)` is the declared expected/robust
  cost functional; `Lhat_t(a)` is its estimate. These need not be identical.
- `g_t(i)` is the revealed bounded scoring loss of expert `i`; `r_t` records
  resource use. `tau_t` is a feedback time, not a theory version in this file.
- A comparison must fix whether its regret benchmark is the best fixed expert,
  a fixed decision, an adaptive policy with the same observations, or an oracle.
  These benchmarks are not interchangeable.

## 2. Duties

| ID / questions | Operational duty or precise target | Strong comparison / exact source locator | Present disposition and decisive failure witness |
|---|---|---|---|
| U01 / Q1 | Every state update and output is produced by a specified computation using only admitted information and budget. A finite active domain/default policy is declared. | O-PROOF/O-FINITE; S01 §§3.1–3.3; S11 §§5,7; S12 §§2–3 | **Required interface.** An output dependent on a not-yet-revealed label or free full-theory consistency oracle fails it. |
| U02 / Q1 | Preserve separate statuses for accepted theory-conditional proof/refutation, interpreted answer under its soundness/execution bridge, pending/no result, execution failure, conflict and stale scope. | O-PROOF; inherited current-request checking | **Required interface.** An unresolved true/false pair must not both become “false.” EX01. |
| U03 / Q1,Q4 | On a fully enumerated finite fragment, a probability/expectation state respects every selected Boolean constraint actually represented in that fragment; for example a represented `phi -> psi` entails `p(phi) <= p(psi)`. | O-FINITE/O-PROB; S01 §4.5; S13 Theorems 2.2/2.4 and §3.2 for the expectation type | **Finite conditional reconstruction** in EX01. Distinguish linear, lower/upper and merely learned functionals; arbitrary lower/upper costs are not additive. No unprocessed arithmetic closure follows. An uncharged enumeration or ignored constraint within the claimed scope invalidates the claim. |
| U04 / Q1,Q4 | A newly received, version-matched Boolean answer under the applicable soundness/execution bridge fixes that query's truth coordinate at the next eligible update. Dependent estimates are recomputed or explicitly marked stale. | O-PROOF + ordinary dependency tracking | **Required interface.** Retaining a contradictory active bound after accepted resolution fails it; a proof in an unsound alternative theory does not settle interpreted truth. This is a hard-evidence interface requirement, not an exact finite-time LI property. Old forecasts remain immutable for scoring. |
| U05 / Q1,Q4 | If a pointwise convergence claim is made, state which fixed queries converge and under which stream. If eventual correctness is claimed, state the needed resolution/soundness assumptions. | S01 Theorems 4.1.1–2 and 4.2.1 | **Later theorem target, not imported.** A stationary but incorrect forecast, or a stream of fresh unresolved queries, defeats careless inference from convergence to learning. |
| U06 / Q1,Q4 | On a declared recurring family, evaluate forecasts made before individual resolution; charge any shortcut used to recognize the pattern. | O-ONLINE; S01 Theorem 4.2.1 as the stronger theoretical comparator | **Later restricted target.** Memorizing a label after receipt does not establish anticipatory learning; no efficient shortcut is withheld from the ordinary method. |
| U07 / Q4 | If calibration is claimed, specify the bin/selection/weighting rule and show the corresponding resolved-frequency or weighted signed-error statement. | S02; S01 Theorems 4.3.3, 4.3.8; exact schemas in the import audit §4 | **Separate target.** LI's recurring result is a limit-point statement; the selected feedback theorem gives convergence with additional family, weighting/divergence and deferral/timely-feedback hypotheses. Neither follows from a finite cohort statistic or weak-expert regret. EX08. Never score unresolved labels as zero. |
| U08 / Q4 | For full feedback and `g_t(i)` in `[0,1]`, compare cumulative predictive loss with `min_i sum_t g_t(i)` over the same fixed expert set. Name the mixture/update, scored output, adaptation and timing assumptions. | O-ONLINE; S10 §2, Figure 1, Theorem 2/Corollary 3 | **Comparator contract.** A different output needs its own loss bridge; an unanalysed projection does not inherit the mixture bound. Finite-expert regret does not imply non-exploitation by every efficient trader. EX08 separates the duties. |
| U09 / Q1,Q4 | For exogenous delayed feedback, record outstanding labels and satisfy the chosen wrapper theorem's base-regret and delay assumptions. For action-dependent discovery, state a different guarantee or report it as empirical. | S14 Algorithm 1 and Theorem 1; O-META for paid discovery | **Required distinction.** The selected wrapper uses a nondecreasing concave base-regret bound `f` with `f(0)=0`, the applicable delay independence, and charged active copies. Letting the proof policy determine delays does not automatically satisfy it. |
| V01 / Q4,Q5 | Distinguish semantic payoff, a subjective expectation, a learned estimate, a certified interval and a realized score. | O-PROB and S02; S01 Definition 4.8.2; inherited source/evidence modes | **Required typing.** Exact finite expectation identities use a supplied coherent law, not merely LI's threshold-price notation `E_n`. Calling an arbitrary cost “the probability” fails the known-stakes test. EX02. |
| V02 / Q5 | Define the requested recovery service: full law, a query family, a bounded interval, or one decision. Two admissible inputs with the same summary must give the same exact answer for an exact decoder to exist. | Ordinary finite expectation/information recovery; inherited retention results | **P3-02 target.** EX02/03 are witnesses of non-identification for specified summaries, not a universal impossibility of scalar representation. |
| V03 / Q4 | Compare action quality as well as forecasts. A sufficient local bridge is: if every action-cost estimate has error at most `epsilon`, the estimated minimizer's true cost exceeds the true minimum by at most `2 epsilon`. | Ordinary decision theory; derivation in EX08 | **Elementary conditional bridge.** It needs uniform action-cost control in common units. It does not establish a learning rate. |
| V04 / Q3,Q4 | Account for hard resource limits and all materially different forecast, proof, storage, acquisition and checking costs. Declare primitive operations, precision, advice/caches, amortization and readable information. Estimate the benefit of thinking from allowed evidence. | O-META; S03 Definitions 1–3; S20 performance profiles; S21 acquisition; main contract §6.3 | **P3-07 target and implementation closure requirement.** A free value-of-computation oracle, an uncharged answer table, or a claim that one-step lookahead is always optimal fails the contract. EX07; resource review RI01–04. |
| M01 / Q3 | Keep model/criterion scopes and applicability assumptions explicit. Compare selection, retention, approximation quality and logical truth as different services. | O-COMB; phase-two paper §8.1; S08 and S15 | **Required comparison.** A model can be conditionally useful without being an exact equation. Ordinary scoped modeling must receive the same library and evidence. EX04. |
| R01 / Q1–Q5 | On evidence withdrawal, objective change or semantic version change, mark dependent warrants stale/unusable until rechecked or transported with a proved correction; pay for the checks actually performed. | O-REUSE; inherited source transport | **Inherited conditional service; new application unproved.** A previously checked result on a different version is not automatically current evidence. Lazy rechecking is allowed; immediate recomputation of every dependent object is not required. EX09. |
| C01 / Q2 | Identify conditioning, token intervention, shared replacement, actor-only replacement, model repair and genuine counterpossible evaluation. | O-CHANGE; S04 §3/§5, S05 §2, S06 Definitions 4–6, S07 §2 | **Required interface.** EX05 gives different answers to superficially similar requests. |
| C02 / Q2 | A claimed uniquely identified consequence must follow from the supplied structural/repair information, not from an arbitrary favored model. | O-CHANGE plus ordinary identifiability reasoning | **Elementary obstruction** in EX06. Identical full observational laws can have different intervention losses. A unique policy-selected report is a different service. |
| C03 / Q2 | Record whether admissible alternatives exist. Separate optimality, coverage of all minimizing consequences and policy selection. If equally preferred alternatives disagree, preserve their range or use an announced tie policy. | Ordinary weighted repair/ranked revision with the same catalogue | **Required interface.** EX06 makes outcome-selective tie breaking visible; an empty selection cannot warrant usefulness. A known rank-zero candidate need not identify the consequence of every tied candidate. |
| C04 / Q2 | A genuine counterpossible analysis preserves the original antecedent and ordinary interpretation while explicitly identifying any exceptional hypothetical evaluation/consequence rules. | S07 §§2,3.1; explicit ordinary classical infeasibility diagnosis | **P3-04 obligation.** Changing the meaning of “rational” and calling it an answer to the original question fails topic preservation. EX10 and GC01 distinguish defining an exceptional evaluation from defending its relevance. |
| I01 / Q2–Q5 | An alleged representation equivalence transports operations, constraints, evidence, actions and costs. Refactoring preserves a result only under a declared identity/transport map. | Ordinary semantics and inherited coordinate/source transport; S07 §3.1 | **Required test.** A numeral recoding or program renaming alone does not establish operational equivalence. EX09/10. The contract does not demand identical hypothetical answers for every classically equivalent impossible antecedent. |
| F01 / Q1,Q4 | A self-model names its own versioned procedure. Staged evaluation and report-dependent feedback are distinct; self-endorsement supplies no proof. | Inherited `SELF-MIX`; S12 §5.3; S01 §§4.11–4.12 only as later comparison | **Inherited bounded case; broader duty open.** Proper scoring under an exogenous law does not ensure a valid report under endogenous outcomes. EX11. |

S-identifiers refer to the [primary-source record](../literature/01_source_contracts.md).

## 3. What different evidence would mean

An exact translation with preserved information, operations and charged resources
establishes equivalence for its stated fragment. Matching a finite table alone
establishes agreement on that table. A separating pair refutes only a decoder
restricted to the proposed summary. A proof of a regret or coverage statement
must retain its quantifiers, comparator and feedback assumptions. An empirical
advantage requires a prospectively fixed comparison and resource account.

Contribution assessment remains separate. A useful interface or application can
matter even when an ordinary method reproduces its numerical outputs, but it
must identify the exact added organization, theorem, guarantee or capability
and compare it with the closest ordinary combination. Calling several known
methods together does not establish that delta by itself.

## 4. Ownership of the next work

P3-02 owns probability/expectation identification; P3-03 owns the bounded
logical information/update procedure; P3-04/05 own counterfactual semantics
and transport; P3-06 owns refinement guarantees; P3-07 owns paid reasoning;
P3-08/09 turn the accepted contracts into an implementation and frozen challenge.
This matrix does not start those items or require every unrestricted duty to
be solved. Later work must report proved, reduced, finitely supported, refuted,
narrowed or unestablished status for every duty it actually claims.
