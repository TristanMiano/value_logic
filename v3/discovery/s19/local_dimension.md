# Local dimension reduces acquisition, but not global ambiguity

Codex (GPT-6), October 26, 2026. DEVELOPMENT. This is a constructive
ordinary-control refinement of [AR1](anchor_ranges.md), not a new
fixed-dimensional linear-programming theorem.

## Exact receipts: reuse equality bases

Suppose a_j=b_j and the ambient dimension of B_i is d_i. Write
Q_i(T)=Q_i(empty) intersect {g_ji=a_j : j in T}. Gaussian elimination
either finds an inconsistent affine equality system, making the slice
empty, or selects a subset J of at most d_i rows with exactly the same
affine solution set. In the latter case Q_i(T)=Q_i(J), including when
both are empty because of the base inequalities. Hence all local ranges
can be obtained from at most

    2 * sum_i sum_(r=0)^min(d_i,k) binom(k,r)

LPs, plus equality elimination and table lookup for the 2^k subsets.
The ambient version needs no uncharged computation of the affine hull.
Dependent equations with inconsistent constants must be detected; using
only the rank of coefficient normals would be unsound.

The AR1 table still has 2^k entries per configuration. This observation
reduces local LP acquisition, not the subset-combination bound. Every
range endpoint comes from one of these smaller local lists, so the number
of distinct endpoints and connected value components is polynomial in k
for fixed local dimension and polynomially many configurations. This is
compatible with the exponential-output example, whose dimension grows.

## Interval receipts: ordinary vertex enumeration is a stronger control

For arbitrary intervals, equality-basis reuse does not identify whole
slices: two-dimensional polytopes can have distinct slices for every subset
of clipping inequalities. Nevertheless, in fixed dimension an ordinary
arrangement enumeration avoids an exponential number of LP calls.

Let Q_i(empty) have m_i listed inequalities, including every old lower
bound. Enumerate intersections of d_i independent rows selected from these
and the k optional upper rows. Retain unique points satisfying Q_i(empty),
and label each by the mask of optional upper inequalities it satisfies.
At most binom(m_i+k,d_i) row systems are attempted. For every T, take the
minimum and maximum f_i over retained points whose mask contains T.
These are the exact local extrema: all retained points used are feasible,
and every nonempty compact Q_i(T) has an optimizing vertex determined by
d_i independent active rows from the enumerated list. This remains true
for lower-dimensional nonempty slices when all equalities are represented
by their two inequalities. Zero-dimensional ambient spaces are handled
directly. Superset min/max transforms compute the table in O(k*2^k) after
point generation, apart from feasibility masks and exact arithmetic.

This is a potentially expensive conventional control when m_i or d_i is
large. It is not an observed speed improvement or a reason to present
2*n*2^k LPs as a necessary acquisition lower bound.

## One-dimensional local sources can still encode SAT

Given a CNF formula on n Boolean variables with k nonempty clauses, use
independent x_i in [0,1]. In clause j set g_ji=1-x_i for a positive
occurrence, g_ji=x_i for a negative occurrence, and g_ji=1 when absent.
Remove tautological clauses first. Retain the exact observation min_i g_ji=0.
All lower bounds are automatic. The upper observation says that at least
one literal of clause j is realized at its Boolean endpoint. A satisfying
Boolean assignment is a compatible source. Conversely, round every
interior x_i arbitrarily: none was a zero witness, so all existing clause
witnesses survive and the rounded assignment satisfies the formula.
Thus consistency is equivalent to CNF satisfiability. An empty clause
can instead be encoded by all g_ji=1 with the same demanded value zero.

This elementary reduction is a comparison barrier, not a claimed new
SAT theorem. It rules out a generic polynomial algorithm based only on
small local dimension unless P=NP. It does not contradict fixed-parameter
tractability in k or polynomial output size. With every new f_i=0, the
complete value set is simply {0} or empty, yet distinguishing those cases
already carries the satisfiability question.

No new probe is required for these linear-algebra and direct-reduction
screens. A future implementation should choose LP, equality reuse or
vertex enumeration according to the actual dimensions and representation.
