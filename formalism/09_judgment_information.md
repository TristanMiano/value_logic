# Conditional Information from Successful Judgment

Status: Task 22A completed

Date: 2026-07-18

Depends on: [`notes/policy_value_judgment.md`](../notes/policy_value_judgment.md),
claim `B01` in [`notes/claim_ledger.md`](../notes/claim_ledger.md), and the
proper-scoring scope recorded for `GneitingRaftery2007` in
[`notes/literature_map.md`](../notes/literature_map.md)

## Durable result summary

1. **A population score gap can prove outcome information.** Let `N` be the
   declared nuisance context, `J` a pre-outcome judge report, and `Y` a held-out
   outcome. If a predictor using `(J,N)` has strictly lower expected loss under
   a strictly proper scoring rule than the *Bayes-optimal* predictor using `N`
   alone, then `I(J;Y|N)>0`. A gap against an arbitrary or misspecified baseline
   does not have this implication.
2. **Log loss gives the strongest clean quantitative statement.** If the
   expected log-loss improvement is `delta>0`, measured in nats, then

   ```text
   I(J;Y|N)
     = delta + expected conditional KL calibration regret
     >= delta.
   ```

   Equality holds when the judge's predictive distribution is the true
   conditional distribution of `Y` given `(J,N)`.
3. **General strict propriety gives positivity, not a score-independent Shannon
   bound.** The optimal proper-score improvement is an expected scoring-rule
   divergence. Strictness makes it positive exactly when conditional outcome
   laws differ. A numerical conversion to Shannon mutual information requires a
   named score and normalization or a strong-propriety constant.
4. **Outcome information transfers to task information only through an explicit
   mediation condition.** Define the outcome-identifiable task quotient
   `K=k_N(Z)` by grouping latent task labels with the same conditional outcome
   law `P(Y|Z,N)`. If `J` and `Y` are conditionally independent given `(Z,N)`,
   then they are conditionally independent given `(K,N)`, and

   ```text
   I(J;K|N) >= I(J;Y|N).
   ```

   Thus a log-loss gap `delta` implies `I(J;K|N)>=delta` under these assumptions.
5. **The theorem identifies only the quotient relevant to the held-out
   outcome.** Duplicated task labels or distinctions that do not change
   `P(Y|Z,N)` cannot be recovered from this evidence. Additional independently
   measured outcomes may refine the quotient.
6. **Recursion contributes only incremental information.** At level `m`, the
   correct baseline conditions on nuisance context and every earlier report.
   The Bayes log-loss gain from adding `J_m` is exactly
   `I(J_m;Y|N,J_0,...,J_(m-1))`. Pure copying has zero gain even when agreement
   is perfect.
7. **Leakage, omitted nuisance, instability, copying, and sample noise remain
   live empirical threats.** A held-out estimate must certify a positive
   population gap under lineage separation and a frozen evaluation rule.
   Neither calibration, agreement, nor recursion alone is enough.
8. **`B01` survives as a scoped theorem, not as an unrestricted slogan.** It may
   appear in the formal paper as a compact motivating proposition and
   countermodel boundary. It is independent of the license calculus and does
   not license a judge or establish that its representation is human-readable,
   causal, true, or complete.

## 1. Task-local model and notation

This note uses a finite probability model so every conditional law and entropy
is elementary. Extensions to standard Borel spaces require regular conditional
probabilities and integrability assumptions but do not change the basic
factorization.

The task-local random variables are:

| symbol | meaning |
|---|---|
| `Z` | latent task label or structure |
| `Y` | held-out outcome whose distribution reflects task-relevant performance |
| `J` | judge report available before `Y` is revealed |
| `N` | declared nuisance/context variables available to the baseline |
| `q_(j,n)` | predictive distribution over `Y` issued using `(J=j,N=n)` |
| `K=k_N(Z)` | outcome-identifiable quotient of the latent task |

