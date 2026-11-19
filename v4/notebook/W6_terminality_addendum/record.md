# P4-R6-C002 · Terminality under permanent pressure

Codex (GPT-6.2 Astra), November 18, 2026. The author invoked Fable's
[brief](BRIEF.md) from main at `db21e568` and supplied the override verbatim:

> This is an addendum to W6 that requires about one extra hour. Please follow the instructions in it.

Use 60 engaged research minutes for this cycle. Initial credit zero. W6
C001 closed at 240.213796685 minutes. The [clock](timing.jsonl) has its own
balance. Compute remaining minutes as max(0, 60 minus research_min) since
the shared clock displays the 240-minute default. Publication earns no credit.

For C5 and C7, ask which values a controller repeatedly expresses when an
environmental demand lasts indefinitely. Compare a terminal assessment, a
running incentive, and a transmitted controller in the finite W6 worlds.
Test both survival of an independent end and disappearance of its influence.
Compare maxima to behavior and control with the observation interface held
explicit. Seek an intervention definition usable by W7 and specify which
observations distinguish mechanisms. C3 concerns the analogy to limits under
successful use. Plan roughly 12 minutes of source reconstruction, 30 of
proof and example design and 18 of checks and scientific review.

## Scientific decisions and prospective check

Fable's original probe was rerun, including the rate shares at 20,000 updates.
The sharp finite-horizon test compares endpoint columns. In the independent
two-state priority model the same right eigenvector gives both the price of
installing the priority and the probability of losing it in the ancestors of
distant survivors. Checking the other direction led to two constructions:
an exact chooser can retain an end in a vanishing payoff gap, and a separable
running end can retain its full effect alongside a permanent pressure.

**Small deployment test specified before running it.** Use R6.12's physical
two-state environment with survival (1, 0.7) and its original live movement
matrix. Reset in A, where the current survival check passes. Assign 4,096
training trials per initial destination, A and B. Use ten further baseline
steps and accept survival alone. Give the learner only the initial
destination and a binary success flag. Store add-one-smoothed success
frequencies for the two destinations. Use 16 independent Python Random
seeds 17001 through 17016. Keep every seed.

At deployment offer the same two destinations with a new one-time survival
factor 1/d on A, where d is 1.5, 2, or 2.5. Use a greedy comparison of stored
score divided by cost with the competing score, breaking ties toward B.
Supply the price without relearning. Audit success under both pure final
assessments A and B at the original horizon, including the failure probability.
The column envelope predicts A at 1.5 and B at 2.5 for both ends. At 2 the
two ends can disagree. Count actual choices over seeds and report the central
boundary, where a learned score can lose to the endpoint-specific oracle.
Intervene by equalizing the two stored scores with the environment and price
still fixed. This is a causal test of this small controller's score interface.
Its transfer uses the known price rule, fixed continuation and the specified
one-step action menu. The training program is blind to the audit's true K
and alternative endpoints. Code and a short printed result suffice.


## Observed credit

Closed November 18 at 09:52:12 UTC. **3,620,366,586,300 ns = 60.339443105 engaged minutes** against the author’s 60-minute minimum. The appended exclusion discards the full interval straddling context recovery. Research and review resumed in the same cycle. Publication and handoff maintenance carry zero research credit.

## Assessment and handoff

**Advance at stated scope; available to recur.** The [result and proofs](../../results/R6_terminality.md) answer the two questions in the addendum. The project contribution is a measurable account of terminality in practice, joining the W6 selection and decision models. It uses established conditioning, entropy-regularized control, modifier selection and ancestral bias. It claims neither first discovery of those mechanisms nor an independent confirmation. The two requested policy-reconstruction documents were read at revision 5173cb04, with links in the result. The associated project's conclusions about a specified decoder and expected utility are used at their stated scope.

The decision model yields an exact price over all nonnegative final assessments, plus a deployed controller whose choices depend on its learned scores. The post-deployment binomial calculation marginalizes over training draws and reconstructs the observed transition between common choices and end-specific regret. The transmission model yields a selection-only route from zero adoption to near-universal adoption without a zero revision rate. The checks sum initially absent programs at 41 positive rates for the infinite example. After scaling reproduction by its upper bound of two, all omitted mass is bounded by its initial share $2^{-41}$. This gives certified finite-time intervals. A finite model can reach a specified approximation with a suitably low positive rate.

A consequential distinction emerged when I varied the form of time dependence. A common pressure bounded away from neutrality can sustain the priority with fixed revision. A positive advantage that tends to neutrality can leave the population evenly split. With rates tending to zero under fixed pressure, a population can approach full adoption whether a forward line makes finitely or infinitely many revisions. The survival probabilities on the two sides of the choice, current shares, and the rate along a sampled ancestry each answer a different question. These are mathematical and computational results in specified models.

**For W7.6.** Observe prices actually paid when the agent expects equal downstream benefits, and compare all transmissions with descendant-weighted histories. Test both a retained preference and a response that changes when the instrumental benefit changes. Where choices cannot decouple the downstream benefits, preserve the corresponding ambiguity. How conflicts between encoded ends are resolved, how revision procedures arise in a finite population, and the corrigibility-games comparison remain for W7.

**Aim-balance self-review.** Read the charter's Drift section, the aim policy, the author’s decision and brief, R6.4/R6.8/R6.12/R6.13/R6.15, the new result, its checks and the active plan. I paired the common-choice construction with a clamped end that still matters, the population limit with lineages that keep revising, and the learned controller with score edits and a better-informed planner. I corrected the implicit restriction to nonnegative outcomes by allowing a common exit payoff, and distinguished absolute from proportional prices. C5 and C7 advance at this scope. C3 gains an outcome-tested judgment about a declared continuation. C1, C2, C4 and C6 receive no new result. The recommended next test and the open interpretation of an ultimate want are in the result’s closing sections.
