# F03 continuation — proof-system and solver import audit

Session: 2026-09-22-S2 (America/Los_Angeles; observed clocks on September 23 UTC).
Source revision: `973af3cd668fb4f558f2ca30133da3779a68e1b4`.
Status: continued source audit; task completion depends on the recorded L60 minimum.
No core, F04 result, or readiness-gate decision is introduced.

This note supplements [the source cards](01_foundations.md) and
[the first mapping note](01a_import_boundaries.md). S01–S11 retain their original
identities and inspection records in [the source manifest](F03_sources.json).
A newly located 2026 paper is added as S12 because it directly addresses the
unbounded arithmetic/consequence question, not to increase a source count.

## 1. Source-level checks and limits

### S02: distinguish substitution from reflection

In Mardare–Panangaden–Plotkin's accepted LICS 2016 manuscript, Definitions
2.1–2.2 specify the substitution and infinitary Archimedean rules; Definition
3.1 fixes max-product nonexpansiveness. Theorem 5.2 is the completeness statement
for that theory, not for any proposed Value Logic signature.

The parsed paragraph between Theorems 5.1 and 5.2 contains an apparent claim
that arbitrary substitutions reflect unconditional provability and preserve
distance exactly. Identifying substitutions need only decrease distance; the
small example in section 2 checks this independently. A page-2 screenshot was
unavailable, so this is recorded as an unresolved transcription/proof-step
question, not a confirmed published erratum. The paragraph's immediate
nonexpansiveness goal needs only the weaker direction. Separately, converting
local hypotheses into universally substitutable axioms needs justification.
Neither observation refutes the stated completeness theorem. We do not use an
unreconstructed stronger proof step as a premise.

### S10: its substitution and completeness are not a finitary shortcut

Mio–Sarkis–Vignudelli (LMCS 2024), Definition 4.1, requires a substitution to
preserve the entire supplied variable relation. Theorem 4.4 proves soundness.
Definition 5.2 quotients by provable **ordinary equality**, while Lemma 5.3 uses
order-completeness for the inferred distance. Lemmas 5.7–5.12 support Theorem
5.13's completeness argument; footnote 10 explicitly uses choice of
representatives. These are not claims of decidable finite proof search.

Section 9.1 compares *basic*, variable-premise quantitative inferences with its
relation-indexed equations. The proof systems are not related simply by deleting
non-basic derivations. The discussion also distinguishes bounded relations
from the earlier extended metrics. Section 8 supplies the additional laws for
selected generalized metric categories. Arbitrary fuzzy relations do not
silently inherit symmetry, separation, or triangle laws. Our finite translation
below keeps these hypotheses explicit and does not import free-algebra or monad
results beyond the stated interface.

### S06: algebra, solution preservation, and termination are different checks

Bistarelli–Montanari–Rossi (JACM 1997), Definitions 2.1–2.2 and section 4,
distinguish semiring structure from hypotheses of their local-consistency
algorithm. Theorems 4.9/4.13 and 4.16 use multiplicative idempotence for the
stated equivalence/order results; Theorem 4.14 supplies a separate finite
closed-value-set termination condition. Thus an algebra match is not by itself
a solver correctness or termination result.

The paper also supplies a positive alternative: Definition 5.1's parsing-tree
conditions, Definition 5.2, and Theorem 5.3 concern a structured bottom-up
solution computation. This is not the same unrestricted repeated propagation.
Section 3's combination/projection identities and the parsing conditions matter.
The finite example below illustrates elimination without reusing a factor; it
does not assert the general theorem for a carrier outside the paper's axioms.
The inspected author-uploaded full text has damaged mathematical typography;
only unambiguous clauses and separately reconstructed finite identities are used.

### S12: a directly relevant arithmetic logic published in 2026

Giorgio Bacci, Radu Mardare, Prakash Panangaden and Gordon Plotkin,
*Rational Lawvere Logic*, CSL 2026, LIPIcs 363, 3:1–3:21,
DOI `10.4230/LIPIcs.CSL.2026.3`, is an additional primary antecedent.

Sections 2–4 interpret formulas over `[0,infinity]` with explicit endpoint
arithmetic. A sequent sums its antecedent formula values and compares the sum
with its consequent; repeated formula occurrences matter. Definition 6 includes
disjunctive consequence, not only single-rule chaining. Theorems 7 and 9 give
soundness and finite-theory completeness; Theorem 15 separates infinite-theory
noncompactness. Theorem 11's polynomial step includes finiteness premises and
uses the Positivstellensatz.

