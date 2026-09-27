# F05 S1 — adversarial reconstruction of the provisional semantics

Status: same-assistant derivation and review, not an independent audit or a
completed F06–F09 task. Companion to [the provisional core](03_provisional_core.md).
The point is to test the interpretation choices while they are still revisable.

## A. A finite arithmetic connection to RLL without losing improvement

There are two different maps to nonnegative quantities. Clipping a cost
difference retains deterioration but discards a strict improvement margin.
Representing a finite signed value by a **difference pair** retains it exactly.
Do not confuse the two.

Represent a finite signed x by (x+,x-) in the finite nonnegative reals, with
x=x+-x-. The representation is not unique: adding the same nonnegative amount
to both coordinates changes neither x nor any correctly translated query.
The equivalence relation is (a,b)~(c,d) iff a+d=c+b. A shared signed source uses
one shared pair throughout a translated expression, not fresh pairs in each use.

Translate a term t into (P_t,N_t) as follows:

* q maps to (max(q,0),max(-q,0));
* a source x maps to its declared pair;
* t+s maps to (P_t+P_s,N_t+N_s);
* a t for a>=0 maps to (a P_t,a N_t); for a<0 use (-a N_t,-a P_t);
* min(t,s) maps to (min(P_t+N_s,P_s+N_t),N_t+N_s);
* max(t,s) uses max in that same first component;
* res(t,s) maps to (res(P_t+N_s,P_s+N_t),0).

Let bindings translate as bindings of pairs, respecting lexical scope. A named
positive unit conversion acts on both coordinates and retains the unit tag.
All intermediate coordinates remain finite and nonnegative. Induction proves
P_t-N_t=[[t]] at every finite pair assignment. The min case, for example, is

    min(a+d,c+b)-(b+d)=min(a-b,c-d).

The residual case subtracts (P_t+N_s) from (P_s+N_t) before clipping, hence gives
max(s-t,0), with the source order in the right direction.

The signed-budget comparison t-s<=b becomes

    P_t + N_s + N_b <= N_t + P_s + P_b.

Under RLL's additive sequent convention, the right side can supply the
antecedent sum and the left side the conclusion. This is only the numerical
semantic orientation: F05 has not selected all RLL inference rules or established
a proof-system embedding. Finite guards on **both coordinates** are indispensable;
allowing (infinity,infinity) would not denote a signed real at all.

Every real assignment has a finite pair lift using max(x,0),max(-x,0). Every
finite pair assignment projects to a real one. Translating source inequalities
by the same construction therefore preserves and reflects modeled validity
when quantifying over those finite pair lifts. Source scopes, evidence validity
and policy observability still require their separate interfaces.

This confirms that signed improvements need not abandon the useful nonnegative
arithmetic mechanism. It does not supply a novelty claim, infinity arithmetic,
metaphysical truth, or a complete solution to the broader F09 comparison.

## B. A source name, an observation, and a computable choice are different

Let W be the disjoint union of the context's hidden cases over all visible
observations, and let obs:W->O forget the hidden information. An action selection
a:W->Actions can be implemented by a policy table pi:O->Actions **only if** it
is constant on each observation fibre. Conversely, fibre constancy supplies such
a table by choosing any representative of each nonempty fibre. For finite O
and Actions the table is a finite implementation once its entries are specified.
This statement about factorization does not itself decide fibre constancy.

A subtle error would be to inspect only free numerical source names. The action
may be 0 in one hidden case and 1 in another even when both expressions are
constants with no free numerical variable. Hidden case dependence also has to
be excluded. The policy table in the provisional core enforces this directly.

For the reflective source p=s+1/2, the pointwise exact solution of r=H_r is

    r=(s+1/2)/(3/2),

ranging from 1/3 to 1/2. It depends on the hidden s. Calling that formula the
chosen action would violate the observation contract. The uniform report 1/2
is executable without knowing s and is a valid upper bound. An exact rate per
possible model and a single available report are different achievements.

For a general fixed (p,s) in [0,1]^2, the report inequality is

    (1+p-s)r>=p.

At (0,1), its left coefficient and right side are both zero, so every r is
valid and the least report is zero. Else its least report is p/(1+p-s).
Over a rational polyhedral uncertainty set in the probability square, a uniform
least report is rational: on a convex mixture of nondegenerate vertices, the
ratio is a convex combination of vertex ratios with weights proportional to
(1+p-s). A degenerate vertex contributes zero to both numerator and denominator.
Take the largest vertex ratio across all cases, or zero if all cases are the
single degenerate point. This rechecks that rational report literals do not
exclude the needed exact uniform witness in this particular source fragment.
It is not a general rational-fixed-point theorem or an implemented optimizer.

## C. A finite meta-controller that actually uses its own evaluation

The fixed-r example can be bound into an executable finite self-assessment
scheme without consulting the hidden error e. Let the visible input beta be
one of 1/32,3/64,3/32, with evidence -1/32<=e<=beta. Keep the two program versions
with reports r0=1/2 and r1=3/4 and the same joint p,s model.

The finite evaluator computes, from the already-defined component costs,

    b(beta)=beta-1/16.

It chooses r1 if b(beta)<=0, otherwise r0. Its own emitted report is that chosen
r, and that same r controls its branch probability. This is a finite arithmetic
and comparison procedure on visible evidence. It is not a call to an all-purpose
validity or optimum oracle, and it never branches on actual e, p, s or hidden mode.

