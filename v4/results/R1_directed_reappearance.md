# R1.15 Directed reappearance: useful concepts can require a joint refinement

**Author:** Codex (GPT-6), November 11, 2026. **Cycle:**
[P4-R1-C001, S6](../notebook/P4-R1-C001/record.md).
**Theses:** C1/C2, with a conditional grounding connection to C3.
**Evidence:** a finite proof, exact kernel checks and population ODE checks
by one model. This is an extension and interpretive synthesis, not an
independently confirmed new theorem from the literature.

The author's reappearance reading includes ordered events: seeing one thing
can make another likely next without the reverse being equally likely.
Predictively adequate concepts still exist in that setting, and the coupled
selection theorem survives a directed recurrence law. The important change
is that a useful concept may require several distinctions together. A rule
that accepts only immediately rewarding binary splits can miss it. Joint
proposals, neutral exploratory splits, or explicitly different labels for
current and future roles provide constructive responses.

## 1. The sufficient common concept for an ordered pair

Let X,Y take values in a finite alphabet W, with positive marginals mu,nu.
The joint density relative to their product law is

```math
F_{xy}=\frac{P(X=x,Y=y)}{\mu_x\nu_y}.
```

No conditional-i.i.d. latent state, symmetry, or positive-semidefinite Gram
representation is assumed. For a common conceptualisation c, let Pi_c be
conditional expectation under mu x nu given (c(x),c(y)), and let
I(c)=I(c(X);c(Y)). Two symbols are row twins if their F-rows coincide and
column twins if their F-columns coincide. Let c^dagger be the common
refinement of those two equivalence relations.

**Theorem 32 (directed sufficient concepts).** I is monotone under refinement,
and

```math
I(X;Y)-I(c(X);c(Y))
=\sum_{x,y}\mu_x\nu_y F_{xy}
       \log\frac{F_{xy}}{(\Pi_cF)_{xy}}\ge0.                 \tag{32.1}
```

Equality holds exactly when Pi_c F=F, equivalently when c refines
c^dagger. Terms of zero joint mass are zero. A positive joint entry cannot
have a zero block average, so the expression is well defined.

*Proof.* The coarse pair density is the block average Pi_c F. Subtracting
its information from the fine information gives (32.1), the relative
entropy between the true joint law and the law whose density is Pi_c F.
Its equality condition is equality of the laws. Block constancy is
equivalent to constancy of both rows and columns within every common cell:
block constancy gives both; their conjunction compares any two entries in
the same block. Monotonicity follows either by data processing or by applying
the same argument to a nested pair of partitions. QED.

If the current and next role are allowed different conceptualisations c,d,
the same proof says that full information is retained exactly when c
separates the row twins and d separates the column twins. Requiring one
shared vocabulary uses their common refinement. These are different typed
representation choices, rather than different names for one partition.

Under R1.6's shared-likelihood Gram assumption, row and column twins agree
with equally diagnostic observations, recovering Theorem 13(b). In an
arbitrary ordered process, c^dagger describes the joint recurrence law; it
does not identify an unobserved persistent state's sufficient statistic.

## 2. The coupled dynamics do not require reversibility

**Corollary 32A (directed population grounding).** In R1.9 replace symmetric
admissible densities by nonnegative matrices satisfying both

```math
\sum_y\mu_yR_{xy}=1,\qquad \sum_x\mu_xR_{xy}=1.             \tag{32.2}
```

Keep its fixed positive environmental share, finite catalogue including the
fine concept with positive initial weight, bounded positive calibration
rates, common mu-weighted score, and common reference experiment. Then all
conclusions of Theorem 18 hold: forecasts approach Pi_c F, the aggregate
approaches F, and insufficient concepts lose influence. The coarsest
sufficient common concept is c^dagger from Theorem 32 with nu=mu.

*Proof.* Matrices satisfying (32.2) form a compact convex set, and block
conditional expectation preserves both normalizations and nonnegativity.
It is still an orthogonal projection. Inspecting Theorem 18's proof, the
potential derivative, calibration contraction, fine-model advantage,
projection residual and final weight-ratio arguments use precisely those
properties; no step uses R=R^T. The same potential therefore proves the
same convergence. Theorem 32 identifies the limiting quotient. QED.

The score is evaluated with current contexts distributed according to the
fixed mu. Fresh reference contexts implement this population experiment.
A deterministic sequence of transition laws all preserving mu also preserves
that marginal when started at mu. An arbitrary adaptive single-chain learner
can correlate its chosen law with its current state; matrix stationarity
alone then does not establish that its sampled contexts have law mu. No
finite-data Markov adaptation theorem is smuggled into this corollary.

## 3. A purely temporal distinction and two useful repairs

**Proposition 33 (binary-refinement plateau).** On three symbols with
uniform mu, let

```math
K=\begin{pmatrix}0&1&-1\\-1&0&1\\1&-1&0\end{pmatrix},
\qquad F=\mathbf 1+aK,\qquad 0<|a|<1.                       \tag{33.1}
```

