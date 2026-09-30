# F09 reconstruction A — Boolean and phase-one interfaces

Research contributor: **Codex (GPT-6)**. September 30, 2026 UTC.
Working derivation for [the principal F09 note](05_fragments_and_comparisons.md).
This is a same-assistant reconstruction from definitions, not an independent
review or a claim of novelty for Boolean/three-valued algebra.

## 1. Boolean losses and actual native consequence

Fix one unit U. Encode true by loss 0 and false by loss 1. For a propositional
formula A define L recursively:

    L(top)=0                 L(bottom)=1
    L(p_i)=x_i               L(not A)=1−L(A)
    L(A and B)=max(L(A),L(B))
    L(A or B)=min(L(A),L(B))
    L(A implies B)=res(L(A),L(B))=max(L(B)−L(A),0).

Every displayed operation is an F05 term operation or abbreviation. A source
assignment is Boolean when every x_i is 0 or 1. The source value is the **loss
bit**, the complement of the ordinary truth bit.

**B1 (Boolean interpretation).** For every Boolean assignment, L(A) belongs to
{0,1} and equals 0 exactly when A is classically true.

Proof by structural induction. The constants and atoms give the base. The
complement exchanges 0 and 1. A maximum is zero exactly when both inputs are
zero; a minimum is zero exactly when either input is zero. The residual is 1
only for the pair (0,1), precisely a true antecedent and false consequent.
These computations give closure and truth preservation simultaneously. Hence
classical equivalence is equality of the translated functions on this domain.
Both zero-budget comparison directions express that equality natively, by U1.

This is a sublanguage interpretation. It is not a subalgebra closed under every
F05 operation: 1+1=2 and signed scaling can also leave {0,1}. No assertion that
all loss expressions are propositions follows from B1.

For n atoms, let C_B have one case for each vector e in {0,1}^n, with the two
affine rows x_i<=e_i and e_i<=x_i for each coordinate, and witness e. For n=0
there is one empty-dimensional case with no rows and its empty witness. These
are admitted finite, rational, feasible cases. They do not give a program
permission to observe the case: every case proves the same literal query.

For a finite premise family Gamma put P_Gamma=max{L(A): A in Gamma}, using 0
for an empty family. This represents failure of the conjunction of premises.

**B2 (exact entailment).**

    Gamma classically entails B
      iff C_B semantically validates L(B)<=P_Gamma
      iff a native global proof of L(B) <=[0] P_Gamma exists.

At any valuation, if all premises are true, P_Gamma=0, so the inequality demands
L(B)=0. If some premise is false, P_Gamma=1, and every Boolean conclusion loss
is at most 1. This proves the first equivalence in both directions. All rows
and terms use U, so the target reduct is the original context; F08 U1 supplies
the second. An invalid classical entailment supplies a rational source model
with difference exactly 1, which F07 soundness excludes from a zero-budget proof.
The difference takes values in {−1,0,1}; the same equivalence holds for every
rational requested budget 0<=b<1. At b=1 even invalid entailments pass.

Do not instead require a case for every model of Gamma without addressing
inconsistency: Gamma may have no models, whereas F05 requires nonempty source
contexts. Encoding the premises in P_Gamma handles explosion as a valid
conditional query over the nonempty Boolean cube; it introduces no empty case
or ex-falso rule into the native source interface.

The direct finite construction is also transparent: in each point case the
two rows establish each x_i=e_i, structural congruence evaluates the translated
formula to its Boolean constant, and the constant comparison proves the local
query. Rewriting back to the fixed literal pair and using all_cases closes the
global proof. This describes proof existence, not a polynomial-size compiler or
an implementation of general propositional proof search.

### 1.1 Failed interval and connective overgeneralizations

On the admitted interval 0<=x<=1, the translated excluded middle has loss

    L(p or not p)=min(x,1−x).

At x=1/2 it is 1/2, so it is not zero-budget valid. The continuous interval is
therefore not the Boolean fragment. Even classical-equivalent presentations of
implication differ away from the endpoints: res(x,x)=0 for all x, whereas
min(1−x,x)=1/2 at x=1/2. B1 does not designate a unique real-valued extension of
classical syntax.

A continuous {0,1}-valued function on a connected source domain is constant:
if it took both values, its image would be a connected subset of R containing
0 and 1, hence would also contain 1/2. Every native term is continuous. Thus a
nonconstant Boolean-valued term on an interval cannot be obtained merely by
thresholding with the existing term operations. Disconnected source cases, or
an explicitly external Boolean observation, are substantive assumptions.

