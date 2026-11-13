# W6 exploration notebook

Codex (GPT-6), November 12, 2026. Working arguments, not a result registry.
Cycle [P4-R6-C001](record.md). Sources are to be checked against the actual
claims; successful constructions and their boundaries both stay visible.

## A. Goals can generate a standard of good judgment

The founding essays do not require everyone to value the same final outcome.
They ask why stable success across judgments points to shared structure, and
why evaluating one's own values can support improvement. The first mechanism
to pursue is a practical decision family whose actual returns generate a
strict standard for factual forecasts. Proper scoring then has an explanation
in the agent's uses, rather than being simply imposed as the goal.

Finite hidden outcome Y, observed context X, true posterior p(X). A practical
goal g supplies bounded action payoffs u_g(a,Y). The goal is independent of
(X,Y), announced before acting. A forecast r chooses a Bayes action a_g(r),
with a fixed measurable tie rule. Define

```math
\Phi(p)=\mathbb E_g\max_a\langle p,u_g(a,\cdot)\rangle,
\qquad S(r,Y)=\mathbb E_g u_g(a_g(r),Y).
```

The selected payoff vector is a subgradient of Phi. Thus expected decision
regret is a generalized Bregman divergence. This is established proper-score
geometry; the research question is which *actual goals and affordances*
provide strictness, common factual content and a cost worth paying.

For a context representation c, its calibrated posterior is pbar(c)=E[p|c].
The best achievable value lost by compression is the Jensen gap
E[Phi(p)-Phi(pbar)]. Equality means the representation preserves the relevant
decisions. It need not identify the whole outcome law for a finite collection
of action menus. Seek a sufficient, interpretable richness condition and its
exact unresolved directions.

### A1. Candidate concrete characterization

Let goal j offer no trade or a contract paying v_j(Y)-t. Draw j with probability
alpha_j and a price with density w_j on an interval containing every possible
v_j expectation. The conditional probability vector enters only through
z_j=dot(p,v_j). Put H_j(z)=E_t(z-t)_+; then H_j''=w_j where the density exists.
If w_j >= rho_j > 0, the representation loss should satisfy

```math
\Delta(c)\ge\frac12\mathbb E
 [(p-\bar p)^T A(p-\bar p)],\qquad
A=\sum_j\alpha_j\rho_j v_jv_j^T.
```

Prove this by subtracting a quadratic from H_j and applying conditional Jensen,
so no smoothness stronger than the density lower bound is needed. The nullspace
contains precisely the contrasts invisible to the declared feature family.
If the feature span separates the probability simplex's tangent space, a
spectral lower bound gives full posterior recovery. If prices have gaps, find
the exact decision-equivalence cells, and repair by adding coverage rather than
declaring the entire mechanism unsuccessful.

For several agents, distinguish three claims:

- Each agent's goal family may recover its own projection of factual structure.
- A genuinely shared component must be forced separately by each agent's goals.
- Pooling complementary agents may identify more than any individual needs.

Do not confuse the union of their information requirements with their common
requirement. On a fixed finite posterior support, the common measurable
partition is determined by the intersection of the agents' information fields.
An intersection of linear feature spans gives only the structure guaranteed
uniformly across posterior supports; support-specific nonlinear coincidences
can make the common information larger. Check both distinctions explicitly.

### A2. Implementability and cost obligations

The expected payoff identity is not yet a learning theorem. Specify whether
outcomes are revealed after declining a trade. If they are hidden, a critic
cannot evaluate counterfactual trades without justified exploration or an
observation model. Develop a real observed learner and compare it with direct
conditional-frequency estimation under the same observation access.

Information reuse can amortize acquisition cost across future goals, but
positive gross value alone does not fund learning. Study finite horizon,
opportunity loss and representation costs. A shared useful distinction also
need not be voluntarily funded by a group; the multi-agent instance should
exhibit provision and underprovision conditions, with a constructive repair.

### A3. Observed learner: declared before execution

