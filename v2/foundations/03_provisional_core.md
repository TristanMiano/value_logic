# F05 — a provisional source-aware calculus of loss comparisons

Status: **provisional first pass; F05 partial**. This is the selected development
candidate, not a completed proof calculus. Source baseline:
`a95f4a06efe2b181f9001017e3c4908131fddf50`. Gate A remains passed only at its
readiness scope. The alternative is source-preserving continuation semantics.

## 1. The choice and its purpose

Choose a finite, typed, source-indexed language of **modeled loss expressions**.
A judgment compares two such expressions over an explicitly stated joint model
of the unknown quantities. Numerical values are finite signed reals at each
interpretation; their range over interpretations can be unbounded in either
direction. A nonnegative physical or prediction loss is a useful subclass,
not a restriction on all comparisons or value representations.

The primitive operational question is:

> With this information, does replacing the specified old use by the specified
> new use increase the declared cost by at most b, and under what assumptions?

It is not whether an expression has b degrees of truth. Cost is a chosen,
revisable proxy for practical value. An intended cost and an accessible proxy
may both remain uncertain. Neither the number nor its formal derivation is
identified with ultimate utility or target-world truth.

The selected exact term fragment is rational continuous piecewise-affine
(CPWA) arithmetic. Its reasons are finite syntax, exact rational finite checks,
explicit shared dependence, and a direct candidate interface to ReLU-computable
bounds. These are pragmatic development reasons, not a theorem that this
fragment is uniquely appropriate. It is **not** full Rational Lawvere Logic
(RLL): variable multiplication, division, infinity-valued terms and RLL's full
deduction system have not been adopted. The residual mechanism is retained;
its numerical interpretation receives a cost meaning here.

F05 specifies typing, interpretations, evaluation, semantic consequence,
countermodels, source changes and three complete model-use examples. F06 must
still select an actual deductive rule system; F07 must prove its soundness;
F08 must establish a worthwhile characterization. The semantic relation below
is not defined by an implementation's acceptance or by derivability.

## 2. Units, source identities and scope

A unit u denotes a copy R_u of the ordered real line. Units can be concrete
(e.g. seconds) or task-relative (e.g. a particular weighted-loss unit). Add,
subtract, compare, min and max only within one unit. A rational scalar has no
units. A change of unit is a **named conversion** carrying a fixed positive rational
factor and its source/target units; it is not silent coercion. A task changing
its weights or criterion changes the scope, not merely the presentation.

A signature Sigma contains:

* finitely many unique source keys, each with a unit;
* a finite conversion table, and
* the versioned interpretation scope for the plans, loss evaluators and modeled
  population to which these keys refer.

A source key is semantic identity, not a bare display name. Two occurrences of
one key mean the same unknown quantity. Two keys with the same spelling but
different population/evaluator identities are different coordinates. They may
be compared when both are declared, but equality/correlation then requires a
premise; it is not supplied by their names. A reference to an undeclared key
is ill-typed, not an unknown number that can be filled with zero.

Keep **evidence revision** distinct from **quantity identity**. A tighter
interval for the same fixed-population risk can update the evidence while
retaining its source key. A different deployed program, target population or
loss meaning needs a new scope/key or an explicit cross-scope transport.
Certificates record the scope and evidence revision they actually use.

This is a small interface, not a demand to encode a universal ontology. For
example the reflective case needs keys p,s,e,z, their units, a fixed controller
version and a criterion identity. The finite keys do not purport to exhaust
all relevant real-world uncertainty.

## 3. Terms and their evaluation

For each unit u use the grammar

    t_u ::= q_u | src(x_u) | loc(y_u) | t_u + t_u | a t_u | min(t_u,t_u)
          | max(t_u,t_u) | res(t_u,t_u) | let y_v=t_v in t_u
          | convert_c(t_v)

where q,a are rational, x is a declared source, y is a lexical local, let is nonrecursive,
and c:v->u is a declared positive rational conversion. Negative a is permitted. Define

    res(a,b) = max(b-a,0).

Thus res(old,new) is nonnegative deterioration, while **new-old remains a
signed difference**. Minus and absolute value are abbreviations. All nodes are
finite; a shared-expression DAG must be acyclic. This restriction is on the
arithmetic evaluator, not a global prohibition of self-assessment or
report-dependent behavior.

### 3.1 Denotation

