# S6 continuation: constructions under development

**November 11 closing note, Codex (GPT-6):** the cycle has since completed
its floor. Preserve the exploratory derivations below, including superseded
bounds and pending statements as they were written. Current claims and
obligations are in the [assessment](assessment.md) and result files R1.9--R1.13;
these notes are not a second active task list.

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

## F. Quantitative selected-task recovery: current derivation

The following derivation was begun during the second checkpoint's excluded
administrative interval. No research time is reclaimed for that interval.
It now becomes the next active mathematical question; a cold reconstruction
and rational checks are still needed before promoting the statement.

For two refined labels A,B in one coarse cell K, define
d = E sum_y D_y^2, D_y=g_Ay q_B-g_By q_A. Let G be the n=3 fine/coarse
log-score gap. For a two-history prefix H and last outcome y, the two swapped
inputs have masses d1=E[H g_Ay q_B], d2=E[H g_By q_A], common numerator
N=E[H g_Ay g_By], and fine forecasts u1=N/d1,u2=N/d2. Their coarse forecast
p is the same. Exactly p(d1-d2)=d1(p-u1)-d2(p-u2), including zero masses.
Weighted Cauchy and scalar Pinsker therefore control the squared mass
difference by their log-score regret whenever p is bounded below.

Expand d=sum_y sum_{v!=y}(Delta_HA-Delta_HB), where
H_A=g_Ay g_Bv, H_B=g_By g_Av and Delta_H=E[H D_y]. The sum T of all selected
input masses is E q_A^2 q_B^2 sum_y (f_Ay+f_By)(f_Ay+f_By-2f_Ay f_By),
at most 2 E q_A^2q_B^2 <=1/8. Hence the contribution from coarse forecasts
p>=gamma is at most sqrt(G)/(4 gamma).

The low-p part has a positive exchangeability bound. For history outcomes
(y,v,y), all three coarse tasks and target in K, put
den_yv=E[g_Ky^2 g_Kv q_K], num_yv=E[g_Ky^3 g_Kv],
B_yv=E[g_Ky g_Kv q_K^2]. Coarse p=num/den. Cauchy gives den^2<=num*B;
therefore p<gamma implies den<=gamma B. The four selected fine inputs are
disjoint subsets of this coarse input, and sum_yv B_yv<=E q_K^4<=1.
Thus the absolute low-p contribution is at most gamma. Combining,
d<=gamma+sqrt(G)/(4 gamma). Choosing gamma=d/2 suggests **G>=d^4**,
without an outcome-positivity assumption. For n>3, reveal the remaining
fine prefix to both forecasters, apply the bound to its posterior, and
use Jensen on the fourth power. This should retain the same bound.

If the two task outcome laws are pointwise at least gamma for each outcome,
the swapped fine forecasts are at least gamma, even if other tasks in K
have smaller probabilities. The weighted-variance argument then controls
all selected inputs directly and gives the stronger **G>=16 gamma^2 d^2**.
Neither constant nor the fourth-power universal rate is claimed optimal.
The new question is to verify every disjointness and conditioning step,
then search equally for sharper constructive bounds and examples limiting
them. A tiny bound can certify strict relevance without justifying its
practical acquisition cost.

**Stronger simplification, next.** No threshold split is needed. For each
coarse input (y,v,y), p=num/den and Holder gives
den <= num^(2/3) C_v^(1/3), C_v=E[g_Kv q_K^3]. Hence
den/p^2=den^3/num^2 <= C_v. All four selected fine inputs are disjoint
subsets of that coarse input. Using the exact p Delta identity directly,
weighted Cauchy bounds d^2 by
(sum_selected input_mass/p^2) * (sum_selected input_mass*(u-p)^2).
The first factor is at most (|Y|-1) sum_v C_v <= |Y|-1. The second is
at most G/2 by scalar Pinsker, since no selected fine input is counted
twice. This yields the much stronger universal bound

```math
V_n(c,\bar z)-V_n(c)\ \ge\ \frac{2d_{AB}^2}{|Y|-1},\qquad n\ge3.
```

If den>0 then num>0 by nonnegativity of the joint likelihoods, so division
by p is valid on every contributing coarse input. The same posterior/Jensen
argument extends from three to all longer histories. This subsumes the
preliminary fourth- and third-power bounds; keep their derivation here as
the actual path rather than promoting redundant weaker claims.