For nonnegative terms, zero-loss observations still preserve the positive
fragment: max(a,b)=0 iff both are zero, and min(a,b)=0 iff at least one is zero.
There is no general complement term justified by this observation. For example
1−a has neither the required range nor the required zero set on arbitrary
nonnegative a. A native comparison is a statement about losses; it does not
automatically inherit a truth-functional negation operation on those statements.

## 2. What is exactly recovered from phase one

The authoritative clauses are [phase-one core §§4–6](../../formalism/07_core_calculus.md),
with executable consumers in [verification/kernel.py](../../verification/kernel.py).
The earlier `02_license_semantics.md` is historical and points to that core.
Phase one first checks well-formedness, then supplies a total diagnostic for
every required/report slot. Its required status order is

    refuted < open < supported,

and its nonempty required family aggregates by minimum. Missing evidence is an
open diagnostic; a missing diagnostic record violates the totality contract.
An invalid frame or missing action fallback can make a request Undefined before
any meaningful atom is assessed. Neither failure is a numerical loss value.

**B3 (assessment-algebra embedding).** Define

    e(refuted)=1, e(open)=1/2, e(supported)=0.

Then e is injective and e(meet_i z_i)=max_i e(z_i). Proof: it reverses the two
finite chains, so their least element maps to the largest loss. A nonempty
family therefore has encoded loss 0, 1/2 or 1 exactly for Granted, Withheld or
Refused, *conditional on the same external well-formedness and diagnostics*.
All three values and max are native terms; the closed numerical identity is
an exact semantic identity, with a native proof by the one-unit U1 theorem.

The middle value is a code for unresolved evidence, not a calibrated probability
or an expected task loss. Phase one's core needs only this meet operation; a
full negation/disjunction extension must not be silently attributed to it.
Replacing every open diagnostic by a free Boolean variable would change the
semantics: repeated uses of that variable gain shared possible-world relations
that are not part of the bare three-element meet algebra.

### 2.1 Exact upper-bound and fallback adapters

Let a phase-one certificate be a supplied nonempty rational interval [l,u]
for one scalar risk x and a rational threshold tau. Form the one-unit context
l<=x<=u. Its modeled requirement is f=x−tau<=0.

**B4a.** The phase-one upper-bound consumer and the following native/exact
quantitative observation agree:

* supported iff a native proof f <=[0] 0 exists (equivalently u<=tau);
* refuted iff a native proof 0 <=[−delta] f exists for some rational delta>0
  (equivalently l>tau);
* open otherwise.

For support the upper endpoint gives necessity and the source upper row gives
sufficiency. For refutation the lower endpoint gives necessity; if l>tau use
delta=l−tau and the lower row. At l=tau equality is permitted: it is not a
refutation. This strict/inclusive distinction matches the actual consumer.
Missing certificate evidence stays an external open diagnostic, not a fabricated
interval or a failed proof search. Producer resource exhaustion also is not a
semantic refutation.

For candidate x in [l_e,u_e], fallback y in [l_F,u_F] and required advantage d,
use the **Cartesian rectangle** and f=x+d−y. Its extrema are l_e+d−u_F and
u_e+d−l_F, attained at the opposite corners. Thus the two native observations
agree exactly with `assess_improvement`: supported if u_e+d<=l_F, refuted if
l_e+d>u_F, open otherwise. This is B4b. It is an adapter for the existing
endpoint consumer, not a theorem that marginal intervals retain all information.

For a concrete separation let x range over [0,1] and y=x+1, with d=1. The joint
margin is identically zero and has a source-based native proof. The marginal
intervals are x in [0,1], y in [1,2]; their rectangle has margin ranging over
[−1,1], so the phase-one endpoint consumer returns open. The richer source
contract supports more, while the exact endpoint adapter remains correct.

### 2.1a Finite vector/region conditions without forcing a scalar tradeoff

Phase one's formal core also allows vector/partially ordered quantities and
general acceptable regions. The scalar interval adapter does not exhaust that
interface. A finite componentwise requirement has a precise positive extension:
after declared positive bridges put margins m_i in one comparison unit, then

    every m_i<=0 iff max_i m_i<=0
                 iff sum_i max(m_i,0)<=0.

Both encodings use native terms. They enforce a hard conjunction, with no
compensation between a violation and an unrelated surplus. A signed weighted
sum is different: margins (1,−1) sum to zero despite a violated first condition.
At nonzero allowance b the maximum and summed-positive-part encodings also
give different tolerance regions; their zero-set agreement is not an equality
of all quantitative budgets.