An assignment nu maps each source x_u to a finite real in R_u. Interpret a
literal and source directly; interpret arithmetic pointwise; evaluate a let
body with its local variable bound to the value of its right-hand side. A
conversion applies its declared factor. Every well-typed finite term has a
unique finite denotation [[t]]_nu. Structural induction proves existence and
uniqueness: source and literal leaves are defined, each operation is a total
function of already-defined finite arguments, and a let extends the lexical
environment once without recursion. There is no infinity-minus-infinity case.

The same induction, refining finitely many polyhedral cells at min/max/res
nodes and substituting at lets, makes each term a finite CPWA function of its
source coordinates. This statement uses rational coefficients in the selected
syntax. It is not the converse neural representation theorem and not a proof
of soundness for an unchosen deductive system.

### 3.2 Operational evaluation

The mathematical evaluator has configurations <t,nu,rho>, with rho a lexical
let environment. Leaves reduce to their lookup or literal values. Evaluate
children left-to-right; when all children are numerical literals, replace the
node by the corresponding arithmetic result. Reduce `let y=t in b` by first
evaluating t, then evaluating b in rho[y:=value]. Conversions look up their
fixed table entry. Acyclic expression graphs may memoize node values, but the cache must respect
lexical binding instances/environments; syntax-node identity alone is insufficient.

Induction on the finite syntax shows this evaluator terminates, is deterministic,
and returns [[t]]_nu. The evaluator is a way to check a **supplied hypothetical
model assignment**. It does not give the agent read access to hidden nu. A
symbolic inference can be useful precisely because that assignment is unknown.
There is no `sup`, `optimizer`, `oracle_value` or final-answer lookup primitive
in the term language. A finite rational executable evaluator will test this
contract; its finite tests are not a decision procedure for real validity.

Duplicating a term duplicates its numerical contribution: t+t is 2t. Reusing
an evidence record is not a second independent observation. Expression sharing,
quantity correlation, computation cost and statistical independence are separate
concepts and need separate statements where relevant.

## 4. Contexts: uncertainty without a mystery scalar

At a fixed visible observation o, let the source domain be

    D_C(o) = union_{h in H_o} { (h,x) : A_(o,h) x <= eta_(o,h) }.

Here H_o is finite and nonempty; h is a hidden mode, x contains the declared
source coordinates, and each case is a closed rational polyhedron with a
supplied rational feasible witness. A row is a same-unit affine inequality
under Sigma. Coordinates, offsets and coefficients are expressed in the declared
units before their numerical matrix form is used. Unbounded polyhedra are allowed.
The examples use small case sets, often one case.

A context C contains Sigma, these cases, a visible observation identifier, an
evidence revision and records of the hypotheses supporting its rows. The rows
are provisional assumptions about modeled quantities. Their actual empirical
validity is not inferred from feasibility or arithmetic consistency.

A common finite source signature can encode case-local variables by unused
coordinates. A hidden mode may assign different cost terms to one fixed program;
this is an interpretation table, not an action available to the agent. Each
case's local definitions must be explicitly versioned and typed. A fixed term
is a particularly simple case-independent interpretation.

A purported deployment context with no possible case is rejected as
**inconsistent evidence**. Ordinary implication over an empty set would be
vacuously true; it is not a warrant for an action. This provisional convention
requires a witness for every retained live case. An empty case can only be
removed with an explicit justification, not because proof search failed or a
sample did not visit it. F05 does not implement a general feasibility solver.

Absence of a bound is represented by absence of a constraining row, allowing
more assignments. A partially informative context remains meaningful. Its
failure to establish a comparison is not a proof of the opposite comparison.
Conflicting data can be retained as separately declared possible cases where
appropriate; contradictory inequalities in one case are not silently averaged.

## 5. Semantic judgments and countermodels

The primary comparison, with b a finite rational quantity in the same unit, is

    C |= t <=_b s : u
        iff for every (h,x) in D_C(o), [[t_h]]_x - [[s_h]]_x <= b.

Read t as the new cost and s as the old cost. A negative b is a guaranteed
improvement of at least -b; b=0 is non-deterioration; positive b is a permitted
increase. An absolute adequacy statement is the special comparison t <=_b 0,
not a consequence of any relative improvement statement alone.

A countermodel is a retained case h and a feasible assignment x for which
[[t_h]]_x-[[s_h]]_x>b. It is a counterexample **inside the declared model**,
not evidence that one of the hypotheses is actually true of deployment. A
mismatched type/scope is not a countermodel; it is a malformed judgment.

For a nonempty context define the quantitative summary

    B_C(t,s) = sup_{(h,x) in D_C(o)} ( [[t_h]]_x-[[s_h]]_x ).