The syntax permits real constants. Section 7 restricts complexity statements to
binary-encoded rational constants: consequence is in PSPACE for the full logic,
and co-NP-complete for its affine fragment. Those statements do not supply a
polynomial-time reasoner or a theorem for signed/infinite arithmetic chosen
differently. This paper deserves an explicit comparison before inventing another
arithmetic deduction system. The adaptations below are narrower, independently
worked mappings; they do not choose S12 as the project core.

### S03–S05 and S07–S08: read the representation theorem at its actual scope

S03's section 3.3 works with positive linear **contractions** on measures:
subprobability mass is intentional. S05's Corollary 3.8 instead requires exact
additive homogeneity. These are compatible only after specifying which outcomes,
including nontermination, receive the common continuation shift. Renormalizing
survivors is a changed evaluation, not the duality in S03.

S04's Definitions 2.1–2.2 use a closed convex domain and finitely many affine
components; the interior-region proof uses that geometry. F02's global
finite-piece specialization fits this part of the theorem. S05's Theorem 3.4
and Corollary 3.8 remove the finite-piece requirement, but the outer minimization
can range over all input vectors and uses the unknown function's own values.
It is not a finite description or an implementation witness. S05's additional
positive-homogeneity requirement for a no-immediate-payment representation
must not be silently dropped.

S07's section 4.7.4 and Figure 4.9 were checked again, including the figure on
printed page 179 (PDF index 192). Strictly positive dual weights and merely
nonnegative weights have different Pareto implications. Source optima presuppose
attainment; scalar infima alone need not preserve a deterministic feasible menu.
The lottery permission in F02 is a separate operational premise.

S08's Assumption 1 and Theorem 1, equations (9)–(15), separate two decisions:
future conditional distributions may be pasted independently in the allowed
uncertainty family, and the adversary may choose a distribution for each
state–action pair. Equation (15) uses that latter structure to show that
randomization does not improve the robust value. The finite specialization
retains both conditions. A shared parameter constraining multiple actions is
not automatically covered, even for one decision epoch. No claim is made about
arbitrary unbounded rewards, measurable selectors, or the full infinite-horizon
extensions of the report.

### S11: exactness has an extra lifting hypothesis

Jurka–Milius–Urbat's section 4.2 uses c-reflexive quotients: each sufficiently
small target substructure has a relation-reflecting copy above it. Section 5's
Exactness theorem additionally assumes that every operation lifting preserves
surjective maps which both preserve and reflect relations. Its quotient object
is specified by a **compatible pair** of a refining relational structure and
an algebra congruence, not by an arbitrary numerical equivalence alone.

The named theorem and its proof sketch were checked; the entire categorical
appendix was not reconstructed. Section 6 explicitly leaves a concrete complete
deduction system as further work. Consequently a variety/exactness result is a
source for possible semantics, not a supplied executable proof calculus.
The HTML's broken theorem numbering is not used as a numerical locator.

### Source-transcription cautions

The primary mathematics takes precedence over ambiguous prose transcription.
In S12, section 3's displayed definitions and case table make `Z` a zero test
and `|phi|` double negation, whereas two later prose phrases disagree with those
displays. The numerical examples below use the displays and sequent semantics.
We do not transcribe ambiguous reduction pseudocode into a proof checker or
claim to have independently certified all of Theorem 9. Table 1's endpoint
arithmetic was visually inspected (PDF index 3); repeated attempts to render
Table 2 failed, so its typography is not claimed as visually checked.
These recorded issues are reasons to check exact equations, not declarations
that the published main theorems are false.

## 2. A substitution contract that can actually be checked

The following are elementary adapter arguments, not claims that a new calculus
has been chosen or that a published completeness proof has been re-proved.

### 2.1 Identifying variables need not preserve information

Take the empty algebraic signature with two freely distinguishable variables
`x,y`. An identifying substitution sends both to `z`. The substituted identity
`z=z` holds, while the original identity `x=y` does not hold in all two-element
interpretations. Likewise the discrete extended distance of the two free terms
can decrease from infinity to zero. Preservation under substitution therefore
does not imply reflection. This is the narrow check relevant to the S02
transcription issue in section 1.

