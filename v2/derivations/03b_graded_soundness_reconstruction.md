# F07 S1 — graded soundness after weakening numerical premises

Status: **first-pass mathematical reconstruction**, not task completion.
This checks the mathematical contract behind [F06 residual discharge](02b_source_transport_and_withdrawal.md)
and [derived cases](02c_derived_cases_and_completion.md), independently of their
proof emitters. It uses the [native soundness semantics](03_soundness.md), not a
new trusted instruction or a sampled final-score oracle.

## 1. Freeze the proof, not its current empirical validity

Fix one accepted LOCAL native K proof P. Its root is

    t <=[b] s : u.

Each source-row leaf i has a normalized expression a_i and literal bound eta_i.
A repeated citation of the SAME row refers to the same coordinate eta_i in the
following construction, although arithmetic occurrences still count separately.
Freeze the signature, the term expressions, the case, all rule parameters,
conversions and exact rewrite identities. We do not change the meaning of a
source, program, observation or criterion while calling it an evidence update.

Replace the numerical bound at each row leaf by a formal variable zeta_i with
that row's unit. Define a typed bound expression B_j(zeta) at each proof node:

| Node | Bound expression |
|---|---|
| source row i | zeta_i |
| exact constant difference c | c |
| lattice injection/projection | 0 |
| rewrite or negation | B_parent |
| addition or transitivity | B_left+B_right |
| nonnegative scaling k | k B_parent |
| positive unit conversion c | convert_c(B_parent) |
| fixed slack d>=0 | B_parent+d |
| combining proofs of the same query | min(B_left,B_right) |
| common-target min/max or min/max congruence | max(B_left,B_right) |
| residual congruence | max(B_left+B_right,0) |

The local fragment has no `all_cases` node; a global proof can first be
localized to a fixed case as described in the companion scope note. Every
entry is an ordinary finite CPWA expression. Existing numerical literals in
the *query terms* stay fixed. This construction does not replace all occurrences
of the same number with a new evidence parameter.

### Lemma G1 — exact snapshot and monotone bound program

At the old bound vector eta, B_P(eta)=b. Further, B_P is nondecreasing in each
of its row-bound coordinates after the declared positive unit conversions.

**Proof.** At eta, the table is exactly the native rule budget calculation,
so equality follows by induction over P. Each listed operation is monotone in
its inputs, including min, max and the nonnegative clipping of a sum. Constant
nodes are independent of eta. Positive conversion/scaling preserves order.
Composition of these monotone maps gives coordinatewise monotonicity. ∎

The monotonicity claim is about bounds, not about the source loss expressions.
Those may contain negative coefficients, and a better upper bound can be
negative. Signed budgets are preserved throughout; no global nonnegative
truth-degree interpretation is introduced.

## 2. Semantic replay with arbitrary current bounds

### Theorem G2 — bound-program soundness

For any finite real assignment x and real bound vector zeta such that

    a_i(x)<=zeta_i for every source row actually used by P,

we have

    E_x(t)-E_x(s)<=B_P(zeta).

**Proof.** Use induction over the proof's ancestor DAG, evaluating every B_j at
this fixed zeta. At a row, its required inequality is exactly the premise of
the theorem. Constant and lattice base cases are source-free identities.
For a rewrite/negation, equality of numerical differences carries the parent
bound unchanged. Adding or telescoping two inequalities sums their bounds.
Scaling and conversion use their nonnegative/positive factors; slack adds a
nonnegative allowance. Two proofs of the same difference permit a minimum.
A lattice operation permits the maximum of its two parent bounds. Residual
congruence permits max(sum,0), with the first argument reversed. These are the
pointwise lemmas in the native soundness audit, valid for any finite real
bounds, not only the old rational snapshot. The root gives the statement. ∎

This is not a theorem that an unmodified old certificate can be accepted with
its old fingerprint and old b. A concrete replay must issue a new trace in the
current context and bind its newly calculated root to the intended request.
The theorem explains *why* that reconstruction is sound when its hypotheses
hold. If the source coefficients, rewrites or meanings change, this frozen
bound program is not automatically the same object.

## 3. Numerical assumption violations become a proved loss allowance

Let W be a chosen set of withdrawn rows. For i in W define

    v_i(x)=max(a_i(x)-eta_i,0),
    zeta_i(x)=eta_i+v_i(x)=max(eta_i,a_i(x)).