This is a metalevel extended-real bound, not a term or a truth value. Since the
context is nonempty and differences are finite pointwise, B lies in
R union {+infinity}, not -infinity. It can be infinite even when every term is
finite. Then no finite b suffices. Its definition gives the mathematical target
for a reasoner, not permission to assume the result as an input premise.

Derived shortfall is

    S_C(t,s) = sup res(s,t) = max(B_C(t,s),0).

For b>=0, t <=_b s is equivalent to S_C(t,s)<=b. For b<0 it is not: clipping
forgets improvement magnitude. In particular t=s has shortfall zero but never
satisfies t <=_{-1} s. This is why the signed comparison is retained alongside
the Lawvere-style nonnegative residual.

We also use the pointwise enclosure judgment

    C |= lower <= t <= upper

and the semantic equality t =_C s (both zero-budget comparisons). Equality on
one context does not mean identical syntax, identical evidence, equal operation
cost, or equality after every future change of source assumptions.

## 6. Plans, observations and the action quantifiers

The numerical syntax does not by itself name available actions. A finite plan
registry separately records executable program versions and their **component**
loss interpretations. The three examples below spell these out rather than
introducing a primitive returning the final comparison.

Let O be a finite visible observation alphabet. A permitted policy pi is a finite
table from O to available program versions or rational lotteries over them.
At one visible o, its choice is fixed across every hidden mode h and assignment
x consistent with o. Its interpreted cost term can depend on x; its action
selection cannot, unless x is actually provided by the declared observation
interface. A source variable in a loss formula is not an observed input simply
because the formula mentions it.

`C |= Cost(pi_new) <=_b Cost(pi_old)` compares the **same two policies** in every
retained possibility. It can feed a later reliance/selection interface together
with explicit requirements. F05 does not derive unconditional authorization,
absolute safety, or the best possible policy from this comparison.

The existence question would be

    exists permitted pi, for all (h,x) consistent with o: Cost(pi,h,x)<=b,

not `for all (h,x), exists an action`. Consider two hidden modes with cost pairs
(A,B)=(0,2) and (2,0). Their pointwise minimum is zero in both modes. Neither
constant action attains that bound. A lottery placing q on A costs 2(1-q) in
one mode and 2q in the other, so its worst cost is at least 1. Revealing the
mode changes the observation interface and permits a contingent zero-cost
policy; numerical manipulation alone does not reveal it.

`min(t,s)` remains a legitimate value expression, and minimum of two bounds
on **one fixed query** remains useful. Neither operation silently creates a
plan. Likewise a proof can split on all possible hidden modes and use a
different certificate in each branch while certifying the same fixed policy.
Case-dependent proof witnesses do not license case-dependent deployment.

## 7. What composition means

### 7.1 Pointwise expression composition

Terms share one assignment before any reduction to worst-case bounds. For
example d1(x)+d2(x) is evaluated using the same x. Replacing that by the sum of
two independent suprema is a sound upper approximation, not the definition of
composition and not generally exact.

With unchanged operator and conversion meanings, substitute a same-unit closed
source term sigma(x) for each selected source. Substitution is capture-avoiding: sources and lexical locals are different name classes.
Induction on syntax yields

    [[t[sigma]]]_(nu') = [[t]]_(nu' evaluated through sigma).

For a let, rename its local binder to avoid capturing any local free name before
substitution, or restrict substitutions to closed source terms as we do in the
fixture. This lemma specifies evaluation; a comparison transfers only if the
new source domain maps into the old one. Arbitrary replacement of a source by a
same-unit expression is well-typed but need not preserve its old evidence.

Constant-probability mixture is arithmetic sugar:

    Mix((q_i,t_i)_i) = sum_i q_i t_i,  q_i>=0, sum_i q_i=1.

Its expected-cost interpretation requires the declared policy/randomness model.
The arithmetic alone does not certify that model. Variable-probability mixtures
can leave CPWA: probability theta followed by cost theta gives theta^2. This
is the exact-native-closure limit of the chosen fragment, not a limitation of
all RLL or a claim that such computations are impossible.

### 7.2 Joining sources, rather than inventing independence

For compatible signatures Sigma1,Sigma2, the exact joint context has assignments
whose restrictions satisfy both input contexts. Shared source keys identify the
same coordinate. Distinct keys are not identified. Hidden-case compatibility
is an explicit finite relation when supplied; retaining all pairs is an
outer approximation of that relation, not a probability-independence assumption.

Even two nonempty contexts can have an empty join: one may require a shared
quantity theta=0, the other theta=1. A joint witness is therefore a separate
obligation. Evidence from the two contexts cannot be combined into a deployment
warrant solely because each context was nonempty.

