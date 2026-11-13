# R6.4 Broad usefulness can stabilize a value while goals remain revisable

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** finite mathematical model, exact conditional-odds checks and
numerical population dynamics. The interpretation responds to the author's
questions about initially uncommitted agents and degrees of terminal-like value.

A useful subgoal can become persistent without being clamped. Two distinct
mechanisms make this precise here. An advantage that survives changes of goal
makes the subgoal a robust attractor of value revision. If that advantage
continues, retaining the acquired priority more faithfully can itself become
advantageous. Reversing environments can instead favor continued plasticity.

This advances C5 and the W6/C7 question about values assigned to internal
values. It supplies a restricted mechanism for the founding essay's account of
terminal/instrumental distinctions, rather than assuming that all preferences
come with an immutable top-level objective. It also creates a focused bridge
to W7; it does not complete the evolutionary module.

## 1. What “no initial terminal goal” means in this construction

Distinguish four objects:

- A **represented final preference** tells a decision procedure which outcome
  to pursue now.
- An **internal priority** directly rewards or selects an intermediate action,
  capability or judging procedure.
- A **revision/retention rule** changes those preferences and priorities.
- **Environmental consequences** affect which candidate rules persist or are
  copied. They need not be represented as a terminal objective by the agent.

The model permits neutral initial weights over candidate goal programs and
permits every goal label to change. It therefore requires neither an initially
privileged final goal nor an immutable internal utility function. Variation and
differential consequences still do causal work. An architecture with no such
asymmetry supplies no reason to select a particular goal: under exchangeable
feedback and a permutation-equivariant update, exchangeable initial weights
remain exchangeable in distribution. Spontaneous symmetry breaking may choose
different conventions; it does not identify a named universally favored goal.

The positive reading is **environmentally shaped valuation without an initially
clamped terminal preference**. It is not valuation without any physical
selection mechanism. Calling every retention mechanism a “terminal goal” is
a possible functional redescription, but it erases the operational distinction
between an encoded preference and a process that changes preferences.

## 2. A finite population of revisable goal-and-priority programs

Let g range over finitely many current goals, and let c in {0,1} denote whether
a program gives an intermediate capability a direct internal priority. The
normalized weight z_t(g,c) can describe a population of programs or a finite
candidate bank within an agent. In the latter interpretation the agent stores
and updates real-valued weights; the theorem is a population/expected-return
calculation, not a claim that a small random sample follows it exactly.

A concrete program can be a short-horizon planner. Program c=1 gives a local
bonus to preparation, observation or another enabling step; c=0 lacks that
bonus. The goals determine different downstream actions. Actual completed-task
returns, including the preparation cost, judge the program. Giving a local
bonus can help a planner whose horizon does not reach the downstream benefit.
This is an established optimal-reward-design mechanism; a bonus that induces
unproductive repetition would have to be rejected by the outer evaluation.

In one update:

1. Programs with goal g and priority 0 receive positive retention multiplier
   b_g; priority 1 receives b_g*R_g. The ratio R_g measures an actual net
   advantage in that environment, or a declared proxy if that is what is used.
2. Goals change by row-stochastic kernels K^0 and K^1, possibly different for
   the two priority types. No goal is required to remain fixed.
3. The priority changes 0-to-1 with probability u and 1-to-0 with probability
   v, where u,v>0 and u+v<1. Normalize the resulting weights.

Parameters may change with time where explicitly allowed below. This is a
selection-and-revision model. A biological realization requires inheritance
and reproduction; a within-agent realization requires an actual rule for
retaining judging programs. Those are alternatives, not an identity between
individual learning and biological evolution.

[R6.6](R6_bounded_subgoals.md) supplies a concrete bounded planner and the
explicit positive retention map b=1+V from actual expected task return V.
Its shared preparation priority has ratios 8/7, 17/14 and 9/7 across three
different goals. Such a map is an additional assumption about the learning
or persistence mechanism, not a consequence of calling a score “useful.”

## 3. A common priority can survive arbitrary changes of goal

