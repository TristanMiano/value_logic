# Checked source ambiguity floors for acquisition

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**

This validates the principal's proposed adversarial-mixture screen and
its deterministic lattice strengthening. The principal owns the new
implementation and read-only probe. This note performs no acquisition,
stream rerun or modification of earlier evidence and adds no principal
research-clock credit.

The screen can prove that further logical evidence alone cannot close a
fixed-source request at its tolerance. It does not prove that observing
costs immediately is the cheapest complete schedule.

## 1. A mixture lower bound with checked ingredients

Fix the original nonempty feasible repair set F, its ordered violation
features, and a known replacement price $`p\geq0`$. The action set
contains **every** feasible fixed repair and replacement. Define:

```math
C^*(w)=\min_{z\in F}w^\top z,
\qquad
V(w)=\min\{p,C^*(w)\},
\qquad
R^*(W)=\min_a\sup_{w\in W}\{c(a,w)-V(w)\}.
```

Let $`w_s\in W`$ be compatible source scenarios and choose
$`\lambda_s\geq0`$ with $`\sum_s\lambda_s=1`$. Set
$`\bar w=\sum_s\lambda_s w_s`$. Suppose independently checked
evidence gives:

```math
L_{\rm bar}\leq V(\bar w),
\qquad
U_s\geq V(w_s).
```

Then:

```math
R^*(W)\geq
B_{\rm mix}:=
\max\left\{0,L_{\rm bar}-\sum_s\lambda_s U_s\right\}.
```

For every fixed action a, its worst regret is at least its weighted
average over the selected scenarios. Repair costs are linear in w;
replacement is the constant affine cost p. Therefore:

```math
\sup_{w\in W}\{c(a,w)-V(w)\}
\geq c(a,\bar w)-\sum_s\lambda_s V(w_s)
\geq L_{\rm bar}-\sum_s\lambda_s U_s.
```

The lower bound applies to every action, so minimize over them and add
the valid zero floor. The same argument applies to randomized repairs
evaluated by expected action cost, because averaging their affine cost
functions preserves the inequality.

The coefficients lambda specify an adversarial mixture used to prove a
lower bound. They are not learned probabilities, a posterior, or a
runtime model. With exact optima, the expression is the concavity
gap of V under that mixture. This is an ordinary minimax dual/Jensen-gap
construction; no originality claim is made.

The mean need not be an actual discrete cost-source configuration.
Only the endpoint scenarios must be compatible with W. The mean
objective is a legitimate separately priced logical query under the
same immutable hard source, and its checked lower participates in the
algebra above.

## 2. Obtaining the numbers without free optimum labels

A checked feasible repair at scenario s with cost $`K_s`$ supplies
$`U_s=\min(p,K_s)`$. Different scenarios may use different
retained feasible repairs. Replacement alone supplies the weaker upper
p. A native optimum label, an unverified model or a lower bound cannot
be substituted for this feasible upper.

A checked repair lower $`L_q\leq C^*(q)`$ at the mean gives
$`L_{\rm bar}=\min(p,L_q)`$. For two integer scenarios a and b
with equal coefficients, use homogeneity of the **repair optimum**:

```math
C^*((a+b)/2)=C^*(a+b)/2.
```

Thus a raw checked lower $`L_{\rm sum}\leq C^*(a+b)`$ gives:

```math
L_{\rm bar}=\min(p,L_{\rm sum}/2),
\qquad
B_{\rm mix}=
\max\{0,\min(p,L_{\rm sum}/2)-(U_a+U_b)/2\}.
```

Clip **after** scaling the repair bound. The function V is not
homogeneous when the replacement price remains fixed:
$`\min(p,L_{\rm sum})/2`$ is a different quantity and can
needlessly weaken the screen. More general rational mixtures use the
same rule: form an integral objective with a verified common scaling
factor, divide its raw repair lower by that factor, and then compare
with the original p.

Each scenario must have a reconstruction from the current original
mode sets and observations. An unattainable coordinate-box corner is
not an adversary for the smaller correlated source. Source identities,
ordered logical features, current assumptions and audit dependencies
must match. A receipt hash binds bytes; it does not establish the truth
of an external observation channel.

## 3. What a positive floor means for acquisition

If $`B_{\rm mix}>\tau`$, even the best action selected with
complete logical knowledge has worst-source regret above the requested
tolerance. Adding witnesses or logical proofs while leaving the same
compatible scenarios and action meanings intact cannot close the
request. This includes revealing valid source-global equalities:
they strengthen knowledge of the same feasible set rather than change it.

Consequently, no closing audit leaf may retain all the scenarios used
in that positive floor. For a two-scenario floor, its actual observation
path must distinguish those source realizations. This can identify
cost distinctions that a useful audit needs to address. It does not
choose the cheapest set or ordering of such observations.

A floor at or below tolerance is inconclusive. The true ambiguity may
be larger, or the current certificate may merely be too weak. Logical
work may also be valuable before an eventually necessary audit: one
proof can prepare several observation branches or be cheaper at a
shared objective. The screen therefore supplies a reason to avoid
logically impossible immediate closure attempts, not a dominance
theorem for audit-first scheduling.

