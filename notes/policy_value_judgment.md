# Task 22: Policy–Value Correspondence and Recursive-Judgment Audit

Date: 2026-07-18
Status: completed; amended by the completed Task 22A theorem

## Durable decision summary

1. **The representational existence claim was not refuted.** For finite action
   sets, every deterministic policy has a lossless scalar code on the same state
   domain, and it also has a lossless action-score representation decoded by a
   fixed `argmax` rule. After restricting the representation space to the
   encoder image, these constructions are genuine bijections. This supports a
   precise finite existence form of `C01`.
2. **The counterexamples reject a stronger identification, not existence.** A
   policy does not determine a reward, a standard return-based value function,
   or a unique, natural, or identifiable preference representation. Conversely,
   a standard state-value function does not in general determine the original
   policy. Thus `C01` must be split by scope rather than marked categorically
   refuted.
3. **The strongest result for the companion's particular reconstruction is
   environment-relative forward evaluation plus conditional behavioral
   reconstruction.** Once the state,
   dynamics, reward/return, horizon or discount, perspective, initial/evaluation
   distribution, and policy are fixed, the policy induces `V^pi`, `Q^pi`, and
   occupancy measures. A learned surrogate may approximate those objects.
4. **Greedy use of `V^pi` or `Q^pi` is generally policy improvement, not
   inversion.** It reconstructs the original policy only on states where that
   policy is already greedy with respect to its own value, with compatible
   tie-breaking and perspective conventions. Otherwise it deliberately returns
   a different policy.
5. **Occupancy is behavioral distribution, not utility.** A full state–action
   occupancy measure can recover a Markov policy on positively occupied states
   by conditionalization under the stated regularity conditions. State
   occupancy alone loses the action choice; neither object supplies reward or
   preference without additional assumptions.
6. **Behavior supports only constrained rationalization.** Choices can impose
   local ordinal inequalities when feasible sets and consistency assumptions
   are known. Cardinal reward, off-support behavior, planner imperfections, and
   mechanism remain non-identifiable. Constant rewards, reward invariances, and
   unknown planner/reward decompositions make unrestricted rationalization
   vacuous.
7. **The companion repository is an instructive conditional case study.** At
   the inspected commit it implements frozen-policy rollout evaluation,
   separate value/Q regression, and greedy agreement tests in deterministic
   games. It does not use a policy “alone,” recover a unique reward, invert an
   arbitrary policy, or identify the policy network's mechanism.
8. **Recursive judgment now has a scoped information theorem.** Task 22A proves
   that positive population improvement under a strictly proper loss over the
   true nuisance-conditioned Bayes baseline implies `I(J;Y|N)>0`. Under log
   loss, an improvement of `delta` nats gives `I(J;Y|N)>=delta`.
9. **Task information still requires mediation and a quotient.** If residual
   judge–outcome dependence is mediated by latent task `Z`, the same lower bound
   applies to the outcome-identifiable quotient `K=k_N(Z)`. Leakage, omitted
   nuisance, duplicated task types, instability, calibration alone, and
   recursion-by-copying block stronger readings.
10. **These results do not alter the license calculus.** Policy/value material is
   optional motivation, a bounded companion case study, or future work. It is
   not a dependency of the finite-stage semantics, metatheory, neural
   representation results, or frozen experiment.

## 1. Scope and inspected evidence

