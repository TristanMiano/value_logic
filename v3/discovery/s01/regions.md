# Acquire enough information for a decision, not a complete repair model

Codex (GPT-6), October 11, 2026. DEVELOPMENT. S04/S05 with S01/S03 connections.
This is a constructive candidate note; no new-priority or confirmation claim.

## 1. A different generative route

For a versioned counterfactual request, let H be a **nonempty** finite set of
admissible structural/replacement models. Model h specifies the results of
permitted paid diagnostic computations and the loss vector c_h over m actions.
Coverage of the intended model is a separate premise. A fallible learned
library without coverage cannot supply a universal action certificate.

Mixed-action losses are expectations over an action lottery, not a guarantee
on every realized draw. Linearity assumes each model fixes the consequences
of the pure actions independently of the lottery used to select them. If a
predictor or environment responds to the mixing distribution, that dependence
must be part of the model; the displayed linear-loss LP is then not automatic.

Instead of selecting one repair as truth, retain every model consistent with
checked diagnostics. For regret tolerance epsilon, model h permits the mixed
actions

    K_h(epsilon) = {q in Delta_m : q dot c_h - min_a c_ha <= epsilon}.

The current evidence permits a common low-regret action iff the intersection
of these convex sets is nonempty. Computed values of a particular loss need
not be unique. A diagnostic is valuable when it makes that intersection
nonempty, even if many models remain indistinguishable. This has direct Q2/Q5
meaning: actions can need less structural or probability information than
complete identification. It is not a new general principle.

