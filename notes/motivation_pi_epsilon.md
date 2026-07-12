# From Indefinite Theory Succession to `Pi(M,D,epsilon)`

Created: 2026-07-10  
Task: TODO Task 2  
Status: Conceptual derivation and notation recommendation; not yet the final formal calculus.

## Executive answer

The main question does **not** immediately force the exact three-place expression

```text
Pi(M,D,epsilon).
```

It directly motivates `M` and `D`:

- `M` is the model or theory being considered;
- `D` is the domain on which that model may remain usable despite later supersession.

It also motivates some comparison of performance, because “Newtonian mechanics is still useful here” must eventually distinguish successful from unsuccessful reliance. But the main question alone does not determine:

- what counts as an error;
- how errors across a domain are aggregated;
- whether performance is predictive, decision-theoretic, computational, or multi-objective;
- whether adequacy means satisfying an external safety requirement, improving on a fallback, or being best among known alternatives;
- whether one scalar threshold is sufficient.

`L` and `epsilon` arise when the pragmatic phrase “usable on this domain” is operationalized as a permission to rely on `M` for a task. A useful minimal kernel is

```text
Adeq(M;D,L,epsilon)  iff  R_{D,L}(M) <= epsilon,
```

where `R_{D,L}(M)` is a domain-level risk induced by a local loss and an aggregation rule.

The new observation developed in this note is that `epsilon` need not always be an arbitrary externally supplied number. If the agent has a fallback, null policy, status-quo model, or “do nothing” option `B`, then `B` supplies an endogenous benchmark:

```text
M is worth using only if it performs sufficiently better than B.
```

For a loss-like objective `J`, this produces the signed surplus

```text
s_B(M,D) = J(B,D) - J(M,D) - Delta,
```

where `Delta >= 0` is the improvement required to cover switching, computation, measurement, or intervention costs. The license condition is `s_B(M,D) >= 0`. ReLU then has a direct interpretation:

```text
ReLU(s_B(M,D)) = positive surplus over the outside option.
```

This is one principled origin for a threshold. It does not eliminate externally imposed tolerances: a model can beat a disastrous status quo while remaining unsafe. The mature predicate should therefore distinguish at least:

1. **absolute adequacy:** does the model meet hard task/safety requirements?
2. **baseline improvement:** does it beat the fallback enough to justify use?
3. **comparative admissibility:** is it undominated, or close enough to best, among the models actually considered?

The compressed `Pi(M,D,epsilon)` can be used later, but only after the loss, benchmark, evidence state, and comparison rule are fixed by context.

---

## 1. What the motivating question gives us

The project begins from four observations:

1. Scientific theories often arrive in a sequence.
2. A successor may outperform a predecessor without making the predecessor useless everywhere.
3. A bounded agent may not know whether the current theory is final.
4. The agent must nevertheless decide which model to rely on in a particular situation.

Let `X` be a space of possible cases or situations and let `M` be a model. The Newtonian example immediately blocks an unqualified one-place judgment such as

```text
Accept(M).
```

If the same model is usable for a classroom projectile and unusable for GPS timing, the judgment must vary with application. This directly motivates

```text
Accept(M,D),
```

where `D` identifies the relevant cases, distribution, scale, or task family.

This is the first conclusion that follows almost directly from the main question:

> Domain relativity is not an optional embellishment. It is required to express the motivating fact that a superseded theory can remain usable locally.

The main question also implies stage or agent relativity at the epistemic level. “Best currently known” depends on an agent's evidence, model library, and search effort. But these indices do not yet belong inside the minimal empirical adequacy predicate. They belong to a later license predicate built from adequacy.

---

## 2. Why domain relativity alone is insufficient

`Accept(M,D)` still leaves “accept” uninterpreted. Two agents could agree on `M` and `D` while disagreeing because:

- one needs centimeter accuracy and the other needs meter accuracy;
- one cares about average error and the other about the worst case;
- one uses the model for explanation and the other for control;
- one can afford an expensive calculation and the other cannot;
- one faces a safe fallback while the other faces a deteriorating status quo.

