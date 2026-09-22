# F02 — Competing Semantic Candidates

Original research: September 21, 2026; continuation: September 22, 2026.
Source revision: `ba551afe7f4c026c075a49b09b341eec446caf1a`.
Status: **F02 complete at its comparison scope**; 61.118295 cumulative credited
D minutes and 124 passing dedicated checks. No permanent core or gate decision.
The [original partial session](../work_logs/F02_2026-09-21_S1.md) is preserved;
see the [completion record](../work_logs/F02_2026-09-22_S2.md) and
[reconstruction supplement](02a_candidate_reconstruction.md) for the further
proofs, countermodels, source checks and acceptance evidence.

## Durable question

What should a value expression *mean*, which operations on those meanings are
licensed, and what information survives a composition? This note compares four
concrete answers, not three encodings of the same real number:

- **S: evaluated scalar values.** Meaning is a task-relative numerical value;
  its natural compositional fragment consists of additive payoffs and mixtures.
- **P: aligned value profiles.** Meaning is a payoff function on shared
  scenarios; pointwise operations retain dependence before evaluation.
- **T: continuation-value transformers.** Meaning is an ordered map from
  possible downstream value functions to present values; sequencing is function
  composition rather than an operation on already-evaluated scores.
- **G: achievable guarantee fronts.** Meaning is a partially ordered set of
  resource/error budgets a legal menu can meet; probability is not required.

All four are proposals. Probability, additive reward, an uncertainty model,
and these particular operators are additional mathematical assumptions, not
consequences of epistemic nonfinality. A scenario or transition model is a
revisable working model, not access to a metaphysical world. Mathematical claims
below are conditional demonstrations for the displayed fragments, not the later
F07 soundness result, a novelty claim, or selection of a final calculus.

