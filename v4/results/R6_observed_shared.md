# R6.2 Successful use can select a shared distinction from observations

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** finite learning argument and a predeclared synthetic experiment,
followed by a separately declared price-coverage perturbation.

The [goal-geometry construction](R6_goal_judgment.md) says which judgments
would be useful if the world were known. Here the learner receives outcomes,
not the hidden grouping of contexts. Evaluating its candidate judgments by
their practical returns selects the common hazard distinction when that
distinction is worth its retention cost. The same construction explains when
an imposed accuracy score would instead reward unnecessary detail.

This advances the C1/C2 mechanism and a bounded C3 connection: useful judgment
can reveal factual kinds through observation. The candidate vocabulary is
finite and supplied. The experiment does not generate an unrestricted ontology.

## 1. What the learner observes and chooses

There are eight equally frequent raw context labels. Their hidden meanings are
the eight triples (H,A,B) of binary variables, with a fresh permutation of the
labels for each run. Two agents care about (H,A) and (H,B), respectively. A
goal selects the shared or private outcome with equal probability for each
agent. The relevant binary outcome has probability 0.2 or 0.8 according to
the corresponding hidden bit. Thus H denotes a hazard-probability distinction,
not an outcome that the learner can predict without error.

Equivalently, sample j in {H,A,B} with probabilities (1/2,1/4,1/4) and evaluate
twice the payoff of a trade on outcome Y_j. A price t is independent and
uniform on [0,1]. A forecast q buys exactly when q>t. The realized payoff is

```math
Z(q,Y_j,t)=2\mathbf 1\{q>t\}(Y_j-t).                 \tag{L.1}
```

This normalization gives the sum of the two agents' expected payoffs per use.
The learner sees the raw context, j, t and Y_j. It observes Y_j even after
declining; its action does not change the outcome. Hidden bits and true
conditional probabilities are available only to the generator and the final
population evaluation.

The candidate family is every partition of the eight labels: 4,140 candidates.
For each cell and goal, fit the observed binary frequency with add-one
smoothing. Use independent validation data to choose the candidate with the
largest estimated practical payoff minus 0.02 times (number of cells minus
one). The charge is a declared retention price. Training observations, search,
raw-input access and elapsed computation are not monetized in this comparison.

Two validation judges assess exactly the same population objective:

1. **Realized-payoff judge:** average (L.1).
2. **Integrated-payoff judge:** average its conditional expectation over the
   known random price, 2*q*Y_j-q^2.

The second is ordinary Rao--Blackwellization. It uses known environmental
randomization to remove price noise; it does not receive hidden probabilities.
It is a different finite-sample evaluator, not an independent rival to the
population objective. Squared-error evaluation differs from this integrated
payoff by an outcome-only term. That identity explains why the familiar score
is appropriate in this environment.

## 2. A finite guarantee and an eventual recovery statement

**Proposition 1 (finite validation).** Condition on the training sample and
let M be the number of fitted candidates. Suppose independent validation
observations are identically distributed, the judge is unbiased for each
candidate's actual expected payoff, and its values lie in an interval of width
R. Let k(c) be a fixed, known candidate charge. With probability at least
1-delta, the validation-selected candidate has population net value at least

```math
\max_c\{V(c)-k(c)\}
 -2R\sqrt{\frac{\log(2M/\delta)}{2N}}.                 \tag{L.2}
```

*Proof.* Hoeffding's inequality and a union bound give simultaneous deviation
at most R*sqrt(log(2M/delta)/(2N)) for every validation mean. On that event,
compare the selected candidate with the population-best fitted candidate and
apply the deviation bound once to each. The deterministic charges cancel from
the deviations. QED.

Here R=4 for the realized judge and R=2 for the integrated judge. This is a
conservative guarantee against the best **trained** candidate, not against a
forecaster supplied with the true law. At the experiment's sample sizes it is
too loose to certify exact hazard recovery; the observed counts below are
finite experimental evidence, not a consequence of a tight certificate.

**Proposition 2 (finite-vocabulary consistency).** Suppose every raw-context/
goal pair has positive probability, training consists of growing prefixes of
an iid stream, independent validation sizes tend to infinity on a fixed
schedule, and the population-optimal partition is unique with a positive
net-value gap. Then the selection error probability tends to zero. For a
schedule with summable validation error bounds, selection is eventually
correct almost surely.

*Proof.* The strong law gives convergence of all finitely many cell/goal
frequency estimates; smoothing vanishes. Expected payoffs converge because
the integrated payoff is continuous in q. With finitely many candidates the
convergence is uniform. The positive optimality gap therefore persists for
all sufficiently large training samples. Apply (L.2) to the validation sample.
For the almost-sure claim, choose validation sizes so that the probabilities
of deviations exceeding a fixed fraction of the gap are summable and apply
Borel--Cantelli. QED.

