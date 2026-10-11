# P3-02 — Probability information in values

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: **COMPLETE at finite probability-information scope; all executable evidence is DEVELOPMENT**.
[Research90 and exact actuals](../work_logs/P3_02_2026-10-07_S1/actuals.json) are closed; P3-N01 remains NOT YET SUPPORTED.
Contract: [P3-01](../foundations/01_problem_contract.md), especially Q5 and
duties V01/V02/R01/I01. [Observed session](../work_logs/P3_02_2026-10-07_S1.md).
P3-A is a separate gate; this note does not attempt it or start P3-03.

## 1. Answer and exact scope

Values **can** contain probability information. The answer depends on their
meaning, the retained queries, the admitted source family, and what must be
recovered. A full coherent linear expectation functional determines its
probability law. A finite vector of expected losses determines only the law's
equivalence class under those measurements, unless the measurements separate
all admitted laws. That class may nevertheless determine every loss needed
for a task, a sharp interval, or an optimal action.

This note investigates a **finite linear-expectation fragment**. It does not
assume that every useful value must be scalar, bounded, probabilistic or
represented by a neural network. Nor does it assert that the finite admitted
states are all models of arithmetic. The source and loss table are supplied
or constructed through the separately charged, versioned information contract.
The results are conditional mathematics about that table, not a logical-belief
learning algorithm or empirical validation of its probability weights.