`J` here is a random report, not the project's license judgment, a task loss,
or the informal operation called `J` in the source posts. This deliberate local
overload follows the Task 22A roadmap; the symbols do not enter the canonical
`E,Q,S` core notation.

Write

```text
p_n       = P(Y in . | N=n),
p_(j,n)   = P(Y in . | J=j,N=n),
p_(z,n)   = P(Y in . | Z=z,N=n).
```

All information quantities use natural logarithms and are measured in nats.
The report must be pre-outcome relative to the declared data lineage. Calling a
variable `J` does not itself guarantee this non-leakage property.

### Proper-loss convention

Let `ell(q,y)` be a loss for quoting distribution `q` when outcome `y` occurs.
For a true distribution `p`, define

```text
L_ell(q;p) = sum_y p(y) ell(q,y),
H_ell(p)   = L_ell(p;p),
D_ell(p,q) = L_ell(q;p) - H_ell(p).
```

The loss is **strictly proper** when `D_ell(p,q)>=0`, with equality exactly when
`p=q`. This is the loss-minimization version of the proper-scoring convention
audited through `GneitingRaftery2007`.

The Bayes-optimal nuisance-only risk and the risk of the actual judge predictor
are

```text
R_N^ell = E[H_ell(p_N)],
R_q^ell = E[ell(q_(J,N),Y)].
```

The adjective *best* in “best nuisance-conditioned baseline” is load-bearing:
the baseline quotes the true conditional law `p_N`, not merely a convenient
trained comparator.

## 2. Strictly proper improvement implies outcome information

### Lemma 1: proper-loss decomposition

For any report `q_(J,N)` with finite risk,

```text
R_N^ell - R_q^ell
  = E[D_ell(p_(J,N),p_N)]
    - E[D_ell(p_(J,N),q_(J,N))].                 (1)
```

**Proof.** Add and subtract the Bayes risk based on `(J,N)`,

```text
R_(J,N)^ell = E[H_ell(p_(J,N))].
```

Conditioning first on `(J,N)` gives

```text
R_q^ell - R_(J,N)^ell
  = E[D_ell(p_(J,N),q_(J,N))].
```

The nuisance report `p_N` is constant across `J` at fixed `N`. Therefore its
expected loss evaluated under `p_(J,N)`, averaged over `J|N`, is its expected
loss under `p_N`, namely `H_ell(p_N)`. Hence

```text
R_N^ell - R_(J,N)^ell
  = E[D_ell(p_(J,N),p_N)].
```

Subtracting the first equality from the second proves (1). `square`

### Theorem 2: qualitative outcome-information theorem

Suppose `ell` is strictly proper and

```text
delta = R_N^ell - R_q^ell > 0.
```

Then `I(J;Y|N)>0`.

**Proof.** Equation (1) and nonnegativity of the second divergence imply

```text
E[D_ell(p_(J,N),p_N)] >= delta > 0.
```

Strict propriety therefore gives `p_(J,N) != p_N` on an event of positive
probability. For finite variables, conditional mutual information is zero
exactly when these conditional distributions agree almost surely. Thus
`I(J;Y|N)>0`. `square`

The theorem does not assume that the actual judge is Bayes-optimal. A poor
judge can discard some information present in `J`; any positive improvement by
that judge still certifies that the report variable contains outcome
information. Conversely, `J` can contain information that the chosen predictor
fails to exploit, producing no observed improvement.

### Population versus held-out estimates

Theorem 2 concerns expected risk under a fixed target distribution. A positive
finite-sample difference is an estimator, not the theorem premise. An empirical
application needs, at minimum:

- a frozen scoring rule and comparator;
- held-out outcome and lineage separation;
- an uncertainty procedure for the paired population risk gap;
- no selection of reports, tasks, or nuisance variables using the same outcome
  records without accounting for that selection; and
- replication or an explicit transport argument for any new population.

Within value logic, an accepted confidence statement about `delta>0` could
support a scoped evidence atom. Mutual information itself does not bypass the
ordinary evidence mode, checker, profile, or world-to-record soundness bridge.