Positive exposure, feedback after declining and continued sampling are
assumptions. This result does not yet show that a self-interested agent will
pay to maintain them; [R6.3](R6_shared_observation.md) treats one provision
mechanism separately. [R6.16](R6_learned_concepts.md) later implements
paid, selectively observed learning under a different declared experiment.

## 3. The observed result

The [pre-execution contract](../notebook/P4-R6-C001/explore.md#a3-observed-learner-declared-before-execution)
fixed 32 seeds, 8,192 training observations and the four nested validation
sizes below. The exhaustive population benchmark has a unique optimal
two-cell partition: H. Its net value is 0.275. Hidden context permutations
are never passed to fitting or selection.

| Validation observations | Realized judge: exact H, out of 32 | Integrated judge: exact H, out of 32 | Realized judge: mean population net value | Integrated judge: mean population net value |
| ---: | ---: | ---: | ---: | ---: |
| 128 | 0 | 11 | 0.248091 | 0.261615 |
| 512 | 5 | 31 | 0.259893 | 0.274558 |
| 2,048 | 25 | 32 | 0.271253 | 0.274834 |
| 8,192 | 32 | 32 | 0.274834 | 0.274834 |

The same-data constant and full eight-cell frequency estimates have mean
population net values 0.249905 and 0.199526. The full estimate loses on the
declared retention charge, despite better gross information. The 128-observation
realized judge slightly underperforms the constant baseline: searching many
noisy judgments can select a costly mistake. Integrating known price noise or
collecting more validation evidence repairs this case. Neither improvement is
a claim that more information is inherently bad or that all search costs have
been repaid.

The [implementation](../notebook/P4-R6-C001/observed_goals.py) stores
[every seed and selection](../notebook/P4-R6-C001/observed_goals.json).
It also compares its accelerated validation calculation with literal realized
payoffs and integrated scores in 512 independent-formula checks. The table
is descriptive of the specified synthetic world; seeds are not real populations.

## 4. Goal coverage and cost jointly determine useful detail

Now replace the price law by an equal mixture of Uniform[0,0.1] and
Uniform[0.9,1]. Every calibrated prediction here lies between 0.2 and 0.8.
Every such forecast therefore makes the same actual trades. Retaining a
finer partition has zero gross decision benefit.

The separately specified [coverage check](../notebook/P4-R6-C001/coverage_check.py)
keeps the same training contract and compares the actual-payoff judge,
integration under the **actual** price law, and deliberately incorrect
uniform-price integration. At 8,192 validation observations, both correct
judges select the constant representation in all 32 runs, with net value
0.45. The misspecified uniform-price judge selects H in all 32, with actual
net value 0.43. It pays for a distinction the current goals do not use.
The [saved results](../notebook/P4-R6-C001/coverage_check.json) preserve the
512-observation comparison too.

**Constructive coverage/cost repair.** Mix a fraction epsilon of uniform prices
back into this price law and reuse a retained representation for T independent
uses, paying its retention charge once. In this specified world, a partition's
gross gain over the constant is 0.36*epsilon times its gain in R6.1's noiseless
uniform-price table. The factor 0.36 is the squared contrast (0.8-0.2)^2.
The gap-price component is constant across representations. Thus the complete
finite frontier depends on B=epsilon*T:

| Coverage times reuse B | Optimal number of cells, away from boundary ties |
| --- | ---: |
| B < 4/9 | 1 |
| 4/9 < B < 16/9 | 2, retaining H |
| 16/9 < B < 32/9 | 4, all optima retaining H |
| B > 32/9 | 8 |

At the three boundaries the tied cell counts are {1,2}, {2,3,4} and
{4,5,6,7,8}, respectively. Subtracting the linear charge from the exact
frontier in R6.1 proves these thresholds; the numerical checker also evaluates
representative mixture/reuse pairs. This is a finite population result, not
an observed adaptive acquisition policy.

Positive goal coverage creates a pressure toward factual accuracy. Enough
coverage and reuse make that pressure worth a specified resource cost. Neither
condition alone says every distinction should be learned immediately.

## 5. Established alternatives and the remaining step

The finite selection proof is standard uniform convergence. Decision
calibration and omniprediction already connect predictive quality to families
of downstream decisions; reward-free exploration supplies much stronger
sequential learning machinery for unknown MDPs. The focused
[source comparison](../notebook/P4-R6-C001/sources.md) states their different
quantifiers and what was actually read.

The useful synthesis here is the explicit chain from overlapping practical
goals, through judged forecast performance, to a learned shared kind and its
coverage/cost boundary. It is not a new general learning algorithm. The main
open step is a funded, bounded procedure that proposes new distinctions and
chooses its own informative observations while preserving those guarantees.
The fixed vocabulary and externally supplied feedback keep that step visible.
