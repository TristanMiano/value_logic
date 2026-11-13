# R6.10 Credible value revision can create better opportunities

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** an elementary trust-game construction, a specified two-type
dynamic, analytic thresholds and numerical checks. This is a synthesis with
established commitment and preference-evolution mechanisms.

Changing what an agent will value later can improve what it can achieve now,
when others can recognize and rely on that change. A preference for returning
a benefit can become useful because it attracts trust. Depending on the
information environment, that preference can spread, coexist with a different
one, or lose its advantage. This adds a strategic mechanism to W6/C5's account
of values applied to values, distinct from local reward shaping.

## 1. A goal change that the previous goal can endorse

A trustor chooses Refuse or Invest. Refuse pays (1,0), with the trustor's
wealth first and the trustee's second. After Invest, the trustee chooses:

| Trustee's action | Trustor's wealth | Trustee's wealth |
| --- | ---: | ---: |
| Return | 2 | 1 |
| Grab | 0 | 3 |

Initially the trustee maximizes its own wealth. If its unchanged preferences
are known, the trustor anticipates Grab and refuses; the trustee receives zero.
Before this choice, suppose the trustee can pay cost k to install an observable
and credible downstream preference

```math
u_\lambda=\text{own wealth}+\lambda\,\text{partner wealth},
\qquad \lambda>1.                                      \tag{S.1}
```

This preference strictly chooses Return, since 1+2*lambda>3. The trustor
then invests. Evaluated by the trustee's *previous* wealth objective, the
change yields 1-k rather than zero. Thus for k<1 the previous objective
strictly favors installing the different downstream objective.

The commitment must remain effective until the promised action. A trustee
that can secretly restore Grab after investment would not support this
reasoning if the trustor anticipates the restoration. A verifiable restriction
of the trustee's future action set to Return can achieve the same outcome
while preserving the original utility. That is a distinct commitment
implementation with potentially different costs, not proof that the utility
change and the action restriction are identical mechanisms.