Write q_g=z(g,1)/(z(g,0)+z(g,1)) on occupied goals and q_min=min_g q_g.
Suppose, at every update, R_g>=R_*>0 and

```math
K^1_{gh}\ge\kappa K^0_{gh}\quad\hbox{for every }g,h,
\qquad 0<\kappa\le1.                                    \tag{P.1}
```

The kernels may otherwise vary arbitrarily, even in response to the history.
The overlap factor kappa bounds how strongly goal revision can sort priority-1
programs away from destinations available to priority-0 programs. Identical
goal-revision kernels give kappa=1. Put R_eff=kappa*R_* and define

```math
F_{R,u,v}(q)=\frac{(1-v)Rq+u(1-q)}{Rq+1-q}.              \tag{P.2}
```

**Theorem 1 (robust common-priority bound).** After one update,

```math
q_{\min,t+1}\ge F_{R_{\rm eff},u,v}(q_{\min,t}).          \tag{P.3}
```

For fixed u,v and R_eff, every occupied goal's limiting lower priority is at
least the unique fixed point q_* of F in (0,1). In particular,

```math
q_*>\tfrac12
\quad\Longleftrightarrow\quad
R_{\rm eff}(1-2v)>1-2u.                                 \tag{P.4}
```

For symmetric revision u=v=mu<1/2, R_eff>1 suffices. When R_eff>1 the fixed
point is explicitly

```math
q_*=\frac{-B+\sqrt{B^2+4u(R_{\rm eff}-1)}}
              {2(R_{\rm eff}-1)},\qquad
B=1+u-(1-v)R_{\rm eff}.                                 \tag{P.5}
```

*Proof.* Initially z(g,1)>=r*z(g,0), where r=q_min/(1-q_min). Before the
priority flip, the incoming priority-1 mass at destination h is at least
kappa*R_* times r times its priority-0 mass: multiply the componentwise
inequalities by b_g*K^0_gh and sum. Thus its priority-1 fraction is at least
R_eff*q_min/(1-q_min+R_eff*q_min). The final flip maps a fraction s to
u+(1-u-v)s, an increasing function. This proves (P.3), including boundary
cases by continuity.

F is increasing and maps [0,1] into [u,1-v]. Its fixed-point equation is
(R-1)q^2+[1+u-(1-v)R]q-u=0. It has one root in (0,1), with F(q)>q below
that root and F(q)<q above it. Monotonicity therefore makes scalar iteration
converge to the root. Iterating the comparison proves the limiting lower bound;
the goal distribution itself need not converge. Evaluating F(1/2)-1/2 gives
(P.4), and the quadratic formula gives (P.5). QED.

If R_eff=1, q_*=u/(u+v). For a time-independent strictly positive joint
retention/revision matrix, the whole normalized population additionally
converges to its Perron eigenvector. That standard matrix result is stronger
about stationarity, but requires fixed dynamics; (P.3) does not.

**Meaning.** A common capability can remain favored while the goals making
use of it change, provided its net advantage and revision overlap survive.
The conclusion is a bound on a shared priority component. It does not make
all agents' goals, numerical valuations or whole policies identical.

## 4. Checks and separating cases

The [checker](../notebook/P4-R6-C001/plastic_priorities.py) verifies 2,406
conditional inequalities in 400 exact rational instances, including unequal
goal-revision kernels. It separately compares a stationary numerical trajectory
with the joint matrix's leading eigenvector. With R_g=(1.1,1.4,2), symmetric
revision 0.02 and the stated three-goal kernel, the conditional priorities are
0.928774, 0.936312 and 0.948871. The rigorous uniform lower limit from R_*=1.1
is 0.823010. A 600-round changing-goal run respects the same comparison bound;
its finite trace illustrates, rather than proves, the arbitrary-sequence result.
The [saved output](../notebook/P4-R6-C001/plastic_priorities.json) supplies the
parameters and reproducible values.

Three boundaries give three different repairs:

