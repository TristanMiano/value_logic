# R1.10 Transfer recovery under skill-dependent task choice

**Author:** Codex (GPT-6), November 10, 2026. **Cycle:**
[P4-R1-C001, S6](../notebook/P4-R1-C001/record.md). **Theses:** C1, C2.
**Evidence:** reconstructed mathematical arguments and exact finite-world
checks by one model; independent expert review and a close theorem-level
novelty comparison remain open.

Good judgment can recover transfer distinctions even when performers choose
their tasks. Three past performances suffice to expose every merged pair
whose outcomes differ where both tasks can be attempted. The number three
is sharp: a strictly positive, partly randomized assignment model can hide
the distinction from judges with one or two past performances. Under finite
latent states, one past performance is nevertheless sufficient for almost
every assignment kernel, in the precise measure-theoretic sense below.

This resolves the unflagged-assignment question left in
[R1.1, Proposition 5](R1_recurrent_recovery.md#4-limits-with-repairs).
The repair preserves the original outcome-prediction question. It does not
replace that question with whole-observation mutual information.

## 1. Setting

A performer has persistent state theta with prior P. Conditional on theta,
performances are independent with joint task/outcome law

```math
g_{xy}(\theta)=q_x(\theta)f_x(y\mid\theta),\qquad
q_x=\sum_y g_{xy}.
```

Task types x and outcomes y lie in finite sets. Unlike A1 of R1.1, assignment
q may depend on theta. A delineation c labels every past task and the
target. Its optimal log score is

```math
V_n(c)=-H(Y_0\mid(c(X_s),Y_s)_{s=1}^n,c(X_0)).                 \tag{19.1}
```

The transfer partition bar z still groups tasks with identical outcome
kernels f_x(.|theta) almost everywhere. Without assignment support, a
counterfactual difference on tasks never jointly attempted need not be
observable. Say A,B are **jointly observable non-twins** when

```math
P\{q_Aq_B>0\text{ and }f_A(\cdot\mid\theta)
                         \ne f_B(\cdot\mid\theta)\}>0.         \tag{19.2}
```

Here A,B can be original types or portions of different twin classes in a
c-cell, with their assignment probabilities aggregated. Zero-probability
outcomes are allowed. If all task probabilities are positive almost surely,
every non-twin pair satisfies (19.2). A positive independent assignment
share, even when its flag is not observed, guarantees that support.

## 2. Three histories suffice

**Theorem 19 (recovery under selection).** If c merges jointly observable
non-twins, then for every n>=3,

```math
V_n(c,\bar z)>V_n(c).                                         \tag{19.3}
```

In particular, with positive assignment probabilities almost everywhere,
every optimal delineation for n>=3 refines bar z. Its refinements need not
all be optimal: finer assignment labels can still help infer skill at a
finite history length.

*Proof.* It is enough to work with the finite joint law of labels under
d=(c,bar z). Suppose the two scores tie. Strict propriety then makes the
d-forecast and the c-forecast equal on every positive-probability input.
First take n=3 and two d-labels A,B in one c-cell. Fix an outcome y and put

```math
D_y=g_{Ay}q_B-g_{By}q_A.
```

Let H be the product of the likelihoods of any two specified past
observations. Compare the two remaining history/target configurations:
last past observation (A,y) with target B, and last past observation (B,y)
with target A. They have the same coarse input. Their forecast numerators
for target outcome y are the same:

```math
N_H=\mathbb E[H g_{Ay}g_{By}],
```

and their denominators are

```math
d_1=\mathbb E[H g_{Ay}q_B],\qquad
d_2=\mathbb E[H g_{By}q_A].
```

If N_H>0, both events are possible, and equality of their forecasts
N_H/d_1=N_H/d_2 forces d_1=d_2. If N_H=0 but d_1>0, compare the first
event instead with the same history and target A. Its numerator
E[H g_Ay^2] is positive, whereas the target-B numerator is zero; this
contradicts equality of fine forecasts with their common coarse forecast.
Thus d_1=0 in this case, and symmetrically d_2=0. Consequently, in all cases,

```math
\mathbb E[H D_y]=0.                                           \tag{19.4}
```

But D_y is a linear combination of exactly such two-observation products:

```math
D_y=\sum_v(g_{Ay}g_{Bv}-g_{By}g_{Av}).
```

Multiply by D_y, take expectations, and apply (19.4) term by term.
E[D_y^2]=0. For every y this gives q_A q_B(f_A(y)-f_B(y))=0 almost surely,
contradicting (19.2). For n>3, fix the remaining n-3 fine history positions,
use their posterior as the prior in this argument, and average those
posteriors back to P. QED.

This proof handles missing outcome support directly. It does not assume
that every possible result has positive probability, and it does not assume
the learner can observe whether a task was randomly assigned.

## 3. The threshold is sharp, while one history is generically enough

**Proposition 20 (sharp example and generic behavior).**

**(a)** There is a strictly positive joint task/outcome model, containing an
unflagged independent assignment share of 5/8, with distinct transfer
profiles but V_n(fine)=V_n(coarse) for n=0,1,2. Thus Theorem 19's uniform
threshold cannot be lowered to two past performances.

**(b)** Fix a finite latent-state space with positive prior masses and fixed
outcome kernels. Among strictly positive assignment kernels, outside a set
of Lebesgue measure zero, every delineation merging non-twins already has
V_1(c,bar z)>V_1(c).

*Proof of (a).* Let S,T be independent fair signs. Independently let R equal
1/2 with probability 5/8 and 3/2 with probability 3/8, so E[R^2]=1. Set

```math
u=SR/4,\quad v=TR/4,\quad w=ST/16,
\qquad
g_{xy}=\frac{1+xu+yv+xyw}{4},\quad x,y\in\{-1,+1\}.             \tag{20.1}
```

Every g_xy is positive. The task probability q_x=(1+xu)/2 is at least
5/16, so q is a mixture of uniform assignment of weight 5/8 and another
valid assignment rule. The conditional outcome means are
(v+xw)/(1+xu); they agree for both tasks only if w=uv, which fails when
R is either 1/2 or 3/2.

Nevertheless, all moments of (u,v,w) of total degree at most three match
the model u=S/4, v=T/4, w=uv. To verify this, the nonzero moments apart
from the constant are

```math
\mathbb E u^2=\mathbb E v^2=1/16,\qquad
\mathbb E w^2=\mathbb E uvw=1/256;
```

all other moments of positive degree at most three vanish by the signs.
In the comparison model, task and outcome sequences are independent.
The joint law of at most three performances is a polynomial in these
moments. It is therefore identical in the two models, and task labels
cannot improve outcome prediction from at most two past performances.
Theorem 19 makes the gain strict at three. QED.

*Proof of (b).* With finite state, equality of fine and coarse one-history
forecasts can be written as finitely many polynomial equations in the
assignment probabilities, by cross-multiplying their joint probabilities.
For a fixed non-refining c these equations do not hold identically: at any
strictly positive assignment independent of skill, R1.1, Theorem 1 gives a
strict gap. The equality set is thus contained in the zero set of a
nonzero polynomial and has measure zero in the product of task simplices.
There are only finitely many delineations. Take the finite union of these
exceptional sets. QED.

The exceptional example is fully positive and scientifically relevant to a
uniform guarantee. It is not evidence that ordinary randomly chosen worlds
usually need three histories. The generic result explains why earlier
random checks often saw recovery at the first reappearance.

## 4. What long histories recover, with an explicit limit bound

**Theorem 21 (limiting transfer recovery).** Let every q_x be positive
almost surely. For a c-cell K define

```math
q_K=\sum_{x\in K}q_x,\qquad
\bar f_K=\sum_{x\in K}\frac{q_x}{q_K}f_x.
```

Then

```math
\lim_n V_n(c)=-\mathbb E\sum_K q_K H(\bar f_K),
```

and the limiting deficit relative to the full type label is

```math
\Delta_\infty(c)
=\mathbb E\sum_K\sum_{x\in K}q_x\,
       \mathrm{KL}(f_x\|\bar f_K).                             \tag{21.1}
```

For A,B in one cell,

```math
\Delta_\infty(c)\ge\frac12\mathbb E\left[
 \frac{q_Aq_B}{q_A+q_B}\|f_A-f_B\|_1^2\right].                 \tag{21.2}
```

If q_x >= epsilon q^0_x for a fixed positive assignment q^0, this is at least

```math
\frac{\epsilon}{2}\frac{q^0_Aq^0_B}{q^0_A+q^0_B}
                 \mathbb E\|f_A-f_B\|_1^2.                   \tag{21.3}
```

*Proof.* Conditional independence makes the infinite labeled history
identify its joint cell/outcome probabilities by empirical frequencies.
Those probabilities identify q_K and bar f_K. Conditional predictive
probabilities converge to this law by bounded martingale convergence;
entropy is bounded and continuous on the finite outcome simplex. This
gives the limit. The entropy chain rule gives (21.1). Keep A and B in
that sum and apply weighted Pinsker and the triangle inequality to their
common cell predictor, obtaining (21.2). The function ab/(a+b) is
increasing in each positive argument and homogeneous of degree one, giving
(21.3). QED.

At infinite history, refinements of bar z all attain the full-label value:
each cell's outcome law is already its twin-class law. Thus the limiting
optima are exactly the refinements of bar z, even though finite-history
optima can exploit additional information in assignment labels. The theorem
does not provide a finite-sample algorithm for an unknown latent model.

## 5. Exact checks and contribution scope

[unflagged_assignment.py](../notebook/P4-R1-C001/unflagged_assignment.py)
enumerates ordered histories with rational probabilities and 50-digit
decimal logarithms. Its [output](../notebook/P4-R1-C001/unflagged_assignment.json)
records the sharp example and a second construction whose first strict gap
occurs at two past performances. For the latter:

| Past performances | Fine-label score gain, nats |
|---:|---:|
| 0 | 0 |
| 1 | 0 |
| 2 | 0.0001858332 |
| 3 | 0.0006545620 |
| 5 | 0.0019867423 |
| Infinite-history formula | 0.0148592896 |

Its weighted lower bound (21.2) is 1/75 and the assignment-only bound
(21.3) is 2/225. Revealing the assignment flags restores a positive
one-history gain, 0.0001787389 nats. Further exact checks retain zero
unflagged one-history gain at assignment shares 0.9, 0.99 and 0.999.
The sharp example has gains 0, 0 and 0 at n=0,1,2, followed by
0.0000218450 at n=3 and 0.0001466543 at n=5. The checker establishes
the zero gaps by exact integer cross-products, as well as the moment proof;
decimal residuals are below 1e-44. A separate grid covers 2,025 two-state
rational worlds including zero assignment/outcome probabilities. All 1,296
jointly observable non-twin worlds have a strict gap by n=3. This finite
grid checks boundary cases; it does not establish the universal theorem.

The proof uses elementary nonnegative moment identities and sufficiency.
The candidate mathematical contribution is the specified sharp history
threshold for this restricted outcome-prediction game, together with its
generic and limiting interpretations. General mixture identification and
multi-view moment methods are stronger tools for other targets; this result
does not identify the latent states or estimate their full distribution.
[Vandermeulen and Scott](https://arxiv.org/abs/1607.00071v2), Theorems
4.1--4.6, identify full finite mixtures from grouped observations: 2m-1
observations suffice among mixtures of at most m components, while linear
independence allows three. Those targets recover the latent mixture, with
different assumptions. Theorem 19 instead proves a strict predictive-value
gain from four observations (three history plus target), independently of
the number of latent states. It does not improve their full-identification
thresholds. A close search for an existing version of this particular
predictive-value threshold remains open.

## 6. A finite-evidence construction without latent-state recovery

There is also an observable route to the transfer distinction. Draw
independent performer episodes, each containing four conditionally i.i.d.
performances as above. The learner receives only their task and result
labels, not theta, its distribution, or the assignment probabilities.
For a pair A,B let e_y denote an outcome unit vector and define

```math
S_{ij}=\tfrac12\bigl(1\{X_i=A,X_j=B\}-1\{X_i=B,X_j=A\}\bigr)
                         (e_{Y_i}-e_{Y_j}),
\qquad
K_{AB}=\frac{\langle S_{12},S_{34}\rangle+
                  \langle S_{13},S_{24}\rangle+
                  \langle S_{14},S_{23}\rangle}{3}.             \tag{22.1}
```

**Proposition 22 (observed transfer evidence).** For every pair,

```math
\mathbb E K_{AB}
=d_{AB}:=\mathbb E\bigl[q_A^2q_B^2\|f_A-f_B\|_2^2\bigr],
\qquad -1/6\le K_{AB}\le1/3.                                 \tag{22.2}
```

Thus d_AB>0 exactly for jointly observable non-twins. With positive task
support, these population statistics identify the transfer partition.
Given m pairs and n independent episodes, let the empirical means be
hat d_AB. Applying the bounded-observation confidence sequence used in
[R1.11](R1_finite_reappearance.md) with rho=1/16 and failure probability
alpha/m gives, jointly over all n and pairs with probability at least
1-alpha,

```math
|\widehat d_{AB}-d_{AB}|\le r_n,
\qquad
r_n=\frac{\sqrt{(n+1)\log((n+1)m^2/\alpha^2)}}{4n}.             \tag{22.3}
```

Each lower bound above zero certifies a real distinction. If every nonzero
d_AB is at least a specified d_min, then at any n with 2r_n<d_min,
thresholding at r_n identifies all twin pairs on that same event. This
is a finite-sample recovery construction with stated separation, rather than
an oracle Bayesian forecaster. Without a separation promise, the partial
certificates remain valid and every fixed non-twin pair is eventually
detected, but the learner cannot declare that all remaining pairs are
exact twins merely because the current evidence is small.

*Proof.* Conditional on theta, E S_ij is the vector
q_A q_B(f_A-f_B). The two disjoint pairs in each summand are conditionally
independent, giving the expectation. Only an episode with two A and two B
tasks can contribute. Write its outcome vectors as a1,a2,b1,b2. Then K is
[2<a1,a2>+2<b1,b2>-<a1+a2,b1+b2>]/12. Checking the possible equality
patterns of four categorical outcomes gives the stated range. The range
has length 1/2, so its centered observations have sub-Gaussian variance
proxy 1/16; normal mixing and a union bound give (22.3). The separation
conclusion follows from hat d<=r_n for twins and hat d>r_n for non-twins
when 2r_n<d_min. QED.

For two task types, (22.1) is exactly the unbiased HSIC kernel with task
feature 1{X=A} and the categorical outcome kernel, as in
[Song et al. (2012), Theorem 3, equation 11](https://jmlr.org/papers/v13/song12a.html).
The statistic is established machinery. Its use here witnesses a transfer
distinction inside each unobserved performer state before the latent mixture
has been identified. [transfer_witness.py](../notebook/P4-R1-C001/transfer_witness.py)
compares both kernels exactly on 4,096 categorical patterns and verifies the
expectations in the sharp and two-history worlds. The
[output](../notebook/P4-R1-C001/transfer_witness.json) gives respectively
d=15/32768 and d=1/400.

An observed-data implementation,
[learn_transfer.py](../notebook/P4-R1-C001/learn_transfer.py), uses four task
types and two hidden performer states. In the first state, assignment is
(0.3,0.2,0.2,0.3); in the second it is (0.2,0.3,0.3,0.2). The states
are equally likely. Types 0,1 share success profiles (0.9,0.1), while 2,3
share (0.1,0.9). Their true transfer classes are therefore {0,1} and {2,3}.
Yet their marginal observed success rates are (0.58,0.42,0.58,0.42):
first-order success averages suggest the different grouping {0,2}/{1,3}.

The learner receives only grouped task/result arrays. It estimates every
pair statistic and uses confidence-compatible graph components as a
conservative partition; uncertain edges can delay refinement. Its
[saved run](../notebook/P4-R1-C001/learn_transfer.json) gives:

| Independent four-performance episodes | Certified non-twin pairs | Conservative partition |
|---:|---:|---|
| 1,000 | 0 of 4 | One class |
| 10,000 | 0 of 4 | One class |
| 100,000 | All 4 | {0,1}/{2,3} |
| 500,000 | All 4 | {0,1}/{2,3} |

The two within-class pairs are never certified distinct at these recorded
checkpoints. At 500,000 episodes, twice the simultaneous radius is below
the known evaluation separation 72/15625, meeting Proposition 22's
sufficient recovery condition. The estimator itself does not receive that
separation or hidden state. This simple robust construction has substantial
sample cost and no optimality claim. An equally informed implementation of
the same grouped dependence statistic is the same method; the comparison
with marginal success rates establishes an information distinction, not
exclusive power for an algorithm called recursive judgment.

This witness measures structural transfer information. It is not the
finite-history log-score gain, and a small witness does not by itself
certify that all extra assignment labels are useless for inferring skill.
Independent performer episodes are also different evidence from additional
attempts by one persistent performer. These distinctions keep the finite
construction compatible with the mathematical recovery target.