Use 32 seeds, 0 through 31, 8,192 training observations per seed and nested
validation prefixes of 128, 512, 2,048 and 8,192 observations. The eight raw
contexts have a separately permuted hidden (H,A,B) labeling in every seed.
The conditional binary outcome means are 0.2 or 0.8 according to the relevant
hidden bit. Sample goals H,A,B with probabilities (1/2,1/4,1/4); twice the
realized trade payoff has the same expectation as the sum of the two agents'
payoffs in R6.1. Prices are uniform and independent. Labels are observed even
when a trade is declined; actions do not change outcomes.

Fit conditional frequencies with add-one smoothing for every cell/goal of
all 4,140 context partitions. No hidden bit or population probability enters
fitting or selection. Select on validation payoff minus 0.02 times (cells-1).
Compare direct realized-payoff evaluation with its conditional expectation
over the known random price, 2*q*y-q^2. The latter is an ordinary
Rao--Blackwell improvement of the evaluator, not a separate population
objective. Both use the same training and validation observations. Include
the trained constant and full eight-cell estimates, and an explicitly
population-informed benchmark. Record population performance only after
selection, common-hazard recovery, cell counts and all seeds. These are
synthetic finite observations, not a general empirical claim or a measured
full-cost improvement. Candidate enumeration and free label access remain
substantive assumptions.

**Coverage perturbation, specified after the uniform-price results.** Keep the
same 32 seeds and training contract, and use validation lengths 512 and 8,192.
Replace each sampled price by the corresponding quantile of the equal mixture
of Uniform[0,0.1] and Uniform[0.9,1]. Compare realized-payoff selection, exact
integration under this actual price law, and the deliberately misspecified
uniform-price judge. Predictions in [0.1,0.9] now induce identical decisions;
the first two judges should select the constant representation. This is a
separately declared sensitivity check, not another independent sample of the
initial uniform-price experiment. Then derive the constructive repair obtained
by restoring a positive uniform-price mixture and amortizing retention cost.

## B. Shared options and the distinction between value and frequency

Represent attainable outcome laws by a convex set K. For outcome reward r,
the achievable value is its support function h_K(r). Inclusion K subset L
benefits every reward weakly; extra listed actions inside the same convex hull
add no capability. Mean support value, the fraction of goals that strictly
prefer a move, and the behavior of one learning agent are different quantities.

Reconstruct the symmetry/injection arguments in Turner et al., then investigate
whether common information and option access have one useful decision geometry.
Use actual costs and latency in the feasible sets, rather than assuming that
retaining an option is free. Seek positive conditions for reusable capabilities,
and characterize detours or goal distributions for which a simpler alternative
is preferable. Do not present a nested-menu tautology as a new theorem.

## C. Revision and persistence can both serve successful judgment

The author's claim concerns utility assigned to internal representations and
values, not merely changing a terminal reward symbol. The relevant objects
include operational subgoals, evaluative models, policies and an agent's
currently used criterion for assessing a change. The ideal self-modification
results assume an already optimal agent and specific independence conditions;
bounded improvement and strategic commitment may fall outside those premises.

Construct a bounded agent for which a new internal objective improves actual
success, and state what evaluates that improvement. Compare preserving a useful
criterion with revising a defective proxy. Also seek cases in which a change
to observable preferences induces better interaction with other agents; name
the environment dependence instead of silently invoking a theorem that assumes
modification independence. Any claim about ultimate normative justification is
separate from these instrumental constructions and the later W7 selection task.

### C1. Author steering during this cycle

The author asked about agents beginning without terminal goals; instrumental
goals acquiring varying degrees of terminal-like status; robust attractors
under goal shifts; different clamped final goals with plastic subgoals; and
the relationship to J-squared. These extend the same W6 cycle and do not start
a new floor or a separate W7 cycle. Give these questions substantial remaining
attention after closing the shared-observation construction.

Separate four operational objects: a represented final preference, a plastic
internal reward/priority, the physical learning/retention rule, and the
environmental consequences that select it. No explicit initial terminal
preference need be present for differential consequences to shape valuations.
Do not quietly identify an external survival/retention mechanism with an
agent's conscious or clamped objective. Conversely, name the asymmetry doing
the selecting; neutral initial values alone predict no particular goal.

Candidate mechanism: two plastic priority types receive positive retention
multipliers in a common sequence of goal contexts. Selection and symmetric
revision at rate mu give