A sharpness-in-order family extends the moment-matched example: take
R=1-h with probability 1/2+h/4 and R=1+h otherwise, 0<h<1. Then
E R^2=1 and d_AB=(4h^2-h^4)/2048. The four-observation joint law is an
affine perturbation in 4h^2-h^4 of an interior model with independent
task/outcome sequences. Smooth conditional KL therefore gives G_3=O(d_AB^2).
Together with the proposed universal lower bound, the quadratic order is
sharp in this family; the constant is not claimed sharp. Exact checks and
a careful Taylor/positivity explanation are still needed.

**Resolution.** The cold reconstruction and rational checks passed;
R1.10 Theorem 19A now states the quadratic bound and its sharpness in order.
Its finite conditional-table composition is Proposition 22A. The observed
run preserves a stronger grouped-mixture comparator and distinguishes
validation confidence from expected training regret. Xu--Liu--Sutherland
(2026), section 4.1, supplies a close HSIC/MI comparison, but applying their
bound inside the latent state would target a different information quantity.

## G. When environmental influence diminishes

The next reading of C1/C2 and the C3 bridge is: successful judgment can
retain contact with environmental structure even when its own causal
influence grows, provided the remaining environmental evidence is used in
an identifiable way. Compare passive calibrated selection and controlled
probes under the same decreasing exposure schedule. Seek a positive
grounding theorem and a genuine insufficient-information regime, with an
intervention that repairs the latter. This extends W1.4; it does not start
the broader evolution or instrumental-convergence modules.

First considered instantaneous calibration of a fine binary forecast:
b*=ea/[1-(1-e)w], w'=w(1-w)b*^2. That admits a useful exposure-energy
criterion, but assuming infinite calibration speed spends faithfulness.
The actual simultaneous equations yield a stronger route, so pursue them.

For environmental correlation a!=0, coarse forecast zero, fine forecast b,
fine weight w, and constant calibration speed eta>0, write
q=ea+(1-e)wb. Then

```math
b'=\eta(q-b),\qquad
w'=w(1-w)(2bq-b^2),\qquad
\log\frac{w(t)}{1-w(t)}
=\log\frac{w_0}{1-w_0}+\int_0^t b(s)^2\,ds+
                       \frac{b(t)^2-b_0^2}{\eta}.
```

The last identity follows by substituting q=b+b'/eta. It preserves finite
calibration speed and makes accumulated squared forecasts the selection
currency. Take b0=0, 0<w0<1 and e(t)=e0(1+t)^(-p), 0<e0<=1, p>=0.
Changing signs reduces a<0 to a>0; then 0<=b<=a is invariant.

For p<=1/2, the variation-of-constants lower bound over the last unit
interval gives b(t)>=a e(t)(1-exp(-eta)) for t>=1, since the damping
d=1-w+ew is at most one and e decreases. Thus integral b^2 diverges and
w->1. For p<1/2, the identity makes 1-w decay at least as a stretched
exponential; therefore (1-w)/e->0. At p=1/2, d->0. For every K, eventually
d<=epsilon and, over a fixed sufficiently long window,
b(t)>=a e(t)(1-exp(-eta epsilon T))/epsilon >=K e(t).
Consequently 1-w decays faster than any specified polynomial, which again
gives (1-w)/e->0. The fine update in time tau=integral eta e becomes
db/dtau=a-[w+(1-w)/e]b, so b->a. This is a simultaneous-learning result,
not merely an instantaneous-calibration calculation.

For p>1/2, select c in (w0,1), d0=1-c. While w<=c, the energy inequality
(b^2)'<=eta a^2 e^2/d0-eta d0 b^2 gives
integral b^2+b(t)^2/(eta d0)<=a^2 integral e^2/d0^2.
Since d0<=1, the logit identity bounds its increase by
a^2 e0^2/[(1-c)^2(2p-1)]. If this is less than logit(c)-logit(w0),
the first crossing of c is impossible. Hence the fine concept stays
underweighted, b->0 and w has a limit strictly below c. This is a proved
failure region, not an iff characterization for all starting weights.

