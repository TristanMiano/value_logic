# R1.8 How much predictive value is lost by merging kinds?

**Author:** Codex (GPT-6), November 10, 2026. **Cycle:**
[P4-R1-C001, S6](../notebook/P4-R1-C001/record.md). **Theses:** C1, C2.
**Evidence:** mathematical derivations and independent finite-world checks.
The two bounds below extend R1.1 and R1.6; they have not received independent
expert or formal verification. All logarithms are natural.

The qualitative recovery theorems say that optimal judgment preserves every
predictively meaningful distinction. These bounds make that claim useful
before exact optimality: a nearly optimal judge cannot erase a distinction
whose frequency and predictive separation make its loss too expensive. The
results concern the best forecast a representation supports, not a promise
that a finite learner has already found that forecast.

## 1. A transfer bound for every positive history length

Use the setting of [R1.1](R1_recurrent_recovery.md). A performer has persistent
latent skill theta. Tasks are independently drawn from q, independently of
skill (A1). Given skill and task types, outcomes on different attempts are
independent (A2). There are finitely many types and outcomes. Types are twins
when their skill-dependent outcome laws agree almost everywhere; bar z is
their quotient. A delineation c supplies labels for n earlier attempts and
the target. Its best expected log score is

```math
V_n(c)=-H(Y_0\mid H_n^c,c_0).
```

**Theorem 16 (uniform-history separation bound).** Let one c-cell contain
portions of two distinct twin classes A and B with unconditional task
probabilities alpha and beta, both positive. Put

```math
k=\frac{\alpha\beta}{\alpha+\beta},\qquad
d_y=\mathbb E\bigl[(f_A(y\mid\theta)-f_B(y\mid\theta))^2\bigr].
```

For every integer n >= 1,

```math
V_n(\bar z)-V_n(c)\ \ge\ \frac{k^2}{2}\sum_y d_y^2.                 \tag{16.1}
```

This is the bound of R1.1, Theorem 2, with its restriction to n=1 removed.
It does not assert that the actual left side increases with n.

*Proof.* Let d=(c,bar z) be the common refinement. R1.1 gives
V_n(d)=V_n(bar z). Its full and coarse Bayes forecasts, M_d and M_c, obey

```math
V_n(d)-V_n(c)
=\mathbb E\,\mathrm{KL}(M_d\|M_c)
\ge\frac12\sum_y\mathbb E\bigl(M_d(y)-M_c(y)\bigr)^2.              \tag{16.2}
```

Condition on R, the fine labels and outcomes at history positions 2 through
n. Write P_R for the resulting skill posterior. Task assignment at position
1 and the target is still independent of R and skill. For each outcome y set

```math
D_A=\mathbb E[f_A(y\mid\theta)\mid R],\quad
D_B=\mathbb E[f_B(y\mid\theta)\mid R],\quad
N_{ab}=\mathbb E[f_a(y\mid\theta)f_b(y\mid\theta)\mid R].
```

Keep just the events on which the first outcome is y and both selected task
instances lie in the confused cell. The coarse forecast has a common value
on AA, AB, BA, BB, even after R is fixed. On positive-probability events the
fine forecasts are N_ab/D_a. Write
u=(N_AA-N_AB)/D_A and v=(N_BB-N_BA)/D_B; zero-denominator contributions are
zero. Minimizing a weighted squared error over any common reference value,
separately for AA/AB and BB/BA, gives a conditional contribution at least

```math
\frac{k}{2}\sum_y(\alpha D_Au^2+\beta D_Bv^2).
```

The common reference need not be the optimal forecast after R is revealed;
this observation avoids an unjustified exchange of conditioning and
optimization. The Gram identity gives

```math
D_Au+D_Bv
=\mathbb E[(f_A(y\mid\theta)-f_B(y\mid\theta))^2\mid R]=d_y(R).
```

Cauchy--Schwarz and D_A,D_B <= 1 imply

```math
d_y(R)^2
\le(\alpha D_Au^2+\beta D_Bv^2)
   \left(\frac{D_A}{\alpha}+\frac{D_B}{\beta}\right)
\le\frac{\alpha D_Au^2+\beta D_Bv^2}{k}.
```

Average over R, then use Jensen and the fact that the posterior laws P_R
average to the prior. This gives (16.1). QED.

The useful consequence survives nonmonotone gains from longer histories:
if a judge's score is within eta of V_n(bar z), its representation cannot
contain any merge whose right side exceeds eta. A small bound does not show
that a merge is harmless; it only fails to rule the merge out.

## 2. A sharp small-separation bound for diagnostic kinds

Use the setting of [R1.6](R1_reappearance.md). Two sightings W_1,W_2 are
independent conditional on persistent state theta, each with law L(.|theta)
on a finite alphabet. Discard zero-marginal observations and let
mu_w=E L(w|theta)>0. The diagnostic profile of an event set A is

```math
\ell_A(\theta)=\frac{L(A\mid\theta)}{\mu(A)}.
```

