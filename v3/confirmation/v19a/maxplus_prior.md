# Exact max-plus set estimation: a closer antecedent

Codex (GPT-6), October 28, 2026. P3-11-A1 comparison and reconstruction.

## Read scope and inherited result

Read the authors' full text of Espindola-Winck, Hardouin and Lhommeau,
[Max-plus polyhedra-based state characterization for uMPL systems (2022)](https://www.researchgate.net/publication/360835643_Max-plus_polyhedra-based_state_characterization_for_uMPL_systems),
especially Section II.B--E, Section III.B equations 19--25 and Proposition 2's
proof, and Section III.C Proposition 3. Its observation matrix has independently
varying interval entries. The inverse-image condition is expressed by lower
and upper max-plus matrix products, then encoded by two-sided max-plus
constraints. Prediction and measurement information are intersected.
These are strong exact-consistency antecedents, not merely interval-hull
approximations. Their generator representation can avoid explicit expansion
of all observation-winner assignments.

The authors' [2025 Automatica article](https://www.sciencedirect.com/science/article/pii/S0005109824003935)
describes exact conditional reach sets and a concise max-plus-polyhedral
method. The publisher's Section 3 snippet assumes a compact max-plus
polyhedron for the input set. Full proof text was not retrieved: the public
author-host PDF timed out, and the previously encountered HAL access block
was not bypassed. The 2022 proof read is not substituted for an unseen
2025 proof. The [2025 fixed-point paper](https://link.springer.com/article/10.1007/s10626-025-00413-w)
was available only at abstract scope; its full-text author-host retrieval
also timed out. These access limits remain in the overall novelty judgment.

## Reconstruction of the interval observation step

Write ordinary arithmetic explicitly. For fixed x and independent coefficient
intervals L_ij <= C_ij <= U_ij, the possible values of row i are exactly

    [max_j(L_ij+x_j), max_j(U_ij+x_j)].

Necessity follows from monotonicity. For sufficiency interpolate all entries
of that row from L to U with one scalar t in [0,1]. Its maximum is a continuous
function, with the two displayed endpoint values, so it takes each intermediate
value. Rows can choose their interpolation parameters independently. Thus an
observed vector z is possible exactly when both displayed inequalities hold
for every row. The lower condition chooses at least one witness j in each
row; the upper condition constrains every j. This is the same familiar
universal/existential pattern used in V19, with signs reversed.

Encoding these conditions in two-sided tropical equations is established
machinery. It would be incorrect to claim that retaining a nonconvex source,
conditioning on winner-ambiguous observations, or avoiding explicit winner
enumeration is by itself new to V19.

## Why the native max-plus-polyhedron specialization does not absorb V19

This is a structural comparison, not a claim about the unexamined later
algorithm. A set defined by tropical affine halfspaces is closed under
normalized tropical combinations: for points x,y, the point
max(lambda+x,mu+y) is retained whenever max(lambda,mu)=0. Substituting this
combination into each max-affine side distributes the maximum; an inequality
holding for both x and y still holds. Intersections preserve that closure.

Such a set of finite real vectors is path connected. Starting from x, take
max(x,t+y) as t increases from a sufficiently negative finite value to zero;
then decrease the shift on x in max(s+x,y) until reaching y. Both path pieces
stay in the set. Consequently every continuous scalar readout of a compact
nonempty such set has a connected, closed interval image. This is our direct
reconstruction from the defining inequalities; it is not an attributed new
theorem of V19 or a claim of priority for tropical convexity.

V19 admits ordinary affine coupling within a block that breaks this closure.
In its two-coordinate source, the endpoints (10,11) and (12,10) belong to the
first block's original ordinary polytope, while their componentwise minimum
(10,10) does not: the parameterization (10+2t+u,11-t+v), with t in[0,1] and
u,v in[0,0.1], would require t=u=0 and v=-1. After sign reversal this violates
max-plus closure. Its conditioned source has a disconnected scalar image,
so it cannot itself be a single compact tropical polyhedron under the same
coordinates and continuous readout. Adding projected tropical auxiliary
coordinates does not cure that closure mismatch under ordinary coordinate
projection. A different representation or a disjunctive extension may still
solve it, at a cost that must be stated.

The surviving distinction is therefore not exact set estimation as an idea.
It is the particular whole-range output/resource/certificate guarantee for
independent ordinary polytopic blocks with arbitrary affine receipt forms.
V19 uses local ordinary LPs to preserve those couplings before combining
receipt subsets. The scalar offset-only case is already covered by stronger
ordinary structure and remains a simplifying control. This comparison supports
a narrow specialization/synthesis claim; it does not prove its moderate novelty
or practical superiority, and it leaves the inaccessible full texts visible.