The pragmatic background supplies the next step. A bounded agent does not observe a theory's final truth-status. It observes records and consequences:

- predicted versus observed quantities;
- probability assigned to events that occur;
- successful versus failed classifications;
- rewards or harms caused by actions selected using the model;
- compute, time, measurement, and switching costs.

To convert those observations into a reproducible judgment, the agent needs a discrepancy or loss.

Let a record be `z=(x,y)`, where `x` is a case and `y` is an observed outcome. Let

```text
ell_L(M,z) >= 0
```

measure the local mismatch relevant to purpose `L`. Examples include absolute error, squared error, negative log likelihood, classification loss, constraint violation, or decision regret.

This does not make loss a measure of metaphysical falsity. It makes loss a measure of model–task mismatch under an explicitly chosen evaluation rule.

---

## 3. From local loss to domain risk

A domain contains more than one case, so local losses must be aggregated. Write

```text
R_{D,L}(M) = rho_D(z -> ell_L(M,z)),
```

where `rho_D` is a domain-level risk functional.

Several choices are possible:

### 3.1 Expected risk

If `D` induces a probability distribution `mu_D`, then

```text
R_{D,L}^{mean}(M) = E_{z ~ mu_D}[ell_L(M,z)].
```

This is appropriate when average performance on a stable distribution is the target.

### 3.2 Worst-case risk

If `D` is a set of cases and every case must be controlled, then

```text
R_{D,L}^{max}(M) = sup_{z in D} ell_L(M,z).
```

This is more natural for some safety or verification claims.

### 3.3 Tail or quantile risk

If rare failures matter but worst-case analysis is too conservative, one may use a high quantile, conditional value at risk, or a failure-probability constraint.

### 3.4 Empirical risk

For an observed sample `E_t={z_1,...,z_n}` from the domain,

```text
Rhat_{E_t,L}(M) = (1/n) sum_i ell_L(M,z_i).
```

This is observable, but it is only an estimate of domain risk.

### 3.5 Decision risk or regret

If the model is used to select actions, let `a_M(x)` be the action chosen using `M`, and let `a_star(x)` be an oracle or benchmark action. Then

```text
ell_dec(M,x) = U(a_star(x),x) - U(a_M(x),x).
```

The resulting risk asks how much utility is lost by relying on the model. It can rank two predictively distinct models as decision-equivalent, or make a small predictive discrepancy decisive near an action boundary.

The expression `Pi(M,D,epsilon)` suppresses all of these choices. It is therefore safe only after `L` and `rho_D` are fixed.

---

## 4. The first route to `epsilon`: an external adequacy requirement

Once risk is defined, a threshold turns a graded comparison into a reliance rule:

```text
Adeq(M;D,L,epsilon)  iff  R_{D,L}(M) <= epsilon.
```

Under this reading, `epsilon` is:

> the largest domain-level loss that the application is prepared to treat as acceptable.

It is not:

- the probability that `M` is false;
- the fraction of `M` that is false;
- a universal constant applying across domains;
- meaningful without the units and scale induced by `L`.

An external `epsilon` is natural when tolerances arise from outside model comparison:

- an engineering safety constraint;
- a legal or contractual requirement;
- an instrument resolution;
- a maximum acceptable failure probability;
- a scientific precision target;
- a resource budget.

This route explains why Newtonian mechanics can be adequate for one purpose and inadequate for another even on superficially similar physical systems. Tightening the required precision changes the license without changing the equations.

---

## 5. The second route to `epsilon`: the fallback or status quo

Many decisions do not begin with a free-floating tolerance. They begin with an outside option.

Let `B` denote a baseline. Depending on the setting, `B` may be:

- “do nothing”;
- preserve the status quo;
- abstain and request more information;
- use a default action;
- use a null predictor such as a base-rate or persistence model;
- continue using an older scientific model;
- defer to a human or a more expensive procedure.

Crucially, doing nothing is usually still a policy. The world continues to evolve, and the status quo has an outcome distribution, opportunity cost, and risk.

Let `J(M,D)` be the total task loss of relying on `M`. It may include predictive or decision risk plus costs:

