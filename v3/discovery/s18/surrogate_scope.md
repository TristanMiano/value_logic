# A tiny bound-adequate family can be inadequate for observations

Codex (GPT-6), s18 DEVELOPMENT. A representation consequence of the convex
envelope theorem, with ordinary robust optimization and abstract interpretation
as direct antecedents. No new general abstraction theory is claimed.

Let the uncertainty regions be a_i+C, P=conv{a_i}, and let C be a polytope
with vertices c_1,...,c_k. Retain the following k+1 surrogate feasible sets:

    P+C, P+c_1, ..., P+c_k.                                (S1)

For every finite continuous convex objective f, the minimum and maximum of
min_H f over this tiny surrogate family equal the exact corresponding bounds
over all independently selected witness hulls. The outer set P+C supplies
the lower endpoint; convexity of g(c)=min_P f(a+c) puts its maximum at a
vertex of C. Their intersection is also the exact guaranteed feasible core.
The outer set can be represented by the shared P,C rather than by an
explicit Minkowski-sum vertex list, but its optimization cost remains real.

The first surrogate P+C need not itself be a possible source. All members
can nevertheless be collectively adequate for these interval and fixed-action
questions. This gives a precise example of useful models that are not a
complete set of possible true worlds. The exact same construction is an
ordinary robust-optimization representation.

## Exponentially many joint observations can remain

For i=1,...,n let a_i=(i,i^2) and C={(0,t):|t|<=epsilon}, with0<epsilon<1/2.
Consider the2^n allowed corner configurations x_i=(i,i^2+s_i epsilon),
s_i in{-1,+1}. Query h_i=(-2i,1). For any j!=i,

    h_i dot x_j - h_i dot x_i = (j-i)^2+(s_j-s_i)epsilon > 0.

Thus the i-th generator uniquely attains this objective and its value is
-i^2+s_i epsilon. The n jointly observed values identify every sign s_i.
Any explicit family of actual hull representatives preserving all these
joint observation vectors needs at least2^n members. Yet(S1) has just three
members and preserves every individual convex optimum interval and the
guaranteed-action core for the original uncertainty family.

This is a lower bound for an explicit representative-world family, not for
all symbolic representations. The original n regions already encode the
entire family compactly, and a symbolic update can retain their dependencies.
Nor does(S1) preserve the exact set of possible values of a query: it preserves
the endpoints of the interval. Directly conditioning its three members on a
generic exact scalar observation can fail even after one observation.

The operational repair is the source-bound attainer representation in
conditioned_hulls.md. Its distinction between scalar, incidence and full
witness retention is a more useful next design question than treating the
three surrogate sets as a calibrated probability model.
