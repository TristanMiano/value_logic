# Domain Transport and Routed-Cover Bounds

Status: Task 14A cross-layer theorem cluster

Date: 2026-07-12

Depends on: [`07_core_calculus.md`](07_core_calculus.md), [`08_metatheory.md`](08_metatheory.md), [`04_dominance_retention.md`](04_dominance_retention.md), and [`05_atlas.md`](05_atlas.md)

## Durable result summary

This file proves the quantitative extension results that connect the compact license calculus to subdomains, hard routers, bridge models, blends, and composed use plans. It adds no core carrier.

1. **Free restriction of expected-risk adequacy is equivalent to an almost-sure pointwise bound.** For nonnegative integrable loss, every positive-measure measurable subdomain has conditional expected loss at most `epsilon` iff the loss is at most `epsilon` almost surely. A parent expected-risk certificate alone can hide an arbitrarily bad positive-measure subdomain.
2. **Hard-routed risk has an exact partition decomposition.** Under measurable coverage, the global loss is the sum of correct-route, misroute, and fallback integrals. Bounded misroute and fallback losses give an explicit penalty bound. A whole-cell mean certificate can bound the correct integral conservatively, but multiplying that mean by the selected mass is invalid unless the selected subset is separately certified or the cell bound is pointwise/uniform.
3. **Prediction bridges control task risk only through a task-loss regularity bridge.** If task loss is `K`-Lipschitz in the translated prediction and two chart outputs disagree by mean `delta`, their risks differ by at most `K delta`. A convex blend inherits corresponding excess-risk bounds. Predictive closeness alone does not control discontinuous or unbounded-sensitivity task loss.
4. **Finite plan-DAG errors propagate through downstream sensitivities.** With coordinatewise Lipschitz constants and intrinsic component errors valid on the reachable perturbation tube, output error is bounded by a path-sum of products of downstream Lipschitz constants. Outer Lipschitz task loss turns that into an excess-risk bound. Naive unweighted summation fails under amplification; cost addition also requires an explicit resource aggregator.
5. **Exact group-valued bridges admit global frame potentials iff every cycle product is identity.** A nontrivial cycle defect is precisely an obstruction to path-independent global coordinates on the declared overlap graph.

All results are conditional. The finite regression witnesses are executable in [`verification/test_transport_routing.py`](../verification/test_transport_routing.py).

## 1. Probability and transport notation

Let

```text
(X,Sigma,mu)
```

be a probability space. All sets below are measurable, all routing functions are measurable into finite discrete sets, and all losses are measurable. Whenever a risk or conditional disagreement is displayed, the relevant quantity is assumed integrable. For a nonnegative integrable loss `ell:X->[0,infinity)` and a set `A` with `mu(A)>0`, define

```text
R_A(ell) = (1/mu(A)) integral_A ell dmu.
```

Null sets do not receive ordinary conditional means. A carrier subset of zero parent probability may still support a new domain with a newly supplied measure, but it is not obtained by conditioning `mu`.

For predictions in a normed vector space `Y`, `norm(y-y')` is computed only after a typed bridge has placed both predictions in the same frame and given interpolation/disagreement a task meaning.

## 2. Exactly when expected adequacy restricts freely

### Theorem 1: all-subdomain expected adequacy iff pointwise adequacy almost surely

Let `ell` be nonnegative and integrable, and let `epsilon>=0`. The following are equivalent:

1. for every `A in Sigma` with `mu(A)>0`,

   ```text
   R_A(ell) <= epsilon;
   ```

2. `ell(x)<=epsilon` for `mu`-almost every `x`.

**Proof.** If (2) holds, integrate the almost-sure inequality over any positive-measure `A` and divide by `mu(A)`.

Conversely, suppose (2) fails. Then

```text
B={x:ell(x)>epsilon}
```

has positive measure. Since `ell-epsilon` is positive on `B`, there is some integer `n>=1` for which

```text
B_n={x:ell(x)>=epsilon+1/n}
```

has positive measure; otherwise `B=union_n B_n` would be null. Hence

```text
R_{B_n}(ell) >= epsilon+1/n > epsilon,
```

contradicting (1). `square`

