# An explicit interval-receipt adapter for difference constraints

Codex (GPT-6), October 19, 2026. DEVELOPMENT derivation.
Ordinary simple temporal networks supply the underlying representation.

Let x_0=0 and let a nonempty bounded integer source be described by difference
constraints x_j-x_i<=d_ij. Include finite initial bounds on every variable.
Prepare the all-pairs shortest-path closure D, so D_ij is the exact largest
possible x_j-x_i. Integer bounds yield integral feasible extremal potentials.
Source preparation, correctness of the model and bit-complexity are charged.

Further receipts only add unary bounds L_k<=x_k<=U_k against the SAME reference
zero. Let u_i and l_i be the tight current upper/lower bounds, initially
u_i=D_0i and l_i=-D_i0. A new upper bound U_k updates

    u_i <- min(u_i, U_k+D_ki) for every i;

a new lower bound L_k updates

    l_i <- max(l_i, L_k-D_ik) for every i.

Include the reference coordinate in consistency checks, or equivalently reject
any l_i>u_i including its fixed zero. For a consistent history the exact current
difference bound is

    D'_ij = min(D_ij, u_j-l_i).

Proof: every newly added arc touches reference zero. A shortest path in a
consistent difference graph can be chosen without repeated vertices, so it
either uses only old arcs or passes through zero once. Paths from zero to i
use at most one new outgoing bound, giving the displayed upper update; paths
to zero give the lower update. Any negative cycle must also pass through
zero, with a new upper/lower combination witnessing incompatible unary bounds.
Conversely, l_i>u_i itself is inconsistent. Concatenating shortest paths may
repeat a vertex, but removing its nonnegative cycle cannot increase cost, so
the same minimum formula remains exact.

This gives O(n) arithmetic/comparison work per new bound after O(n^3) generic
closure preparation and O(n^2) stored distances. Each requested difference
bound costs O(1). No claim is made for arbitrary new relational constraints,
withdrawals, an unfixed reference, or arbitrary real arithmetic bit complexity.
It is not the Boolean one-total-propagation-pass guarantee: many successive
bounds can each change n endpoints.

For a specified schedule edit y_i=x_(r_i)+a_i using copies and known offsets,
a target y_j-y_i<=b is universally valid exactly when

    min(D_(r_i,r_j), u_(r_j)-l_(r_i)) + a_j-a_i <= b.

Constants use reference origin zero. Thus current edits can be checked through
the immutable original distances without unfolding an action history. Actual
editing/sensing costs and selecting a useful plan are separate. This is a
mathematical schedule-transformation service, not a causal policy that can
rewrite past execution times or guarantee dynamic controllability.

Difference-constraint sources are median-closed: if x_j<=x_i+d holds in three
worlds, monotonicity and translation equivariance of median preserve it. This
is the compact symbolic specialization of [ordered_sources.md](ordered_sources.md),
avoiding explicit enumeration of every integer-domain pair tuple.

Dechter, Meiri and Pearl (1991), Temporal Constraint Networks, is the primary
STP/shortest-path antecedent. The bound-update formula is a direct constrained
shortest-path specialization. Priority for the formula or its scheduling use
has not been established; an ordinary implementation of these same distance
updates ties. A small independent world/closure comparison is appropriate,
not a new claim to have invented temporal reasoning.

The [finite screen](interval_probe.json) agrees with both direct integer worlds
and a fresh all-pairs closure on 14,399 tight difference bounds. It also checks
960 sequential unary updates and 20,640 on-demand difference queries. These
counts show finite semantic agreement, not a runtime-saving percentage.

The Dechter–Meiri–Pearl PDF fetch returned HTTP 502. Hunsberger's accessible
AAAI 2002 primary paper, Definitions 2–4, Facts 2–3 and Theorem 4, explicitly
states the attributed distance-matrix and tight attainable-difference results.
The interval-update specialization above is directly proved here; the original
1991 full text has not been read during this session.
