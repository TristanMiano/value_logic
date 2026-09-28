# F07 S4 reconstruction record

Author: ChatGPT (GPT-6 Astra Pro). New same-assistant reconstruction, not external review.
The closed clock segments identify research time. Writing up prepared results and code/tests are excluded from D.

## D1/D2: native contract and normalization

Use a tagged model `(h,x)` with `x in D_h` for a local claim; the global claim
quantifies over all such tags. The same raw pair in `all_cases` is independent
of h. This prevents the ambiguous inference from membership in another case's
union to validity of a named local case. No observations are created by this
numeric quantifier.

Normalize with an environment of **already captured forms**. Maintain
`valuation(normal_env(z)) = value_env(z)` at every lexical scope. Constants,
source atoms, linear coefficient collection and explicit conversions preserve
this invariant. Min/max atoms contain normalized child forms; constant folding
is applied only to source-independent children. Equal forms imply equal
functions, without a completeness assertion. Negative coefficients are allowed
in forms, but proof-budget scaling remains nonnegative. All cancelled values
are finite; source coordinates can be unbounded across assignments.

The complete `_expected` body was reconstructed constructor by constructor.
The final same-difference check transfers the result to the stored pair; each
parent is earlier and already validated in the same case (except all_cases).
Typed zero in middle/common-term checks forces parent units to match the
current result. `negate` reverses and negates both terms without negating the
budget. Signed max/min congruence uses common-shift equivariance; residual
congruence needs the zero branch and contravariant first argument. A feasible
witness prevents empty local domains but is not evidence of empirical coverage.
`check` validates **every** stored step even when root is earlier; pruning a
trace containing a bad unused node is not promised.

Deeply immutable finite standard data and exact int/Fraction arithmetic are
part of the theorem. A frozen dataclass annotation alone does not assert that
arbitrary subclasses, malicious methods or mutable containers are admitted.
No runtime/hardware theorem or proof-search completeness follows.

For withdrawn row `a<=eta`, replacing its leaf budget by
`eta + max(a-eta,0)` yields a coordinatewise larger input to a monotone budget
DAG. Therefore its allowance E is at least the localized baseline b_h **at all
finite assignments**, even outside retained source rows. The conclusion
`Delta<=E` still needs those retained rows. The penalty E-b_h vanishes when
all used withdrawn rows hold, including when b_h is negative. This is not a
certificate that a metadata field named penalty equals E-b_h.

## New bounded proof obligation to finish during this pass

Derive a finite linear-growth majorant for the **normalized paired difference**,
not the two absolute losses. The recursive normal-form envelope can remove a
common unbounded baseline before asking for probability moments. This would
supply explicit sufficient hypotheses for the existing expectation corollary,
without starting F08's representation/completeness task.

## D3/D4: complete case-producer reconstruction

`validate_live` explicitly requires the guard and conclusion to have the same
unit. The suspected cross-unit loophole is **excluded by the wrapper**; it is
not a discovered bug. Named conversions can be used explicitly before splitting.

For one guard loss H>=0, the envelope invariant is
`t <=[0] baseline + error`, `0 <=[0] error`, and the numerical equality
`error = gain*H` with gain>=0. Constants have zero gain; sums add gains;
nonnegative scaling and declared positive conversions transport them. At a
min/max node choose the larger child gain K. The edge
`0 <= (1-k/K)*K*H` raises the smaller error (K=0 uses exact zero equality).
The minimum uses the child with smaller baseline; the maximum raises both
baselines and has maximum proof budget zero. Thus the baseline is exactly the
zero-defect snapshot, not necessarily the original global-case budget.

For an empty branch g(x)=c*x+d<=0, a nonnegative row combination with
`sum lambda_i a_i = -k*c*x`, k>0, gives
`-g <= q = sum lambda_i eta_i/k - d`. A strict q<0 excludes the branch on the
parent domain. q=0 does not exclude the boundary and is correctly refused.
Transport of the surviving branch may improve the bound; its old budget is
not asserted equal to the returned root budget.

The two-live-branch proof is independently justified by the ordinary sign
partition, and constructively by global allowances
`Delta<=A+alpha*rho(g)` and `Delta<=B+beta*rho(-g)`.
Their common-query minimum plus disjoint positive parts gives
`Delta<=max(A,B)`. Literal pair identity precludes selecting different actions
in hidden sign cases. At g=0 both branches may apply; no strict split is assumed.

For weighted coverage, positive k_i,w_i and current checked allowances
`Delta<=A_i+k_i*rho(g_i)` and `sum w_i*g_i<=eta` imply

    H = sum w_i/k_i > 0,
    S_A = sum w_i*A_i/k_i,
    M = max(max_i A_i, (eta+S_A)/H),
    Delta <= M.

Direct proof: Delta>M forces every g_i >=(Delta-A_i)/k_i>0, contradicting the
weighted raw-guard bound. The emitted proof shifts by (M-A_i)/k_i, moves
positive scaling inside rho, combines proof bounds with positive-min, bounds
the minimum of shifted guards by their positive weighted average, and clips
its nonpositive bound with zero. All final steps have budget zero until the
literal M is externalized. No mean-of-positive-parts assumption occurs.