```text
J(M,D) = R_{D,L}(M) + C_use(M,D).
```

Let `Delta >= 0` be the minimum improvement required to justify switching from `B` to `M`. Then define

```text
s_B(M,D) = J(B,D) - J(M,D) - Delta.
```

The model beats the outside option when

```text
s_B(M,D) >= 0,
```

equivalently,

```text
J(M,D) <= J(B,D) - Delta.
```

Thus the fallback induces a contextual threshold

```text
epsilon_B(D) = J(B,D) - Delta.
```

This gives a direct pragmatic origin for `epsilon`: it is the loss ceiling a model must beat to improve on what the agent would otherwise do.

### 5.1 Why this is especially compatible with ReLU

The signed quantity `s_B` has a natural meaning on both sides of zero:

- `s_B > 0`: positive surplus over the outside option;
- `s_B = 0`: exact indifference after costs;
- `s_B < 0`: the fallback is better by `-s_B`.

Then

```text
ReLU(s_B)
```

is exactly the positive improvement margin. The null branch is not an arbitrary mathematical trick: it corresponds to retaining the fallback when the candidate fails to beat it.

This is stronger motivation for a zero threshold than the generic claim that “adequate means activation above zero.” The zero is the point of indifference between the candidate and its outside option after relevant costs.

### 5.2 Predictive and decision baselines must not be conflated

For pure prediction, `B` can be another predictor and `J` can be predictive risk. For action, “do nothing” is a policy and the correct comparison is usually decision loss or regret.

A theory can predict better than a null model while still inducing worse actions. Conversely, a coarse theory can be predictively worse but decision-equivalent on the available action set. The baseline comparison should therefore occur at the level of the actual task.

### 5.3 Relative improvement can be additive or multiplicative

The additive margin above uses

```text
J(B,D) - J(M,D).
```

If risks are positive and orders of magnitude matter, a multiplicative comparison may be better:

```text
s_B^log(M,D) = log J(B,D) - log J(M,D) - log gamma,
```

where `gamma >= 1` is the required improvement factor. This form motivates log-loss margins later, but it requires careful handling of zero risk.

---

## 6. Why beating the status quo is not always enough

The baseline route is important, but it cannot replace every external tolerance.

Suppose the status quo has catastrophic expected loss. A new model that is slightly less catastrophic beats the baseline but should not automatically receive a safety license. Conversely, a model can meet a hard safety requirement while offering too little improvement to justify its implementation cost.

Therefore distinguish:

### 6.1 Hard adequacy

```text
HardAdeq(M) iff R_{D,L_hard}(M) <= epsilon_hard.
```

### 6.2 Improvement over fallback

```text
Improve_B(M) iff J(M,D) <= J(B,D) - Delta.
```

### 6.3 Combined reliance condition

```text
Use_B(M) iff HardAdeq(M) and Improve_B(M).
```

If both use the same scalar loss, the effective threshold is

```text
epsilon_eff(D) = min(epsilon_hard, J(B,D) - Delta).
```

But this minimum is valid only when both quantities are expressed in the same loss units. Otherwise the conditions must remain separate.

This distinction prevents two errors:

- treating any improvement as sufficient for safety;
- treating any safe model as worth adopting regardless of cost or benefit.

---

## 7. “Better than other models” is a third condition

The outside option is not the same as the full model library.

Let `K_{a,t,b}` be the set of models retrieved or evaluated by agent `a` at stage `t` under search budget `b`. Define a scalar objective `J(M,D)` for the moment.

The best retrieved score is

```text
J_star(K,D) = inf_{M' in K} J(M',D).
```

Several comparative standards are possible.

### 7.1 Exact best-known selection

```text
Best_K(M,D) iff J(M,D) = J_star(K,D).
```

This is brittle under noise and ties.

### 7.2 Near-best admissibility

```text
NearBest_K(M,D,eta) iff J(M,D) <= J_star(K,D) + eta.
```

This retains models whose disadvantages are within a comparison tolerance `eta`.

### 7.3 Dominance or Pareto admissibility

