# Why independent generator regions matter computationally

Codex (GPT-6), October26,2026. DEVELOPMENT; explicit reduction.

Allow an arbitrary compact rational polytope coupling all hidden generators.
Even consistency of k coordinate-minimum receipts then encodes multicolored
k-clique. Let graph vertices be partitioned into k colors, and let theta_v
be one scalar in[0,1] per vertex. Impose common linear constraints

    sum_(v of color j) theta_v <= 1       for every color j,
    theta_u+theta_v <= 1                 for every cross-color nonedge.

For each vertex v of color j, create a generator x_v in R^k equal to the
all-ones vector except for coordinate j, which is1-theta_v. Retain all
k coordinate minima equal to0. A receipt for color j forces some vertex
of that color to have theta_v=1. The color constraint then forces every
other vertex of that color to0. The nonedge inequalities say the selected
vertices form a clique. Conversely a multicolored clique supplies precisely
such a compatible generator selection. The initial coupled polytope is
nonempty (theta=0), rational, compact and explicitly described in polynomial
size. All receipt values are0 and all generator regions before coupling are
simple line segments.

Therefore an f(k)*polynomial(input-size) algorithm for this unrestricted
coupled extension would give one for multicolored k-clique. This is an
explicit parameter-preserving implication, not an unconditional exponential
lower bound. The independent-source subset recurrence avoids these shared
selection constraints. Simply inserting coupled LPs into each face table
would lose the independence needed to combine their witnesses.

For k fixed, enumerating n^k attainer choices and solving a coupled LP still
gives a direct procedure. It has a different parameter dependence from the
independent-source n*3^k recurrence. A finite mixture of explicitly listed
independent regimes can instead be handled regime by regime, paying their
number. Neither observation makes arbitrary coupling free.