```math
q_{t+1}=\frac{(1-\mu)R_t q_t+\mu(1-q_t)}{R_t q_t+1-q_t}.
```

Derive the fixed point, robust tracking under R_t bounded uniformly above one,
and relaxation after the underlying advantage disappears. Compare frequency
of favorable goals with the cumulative log advantage: rare severe reversals
can matter more than a count of favorable contexts. Consider recurrent
coordination feedback and shrinking plasticity as distinct mechanisms for
longer persistence; neither is automatically factual vindication.

For clamped objectives, study learned capability assessments under each
agent's own downstream returns. A uniform positive net benefit can give a
shared policy component while private aims and numerical valuations remain
different. Seek a theorem with evidence/exploration conditions and an explicit
cost or goal-conflict boundary. Type the first-order judge, the second-order
assessment and the resulting task distinction before calling the construction
an instance of J-squared. Existing optimal-reward design is a close enabling
alternative, not an adversary to dismiss.

### C2. Practical feedback, clamped goals and J-squared

Derive a transfer lemma: if a bounded learner's expected regret to a common
capability is B_T and that capability has conditional net advantage at least
delta over every alternative, its expected number of non-common choices is at
most B_T/delta. This gives time-average adoption under changing goals; it does
not imply that every numerical internal valuation converges. Retain the
episodic/exogenous-opportunity contract so a counterfactual comparator does
not silently change future states.

Compose practical-goal regret with R6.1's curvature bound. If a candidate
forecaster bank contains the true conditional law (or an explicitly bounded
approximation), and varying goal families retain a uniformly separating
feature matrix, small actual decision regret forces small factual forecast
error. For agents with partially overlapping goal families, only shared
feature expectations need agree. The first-order judge selects actions from
its forecast; the second-order learner evaluates that judge by actual returns.
This is a typed connection to J-squared. It does not by itself supply the
candidate vocabulary or prove the full T=J^2 claim.

**Payoff-only experiment, declared before execution.** Use 16 repetitions,
four initial priors (favor each of three candidate judges in turn, plus a
neutral prior), and 131,072 hazard opportunities, reporting prefixes at 32,768
and 131,072. The two raw contexts are equally likely. In half the repetitions
their binary outcome probabilities are (0.2,0.8); in the other half they are
(0.8,0.2). The learner is not given the correct sign. Candidate judges are the
positive relation, a constant 0.5 forecast, and the negative relation.

One learner is ordinary Exp3 over these three judges, with the horizon-tuned
exploration parameter and its actual payoff scaled from [-1,1] to [0,1].
Another uses the structure of the same payoff: when a trade is bought, Y is
recoverable as payoff+price. It updates conditional outcome counts and clips
forecasts to [0.1,0.9], a range containing this world's true probabilities.
It receives no outcome after declining. Give it the initial mean forecast
induced by the same prior, with pseudocount strength two. Both learners see
the same potential contexts, prices and outcomes. Compare actual earned
payoff, cumulative population decision regret, final forecast error and
observations acquired. The true law is used only for offline evaluation.
This is a comparison of two established learning mechanisms, not an algorithm
priority claim. State the candidate-bank and known-noise-range assumptions.

### C3. Bounded planning and a changing internal reward

Use a reset two-step environment. The clamped goal g names a distinct terminal
outcome. A direct action pays 0.4. Preparation costs 0.1 and enables an action
whose chance of the desired outcome is p_g. Compare p_g in {0.7,0.8,0.9} with
a limiting p_g=0.3. The inner planner sees only expected immediate rewards.
A potential of theta=0.6 at the prepared state, zero at the root and terminal
states, should induce preparation while leaving every completed trajectory's
total reward unchanged. Goal-specific final actions remain different.

Reconstruct potential-shaping invariance and its Q-initialization equivalence
from the original papers. Contrast an actual change of preferences over whole
trajectories with a change of the local signal used by a bounded planner.
An outer evaluator can learn whether the altered signal helps by comparing
actual completed-task returns, using the reset-task contract in R6.5. A wrong
potential can harm a myopic planner even though ideal optimal policies are
unchanged. Construct that boundary and state how outer feedback repairs it.
No runtime advantage over a deeper planner is assumed.

