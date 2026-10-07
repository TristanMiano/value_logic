# What the neural diagnostic can distinguish

Contributor: ChatGPT (GPT-6 Astra Pro), F15-ND01, 2026-10-05.
Status: derivation and interpretation developed before ND01 outcomes, with
subsequent saved-data checks to be linked separately. These are elementary
specializations to this architecture, not a new general interpretability
theory or a worldwide-priority claim.

## 1. The ordinary objective does not identify the proposed internal factors

At a fixed input, write `J0=cFN*eta` and `J1=cFP*(1-eta)`. The expected
ordinary weighted binary cross-entropy is

```math
L(p)=-J_0\log p-J_1\log(1-p).
```

Positive costs make this strictly convex on `(0,1)`, so

```math
p^*=\frac{J_0}{J_0+J_1},\qquad
z^*=\log J_0-\log J_1
 =\log c_{FN}-\log c_{FP}+\log\eta-\log(1-\eta).
```

The ordinary objective rewards this total. It does not separately supervise
the two cost contributions or the assignment of hidden coordinates to them.
For example, a price contribution and a probability contribution suffice to
describe the same optimal output, without dividing neurons into one block
for `J0` and another for `J1`. Adding a function to both log-cost factors also
leaves their difference unchanged. This establishes underidentification by
the output function, not representability of every such alternative by the
particular finite network. Finite training dynamics can favor some solutions;
ordinary behavioral adequacy alone does not tell us which was learned.

This is why the requested explanation matters: **ordinary training gives the
network no task-specific reason to organize useful features into one clean
eight-neuron block per expected cost**. A coordinate probe relies on an
additional accessibility property. Mixed features, distributed directions,
and a different task decomposition are possible explanations for failure.
Actual technical superposition is a more specific empirical claim, requiring
evidence about feature dimensionality and interference that ND01 does not
collect. The distinction is established terminology, not a reason to discount
the user's central point; see the checked sources in the representation note.

## 2. An exact decomposition of intervention error

The frozen low-level network has hidden activation `h(x)` and scalar logit

```math
z(x)=\beta+v^T h(x).
```

For an eight-coordinate subset `S`, define its native head contribution
`phi_S(x)=sum_{j in S} v_j h_j(x)`. The implemented swap is exactly

```math
z_{S\leftarrow d}(b)=z(b)+\phi_S(d)-\phi_S(b).
```

Let `ell_0=log J0`, `ell_1=-log J1`, `e=z-z*` and
`r_S=phi_S-ell_role`. The target identity intervention has logit
`z_H=z*(b)+ell_role(d)-ell_role(b)`. Subtraction gives

```math
\boxed{z_{S\leftarrow d}(b)-z_H=e(b)+r_S(d)-r_S(b).}
```

The same identity holds for a fractional mask if `phi_S` is replaced by
`phi_m=sum_j m_j v_j h_j`. Thus intervention error can arise both from
ordinary prediction error and from failure to isolate the right contribution.
The two terms can reinforce or cancel on a particular stratum. Comparing only
their separate RMS values is insufficient: for `delta_r=r(d)-r(b)`,

```math
E[(e+\Delta r)^2]=E[e^2]+E[(\Delta r)^2]+2E[e\,\Delta r].
```

Report all three terms when attributing error. A negative cross term can make
a selected intervention look better than the isolated contribution warrants.
It can also make a probability-optimal choice differ from a logit-optimal one.
Since sigmoid has derivative at most `1/4`, probability error is bounded above
by one quarter of absolute logit error. There is no corresponding unrestricted
lower bound: sigmoid can suppress large logit changes in saturated regions.

If base logits were exact and the intervention were exact for every pair in
a connected comparison domain, `r_S` would have to be constant on that domain.
For equal-target pairs, the high-level contribution is constant by construction;
nonzero actual output change measures failure of target invariance directly.
F15's conditional finite pair populations do not establish global constancy,
global disentanglement or an unrestricted representation theorem.

## 3. What exhaustive binary optimization adds

For one role and its fixed discovery pairs, set

```math
A_{ij}=v_j(h_j(d_i)-h_j(b_i)),\qquad
t_i=z_H(b_i,d_i)-z(b_i).
```