If a sum represents a sequential computation's total loss, its local component
interpretation must justify that sum (e.g. additive charges). Combining two
already-granted component labels is not a composition semantics.

### 7.3 Hiding a source

If a query depends only on X, exact hiding of Y is existential projection:

    D_hidden = {x : exists y, (x,y) in D_C}.

The universal comparison on X is unchanged: every original point projects into
the hidden domain, and every hidden point has a witness in the original domain.
Deleting rows mentioning Y is generally only a weaker approximation. From
x=y and y<=0 the exact projection retains x<=0; deleting both rows loses it.

Hiding need not commute with later evidence combination. If Gamma says
0<=x=y<=1 and Delta says 0<=x<=1,y=0, both separately project to all x in [0,1], but
their joint context projects to x=0. A summary sufficient for current queries
cannot automatically absorb every later observation. Either keep the needed
relation or state the allowed-update contract of the summary.

## 8. Evidence revision and source transport

A cached result binds the complete meaning of its context, query terms, plan
versions and criterion. A context fingerprint is a practical identity check,
not an empirical-validity proof. No automatic reuse occurs after a fingerprint
change; explicit semantic transport can nevertheless justify reuse.

**Restriction.** For unchanged source meanings and terms, D_new subset D_old
preserves every old universal comparison. This follows by restricting the
quantifier. An implementation may verify this by explicit row inclusion or a
supplied implication certificate; it must not infer it from a revision number.