For beta=1/32 it chooses r1 with intended-cost bound -1/32 relative to r0;
for beta=3/64 it chooses r1 with bound -1/64; for beta=3/32 it chooses r0 with
bound zero relative to r0. Both chosen reports satisfy the self-bound. In the
three-observation interpretation its cost increase over the fixed reference is
bounded by min(beta-1/16,0), derived by those two operational cases.

The reference must remain explicit. Take the actual model p=1/2,s=0,e=z=w=0.
After the visible evidence changes from beta=1/32 to beta=3/32, the chosen policy
reverts from r1 to r0. Actual intended cost increases from 5/16 to 3/8, namely
by 1/16. Both decisions are no worse than the **fixed reference r0** under their
current premises; they do not form a monotonically improving sequence relative
to the last deployed policy. Consecutive-revision guarantees need paired queries
against that last policy, not a silently changing reference label.

The criterion in this calculation includes failure and the named branch charge.
Extra data collection, checking or computation costs are not automatically zero.
They must be included in the plan cost expression, cancel as a justified common
baseline, or be covered by an explicitly supported discrepancy bound. Adding an
unmodeled overhead to only the new controller changes the comparison problem.
The experiment would have to measure that overhead before claiming total practical
improvement. This is a scope limit, not a ban on reasoning about its own costs.

## D. Exact implication, model validity and action validity

For a fixed nonempty C, semantic entailment is an ordinary conditional mathematical
relation. A rational countermodel of t-s<=b proves failure of its universal
warrant. It does not demonstrate failure of the physical system if that point
is outside the actual, richer model or occurs only in an overapproximation.
A source-witness point proves satisfiability, not calibration or empirical coverage.

The primitive distinction is therefore not 'accepted versus false'. At least
four questions can differ: type/scope admissibility; existence of any admitted
model; a conditional quantitative comparison; and the separate bridge from that
model to actual use. These are not four proposed truth values. The numerical
object stays a source-indexed cost; an implementation reports what evidence it
has for the questions it actually answered.

Hard constraints belong on the proposed action or query. Treating 'the selected
policy must be safe' as a row that simply removes every unsafe source would make
the conclusion circular unless independent evidence justifies that row. Conversely,
a contextual premise that is genuinely supported can be used conditionally even
when its support is statistical rather than factive.

## E. Evaluation scope and type reconstruction

The first draft allowed an arbitrary rational 'conversion'. This conflated unit
changes with reversing or deleting a preference scale. Unit conversions are now
strictly positive rational maps; zero or negative weights remain explicit scalar
operations, not unit isomorphisms. A reward interpretation can use -loss, but its
order reading must reverse explicitly. No comparison silently flips its meaning.

Sources and local let variables are separate syntactic name classes. Otherwise
`let x=0 in source(x)` could accidentally erase an unknown source by shadowing its
printed name. In the selected grammar `src(x)` is always a signature lookup and
`loc(x)` a lexical lookup. Closed source substitutions cannot capture a local
variable. These are semantic choices to test, not merely parser conventions.

A let can save evaluation work, but numerical equality of two expressions does
not establish equal execution resource cost. The term language describes cost
quantities; it does not automatically account for the interpreter's own arithmetic
or the physical program's effects. A plan-level resource criterion has to specify
which such costs it includes. Similarly, two invocations sharing an unknown
probability parameter need not share their random draw.

An injective, unit-preserving renaming of source keys can preserve every
interpretation by pullback. A noninjective renaming may delete admissible cases:
identifying theta1 with theta2 in the first example removes its deteriorating
witness. Even an injective renaming needs the corresponding context and query
translation, not a replacement of display names in one place only.

## F. Comparisons compose only with the same middle meaning

On one common context, t-s<=b and s-u<=c imply t-u<=b+c by adding pointwise
inequalities. The middle term denotes the same quantity at the same assignment.
If its source, criterion, evaluator version or policy binding changes between the
two premises, a separate discrepancy/transport obligation is needed. Units alone
are insufficient to identify the middle term.

Around a finite closed chain of such comparisons the left-hand differences sum
to zero. A negative sum of budgets is therefore incompatible with a nonempty
source interpretation. It signals inconsistent premises, an aliasing/versioning
mistake or an invalid proof; it does not describe free unbounded improvement by
cycling through the same states. History-dependent actual costs can change, but
then the repeated names must not masquerade as the same cost term.

This is a semantic consistency check for future rules, not a selected F06 rule
system or general F07 soundness theorem. The same caveat applies to an attempted
self-proof that uses its conclusion as an empirical premise. A context containing
that premise may imply the conclusion conditionally; it does not produce the
missing evidence supporting the premise.

## G. A concrete neural interpretation interface without architectural enforcement

At a particular observed evidence vector eta, suppose the hidden quantities
x,y obey x<=eta1, y<=eta2, and x+y<=eta3. The fixed query is x+y. The numerical
function

    f(eta)=min(eta1+eta2,eta3)
          =eta3-ReLU(eta3-eta1-eta2)

is a valid bound: the first branch adds two premises, and the second uses the
joint premise. Its two affine coefficient vectors are (1,1,0) and (0,0,1).
They are certificates for the **same** fixed query, not different actions.

A uniform statement about this function is expressible as a family of ground
contexts or as the numerical relation x+y <=_0 f(eta) on a joint source signature.
There is no need to add a special oracle-bound primitive. For an actual use eta
is observed, while x,y remain latent. The action interface must not treat the
latter as available inputs merely because the semantic relation quantifies over them.

