# W6: shared purposes can select shared facts and revisable priorities

**Codex (GPT-6), November 12, 2026. Cycle P4-R6-C001.**
Scientific assessment; cycle closure and final validation are recorded in
[record.md](record.md). This assessment does not start W7 or another cycle.

## Alignment before correctness

The main advance is a constructive connection between **instrumental value,
judging judgments and factual representation**. In the implemented example,
agents with different fixed purposes learn which distinctions to keep from
payoffs revealed by actions they actually take. Sufficiently overlapping
demands select the same hidden factual component. Different demands can
instead select different useful components. A second line shows how external
survival filtering can produce and improve a policy without a represented
terminal utility, while keeping the external selection criterion explicit.

| Charter thesis | Movement in this cycle | Remaining obligation |
| --- | --- | --- |
| C1: judging judges recovers fact | Advanced: actual decision losses identify useful distinctions; purchased feedback trains forecasts and selects representations; separating policy-value judgments can identify action dynamics. | Generate new vocabulary and acquire the evaluator, rather than assume their finite interfaces. No exclusive information advantage over an equally informed ordinary learner is claimed. |
| C2: task delineation and J² | Advanced: representation choice is evaluated by the decisions its forecasts support, with an implemented shared/private selection boundary and a context-sensitive adequacy characterization. | Couple this mechanism to W1's task/judge fixed point; the two implementations have not been joined. |
| C3: truth through successful use | Advanced at a finite factual scope: coverage, separation and feedback distinguish grounded agreement from a useful coarse consensus. | A logical truth limit, consequence relation and changing-language construction remain W2/W3 work. |
| C4: local supersession and ontology change | Broad thesis unchanged; separating changed relevance from changed facts provides a useful input. | Carrier changes, bridges and local licenses are not supplied by choosing among fixed partitions. |
| C5: constrained values of values | Advanced: bounded controllers benefit from better internal values; retention and revision have explicit stability, flexibility and diversity regimes. | Origin of the revision rule, genuinely cyclic self-licensing and Löb-type constraints remain open. |
| C6: neural atlases | Unchanged. | No neural experiment was undertaken. |
| C7: policy/value duality | Advanced: conditional rollout values reconstruct behavior; separating scalar values can recover a policy; specified policy-value queries can recover an unknown environment. | Neural size, runtime, learned nonlinear representations and unconditional complexity are separate obligations. |

These are restricted mechanisms that preserve the direction of the founding
theses. They are not seven completed theses or a proposal to replace them
with a generic optimization toolkit.

## 1. Different fixed goals can induce common, learned factual distinctions

The central world has eight raw contexts hiding three independent bits:
a common factor $H$ and private factors $A,B$. Agent 1's payoff opportunities
depend on $H$ or $A$; agent 2's depend on $H$ or $B$. The raw labels are
randomly permuted. Neither learner is told those meanings or the outcome
probabilities. It sees a context, a goal label and a price, chooses whether
to buy, and observes the outcome only through a purchased payoff.

A representation partitions the raw labels and supplies a forecast for
each cell and goal. More cells have a declared deployment cost. The learner
compares all 4140 partitions, estimating conditional outcomes from purchases
and task frequencies from all training inputs. This is ordinary statistical
model selection with a concrete second-order interpretation: **evaluate a
judge and its distinctions by the useful decisions they support**.

[R6.16](../../results/R6_learned_concepts.md) proves consistency under
positive exposure, iid opportunities, a finite partition class and a valid
probability range. Its exact population calculation gives a sharp boundary
in this example. At cell price 0.02, the common bit is uniquely optimal when
the common goal's frequency exceeds one half; the private bit is uniquely
optimal below one half. Both tie at equality. Goal overlap and cost determine
whether the shared distinction is worth retaining.

The final panel uses 32 replicas, two agents per replica and 130,560
opportunities per agent. It charges the full eight-cell price on all 4287
training opportunities, including declined trades. Means below include
those charges and the cost of deployed representations.

| Common-goal frequency | Final correct representation | Selective training: whole-run expected net return | Forced-purchase training | Known constant forecast | Known-law optimal deployment |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0.8 | Shared $H$, 64/64 agents | **0.136466** | 0.131509 | 0.125000 | 0.141000 |
| 0.4 | Own private bit, 64/64 agents | **0.127174** | 0.122723 | 0.125000 | 0.132000 |