The nonnegativity hypothesis matches the project's risk interpretation. The equivalence also holds for an integrable real-valued `ell`; integrability and measurability are what make the conditional means and superlevel sets available.

### Corollary 2: certificate criterion for free restriction

An expected-risk adequacy certificate can be transported without re-evaluation to **every** positive-measure measurable subdomain exactly when its premises establish the almost-sure bound

```text
ell <= epsilon  mu-a.s.
```

or an equivalent uniform certificate. A certificate of only

```text
R_X(ell)<=epsilon
```

does not suffice.

This is a semantic transport theorem. Operational reuse also requires the same loss, frame, task, measure conditioning, certificate mode, and provenance validity.

### Counterexample 3: parent average hides a bad subdomain

Let `X=[0,1]` with uniform measure and

```text
ell(x)=1  on [0,0.1]
ell(x)=0  otherwise.
```

Then `R_X(ell)=0.1`. At tolerance `epsilon=0.1`, the parent domain is adequate, but

```text
A_bad=[0,0.1],
R_A_bad(ell)=1.
```

The same construction can hide the bad region inside one member of any coarse finite partition. Testing only a declared family of cells yields guarantees only for that family, not for every measurable subdomain.

### Qualification 4: null sets and data-dependent scopes

Theorem 1 concludes an almost-sure, not everywhere, bound. Changing loss on a null set does not change any positive-measure conditional expectation. If a router or analyst chooses `A` using the same evaluation data, the population identity remains true for the resulting measurable set, but a finite-sample certificate needs simultaneous validity, sample splitting, or another selection-aware procedure. Measurability alone is not an operational answer to post-selection.

**Project impact.** Aggregate expected adequacy must not be silently copied to learned subdomains. Task 15 must encode certificate scope, and the experiment must distinguish whole-domain evidence, prespecified-cell evidence, and pointwise/uniform support.

## 3. Hard-router risk decomposition

### 3.1 Selection cells

Let `C_0,C_1,...,C_m` be a measurable partition of `X`. Each `C_i`, for `i>=1`, is the cell on which expert `i` is the declared correct/reference route for this theorem. `C_0` is the declared gap/fallback-only cell and may be empty. These cells may refine overlaps in a scientific licensed cover; they are a selection/evaluation partition, not a claim that scientific domains are disjoint.

Let the hard router be

```text
r:X -> {1,...,m,F},
```

where `F` is the explicit fallback. Let `ell_j(x)` be the loss incurred by expert `j` on `x`, and let `ell_F(x)` be fallback loss. Define

```text
G_i = C_i intersection {x:r(x)=i}                    correct-route cell
M   = union_i (C_i intersection {x:r(x) in I\{i}})
      union (C_0 intersection {x:r(x) in I})          misroute/unlicensed event
B   = {x:r(x)=F}                                      fallback event.
```

`G_1,...,G_m,M,B` form a measurable partition of `X`. Define routed loss

```text
ell_r(x)=ell_{r(x)}(x) if r(x) in I
        =ell_F(x)      if r(x)=F.
```

### Theorem 5: exact hard-router decomposition

For nonnegative integrable routed loss,

```text
R(r)
 = sum_i integral_{G_i} ell_i dmu
   + integral_M ell_r dmu
   + integral_B ell_F dmu.
```

Equivalently, when the conditioning events have positive measure,

```text
R(r)
 = sum_i mu(G_i) R_{G_i}(ell_i)
   + mu(M) R_M(ell_r)
   + mu(B) R_B(ell_F).
```

Zero-measure terms are defined as zero without assigning a conditional mean.

**Proof.** The displayed events are a finite measurable partition of `X`. Split the integral of `ell_r` over that partition and use the definition of conditional mean on positive-measure parts. `square`

**Active-set version.** A scientific overlap need not have one uniquely correct expert. Let `A(x) subseteq I` be the measurable set of authorized/reference experts, define

```text
G_j={x:r(x)=j and j in A(x)},
M={x:r(x) in I and r(x) notin A(x)},
B={x:r(x)=F}.
```

These events again partition `X`, so the same identity and bounds hold. The cell presentation is the special case `A(x)={i}` on `C_i` and `A(x)=empty` on `C_0`.