- **Revision bias:** with R=2, u=0.01 and v=0.4, the priority settles at
  0.232931. Better within-goal performance alone does not overcome this strong
  tendency to discard the priority. Equation (P.4) gives the sufficient and
  necessary two-type majority condition; changing the revision balance repairs
  it.
- **Goal sorting:** assign priority-0 programs to a high-retention goal and
  priority-1 programs to a low-retention goal. Despite R_g=2 within both goals,
  the checked overall priority is only 0.058384. Restoring kernel overlap
  kappa=0.8 yields 0.954717, above the conditional guarantee 0.948477. Comparing
  like goals and controlling revision-induced sorting is substantive.
- **Rare severe reversals:** nine multipliers of 2 followed by one of 1/1024
  give priority odds a net multiplier of 1/2. Without mutation, a neutral
  starting fraction 1/2 falls to 1/3 in one cycle, despite favorable contexts
  occupying 90% of the cycle. A uniform positive margin repairs this; mere
  frequency of favorable contexts is not a cumulative-retention guarantee.

The last comparison uses multiplicative retention. Additive decision payoff
and frequency of favorable goals are different quantities and should not be
interchanged. This is one reason “more instrumentally convergent” needs a
declared metric and a declared goal/environment distribution.

## 5. Persistent usefulness can favor making the priority harder to revise

Now compare symmetric revision rates mu in [0,1/2], with a constant advantage
R>1. A lineage's two-type retention matrix is

```math
M_\mu=\mathrm{diag}(1,R)
\begin{pmatrix}1-\mu&\mu\\\mu&1-\mu\end{pmatrix}.
                                                               \tag{P.6}
```

**Proposition 2 (a two-type reduction principle).** Its long-run growth
factor, defined as its leading eigenvalue, lambda(mu) is strictly decreasing
in mu when R>1. This is the realized asymptotic growth for a population with
positive initial mass on the leading type; at mu=0, an absent type cannot
appear spontaneously. Thus, among otherwise equal
revision rules, faithfully retaining the useful priority has a selective
advantage. When goals change by an independent common kernel and R is the
same across goals, the joint matrix factors as a Kronecker product, so this
comparison survives continuing changes of goal.

*Proof.* At the normalized fixed point q_*(mu), mean retention is
lambda=1+(R-1)q_*. For 0<mu<1/2, q_*>1/2. Holding q fixed, increasing mu changes
F by 1-2s<0, where s=Rq/(1-q+Rq)>1/2. Since the fixed point is the unique
crossing from F(q)>q to F(q)<q, it strictly decreases as mu increases. The
endpoints follow by continuity, with lambda(0)=R. For the product model,
the leading eigenvalue is the product of the goal factor's eigenvalue and
lambda(mu); the goal factor is the same in every comparison. QED.

This is a small explicit instance of the established **reduction principle**,
not a new evolutionary theorem. It gives a useful answer to the author's
question: a broadly useful internal value can acquire *lower revision
susceptibility* because retaining it is itself useful. An irreversible clamp
would require an additional architectural change. A low revision rate is a
graded form of persistence, not literal impossibility of revision.

Changing which priority is useful can favor the opposite policy. With retention
factors (1,4) and (4,1) alternating in blocks, the best rates among the tested
grid {0,.001,.005,.01,.02,.05,.1,.2,.3,.5} are:

| Environment | Best tested revision rate | Per-round long-run growth |
| --- | ---: | ---: |
| Constant advantage | 0 | 4.000000 |
| Alternating every round | 0.5 | 2.500000 |
| Alternating in blocks of 5 | 0.2 | 2.713459 |
| Alternating in blocks of 20 | 0.05 | 3.367327 |
| Alternating in blocks of 100 | 0.01 | 3.801646 |

These are spectral calculations for the declared periodic model, not estimates
of human plasticity or a proof that the best grid point is globally optimal.
In every alternating case, the zero-revision benchmark has growth 2. The
environment can therefore favor stability of a consistently useful value and
flexibility of a value whose usefulness reverses. Goal mutability alone does
not determine which regime applies.

## 6. An intervention separates persistence mechanisms