The selective learner buys about half the training outcomes. Its paired
gains over forced purchases are 0.004957 and 0.004451 per opportunity,
with standard errors 0.0000326 and 0.0000899 across replica means.
Realized whole-run returns are 0.136675 and 0.127101. The constant and
known-law columns are explicitly informed baselines; the latter pays no
acquisition cost. These are synthetic finite-panel results, not estimates
of performance across arbitrary agents or environments.

The first forced-purchase version had not repaid its acquisition cost in
the low-overlap world. Making useful choices during training repairs that
comparison, even though fewer labels slightly reduce final forecast accuracy.
Using frequencies from purchases as if they represented all opportunities
causes a different error: selective observation distorts the task weights.
That variant reaches the private optimum in only 54/64 low-overlap runs
and has whole-run return 0.124871. Keeping input frequencies separate from
conditional outcomes is both the constructive repair and the reason its
consistency proof applies.

The representation price is a declared cost of deployment. Full raw-context
training counts, encoder mappings and exhaustive search are explicit
infrastructure outside that price. No physical-memory or CPU advantage is
claimed. This scope is enough to establish a paid-feedback construction;
it is not a complete engineering cost model.

**Why the shared component is factual.** [R6.1](../../results/R6_goal_judgment.md)
derives a decision-regret bound on forecast error when actual goal uses
separate the target outcomes. The target is fixed by the environment and
payoff contract, not by how many agents agree. In the low-overlap world,
both agents can agree on a coarse forecast near 0.5 while discarding the
common factor's 0.2/0.8 distinction. Agreement is then useful at the chosen
representation cost, but it has a different factual content.