This is a bounded identifiability and literature audit, not a second
implementation project. It covers inherited claims `B01–B05`, `C01–C11`, and
`G01–G06`; the policy/value sections of the source posts; the existing
literature map; and the companion repository
[`policy_value_isomorph`](https://github.com/TristanMiano/policy_value_isomorph/tree/097ea8897fb203b9b3a6ceafcb29e11bdc6cdd6c)
at exact remote `main` commit
`097ea8897fb203b9b3a6ceafcb29e11bdc6cdd6c` (2026-07-10).

The local companion checkout remained on older commit `4077eb5...` and showed
pervasive unstaged newline changes. Ignoring end-of-line differences produced
no content diff, but this audit nevertheless fetched the remote object and read
files through Git without switching or modifying the companion working tree.
No companion training or test command was run. The implementation conclusions
below are code-and-test-contract inspection claims, not fresh empirical results.

The primary literature checked for this audit includes policy evaluation and
improvement, inverse-reinforcement-learning identifiability, reward
invariances, occupancy equivalence, revealed preference, proper scoring rules,
and belief-state sufficiency. The most directly controlling sources are:

- Sutton and Barto,
  [*Reinforcement Learning: An Introduction*](https://www.incompleteideas.net/book/bookdraft2018mar21.pdf),
  second edition, especially the policy-evaluation and policy-improvement
  results;
- Ng and Russell (2000),
  [“Algorithms for Inverse Reinforcement Learning”](https://ai.stanford.edu/~ang/papers/icml00-irl.pdf);
- Armstrong and Mindermann (2018),
  [“Occam's Razor Is Insufficient to Infer the Preferences of Irrational Agents”](https://proceedings.neurips.cc/paper_files/paper/2018/hash/d89a66c7c80a29b1bdbab0f2a1a94af8-Abstract.html);
- [Kim et al. (2021)](https://proceedings.mlr.press/v139/kim21c.html) and
  [Cao, Cohen, and Szpruch (2021)](https://proceedings.neurips.cc/paper/2021/hash/671f0311e2754fcdd37f70a8550379bc-Abstract.html)
  on scoped reward identifiability;
- [Skalse et al. (2023)](https://proceedings.mlr.press/v202/skalse23a.html)
  on invariances and partial identifiability across reward-learning data
  sources;
- [Laroche and Tachet des Combes (2023)](https://proceedings.mlr.press/v202/laroche23a.html)
  on occupancy measures;
- [Afriat (1967)](https://cowles.yale.edu/sites/default/files/files/pub/d01/d0177.pdf)
  on utility rationalization from finite choice data under stated consistency
  conditions;
- [Gneiting and Raftery (2007)](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf)
  on strictly proper scoring rules; and
- [Smallwood and Sondik (1973)](https://doi.org/10.1287/opre.21.5.1071) and
  [Kaelbling, Littman, and Cassandra (1998)](https://doi.org/10.1016/S0004-3702(98)00023-X)
  on belief-state formulations for partial observability.

## 1A. Author motivation for the policy/value interpretability bridge

**Source status:** the following is a transparent paraphrase of project-author
guidance supplied on 2026-07-18. It records intended motivation, not an
independently established mathematical or empirical result.

The author intends *policy* in a deliberately broad black-box sense: a bounded
mapping that may perform essentially any computation on its state domain and
emit a successor state or an action whose deterministic environment transition
produces that successor. The attraction of policy-to-value reconstruction is
therefore not limited to recovering a conventional reward table. A value
function is envisioned as a particularly high-level model of agent behavior—a
way of describing what states or prospects the black box acts as though it
ranks, even when the underlying system contains no explicit utility module that
can be read out.

Additional project-author guidance supplied on 2026-07-18 makes the non-claim
explicit. The project does not try to decide whether an arbitrary policy has a
*true* utility function at all. Its practical target is an approximate
value-function representation of the model. No claim is made that this
surrogate recovers a true utility if one exists, or that an infinite-compute
limit would identify a uniquely truest recoverable approximation. Those are
separate questions and remain outside the project.

The author also records the historical reason this route led to pragmatic
logic: value was the first semantic object that seemed straightforward to
recover from black-box behavior, whereas beliefs were not recovered first and
their extraction was harder to formulate. The adjudicated project restatement
is “value as a promising first semantic foothold,” not a theorem that value is
metaphysically prior, that belief is reducible to value, or that belief
extraction is impossible.

On this view, full mechanistic transparency may be unattainable and is not the
only useful target. A learned model-of-a-model can still contain interpretable
information: stable rankings, local comparisons, failure regions, or
counterfactual predictions that compress some behavioral structure of the
original policy. This is the intended reason to bridge
`policy_value_isomorph` with value logic. The policy/value project supplies a
candidate high-level surrogate; value logic can state the domain, evidence,
margin, abstention, and provenance conditions under which reliance on that
surrogate is warranted.

The project's adjudicated restatement is slightly narrower than calling value
*the* highest-level interpretability model. It treats value as one especially
promising agent-level abstraction whose usefulness must be graded. The finite
existence construction shows that a lossless value-like representation can be
defined; the companion asks whether a semantically meaningful approximation can
be learned; Task 23 specifies separate tests of behavioral usefulness, domain
stability, human inspectability, and representational or causal faithfulness.
It need not be the unique true internal utility to be informative, but action
agreement alone is not yet interpretability.

## 2. Representational existence and the operational maps

### 2.1 A finite existence result

The word *isomorphism* first needs objects and structure. At the weakest
set-theoretic level, the finite deterministic existence claim is elementary.
Let `S` be any state set, let `A` be a finite action alphabet, and fix an
injective code `c:A -> R`. For the deterministic policy space `Pi = A^S`, define

```text
E_c(pi)(s) = c(pi(s)),
D_c(u)(s)  = c^{-1}(u(s))  for u in c(A)^S.
```

Then `D_c o E_c = id_Pi` and `E_c o D_c = id_(c(A)^S)`. Thus `E_c` is a
bijection between policies and a restricted class of real-valued functions on
the same state domain. It is lossless even though its scalar labels and their
ordering are conventional. This is a representation theorem, not yet a theorem
that the scalar has return, preference, or cardinal-utility semantics.

If decision semantics rather than a categorical scalar code is required, let

```text
U_pi(s,a) = 1 if a = pi(s), and 0 otherwise.
D(U)(s)   = tie-broken argmax_a U(s,a).
```

Again `D(U_pi)=pi`; restricting the score space to the encoder image makes the
maps inverse. A stochastic policy can similarly be represented by its
state–action probability scores and recovered by normalization rather than
`argmax`. These constructions establish existence but not uniqueness: many
score functions induce the same policy, and different codings impose different
geometry. For infinite action classes or when continuity, measurability,
computability, naturality, or preservation of a richer algebra is required,
those conditions must be stated and proved separately.

This is the point missed by the initial Task 22 wording. Counterexamples against
one proposed reconstruction cannot refute the existence of some encoding. They
can show that the encoding is not the standard return value, not unique or
canonical, not identified from observations, or not practically recoverable by
the tested procedure.

### 2.2 Standard return evaluation and practical reconstruction

Fix an MDP or game specification

```text
M = (S, A, P, r, gamma, mu, perspective, horizon),
```

with a sufficiently Markov state, legal-action map, transition kernel, reward
or terminal utility, discount/horizon convention, initial or evaluation
distribution, and perspective convention. For a policy `pi`, standard forward
evaluation defines

```text
V^pi(s)   = E_pi[sum_t gamma^t r_t | S_0=s],
Q^pi(s,a) = E_pi[sum_t gamma^t r_t | S_0=s, A_0=a],
rho^pi(s,a) = E_pi[discounted visits to (s,a) | S_0~mu].
```

Under the usual finite discounted assumptions, `V^pi` and `Q^pi` are unique
solutions of the policy-evaluation equations. This is a map from the pair
`(M,pi)`, not from `pi` alone. Occupancy additionally depends on `mu` and on the
discount or horizon convention.

The reverse-looking constructions are different maps:

```text
G(Q)(s) in argmax_a Q(s,a)
pi_rho(a|s) = rho(s,a) / sum_b rho(s,b), when the denominator is positive.
```

`G(Q^pi)` is a greedy-improvement policy. It equals `pi` only when `pi` is
already greedy with respect to its own action values and the chosen tie rule
matches. `pi_rho` recovers a Markov behavior on the support of a full
state–action occupancy measure; it says nothing about zero-occupancy states and
does not recover a reward. These particular standard-return and occupancy maps
are conditional correspondences, not mutually inverse structure-preserving
bijections. That limitation does not apply to every possible representational
encoder such as `E_c` or `U_pi` above.

The final paper and blog should preserve both formulations:

> **Finite representational policy–value correspondence:** after fixing a
> policy class, a value-like scalar or action-score representation class, and a
> decoder, a lossless policy encoding exists; on the encoder image the maps are
> inverse. This is an existence result, not a claim of uniqueness, naturality,
> return semantics, identifiability, or easy reconstruction.

> **Environment-relative policy evaluation with conditional behavioral
> reconstruction:** a fixed policy and fully declared decision process induce
> value and occupancy objects; those objects can reconstruct behavior only on
> stated supports and under stated greediness, tie-breaking, and information
> assumptions.

## 3. What four counterexamples do—and do not—show

### 3.1 A policy alone does not determine value

Take the same one-state policy in two otherwise identical discounted processes.
Give every transition reward zero in the first and reward one in the second.
The policy is identical, but its value is respectively `0` and
`1/(1-gamma)`. Dynamics, reward, discount, and perspective are inputs to value;
they cannot be recovered from the policy object by definition.

### 3.2 Policy evaluation followed by argmax need not recover the policy

At a state with two terminal actions, let action `a` return `1` and action `b`
return `0`, while the frozen deterministic policy chooses `b`. Then
`Q^pi(s,a)=1` and `Q^pi(s,b)=0`. Greedy recovery chooses `a`, not the frozen
policy. This is exactly the point of the policy-improvement operator. Agreement
with the original policy is expected only if the original policy is already
greedy or approximately so on the evaluation distribution.

### 3.3 The forward policy-to-value map is not injective

If two legal actions have identical transition and reward consequences, two
policies that choose different actions have the same `V^pi`. More generally,
state value averages action values under the policy, so different stochastic
mixtures can have the same average. Differences at unreachable states are also
invisible to an occupancy-weighted evaluation. Therefore `V^pi` cannot be a
general inverse encoding of `pi`.

### 3.4 Visitation is not preference or cardinal utility

A state can have high occupancy because it is unavoidable, absorbing, slow to
exit, or common under the initial distribution while being negatively rewarded.
A preferred terminal state can have small occupancy because episodes end upon
reaching it. State visitation therefore does not inherit a utility ordering.
Full state–action occupancy can encode behavior on its support, and expected
return can be written as an occupancy–reward pairing once a reward is supplied;
neither fact identifies occupancy with reward.

These examples refute unrestricted `C03`, unrestricted `C08`, and only the
stronger reading of `C01` on which the inverse must be the standard
return/occupancy construction, unique, canonical, or observationally
identifiable. They do **not** refute the finite existence construction in
§2.1. A constant reward also makes every action optimal, rationalizing any
policy while revealing no distinctive preference. Reward transformations and
unknown planner/reward decompositions create wider equivalence classes
documented by the IRL literature. Multiple environments, discounts,
interventions, or structural restrictions can shrink those classes, but doing
so adds assumptions to standard-return identification rather than erasing the
separate representation-existence result.

## 4. Companion-repository adjudication

The inspected commit's README is appropriately cautious in its project-thesis
section but still asks whether value can be reconstructed from a policy
“alone.” The implementation actually supplies the missing background:

- deterministic tic-tac-toe rules and legal actions;
- terminal utility in `{-1,0,+1}`;
- a fixed root-player perspective and turn-conditioned `argmax/argmin` rule;
- on-policy sampled states and rollout budgets;
- a frozen heuristic or one-hidden-layer `tanh` policy;
- Monte Carlo `V^pi` and `Q^pi` targets;
- separate MSE-trained value/Q regressors; and
- masked-cross-entropy policy imitation, explicit agreement/calibration
  utilities, and modest test thresholds.

The code therefore implements a legitimate experiment in **forward policy
evaluation, surrogate fitting, and conditional greedy agreement**. In the
deterministic no-intermediate-reward setting, successor-state values and action
values agree under the declared sign/perspective bookkeeping. The tests inspect
loss decrease, legal actions, an MAE threshold, at least `.55` Q-policy
agreement in one small sample, comparison with successor-value recovery, and
simple forced moves. This is an implementation witness and test contract, not
an estimate of generalization across policies, games, or distributions.

Three interpretations of the companion experiment are not licensed:

1. **Policy-only recovery of standard return or reward.** The game, terminal
   utility, state convention, perspective, rollout procedure, and sample
   distribution do essential work.
2. **Inversion of an arbitrary policy by this learned `V^pi/Q^pi` route.** The
   recovered `argmax/argmin` policy is a greedy policy derived from `V^pi` or
   `Q^pi`; disagreement can be correct policy improvement rather than
   reconstruction failure. This says nothing against the direct existence
   encoders in §2.1.
3. **Mechanistic interpretability.** The policy and value networks are trained
   separately. Agreement does not identify shared hidden features, causal
   computation, reasons, or the policy's internal value representation.

Task 23 uses this repository as a conditional implementation witness and
allocates future behavioral agreement, return/value fidelity, support/shift,
representation, and causal tests to it. No result here makes the companion a
core dependency of value logic.

## 5. What behavior can rationally reveal

Observed choices can reveal a local preference ordering only relative to known
feasible alternatives and a consistency model. If a deterministic policy
chooses `a` from a known feasible set and is assumed to maximize a stable
criterion, one may record the inequality `a >= b` for alternatives `b` in that
set. Revealed-preference theorems add substantive consistency, budget, and
regularity assumptions before producing a utility representation. Even then,
utility is ordinarily unique only up to an equivalence class appropriate to the
theorem, not as a privileged neural mechanism or cardinal reward.

For a general policy, rationalization is underdetermined in at least four ways:

- different rewards can induce the same optimal behavior;
- different planner/reward pairs can generate the same suboptimal behavior;
- off-support behavior is unconstrained by observed occupancy;
- state aliasing can turn apparently inconsistent choice into consistent choice
  on a richer history or belief state.

Enlarging the state to a sufficient history or correctly maintained belief
state can restore a Markov control problem under a specified model. It does not
identify an arbitrary learned compression, nor does it remove reward/planner
ambiguity.

## 6. Recursive judgment after Task 22A

The motivating idea behind `B01` is plausible only after separating three
objects:

- latent task structure `Z`;
- a held-out performance outcome `Y`; and
- the judge's pre-outcome report `J`, based on permitted observations and
  nuisance context `N`.

A judge can predict `Y` using leakage, subject identity, base rates, or a stable
nuisance without representing the task distinction of interest. A report can
also be calibrated while remaining constant and uninformative. Task 22A now
settles the positive direction in
[`formalism/09_judgment_information.md`](../formalism/09_judgment_information.md):

```text
positive strict-proper-score improvement over Bayes P(Y|N)
    -> I(J;Y|N) > 0,

log-loss improvement delta
    -> I(J;Y|N) >= delta.
```

Define `K=k_N(Z)` by merging latent task labels with identical
`P(Y|Z,N)`. Under `J` independent of `Y` conditional on `(Z,N)`, quotient
mediation and data processing give

```text
I(J;K|N) >= I(J;Y|N).
```

Thus the surviving theorem uses these assumptions and interpretations:

| assumption | required role |
|---|---|
| nondegenerate latent task `Z` | excludes a one-type or label-only tautology |
| stable `P(Y given Z,N)` across train/test | makes task distinctions predictively meaningful |
| held-out outcome and lineage separation | blocks direct label or future-data leakage |
| nuisance-complete baseline `P(Y given N)` | prevents base rate, identity, or difficulty from masquerading as task information |
| strictly proper score and positive population loss gap | turns improvement over the Bayes baseline into an outcome-information theorem |
| mediation/non-leakage `J independent of Y given (Z,N)` | makes outcome information attributable to the scoped latent structure |
| identifiable task quotient | limits recovery to distinctions that change observables; labels may remain permutation-equivalent |
| independent evidence at each recursive level | prevents self-endorsement, copying, and collusive fixed points |
| stationarity or modeled feedback | prevents evaluation incentives from silently changing the target |
| replication under shift | separates stable structure from dataset-specific shortcuts |

Task 22A supplies the matching countermodels: a poor comparator can be beaten by
an uninformative report; omitted identity can predict outcomes without task
information; future leakage defeats mediation; duplicated types identify only
the quotient; deployment instability destroys transfer; and copied recursive
reports have zero incremental conditional information.

Recursive evaluation does not itself provide ground truth. It may create a
useful training/evidence architecture if later judgments are checked against
independent outcomes, but additional levels can also amplify shared bias or
collusion. At recursive level `m`, the relevant gain is
`I(J_m;Y|N,J_0,...,J_(m-1))`; copying makes it zero. `B02` therefore remains
motivation/future empirical work. The slogan
`T=J^2` is not a typed theorem and is excluded from technical claims unless a
later artifact supplies domains, codomains, and an equivalence criterion.

## 7. Claim dispositions and publication allocation

| claim group | Task 22 disposition | provisional public location |
|---|---|---|
| `C01`, policy–value isomorphism | `S1` for finite lossless representational existence; `X1` only for the standard-return/occupancy, unique, natural, or identifiable strengthening | concise formal/motivating proposition plus explicit semantic boundary |
| `C02`, value plus environment and decision rule induces a policy | `S1` as a conditional construction, including ties | optional formal/case-study background |
| `C03`, occupancy counts are utility | `X1` as a general identity; support-relative behavioral occupancy survives | limitation or omit |
| `C04`, revealed ordering | `S1` only under known feasible sets and consistency/rationality assumptions | short related-work qualification |
| `C05–C07`, scoped evaluation/recovery and sufficient state | implementation/formal support at exact scope; broader empirical generalization remains `T0` | companion case study |
| `C08`, value must match policy complexity | `X1` without counting dynamics/decision machinery; constant-value counterexample | omit except as a limitation |
| `C09–C10`, LLM values and fragility conclusions | still underspecified/untested | future work or omit |
| `C11`, policy-only non-identifiability | `S1` formal and literature-supported | formal paper boundary and case-study setup |
| `B01`, task information from successful judgment | `S1` scoped proper-score/log-loss theorem; `X1` unqualified baseline, mediation, or recursion strengthening | compact formal-paper motivation theorem with adjacent countermodel; not a novelty headline |
| `B02–B04`, recursive measurement/centroids/`T=J^2` | motivating or untyped; no theorem | Substack motivation with explicit caveat, or future work |
| `B05`, improvement requires value change | `X1` as universal wording: fixed-objective world-model or policy learning is a counterexample | omit |
| `G01–G03`, current companion code/test scope | `S1` by pinned code/test-contract inspection; tests not rerun here | companion case-study appendix/repository link |
| `G04–G06`, mechanistic/transparency bridge | seven-axis design and behavioral/mechanism separation are valid; empirical transparency remains `T0` | Task 23 design and future companion evidence |

The scoped negative results affect optional motivation, not the project's
central question. The formal paper may include the finite encoder proposition,
then the policy-evaluation map and compact counterexamples to show why that
existence result does not supply return semantics, identification, or a
practical reconstruction guarantee.
The Substack post may state that successful held-out prediction forces
outcome/task-quotient information only with the Task 22A baseline, mediation,
and stability conditions. Task 23 supplies an evaluation design but no positive
interpretability result, so the companion repository remains an implementation
witness and prospective bounded case study. Equating the existence
correspondence with standard return, occupancy-as-utility, value-complexity
necessity, and unqualified claims that recursive judgment “measures fact” are
excluded. The qualified finite existence claim is retained.

## 8. Task 23 follow-through

Task 23 is complete in
[`policy_value_interpretability.md`](policy_value_interpretability.md). Its test
program remains companion/future work. The repository now proceeds to **Task 24
— Build the counterexample and limitations section**.