This M is sharp for unrestricted guards with only these aggregate premises:
if Q=(eta+S_A)/H>=max A_i set g_i=(Q-A_i)/k_i. Otherwise choose j with A_j=M,
set g_i=(M-A_i)/k_i for i!=j and set g_j to make the weighted sum eta; g_j<=0.
All allowances equal M. Additional source relationships can make M loose.
The existing F06-C18 already excludes source-relative optimality; this audit
confirms rather than repairs that scope.

For the two shifted hinges, the independent contradiction proof uses
`r>a+(M-A)/alpha` and `r<c-(M-B)/beta`, incompatible at the declared M.
For unrestricted r, the plateaus or their intersection attain M. With raw=0,
A=0,B=1,a=c=0,alpha=beta=1 the same formula is 1 while the actual expression
is identically zero. This is a regression for the stated unrestricted-scalar
scope, not a false native inequality.

Decoder notes: K checking authenticates the returned proof, not arbitrary
unused term-table entries, original history, or resource sufficiency. The
term-occurrence limiter counts displayed new/old terms, not every term in rule
data. These distinctions need exact reporting and do not imply numeric unsoundness.

## Source grafting, primitive elaboration and softening correspondence

Let sigma assign each old source a closed new-signature term of the same unit.
At a finite new assignment y, put Phi(y)_z = [[sigma(z)]](y). Structural
induction, strengthened to captured local environments, gives
`[[sigma(t)]](y) = [[t]](Phi(y))`. Closure prevents local capture; fixed
conversion factors are needed in the conversion step. For exact normal forms,
send each source atom to the replacement's form, each min/max atom to the
operation on recursively transformed child forms, and extend linearly over
collected coefficients. Constant folding and cancellation commute with this
map. Thus recognized old exact equalities remain recognized after legal
substitution; this is not completeness of normalization.

Full inclusion `Phi(D_new) subset D_old` would require all original row bounds.
The actual `transport` interface does not require that stronger premise. Its
leaf replacements prove substituted normalized directions at CURRENT local
budgets. A row replacement originally global is first localized, so its actual
local budget can be smaller than its advertised global maximum. The recursive
reconstruction either uses an exact constant difference, grafts a checked leaf,
chooses an available proof-minimum parent, or rebuilds a native constructor with
new budgets. Each case induction therefore proves the mapped old expression
pair in that new case without copying historical budgets. Every new case is
covered; the final returned root is global, even when the new context has one
case. A local receiving request needs an explicit localization. Constant
shortcuts and available-parent choices mean that an arbitrary returned bound
need not equal the frozen original budget recurrence. Scope/observation labels
and the mathematical substitution do not certify the physical program map.

`prune` checks the entire input before deleting nonancestors. Sorting retained
old indices preserves strict parent order; `_copy_into` adds one constant index
offset. `localize` visits a fixed target case, chooses its unique parent at
`all_cases`, and otherwise reconstructs native nodes. Its memo key is a proof
node in one fixed localization, not an open term evaluated under varying local
environments. Literal root pairs are preserved; budgets can only decrease.

`compile_primitives` preserves the fixed numerical snapshot. Transitivity is
addition followed by cancellation; negation preserves the signed difference.
For slack k>=0, `min(0,k)<=k` at budget zero, added to `k<=0` at budget k,
produces a reflexive comparison at budget k. Adding it to the old proof and
rewriting gives the promised slack. Max congruence uses two injections into a
common old maximum; min congruence uses two projections from a common new
minimum. Residual congruence reverses the first comparison, adds the second,
and compares its preactivation with the unchanged zero branch. A proof minimum
keeps its currently cheapest parent. Each reconstructed node is checked to
retain its exact snapshot budget, and only the ten declared primitive tags
remain. The compiler is not evidence-update preserving: varying only row
allowances, its frozen chosen-branch budget is at least the original minimum
program, with equality at the compilation snapshot.

For the declared finite salvage grammar a label (S,b) denotes one strategy
requiring rows S. `(T,c)` with T subset S and c<=b dominates it for EVERY alive
set: availability is preserved and every budget consumer is monotone. Parent
combinations union supports but do not erase numeric multiplicity; a reused
row counts once as an identifier and twice in an additive use. Finite tree
unrolling witnesses independent choices at repeated DAG occurrences; for any
fixed alive set choosing one cheapest available strategy at a shared node
cannot worsen any monotone consumer. This does not turn the static global
frontier into the larger case-local salvage grammar. Explicit frontier limits
can refuse even when another shortcut already proves the root; neither
termination/resource optimality nor arbitrary proof-search completeness follows.