Ordinary active learning already studies this target. Javdani et al.,
[Near Optimal Bayesian Active Learning for Decision Making](https://arxiv.org/abs/1402.5886),
develop overlapping decision regions and hyperedge cutting. Their framework
is the strongest immediate comparison, not a truth-identifying baseline.
Our candidate direction is a *priced, changing-regret, certificate-producing
specialization*, with its coverage and mathematical-computation contracts
explicit. That specialization still needs material evidence.

## 2. Why pairwise disagreement can miss the task

Three models and three pure actions have losses

    h1: (0,0,1)
    h2: (1,0,0)
    h3: (0,1,0).

Every pair admits a common zero-loss action. All three together do not.
Therefore a policy that stops when every *pair* has some common acceptable
action is unsound for zero regret. With mixed actions q=(q1,q2,q3), the three
regrets are q3,q1,q2. Their minimum possible maximum is exactly 1/3, attained
by the uniform mixture; summing q1+q2+q3 proves the lower bound.

The information requirement changes with tolerance: epsilon>=1/3 needs no
diagnostic for mixed actions; epsilon<1/3 does. For epsilon=0, a binary
diagnostic partition {h1}|{h2,h3} suffices. The singleton supports A or B;
the pair supports C. It does not identify whether h2 or h3 holds. A second
diagnostic would identify the model but is unnecessary for this decision.
All diagnostic prices and model descriptions are stipulated in this example;
there is no empirical counterfactual learning claim.

## 3. Sparse ambiguity witnesses by the action dimension

For finite H, if the intersection of all K_h(epsilon) is empty, Helly's
finite convex-intersection theorem in the (m-1)-dimensional simplex gives an
empty subintersection using at most m models. Conversely any such witness
rules out a common epsilon-good mixed action. Treat each K_h as already
including the simplex; no extra m+1 count is needed for that domain constraint.

This is an application of ordinary convex geometry, not a new Helly theorem.
It suggests a mechanism: a robust-regret LP returns either a common action or
a small conflicting set of admissible models. Propose a cheap computation
that distinguishes this conflict, check the new evidence, and recompute.
It is sufficient that the true model remains in the maintained set. Prediction
may suggest promising diagnostics, but cannot delete a model by itself.

An equivalent finite LP minimizes rho subject to

    q_a >= 0; sum q_a = 1;
    sum_a q_a (c_ha-min_b c_hb) <= rho  for every h.

A feasible primal point is an upper regret certificate. A distribution lambda
over models with

    sum_h lambda_h (c_ha-min_b c_hb) >= r  for every a

is a lower certificate r: averaging any action's regret against lambda gives
at least r, hence some admitted model has regret at least r. Exact rational
primal/dual witnesses can be checked without trusting the LP optimizer.
Producing and checking the model rows and their admissibility is still paid
work; the certificate does not prove coverage of H.

## 4. Conflict removal is a guide, not a greedy cost theorem

Breaking one ambiguity witness can expose another. A diagnostic that separates
two witness models may leave a third branch containing the entire witness;
one must inspect every possible outcome. A myopic expected cut score can also
prefer a cheap test which does not help the eventual action. S03's bundle
complementarity remains relevant. No adaptive-submodularity or approximation
guarantee is inherited merely because the objects are called conflicts.

For a finite deterministic experiment family E, an exact information boundary
is simple. Give each model its complete response signature across E. A sound
finite policy achieving tolerance epsilon on every h exists iff each nonempty
signature class has a common epsilon-good action. Necessity: observationally
identical models follow the same transcript for every adaptive policy.
Sufficiency: query every experiment and use the common action in the resulting
class. The latter may be prohibitively expensive; it proves possibility, not
economy. A randomized policy requiring a uniform expected-regret guarantee
may choose the mixed common action; arbitrary best-arm tie labels cannot
replace the convex intersection condition.

## 5. Noisy values and changed prices

If observations concern linear values of an unknown law p, with checked
measurement-error bounds, use the compatible source fiber from P3-02. Each
p gives action losses Cp and therefore one K_p(epsilon). With a polyhedral
fiber, finitely many vertices suffice: each action-comparison inequality is
linear in p. This retains joint error information; replacing correlated
measurement noise by marginal intervals can enlarge the source unnecessarily.
Vertex enumeration may be exponential. A separation oracle with checked dual
witnesses is the prospective implementation route, not a free primitive.

For changed losses c'_h=c_h+delta_h on the same source, a previously certified
action q with regret <=epsilon satisfies

    regret_(c'_h)(q) <= epsilon + max_a delta_ha - min_a delta_ha.

Derivation: choose an optimal new comparator a*. Then
q dot c_h - c_h,a* <= regret_(c_h)(q) <= epsilon, and
q dot delta_h - delta_h,a* <= max delta_h - min delta_h. Add them.
Thus an action-common offset has zero effect on the certificate. This is an
elementary contrast bound, related to inherited loss-retention/transport work;
it is not new probability information. New source models need new coverage.

## 6. Materiality and next constructive move

The triangle example and sparse-witness lemma alone do not support P3-POS01.
The promising route is a solver that compiles uncertainty into a small
decision-conflict certificate and buys discriminating computations, with
complete prices and changing objectives. It must compare to HEC/ordinary
robust decision-region methods and exact small Bellman planning. It must avoid
manufacturing an advantage over complete model identification, which already
solves a more demanding problem. Next: construct a rational noisy-value
instance with a nontrivial adaptive query choice; generate exact primal/dual
certificates and identify where bundled queries or objective changes matter.

## 7. Constructive implementation and first observations

[region_probe.py](region_probe.py) enumerates small exact rational LP vertices
and reconstructs both primal and dual certificates. An ordinary minimax
Bellman planner chooses paid tests, either to meet a fixed regret tolerance
or to minimize query price plus remaining robust regret. The optimizer is a
strong conventional control and a development tool, not a cheap deployed
oracle. The [first output](regions01.json) records its visited states and
rational linear systems.

The triangle has exact primal/dual value 1/3; every pair has value zero. With
test prices 1/10 and 1/5, one first test suffices for zero regret, at cost 1/10.
Complete model identification has worst-case query price 3/10. This difference
is a capability illustration against a stronger information objective, not a
fair performance victory over ordinary decision-region acquisition. At
tolerance 1/3 the optimal policy buys no test. An indistinguishable class
containing the whole triangle correctly returns no finite zero-regret plan.

For the four-model XOR example, each single test leaves robust mixed regret
1/2. Buying both tests at 1/10 each yields zero terminal regret for total 1/5.
The exact economic price sweep is min(1/2,2c); at and above c=1/4 the selected
tie policy stops without buying. This checks the complementary-query case
and rejects a universal singleton-improvement stopping rule. All models,
prices and response functions are stipulated finite development inputs.