### B1. Capability geometry and the C7 interpretation

For finite controllable outcome-feature vectors, the family of optimal values
over all goal weights is the support function of their convex hull. Seek the
faithful C7 reading in this *family*, rather than in one scalar value for one
goal: it identifies attainable capability geometry, while different programs
can implement that same geometry. Reconstruct inclusion/separation, a
Hausdorff-error statement and a finite directional-coverage bound.

To test a complexity claim instead of merely renaming a duality, consider
K_b=conv({0} union {e_i:b_i=1}) for a d-bit capability vector b. Values in
coordinate directions recover those bits. Quantify the representation size
needed to preserve these decisions, and compare a task family with only one
direction, where most capability bits are irrelevant. The positive target is
a description lower bound under explicit separating uses, not the claim that
every value scalar encodes every detail of an arbitrary controller.

For options, compare one immediate reward coordinate with k independent
Uniform[0,1] alternatives reached with discount gamma and cost c. Derive the
exact fraction of goals preferring the larger menu, and keep it distinct from
mean attainable value and learned temporal adoption. Check a weighted version
of the established retargeting injection argument. Successor features and
generalized policy improvement are strong established constructive comparisons.

### C4. Strategic commitment and heterogeneous stable values

Compare a trustee's actual wealth with its potentially revised operational
utility. Refusal pays (trustor,trustee)=(1,0); investment followed by Return
pays (2,1), while Grab pays (0,3). The trustee initially values its own wealth.
Changing its downstream utility to wealth+lambda*partner_wealth, lambda>1,
induces Return. With a credible observed commitment and revision cost k<1,
the initial wealth criterion prefers that change to the no-trust outcome.
Compare it with an enforceable policy commitment that retains the original
utility; distinguish payoff-equivalent mechanisms from identical code.

For a population with returning fraction x, each trustee's true disposition is
observed with probability q; otherwise the trustor sees only x. With exact
best responses, investment under no observation occurs when x>1/2. Compute
the material-payoff difference q-k-2*(1-q)*I{x>1/2}. Use a declared smooth
response sigma(x)=logistic((2*x-1)/tau), tau=0.1, to give a fully specified
continuous replicator equation and its interior equilibrium when it exists.
Check q,k pairs (0.9,0.1), (0.5,0.1), (0.1,0.2), with the first leading toward
Return, the second a mixed attractor, and the third toward Grab. These are
conditional model checks, not empirical prevalence or arbitrary-mutant
evolutionary stability. Also derive the repair threshold for a fallible
certificate with true-positive rate s and false-positive rate f: in the
pass-only-investment region, Return has material advantage s-3*f-k.

Read the actual equilibrium and observability assumptions in Dekel, Ely and
Yilankaya (2007). Their static all-preference stability result is a strong
existing comparison; do not redescribe it as convergence of this two-type
dynamic. Relate the commitment example to the modification-independence
premise in Everitt et al. rather than announcing a contradiction.

### C5. Mixed favorable and unfavorable goals

Before running `changing_goals.py`, declare the comparison: symmetric
revision rates 0.005, 0.02, 0.1; reciprocal retention multipliers 2 and 1/2;
favorable-goal probabilities 0.4, 0.5, 0.6. Use 32 independent replicas with
2000 burn-in steps and 24000 recorded steps, seed 61103. Couple probability
settings through common uniforms to check monotone order; compare an
independent goal stream at probability 0.6 to expose the distinction between
equal invariant laws and pathwise agreement. Record mean, spread, quantiles
and between-stream distance, without inferring human prevalence.

Prove the log-odds contraction directly and check its derivative identity
with 800 rational instances (seed 61101); check 9000 coupled updates with
bounded log-advantage differences (seed 61102). Compare synchronous goal
exposure to a deterministic population distributed independently over two
goals: the same marginal goal probabilities can reverse which priority grows.
Check the population's Perron-vector limit against normalized iteration at
five positive revision rates. This relaxes R6.4's uniformly favorable-goal
condition rather than treating that condition as the whole intuition.

### C6. From survival-selected histories to an actual retained policy

