# Several models can be jointly task-adequate without one adequate model

Codex (GPT-6), October 19, 2026. DEVELOPMENT strengthening of
[scoped_service.md](scoped_service.md), using ordinary disjunction and projection.
The original union-of-envelopes premise remains sufficient but is not maximal.

Fix observable original coordinates Q and target scopes J. Let F_1,...,F_M
be the supplied nonempty source branches, U their union, and let H(F) denote
the Q-plus-J envelope of a source F. There are two different adequacy events:

    H_one = union_m intersection_J cylinder(P_(Q union J)(F_m));
    H_joint = intersection_J union_m cylinder(P_(Q union J)(F_m)) = H(U).

Always H_one is a subset of H_joint. The inclusion can be strict because the
witness branch m may depend on J in the second event. Both contain U. The
second is the largest source preserving the declared conditional projection
service of U. No probabilities or truth weights on model indices are needed.

After any actual receipt h on Q, a branch-aware controller computes

    P_J(U intersect h) = union_m P_J(F_m intersect h),

discarding inconsistent branches and retaining branch identity during updates.
If actual x belongs to H_joint, for each J some F_m-world agrees with x on all
Q union J. That witness survives every actual receipt in the fixed interface,
so the actual J-pattern is present in the computed union. It is immaterial
that a different J needs a different model. A conjunction of target clauses
is therefore safe, clause by clause, at every allowed release. At least one
branch survives each history because there is at least one target scope.

A warranted Pr(x not in H_joint)<=epsilon consequently suffices for the same
unconditional adaptive-stream release bound. The controller and its stated
post-preparation work bound are unchanged. The event is weaker than one branch
being task-adequate, but obtaining its warrant can be harder to represent or
calibrate. A bound on H_one failure implies the corresponding bound for H_joint;
the reverse implication is invalid.

## Four-bit example with a useful observation-enabled edit

Use Q={q} and declared singleton target scopes {a},{b},{r}. Let

    F_1 = (q=>a) AND (q=>NOT b) AND (q=>r);
    F_2 = (q=>NOT a) AND (q=>b) AND (q=>r).

Each branch is binary and equals its own task envelope. Their union, when
q=1, requires opposite a,b and r=1; when q=0 it imposes no restriction.
H_joint instead is exactly q=>r: a and b each have both values in the union's
individual conditional projections. Actual (q,a,b,r)=(1,1,1,1) belongs to
H_joint but to neither F_1 nor F_2, hence not to H_one. Every model is false
and every individual model's envelope fails on that world.

After observing q=1, toggling r to achieve NOT r is nevertheless valid for
every jointly adequate actual world. Before that observation, the same toggle
cannot be certified. a and b can remain unresolved for other permitted unary
tasks. This is a concrete benefit of a task-scoped ensemble contract, not a
claim that the models collectively describe one correct full world.

Adding the pair scope {a,b} changes the warrant. At q=1 its source patterns
are only 01 and 10, so the actual 11 world is excluded from the new envelope.
One must not build a pair target by freely combining the old singleton
witnesses. Likewise, merging branch pair tables before conditioning remains
unsound: the earlier even-parity example in model_unions.md still applies.

## Limits and contribution interpretation

This strengthens the fallible-model premise of the combined service without
changing its exact inference implementation. It makes the connection to using
several imperfect models more explicit: useful task agreement can survive the
failure of every full model. It does not manufacture physical coverage evidence,
conditional acceptance guarantees, or empirical savings. H_joint can be much
larger than H_one precisely because the task interface asks less; that is a
declared capability boundary, not universal superiority.

Existential projection and disjunctive representations already supply the
algebra. The relevant potential contribution is the specified observation,
action, adequacy and cost contract. A closer-prior comparison remains necessary.
The example is directly enumerable over sixteen worlds; no extensive new
test campaign is warranted for these set identities.