Local premises and universal axioms are also different. Under one assignment,
`x=y` may hold while `z=w` fails; taking `(x,y,z,w)=(0,0,0,1)` witnesses that.
Adding `x=y` as a universally substitutable identity instead forces all elements
to agree. A source-import proof must explain the transition between these uses.
A possible repair is to freeze local variables as named constants, but the
conservativity of that translation is an obligation, not established here.

### 2.2 Finite variable-premise translation for S10

Let `X` contain every variable used in a finite set of relational premises
`Gamma` **and its conclusion**. For an ordered pair `(x,y)`, let

$$
r_X(x,y)=\inf\{\epsilon:(x,y,\epsilon)\in\Gamma\},
$$

using `1` when the set is empty. Premises and relations take values in `[0,1]`.
For a fuzzy relation `d_A` on an interpretation carrier, a map `v:X->A` is
nonexpansive exactly when

$$
d_A(v(x),v(y))\leq r_X(x,y)\quad\text{for every }x,y.
$$

With finite Gamma this is precisely satisfaction of all its supplied bounds;
unspecified pairs impose only the automatic bound one. Do not insert symmetry,
triangle closure, or zero diagonal unless those are part of the actual category.
The construction uses the relation as a variable context, not as a probability.

A substitution `sigma:X->Terms(Y)` is allowed only after each required pair of
substituted terms is proved within the corresponding `r_X` bound. To check the
semantic reason, choose an admissible interpretation `u:Y->A` and put
`v(x)=eval_u(sigma(x))`. The pair obligations make `v` admissible. Structural
induction gives `eval_v(t)=eval_u(sigma(t))`, so a valid conclusion at X
transports. Operation-specific metric laws are not obtained for free.

For example, a context permitting `d(x,y)<=1/5` cannot be replaced by one only
ensuring `d(u,v)<=9/10`. In the directed real relation below, values `u=0,v=9/10`
meet the latter premise and violate the former. This is a counterexample to
unrestricted contextual substitution, not to the guarded rule in S10.

### 2.3 Bounded relation, unbounded values, and a lost endpoint

For a declared positive unit scale `a`, define on all real values

$$
d_a(x,y)=\min\{1,(y-x)_+/a\},\qquad t_+=\max(t,0).
$$

This bounded, generally asymmetric relation distinguishes ordered shortfall.
Zero means `x>=y`, not ordinary equality. For `epsilon<1`, the inequality
`d_a(x,y)<=epsilon` is exactly `y-x<=a epsilon`. At `epsilon=1`, the statement
is automatic and gives no finite real-unit error bound.

Positive-part subadditivity proves the capped triangle and sum bounds. For
example,

$$
d_a(x_1+x_2,y_1+y_2)
\leq\min\{1,d_a(x_1,y_1)+d_a(x_2,y_2)\}.
$$

When a component distance is one the right side is one; otherwise the real
shortfall bounds add and then cap. Pointwise minimum and maximum instead admit
the maximum of the two component distances. These are checked numerical laws
for this declared relation, not imported from a theorem about arbitrary
operations.

Even scalar rescaling needs an endpoint condition. With `a=1`, `x=0`, `y=100`
and `lambda=1/2`, both the input and scaled-output distances are one. Thus the
claim `d(lambda x,lambda y)<=lambda d(x,y)` fails. For input allowance below
one, however, it follows from the real-unit bound that

$$
d_a(\lambda x,\lambda y)\leq\min\{1,\lambda\epsilon\}
\quad (\lambda\geq0,\ \epsilon<1).
$$

At input allowance one, the justified allowance is one for every positive
lambda, and zero for lambda zero. A bounded relation may encode unbounded
values without carrying uniformly recoverable finite error at its endpoint.
This directly separates S10's relation range from a universal value bound.

### 2.4 Why a zero-distance quotient can fail for a proposed summary

For two equally weighted scenarios define `d(X,Y)=|E[X]-E[Y]|`.
`X=(3,-1)` and `Y=(-1,3)` have distance zero. Keeping `Z=X`, their pointwise
minima with Z have means one and minus one. Thus equivalence by this distance
is not a congruence for pointwise minimum. It cannot define that operation on
mean-equivalence classes. This reuses F01's separating example to explain why
S10's ordinary-equality quotient must not be replaced by an arbitrary numerical
zero class. S02's nonexpansiveness premise excludes this failure; it is absent
from an arbitrary fuzzy-relation algebra.

