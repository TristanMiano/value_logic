# A precise boundary for the tropical set-estimation comparison

Codex (GPT-6), October29,2026 UTC. Post-A1 DEVELOPMENT comparison.
This strengthens the scope comparison without claiming that tropical methods
are generally weak or that the present algorithm is the strongest algorithm.

The accessible [ECC2022 predecessor](https://perso-laris.univ-angers.fr/~hardouin/ECC22_Guilherme.pdf)
was read at the model in sectionII-C, the two-sided-equation representation
inII-E, the inverse-image equations19--25 and Lemma2/Proposition2 inIII-B,
and the intersection equations26--31/Proposition3 inIII-C. It represents
compatible states by tropical generators and intersects prediction with
measurement inverse images. Its uncertain coefficients are interval matrix
entries. SectionII-E expressly leaves a worst-case exponential generator count;
the practically polynomial behavior is not a proved generic bound. This is
substantial whole-set prior work, not merely point estimation.

The [2025 Automatica paper](https://www.sciencedirect.com/science/article/pii/S0005109824003935)
remains only partially accessible. Its full proof has not been cleared by
reading this predecessor. The author's index points to a HAL copy; access to
HAL and the linked thesis was blocked. No inference of absence follows.

## Independent nonrepresentation check

A max-plus polyhedron is closed under coordinatewise maximum. Indeed, if
both x and y satisfy a tropical affine inequality, substituting max(x,y)
takes the maximum of their respective left and right sides and preserves it.
The same is true of an intersection of such inequalities. Projection onto
any subset of its coordinates preserves this property: lift two projected
points to feasible full points, take their coordinatewise maximum, and project.

The ordinary sum strip in the noisy receipt example does not have this
property. Both(1/5,1) and(1,1/5) satisfy x+y=6/5 and hence the strip
119/100<=x+y<=121/100. Their coordinatewise maximum(1,1) does not.
Consequently this strip cannot be the exact coordinate projection of a
single max-plus polyhedron, even with additional existential tropical
coordinates. The analogous failure of coordinatewise minimum rules out a
simple reversal to one min-plus polyhedron as a cure.

For the complete noisy source, take the two feasible tuples

    A=((1/5,1),(1,4/5)),  B=((1,1/5),(4/5,1)).

Each has the stipulated block sums and both coordinate-max receipts equal1.
Their coordinatewise maximum has both blocks(1,1), violating both upper sum
bounds. Thus the exact source itself also fails tropical max-closure.
Replacing a sum by a new response coordinate does not remove the problem:
the graph z=x+y contains(1/5,1,6/5) and(1,1/5,6/5), but not their maximum
(1,1,6/5). The ordinary consistency equations must still be represented.

This only rules out that direct single-polyhedron representation and its
coordinate projections. It does not rule out a union, a general disjunctive
encoding, a different non-coordinate transformation, or an algorithm that
combines tropical reasoning with ordinary linear constraints. Nor does it
prove that no existing paper gives the present parameterized result.

## Consequence for the contribution judgment

The strongest fair statement is that whole-state conditioning and tropical
compression are established, while ordinary within-block affine coupling
prevents importing this particular representation without more work. V19's
bounded proposed delta remains its complete scalar-image construction with
the stated report-parameter bounds and source/certificate interface. The
greatest-point control shows that some coupled ordinary polytopes nevertheless
have an easier route. Neither a nonrepresentation argument nor a failed
download is evidence of standalone novelty. The remaining full-text/expert
comparison risk stays in the80--90% judgment rather than being declared solved.