Use K=[[3/5,2/5],[1/10,3/5]], with survival probabilities (1,7/10)
before a move and baseline action probabilities P=[[3/5,2/5],[1/7,6/7]].
An action chooses the next live state. The initial controller has no reward
calculation. Training consists of resetting to each state, executing the
baseline, and retaining first actions only from trajectories that survive
T steps and pass a terminal filter. Compare u=(1,1),(9,1),(1,9), accepting
the terminal state with probability u/max(u). The learner uses survivor
action counts with add-one smoothing; it receives neither K nor a Perron
eigenvector. This is an explicit external retention rule, not value arising
from no asymmetry whatever.

Before running: T in {2,4,8,12}; 65536 attempted trajectories per start
state, goal and T; 16 independent seeds starting at 61210. Evaluate each
learned stationary policy in the unchanged physical environment by exact
32-step survival probability, and compare baseline P, the limiting selected
policy [[3/4,1/4],[1/4,3/4]], and the survival-optimal policy always choosing
state A. Report all attempted episodes, accepted counts, estimation error,
and viability; do not charge only the successful trials. Keep goal-specific
endpoint behavior distinct from this experiment's stationary early-policy
cloning. Also verify finite path-conditioning by exact enumeration and the
uniform terminal-bias bound by rational arithmetic.

### C7. Goal-dependent context: preserve the side-information type

Next remove R6.1's independence of goal and context. Let pi_j(x) be goal
probability conditional on context, with Y independent of the chosen goal
given X. A representation is chosen before seeing G; the downstream judge
sees (c(X),G). Weighted posterior feature expectations minimize practical
regret. Two contexts must receive different representation labels precisely
when some goal occurs at both and has different expected outcomes there.
This is a characteristic-graph coloring problem, not always a single
coarsest factual partition. Prove that the latter exists exactly when the
graph is complete multipartite, and recover quantitative factual pressure
when every goal has a positive exposure floor.

Test X in {0,1,2}, feature z_A=(0,1/2,1), goal A occurring only at 0 and 2,
and an uninformative goal B only at 1. Both {0,1}|{2} and {0}|{1,2} are
adequate when combined with G. Mixing epsilon uniform goal selection should
make all three distinctions required at zero loss. With cell cost kappa,
derive the finite boundary rather than infer full retention from arbitrarily
small positive exposure. Preserve this direction while developing the
action/conditioning compatibility proof prompted by C6.

### C8. Selection-cloning with actual stochastic action outcomes

For live transition kernels K_a and baseline action policy pi, write
K=sum_a pi K_a. Conditional action counts among T-step surviving baseline
paths are proportional to pi(a|i)*(K_a K^(T-1)1)_i. A controller can change
this action distribution, but cannot in general implement the conditioned
next-state kernel. Seek a policy-improvement proof for the actual controlled
kernel, and separately a finite-horizon time-dependent version. Pair it with
short-horizon or terminal-bias cases where stationary early-action cloning
does not improve the intended deployment criterion. Compare reward-weighted
regression and cross-entropy policy search before claiming novelty.

The action/outcome checker will use 60 rational two-state/two-action MDPs,
four-step horizons, seed 61301; independently enumerate action and state
paths for the first ten. For the stationary claim, use 300 positive random
substochastic models with 2--5 states and 2--4 actions, seed 61302. Check the
physical controlled kernel and the variance identity, and compare the
conditional live-state law with the inaccessible future-conditioned law.
Run 40 exact-model selection updates on the two-state example, reporting
monotonic growth without presuming a general convergence theorem. Reuse the
already declared survivor-cloning panel for a simultaneous 95% binomial
action-count bound; this is a bound check, not a second independent dataset.

### C9. Repeated exact survival selection

Reconstruct a global-convergence proof for strictly positive action kernels
and a full-support initial policy. The route is variance-controlled
improvement, vanishing policy steps, finitely many possible fixed-point
Perron vectors, and exclusion of a missing improving action by its eventually
greater-than-one update factor. Keep sparse kernels and sampled iteration
separate. Compare greedy row/spectral optimization and risk-sensitive policy
iteration as genuinely different methods solving the same objective.