If performance has several dimensions—accuracy, cost, robustness, coverage—then `M` is admissible when no retrieved model is at least as good on every relevant dimension and strictly better on one.

This is important for the motivating physics example. General relativity may improve fidelity while Newtonian mechanics remains cheaper, simpler, or sufficiently accurate on a restricted domain. Requiring a single globally best model would erase precisely the retention phenomenon the logic is meant to explain.

### 7.4 Combined scalar form

When a single objective is legitimate, one possible combined rule is

```text
Pi(M) iff
    J(M,D) <= epsilon_hard
    and J(M,D) <= J(B,D) - Delta
    and J(M,D) <= J_star(K,D) + eta.
```

Equivalently, the model must fall below the smallest applicable ceiling:

```text
J(M,D) <= min(
    epsilon_hard,
    J(B,D) - Delta,
    J_star(K,D) + eta
).
```

Again, this scalar compression is valid only if all terms share a meaningful scale.

---

## 8. Adequacy, licensing, and selection should be separate predicates

The notation becomes clearer if one predicate does not carry every idea at once.

### 8.1 World- or task-level adequacy

```text
Adeq(M;D,L,epsilon) iff R_{D,L}(M) <= epsilon.
```

This is a claim about model performance relative to an evaluation rule.

### 8.2 Evidence-relative certified adequacy

The true domain risk is generally unknown. Let `E_t` be the evidence available at stage `t`, and let

```text
U_{a,t,alpha}(M;D,L | E_t)
```

be an upper risk bound with confidence or coverage level `alpha`. Then

```text
CertAdeq_{a,t}(M;D,L,epsilon,alpha | E_t)
    iff U_{a,t,alpha}(M;D,L | E_t) <= epsilon.
```

This says the evidence supports adequacy at a stated calibration level. It does not say the risk is known exactly.

### 8.3 Baseline-relative improvement

```text
Improve_{a,t}(M;B,D,Delta | E_t)
    iff U(M;D | E_t) + Delta <= LBound(B;D | E_t),
```

where conservative comparison may require an upper bound for the candidate and a lower bound for the baseline. Other statistical comparison rules are possible.

### 8.4 Library-relative admissibility

```text
Admissible_{a,t,b}(M;D,K)
```

means that no model actually retrieved/evaluated under budget `b` defeats `M` according to the chosen scalar, Pareto, or robust comparison rule.

### 8.5 The use-license

The project's eventual `Pi` is best treated as a composite permission:

```text
Pi_{a,t,b}(M;D,L,epsilon,alpha,B,Delta,K | E_t)
    iff CertAdeq_{a,t}(M;D,L,epsilon,alpha | E_t)
        and Improve_{a,t}(M;B,D,Delta | E_t)
        and Admissible_{a,t,b}(M;D,K).
```

Not every application needs every conjunct. For example:

- a hard safety certificate may not require best-known selection;
- a low-stakes router may use only baseline improvement and abstention;
- scientific practice may retain every adequate Pareto-undominated model.

This factorization answers the opening question more accurately than treating `Pi(M,D,epsilon)` as primitive. The three-place expression is a compressed surface form for a structured, evidence-relative permission.

---

## 9. The epistemic status of observed error

The pragmatic background does not usually give the agent “the error rate.” It gives a finite sample from which error is estimated.

Let

```text
Rhat_n(M) = (1/n) sum_i ell(M,z_i).
```

Even if `Rhat_n(M)=0`, the domain risk may be positive. A rigorous license therefore needs one of the following:

- a probabilistic model and posterior statement;
- a frequentist confidence bound;
- a concentration bound under sampling assumptions;
- a conformal/selective guarantee;
- a worst-case verification result over a defined set;
- an explicit statement that the license is empirical-only and sample-relative.

One generic calibrated form is

```text
Pr(R_{D,L}(M) <= epsilon | E_t) >= alpha,
```

but this notation is ambiguous until the probability is identified as Bayesian posterior probability, repeated-sampling confidence/coverage, or something else.

A more neutral architecture is:

```text
UpperRiskBound_{a,t,alpha}(M,D,L,E_t) <= epsilon.
```

The guarantee associated with `UpperRiskBound` must then be stated separately.

