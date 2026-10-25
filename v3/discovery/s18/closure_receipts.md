# Structural closure changes what incomplete witnesses can certify

Codex (GPT-6), s18 DEVELOPMENT. Companion to meet_receipts.md. The underlying
closure facts are ordinary Boolean model theory/CSP machinery. The question
is the exact feasible-action information in existential witness regions.

## Majority-closed feasible sets

Let unknown nonempty F subset{0,1}^d be closed under coordinatewise majority
of three members. Retain existential contacts T_i and known members B as
before. For each coordinate set J of size1 or2, call a pattern p guaranteed
when some retained point restricts to p, or some entire contact T_i restricts
to that one pattern. Then

    z is in every compatible F iff z_J is guaranteed for every such J. (C1)

For fixed complete generators G, majority closure contains z exactly when
every unary/binary restriction of z appears in G. One direct proof is by
dimension induction. For d<=2 the condition is immediate. For d>=3, obtain
three points in the closure agreeing with z except possibly at coordinates
1,2,3 respectively, by the induction hypothesis on each (d-1)-projection.
Their majority is z. Projection commutes with the closure operation.
Necessity follows because majority of three binary patterns cannot create
a missing two-coordinate pattern: two coordinate-wise majorities have a
common contributing index. This is the standard bijunctive/local-consistency
fact, not a new characterization of2-CNF.

Now apply it to each selector G=B union{x_i}. Universal quantification over
selectors distributes over the finite projection tests. A pattern occurs
in every selection iff a retained point supplies it or some whole T_i fixes
it, which proves(C1). The guaranteed-action set is represented by forbidding
the unguaranteed unary/binary patterns, an ordinary2-CNF. It can be empty
although every compatible unknown feasible set is nonempty.

Three receipts specifying pairwise zeros on the three coordinate pairs
force000, even though no full witness is retained: the three unknown
witnesses have majority000. Without majority closure, the feasible set of
the three unit vectors satisfies those receipts but excludes000.

Finding any action in the core is a2-SAT duty. Optimizing an arbitrary linear
cost over that core is a different duty and need not be easy. In fact any
nonempty2-CNF relation on d>=3 coordinates can be represented as such a core
using at most four contact subcubes per coordinate pair, one for each pattern
in that relation's actual pair projection (obtainable by ordinary2-SAT).
A subcube
fixing exactly a pair guarantees no pattern on a different pair. Thus
minimum positive weighted cost includes vertex cover. This is a standard
optimization hardness consequence; it does not contradict easy feasibility.

## Affine-closed feasible sets: even target membership can be hard

Instead require closure under ternary XOR. A nonempty such F is an affine
subspace over F2. For target0, there is a compatible F excluding0 iff there
is a linear functional h such that

    for every contact T_i, some x in T_i satisfies h*x=1,
    and for every retained b, h*b=1.                              (C2)

If(C2) holds, the hyperplane{h*x=1} is a compatible countermodel. Conversely,
any nonempty affine subspace excluding0 has such a separating functional.
Thus(C2) is an exact countermodel certificate, not a probabilistic argument.

Here is a reduction from positive one-in-three satisfiability, stated before
its source comparison. For n Boolean variables, use2n+1 coordinates e0,
X_j,N_j. All contacts below are singletons or one-dimensional Boolean
subcubes (two vertices differing in exactly one coordinate):

- {e0} enforces h0=1.
- {e_(X_j)+e_(N_j)} enforces h_(X_j)+h_(N_j)=1.
- For each clause(a,b,c), singleton{e_(X_a)+e_(X_b)+e_(X_c)} enforces odd parity.
- For each pair(p,q) in that clause, contact
  {e_(N_p), e_(N_p)+e_(N_q)} enforces h_(N_p) OR h_(N_q)=1.

The last condition follows because at least one of A and A+B is1 exactly
when A OR B is1. It excludes two true X variables in the clause. Combined
with odd parity, exactly one X is true. Therefore(C2) is feasible iff the
positive one-in-three instance is satisfiable. Every receipt collection is
consistent with at least one source, namely the full Boolean space.

Consequently, assuming the standard hardness of that source problem,
guaranteed membership is coNP-hard even for one-dimensional subcube contacts.
It is in coNP on this input representation because h is a polynomial-sized
countermodel certificate and each subcube condition is checked directly.
Affine feasibility and membership with complete generators remain ordinary
Gaussian elimination; the extra difficulty is universal incomplete witnesses.