## 3. Quantitative lower bounds

### Theorem 3: exact log-loss identity

Let

```text
ell_log(q,y) = -log q(y),
```

and assume finite risks. Then

```text
R_N^log - R_q^log
  = I(J;Y|N)
    - E[KL(p_(J,N) || q_(J,N))].                 (2)
```

Consequently, if the actual judge improves log loss by `delta>0`,

```text
I(J;Y|N)
  = delta + E[KL(p_(J,N) || q_(J,N))]
  >= delta.                                      (3)
```

Equality holds exactly when `q_(J,N)=p_(J,N)` almost surely.

**Proof.** For log loss, the scoring divergence is KL divergence. The first
expectation in (1) is

```text
E[KL(P(Y|J,N) || P(Y|N))] = I(J;Y|N).
```

Substitution into (1) proves (2), and rearrangement proves (3). `square`

This is the strongest simple answer to the Task 22A lower-bound request. The
judge's observed population improvement is a conservative lower bound because
any conditional miscalibration or unused information appears as the nonnegative
KL remainder.

### Corollary 4: one Brier-loss conversion

For categorical `Y`, use the unscaled Brier loss

```text
ell_B(q,y) = sum_a (q(a)-1[a=y])^2.
```

Its conditional divergence is `||p-q||_2^2`. If the Brier improvement over the
Bayes nuisance baseline is `delta_B>0`, Pinsker's inequality gives

```text
I(J;Y|N)
  >= (1/2) E[||p_(J,N)-p_N||_2^2]
  >= delta_B/2.                                  (4)
```

The factor changes if the Brier loss is rescaled. For a generic strictly proper
loss, Theorem 2 supplies positivity, but there is no universal
score-independent numerical conversion: score rescaling and different boundary
curvature change the units of the gap. A stronger bound requires a fixed
normalization and an appropriate strong-propriety inequality.

## 4. From outcome information to the identifiable task quotient

The latent label `Z` may contain distinctions that no held-out outcome can
reveal. At each nuisance value `n`, define

```text
z ~_n z'  iff  p_(z,n) = p_(z',n).
```

Let

```text
K = k_N(Z) = p_(Z,N),
```

viewed either as the conditional probability vector itself or as its
equivalence-class index. `K` is the **outcome-identifiable task quotient** for
this `Y` and `N`. It is no finer than the distinctions that change the held-out
outcome distribution. Here *identifiable* names an equivalence relation once
the conditional kernel is fixed. It does not assert that an unlabeled latent
mixture, its class names, or `K` itself can be statistically recovered from
observations of `(J,Y,N)` without further assumptions or task labels.

### Lemma 5: quotient mediation

Assume the conditional Markov condition

```text
J independent of Y given (Z,N).                  (M)
```

Then

```text
J independent of Y given (K,N).
```

**Proof.** Fix `(k,n)`. Every `z` in that quotient class has the same outcome
law `p_(z,n)=k`. By (M),

```text
P(J=j,Y=y | K=k,N=n)
  = sum_z P(z|k,n) P(j|z,n) P(y|z,n)
  = k(y) sum_z P(z|k,n) P(j|z,n)
  = P(Y=y|k,n) P(J=j|k,n).
```

Thus the conditional joint law factors. `square`

### Theorem 6: latent-task information bound

Under (M),

```text
I(J;K|N) >= I(J;Y|N).                            (5)
```

Therefore:

1. any strictly proper improvement over the best `N`-conditioned baseline
   implies `I(J;K|N)>0`; and
2. a log-loss improvement `delta>0` implies

   ```text
   I(J;K|N) >= I(J;Y|N) >= delta.                (6)
   ```

**Proof.** Lemma 5 gives the conditional Markov chain `J - K - Y` given `N`.
The conditional data-processing inequality gives (5). Theorem 2 supplies the
first consequence, and Theorem 3 supplies the second. `square`