This is a positive directed stationary recurrence law. Its full information is

```math
I(X;Y)=\frac{(1+a)\log(1+a)+(1-a)\log(1-a)}{3}>0.          \tag{33.2}
```

Every common two-cell conceptualisation has Pi_c F=1 and I(c)=0. Thus no
single binary split of the one-cell vocabulary earns information, while
the three-way refinement earns (33.2). The strict single-split criterion
of R1.6 Theorem 13(c) does not extend to this ordered world without its
Gram assumption.

*Proof.* K is skew-symmetric and has zero row and column sums, establishing
normalization. For any block A, the sum of K over A x A is zero by
skew-symmetry. Its sum over A x A^c is also zero by the row-sum condition;
the remaining two block sums vanish likewise. This proves the two-cell
claim. There are three entries each of densities 1,1+a,1-a, which gives
(33.2). Their rows and columns are distinct, so the three-way concept is
the sufficient one. QED.

The limiting example is positive and has a direct interpretation: a
preferred direction of recurrence around a cycle. It is not an impossible
probability table or an effect of zero-probability events. The separation
also has a robust quantitative form. Put v=(1,-1,0), S=vv^T and replace F
by 1+aK+delta S, with 0<delta<a and a+delta<1. For every common binary c,

```math
I(c)\le\delta^2\|\Pi_cS\|_\mu^2\le\tfrac49\delta^2,
\qquad I(X;Y)\ge\tfrac29 a^2.                              \tag{33.4}
```

The upper bound uses relative entropy at most chi-squared divergence and
the contraction of projection; the K part projects to zero. For the lower
bound, the bounded test function K has expectation 2a/3 under the joint
law and zero under mu x mu, so their total variation is at least a/3.
Pinsker gives (33.4). Thus the joint proposal can remain materially useful
when every binary split has a small nonzero gain.

**Joint proposal.** Add the three-way concept with positive weight to a
catalogue that previously contained only one- and two-cell concepts.
Corollary 32A applies from that moment. In the one-parameter cycle family,
write its forecast as 1+bK and its weight as w. Against the uniform coarse
forecast, the equations reduce to

```math
q=ea+(1-e)wb,\qquad
\dot b=\eta(q-b),\qquad
\dot w=\tfrac23w(1-w)(2bq-b^2).                             \tag{33.3}
```

With positive e,eta,w(0), the new concept converges to the environmental
law. The two-cell models alone, initialized at their uniform projections,
stay uniform. A catalogue-generation policy may therefore need to evaluate
a compound proposal before it has a locally profitable first split.
Allowing a zero-gain first split and then the positive second split also
repairs this three-symbol example; its acquisition and complexity costs
still matter to a bounded agent.

**Role-specific partial concept.** Let the current-event label distinguish
symbol 1 from {2,3}, and the next-event label distinguish 2 from {1,3}.
The projected K on these two roles is

```math
\begin{pmatrix}1&-1/2\\-1/2&1/4\end{pmatrix},
```

with product cell masses (1,2;2,4)/9. It has positive information for
a!=0 even though every shared binary vocabulary has none. This is a
useful partial repair, not full recovery of all three-symbol structure.
Typing the roles can expose a promising intermediate representation that
an insistence on one immediate binary vocabulary hides.

## 4. Evidence, comparisons and the remaining question

The relative-entropy decomposition is standard sufficiency/data processing.
[Shalizi and Crutchfield's predictive-state framework](https://arxiv.org/abs/cond-mat/9907176v2)
is the close enabling comparison for retaining predictive distinctions;
the current construction uses a finite ordered pair and an explicitly common
or role-specific vocabulary. It does not claim their infinite-history
results from a one-step calculation. Corollary 32A extends our specified
population selection model, not general strategic or evolutionary dynamics.

The substantive addition for W1 is the characterized temporal boundary and
its constructive response: judgment can select factual recurrence structure
without reversibility, but an ontology search restricted to individually
profitable binary refinements can fail. The right next question is how a
bounded reasoner proposes, funds and retains promising compound distinctions
before they earn immediate credit. A full-joint Markov estimator already
represents this cycle; it is a genuine conventional alternative. A method
using (33.3) under a different name is the same coupled learner.

The companion [directed_reappearance.py](../notebook/P4-R1-C001/directed_reappearance.py)
and its [output](../notebook/P4-R1-C001/directed_reappearance.json) check 20
cycle decompositions, 75 general role-projection identities, four robust
perturbations and two population birth trajectories. At a=0.6 the full
information is 0.12849650 nats; the role-specific binary labels retain
0.04402454 nats, while common binary labels retain zero. With a=0.6 and
delta=0.01, the strongest common binary label retains 0.00001249 nats,
against 0.12902094 for the full vocabulary. These checks and the proof are
by the same model. General finite-data learning
under an adaptively changing directed chain remains an explicit obligation.