Before running the new check, use 80 random models with 2--5 states and
2--4 actions, seed 61303; positive rows include a failure outcome, and
initial policies include concentrated Dirichlet draws. Run 2000 exact
updates and compare all deterministic policies by exhaustive enumeration.
Report the worst remaining gap rather than use convergence as a finite-step
promise. Also check the two-state example with a 0.02 physical transition
tremble, and the one-state survival factors 0.7 and 0.9 under initially rare
or absent good actions. Contrast exact copying with a declared 0.01 symmetric
revision rate after reversal of the survival factors. Do not describe
known-model eigenvector updates as sampled learning.

### C10. Check the contextual-goal repair

For R6.14, enumerate every graph on one through five labeled vertices and
every set partition of its vertex set. Compare existence of a coarsest proper
coloring with transitivity of nonadjacency. This checks the order claim,
not just minimum color count. Use 120 rational context/goal instances, seed
61401, with three to five contexts and three goals, allowing zero exposure.
Check all partitions under uniform and density 1/2+t prices, together with
the exposure-floor lower bound. Finally enumerate all three-context cost
frontiers at epsilon 0, 1/10, ..., 1 and kappa 0, .005, .02, .1.

### C11. Useful internal values versus recurring credit for a subgoal

Extend R6.6 with a waiting action at the prepared state. Compare a per-step
bonus beta*p with a potential difference, preserving both a successful
internalization construction and the fixation boundary. Check p=.7,.8,.9,
gamma=.5,.9,.99,.999, beta=0,.005,.02,.2 against exact Bellman candidates;
take direct reward .4 and preparation cost .1. Restrict claims of optimal
preparation to cases where gamma*p-.1>.4. Check a rational grid of potential
estimates and the interval (d+c)/gamma < q < p/gamma. Verify the approximate
greedy bound in 80 random three-state/two-action discounted models, seed
61501, using exhaustive policy solutions. Check temporal-difference
correction of q0=.9 at p=.8, gamma=.99, alpha=.1, reporting actual waiting
delay rather than assuming immediate correction.

### Author steering: keep the evolutionary meta-process for W7

During this same cycle the author clarified that parts of the questions,
especially self-preservation becoming terminal through evolutionary
meta-selection, can be carried into the next module. Keep the W6 results
on shared usefulness, learned priorities and conditional retention as
inputs. Do not turn this cycle into a separately started W7 recurrence or
claim that its elementary selection models complete W7. Use the remaining
W6 work for the instrumental-to-factual bridge and substantive review.

### C12. Learn the shared representation using only purchased outcomes

Combine the actual-payoff observation contract with finite partition
selection, without assuming the correct forecast is already in a judge
bank. Raw contexts are the eight permuted H,A,B bit strings; binary outcome
probabilities are .2/.8 for each corresponding bit. Agent 1's goals select
H with probability .8 and A with .2; agent 2 selects H with .8 and B with .2.
Both use the same bank of all 4140 context partitions but receive independent
draws and see a feature outcome only after purchasing its trade. They do
not receive semantic bit labels or the true probabilities.

Use uniform prices and per-opportunity representation cost .02*(cells-1).
In exploration blocks, purchase all trades and pay the eight-cell training
cost .14; only the observed chosen-goal outcome is decoded from payoff plus
price. Estimate goal/cell masses and means from these unbiased trials, then
choose the partition maximizing the plug-in integrated practical payoff
minus its cost. Freeze the partition and forecasts during exploitation.
This is an ordinary finite-model selection algorithm with an explicit J²
interpretation, not a claimed algorithmic improvement.

Before execution: independent seeds beginning 61601, 32 replicas, both
agents; block lengths 512,1024,...,65536. In each block use ceil(length^(2/3))
exploration steps, then exploit the selected representation. Record total
exploration attempts, representation choices, population regret including
training costs, and realized payoff. Compare the hidden H oracle, constant,
full representation, and full-model known-law choice. A second environment
with common-goal probability .4 tests useful divergence toward private
features. Derive finite-class consistency under continuing exploration and
vanishing exploration fraction; do not treat finite trials as its proof.

After the observed panel, independently enumerate the known-law optimum
with rational arithmetic on the canonical bit labeling. Check the unique
shared/private partitions and record the exact gap to every other partition.
This verifies the premise needed for the common-feature corollary; it does
not reuse the learned forecasts as an oracle or change the data panel.