This theorem cashes the defensible part of `B01`: successful held-out
prediction can force information about stable, outcome-relevant task
distinctions. It does not identify the full latent ontology. If two task labels
have the same conditional performance law, the quotient deliberately merges
them. If several independent outcome families matter, one may replace `Y` by
their joint vector; that can refine `K`, but only for distinctions those outcomes
actually change.

The condition (M) is not merely the claim that `Z` and `Y` are correlated. It
says all judge–outcome dependence left after conditioning on `N` is mediated by
the declared task structure. Direct outcome leakage, an omitted subject-ability
variable, or another common cause violates it.

### Stability qualification

The quotient and all bounds are distribution-relative. A training-population
kernel `P_train(Y|Z,N)` does not license claims about a deployment kernel
`P_deploy(Y|Z,N)` unless they are equal at the required scope or connected by a
separately justified transport model. “Stable task distinctions” in the public
claim should mean stability of the relevant outcome kernel, not merely stable
task names.

## 5. What recursion can add

Let

```text
H_(m-1) = (J_0,...,J_(m-1))
```

be all reports already available before recursive level `m`. The correct
baseline for testing the new report `J_m` is the Bayes predictor conditioned on
`(N,H_(m-1))`, not the original `N`-only predictor.

### Theorem 7: incremental recursive information

Under log loss, the Bayes risk improvement from adding `J_m` is exactly

```text
I(J_m;Y | N,H_(m-1)).                            (7)
```

For an actual predictor whose population log-loss improvement over the best
history-conditioned baseline is `delta_m>0`,

```text
I(J_m;Y | N,H_(m-1)) >= delta_m.                 (8)
```

If the recursive non-leakage condition

```text
J_m independent of Y given (K,N,H_(m-1))
```

also holds, then

```text
I(J_m;K | N,H_(m-1)) >= delta_m.                 (9)
```

**Proof.** Apply Theorems 3 and 6 with the enlarged nuisance variable
`N'=(N,H_(m-1))`. `square`

### Corollary 8: copying adds no evidence

If `J_m` is a deterministic function of `(N,H_(m-1))`, then

```text
I(J_m;Y | N,H_(m-1)) = 0.
```

It cannot improve population log loss over the best history-conditioned
baseline. Perfect agreement with an earlier judge is compatible with zero new
information.

The same conclusion holds for randomized copying whose extra randomness is
conditionally independent of `(Y,K)`. Recursion can add information only when a
new level receives evidence not already measurable from the conditioned
history. This is the precise content behind the requirement for independent
evidence at recursive levels.

## 6. Required countermodels

Each countermodel is finite and uses `N` constant unless otherwise stated.

### 6.1 A non-Bayes baseline creates a false “improvement”

Let `Y` be a fair bit and let `J` be independent of it. A bad baseline predicts
`P(Y=1)=0.9`; the judge predicts `0.5`. Under log loss, the bad baseline risk is

```text
-(1/2)log(0.9) -(1/2)log(0.1) > log 2,
```

while the judge risk is `log 2`. The judge “wins,” but `I(J;Y)=0`. Theorem 2 is
not contradicted because the comparator was not the best nuisance-conditioned
baseline.

### 6.2 An omitted nuisance masquerades as task information

Let `Z` and a pre-outcome subject variable `W` be independent fair bits. Set
`Y=W` and `J=W`, while the declared `N` omits `W`. The judge predicts perfectly
and beats the constant baseline by `log 2`, but

```text
I(J;Z)=0.
```

The report contains real outcome information, but none about the task. If `W`
is included in `N`, the best baseline is already perfect and the gap vanishes.
Relative to the incomplete `N`, condition (M) fails.

### 6.3 Direct leakage predicts outcomes without task structure

Let `Z` be constant, let `Y` be a fair bit, and let the purported report be
`J=Y` because the outcome or a deterministic proxy leaked into the report.
Again the log-loss gap is `log 2`, while the task quotient is constant and
`I(J;K)=0`. Held-out naming without lineage separation does not prevent this
countermodel.

