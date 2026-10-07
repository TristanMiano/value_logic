# P3-01 — separating examples for the research contract

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: **development constructions**, not a frozen experiment or novelty claim.
The examples distinguish services and missing assumptions. They do not select
the final benchmark or execute the later P3-02–07 tasks.

Each example names its information, required answer, ordinary comparison and
precise limit. Reproducible finite checks are linked here when available.

## EX01 — unresolved truth, failed search and finite coherence

Select three prime mathematical claims `phi`, `psi`, `chi`. The checked Boolean
record currently contains only `psi <-> not phi`; neither `phi` nor its negation
has been received. The selected finite assignments are

| phi | psi | chi |
|---:|---:|---:|
| 0 | 1 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 0 |
| 1 | 0 | 1 |

Any normalized nonnegative weights on these four assignments give
`p(phi)+p(psi)=1`. Uniform weights give `p(chi)=1/2`. This remains a legitimate
state of the **selected information fragment** even if `Gamma` proves `chi`
but the learner has not processed its proof or computed an equivalent shortcut.
These assignments are not asserted to extend to full arithmetic models. Once
a checked proof of `chi` is received, keep only the two `chi=1` rows. Once
`phi` is also resolved as true, only `(1,0,1)` remains.

**Conditional finite claim.** If every processed Boolean constraint is true of
the actual finite truth vector, that vector belongs to the retained set.
Indeed it satisfies each defining constraint. A further true constraint keeps
it there. Consequently, extrema of a loss over that set bound its value at the
actual vector, and a probability distribution on the set respects its Boolean
relations. The distribution's particular weights do not follow from this proof.
Their calibration and learning are separate obligations.

The construction uses at most `2^k` assignments for `k` selected prime claims,
with explicit Boolean evaluation and proof checking. It costs computation.
No full-theory model or consistency oracle is needed. A partially completed
enumeration must not return extrema as if all assignments had been examined;
it needs an outer bound or an unfinished status.

**Truth/search separation.** Two bounded-program claims with opposite true
labels may both receive `NO_RESULT` from a stopped investigator. That status
does not determine either label. A complete simulation up to the bound *inside
the proposition* can decide a bounded-execution claim; an investigator stopped
earlier cannot. Ordinary methods get the same code and may find shortcuts.
No difficulty lower bound is claimed by choosing a syntactically long program.

**What it establishes:** a standard finite constraint comparator can be locally
coherent and computationally non-omniscient. It does not establish that value
logic needs a new truth algebra to express logical uncertainty, or that a
uniform mixture is a good predictor. This is an independent elementary
reconstruction prompted by the source and inherited-interface audits.

## EX02 — the same cost can encode different beliefs

An action costs zero when `phi` is true and `K>0` when it is false. If its
declared subjective expected loss is `v`, then

$$
v=K(1-p),\qquad p=1-v/K.
$$

| Retained expected loss | Known penalty | Recovered probability of phi |
|---:|---:|---:|
| 3 | 10 | 7/10 |
| 3 | 100 | 97/100 |

Without `K`, the value `3` does not identify the probability. With an unknown
additive charge `c`, the same problem becomes `v=c+K(1-p)`. An ordinal
preference for this action over another contains still less information. A
single realized zero loss after one success is also not the subjective
probability or an expected loss.

**Required answer:** identify what is known and which recovery service is
requested. For unequal known binary payoffs, invert the affine relation;
otherwise supply the compatible set or explain non-identification. Ordinary
expected-loss algebra provides the same answer. This is a P3-02 test case,
not its general finite-matrix characterization.

## EX03 — equal marginal values, opposite decisions

The epistemic source permits one of two stipulated joint laws on Boolean
losses `X,Y`. Both have `E[X]=E[Y]=1/2`:

| Law | Positive-mass assignments | E[max(X,Y)] |
|---|---|---:|
| Same | `(0,0)` and `(1,1)`, each with weight 1/2 | 1/2 |
| Opposite | `(0,1)` and `(1,0)`, each with weight 1/2 | 1 |

An action with loss `max(X,Y)` is preferable to a sure loss `3/4` under Same
and worse under Opposite. The two marginal means cannot answer this decision.
A joint probability model or an aligned value profile can. For the sum
`X+Y`, however, both marginal means are sufficient: its expectation is `1`
under either law.

This is the inherited dependence obstruction from [paper §2](../../paper_v2.md),
made decision-discriminating with the `3/4` fallback. The fixture's weights
are supplied epistemic/task assumptions; using deterministic mathematical
outputs as its interpretation would not make their truth physically random.
It refutes only the specified marginal-only decoder. A task-specific scalar
containing `E[max(X,Y)]`, with its identity and scope, answers this one query.
Whether it suffices for later queries is a separate retention question.