This is a literal change in preferences over the two complete outcomes,
unlike [R6.6's potential transformation](R6_bounded_subgoals.md), which
preserves complete-trajectory rewards. The explanation is a changed social
opportunity, not an unexplained attraction to changing goals.

The optimal self-modification theorem in
[Everitt et al. (2016), technical-report theorem 16](https://arxiv.org/abs/1605.03142)
assumes modification-independent beliefs and utility, as well as an initially
optimal realistic agent. Here the opponent observes the actual installed
preference and responds to it. Replacing the continuation while keeping a
misleading appearance of commitment is not an allowed equivalent splice.
This is a constructive case outside that independence premise, not a
counterexample to the theorem.

## 2. Partial observability changes which values persist

Consider a population containing returning and grabbing dispositions. Let x
be the fraction that Return. A trustor sees the trustee's true disposition
with probability q, independently of its type. Otherwise it knows only x.
It invests in an observed returning type and refuses an observed grabbing
type. When unobserved, its expected investment payoff is 2*x, so an exact
wealth-maximizing response invests precisely when x>1/2; at the tie, either
action or a mixture is optimal.

Returning types pay a per-encounter maintenance cost k>=0. This is a declared
cost of sustaining the disposition or assurance, distinct from the one-time
installation cost in section 1. Let z be the investment probability when
the type is unobserved. Material payoffs are

```math
f_R=q+(1-q)z-k,\qquad f_G=3(1-q)z,
\qquad D(x)=f_R-f_G=q-k-2(1-q)z.                        \tag{S.2}
```

With exact best responses, z=0 below x=1/2 and z=1 above it. Therefore:

- If q>(2+k)/3, Return has positive material advantage on both sides, and
  also under every mixture at the tie. The threshold is feasible when k<1.
- If q<k, Return has negative advantage for every z.
- If k<q<(2+k)/3, Return is favored when rare but Grab is favored when
  Return is common enough to attract unobserved trust. At x=1/2, the
  indifference-compatible investment rate
  z_*=(q-k)/(2*(1-q)) equalizes material payoffs.

These signs already distinguish common adoption from persistent diversity.
They do not, by themselves, specify a convergence trajectory at the
discontinuous best-response threshold.

### A fully specified smooth dynamic

For an explicit bounded-response model, let the trustor instead use
z=sigma_tau(x)=1/(1+exp(-(2*x-1)/tau)), with tau>0. This is a stipulated
noisy choice rule, not an exact best response. Let the two dispositions change
in frequency according to the continuous replicator equation

```math
\dot x=x(1-x)\bigl[q-k-2(1-q)\sigma_\tau(x)\bigr].     \tag{S.3}
```

This models differential material retention of dispositions, not a trustee
deliberately maximizing population fitness. A common baseline can be added to
both material fitnesses without changing this equation.

**Proposition 1 (a mixed attractor under partial observability).** For q<1,
if D(0)>0>D(1), there is a unique interior equilibrium

```math
x_* =\frac12+\frac{\tau}{2}\log\frac{z_*}{1-z_*},
\qquad z_* =\frac{q-k}{2(1-q)},                         \tag{S.4}
```

and every initial x in (0,1) converges to it. If D(1)>0, every interior
trajectory converges to one; if D(0)<0, every interior trajectory converges
to zero.

*Proof.* D is strictly decreasing because sigma_tau is strictly increasing.
In the first case it has exactly one zero, given by inversion of the logistic
function. Below it the derivative in (S.3) is positive; above it the derivative
is negative. One-dimensional uniqueness and bounded monotone trajectories
give convergence. The constant-sign cases follow the same way. QED.

At tau=0.1, the checked cases (q,k)=(0.9,0.1), (0.5,0.1), and (0.1,0.2)
give, respectively, convergence toward Return, an interior equilibrium
x_*=0.479727, and convergence toward Grab. The middle case is a positive
construction of lasting heterogeneous values, rather than a failure to run
convergence long enough. Restricted two-type stability is not stability
against every possible new preference or signaling strategy.

## 3. Reliable judgment can make the commitment useful

Perfect recognition is a substantive informational assumption. Replace it by
a binary certificate with true-positive probability s for Return and
false-positive probability f for Grab. Suppose the trustor invests only after
a pass. Then the material difference is

```math
D_{\rm pass}=s-3f-k.                                    \tag{S.5}
```

With a known population x and Bayes-correct beliefs, pass-only investment is
indeed an optimal strict response when

```math
\frac{f}{s+f}<x<\frac{1-f}{2-s-f},                       \tag{S.6}
```

assuming the denominators are positive. The first inequality makes a pass
more likely to come from Return than Grab; the second makes that false after
a fail. Equation (S.5) then states precisely when better assurance favors
the returning disposition. Reducing false positives can be particularly
valuable because a falsely trusted grabbing type receives three units.

For s=0.9,f=0.1,k=0.1, the difference is 0.5 in the pass-only region
0.1<x<0.9. For s=0.6,f=0.3,k=0.1, it is -0.4, even though the certificate
is informative; improving its discrimination is the constructive repair.
The two observation models are separate declared cases, not parameters
silently combined in one equation.

The first-order judgment predicts a partner's disposition and selects whether
to trust. A second-order assessment can judge that prediction process by
actual returns, as in R6.5. The useful fact is whether the partner will return
the benefit. This connection requires outcomes or justified audits that can
correct mistaken assurances; widespread belief in a commitment does not
substitute for its actual reliability.

## 4. Established work and the W7 boundary

[Dekel, Ely and Yilankaya (2007)](https://faculty.wcas.northwestern.edu/dekel/papers/Evolution%20of%20Preferences.pdf)
already distinguish subjective preferences from material fitness and show
that observability changes stable outcomes. Their stability concept admits
arbitrary mutant preferences and quantifies over specified post-entry
equilibria. With observable preferences, stability requires their defined
symmetric efficiency; with no observability, Nash conditions govern stable
outcomes. This is a stronger static comparison than the restricted two-type
model here, but it is not a convergence theorem for (S.3).

Their model assumes equilibrium adaptation and an exogenous observation
structure. Their discussion explicitly raises the possibility of mutants
that mimic the appearance of a different disposition. Our certificate
calculation makes one such vulnerability and repair quantitative, without
claiming to solve the general signaling or evolutionary problem.

The cycle's contribution is the typed connection among **value revision,
changed opportunities, reliable judgment and conditional persistence**.
R6.4 treats changing goals with a uniform capability advantage; this result
adds frequency-dependent strategic responses. A full account of how revision,
inheritance, observability and the available preference vocabulary arise
belongs to the proposed W7 investigation, which this cycle does not start.

The [checker](../notebook/P4-R6-C001/strategic_values.py) records the payoff
inequalities, analytic equilibrium and finite trajectories. None is an
empirical claim about human motives or a proof that a particular moral value
is universally optimal.