The ordinary comparator receives the same states, known loss semantics,
constraints, observations and resources. It may use a probability vector, a
credal polytope, linear algebra, linear programming and the same certificates.
The familiar expectation identity and rank/fiber method are reconstructed
antecedents; phase two already uses the latter for retention and repair
([paper §7](../../paper_v2.md#7-what-must-survive-a-cost-revision)). No priority
or superiority claim follows from writing those results in value terminology.

### Reading guide

| Question | Main location |
|---|---|
| Which probabilities or expectations do known losses identify? | §§3–4: binary stakes, fibers, normalization, row spaces and source restrictions |
| What remains useful without a full law? | §§5–7: one decision, certified intervals, regret and missing dependence; §9: essential-action characterization |
| What do coherence and scores actually supply? | §8, with finite-sample and scalar-risk boundaries in §16 |
| How do units, payoff uncertainty and noisy estimates change recovery? | §§10–12, with nonlinear units and outcome stakes in §17 |
| Which conclusions enter the inherited proof language? | §13: actual source/unit certificates and obstructions |
| What about conditional probabilities and strong ordinary estimation? | §§14–15: ratio recovery, fractional LP and affine optimal-recovery comparison |
| What additional queries are necessary and available? | §18: calibrated target repair, bounded stakes, restricted menus and offset recovery |
| What is implemented, and what evidence was saved? | §19: exact audit/verifier interface and development provenance |
| Can action choice require less than numerical target recovery? | §20: calibrated decision criteria, coefficient alphabets and approximate regret |
| What contribution is supported or still open? | §21: ordinary comparisons, the narrower adaptation candidate and phase-wide limits |

## 2. Types, input contract and the basic fiber

Let the finite state space be `Omega={1,...,n}`, with `n>=1`. A supplied
admissible family `P` is a nonempty subset of the probability simplex

```math
\Delta_n=\{p\in\mathbb R^n:p_i\ge0,\ \mathbf1^Tp=1\}.
```

Here the subscript counts states; the simplex has dimension `n-1`. In this
fragment `p` may be an explicitly subjective law over unresolved assessment
cases. It is not mathematical truth, a proof-status vector, or an asserted
physical randomness of a fixed mathematical answer.

| Object | Meaning | What it does not imply |
|---|---|---|
| `L[j,i]` | Known statewise loss of query/action `j` in state `i`, with units and scope | A belief about which state occurs |
| `y=Lp` | Exact expected losses under one fixed supplied law | Accuracy of that law for an application |
| `y_hat` | Learned or numerically estimated expected-loss vector | Existence of a compatible law without a coherence check |
| `F(y)` or `F(y_hat,epsilon)` | All admitted laws compatible with exact observations or stated error bounds | A unique law, or a statistical coverage guarantee without its premises |
| `q` | A reported probability or a decoded compatible estimate | That it was elicited optimally or learned from sufficient evidence |
| `L[:,i]` | Realized losses when state `i` occurs | The vector of pre-outcome expectations |

For a known matrix `L in R^(m x n)`, define

```math
F(y)=\{p\in P:Lp=y\}.
```

This is the **observation fiber**. An empty fiber means the exact observations
and premises are incompatible, not that every decision has a valid bound.
Existence, exact knowledge and estimation must remain separate. When the
matrix/source are rational polyhedral, the finite algebraic certificates below
can use rational arithmetic. Real coefficients have the same mathematical
identities but need a separate computational encoding.

### Fiber principle (PI-1)

For any specified target map `T:P -> Z`, an exact decoder from `Lp` exists
if and only if

```math
Lp=Lq\quad\Longrightarrow\quad T(p)=T(q)
\qquad(p,q\in P).
\tag{1}
```

**Proof.** A decoder has only one output on the common input. Conversely, if
(1) holds, define its output on an attainable observation to be the common
target value on that fiber. This proves existence, not computability or cheap
access. A pair with identical observations and different targets is a complete
obstruction to that exact service. A randomized decoder cannot be almost surely
correct on both members of such a pair. No linearity of the decoder is assumed.

Different requests choose different `T`: the full law, a finite vector `Cp`,
an event probability, a preference relation, or a specified decision. Computing
a range over the fiber is another service and need not produce a point.

## 3. Binary losses and nuisance stakes

For an event with subjective probability `p`, known losses `c_1` on the event
and `c_0` off it give

```math
v=c_0+(c_1-c_0)p.
\tag{2}
```

If `c_1 != c_0`, then `p=(v-c_0)/(c_1-c_0)`. An exact feasible expectation
lies between the two losses. If they are equal, the value is constant and
contains no event-probability information. This reconstructs the elementary
bridge already used in P3-01. Changing the known loss gap changes sensitivity:
an expected-loss error bounded by `eta` yields probability error at most
`eta/|c_1-c_0|`, before intersection with `[0,1]`.

**Confounding.** For loss zero on truth and `K` on falsity, `v=K(1-p)`.
The same `v=3` results from `(K,p)=(10,7/10)` or `(100,97/100)`. Unknown
additive cost `b` adds another nuisance in `v=b+K(1-p)`. It must be retained,
calibrated or included in the compatible family. Under the declared zero-versus-
positive-`K` payoff contract, a realized zero loss identifies that trial's event
outcome, not the earlier subjective probability. With zero stakes even this
outcome inference disappears.

**Unknown stakes do not always prevent recovery.** If an exhaustive partition
has values `v_i=s p_i` with the **same unknown positive** `s`, then

```math
s=\sum_i v_i,\qquad p_i=\frac{v_i}{\sum_jv_j}.
\tag{3}
```

Normalization calibrates the scale. With an unknown common offset, a known
zero-payoff anchor with report `v_0=b` gives `v_i=b+s p_i`, and the same formula
uses `v_i-v_0`. This works because the reports share an explicitly stipulated
transformation; unrelated unknown stakes `v_i=s_i p_i` do not obey it.
With unknown scale or offset the observation map is a map of the enlarged
state `(p,s,b)`. The general fiber principle still applies, but the fixed-known-
`L` rank criterion below does not apply without a separate calibration argument.
If the common scale is zero, the calibration disappears. Negative scales need
their declared sign when transporting preferences. A nonzero scale suffices
for the bare ratio identity, but the positive case matches ordinary stakes.

Equation (3) is a mathematical decoder, not automatically a native variable
division rule. A fixed rational probability threshold `t` can nevertheless be
tested by the affine inequality `v_i >= t sum_j v_j` under the separately
justified positive-denominator premise. Exact probability output and threshold
certification thus have distinct implementation needs.

## 4. Exact finite recovery

Put

```math
A=\begin{bmatrix}\mathbf1^T\\L\end{bmatrix},\qquad
b(y)=\begin{bmatrix}1\\y\end{bmatrix}.
\tag{4}
```

The normalization row is known information. Omitting it gives an incorrect
rank requirement.

### Full law and specified expected losses (PI-2)

On the **full simplex**, the following are equivalent for a target matrix `C`:

1. `Cp` is exactly determined by `Lp` for every `p in Delta_n`.
2. `ker A` is contained in `ker C`.
3. Every row of `C` is in the row span of `A`.
4. There are a vector `a` and matrix `B` such that
   `C=a 1^T+B L`, giving `Cp=a+B y`.

In particular, the full law is recoverable exactly when `rank A=n`.
This is equivalent to affine independence of the `n` columns of `L`.
At least `n-1` independent scalar affine measurements are therefore needed
for global full-law recovery in this measurement class.

**Proof.** Conditions 2 and 3 are the finite rowspace/nullspace identity;
3 and 4 merely split off the normalization row. Condition 4 is an explicit
decoder. If 2 fails, choose `d in ker A` with `Cd != 0`. The uniform law
`u=(1/n,...,1/n)` has positive coordinates. For sufficiently small `t>0`,
`p_+=u+td` and `p_-=u-td` both belong to the simplex. They have the same `Lp`
because `Ld=0`, and different targets because `Cd != 0`, contradicting 1.
Take `C=I` for full-law recovery. This necessity argument defeats **arbitrary
decoders**, not just affine decoders.

The coordinate lower bound is not a bit bound, a sample-complexity bound or a
prohibition on arbitrary nonlinear real encodings. A known finite catalogue of
laws may be separated by one carefully chosen linear measurement. Computation,
precision, storage and acquisition remain charged under P3-01's contract.

### Constructive positive case

Retain `y_1=p_1` and `y_2=p_2` on three states. Then
`p=(y_1,y_2,1-y_1-y_2)` is the unique compatible law whenever
`y_1,y_2>=0` and `y_1+y_2<=1`. More generally, `n-1` known singleton-indicator
expectations recover all `n` probabilities. The decoder does not require the
values to have been named probabilities at storage time; their payoff meanings
and normalization are what license the interpretation.

### Task-only positive case

Retain `y=p_1` on three states. Every target loss of the form
`c=(alpha+beta,alpha,alpha)` has expectation `alpha+beta y` although `p_2`
and `p_3` remain unidentified. Thus an entire task family may be answered
exactly without a full-law decoder. One should test the requested family,
not demand more information than it uses.

### Restricted source families (PI-3)

For arbitrary `P`, use the literal fiber principle (1). If `P` is convex and
`V=span(P-P)` is its actual affine direction space, the target criterion is

```math
\ker(L|_V)\subseteq\ker(C|_V).
\tag{5}
```

**Proof.** Every admissible difference lies in `V`, proving sufficiency.
A nonempty finite-dimensional convex set has a relative-interior point. A
small relative ball about that point realizes sufficiently small opposite
perturbations in any direction of `V`, proving necessity as before. Restrict
attention to the actual affine hull, including any constraints that are tight
throughout the source. If it is explicitly `Hp=h`, with normalization included
and a relatively open feasible neighborhood, (5) is the row-span criterion
for `[H;L]`; an outer affine description that misses a smaller face can overcount.

Convexity matters to this rank characterization. For the nonconvex catalogue
`P={e_1,e_2,e_3}` and `L=(0,1,2)`, the value identifies the permitted law
despite `rank A=2<3`. On the full simplex, the same observation map does not.
Convexifying the source **before** imposing the observation can destroy exact
identification even of a linear target: at `y=1`, the catalogue admits only
`e_2`, whereas its convex hull also admits `(e_1+e_3)/2`. Native finite unions
of polyhedra must therefore retain their declared source semantics. In contrast,
convexifying an already formed fiber preserves its linear extrema and whether
a linear target is constant.

### Local identification at one observation (PI-4)

Global non-identification does not imply that every observation is ambiguous.
For `L=(0,1,2)`, observing `y=0` forces `p=e_1`; observing `y=1` admits both
`e_2` and `(e_1+e_3)/2`.

More precisely, for a nonempty full-simplex fiber let
`J={i:some p in F(y) has p_i>0}`. Restrict matrices to columns in `J`.
The target `Cp` is constant on this fiber exactly when

```math
\ker A_J\subseteq\ker C_J.
\tag{6}
```

**Proof.** Every fiber law is zero outside `J`. Averaging finitely many
feasible laws that collectively witness each member of `J` gives a feasible
law strictly positive on `J`. Opposite sufficiently small perturbations in
`ker A_J` are therefore feasible. This proves necessity and sufficiency by
the same argument. In particular the fiber is a singleton iff
`rank A_J=|J|`. The support of one arbitrary feasible law cannot replace `J`:
at `y=1`, selecting `e_2` alone would falsely certify uniqueness.

## 5. Preferences and decisions need their own service

Let a finite action family have rows `c_a`, with expected cost `c_a p`.
For one nonempty fiber write

```math
\mathrm{Opt}(p)=\arg\min_a c_a p.
```

The following are different requests:

| Requested service | Exact fiber condition |
|---|---|
| Every specified absolute cost | Each `c_a p` is constant |
| Every specified cost difference | Each `(c_a-c_b)p` is constant |
| Every pairwise preference, including ties | Each sign of `(c_a-c_b)p` is constant |
| The complete set of optimal actions | `Opt(p)` is constant |
| Some action guaranteed optimal | `intersection_(p in F(y)) Opt(p)` is nonempty |
| A prescribed tie-broken action | That particular selector is constant |

For a decoder that supplies *some* optimal action at every observation, the
common-optimum condition must hold on every nonempty fiber. It is necessary
because the reported action must work for all compatible laws, and sufficient
by selecting, for example, the first common optimum in a declared finite order.
This is an existence argument; the universal comparison still needs checking.

**A useful decision with unidentified absolute costs.** On three states retain
`y=p_1` and let `c_A=(0,1,2)`, `c_B=(1,0,1)`. Their expected costs are
`1-y+p_3` and `y+p_3`, so the difference is `1-2y`. Choose `A` for `y>1/2`,
`B` for `y<1/2`, and either at equality. Neither absolute cost nor the full
law is identified, while this changing, nonconstant decision is exact.

**Preferences are weaker than differences.** If `c_A=0` and `c_B=(1,2,3)`,
the strict preference for `A` holds for every law with no observed value,
although the difference varies. **One choice is weaker than all preferences:**
with `c_A=(0,0)`, `c_B=(1,3)`, `c_C=(3,1)`, action `A` is always best while
the ranking of `B` and `C` changes. **One choice is weaker than the optimum
set:** with `c_A=(0,0)`, `c_B=(0,1)`, action `A` always works but ties depend
on the law.

An expected-loss decision under a particular unobserved law `p`, an absolute minimax
decision over `F(y)`, and a minimax-regret decision are different consumers.
An ordinary robust optimizer may still select an action when there is no
common Bayes-optimal action; that does not recover the missing Bayes decision.

## 6. Partial identification and certificates

Exact recovery is one endpoint of a useful range of services. Let a nonempty
compatible source be the rational polytope

```math
F(y)=\{p\geq0:Ap=b(y),\ Gp\leq g\},
\qquad
\ell_y(c)=\min_{p\in F(y)}cp,\quad
u_y(c)=\max_{p\in F(y)}cp.
\tag{7}
```

Normalization is included in `A`, so the source is bounded. Both extrema are
attained. Convexity makes the target range the entire interval
`[ell_y(c),u_y(c)]`; on a finite union one can instead optimize on each nonempty
piece and take the outer extrema, while the attainable range may have gaps.
An interval of zero width is local exact recovery. An empty compatible source
is a failed premise, not a warrant to make an arbitrary decision.

### Checkable upper and lower certificates (PI-5)

For any free vector `lambda` and nonnegative vector `mu`,

```math
A^T\lambda+G^T\mu\geq c^T
\quad\Longrightarrow\quad
cp\leq\lambda^Tb(y)+\mu^Tg\quad(p\in F(y)).
\tag{8}
```

This is direct arithmetic: multiply the componentwise inequality by `p>=0`,
use the equalities, and multiply the upper inequalities only by nonnegative
coefficients. A feasible law attaining the proposed bound proves sharpness.
Apply the same construction to `-c` for a lower bound. Ordinary finite linear
programming duality supplies matching dual bounds when the primal is feasible
with finite optimum; a strictly positive law or a Slater point is not required
for this linear-programming statement. Rational data admit rational optimum
witnesses and dual certificates. This is an ordinary LP comparison and a
possible proof object for a native rational affine implementation, not a new
duality theorem. [P02-S5](../literature/02_probability_sources.md)

**Sharp three-state example.** Retain `y=p_2+2p_3=1/2`. Every compatible law is

```math
p=(1/2+t,\ 1/2-2t,\ t),\qquad 0\leq t\leq1/4.
\tag{9}
```

Thus the expected singleton loss `p_3` is exactly bounded by `[0,1/4]`.
The lower certificate is `p_3>=0`; the upper is
`2p_3<=p_2+2p_3=1/2`. The laws `(1/2,1/2,0)` and `(3/4,0,1/4)` attain
the endpoints. Against a constant fallback loss `3/10`, the singleton gamble
is strictly better at every compatible law. Against a fallback `1/8`, the two
endpoints require opposite optimal actions. The same incomplete probability
information is sufficient for the first decision and insufficient for the
second.

### Decision regret can be bounded directly (PI-6)

For a finite action family, the worst compatible regret of action `a` is

```math
W_y(a)=\max_{p\in F(y)}\left(c_a p-\min_b c_b p\right)
      =\max_b u_y(c_a-c_b).
\tag{10}
```

The second equality uses only a maximum over a finite family; it holds for
nonconvex compact sources too. Since `b=a` is included, `W_y(a)>=0`.
Moreover, `W_y(a)=0` exactly when `a` is optimal at every compatible law.
Minimizing `W_y(a)` defines a minimax-regret action if no common optimum exists.
It does not identify a Bayes law or promise a Bayes-optimal action for every
compatible law. Directly bounding `c_a-c_b` can be much tighter than subtracting
independent bounds on the two absolute costs: the common unknown `p_3` in
the example of section 5 cancels exactly.

### Randomization changes positive regret, not the exact common-optimum test

Let a private action draw use probabilities `lambda_a` after seeing the
retained observation. Nature's compatible law is chosen without observing
that draw, and the target is expected regret over the draw. Then

```math
\sup_{p\in F}\sum_a\lambda_a
\left(c_ap-\min_b c_bp\right)=0
\quad\Longleftrightarrow\quad
\mathrm{supp}\lambda\subseteq\bigcap_{p\in F}\mathrm{Opt}(p).
\tag{10a}
```

Every summand is nonnegative, so a positive-weight action must itself have
zero regret at every compatible law. Thus randomization cannot rescue the
absence of a common optimum for this exact service. It can reduce positive
minimax regret: with no information on `Delta_2` and losses `(0,1)` and
`(1,0)`, a mixture choosing the first action with probability `lambda` has
worst expected regret `max(lambda,1-lambda)`. The half-half mixture has
regret `1/2`, while every deterministic choice has regret one. Allowing nature
to choose after seeing the actual draw changes the contract and removes this
particular improvement. The
[separate audit](../work_logs/P3_02_2026-10-07_S1/reviews/noise_principal_audit.md#5-randomized-decisions-exact-and-approximate-service)
proves the finite statement; no randomized acquisition policy is supplied.

### Estimated values need an error contract

If the retained values are estimates, a declared deterministic error set gives

```math
F(\widehat y,\varepsilon)
 =\{p\in P:-\varepsilon\leq Lp-\widehat y\leq\varepsilon\}.
\tag{11}
```

The resulting interval and decision guarantees are conditional on the source
and error premises. If a statistical method establishes their joint coverage
at a stated level, the resulting guarantees inherit that coverage; interval
arithmetic alone supplies none. Separately trained value estimates can be
incompatible with any normalized law. Projecting an incoherent estimate into
the attainable expectation set produces a coherent estimate but does not, by
itself, establish its accuracy or coverage. Retained sample histories, joint
error information, acquisition costs and update rules can matter even when the
reported numbers are the same.

## 7. Dependence and missing information

### Marginals can lose the task's dependence

On the ordered joint states `00,01,10,11`, compare

```math
p_{\rm same}=(1/2,0,0,1/2),\qquad
p_{\rm opposite}=(0,1/2,1/2,0).
```

Both have `E[X]=E[Y]=1/2` and `E[X+Y]=1`. But
`E[max(X,Y)]` is respectively `1/2` and `1`. A constant fallback `3/4`
therefore requires opposite choices. Given only the two marginals, the fiber is

```math
p=(t,1/2-t,1/2-t,t),\quad 0\leq t\leq1/2,
\qquad E[\max(X,Y)]=1-t\in[1/2,1].
\tag{12}
```

The maximum is nonlinear in the state variables `X,Y`, but it is a **known
linear expectation** of the joint-state loss row `(0,1,1,1)`. Retaining that
one target expectation answers this decision; retaining `E[XY]` also suffices
because `max(X,Y)=X+Y-XY` on these states. Full joint-law recovery is sufficient
but unnecessary. This reconstructs the inherited P3-01 EX03 obstruction and
adds its explicit compatible interval; the old example is not counted as new
experimental evidence. [P3-01 separating examples](../foundations/01_separating_examples.md)

### Known random stakes differ from unknown stake parameters

Suppose `K` is a state-observed stake taking values `1` and `3` with probability
`1/2` each. The payoff is the known joint-state quantity `K 1_A`, and its
expectation is `1`. Write `x=P(K=1,A)` and `z=P(K=3,A)`. Then

```math
x+3z=1,\quad 0\leq x,z\leq1/2
\quad\Longrightarrow\quad
1/6\leq z\leq1/3,
\quad P(A)=x+z=1-2z\in[1/3,2/3].
\tag{13}
```

Both endpoints extend to feasible joint laws with the declared stake marginal.
Although `E[K]=2`, dividing the retained expected loss by `2` gives `1/2`,
which need not be `P(A)`. The missing term is explicit:

```math
E[K1_A]=E[K]P(A)+\mathrm{Cov}(K,1_A).
```

Independence is sufficient to remove it but has not been assumed. On an
enumerated joint state space the payoff coefficients `1` and `3` are known,
so all these constraints are affine in the joint law. If instead the stakes
and probabilities are separate jointly uncertain numerical parameters, their
product is not a native affine expression. A joint-state model, a proved
enclosure or an explicit language extension is needed; notation alone cannot
remove the distinction.

### Credal and counterfactual boundaries

The inherited [EX12](../foundations/01_separating_examples.md) compares two credal sets with identical lower/upper
probabilities for every event, yet upper expectations `4/3` and `5/3` for
the loss `(0,1,2)`. Against the fallback `3/2`, robust decisions differ.
Thus even **all event intervals** need not identify the upper expectation
functional or its robust decisions. A full coherent lower/upper expectation
functional on all gambles identifies the associated closed convex credal set;
it does not identify an original nonconvex family inside that hull.
[P02-S1](../literature/02_probability_sources.md)

Finally, a recovered observational joint law does not generally identify
counterfactual dependencies. That inherited P3-01 EX06 boundary remains intact.
No counterfactual semantics or P3-04 result is established here.

## 8. Coherent expectations and proper scoring rules

### A whole expectation functional versus a finite record

On a finite state space, a functional `E` on **all** real loss vectors that is
linear, positive on nonnegative losses and normalized by `E(1)=1` has the form
`E(c)=cp` for a unique normalized law. Indeed set `p_i=E(1_{i})`; positivity
gives `p_i>=0`, normalization gives `sum_i p_i=1`, and expanding
`c=sum_i c_i 1_i` gives the representation. A functional on only a coarser
observable partition identifies the law on that partition. This is ordinary
finite coherent expectation, not a new interpretation theorem.
[P02-S1](../literature/02_probability_sources.md)

A finite record `y`, with the full simplex as its source and no additional
law restrictions, is compatible with some law exactly when
`y in conv{L[:,1],...,L[:,n]}`. This also has the familiar unrestricted,
frictionless finite-gamble reading. A signed position vector `w` has net
state payoffs `w^T(L[:,i]-y)`. If `Lp=y`, their expected payoff is zero, so
they cannot be strictly positive in every state. Conversely, if `y` lies
outside the compact convex hull, strict separation gives a choice of sign
for `w` making every such net payoff positive. This statement uses sure gain
**strictly in every admitted state**. A nonnegative payoff positive only on
some states needs a support qualification to rule it out; fees, position
restrictions and computational access define other exploitation criteria.
Coherence is compatibility, not evidence that the compatible law is accurate.

### What strict propriety identifies

Let `ell(q,i)` be a known loss for reporting `q` when outcome `i` occurs,
and let `R_p(q)=sum_i p_i ell(q,i)` be its risk under a fixed outcome law.
Strict propriety says that the unique optimal report is `q=p` on the stated
domain. It does not say that one achieved scalar risk identifies `p`, that
an observed realized score equals its expectation, or that a learner has
found the optimum. If the report changes the outcome law, this fixed-law
incentive argument needs a different causal/game contract.
[P02-S2](../literature/02_probability_sources.md)

For the multiclass Brier loss,

```math
\ell(q,i)=\|q-e_i\|_2^2,\qquad
R_p(q)=1+\|q\|_2^2-2q^Tp
      =1-\|p\|_2^2+\|q-p\|_2^2.
\tag{14}
```

This directly proves strict propriety. A **certified excess risk** at most
`delta` gives `||q-p||_2<=sqrt(delta)`; a small realized score alone supplies
no such certificate. At the uniform report `u`, the risk is always `1-1/n`,
regardless of `p`. The optimum risk `1-||p||_2^2` also fails to identify the
law, for example across permutations or distinct pure laws. In contrast,
the known vertex probes have risks `R_p(e_i)=2(1-p_i)`; `n-1` such expected
risks plus normalization recover the full law.

One scalar score is not universally uninformative. Under the *binary scalar*
convention `ell(q,X)=(q-X)^2`,
`R_p(q)=q^2+(1-2q)p` recovers `p` whenever the known `q` is not `1/2`.
The usual failure is lack of the necessary measurement rank or score/payoff
semantics, not the word “score.”

For logarithmic loss use positive report coordinates. A uniform report has
constant risk `log n`. Let `q^0` be uniform and let `q^j` assign `2/(n+1)`
to state `j` and `1/(n+1)` to every other state. Then

```math
R_p(q^j)-R_p(q^0)
=\log((n+1)/n)-p_j\log2.
\tag{15}
```

These exact risk differences recover the respective probabilities. Boundary
log reports with infinite losses cannot be treated as finite matrix rows.
Natural-log coefficients are not automatically native rational constants;
some other exact choices are rational, such as the base-2 losses `(1,2,2)`
for report `(1/2,1/4,1/4)`. Fixed rational Brier reports give rational rows.
Optimizing a variable report introduces its own nonlinear operations and
computational costs; the finite-row result is not that optimization procedure.

### Information span of finite strictly proper scores (PI-7)

Assume `n>=2`, a report domain containing every strictly positive probability
vector, finite known score vectors `ell(q)` for its reports, and unique global
minimum `q=p` for every strictly positive law `p`. For any fixed report `q^0`,

```math
\mathrm{span}\{\ell(q)-\ell(q^0):q\text{ admissible}\}
=\mathbb R^n.
\tag{16}
```

**Proof.** Suppose a nonzero vector `z` annihilates all the differences.
If `1^T z=0`, take an interior law `p` and sufficiently small nonzero `t`
so that `p+t z` is also interior. Its risk function differs from `R_p` by
the report-independent constant `t z^T ell(q^0)`. Their unique optimizers
must agree, contradicting strict propriety at distinct laws. If `1^T z!=0`,
put `r=z/(1^T z)` and choose an interior law `p!=r`. For sufficiently small
`0<t<1`, the vector `p_t=(1-t)p+t r` is interior even if `r` itself has
negative coordinates. Now
`R_{p_t}(q)=(1-t)R_p(q)+t r^T ell(q^0)`. The positive scaling and constant
again preserve the optimizer, contradicting `p_t!=p`. Both cases are
impossible. No differentiability is needed. For `n=1` the law is already
known and this stronger span claim need not hold.

In particular `span{1,ell(q)}=R^n`: with known absolute risks, `n-1`
suitably selected raw score rows, together with normalization, suffice.
Likewise `n-1` suitable **difference** rows modulo constants suffice when
those differences are directly available. Computing a preselected difference
basis from a baseline and its associated raw reports can use `n` reports;
that is not a lower bound on the best raw-query selection. A restricted
report menu must be checked for its actual rank. Merely proper constant
scores fail this argument, and an approximate optimizer is not an exact
expectation oracle. Selecting accessible probes, evaluating expectations,
precision and search costs remain part of the service contract. This is an
elementary finite reconstruction of strict propriety and linear algebra.

### Shared unknown score units can be calibrated (PI-8)

Now suppose the observed numbers obey the stronger declared relationship

```math
v(q)=b+s R_p(q),\qquad s>0,
\tag{17}
```

with the **same** unknown `b,s` for every report. Select `n` independent
difference rows in (16), stack them as an invertible `D`, and set
`d_j=v(q^j)-v(q^0)`. Then

```math
x=D^{-1}d=s p,\quad s=\mathbf1^T x,
\quad p=x/s,\quad b=v(q^0)-\ell(q^0)x.
\tag{18}
```

Thus `n+1` raw expected-score values can recover the law and both nuisance
parameters. This is a constructive exception to arbitrary unknown-stakes
confounding. These formulas require known base rows and a shared nonzero affine
transformation; other payoff uncertainty or estimated-input models need their
own identification and error contracts. The algebra recovers `p` even
for a stipulated common nonzero negative scale, but positive scale is needed
to preserve the original minimization incentives.

The raw-query count is sharp for this global finite linear-probe model with
arbitrary interior laws, `s>0` and `b in R`. With `k` probes, differencing
leaves at most `k-1` equations in `x=s p`. If `k-1<n`, choose a nonzero hidden
direction `h`. Select `x>0` not proportional to `h` and perturb to
`x+t h>0`; adjust `b` to keep the baseline value fixed. Every probe agrees,
but normalization gives different laws. This rules out every decoder for
the fixed probe menu. It is not a claim about optimized reports, arbitrary
nonlinear encodings or adaptive query policies.

**Rational Brier construction.** Use the uniform report and all `n` vertices.
Write `v_0=v(u)`, `v_i=v(e_i)` and `d_i=v_i-v_0`. Then

```math
s=\frac{\sum_i d_i}{n-1},\qquad
p_i=\frac{1+1/n-d_i/s}{2},\qquad
b=v_0-s(1-1/n).
\tag{19}
```

For `n=3`, the values `(v_0,v_1,v_2,v_3)=(7,10,9,8)` give
`s=3`, `b=5`, and `p=(1/6,1/3,1/2)`. All payoff rows and observations
are rational. Variable normalization still needs the implementation contract
discussed in section 3. Without a positive lower bound on `s`, small numerical
errors can swamp probability information as the scale approaches zero.

Successful algebra does not verify the input's semantic type. If all selected
reports are scored on the **same realized outcome** `Y`, the same full-rank
calibration procedure receives `b+s ell(q,Y)` and returns the point mass
`e_Y`. Averaging a shared finite outcome sample similarly produces its
empirical law. Neither output is thereby the earlier subjective law or the
population law. This hostile case is included in the exact development check.

### Ordinary methods can score only the task property

For a chosen target matrix `C` with `k` rows, report `r in R^k` and use outcome loss
`||r-C[:,i]||_2^2`. Its expectation is

```math
\|r-Cp\|_2^2
 +\sum_i p_i\|C[:,i]\|_2^2-\|Cp\|_2^2.
\tag{20}
```

The unique optimum report is `r=Cp`. This directly elicits the specified
expected-loss vector even if it identifies no full law. Known scoring weights
or units specify the norm; the square is part of an external scoring/learning
method, not an implicit extension of phase two's native language. Ordinary
property elicitation and low-rank surrogate methods already supply this
comparator. These identities establish neither online convergence nor any
Logical-Induction-like refinement duty.
[P02-S3/S4/S7](../literature/02_probability_sources.md)

## 9. A sharper characterization for one optimal action

The fiber condition in section 5 is general. The following sharper result
uses a **finite action menu, the full real simplex, fixed exact linear
observations, and permission to return any minimizing action**. It does not
assume recovery of every action's cost or every pairwise preference.

First merge identical loss rows. Call an action *essential* if it is uniquely
optimal at some strictly positive law, and let `E` be this set. The essential
rows preserve the entire lower envelope
`f(p)=min_a c_a p=min_(a in E) c_a p`. To see this, avoid the finite proper
tie hyperplanes at an interior law; its minimizer is unique and essential.
Approach any boundary or tied law by such laws and take a subsequence with
one fixed minimizing action. Continuity proves the asserted equality.
Discarded rows can add ties but cannot be the only optimum anywhere.

### Essential-difference criterion (PI-9)

Let `A=[1^T;L]` as before. A selector returning some optimal action from `Lp`
exists for **every** law in the full simplex if and only if

```math
c_a-c_b\in\mathrm{row}A\qquad(a,b\in E).
\tag{21}
```

Equivalently, choose one essential reference action `a_0` and factor

```math
c_a=c_{a_0}+\alpha_a\mathbf1^T+\beta_a L\quad(a\in E).
\tag{22}
```

The constructive selector minimizes `alpha_a+beta_a y`; the common expected
baseline `c_{a_0}p` may remain unknown. If `D_E` contains the differences
from the reference, the minimum number of freely chosen **fixed linear
expectation coordinates** for this service is
`rank([1^T;D_E])-1`. Computational cost, accessible measurement menus and
precision are separate constraints.

**Necessity, including hidden tie actions.** The essential optimal cells are
the full-dimensional cells of a finite affine lower envelope. Their adjacency
graph through facets meeting the simplex interior is connected: a generic
polygonal path between two strict-cell points stays in the interior and
avoids boundary intersections of codimension at least two. A generic point
on a shared facet has exactly two essential pieces locally. If three distinct
affine pieces coincided along the whole facet, their nonzero differences
would have the same zero hyperplane and hence be proportional as affine
functions on the simplex affine hull. A middle piece would be a strict convex combination of
the extreme two and could never be uniquely minimal.

Suppose adjacent actions `a,b` have a hidden direction `h in ker A` with
`(c_a-c_b)h>0`. At a generic interior facet law `p^0`, choose small `t>0`
with `p^+=p^0+t h` and `p^-=p^0-t h` both feasible and in the two local
cells. They have the same observation, while

```math
\frac{f(p^+)+f(p^-)}2
 =f(p^0)-\frac t2(c_a-c_b)h<f(p^0).
\tag{23}
```

If **any** original action were optimal at both endpoints, its affine cost
at their midpoint would equal the left side, below the minimum at `p^0`.
That is impossible, including for an otherwise discarded tie action. Thus
every adjacent difference annihilates the hidden directions. Connectivity
and the rowspace/nullspace identity give (21). Sufficiency follows at once
from (22) and the essential-envelope reduction. With one essential action
the criterion is vacuous; with one state the decision is constant.
The [separate finite reconstruction](../work_logs/P3_02_2026-10-07_S1/reviews/decision_geometry.md)
contains the cell and boundary arguments in full.

### Convex restricted sources and unobserved case identity

The same criterion extends to any nonempty **convex** admitted source `P`.
Merge loss rows that are identical as affine functions on `aff(P)`, define
`E_P` by unique optimality somewhere in `ri(P)`, and put
`V=span(P-P)`. Then some optimal action is recoverable everywhere on `P` iff

```math
(c_a-c_b)h=0\qquad
(a,b\in E_P,\ h\in V\cap\ker L).
\tag{21a}
```

The essential-envelope argument holds by approaching any source point from
its relative interior. A generic polygonal path stays in that open convex
relative interior; the finite affine tie hyperplanes provide the same local
facet and midpoint obstruction used above. Conversely, each essential
difference factors on `aff(P)` through a constant and `Lp`. Neither
compactness nor a polyhedral outer boundary is needed for this exact
finite-menu claim. In a zero-dimensional source the decision is constant.
Identifying the actual affine hull and essential actions remains an access
or computation requirement, not a free consequence of the theorem.
The [separate audit](../work_logs/P3_02_2026-10-07_S1/reviews/principal_mathematics_audit.md#4-optional-convex-source-extension-of-pi-9)
gives the reconstruction.

For a **union** of convex cases, checking each case separately is insufficient
unless case identity is retained or their overlapping observations are also
checked. Let

```math
P_1=\mathrm{conv}\{e_1,e_2\},\quad
P_2=\mathrm{conv}\{e_3,e_4\},\quad P=P_1\cup P_2,
```

and take `L=(0,1,0,1)`, `c_A=(0,0,1,1)`, `c_B=(1,1,0,0)`.
Action `A` is uniquely optimal throughout `P_1`; `B` is uniquely optimal
throughout `P_2`. Nevertheless, for every `y in [0,1]`, the laws
`(1-y,y,0,0)` and `(0,0,1-y,y)` have the same observation and opposite
optima. The union has no summary-only optimal selector. Retaining the pair
`(case,y)` resolves this obstruction; without it, PI-1's actual fibers must
compare laws across cases. Fallible-model catalogues therefore need an
explicit account of which model identity is observed and which is uncertain.

### Two actions, dominance and ties

For two actions let `r=c_1-c_2`. If `min_i r_i<0<max_i r_i`, there is an
interior law with `rp=0`: slightly mix each of a positive/negative pure
witness with the uniform law and then mix the two resulting interior laws.
A hidden direction with `rh!=0` gives opposite unique optima on that same
fiber. Consequently, in this strict-crossing case, preserving some optimal
action already requires the exact numerical difference `rp` to be recoverable.

This is not true without crossing. For `r=(0,1,2)` and retained `y=p_1`,
the sign is zero exactly at `y=1` and positive otherwise, although the value
`p_2+2p_3` is unknown. With no observation the second action still always
works, but its complete tie information does not. The boundary premise is
doing substantive work in the characterization.

**Nonconstant decision without all preferences.** Take
`c_A=(0,1,1)`, `c_B=(1,0,0)`, `c_D=(1/4,5/4,9/4)` and retain `p_1`.
Action `D` is strictly dominated by `A`; the essential difference is `1-2p_1`.
At the two laws `(2/3,1/3,0)` and `(2/3,0,1/3)`, the costs `(A,B,D)` are
respectively `(1/3,2/3,7/12)` and `(1/3,2/3,11/12)`.
The optimal action is `A` at both, but the ranking of `B,D` reverses.
This rejects an unnecessarily strong requirement to recover differences
between every pair of original actions.

### Strong ordinary comparison and quantitative interpretation

Ordinary calibrated-surrogate theory already organizes losses by the sets of
laws at which each action is optimal. For the squared feature surrogate
`psi_i(u)=||u-L[:,i]||_2^2`, the laws having optimal report `u` are exactly
the fibers `Lp=u`. The common-optimum requirement is therefore directly
anticipated by that framework. Low-rank squared-loss methods also learn
expectation codes and decode actions without full-law recovery.
[P02-S6/S7](../literature/02_probability_sources.md)

The finite factorization supplies an elementary error bridge. If the decoder
minimizes `alpha_a+beta_a u` over essential actions, then under any fixed law

```math
\mathrm{regret}_p(\mathrm{decode}(u))
\leq
\max_{a,b\in E}\|\beta_a-\beta_b\|_*\,\|u-Lp\|.
\tag{24}
```

Indeed compare the chosen action with an essential true optimum; their
predicted difference is nonpositive and their error difference is bounded
by the dual-norm inequality. For a squared feature surrogate its excess risk
is exactly `||u-Lp||_2^2`, giving the usual square-root regret bound.
The factorization does not provide the data, optimizer or bounded reasoning
procedure that would establish such an excess-risk guarantee.

The dimension restriction must not be generalized to every report. For
ordinal absolute loss on labels `1,...,n`, adjacent action differences are
signed prefix indicators, all actions are essential, and the fixed-linear
criterion requires `n-1` coordinates. A scalar optimized median report is
nonlinear in `p` and can serve the ordinal decision. With an exact oracle for
prefix probabilities, an adaptive binary search for the first prefix at least
`1/2` takes at most `ceil(log2 n)` queries. Those are different information
services, with their own access and cost contracts. No lower bound on all
nonlinear encodings or paid acquisition policies follows from (21).

## 10. Changes of units, normalization, prices and retained information

### Known recoding and changed objectives

A known invertible affine recoding `y'=Ty+d` preserves all fibers: decode
`y=T^{-1}(y'-d)` first. Known nonzero changes of each measurement unit are
included. If some coordinates are deliberately discarded, apply the target
criterion to the resulting observation; invertibility of the whole record is
not necessary for a smaller service. A common positive scale and a common
action-independent constant preserve ordinary expected-cost preferences.
Independently rescaling action scores and then comparing their raw numbers
generally changes the decision unless the original units are restored.

A common **state-dependent** added cost `h` cancels action differences at a
fixed law, but not generally absolute minimax costs over a law family.
For two states let `c_A=(0,4)`, `c_B=(3,3)` and allow every law. Their
worst costs are `4,3`, so absolute minimax chooses `B`. Adding `h=(4,0)`
to both rows gives worst costs `4,7`, so it chooses `A`. Every pointwise
action difference is unchanged. Minimax regret is unchanged too, because its
definition uses these differences. One must retain the service distinction
when interpreting an “irrelevant baseline.”

A price change is a new known target matrix `C` only if it refers to the
same declared state law and statewise use/payoff semantics. Price-dependent
behavior or an unprovided counterfactual dependency is an additional modeling
problem. Under the fixed-source contract, section 4 directly answers whether
the old `Lp` determines the newly priced losses `Cp`.

### Unknown common units: a precise obstruction (PI-10)

Let `n>=2`, let `L` be known, and observe `v=sLp`, with the same unknown
`s>0` for every coordinate. For a **nonconstant** scalar target `cp`, global
recovery over the full simplex and every positive scale holds exactly when

```math
\mathbf1^T\in\mathrm{row}L
\quad\hbox{and}\quad c\in\mathrm{row}L.
\tag{25}
```

If `alpha L=1^T` and `beta L=c`, then `s=alpha v` and
`cp=(beta v)/(alpha v)`. To prove necessity of the constant row, choose
`h in ker L` with `H=1^T h!=0` if that row is missing. Because `c` is
nonconstant, some interior `p` satisfies `ch-Hcp!=0`. For sufficiently small
nonzero `t`,

```math
p_t=\frac{p+th}{1+tH},\qquad s_t=s(1+tH)>0
\tag{26}
```

are admissible and have `s_t Lp_t=sLp`, but
`cp_t-cp=t(ch-Hcp)/(1+tH)!=0`. If the constant row is present and the
target row is absent, the ordinary zero-sum kernel perturbation proves
non-recovery. Constant targets need no observation and are expressly excluded
from the nonconstant-target necessity statement. Full-law recovery is
equivalent to `rank L=n`, not merely `rank([1^T;L])=n`.

If an unrestricted common offset is also unknown,
`v=sLp+b1`, form the matrix `D` of differences from one reference loss row.
The observed differences are `sDp`, and no omitted reference value supplies
extra law information when `b` is unrestricted. Thus the criterion becomes
`1^T,c in row D`. If scale is known, only
`c in row([1^T;D])` is required. Applied to strictly proper finite scores,
this gives the sharp fixed raw-probe counts below for `n>=2`, exact fixed
raw probes from a sufficiently rich accessible finite-score family, and a
known scale assumed nonzero when applicable:

| Calibration information | Full-law query count, with suitable accessible probes |
|---|---:|
| Scale and offset known | `n-1` |
| Scale known, common offset unknown | `n` |
| Positive common scale unknown, offset known | `n` |
| Both common scale and offset unknown | `n+1` |

These are exact-information counts over all interior laws and unrestricted
stated nuisance parameters. Restricted calibration ranges or a single boundary
observation can identify more locally. With an additive nuisance `B theta`,
an information-preserving reduction uses a **complete** left annihilator `N`
with `ker N=im B`; merely finding some `NB=0` can discard useful information.
The [independent nuisance reconstruction](../work_logs/P3_02_2026-10-07_S1/reviews/nuisance_information.md)
states this extension and the required unconstrained-nuisance hypotheses.

### Normalizing arbitrary values can erase information

Suppose `L>=0` and every column sum `a_i=sum_j L_{ji}` is strictly positive.
Then the normalized report

```math
w(p)=\frac{Lp}{a^Tp}
\tag{27}
```

has exactly the law-collision relation of the unknown-positive-scale model.
Equal normalized reports mean positively proportional original reports, and
the converse is immediate. Thus full recovery from `w` needs `rank L=n`.
Normalizing a single positive row, for example `L=(1,2)`, produces the constant
one and destroys the binary-law information present in its unnormalized mean.
If a column sum vanishes, the positivity and denominator premises must be
reexamined; silently dropping that state can change the source.

Unknown common scale can nevertheless preserve useful decisions when it
preserves no nonconstant linear probability target globally. For

```math
L=\begin{bmatrix}0&1&2\\1&0&1\end{bmatrix},
\tag{28}
```

the constant row is absent from `row L`. Still `argmin(v_1,v_2)` is the
correct action under every positive common scale, and the choice changes with
`p_1` at `1/2`. The laws `p=(3/5,1/5,1/5)` with `s=1` and
`q=(11/18,1/9,5/18)` with `s=9/10` give the same `v=(3/5,4/5)` and the
same normalized `w=(3/7,4/7)`. This establishes decision sufficiency under
nuisance while probability recovery fails. Normalizing values of overlapping events also does
not turn them into their event probabilities: the calibration in section 3
requires a declared exhaustive **disjoint** partition.

### Minimal additional task information (PI-11)

For a nonempty convex source `P`, use its actual affine direction space `V`
and old hidden space `U=V intersect ker L`. To recover a new expected-loss
family `Cp`, the minimum number of freely chosen additional exact linear
measurements is

```math
r=\dim C(U)
 =\mathrm{rank}([L;C]|_V)-\mathrm{rank}(L|_V).
\tag{29}
```

**Proof.** An additional matrix `M` succeeds exactly when
`ker(M|_U) subset ker(C|_U)`. The rank of `M|_U` must therefore be at least
`rank(C|_U)=r`. Conversely choose `r` target rows whose restrictions form a
basis of the row space of `C|_U`. Their common kernel on `U` is the required
one, so those measurements attain the bound. Rank-nullity gives the second
expression in (29). This is the inherited retention/repair argument applied
to the specified probability consumer.

An available measurement menu can require more than `r`. With no old data on
three states, target `p_1` needs one freely chosen coordinate. If the only
available queries are `p_1+p_2` and `p_2`, neither alone suffices; both together
do. The rank count does not price those measurements or guarantee their
availability. A smaller decision-only repair can instead target the essential
differences in section 9. Restoring a whole law is warranted only when the
chosen future service actually needs it.

Small price changes also separate exactness from significance. If
`C(delta)=C_0+delta R` and the old summary already determines `C_0 p`, then
on each old fiber the new target width is `|delta|` times the width of `Rp`.
Any nonzero `delta` can expose a previously hidden direction while its absolute
cost effect tends continuously to zero. Conversely, inferring `Rp` from a
noisy small difference may divide error by `|delta|`. Phase two already makes
this distinction for its reset/price family; P3-02 does not claim it as a new
induction or recovery theory.
[Inherited retention record](../literature/02_probability_sources.md)

## 11. Bounded uncertainty about the payoff table

Known exact payoffs are a strong premise. Some uncertainty can still be
handled exactly without introducing a general multiplication rule.

### Independent payoff boxes project to affine law constraints (PI-12)

Suppose the admissible payoff matrices are the complete componentwise box
`lower_L <= L <= upper_L`, with finite known bounds satisfying
`lower_L <= upper_L` entrywise. Then

```math
\{p\in\Delta_n:\exists L\in[\underline L,\overline L],\ Lp=y\}
=\{p\in\Delta_n:\underline Lp\leq y\leq\overline Lp\}.
\tag{30}
```

**Proof.** Nonnegative probabilities give the displayed inequalities for
every admissible `L`. Conversely, for each row let
`a_j=lower_L[j,:]p` and `b_j=upper_L[j,:]p`. If `a_j<b_j`, select
`theta_j=(y_j-a_j)/(b_j-a_j)` and use row
`lower_L[j,:]+theta_j(upper_L[j,:]-lower_L[j,:])`. It is admissible and
has expectation `y_j`. If `a_j=b_j`, feasibility requires `y_j=a_j` and
any row on that segment works. Row choices may be combined because the
matrix source permits them independently. Zero-probability coordinates cause
no division by `p_i` in this construction.

The original joint expression is bilinear, but this **existential projection**
has a finite affine description. An equivalent lift uses variables
`x_ji=L_ji p_i` subject to
`lower_L_ji p_i <= x_ji <= upper_L_ji p_i` and `sum_i x_ji=y_j`;
at `p_i=0` the bounds force `x_ji=0`. The projection theorem justifies this
restricted interface; it does not make arbitrary products native.
If an independent box error `epsilon` is also admitted, replace the bands by
`lower_L p-epsilon <= y <= upper_L p+epsilon`.

These are **compatibility** statements: for each candidate law there exists
an admitted payoff table and error. They do not assert that every table in
the box gives the observation. If several populations or records share one
actual table, each candidate tuple `(p^(1),...,p^(r))` must admit one common
`L` satisfying all its observation equations simultaneously. Different
alternative tuples may still use different witness tables. Allowing a separate
table for each population within one tuple drops a substantive shared-source
constraint. Structured row/entry correlations must likewise be retained.

### Why payoff dependence cannot be replaced by separate bounds

Let `L(s)=s I_2`, where one common stake satisfies `1<=s<=2`, and observe
`y=(2/3,2/3)`. Normalization forces `s=4/3` and `p=(1/2,1/2)`.
If the two stakes are instead independently bounded in `[1,2]`, equation (30)
admits all `p=(u,1-u)` with `1/3<=u<=2/3`. The endpoint `p=(1/3,2/3)`
uses stakes `(2,1)` and is impossible under the shared-stake contract.
Replacing the shared parameter by coordinate bounds loses identification.

The same issue can occur within a row. With the constrained row
`L(s)=(s,1-s)`, `0<=s<=1`, and `p=(1/2,1/2)`, the expectation is always
`1/2`. Independent entry bounds `[0,1]` falsely admit every expectation in
`[0,1]` at that law. This is an obstruction to the independent-box premise,
not to the exact projection theorem under its actual hypotheses.

For a binary loss with zero payoff off an event, stake `K in [a,b]`,
`0<a<=b`, and observed expectation `v>=0`, the event probability lies in
`[v/b,v/a] intersect [0,1]`, whenever that set is nonempty. Those bounds
follow from `a p<=v<=b p` and are sharp. This retains partial probability
information while acknowledging stake uncertainty. A known *random* stake
on a joint state space, as in section 7, is a different semantic contract.

The [payoff-uncertainty reconstruction](../work_logs/P3_02_2026-10-07_S1/reviews/payoff_uncertainty_projection.md)
records the quantifiers, boundary cases and independent proof. The result is
an elementary projected-compatibility adaptation, with no general robust
bilinear-programming or probability-estimation claim.

## 12. Noisy information and coherent recovery

### Exact rank need not give stable inversion

On three states consider

```math
L_\delta=\begin{bmatrix}0&1&1\\0&1&1+\delta\end{bmatrix}.
\tag{31}
```

For known `delta!=0`, normalization and these two rows recover the full law;
in particular `p_3=(y_2-y_1)/delta`. If the two measured means each have
absolute error at most `epsilon`, this algebraic estimate can have error
`2 epsilon/|delta|`, before source constraints are used. At `delta=0`, the
third-state probability is not identified. Nevertheless the task expectation
`p_2+p_3=y_1` remains directly estimated with error at most `epsilon`.
Ill-conditioned full-law recovery need not make that smaller task difficult.

The error relation matters as much as its coordinate bounds. Paired samples,
shared calibration errors or other retained joint information may make the
difference much more accurate than two separately bounded estimates suggest.
No intrinsic statistical `1/|delta|` penalty is claimed for every observation
protocol. Phase two already distinguished exact small-edit information from
its practical error and acquisition costs.

### Sharp scalar information radius (PI-13)

Let `P` be nonempty compact, `L,c` known, and assume adversarial observation
error `e` lies in one known nonempty compact set `E`, with the same set admissible for
every law: the joint source is `P x E`. This is a deterministic Cartesian
source premise, not an assertion of statistical independence. Write
`F_z={p in P:z-Lp in E}` for each feasible observation `z`.
For a scalar target the best unrestricted worst-case estimate on that fiber
is the midpoint of its attainable extrema, with radius
`(max_(p in F_z) cp-min_(p in F_z) cp)/2`. Globally,

```math
R_{\rm free}
=\frac12\max\{|c(p-q)|:p,q\in P,\ L(p-q)\in E-E\}.
\tag{32}
```

**Proof.** Two laws can produce the same observation exactly when
`Lp+e_p=Lq+e_q` for some `e_p,e_q in E`, equivalently
`L(p-q) in E-E`. Every shared-observation pair forces error at least half
its target separation for any decoder. The midpoint estimate on each fiber
attains half its diameter, giving the matching upper bound. Compactness
supplies attained extrema. Convexity is unnecessary for this unrestricted
scalar statement; if the fibers are convex, averaging endpoint laws also
makes the scalar midpoint attainable by a compatible law.

For coordinate box errors `|e|<=epsilon`, condition (32) is
`|L(p-q)|<=2epsilon`. For a law-dependent joint error mechanism, use its
actual observation relation instead of inserting an unrelated fixed `E`.
This is a direct reconstruction of the inherited optimal-recovery method,
not a new estimation theory. Mathematical decoder existence does not by
itself supply a finite computational budget.

### A sharp conditioning case, including source constraints

For (31), `delta>0`, and equal coordinate errors `epsilon>=0`, the exact
global scalar radius for `p_3` is

```math
R_\delta(\epsilon)
=\frac12\min\left\{1,\frac{4\epsilon}{\delta},
                         \frac{1+2\epsilon}{1+\delta}\right\}.
\tag{33}
```

To verify it, write a nonnegative target difference as
`h=p-q=(-t,t-r,r)`, `r>=0`. A zero-sum vector is a difference of normalized
laws exactly when its positive mass is at most one. Here that condition is
`r<=1` and `r-1<=t<=1`. Overlap of the observation boxes gives
`-2epsilon<=t<=2epsilon-delta r`. The two intervals intersect exactly when
the three bounds on `r` in (33) hold. For the maximal such `r`, set
`t=min(0,2epsilon-delta r)`, choose
`q=e_2`, `p=(-t,1-r+t,r)`, and use the midpoint of their two expectation
vectors as the common observation. This attains the bound.

The simple bound `min(1/2,2epsilon/delta)` can therefore be strictly loose.
For `delta=2`, `epsilon=2/5`, it gives `2/5`, while the exact radius is
`3/10`. The pointwise intervals have an equally explicit form: for a feasible
`z` and `delta>0`,

```math
\begin{aligned}
\ell_z(p_3)&=\max\left\{0,\frac{z_2-1-\epsilon}{\delta},
                            \frac{z_2-z_1-2\epsilon}{\delta}\right\},\\
u_z(p_3)&=\min\left\{1,z_1+\epsilon,
                       \frac{z_2+\epsilon}{1+\delta},
                       \frac{z_2-z_1+2\epsilon}{\delta}\right\}.
\end{aligned}
\tag{34}
```

These follow by intersecting the possible intervals for `p_2+p_3` after
fixing `p_3`. They use only min/max and rational affine operations when
the parameters are fixed rational constants. The
[independent conditioning proof](../work_logs/P3_02_2026-10-07_S1/reviews/noise_conditioning_case.md)
and fourteen exact, certificate-backed development regimes check this
specific construction. At `delta=0` the radius is `1/2`, including zero
noise; at positive `delta` and zero noise it is zero.

### Joint error information can restore exact recovery

Let `P=Delta_2`, `L=I`, and the error be one shared additive bias
`e=b(1,1)`, `|b|<=1/4`. Normalization gives
`b=(z_1+z_2-1)/2` and `p_1=(1+z_1-z_2)/2`, so recovery is exact.
Replacing that joint error set by the coordinate box `|e_i|<=1/4` changes
the source. At `z=(1/2,1/2)` it admits `p_1 in [1/4,3/4]` and radius
`1/4`. The less informative error representation discarded the shared-bias
calibration. The same issue can arise after subtracting one common noisy
anchor from several measurements.

### A coherent vector answer can cost more

For a finite vector target `Cp` on one compact fiber, let its coordinate
extrema be `[a_j,b_j]`. In the ordinary unweighted maximum-coordinate norm,
an unrestricted vector has sharp radius
`r_free=max_j(b_j-a_j)/2`. If the answer must instead come from one law
`q in F_z`, the sharp compatible radius is

```math
r_{\rm coh}=\min_{q\in F_z}\max_j\{C_jq-a_j,\ b_j-C_jq\}.
\tag{35}
```

When the fiber `F_z` is a nonempty compact polytope, this is an LP after
introducing the radius variable and computing the extrema. When `F_z` is
compact convex, it is a convex optimization problem, not necessarily a finite
LP. Convexity of `P` alone is insufficient if the error set is nonconvex.
For a finite union of compact polyhedral cases, first compute extrema over
the whole union, then minimize the center objective on each case and take
the best attained value; the union itself need not be one LP. Equality with
the free radius holds exactly when

```math
C(F_z)\ \cap\ \prod_j[b_j-r_{\rm free},\ a_j+r_{\rm free}]
\ne\varnothing.
\tag{36}
```

Take `F_z=Delta_3`, no informative observation, and `C=I`. The unrestricted
center `(1/2,1/2,1/2)` has radius `1/2` but is not a law. A compatible law
with radius `r` must satisfy `1-q_i<=r` for all three coordinates; summing
gives `r>=2/3`. The uniform law attains that bound. For a scalar target on
a convex fiber the midpoint can be attained by a law, so this particular
coherence penalty is multidimensional. Other norms require their own center
analysis; half the diameter is not a universal vector-radius formula.

This generic center machinery, its factor-two bound, and related probability-
simplex gaps already occur in phase-two records. F16's equal-radius result
uses its particular reset/price/source geometry; convexity alone does not
supply the intersection in (36). Its existing noisy-source boundary remains
an inherited example, not a new P3-02 experiment.
[F16 generic centers](../../v2/work_logs/F16_2026-10-05_S1/root_reconstruction.md)
and [uncertain-source boundary](../../v2/work_logs/F16_2026-10-05_S1/source_uncertainty_boundary.md).

### Noisy calibration is a different observation model

For unknown common-scale values `x_i=s p_i`, suppose the observations are
`z=(2,1)` with errors `(1/2,1/4)`. The compatible value box is
`x_1 in [3/2,5/2]`, `x_2 in [3/4,5/4]`; it proves `s=x_1+x_2>=9/4`.
The exact probability interval is

```math
\frac6{11}\leq\frac{x_1}{x_1+x_2}\leq\frac{10}{13}.
\tag{37}
```

The lower affine certificate is `6x_2-5x_1<=0`, the upper is
`3x_1-10x_2<=0`, and the appropriate box corners attain both bounds.
Its midpoint `94/143` has radius `16/143`; normalizing the observed vector
gives `2/3` with larger worst error `4/33`. If the scale were separately
known to be `3`, the additional equality would narrow the interval to
`[7/12,3/4]`. Assuming that calibration without evidence would overstate
the retained information. These ratio bounds concern an enlarged calibration
source, not the unchanged fixed-`L` box-noise model of (32).

A compatible decoded law is still an estimate. Selecting it does not license
replacing the compatible source by its singleton for future queries. Likewise,
a simultaneous confidence-source guarantee can bound the unconditional event
of a selected false conclusion, but does not automatically give the same
error probability conditional on accepting a conclusion. No statistical
coverage, online learning or revision policy is proved by these deterministic
recovery calculations.

## 13. What the inherited native language can certify

The mathematical recovery statements do not silently extend the language.
Phase two admits known rational affine coefficients and finite piecewise-affine
terms, explicit nonempty rational polyhedral source cases, and declared directed
unit conversions. A coordinate named `p` is not a probability merely because
its unit is called `P`: nonnegativity, normalization and payoff meaning are
separate source premises.
[Core](../../v2/foundations/03_provisional_core.md),
[inference rules](../../v2/derivations/02_inference_rules.md), and
[P3-01 boundary](../foundations/01_representation_boundaries.md).

### A calibrated binary certificate

Let `p:P`, `y:U`, and declare only `w:P->U` with factor `4`. Suppose the
source states `y=1_U+w(p)`, `2_U<=y<=3_U`, and `0<=p<=1`.
Adding the correct source rows gives native loss-unit conclusions
`w(p)<=2_U` and `-w(p)<=-1_U`. The full numerical source therefore implies
`1/4<=p<=1/2`.

But without a declared path from `U` to `P`, these are not native
probability-unit conclusions. The target-`P` reduct retains only `0<=p<=1`;
the assignment `p=3/4,y=5/2` satisfies that reduct and refutes `p<=1/2`.
This is the inherited unit-reduct obstruction, not a failed search budget.
A declared reciprocal calibration with factor `1/4` converts the actual
loss-unit proofs, including their budgets, into the probability-unit bounds.
Alternatively an explicit external semantic adapter can interpret the
loss-unit results; it must not describe that interpretation as a native
undeclared inverse.

### A finite matrix certificate

After legitimate unit transport, retain both orientations of

```math
p_1+p_2+p_3=1,\qquad
p_1+2p_2=5/4,\qquad p_2+3p_3=5/4,
\tag{38}
```

together with nonnegativity. The augmented matrix has determinant `4`, and
its unique law is `(1/4,1/2,1/4)`. For example, putting
`s=p_1+p_2+p_3`, `ell_1=p_1+2p_2`, `ell_2=p_2+3p_3`,

```math
p_1=(3/2)s-(1/2)\ell_1-(1/2)\ell_2.
```

The source rows `s<=1`, `-ell_1<=-5/4`, `-ell_2<=-5/4`, with
nonnegative multipliers `3/2,1/2,1/2`, certify `p_1<=1/4`.
Opposite equality orientations certify its lower bound; the other two
coordinates work in the same way. Signed row-span coefficients are legal
because both equality orientations are retained. They do not permit
multiplying a one-sided inequality by a negative number while preserving
its direction. General rational LP witnesses in section 6 can be checked
by the same arithmetic after actual unit transport and source validation.

### Ratios, uncertain products and proof scope

Under a justified common-positive-scale interpretation `v_i=s p_i`, a fixed
rational threshold `p_i>=t` is equivalent to
`t sum_j v_j-v_i<=0`. This is an affine loss-unit query. If the source proves
a known rational lower bound `sum_j v_j>=eta>0`, the external ratio
interpretation is justified even though variable division is not native.
The global mathematical domain `s>0` is open; representing it by one of the
native closed source cases requires such an actual bound or a separately
checked concrete observation. It is not silently encoded by a finite union
of closed positive-margin cases covering every positive scale.

Known statewise random-stake payoffs are finite affine rows in the joint law.
The independent-box projection in section 11 is also affine after its proved
elimination. Arbitrary products of jointly uncertain coefficients and
probabilities, variable scoring-rule optimization, variable ratios, and
unprovided unit inverses remain outside the inherited exact grammar unless
an appropriate extension or proved enclosure is explicitly supplied.

### Executed native development scope

The [native check](../checks/02_native_probability_check.py) reuses the
unchanged F06/F07/F08 tooling with newly declared P3 source scopes. Its first
run passed five supplied groups: **13 accepted native target receipts,
three expected rejections**, and the feasible probability-unit reduct
countermodel. It checks loss-unit inversion, a declared reciprocal calibration,
six bounds recovering the three-state law, invalid negative multipliers,
and three affine certificates for a common-scale threshold example.
The [saved result](../work_logs/P3_02_2026-10-07_S1/development/native_probability_agent.json)
retains complete traces, requests, source contexts and dependency hashes.

The observations and payoff identities in these fixtures are stipulated
mathematical premises. The run demonstrates acceptance/rejection at this
interface; it does not produce empirical probability estimates, prove their
coverage, implement a general learner, or turn a recovery identity into an
automatic native probability calculus. The
[separate native reconstruction](../work_logs/P3_02_2026-10-07_S1/reviews/native_probability_bridge.md)
records the rules and actual execution boundaries.

## 14. Conditional probabilities and ratios of retained losses

The unknown-scale obstruction PI-10 concerns **nonconstant linear targets**.
It does not say that every nonlinear probability property is lost. A
conditional probability gives a constructive and useful exception.

### Nonconstant ratio characterization (PI-14)

Let `P` be nonempty convex, let `a,b` be known rows with `bp>0` throughout
`P`, and assume the target

```math
T(p)=\frac{ap}{bp}
\tag{39}
```

is nonconstant on `P`. With known-unit observations `Lp`, this target is
recoverable globally iff **both** numerator and denominator are recoverable:

```math
ah=bh=0\qquad(h\in V\cap\ker L),\qquad V=\mathrm{span}(P-P).
\tag{40}
```

**Proof.** For an interior point relative to `aff(P)`, every sufficiently
small perturbation in a hidden direction `h` remains in the same fiber.
Constancy of (39) on that segment gives
`(ah)(bp)-(bh)(ap)=0`. This holds at every relative-interior law. If `bh`
were nonzero, it would force `T(p)=ah/bh` throughout the relative interior,
and by continuity throughout `P`, contradicting the nonconstant premise.
Thus `bh=0`, and positivity of `bp` gives `ah=0`. Conversely these two
annihilation conditions recover numerator and denominator by PI-3, so their
ratio is known. No compactness or positive uniform lower bound on `bp` is
needed for this exact information statement. A constant target needs no
observation and is expressly excluded from its necessity claim.

With a common unknown positive scale, `v=sLp`, use instead

```math
ah=bh=0\qquad(h\in W\cap\ker L),\qquad W=\mathrm{span}(P).
\tag{41}
```

Indeed the positive cone `C_+(P)={sp:s>0,p in P}` is convex and has affine
direction space `W`; the ratio is unchanged by positive scaling. Apply the
same hidden-direction argument to `x=sp` on that cone. For a source
containing all interior simplex laws, (40) becomes
`a,b in row([1^T;L])`, while (41) becomes `a,b in row L`.
Taking `b=1^T` recovers PI-10's nonconstant linear-target condition. For a
conditional denominator, the constant row need not be present.

**Positive case without scale recovery.** Use states
`A and B`, `not A and B`, and `not B`. The known rows
`a=(1,0,0)`, `b=(1,1,0)` give `T=Pr(A|B)` whenever `Pr(B)>0`.
Observed values `v_1=s Pr(A and B)`, `v_2=s Pr(B)` identify
`T=v_1/v_2`, although they need not identify `s`, `Pr(B)`, or the full law.
The constant row is absent from their rowspace because both rows vanish
outside `B`. This is genuine probability information under the stipulated
loss semantics, not recovery of an unconditional probability by assumption.

Convexity is substantive. On the catalogue `P={e_1,e_2,e_3,e_4}`, use
`a=(1,2,1,2)`, `b=(1,2,2,4)`, and `L=(0,0,1,1)`.
The nonconstant ratio takes values `(1,1,1/2,1/2)` and is identified by `L`,
although neither numerator nor denominator is identified within the fibers.
The convex-source necessity does not apply to that catalogue. Likewise,
a ratio can be constant on one particular observation fiber even though
its numerator and denominator vary there; the global nonconstant premise
must not be repurposed as a local criterion.
The [separate ratio review](../work_logs/P3_02_2026-10-07_S1/reviews/conditional_probability_review.md)
checks these boundaries and the scale extension.

### A threshold can need less information than its conditional probability

In the same three states, retain only the nonnegative loss
`L'=(2,0,1)=1^T+(1,-1,0)`. Observation `L'p=6/5` fixes
`d=p_1-p_2=1/5`. Write
`p=(u+d,u,1-2u-d)`, where `0<=u<=2/5`. Then

```math
\Pr(A\mid B)=\frac{u+d}{2u+d}\in[3/5,1].
\tag{42}
```

Both endpoints are attained, so the probability is only partially identified,
but its comparison with `1/2` is settled. For example, the laws
`(2/5,1/5,2/5)` and `(1/2,3/10,1/5)` give conditional probabilities
`2/3` and `5/8` with the same retained loss. At the different observation
`L'p=1`, the admitted positive-denominator fiber has conditional probability
exactly `1/2`, although its event mass can vary. The pure `not B` law has
zero denominator and is outside this conditional service.

More generally, for a fixed threshold `tau` and positive denominator,
`T(p)<=tau` is exactly `(a-tau b)p<=0`. A certified affine inequality
can therefore answer a conditional threshold without evaluating variable
division or identifying the ratio numerically. Native use still requires the
correct units, source premises and, where demanded by a closed source case,
a proved denominator margin.

### Sharp ratio intervals and denominator stability

For a rational nonempty compact polytope
`F={p>=0:Bp=d,Gp<=g}` with normalization included in `Bp=d`, assume
`bp>=beta>0`. The substitution `t=1/(bp)`, `x=tp` turns optimization of
`ap/(bp)` into the ordinary linear program

```math
\begin{aligned}
\text{minimize or maximize }& ax,\\
\text{subject to }& Bx=dt,\quad Gx\le gt,\quad bx=1,\\
&x\ge0,\quad 0\le t\le 1/\beta.
\end{aligned}
\tag{43}
```

Normalization gives `1^T x=t`; together with `bx=1`, it forces `t>0`.
Thus `p=x/t` is the inverse construction. This is the positive-denominator
specialization of ordinary linear-fractional programming, not a new solver.
[P02-S8](../literature/02_probability_sources.md)
A threshold certificate may instead bound the linear row `a-tau b`
directly. The stated positive margin makes this transformed source compact
and supports stability; it is sufficient, not a claim that every sharp
fractional optimum requires such a uniform margin.

Exact recovery alone does not ensure a stable conditional estimate. With
`p_epsilon=(epsilon,0,1-epsilon)` and
`q_epsilon=(0,epsilon,1-epsilon)`, their full laws approach each other as
`epsilon` tends to zero, but `Pr(A|B)` remains respectively one and zero.
Even a small full-law error need not control a rare-event conditional ratio.
If `u=Pr(A and B)`, `v=Pr(B)>=beta`, estimates satisfy
`|u_hat-u|<=eta_u`, `|v_hat-v|<=eta_v<beta`, and the estimated denominator
is used, then

```math
\left|\frac{u_{\rm hat}}{v_{\rm hat}}-\frac uv\right|
\le\frac{\eta_u+\eta_v}{\beta-\eta_v}.
\tag{44}
```

This follows by cross-multiplication and `0<=u/v<=1`. Clipping the result
to `[0,1]` cannot increase scalar error. Joint feasible-source optimization
can be sharper than this coordinatewise bound. Conditional error and
unconditional expected decision loss remain different endpoints; a large
conditional error on a rare event does not automatically imply a large
unconditional loss.

Finally, for reports `q in [0,1]`, the ordinary outcome loss
`1_B (q-1_A)^2` has expectation
`Pr(B)[(q-Pr(A|B))^2+Pr(A|B)(1-Pr(A|B))]`. For `Pr(B)>0`, its unique
optimal scalar report is the conditional probability. Its excess expected
loss is `Pr(B)(q-Pr(A|B))^2`; turning a small excess into a small conditional
probability error requires control of the event mass. This directly elicits
the smaller property. It supplies neither an exact optimizer nor finite-sample
accuracy; it also does not satisfy PI-7's premise of eliciting the entire
unrestricted law. Fixed rational reports have known finite payoff rows;
optimizing a variable report is an external scoring operation with its own
computational contract.

## 15. A strong ordinary affine-recovery comparator

A nonlinear fiber calculation can be useful without beating the best ordinary
method at the same endpoint. For scalar **global** worst-case recovery over a
compact convex source, an affine decoder already attains the unrestricted
information radius. This distinction is relevant to the interpretation of
section 12's sharper conditioning bound.

### Global affine sufficiency (PI-15)

Let `K` be a nonempty compact convex subset of a finite-dimensional real
space, let `N` be a known linear observation map, and let `c` be a known
scalar linear target. Then

```math
\inf_g\sup_{x\in K}|cx-g(Nx)|
=\min_{\alpha,\beta}\sup_{x\in K}|cx-\alpha-\beta Nx|
=\frac12\max_{\substack{x,x'\in K\\Nx=Nx'}}|c(x-x')|.
\tag{45}
```

The decoder output is unrestricted; source compatibility, a particular
pointwise error budget and computation costs are separate requirements.
The affine constant is allowed. Central symmetry is not needed.

**Finite polytope proof.** For `K=conv{x_1,...,x_s}`, put `z_i=Nx_i`
and `t_i=cx_i`. The best affine error is the LP minimizing `r` subject to
`t_i-alpha-beta z_i<=r` and `alpha+beta z_i-t_i<=r` for every `i`.
The paired constraints imply `r>=0`; keep `r,alpha,beta` free in the
Lagrangian. Its dual has nonnegative weights `mu_i,nu_i`, with
`sum mu=sum nu=1/2`, `sum mu_i z_i=sum nu_i z_i`, and objective
`sum (mu_i-nu_i)t_i`. Thus `x^+=2 sum mu_i x_i` and
`x^-=2 sum nu_i x_i` are admissible indistinguishable laws, and the dual
objective is half their target separation. Conversely every such pair has
a dual representation by its convex weights. Ordinary finite LP duality
therefore gives the last equality and an attained affine optimum. The
unrestricted equality is the scalar fiber argument of PI-13.

For general compact convex `K`, choose finitely many observations affinely
spanning `NK`, with source preimages. Values of any candidate affine decoder
at those points lie in a compact box if its error is bounded by the proposed
radius. Every finite further constraint set is satisfiable by applying the
polytope proof to the convex hull of its source points. Compactness and the
finite intersection property then give an affine function satisfying all
constraints. This is an existence proof, not an implementation from an
unspecified nonpolyhedral source oracle.

For bounded noise with a compact convex **joint** source, set
`x=(p,e)`, `N=[L I]`, and `c'=(c,0)`. The theorem applies to
`z=Lp+e`; it does not need a stochastic independence assumption. A
nonlinear target after eliminating nuisance parameters, or a nonconvex
joint mechanism, requires its own argument. Finite-vector unrestricted
recovery in the maximum-coordinate norm also admits a globally optimal
affine decoder: stack the optimal scalar decoders, and take the maximum
of their radii. This does not impose vector coherence or cover other norms.
The [separate proof](../work_logs/P3_02_2026-10-07_S1/reviews/affine_scalar_recovery.md)
records all these steps and their boundaries. The ordinary information-radius
framework is documented in [P02-S9/S10](../literature/02_probability_sources.md);
the present affine proof is a direct finite reconstruction, not an import
of a hyperellipsoid theorem into the simplex setting.

A sharper named ordinary ancestry is also available: Osipenko's introduction
states the Smolyak theorem for a scalar linear target on a convex centrally
symmetric source. Apply it to `W=conv{+(x,1),-(x,1):x in K}`, with
observation `(Nu,t)` on `(u,t)` and target `cu`. Its zero-information
section has `u=(x-x')/2`, `Nx=Nx'`, so the radius is the pair half-width
in (45). A linear rule on `(Nu,t)` restricts at `t=1` to an affine rule
on `Nx`. This homogenization explains the inherited optimal-recovery content;
the original 1965 source is not claimed read, and the proof above remains
self-contained.

### The sharp conditioning bound already has an affine implementation

Under exactly the `L_delta`, `delta>0`, `epsilon>=0` assumptions of (33),
the following three decoders have their stated attained errors:

| Affine decoder for `p_3` | Exact global worst absolute error |
|---|---:|
| `g_0(z)=1/2` | `1/2` |
| `g_1(z)=(z_2-z_1)/delta` | `2 epsilon/delta` |
| `g_2(z)=(z_2-1/2)/(1+delta)` | `(1/2+epsilon)/(1+delta)` |

For the third row, the error is
`(p_2-1/2+e_2)/(1+delta)`; the bounds on `p_2,e_2` give both the upper
bound and attaining endpoints. Choose the decoder with the smallest known
error bound, using `delta,epsilon`, before the observation. This attains
(33). It is **not** the pointwise minimum of the decoder outputs.
The inversion row is optimal up to
`epsilon=delta/[2(delta+2)]`, the third row from there to `epsilon=delta/2`,
and the constant thereafter; either neighboring row works at a boundary.
The previously displayed improvement over clipped inversion is consequently
not an improvement over this stronger ordinary affine baseline.

### Global optimum, pointwise optimum and compatible output differ

For `P=Delta_3`, retain `z=p_2+2p_3` and target `p_3`. Its fiber interval is
`[max(0,z-1),z/2]`, so the best global radius is `1/4`.
The affine rule `g(z)=z/2-1/4` attains it, but returns `-1/4` on the
singleton fiber `z=0`. The pointwise midpoint is instead

```math
m(z)=
\begin{cases}
z/4,&0\le z\le1,\\
3z/4-1/2,&1\le z\le2.
\end{cases}
\tag{46}
```

It is compatible and has the same global radius. Any affine rule also
required to be compatible at **every** observation must pass through the
two singleton endpoints, hence be `z/2`; its global radius is `1/2`.
An ordinary piecewise-affine solver is allowed to use (46), so this is a
service distinction, not an exclusive advantage for the native language.

If the source contains only the three pure laws rather than their convex
hull, the three observed values are distinct and a nonlinear lookup recovers
the target exactly. The best affine radius is still `1/4`. This counterexample
shows why PI-15 must retain its convexity premise and why adding possible
mixtures can change an information problem.

## 16. Finite storage, realized observations and one scalar risk

The preceding exact-real observation counts are not bit counts or sample
complexities. The distinction matters for a bounded reasoner and already
appears in phase two's
[future-query and finite-code discussion](../../v2/derivations/06_n01_decision_retention.md#d20-current-answers-and-sufficiency-for-future-edits-are-different-contracts).
The following direct reconstructions make several relevant limits explicit.

### A finite code budget has a different sharp bound

For any deterministic encoder of `p in [0,1]` into at most `N>=1` codes
and decoder outputs `d_1,...,d_N`, let
`R=sup_p |p-d_(code(p))|`. The `N` intervals `[d_j-R,d_j+R]` cover
`[0,1]`; their total length is at most `2NR`. Consequently

```math
R\ge\frac1{2N}.
\tag{47}
```

Equal-width bins with midpoint decoding attain this bound. No continuity or
measurability assumption on the encoder is needed. At most `B` fixed-length
bits therefore imply `R>=2^(-B-1)`. A specified floating-point format need
not attain that optimum, and arbitrary exact-real coordinates are a different
interface. Exact recovery of an entire continuum is impossible with finitely
many codes.

A fixed action label can be much cheaper: one bit stores the answer to a
specified binary threshold. This presumes the encoder can compute the answer
from its permitted evidence. It gives no free access to the latent law and
need not preserve other thresholds, changed prices or future source edits.
The same qualification applies to the ideal equal-bin encoder itself.

### One finite sample and a known sampling distribution are different inputs

For `N>=1` iid Bernoulli observations and `0<p<1`, every binary transcript
with `k` ones has likelihood `p^k(1-p)^(N-k)>0` under every interior law.
Thus its strict positive-likelihood compatibility set is still `(0,1)`.
No decoder of that transcript has a zero-error full-probability guarantee
uniformly over all parameters and possible transcripts; the strict
worst-case absolute radius remains `1/2`.

This does not mean the observation lacks statistical information. After `N`
ones, for example, the likelihood ratio of `p=3/4` to `p=1/4` is `3^N`.
The statistical model is identifiable from its **transcript distribution**:
that distribution's first-coordinate probability is `p`. Confidence with
nonzero failure allowance, posterior inference and consistency are different
guarantees. None is supplied by the zero-error support argument. It also does
not model the truth of a fixed mathematical statement as an iid random outcome.

A fixed finite loss row can likewise have distinct realized values for all
states, making the **distribution of its realized loss** identify the law,
while its single mean does not. With loss `(0,1,2)`, the laws
`(1/2,0,1/2)` and `(0,1,0)` have equal mean one but different realized-loss
distributions. Mean recovery, observing a draw, and knowing the distribution
of draws must not be interchanged.

### The sample coupling belongs in a score-recovery contract

For fixed report rows and a common outcome batch `Y_1,...,Y_M`,

```math
\frac1M\sum_{t=1}^M L[:,Y_t]=L\widehat p,
\qquad
\widehat p_i=\frac{\#\{t:Y_t=i\}}M.
\tag{48}
```

Thus an exact inverse returns the empirical law. This algebra needs no iid
assumption; connecting the empirical law to a population law requires a
separately justified sampling or error model. If positive trial stakes
`s_t` are shared across all probes but vary by trial, calibration can instead
return the empirical law weighted by those stakes. The output is not thereby
the unweighted empirical law or an earlier subjective belief.

Different probe batches need not produce any coherent exact expectation
vector. For the two vertex reports of binary vector-Brier loss, every
expected-score vector is `(2p_2,2p_1)` and sums to two. Scoring the first
report on outcome 1 and the second on a separate outcome-2 trial gives
`(0,0)`. Both realized scores are legitimate; interpreting them as the exact
means of one normalized law is not. A separately justified joint error or
sampling contract is needed.
The [finite-observation review](../work_logs/P3_02_2026-10-07_S1/reviews/finite_observation_boundaries.md)
records these constructions, including the state-dependent trial-weight case.

### Strict propriety does not impose one universal scalar-risk answer

One scalar **optimal** risk can identify a binary law for a suitable known
score. For `Y in {0,1}`, the loss
`ell(q,Y)=(q-Y)^2+2Y`, `q in [0,1]`, remains strictly proper and has

```math
R_p(q)=(q-p)^2+3p-p^2,\qquad
H(p)=\min_q R_p(q)=3p-p^2.
\tag{49}
```

The Bayes risk `H` is strictly increasing on `[0,1]`, with inverse
`p=(3-sqrt(9-4H))/2`. A guarantee of the exact optimum value is part of
this input contract; merely observing a score or an approximate optimization
result is not that oracle. The state-dependent additive term preserves the
optimal report while changing the scalar risk's information content.

For `n>=3`, no **continuous** scalar summary identifies all interior simplex
laws. Choose a small two-dimensional circle in the interior. The difference
between the summary at opposite points is continuous and changes sign after
half a turn; the intermediate value theorem therefore gives distinct opposite
laws with equal summaries. Under PI-7's assumptions the finite Bayes risk is
concave and hence continuous on the interior, so this applies to its single
optimal value. It does not cover arbitrary discontinuous encodings, restricted
one-dimensional sources or the optimizer report itself. The
[scalar-risk audit](../work_logs/P3_02_2026-10-07_S1/reviews/noise_principal_audit.md#6-one-scalar-optimal-risk-a-scoped-positive-and-obstruction)
supplies the direct proof and local continuity justification. No general
representation format for value logic is chosen by these scoped limits.

## 17. Arbitrary monotone units and outcome-dependent stakes

The calibration class matters. A known invertible transformation of an exact
expectation can be undone; a shared unknown positive affine transformation has
the finite calibration results above. Arbitrary unknown increasing transforms
have a different information boundary. Transforming the semantic payoffs is
also a different operation from transforming their already computed means.

### Weak-order characterization (PI-16)

Let `L` have finitely many fixed known rows and let the recorded vector be
`v_j=g((Lp)_j)`, where one arbitrary strictly increasing real function `g`
is shared across this record and unknown. Recovery must work for every
admissible pair `(p,g)`. Two laws can produce the same record, with different
candidate nuisance functions, **if and only if their labeled risk vectors
have the same complete weak order, including ties**.

Necessity follows because strict increase preserves and reflects every
comparison and equality. For sufficiency, list the distinct levels of each
risk vector in their common order. Map each list to the same increasing list
of output levels by linear interpolation, extending both exterior intervals
with positive slopes. These globally strictly increasing functions produce
the same record. The construction also works within continuous increasing
bijections. Consequently an arbitrary target is recoverable exactly when it
is constant on these weak-order classes.

On the full interior of `Delta_n`, `n>=2`, this finite service cannot identify
the full law or any nonconstant linear expectation. The finitely many proper
tie hyperplanes `(L_i-L_j)p=0` leave some relative open ball avoiding them;
identically tied rows can be ignored. The complete weak order is constant on
that ball, while every nonconstant linear target varies there. This rules out
arbitrary exact decoders under the stated finite-query nuisance contract.
It is not a claim about every value representation or a full report-order
oracle.

There is a useful positive case: if the queried rows are the action menu,
their complete preference ordering, optimal set and any fixed tie rule are
preserved. No full law or absolute risk recovery is necessary. By contrast,
transformed numerical gaps have no uniform interpretation as original regret
without restrictions on `g`. A merely nondecreasing transformation may merge
distinct risks and create false ties.

Even zero and one anchors do not calibrate an otherwise arbitrary increasing
function. Query binary rows `(0,0)`, `(1,1)` and `(1,0)`. The law
`p=(1/4,3/4)` with the identity transformation gives `(0,1,1/4)`. The law
`q=(3/4,1/4)` gives that same record under

```math
h(t)=\begin{cases}t/3,&t\le3/4,\\3t-2,&t\ge3/4.\end{cases}
\tag{50}
```

Both branches agree at `3/4`, have positive slopes, and fix zero and one.
The event probabilities nevertheless differ. Additional finite anchors can
bound intervals without removing the general open-cell obstruction.

The nuisance quantifier is essential: comparing two hypotheses while forcing
the *same fixed* injective `g` would preserve the original `Lp` equality
classes. That does not describe a decoder ignorant of which `g` generated
the record. Likewise, a function shared across multiple observed records
imposes cross-record comparisons; apply the finite-order analysis to the
combined labeled vector rather than discard that information.

An oracle supplying the entire expected-score ordering over all reports of
a strictly proper score determines its unique minimizing report, when that
report is admitted and propriety holds there. A common increasing transform
after expectation preserves this optimizer. Extracting it from an entire
order relation or receiving it from an optimization service is a stronger
access contract than finitely many fixed score probes. No finite-call
algorithm for an arbitrary real optimizer follows from this statement.

### Transforming payoffs can change the decision

Take `p=(1/2,1/2)`, action losses `ell_A=(0,4)` and
`ell_B=(5/2,5/2)`. Squaring is strictly increasing on their nonnegative range.

| Quantity | Action A | Action B | Minimizer |
|---|---:|---:|---|
| Original expectation `E[ell]` | `2` | `5/2` | A |
| Square the expectation `(E[ell])^2` | `4` | `25/4` | A |
| Square each payoff first `E[ell^2]` | `8` | `25/4` | B |

The last operation changes the semantic gamble. It is not merely a new label
for the old expected loss. The globally increasing function `t|t|` supplies
the same example if the transformation must be defined on all reals.
Positive affine transformations are the commuting case:
`E[alpha ell+beta]=alpha E[ell]+beta`, for known normalized expectation
and `alpha>0`. Neither this identity nor the counterexample imports a broader
utility-representation theorem.

### Outcome-dependent stakes tilt the scoring target

For a score `ell(q,i)` and strictly positive finite outcome stakes `s_i`
shared across reports, define

```math
S=\sum_i p_i s_i>0,\qquad r_i=\frac{p_i s_i}{S}.
\qquad
\sum_i p_i s_i\ell(q,i)=S R_r(q).
\tag{51}
```

If the base score is strictly proper at the admitted report `r`, the unique
minimizer is `r`, which can differ from `p`. An interior-only score need not
attain its minimum when `r` is a boundary law; full-simplex Brier loss does.
Common positive stakes preserve `r=p`; for a fixed law this equality holds
exactly when the stakes are constant on its support. Known relative stakes
permit the inverse

```math
p_i=\frac{r_i/s_i}{\sum_k r_k/s_k}.
\tag{52}
```

Independently unknown positive stakes instead confound the weights. Even the
full event-value vector `v_i=s_i p_i` identifies only support in general:
every normalized law `q` with that same support matches it using
`t_i=v_i/q_i` on the support and arbitrary positive stakes elsewhere. A
singleton support is the explicit full-law exception. Normalizing `v`
returns the tilted law `r`.

For example, `p=(1/2,1/2), s=(1,3)` and
`q=(1/4,3/4), t=(2,2)` both give event values `(1/2,3/2)` and the same
**entire expected-score function** for every report. For binary squared loss
with the first outcome coded one, the minimizing report is `1/4`: its staked
risk is `3/8`, compared with `1/2` at report `1/2`. An optimizer oracle does
not recover the original unweighted law under these unknown stakes.

Report-independent outcome additions contribute the same `a p` to every
report risk and preserve its optimizer at a fixed law. They can still change
absolute risks and uncertainty-set criteria. Zero or negative stakes,
report-dependent transformations, and law-dependent decision objectives
require separate premises. These are direct semantic reconstructions and
counterexamples; the [unit review](../work_logs/P3_02_2026-10-07_S1/reviews/nonlinear_unit_boundaries.md)
records their fuller assumptions. No nonlinear primitive is thereby added to
phase two's native language.

## 18. Minimum repair of a specified target under four calibration contracts

PI-11 repairs a known-unit target. PI-10 specifies which targets survive
unknown common scale and offset. Combining them gives a constructive
target-specific repair count, without requiring reconstruction of the full
law or every nuisance parameter.

### Calibrated repair characterization (PI-17)

Let `L` and `C` be known finite rational matrices on the **full** `Delta_n`.
Every old and additional query concerns the same `p` and the same nuisance
parameters. Additional queries may be any fixed known rational loss rows;
finite negative payoffs are allowed. Their number counts scalar raw queries,
not arithmetic, acquisition cost or bits. The observation contracts are
`Lp`, `Lp+b 1`, `s Lp`, and `s Lp+b 1`, with `s>0` where unknown.
Any known nonzero scale and known offset have first been removed.

First, if all target rows are constant across states, no query is needed.
This includes an empty target family and every target when `n=1`. Assume
hereafter that at least one target is nonconstant.

If the offset is known, let `M=L`. If it is unknown and at least one old
row exists, choose a reference `L_0` and let `M` contain the differences
`L_j-L_0` for `j>0`. With no old row, set `M` empty. Define the base `B`,
required rows `R`, and missing dimension by

```math
\begin{array}{c|c|c}
&B&R\\\hline
\text{known scale}&[\mathbf1^T;M]&C\\
\text{unknown positive scale}&M&[\mathbf1^T;C]
\end{array}
\qquad
r=\mathrm{rank}[B;R]-\mathrm{rank}B.
\tag{53}
```

The exact minimum number of additional raw queries is

```math
\boxed{r+\mathbf1\{\text{offset unknown and no old row exists}\}.}
\tag{54}
```

**Lower bound.** With an old offset reference, a new raw row `a` contributes
the effective row `a-L_0`; with known offset it contributes `a`. Each adds
at most one dimension. The known-scale criterion requires the target rows
in the completed augmented row space. For unknown scale, any nonconstant
target also requires the constant row, by PI-10. Thus at least `r` additional
effective dimensions are necessary. If an unknown offset has no old
reference, `t` raw queries supply at most `t-1` difference rows, giving the
extra one. These criteria rule out arbitrary exact decoders, not just linear
ones.

**Construction.** Choose required rows `q_1,...,q_r` whose cosets extend the
base to include all of `R`. Iterating through the rational rows of `R` and
retaining each rank increase suffices. Query these raw rows:

| Offset information | Additional raw rows |
|---|---|
| Known offset | `q_1,...,q_r` |
| Unknown offset with old reference `L_0` | `L_0+q_1,...,L_0+q_r` |
| Unknown offset with no old row | `0,q_1,...,q_r` |

The completed effective rows contain the required span. Known-scale targets
therefore have identities `c=gamma 1^T+beta M_final`, hence decoder
`gamma+beta z`. Under unknown scale there are identities
`alpha M_final=1^T` and `beta M_final=c`; on any admissible record,
`alpha z=s>0` and `cp=(beta z)/(alpha z)`. This is a mathematical ratio
decoder, subject to §13's native-language distinction.

The no-old-query specialization is particularly simple. For a nonconstant
target family let `d_C=rank[1^T;C]-1`.

| Contract | Minimum fixed scalar raw queries from scratch |
|---|---:|
| Known units | `d_C` |
| Unknown common offset | `d_C+1` |
| Unknown common positive scale | `d_C+1` |
| Unknown common positive scale and offset | `d_C+2` |

Full-law recovery substitutes `d_C=n-1`, for `n>=2`. A single specified
nonconstant expectation needs only `1,2,2,3` respectively, irrespective of a
larger state count. Constants need zero under all four contracts. Repeated
or zero old rows are handled correctly: a zero old row supplies an offset
reference even though it adds no linear rank.

**Recovering the target need not recover the offset.** With three states,
old row `e_2`, target `p_1`, and unknown positive scale and offset, add
`e_2+1` and `e_2+e_1`. Their differences identify `s` and `s p_1`.
Nevertheless

```math
(p,s,b)=((1/2,1/4,1/4),2,0),\qquad
(q,s,b')=((1/2,1/8,3/8),2,1/4)
\tag{55}
```

both yield the complete raw record `(1/2,5/2,3/2)`. The target and scale
are known while the offset and remaining law remain confounded. Calling
this complete nuisance calibration would overstate the service.

The [repair review](../work_logs/P3_02_2026-10-07_S1/reviews/calibrated_repair_review.md)
gives the detailed quotient proof and edge cases. This is a finite
retention/repair adaptation with ordinary row-space and nuisance-calibration
ancestry. A restricted purchasable menu, query-specific stakes, noisy values,
adaptive acquisition or a smaller source changes the problem. The dimension
count does not assert that every chosen semantic payoff is cheaply available.

### Nonnegative rows, bounded stakes and restricted purchases

Requiring every **added** payoff row to be nonnegative, or even strictly
positive, does not increase PI-17's full-simplex linear-target count when
there is no upper bound and all such rows are available. With known scale,
the constant row is already in the base; shift a required row by a sufficiently
large known rational multiple of `1`. With unknown scale and a nonconstant
target, first retain or acquire the required constant calibration direction,
using one of the already counted queries, and then make those shifts. If the
offset is unknown, shift the proposed raw row relative to its old reference;
with no old reference, start with a positive constant reference instead of
zero. The [scope review](../work_logs/P3_02_2026-10-07_S1/reviews/calibrated_repair_scope.md)
gives all four constructions. These arbitrary shifts are not free in money
or risk merely because the number of scalar queries is unchanged.

A fixed semantic payoff box can have a different answer. On `Delta_4`, take
one old row `a=(0,0,1,1)`, target `c=(0,1,0,1)`, and allow additional raw
payoff rows only in `U=[0,1]^4`. Then

```math
(a+\mathrm{span}\{\mathbf1,c\})\cap U=\{a\}.
\tag{56}
```

Indeed a candidate has coordinates
`(beta,alpha+beta,1+beta,1+alpha+beta)`. The first and third box constraints
force `beta=0`; the second and fourth then force `alpha=0`.

With known scale and unknown offset, a single successful new row would have
to be `a+alpha c+beta 1`, `alpha!=0`. Equation (56) excludes it. Two boxed
queries `0,c` suffice by their difference, so the minimum rises **from one
to two**. With unknown positive scale and offset, two successful new
differences would have to span exactly `span{1,c}`. Both corresponding raw
rows are again excluded by (56). Three boxed queries `0,1,c` recover the
scale and target, so the minimum rises **from two to three**. The old row
also obeys the box. The box constrains semantic stakes in the declared
units, not the transformed numbers `s Lp+b 1`.

There is an exact test for this extra query. Suppose an old offset reference
`L_0` exists, the free deficit is `r>0`, and every row of `U=[0,1]^n` is
available. Write `B` for the base row space in (53), `W=B+row(R)`, and
`S=(U-L_0) intersect W`. The boxed minimum is

```math
\begin{cases}
r,&B+\mathrm{span}S=W,\\
r+1,&B+\mathrm{span}S\ne W.
\end{cases}
\tag{57}
```

For necessity of the first line, `r` successful new differences leave no
dimension outside `W`: their span with `B` must equal `W`. Each must lie
in `S`. Conversely, choose `r` members of `S` whose classes form a basis
of `W/B`. Their raw rows are boxed and supply exactly the required
directions. With rational input, the bounded rational polytope `S` is
spanned by its rational vertices, so rational query choices suffice.

For the remaining upper bound, buy the interior reference `(1/2)1` first.
The remaining rank gap cannot increase. Small rational perturbations of
that reference realize every remaining required direction inside the box,
using at most `r` further queries. This proves the second line when the
first condition fails. If the target is already recovered, no query is
needed. With known offset, or with no old reference so its first query is
already counted, the full box preserves PI-17's count. An interior old
reference, including a computable affine combination of old rows whose
coefficients sum to one, is sufficient to attain `r`; it is not necessary.

A finite purchasable menu can impose a larger penalty or make repair
impossible. With known units, no old queries and target `p_1` on `Delta_3`,
the menu `{(1,1,0),(0,1,0)}` requires both rows, although the free gap is
one: their difference is `e_1`, while neither alone separates the relevant
pure-law pair. The menu `{1,e_2}` never separates `e_1` from `e_3`, so no
number of repetitions repairs that target. Minimizing actual acquisition
price requires that menu and its costs, not just the free rank deficit.

### A precise additional condition for offset recovery

For any completed nonempty raw menu `F`, choose reference `F_0` and
difference matrix `D_F`. With known nonzero scale, the offset is recoverable
on the full simplex exactly when `F_0 in row[1;D_F]`. If
`F_0=gamma 1+beta D_F`, its value is `b=v_0-s gamma-beta z`, where `z`
contains raw differences. Failure supplies a normalized hidden direction
along which changing the law and offset leaves the record fixed.

With unknown positive scale and offset, the exact criterion instead is

```math
F_0\in\mathrm{row}D_F
\quad\Longleftrightarrow\quad
0\in\mathrm{aff}\{F_i\}.
\tag{58}
```

An affine combination of the payoff rows equal to zero gives the same
combination of their readings equal to `b`. Conversely let `x=s p`, whose
admissible set contains the positive orthant. If no such extracting row
identity exists for the observation map `[F,1]`, a kernel direction
`(h,k)` with `k!=0` changes `b` while preserving the record; a small
perturbation keeps `x>0`. This proves necessity. Partial-target recovery
can identify `s` without satisfying (58). Full-law recovery with `n>=2`
does imply it under this nuisance contract, but the constant one-state law
does not. These are additional service conditions, not promises made by
the target-repair count.

## 19. A constructive exact certificate companion

The [audit program](../checks/02_finite_information_audit.py) implements a
strictly smaller fragment than this entire note: known rational `L,C`, the
full real normalized simplex, exact expected-loss semantics, and one of the
four shared scale/offset contracts. It accepts a measurement design and target
family, not observed samples or a fitted probability model. It returns:

- an affine or ratio row identity for every recoverable linear target;
- an actual pair of interior normalized laws with admissible nuisance values,
  identical raw records and different targets whenever recovery fails;
- full-law coordinate decoders or a separating-coordinate witness;
- PI-17's minimum freely chosen extra-query count, the proposed raw payoff
  rows, independent hidden directions proving necessity, and target identities
  proving the repair sufficient.

The [separate verifier](../checks/02_finite_information_verify.py) imports no
generator or elimination routine. It checks exact rational identities and
actual witness observations. For repair necessity, the selected required
rows `q_i` and hidden directions `h_j` satisfy `B h_j=0` and
`q_i h_j=delta_ij`; this proves their independence modulo old information.
The repaired positive certificates establish sufficiency. Summary rank
numbers and construction-only intermediate fields are not independently
certified by this verifier.

### Concrete interface

For old loss `e_2`, target `p_1`, and unknown common scale and offset, an
input file contains

```json
{
  "n_states": 3,
  "losses": [[0, 1, 0]],
  "targets": [[1, 0, 0]],
  "calibration": "unknown_affine"
}
```

Run from the repository root, choosing a fresh result path:

```bash
python v3/checks/02_finite_information_audit.py --input input.json --output certificate.json
python v3/checks/02_finite_information_verify.py certificate.json
```

The certificate says the old target is not globally recoverable and supplies
a same-record obstruction. Two extra rows `(1,2,1)` and `(1,1,0)` suffice
and are minimal. Their record differences decode
`p_1=(v_2-v_0)/(v_1-v_0)`, with `v_1-v_0=s>0`. Both hypotheses in (55)
therefore return `1/2`, despite their different offsets and remaining law.
No observed `v` is needed to certify this design-level identity. Applying it
to particular numbers still requires the declared expectation premises.

JSON integers and exact rational strings are accepted; floating-point JSON
numbers, booleans, bad dimensions and unsupported source or calibration
fields are rejected. Omitting `targets` requests all coordinates; an empty
target list requests the vacuous service. A result path is created
exclusively so an existing result is preserved.

### Arithmetic validity, input binding and semantic truth are distinct

Verifier acceptance is relative to the **problem declared inside its
certificate**. It does not authenticate execution metadata, compare against
an independently supplied original request, prove the semantic loss table
correct, or establish that future numbers are expectations. The generator's
CLI records source and input byte hashes; a caller must separately compare
those with its actual inputs. The saved standalone interface check performs
that additional comparison for the example above.

The mathematical companion also does not establish native proof eligibility.
It permits ordinary signed rational row calculations and symbolic ratio
decoders under their hypotheses. Section 13 separately checks what can be
expressed or certified through inherited source scopes and directed units.
The independent arithmetic verifier and the unchanged native checker serve
different declared contracts.

This companion does not implement the note's arbitrary restricted sources,
decision-only criterion, noisy intervals, unknown payoff matrices, monotone
calibration, bounded purchasable menus, conditional ratios, computational
budgets or any logical forecast learner. An ordinary probability method may
use the same program and certificates.

### Recorded development evidence

The [first saved corpus run](../work_logs/P3_02_2026-10-07_S1/development/constructive_audit_1.json)
passed **10,660** deterministic cases: 9,744 three-state certificate cases,
880 binary cases checked against a separate slope/determinant and exhaustive
repair oracle, and 36 named rational or edge cases. All 12 expected invalid
inputs and 9 deliberately false certificates were rejected. The corpus and
code hashes were saved before execution. The 36 named certificates are
retained in full; the remaining ordered stream is represented by cumulative
digests and checkpoints, with its deterministic generating code. That digest
does not independently prove the correctness of an unavailable transcript.

The [standalone interface check](../work_logs/P3_02_2026-10-07_S1/development/constructive_cli_2.json)
then verified the example's original input binding, independent arithmetic
acceptance, both target decodes in (55), and refusal to overwrite an existing
certificate. Its
[first attempt](../work_logs/P3_02_2026-10-07_S1/development/constructive_cli_1.json)
had a path-reporting error in the interface harness after generation and
input binding succeeded. That failed result, original source bytes and
generated certificate are preserved; the corrected version completed the
same declared check. The scientific generator and arithmetic verifier were
unchanged, and the full corpus was not rerun.

These are development checks and same-model internal reviews, with no frozen
final challenge or independent scientific replication. Exact identities and
explicit collisions carry the general finite claims; enumeration exercises
the implementation and specific boundaries. Assertion counts do not count
independent findings, and concurrent execution/review adds no extra measured
principal research credit.

## 20. Calibrated information for one action can be smaller still

PI-17 concerns exact numerical targets. Even a task-specific loss vector can
retain more information than choosing one action requires. The distinction
persists under scale and offset uncertainty and has a sharp finite version.

### Calibrated essential-difference criterion (PI-18)

Use PI-9's finite action menu on the full `Delta_n`, merge identical rows,
and retain its essential set `E`. Let `D_E` contain their differences from
one essential reference. The service must return **some** Bayes-optimal
action at every law, including ties. Observations are fixed exact loss
queries under a common positive scale and/or unrestricted offset as declared.

Let `M=L` when the offset is known and use the old raw-row differences when
it is unknown. Then this service is possible exactly when

```math
\begin{array}{c|c}
\text{known scale}&\mathrm{row}D_E\subseteq
                         \mathrm{row}[\mathbf1^T;M]\\
\text{unknown positive scale}&\mathrm{row}D_E\subseteq
                         \mathrm{row}M.
\end{array}
\tag{59}
```

Unlike recovery of a nonconstant linear target, the second condition does
**not** separately require the constant row. If an essential difference is
`beta M`, the observed effective vector gives `s(c_a-c_b)p=beta z`.
Its sign is enough; the positive scale need not be decoded.

**Proof.** The known-scale case is PI-9 after removing the offset.
For unknown scale set `x=s p`. Its admitted source is the convex cone
`{x>=0:1^T x>0}`, whose interior is the positive orthant and whose
linear span is all of `R^n`. Since `s>0`, an action minimizes `c_a p`
exactly when it minimizes `c_a x`. The essential actions are unchanged.
Apply PI-9's relative-interior facet and midpoint proof on this cone: a
hidden direction `h in ker M` crossing an essential-action facet gives two
positive source points with the same effective record and no common optimal
action. Normalizing those points gives admissible laws and positive scales.
Thus every essential difference must annihilate `ker M`, which is the
second row-space condition. Conversely that condition computes all scaled
essential differences and therefore an optimal essential action. An unknown
offset provides no extra law information beyond differences: adjust the
candidate offset to match the reference coordinate whenever the differences
match. This completes both directions, with arbitrary decoders allowed.

If there is only one essential action, it is optimal everywhere and no
measurement is needed. Otherwise put

```math
d_E=\mathrm{rank}[\mathbf1^T;D_E]-1,\qquad
r_E=\mathrm{rank}D_E.
\tag{60}
```

For rational action rows, the exact from-scratch minima for freely chosen
fixed rational raw rows are

| Contract | Minimum queries for some optimal action |
|---|---:|
| Known units | `d_E` |
| Unknown common offset | `d_E+1` |
| Unknown common positive scale | `r_E` |
| Unknown common positive scale and offset | `r_E+1` |

The lower bounds follow from (59) and the maximum rank contributed by each
raw row or difference. Bases of `D_E` modulo constants, or of `D_E`
itself, give matching constructions; an unknown offset with no old record
uses one extra reference. Here `r_E` is either `d_E` or `d_E+1`.
Strict feasibility by a rational LP can determine which finite rational
action rows are essential; that computation and query availability are
additional resource duties. No bit or sample-complexity claim follows from
these fixed linear-coordinate counts.

### A binary separation from full probability recovery

Take two action losses `c_A=(1,0)` and `c_B=(0,1)`. Their difference is
`(1,-1)`. With unknown common positive scale and known offset, the single
signed query gives `v=s(2p_1-1)`. Its sign chooses a minimizing action;
zero is the genuine tie. Neither `s` nor a nonconstant linear expectation
is globally recoverable from this one row.

For this example the exact unrestricted query counts are:

| Contract | Recover `p_1` | Choose some optimal action |
|---|---:|---:|
| Known units | `1` | `1` |
| Unknown offset | `2` | `2` |
| Unknown positive scale | `2` | `1` |
| Unknown positive scale and offset | `3` | `2` |

Under unknown positive scale, one **nonnegative** query cannot make this
decision globally. A nonzero nonnegative row has strictly positive mean
under every interior law; any positive recorded value can therefore be
matched at any such law by adjusting the scale. The zero row is also
uninformative. Two event queries `e_1,e_2` suffice by comparing their
readings. This shows why §18's no-penalty result for nonnegative queries
must stay scoped to full-simplex **linear-target recovery**, where retaining
the constant calibration direction is necessary. Decision-only recovery
does not impose that requirement.

Positive-scale invariance does not always eliminate the extra dimension.
For binary actions `(0,1)`, `(2/5,2/5)` and `(1,0)`, all three are
essential: the middle action is uniquely optimal for `2/5<p_1<3/5`.
Their essential differences span `R^2`, giving `d_E=1`, `r_E=2`.
Known scale needs one query; unknown scale needs two. A single threshold
sign and a three-region choice have different information requirements.

### The coefficient alphabet can change an exact count

The rational-action qualification in the count table is substantive. On
`Delta_3`, take two known action losses `A=(1,sqrt(2),0)` and `B=(0,0,1)`.
Their contrast `d=(1,sqrt(2),-1)` changes sign across an interior tie plane.
Assume an external exact decoder may use the known algebraic constant; no
native irrational-coefficient operation is supplied by this example.

One real signed query `d` decides the action. A single rational row cannot
do so even with known units: an identity `d=alpha 1+beta l` would force
the irrational contrast ratio `(1+sqrt(2))/2` to equal the rational ratio
`(l_2-l_3)/(l_1-l_3)`. Two rational event rows suffice with normalization.

Under unknown positive scale, two rational signed rows `(1,0,-1)` and
`e_2` preserve the sign of `d p`. But any rational plane containing `d`
has a rational normal `(h_1,h_2,h_3)` satisfying
`h_1+sqrt(2) h_2-h_3=0`; hence `h_2=0,h_1=h_3`. That plane is
`W={(a,b,-a)}`. Its nonnegative rows lie on the single `e_2` ray and
cannot span it. Therefore two rational nonnegative queries cannot implement
the exact decision. Three event rows do. The sharp counts are

| Permitted query rows | Known units | Unknown positive scale |
|---|---:|---:|
| Real, signed | `1` | `1` |
| Real, nonnegative | `1` | `2` |
| Rational, signed | `2` | `2` |
| Rational, nonnegative | `2` | `3` |

The [coefficient-alphabet review](../work_logs/P3_02_2026-10-07_S1/reviews/coefficient_alphabet_boundary.md)
supplies the arbitrary-decoder lower bounds and each attaining construction.
Only under this particular combination of target, exactness, source,
calibration and nonnegative rational queries does every successful menu
have full rank and therefore permit full-law recovery. It is not a general
necessity for useful decisions.

Approximate decision service changes the conclusion. Choose a positive
rational `a` with `|a-sqrt(2)|<=eta` and query `q=(1,a,-1)`. If its sign
selects the wrong original action, that action's regret is at most

```math
|d p|\le |(d-q)p|\le\eta p_2\le\eta.
\tag{61}
```

A common positive observation scale preserves this sign. Thus one rational
signed query achieves every specified positive regret tolerance, even though
one cannot provide the exact global service. With known units, one
nonnegative row `q+1` works by subtracting the known constant; with unknown
scale, the two rational nonnegative rows `(1,a,0)` and `(0,0,1)` work by
their difference. A true gap greater than `eta` guarantees the exact choice.
These bounds use the stated action units: multiplying the actual payoffs by
`K>0` multiplies the regret bound by `K`. This preserves P3-01's distinction
between numerical approximation and performance under growing stakes.

These results concern the listed expected-loss objective with its given
action menu. Preserving all optimal ties, every pairwise preference,
absolute risks, untransformed acquisition fees or uncertainty-set minimax
objectives can impose other requirements. The
[calibrated-decision review](../work_logs/P3_02_2026-10-07_S1/reviews/calibrated_decision_review.md)
contains the direct proof. This is a finite extension of the ordinary
essential-cell argument; the certificate companion in §19 does not
implement decision-only selection.

## 21. Comparison, contribution disposition and open obligations

The result is a conditional **yes** to Q5. Probability information can be
present in values whose payoff meaning and observation contract make it
recoverable. Arbitrary numerical usefulness estimates need not satisfy that
contract. Even within finite linear expectation, full-law recovery, a chosen
loss family, sharp compatible bounds and one action are different services.
The matrices, source restrictions, units, nuisance mechanism, permitted
queries and decoder requirements determine which is available.

### What is inherited, reconstructed, adapted or open

| Object | P3-02 disposition | Strong ordinary comparison and exact limit |
|---|---|---|
| Coherent expectation and known contingent losses | Inherited ordinary mathematics, directly reconstructed | A normalized positive linear functional determines a finite law. Ordinary expectation algebra already recovers known-stakes probabilities; cost notation creates no new induction theory. P02-S1/S2. |
| Finite targets, partial identification and retention | Reconstructed finite characterizations and phase-two adaptation | Fibers, row spaces, feasible endpoint pairs and LP dual certificates implement the same information service for an ordinary probability or credal method. Phase-two kernel, repair and compatible-center arguments remain inherited. PI-1–6, PI-10–13; P02-S1/S5/I1. |
| Proper scores, optimized reports and useful smaller properties | Reconstructed comparisons, with a proved finite score-span lemma and explicit calibration cases | Ordinary scoring and property elicitation may target `Cp` or a conditional property directly. Finite risk queries, a full risk function, an optimizer, estimated risks and realized scores are different inputs. No learning guarantee follows from propriety. PI-7/8/14; P02-S2–4/S6/S7. |
| One optimal action and permitted query design | Proved-in-fragment essential-action, calibration and repair refinements | The finite lower-envelope geometry, quotient dimensions and declared payoff menu specify the service. These ordinary methods can choose smaller task representations, signed contrasts or bounded queries too. They are not restricted to full-law recovery or naive inversion. PI-9/17/18. |
| Noisy recovery and affine baselines | Inherited framework, direct specialization and exact hostile examples | Ordinary optimal recovery supplies local/global radii; the scalar affine result follows from the theorem stated by Osipenko via homogenization. The sharp three-state noise radius already has a best ordinary affine implementation. No advantage over that stronger comparator is established. PI-13/15; P02-S9/S10/I1. |
| Ratios, payoff uncertainty and changes of units | Direct finite reconstructions and semantic obstructions | Ordinary fractional programming and compatibility projection reproduce the numerical conclusions. Shared versus independent stakes, actual joint errors, positive denominators and transformations before versus after expectation matter. PI-10/12/14/16; P02-S8. |
| Mapping into Value Logic and a reusable audit | Concrete finite formal adaptation and implementation candidate | Section 13 maps selected results to actual source identities, directed unit paths and rational native certificates. Section 19 implements a smaller full-simplex linear-target audit with exact decoder and collision certificates. The ordinary comparator may use that same implementation and proof interface. |
| Logical learning, model usefulness and counterfactual transport | Open prospective research | No bounded mathematical forecast learner, LI-like refinement theorem, model-plurality advantage, paid-acquisition improvement or identified counterfactual dependency model is established here. P3-A remains a separate unattempted gate. |

Source identifiers refer to the
[selected primary-source contracts](../literature/02_probability_sources.md).
The finite proofs in this note establish their stated conditional claims;
they do not establish worldwide priority. Some combined statements and
counterexamples are newly written for this project, but an exact numbered
antecedent not appearing in the selected reading is not evidence of novelty.
Conversely, ordinary mathematical ingredients do not by themselves rule out
a useful project-specific adaptation.

### Narrow candidate: a finite information audit for Value Logic

| Required contribution field | Current concrete content |
|---|---|
| Object | A declared-input audit connecting retained loss information to a specified probability, target-loss, interval or decision service, with an explicit interpretation route. |
| Type | Candidate modest formal adaptation and useful synthesis/implementation. No original-theorem requirement or exclusive capability is presumed. |
| Exact delta under consideration | The assembled source/payoff/calibration/service contract; the scoped identification and repair cases; the worked mapping into the existing proof interface; and a reusable exact certificate companion for a strictly smaller linear-target fragment. This is more concrete than renaming probabilities or listing ingredients. |
| Magnitude | Finite conditional scope. The implemented companion handles rational full-simplex linear targets under four exact shared calibration contracts. It does not implement the whole derivation, statistical learning, general logical uncertainty or arbitrary value representations. |
| Evidence | Direct proofs, explicit separating laws, sharp endpoint and dual constructions, selected primary-source comparison, native certificate cases, saved deterministic development results and internal same-model hostile reviews. No blind challenge or independent replication is claimed. |
| Named comparison scope | The combined ordinary finite-probability/credal, expectation, scoring, LP/fractional-programming and optimal-recovery methods, given the same information, admissible queries, resources and proof tools. No numerical capability or resource advantage over that combination has been shown. |
| Disposition | A concrete narrower candidate is available for assessment at the separate gate. Its usefulness and contribution delta must be evaluated under that scope; task completion and tested arithmetic do not supply a gate pass. |

**P3-N01 remains NOT YET SUPPORTED.** Its broader target links logical
forecasts, paid computation and justified revision; the present finite audit
does not establish that phase-wide contribution. This status does not erase
the conditional mathematics or preempt every modest synthesis/application
candidate. It preserves the distinction between completing P3-02 and
supporting a contribution.

### What remains outside the established result

The source or error model must still be justified for an application. Exact
compatibility is not calibration or truth; a selected compatible law is not
permission to discard the rest of a warranted source. Finite-sample evidence
needs an explicit sampling or error contract, and bounded logical uncertainty
does not become iid by changing terminology.

Information counts do not pay for computing semantic losses, finding an
essential action set, acquiring a new query, representing exact reals,
checking a source or solving an optimization problem. Restricted sources,
finite query alphabets and actual budgets can change the feasible service.
Known rational row operations are compatible with a finite algebraic audit;
arbitrary uncertain products, nonlinear score optimization and variable
normalization need their own implementation or certified enclosure.

Finally, a recovered observational law does not identify counterfactual
dependencies. Preserving the numerical answer under a unit change does not
alone preserve positions, access, fees or operations in an exploitation or
paid-computation criterion. Those P3-01 obligations remain intact. The
recommended next scheduled item is the separate **P3-A** gate after this
task's final records and protected minimum are satisfied; this note neither
attempts it nor starts P3-03.