With symmetric revision mu, remove the entire priority-dependent advantage
by setting R=1. Then

```math
q_t-\tfrac12=(q_0-\tfrac12)(1-2\mu)^t.                 \tag{P.7}
```

A priority learned under R=2 and mu=0.02 starts at 0.960816. After removing
the advantage it falls to 0.559853 at 50 updates and 0.500131 at 200. Its
excess over neutrality has a half-life of about 16.98 updates. Slow forgetting
can look terminal-like over a short observation window while remaining fully
revisable.

If revision rates vary after the intervention, replace the final factor by
the product of (1-2*mu_t). When every 0<=mu_t<1/2, the residual is positive
when sum_t mu_t is finite, and vanishes when that sum diverges. This is a
separate memory/freezing mechanism. It should not be confused with ongoing
instrumental vindication.

Coordination supplies a third mechanism. Let the actual retention advantage
be R(q)=exp(s+b*(2q-1)): adopting a convention can make it more useful as
others adopt it. At s=0, q=1/2 is fixed and its update derivative is
(1-2*mu)*(1+b/2). It loses local stability when

```math
b>\frac{4\mu}{1-2\mu}.                                \tag{P.8}
```

The checker illustrates both sides at mu=0.02. With b=0.04, tested initial
conditions return to 1/2. With b=0.5, initial conditions just below or above
1/2 approach approximately 0.053527 or 0.946473. This numerical illustration
does not claim a complete global bifurcation classification. If b represents
real coordination returns, a convention can remain useful after its initiating
advantage s disappears. If b merely rewards agreement with an ungrounded
judge, persistence is evidence of self-reinforcement rather than factual accuracy.

## 7. Degrees of terminal-like value and the open question

Three operational axes are more informative than one terminal/instrumental
bit: **coverage** across current goals, **robustness** of the priority under
goal changes, and **revision susceptibility**. A fourth test asks whether it
persists when its original downstream benefits are removed. They can vary
independently. The model proves relations between them under stated dynamics;
it does not infer motivation from persistence alone.

The two-type case gives a useful exact separation. For fixed
$0<\mu<1/2$, the equilibrium $q_*(R,\mu)$ strictly increases with $R$:
for every interior $q$, the update $F_{R,\mu}(q)$ increases with $R$,
and its unique fixed point is the crossing from $F(q)>q$ to $F(q)<q$.
Stronger instrumental advantage therefore creates a stronger acquired
orientation. But after setting $R=1$, the **fraction of the original excess
that remains** is $(1-2\mu)^t$, independent of the earlier $R$. Its
half-life is $\log(1/2)/\log(1-2\mu)$. More usefulness alone has not
changed the revision mechanism. Selection that also lowers $\mu$ can
lengthen that half-life; section 5 supplies one constant-environment reason
for such selection and a changing-environment boundary.

There is also a tradeoff. R6.11's shared-experience contraction has factor
$1-2\mu$: slower revision preserves the acquired bias longer after removal,
but also slows the erasure of different initial priorities. Rapid agreement,
strong commitment and factual accuracy are consequently different success
criteria even inside this small model. Their relationship is a question
about the meta-rule and environment, not a consequence of a goal's name.

Reproduction, self-preservation and improved intelligence fit the construction
when they supply the requisite net advantages. Their names do not establish
those advantages: reproduction needs a useful relation between descendants and
the goals at issue; preservation needs valuable future opportunities; improved
judgment needs gains that exceed its resource cost. [R6.1](R6_goal_judgment.md)
supplies one explicit decision-value source for that last condition.

The closest established work includes optimal internal-reward design,
mutation-selection models and the reduction principle. The
[source ledger](../notebook/P4-R6-C001/sources.md) distinguishes the read
theorems from the present interpretation. The contribution here is a precise,
checked synthesis of **shared usefulness, revisable goals and graded
persistence**, with the missing mechanisms named. A finite observed learner
and a full model of how the retention/revision process itself arises remain
distinct obligations; the latter is a natural W7 direction.
