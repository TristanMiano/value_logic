# Future values from partial receipts about unknown feasibility

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; broad discovery.
This is a small exact information problem, with ordinary inverse optimization,
set identification and incumbent reuse as mandatory comparisons.

Let A be a known finite set of action vectors. Its unknown nonempty feasible
subset F represents unresolved mathematical feasibility. Old computations
at weights w_i retained truthful intervals

    l_i <= min_(a in F) w_i^T a <= u_i,  i=1,...,m.

Their witnesses may have been discarded. Let B be any actually retained,
proved-feasible actions. Define

    P={a in A: w_i^T a>=l_i for every i},
    T_i={a in P: w_i^T a<=u_i}.

Consistency requires B subset P and every T_i nonempty. For m>=1 these
conditions suffice: F can be the union of B and one chosen element of each
T_i. Thus the exact information class is

    B subset F subset P,  F intersects every T_i.

For a new weight w, put h(a)=w^T a. The sharp interval for the new optimum is

    lower = min_(a in P) h(a),
    upper = min( min_(b in B) h(b), min_i max_(a in T_i) h(a) ),   (1)

where the minimum over empty B is +infinity. For the lower endpoint, add
an h-minimizing element of P to any compatible feasible set. This changes
none of the old lower inequalities or existential upper receipts. For the
upper endpoint, choose an h-maximizer from each T_i and adjoin B. Its
minimum h is exactly the right side of(1). Both endpoints are attained
by finite feasible sets. Intermediate values need not all occur because A
is finite. With no old receipts and no B, the upper endpoint is max_P h;
with no receipts and nonempty B it is min_B h.

This is a max/min consequence of the explicit information contract. It does
not prove that arbitrary feasibility predicates admit cheap membership or
optimization queries. Computing P and the contact sets can be expensive,
and all stored weights, arithmetic and source binding have costs.

## A value conclusion need not provide an action

Take A={(0,2),(2,0),(1,1),(3,3)}, B empty, and two receipts at coordinate
weights, each interval[0,1]. Then

    T_1={(0,2),(1,1)}, T_2={(2,0),(1,1)}.

For w=(1,1), formula(1) gives the exact new optimum2. Yet neither singleton
(1,1) nor either other inexpensive action is known feasible: both
F_1={(1,1)} and F_2={(0,2),(2,0)} satisfy the receipts and are disjoint.
No deterministic action is guaranteed feasible over this information class.
Choosing a subproblem whose reoptimized cost is below3 is warranted;
delivering an executable feasible action still requires information.

The same point is immediate from ordinary existential logic. It is a useful
interface distinction, not a new decision principle. If the old optimizer
returned and retained an actual incumbent, B is nonempty and its ordinary
reweighted cost is an available stronger upper control. A value-only service
or an intentional storage constraint must be justified, not invented to make
this construction appear advantageous.

## Early disposition

Keep the exact interval as a small reusable characterization. Do not build
a benchmark against full truth recovery: the first required comparison is
ordinary retained-incumbent evaluation and direct new-objective optimization.
An application with meaningful existential receipts but expensive witnesses
could make the interface useful, but neither its occurrence nor a moderately
novel algorithmic contribution has been established.

## Compact convex action sets

The same endpoint formula extends to a compact action universe A in R^d,
linear old and new objectives, and a nonempty compact convex unknown F.
Assume A is convex, P nonempty, all T_i nonempty and B a finite subset of P.
For either endpoint, choose the finite points in the construction above and
take their convex hull. This remains in P and A, intersects every T_i and
has the same minimum of every linear functional as the selected points.
Compactness supplies all extrema. Thus convex feasibility does not by itself
restore a lost action witness or improve(1). Closed unbounded universes need
infima/suprema and separate attainment arguments; they are not included here.

## From an existential value receipt to a usable finite action

Return to finite A and suppose B is empty. A membership query for a in P
truthfully answers a in F or a not in F, at fixed known positive cost c_a.
Both answers must be justified under this interface. In particular this is
not an assumption that arbitrary unresolved mathematics has a cheap total
decision procedure. An action can be delivered when its membership follows
from receipts and query answers; a redundant direct membership query is not
required after a logical implication has settled it.

Let G={a in P:h(a)<=tau} be acceptable actions. A robust existence conclusion
holds precisely when some T_i is contained in G. This follows from(1): if
every T_i has a point outside G, choose such a point from every T_i to get a
compatible F disjoint from G. Assume at least one contained T_i exists.

The exact optimal deterministic worst-case query fee for delivering an
acceptable action is

    min_(i:T_i subset G) [sum_(a in T_i)c_a - max_(a in T_i)c_a].  (2)

A singleton contact set costs zero. To attain(2), select a minimizing T_i,
leave one most expensive member unqueried, and test the others in any order.
Stop at a positive answer. If all tested members are negative, the old
existential receipt proves the unqueried member feasible. The maximum fee is
the sum in(2), not the sum including a final redundant check.

For the lower bound, an adversary answers yes to every query outside G and
no to queried actions in G until some contained T_i has only one unqueried
member. These answers are jointly consistent: include all of P outside G
and all unqueried members of G in F. Until a contained contact set becomes
a singleton, no individual remaining acceptable action is forced feasible:
omitting that action still leaves every contact set hit. Thus an algorithm
cannot soundly return an acceptable action sooner. At termination its negative
queries contain T_i minus one member, costing at least the corresponding
sum minus maximum, and hence at least(2). Positive answers outside G cannot
do better in this adversarial execution. The argument permits adaptive
deterministic query choices and inference from all the original receipts.

This distinguishes three resources: retaining an existential upper-value
receipt, retaining an actual witness, and paying to reconstruct a witness.
If an incumbent was already retained, its membership fee is zero and its
new objective must be evaluated as the ordinary control. Source binding,
contact-set generation and the cost of the receipt itself remain payable.
Equation(2) is a small finite search characterization; novelty is unassessed.

### Finite development check and randomization boundary

[receipt_search_check.py](receipt_search_check.py), executed once with
Python3.13.14, compares(2) with unrestricted adaptive deterministic minimax
decision trees over the complete feasible-set information class. All166
nonempty antichains of nonempty subsets on four actions, all15 acceptable
sets and two positive cost profiles are considered. The
[saved result](receipt_search_result.json) records2,656 feasible target/cost
cases,1,162 target families without a guarantee, and34,564 dynamic-program
states; all agree. Runtime67,239,200ns is the probe's measured runtime,
not a billed-source or practical speed comparison. The proof above carries
the general claim; the finite check only checks these cases.

Equation(2) is a deterministic worst-case fee, not an expected-fee lower
bound for randomized querying against a fixed hidden F. With one k-member
contact set and unit fees, a uniformly random order, inferring the final
member after k-1 negatives, has worst expected fee

    (k+1)/2 - 1/k.

The worst case is a singleton F; averaging over uniformly hidden singleton
members gives the matching lower bound for any zero-error randomized
algorithm. In contrast, with four actions and all four three-member contact
sets, every compatible F contains at least two actions. A random first
query followed, if necessary, by any second query/inference costs at most
3/2 in expectation; averaging over the six two-member feasible sets shows
optimality. Searching only one chosen three-member contact set has worst
expected fee5/3. Joint existential information can therefore matter for
randomized extraction even though the deterministic fee chooses one set.
This is standard promise search, not a new general separation theorem.