The frozen [finite screen](union_probe.json) passes 2,333 conditional projection
comparisons across 90 source panels. Two random panels strictly enlarge the
one-branch envelope by five worlds in total; the explicit four-bit example has
12 jointly adequate worlds versus 10 one-branch-adequate worlds. These small
counts verify the distinction, not its frequency in a real application.

## What supplied marginal error warrants can and cannot buy

Let E_(m,J) be failure of the Q-plus-J projection condition for model m, with
supplied bounds Pr(E_(m,J))<=epsilon_(m,J) on the SAME actual world and fixed
interface. Then

    Pr(x outside H_joint)
      = Pr(union_J intersection_m E_(m,J))
      <= min(1, sum_J min_m epsilon_(m,J)).

This uses no independence. It can improve the simple fixed-model bound
min_m sum_J epsilon_(m,J) when models have complementary task strengths.
For example the array [[0.001,0.2],[0.2,0.001]] gives 0.002 versus 0.201
before capping. These are supplied-premise bounds, not measured errors or
claims of realistic calibration prices. Given only arbitrary marginal upper
bounds on these events, the smaller union bound is sharp: choose all models'
bad events for each J to coincide, and arrange the resulting J-events disjointly
until their union reaches probability one. Actual projection structure can
impose stronger constraints, so this argument does not establish attainment
for every specified source ensemble.

There is an immediate strong ordinary comparator. Fix, before deployment, a
model m(J) attaining the smallest supplied bound for each task scope. Compile
that scope's permissions using only its selected model. The intersection of
the selected adequacy events has the same sum-of-minima failure bound. Because
its source patterns are a subset of the full union's, it can permit at least
as many clausewise actions. Thus marginal bounds alone do not make the full
ensemble's conservative action service better than ordinary per-task model
selection. A stronger justified joint-coverage event, different service needs
or useful implementation reuse would be needed to show an additional benefit.

This is another early economic/decision screen: keep the weaker semantic
premise, but do not build an ensemble benchmark around a weak fixed-model
comparison. Selecting models after inspecting the deployment world or the
same calibration labels would require selection-aware warrants.

The comparator's action inclusion also survives any common legal-action
constraint: intersect both permitted menus with that same constraint. It need
not posit one globally correct selected model, since each target clause has
its own selected adequacy event. The fixed all-Q warrant covers adaptive unit
receipts for that scope. A selected model contradicted by an actual receipt
must trigger the specified conflict/fallback behavior; an empty source is
never converted into permission. The comparison does not optimize observation
policy, calibration labels or source-preparation work, which remain separate
opportunities and costs.

## Exact abstract-interpretation comparison

For fixed Q and J, the envelope operator rho(F)=H(F) is extensive, monotone
and idempotent. The first two properties follow directly from existential
projection. For idempotence, each Q-plus-J projection of H(F) is exactly the
corresponding projection of F: one inclusion uses F subset H(F), the other
uses the defining cylinder constraint. Applying the operator again therefore
changes no projection. Empty F maps to empty because the target family is
nonempty. Thus these envelopes are an ordinary closure-based abstract domain,
and H_joint is its abstract join of the source models. H_one need not itself
be a closed element of that domain.

This pins down a close antecedent rather than merely citing abstraction in
general. The larger ensemble event is a consequence of ordinary abstract join;
it is not new algebra for combining unreliable models. The candidate delta
must lie in the exact public observation/action contract, its useful compact
realization and resource bound, or a justified application of that contract.
Gulwani–Tiwari 2006 Section 6 and the Cousot overview's Sections 3.14–3.17,
listed in literature.md, make the established combination context explicit.

For any receipt predicate h depending only on Q, there is also the exact
transfer identity rho(F intersect h)=rho(F) intersect h. Every projected
scope contains Q, so projecting F intersect h simply restricts each stored
Q-plus-J relation by the same h; intersecting the resulting cylinders gives
the identity. This includes unit, interval and other exact Q-only receipts.
It is a completeness statement for the declared observation operation, not
a cheap-update theorem for arbitrary source representations. The separate
binary/median/temporal hypotheses provide the useful implementations.