For retained rows put zeta_i=eta_i. Let D_remaining be the domain satisfying
the retained used rows, with any additional structural/operational domain kept
explicit. Removing rows preserves the original feasible witness.

### Theorem G3 — graded premise-discharge soundness

For every x in D_remaining,

    E_x(t)-E_x(s) <= B_P(zeta(x)).

Let

    R_P(x)=B_P(zeta(x))-b.

Then R_P is a finite nonnegative CPWA function, and

    E_x(t)-E_x(s) <= b+R_P(x),
    max(E_x(t)-E_x(s)-b,0) <= R_P(x).

At every point satisfying all the original used rows, R_P(x)=0.

**Proof.** A retained row satisfies a_i<=eta_i by the domain assumption. A
withdrawn row satisfies a_i<=max(a_i,eta_i) at every real assignment. Apply G2
with this zeta(x). Since zeta(x)>=eta coordinatewise, G1 gives B_P(zeta(x))>=b;
therefore R_P>=0. The first inequality was already proved; combine it with
R_P>=0 to bound the nonnegative conclusion overrun. Finiteness and CPWA closure
follow from the finite expression constructors. On the old used-row domain,
all v_i vanish, so zeta=eta and G1 gives R_P=0. ∎

This is an exact semantic statement about the proof-derived allowance. It does
not say the withdrawn rows are probably correct, that R_P is small, or that
R_P is the smallest possible allowance. It explicitly relates a premise
violation to a possible increase beyond the requested loss bound.

### 3.1 A minimal useful example

A source premise d<=-1/2 has a one-row proof of that comparison. After removing
it, G3 yields

    d <= -1/2 + max(d+1/2,0).

At d=-1/4, the allowance is 1/4 and a quarter-unit improvement remains. At
d=1/4, the allowance is 3/4 and no improvement is asserted. The arithmetic
formula is valid everywhere; which regime applies is an additional modeling
or evidence question. This is not replacing the failed premise by an equally
strong unverifiable assumption.

### 3.2 The allowance is proof-relative, not a universal degree of truth

Consider a proof that adds x<=0 and -x<=0 and rewrites its root to 0<=0. If
both rows are withdrawn, this proof's bound program yields R_P=|x|. A direct
constant proof of 0<=0 yields the identically zero allowance instead.
Both are sound; the former is needlessly sensitive because of its derivation.
Thus R_P=0 does not characterize the truth of every old premise, and R_P need
not equal the actual conclusion overrun. A proof-independent optimal penalty
or resource-bounded search for a tighter one is a further question, not a
consequence smuggled into G3.

## 4. Cases can become graded alternatives over a common base

Let C0 be a shared nonempty base domain. It may retain probability ranges,
program interpretation constraints and other obligations that are not being
withdrawn. Suppose finitely many local proofs P_h establish the SAME numerical
query t-s under C0 together with extra rows E_h. Discharge only those extras,
obtaining allowances B_h(x) valid throughout C0 by G3.

### Corollary G4 — graded alternative-proof bound

Throughout C0,

    E_x(t)-E_x(s) <= min_h B_h(x).

**Proof.** Each discharged proof now establishes its inequality on the SAME
base domain, not only on its old case. Their numerical difference is identical,
so it is bounded by each B_h and hence by their finite minimum. ∎

No deployed action is selected using h. The policy pair is fixed; the index
selects which numerical argument supplies a bound. Coverage of the old zero-
violation regions is not required for G4 because violations have been retained
quantitatively. If one old case applies at x, its allowance reduces to its old
budget there. In an uncovered gap, a finite penalty may still leave improvement.

The correct aggregator after full discharge is a MINIMUM of globally applicable
bounds. The original `all_cases` rule used a MAXIMUM of conditional local
budgets. Confusing these two situations would be unsound; G4 changes the domain
on which the branch arguments apply before taking the minimum.

### 4.1 Opposite and imperfect numerical guards

For opposite guards u<=0 and -u<=0, suppose the discharged bounds are

    D<=A+alpha max(u,0),
    D<=B+beta max(-u,0),

with nonnegative alpha,beta. At least one penalty is zero, so G4 implies
D<=max(A,B). F06 emits an ordinary trace deriving the same conclusion; it does
not trust this external case argument as a new primitive.

For shifted guards, let

    D<=-1/2+max(u+1/4,0),
    D<=-1/2+max(1/4-u,0).