### Theorem 6: bounded misrouting/fallback penalty

Assume

```text
R_{G_i}(ell_i) <= epsilon_i  whenever mu(G_i)>0,
ell_r <= L_M  almost surely on M,
ell_F <= L_F  almost surely on B.
```

Then

```text
R(r)
 <= sum_i mu(G_i) epsilon_i
    + L_M mu(M)
    + L_F mu(B).
```

**Proof.** Substitute each bound into Theorem 5. `square`

This is the sharp form when certificates cover the actual selected subsets `G_i`.

### Corollary 7: conservative bound from whole-cell expected certificates

Suppose only

```text
R_{C_i}(ell_i) <= epsilon_i
```

is certified. Because loss is nonnegative and `G_i subseteq C_i`,

```text
integral_{G_i} ell_i dmu
 <= integral_{C_i} ell_i dmu
 <= mu(C_i) epsilon_i.
```

Therefore

```text
R(r)
 <= sum_i mu(C_i) epsilon_i
    + L_M mu(M)
    + L_F mu(B).
```

This conservative bound may count loss on misrouted cases once through the whole-cell certificate and again through the explicit misroute penalty; that is the price of not knowing the selected-subset risk. The selected-mass coefficient `mu(G_i)` cannot replace `mu(C_i)` without a selected-subset or pointwise certificate. By Theorem 1, an almost-sure cell bound `ell_i<=epsilon_i` does justify `mu(G_i)epsilon_i` for every measurable router selection.

### Counterexample 8: selection invalidates naive rescaling

Let one cell `C` have two equal-probability parts, with expert loss `0` on the first and `1` on the second. Then

```text
R_C(ell)=0.5.
```

If the router selects the expert only on the high-loss half, `mu(G)=0.5` and the actual correct-route contribution is `0.5`. The naive term

```text
mu(G) R_C(ell)=0.25
```

underestimates it by a factor of two. The conservative whole-cell integral bound is `mu(C)R_C=0.5`, which is exact here.

### Counterexample 9: rare misrouting can have unbounded cost

For any small `p>0`, let `mu(M)=p` and set routed loss on `M` to `1/p^2`. The misroute contribution is `1/p`, which diverges as `p` decreases. No risk bound depending only on misroute probability exists without bounded loss, a tail/moment condition, or a direct conditional-risk estimate.

### Counterexample 10: missing coverage loses mass

If `C_0,C_1,...,C_m` do not cover `X` and the uncovered set is omitted rather than assigned to a reference cell or explicit gap, the proposed decomposition simply drops its loss. Coverage, explicit gaps, and fallback events are theorem hypotheses, not presentation details.

**Project impact.** The later router must report at least correct-selected risk or a valid conservative substitute, misroute mass and loss scale, fallback mass and loss, and coverage. Accuracy of route labels alone cannot establish deployed risk.

## 4. From prediction bridges to task-risk bounds

Let `O subseteq X` have positive measure. Let `f:O->Y` be one chart prediction and `g:O->Y_g` another. A typed bridge

```text
T:Y_g -> Y
```

places `g` in the task frame. Let `z(x)` be the target outcome and `lambda(y,z)` the task loss. Write

```text
R_O(f)=E[lambda(f(x),z(x)) | x in O].
```

Assume a uniform Lipschitz condition in the prediction argument:

```text
abs(lambda(y,z)-lambda(y',z)) <= K norm(y-y')
```

for all predictions and outcomes reached on `O`.

### Theorem 11: bridge disagreement bounds risk difference

If

```text
E[norm(f-Tg) | O] <= delta,
```

then

```text
abs(R_O(f)-R_O(Tg)) <= K delta.
```

The same conclusion follows from the stronger pointwise bridge bound `norm(f-Tg)<=delta` almost surely.

**Proof.** Pointwise Lipschitzness gives

```text
abs(lambda(f,z)-lambda(Tg,z)) <= K norm(f-Tg).
```

Integrate conditionally and apply `abs(E U)<=E abs(U)`. `square`

### Theorem 12: convex blend excess-risk bounds