This stage index matters because licenses can change for two independent reasons:

1. new data changes the estimated risk;
2. a new alternative changes the baseline or best-known comparison.

No change in metaphysical truth is required for either update.

---

## 10. Units, scaling, and why `epsilon` has no meaning by itself

If loss is measured in meters, `epsilon` is in meters. If loss is squared error, `epsilon` has squared units. If loss is classification error, `epsilon` may be dimensionless. If loss is regret, it has utility units.

For any positive constant `c`, define

```text
R'(M) = c R(M),
epsilon' = c epsilon.
```

Then

```text
R(M) <= epsilon  iff  R'(M) <= epsilon'.
```

So adequacy belongs to the pair `(R,epsilon)`, not to `epsilon` alone.

The numerical size of the margin

```text
epsilon - R(M)
```

also depends on scale. An ordinal comparison may survive a monotone transformation while cardinal margin arithmetic does not. If downstream neural layers consume margins as quantities, the project must justify the normalization or calibration that makes those magnitudes comparable.

Possible normalizations include:

- relative error;
- error divided by measurement uncertainty;
- decision regret in normalized utility units;
- log risk ratios relative to a baseline;
- dimensionless physical groups.

These are substantive modeling decisions, not cosmetic preprocessing.

---

## 11. When a scalar `epsilon` is justified

A scalar threshold is well motivated when all of the following are approximately true:

1. A fixed task supplies a real-valued loss.
2. Domain performance has a justified scalar aggregation.
3. Trade-offs are already encoded in that loss or are irrelevant.
4. The scale and units are fixed or normalized.
5. The risk estimate can be calibrated or verified.
6. A threshold corresponds to a real action, safety, or adoption boundary.

Examples include:

- maximum acceptable mean absolute position error for a specified calculation;
- maximum failure probability for a defined component;
- maximum expected decision regret under a fixed utility model;
- minimum improvement over a named baseline after costs.

Under these conditions, `epsilon` is not arbitrary. It expresses the decision boundary already present in the task.

---

## 12. When a scalar `epsilon` should be rejected

A single scalar should not be assumed when:

- errors have incomparable units or stakeholders;
- catastrophic tail failures cannot be traded against average accuracy;
- the loss is only ordinal;
- hard constraints coexist with soft objectives;
- costs, robustness, coverage, and accuracy are intentionally kept separate;
- the domain is poorly specified or shifting;
- no defensible scalarization of values exists.

Then a more honest object is a vector:

```text
R(M,D) = (R_1(M,D),...,R_k(M,D))
```

with a tolerance vector

```text
epsilon = (epsilon_1,...,epsilon_k),
```

and componentwise adequacy

```text
R_i(M,D) <= epsilon_i for every hard dimension i.
```

Other dimensions may be handled through Pareto dominance, lexicographic priority, or explicit incomparability. This is not a failure to finish the scalar calculation. It may be the information the logic is supposed to preserve.

---

## 13. Four elementary consequences

These are definitional sanity checks, not deep metatheorems.

### Proposition 1: tolerance monotonicity

If

```text
Adeq(M;D,L,epsilon) iff R_{D,L}(M) <= epsilon,
```

then for `epsilon' >= epsilon`,

```text
Adeq(M;D,L,epsilon) implies Adeq(M;D,L,epsilon').
```

**Proof.** `R <= epsilon <= epsilon'`. Therefore `R <= epsilon'`.

This monotonicity should later be enforced by the neural parameterization rather than merely learned from examples.

### Proposition 2: positive rescaling invariance

For `c>0`, define `R'=cR` and `epsilon'=c epsilon`. Then

```text
R <= epsilon iff R' <= epsilon'.
```

This confirms that the numerical threshold is inseparable from its loss scale.

### Proposition 3: adequacy is not exclusivity

Two different models can both satisfy

```text
R(M_1,D) <= epsilon
and
R(M_2,D) <= epsilon.
```

Therefore adequacy alone does not select a unique model. A router needs a separate comparison, cost, tie-breaker, or mixture rule.

### Proposition 4: dominance does not erase adequacy

