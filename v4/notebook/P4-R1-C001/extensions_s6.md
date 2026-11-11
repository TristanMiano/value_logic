# S6 continuation: constructions under development

Codex (GPT-6), November 10, 2026. Same open cycle. These are working
derivations, not final result dispositions. Completed first checkpoint is
commit `1bac0e19`; see [review_s6.md](review_s6.md).

## A. What representation does coupled recovery need?

The proof of R1.9, Theorem 18, does not essentially require symmetry or a
common stationary marginal. It works in a finite-dimensional Hilbert space,
with a compact convex forecast set K, orthogonal projections P_c preserving
K, one identity projection with positive weight, a fixed F in K, and rates
bounded above and away from zero. Replace the entrywise maximum norm by
the maximum over models of the Hilbert norm. Conditional expectations of
arbitrary finite input/output partitions give concrete admissible examples.

If only a sufficient model g (P_g F=F) is present, then at an exactly
calibrated profile its advantage is

```math
s_g-\bar s=e^2\|d_\parallel\|^2+(2e-1)\|d_\perp\|^2+V,
\qquad d=F-\bar R,
```

where parallel/perpendicular refer to P_g and V is forecast disagreement.
Thus e>1/2 gives the same positive-gap contradiction as Theorem 18. At
e=1/2, a zero advantage forces d_parallel=0 and V=0; the calibration identity
V=e<F-bar R,bar R> then forces d_perp=0. Compactness gives a positive
advantage on any calibrated set with a positive potential gap, so equality
also suffices. If P_g commutes with every P_c, the calibrated Q lies in the
g-space for any e>0, and g plays the role of the finest representation.

Mere realizability can fail below that threshold. For a concrete partition
example take mu=(1/3,1/3,1/3), v=(1,1,-2), F=1+(1/5)vv^T,
g=(0,0,1), c=(0,1,1), and e=1/10. At the c-only boundary Rc=P_cF,
Rg=P_g[eF+(1-e)Rc]. The sufficient g's invasion advantage should be
-0.00609375. Forecast calibration is stable and this negative invasion
eigenvalue makes the incorrect boundary locally attracting. Add the finest
partition, use a commuting catalogue, or increase exposure to repair it.
Numerical/exact checks and full statements are pending.

## B. Finite observations: correction and decisions

Binary recurrence statistic Z in {-1,+1} has predictable conditional mean
q_t=e_t a+(1-e_t)b_t, with fixed environmental correlation a in [-1,1].
The controller b_t and environmental share e_t are known before the fresh
outcome. They may depend on the past. This conditional-law assumption holds
for a binary Markov kernel or fresh paired episodes; it must not be silently
inferred from arbitrary persistent-latent-state histories.

Retain just U=sum e_t[Z_t-(1-e_t)b_t] and V=sum e_t^2. Then U-aV is a
martingale with conditional sub-Gaussian variance process V. A normal
mixture gives, simultaneously for all times with probability at least 1-delta,

```math
|U-aV|\le\sqrt{(V+\rho)\log\frac{V+\rho}{\rho\delta^2}},\qquad\rho>0.
```

This is the standard Howard et al. normal-mixture boundary applied to the
corrected stream, not a new concentration theorem. Known feedback changes
do not require discarding U,V. With an incorrect share estimate e_hat the
population bias is (e/e_hat-1)(a-b); unknown feedback errors are amplified
at weak exposure. A known bound on mechanism error can widen the interval.

For a confidence interval [l,u], a fine forecast b has environmental Brier
gain 2ba-b^2 over the coarse forecast, at additional cost kappa. Oracle
representation gain is a^2. If the interval excludes zero, the endpoint
nearest zero is a usable forecast whose guaranteed gain is min(a^2) over
the interval. If max(a^2)<kappa, even the ideal fine model cannot repay its
cost. The regret bound of a current fine forecast b is
max{b^2+kappa-2bl,b^2+kappa-2bu,(l-b)^2,(u-b)^2}; for a coarse forecast it
is max(0,max(l^2,u^2)-kappa). H times this bound caps the value of pure
information for H future evaluations, supplying a sufficient stopping test.

## C. Randomized exclusion probes without a source flag

There is a stronger constructive route when the agent controls its own
component. On a probe choose a uniformly random symbol A from K symbols.
The agent component produces A exactly; the environment produces Y from
fixed p, independently of fresh A. The mixture's environmental share e_t
may be unknown and predictable. Accept only Y != A. Then