Changing the hard source, feature meanings, available actions, external
replacement price or admitted cost-source model changes the problem.
An old floor is not automatically valid after such a revision.
Model-dependent scope changes are not a way to close the original
immutable-source request.

## 4. A stronger floor for deterministic repairs with integer costs

For the two-scenario case, suppose a and b have nonnegative integer
coordinates and p is an exact nonnegative rational with denominator D.
Let $`g_a`$ and $`g_b`$ be the gcds of their coefficients.
A zero objective has gcd zero and contributes cost zero below.

Take any **pure fixed repair** whose maximum regret at the two
scenarios is r. Since $`V(a)\leq U_a`$ and
$`V(b)\leq U_b`$, its two costs obey:

```math
a^\top z\leq
g_a\left\lfloor\frac{U_a+r}{g_a}\right\rfloor,
\qquad
b^\top z\leq
g_b\left\lfloor\frac{U_b+r}{g_b}\right\rfloor.
```

Interpret a zero-gcd contribution as zero, without division. The same
repair also satisfies $`(a+b)^\top z\geq L_{\rm sum}`$.
Thus the sum of the two rounded upper bounds must reach
$`L_{\rm sum}`$.

At these integer scenarios, the maximum regret of a pure repair lies
on the grid $`\{t/D:t\in\mathbb Z_{\geq0}\}`$.
Define:

```math
r_R=
\min\left\{\frac tD:
t\in\mathbb Z_{\geq0},\quad
g_a\left\lfloor\frac{U_a+t/D}{g_a}\right\rfloor+
g_b\left\lfloor\frac{U_b+t/D}{g_b}\right\rfloor
\geq L_{\rm sum}\right\}.
```

Every pure repair has worst regret at least $`r_R`$. This is a
necessary lattice condition, not a claim that an attaining feasible
repair exists. For replacement, a separate lower bound is:

```math
r_P=\max\{0,p-\min(U_a,U_b)\}.
```

The full deterministic-action floor is therefore:

```math
R^*(W)\geq B_{\rm lattice}:=\min(r_R,r_P).
```

The minimum across the repair and replacement branches is essential.
The raw sum lower must remain unclipped in the repair condition; the
separate replacement branch handles the outside option. The arguments
only require the two selected scenarios to be integer objectives.

For the same proof and witnesses, this bound is at least the simple
half-mixture bound. Rounding implies:

```math
r_R\geq\max(0,L_{\rm sum}/2-(U_a+U_b)/2),
\qquad
r_P\geq\max(0,p-(U_a+U_b)/2).
```

Taking their minimum gives at least $`B_{\rm mix}`$. The
additional arithmetic can still cost more than the practical value of
that tightening.

### Exact calculation and a critical limitation

Use integer t and exact rationals. When the witnessed clipped uppers
have denominator dividing D, the first rounded term is:

```math
g_a\left\lfloor
\frac{D U_a+t}{Dg_a}\right\rfloor.
```

The necessary condition is monotone in t, so integer bisection suffices.
A finite upper search limit is
$`D\max(\sum_j a_j,\sum_j b_j)`$ for a nonempty feasible
Boolean source: every repair costs no more than that unscaled
maximum at the two scenarios. Charge gcds, exact arithmetic,
bisection, scenario construction and receipt checking. If both
objectives are zero, a valid raw sum lower cannot be positive.

**This lattice strengthening does not apply to expected-cost randomized
repairs.** Their scenario costs need not lie on either pure-repair
lattice. The mixture floor remains valid for that larger action class;
the strengthened screen is scoped to the fixed deterministic repair
or replacement contract.

## 5. Opposing costs show both the gain and the scope

For hard source $`z_1\lor z_2`$, choose integer
$`H>0`$ and scenarios:

```math
a=(0,H),\qquad b=(H,0).
```

Checked opposite feasible repairs give $`U_a=U_b=0`$.
A paid sum-objective proof at $`a+b=(H,H)`$ can establish
$`L_{\rm sum}=H`$. The mixture floor is
$`\min(p,H/2)`$.

Both objective gcds equal H. The repair condition is
$`2H\lfloor r/H\rfloor\geq H`$, whose first admissible
regret is H. Replacement's floor is p. Therefore:

```math
B_{\rm lattice}=\min(H,p).
```

This equals the actual deterministic minimax regret: either fixed
single-violation repair loses H in one endpoint, the both-violation
repair loses H in both, and replacement loses p. The 50/50 randomized
mixture of the two single-violation repairs instead has endpoint
expected regret H/2, illustrating exactly why the lattice extension
needs its deterministic-action restriction.

The construction reuses the same admitted proof and endpoint witnesses;
computing its strengthening adds no logical evidence acquisition.
That statement concerns the mathematics. Any actual probe must record
its own arithmetic/checking invoice and must not retroactively treat
this read-only screen as a change to an already executed controller.