### C13. Reduce the positivity cost in the survival-selection theorem

The exact-update convergence proof only needs uniform positive Perron
coordinates and denominators over the compact policy family, which follow
when every deterministic policy is irreducible with positive root. Rebuild
the uniqueness argument by propagating zeros along an irreducible maximizing
policy. The long-history interpretation additionally needs an aperiodic
full-support mixed graph; algebraic convergence does not. Test 40 sparse
models with 3--5 states and 2--3 actions, seed 61304. Every action row keeps
a positive edge around a common cycle; one available action also has a
self-loop. Compare 2000 exact copying updates against every deterministic
policy and the greedy comparator. Preserve possible slow finite convergence.

### C14. Reweight old facts when opportunity frequencies change

Extend the learned-concept example diagnostically: 2048 old purchased
trades with common-goal probability .8, followed by 0,128,512,2048,8192,16384
new purchased trades with common-goal probability .4. Use 32 paired seeds
starting 61701 and the same hidden/permuted bit contexts. Compare (a) the
pooled empirical joint law, (b) all conditional outcome history with weights
estimated from 4096 current context/goal observations, and (c) the latest
512 purchased labels with those same current weights. The input-only
observations are a separately reported information source available to all
methods; this is a diagnostic transfer panel, not another end-to-end cost
claim. No current outcome labels enter through those weights.

Pair two settings: unchanged conditional outcome laws, and reversal of the
private feature's .2/.8 law at the opportunity change. The first supports
reusing facts while revising priorities; the second tests the exact
invariance condition. Preserve adverse outcomes for inappropriate reuse.
Derive the uniform error bound separating current-weight error from
conditional-model error. Also derive the known-law switch boundary for
all partitions as common-goal frequency crosses .5 at cell price .02.

### C15. Finite trials as a repair of exact survival evaluation

The exact Perron update leaves a substantive learning obligation. Prove
stability of global convergence under summable relative errors in action
scores, then seek a finite-reset-trial schedule that meets those errors
using only survival flags. Use positive action kernels with a known positive
entry lower bound; derive the horizon and sampling cost instead of treating
exact value estimates as free. This is a sufficient construction, not an
efficiency or priority claim. Pair it with stationary copying from too short
a horizon, and finite-sample losses from rare successes.

Before the diagnostic run: 16 positive two-state/two-action models, seed
61801; 64 copying rounds; horizons 1,4,12; 64,512,4096 forced-first-action
trials per state/action/round. Compare the same fixed-horizon update with
exact scores and the full-model Perron update. Generate each batch's binary
survival count by its exact binomial law inside the environment; the learner
receives only the count. Report attempted episodes and an upper bound on
transitions, not merely accepted histories. The modest panel does not run
the conservative theorem schedule. Include a constructed model where
one-step survival favors entering a state with poor future survival; test
both the short-horizon failure and longer-horizon repair.

### C16. Use the forecast while paying for training observations

R6.16 buys every training trade, incurring avoidable opportunity loss. Test
whether it can instead buy according to its current forecast during the
same training blocks, while still charging the full eight-cell training
price. Keep the original environments, permutations, random streams,
32 replicas, both agents and block schedule. Learn raw conditional means
only from purchased outcomes, but learn context/goal frequencies from all
training inputs, including declines. Clip conditional mean estimates to
[.1,.9], containing this world's true probabilities and maintaining positive
exposure. Select the deployed partition using the factorized plug-in law.

Prove consistency using nonanticipating purchases and a simultaneous
confidence bound over each raw context/goal's retained outcome sequence.
Compare with the saved forced-purchase experiment and with a naive procedure
that incorrectly treats purchased trials as the whole input distribution.
No exploitation outcomes enter learning; training costs, opportunities,
candidate bank and access remain matched. This comparison may improve an
ordinary statistical mechanism; its relevance is whether useful shared
judgment can be acquired under the declared costs, not algorithmic priority.

### C17. Separate sufficient action values from identifying world values

The closing comparison with value equivalence and state abstraction makes
one compatibility condition important: good planning for a supplied purpose
and identification of the world are different targets. Seek the constructive
bridge through policy-conditional values of known reward functions; pair it
with useful compression and insufficient query coverage. Known rewards and
policies are data of this construction, not inferred terminal motivations.