Suppose

```text
R(M_new,D) < R(M_old,D) <= epsilon.
```

Then `M_new` has lower risk, but `M_old` remains adequate under the same threshold.

This elementary separation between **adequate** and **best** is the mathematical core of retaining a superseded model. Whether the old model remains selected depends on costs, robustness, subdomains, and the model-selection rule—not on adequacy alone.

---

## 14. Boundary convention and the future ReLU mapping

There is a small but important mismatch between inclusive adequacy and strict positive activation.

Let

```text
s(M,D) = epsilon - R(M,D).
```

Then

```text
R(M,D) <= epsilon iff s(M,D) >= 0.
```

But

```text
ReLU(s) > 0 iff s > 0 iff R(M,D) < epsilon.
```

At exact equality, `ReLU(s)=0`, the same output produced by every negative score. The project must choose one convention:

1. define neural licensing strictly, `R < epsilon`;
2. keep inclusive adequacy, use the signed preactivation and a separate `s >= 0` comparator;
3. treat `s=0` as an undecided/no-slack boundary rather than an ordinary positive license.

This note recommends option 2 for the formal semantics:

- the signed score carries the complete comparison;
- an inclusive comparator determines the formal license;
- ReLU carries only positive usable slack downstream.

This preserves the distinction established in Task 1: ReLU is not the whole information state.

For the fallback form,

```text
s_B(M,D) = J(B,D) - J(M,D) - Delta,
```

the same boundary issue appears. Zero means exact indifference after costs, which may rationally license either fallback, candidate, or abstention depending on the tie policy.

---

## 15. Worked examples

### 15.1 Classroom projectile versus precision timing

Let `M_N` be a Newtonian model.

For a classroom projectile:

- `D_class` contains low-speed, weak-field trajectories over short durations;
- `L_class` may be relative position error;
- `epsilon_class` may be set by instructional or measurement resolution;
- `B_class` may be a constant-velocity or no-model baseline.

`M_N` can both beat `B_class` and satisfy the external tolerance.

For precision timing:

- `D_time` includes accumulated clock effects;
- `L_time` measures timing or downstream position error;
- `epsilon_time` is much stricter;
- the fallback may be the currently deployed corrected model, not “do nothing.”

The judgment changes because `D`, `L`, `epsilon`, and `B` change. The proposition “Newtonian mechanics is false” does not contain enough information to decide either use.

### 15.2 A classifier with abstention

Suppose `M` classifies medical images. The outside option `B` sends a case to a human reviewer.

- Predictive error alone is not enough because review has cost and delay.
- `J(B,D)` includes reviewer error, time, and expense.
- `J(M,D)` includes model errors and intervention costs.
- A hard false-negative constraint may remain separate from total expected cost.

The model should act only where it beats referral by enough and satisfies the hard constraint. Elsewhere the null branch routes to the human. This is a literal “otherwise” model.

### 15.3 A deteriorating status quo

If doing nothing causes harm, `J(B,D)` may be large. Many interventions can beat it, but only some meet a safety floor. This shows why baseline improvement and hard adequacy cannot be merged without checking units and values.

### 15.4 Multiple adequate scientific models

Suppose `M_1` and `M_2` both fall below the predictive threshold on `D`, but `M_1` is faster and `M_2` is more robust near the boundary. Neither dominates on the full objective vector. The correct output may be a retained pair of licenses rather than one winner.

---

## 16. What is forced, motivated, and optional