The conceptualisation c is applied to both sightings. Its best log-score
gain over its own unconditional baseline is I(c(W_1);c(W_2)). This explicit
baseline matters when different conceptualisations change the event being
predicted.

**Theorem 17 (diagnostic merge bound).** Let disjoint nonempty sets A and B
lie in one c-cell. Set alpha=mu(A), beta=mu(B), k=alpha beta/(alpha+beta), and

```math
d_{AB}=\mathbb E[(\ell_A-\ell_B)^2].
```

Then

```math
I(W_1;W_2)-I(c(W_1);c(W_2))\ \ge\ 2k^3d_{AB}^2.                 \tag{17.1}
```

The bound is asymptotically attained in the balanced binary family below.

*Proof.* Data processing and the chain rule give

```math
I(W_1;W_2)-I(c(W_1);c(W_2))
\ge I(W_1;W_2\mid c(W_1)).                                    \tag{17.2}
```

Let r_A and r_B be the laws of W_2 conditional on W_1 belonging to A and B.
Pool the terms for A and B in the conditional mutual information by convexity
of KL. Pinsker's inequality and a weighted triangle inequality show that,
for the common coarse-cell predictor r,

```math
\alpha\mathrm{KL}(r_A\|r)+\beta\mathrm{KL}(r_B\|r)
\ge\frac12\left(\alpha\|r_A-r\|_1^2+
                         \beta\|r_B-r\|_1^2\right)
\ge\frac{k}{2}\|r_A-r_B\|_1^2.                                \tag{17.3}
```

Put t=r_A-r_B. Conditional independence implies
t(v)=E[L(v|theta)(ell_A-ell_B)], so

```math
\frac{t(A)}{\alpha}-\frac{t(B)}{\beta}=d_{AB}.
```

The test function 1_A/alpha-1_B/beta has range 1/k and t has total mass zero.
Subtracting the midpoint of that range gives
d_AB <= ||t||_1/(2k). Substitution into (17.3) proves (17.1). QED.

**Sharpness example.** Let theta take two equiprobable values and W be
binary with marginal masses 1/2. In the two states let the normalized
likelihoods of A be 1+epsilon and 1-epsilon, with those of B interchanged.
For 0<epsilon<1 and the constant conceptualisation,

```math
d_{AB}=4\epsilon^2,\qquad 2k^3d_{AB}^2=\frac{\epsilon^4}{2},
```

while the exact information loss is

```math
\frac{(1+\epsilon^2)\log(1+\epsilon^2)
      +(1-\epsilon^2)\log(1-\epsilon^2)}2
=\frac{\epsilon^4}{2}+O(\epsilon^8).                            \tag{17.4}
```

Thus weak latent distinctions can have fourth-order predictive value. The
bound does not promise that finding them is cheap. It identifies the scale
at which an approximately optimal judge must preserve them, closing the
explicit-bound obligation in R1.6, Corollary 14.

## 3. What the two games share, and what they do not

Both use strictly proper prediction to evaluate conceptual distinctions.
They are not identical objectives. Under the independent task assignment of
R1.1, put W=(X,Y). Then

```math
I((c(X_1),Y_1);(c(X_2),Y_2))
=H(Y_2\mid c(X_2))+V_1(c).                                    \tag{17.5}
```

The entropy baseline on the right depends on c. In a world with no varying
skill, two equally common tasks with success probabilities 1/5 and 4/5
are independent across performances. All pairwise mutual informations in
(17.5) are zero, but preserving task identity improves V_1 by
0.1927447570 nats. It predicts task-specific difficulty. Retaining the
baseline and the target question makes the common proper-scoring explanation
precise without identifying scientifically different optimization problems.

## 4. Evidence, established ingredients and remaining work

The independent [audit_s6.py](../notebook/P4-R1-C001/audit_s6.py) uses rational
joint probabilities and 50-digit decimal logarithms. It enumerates ordered
histories, rather than importing the earlier multinomial implementation.
Its [saved output](../notebook/P4-R1-C001/audit_s6.json) records 44
uniform-history bound comparisons through n=5 and 660 diagnostic-bound
comparisons in 24 rational worlds. No violation occurred. In the balanced
binary sequence epsilon=1/2 through 1/64, actual loss divided by (17.1)
decreases from 1.010686 to 1.000000009934. These are small-model checks,
separate from the arguments above.

The proof ingredients are classical sufficiency, strict propriety, the
chain rule, Pinsker's inequality and a Gram representation. The strongest
qualitative comparison is [Shalizi and Crutchfield's predictive-state
refinement lemma](https://arxiv.org/abs/cond-mat/9907176v2), whose statement
and proof were read during this review. These explicit bounds address the
particular restricted representations in R1.1 and R1.6. A theorem-level
novelty claim would require a closer comparison with quantitative
sufficiency and information-contraction results; none is made here.

The next practical step is a finite-data certificate for a useful distinction,
with its observation and computation costs made explicit. The bounds are
also relevant to deciding when further refinement is worth evaluating. They
do not establish that finite-sample optimal partitions form a nested sequence,
or that every factual distinction must be retained for every decision task.