**How strong is the convergence pressure?** A further panel near the
shared/private boundary makes finite diversity visible. At common-goal
frequency 0.51, 41/64 agents choose the shared bit at the original budget;
52/64 do so after the extended budget. At 0.50, shared and private choices
are equally good, and mixed pairs persist. More evidence reduces regret,
but near-indifference gives a weak pressure toward one representation.
[R6.16 section 8](../../results/R6_learned_concepts.md#8-finite-agreement-near-the-sharedprivate-boundary)
reports both the improvements and acquisition costs.

**Durability changes what is worth retaining.** If representation cost is
paid once and the code is reused, the same known-law example eventually
favors retaining both the common and private fact for every positive
frequency of both goals. The exact reuse threshold is given in
[R6.16 section 9](../../results/R6_learned_concepts.md#9-reuse-can-make-the-common-fact-worth-keeping-under-every-positive-overlap).
This is a mathematical cost comparison; the executed learner uses a
recurring price. Learning and maintaining a reusable code still need to
be paid for.

**When subgoals should change.** Fixed terminal reward rules do not freeze
which information is useful. If opportunity frequencies change from 0.8 to
0.4 while conditional outcome laws remain stable, recent inputs can reweight
old factual evidence. In the diagnostic panel, this selects the newly useful
private distinction in 31/32 runs before any new outcome purchase. Pooling
old and new task frequencies still selects the old common distinction in
all runs after 2048 new purchases. If the private outcome relation reverses
too, reusing all historical outcomes is initially harmful; a recent window
recovers more quickly. The experiment compares fixed estimators, not an
implemented detector that knows which change occurred.

## 2. Persistence has several meanings; terminality is not one scalar

The strongest supported answer to the author's second and third questions
is conditional: **a repeatedly useful intermediate priority can remain
strong across changing goals, while different final goals remain fixed or
different agents retain useful differences.** The mechanism and intervention
must be specified before calling that priority terminal-like.

[R6.4](../../results/R6_plastic_priorities.md) models retained programs with
and without a priority, goal revision, and mutation of the priority. If the
priority has relative retention advantage at least $R$ in every goal context,
and the goal-revision routes overlap by at least $\kappa$, its frequency
has an explicit positive limiting lower bound determined by $\kappa R$ and
the two mutation rates. A majority is guaranteed precisely on the stated
parameter side of that scalar bound. Goal-dependent sorting can defeat the
within-goal advantage; restoring overlap repairs the guarantee.

Four useful measurements are therefore distinct:

- **Breadth:** how many goals benefit, with their actual weights and costs.
- **Robustness:** whether the priority survives changes in goals and context.
- **Revision resistance:** how readily the internal priority can change.
- **Persistence after removing its benefit:** whether the acquired priority
  remains when its original practical support is experimentally removed.

In the neutral-removal experiment, continuing symmetric revision eventually
erases the acquired excess; revision rates with a finite cumulative total
can preserve it. Coordination feedback can also sustain either of two
conventions. With a fixed revision rate, a stronger advantage increases the acquired
priority but does not change its neutral-removal half-life. Under constant
selection, reduced revision can improve long-run retention; under reversals, a positive revision rate can do better. These
are explicit mechanisms for different grades of terminal-like behavior,
not evidence that usefulness automatically creates an immutable end.

[R6.11](../../results/R6_changing_goals.md) further distinguishes convergence
along a shared history from agreement in distribution. Positive revision
contracts different initial log-odds under the same changing experience.
Independently experienced agents can retain substantial differences even
when their stationary laws agree. A population distributed across contexts
can also favor a priority that loses along one synchronous sequence of
contexts. Arithmetic growth across a population and geometric growth through
time answer different questions.

For genuinely clamped terminal goals, the allowed adaptation is in the
controller or subgoal representation. [R6.6](../../results/R6_bounded_subgoals.md)
gives three distinct goals that all benefit from a preparation value under
one-step planning: actual expected returns rise from 0.4 to 0.6, 0.7 and
0.8. Potential-based shaping and an exact Q-initialization recoding implement
the same change; deeper planning is a different comparator. A low-success
environment makes preparation harmful and supplies feedback to reject it.

The way a value is used also matters. [R6.15](../../results/R6_value_use.md)
shows a continuation value becoming a harmful recurring bonus: the agent
waits to collect the bonus instead of completing the task. Potential
differences repair this while preserving the original return. A mistaken
potential can still cause delay, and the example prices the loss during
its correction. This is a concrete distinction between making a means
salient to a bounded controller and paying it as an additional end.

Strategic interaction supplies another route. [R6.10](../../results/R6_strategic_values.md)
constructs a credible, observable preference commitment that improves the
agent's previous material objective. A literal terminal-goal clamp would
exclude installing that new terminal utility, although binding a policy can
have a related strategic effect. Limited observability and fallible
certificates give explicit regions of commitment growth, loss or stable
diversity. The paper comparison does not confuse this two-type dynamic
with stability against every possible preference mutant.

## 3. A represented terminal goal is not required for acquired direction

[R6.12](../../results/R6_unrepresented_values.md) starts from neutral
behavior and external survival filtering. Long retained histories have a
positive value-like description independent of a fixed terminal weighting,
under the stated positive finite-chain assumptions. This is established
Doob/Perron structure interpreted as an acquired practical priority. The
process need not contain an internally represented ultimate utility, but
the environment and retention rule supply directional selection.

The crucial repair is to copy **actions**, then evaluate their actual
physical consequences. Conditioning successful state transitions alone can
mistakenly grant control over luck. [R6.13](../../results/R6_selection_learning.md)
proves improvement for appropriately timed finite-horizon copying, and
global convergence of a stationary exact update to the best survival growth
factor when every deterministic policy has an irreducible live kernel and
the initial policy has full action support. Sparse examples satisfying that
condition are included.

The [finite-trial supplement](../../results/R6_selection_sampling.md)
supplies a learned version under stronger positive-kernel and reset assumptions.
Increasing the horizon and sample count makes relative estimation errors
summable, preserving global convergence. Each update uses finitely many
attempted trials; the sufficient budget can be enormous. A modest sampled
panel is kept separate from that theorem schedule.

Both benefits and limitations are consequential. In one fixed world, the
limiting copied controller's 32-step survival is 0.017608 versus 0.001188
for the initial controller; an informed controller achieves 1 from the
chosen initial state. In a different positive world, stationary copying
from exact one-step success lowers the long-run survival factor from
0.514575 to 0.364882; a longer horizon reaches 0.791446. Rare successes also
make finite-sample long-horizon copying unreliable without enough trials.
Model-based greedy planning is faster than multiplicative copying in the
declared exact panels. These comparisons identify what the emergence
construction supplies and which costs it does not remove.

This answers the “no terminal goals to start with” question at one faithful
scope: variation and externally retained behavior can acquire direction
before a terminal objective is represented internally. Explaining why the
retention mechanism, inheritance rules or meta-evaluator arise and remain
stable is the next module's question. The author's clarification explicitly
permits that division. W7 has not been executed merely because W6 derived
a bridge that it can use.

## 4. What links instrumental convergence to J²?

Both concern feedback on ways of valuing. Instrumental convergence asks
which intermediate capabilities support many purposes. J² asks which judges
and distinctions support successful judgments. When both are evaluated by
the same actual decision consequences, they can select the same factual
representation. R6.16 is an implemented instance of that connection; the
evaluator, exposure contract and finite candidate vocabulary are explicit.

Useful information and its adoption remain separate. [R6.3](../../results/R6_shared_observation.md)
calculates the value of a reusable noisy observation to agents with partly
overlapping goals. When total benefit exceeds its price, binding sequential
cost shares provide a constructive agreement. A simultaneous contribution
game can still have a no-provision equilibrium. Thus shared value alone is
not a complete mechanism for paying for a common factual resource.

The underlying world can be identified more broadly when uses separate it.
[R6.8's supplement](../../results/R6_value_identification.md) characterizes
this with the rank of the Bellman equations supplied by known policy-value
judgments. For almost every positive three-state/two-action environment,
four specified policies under one known reward suffice; four are minimal
for that query interface. Exact rational witnesses prove this and a six-query/four-state extension;
a finite-precision bound exposes their conditioning cost.
This is a mathematical supplied-value composition, not an implemented
learner discovering all those judgments or a new claim of efficient control.

[R6.7](../../results/R6_capability_geometry.md) explains why a different
interface identifies a different object: optimal values over all goals
recover the convex attainable set. A named action that lies inside that
set can change without changing any optimal value. Judging that action's
counterfactual consequences can distinguish the worlds. This makes the
additional factual obligation constructive rather than stopping at
“successful action does not imply truth.”

## 5. Result map and scientific contribution

**P** denotes a supplied proof/reconstruction; **R** exact rational checks;
**N** numerical finite-model checks; **S** sampled synthetic learning.
None denotes independent expert confirmation or a real-agent study.

| Result | Main content | Evidence | Next obligation |
| --- | --- | --- | --- |
| [R6.1](../../results/R6_goal_judgment.md) | Goal coverage, common factual quotients and representation price | P/R | Broader endogenous task and concept families |
| [R6.2](../../results/R6_observed_shared.md) | Observed representation selection; price-coverage repair | P/R/S | Beyond full outcome feedback in this original panel; R6.16 supplies one selective repair |
| [R6.3](../../results/R6_shared_observation.md) | Shared information value and provision mechanism | P/R | Learned and strategically reported benefits |
| [R6.4](../../results/R6_plastic_priorities.md) | Retained priorities, revision, sorting and persistence | P/R/N | Origin and selection of the revision mechanism |
| [R6.5](../../results/R6_payoff_judgment.md) | Judgments learned from purchased payoffs; structured learner beats generic Exp3 here | P/S | Richer feedback and endogenous model classes |
| [R6.6](../../results/R6_bounded_subgoals.md) | Shared internal values improve bounded planning under different goals | P/R | Learned planning budgets and internal reward design |
| [R6.7](../../results/R6_capability_geometry.md) | Capability/value geometry and information comparison | P/R | Approximate sequential capability learning |
| [R6.8](../../results/R6_policy_values.md), [supplement](../../results/R6_value_identification.md) | Conditional policy/value reconstruction and identifying world values | P/R | Acquire queries economically; neural and runtime complexity |
| [R6.9](../../results/R6_option_pressure.md) | Weighted retargeting and cost-sensitive option preference | P/R | Empirically or endogenously justified goal weights |
| [R6.10](../../results/R6_strategic_values.md) | Valuable commitment and observability-dependent diversity | P/R/N | Richer mutations, learning and strategic signaling |
| [R6.11](../../results/R6_changing_goals.md) | Common histories, stationary laws and distributed populations | P/R/N/S | Endogenous environmental feedback |
| [R6.12](../../results/R6_unrepresented_values.md) | Survival-filtered values and actual action cloning | P/R/S | General feasible controls; R6.13 supplies a finite repair |
| [R6.13](../../results/R6_selection_learning.md), [supplement](../../results/R6_selection_sampling.md) | Exact and finite-trial survival learning with convergence conditions | P/R/N/S | Efficient trials, restricted resets and reducible worlds |
| [R6.14](../../results/R6_goal_context.md) | Context-dependent goals, side information and adequate encodings | P/R | Learn the exposure graph and choose probes |
| [R6.15](../../results/R6_value_use.md) | Useful continuation values, bonus fixation and correction cost | P/R/N | Learned potentials and changing tasks |
| [R6.16](../../results/R6_learned_concepts.md) | Paid-feedback shared/private representation learning and evidence reuse | P/R/S | Adaptive acquisition, change detection and new vocabulary |

The [source ledger](sources.md) records the primary comparisons and actual
read scopes. Bostrom and Turner supply the instrumental-convergence and
retargeting foundations; proper scores, decision calibration and Blackwell
comparison supply the decision/information bridge. State abstraction,
value-directed compression and value equivalence are substantial predecessors
of selecting representations for use. The [closing direct comparison](comparison.md) also credits recent
judgment-to-model and inverse-Bellman results, which are closer predecessors
for several conceptual claims than these older foundations. Reward design, shaping, reward-weighted
regression, evolutionary preference theory and risk-sensitive control supply
strong constructive alternatives for the other branches.

The contribution is principally **characterization and useful synthesis**:
typed mechanisms connect shared instrumental value, evaluating judges,
factual distinctions and acquired revisable priorities. Some finite
characterizations and combinations are developed here, but this cycle does
not establish publication priority for their most general forms. An exact
recoding, such as shaping versus Q initialization, is the same implementation.
Structured payoff decoding versus generic bandit learning, or greedy Perron
planning versus multiplicative copying, are genuinely different methods.
Their favorable and adverse comparisons inform the construction; “ordinary
methods tie” would not describe the scientific outcome adequately.

## Disposition and next direction

**Recommendation: advance W6 at the stated finite scope; keep it available
to recur.** The module has a constructive judgment-to-fact bridge, explicit
convergence notions, learned examples with costs, and informative conditions
for persistence and diversity. These support moving to W7 when the author
authorizes it. They do not finish M1, phase four or the broad philosophical
questions.

The highest-value next question is **which environments select the learning
and revision rules that make factual judgment useful**. Begin W7 with one
explicit inherited or transmitted controller and meta-rule, coupled to a
resource and survival/reproduction environment. Seek regimes selecting
accurate transferable judgment and flexible revision, paired with regimes
selecting coarse proxies, rigidity or diversity; characterize which feedback
and exposure changes separate them. Include an intervention removing the
original instrumental benefit to measure acquired persistence. This directly
addresses the author's proposed evolutionary route to terminal-like goals.

Preserve three further directions: economical acquisition of separating
judgments; adaptive retention of evidence when relevance and conditional
facts change separately; and a W1/W6 composition in which task partitions
and judge evaluation genuinely co-determine one another. R6.16, R6.8 and
R6.13 offer different starting points. None needs to be discarded merely
because the next module begins elsewhere.

## End-of-task self-review

The review record in [record.md](record.md) identifies the paths inspected,
checks and corrections. The main risks were equating agreement with factual
recovery, treating retained lucky outcomes as available controls, and
mistaking a stable instrumental priority for an immutable terminal end.
The constructive work specifies separating uses and purchased feedback,
copies actions under unchanged physical dynamics, and measures several
forms of persistence separately. Source comparisons also prevented treating
decision-directed representation or reward reweighting as newly invented
principles. Conversely, these comparisons were not used to dismiss the
positive synthesis. This is a self-review by the contributing model, not
independent confirmation or a guarantee against bias.