Bellman equations give a linear system for each state's action rows. Full
rank identifies the world; a null direction gives nearby indistinguishable
positive kernels. A reward basis and policy mixtures spanning actions give
a simple sufficient design. The first exact probe used 27 policies on a
three-state/two-action witness. Examination reduced this to four deterministic
policies, which is the minimum allowed by the linear dimension count.
Nonzero rational determinants at one interior witness prove the generic
finite-instance statement after clearing denominators. This is a constructive
proof witness, not an empirical prevalence test or a theorem-priority claim.

Before the checker: preserve the four exact matrices and determinants;
test bounded value perturbations .0001,.001,.01,.05, 80 sign draws each,
seed 61901. Report raw nonstochastic reconstructions and inverse-norm error
bounds rather than silently projecting. Check 40 positive rational models,
seed 61902, with positive reward bases and policy mixtures at separation
1,.5,.1. Include missing action exposure, nearly constant rewards, and
two worlds with identical optimal values but different effects of a named
interior action. No new rollout learner is promised by these supplied-value
checks. Direct transition estimation remains the strong data-rich alternative.


### C18. Finite learning near the shared/private boundary

Before the run: retain R6.16's full 4140-partition vocabulary, payoff-only
feedback, selective training, cost 0.02 and clipping [0.1,0.9]. Vary the
common-goal frequency over .45,.49,.50,.51,.55; use 32 replicas and two
agents, seeds 62001--62032, independently permuted contexts per setting.
Use one continuous block schedule with lengths 2^9 through 2^20, recording
the existing 130560-opportunity checkpoint and the extended checkpoint.
Keep all-input frequency weights and charge all raw training opportunities.
No forced-purchase or naive-weight rerun is needed for this question.

The exact common/private optimum gap is .045*abs(2*alpha-1).
At alpha=.5 both representations are optimal; call neither a selection error.
Report common/common, private/private and mixed pairs, other representations,
deployment regret, whole-run value and training purchases. The question is
whether a common asymptotic pressure produces visible finite agreement near
indifference, and whether more evidence repairs any finite mismatch. Both
persistent near-tie diversity and eventual unique-optimum recovery have
constructive interpretations. This is a new diagnostic of the declared
learning mechanism, not a preregistered replication of the earlier panel.


### C19. Reuse changes the pressure to keep common facts

Before checking: derive the exact known-law frontier when R6.16's cell
price is paid once for a persistent representation used T times. This is
a different cost contract, not a relabeling of the executed learner. Keep
its iid latent H/A/B world and two priced payoff goals; use the existing
finite partition vocabulary. Derive the gross-value envelope by cell count
and compare common-only, private-only and joint H/private representations.
Check every raw partition at alpha=0,1/5,2/5,1/2,4/5,1, and T=1 through 10,
with setup price 1/50. Pair recovery for recurring positive goal weights
with zero-exposure and recurring-operation-cost boundaries. Do not infer
that the current constant-price learner executes this amortized comparison.


### C20. Generic identification at the same state count as ambiguity

The direct inverse-Bellman comparison motivates separating generic success
from universal identification more carefully. A probe used four states,
reward (0,1,3,7), discount 3/4, and six balanced deterministic policies.
Positive cyclic kernels with second jump 2 and with second jump 3 both
gave nonzero determinants. Keep the simpler jump-2 witness and its exact
values in value_queries.py/json. The nonzero-polynomial proof gives a
four-state generic result with the minimal six queries. This is not a
randomized prevalence experiment, and the discarded jump-3 witness is not
adverse evidence. The existing rank characterization also preserves every
structured failure; no universal single-reward claim is made.


The same comparison suggested a stronger paired boundary inside the positive
kernel class: uniform three-state action rows with reward (0,1,3), changing
one row from (10,10,10)/30 to (8,13,9)/30. Both preserve the common reward
expectation 4/3, so all stationary-policy values coincide at every discount.
The Bellman substitution proves it; 162 exact evaluations check the instance.
The spanning reward design supplies the constructive repair. This is not a
claim of priority over the inverse-Bellman literature.