The independent softening receiver computes each affine intercept by evaluating
at the zero source assignment, which need not be feasible. Affine totality and
induction show this equals the collector's constant coefficient. Following only
the chosen case through `all_cases` reconstructs the LOCAL baseline b_h and the
symbolic allowance E. Retained rows contribute eta; removed rows contribute
`eta+max(direction-eta,0)`. Every other local budget constructor is reproduced.
Thus E>=b_h at every finite assignment, and E=b_h when the used withdrawn rows
hold; the conclusion Delta<=E additionally uses retained-row validity.
`receive_softening` checks the entire revised context, exact withdrawn indices,
b_h, E and E-b_h before binding the actual proof. After E's mathematical meaning
is checked, its returned syntactic presentation may be used in the literal
requested root. This is not permission for an arbitrary field to redefine the
request. A numerically valid allowance and authenticated provenance of a
specific earlier producer call remain different claims.

## A cancellation-aware sufficient moment and perturbation certificate

For the fixed signature with n numeric source coordinates, let F=N(t-s) be the
existing exact normal form of a well-typed paired difference. Define a vector
L(F) in nonnegative rational n-space. A source atom z_j has vector e_j. A min
or max atom with child forms G,H has vector `L(G) join L(H)` (componentwise
maximum). A form `c+sum a_i atom_i` has vector `sum |a_i| L(atom_i)`.
All recursion is over the finite normalized expression. Its constant is
`c0 = [[t-s]](0)`, where the zero source point need not be feasible.

For scalars a,b,c,d, put h=max(|a-c|,|b-d|). Monotonicity and common-translation
invariance give `|min(a,b)-min(c,d)|<=h`, and the identical statement for max.
For nonnegative coordinate differences d_j,
`max(sum p_j*d_j,sum q_j*d_j)<=sum max(p_j,q_j)*d_j`.
Induction on atoms and forms, using the triangle inequality at a collected
linear combination, therefore proves, for ALL finite x,y,

    |Delta(x)-Delta(y)| <= sum_j L_j |x_j-y_j|,
    |Delta(x)| <= |c0| + sum_j L_j |x_j|.

This is a sufficient bound, not the smallest Lipschitz vector or a complete
relevance analysis. Normalize the PAIRED difference before constructing it:
shared affine or identical-atom terms then cancel. For example
`res(z,z+x)` normalizes to `max(x,0)`, so z receives coefficient zero. In
contrast, the collector need not reduce `max(z+x,z+y)-z` to `max(x,y)`; a
nonzero z coefficient in its envelope need not be necessary. No new inference
axiom, piecewise-affine representation theorem, or F08 result is asserted.

For measurable random coordinates, first absolute moments are required only
for coordinates with L_j>0. Their finiteness implies
`E|Delta| <= |c0| + sum_j L_j E|X_j| < infinity`. No independence, second
moments or first moments for cancelled common baselines are needed. If the
actual random assignment lies in the requested proof domain almost surely,
K's pointwise constant bound then gives the finite paired mean `E Delta<=b`.
It does not authorize subtracting two individually infinite expectations.
Even without this sufficient moment certificate, a constant pointwise upper
bound makes Delta's positive part integrable and permits an EXTENDED mean in
[-infinity,b]. That distinct outer interpretation does not insert infinity
arithmetic into native terms or establish a finite utility number.

The same vector gives a quantitative source bridge. If x is in the checked
domain and actual compatible coordinates y satisfy `|x_j-y_j|<=d_j`, then
`Delta(y)<=b+sum L_j*d_j`. The coordinate meanings and program must stay fixed;
probability legality and observation constraints remain external. This is a
current paired comparison. A historical comparison is instead
`J_new(y)-J_old(x)=Delta(y)+J_old(y)-J_old(x)`, requiring an old-program drift
bound as well. A common baseline may have zero coefficient in Delta and a
nonzero historical drift. Taking J_new=Z-1 and J_old=Z makes the distinction
explicit: every current paired difference is -1, while historical change is
`Z_new-Z_old-1` and is unbounded without a drift premise.

In the existing fixed-report example,
`Delta=(s-p)/4+1/16+e`; its normalized vector is L_p=L_s=1/4, L_e=1 and
L_z=0 for the shared baseline. At beta=1/32, eta=1/16 the certified bound is
-1/64. Errors at most epsilon in EACH p and s, with e unchanged, cost at most
epsilon/2. Strict improvement survives epsilon<1/32; equality only gives
non-deterioration. This boundary is attained: start at p=7/16,s=0,e=1/32 and
move to p-epsilon,s+epsilon. At epsilon=1/32 the resulting paired change is
zero, and the probabilities remain legal. This does not assume that the old
guard bound continues to hold at the perturbed point.

For a symbolic soft allowance `Delta<=b+R`, R>=0, finiteness of E R gives a
one-sided integrable upper envelope. A finite paired expectation still needs
integrability of Delta's negative part; the normalized growth certificate is
one sufficient condition. For b<B, failure of inclusive threshold B implies
R>B-b, and failure of strict threshold B implies R>=B-b. Both admit the usual
upper bound `min(1,E R/(B-b))` under the stated probability premise, without
turning expected guards into pointwise guards or conditional coverage into
unconditional coverage. These elementary outer bridges are not new K rules.