## 3. Fixed arithmetic semantics: an explicit S12 test interface

All costs in this section are in one declared normalized unit. The endpoint
operations follow S12's displayed definitions. The checks implement arithmetic
and small examples only: **not its complete proof system or decision procedure**.

For nonnegative extended values, use ordinary extended addition, and
multiplication with `0*infinity=0`. Let `b dotminus a` and `b/a` satisfy

$$
c+a\geq b\iff c\geq b\mathbin{\dot{-}}a,
\qquad ca\leq b\iff c\leq b/a.
$$

The endpoint table forced by these adjunctions includes

$$
\infty\mathbin{\dot{-}}\infty=0,\quad
0/0=\infty,\quad b/0=\infty,\quad
b/\infty=0\ (b<\infty),\quad \infty/\infty=\infty.
$$

These are algebraic conventions with specific purposes. In particular, they
do not define a statistical conditional expectation on a null event.

### 3.1 Occurrences inside a sequent are resources

Write `Gamma |- z` for the numerical inequality `sum(Gamma)>=z`. With values
`p=1,q=2`, `p,p |- q` holds but `p |- q` fails. Removing a repeated antecedent
is therefore not a generally valid rule. This says nothing against reusing an
already established *hypothesis sequent*: source hypotheses form a set, whereas
antecedents inside one sequent form a list.

A small useful composition is different. From the bounds `1>=u`, `1>=v`, and
`u+v>=e`, adding gives `2>=u+v>=e`. This produces an allowance of two, not one.
The numerical example `u=v=1,e=2` attains it. This is one arithmetic instance
of resource-sensitive reasoning, not a choice of the eventual project syntax.

Cancellation is also guarded. `0+infinity >= 1+infinity` holds, but `0>=1`
does not. Cancelling a common **finite** nonnegative summand is valid, including
when the other summands are infinite; cancelling an infinite summand is not.
Likewise multiplying or dividing inequalities to eliminate a factor needs the
factor's sign and endpoint conditions. Merely naming a division operator does
not make those hypotheses disappear.

### 3.2 Finite consequence does not supply an infinite-premise rule

For a numerical variable `p>=0`, consider the premises `2^-n >= p`, one for
every integer `n>=1`. Together they force `p=0`. For any finite subfamily whose
largest exponent is N, `p=2^-N` satisfies it and is positive. No argument whose
premises are limited to that finite subfamily establishes the zero bound.

For a positive requested allowance delta, choose N with `2^-N<=delta`; the
single N-th premise does suffice. Exact zero and a positive tolerance have
different finite evidence requirements. This reconstructs the relevant
noncompactness boundary without pretending that the implemented fixtures prove
an infinite theorem or implement the source's finite-completeness procedure.

### 3.3 Arithmetic encoding is not evidence that the premises are consistent

The finite premises `0>=p` and `p>=1` have no nonnegative model. Consequently,
every numerical conclusion is a semantic consequence of them. That is ordinary
logical behavior, not a justified permission to act. A consumer requiring a
nonempty compatible evaluation model must check or receive that evidence
separately. This preserves F01's empty-evidence distinction when using a
complete arithmetic backend.

## 4. Signed polynomial comparisons without infinite subtraction

This is a finite semantic adapter, related to the positive/negative-polynomial
method in S12's Lemma 14, rather than a new primitive or an implementation of
its Positivstellensatz proof procedure.

Represent a finite signed real x by a pair `(x+,x-)` of **finite** nonnegative
reals satisfying `x=x+-x-`. A pair is not required to be canonical. Define

$$
(a,b)+(c,d)=(a+c,b+d),\qquad -(a,b)=(b,a),
$$

$$
(a,b)(c,d)=(ac+bd,ad+bc).
$$

Expansion verifies that decoding preserves addition, negation and
multiplication. Structural induction therefore translates every finite real
polynomial expression to a pair of nonnegative polynomial expressions.
For a comparison `t<=s`, the exact translated inequality is

$$
s^++t^-\geq t^++s^-.
$$

Every finite real assignment has a representing pair assignment, and every
finite pair assignment decodes to one, so translating a finite system of these
comparisons preserves its models up to that representation. Explicit finiteness
constraints are essential: `infinity-infinity` is not a decoded signed value.
No subtraction of infinities is introduced by this construction.

