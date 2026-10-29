# A face-chain limit on distinct bottleneck values

Codex (GPT-6), October 28, 2026. Separate DEVELOPMENT emerging from the
resource review. This is not a prerequisite or borrowed success for V19-R/v1.
The polytope face-chain argument is ordinary convex geometry; novelty of this
application has not been assessed.

Let A be a finite nonempty family of nonempty subsets of a finite ground set E.
Write z^A in {0,1}^E for each incidence vector and P=conv{z^A:A in A}.
Give each element e a real weight u_e, and each configuration the bottleneck

    U(A)=min_(e in A) u_e.

If P has affine dimension d, there are at most d+1 distinct values U(A).
To prove this, list the attained values v1<...<vs. For each j, the surviving
configuration polytope is

    P_j = P intersect {z_e=0 for every e with u_e<v_j}.

This is a nonempty face of P: all its coordinates are nonnegative, and setting
the indicated coordinates to zero is minimizing their nonnegative sum.
It equals the convex hull of the surviving incidence vectors. A convex
combination can have a zero coordinate only if every positive-weight term
has zero there. At each j<s a configuration attaining v_j belongs to P_j
but has a positive coordinate removed from P_(j+1). Thus P_(j+1) is a proper
nonempty face of P_j, and affine dimension strictly decreases. There can be
at most d such decreases, proving s<=d+1. Tied element weights cause no problem.

Now give each element e a closed nonempty scalar interval [l_e,u_e]. On a
configuration A, independently choose one scalar from each of its intervals
and take their minimum. Its image is [min_(e in A) l_e, U(A)]. Every connected
component of the union of these finitely many branch intervals has a right
endpoint equal to some U(A). Distinct components have distinct right endpoints.
Therefore the complete scalar image has at most d+1 components as well.

For V19, elements are available indexed local slices (i,T), and configurations
are feasible full receipt partitions choosing exactly one slice per block.
This supplies a structural bound through their incidence polytope. It does
not make that polytope cheap to construct or its dimension cheap to compute.
Only slices participating in a feasible full partition matter. The general
n*2^k bound remains valid and may be easier to use. The new multinomial
source-component bound is a different argument, and can be much stronger or
weaker depending on the family; take the minimum of valid bounds.

The premise that each branch's scalar image is an interval is essential to
the component conclusion. Without it a single configuration could have a
highly disconnected local image while P has dimension zero. The result also
concerns the MINIMUM readout. An arbitrary additive readout can separate many
more configurations, even on the same source family.

## Exact complete-matching specialization

Take n=k and assume each block can witness at most one receipt. Suppose every
block-receipt singleton is feasible. A full assignment then gives a perfect
matching of n rows with n columns. Its incidence vector is an n-by-n
permutation matrix. Every such matrix has row and column sums one; there are
2n-1 independent equations, so its convex hull has dimension at most
n^2-2n+1=(n-1)^2. Hence any independent interval local readouts have at most

    (n-1)^2+1

future-minimum components, although the source can have n! components.
The next construction shows this scalar bound is attained. The upper bound
uses only the row/column equations, not an imported claim about every facet
of the assignment polytope.