## Consolidated theorem quantifiers and modeled-use witness

Fix the actual current context and request BEFORE considering a candidate
trace. The native theorem quantifies over every finite assignment in the
requested local case D_h, or in the union D_* for an explicitly global request.
Using D_* alone to test a local node is insufficient. All same-domain parents
are evaluated at the SAME assignment. Normalization validates every original
child before cancellation; neither a zero coefficient nor an equal-looking
source label creates a missing interpretation. A context fingerprint is a
stale-input guard, not a proof of physical identity or empirical correctness.
Even if a fingerprint collided, the numerical checker still checks actual
rows of the actual context; independently binding the intended context remains
the caller's obligation. Unsupported mutable/adversarial objects and resource
failures are not successful executions covered by the code-correspondence claim.

The sixteen native cases exhaust the implementation's rule dispatch. Negative
scaling is available in TERMS but not in the one-sided bound-scaling rule.
`negate` preserves the difference by reversing the pair; it does not negate an
upper budget. `meet_proofs` uses equal numerical differences, whereas
`all_cases` requires literally identical expression pairs and exact coverage of
all live cases. The latter takes a maximum, not a probability-weighted average.
Consequently hidden cases cannot silently become observations available to a
policy. Every stored instruction is checked before the designated root is
returned; an invalid unused instruction is not rescued by a small valid root.
These are explicit premises/correspondence facts, not claims that every possible
Python object is exhaustively validated by a security parser.

The direct report-policy model is nonvacuous independently of proof syntax:
under fixed report r, choose branch two with probability r; its unit-priced
failure probability is (1-r)p+r*s and resource cost is r/4. At reports 1/2 and
3/4, the intended paired difference with separately bounded discrepancy e is
(s-p)/4+1/16+e. With e<=1/32 and s-p+1/2<=1/16 the bound -1/64 follows, and
p=7/16,s=0,e=1/32 attains it. The shared finite baseline is arbitrary. These
numbers form a legal branch-probability model and a rational feasible source
point; the source witness does not establish that a measured deployment uses
that model. A report's calibration and a policy's improvement remain separate
claims. The new moment/perturbation envelope concerns this fixed paired program,
not a learned mechanism, an observation policy, or a replacement for F08.

## Initial integration failure: strict target versus negative bound

The first S4 run had two harness errors. It passed `strict=True` with the
request budget equal to the derived sharp budget -1/64. The receiver correctly
rejected this: strict means Delta < REQUESTED B, not merely Delta < 0. The
attaining point p=7/16,s=0,e=1/32 refutes the strict claim Delta < -1/64.
To request strict improvement, independently set the target B=0 while retaining
the emitted bound -1/64. The correction keeps both tests: rejection at the
attained target and successful strict acceptance at zero. No kernel, producer
or receiving condition is weakened. Initial source and failing logs are retained.

## Typed guard envelopes and a noncircular hinge proof

The guard envelope uses a NUMERIC gain relative to one fixed hinge. An
intermediate converted error can have a different unit from that hinge: its
actual upper/nonnegative K proofs retain the intermediate unit, while the
normal-form invariant states equality of numeric coordinates to gain*hinge.
At a min/max node both errors have the same current unit; taking K=max(gains)
and scaling `0<=error_K` by `1-gain_i/K` proves `error_i<=error_K` through a
same-unit rewrite. K=0 instead uses exact constant equality. Addition and
positive conversion preserve these invariants. Final discharge requires the
original guard and conclusion to have the same unit and performs a checked
rewrite to the typed final gain*hinge. Thus an intermediate numeric comparison
is not an illicit K unit conversion. The helper's builder-state invariant is
part of the construction contract; arbitrary manually forged builder states
are not independently authenticated by helper metadata.

The direct `disjoint_hinges` proof avoids sign compilation and positive-min:
put a=max(u,0), c=max(-u,0), m=min(a,c). From 0<=a and u<=a, obtain
-u<=a-u and 0<=a-u, hence c<=a-u. From m<=a obtain 0<=a-m;
from m<=c<=a-u obtain u<=a-m. Taking their common maximum gives
`a=max(u,0)<=a-m`, hence m<=0 by exact-difference rewriting.
For w=min(alpha*a,beta*c), K=max(alpha,beta)>0, nonnegativity of a,c gives
`w/K<=(alpha/K)*a<=a` and `w/K<=(beta/K)*c<=c`. Thus w/K<=m<=0,
so w<=0. K=0 is a constant proof. No case axiom or coverage lemma occurs.

The later positive-min construction splits only on a-c. On a<=c, the native
common-min rule gives a<=min(a,c), positive-part congruence gives
rho(a)<=rho(min(a,c)), and a lattice projection bounds min(rho(a),rho(c))
by rho(a). The other branch is symmetric. These branch proofs are discharged
using the already available direct disjoint-hinge lemma, then transported as a
row-free generic theorem. Weighted coverage uses positive-min only AFTER this
construction. The routine-level dependency order is therefore acyclic.