| Ingredient | Status from the main question | Reason |
|---|---|---|
| Model `M` | Directly forced | The question concerns successive theories/models. |
| Domain `D` | Directly forced | Superseded theories remain useful only in restricted contexts. |
| Performance comparison | Strongly motivated | “Useful” must distinguish reliance outcomes somehow. |
| Local loss `ell` | Operational choice | The question does not determine what mismatch matters. |
| Domain risk `R` | Operational choice | Mean, worst-case, tail, regret, and verification are different. |
| External `epsilon` | Sometimes externally forced | Safety, precision, law, or task requirements may supply it. |
| Baseline-induced `epsilon_B` | Pragmatically derived when a fallback exists | Candidate must beat what happens otherwise. |
| Improvement margin `Delta` | Decision/cost choice | Adoption may require more than weak improvement. |
| Comparison tolerance `eta` | Optional | Useful for noise, ties, and near-best retention. |
| Confidence/calibration `alpha` | Required for many finite-data claims | Observed error is not domain risk. |
| Agent/stage `a,t` | Required for epistemic licensing | Evidence and available models change over time. |
| Search budget/library `b,K` | Required for “best known” | No-better-model claims are relative to what was searched. |
| Cost vector | Optional but often necessary | Accuracy alone may not explain model retention. |
| Scalarization | Not forced | Multi-objective structure may need to remain partial. |

The exact final form is therefore not obtained in one step. It is assembled by making each hidden pragmatic choice explicit.

---

## 17. Recommended provisional notation

Use three layers in subsequent work.

### Minimal performance predicate

```text
Adeq(M;D,L,epsilon).
```

### Evidence-relative license

```text
CertAdeq_{a,t}(M;D,L,epsilon,alpha | E_t).
```

### Full pragmatic use-license

```text
Pi_{a,t,b}(M;D,L,epsilon,alpha,B,Delta,K | E_t).
```

with the intended factorization

```text
Pi = certified hard adequacy
     + sufficient improvement over fallback
     + admissibility among retrieved alternatives.
```

The plus signs here mean conjunction of requirements, not numerical addition.

For exposition, the paper may introduce `Pi(M,D,epsilon)` first as a deliberately compressed notation, then immediately unpack it. This gives the reader the intuitive object without pretending its exact signature fell directly out of the motivating question.

---

## 18. Draft opening argument for the eventual paper/post

The following is a compact prose version suitable for adaptation later:

> A bounded reasoner need not know whether a theory is finally true in order to know that relying on it produces smaller errors than relying on an alternative. This does not immediately give us a three-place logic of model, domain, and tolerance. It first gives us a model and a domain: Newtonian mechanics can succeed here and fail there. Error enters only when “succeeds” is operationalized against observations or the consequences of action. A tolerance enters when that graded performance is turned into a decision—use this model, keep the fallback, or abstain. Sometimes the tolerance is externally imposed by safety or precision. Sometimes it is induced by the status quo: a model is worth using only if it beats what we would otherwise do by enough to justify its cost. Thus `epsilon` is not a degree of falsity. It is a decision boundary on an explicitly chosen loss. And because observed error is itself estimated from finite evidence, the mature judgment must remain indexed by evidence, domain, and stage.

This should appear before neural-network geometry. It motivates why a later ReLU score may cross zero: zero can represent indifference with a fallback, while positive activation represents surplus performance. It also explains why the signed preactivation must be retained—negative values say how much better the fallback is.

---

## 19. Open questions handed to later tasks

Task 3 must decide how much of the following information is explicitly represented versus absorbed into learned vectors or weights:

- the model identity;
- the domain descriptor;
- the baseline/fallback;
- the local and aggregate loss;
- hard tolerance;
- improvement and near-best margins;
- uncertainty/calibration;
- cost and provenance.

Task 5 must decide whether `Pi` names the complete use-license or only the adequacy component.

Task 7 must give types to `D`, `L`, evidence, baselines, and model libraries.

Task 8 must define the finite-stage semantics and statistical interpretation of `alpha`.

Task 10 must replace scalar best-known comparison with Pareto dominance where required.

Task 16 must choose the boundary convention and ensure the neural architecture preserves access to signed scores.

Task 18 must decide whether cross-entropy trains adequacy, model selection, policy imitation, or some combination; these are not the same target.

## Task conclusion

`Pi(M,D,epsilon)` is best understood as a compressed endpoint of a derivation, not as an unexplained primitive. `M` and `D` come directly from the phenomenon of local retention under theory succession. Loss comes from operationalizing pragmatic success. `epsilon` comes from turning performance into a decision boundary, either through an external requirement, a fallback/status-quo comparison, or both. Comparison with other known models is a further admissibility condition, not the definition of empirical adequacy itself.