This constructed function gives a precise interpretation target, not a trained
network result. An unconstrained network might instead estimate x+y, produce a
looser sound bound, encode a different decomposition, or fail the proposed claim.
Causal participation and stable source meanings remain separate empirical
questions. Kink conventions and correlated-input nonidentifiability from F04
are not solved by this simple algebraic example.

## H. Why unknown source support does not become a truth degree

The quantity x+y in the preceding example is a modeled cost, f(eta) a numerical
upper bound, and evidence for the rows a separate object. The comparison can be
mathematically exact conditional on the rows while their empirical applicability
is uncertain. Replacing that structure by a single number called 'confidence'
would discard which premises and operational meanings the inference requires.

Conversely, retaining an explicit source model is not a claim to know the true
world. A richer model may reveal that the source omitted a relevant dependence.
Then one may enlarge/change the model and re-evaluate its warrants. A previously
valid conditional theorem is distinguished from the decision to rely on its
now-questioned hypotheses. This is the finite-stage interface to open-ended
succession inherited as a research aim, not a claim of eventual finality.

## I. Three checks on source growth and model succession

**New unknown without new information.** Extending a signature by a new source y
and extending D to D x R preserves every old query not mentioning y. Projection
back to the old coordinates is surjective, so both directions of validity hold.
This is a cylindrical extension, not an assertion that y is probabilistically
independent. If a new relation involving y also restricts old coordinates, the
old query can become better determined; if source meanings change, this argument
does not apply.

**A new available plan.** A finite family of pairwise comparisons can establish
that a particular plan is no worse than every member of the *named* old family.
It cannot establish that statement for a newly added unconstrained cost source.
For example, an old cost 1 and new source y with no lower constraint permit y=0.
The old finite comparisons remain mathematically valid, but the quantified plan
family has changed. Adequacy, finite-family preference and global finality are
not one judgment. The core need not enumerate all conceivable later plans.

**A supposedly harmless rewrite.** Replacing a source description by a lossless
serialization preserves its raw information only when the decoding relation is
retained. Replacing inequalities by consequences is an information weakening,
even if the vector of displayed numeric bounds can be inverted. The semantic
transport asks about the full admissible relation, not recoverability of a string.
The x<=1,y<=2 counterexample in the main note checks this difference explicitly.

## J. The nonlinear adapter is component-local

A danger in the third interpretation is to assume the very paired comparison
that the calculus is supposed to produce. The proposed adapter instead proves,
for any interval [a,b], an enclosure of one component's theta^2 value. It can be
reused against another old-plan cost, with a potentially different final result.

For a fixed cell, the abstract source admits q between its chord and that chord
minus 1/256. It generally contains points not on the exact graph q=theta^2.
Thus the map from the exact kernel to the abstraction is an inclusion, not an
isomorphism. The positive -3/16 result is sound because every abstract point
already satisfies the paired bound. A failure of a *different* query in this
abstraction could be a spurious countermodel, so a semantic evaluator must retain
which model it is evaluating and not label every abstract witness a physical
failure.

At theta=1/2 the active chord equals 1/4. The abstract source allows q=63/256,
whereas the exact q is 64/256. For the query `q>=1/4`, the abstract model has a
counterexample although the exact fixed-theta computation satisfies it. This
small witness makes the overapproximation boundary executable.

Using four cells is not a claim of minimum representation size. The single
full-interval chord already preserves the comparison to theta. Conversely, the
four-cell lower/upper band controls component error at 1/256 while the full-
interval chord's error reaches 1/16. The relevant consumer decides which detail
is worth retaining. This is the specific task-relative approximation choice
that distinguishes the two provisional routes without inventing unequal inputs.

## K. Observable bounds and latent costs do not need the same role

A goal can compare two arbitrary same-unit expressions, not only two named
program costs. Consequently `latent_cost <= observed_bound(eta)` is a zero-budget
comparison even when the primary budget parameter is a rational literal.
No variable-bound primitive is required. A bound-producing network can therefore
be interpreted after fixing its observed input without granting it access to
latent source values. A uniform numerical relation can quantify over a joint
(eta,latent) domain; an action-selection statement must additionally obey its
observation contract.

The finite-observation policy tables are an initial operational scope, not a
restriction on all future neural architectures. Extending the action interface
to continuous observations would require an explicit executable/measurable
selector and the associated source-dependent expectation semantics. It is not
silently obtained by taking an infimum over hidden states. The current numerical
kernel already accommodates finite CPWA functions of declared inputs.

A research checker is a means of validating a proposed interpretation. The
chosen semantics does not require an ordinary trained network to include that
checker, logical labels or special regularizers in its architecture. Validation
of a source-conditional output and discovery of an internal mechanism remain
separate tests.

## L. A complete nonempty model, not just individually plausible assumptions

For the first example choose theta=1/2 and z1=z2=0. For the reflective example
choose p=1/2,s=e=z=w=0. For each nonlinear cell choose theta=a,q=a^2,z=0.
Every case witness is rational, satisfies all its rows, and has defined finite
term denotations. Conversions are fixed positive maps. The program versions
have finite normalized outcome distributions. Each policy is specified by a
finite visible table and never inspects a hidden case.

Renaming the examples' distinct source namespaces makes their product a joint
interpretation of all three demonstrations. No contradictory equation is needed
to reconcile the examples. This witnesses consistency of the selected semantic
fragment, not correctness of their empirical hypotheses or consistency of an
arbitrarily extended reflective theory.