The strict ray API is intentionally narrower than arbitrary native exclusion.
Its nonzero parent-row weights must already have the guard's unit. For p:P,
parent p>=1 and price:P->U with factor 2, the native conversion rule proves
`-price(p)<=-2` in U. A raw-row ray in the U guard adapter cannot instead add
an unconverted P row. Refusal there is an availability restriction, not a
counterexample to the native exclusion or a missing sign in its theorem.

## Outer fault probabilities and value bounds

For at most k faulty ARGUMENTS about one same difference, the (k+1)-th smallest
bound is justified because its first k+1 indices contain a valid argument.
A SOURCE fault can disable several duplicated arguments; supports {a},{a},{b}
with bounds 0,0,1 and at most one source fault require worst-case bound 1, not
the median 0. This is why support identities and repeated numerical uses have
different accounting.

For a registered family with failure indicators F_i and Pr(F_i=1)<=alpha_i,
`d>B_(r)` implies at least r failed arguments. Removing any t<r indicators
leaves at least r-t failures, so its probability is at most
`sum_(i not removed) alpha_i/(r-t)`. Removing the t largest alpha_i is best
for that t; minimizing over t gives the implemented refined bound. Independence
is unnecessary. The event is STRICTLY d>B_(r): if d=B_(r), all inclusive
arguments may be valid. Issuing only when B_(r)<0 converts strict-improvement
failure d>=0 into that strict upper-bound failure event. It does not convert
an unconditional joint-error allowance into the same conditional-on-issuance
allowance; division by the issuance probability is still required.

High-probability source applicability alone does not bound expected loss outside
the certified domain. For example, a positive discrepancy M on an event of
probability epsilon contributes epsilon*M to a paired mean; no finite control
follows from epsilon alone when M is unbounded. A heavy positive discrepancy
can have infinite mean even though every realized source value is finite and
its old upper row holds with probability 1-epsilon. In contrast, a common heavy
tailed baseline can cancel entirely. The new envelope retains the discrepancy
coefficient but removes a normalized common baseline, making this distinction
explicit without claiming to validate supplied empirical moments.

## Actual case/coverage outputs and rewrite locality

In strict-ray sign compilation the surviving branch's normalized added row
may have a nonzero affine offset. The implementation adds a checked constant
comparison before rewriting the opposite-guard proof to that normalized row.
Thus grafting uses the actual shifted replacement budget. `branch_budgets`
records the original branch budget, not a promise that the returned current
proof has that identical bound; transport may improve it. In the two-live case,
the literal query pairs must agree, the reported gains come from the verified
single-hinge envelopes, and the returned comparison uses max(branch baselines).
No `CaseResult` narrative is authenticated merely by checking a separately
supplied arbitrary proof; the code postcondition presumes execution of this
transformation on its supported inputs.

For the scalar offset hinge formula, M>=A,B makes both shift distances
(M-A)/alpha and (M-B)/beta nonnegative. M>=Cstar is precisely the inequality
`a+(M-A)/alpha >= c-(M-B)/beta`, allowing the shifted hinges to be bounded by
opposite hinges of one scalar. Clipping the intermediate nonpositive offset
bound with zero is necessary. Baseline plateaus attain A and B on sufficiently
negative/positive free scalars; when Cstar exceeds both, the two active lines
intersect and attain Cstar. Sharpness is for a FREE scalar, not the image of a
source-constrained raw term. The zero-gain cases choose a constant branch.

Weighted coverage's H=sum(w_i/k_i)>0 and
`M=max(max A_i,(eta+sum w_i*A_i/k_i)/H)` make its shifts nonnegative. After
shifting, Delta-M is bounded by every positive part rho(v_i). The positive-min
lemma bounds it by rho(min_i v_i). Projections and weights w_i/k_i give
`min_i v_i <= sum_i w_i*h_i/H <= (eta-H*M+sum_i w_i*A_i/k_i)/H <= 0`.
The code then clips with zero, whose budget is exactly zero, and externalizes M.
For one entry this reduces to `A+k*max(eta/w,0)`. Entries require literal
common-query roots, positive weights/gains and local scope; the covering proof
may first be explicitly localized. Equivalent but differently displayed entry
pairs need their own checked rewrites rather than silent acceptance.

A second reconstruction views native terms as finite-valued functions on the
ambient source space. Restriction preserves their pointwise arithmetic and
lattice operations. An expectation is positive and linear on its integrable
domain but need not preserve min/max. Applying expectation to a complete
pointwise bound is therefore different from replacing its source functions by
means inside a nonlinear term. When only the paired difference is integrable,
apply the functional to that difference, not to two undefined absolute means.