Use [F01's examples](01_requirements_and_separating_examples.md) and its
[reconstruction](01a_reconstruction_and_information_contracts.md) for the common
questions. The [claim ledger](../claim_ledger.md) distinguishes demonstrated
candidate properties from future obligations. The [standalone fixture suite](../checks/f02_candidates.py) checks finite
calculations; it is not F11's reasoner. Its [recorded results](../checks/F02_results.json)
are constructed development evidence, not a frozen empirical challenge.

## 1. Common comparison contract

### 1.1 Meaning, evaluation, and encoding

A semantic object is what the proposed mathematical operations act on. An
evaluation answers a particular operational question about that object. An
encoding changes its storage or coordinates. A decimal/binary change does not
create a different candidate; discarding a payoff profile except for its mean
does. Conversely, encoding an entire profile into one real and equipping that
code with special decoders does not turn it into candidate S's ordinary numerical
value algebra. No impossibility for *all* real-number encodings is claimed.

The request `q` records whichever task, units, population, information access,
tolerance, and resource conditions a worked example needs. This is not a frozen
record schema. Each candidate must declare what it retains after ingestion;
looking up discarded information through a model ID counts as additional input.
A richer candidate is not credited with solving a problem from information that
was never supplied. Extra acquisition and computation have costs separate from
mathematical sufficiency.

Values are larger-is-better in a declared payoff unit `u`; the F01 loss examples
use their negatives where appropriate. Additive costs have first been converted
into that unit by a declared exchange rate. Different physical units cannot be
silently added. An admissibility question such as E01's error tolerance and work
budget is distinct from its scalar objective. A supplied admissible set can be
used by any candidate; its existence does not establish a new licensing axiom.

### 1.2 What an answer claims

For this comparison, distinguish exact numerical evaluation, sound numerical
bounds, a decision guaranteed within a stated tolerance, and rejection of a
query outside a candidate's fragment. A candidate may make a restriction, but
must state the capability lost. Answering every fully specified admitted query
with “unknown” would not demonstrate a useful calculus.

The candidate objects below are initially mathematical *meanings*. Claims that
finite observations establish those meanings require a separately declared
evidence model. Where uncertainty is used, it is explicit. A set of possible
models is not automatically a calibrated confidence set or a probability law.

## 2. Candidate S — Evaluated scalar values

### 2.1 Carrier and operations

For a fixed request `q` and payoff unit `u`, let the carrier be `R_u`, an ordinary
copy of the finite real numbers in that unit. A plan `e` is summarized by

$$
s_q(e)=v_q(e)\in\mathbb R_u.
$$

The subscript is retained as a type/scope annotation; the numeric value alone
does not identify a task. The candidate admits these operational interpretations:

| Operation | Formula | Interpretation and required premise |
|---|---|---|
| Additive joint payoff | `v + w` | Returns are added under one unchanged evaluation law; no independence is needed for linear expectation. |
| External mixture | `t v + (1-t) w`, `0<=t<=1` | A declared lottery chooses between uses, with the specified weights rather than outcome-dependent routing. |
| Nonnegative payoff scaling | `a v`, `a>=0` | A known change in stakes/units; order is preserved. Negative scaling is permitted only as an explicitly order-reversing operation. |
| Best fixed alternative | `max(v,w)` | Choose between two known evaluated alternatives before any further information. |
| Worse evaluated alternative | `min(v,w)` | The smaller *evaluated* value, not the expected bottleneck of jointly varying outcomes. |
| Added bonus required | `b >= target-v` | With additive bonuses, this exactly characterizes reaching the target. If bonuses must be nonnegative, use `max(target-v,0)`. |

These are not declared Boolean connectives. In particular, numerical negation
`-v` changes payoff sign; it does not create an available action that negates the
original action's consequences.

For a linear expectation interpretation, the additive rule follows directly:

$$
\mathbb E(X+Y)=\sum_\omega p_\omega(X_\omega+Y_\omega)
=\mathbb EX+\mathbb EY.
$$

It holds for every joint alignment with these expectations. For a random choice
with fixed mixing probability `t`, the conditional expected value of the lottery
is `t EX+(1-t) EY`. Outcome-dependent switching is a different operation.

There is already useful multistep reasoning in this restricted algebra. For the
same task and units, if `v_A >= v_B-epsilon` and `v_B >= v_C-delta`, then

$$
v_A\geq v_C-(\epsilon+\delta).
$$

Adding two such comparisons adds their error allowances. This is a scoped
substitution calculation, not evidence that arbitrary sequential programs have
additive values. Every rule needs an operation with the claimed meaning.

### 2.2 Worked S example 1: cheap versus accurate use (E01)

F01 supplies errors `a^3,0` and work costs `1,8`. Fix
`a=1/10`, `lambda=1/1000`, tolerance `1/100`, and budget `8`.
Both candidates are admissible. Converting smaller-is-better combined loss to
payoff gives

$$
v_c=-\frac{2}{1000},\qquad v_a=-\frac{8}{1000}.
$$

Their value difference is `6/1000`, so S chooses the cheap use exactly. If the
exchange rate is instead `1/10000`, fresh inputs give `-11/10000` and
`-8/10000`, and the accurate use wins. A change of exchange rate is not a
contradiction in one fixed numerical ordering.

The old scalar pair alone does not separate error from work cost. At the E01
collision `a=1/2`, `lambda=1/56`, both combined losses are `1/7`, while only the
accurate model meets error tolerance `1/100`. A feasibility flag or the original
error/cost data repairs that query, but it is additional retained information,
not a property of the combined number. A lexicographic value-plus-feasibility
object is a legitimate alternative, not this single-number baseline.

### 2.3 Worked S example 2: task-conditioned comparisons (E02)

For errors `A=(0,4)` and `B=(1,1)`, at task weight `theta=9/10` the payoff
scalars are `-2/5` and `-1`, and S prefers A. At `theta=1/10`, supplied anew,
they are `-18/5` and `-1`, and S prefers B. Each contextual comparison is exact.

What S cannot infer from one evaluated pair is the response to an arbitrary
future weight. Retaining the two error coordinates, endpoint scores, or the
whole map `theta -> v_theta` would change the retained object. A family of
context-indexed scalars may be the right practical choice, but should not be
misdescribed as a single score preserving all task information.

### 2.4 Worked S example 3: where additivity survives dependence (E03)

Take `X=(3,-1)` and either `Y=(-1,3)` or `Y=X`, with equally weighted scenarios.
All individual means are one. In both alignments, the expected additive joint
payoff is exactly two, so S answers that query without joint information.
The expected bottleneck is respectively `-1` and `1`. The numeric operation
`min(1,1)=1` is *not* a valid evaluation of the first bottleneck.

This is a separation of operations, not a dismissal of scalar value. More
strongly, for `n>=0`, the profiles `(1+n,1-n)` and `(1-n,1+n)` each have mean
one but their bottleneck has mean `1-n`. Thus the two means alone do not even
supply a finite uniform lower bound over this unbounded family. Their additive
mean is still exactly two. Support information or a stated restricted family
can change that conclusion.

### 2.5 Explicit uncertainty extension, S-interval

A conservative extension stores a nonempty closed interval `[l,u]` containing an
unknown *evaluated scalar*, not a distribution of per-scenario payoffs. With
finite endpoints, interval addition and subtraction give

$$
[l,u]+[l',u']=[l+l',u+u'],\qquad
[l,u]-[l',u']=[l-u',u-l'].
$$

These are exact answer ranges when every displayed pair is jointly possible,
and otherwise sound enclosures. For a shared unknown `z in [0,1]`, treating
`z-z` as two independent intervals returns `[-1,1]` instead of the exact zero.
Expression identity or a relational constraint can prevent that loss, but is
additional structure. The empty set is not an uncertain finite scalar, and
must not be silently replaced by zero or an arbitrary grant.

This extension can make useful tolerance-relative conclusions. If the supplied
answer enclosure is `[-1/2,-1/3]`, it certifies a lower threshold `-3/5` without
an exact value. S-interval is not credited with deriving that enclosure from
marginals and covariance it does not retain; P or an external justified
calculation can supply it. “Receiving a correct bound” and “deriving that bound
from a richer premise set” are different benchmark tasks.

### 2.6 Preservation, loss, and scale

S preserves evaluated payoff, its ordinary numerical ordering, additive
composition, and the specified fixed-task comparisons. It discards which
scenario produced which contribution, unevaluated task coordinates, output
states, information schedules, and shared uncertainty unless those are supplied
separately. It has a one-real mathematical carrier, not a claim of constant
bit complexity for arbitrary exact reals.

There is no universal finite upper or lower bound on `R_u`. Restricting to one
fixed bounded interval breaks closure under unrestricted addition and positive
scaling. Exact bounded recoding is different: after normalization by a declared
unit scale, `h(v)=v/(1+|v|)` encodes R into `(-1,1)`. Define
`a plus_h b = h(h^{-1}(a)+h^{-1}(b))`; then addition is preserved *with that
transported operation*. Ordinary addition of the codes does not do so.

Positive rescaling preserves ordinary order and scales tolerances. Translating
all terminal alternatives by the same constant preserves a fixed comparison,
but a two-term sum acquires two copies of that constant. One cannot demand both
unchanged ordinary addition and an unexplained single global offset. Unit,
origin, and aggregation conventions travel with the operation.

## 3. Candidate P — Aligned value profiles

### 3.1 Carrier, interpretation, and evaluation

Fix a finite scenario set `Omega` and common unit `u`. The carrier is

$$
\mathcal P_u(\Omega)=\mathbb R_u^\Omega.
$$

A value object `x` assigns a payoff to each scenario. It retains observable
payoff behavior, not a model's source code, proof history, or unrestricted raw
state. A joint use must share the scenario indexing. Independently permuting
one component's coordinates while keeping the others fixed generally changes
the meaning; a common permutation of all components and weights does not.

For explicitly supplied nonnegative task weights summing to one,

$$
V_p(x)=\sum_{\omega\in\Omega}p_\omega x_\omega.
$$

Weights may be stipulated population probabilities or task-importance weights,
as identified in the example. Other evaluations are possible later, but results
that use linearity below apply to this declared fragment only.

Pointwise order, addition, scaling, minimum, and maximum are well-defined after
types and alignment agree. They encode respectively pointwise comparison,
additive simultaneous payoff, changes of stakes, a stipulated joint bottleneck,
and a payoff envelope. Calling an envelope attainable requires an information
and action-access argument; it is not supplied by the vector operation.

### 3.2 Worked P example 1: joint alignment and its exact scalar boundary

For E03, retain the two aligned coordinates. With `X=(3,-1)`, `Y=(-1,3)`, and
`Y'=X`, the calculations are

$$
V_p(X+Y)=2,\quad V_p(\min(X,Y))=-1,\quad
V_p(\min(X,Y'))=1.
$$

P separates the bottlenecks that S merges. This gain comes from the supplied
alignment, not from larger storage by itself. Two unaligned marginal profiles
do not determine which joint table should be used.

The boundary at which scalar minimum *does* commute with this evaluation is
particularly informative. Let `p` be any finite weight vector. Then

$$
V_p(\min(x,y))\leq\min(V_p(x),V_p(y)).
$$

Assume `V_p(x)<=V_p(y)`. Equality holds exactly when

$$
0=V_p(x)-V_p(\min(x,y))
 =\sum_\omega p_\omega(x_\omega-y_\omega)_+.
$$

Every term is nonnegative, so this means `x_omega<=y_omega` at every
positive-weight coordinate. Interchanging x and y covers the other ordering.
Thus equality holds precisely when one profile dominates the other on the
supported scenarios. Zero-weight coordinates do not matter for this evaluation.

Equivalently, the information-sensitive gap is

$$
\min(V_p(x),V_p(y))-V_p(\min(x,y))
=\frac{V_p(|x-y|)-|V_p(x-y)|}{2}.
$$

The same nonnegative gap separates the evaluated maximum envelope from the best
fixed evaluated alternative. For E03's crossed profiles it is two. Dependence,
nonlinearity, and information access are related, but they are not one concept:
a bottleneck may be a joint score without any choice, whereas an envelope may
require a chooser to observe the relevant scenario.

### 3.3 Worked P example 2: a family of tasks without a universal ranking

Represent E02's payoffs by `x_A=(0,-4)` and `x_B=(-1,-1)` on the two output
coordinates, and evaluate with `p_theta=(theta,1-theta)`. P derives the entire
response difference `V_theta(x_A)-V_theta(x_B)=4 theta-3`.
It therefore derives both previous reversals and their threshold `3/4` without
fresh raw-model evaluation. The profiles are incomparable in pointwise order.

For a restricted task interval `[ell,r]`, an affine difference is nonnegative
throughout exactly when it is nonnegative at both endpoints (or the single
endpoint when `ell=r`). Hence on `[1/4,3/4]`, B is never worse even though B
does not dominate pointwise over the unrestricted two-coordinate task family.

More generally, if admitted task weights form the convex hull of finitely many
weights `p_1,...,p_k`, comparisons at those vertices suffice: every other
weighted difference is their convex combination. This supplies a genuine
compression option when only those *linear evaluation* queries are admitted.
It does not show that the compressed scores are closed under pointwise minimum;
E03 supplies the counterexample when the sole retained weight is `(1/2,1/2)`.

### 3.4 Worked P example 3: error propagation is typed composition

Let x and x-hat be intermediate-output profiles in an input unit, and let g and
g-hat map those inputs to output values. Suppose, at every reachable coordinate,
`|x-hat-x|<=delta`, `|g-hat(x-hat)-g(x-hat)|<=eta`, and g is K-Lipschitz on the
region connecting the ideal and perturbed inputs. Adding and subtracting
`g(x-hat)` proves

$$
|\hat g(\hat x)-g(x)|\leq\eta+K\delta.
$$

With F01's `delta=1/100`, `K=100`, and `eta=1/50`, the bound is `51/50`, not
the unweighted sum `3/100`. K carries the output/input unit conversion.
An error assertion only at ideal inputs does not establish the asserted eta
bound at the actual perturbed input. P keeps the intermediate profile available,
but does not invent the missing regularity/scope premise.

For a bottleneck, uniform component errors epsilon and delta instead imply

$$
\|\min(x,y)-\min(\hat x,\hat y)\|_\infty
\leq\max(\epsilon,\delta).
$$

Indeed if both component deviations are at most a, the approximate minimum lies
between the original minimum minus a and plus a. With mean absolute component
errors, the safe general bound is their sum, not their maximum. For exact
`x=y=(1,1)` and approximate `x-hat=(0,1)`, `y-hat=(1,0)`, each component has
mean absolute error `1/2`, while the bottleneck has error one. Thus an “error
number” without its aggregation contract is insufficient even with correct units.

### 3.5 Uncertainty must retain the relation it purports to retain

An explicit finite extension has a nonempty set of possible indexed models
`theta`. Each supplies aligned profiles `x_theta` and weights `p_theta`.
Its lower and upper evaluations are

$$
L(x)=\min_\theta V_{p_\theta}(x_\theta),\qquad
U(x)=\max_\theta V_{p_\theta}(x_\theta).
$$

Composition uses the *same* theta for all jointly constrained components.
For addition, `L(x+y)>=L(x)+L(y)`; equality is not automatic because the
component minima can occur in different models. Negation exchanges bounds:
`L(-x)=-U(x)`. A constant shift c adds c to both bounds. These follow directly
from the finite nonempty definition, not a representation theorem for arbitrary
uncertainty records. Empty compatibility receives an explicit inconsistent
status, not a usable lower-value certificate.

Even compressing each coordinate to its lowest possible value can lose useful
correlation. Suppose the two possible profiles are `(3,-1)` and `(-1,3)`, with
uniform weights. Every possible model gives evaluated value one, so L is one.
The pointwise envelope is `(-1,-1)` and evaluates to minus one. It lets the
adversary change the model separately at each coordinate. This is a conservative
lower bound, but calling it the exact model-wise value would change the problem.

F01's covariance example supplies another useful specialization: a relational
set of joint tables with the stated marginals and covariance zero yields the
sharp bottleneck interval `[-1/2,-1/3]`. A relational set of profiles can express that input contract; the full
moment-constrained family is an additional set/constraint description, not
silently a finite list of thetas. The bound itself is demonstrated in F01,
not obtained merely by declaring this representation. Once the interval has
been justified, S-interval can carry
its threshold consequence just as well; P's extra role is preserving premises
needed for that derivation or further joint operations.

### 3.6 Scale, storage, and limits

Each finite profile is bounded individually; the *carrier* has no common bound.
The two-coordinate family `(1+n,1-n)` shows that arbitrarily large positive and
negative values need no infinite scenario space. Coordinatewise exact bounded
recoding is possible, but all operations and evaluation must travel with it:

$$
V^{h}_p(z)=h\left(\sum_\omega p_\omega h^{-1}(z_\omega)\right)
$$

if the result is also encoded. Averaging the codes is a different evaluation.
Here h is understood after normalization by a stated payoff-unit scale; the
constant 1 is not added to a dimensioned quantity without conversion.

For a countable scenario extension, finite expected values require integrability
under the specified weights. Addition and pointwise min/max of two integrable
profiles stay integrable, since their absolute values are bounded by the sum
of the component absolute values. Arbitrary nonlinear composition need not:
a square can destroy integrability. A finite observed prefix or finite code
precision is not a uniform tail/decoding-error guarantee over an unbounded family.

P costs O(number of retained scenario entries) for direct finite pointwise
operations; optimizing a relational uncertainty set can cost much more. It
preserves payoff dependence and task responses at that level, not arbitrary
internal model structure. It does not, without additional semantics, encode
state-changing sequential processes, available observations, proof-system
meaning, or evidence provenance. Those are either explicit extra interfaces or
questions outside its basic fragment.

## 4. Candidate T — Ordered continuation-value transformers

### 4.1 The object is a response to downstream value

Let A and B be finite, nonempty input and output interfaces. A continuation is
`h:B->R_u`: the value of whatever will happen after the present step finishes.
The proposed semantic object is a map

$$
T_e:\mathbb R_u^B\longrightarrow\mathbb R_u^A.
$$

`T_e(h)(a)` is the present value of using e at input a and then obtaining
continuation h. It is not merely a forecast of the next state and not merely
the value of e under one already-selected continuation. Its numerical modeling
assumptions must still be stated. Start with the concrete primitive

$$
T_{r,P}(h)=r+Ph,
$$

where r is a finite immediate-payoff vector and P is a finite row-stochastic
matrix. The deterministic subcase is `T_(f,r)(h)(a)=r(a)+h(f(a))`.
Probabilities are assumed in this stochastic candidate; the deterministic
subcase does not require uncertain frequencies. This is not a derivation of
expected utility from the project's philosophical commitments.

The semantic carrier consists of the maps denoted by finite typed expressions
generated from these primitives by composition and nonempty finite pointwise
minimum and maximum. Two expressions denoting the same map are identified for
this extensional comparison. An expression is a constructive representation of
the map; retaining its branch syntax or a policy witness is extra information
when a later question inspects it. Identity is `h->h`.
Expressions with no available branch require an
explicit separate disposition; empty min/max is not silently assigned a finite
value. Define

$$
(T;S)(h)=T(S(h)),\qquad
(T\sqcap U)(h)(a)=\min(T(h)(a),U(h)(a)),
$$

and similarly maximum `sqcup`. T runs first and S second, although continuation
values propagate in the opposite order. Branch operations require matching
input/output interfaces and units.

**Operational interpretation is essential.** Maximum can mean controlled
selection at a state the chooser actually observes. Minimum can mean a declared
adversarial choice or a robust alternative at the stated information stage.
Neither operation creates observations or makes globally shared uncertainty
independent at successive nodes. Which branches are available, who chooses,
and what is known at that point belong to the term's interpretation.

### 4.2 A useful failed restriction: lower envelopes alone are not closed

One tempting smaller carrier consists only of lower envelopes of affine
expectations:

$$
T(h)(a)=\min_j\{r_j(a)+p_j(a)\cdot h\}.
$$

It is concave in h: each affine branch evaluated at a mixture equals the same
mixture of branch values, and taking a minimum gives at least the mixture of
the two separate minima. It naturally expresses certain robust evaluations.
But an agent's available choice can have `D(h)=max(h_0,h_1)`. At
`h=(1,0)` and `k=(0,1)`,

$$
D((h+k)/2)=1/2 < (D(h)+D(k))/2=1.
$$

Thus D is not concave and cannot be represented by that proposed lower-envelope
carrier. The T candidate here includes max as well as min and does **not** impose
concavity on every object. A pure lower-expectation candidate remains possible
with controlled choice kept in a separate layer, but that is a different
closure/interface decision. This is a worked failure and scoped repair, not an
assertion that coherent uncertainty models are wrong.

### 4.3 Properties shared by the finite T expressions

Every generator, and hence every finite expression, is monotone and commutes
with a common constant payoff shift:

$$
h\leq k\ \Longrightarrow\ T(h)\leq T(k),\qquad
T(h+c\mathbf1_B)=T(h)+c\mathbf1_A.
$$

For an affine primitive, the first property uses nonnegative entries of P and
the second uses each row sum being one. Min and max preserve both properties;
composition preserves them by substitution. This checks the proposed operations
against an independently specified numerical meaning rather than defining
“sound” to mean “generated by our syntax.” It is still only candidate-level
structure, not the eventual general proof system.

For finite h,k put `d=||h-k||_infinity`. Monotonicity and the shift law give

$$
T(k)-d\mathbf1_A\leq T(h)\leq T(k)+d\mathbf1_A,
$$

so these maps are nonexpansive in the uniform norm. This is a substantive
restriction of T: arbitrary amplification of terminal payoff is not in this
unit-normalized class. A discounted or gain-sensitive class could change the
shift law and norm coefficient, but that would be an explicit alternative.

An order on matching interfaces is `T >= U` when `T(h)(a)>=U(h)(a)` for every
admitted input and continuation. Composition is order-preserving on either
side because all T maps are monotone. The continuation family must be explicit:
section 4.7 shows that quantifying over *all* real continuations can make this
order too strong for the intended approximation question.

### 4.4 Worked T example 1: equal current scores, different downstream use

There is one input and two possible outputs, L and R. Two zero-cost deterministic
steps select L and R respectively:

$$
T_L(h)=h_L,\qquad T_R(h)=h_R.
$$

Their value at zero continuation is the same: `T_L(0)=T_R(0)=0`.
For `h=(10,0)`, their values are 10 and 0; for `h=(0,10)` the comparison reverses.
An immediate scalar cannot answer both future questions. T retains the effect
on possible downstream tasks through its response function.

A small composed calculation makes this operational. Step e costs one and
outputs low/high with probabilities `1/4,3/4`. Step f costs two and maps low to
failure and high to success. With terminal values `h(failure)=0` and
`h(success)=10`,

$$
T_f(h)=(-2,8),\qquad
(T_e;T_f)(h)=-1+\tfrac14(-2)+\tfrac34(8)=\tfrac92.
$$

The composed primitive has immediate payoff minus three and terminal
probabilities `(1/4,3/4)`, so it separately gives `-3+15/2=9/2`.
Replacing e by a zero-cost half/half transition gives final value three, even
though its zero-continuation value is better than e's. This is a comparison of
uses under the supplied downstream task, not a metaphysical ranking of steps.

A profile holding only immediate payoffs also misses this distinction. A profile
that additionally retains output states or full trajectories can recover it;
that observation limits any claim that T is more expressive than every possible
profile representation. The different proposal is to make continuation response
and typed sequencing primitive rather than reconstruct them from arbitrary
trajectory tables for each query.

### 4.5 Worked T example 2: observation timing (E08)

Let the hidden binary case W be uniform, and let a binary observed signal S
agree with W with symmetric accuracy `p>=1/2`. Reward is 3 when action a equals
W and -1 otherwise; acquiring S costs kappa. The model supplies the joint law,
not just two marginal signal frequencies.

Use an observation step from one initial state to the two **observed** signal
states, each with probability `1/2`. At signal s, the next action step uses the
specified conditional law `Pr(W=s|S=s)=p` to evaluate either action, and permits
maximum only over actions depending on s. With the terminal correctness reward,
these conditional action values are `4p-1` and `3-4p`. Therefore

$$
V_{\rm acquire}=4p-1-\kappa,
\qquad V_{\rm optional}=\max\{1,4p-1-\kappa\}.
$$

At `p=3/4`, `kappa=1/4`, optional value is `7/4`. A fixed uninformed action gives
one. The hidden-state envelope gives three but is not attainable under this
signal contract. Placing the action maximum after a hidden-state observation
would describe a different system, not improve an inference about this one.

There is a representation obligation here: the observation's marginal kernel
alone does not contain the posterior relation between W and S. Supply that
joint law/conditional interface, or use finite posterior-belief states as the
observed outputs. A changed prior or observation model can require rebuilding
that interface. Keeping the conditional relation implicit is not free inference.

### 4.6 Shared uncertainty can invalidate an exact sequencing interpretation

Suppose an unknown but fixed `theta in {0,1}` supplies first reward theta and
second reward `1-theta`. The true total in every admitted model is one. If each
stage is first reduced to its own lower value transformer on a singleton state,

$$
L_1(h)=\min_\theta(\theta+h)=h,\qquad
L_2(h)=\min_\theta(1-\theta+h)=h,
$$

their composition at zero is zero, not one. It lets one model minimize the first
stage and the other minimize the second. The result is a valid conservative
lower bound here, but not the exact value for a shared fixed parameter.

A scoped repair is to keep the parameter family through composition and only
then minimize:

$$
\min_\theta(T_1^\theta;T_2^\theta)(0)=1.
$$

Alternatively, a state/interface can preserve relevant hidden memory together
with restrictions on who observes it. Simply putting theta into an agent-visible
state and allowing choice based on it can give an *optimistic* error instead.
This repair requires more information; plain stagewise lower maps have already
forgotten the relation and cannot reconstruct it.

When each stage really permits nature to choose independently at each reached
state, lower-envelope composition does have the corresponding exact meaning.
For nonnegative transition weights `p_b`,

$$
\sum_b p_b\min_j z_{bj}
=\min_{(j_b)_b}\sum_b p_b z_{b j_b}.
$$

Choose a minimizing j separately for every b for one inequality; every joint
choice is at least the separate minima for the other. The finite product of
choices is the hypothesis. If a common j must serve all b, the displayed
minimum ranges over too many combinations. We use this elementary identity
rather than assume that every uncertainty source has such a product structure.

Controlled choice has an analogous quantifier boundary. With payoff table
`a: (1,0)` and `b: (0,1)` over two hidden models, best robust deterministic
choice has value `max_a min_theta payoff = 0`. If the model were revealed before
choice, `min_theta max_a payoff = 1`. A half/half randomized action, with the
model fixed independently of the random draw, guarantees `1/2`; no mixture
beats it because `min(t,1-t)<=1/2`.
Averaging the already-minimized separate action values instead gives zero.
Hence neither max nor random mixture restores coupling information after it is
lost. A stated finite menu can include that lottery; optimization over every
continuous randomized policy is not automatically closure of the finite syntax.

### 4.7 A second boundary: all future values may be too demanding

For one-input affine steps `T(h)=r+p dot h` and `U(h)=s+q dot h`, with p and q
probability vectors, requiring `T(h)>=U(h)-epsilon` for *every* `h in R^B` and
finite epsilon forces `p=q`. If d=p-q is nonzero, choose `h=-t d`:

$$
T(h)-U(h)+\epsilon=r-s+\epsilon-t\sum_b d_b^2,
$$

which is negative for a sufficiently large t. If p=q, the requirement is exactly
`r-s+epsilon>=0`. Thus unrestricted continuation comparison cannot declare two
different transition laws uniformly interchangeable within finite error.
This is not a reason to bound value itself. It is a reason to declare what
future tasks the approximation is supposed to serve.

A useful family limits *relative stakes*, not absolute values:

$$
\mathcal H_M=\{h:\max_b h_b-\min_b h_b\leq M\},\qquad M\geq0.
$$

It contains arbitrarily positive and negative constant shifts. Since d sums to
zero, those shifts cancel in a comparison. Writing
`TV(p,q) = (1/2) sum_b |p_b-q_b|`, one obtains the exact criterion

$$
T(h)\geq U(h)-\epsilon\text{ for all }h\in\mathcal H_M
\quad\Longleftrightarrow\quad
r-s+\epsilon\geq M\,\mathrm{TV}(p,q).
$$

To prove it, shift h into `[0,M]^B`. The smallest `d dot h` sets h to M where
d is negative and zero where d is positive, giving
`M sum_(d_b<0) d_b = -M TV(p,q)`. This assignment is allowed and attains the
bound. The proof handles M=0 and p=q directly. There is no change from this
finite extremum calculation to a claim about unknown empirical transitions.

For example, cheap step C costs one and always reaches L; accurate step A costs
two and always reaches R. Then `T_C-T_A=1+h_L-h_R`. C is no worse for every
continuation of span at most one, even though it is not uniformly better over
all real continuations. For span M greater than one, `h=(0,M)` is a separating
task. This links tolerable loss, task scope, and resource benefit while leaving
the carrier unbounded.

### 4.8 Composing tolerated guarantees needs a closure premise

Let `T1,U1: R^B -> R^A` and `T2,U2: R^C -> R^B`. Suppose
`T1(k)>=U1(k)-epsilon1` for every `k in H_B`, and
`T2(h)>=U2(h)-epsilon2` for every `h in H_C`, uniformly across the relevant
input states. If `U2(H_C)` lies in `H_B`, monotonicity and constant shifts give

$$
\begin{aligned}
T1(T2(h))
&\geq T1(U2(h)-\epsilon2\mathbf1_B)\\
&=T1(U2(h))-\epsilon2\mathbf1_A\\
&\geq U1(U2(h))-(\epsilon1+\epsilon2)\mathbf1_A.
\end{aligned}
$$

The closure premise is not a decorative condition. Take T1 and U1 to select L
and R, so their difference is at least -1 on `H_B=H_1`. Let `T2=U2` map a scalar
terminal h to `(h,h+10)`. It has zero approximation error, but its output at zero
is not in H_1. The composite values are 0 and 10, violating the purported
one-unit bound if closure is omitted.

A sufficient finite check for a shift-preserving monotone U is

$$
\mathrm{osc}(U(h))\leq\mathrm{osc}(U(0))+\mathrm{osc}(h).
$$

If h ranges from m to m+M, monotonicity sandwiches U(h) between U(0)+m and
U(0)+m+M. Thus choosing `M_B>=osc(U2(0))+M_C` is sufficient for these span-bounded
families. This may be conservative; it is not claimed necessary.

### 4.9 Relationship to S and P, and the candidate's limits

On a singleton input and output, any constant-shift-preserving T has
`T(h)=T(0)+h`. Composition adds the two constants; min/max compare them.
Thus S's additive algebra is an exact one-state fragment of this T semantics,
not an opponent that must be declared “false.” Moving to T makes a larger
operational interface primitive.

A profile x can likewise be viewed as the special map from a singleton terminal
interface to scenario inputs, `T_x(c)=x+c`. This is an exact representation of
its value object. It does **not** automatically preserve every profile operator
as the same transformer operator: ordinary function addition gives
`T_x(c)+T_y(c)=x+y+2c`, counting the continuation twice, whereas the intended
profile-sum map is `x+y+c`. Parallel reward combination needs its own declared
constructor and joint transition/coupling. Separate marginal transformers cannot
reconstruct E03's dependence-sensitive bottleneck any more than separate full
marginal distributions can.

T retains responses to downstream functions and composes typed operational
steps. An affine primitive is stored by `(r,P)` rather than enumerating all
continuations. A finite min/max expression gives a constructive description of the response
map. Its syntax may retain decision and uncertainty structure that the map alone
forgets; section 9.1 shows why those information contracts must be distinguished.
The extensional map does not automatically retain shared latent parameters,
observation restrictions, joint outcomes of parallel steps, or the empirical
basis for its kernels. Those must be present in its interface or declared out
of scope. Lowering such structure too early may produce either conservative
loss or an invalid optimistic interpretation.

Direct evaluation of one dense affine primitive costs `O(|A| |B|)` arithmetic
operations. Finite expression evaluation additionally depends on expression
size and sharing; representation and comparison of large response maps are not
claimed efficient in general. Infinite horizons, arbitrary continuous-policy
optimization, and countable unbounded-state closure are outside this finite
candidate, not silently resolved by its notation.

## 5. Candidate G — Ordered sets of achievable guarantees

### 5.1 Why add a fourth candidate?

S, P, and the stochastic examples of T share many expectation-based examples.
A genuinely different possibility makes *which requirements can be met* the
value object, without requiring a probability distribution or a single tradeoff
rate. Adding G remains within F02's candidate-comparison scope. It does not
replace the other candidates or expand this task into choosing a final core.

Start with a finite menu of available, deterministic uses. Each has a vector of
costs or errors in d declared component units, with smaller components better.
Let A be the finite set of their performance vectors. Define the value object

$$
\Gamma_A=\{b\in\mathbb R^d:\text{some }a\in A\text{ satisfies }a\leq b\},
$$

where inequality is coordinatewise. It is the set of requirement budgets that
this menu can meet. Inclusion is the capability order: `Gamma_A` is at least as
capable as `Gamma_B` when `Gamma_A` contains `Gamma_B`. This is generally a partial
order, not an unexplained total numerical ranking.

One concrete representation retains A's nondominated vectors (a finite antichain)
plus witness labels when an actual use must be returned. Removing a dominated
vector does not change the budget set: if `a<=a'<=b`, a already witnesses that
budget. It does not preserve every other fact about a discarded use, such as its
identity or its compatibility with a future program. Those require a richer type.

The empty menu gives the empty capability set. It means “no available use in this
menu,” not “the evidence is contradictory.” Evidence records still need their own
interpretation. Likewise, if A consists of certified upper bounds rather than
exact deterministic costs, Gamma_A certifies a subset of feasible budgets; it
is not automatically the exact attainable set. Do not convert uncertainty about
outcomes into a menu of outcomes the agent may choose.

### 5.2 Concrete operations and their meanings

For matching scope and component units:

**Choice of an available use:** `Gamma_A union Gamma_B`, represented by the
nondominated part of `A union B`. A witness selects a use from the chosen menu.

**Additive joint use with freely combinable component choices:**

$$
\Gamma_A\otimes\Gamma_B=\Gamma_{\{a+b:a\in A,b\in B\}}.
$$

This formula assumes both costs add and every pair of local uses is admissibly
composable. The common upper cone does not change it: sums of nonnegative slack
vectors are exactly another nonnegative slack vector.

**A budget adequate for either menu when each is considered separately:**

$$
\Gamma_A\cap\Gamma_B
=\Gamma_{\{\max(a,b):a\in A,b\in B\}}.
$$

Here max is coordinatewise. A budget in the intersection has a witness in each
menu; taking their coordinatewise maximum gives the claimed generator. Conversely,
a budget above such a maximum is adequate for both. This does not pay the sum
of their joint costs and does not require one shared policy to witness both.

Choice is associative and idempotent. Additive independent joint use is
associative and distributes over choice, since `(A union B)+C` consists of
exactly `A+C` together with `B+C`. The empty menu is a choice identity and an
annihilator for independent joint use; the zero-cost menu `{0}` is a joint-use
identity. These are elementary finite-set identities with explicit operational
premises, not universal logical laws for shared-state programs.

Every strictly positive diagonal change of component units preserves budget
membership and the partial order after both performance vectors and budgets are
converted. A nonnegative linear transformation preserves component inequalities
but may discard distinctions if it is not invertible. Negative conversion
coefficients would reverse a cost order and need a different declared meaning.

### 5.3 Worked G example 1: retaining adequacy and resources (E01)

Use menu `A={(a^3,1),(0,8)}` in error/work units, with witness labels cheap and
accurate. Both vectors are nondominated for `a>0`: one has less work, the other
less error. At `a=1/10`, the budget `(1/100,8)` is met by both. At `a=1/2`,
only the accurate use meets it. At `a=1/2` and budget `(1/100,2)`, the menu cannot
meet the request at all. These distinctions require no scalar exchange rate.

If the request additionally supplies lambda and asks which admissible use
minimizes `error+lambda work`, evaluate that scalar on the *admissible* menu.
The candidate permits scalarization for a stated task without making it the
permanent capability object. A witness label is needed to execute the selected
use; a bare set of budgets only answers existence/adequacy questions.

### 5.4 Worked G example 2: every weighted score can miss a useful option

Consider the deterministic two-component menus

$$
A=\{(0,2),(2,0)\},\qquad
B=A\cup\{(3/2,3/2)\}.
$$

Every vector in B is nondominated. For every nonnegative normalized weight
`(theta,1-theta)`, the best scalarized cost in A is

$$
\min\{2(1-\theta),2\theta\}\leq1,
$$

while the added vector costs `3/2`. Therefore *all these weighted-score queries*
give identical answers for A and B, not merely one chosen score.
Nevertheless, budget `(3/2,3/2)` is feasible in B and infeasible in A.
An entire family of scalarized optimum values can thus discard an option that
matters for a different legitimate requirement question.

Allowing mixtures changes the contract. A half/half lottery over A has mean
performance `(1,1)`, but neither realized use meets the displayed coordinate
caps. Replacing A by its convex hull is appropriate only for a declared
mixture/mean-performance interpretation, not for this deterministic per-use
budget query. The example is not a claim that randomization is never useful.

For F01's E02, singleton menus `(0,4)` and `(1,1)` likewise have incomparable
budget sets, while a supplied weight theta recovers the previous task-specific
ranking. G can retain this partial information rather than force one winner.

### 5.5 Joint choice requires compatibility, not just separate attainable values

Let one *shared controlled choice* `i in {0,1}` determine two stage costs:
first cost i, second cost `1-i`. Each marginal menu alone has minimum zero.
Freely combining those separate marginal minima predicts total zero, although
every allowed shared choice has total one. Here the mistake is optimistic: it
asserts a budget can be met by an unavailable pair of local policies.

The repair keeps the compatibility relation. Pair only `(first_0,second_0)` and
`(first_1,second_1)`, so the summed frontier is `{1}`. If i instead denotes an
uncontrolled unknown model and a worst-case guarantee is requested, the relevant
quantifiers change again. The attainable-choice interpretation must not be
silently reused for model uncertainty.

Even ordinary Pareto pruning can be premature when endpoints are discarded.
Suppose a first step can reach L at cost zero or R at cost one. A continuation
costs 100 from L and zero from R. Pruning the first step solely by immediate
cost keeps L and leads to 100, losing the valid total-cost-one plan through R.
Taking the independent marginal minimum of both stages is worse in another way:
it predicts zero using the incompatible L-prefix and R-suffix.

### 5.6 An explicit typed relational extension, not a magic repair

For finite input/output interfaces X,Y, retain a finite set of labeled triples
`(x,c,y)`, where c is a d-dimensional cost vector and the label supplies a
controllable implementation/witness. Sequential composition joins matching
intermediate endpoints and adds cost:

$$
(x,c,y)\ ;\ (y,d,z)\ \mapsto\ (x,c+d,z).
$$

Choice takes union. Pareto pruning is permitted only within the same input/output
pair and the same required compatibility information. For the L/R example,
composition before endpoint erasure returns costs 100 and 1, whose scalar frontier
is `{1}`. Associativity follows by enumerating exactly the same compatible paths
and using associativity of cost addition. It does not license forgetting a shared
policy parameter that still constrains which paths are available.

This is a substantive alternative to T: values can be relations of achievable
resource guarantees, with composition by joining interfaces and projecting
intermediate states. No probability is required. Its basic quantifier is
existence of a permitted path/use. It does not represent adversarial transitions
or stochastic averages without an additional, explicitly different semantics.
A graph edge denoting an uncontrolled possible outcome cannot be treated as a
controllable edge simply because their shapes look alike.

### 5.7 Boundedness, representation, and limits

Finite fronts may have arbitrary finite real coordinates; the carrier has no
common cost bound. Componentwise exact increasing recoding preserves Pareto
comparisons and choice, while additive composition requires transported
addition. The identity between “bounded code” and “bounded represented cost” is
rejected here just as for S and P.

When d=1, every nonempty finite front reduces to its smallest cost. Choice then
uses numerical minimum and independent joint use adds costs. This is a
minimization counterpart of S's scalar additive fragment. For d greater than one,
ordinary real order alone cannot faithfully express every incomparability.
Special encodings with nonstandard decoders are not excluded.

A minimal front does not retain the full original menu, much less model source
code; dominated performance options are removed under stated query restrictions.
Its size can still grow badly with independent compositions and many objectives.
Constructing a joint menu forms up to `|A| |B|` sums before pruning. No polynomial
bound on frontier size across arbitrary compositions is claimed.

G's budget semantics naturally addresses hard requirements and noncompensating
objectives. It does not directly answer an expectation of a bottleneck from
marginal distributions, maintain scientific evidence provenance, or preserve
hidden information schedules. Conditional lifting to richer labeled/resource
relations has a price and must not be scored as a free capability of the basic
front. The non-probabilistic fragment is valuable without pretending to cover
all F01 queries unchanged.

## 6. Common-example comparison

The columns describe each candidate with its **declared retained inputs**, not
an implementation that silently retrieves a discarded full model. A conditional
answer is not an unconditional pass. Supplied correct scalar values are usable
by S even when another candidate was needed to derive them.

| Question / input contract | S: scalar (optional interval) | P: aligned profiles | T: continuation transformers | G: guarantee fronts / typed relation |
|---|---|---|---|---|
| E01: preference *and* error/work feasibility | Exact preference at fixed q; the combined value alone merges distinct feasibility cases. | Needs separate typed error/work channels or supplied feasible set, not just the combined payoff profile. | Needs resource information in state/type or a separately supplied feasible set; one reward scalar is not a hard budget proof. | Error/work front directly answers deterministic budget membership; a scalar preference can be applied after feasibility. |
| E02: changing nonnegative task weights | Exact for newly supplied scalar values; one old evaluation does not determine other tasks. | Coordinate profiles derive the entire admitted weight family and its restricted dominance. | Output-state response supports admitted terminal loss functions; changing an unretained prior/interface needs more input. | Preserves incomparable budget capabilities and permits optional task scalarization. |
| E03: aligned expected bottleneck | Additive means work; the bottleneck is not determined by two means. A justified interval can carry a threshold consequence. | Exact when common alignment is supplied; relational model sets can express missing coupling and tolerated bounds. | A joint-output transition can evaluate the bottleneck; separate marginal transformers cannot recover the coupling. | No intrinsic marginal-probability/bottleneck semantics; a supplied deterministic or worst-case bound can be a component guarantee. |
| E04: sequential approximation | Local scalar bounds suffice only when the requisite sensitivities, scopes, and aggregation are supplied. | Pointwise composition plus reachable-scope bounds gives the stated propagation inequality. | Native typed sequencing; its terminal-value norm bound is not a replacement for physical input sensitivity K. Restricted tests need closure under the suffix. | Matching-endpoint relations compose the stipulated additive resource bounds. Physical error bounds additionally need valid sensitivity/aggregation laws; matching endpoints alone does not establish them. |
| E05: incomplete versus conflicting evaluation | An interval and nonempty-basis status can distinguish them; a bare number cannot. | Explicit nonempty joint model set versus incompatible premises; coordinate envelopes can lose dependence and endpoint information. | Min branches require an explicit nonempty family and information stage; discarded shared models are not reconstructed by composition. | Empty available menu is not the same as contradictory evidence. Basic G needs a separate evidence interpretation. |
| E06: finite interpreted axiom/decoder example | Given evaluated decoder risks, can choose; does not derive them from residue syntax alone. | Can evaluate a supplied menu of legal decoder payoff profiles on the common N index; pointwise best decoder is not a legal fixed decoder. | Needs a joint reference/output or posterior-belief interface with controls restricted to observed residues. A marginal residue transition alone is insufficient. | Typed deterministic relations can compose the exact paired-residue decoder; average decoder risk requires the specified weighting as extra semantics. |
| E07: unbounded value and recoding | R has no global cap; bounded code must transport arithmetic. | Finite profiles may have arbitrarily large entries; countable evaluation needs integrability/tail assumptions. | Finite real continuations need no global cap. Bounding relative task span differs from bounding all values; arbitrary infinite-horizon closure is not given. | Finite fronts can have arbitrary real components; order is preserved by increasing recoding, additive costs require transport. |
| E08: informed versus uninformed choice | Can carry the calculated optimum, but cannot infer the signal schedule from that value. | Needs the legal observation partition/policy menu; evaluating a pointwise maximum alone can be unattainable. | Choice placement at observed interfaces makes the schedule explicit; the conditional joint model is still required. | Needs legal policy labels/compatibility; a frontier of statewise chosen outcomes can promise unavailable guarantees. |
| New separating query: weighted optima versus deterministic hard budgets | Even all nonnegative weighted optimum values merge the two menus in section 5.4. | Can distinguish them if actual menu/performance vectors are retained; their weighted summaries alone do not. | A supplied deterministic output menu with the right terminal tests can distinguish them; one family of linear tests may not. | The nonconvex frontier distinguishes them directly without introducing probability. |

The mathematical-family comparison also distinguishes **what is a primitive**:

| Candidate | Primitive object | Natural order | Directly supported composition | Deliberately not automatic |
|---|---|---|---|---|
| S | Evaluated real in a fixed scope/unit | Numerical value order | Additive returns; fixed mixtures | Joint nonlinear outcome queries or unknown future contexts |
| P | Common-index payoff function | Pointwise or declared test-relative order | Aligned pointwise operations | Which output-dependent choices are operationally attainable |
| T | Finite typed response map to continuation values | Pointwise order on declared downstream tests | Backward value propagation / forward step sequencing | Parallel coupling, shared hidden uncertainty, unrestricted future-task approximation |
| G | Set of attainable budgets, finitely generated | Inclusion of capability sets | Menu choice and compatible resource-relation composition | Probability semantics, uncontrolled outcomes as choices, universal scalar ranking |

### 6.1 A concrete scientific-versus-mathematical-use boundary

In the E06 residue example, a legal decoder gets only `N mod k`, not the original
N. For uniform `N in {0,...,5}`, F01 proves best losses `1/2` for predicting parity
from residue three and `2/3` for predicting residue three from parity. The pair
of residues determines N exactly on that domain.

This is an interpreted finite example, not an assertion that one axiom system
is metaphysically correct or that these candidates already reason about arbitrary
theoremhood. P can represent the per-case loss of each legal decoder; S can
carry each resulting mean; G can record deterministic exact-decoder capability;
T can compose a decoder with an explicitly information-preserving interface.
They answer different parts of the operational question. Giving a decoder access
to N, choosing it separately after seeing N, or assuming that a marginal residue
law already contains its relation to N changes the example.

Consequently, none of the four is advertised as having solved the project's
whole mathematics motivation merely by fitting this finite case. A later core
must explain its expressions and inference rules for formal-system use, not
relabel arithmetic tables as a theoremhood calculus.

## 7. Relations between candidates, without erasing their differences

Several fragments translate exactly. S embeds into T's singleton shift maps,
and nonempty one-coordinate G fronts reduce to scalar minimum-cost algebra.
For the latter, switching sign converts minimum cost to maximum payoff;
the empty frontier still needs an explicit extra state or extended value, since
it is not a finite real. P profiles can be encoded as T's scenario-indexed
pure-reward maps, but the mapping does not preserve ordinary function addition
as profile addition without correcting duplicated continuation payoff.

These observations prevent a false four-way exclusivity. “Pick a foundation”
need not mean discard every other mathematical object. S may be an evaluation
layer of P, T, or G. A profile can generate a guarantee front for a declared menu;
a typed transformer can sequence steps whose resource effects are separately
bounded. But bundling all objects together without a useful interface would
avoid rather than answer the foundational question.

Two research distinctions should survive any later combination:

**Operation-relative information sufficiency.** A representation can be sufficient
for one evaluation while failing to preserve an operation used next. E03's
means, G's weighted optima, and T's stagewise lower values all demonstrate this
in different ways. Their positive repairs retain *specific* missing information,
not every raw model detail.

**Tolerance-relative task sufficiency.** Restricted downstream span gives a useful
T comparison even though unrestricted continuations force identical transition
laws. S-interval can certify a threshold without exact recovery. G can answer a
budget query without imposing a total ranking. These are distinct realizations
of F01's original “good enough for the requested use” requirement.

## 8. Assumptions and open obligations

The candidate-level derivations above establish neither a permanent value
ontology nor a full inference calculus. In particular:

| Item | Status now | What remains to be tested |
|---|---|---|
| Additive scalar fragment | Explicit and conditionally demonstrated | Which operational language should expose its legal compositions? |
| P's alignment and evaluation laws | Explicit finite formulas and separating examples | Which joint information can be compressed while retaining repeated operations and tolerances? |
| T's finite generators and closure under min/max/composition | Explicit, with a rejected concavity restriction | Can a small type/interface system reliably prevent hidden-information and shared-uncertainty mistakes? |
| T's restricted-span comparison and error chaining | Proved for the stated finite primitives / monotone shift maps | How should useful continuation families be selected and propagated without an arbitrary global cap? |
| G's budget frontier and compatible cost relation | Explicit non-probabilistic construction | When can witness labels/endpoints be removed without losing future capability? |
| Nonnegative scalarizations lose a nonconvex budget distinction | Exact finite counterexample | How do permitted lotteries, worst-case caps, and alternative tests change the relevant equivalence? |
| Full F01 coverage by any one small candidate | Not established | Which queries belong in the core and which should have explicit extensions? |
| General soundness, completeness, novelty, learnability, and performance advantage | Not claimed | Later tasks and their evidence gates remain required. |

No candidate is selected here. S remains a legitimate restricted baseline, and
P, T, and G each offer a different extension worth auditing. F03 should check
the relevant existing foundations and the exact assumptions of any imported
result; F04 should attack the candidates using discriminating examples. A later
Gate A may select a development question only on that combined evidence.
At the end of S1, the task still required its remaining measured D60 work.
S2 now completes that obligation and the comparison checks; see §11 and the
completion record. Word count and test count alone do not discharge a time floor.

## 9. Same-agent reconstruction: two further information boundaries

This is a non-blinded self-review, not independent review or completion of F16.
Its purpose is to test whether the proposed meanings answer the same operational
questions, rather than let a more expressive-looking notation win by changing
quantifiers.

### 9.1 Capability of a menu is not one fixed implementation

T's controlled maximum `D(h)=max(h_L,h_R)` describes a menu that can choose a
branch after the downstream objective h is specified. For every h there is a
best branch. There is no one fixed branch that attains D for every h: `(1,0)`
requires L and `(0,1)` requires R. Thus

$$
\text{for every }h\text{ there exists a branch achieving }D(h)
$$

must not be strengthened to existence of a single branch that achieves D for
all h. A maximum node's strategy may depend only on information actually
available there, including whether the task itself has already been specified.

G makes an analogous capability statement: each feasible budget may have a
different witness in the menu. Inclusion of budget sets does not assert one
fixed witness satisfies every budget simultaneously. S's maximum retains a
best evaluated value for one request and may likewise erase the witness;
a fixed P profile denotes one outcome profile until an explicit menu is added.
These distinctions qualify the common-example table rather than favor a candidate.

There is a stronger separation even for T's **entire optimized continuation
response**. Let one library permit only zero-cost deterministic outputs L or R.
A second additionally permits a half/half lottery over them. If independent
randomization is not otherwise supplied by the interface, these are different
available libraries, yet for every scalar terminal h they induce the same map:

$$
\max\{h_L,h_R\}
=\max\{h_L,h_R,(h_L+h_R)/2\}.
$$

Now assign two terminal *cost components*: L has costs `(0,2)` and R has costs
`(2,0)`. Require both **mean** costs to be at most one. Neither deterministic
use meets this request, whereas the added lottery has mean vector `(1,1)` and
does. Hence the optimal scalar-continuation map alone does not preserve every
multi-constraint capability of the underlying menu.

This is not the per-realization budget question in section 5.4: the lottery here
satisfies a newly declared mean-cost contract, not a bound on every realized cost.
It is also not a failure when free independent randomization is already part of
both libraries; then both can construct that lottery and the separation disappears.
The exact hypothesis is restricted available controlled programs.

Retaining T's generator syntax or policy menu could distinguish these libraries,
but then that extra structure—not their identical response functions—is doing
the work. A syntax inspection cannot be claimed as an inference from only the
extensional response map. The alternative is to restrict later questions to the
scalar-continuation family for which the maps really are equivalent.

### 9.2 A positive robust extension of G, without probability

A finite nonempty set of possible models does not always require retaining its
full joint table forever. Suppose a fixed legal action a has d cost components
`c_j(a,theta)`, and the query is exactly whether **one action chosen before the
unknown model is revealed** satisfies every coordinate cap in every model.
Define

$$
\bar c_j(a)=\max_\theta c_j(a,\theta),\qquad
\Gamma_{\rm before}=\Gamma_{\{\bar c(a):a\text{ is legal}\}}.
$$

Then membership is exactly the desired statement:

$$
b\in\Gamma_{\rm before}
\quad\Longleftrightarrow\quad
\exists a\ \forall\theta\ \forall j:\ c_j(a,\theta)\leq b_j.
$$

For each a, taking the maximum separately in each coordinate is equivalent to
its universal cap; a single model need not attain all coordinate maxima. Pareto
pruning these robust vectors then preserves this specified family of queries.
The claim is a finite conditional equivalence, not calibration from observations.

For one action with costs `(0,1)` in one model and `(1,0)` in the other, the robust
capability vector is `(1,1)` even though it is never realized. It is nevertheless
exact for componentwise universal budgets. But the total cost is always one,
not two. Applying a sum objective after the robust-coordinate compression loses
that correlation. Thus even this exact compression has an operation boundary.

If model observation is allowed before action selection, the capability is
instead

$$
\Gamma_{\rm after}=\bigcap_\theta
 \Gamma_{\{c(a,\theta):a\text{ is legal in that model}\}}.
$$

Here each model can have its own action witness. With one cost and the two-action
cost table `a:(0,1), b:(1,0)`, a pre-observation action requires budget one, whereas
post-observation choice requires only zero. This is a declared change in
information access, not a mathematical contradiction or a cost-free repair.
The extension demonstrates useful non-probabilistic reasoning while preserving
the distinction between controlled menus and uncontrolled possibilities.

### 9.3 Totality and signed-cost assumptions stay explicit

T's stochastic rows sum to one. This is a finite total-step model, which can
include a declared failure/fallback outcome as a state but does not prove that
failure never occurs. A subprobability operator `T(h)=h/2` would violate the
common-shift law `T(h+c)=T(h)+c`; its rows are correctly excluded from the current
candidate rather than covered by the same theorem. Infinite execution and
termination-sensitive semantics need separate treatment.

G with arbitrary signed costs has zero-cost identity `{0}`, but that identity
is not necessarily the greatest capability: a rebate cost `{-1}` can meet
budgets that `{0}` cannot. Thus a theorem for an algebra requiring its
multiplicative identity to be a greatest value cannot automatically be imported.
With a declared nonnegative resource domain that boundary can change. The
[limited source check](../work_logs/F02_2026-09-21_S1_sources.md) records this as an
assumption to audit, not as an already verified external theorem.


### 9.4 Scope corrections from the final candidate audit

The T candidate is the **extensional response map**, with finite expressions as
a constructive representation. It is not at the same time a syntax-sensitive
policy menu. The distinction matters because section 9.1 gives different menus
with the same response map. The definitions above now state explicitly when a
branch witness or syntax is additional retained information. This clarification
does not select a core or add an inference rule.

Similarly, P's finite-theta uncertainty extension and an arbitrary relational
constraint set are not identical carriers. The covariance-constrained family
mentioned in section 3.5 requires that extra set description (or an independently
justified finite reduction), rather than being a capability earned by an
unexplained finite list. F01 supplies the interval argument; F02 distinguishes
representability of the premises from an algorithm for deriving their bound.

The type checks in the executable fixtures reject mismatched dimensions, units,
and probability rows. They do not certify observation access, empirical validity
of a kernel, or that a pair of policy labels is actually compatible. Those
remain explicit premises of the demonstrations, not facts established by the
Python type annotations.


## 11. F02 completion and interpretation refinements

The [S2 supplement](02a_candidate_reconstruction.md) preserves the comparison
rather than freezing a favorite core. All-weight optimum agreement identifies
convex upper budget hulls, not arbitrary deterministic feasible menus. Permitting
lotteries and charging expected resources changes that question; per-use caps
and common hidden-model choices need separate treatment. A fixed weighted task
can nevertheless admit a much smaller exact endpoint cost kernel for sequencing.

Finite continuation expressions characterize a precise class of order- and
common-shift-preserving piecewise-affine maps when arbitrary finite stochastic
affine primitives are allowed. That is an extensional result, not preservation
of hidden action menus, observations or resource costs. Boolean terminal tests
alone can miss differences between nonlinear expressions. Explicit piecewise
structure supplies a finite comparison repair on bounded relative-stake domains.

Guarantee fronts admit directed, unit-aware approximation bounds and controlled
finite rounding. Directly squashing large absolute values can destroy even
bounded-relative-stake decisions, but centering before encoding and retaining
the common offset supplies a constructive bounded-coordinate alternative.
Algebraic, operational, task-family and numerical closure are separate tests.
The supplement ends with one shared signal/error/cost example interpreted by
all four candidates, with the same admissibility inputs and observation access.

These are conditional candidate-level results and same-agent reconstructions.
The 124 passing checks support their finite fixtures; general statements rely
on the displayed proofs. No novelty, independent review, final calculus,
F03 completion or readiness-gate pass is asserted. F03 is the next task.