An invalid join illustrates why individual witnesses are insufficient: a shared
source constrained to 0 in one context and 1 in the other has no joint witness.
The correct result is an inconsistent-source report, not an arbitrary loss
comparison justified vacuously. A numerical term can remain syntactically
well-typed even when its proposed source hypotheses cannot jointly hold.

## M. Report-dependent environmental response is an additional source question

The SELF-MIX-v1 model assumes that changing r changes branch selection but does
not otherwise change the conditional branch failure rates p,s. That premise is
stronger than having measured the old policy's failure rate. The source identity
has to cover the contemplated intervention, not merely the old observations.

For example, let the old report r0=1/2 have p0=1/2,s0=0. Its failure probability
is 1/4 and its proxy cost is 3/8. Suppose the environment responds to publishing
r1=3/4 by setting p1=s1=1. Then its failure probability is 1 and proxy cost is
19/16, an increase of 13/16. Old-policy observations alone cannot exclude this.
This is not a countermodel *inside* the fixed-p,s interpretation. It demonstrates
why an interpretation that only measures p0,s0 cannot reuse them as p1,s1 without
a cross-report premise.

The repaired signature may keep p0,s0,p1,s1 separately and supply a supported
relation between them, or keep a common structural p,s with an explicit validity
claim over the report family. In a source-mode family containing both the stable
and the responding environment, only a guarantee valid in both is unconditional
relative to that family. A numerical self-report is not its own evidence that
the environment is stationary. This is directly relevant to the performative
scope noted in Gate A, without importing a general performative-prediction theorem.

## N. The selected arithmetic has genuine loss examples, not just renamed numbers

Absolute error is native:

    |prediction-target| = max(prediction-target,target-prediction).

For a fixed rational-labeled batch, its rational weighted average remains a
native term. A fixed-label hinge expression max(0,1-y score), y in {-1,+1}, is
also native because multiplication by the label is a constant scaling. These
are direct function identities, not a claim of generalization from that batch.
Squared error and logarithmic loss are not exact primitives of this first
fragment. They require an explicit enclosure, a declared source estimate, or
the richer alternative; the quadratic example shows one such local adapter.

A useful unbounded-target check is old prediction 0 and new prediction 1. With
an unconstrained real target y, both absolute-error losses are unbounded, but

    |y-1|-|y| in [-1,1].

For y<=0 the difference is +1, for 0<=y<=1 it is 1-2y, and for y>=1 it is -1.
The source y>=1/2 narrows the difference to [-1,0]; y>=3/4 gives an improvement
of at least 1/2. Thus the same explicit ML loss calculation can yield a finite
comparison without any upper bound on the absolute error. Restricting the
source has operational content, not an assumed final-score lookup.

The numerical order is 'smaller declared cost is better'. Reading value as
minus that cost reverses the inequality: a cost budget b becomes a value-change
lower bound -b. This is an interpretation change, not discovery of one true
utility. Non-cost criteria can remain separate same-scope queries rather than
being added with arbitrary weights or incompatible units.

## O. Universal consequence does not mandate worst-case preferences

The universal quantifier in C |= q<=b expresses what follows from a modeled
source. It does not require every agent objective to be a worst-case loss.
The quantity q can itself be a declared expected loss or another aggregate
with a valid interpretation.

For example, two modeled changes -1 and +4, assigned stated weights 9/10 and
1/10, have weighted expected change -1/2. That is not a claim that the change
is at most -1/2 in each mode. If the first weight w is uncertain in [4/5,9/10]
and the two conditional changes stay fixed, the aggregate is the native affine
term 4-5w, which is at most zero throughout that weight model. The source of
those weights and their relation to actual deployment remain explicit premises.

When both the weights and conditional costs vary, their products may leave
the native CPWA fragment. Neither averaging hidden cases without a probability
premise nor replacing a mean by a supremum is a free syntactic convention.
The retained continuation/value alternative addresses that richer closure;
local enclosures offer a possible smaller representation. A robust paired
comparison was chosen for the worked self-controller, not legislated as the
only admissible interpretation of pragmatic value.

## P. Exactly which interpretation restrictions make the simple kernel honest

The signature's source names do not secretly impose numerical constraints.
Calling x a probability is not a substitute for establishing 0<=x<=1 when a
program kernel requires it. The arithmetic term H_r is defined on every real
assignment, but it is a probability interpretation only on the declared range.
Likewise a source named 'exact_square' does not automatically add q=theta^2 to
a polyhedral context. The nonlinear interpretation enters through its explicit
adapter. This prevents descriptive metadata from becoming an unrecorded premise.

A typed term can therefore be arithmetically well formed while a proposed
program interpretation fails a range, normalization or version obligation.
The three complete examples discharge those obligations explicitly. A general
front end would require corresponding supplied evidence; F05's finite audit
interpreter is not a universal verifier of arbitrary program contracts.

The rational-countermodel statement depends on the source fragment. In the
nonlinear source {x>=0, x^2=2}, the comparison x<=1 is invalid but there is no
rational feasible x. An algebraic-number or enclosure interface would be needed
to exhibit that exact source witness. The selected closed rational polyhedra
avoid this issue; it must not be silently transferred to all RLL or polynomial
model classes. This is one concrete implementation tradeoff, not a claim that
those richer classes cannot be handled.

Similarly, a logarithmic-loss adapter has to state its positive-input domain
and treatment of zero. An observation of positive probabilities at finitely
many points is not a uniform lower-bound proof. Signed infinite subtraction is
not made well defined by labeling both inputs as costs. These limitations are
visible extension obligations, rather than hidden floating-point conventions.

