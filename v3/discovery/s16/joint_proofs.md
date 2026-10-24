# Joint proof receipts without resolving every case

Codex (GPT-6), October 23, 2026. DEVELOPMENT; a proposed adapter, not a
new concentration theorem. This connects unresolved mathematics, fallible
predictions and bounded verification. The statistical comparator is an
ordinary e-process with the same logical constraints and optimization access.

## Latent process and a proof-constrained lower bound

Start with iid cases and their fixed Boolean losses Y_i. For a marginal null
E[Y_i]>=p0 use the predictable nonnegative factors of
[randomized proof purchase](randomized_proofs.md). Freeze each prediction,
purchase coin, propensity and bet at the originally required time. Write

    f_i(Y_i)=K_i-b_i*Y_i,
    K_i=1+lambda_i*(p0-mu_i+A_i*mu_i/pi_i),
    b_i=lambda_i*A_i/pi_i.

Choose the bet strictly inside its allowed range so K_i>b_i>=0. This avoids
logarithms of zero; zero-factor endpoints can instead be handled directly.
For a prefix n, a sound proof state supplies a nonempty set C of possible
Boolean vectors containing the actual (Y_1,...,Y_n). This may include
implications, exclusions, aggregate bounds and completed individual losses.
No probability calibration of C is assumed: its containment must be proved,
or separately covered by an explicitly charged failure event.

Set w_i=log(K_i/(K_i-b_i))>=0. Then

    L(C)=exp(sum_i log K_i - max_{y in C} sum_i w_i*y_i)
        =min_{y in C} product_i f_i(y_i)
        <=product_i f_i(Y_i)=E_n.                           (1)

Every sound proof refinement may shrink C, increasing L. The event that any
such lower bound, for any historical prefix and any completion order, exceeds
1/delta is contained in the latent e-process crossing event. Ville therefore
controls its probability by delta under the null. Proof choices may depend
on observed cases and previous proof work; sound containment and the original
predictability conditions are what matter. Never rewrite old bets using later
proof outcomes. The lower process need not itself be a supermartingale.

## A bounded reasoner need not solve the logical optimization

Any certified upper bound B>=max_C w^T y gives the valid lower wealth
exp(sum log K_i-B). A feasible Boolean assignment is a LOWER bound on that
maximum and is the wrong direction for certifying risk. Time-limited SAT or
integer optimization needs a checked upper bound, not its best incumbent.

Suppose the proof state entails Ay<=d with y>=0; include y<=1 among these
rows when needed. A nonnegative vector rho with A^T rho>=w certifies
w^T y<=d^T rho. Thus a dual-feasible rho suffices. More generally a sound
branch-and-bound tree can cover C and provide an upper bound on every leaf.
The representation, solver work, certificate checker, logs and rounding are
all paid. Real logs need outward bounds, not unchecked floating substitution.
Logical optimization is NP-hard in general; this is an interface for useful
partial computation, not a polynomial-time solution of arbitrary reasoning.

Singleton constraints y_i<=U_i recover the old independent partial-proof
rule. Adding sound joint constraints can only improve the exact optimum.
A relaxed feasible set can weaken that gain but preserves validity. This
monotonicity is deterministic and applies simultaneously to every later
proof refinement on the same receipt event.

## A strict capability separation at the receipt boundary

Without subsampling, take p0=1/5, lambda=1/2, n=100. Thus f_i(0)=11/10 and
f_i(1)=3/5. Suppose a sound aggregate certificate proves sum_i Y_i<=10,
while every individual loss remains unresolved. Equation (1) yields

    L=(11/10)^90*(3/5)^10 > 20.

This settles the level1/20 risk test. The per-case-upper-bound interface
sets every U_i=1 and yields (3/5)^100<1. The improved interface can use the
aggregate certificate without first identifying the ten possible failures.
This is an information/capability comparison conditional on a paid sound
certificate; its construction cost and occurrence frequency are unspecified.
An ordinary implementation using that certificate obtains the same result.
No audit-fee or runtime saving follows from the algebra alone.

## Screens and next useful question

Do not manufacture complementary pairs of losses and then call them iid
samples. Their dependence can invalidate the latent test even though their
joint logic is sound. For example, Y_2=1-Y_1 changes the conditional mean
of the second loss after the first is revealed. A process justified for that
sampling design needs a separate argument.

Known finite families of possible loss patterns permit direct maximization;
ordinary uniform confidence bounds or multinomial methods may already be
stronger and cheaper. Pairwise exclusions lead to maximum-weight independent
set; an arbitrary exclusion graph has no general cheap exact solver. These
comparators prevent treating logical structure as free economic advantage.

The next screen is a natural source of inexpensive shared proof constraints,
plus its actual checker and strongest conventional control. Generic robust
optimization and lower-process domination are established machinery. A new
service adapter must demonstrate a useful explicit delta beyond renaming them.

The numerical crossing example was checked by exact rational arithmetic in
[moments_probe.py](moments_probe.py); the general probability argument is
a same-model derivation, not independently verified by that finite check.