Minimum and maximum of two finite signed values also have a finite adapter:
use the common offset `b+d` to obtain

$$
\max(a-b,c-d)=\max(a+d,c+b)-(b+d),
$$

and the same identity with min. Thus some finite S/P/T calculations can be
encoded using the source arithmetic once their actual data, units, scope,
alignment and observation schedule are supplied. This does not recover omitted
information, preserve strategy witnesses automatically, or prove efficient
symbolic compilation. If the source's full finite-completeness theorem is used
as a backend, its whole deduction language and finiteness hypotheses remain part
of the import. Our tests verify the adapter, not that backend.

## 5. Nonconvex budget questions have a finite arithmetic encoding

Let `C={c_1,...,c_m}` be a **finite nonempty** set of normalized nonnegative
k-dimensional cost vectors, `k>=1`, and let b be a finite nonnegative budget.
Define the maximum violation of option i, then the best available violation:

$$
v_i(b)=\max_j(c_{ij}-b_j)_+,
\qquad v_C(b)=\min_i v_i(b).
$$

Every component violation is nonnegative. The maximum is zero iff all component
limits hold. Because the menu is finite and nonempty, its minimum is zero iff
at least one option has zero violation. Therefore

$$
v_C(b)=0\iff \exists i\ \forall j\ c_{ij}\leq b_j.
$$

This uses minimum and maximum, not a weighted average, so it preserves a finite
nonconvex menu. For the familiar F02 costs `(0,2),(2,0),(3/2,3/2)` at budget
`(3/2,3/2)`, the violations are `1/2,1/2,0`; the otherwise unsupported third
option is exactly the feasible one. In S12 the formula is a finite disjunction
of conjunctions of `b_j multimap c_ij`, using its displayed max/min semantics.
A units checker is external to that untyped numerical encoding.

Two failure conditions are essential.

**Attainment.** For an infinite menu of positive one-dimensional costs `1/n`
and zero budget, the infimum of violations is zero, but no option is feasible.
Infinitely replacing the finite minimum changes the existential reading.

**Information and one common witness.** Suppose an unknown state theta is 0 or
1. Option A has cost zero in state 0 and cost two in state 1; option B does the
reverse. At zero budget, `min_i v_i(theta)=0` in both states, but neither fixed
option has a robust zero-cost guarantee. Numerically,

$$
\max_\theta\min_i v_i(\theta)=0,
\qquad \min_i\max_\theta v_i(\theta)=2.
$$

An arithmetic proof of the first expression does not license the second.
An observed theta would permit an adaptive selector; an unobserved theta would
not. G's achievable witnesses and T's observation schedule are therefore not
supplied simply by encoding their numerical expressions in a complete logic.

For compatible finite composition, the same construction can range only over
allowed option pairs `(i,j)`, with costs added according to the declared
resource aggregator. Replacing that allowed relation by all pairs is an extra
feasibility assumption, not an arithmetic theorem.

## 6. A solver import needs more than matching algebraic notation

The symbol called addition has different jobs in these sources. In the usual
weighted-constraint example of S06, semiring addition selects the lower cost
and semiring multiplication adds costs. In S12 both arithmetic operations have
their numerical meanings. For G, union selects available budgets while
Minkowski sum accounts for compatible resource composition. An equality of
symbols is not a semantics-preserving translation.

### 6.1 Repeatedly reusing a factor can change the answer

Take singleton variable domains, a unary cost one and a binary cost two. Their
combined cost is three. Replacing the unary factor by the projection of its
combination with the binary factor gives a new unary cost three. If the same
binary factor is retained, the new total is five. Repeating gives seven, nine,
and so on. This illustrates why copying an idempotent-constraint propagation
argument to additive costs is invalid. It is not a counterexample to S06's
stated theorem, which assumes the relevant idempotence.

### 6.2 A finite elimination that does preserve the value

Let x,y range over `{0,1}`, with unary costs `a=(0,2)`, `b=(1,0)`, and pair
cost `c(x,y)=0` on equal values, `3` otherwise. The joint total table is

$$
\begin{array}{c|cc}
 & y=0 & y=1\\
x=0&1&3\\
x=1&6&2
\end{array}
$$