Assume `Y` is convex and let measurable `a:O->[0,1]`. Define the blended use plan

```text
h=a f + (1-a) Tg.
```

Then

```text
R_O(h)
 <= R_O(f)  + K E[(1-a) norm(f-Tg) | O],

R_O(h)
 <= R_O(Tg) + K E[a norm(f-Tg) | O].
```

In particular, a pointwise disagreement bound `norm(f-Tg)<=delta` yields

```text
R_O(h) <= min(
    R_O(f)  + K delta E[1-a | O],
    R_O(Tg) + K delta E[a | O]
).
```

**Proof.** `norm(h-f)=(1-a)norm(Tg-f)` and `norm(h-Tg)=a norm(f-Tg)`. Apply the Lipschitz inequality and integrate. `square`

No convexity of task loss is required. If `lambda(.,z)` is also convex, the familiar pointwise convex-loss bound supplies an additional comparison to the weighted component losses.

### Counterexample 13: predictive closeness without task regularity

Let binary decisions be obtained by thresholding a scalar prediction at zero, and use zero-one decision loss. Predictions `f=-eta` and `Tg=+eta` are only `2 eta` apart, which can be arbitrarily small, but they induce opposite actions; for a suitable target, their losses differ by one. Zero-one threshold loss is not Lipschitz in the raw score at the decision boundary.

Even smooth squared loss is not globally Lipschitz on an unbounded prediction range: with target zero, predictions `N` and `N+delta` differ by `delta` while their squared losses differ by `2N delta+delta^2`.

### Qualification 14: bridge risk is not blend authorization

Theorems 11–12 require a common task frame, meaningful norm, measurable bridge and weights, and Lipschitz control on the reached range. They do not show that convex combinations preserve conservation laws, discrete validity, calibration, safety constraints, or causal meaning. The blend remains a new use plan with its own `WF`, constraints, fallback, and certificate trace.

**Project impact.** A bridge head should expose disagreement and the task-sensitivity constant or certificate used to translate it. Smooth interpolation or small prediction distance alone is not an adequacy certificate.

## 5. Finite plan-DAG error and cost propagation

Let a finite directed acyclic graph have node set `V` and output node `o`. Each node `v` has an ideal operation `F_v` and implemented operation `Fhat_v`. For every edge `u->v`, input/output types and frames match.

Let `e_v` be the distance between implemented and ideal node outputs on the same external case. Assume, throughout the full reachable perturbation tube:

1. intrinsic implementation error at node `v` is at most `delta_v` when ideal and implemented operations receive the same admissible input tuple;
2. `F_v` is coordinatewise Lipschitz:

   ```text
   d_v(F_v(y),F_v(y'))
   <= sum_{u in pred(v)} L_{u,v} d_u(y_u,y'_u).
   ```

Then triangle inequality gives the local recurrence

```text
e_v <= delta_v + sum_{u in pred(v)} L_{u,v} e_u.
```

### Theorem 15: path-sensitivity error budget

For nodes `u,v`, define

```text
W_{v,v}=1,
W_{u,v}=sum over directed paths p:u->v of
        product over edges (a->b) in p of L_{a,b},
```

and `W_{u,v}=0` when no path exists. Then

```text
e_o <= sum_{u in V} W_{u,o} delta_u.
```

**Proof.** Topologically order the DAG. Repeatedly substitute the local recurrence. Every intrinsic error `delta_u` reaches `o` once for each directed path from `u` to `o`, multiplied by the Lipschitz constants along that path. Finiteness and acyclicity make the expansion finite. `square`

### Corollary 16: excess task risk of a composed plan

If the outer task loss is `K`-Lipschitz in the output on the reached range, then relative to the ideal composed plan,

```text
R(Fhat_G)-R(F_G)
 <= K sum_{u in V} W_{u,o} delta_u.
```

Use absolute value for a two-sided risk-difference bound.

**Proof.** Apply the pointwise output bound from Theorem 15 and then Theorem 11 with the identity bridge. `square`

### Proposition 17: additive cost is an accounting hypothesis

If every node executes once, scalar node costs `c_v` are measured in the same additive unit, and orchestration cost is `c_coord`, then