```math
P(Y=y,\mathrm{accept}\mid\mathrm{past})
=e_t(1-1/K)p_y.
```

Accepted symbols have exactly the environmental law, with no source flag
and no knowledge of e_t. For fixed e, expected probes for m clean samples
are m/[e(1-1/K)]; binary probes cost twice the flagged-source ideal.
The random action can have a real intervention cost, which must be counted.
The elementary rejection identity needs a closest-work comparison and
checks, not a novelty assertion by inspection.

The pair of successful/failing cases matters. Neutral binary feedback b=0
gives only Bernoulli((1+ea)/2) observations; distinguishing a=0 from a=d
requires order 1/(e^2 d^2) trials. Deliberately chosen exclusion probes attain
order 1/(e d^2) for bounded-away-from-boundary environmental parameters.
Thus e^-2 is an overlap penalty, not an unavoidable unflagged-source law.
If the agent component misfires with probability at most epsilon, accepted
data can be contaminated by at most
(1-e)epsilon/[e(1-1/K)+(1-e)epsilon]. With no lower exposure bound that
quantity cannot be uniformly controlled. Balanced exclusions for stochastic
agent mechanisms or calibrated corrections are possible repairs to explore.

## D. Unflagged assignment in the original outcome game

Candidate exact counterexample to universal one-history recovery under
positive unflagged random assignment. Let U,V,W be independent fair signs,
q_A=1/2+tU, q_B=1/2-tU, p=1/2, and

```math
q_A f_A=pq_A+k(\tfrac12V+tW),\qquad
q_B f_B=pq_B+k(\tfrac12V-tW).
```

Choose t=1/4,k=1/10. All probabilities are strictly between zero and one;
assignment contains an unflagged independent share 1/2. The two f profiles
are not twins. Multiplication of the span of {1,U} into {V,W} is an
isometry, giving E[g_a q_b]=p E[q_a q_b] and
E[g_a g_b]=(p^2+k^2)E[q_a q_b], where g_x=q_x f_x. Therefore the fine
one-history forecasts depend only on the observed past result, not on
either task label. Exact enumeration is pending.

Positive assignment still suggests eventual recovery: infinite fine history
identifies the joint observation law q_x(theta)f_x(y|theta). Full support
then identifies every conditional outcome kernel. A merged target cell
loses a positive weighted entropy gap when its type-specific kernels differ.
Construct a quantitative lower bound with q_x >= epsilon q0_x, and state
the finite-type/finite-outcome assumptions carefully. This is a positive
longer-history repair, not a general failure of recovery.

**Stronger three-history result derived next.** If every task/outcome joint
likelihood g_xy=q_x f_xy is strictly positive almost everywhere, three past
performances suffice to force separation of non-twins, even with arbitrary
skill-dependent assignment. Suppose the fine/coarse values tie. For a fixed
two-observation prefix H, compare histories ending in (A,y), target B, with
histories ending in (B,y), target A, predicting y. The numerators are the
same positive number E[H g_Ay g_By]. Equal forecasts force
E[H(g_Ay q_B-g_By q_A)]=0. The difference D_y=g_Ay q_B-g_By q_A is a linear
combination of products H of two observation likelihoods. Thus E[D_y^2]=0.
All f_Ay=f_By. For longer histories condition on the remaining prefix first.
This proves strict improvement by adding the twin-class label whenever a
coarse cell merges distinct profiles. It does not say every refinement is
already optimal under selection-dependent assignment.

Three is sharp in this positive class. Let latent fair signs S,T and an
independent R with P(R=1/2)=5/8,P(R=3/2)=3/8. Put u=SR/4,v=TR/4,w=ST/16,
and joint task/outcome law L(x,y)=(1+xu+yv+xyw)/4 for x,y in {-1,+1}.
All entries are positive. The first three moments match a model where task
and outcome sequences are independent: E u^2=E v^2=1/16,
E w^2=E uvw=1/256, all other nonconstant moments of degree at most three
vanish except those pure second moments. Therefore histories of length at
most two give no fine/coarse score gap. Yet w != uv when R != 1, so tasks
are not twins. The assignment law contains an independent share 5/8.
Exact enumeration has been added to unflagged_assignment.py; final result
statement, proof audit and output inspection are pending.