Eliminating y once yields the message
`m(x)=min_y[b(y)+c(x,y)]=(1,0)`. Then `a+m=(1,2)` has the correct minimum one.
Every factor was used exactly once. Independently minimizing the three factors
would instead give zero and ignore incompatible minimizing assignments.
The equality follows directly by grouping a finite minimum; it does not require
multiplicative idempotence. This is a positive restricted computation to compare
with S06's parsing-tree approach, not a claim that an unrestricted iterative
solver has been verified for G.

### 6.3 The remaining carrier checks

All upper sets in nonnegative resource space, with union and Minkowski sum,
provide a useful comparison where the nonnegative cone is both unit and top.
Finite-generator representations do not automatically support arbitrary joins.
Allowing signed resource space makes the unit cone different from the whole
space. In either case Minkowski multiplication is not idempotent: translating
by a nonzero positive cost twice changes the frontier. A proposed solver must
state which of these properties it uses, how witnesses are represented, and why
its actual iteration terminates. F03 does not select or implement that solver.

## 7. Robust optimization: action coupling matters even with one stage

S08's equation (15) eliminates randomization using separate worst-case choices
for every action. The following small reconstruction makes that premise visible.

There are two actions and two possible shared reward models:

$$
r_0=(0,1),\qquad r_1=(1,0).
$$

The unknown model is chosen against the policy but cannot depend on the realized
random draw. If action A is used with probability q, its worst expected reward
is `min(q,1-q)`. Pure actions have worst value zero; mixing equally gives one
half. The shared-model restriction is therefore significant even before any
temporal composition.

If uncertainty is enlarged so the adversary independently chooses a worst
reward for each action, `(0,0)` becomes admissible and every mixture has value
zero. This is the actionwise product structure used in the finite Bellman
specialization. The comparison does not refute S08 or assert that its general
model always reveals a hidden parameter; it identifies a hypothesis that T
must preserve when applying the theorem. Temporal pasting is a further,
separate scope requirement. The source's Markov policy reduction is not an
excuse to forget information that a genuinely history-dependent model needs.

## 8. Mass, units, and type boundaries of transformer imports

For a finite substochastic row K with total mass m, define `T(f)=Kf`.
Then `T(f+c 1)=T(f)+cm`. Exact common-shift homogeneity needs m=1, or a completed
outcome interface on which the common shift includes the missing-mass outcome.
For example, surviving with probability `1/100` to reward ten gives value
`1/10`; conditioning on survival gives ten. A certain reward one lies between
these values, so normalization can reverse the comparison.

Appending a cemetery outcome with payoff zero retains the first value.
Changing that payoff to a penalty changes the task. Shifting only living-state
payoffs while fixing the cemetery payoff still does not give an unqualified
cash-shift law. These finite identities are the exact boundary between the
S03 and S05 interfaces. No unbounded-integral or termination theorem follows
from them.

A further typing boundary remains. The equational sources generally use one
carrier and a declared signature; F02's transformers can have different input
and output state counts, and its costs can have distinct physical units. One
may examine a fixed type or prove a many-sorted translation. Arbitrarily adding
ill-typed values or totalizing partial composition is not justified by the
single-sorted source theorem. No such global translation is claimed here.

## 9. Consequences for the pending foundation decision

The audit does not select a winner. It separates four possible uses of the
literature, each with an explicit obligation before adoption:

| Possible use | What the checked sources supply | What remains to be established |
|---|---|---|
| S10 relation-indexed algebra | Explicit guarded substitution and a sound/complete equation framework | The project's actual relation, types, operation laws and meaning of consequences; any effective restricted prover |
| S12 fixed numerical arithmetic | A direct language for finite unbounded nonnegative arithmetic inequalities | Signed/type/evidence adapters, preservation of available information and strategy witnesses; an implemented proof checker rather than numerical fixtures |
| S06 constraint algorithms | Distinct algebraic, propagation, termination and parsing-tree results | Exact carrier match and a solver proof with the correct factor, compatibility and witness discipline |
| S03/S04/S05/S08 transformer antecedents | Linear subprobability, finite affine-piece, general minimax and rectangular robust cases | Selection of the actual admitted class and what its operational realizations preserve |

S11 supplies a broader relational-semantic comparison, not a substitute for the
first two rows' concrete deduction obligations. Source counts, citation counts,
and passing fixtures do not select a core or pass Gate A. The exact F03 task
status, active source-reading time, and remaining work are in the session record.