More generally, let the declared acceptable region be a finite nonempty union
of rational closed polyhedra in finitely many represented coordinates r_i.
Its violation term

    V(r)=min_h max(0, max_j(a_hj*r−b_hj))

is zero exactly on that region; an unconstrained component has violation zero.
Every r_i must be a native term with the necessary explicit unit bridges.
Support over an admitted source is exactly V<=0; refutation is exactly V>0
everywhere. The composed V is finite rational CPWA on the finite closed
polyhedral source, so refutation has a positive rational lower margin as in B4.
U1 turns these into native certificates **on the target reduct**. If comparing
several native component judgments, use the same target-unit view for all of
them; inaccessible rows can otherwise give different evidence domains.

This is an exact finite-polyhedral region adapter, not a scalar order embedding
of every vector value. No one real number with its ordinary total order can
preserve and reflect componentwise order on R^2: (0,1) and (1,0) are incomparable,
whereas their two real codes must be comparable in at least one direction.
Retaining multiple components/queries avoids that specified obstruction.

The acceptable-region hypothesis also matters. On [0,1]^2 the quarter disk
x^2+y^2<=1 cannot be the exact zero/sublevel set of a finite CPWA term. Such
a set is a finite union of polyhedra, whose boundary lies in finitely many
lines; each line meets the circular arc in at most two points. The arc has
infinitely many points. Finite approximations or an external region certificate
can be useful, but they are not an exact import of that curved region into the
selected arithmetic/source language.

Similarly, a phase-one region certificate U=(0,1] for requirement r<=0 is
disjoint from the acceptable region, yet it has no positive uniform lower
margin. That open source is outside F05. Replacing it by [0,1] changes the
assessment to open by adding the boundary model r=0. Thus the positive-margin
refutation adapter must not be generalized to arbitrary nonclosed certificate
regions without changing its interface.

### 2.2 Why joint conjunction and diagnostic aggregation differ

For nonempty source domain D and real margins f_i, let s_D(f_i) be supported
when every f_i<=0, refuted when every f_i>0, and open otherwise. In the present
one-unit finite CPWA/polyhedral fragment, each universal strict positivity has
a positive rational lower bound: the finite closed piecewise-polyhedral range
attains a finite lower endpoint. Thus the observation has the two native
certificate forms of B4, even on an unbounded domain.

Compare phase one's atomwise meet with assessing the joint margin max_i f_i.
They agree on support: all margins are universally <=0 exactly when each is.
Any individually refuted requirement refutes the maximum. But the converse is
false: `for every source point some requirement fails` does not imply `some
one requirement fails at every source point`.

Example: one source with two point cases x=0 and x=1, and requirements x<=0,
1−x<=0. Both atoms are open. Their diagnostic meet is open, while max(x,1−x)
is identically 1 on this domain, so the joint requirement is refuted. All
quantifiers, witnesses and scopes have changed explicitly; this is not a bug
in phase one's conservative atomwise interface.

**B5 (exact aggregation boundary).** For a fixed finite nonempty required family,
the two observations differ exactly when every individual accepted set
A_i={x in D:f_i(x)<=0} is nonempty but their intersection is empty. Proof:
support is already equivalent. Atomwise refutation means some A_i is empty;
joint refutation means their intersection is empty. If neither refutes and
not all support, both are open. These cases exhaust the possibilities.

A useful sufficient condition is D=product_i D_i with f_i depending only on
coordinate block i: choose one accepted point in each nonempty A_i and combine
them. This is a Cartesian information assumption, not stochastic independence.
Correlated source cases generally violate it. For exact phase-one behavior,
retain per-atom assessment and diagnostic aggregation; do not replace them with
a stronger joint query without declaring a new evidence consumer.

## 3. Explicit limit of the phase-one relationship

These are an algebra embedding and exact certificate-consumer adapters, not a
faithful embedding of the full license calculus. Two phase-one requests can
have the same risk intervals, margins and coded atom statuses but different
well-formedness (e.g. a missing required fallback). One is Granted and the
other Undefined. Two supported atoms can also have different provenance and
withdrawal dependencies while their status constants are equal. A projection
that forgets those fields cannot reconstruct the lost outcomes or revisions.

This is a noninjectivity claim about the **specified quantitative projection**,
not an impossibility theorem about every conceivable encoding into real numbers.
Native contexts retain their own source identity/scope, but that does not make
them automatically implement the phase-one trace verifier, library search,
selection, archival history, confidence semantics, or safety diagnostics.
Supplying those as arbitrary constants would encode the answers, not derive
their validity from the new calculus. Their richer import remains explicit.