## EX04 — useful fallible models and an ordinary reconstruction

Use the inherited illustrative reference `f(x)=x+x^3`, approximate model
`m(x)=x`, and a more expensive exact reference calculation. On `|x|<=a`,
the approximation error is at most `a^3`. If the accurate calculation costs
`c` more in the same loss units, the approximate-minus-accurate total loss is
bounded by `a^3-c`. This can be negative on one task and positive on another.

The explicit values and adequacy/resource distinctions are already in
[F01 EX01](../../v2/foundations/01_requirements_and_separating_examples.md#2-e01--a-more-accurate-model-need-not-be-the-better-use).
They are constructed mathematics, not measurements of Newtonian or relativistic
physics. Ordinary conditional algebra and task-based model selection reproduce
the bound with the same error evidence and prices.

**Theory tagging test.** Separately retain `Gamma_A={P}` and `Gamma_B={not P}`.
It is consistent at the metalevel to record “A proves P” and “B proves not P,”
and compare the costs of using their models in different scopes. Removing the
tags and taking both premises as jointly true would be a different theory.
An ordinary classical metatheory can preserve those tags too.

**What would improve the comparison:** a supported gain in learning applicability,
selecting paid computations or retaining transportable evidence under matched
information and costs. Simply keeping more than one useful model does not yet
show a capability absent from ordinary modeling. That remains a phase-three
research target rather than a reason to discard the motivating philosophy.

## EX05 — four meanings of “if the action were different”

Fix a history `h`, a function `f0(h)=0`, and equations

```
Z = f0(h)
A = Z
B = Z
L(A,B) = 2 + A - 2B.
```

The actual values are `A=B=0`, with loss `2`. Consider “if A were 1”:

| Operation and retained structure | A | B | Loss |
|---|---:|---:|---:|
| Condition on A=1 while retaining every equation | — | — | no compatible state |
| Override only A's equation, retain B=Z and f0 | 1 | 0 | 3 |
| Replace f0 by f1 with f1(h)=1 and redirect both uses | 1 | 1 | 1 |
| Replace only the actor's call; B still uses f0 | 1 | 0 | 3 |

The value expression evaluates each specified case correctly; it does not pick
the operation. A predictor or copy follows the replacement only if the
dependency contract says it does. Same history and identical actual outputs
do not supply that contract. See S04/S05 for the primary comparisons; this
finite arithmetic is a fresh contract fixture, not a new counterfactual theory.

## EX06 — observational identity and tied minimal repairs

### A. Even a complete observational law can miss the dependency

Let `U` be binary and compare these two acyclic models:

```
M_direct: A=U, B=A
M_common: A=U, B=U
L(A,B)=2+A-2B.
```

For either value of `U`, both models return `(A,B,L)=(U,U,2-U)`. They therefore
have exactly the same full observational law for every stipulated law on `U`.
With `U=0`, intervention `A:=1` gives loss `1` in `M_direct` and loss `3` in
`M_common`.

**Proof of non-identification.** A decoder whose input is only that shared
observational law receives the same input in the two models and must return
the same output. The required intervention outputs differ, so that decoder
cannot be correct on both. A randomized decoder cannot guarantee an exact
correct answer on both either. A reported set `{1,3}` or interval `[1,3]`
preserves this particular ambiguity. Explicit structural evidence can narrow it.
This is an elementary identifiability witness, equally applicable to an
observational probability summary and an observational value summary.

### B. Equal-cost repairs need a visible tie policy

Take the original soft constraints

```
c1: A=0
c2: B=0
c3: A=B
```

with Boolean variables. Add hard antecedent `A=1`. A repair may delete original
constraints, at cost one per deletion; all retained constraints must hold. Every
repair deletes `c1`. It must also delete either `c2` or `c3`. The two minimal
deletion sets are therefore:

| Deleted constraints | Retained constraint | A,B | Loss | Repair cost |
|---|---|---|---:|---:|
| c1,c2 | A=B | 1,1 | 1 | 2 |
| c1,c3 | B=0 | 1,0 | 3 | 2 |

No one-deletion repair works: if `c1` remains it contradicts the antecedent;
if only `c1` is deleted, `B=0` and `A=B` still imply `A=0`. Deleting all three
is feasible but not minimal. Announce any tie breaker independently of the
reported intervention result, or return the loss range. Choosing the smaller
loss is a valid *planning preference* if declared; it is not a discovery that
this is the unique closest hypothetical.

Failure to find a repair within a budget is not a proof that none exists.
A best-found repair is not certified globally minimal without search coverage
or a lower-bound certificate. Both distinctions belong in the response status.

## EX07 — valuable computation and complementary evidence

### A. Equal uncertainty, different stakes

For two unresolved Boolean questions, stipulate the same epistemic belief
`p=1/2`, symmetric wrong-answer losses `K=10` and `K=1`, and a computation
that resolves the chosen question exactly at a cost of `2`. Guessing has
expected task losses `5` and `1/2`. Buying the computation has total loss `2`.
Thus it is useful for the first and harmful for the second under this model.
Ordinary expected-cost metareasoning reaches the same decision.

The joint outcome law and reliability of the computation are assumptions in
this idealized fixture. A practical method must obtain useful estimates of
them without a free oracle. Mathematical determinism does not prevent an
agent from having the stipulated uncertainty before it computes the answer.

### B. One-step value of computation can miss a useful pair

Now suppose an agent's current epistemic model makes two unrevealed bits `X,Y`
uniform and independent. Its task is to predict `X xor Y`, with wrong-answer
loss `10`. Reading either bit costs `1` and reveals it without error.

- Stopping immediately has expected loss `5`.
- Reading just one bit leaves the XOR unbiased; expected total loss is `6`.
- Reading both bits makes the task answer known; total loss is `2`.

A myopic policy comparing only “read once then stop” with “stop now” declines
both first reads. The best policy in the stated finite catalogue reads twice.
This counterexample challenges unrestricted claims for one-step reasoning
selection, not metareasoning itself. It motivates a lookahead/budget comparison
in P3-07, while keeping the cost of discovering this dependence explicit.

## EX08 — prediction, calibration and action are different targets

### A. Zero expert regret is compatible with bad belief estimates

Use a sole predictor that always reports `1/2`. On a stream of true claims with
answers revealed after their forecasts, following that predictor has zero
regret relative to the available expert class. Its mean Brier loss is `1/4`
and its mean signed probability error is `-1/2`. It never learns certainty.
Thus a finite-expert regret guarantee alone does not establish calibration,
truth learning or the Logical Induction criterion. Expanding the expert class
may help, at a cost; it changes the comparison contract.

### B. A better forecast can change no decision

For a true Boolean claim with symmetric wrong-answer stakes `K`, forecasts
`0.6` and `0.9` both select the true answer at threshold `1/2`. Their realized
decision loss is the same (`0`), although Brier losses are `0.16` and `0.01`.
Forecast quality remains meaningful, but this episode alone demonstrates no
decision advantage.

### C. A small forecast difference can cross an expensive threshold

For that same true claim, forecasts `0.49` and `0.51` straddle the threshold.
Their Brier losses differ by `0.02`, while the realized action losses differ
by `K`. With unbounded `K`, no stake-independent bound converts this fixed
score difference into a decision-loss difference. Stakes and units matter.

### D. A useful conditional bridge has an elementary proof

Suppose every available action has a true declared cost `L(a)` and an estimate
with `|Lhat(a)-L(a)|<=epsilon`. Let `ahat` minimize estimated cost and `astar`
minimize true cost, both over the same finite available action set. Then

$$
L(\widehat a)
\le \widehat L(\widehat a)+\epsilon
\le \widehat L(a^*)+\epsilon
\le L(a^*)+2\epsilon.
$$

Uniform control in common cost units supplies this bridge. It is ordinary
decision algebra, not a new learning guarantee. The premise says nothing
about how much computation produced the estimates or whether they remain
accurate after the objective changes. Those become explicit later duties.

## EX09 — withdrawal, new prices and operational identity

Suppose an old source says `0<=x<=1/4` and a comparison has difference
`d=x-1/2`. Its sharp upper bound is `-1/4`. Withdrawing the upper premise and
admitting `0<=x<=1` changes that bound to `+1/2`. An old proof remains a valid
proof from its original premises, but no longer warrants the same current
comparison. If rechecking is too expensive now, mark the warrant stale and use
a permitted fallback; do not silently retain the old negative bound.

A price change is different from evidence withdrawal. A subjective success
probability `7/10` gives expected failure cost `3` at penalty `10`, and `6` at
penalty `20`. Against a fixed fallback of `4`, the preferred action changes.
Retaining the belief and loss formula permits an ordinary exact update. Keeping
only the old action choice does not. This simple example does not prove that
the entire probability law is necessary for every later price query.

**Refactoring witness.** Start with EX06's three soft constraints and equal
per-occurrence deletion weights. Duplicate the *same evidence identity*:

| Presentation | Original solutions | Minimum deletion cost after A=1 | Losses of all minimizing repairs |
|---|---|---:|---|
| A=0; B=0; A=B | `(0,0)` | 2 | `{1,3}` |
| A=0; B=0; A=B; A=B | `(0,0)` | 2 | `{1}` |
| A=0; B=0; A=B; B=0 | `(0,0)` | 2 | `{3}` |

The duplicated assertion changes no ordinary model, but raw deletion distance
changes the selected hypothetical. Keeping evidence identity and transporting
the edit weights fixes this fixture. It does not prove invariance for arbitrary
program refactoring; P3-05 owns that wider question. Two genuinely independent
observations would be a different evidence history, not this duplication test.

## EX10 — a genuine counterpossible is not just another model

Use the standard integer and rational interpretation, with the ordinary
divisibility and lowest-terms facts retained. “sqrt(2) is rational” implies
positive coprime integers `p,q` satisfying `p^2=2q^2`. Squaring preserves parity,
so `p` is even. Substituting `p=2k` gives `q^2=2k^2`, so `q` is even too.
That contradicts coprimality. This familiar conditional argument is enough to
show why the antecedent has no ordinary satisfying case under this background.

There are three distinct follow-up questions:

1. A bounded reasoner has not yet found that argument. Its uncertainty is
   epistemic and computational; it need not already know the contradiction.
2. Replace the meaning of “integer” by elements of a larger domain such as
   `Z[sqrt(2)]`, and “rational” by ratios in that domain. The element is now
   trivially a ratio, but the interpretation has changed. Record the translation.
3. Keep the original antecedent and interpretation, but ask for a nonvacuous
   consequence of supposing it. This needs a specified counterpossible
   evaluation/selection rule; the ordinary proof above does not provide one.

Similarly, a union containing one ordinary case satisfying `P` and another
satisfying `not P` represents uncertainty about `P`; it contains no case
satisfying `P and not P`. Empty-context rejection avoids a false usefulness
warrant, but is not by itself a nonclassical consequence relation.

The source comparison S07 supplies an existing route using impossible worlds.
P3-04 must state how its chosen route treats retained inference rules, relevance,
selection, ties and costs. This example currently diagnoses the missing
interface; it does not pretend that returning “infeasible” solves every
counterpossible question.

## EX11 — proper prediction and a report that changes its target

The inherited report-controlled program has

$$
H_r=(1-r)p+rs.
$$

For `p=1,s=1/2`, this becomes `H_r=1-r/2`. Its report-induced expected Brier
loss is `r^2+(1-2r)H_r`. The minimum occurs at `r=5/8`, where the actual
failure rate is `11/16`, exceeding the report by `1/16`. The Brier loss is
`7/32`. The self-consistent report `r=2/3` gives loss `2/9`, larger by `1/288`.

For a fixed exogenous outcome mean `H`, the familiar decomposition
`E[(r-Y)^2]=(r-H)^2+H(1-H)` is minimized at `r=H`. Here `H_r` changes with the
report. The example therefore tests an assumption, not a contradiction in
proper scoring. An accepted proof about a particular report/program version
is also different from a learned forecast about a future version.

All these numerical results are **inherited**, from
[the observation/revision audit §24](../../v2/foundations/03b_observation_and_revision_audit.md#24-a-proper-prediction-loss-need-not-enforce-a-self-report-under-feedback).
P3-01 rechecks their relevance to update timing; it does not claim them as new.

## EX12 — even all event intervals can omit a cost distinction

This new numerical fixture illustrates an **established** expectation/credal
expressiveness distinction (S13, Example 2.11 and Theorem 4.1). It is not a
novel claim about expectations.

Take a three-state space. Let `Q` be the convex hull of

```
(2/3,1/3,0), (0,2/3,1/3), (1/3,0,2/3),
```

and `P` the convex hull of all six permutations of `(2/3,1/3,0)`. Each
coordinate ranges from `0` to `2/3` in both sets. Hence every event has the
same probability interval under both: singletons `[0,2/3]`, two-state events
`[1/3,1]`, the empty event `{0}` and the whole space `{1}`.

For an action with statewise cost `g=(0,1,2)`, its costs at Q's three vertices
are `1/3,4/3,4/3`. At P's six vertices they are
`1/3,2/3,2/3,4/3,4/3,5/3`. Linear evaluation on a convex hull has its extrema
among these vertices, so

$$
\sup_{q\in Q}E_q[g]=4/3
<3/2<
\sup_{p\in P}E_p[g]=5/3.
$$

Under the declared worst-expected-cost decision rule, a sure fallback costing
`3/2` is worse than `g` under Q and better under P. All event intervals agree,
but the robust decision reverses, with margin `1/6` on each side.

This motivates richer cost-query information in an imprecise setting. The
strong ordinary comparator is a joint credal set or its expectation functional,
which retains the distinction too. It would be misleading to give value logic
that full structure and restrict its ordinary competitor to event intervals.
The general characterization and the cost of retaining/querying this information
remain P3-02 and subsequent work.