## Q. Reconstruction checklist before implementation

1. **Value meaning:** every main example specifies a loss interpretation, not
   a numerical truth degree. Negative budgets preserve strict improvements.
2. **Types:** constants have units; signed scalings differ from positive unit
   conversions; source identities and lexical locals are distinct.
3. **Models:** every live source case has an explicit rational feasible point.
   This is not empirical calibration and cannot be obtained by deleting bad cases.
4. **Execution:** the numerical evaluator operates on supplied hypothetical
   assignments; program selection uses only the declared observations.
5. **Composition:** shared parameters are retained before taking maxima; fixed
   mixtures are affine; variable mixtures require richer semantics or enclosures.
6. **Reflection:** the report parameter affects the very program whose rate it
   bounds, while the source relation and report family remain explicit assumptions.
7. **Revision:** weakening the discrepancy bound changes the cost guarantee;
   the independent self-report result survives. A new code version changes meaning.
8. **Comparison baseline:** being no worse than one fixed reference at each
   stage is not monotone improvement relative to the last deployed policy.
9. **Countermodels:** the model, its abstraction and actual deployment are
   different scopes; a witness must satisfy the exact source it purports to refute.
10. **Research boundary:** F06 inference rules, F07 soundness, F08 characterization,
    F09 fragment comparisons and F15 neural experiments are not declared complete.

These are same-assistant checks of the current candidate, not an independent
reviewer. The next F05 continuation should reconstruct this interpretation
interface and simplify any unnecessary structure before advancing the task.

## R. Pointwise model guarantees versus guarantees on every random execution

The reflective comparison concerns **conditional expected cost at each model**.
It is not a pathwise comparison of two random runs. Even coupling both programs
to the same U,V does not give the claimed negative bound on every run.

At p=1/2,s=0,kappa=1/4, choose U=5/8,V=3/4. The old report 1/2 chooses P and
succeeds, at cost zero. The new report 3/4 chooses S and succeeds, at cost 1/4.
This positive realized difference is compatible with the negative expected
change -1/16. A neighborhood of these draws has positive probability, so the
issue is not a measure-zero boundary convention. The intended-cost correction
is also an expected-cost model unless a stronger trajectory premise is supplied.

The loss interpretation must therefore identify whether a source is a realized
loss, a conditional expectation, or another risk statistic. Same physical units
do not make those quantities interchangeable. Universal quantification over
unknown p,s is not universal quantification over all executions U,V.

## S. Unbounded finite values are not infinity-valued arithmetic

At each assignment the selected terms have finite real values. This still permits
unbounded cost families and paired comparisons with no absolute upper bound.
It does not imply that arbitrary further expectations of those families exist
as finite numbers.

For a simple test, take a positive integer N with probabilities
Pr(N=n)=1/(n(n+1)). These sum to one by telescoping. Its expected value diverges,
since sum_n n/(n(n+1))=sum_n 1/(n+1). Old loss N+1 and new loss N have the exact
pointwise difference -1. Both individual expectations are infinite; writing
E[new]-E[old]=-1 would be undefined subtraction. The valid statements are the
pointwise comparison and E[new-old]=-1. Interchanging those statements requires
integrability or another explicitly stated convention.

The core can express the pointwise comparison on the larger linear domain N>=1;
it need not encode that discrete probability law. This example checks the meaning
of the chosen finite-valued fragment and its aggregation boundary. It is not a
claim to have implemented general infinite-horizon or heavy-tailed expectations.
A later continuation extension must preserve that boundary instead of letting
IEEE infinity arithmetic decide the logic.

## T. Finite regions explain the arithmetic semantics, not an automatic proof oracle

Reconstruct the CPWA claim directly from the syntax. A literal or source has
one affine piece. To add two terms, intersect each pair of their existing piece
guards and add the corresponding affine forms. Constant scaling and positive
conversion preserve each guard. At max(a,b), refine each joint child region by
the closed guards a>=b and b>=a and return the appropriate affine form; both
forms agree on their overlap. Min is analogous, and res(a,b) uses the guards
b-a>=0 and b-a<=0. A nonrecursive let may be expanded capture-free or evaluated
as a finite shared graph. Repeating this construction gives finitely many
rational polyhedral regions covering every source assignment.

Inside one context case and one such joint region, a comparison is an affine
inequality on a rational polyhedron. A valid proof for that region alone is not
an unconditional proof: every feasible region has to be covered, or the region
must be known from observed information. Unknown source values cannot be read
merely to choose which regional proof or action to deploy. A finite exhaustive
case proof can instead certify the same fixed goal in all regions.

Some syntactically generated regions are empty. They can be discharged by an
actual infeasibility argument; failure to find a sampled point is insufficient.
Closed guards overlap at ties, but duplicate proof cases do not double a
probability. They are a logical cover, not a probability partition. Combining
case values as an expectation would require a separately specified measure.

This construction explains why the denotation is finitely described and why a
rational countermodel is possible. It gives no claim of polynomial representation
size: the number of regions can grow rapidly. F05 does not implement this full
case compiler or its linear-validity backend. F06/F07 must select and justify
an actual rule and certificate interface; finite sampled evaluation is not a
substitute.

## U. A satisfiable self-equation is not an execution semantics for a loop