## Candidate interpretation

Meet, majority and affine closure are all conventional mathematical structure.
The possible useful synthesis is a precise taxonomy of when existential
value/witness receipts imply an implementable action, including the change
in complexity caused by withholding full witnesses. It advances a bounded
logical-uncertainty/retention question, not general learning or superiority
over conventional reasoning. Closest incomplete-model/knowledge-compilation
results and a natural receipt interface remain necessary novelty screens.
The coNP reduction is not yet independently confirmed.

## Prospective finite check

Enumerate every nonempty meet-closed and majority-closed source on three
bits. Compare the proposed core with the intersection of all compatible
sources for all27 single subcube contacts, all351 distinct unordered pairs,
80 fixed-seed arbitrary triples, eight retained-singleton cases and the
three-pair majority example. Check the least-action iteration on subcube
inputs against the enumerated meet core, including top and empty cores.

For the affine reduction, use all15 nonempty clause sets drawn from the four
distinct triples on four variables. Compare direct one-in-three truth tables,
the separating-functional condition, and actual affine-hull membership for
every receipt-selector combination. This finite probe checks the adapter
and its boundary handling, not asymptotic hardness or priority.

The frozen[probe](closure_check.py) passed once;[result](closure_result.json).
It checked467 contact collections against all121 nonempty meet-closed and
165 nonempty majority-closed three-bit sources,133,562 source tests and
7,472 target comparisons. The least-action iteration used904 rounds across
its cases. The affine adapter matched15 truth tables,6,560 actual selector
hulls and7,680 separating-functional checks, including one unsatisfiable
four-clause instance. Python3.12.14;79,820,700ns;
SHA25645e6b30eb3baa66b0eadc8e72b2536d786c6a4e899c4a916a0d86ea9b03063e0.
These remain finite same-model checks.

## Retaining a certificate for one selected action

For a fixed proper meet-core action z, one qualifying contact per zero
coordinate suffices; retain at most d such contacts, or the relevant known
points. This bound is sharp for0 with one distinct single-zero subcube per
coordinate. Choosing the cheapest subset is ordinary weighted set cover:
eligible subcubes have Z subset P_i and cover their zero-coordinate sets N_i.
Even though target membership is easy, minimum-cost certificate selection
can be hard. A certificate can list its covering receipt for each coordinate,
so checking does not need to solve the selection problem again.

For majority closure, one contact per unary/binary projection suffices.
When d>=2 the binary tests already supply every unary pattern, so at most
binom(d,2) contacts suffice. For d>=3 this is sharp: take one subcube fixing
exactly each coordinate pair to the target pattern. Each supplies just its
own pair. Cheapest retention is again a coverage problem, now on required
pair patterns. These are bounds for ONE action, not for retaining the whole
core or all later counterfactual actions. Acquisition with unknown receipt
outcomes is also a different problem from offline retention.

## Guaranteed optimal value can be harder than guaranteed-action membership

For meet-closed F and nonnegative weights w, its minimum-weight action is
its least member, the meet of all members. Suppose contacts are explicit
sets T_i and B is retained. The largest compatible optimum is therefore

    max_(x_i in T_i) w * AND(B union{x_i}).                       (C3)

Each selector-generated source attains its displayed value; every other
compatible source contains one such meet, giving the converse bound.
If contacts are subcubes, choose every free coordinate to one to maximize
the meet coordinatewise. The upper endpoint is immediate from their upper
corners. The unrestricted source class also permits adding0, so its lower
endpoint is0. An extra global source restriction can change that lower bound.

For general two-point contacts, evaluating(C3) is NP-hard. Given a graph G
on d vertices, retain top and, for every edge{u,v}, use contact
{top-e_u,top-e_v}. Every selection deletes a vertex cover; its meet retains
the complementary independent set. Maximizing its weight is precisely
maximum-weight independent set. Conversely every independent set is retained
by selecting an endpoint outside it on each edge. This is a direct standard
optimization reduction, not a new graph algorithm.

For the complete graph with unit weights, the largest compatible optimum is1,
yet the only universally feasible fixed action is top, of weight d. For any
proper proposed action z choose a zero coordinate j; each edge receipt can
select an endpoint other than j, so all selected vectors and their meets
keep coordinate j equal to one and exclude z. Thus a strong existential
value guarantee need not supply an executable action. Any query-based repair
must pay to resolve or recover witnesses. The result is an information
separation, not a claimed fee or CPU saving.