For u>=0 the second penalty is <=1/4; for u<=0 the first is <=1/4. Thus their
minimum is at most -1/4 for every real u. Equality occurs at u=0. This independently
reconstructs F06's imperfect-coverage result and makes its quantifiers explicit:
one common D, two arguments, no assumption that a hidden mode is observable.

## 5. What remains to be checked about implementations

G2–G4 prove the mathematical transform's meaning. The existing symbolic emitter
returns an ordinary zero-budget proof of `t <=[0] s+B_P(zeta(x))`. Acceptance
by the unchanged native checker establishes the numerical meaning of that
returned root. A contract audit must ALSO establish that its returned allowance,
selected withdrawn rows and root terms are the ones promised to its caller.
This is why request binding and producer-specific invariants remain separate
from the compact native soundness theorem.

No claim is made here that every optional producer is complete, polynomial-time,
or incapable of exhausting resources. The first F07 pass has not replaced the
later soundness reconstruction or established the overall Gate B requirements.

## 6. Reconstructing source grafting without assuming source inclusion

A proof can survive a source change even when the entire old source does not.
The exact statement is most transparent as proof substitution.

Let Sigma_old and Sigma_new have the same unit/conversion conventions. A map
sigma assigns a closed, well-typed new term to every old source name, with the
same output unit. For a new assignment x', define an old assignment by

    sigma_*(x')_z = E_(x')(sigma(z)).

Every coordinate is finite because the replacement terms are finite and total.
All substitutions are simultaneous; inserted terms are not recursively rewritten
by the same source map. Free local variables are forbidden in replacements.

### Lemma G5 — denotational substitution

For every old term t,

    E_(x')(t[sigma]) = E_(sigma_*(x'))(t).

**Proof.** Induct on t, strengthening the induction to arbitrary compatible
local environments. A source leaf is the defining equation of sigma_*.
Constants and local lookups are unchanged. Arithmetic and conversion commute
because their operations and factors are fixed. At a let, evaluate the replaced
right-hand side first; the induction hypothesis gives the same bound value on
both sides, so the body induction applies to the identically extended local
environment. Closed replacement terms cannot capture an old local binder. ∎

Exact normalization identities also survive this substitution. One direct
normal-form proof substitutes the normalized new forms for source keys in an
old normal form, recursively rebuilding min/max keys and collecting rational
coefficients. If a nonlinear key becomes constant it is folded by the same
rule. This operation commutes with normalization by structural induction,
including the already-captured normal forms stored for lexical bindings.
It therefore maps equal old normal forms to equal new ones.

### Theorem G6 — proof-local grafting soundness

Let P be a local old proof with row expressions a_i and frozen bound program
B_P. In one target context/case suppose there are checked replacement proofs

    sigma(a_i) <=[beta_i] 0

for every old source row needed by P. Then the substituted root obeys

    t[sigma]-s[sigma] <= B_P(beta)

throughout that target domain. It is not necessary that beta_i<=eta_i, or that
the target assignments map into the ENTIRE old source.

**Semantic proof.** Each checked replacement has its stated inequality by S6.
At a target point x', G5 identifies its left side with a_i(sigma_*(x')). Apply
G2 to that old-coordinate assignment and the current bounds beta. Apply G5
again to the old root terms. This gives exactly the displayed result. ∎

**Syntactic reconstruction.** Replace each row leaf by its current checked
proof, shift parent indices to preserve the DAG order, substitute source terms
in every old instruction and term-valued parameter, and recompute budgets
from the unchanged local constructor rules. G5's normal-form observation
preserves exact rewrite/middle-term checks. The resulting trace has budget
B_P(beta) and is checked entirely under the target context. Constants and
nonnegative slacks embedded in the old query remain fixed. A compiler that
finds additional identities may return a better bound; it must expose its
actual root rather than claim that every reconstruction has the identical
numeric budget.

A global old proof can first be localized for each new case's selected old
case. Supply replacements for each localized dependency set and cover every
new live case. The final union takes the maximum of the new local bounds.
There is still one literal requested comparison; a different proof choice in
a hidden case is not a different deployed action.

### 6.1 A non-inclusion example