Transport's rewrite argument uses identities valid on the AMBIENT source
space. Equality only on an old empirical domain is not a row-free identity.
For example, x=0 may follow from two old source rows, but K cannot rewrite a
constant proof into x<=0 without a row-dependent derivation. Under withdrawal
that dependence must be reestablished or discharged. The actual normalizer
receives a signature, not contextual assumptions; this is a load-bearing
condition of its substitution argument, not an assertion that contextual
reasoning is impossible. A future contextual simplifier would need explicit
proof/source dependencies rather than importing old equalities as constants.

## Integration, interface composition and the local zero-defect condition

The moment corollary fixes the signature, expression pair and rational request
bound. Finite native expressions are continuous (indeed the derived envelope
is globally Lipschitz), so measurable source coordinates make the difference
measurable; affine case domains and their finite union are measurable as well.
For a random data-selected bound, a finite realized number does not by itself
make its positive part integrable across datasets. Random coefficients/pairs
likewise require their joint moment hypotheses. Those are not covered by
silently reusing the fixed-expression certificate.

The existing coupling claim also survives this reconstruction. For the same
marginal laws of finite variables X,Y, if X-Y is integrable in each of two
couplings, its mean agrees in both. Apply symmetric clipping T_M to each
variable: `|T_M(X)-T_M(Y)|<=|X-Y|`, the clipped mean difference depends only on
the marginals, and dominated convergence gives the paired limit. Coupling can
change integrability and tails; it cannot change two FINITE paired means solely
by changing the coupling. The new common-baseline example changes no such
marginals or conclusion. Historical drift changes the comparison itself.

A current valid near-exclusion allowance is not authenticated historical
provenance. In particular the receiver checks the gain/guard relationship in
the supplied current numerical proof, not uniqueness of that gain or the fact
that a particular earlier procedure ran. A zero hinge admits multiple gains.
The softening receiver binds a stronger mathematical relation to a PARTICULAR
old proof, withdrawal set and revision; even it does not prove execution history
or physical source provenance. Either receiver may accept a different generator
that supplies the required checked postcondition. Conversely an arbitrary valid
trace does not authenticate a field used to construct the intended request.
Inputs defining the request/context must be fixed independently, and every
output field used to interpret that request needs the specified relation check.

For localized numerical discharge E>=b_h everywhere, and E=b_h whenever that
localized proof's used withdrawn rows hold. The actual bound Delta<=E still
requires its retained rows. Neither conclusion asserts that a single local
allowance is a global proof or that all cases share the same applicability.
A naive maximum of separately globalized case allowances may lose the desired
zero-penalty property on the original union. For example, use cases

    a: d-r<=0, r<=0;        b: d+r<=0, -r<=0,

with each proof deriving d<=0 by addition. With both rows withdrawn, their
allowances are `E_a=(d-r)+ + r+` and `E_b=(d+r)+ + (-r)+`.
At d=r=-1, case a originally holds and E_a=0, but E_b=1. The maximum gives a
positive penalty on an originally valid case. Here both fully discharged
allowances hold on the same enlarged domain, so their minimum is sound; with
different retained domains that minimum would require an additional common-
domain argument. The implemented contract deliberately localizes first and
makes no blanket global-vanishing assertion. This example tests its scope,
not a proposed new global-discharge implementation.

## Additional audit: rational countermodels and exact source syntax

For an invalid inclusive native bound, continuity gives a strict violation
neighborhood. A rational polyhedral case has rational points arbitrarily near
any of its points: retain all affine rows active at that point as equalities,
solve their rational affine system by elimination, and approximate within its
rational basis while preserving the finitely many inactive strict slacks.
Thus a strict violation admits a rational countermodel in that same case.
This density argument alone would not justify replacing a closed equality
failure of a STRICT target by a strict violation; the strict receiver instead
requires an inclusive certified bound genuinely below its requested target.
No exhaustive finite test or completeness procedure follows from the lemma.

The normalizer's lexical environment stores already captured forms. It does
not memoize an open `loc` node independent of its environment. The new envelope
memoizes closed NORMAL FORMS only, so it does not introduce that capture bug.
Legal source substitutions insert closed images once, rather than recursively
solving an equation when an old and new source happen to have the same name.
For example old x mapped to new x+1 is a finite coordinate substitution, not a
recursive source definition. The native semantic proof covers real assignments;
exact rational point tests are only executable instances of its algebraic proof.

## Observation, reflection and structural interpretation audit

For a COMPLETE finite state table, a desired action (or action-distribution)
map factors through observations iff it is constant on each observation fiber.
Necessity follows by composition; sufficiency defines the action at an observed
label using any member of its fiber. The two finite observation helpers check
exactly the supplied table, not its completeness for an actual deployment.
The native checker does not turn a hidden case into an observation and does
not establish that a predeclared min-of-action-losses term is implementable.
Same-query case compilation prevents one particular silent policy switch; it
is not a general observation-policy verifier.

