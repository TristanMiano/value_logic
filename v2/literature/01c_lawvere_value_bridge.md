# F03 continuation: from Lawvere truth values to pragmatic value

Research date: September 23, 2026. Source repository revision:
`3b5846099ad0ffb6194a5a259b3a0f369d9a9fee`.
Status: a source-informed bridge audit, not a selected calculus or a passed gate.
The author suggested using Rational Lawvere Logic's `[0,infinity]` truth values
as a conceptual bridge to value, possibly unbounded in both directions.
This note makes several different meanings of that proposal precise.

Read alongside [the source cards](01_foundations.md),
[the preceding proof-system audit](01b_proof_system_audit.md), and
[the source manifest](F03_sources.json). The [session record](../work_logs/F03_2026-09-23_S3.md)
records actual effort; interrupted attempts receive no invented time credit.

## 1. What is borrowed, and what is being proposed

**S12 source interface.** Bacci, Mardare, Panangaden and Plotkin,
*Rational Lawvere Logic*, CSL 2026, sections 2-4 and 6, interpret formulas in
`[0,infinity]`: zero is true, infinity false, tensor is addition, conjunction
is maximum, disjunction minimum, and implication is truncated subtraction.
Sequents require the antecedent sum to exceed or equal the consequent.
Definitions 5-6 separate semantic consequence from its disjunctive proof closure.
Theorems 7 and 9 give soundness and finite-theory completeness; Theorem 11 uses
explicit finiteness hypotheses for polynomial sequents. These are the source's
results, not newly proved project metatheorems. The displayed double-negation
finiteness test in section 3, rather than inconsistent informal glosses, is the
interface used below. Source: [publisher paper](https://doi.org/10.4230/LIPIcs.CSL.2026.3).

**S13 targeted comparison.** Metcalfe, Olivetti and Gabbay,
*Sequent and Hypersequent Calculi for Abelian and Lukasiewicz Logics*,
arXiv:cs/0211021v1, Definition 4, section 2.3, Definitions 10-11 and Theorem 12
(printed pp. 4-6), supplies a signed alternative: real-valued Abelian logic with
addition, ordinary negation, minimum, maximum and zero. Formula validity means
nonnegative value. Its implication is the difference of consequent and
antecedent. The reported characteristic-model result concerns this signature;
it does not automatically include nonzero numerical constants, ordinary binary
multiplication, division, infinity, or arbitrary constrained consequence.
Source: [inspected preprint](https://arxiv.org/abs/cs/0211021v1).

This additional source answers the newly requested two-sided-range question.
The original source identities and comparison scope remain intact.
The calculations below are project-side translations and counterexamples from
these declared interfaces. They do not assert novelty or implement either
source's complete deduction system.

The central distinction is between **giving existing numerical semantics a
pragmatic interpretation**, **encoding another structure inside it**, and
**changing the semantic algebra and hence its proof obligations**. All three
are legitimate research options, but they are not the same operation.

## 2. Bridge A: keep nonnegative semantics and interpret quantities as costs

Suppose formulas X and Y denote nonnegative, dimensionless loss quantities,
and E denotes a proposed allowance. The numerical interpretation of

$$
E\vdash X
$$

is exactly `E >= X`: the supplied allowance covers the loss. No absolute
metaphysical truth is needed to stipulate these numbers or to prove a conditional
inequality about them. Whether the premises describe an actual model's behavior
remains an evidence question, outside this arithmetic implication.

For finite x and y, define the defect

$$
r(x,y)=(y-x)_+ = \max\{y-x,0\}.
$$

It is the additional allowance needed when x is already available and y is
required. Directly, for c,x,y nonnegative and finite,

$$
c+x\geq y\quad\Longleftrightarrow\quad c\geq r(x,y).
$$

If y exceeds x, subtract x; otherwise both conditions hold for every
nonnegative c. This two-case proof explains the truncation operationally.
It also shows why the nonnegative restriction on c matters later.

A concrete composition starts with losses x=2/5 and y=7/10. Premises give
`a >= x`, `b >= y`, and `z <= x+y`, where a=1/2 and b=3/4. Adding and chaining
produces `z <= a+b = 5/4`, without needing z's exact value. These are numerical
premises and a conditional arithmetic conclusion, not empirical calibration.

### More reward is not automatically more truth in the source order

Interpreting a large source number as a large benefit is possible as a labeling
choice, but it does not make the source's zero-designated order into
larger-is-better preference. Specify which inequality is meant. A simple
cost-to-benefit reversal is v=-c: it maps `[0,infinity]` to `[-infinity,0]` and
reverses numerical inequalities. It does **not** produce all real values.

For example, source costs 2 and 5 correspond to benefits -2 and -5. The source
sequent `5 |- 2` then says `-5 <= -2`. Relabeling the original costs as rewards
without the reversal would express a different comparison.

### One deficit is not the entire value object

A threshold deficit `(tau-v)_+` erases every distinction among values v>=tau.
At tau=5, values 6 and 100 both have zero deficit. This is exactly sufficient
for checking that threshold and insufficient for ranking those two rewards or
answering arbitrary new thresholds. A defect can therefore be a useful
primitive for a stated query without being a universal replacement for value.

## 3. Bridge B: finite signed values inside the nonnegative arithmetic

This extends the preceding session's finite-pair adapter by stating the exact
semantic-consequence transfer and its limitations.

Let a pair `(a,b)` of **finite** nonnegative reals denote the signed value
`a-b`. There is no global magnitude bound. Pairs are equivalent when

$$
(a,b)\sim(c,d)\quad\Longleftrightarrow\quad a+d=c+b.
$$

This is an equivalence relation: it is equality of decoded real numbers.
Every real x has a representing pair `(max(x,0),max(-x,0))`; a representation
need not be canonical. Adding the same finite amount to both entries changes
neither its decoded value nor any correctly translated comparison.

The following operations respect the equivalence:

$$
(a,b)+(c,d)=(a+c,b+d),\qquad -(a,b)=(b,a),
$$

$$
(a,b)(c,d)=(ac+bd,ad+bc).
$$

Subtracting the output entries gives, respectively, the sum, negative, and
product of the decoded inputs. Thus the quotient is an ordered additive group
(and, with this product, a ring) isomorphic to the finite real numbers. This is
an explicitly reconstructed familiar algebraic construction, not a new
representation theorem for an agent's policy.

For signed terms t and s represented by pairs `(t+,t-)` and `(s+,s-)`,

$$
t\leq s\quad\Longleftrightarrow\quad
 t^++s^-\leq s^++t^-.
$$

The compiled RLL sequent has `s+` and `t-` on its antecedent side and `t+ + s-`
on its consequent side. Keeping the sides in this order is essential.

### 3.1 Exact transfer of finite polynomial consequence

Consider a finite set H of weak inequalities between finite real polynomial
terms and one such target inequality gamma. Normalize each term into a pair
using the operations above. Translate every inequality by the cross-sum rule,
and add a source finiteness sequent for every positive/negative variable used
anywhere in H or gamma. Write this guard collection as Fin.

Then

$$
H\models_{\mathbb R}\gamma
\quad\Longleftrightarrow\quad
\widehat H\cup\mathrm{Fin}\models_{\mathrm{RLL}}\widehat\gamma.
$$

**Proof.** Every guarded RLL assignment decodes to a finite real assignment;
structural induction on the terms preserves their values and the cross-sum
rule preserves every comparison. Conversely, every finite real assignment has
finite nonnegative representing pairs. Therefore a countermodel on either
side supplies a countermodel on the other. Noncanonical choices cause no
problem because the decoded expressions are equal. This establishes both
directions, including satisfiability preservation for H. If H has no model,
both semantic-consequence statements are vacuous; this does not certify an
operationally usable model or waive the project's nonempty-evidence requirement.

Consequently S12's **Theorem 11 (polynomial completeness)** applies directly
to this compiled finite instance: the translated premises and target are
polynomial sequents, and Fin restricts every letter in their union. Use the
fully parenthesized guard `|- ((P -o infinity) -o infinity)`. The non-polynomial
guards are exactly the additional finitising hypotheses permitted by that
theorem. This uses the source's **full** deduction system, not an arbitrary
subset of its rules. It is a conditional reuse of the theorem after proving
the semantic adapter, not a new completeness proof, an implemented complete
prover, or a polynomial-time algorithm. No infinite-premise rule is obtained. Finite constants in the
source language and the representation of those constants in an implementation
must also be specified; a rational fixture is not a representation of every
real input by a finite bit string.

### 3.2 A signed numerical example

Suppose b is a benefit, c a cost, and a resource rule states c<=b+2. The net
value n=b-c must satisfy n>=-2. For b=1/2 and c=2, n=-3/2. Writing benefit and
cost as finite nonnegative channels already makes the deduction visible:
`c <= b+2` is the same inequality as `b-c >= -2` after rearrangement.
This is a net-value calculation, not a requirement that all quantities in
Value Logic be decomposed into economic benefits and costs.

For arbitrary signed b or c, the same cross-sum translation works without a
fixed shift chosen to make all future values positive.

### 3.3 Why finiteness is not optional

If all four entries a,b,c,d are infinity, the cross-sum equality holds in
source arithmetic, but neither difference denotes a real number. Such a pair
must not become a fake signed zero. A bound on magnitude is unnecessary;
**finiteness of each entry** is necessary for this particular decoding.

Nor can a nontrivial additive encoding of all real numbers use just one
ordinary nonnegative number while preserving zero and ordinary addition.
If f does so, then

$$
f(x)+f(-x)=f(0)=0.
$$

Both summands are nonnegative, hence each is zero, for every x. Such a map is
constant. This does not forbid a scalar code with transported operations, a
restricted domain, or the two-channel construction; it identifies which laws
cannot all be retained by the single-number proposal.

### 3.4 Division requires a domain contract

A signed quotient z=x/y, y!=0, can be encoded by its finite polynomial graph
`yz=x`, together with the nonzero guard. For pair inputs x=(a,b), y=(c,d) and
output z=(e,f), that graph is

$$
ce+df+b=cf+de+a,\qquad c\ne d.
$$

Both sides are nonnegative polynomials. This characterizes the decoded quotient
uniquely, although it does not choose unique representing pairs. With x=-6,
y=-2 and z=3, the two sides both equal 6. Omitting the nonzero guard when x=y=0
allows every z, so the graph no longer means a defined quotient. RLL's total
endpoint division must not be substituted for ordinary partial signed division.
This graph adapter is not a claim that the full signed rational syntax has
already been implemented or that existential witnesses are available policies.

## 4. Bridge C: a signed logical algebra, rather than a signed encoding

There is a genuine existing signed-valued comparison to study: S13's real
Abelian algebra. Here zero is a neutral group value, not the largest or smallest
number. In its stated convention a formula is valid when its value is
nonnegative for all assignments. This already answers the narrow possibility
question: a logic can have a two-sided unbounded real value domain.

That does not identify its values with practical utility or import S12's
nonnegative rules unchanged. The following independent arithmetic checks expose
what would change for a direct signed **cost-oriented** sequent interpretation
`sum(Gamma) >= value(phi)`.

**Unrestricted left weakening fails.** `0 |- 0` is valid numerically. Adding
an antecedent of value -1 would give `-1 >= 0`, which fails. Adding an antecedent
known nonnegative is safe. This concerns occurrences *inside* a sequent, not
the ordinary monotonicity of semantic consequence when more hypotheses are
assumed.

**The residual loses its truncation.** When c ranges over all finite reals,

$$
c+x\geq y\quad\Longleftrightarrow\quad c\geq y-x.
$$

For x=2,y=1,c=-1/2, the left side holds. Replacing the right side by
`c >= max(y-x,0)` makes it false. A direct signed group and the nonnegative
cone therefore have different additive implications.

**Multiplication needs sign-sensitive order rules.** From 1>=0, multiplying
by -1 yields -1<=0, not -1>=0. Source rules relying on monotonicity in both
nonnegative factors do not become globally monotone rules for signed products.
S13's connective named addition is not ordinary binary real multiplication.

### 4.1 An exact limited bridge to the signed algebra

There is a small translation that can be proved without importing an enlarged
source theorem. S13's Definition 21 gives a clipped implication and its
Definition 23 clips atoms to a bounded negative interval. Those are close
antecedents, not the same translation as the unbounded negative cone below.
Take the **finite, constant-zero, additive** RLL fragment:
variables, 0, addition, truncated implication, min, and max. Exclude infinity,
nonzero numerical constants, ordinary multiplication, and division.

In the real Abelian algebra, translate a variable p to `min(p,0)`. Translate
addition to addition, a source implication a to b to
`min(e(b)-e(a),0)`, source cost-max to target min, and source cost-min to target
max. Denote the translation by e. For any real assignment v, set
`c(p)=-min(v(p),0)`. An induction gives

$$
e(t)(v)=-t(c).
$$

All finite nonnegative source assignments arise this way (take v(p)=-c(p)).
Thus a source sequent `t1,...,tn |- s` is valid over finite nonnegative values
exactly when the target Abelian formula

$$
(e(t_1)+\cdots+e(t_n))\to e(s)
$$

is nonnegative for all real assignments. The empty sum is zero. This is a
validity bridge for the stated small signature; S13's characteristic-real-model
result pertains to the resulting target formula. It is **not** a claimed
translation of all RLL consequence or its positive constants into unextended
Abelian logic. The opposite cost/benefit polarities are accounted for by the
explicit minus sign, not by identifying same-named connectives. Both source
and target additive operations here are commutative arithmetic operations;
this does not identify them with candidate T's generally noncommutative
composition of processes.

### 4.2 An actual infinity endpoint needs a separate design

A domain unbounded in both directions can simply be the finite reals; it need
not contain either infinity. If infinity is included, familiar finite rules
need review. In particular there is no faithful additive map from the full
nonnegative extended monoid into an additive group: since infinity+x=infinity,
cancellation after mapping would force the image of every x to be zero.

This is not an impossibility theorem for all signed extended algebras. One can
change endpoint operations, drop cancellation at endpoints, or use partial
operations. None of those choices is accomplished merely by extending the
notation `[0,infinity]` to `[-infinity,infinity]`.

## 5. Bridge D: signed values with nonnegative directional loss

One need not require value coordinates and comparison grades to have the same
range. Let Q be a nonempty family of tasks in comparable, normalized value
units. Each model M has finite real values V_q(M); the family need not be
uniformly bounded. Define

$$
\Delta_Q(M,N)=\sup_{q\in Q}\bigl(V_q(M)-V_q(N)\bigr)_+.
$$

This is a nonnegative extended quantity measuring the largest loss from
replacing M by N on the specified tasks. In particular, Delta<=epsilon means
`V_q(N) >= V_q(M)-epsilon` for every admitted q. The statement is relative to
the given value model and task family, not a guarantee that the model is final.

### 5.1 Composition and zero grade

For finite real x,y,z,

$$
(x-z)_+\leq(x-y)_+ +(y-z)_+.
$$

The sum on the right is nonnegative and at least `(x-y)+(y-z)=x-z`, proving
the inequality. Applying it taskwise and taking suprema gives

$$
\Delta_Q(M,P)\leq\Delta_Q(M,N)+\Delta_Q(N,P).
$$

The extended case is harmless: an infinite right side bounds every left side.
Self-distance is zero. Zero directional grade means N weakly dominates M over
Q; it does not require equality or symmetry. Zero grades in **both** directions
mean equality of these task-value profiles, not identity of the physical models.
This reconstructs a Lawvere-style directed-distance interface from signed
values without altering the nonnegative grade arithmetic.

A sharp two-task fixture is M=(5,-2), N=(4,1), P=(2,0). Its successive losses
are 1 and 2; the M-to-P loss is 3. Reverse replacement N-to-M costs 3, not 1.
The input values include negatives, but no negative error allowance is needed.

### 5.2 Unbounded absolute values need not imply unbounded replacement loss

On tasks indexed by all integers n, set V_n(M)=n and V_n(N)=n-1. Both profiles
are unbounded above and below, but their replacement loss is exactly one.
A shared task-dependent offset k(q) cancels in every difference, however large
it is. Model-specific offsets do not generally cancel. These observations
preserve differences, not a purported uniform representation of absolute value.

This does not mean RLL's finite formula language directly contains arbitrary
suprema over infinite Q. Finite Q gives a finite maximum expression; infinite
Q needs a separately justified uniform bound or an explicit semantic extension.
The displayed integer example is justified by its pointwise identity, not a
finite numerical test purporting to enumerate all integers.

### 5.3 Information still matters

Applying a unary nonnegative transformation to each component mean cannot
restore missing dependence. The F01 means for X=(3,-1) and Y=(-1,3) are both one;
changing Y to X keeps both means but changes the mean pointwise minimum.
RLL arithmetic can process supplied joint quantities; the choice of a truth-value
range does not supply them. The same distinction holds between an arithmetic
existence statement and one action available under the actual observation
schedule. No bridge here closes F01/F02's information or witness obligations.

## 6. Implications for the candidate comparison

The author's proposed conceptual bridge is viable in several precise senses.
There is no need to assume a Boolean metaphysical verdict before writing
numerical, value-related inference. Equally, sharing a number range is not
by itself a proof that two calculi have the same rules or meaning.

| Bridge | Preserved directly | Additional obligation |
|---|---|---|
| Nonnegative cost interpretation | The existing numerical interface and its source proof results | Task meaning, units, evidence, and correct comparison polarity |
| Finite signed pairs | Finite signed arithmetic and compiled finite polynomial consequence | Finiteness/type guards and a real compiler/proof checker |
| Direct signed algebra | Ordinary signed addition, subtraction and lattice operations | Exact chosen signature and its own consequence/rule justification |
| Signed values, nonnegative replacement grades | Two-sided value profiles and directed loss accounting | Task scope, joint information, and realization of composed uses |

These can be compared or combined; they do not constitute a fifth selected
candidate. The immediate F03 outcome is an exact map of reusable results and
remaining obligations. S12 and S13 deserve comparison before inventing a new
arithmetic proof system. Neither has been chosen as the core. F04, Gate A,
implementation of a reasoner, and a phase-wide soundness theorem remain later
work. The source audit can be useful while its protected literature time is
still incomplete; the task checkbox must follow the measured record.


## 7. Source-text issue and a conservative import boundary

In S12 section 6, Phase 5 Stage 2 (printed p. 3:15), both the retrieved PDF
text and publisher HTML interchange the labels on the constant sequents
`0 |- 1` and `1 |- 0`. Under the paper's stated sum-at-least-consequent
semantics, the first is false and the second true. Thus a normalization
implementation must not use that retrieved replacement paragraph literally.
The consistent replacements are `1 |- 0` for a valid sequent and `0 |- 1`
for an unsatisfiable sequent. These two arithmetic checks do not depend on
any disputed general theorem.

A screenshot of that page failed, so this record identifies a retrieved-text
inconsistency, not an author-confirmed published erratum. It also does not
claim that the source's main completeness result is false: switching the
representatives would repair this local problem. The signed-polynomial
adapter in section 3 already lands in the hypothesis class of Theorem 11
and does **not** need Phase 5 or Proposition 12. Importing Theorem 11 remains
a reliance on its stated result, not an independent verification of the full
Positivstellensatz-based proof or a claim that a corrected full normalizer has
been implemented here. The earlier double-negation parenthesization issue
likewise remains explicit; our guard is defined by its fully parenthesized
formula and checked directly at finite values and infinity.