The diagnostic logit objective is

```math
f(m)=n^{-1}\|Am-t\|^2
     =m^TQm-2c^Tm+d,
```

where `Q=A^T A/n`, `c=A^T t/n`, and `d=t^T t/n`. Each row belongs to one
of five equally sized strata. This is the same objective for fractional and
exhaustive binary masks, including base error in `t`.

There are `choose(32,8)=10,518,300` binary masks. Enumerating all of them
resolves whether a better mask exists **on this finite quadratic**, subject
to the recorded float64 arithmetic and direct residual check. It removes
random-proposal coverage as an explanation for that optimum. It does not
optimize probability MAE, the original probability-MSE objective, near-boundary
decision disagreement or a worst-stratum criterion. It does not remove
discovery sampling uncertainty. Those distinctions remain even if the
validation ranking is favorable.

For a feasible fractional iterate, convexity gives
`f(s) >= f(m)+gradient(f,m)^T(s-m)` for every feasible `s`. The linear
minimizer under `0<=s<=1, sum(s)=8` selects the eight smallest gradient
coordinates. Consequently the first-order gap supplies the interval

```math
\max(0,f(m)-\mathrm{gap})\le f^*_{\rm fractional}\le f(m).
```

The same lower bound applies to binary masks because their feasible set is
smaller. A positive separation between a fractional feasible value and the
exhaustive binary minimum is evidence of a binary restriction for this
objective. If the iterative fractional solver has not reached the stopping
gap at its fixed cap, its saved feasible value is still a valid achieved
value; do not describe it as the exact fractional optimum.

## 4. A fractional mask can average several imperfect edits

The fractional feasible set

```math
\mathcal M=\{m\in[0,1]^{32}:\mathbf1^T m=8\}
```

is the convex hull of the binary size-eight masks. To check its vertices,
suppose two coordinates were strictly between zero and one: a sufficiently
small positive/negative perturbation transferring mass between them remains
feasible, so that point is not a vertex. A single fractional coordinate is
incompatible with the integer sum after all other coordinates are binary.
Thus every vertex is binary, establishing the claim for this bounded polytope.

If `m=sum_S lambda_S 1_S`, with nonnegative weights summing to one, then

```math
z_m(b,d)=\sum_S\lambda_S z_S(b,d).
```

This is an average of **logits**, not generally of sigmoid probabilities.
Convex logit MSE can improve because different binary edits make errors in
opposite directions. A good fractional mask therefore need not identify a
single clean block or an orthogonal hidden feature. The exhaustive comparison
makes that distinction measurable; the original rounded-mask comparison
alone could not exclude a much better unrounded binary subset elsewhere.

Mask mass eight is also not eight active coordinates. Fractional masks may
use many more neurons, and dead or tiny native contributions can absorb mass
without appreciable output effect. Active-coordinate counts and weighted
contribution statistics should accompany the nominal mass. Individual-neuron
coefficient magnitudes are not invariant to positive hidden rescaling;
`v_j*(h_j(d)-h_j(b))` is invariant and is the appropriate quantity for such
contribution diagnostics. Squared contribution energies still omit cross-term
cancellation, so they are descriptions rather than unique causal attributions.

## 5. Fractional masks are not equivalent to rotated-subspace interchange

An orthogonal-subspace interchange has

```math
h'=h_b+P(h_d-h_b),\qquad P=P^T=P^2.
```

With the scalar head its entire output effect is determined by `a=Pv`:
`z'=z_b+a^T(h_d-h_b)`. Necessarily,

```math
a^T v=v^TPv=v^TP^TPv=\|a\|^2.
```

For nonzero `a`, this condition is also sufficient: the rank-one projector
`P=aa^T/||a||^2` obeys `Pv=a`. For `a=0`, use the zero projector (or a
subspace orthogonal to `v`). The feasible effective coefficient vectors lie
on the sphere with center `v/2` and radius `||v||/2`. A scalar output cannot
identify all of a higher-rank projector: additional projected directions
orthogonal to both `a` and `v` can leave the effect unchanged.

In contrast, a fractional coordinate mask has `a_j=m_j v_j`, hence

```math
a^Tv-\|a\|^2=\sum_j m_j(1-m_j)v_j^2\ge0.
```