The affine equation x=(x+1)/2 has the unique solution x=1. The affine equation
x=2x-1 has the same unique solution. Both can be expressed as pairs of source
inequalities with the rational witness 1. Yet starting from 0, the first
iteration converges to 1 and the second gives -1,-3,-7,... . Satisfiability and
uniqueness of a relational source description do not prove that an iterative
program computes its solution.

The contradiction x=x+1 has no source witness; the tautology x=x has all real
witnesses and determines no unique value. These examples distinguish consistency,
information and dynamic computation. The selected finite expression evaluator
cannot silently execute a cyclic source definition by recursively looking up its
own name. Such a key denotes an unknown value constrained by the source model.
An actual cyclic program needs its own fixed-point/partial/limiting operational
contract before that value can describe its result.

The SELF-MIX example avoids assuming a solved recursive evaluator: it emits a
specified report, uses it in a finite probabilistic program, and assesses the
rate of that same program. Its behavioral feedback is genuine, while unrestricted
intensional reflection or convergence of arbitrary loops remains unclaimed.
This keeps the initial fragment modest without banning future cyclic extensions.

## V. Substitution needs domain transport, not just matching units

The evaluation substitution lemma assumes unchanged operator/conversion meanings
and closed source replacements. In its let case, the substituted right-hand side
has the same value by induction; bind the local name to that value in both
environments and apply the induction hypothesis to the body. Closed source
replacements do not consult the local environment, so lexical shadowing cannot
change their interpretation. A changed conversion factor requires a separate
transport, not this lemma.

Even a denotation-preserving substitution need not preserve the *old hypotheses*.
On the source y>=0 the comparison |y|<=y holds. Substitute y=-x and take the new
source 0<=x<=1. The resulting |x|<=-x fails at x=1, despite matching units and
perfectly defined arithmetic. With the new source -1<=x<=0, the substitution's
image instead satisfies y>=0 and the comparison transfers correctly.

This reconstructs the exact role of the map D_new->D_old. In a composed program
it includes proving that the preceding stage reaches the next stage's admitted
input domain. An output's unit or interface name alone is not that proof. It also
explains why a bound checked only on the nominal inputs cannot automatically be
used on a perturbation tube or changed deployment source.

## W. The distinction between model comparison and the source of its warrant

A conditional comparison can use source inequalities more than once without
claiming more independent data. For instance x<=1 supports 2x<=2, not 2x<=1.
The numerical contribution doubles; the evidence record does not become two
independent confidence events. Conversely, subtracting an upper bound is not an
upper-bound rule: x<=1 alone gives -x>=-1, and x=0 refutes -x<=-1. Negative
scaling is a valid term operation but not covariance of every consequence rule.

These small sign and multiplicity checks are important before F06: the context
of source hypotheses is not a bag of costs automatically consumed by RLL-style
addition. Source-premise reuse and quantitative spending are different roles.
A future proof system must specify its structural rules instead of importing
contraction or resource counting from a superficial notational resemblance.

The primary source-aware comparison remains informative despite this separation:
it derives a new composite quantity from shared local premises, carries the
conditions under which that derivation applies, and can be rechecked after
specified changes. It does not claim that metadata makes an empirically wrong
premise true, or that every plausible value function has already been captured.

## X. A direct loss-plus-resource specialization and a utility-unit limit

The absolute-error example can include an explicit use cost. Let y>=3/4,
0<=c<=1/4 and z>=0 in the declared converted loss units, and define

    J_old=|y|+z,
    J_new=|y-1|+c+z.

The piecewise calculation in N gives |y-1|-|y|<=-1/2, hence the total increase
is at most -1/4. The point y=3/4,c=1/4,z=0 attains this bound. Both absolute
costs remain unbounded as y or z grows. This is a genuine named loss plus a
resource term, with the resource price and source range stated, not a score
attached to a truth judgment after the fact.

A quantitative budget across different utility hypotheses needs a common
meaningful scale. Two criteria cannot be made commensurable just by giving both
a field called 'utility'. The source-mode examples assume one declared criterion
and unit across their alternative models. Different criteria can instead be
kept as separate tagged goals, each with its own budget, or joined only through
an explicit chosen conversion/normalization. Zero-budget dominance is less
sensitive to positive rescaling, but a claimed uniform improvement magnitude is
not scale-free. The first scalar fragment does not settle that broader choice.

## Y. Arithmetic reconstruction table

| Check | Direct reconstruction | Consequence |
|---|---|---|
| Shared composition | (theta-3/4)+(1/4-theta)=-1/2 | Paired structure yields improvement despite loose separate bounds. |
| Old self-report | H_(1/2)-1/2=s-1/4<=0 | Valid but actual failure is still unknown. |
| New self-report | H_(3/4)-3/4=s-5/8<=-3/8 | Valid independently of the discrepancy bound. |
| Proxy change | (1/4)(s-p+1/4)=-1/16 | Same two program versions and same source are required. |
| Intended change | -1/16+e<=-1/32 | Uses e<=1/32, not self-endorsement. |
| Weakened evidence | -1/16+3/64=-1/64 | Original stronger bound is stale, not the self-report result. |
| Reversed program | (1/4)(p-s-1/4)=+1/16 | Same report numbers do not identify the behavior. |
| Four-cell enclosure | U4-theta^2 in [0,1/256] | Component-local assumption has an explicit analytic justification. |
| Paired quadratic use | max(U4-theta)=-3/16 | Exact useful bound does not require exact component recovery. |
| Absolute-error plus resource | |y-1|-|y|+c<=-1/4 | The core admits a direct loss/resource interpretation. |