```text
c_total = c_coord + sum_v c_v.
```

For upper bounds, replace equality with `<=` when the terms are certified upper bounds. Parallel latency is normally a critical-path quantity, peak memory depends on schedule/liveness, shared caching can reduce work, and contention can increase it. Those resources require their own aggregation in `q`; calling all of them “cost” does not make them additive.

### Counterexample 18: unweighted error summation fails under amplification

Let the first component incur error `delta>0`, and let the downstream ideal component be `F_2(y)=K y` with no intrinsic error. The final error is `K delta`. For `K>1`, this exceeds the naive sum `delta+0`. The path-sensitivity theorem gives the correct weight `W_{1,2}=K`.

### Counterexample 19: nominal-input certificates need not compose

Let the nominal intermediate value be zero. An upstream component perturbs it to a small positive `delta`. Let the downstream implementation agree perfectly with its ideal operation at zero but have arbitrarily large error at `delta`. A certificate tested only at the nominal input reports zero downstream intrinsic error, while the composite fails. Theorem 15 avoids this by requiring intrinsic and Lipschitz bounds on the entire reachable perturbation tube.

**Project impact.** The plan registry must store interface/frame compatibility, the domain on which each local error bound holds, downstream sensitivities or a direct composite certificate, and resource-specific aggregation. Component grants are explanatory inputs, not a substitute for composite assessment.

## 6. Exact bridge cycles and global frame potentials

This optional extension formalizes the Task 5 cycle audit in the concise case where exact frame changes take values in a group `G`.

Let `H=(I,E_H)` be a finite overlap graph. For every oriented edge `i->j`, let

```text
g_ij in G,
g_ji = inverse(g_ij).
```

For a path `v_0->...->v_k`, define the ordered product as

```text
g_{v_{k-1},v_k} ... g_{v_0,v_1},
```

so the first traversed map acts first. A **frame potential** is a family `h_i in G` such that

```text
g_ij = h_j inverse(h_i)
```

on every oriented edge.

### Theorem 20: cycle identity iff global frame potentials exist

On each connected component of `H`, the following are equivalent:

1. every closed walk has ordered bridge product equal to the identity;
2. a frame potential `{h_i}` exists.

**Proof.** If potentials exist, substitute `g_ij=h_j h_i^{-1}` around a closed walk. Adjacent factors cancel and the product is identity.

Conversely, choose a root `r` and set `h_r` to identity. For any vertex `i`, define `h_i` as the ordered product along a path from `r` to `i`. If two paths are chosen, following one and the reverse of the other forms a closed walk, so the cycle hypothesis makes their products equal. Thus `h_i` is well defined. Extending a root-to-`i` path by edge `i->j` gives `h_j=g_ij h_i`, equivalently `g_ij=h_j h_i^{-1}`. `square`

Potentials are unique up to common right multiplication on each connected component.

### Counterexample 21: pairwise bridges can be cycle-inconsistent

Use the additive group of real translations on a triangle. Let

```text
g_12=0,
g_23=0,
g_31=1.
```

Every edge is individually invertible, but the cycle sum is `1`, not `0`. No global potentials exist. Transporting a quantity around the triangle changes its frame by one unit.

Approximate, partial, noninvertible, or scope-varying bridges need defect bounds and path-specific provenance rather than this exact theorem.

**Project impact.** The atlas may store pairwise bridges without claiming one global coordinate system. A router or explanation that compares paths must surface cycle defects; otherwise its result can depend on an undocumented translation path.

## 7. Assumption and failure matrix

| result | essential hypotheses | failure when dropped |
|---|---|---|
| all-subdomain equivalence | measurable positive-measure scopes; integrable loss; all subdomains quantified | parent/coarse averages hide bad subsets; null points remain invisible |
| routed-risk bound | measurable covering partition; explicit fallback; selected-subset or conservative local integrals; bounded/tail-controlled penalties | selection bias, omitted gap mass, rare catastrophic misroutes |
| bridge-to-risk bound | common typed frame; meaningful norm; uniform/local Lipschitz loss; measurable disagreement | small prediction gap can flip discontinuous decisions or have unbounded loss effect |
| blend bound | convex output meaning; measurable weights; bridge assumptions | invalid outputs, broken invariants, or uninterpretable interpolation |
| plan-DAG budget | finite acyclic graph; compatible interfaces; tube-valid local errors; downstream Lipschitz constants | amplification, distribution shift between components, undefined feedback cycles |
| additive cost | common unit and explicit additive accounting | parallelism, caching, liveness, contention, and mixed resources change aggregation |
| cycle/potential theorem | exact invertible group-valued bridges on one declared graph/scope | path dependence, unresolved maps, nonzero cycle defects |