Report calibration and utility can separate even with a legal branch model.
When p=0,s=1, h_r=(1-r)p+r*s=r: every fixed report is calibrated, but cost
h_r+c*r increases with r when c>=0. When p=1,s=0, raising r from 1/2 to 3/4
reduces failure probability by 1/4; at resource price c=2 it nevertheless raises
combined cost from 3/2 to 7/4. Thus the fixed c=1/4 in the checked improvement
example is a real component of its interpretation, not an irrelevant label.

If branch laws change with the report or time, write p_0,s_0 and p_1,s_1.
The historical change decomposes as

    (r1-r0)*(s1-p1+c)
      + (1-r0)*(p1-p0) + r0*(s1-s0) + (Z1-Z0) + e.

The first term is the current paired-policy comparison. The other terms need
explicit drift and proxy bounds; calibration of a new report cannot remove
them. All r values in this calculation are fixed rationals, so the represented
arithmetic remains native. A variable-by-variable product or an arbitrary
causal interpretation is not silently inserted into the term grammar.

Proof-local transport can omit unused numerical rows without full old-context
inclusion. It therefore does not automatically preserve operational assumptions
that those rows happened to encode. Withdrawing 0<=p<=1 can leave a sound
arithmetic polynomial comparison without a legitimate branch-probability
interpretation. For example p=2,s=0 can give a seemingly legal mixture output
for some r despite p itself being an invalid probability. The independently
checked physical/model domain must retain the component constraints; numerical
residual discharge alone does not repair probability or observation semantics.

Affine source offsets remain part of the current request. Old row x+2<=5 has
normalized direction x and budget 3. Under the explicit substitution x=2z-7,
a current row z<=4 yields the replacement 2z-7<=1, not 2z<=1 or a copied
budget 3. The added -7 comparison is a checked constant inference. Likewise,
a substitution x->new_x+1 is applied once; it is not recursive self-reference.
A physical meaning change behind a reused source label still requires an
external bridge, even though this numerical substitution is well-defined.

## Final correspondence reconstruction, 17:37:52–17:39:04 UTC

The envelope recursion is over finite closed normal forms, not over a syntax-only
cache of open local terms. If a form is `c + sum a_i A_i`, its coordinate vector
is `sum |a_i| L(A_i)`; for either lattice atom it is the coordinatewise maximum
of the two child vectors. For `d_j=|x_j-y_j|>=0`,
`max(sum L_1j d_j, sum L_2j d_j) <= sum max(L_1j,L_2j)d_j`.
Together with scalar min/max nonexpansiveness and the triangle inequality this
proves the actual recursion. Lexical collection closes local environments first;
normal-form rank is finite. The two local caches are new for each signature and
query. The zero assignment need not satisfy a context: the native denotation is
total on finite source assignments independently of a source case. Rational
symbolic coefficients establish the same structural identity for real sources;
finite rational tests do not stand in for that extension.

Weights are in the declared numerical coordinate conventions. A source may have
a different unit from the objective; a named conversion's factor enters its
weight. A moment is in that source's numerical units, not an implicitly inferred
physical unit. The fixed signature supplies these conventions. Altering a
conversion or program interpretation is not merely changing an evidence row.

The receiving condition authenticates a *valid current numerical allowance*,
not unique historical metadata. With zero gain, a different well-typed guard can
still describe the same valid allowance. The implementation nevertheless asks
for a guard proof: a deliberate availability restriction, not unsoundness.
With a nonpositive guard ceiling the positive-part contribution is zero, but an
inclusive sign branch can remain at equality; this is not strict infeasibility.
The explicit literal rewrites bind the final query without silently interpreting
proof minima as observable actions.

Softening visits root ancestors. An unused withdrawn row can be false while the
penalty remains zero; the correct vanishing hypothesis concerns *used* rows.
The recorded withdrawal set can still include unused requested rows. Duplicate
arithmetic uses need not be duplicate evidence sources.

A one-sided bound `Delta <= b+R` with integrable nonnegative R gives an integrable
positive part and hence an extended expectation in `[-infinity, b+E R]`; it need
not give a finite expectation. Take `Pr(n)=2^-n`, `Delta=-2^n`, `R=b=0`. Each
source value is finite and the numerical inequality holds, but the negative
mean diverges. The new two-sided difference envelope supplies a sufficient
finite absolute-moment condition. This is separate from the example in which
both absolute program means diverge but their common baseline cancels and the
paired difference is integrable. Neither argument introduces native infinity
arithmetic or automatic statistical calibration.

## Fresh receiver/model bridge reconstruction, 17:41:31–17:44:12 UTC

At the attaining paired-policy point `p=7/16,s=0,e=1/32`, the old objective is
`11/32+z` and the new objective is `21/64+z`, so the difference really is
`-1/64`, independent of the common finite baseline. The fixed reports influence
the mixture; their numerical correctness is a separate query, not a consequence
of this utility comparison.

