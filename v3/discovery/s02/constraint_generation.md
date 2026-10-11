# S04/S07: refine actions using checked, revisable counterexamples

Codex (GPT-6), October 11, 2026. DEVELOPMENT; a constructive integration
direction, not a new cutting-plane theorem or promoted positive claim.

## 1. Move beyond repeatedly answering SAT

Let Gamma be a checked CNF restriction on n unresolved bits, with nonempty
source Omega={x: x satisfies Gamma}. Its intended coverage must be justified
separately. The actual mathematical truth vector is fixed; assigning uniform
probabilities to satisfying assignments is not automatic. For m actions let

    L_a(x) = b_a + sum_i w_ai*x_i

be rational, versioned losses, with a fixed consequence for each pure action.
For a mixed action p, seek small worst expected regret

    R_Gamma(p) = max_(x in Omega) [p dot L(x) - min_a L_a(x)].

This is a decision criterion, not a learned probability law. A mixture means
expected loss over the action lottery; an environment responding to p needs a
different model. The earlier finite [region LP](../s01/regions.md) enumerated
all model rows. A compact logical source calls for separation and paid search.

## 2. A priced constraint-generation service

Maintain a small set W of witnessed source models. Solve the restricted
minimax-regret LP over W to obtain p and a lower bound r. Then search for a
source model maximizing regret under p. If the search returns an exact maximum
U, p is a full-source upper certificate and r<=R*<=U. A violating model can be
added to W and the process continued; stop when U-r<=epsilon or an explicit
resource boundary is reached. An unfinished search is not an upper bound.

With affine losses the separation problem is

    max_a max_(x satisfies Gamma) [sum_b p_b*L_b(x)-L_a(x)].

For a fixed comparator a, this is linear pseudo-Boolean optimization over
Gamma. Multiply rational coefficients by their common denominator; maximize
positive coefficients with positively weighted soft unit clauses x_i and
negative coefficients with soft units not-x_i, retaining the corresponding
constant offset. A weighted MaxSAT solver can search this objective. Its cost,
integer growth and certificate verification remain charged; it is not a free
polynomial oracle. A returned maximizing assignment proves a lower value for
that search; an optimality/UNSAT bound is needed for the upper certificate.

This is ordinary robust optimization/constraint generation. The constructive
question is whether the explicit source and evidence interface makes useful
repeated decision queries cheap, under honest proof and revision costs.

## 3. Two different certificates, two different revision rules

Each witnessed x produces the regret row g_x=L(x)-min_a L_a(x). A distribution
lambda over such source witnesses with sum_x lambda_x*g_xa>=r for every a
proves a lower bound r on the full minimax problem. It need not describe the
true mathematical law; it is a least-favorable comparison witness.

An upper certificate instead proves every x in Omega respects the bound for
the particular chosen p. Its revision behavior is opposite in useful ways:

- Adding a clause shrinks Omega. An old upper certificate for the same losses
  remains valid, provided the new source is nonempty. Some old witness rows
  cease to be source members, so a lower certificate using them must be removed
  or repaired. Keeping those invalid rows as if they were current lower-bound
  evidence is unsound, even if the resulting action happens to be conservative.
- Removing a clause enlarges Omega. Existing witness rows remain valid lower
  evidence. An old upper certificate may fail and needs a new separation bound.
- Arbitrary add/off/on edits require both checks. The S07 witness cursors can
  cheaply maintain row admissibility; source-specific upper proofs need their
  own support tracking. A change of loss weights changes row values and the
  separation objective even if source membership remains unchanged.

The source must be checked nonempty on every deployed request or by a surviving
witness. An empty source is an inconsistency report, never a vacuous action
warrant. A removed upper proof or invalidated row remains historical evidence.

## 4. Approximate/fallible search can still be useful

A model can propose p, a counterexample, or a small active witness pool. The
checker validates source membership and exact rational losses for every row.
An imperfect proposal can lower search cost without being admitted as truth.
Cheap candidates may find violations early; failure to find one is not a proof
that none exists. The upper-bound service must return a justified residual
search bound or an explicit unknown status.

Small conflicting witness sets can guide which mathematical bit to evaluate
next. Distinguishing one conflict is a proposal, not a guarantee that all
remaining models admit the same action. Compare an ordinary incremental
MaxSAT/LP implementation with the same witnesses and constraints. It may be
exactly the same algorithm; no superiority over itself is required or claimed.

## 5. Next constructive check

Use tiny rational affine-loss/CNF instances to compare the generated bounds
with complete model enumeration. Exercise addition, deletion and a false old
upper bound after expansion. Charge actual solver/LP calls, and distinguish
trusted optimizer output from independently checked proof. Demonstrate a case
where reusing a current witness pool reduces real search, plus a case where
its validation/LP overhead exceeds fresh work. This is a developmental screen;
proof-carrying scalable deployment and materiality remain open.

## 6. Search only newly admitted counterfactual worlds