## 8. Relation to the compact license calculus

These are extension theorems because they require measure, routing, metric, Lipschitz, graph, and group structure not present in every core request. They enter the core only through typed atoms and certificates:

- a `DomainRestriction` or adequacy witness records whether it is aggregate, declared-cell, selected-subset, pointwise, or uniform;
- a routed plan is a new `e` whose context records the selection partition, loss, fallback, coverage, and penalty assumptions;
- a bridge certificate records translation frame, disagreement norm, scope, task-sensitivity rule, and provenance;
- a blend is a new use plan and rechecks hard constraints;
- a component propagation certificate records the DAG, local error domains, sensitivities, and resource aggregation;
- a cycle audit is report-only unless a profile or transport operation explicitly requires path independence.

The architecture-neutral neural interface therefore needs more than an active-set or router-accuracy label. Depending on the requested theorem, it must preserve local risk scope, selected mass, misroute/fallback mass and severity, bridge disagreement and task sensitivity, component sensitivities, or cycle defect. ReLU can be the reference scorer for these quantities; none of the bounds is ReLU-specific.

## 9. Result classification

| result | classification | paper role |
|---|---|---|
| all-subdomain iff almost-sure bound | elementary measure characterization with a strong transport consequence | paper-carrying extension result |
| exact router decomposition | finite partition identity | infrastructure |
| bounded routed-risk inequality plus selection counterexample | quantitative bound and failure mode | paper-carrying routing result |
| bridge/blend task-risk inequalities | elementary Lipschitz transport bounds | paper-carrying bridge result |
| path-sensitivity DAG budget | finite perturbation-propagation theorem | composition extension |
| cycle/potential equivalence | standard graph/group cocycle characterization | optional atlas extension |

No priority or novelty over the underlying measure, Lipschitz, perturbation, or cocycle mathematics is claimed. The project contribution is their typed integration with profile-indexed licenses, gaps, fallbacks, diagnostics, and neural information requirements. Checkpoint B classifies this cluster as load-bearing integration rather than an independent novelty headline.

## 10. Decisions carried forward

1. Parent expected risk restricts automatically to every positive-measure subdomain only under an almost-sure loss bound.
2. Prespecified finite-cell certificates transport only to those cells unless a stronger theorem is supplied.
3. Router selection changes the evaluated distribution; selected-subset and whole-cell risk are different quantities.
4. Deployed router risk exposes correct-route, misroute, fallback, and uncovered-mass terms.
5. Misroute probability without loss severity is not a safety bound.
6. Prediction disagreement becomes task-risk disagreement only through a typed regularity bridge.
7. A blend is a new plan and rechecks meaning, invariants, constraints, and fallback.
8. Component errors are weighted by downstream sensitivity and must hold on the reachable perturbation tube.
9. Cost aggregation is resource-specific rather than universally additive.
10. Pairwise exact bridges produce global coordinates exactly when cycle products vanish.
11. These results constrain the later neural outputs but do not choose a neural architecture.

## Task conclusion

The licensed-cover metaphor now has quantitative teeth without pretending that local certificates glue themselves together. Aggregate performance can conceal a bad subdomain; routing can select precisely the hard cases; rare mistakes can dominate expected loss; near-identical predictions can induce different actions; and small upstream errors can be amplified by a composed solver. Each positive result therefore names the structure that blocks its counterexample.

This is the correct bridge from the finite-stage logic to a learned scorer/router. The network may estimate local risks, routing events, bridge disagreement, or component sensitivities, but the mathematical decoder must retain the scope, coverage, regularity, and penalty assumptions that turn those estimates into a licensed routed plan.