If a fractionally used coordinate has nonzero output weight, the inequality
is strict and no orthogonal projector has exactly that effective coefficient
on the full hidden space. The fractional and orthogonal-subspace families
both contain binary coordinate swaps but are otherwise different; neither
is automatically a superset of the other. Agreement on a restricted observed
activation-difference span can be less identifying than equality of full
coefficient vectors. A fractional gain motivates further work without
guaranteeing that distributed alignment search will reproduce it.

More precisely, let `D` span the activation differences on a specified
population. Equivalent logits require only `a'-a` in `D`'s orthogonal
complement. The existence question is whether

```math
(a+D^\perp)\cap\{q:q^Tv=\|q\|^2\}\ne\varnothing.
```

If `D` is proper, this intersection always exists for a fractional coefficient.
Choose any unit `n` in `D^perp` and put
`delta=a^T v-||a||^2 >=0`. The required equation for `a'=a+t*n` is

```math
t^2+[(2a-v)^Tn]t-\delta=0,
```

which has real roots because its discriminant is nonnegative. A shift along
`n` does not alter any logits on that population, but can place `a'` on the
projector sphere. This supplies per-role output equivalence, not an identified
feature or compatible projectors for both roles. An empirical null direction
can disappear outside the sampled inputs; a globally inactive coordinate
or an exact affine dependency would make the nullspace argument stronger.
This qualification was identified independently in the mechanism audit.

There is also a metric choice. Positive diagonal reparameterization
`h'=Gh, v'=G^{-T}v` preserves the original function and transported coordinate
swaps. Transporting an orthogonal projector gives `GPG^{-1}`, which is
generally oblique in the new Euclidean metric. A future subspace experiment
should fix its activation normalization or metric from discovery data before
fitting, and specify how it transports under these gauges. F15's coordinate
gauge check cannot simply be relabeled as a subspace gauge check.

## 6. Two good role interventions need not form one joint decomposition

For a diagonal mask `M` and donor hidden state `d`, define
`T_{M,d}(h)=(I-M)h+Md`. Two role interventions obey

```math
T_{M_1,d_1}(T_{M_0,d_0}(h))
-T_{M_0,d_0}(T_{M_1,d_1}(h))
=M_0M_1(d_1-d_0).
```

The output-logit order effect is therefore `v^T M0 M1 (d1-d0)`.
Disjoint binary blocks make this identically zero. Overlapping binary blocks
or fractional masks can create order effects even when each role separately
matches its expected counterfactual reasonably well. Matrix commutation of
the diagonal linear parts does not make these donor-dependent affine maps
commute. Shared projected directions raise an analogous joint-consistency
question for subspace methods.

This is an additional reason to separate a partial intervention correspondence
from a full native two-cost representation. F15 deliberately made composition
secondary. ND01 can report overlap and derived order effects as development
diagnostics, without adding a new confirmatory condition or silently changing
the original endpoint.

## 7. Consequences for the next experimental question

The possible results distinguish different needs:

| Observation | Narrow implication | Evidence still missing |
|---|---|---|
| Larger bounded search improves | Original extraction budget or proposals left useful performance unrecovered. | Whether the attained subset is adequate and distinctive relative to matched controls. |
| Exhaustive binary improves strongly over bounded search | A search-or-selection limitation exists for the registered logit objective. | Rescore the same bounded pool by that objective to isolate candidate coverage; retain probability/decision validation. |
| Fractional masks beat exhaustive binary on discovery and retain a validation gain | The binary restriction matters for these fixed models and this fitted objective. | Whether a different basis supplies a coherent joint decomposition; whether averaging is enough to explain the gain. |
| Both classes remain inaccurate | These extraction families fail to establish the target relation. | Wider subspace/nonlinear families, model optimization quality, or a different learned decomposition. |
| Constructed oracle is accurate but complete calibration fails | Complete-endpoint failure does not imply absence of constructed cost structure. | Which adequacy, control-advantage or scale condition is blocking and whether a differently scoped future claim is appropriate. |

The next experiment should be chosen from these observed discriminations.
It should not simply rerun the unchanged five models hoping for a new outcome,
nor reinterpret all nulls as novel evidence about neural representations.
