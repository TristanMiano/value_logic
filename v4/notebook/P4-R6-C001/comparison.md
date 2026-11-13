# Closing comparison: what the W6 constructions add

Codex (GPT-6), November 12, 2026. Scientific comparison for P4-R6-C001,
completed before its assessment. This is a bounded literature comparison,
not an exhaustive novelty certification. Read scopes are in [sources.md](sources.md).

## Judgment that recovers fact

[Nayebi (2026), *What Capable Agents Must Know*](https://arxiv.org/html/2603.02491)
is a particularly close predecessor. Its theorem 3 recovers predictive
probabilities from low average regret on threshold bets; corollary 5 relates
minimal representations under a common separating evaluation to recoding.
The threshold proof charges wrong decisions by their distance from the
threshold and bounds the probability error by rearranging that mass. The
recoding proof combines no-aliasing with minimality. These already establish
substantial parts of the judgment-to-fact and inter-agent convergence idea.
Their diagnostic and minimality assumptions matter; this review does not
import a general conclusion about arbitrary internal representations.

R6.1's continuous-price quadratic identity is a simple special form of this
bridge, not a newly discovered principle. The W6 contribution should be read
through its additional questions: different agents' task families; their
common information versus pooled information; priced, incomplete exposure;
and actual learning from selectively observed payoffs. R6.14 and R6.16 make
these distinctions explicit. Their finite, fixed-vocabulary answer is useful
without claiming that this is the first decision-based account of factual
representation.

[Richens, Abel, Bellot and Everitt (2025), *General agents contain world
models*](https://arxiv.org/html/2506.01622v5) is a stronger sequential
competence-to-model result: in its finite communicating setup, choices
between composite goals reveal transition probabilities. Its construction
uses repeated transition trials encoded in goals. W6's iid priced-decision
example addresses a smaller information interface and acquisition costs;
it does not supersede that sequential result.

## Values that recover dynamics

[Adamczyk (2025), *Inferring Transition Dynamics from Value Functions*](https://arxiv.org/html/2501.09081)
already inverts deterministic Bellman equations using known rewards,
action-values and a separating state-value map. Its error analysis makes
separation consequential. This is a direct antecedent, not merely general
background on reinforcement learning.

[Letcher et al. (2026), *Inverting the Bellman Equation*](https://arxiv.org/abs/2606.21173v1)
is the strongest direct comparison. It reconstructs dynamics from known
rewards, policies and action-values through a linear inverse Bellman system,
with identifiability, precision and genericity results. Its appendix C.7
also constructs single-reward families that remain ambiguous across all
policies and discounts. Therefore varying policies alone has no universal
identification guarantee.

R6.8's supplement instead specifies **state-value-only** queries and combines
policy mixtures in one design matrix. Its four-query/three-state and six-query/four-state witnesses
establish generic positive cases and minimal query counts for that
interface; they coexist with structured ambiguity at the same state count.
It is a concrete instance and synthesis of inverse-value identification,
with its own exact witness and conditioning bound. Neither Bellman inversion
nor a general claim that values encode a world model is new here.

The reward-timing conventions differ: the source uses next-state rewards,
whereas R6.8 uses current-state rewards. With known state reward and positive
discount, the corresponding state values obey
$V_{\mathrm{current}}=r+\gamma V_{\mathrm{next}}$.
The comparison therefore concerns available observations, not a superficial
notation difference. Supplying all action-values carries more information
per policy than supplying its state values alone. The supplement's row-sum
constraints and joint policy design explicitly account for that interface.

[Batra (2026), *From Optimal Actions to World Models*](https://arxiv.org/abs/2608.07301)
is an additional lead on transition identifiability from optimal actions
across reward functions. Only its abstract was screened here. Its action
interface differs from supplied values or named counterfactual evaluations;
no technical novelty judgment in this cycle relies on its unread proof.

## Retained success and learning

The main R6.13 comparison already credits reward-weighted regression,
risk-sensitive control and Perron optimization. These supply both the
reweighting mechanism and strong competing planning methods. The additional
return-conditioned-learning comparison in its section 6 matters because
copying successful behavior can confound a controllable choice with a lucky
outcome. R6.13's proof changes the action distribution and evaluates it under
the original physical kernel. The finite-trial supplement states the reset,
positivity and increasing-budget conditions needed to learn those updates.

A mathematical convergence guarantee does not imply that this learning
schedule is economical. The small sampled panel and the theorem schedule
remain separate. The strongest practical comparator when a model is available
is greedy risk-sensitive planning, which wins the declared iteration
comparison. External filtering without a represented objective remains a
faithful interpretive contribution; explaining the origin of the filter and
its meta-rule is reserved for W7.

## Consequence for the assessment

The supported claim is a **useful, explicitly implemented synthesis with
finite characterizations**, not the invention of instrumental convergence,
decision-based factual identification, Bellman inversion, or success-weighted
learning. The strongest local evidence is R6.16's shared/private recovery
and paid learning episode, accompanied by conditions distinguishing
agreement, factual content and persistence. The inverse-value supplement
strengthens the conceptual map and supplies a checkable small case. Its
publication novelty remains a separate question.

This comparison corrects an initial risk of treating older proper-score and
value-equivalence work as the closest available comparison. The more direct
recent primary results belong in the record. Recognizing those predecessors
supports the founding mechanism while locating the remaining contribution
more precisely; it is neither evidence that the charter is empty nor a
license to claim its broad theses proved.
