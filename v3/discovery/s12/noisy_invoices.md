# Noisy cost observations: identification and the price of a usable signal

Codex (GPT-6), DEVELOPMENT. This extends the restricted invoice interface in
[s11](../s11/invoice_information.md); it does not propose a new concentration
inequality or replace ordinary experimental design. No application advantage
has been measured. All fees and noise levels below are declared assumptions.

## 1. Contract and identification

Keep the fixed Boolean world, private evaluator, distinct-query cap H and
positive fixed coordinate fees of s11. The true invoice C is charged. The
public observer receives Y=C+Z. For this paragraph Z has a **known distribution
independent of the world and the evaluator's random seed**. Across experiments
the same distribution is used, or the policy-specific distribution is known.
There are finitely many possible true invoice values for each program.

Adding such noise does not change which population laws are identifiable from
the family of invoice experiments. Indeed, if two finite invoice distributions
have the same noisy law, their characteristic functions satisfy

```math
\varphi_Z(t)\sum_{j=1}^k a_j e^{itc_j}=0.
```

Continuity and phi_Z(0)=1 give an interval around zero on which phi_Z is nonzero.
The finite exponential polynomial therefore vanishes on that interval.
Its first k derivatives at zero form a Vandermonde system on the distinct
c_j, so all a_j vanish. Thus convolution is injective on these finite laws.
This argument needs neither a nonvanishing characteristic function everywhere
nor finite noise variance. It says nothing about stable finite-sample inversion.

Consequently, the s11 degree-(H-1) information limit persists under independent
known noise, as do its affine-source and repeated-same-instance distinctions.
Noise does not make full-cube parity observable to a single capped episode.
It also does not destroy population identifiability merely by obscuring
individual invoices. Exact decoding of one noisy invoice is a different claim.

If the noise law is unknown but common and a constant-invoice calibration
program is available, that program identifies the noise law at the population
level; the same argument then applies. Its samples and execution fees are
additional costs. Unknown policy-dependent or world-dependent noise has no
such guarantee: Z=-C, for example, erases everything. A conditionally mean-zero
noise assumption suffices for the moment estimator below, but alone does not
give the preceding exact upper limit on information (noise variance could
itself leak otherwise hidden world information).

## 2. A finite-budget signal estimator

Let chi_S be a nonconstant Boolean character. Query every coordinate in S,
at total fixed fee b. If chi_S=+1, query a nonempty marker **bundle** D disjoint
from S; otherwise stop. Put d=sum of its fees and require |S|+|D|<=H. The
true invoice is b+d*(1+chi_S)/2. Marker answers remain private and unused.

On independent fresh worlds, observe Y and use

```math
T=\frac{2(Y-b)}d-1=\chi_S+\frac{2Z}d.
```

Suppose the readout noise is independent, mean zero and sigma-sub-Gaussian,
with its scale in the same units as the invoice. T estimates mu=E[chi_S]
without bias. Hoeffding's lemma and the noise moment bound give sub-Gaussian
variance proxy v(d)=1+4*sigma^2/d^2. With N independent executions,

```math
\Pr\left\{|\overline T-\mu|>
\sqrt{\frac{2v(d)\log(2/\alpha)}N}\right\}\le\alpha.
```

Charge the **true** fee, not a potentially negative noisy readout. Under a
hard fee budget B, take N=floor(B/(b+d)); require N>=1. This bounds every
realized bill. Replacing N by an observed-cost-dependent stopping time needs
a separate time-uniform argument; an expected budget is not a hard budget.
Preparation, readout calibration and controller computation are not included
in this invoice-only budget and must be reported separately if measured.

For the continuous allocation surrogate, the squared radius is proportional
to

```math
K(d)=(b+d)\left(1+\frac{4\sigma^2}{d^2}\right).
```

For sigma>0 this is strictly convex for d>0, and its unique positive minimizer
satisfies d^3-4*sigma^2*d-8*b*sigma^2=0. It exceeds 2*sigma when b>0. Therefore
the least expensive available marker is not generally optimal. Actual fixed
coordinate fees permit only certain bundle sums; compare those sums using the
integer N expression. The continuous minimizer is guidance, not a license to
invent a new fee or disregard the depth cap.

Among post-parity two-codeword schemes with nonnegative additional fees,
replacing the lower-fee codeword by the empty bundle weakly lowers the worst
bill and increases the signal separation. Thus one-sided marker bundles lose
nothing for this particular upper-bound objective within that coding class.
This does not establish optimality among all adaptive invoice programs.

## 3. Small constructed consequence

On four bits, estimate chi_{1,2}. Relevant fees are (1,1); the two available
markers have fees 1 and 8. Set H=3 and independent sigma=4 noise. Both programs
obey the same cap. Their K values are 195 and 20 respectively. To obtain
radius 0.2 at confidence 0.95, the displayed bound asks for

```text
cheap marker:     ceil(2*65*log(40)/0.2^2) executions, worst fee 3 each;
expensive marker: ceil(2* 2*log(40)/0.2^2) executions, worst fee 10 each.
```

The [executed standard-library calculation](noise_probe.py) and its
[output](noise_probe.json) certify these sample counts as **11,989 and 369**.
It encloses log(40) by exact rational Taylor bounds for the exponential and
checks that both endpoints give the same ceilings. Worst fees are **35,967
and 3,690**, a reduction of **89.7406%**. Maximum coordinate purchases are
35,967 and 1,107; controller and readout computation are not fully metered.
The continuous fee proxy falls by 89.743589...%. This is a constructed
comparison of two sufficient designs, not a measured empirical gain,
all-method lower bound or superiority over ordinary noise-aware design.

The same small probe enumerates 19 declared fee/cap/noise menus and checks
40,736 noiseless world/program cases for the actual invoice decoding and cap.
It also saves analytical reset comparisons, with floating Gaussian diagnostics
labelled separately. It does not simulate coverage or validate the assumed
noise law. The first run completed without an interpreter failure.

With a larger cap, multiple cheap markers can jointly provide a larger signal.
A comparison using only one marker would then be artificially restricted.
For example, an apparent preference reversal between a long direct character
and a short model-based alias can disappear when the alias is allowed a
bundle of otherwise unused queries. Retain the cap and full allowed bundle
menu before making any model-selection claim.

## 4. Source-aware representation extension

For a declared menu of character experiments j with worst fee c_j and noise
proxy v_j, independent sample counts yield proxy sum_j a_j^2*v_j/N_j for the
estimator of a_0+sum_j a_j*chi_j. Under continuous budget sum_j c_j*N_j<=B,
Cauchy-Schwarz gives the minimum proxy

```math
\frac{1}{B}\left(\sum_j |a_j|\sqrt{c_jv_j}\right)^2,
\qquad
N_j=\frac{B|a_j|\sqrt{v_j/c_j}}
 {\sum_k |a_k|\sqrt{c_kv_k}}.
```

Thus the earlier source-residual representation design remains available with
weights sqrt(c_j*v_j), and a warranted leakage penalty epsilon*R remains
separate. The old integer-ceiling reservation can be reused with the complete
menu's sum of worst fees. This is the same conventional allocation argument;
the new work is specifying what a noisy invoice can actually measure and cost.
Joint measurements, variance-adaptive estimators and non-marker programs are
stronger comparison classes, not covered by this optimum.

## Next inexpensive screens

Check the finite calculations; compare all permitted marker bundles; inspect
primary work on noisy stopping-time/timing observations and cost-aware
experimental design. Do not build a large sampling benchmark until a useful
restricted measurement setting or a stronger mathematical delta is apparent.
