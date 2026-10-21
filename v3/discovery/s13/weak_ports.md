# Omit weak interventions without reconstructing their uncertain parameters

Codex (GPT-6), DEVELOPMENT, October21,2026. A task-directed use of standard
inverse M-matrix monotonicity/diminishing returns. The potential contribution
is a calibrated intervention-scope reduction, not a new submodularity theorem.

## A natural restricted mechanism

Let A be symmetric positive definite with nonpositive off-diagonal entries,
and let b>=0. Allowed interventions add nonnegative amounts d_i to selected
diagonal entries. These can represent added conductances to ground, or added
diagonal precision in a compatible Gaussian model. Define

    y(d)=b^T(A+diag(d))^(-1)b,    f(d)=y(0)-y(d).

The positive definiteness and sign pattern persist for d>=0. The inverse
R(d) is entrywise nonnegative: write A+diag(d)=sI-B with B>=0 and spectral
radius(B)<s, then expand its inverse as a convergent nonnegative series.
Let g(d)=R(d)b>=0. Direct differentiation gives

    partial_i y = -g_i^2,
    partial_i partial_j y = 2*g_i*R_ij*g_j >=0.

Thus f is monotone increasing and has diminishing marginal gains in every
coordinate as any other coordinate increases. For disjoint intervention
sets S,T with arbitrary nonnegative strengths,

    0 <= f(d_S+d_T)-f(d_S) <= sum_(i in T) f(d_i e_i).

Integrate the marginal derivatives while adding the coordinates in T one
at a time; each is no larger than its gain when added to the zero vector.
The statement requires coordinate/ground shunts and b>=0. General edge
incidence updates or signed task vectors do not inherit it automatically.

## Paid singleton receipts can warrant an entire edit box

Suppose permitted strengths satisfy0<=d_i<=bar{d}_i. Obtain simultaneous
upper bounds u_i on the physical singleton reductions f(bar{d}_i e_i).
The measurements/calibration and their error confidence are paid inputs.
Choose a set T of ports to omit with sum_(i in T) u_i<=tau. Then for every
choice of retained and omitted strengths in that whole box,

    0 <= y(d_S)-y(d_S+d_T) <= tau.

The controller may choose d adaptively later; this is a pointwise deterministic
consequence on the one simultaneous receipt-validity event. No fresh union
over later queries or arbitrary conditional-confidence claim is needed.
An approximate retained-port model with uniform value error eta therefore
has full-box error at most tau+eta. A decision with a certified value margin
larger than that error can be retained under its separately stated criterion.

Importantly, the original weak ports remain inside the physical system.
Only interventions at those coordinates are omitted. Calibrating the
retained port response still includes every latent coupling in A. Deleting
network nodes or zeroing unmeasured matrix coefficients would be a different,
potentially unsound operation.

This offers a route around pairwise_edits.md's precision problem: first pay
for r singleton bounds, omit ports with small *total* possible impact, then
identify only the retained k-port response if the task needs it. The exact
observable-port protocol needs2k+k(k-1)/2 values in addition to its baseline,
some singleton work being reusable. Measurement accuracy, fixed setup costs
and retained-model conditioning still determine whether this saves resources.
This is a capability/cost bound, not an observed percentage improvement.

## Why the sign/mechanism premise matters

For a general positive-definite system take the inverse block with y0=10,
g=(1,0), V=[[2,1/2],[1/2,2]]. A singleton edit at the second port has no
effect. At unit strengths, the first singleton reduction is1/3 but the
joint reduction is12/35, larger by1/105. Omitting a port based on its zero
singleton effect is therefore unsound for general SPD systems. This block
does not have the inverse M-matrix property of the positive construction.
The earlier cycle-sign counterexample gives a stronger higher-order version.

The relevant ordinary controls are submodular sensor/leader selection,
Kron/Schur reduction and sensitivity-based screening. An identical ordinary
implementation gives the same omission certificate. A useful synthesis
requires an explicit workload or a precise contract delta beyond relabelling
those results; no promotion is inferred from this derivation.

The first ports_probe.py execution checked37296 omission inequalities on16
small rational M-matrix panels, and the1/105 counterexample outside that
class. All passed. This shared probe took2.2337985s including the separate
pairwise-identification screen. It does not certify a physical model class
or a complete measurement/computation economy.

A close primary antecedent is Ma/Garnett/Schneider2013,
[Sigma-optimality for active learning on Gaussian random fields](https://www.cs.cmu.edu/~schneide/nips13ma.pdf),§§3-4, Lemmas2,7,9.
Their nonnegative inverse and diminishing-return machinery already connects
model structure to value-directed observation. The present continuous edit-
box omission contract is an adapter to be compared with that literature,
not a claim to have discovered the underlying property.