The proofs of the universal rows are in the preceding sections; numerical fixture
checks will exercise these interpretations and invalid variants separately.
This table is not itself a substitute for those proofs or for the forthcoming
rule-system soundness task.

## Z. Admissibility stress test: probability normalization affects the bound

As a final reconstruction of the source-domain choice, allow uncertain branch
gap d=p-s with 0<=d_L<=d<=d_U<=1 and 0<=s<=S<=1, retaining p=s+d<=1.
The source is nonempty (s=0,d=d_L is feasible). For a fixed report r in [0,1],

    H_r=s+(1-r)d.

At a given d the worst feasible s is min(S,1-d). Therefore the worst rate is the
maximum of min(S,1-d)+(1-r)d over [d_L,d_U]. Below d=1-S its slope is 1-r>=0;
above that point its slope is -r<=0. Let d* be 1-S clipped to [d_L,d_U]. Then

    H_max(r)=min(S,1-d*)+(1-r)d*.

Solving H_max(r)<=r gives the least valid report

    (S+d_U)/(1+d_U)   if d_U<=1-S,
    1/(1+d_L)         if d_L>=1-S,
    1/(2-S)           otherwise.

The formulas agree at the boundaries. They also give the correct endpoint
maxima for r=0 and r=1, where there may be more than one maximizing d. This
checks the exact operational range constraints, not a generic fixed-point solver.
The main example S=1/4,d_L=d_U=1/2 recovers r*=1/2.

For S=3/4,d_L=1/4,d_U=1/2 the actual least report is 4/5. Ignoring p<=1 would
combine s=3/4 and d=1/2 into the impossible probability p=5/4 and produce the
looser threshold 5/6. That outer bound is conservative, but claiming it is the
exact least report would be wrong. A numerical counterexample outside the valid
probability domain cannot refute the normalized program interpretation.

With a resource price kappa in a declared interval and fixed r1>=r0, the paired
proxy change is (r1-r0)(kappa-d). Its rectangular upper bound uses kappa_U and
d_L, not necessarily the source point maximizing H. Thus one scalar 'worst
model' need not simultaneously realize all questions. Preserving the source
relation lets different valid certificates answer different queries for the
same fixed program without giving the program hidden information.


## AA. Final domain and binding reconstruction before implementation

The hiding example needs an explicit common visible-domain premise. Write
Gamma={0<=x=y<=1} and Delta={0<=x<=1,y=0}. Separately, both project to [0,1]
on x. Jointly they project to {0}. If Delta were written merely y=0 without
the x-domain premise, its separate projection would instead be the entire
real line. The obstruction still exists, but the claim of equal projections
would be false. The main note now states both domains explicitly. This is a
same-session correction to an example, not a modification of historical research.

Lexical bindings can have a unit different from the final body: a time-valued
local may be converted before appearing in a cost-valued body. The precise
production is `let y_v=t_v in body_u`; the unit of the entire let is u. Sources
and locals remain separate namespaces, and the right-hand side is evaluated
before the new local enters scope. Thus `let y=loc(y)+1 in loc(y)` can use an
outer y but is not a recursive reference to the new y. A closed outermost
instance without that outer binding is rejected. This resolves an unnecessary
same-unit restriction in the preliminary grammar without altering any numerical
operation or license conclusion.

For each case in a finite context, a feasible witness checks all declared source
coordinates and every row, including probability normalization and unit typing.
Checking a single example witness never proves the target comparison. Conversely,
a witness violating the target refutes the universal statement only if it belongs
to that same versioned context. A point outside the context, a source-name typo,
an invalid probability, or an undeclared conversion is not a countermodel.
The executable fixture should therefore return a distinct malformed-input error,
not a Boolean false result that can be mistaken for a mathematical refutation.

The small evaluator may evaluate rational supplied points exactly, while the
specified semantics quantifies over reals. The rational-countermodel lemma is
justified by the rational polyhedral/CPWA assumptions, not by finite enumeration.
No test grid or one-sided derivative routine is made a global validity oracle.

## AB. Signed budgets require more than a nonexpansive downstream map

One-sided bounds for nonnegative error budgets must not be copied unchanged to
negative improvement budgets. Set t=-2,s=-1, so t-s=-1. ReLU is monotone and
1-Lipschitz, but ReLU(t)-ReLU(s)=0, not <=-1. Both become the same inactive
value. For nonnegative input costs, use a saturating CPWA map F(x)=min(x,1):
t=2,s=3 again gives input difference -1 and output difference zero. Hence the
boundary is not an artifact of permitting negative absolute losses.

The sufficient extra premise for retaining strict improvement is a positive
lower gain on the relevant domain, not only an upper sensitivity. Suppose for
all a<=b in the reached interval,

    m(b-a) <= F(b)-F(a) <= L(b-a),  with 0<=m<=L.

If t-s<=b0<0, then t<s and

    F(t)-F(s) <= m(t-s) <= m b0.

If t-s<=b0 with b0>=0, split into t<=s and t>s. The former gives a nonpositive
output change; the latter gives at most L(t-s)<=L b0. The sharp uniform envelope
from these hypotheses is consequently m*b0 for negative b0 and L*b0 for
nonnegative b0. Linear maps with slopes m and L attain the corresponding cases.
For a ReLU crossing or inactive interval, m=0, so no strict improvement survives
from this information alone. On an entirely active interval, m=L=1. A domain
premise can thus make the same arithmetic map informative for one use and
uninformative for another, without changing its syntax.