A concrete report-update trap is present in the *same admitted model*. Under
`p<=1,s<=1/4`, `h(3/4)=p/4+3s/4 <= 7/16`. But issuing the report `7/16` changes
the behavior: at `p=1,s=1/4`, `h(7/16)=43/64 > 7/16` by `15/64`. These values
also satisfy the paired-policy guard. The old certificate is about a fixed
program parameter; replacing that parameter by its old bound is not a checked
rewrite. For a fixed rational `r` in `[0,1]`, the separate arithmetic
`h(r)<=1-3r/4` gives a uniform upper self-report when `r>=4/7`; at `r=4/7` the
bound is attained. This is a family of fixed-parameter affine examples, not a
new native bilinear operation, automatic fixed-point solver, or F08 result.
Any proxy discrepancy tied to one pair of programs cannot silently be reused
for a different pair merely because its source keeps the name `e`.

A structural cross-check uses the pointwise ordered vector lattice of finite
functions on the ambient source assignments. Translation preserves finite
joins/meets, negation reverses their order, and positive rational scaling is
monotone. These facts give the native signed max/min budgets, and residuals
use the additional unchanged zero branch. The disjoint-hinge argument needs
no total order on functions: with `a=u join 0`, `c=(-u) join 0=a-u` and
`m=a meet c`, the two bounds on m imply `0,u <= a-m`, hence `a<=a-m` and `m<=0`.
Only finite lattice operations are involved. Nonempty case evaluation prevents
a valid proof of the false constant judgment `0 <=[-1] 0`.

Expectation is a positive linear operation on integrable differences, not a
lattice homomorphism. Thus pointwise proof checking followed by expectation is
legitimate under the explicit integrability/domain premises, while replacing
source profiles by their means before nonlinear composition is not. A covering
family of cases supplies a maximum bound, not a probability distribution over
case witnesses or permission to average their bounds.

Source substitution naturally acts on *ambient* functions. It transports
source-independent identities, but a pullback of an old domain-restricted
inequality needs domain inclusion or fresh leaves. Example: old `x<=0`, map
`x=y+1`, new point `y=0`; the old zero bound is false after that map. A current
proof of `y+1<=1` supplies a sound new bound, not the historical zero. The actual
transport routine checks these new row-direction proofs and covers each current
case. Nonlinear closed images are allowed, but the old affine row's substituted
expression is then a proof goal, not automatically an admitted affine source row.
String observation/version agreement is a guard, not empirical or causal proof.

## Closing reconstruction, 17:44:51–17:48:03 UTC (separate closed D blocks)

For each node in the selected local proof, the independent softening receiver
has four simultaneous invariants: its numerical baseline is the localized old
budget; its symbolic allowance is the old bound program with the selected row
violations internalized; the actual difference is at most that allowance on the
retained local domain; and allowance minus baseline is globally nonnegative.
At all_cases it selects the unique requested parent, not the old maximum. At a
row it independently reconstructs the affine intercept by evaluation at zero.
The remaining recurrence follows precisely the sixteen audited native tags.
Equality with the baseline requires only the used withdrawn row defects to
vanish. Returned metadata is compared with that reconstructed expression and
context *before* the literal numerical request is checked.

This exact softening contract is different from near-exclusion's permitted
stronger output budget. An alternative valid but noncanonical softening
allowance is not automatically the stipulated bound program. Neither API
establishes that a particular historical producer call occurred, or that a
physical source has the meaning of its key. The fault-envelope and finite-policy
helpers likewise require their stated external error-count/probability premises
or complete finite observation/action table; they are not additional native
inference axioms or a check of all possible unlisted states.

For the fixed report model with upper component bounds `p<=P,s<=S` and a fixed
rational `r in [0,1]`, two nonnegative row scalings and addition prove
`h(r)-r <= P-(1+P-S)r`. This is directly compilable to native instructions.
When `d=1+P-S>0`, `r>=P/d` is sufficient and sharp on the full rectangular
component domain; a more constrained domain need not attain its corner. When
d=0, the probability range forces `P=0,S=1`, and all r satisfy the upper-report
condition without division. In the original example the corner `(1,1/4)` is
also feasible under the guard, so the three budgets at `r=3/4,7/16,4/7` are
exactly `-5/16,15/64,0`. Equality supports only an inclusive request.

At this same corner the modeled cost is `J(r)=1-r/2+z`. Replacing the old report
3/4 by its former bound 7/16 raises cost by 5/32 as well as invalidating that
report. Calibration and value are genuinely different questions: adding an
explicit calibration cost `lambda*|h(r)-r|`, lambda>=0, changes the objective to
`1-r/2 + lambda*|1-7r/4| + z`. Its two affine pieces meet at 4/7. Their slopes
show that the minimum is at r=1 for lambda<2/7, at r=4/7 for lambda>2/7, and on
[4/7,1] at equality. This is an elementary fixed-model illustration of declared
criterion dependence, not an empirical recommendation, a new primitive, an
implemented optimizer, or F08 work. No discrepancy premise for one old program
pair is silently inherited by a different pair or criterion.

Unclocked derivation between closed blocks is retained as reconstruction context
but earns no time credit. Closed mixed/recovery intervals are explicitly excluded
in the actuals file. Reported D time is not inferred from this document's length.