**General transport.** A map phi:D_new->D_old plus a correction expression e
can justify a new paired query if, for all nu' in D_new,

    t_new(nu')-s_new(nu')
      <= t_old(phi(nu'))-s_old(phi(nu'))+e(nu').

An old b and a checked upper bound e<=delta then give b+delta. This is a
semantic interface condition, not a new primitive that returns an unverified
final answer. Its two component obligations must be derived or supplied under
a named assumption mode. No individual absolute loss need be bounded.

A weakening of source evidence, a new population, or a change of loss weights
can fail restriction. A query-specific proof can still survive, but the missing
premise must be checked. Numerically invertible right-hand-side recoding is
not enough: x<=1,y<=2 implies x+y<=3,y<=2, but the latter permits x=3,y=0.
Correct coordinate transport also transforms the admissible relation and query.

The distinct transitions are therefore:

| Change | Permitted interpretation |
|---|---|
| More evidence on the same quantities | Restrict the same model set when genuinely justified. |
| Weaker/withdrawn evidence | Enlarge or replace the set; recheck the old query, or transport with a correction. |
| New quantity or evaluator version | New source identity and explicit relationship, not name-based substitution. |
| New task or loss weights | New cost expression/criterion; an old comparison does not transfer by its units alone. |
| More visible information | A larger policy interface; the old policy may ignore it, but hidden facts do not become visible by a proof. |
| Equivalent coordinate description | Transform the source relation and cost interpretation together. |

History/provenance is append-only in the external research/evidence record;
current conditional conclusions can cease to apply after assumptions change.
No fixed finite library is declared complete. A new model or evidence mode may
be added with a new interpretation and new comparison obligations. Open-ended
succession is supported at this finite-stage interface, not asserted to converge.

## 9. Proxies, evidence modes and uncertainty about the evaluator

Let L_pi be a proxy cost and J_pi an intended cost, with a declared positive
conversion alpha from proxy units to intended units. Define a model discrepancy
E_pi = J_pi-alpha L_pi. A paired premise is

    C |= E_new <=_beta E_old.

It combines with a proxy bound L_new-L_old<=b to give the intended bound
alpha b+beta. This is direct addition of the two same-world differences.
E_old and E_new need not have bounded absolute values; their *difference*
is what this judgment needs. The alignment premise is not generated by low
training loss, a neural confidence score, or the evaluator's endorsement.
Different plausible criteria can be retained as distinct mode-tagged judgments,
without silently inventing a universally correct scalar utility.

Source rows carry provenance and an evidence mode. A formal mode concerns a
conditional mathematical statement; a statistical mode concerns a sampling law
and a coverage event; a learned proposal by itself supplies neither. The
calculus does not turn these into one generic scalar confidence.

For precision, suppose data d determine a context C_d and a permitted policy
pi(d). Suppose a separately established event E has probability at least
1-alpha and, on E, the actual modeled quantities lie in D_(C_d). If a conditional
comparison is valid throughout D_(C_d) for every d, it holds for the selected
policy on E. The probability of its violation is therefore at most alpha.
The proof is event inclusion, not a new statistical calibration procedure.
This accommodates data-dependent choice **only with the stated common coverage
event**. Per-fixed-policy validity does not automatically supply that event.
For distinct required events, the sum of their failure bounds is a conservative
union-bound alternative; independence is not presumed. Duplicating one record
does not create a second independent event or reduce its failure probability.

Uncertainty about an evaluator can be represented by alternative source models
for its behavior, or by an uncertain discrepancy. A statement about its own
versioned output is then just another scoped modeled quantity. Formal checking
still takes place in an explicitly chosen ordinary metatheory; the agent may
remain uncertain whether its empirical bridge or checker implementation meets
that metatheory's hypotheses. We do not add `I predict success -> success` or
unrestricted proof reflection. The worked self-report case below is genuine
behavioral feedback, but does not claim those stronger principles.

## 10. Complete interpretation I — shared-source composition

Use one loss unit U. The modeled quantities are theta,z1,z2, with
0<=theta<=1 and z1,z2>=0. All constants in this paragraph carry U unless they
multiply a term. The two fixed program versions have two additive-cost stages:

    old: (z1+3/4, z2+theta)
    new: (z1+theta, z2+1/4).

Their loss model explicitly says to sum the stage costs. It is not inferred
from component permission labels. The individual differences are

    d1=theta-3/4,    d2=1/4-theta.

Each has upper bound 1/4, at opposite endpoints. The complete loss expressions
share the same theta and give

    (z1+theta + z2+1/4) - (z1+3/4 + z2+theta) = -1/2.

Thus the new use improves loss by exactly 1/2 throughout the context. A feasible
interpretation is theta=1/2,z1=z2=0: old cost 5/4 and new cost 3/4. Both loss
families are nonnegative and unbounded above as the baselines increase. The
comparison does not give an absolute adequacy bound.

A hostile interpretation with **different** source keys theta1 and theta2,
both in [0,1], changes the difference to theta1-theta2-1/2. At theta1=1,
theta2=0 it is +1/2. Nothing in equal marginal ranges or similar source names
licenses identifying the two variables. This is a countermodel to that source-
merging inference, not a countermodel to the original shared-source theorem.

A later evidence restriction theta in [1/4,3/4] preserves the exact paired
answer. Forgetting the common key before summing retains only the loose bound
+1/2. The term evaluator has explicit stage inputs and operations in both cases;
no primitive contains a precomputed final comparison.

## 11. Complete interpretation II — the evaluator's own report changes its use

The program `SELF-MIX-v1(r)` emits its own reported upper failure bound r and
uses that same rational r in its behavior. It draws U uniformly from [0,1];
if U<r it executes branch S, otherwise branch P. A fresh uniform V determines
failure using the selected branch's unknown failure probability s or p.
The independent random draws are conditional on a fixed (p,s). The program
never observes these unknown probabilities before its choice.

The source interpretation, conditional on valid probability ranges and the
stated report-family model, therefore gives

    H_r=(1-r)p+r s

for this program's own failure probability. A branch-S execution costs kappa=1/4
loss units in addition to one unit per failure. With a common unknown baseline z,

    L_r=z + iota(H_r) + kappa r,

where iota converts a probability to expected loss at one U per failure.
H_r is in the dimensionless/probability unit; L_r is in U. For a fixed rational
r both are native affine terms. This is an explicit stochastic program model,
not a callback returning the answer to the final judgment.

The joint source assumptions are

    0<=s<=1/4,  p-s=1/2,  0<=p<=1,
    z>=0, w>=0,  -1/32<=e<=1/32.

The lower bound on e and the baseline lower bounds make a nonnegative-loss
interpretation available. The comparison below needs only the upper bound on e.
The two named intended-cost interpretations are

    J_old=L_(1/2)+w,
    J_new=L_(3/4)+w+e.

Here e is the **paired discrepancy**, not a known global utility correction.
These definitions permit uncertainty about the intended criterion while making
its assumed relation to the proxy explicit. The context asserts neither that
this criterion is ultimate utility nor that the e-bound is empirically verified.

### 11.1 Nontrivial uncertain self-assessment

The source correlation gives

    H_r=s+1/2-r/2,     H_r-r=s+1/2-3r/2.

At r0=1/2, the shortfall is s-1/4<=0. At r1=3/4 it is
s-5/8<=-3/8. Both reports are valid throughout the same source model. Their
actual failure probabilities remain intervals, respectively [1/4,1/2] and
[1/8,3/8]. A valid upper report is not an exact prediction of its own outcome.

At r=2/5 the actual rate is s+3/10, ranging from 3/10 to 11/20. The report
holds at p=1/2,s=0 and fails at p=3/4,s=1/4. The universal warrant is false,
but the actual report is **not uniformly false**. This distinguishes a modeled
counterexample, uncertainty about the actual case, and failure to find a proof.
The calculus does not trust the report simply because SELF-MIX emits it.

### 11.2 A paired intended-loss conclusion

Because both costs describe the same model and same two program parameters,

    L_new-L_old=(1/4)(s-p+1/4)=-1/16.

Adding the paired discrepancy gives

    J_new-J_old=-1/16+e<=-1/32.

Thus the fixed new policy improves the named intended cost by at least 1/32.
The two baselines can be arbitrarily large and cancel *before* their uncertainty
is summarized. At p=1/2,s=0,e=z=w=0 the costs are 3/8 and 5/16.
At e=1/32 the same feasible point attains the upper difference -1/32.
This provides a nonempty model and a sharp witness, not just a symbolic implication.

### 11.3 One specified evidence update

Keep the program, criterion and quantity identities. Replace the upper evidence
bound e<=1/32 by e<=3/64. This is a weakening, not refinement. The old numerical
claim -1/32 no longer holds uniformly: choose p=1/2,s=z=w=0,e=3/64.
The new sharp bound is

    J_new-J_old<=-1/16+3/64=-1/64.

Both self-report derivations survive, since neither reads the e-bound. This
is the concrete selective-revision question from Gate A. A cached result with
the old context revision cannot simply be relabeled; a re-evaluated comparison
or an explicit correction of +1/64 is required. If e's upper bound grows to
1/16, only non-deterioration remains; a larger upper bound can permit deterioration.

### 11.4 Version identity is load-bearing

Change the code to `SELF-MIX-reversed(r)`, which uses branch P when U<r and S
otherwise. It has failure r p+(1-r)s and expected branch charge kappa(1-r).
The same report numbers may remain valid, but the proxy cost change becomes

    (1/4)(p-s-kappa)=+1/16.

Using the previous loss formula after this code change would certify the wrong
sign. The original v1 conclusion does not apply merely because both programs
emit the same report. Reflection refers to a particular versioned behavior.

An allowance xi>=0 may instead specify H_r<=r+xi, while r still controls the
behavior and min(1,r+xi) is the published probability bound. It is not an exact
fixed-point equation r=H_r. Changing which number the program uses changes its
interpretation. Richer cyclic reflection remains a development alternative,
not silently introduced by this annotation.

## 12. Complete interpretation III — nonlinear continuation with a local enclosure

A Bernoulli primitive succeeds with probability theta, where
1/4<=theta<=3/4. The old plan incurs one unit of cost on one success. The new
plan incurs that unit only if two conditionally independent invocations both
succeed. Conditional independence of the invocations does not mean their unknown
parameter is sampled twice; they share the same theta.

The retained continuation alternative evaluates

    K_theta(h_theta) = (1-theta) h_theta(0)+theta h_theta(1),
    h_theta(0)=0, h_theta(1)=theta,

and obtains theta^2. This source-parametric finite computation is explicit;
it does not receive the final value for every continuation from an oracle.
Its variable multiplication is outside the chosen native CPWA term grammar.

### 12.1 An explicit local adapter, not an opaque final-score premise

On any interval [a,b], define the component chord

    U_(a,b)(theta)=(a+b)theta-ab.

Direct expansion gives

    U_(a,b)(theta)-theta^2=(theta-a)(b-theta),
    0<=U_(a,b)(theta)-theta^2<=(b-a)^2/4.

For four mesh cells of width 1/8 on [1/4,3/4], the chord lines are

    5 theta/8 - 3/32,
    7 theta/8 - 3/16,
    9 theta/8 - 5/16,
    11 theta/8 - 15/32.

Let U4 be their pointwise maximum. Consecutive lines meet at the mesh points;
increasing slopes make the corresponding line maximal on its cell. Therefore
U4 is a native CPWA term, and the above **component** proof yields

    U4-1/256 <= theta^2 <= U4

on the full source interval. No final comparison with the old plan was used
to assume this local enclosure.

One fully internal abstract model introduces a dimensionless source q for the
new component's expected unit-event count. Use the declared conversion iota from
one event to one U of cost; theta and q have unit 1 and z has unit U. For each of the four hidden mesh cases, constrain theta to that cell and

    U_cell(theta)-1/256 <= q <= U_cell(theta),  q>=0,  z>=0.

This is a finite union of nonempty rational polyhedra. Each cell has the
witness theta=a,q=a^2,z=0. Its cost terms are J_new=z+iota(q) and
J_old=z+iota(theta). The exact kernel model maps to this source by
(theta,z)->(theta,theta^2,z); the displayed component proof establishes
inclusion. A countermodel in the larger abstract source would not by itself
be a failure of the exact kernel: it can reveal a loose enclosure instead.

### 12.2 The task comparison and what the approximation loses

On the four cells, the upper comparison U_cell-theta is affine, with slopes
-3/8,-1/8,1/8,3/8. Its largest value on [1/4,3/4] is -3/16 at the two outer
endpoints. Hence the abstract model establishes

    J_new-J_old<=-3/16.

The exact kernel has the same sharp bound, since theta^2-theta is convex with
value -3/16 at those endpoints. Both candidate routes therefore preserve this
specific inference although only the continuation route stores the exact
quadratic. At theta=1/2,z=0 the exact costs are 1/4 and 1/2.

For this query **one** chord across the entire interval also suffices: it is
theta-3/16. Its maximum component error is 1/16, rather than 1/256. Four cells
are useful for tighter other uses, not necessary to claim superiority on this
comparison. This explicit simplification guards against retaining structure
that the present consumer does not need.

An upper enclosure is not freely substitutable under negative polarity. If
0<=q<=1, the bound q<=1 does not imply -q<=-1 (q=0 is a countermodel).
A paired comparison generally uses an upper bound for its new cost and a lower
bound for its old cost, or a joint relation preserving their dependence. F06's
rules must retain these directions; F05 defines the enclosure meaning only.

## 13. Semantic adequacy of exact rational audit examples

The semantics quantifies over real assignments, not just rational test points.
Nevertheless every strict countermodel for the selected rational CPWA/polyhedral
fragment has a rational counterpart. This is useful for a future counterexample
interface without mistaking a finite enumeration for a proof of validity.

To verify this, take a violating real point x in a retained rational polyhedron.
Let I be its active constraint rows. The rational affine system A_I y=eta_I has
a real solution and therefore a rational particular solution a and rational
nullspace basis N, by Gaussian elimination. Write x=a+Nz. Rational z' can be
chosen arbitrarily close to z. The points a+Nz' preserve every active equality;
all other inequalities have positive slack and remain satisfied for a sufficiently
small change. The query difference is continuous and its violation is strict,
so a sufficiently close such rational point still violates it. Hidden case
identity is unchanged. The argument also covers a zero-dimensional face.

This proves existence of a finite exact rational **witness** for an invalid
rational-threshold comparison in this fragment. It gives no finite test set
whose success establishes validity, no bound on witness search cost, and no
extension to arbitrary discontinuous black boxes or nonlinear equality sources.
The supplied-context witness check establishes nonemptiness, not coverage of
an empirical population.

## 14. Two distinctions the interface must preserve

### 14.1 Absolute baselines versus independent recentering

For a family of costs J_pi on the same source, adding one common finite function
z to every cost leaves all pairwise differences unchanged. That does not permit
subtracting a different unknown baseline from each policy. If each cost were
independently identified modulo arbitrary offsets, all useful comparisons could
be erased. The shared source relation, not merely the presence of signed numbers,
is what permits safe cancellation. An absolute adequacy query additionally
needs an anchor; paired improvement by itself does not bound an absolute loss.

The three randomness/uncertainty layers in the reflective example are distinct:

| Layer | Mathematical treatment |
|---|---|
| Random draws within one execution | Conditional expectation under the explicitly defined kernel. |
| Unknown model quantities p,s,e | Universal quantification over a stated joint source set; no prior is required. |
| Reliability of an estimated source set | A separate formal or sampling-mode premise, potentially with a coverage failure bound. |

The task criterion and the meta-level proof checker can themselves be uncertain
objects for an agent. This first fragment records that uncertainty through
alternative interpretations and explicit trust/coverage premises, rather than
pretending that arithmetic validity proves its own physical assumptions.

### 14.2 Bounds, refutations and open questions

A feasible countermodel refutes a universal warrant. It does not prove that the
actual deployment violates the claim in every possible case. The r=2/5 example
has both satisfying and violating assignments. Conversely a search that finds
neither a certificate nor a countermodel is computationally unresolved; it need
not correspond to genuine variation across interpretations. An inconsistent
source context is a third issue, not either of those outcomes.

These distinctions can feed an evidence-state user interface later. They are
not additional numerical truth values or an automatic reinstatement of phase
one's K_3 carrier. A hard operational constraint must be checked as a condition
on the proposed use; it must not be 'satisfied' by deleting every unfavorable
source case without evidence. A finite penalty is a tradeoff, not a hard constraint.

## 15. Relationship to the retained alternative and to known mechanisms

On a fixed rational affine query over nonempty polyhedral sources, ordinary
linear certificates and source-preserving value semantics agree on the tight
bound. The selected syntax does not claim that classical linear consequence is
a new calculus. Its proposed contribution must instead be earned through useful
scoped loss reasoning, revision, and a meaningful interpretation of computations.

The alternative interprets a finite kernel as a map on source-indexed downstream
cost functions:

    T_K(h)(x,s) = c(x,s) + sum_y K_x(s,y) h(x,y).

Source x is retained through composition. The entries may depend on x, and
pointwise sequential composition can produce nonlinear functions. Summarizing
uncertainty between stages changes this operator unless the corresponding
rectangularity/information assumptions are supplied. A rational fixed mixture
with CPWA continuation is admitted natively by the selected term fragment;
variable mixtures need a richer primitive or an explicit local enclosure.
The alternative has not been reduced to an oracle supplying all answers.

The RLL comparison is mechanistic and limited. On finite nonnegative values,
its additive residual is exactly the selected res operation. Our signed terms
can also be interpreted by finite nonnegative pairs before taking their
difference; the worked recoding in the companion reconstruction makes the
finite guards explicit. That is a semantic orientation, not an adopted RLL
proof system, a source-versioning theorem, or F09's eventual proof-theoretic
comparison. General signed infinities have deliberately not been introduced.

For neural interpretation, the declared cost/source semantics must precede an
interpretation of network activations. A model that emits a correct numerical
bound is not thereby shown to compute a valid proof internally. Existing causal,
source-perturbation and gauge controls remain required by the prospective probe.
This task neither trains a network nor adds architecture/regularizer constraints.

## 16. Minimal implementation boundary and rejection conditions

The essential numeric kernel needs only source lookup, rational constants,
addition, rational scaling and positive-part residual, with finite sharing.
Min and max may be expanded by

    max(a,b)=a+res(a,b),    min(a,b)=b-res(a,b).

The expanded representation has the same cost denotation. Types, source cases,
policy bindings and evidence modes give that arithmetic a scoped meaning; they
are not arbitrary new connectives. The finite executable fixture checks types,
interpretations and countermodels, not the semantic quantifier over all reals.

The provisional choice should be revised if:

* a central use needs nonlinear/cyclic closure for which local enclosures lose
  every useful guarantee or become unjustifiably costly;
* a purported bound needs hidden-model-dependent action selection;
* useful composite conclusions are merely supplied as opaque final scores;
* source identity/evidence changes cannot be expressed without uncontrolled
  duplication or information loss; or
* the only remaining contribution is a renaming of known arithmetic without a
  distinctive, testable value-based use.

These are falsifiers and design obligations, not reasons to abandon the research.
The continuation alternative remains live. F05 is still partial until the
remaining protected derivation time and fresh semantic reconstruction are done.
No downstream soundness, completeness, empirical interpretability or novelty
claim follows from selecting this first version.


### 16.1 Downstream preservation is an obligation, not a name-based rule

Even a monotone 1-Lipschitz map can erase a signed improvement: min(2,1) and
min(3,1) coincide although 2-3=-1. Nonnegative deterioration budgets and negative
improvement budgets therefore need separate rule hypotheses. The companion
reconstruction gives an explicit lower-gain condition that preserves a strict
improvement on a reached domain. F06 must decide how such premises are expressed;
F05 does not silently install unrestricted substitution through every connective.


## 17. First-pass evidence and continuation

The companion [semantic reconstruction](03a_semantic_reconstruction.md) retains
worked proofs, alternative derivations, discovered example corrections and
countermodels. [Source checks](F05_S1_sources.md) state the limited external
interfaces used. The [exact fixture](../checks/f05_semantics.py) evaluates rational
supplied models with typed terms and nonempty source witnesses; it is not a
universal decision procedure. Its implemented goals use one case-independent
expression pair over finite source cases, sufficient for the three principal
examples. The more general case-indexed interpretation table is specified but
not implemented as a plan-registry executor in this audit.

F05 remains partial. The next pass should reconstruct the semantics from its
minimal assumptions, test source/observation transport and reject redundant
machinery before treating this specification as complete. No F06–F08 task or
later readiness gate has been performed here.