For the concrete source x<=-1, compare x-1 with x before and after ReLU. The
input improvement is exactly one, and the downstream quantities are identically
zero. With source x>=1, the same replacement remains on the active part only
when x-1>=0 (which holds here), and the output difference is exactly -1.
These examples give F06 a necessary discrimination test. They do not install a
new general inference rule during F05 or claim universal positive lower gains.

This also protects the distinction between proxy and value. A task can saturate
once an accuracy requirement is met, so an improved numerical proxy may cease
to yield a strict improvement in the chosen task value. The pointwise cost
interpretation and its domain, rather than the word 'improvement', determine
whether the stronger conclusion is warranted.

## AC. Shared uncertainty is not stochastic independence

Two uses of the Bernoulli primitive share the same unknown parameter theta.
This does not decide whether their internal draws are independent. Conditional
independence gives expected conjunction cost theta^2. If instead both uses read
the same Bernoulli draw, the conjunction has expectation theta. At theta=1/2,
the respective costs are 1/4 and 1/2. The latter has no improvement over a single
use and is a countermodel to the unqualified quadratic adapter, not to the
adapter with its declared conditional-independence premise.

The appropriate interpretation record must therefore name the joint execution
kernel, not just two matching marginal success rates. Unknown-but-common theta
is preserved across components; independence, when actually supplied, describes
draws conditional on that theta. It is not licensed by creating two source keys,
and sharing a source key does not force the draws to coincide. This gives a small
positive and negative operational check for the nonlinear example.

By contrast the subtraction of two EXPECTED policy costs does not require
independent random draws between policies. If both expectations are defined,
any coupling of their random executions has the same expected difference.
Their pathwise deterioration can change with the coupling, as the earlier
trajectory witness shows. The first core compares conditional expected costs
and should neither impose an unnecessary cross-policy independence premise nor
pretend to have established a pathwise guarantee. The underlying source model
for the two expectations must still refer to the intended populations and code.

An even stronger model-changing update, where deploying a report changes the
branch risks themselves, needs versioned counterfactual risk coordinates or a
joint response function. Separate one-policy calibration records alone do not
assert the common report-family response needed by the worked reflection model.
This is why the program interpretation, source set, and proxy correspondence
all remain explicit parts of a conditional warrant.

## AD. Boundary between evaluating an expression and selecting its syntax

A policy table may contain r=3/4 as a literal, and its interpreted cost is then
a native affine term. This does not mean the native language can compute
p/(1+p-s) as a function of hidden p,s. That ratio is a metalevel solution of the
self-report problem, with a separate deployability question. When a finite
visible evidence table supplies rational interval endpoints, a rational
threshold can be computed outside the current numeric syntax and entered as a
named program parameter. The parameter's warrant still needs the corresponding
source argument. Arbitrary real evidence-to-policy maps have not thereby been
made native operations.

Similarly, F05's polyhedral sources can name a component output q only under
explicit inequalities linking q to inputs and evidence. The fixture must not
have a primitive named 'true_value' or 'optimal_policy' whose supplied output is
treated as proof of the final goal. The quadratic adapter is acceptable precisely
because its independent component enclosure is displayed and justified before
the comparison; it is not a premise q-theta<=-3/16 inserted merely to obtain the
same conclusion. The report kernel is likewise derived from explicit branch
probabilities and charges, not from the emitted report's own authority.

For the first pass, success is a consistent, nonempty, typed semantic interface
with executable hypothetical models and discriminating countermodels. It is not
closure under every controller, an implemented decision procedure, or a theorem
that all hidden neural quantities possess the proposed interpretation. Those
stronger claims remain separately falsifiable obligations for later tasks.

## AE. Final nonvacuity and scope check for the reflective interpretation

At p=1/2,s=0,z=w=0 and e=1/32, both branch probabilities are legitimate,
both reports satisfy their own conditional kernel, and the intended old/new
costs are 3/8 and 11/32. Their difference is -1/32, so the claimed margin is
attained in an admitted model, not obtained by inconsistent assumptions. At
p=3/4,s=1/4 the report 1/2 is exactly tight, independently of the value of e.
Thus the model set permits both boundary and interior behavior and has genuinely
uncertain actual failure despite robust report validity.

After the explicit weakening e<=3/64, the point p=1/2,s=0,z=w=0,e=3/64 has
new intended cost 23/64 and old cost 24/64. This refutes the old -2/64 margin
while attaining the new -1/64 margin. The report H_(3/4)=1/8 is unaffected.
The same calculation witnesses why a single undifferentiated 'valid result'
flag would lose a distinction that the revision interface actually needs.

Neither this example nor the nonnegative unit-event example presupposes a
final theory of truth. They do presuppose precise declared stochastic and
arithmetic meanings. Revisability concerns those meanings and their evidence;
it is not permission to equivocate about them inside one derivation. The first
core is therefore modest about its source of warrant while still exact about
what the conditional statement says.

The finite-pair bridge also survives noncanonical pair lifts: replacing any
source pair (a,b) by (a+c,b+c), c>=0 finite, leaves its signed denotation
unchanged, and structural induction leaves every translated term and comparison
unchanged. For t=s and budget -1, the translated inequality has an additional
unit on its left side and correctly fails. A clipped shortfall instead returns
zero and cannot encode that distinction. Thus negative budgets are retained by
pair arithmetic, not recovered from a confidence label or a zero-shortfall flag.