An old context has x<=1 and y<=0. A local proof of x<=1 uses only the first row.
A new context has x<=1 and y>=1, with witness (x,y)=(0,1). It is not a subset
of the old context; indeed their y restrictions are incompatible. A replacement
proof for x<=1 is nevertheless available and G6 preserves that query.
Transporting the old conclusion y<=0 would fail without a different adequate
argument. This is selective proof reuse, not blanket persistence under any
history-preserving update.

### 6.2 Current-budget comparison is indispensable

If the new proof establishes x<=2 instead of x<=1, G6 returns budget 2 for the
old x-versus-zero query. That is a correct new warrant, not an old budget of 1.
A receiver requesting x<=1 must reject it unless another proof meets that
request. Exact transport of terms and a successfully checked trace do not
imply preservation of an old *strength*.

## 7. Observation-preserving use needs a commuting information map

G6 is numerical. For a program-use interpretation, let O_old and O_new be the
old and new observation maps. A sufficient condition for transporting an old
observation-based policy pi_old is a supplied map phi satisfying

    O_old(sigma_*(x')) = phi(O_new(x'))

on every admitted new assignment. Then

    pi_new(o') = pi_old(phi(o'))

is an observation-legal new policy. If the declared cost model also transports
under that program relation, the numerical comparison applies to the intended
use. In measurable settings those maps and policies need the corresponding
measurability premises; in the finite observation examples this is automatic.

Without the information equation, an old policy can accidentally receive a
hidden coordinate through a source substitution. For example, old observation
is a binary source x, new observation is constant, and sigma(x) is an unobserved
new binary coordinate. The substituted arithmetic expressions still denote
real functions, but an old action selected using x need not be implementable
from the new constant observation. A matching descriptive string is not a proof
of this information relation.

The current source-transport adapter checks fixed observation and interpretation
identifiers and returns a checked numerical trace. It is not a verifier for
arbitrary observation maps or program code. The equations here state what a
stronger operational use must provide, rather than silently promoting string
identity into a causal or executable equivalence claim.

## 8. A checkable propagation bound for premise error

The expression R_P need not be evaluated by an optimizer to obtain a useful
conservative estimate. The finite proof itself supplies a sensitivity vector.
This is a soundness corollary, not a claim that its estimate is the tightest.

Fix the numerical coordinates of the named units. For each node n form a
nonnegative vector L_n indexed by the local source rows. Use zero for constant
and lattice nodes, the i-th unit vector for row i, preserve L under rewrite,
negate and fixed slack, add parent vectors under addition and transitivity,
and multiply by the nonnegative scale/conversion factor under scaling and
conversion. For proof minimum, common min/max and lattice congruence, use the
coordinatewise maximum of the two parent vectors. For residual congruence,
use their sum: the final clipping at zero has Lipschitz factor one. The entries
carry the appropriate output-unit/input-row-unit conversion when these differ.

### Lemma G7 — proof-derived one-sided sensitivity

For all real row-budget vectors eta,zeta,

    B_P(zeta)-B_P(eta) <= sum_i L_P,i max(zeta_i-eta_i,0).

Consequently |B_P(zeta)-B_P(eta)| <= sum_i L_P,i |zeta_i-eta_i|.

**Proof.** First suppose d=zeta-eta is coordinatewise nonnegative. Induct over
the budget program. Constants have zero change and a row leaf has change d_i.
Addition and nonnegative scaling give the displayed vector recurrence. Both
minimum and maximum are monotone and obey

    |F(a1,a2)-F(b1,b2)| <= max(|a1-b1|,|a2-b2|).

For d>=0, each parent change is nonnegative and at most its vector dotted with
d. Their maximum is at most the coordinatewise-maximum vector dotted with d.
The clipping map max(t,0) cannot amplify a change, so the sum of parent
sensitivities bounds residual congruence. This proves the nonnegative-increment
case. For arbitrary zeta, monotonicity gives

    B_P(zeta) <= B_P(eta+(zeta-eta)_+),

and the first result applies. Swapping eta and zeta and bounding positive parts
by absolute values proves the symmetric statement. ∎

For G3's residual discharge, zeta-eta is the vector of nonnegative violation
losses, with zeros at retained rows. Hence

    0 <= R_P(x) <= sum_(i withdrawn) L_P,i p_i(x).