### 6.4 Duplicated task types identify only a quotient

Let `K` and `U` be independent fair bits, define the raw task label
`Z=(K,U)`, set `Y=K`, and let `J=K`. Prediction is perfect, but the duplicate
index `U` never changes the outcome law:

```text
I(J;K)=log 2,
I(J;U|K)=0.
```

No amount of this outcome evidence identifies which duplicate label was used.
The quotient in §4 removes `U` exactly as required.

### 6.5 Instability destroys transfer

In the training population, let `Z` be a fair bit, `J=Z`, and `Y=Z`. The judge
has a `log 2` improvement. In deployment, keep `(Z,J)` unchanged but make `Y`
an independent fair bit. The deployment improvement and
`I_deploy(J;Y)` are zero. A theorem about the training distribution does not
establish stable deployment task information.

### 6.6 Recursion by copying creates agreement, not increments

Let `J_0` be any report and set `J_m=J_0` at every later level. All levels agree
perfectly, but for `m>=1`,

```text
I(J_m;Y | J_0,...,J_(m-1)) = 0.
```

If `J_0` is uninformative, the whole chain is uninformative. If `J_0` is
informative or leaked, later copies still provide no independent corroboration.

### 6.7 Calibration alone is compatible with zero information

Let `Y` be a fair bit and let every judge always report probability `0.5`.
The report is perfectly calibrated, but constant, so `I(J;Y)=0` and it cannot
beat the best constant baseline. Calibration is a reliability property, not a
claim of resolution or task information.

## 7. Adjudication of `B01` and publication boundary

`B01` receives a split disposition:

- **`S1`, scoped theorem.** In a fixed evaluation population, positive expected
  improvement under a strictly proper loss over the true nuisance-conditioned
  Bayes baseline implies positive conditional outcome information. Under
  conditional mediation through the outcome-identifiable task quotient, it
  implies positive task-quotient information. Log loss gives the quantitative
  lower bound (6).
- **`X1`, unqualified strengthening.** Success against a non-Bayes comparator,
  calibration, repeated agreement, or recursion alone need not imply outcome or
  task information. Outcome information without mediation need not be task
  information, and no theorem recovers latent distinctions erased by the
  outcome kernel.

The formal paper may retain Theorems 3 and 6 as a compact motivation result,
with one leakage or copying countermodel adjacent. The decomposition of proper
scores, the log-loss/KL identity, and data processing are standard mathematics;
the contribution here is their careful application to the project's recursive
judgment claim and the explicit quotient, baseline, lineage, and recursion
boundaries. This should not be advertised as a new information-theory theorem.

The result gives a precise sense in which a model-of-a-model can carry
nontrivial information even when it is incomplete. It does not show that the
information is human-interpretable, causally faithful, a utility function, or a
complete representation of the judged system. Those remain graded empirical
questions for the policy/value interpretability bridge.

`B02` remains future empirical work. A recursive design must test incremental
score improvement at each level against the full prior-report baseline, with
independent evidence and the mediation condition stated at that level. Mere
self-endorsement, interjudge agreement, or inherited calibration is not a
measurement theorem.

Finally, none of these results alters `WF + K_3`, proof-carrying plans, or
stratified system assessment. Information about `Y` or `K` is a target-world
property. Licensing a deployed judge still requires accepted, scoped evidence
and the ordinary world-to-record soundness bridge.

## 8. Handoff

Task 23 uses the following exact claim and no stronger one in
[`notes/policy_value_interpretability.md`](../notes/policy_value_interpretability.md):

> A value-like surrogate or judge that achieves a certified positive held-out
> log-loss improvement over the best declared nuisance-conditioned baseline
> carries at least that many nats of information about the outcome. If all
> residual outcome dependence is mediated by an explicitly defined
> outcome-identifiable task quotient, it carries at least that much information
> about that quotient. This establishes informative partial modeling, not
> complete transparency, unique value recovery, or causal/mechanistic fidelity.