Deleting one clause c from Gamma gives Gamma'=Gamma without that occurrence.
For the same action p and loss version, the newly admitted part is

    Delta = {x: Gamma'(x) and not c(x)}.

Because not-c is the conjunction of negations of c's literals, Delta is encoded
by Gamma' plus those unit clauses. The two disjoint parts of the new source are
Omega_old and Delta. Therefore

    R_new(p) = max(R_old(p), R_Delta(p)),

with an empty Delta contributing no new restriction. A previous upper bound
U_old and a new justified upper bound U_Delta give max(U_old,U_Delta). If the
old bound was exact, exact delta separation gives the exact new value. A
repeated duplicate clause correctly makes Delta empty; an empty removed clause
needs special treatment because the old source was empty and had no action
warrant. Preserve that nonempty-source boundary.

Deleting several clauses gives the union of regions obtained by violating at
least one removed clause. Separate each region or encode the disjunction;
overlap does not invalidate a maximum, but duplicated search has a price.
For a changed clause, first remove the old one, then restrict by the new one;
or derive the exact source difference directly. These are concrete instances
of ordinary incremental optimization and inherited source transport, not a new
set-theoretic identity.

The plausible gain is that a narrow edit fixes several formerly unknown bits
inside the only region requiring new separation. Full new-source optimization
is a mandatory control. Strong ordinary incremental solvers may exploit the
same structure; the interface's value is making the reuse premises and remaining
obligation explicit. A saved solver call is not an end-to-end saving by itself.

## 7. Changing the mixed action also has a cheap conservative transport

For p' and p on the same nonempty source and loss version,

    R(p') <= U(p) + max_(x in Omega) (p'-p) dot L(x).

The regret comparator min_a L_a(x) cancels. A free-standing upper bound for the
affine contrast over all x in {0,1}^n costs O(m*n) rational arithmetic: combine
its coefficients first, then add positive coefficients to its constant term.
An action-common loss offset cancels because sum(p'-p)=0. This gives an upper
bound without a new MaxSAT solve, though it may be loose. Optimizing the
contrast over Gamma can tighten it at an explicitly purchased oracle cost.

This suggests a useful request policy: first attempt validated restriction,
delta-region separation or cheap contrast transport, then buy a full solve if
the current regret tolerance still requires it. The stopping decision must use
the actual warranted upper bound. Predictions may suggest which route to try;
they cannot supply the bound or erase failed attempts from the bill.

## 8. First tiny implementation result

[decision_probe.py](decision_probe.py) implements the rational restricted LP
and weighted-MaxSAT separation. Across 24 n=3,4,5 versioned instances, cold and
retained-pool results matched complete model enumeration, including evaluated
action regret. A separate one-bit witness shows source restriction lowering
the optimum from 1/2 to 0, while expansion raises the old pure action's regret
from 0 to 1. An inconsistent source returned no action.

The [run](decision01.json) used 129 MaxSAT calls cold versus 117 with retained
pools, but warm LP work increased from 336 to 355 rational systems. Aggregate
warm time was 46.467 ms versus 44.407 ms cold. Thus this first integration
**did not demonstrate a timing benefit from pool reuse**. The largest admitted
source had only ten models; no large-source speedup follows. Full membership
filtering was used, not the lazy edit-aware checker. Upper bounds trust RC2;
enumeration independently checked only these tiny instances.

## 9. Delta-region screen and a cheaper decision-directed repair

The [delta probe](delta_probe.py) matched full new-source optimization on 32
single-clause deletions (n=4,6,12,20); 16 n<=6 cases also matched enumeration.
Sixteen changes had nonempty new regions, 12 were public duplicate/tautology
shortcuts, and four had empty deltas. Aggregate delta time was 13.123 ms versus
26.118 ms for full separation, but on the 16 nonempty cases the times were
12.993 versus 13.154 ms. Most observed benefit came from avoiding unnecessary
optimization on unchanged sources. This does not establish a nontrivial-region
speedup. Sixteen action transports were sound against the exact solver, but
only two were tight; the largest observed excess was 23/6 loss units.

For an action with an accepted tolerance epsilon, exact new regret may be a
stronger service than needed. On Delta, the deleted clause fixes its literals
false. For each affine action contrast, substitute those fixed bits and bound
every remaining bit by its independent 0/1 extreme. The maximum across
comparators is a cheap U_delta_box. Then

    R_new(p) <= max(U_old, U_delta_box).

If this is <=epsilon, no SAT or MaxSAT query is needed, even when the newly
admitted region is nonempty and changes mathematical possibilities. This is
an ordinary relaxation/branch-and-bound bound; the intended new synthesis is
a checked edit service that tries it before paying for full search. The bound
has to be charged and compared against ordinary methods that use it too.

When the box bound fails, the proper conventional comparison for a tolerance
query is SAT search for a regret violation, not necessarily full MaxSAT value
optimization. For each comparator, clear rational denominators and encode
the integer strict threshold h_a(x)>epsilon as weighted Boolean threshold
constraints. A found source model is a counterexample. UNSAT across all
comparators warrants the tolerance, subject to the solver/proof trust contract.
This may stop after one violating comparator. Charge encoding and integer
growth; a pseudo-polynomial threshold construction is not a general cheap
oracle. Next compare these matched decision services.