Repeated use is counted by the addition rule, even when the DAG shares a row
node. For the proof adding x<=0 to itself, L=2 and R=2 ReLU(x). An argument
that counted only distinct premise identifiers and assigned coefficient one
would fail at x=1. By contrast, taking the minimum of two proofs with the same
sensitivity need not double that coefficient. This is numerical reuse, not a
probabilistic independence or repeated-observation convention.

### Corollary G8 — expected and high-probability use of violation loss

Supply a probability law over finite assignments under which the retained
premises hold almost surely. Suppose the nonnegative p_i have finite expected
values for all used withdrawn rows. Then

    E[R_P] <= sum_i L_P,i E[p_i],
    E[Delta] <= b + sum_i L_P,i E[p_i],

where Delta=t-s and the expectation of Delta is either an ordinary integrable
expectation or the well-defined extended expectation described in U5. Its
positive part is bounded by the positive part of b plus the integrable penalty;
its expectation therefore cannot be undefined as infinity minus infinity.
For every t>0,

    Pr(Delta > b+t) <= Pr(R_P>t)
                     <= min(1, sum_i L_P,i E[p_i]/t).

**Proof.** Apply G3 and G7 pointwise, integrate their nonnegative upper bound,
and use Markov's inequality on R_P. No independence between the premise errors
is required. The last inequality can be very loose; the theorem states validity,
not useful concentration without further information. ∎

If retained-premise validity holds only on an event E with Pr(E^c)<=alpha, the
safe statement is instead

    Pr(accepted AND Delta>b+t)
      <= alpha + E[1_E R_P]/t,

capped by one. The expectations and the event are additional supplied premises.
The proof does not estimate them from the trace, turn empirical calibration into
an axiom, or establish a conditional error rate among accepted outputs.

An unbounded penalty is allowed provided the required expectation is finite.
For example let N>=1 have probabilities 2^(-n), p=N and L=1; E[p]=2. This
supports an expected comparison even though no finite uniform bound on p exists.
Changing to Pr(N=n)=1/[n(n+1)] makes E[p] infinite: the same pointwise soundness
still holds, but this expected finite-cost conclusion is no longer justified.

## 9. Fixed syntax versus optimization under changing evidence

G7 concerns one frozen proof, not the output of arbitrary proof search. A family
of already valid proofs can supply a pointwise minimum of their current bounds.
For a finite family with a common finite sensitivity vector L dominating every
member's vector, the same argument bounds the selected minimum's change. The
minimizer need not be unique and can switch at a boundary; no differentiability
is used.

Without a common finite L, that extension is not available. A searcher might
select larger and larger coefficients when the source geometry degenerates.
The validity of each returned trace survives, while a uniform robustness claim
about the entire search process remains unproved. Search failure, an unbounded
required coefficient or a timeout is not a counterexample to the returned-trace
soundness theorem. It is a limitation of production/precision that later tasks
must measure separately.
## 10. Coefficient error is not a scalar-bound update

The frozen-row hypothesis in G2 can be weakened only by supplying additional
numerical evidence, not by silently rounding the source coefficients. Suppose
a current source gives

    (a_i+d_i)^T x <= eta_i+epsilon_i.

The old row expression then satisfies

    a_i^T x <= eta_i+epsilon_i-d_i^T x.

This is an expression-valued allowance, not automatically the scalar update
eta_i+epsilon_i. If |x_j|<=M_j is separately warranted on the current domain,
then a sufficient scalar bound is

    beta_i = eta_i+epsilon_i+sum_j |d_ij| M_j.

Each used old row has a replacement bound of the form required by G2/G6. Those
theorems propagate beta through the OLD root expression and proof; they do not
pretend the coefficient arrays remained identical. If a model's intended root
loss expression also changed, its own translation or discrepancy bound must be
supplied as well.

There is no bound depending only on the norm of d_i when x is unrestricted.
For example d_i=(epsilon), x=-K/epsilon, epsilon>0 gives -d_i x=K for arbitrary
K. Tiny rounding error in a coefficient can therefore have an arbitrarily large
semantic effect even though all values are finite. Exact checking avoids the
rounding step; finite-precision implementations require a proved domain-sensitive
allowance of this kind.

A structural change is different again. Missing unit meaning, a malformed
program or a policy that reads unavailable information is not an inequality
with a finite numeric overrun already defined by K. Assigning such a defect a
loss requires an explicit model and revised interpretation. G3 discharges
well-formed numerical assumptions; it does not turn every possible semantic or
metalogical doubt into a valid numeric source term for free.
