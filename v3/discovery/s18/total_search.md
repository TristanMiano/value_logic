# Joint action loss and witness-extraction fees

Codex (GPT-6), DEVELOPMENT, s18. Extends the deterministic extraction contract
in[value_receipts.md](value_receipts.md). Ordinary minimax decision trees and
scheduling with delivery tails are the strongest direct controls. Novelty is
unassessed; the displayed gains are analytic examples, not measured audit-stream
or CPU savings.

## Contract

A finite universe A has an unknown feasible subset F. Truthful existing
receipts say F intersects every nonempty contact set T_i. Optionally B is a
retained set of proved-feasible actions. Querying a costs c_a>0 and truthfully
reveals whether a is feasible. Returning a feasible action costs h_a>=0 in
the same units as the fees. Inference of membership can replace a redundant
query. The objective is worst-case total query fees plus returned action loss.
Receipt acquisition, representing contact sets and computing a policy are
separate costs; no arbitrary mathematical predicate is assumed cheap to query.

## Exact deterministic value

For one contact T, choose a final unqueried action a in T, query the other
members in nonincreasing order of h, stop at the first positive answer, and
infer a if all earlier answers are negative. If q_1,...,q_k is this query
order and C_j=sum_(l<=j)c_(q_l), its worst total is

    V(T,a)=max( max_(j<=k)(C_j+h_(q_j)), C_k+h_a ).           (S1)

The exact optimum among all adaptive deterministic policies is

    V*=min( min_(b in B)h_b, min_i min_(a in T_i)V(T_i,a) ).  (S2)

For a singleton T the inner value is just h_a, with no membership query.
If there are neither contact receipts nor retained feasible actions, this
formula does not apply; that interface needs its own nonemptiness promise.

### Why adaptivity and combining contacts do not improve(S2)

First consider any policy guaranteeing total at most V. At a history with
already spent fee C, suppose its next query is a at cost c_a.

If h_a<=V-C-c_a, its positive branch may be replaced by immediately returning
a without breaking the bound. If h_a>V-C-c_a, the original positive branch
can never return a, since future fees are nonnegative. In that case omit the
query and simulate its positive branch. This is sound: for every actual F
consistent with the old history, F union{a} is consistent with the simulated
positive answer. The receipt class is upward closed. Every other query has
the same answer in F and F union{a}, and every possible returned action is
different from a. The simulated policy therefore returns an action in F while
saving c_a. Apply this replacement recursively to the finite decision tree.

Thus a policy with the same guarantee exists that stops at its first positive
answer. Its all-negative path is a fixed query sequence. When that path ends,
it either returns a retained action b, or an unqueried action a forced by the
receipts. In the latter case some T_i must have had all other members queried
negative. Otherwise deleting a from the remaining candidate universe still
hits every T_i, so a would not be known feasible. Remove all queries outside
this T_i. The shortened policy remains sound and its maximum in(S1) cannot
increase. If the terminal action was retained b, simply returning b initially
is no worse. This reduces every policy to one contact and one final member.

Finally, among queried actions, nonincreasing h is optimal. For adjacent
actions x,y with h_x>=h_y, putting x first gives local peak
max(c_x+h_x,c_x+c_y+h_y). Putting y first gives
max(c_y+h_y,c_y+c_x+h_x), which is at least as large. Later prefix fees are
identical. Repeated exchanges prove the order. This is ordinary maximum-
lateness/delivery-tail scheduling, not a new scheduling algorithm.

### Efficient evaluation once the contact sets are known

Sort T as1,...,m by decreasing h, put C_j=sum_(l<=j)c_l, and compute
P_j=max_(l<=j)(C_l+h_l), S_j=max_(l>=j)(C_l+h_l). Leaving index r unqueried
gives

    max(P_(r-1), S_(r+1)-c_r, C_m-c_r+h_r).                  (S3)

Empty prefix/suffix maxima are ignored. All final-member choices can therefore
be evaluated in linear time after sorting. Summing over the supplied contact
sets gives O(sum_i |T_i| log|T_i|) elementary comparison/arithmetic work,
excluding their construction, rational bit complexity and receipt verification.

## What an uncoupled upper bound loses

Three actions have(c,h) equal to(10,100),(9,0),(9,0), and one receipt says
at least one is feasible. Minimizing the worst search fee alone leaves the
first action unqueried and gives18+100=118 as its worst total. The joint rule
queries that action first and leaves one cheap-loss action unqueried. A
positive first result costs110; any longer path costs at most19. Its exact
worst total is110. Merely adding a maximum action loss to a maximum fee loses
their mutual dependence.

More generally let there be k+1 actions, all query fees1, with one action of
loss k-1 and k actions of loss0. One contact is the whole universe. A static
acceptable-loss cap must admit the high-loss action, so its best worst-fee
bound plus cap is k+(k-1)=2k-1. Querying the high-loss action first and leaving
one zero-loss action unqueried achieves exactly k. The ratio tends to2.

This factor is also an upper bound for the uncoupled approach under this
nonnegative-loss contract. A policy of total value V* returns only actions
of loss at most V* and pays at most V* in fees. Choosing the static cap V*
therefore permits some extraction policy with worst fee at most V*, yielding
an uncoupled bound at most2V*. These are comparisons of guarantees under a
specified information model, not an advantage over an identical ordinary
adaptive policy. The ordinary minimax tree and tail-scheduling reduction tie.

## Prospective finite check

Before execution: enumerate the monotone receipt classes arising from all
nonempty antichains on a universe of four actions. Compare(S2) with an
unrestricted adaptive minimax dynamic program, including continuation after
positive answers and logically forced unqueried outputs. Use three fixed
fee/loss profiles, plus the displayed118/110 example and the unit-fee family
for k=1,...,6. Include two retained-witness cases. Freeze source before running;
preserve a failed version if needed. This checks the finite reduction, not
general proof independence, real membership prices or implementation economics.

[The frozen probe](total_search_check.py) passed once;
[result](total_search_result.json):507 cases,19,301 adaptive DP states and2,762
final-member evaluations. All166 four-action antichains across the three
profiles agree, as do the displayed example, six factor-bound cases and two
retained-witness cases. Python3.12.14;111,451,400ns measured probe execution;
source SHA25634c9396780ba7a5560c0e57015138a614291f5f51e5a1d2df6b7c3d489b690db.
The control permits continuation after positive answers and inference without
queries. No stronger ordinary policy is excluded from this finite comparison.

## Early comparison disposition

The primary-source screen in[literature.md](literature.md) confirms that
Jackson's ordering rule and robust decision-dependent information discovery
already supply both the ordering machinery and the broad paid-discovery
principle. Keep(S2) as a candidate tractable specialization of that ordinary
framework. Its possible delta is the exact one-contact reduction under this
specific upward-closed information contract, not joint optimization itself.
No inspected source establishes the precise reduction, but search absence is
not novelty evidence. A concrete receipt-producing application and closer
sequential-search comparison remain blockers. Return to broad discovery;
do not promote this branch on the finite507-case agreement.
