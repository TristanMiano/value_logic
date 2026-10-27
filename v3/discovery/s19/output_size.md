# Whole-value output can require exponentially many components

Codex (GPT-6), October26,2026. DEVELOPMENT; sharper explicit lower witness.

Let k=2r and take two independently unknown vectors x_1,x_2 in the
hypersimplex {x in [0,1]^k : sum_j x_j=r}. Keep k exact receipts
min(x_(1,j),x_(2,j))=0. Their supports are disjoint; each support has at
least r elements, so each has exactly r and both vectors are Boolean.
Thus x_1 is the incidence vector of any r-subset and x_2 its complement.

Use new affine responses

    f_1(x_1)=sum_(j=0,...,k-1) 2^j*x_(1,j),
    f_2(x_2)=2^k.

The first response always attains the minimum. Binary expansion separates
every r-subset, so the full future-value set has exactly binom(k,r) isolated
points. This doubles the earlier symmetric-readout witness's component
count; it is a construction improvement, not a new benchmark outcome.
An explicit interval-list output therefore needs exponential size in k,
already with two source generators. No subexponential output algorithm
exists in that representation. This does not rule out a compressed symbolic
description, a one-value consistency oracle, approximate output, or other
query-specific answers. No conditional complexity assumption is required
for the explicit-output observation.

The construction can use a common new affine readout by adding a fixed
extra coordinate0 to B_1 and2^k to B_2, and reading its sum with the weighted
old coordinates. The regions then differ, so the homogeneous shortcut is
not contradicted. The input coefficients have O(k)-bit lengths.

## Exploratory menu outcomes

menu_range_probe.py represented each source as a convex hull of vertices
whose receipt coordinates are0 on a coverage mask and1 elsewhere, plus
an integer target coordinate. Exact old zero receipts make Q(T) the hull
of vertices covering T, so local extrema are exact menu extrema. No
unproved mapping from arbitrary interval tables to convex sources is used.

The fixed panel's observed maxima were2,5,6,10,20,33,24,70,92 components for
(k,n)=(2,2),(3,3),(4,2),(4,4),(6,2),(6,3),(6,6),(8,2),(8,4), respectively.
These are maxima within twelve seeded cases per listed family, not universal
extremal values. In particular, no sharper general bound is inferred from
the apparent small-k pattern. The proven AR1 and component-count bounds
remain the available upper bounds.