## E. Completed checks and finite-evidence continuation

The stronger result is now in R1.10. The proof removes outcome-positivity
by comparing a zero cross numerator to a positive same-task square.
unflagged_assignment.json checks 2,025 rational worlds, including zero
assignment and outcome probabilities; all 1,296 jointly observable non-twin
worlds have strict recovery by n=3. The sharp positive world ties through
n=2 exactly by integer cross-products, with n=3 gain 0.0000218450473 nats.

For two task types define, from two same-performer observations,
S_ij=(1/2)(1{Xi=A,Xj=B}-1{Xi=B,Xj=A})(e_Yi-e_Yj).
Its conditional expectation is D_y=q_A q_B(f_Ay-f_By). With four draws,
K=(<S12,S34>+<S13,S24>+<S14,S23>)/3 has expectation E||D||^2 and lies
in [-1/6,1/3]. This is **exactly the unbiased HSIC kernel** for a linear
binary-task feature and delta outcome kernel, not a newly invented statistic.
transfer_witness.py verifies equality to Song et al. (2012), Theorem 3,
equation 11 on all 4,096 task/outcome equality patterns. Four observations
can therefore provide finite evidence of a transfer distinction without
recovering a latent-state mixture. Independent performer episodes are needed
to average this witness using ordinary concentration; one long persistent
performer does not supply independent draws from the population prior.

A tempting shortcut to a quantitative V3 bound was checked and rejected:
replacing the target outcome by its coarse conditional forecast does not
annihilate K. In the sharp world the new expectation is 3615/16777216,
or 241/512 times the original 15/32768. Thus a direct Pinsker comparison to
that coarse-resampled law cannot assume a zero witness. A genuine stability
bound under selection needs another argument; the exact theorem remains.

The catalogue extension is now Corollary 18A in R1.9. The sufficient-model
advantage identity, sharp e=1/2 guarantee, commuting-catalogue repair, and
attracting incorrect boundary are checked by catalogue_geometry.py/json.
The earlier numerical prediction -0.00609375 is exact (-39/6400).

For the finite binary recurrence stream, known-feedback corrected steps and
unknown-share exclusion probes can share **one** pair of retained numbers
(U,V). A corrected step adds (e[Z-(1-e)b],e^2). A probe selects a fresh
uniform A in {-1,+1}, makes the agent component Z=A, and accepts only Z!=A;
an accepted step adds (Z,1), a rejection adds (0,0). Conditional on the past,
each step satisfies E exp{lambda(dU-a dV)-lambda^2 dV/2}<=1. The probe
case follows by conditioning on acceptance, whose probability is e_t/2
and whose mark has mean a. Normal mixing yields the same confidence sequence
across arbitrary predictable switches of these modes. Unknown e_t must be
independent of the fresh A. This is a mathematical combination of standard
correction, rejection and confidence-sequence tools; no new concentration
inequality is being claimed.

For a confidence interval [l,u], fine-forecast cost kappa, and reference
environmental score gain 2ab-b^2, the worst regret of a fine b is
max{b^2-2bl+max(kappa,l^2), b^2-2bu+max(kappa,u^2)}.
For l<u the minimizing b is clip((max(kappa,u^2)-max(kappa,l^2))/(2(u-l)),l,u).
Compare this with the coarse regret max(0,max(l^2,u^2)-kappa). H times the
smaller regret caps the benefit of pure information for H future uses.
This is a sufficient stopping rule, not an assertion that every query below
the bound is worthwhile, and it evaluates the declared reference environment
instead of silently changing the target of the original reappearance score.

For constant unknown e and fixed a in (-1,1), the full likelihood of all
four (A,Z) outcomes is a stronger statistical comparator to discarding
rejections. Its efficient Fisher information for a, treating e as nuisance,
is e/[(1-a^2)(2-e+e a^2)]. Accepted marks supply e/[2(1-a^2)] per raw probe.
Their information ratio is 1-e(1-a^2)/2, tending to one as exposure shrinks.
This calculation is pending numerical/symbolic checks. Stationary full
likelihood and the varying-unknown-share accepted stream have different
nuisance assumptions. A neutral fixed feedback b=0 with known e has
information e^2/(1-e^2 a^2), so the e^-2 versus e^-1 contrast comes from
the experiment, not an inherent superiority of a newly named estimator.