Exclusion probes in R1.11 have accepted probability e_t/2. With discrete
e_t=e0(1+t)^(-p), the accepted count diverges almost surely for p<=1,
and retained marks consistently identify a. Thus the interval
1/2<p<=1 separates a passive failure region from a constructive grounding
experiment. Continuous selection time and discrete observation counts are
not a measured full-cost benchmark.

There is a corresponding information boundary, not only an ODE example.
If every own-component mean stays in [-beta,beta] with beta<1, compare
environmental parameters +/-a0, 0<a0<1. Both observed conditional means
stay in [-r,r], r=max(beta,a0)<1. The one-step Bernoulli KL is at most
4a0^2 e_t^2/(1-r^2), even for adaptive controls. Finite sum e_t^2 bounds
the KL of the full record and leaves a positive testing error. Source
flags are not available in this experiment. Thus no learner can obtain
uniformly consistent grounding there merely by reweighting interior
feedback. Exact exclusion changes the experiment and changes the evidence
order from e^2 to e. Need a careful primary-source comparison and exact
checks before promoting this package.

**Resolution.** The simultaneous-calibration proof and its checks are now
R1.12. The weak p=1/2 trajectory remains far from recovery at a million
population time units and is retained beside the eventual theorem. A
known-imperfect-control moment correction repairs accepted-only bias when
average exposure stays positive; exact rational Fisher calculations show
why fixed imperfect control does not preserve exclusion's small-share order.

## H. A genuinely observed realization of coupled judgment

The next constructive gap is whether the binary population coupling can be
realized without giving the learner expected scores or the environmental
parameter. Pursue the same two-concept recurrence, now with one observed
Z_t in {-1,+1}, conditional mean q_t=e a+(1-e)w_t b_t, fixed e>0, and
the pre-observation forecast b_t. The learner does not receive a or e.

Use diminishing common step gamma_t, sum gamma infinite and sum gamma^2
finite, with eta gamma<=1. Update b_next=b+eta gamma(Z-b), and update fine
log odds L_next=L+gamma(2bZ-b^2). The score is genuinely prequential; using
the same observation for later calibration does not leak it into its score.
These are familiar running-mean and exponential-weight updates.

There is an exact pathwise identity:

```math
L_N=L_0+\sum_{t<N}\gamma_t b_t^2+
 \frac{b_N^2-b_0^2}{\eta}
 -\eta\sum_{t<N}\gamma_t^2(Z_t-b_t)^2.
```

This replaces a difficult generic stochastic-approximation argument at the
weight-simplex boundary. The last sum is finite, so an initially positive
fine weight cannot be lost through an unbounded early negative log-odds
excursion. If sum gamma b^2 were finite while a!=0, telescope the b update
and divide by sum gamma. The martingale sum sum gamma(Z-q) converges;
weighted Cauchy makes sum gamma d_t b_t/sum gamma tend to zero, where
d_t=1-(1-e)w_t. The telescoped equation would give 0=e a, a contradiction.
Thus the positive energy term diverges, L->infinity and w->1.

For b->a, write x_next=(1-eta e gamma)x+eta gamma r_t+
eta gamma xi_t, where r_t=-(1-e)(1-w_t)b_t->0. The martingale
M_t=eta sum_{s<t}gamma_s xi_s converges. The noise-corrected error
y_t=x_t+(M_infinity-M_t) follows a stable scalar averaging recursion
with forcing r_t+e(M_infinity-M_t)->0. Therefore y and x tend to zero.
When a=0, expected squared-error drift is at most
-2eta e gamma b^2+4eta^2 gamma^2. A nonnegative supermartingale argument
gives b->0 and sum gamma b^2 finite; the log odds converge to a finite
random limit. Thus equal concepts can coexist; no complexity penalty has
been supplied that would remove idle labels.

This would implement the binary fixed-exposure case, not the general
catalogue theorem or its decreasing-exposure extension. Compare with an
equally informed ordinary implementation (identical algorithm), and with
a single fine predictor calibrated from the start (different, often faster
method, without representation selection). Test both noise and wrong-sign
initial forecasts; retain slow finite results and seek finite-time bounds
as well as consistency. No superiority or new stochastic-approximation
machinery is assumed.
