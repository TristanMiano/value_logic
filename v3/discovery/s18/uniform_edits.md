# Uniform proof reuse across an adaptively chosen edit class

Codex (GPT-6), s18 DEVELOPMENT. Lineage S08/S08T, with an explicitly different
source: simultaneous sampling over an edit family, rather than transporting
one old count through pointwise known relations. Ordinary uniform convergence,
Occam bounds and multiple-instance learning are necessary controls.

## A finite family needs no frozen proof-search policy

There are N fixed mathematical instances F_i and a fixed finite family E of
H permitted edits. Let y_e(i) be the exact0/1 truth of the edited instance.
Draw n indices independently from the declared task distribution q, before
using those draws to select an edit. For each e, any collection of checked
positive proofs yields a sampled success fraction s_e, counting unresolved
draws as zero. Duplicate indices count with their sample multiplicities.

The proofs may be obtained adaptively, by different fallible models, or by
checking whether old witnesses survive the edit. Pointwise s_e is no larger
than the sampled fraction of the fixed true labels y_e. Hoeffding and a union
bound therefore give, with probability at least1-alpha, simultaneously for
every e and every later proof-acquisition/selection history,

    sum_i q_i y_e(i) >= max(0, s_e-sqrt(log(H/alpha)/(2n))).       (U1)

Proof search need not be fixed in advance for this finite-family argument.
Its censorship only lowers s_e. In contrast, the edit family and sampling
law must support the claimed common event. Counting queries as independent
samples after an outcome-dependent sampling change is invalid. Successful
proofs must bind the actual edited instance; a model's prediction is not a
positive proof. Arbitrary proof acquisition after the initial lottery does
not turn the finite sample into an infinite fresh sample.

For adding at most k clauses from a predeclared catalog of M clauses,
H<=sum_(j=0..k) binom(M,j). With Boolean variables d and non-tautological
clauses of width1..w, M=sum_(j=1..w)2^j binom(d,j). Edits may affect every
instance, so the earlier support-only count transport can become vacuous
while(U1) remains informative. A conventional simultaneous certificate test
using the same sample ties this method.

A countable prefix-coded edit language similarly allocates alpha_e=alpha
2^(-length(e)); Kraft's inequality replaces logH by length(e)log2. The code
must be fixed independently of this lottery. Giving a short program free
access to the realized sample as side information can encode an overfitting
edit and invalidate the bound. This is ordinary Occam accounting, not a new
logical probability assignment.

## Low-dimensional edits alone do not control complexity

Even one planar linear-inequality edit can shatter arbitrarily many hidden
convex feasible sets. For n instances, select2^n distinct unit directions
u_S, indexed by subsets S of{1,...,n}. Choose epsilon>0 small enough that

    (1+epsilon) max_(S!=T) u_S dot u_T < 1-epsilon.

For instance i let F_i be the convex hull of the points r_(i,S)u_S, where
r_(i,S)=1+epsilon if i belongs to S and1-epsilon otherwise. Apply the edit
u_S dot x>=1. If i belongs to S its corresponding vertex passes. If not,
that vertex has projection1-epsilon and every other vertex has projection
strictly below1-epsilon. Hence edited feasibility is exactly the membership
pattern S. All F_i are nonempty convex polytopes. Distinct rational points on
the unit circle and a sufficiently small rational epsilon make the example
rational as well.

Thus parameter dimension alone does not justify a VC bound on the *true*
edited-feasibility class over arbitrary hidden instances. Complexity has
moved into the feasible sets. This is a constructive information obstruction,
not an assertion that every natural application has high complexity.

## A fixed, bounded witness bank restores a useful uniform contract

Suppose a fixed procedure associates at most K checked feasible witnesses
W_i with each base instance, independently of the evaluation lottery. The
procedure need not have been run on all N instances. Its possible output
bank must nonetheless be well-defined, including its fixed randomness.
For halfspace edit(theta,b), define

    f_(theta,b)(i)=1 iff some x in W_i has theta dot x>=b.

Then f<=y. Across the population there are at most NK witness points. The
patterns induced by affine halfspaces on those points number at most

    G <= sum_(j=0..d+1) binom(NK,j),                       (U2)

with the trivial2^(NK) bound when needed. OR-ing within each bank cannot
increase that count. Equation(U1) applies with G in place of H, even for
continuously chosen halfspace edits. This finite-population bound uses a
standard halfspace growth bound and does not require recovering the banks
on unsampled instances. Stronger sample-size-dependent multiple-instance
VC bounds are a literature/comparison obligation, not yet imported here.

Adaptive stopping or scheduling may reveal only part of the fixed banks;
count only the witnessed successes. A globally adapted procedure that changes
which K witnesses belong to W_i is a different class and needs its own
complexity or independent-sample argument. In particular, arbitrary later
proofs were harmless under the finite edit family, but cannot be justified
by a fixed-bank growth bound after changing the bank itself.

This distinguishes three paid resources: producing valid proofs, checking
their survival under edits, and purchasing the sampling guarantee. Its
possible useful delta is a reusable counterfactual certificate interface
with an explicit post-selection contract. No new uniform-convergence theorem,
measured economic gain, or readiness forecast is claimed at this stage.

## Primary-source screen and disposition

The close comparison was decisive about the core complexity claims.
Diochnos/Sloan/Turan, *On Multiple-Instance Learning of Halfspaces* (2011
author preprint; published2012), section3 Theorems1--2, already gives the
O(d log K) upper bound and a matching-order lower construction using cyclic
polytopes. Convexifying each bag preserves intersection with a halfspace.
It therefore already implies our unbounded-complexity obstruction when K
is unrestricted, as well as a stronger general lower bound. Our circle
example is a self-contained illustration of that known phenomenon.
Sabato/Tishby2012 supplies the general bag-class analysis. Do not advance
either a new VC theorem or a new impossibility claim.

Keep the counterfactual proof interface as an S08T adaptation with explicit
censoring and selection semantics. A real repeated-edit workload and complete
cost comparison would be necessary to make it a contribution candidate.
No large SAT harness is justified merely to reproduce the known statistical
principle. Preserve the information distinction between a finite edit catalog
(arbitrary checked proof production allowed) and a bounded fixed witness bank
(the bank restriction is essential to its smaller complexity bound).
