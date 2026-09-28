# F07 — soundness of finite, source-aware signed-loss derivations

Status: **first reconstruction; F07 partial**. September 27, 2026 (UTC).
Reviewed input: `12ba077cb55ef177b5f49ad667dd6750f4e98836`.
Semantics: [F05 provisional core](../foundations/03_provisional_core.md).
Rules: [F06 register](02_inference_rules.md).
Implementation under review: [the unchanged F06 checker](../checks/f06_inference_rules.py).

This note proves an ordinary mathematical soundness result for a precisely
specified finite fragment. It does not define validity to mean acceptance by
the checker. It does not import Rational Lawvere Logic's soundness by analogy,
prove empirical premises, establish general program correctness, or complete
F07's separate D90/reconstruction obligation. The proof is a same-assistant
reconstruction, not a proof-assistant development or an independent review.

## 1. The theorem boundary

The **native fragment K** consists of all sixteen instruction tags recognized
by the reviewed checker:

`constant`, `row`, `rewrite`, `trans`, `add`, `scale`, `negate`, `convert`,
`slack`, `meet_proofs`, `max_common`, `min_common`, `congruence`,
`res_congruence`, `lattice`, and `all_cases`.

This is not just the ten-tag macro basis from F06. Every native tag is audited
below. Source transport, residual discharge, sign splitting and imperfect
coverage are *producers of K traces*, not extra axioms. Their generated traces
are covered when checked against the intended current context; whether each
producer always terminates with the requested output is a separate obligation.

K uses finite, closed, well-typed syntax built from rational literals, declared
source coordinates, addition, rational scaling, minimum, maximum, the residual
`res(a,b)=max(b-a,0)`, nonrecursive lexical bindings and named positive rational
unit conversions. Negative source values and negative comparison budgets are
permitted. The source domain can be unbounded. Values at each particular
assignment must nevertheless be finite real numbers.

The following are deliberately outside this theorem: infinite syntax or proof
cycles; arbitrary Python objects with adversarial methods; mutation of inputs
during checking; floating-point substitution for exact rationals; arithmetic on
positive and negative infinity; native nonlinear multiplication/division;
automatic observation-policy verification; empirical source validation; and a
proof of the entire interpreter or hardware. Resource failure is not acceptance.
These scope conditions are not permanent restrictions on the research program.

## 2. Semantics independent of the proof system

A signature fixes source names and units, and a table of conversions. For every
unit u, use a copy R_u of the finite reals with a chosen numerical coordinate.
A conversion c:u->v with declared k_c>0 means multiplication by that factor
between those unit copies. As in F05, this table can also contain valuation
bridges; reversed unit names do not imply inverse physical meaning or
reciprocal factors. A comparison never silently equates costs
measured under different criteria or with different units.

An assignment x supplies a finite real for every declared source coordinate.
For a local environment rho, define E(t,x,rho) recursively:

- E(q_u,x,rho)=q and E(src(z),x,rho)=x_z;
- E(loc(z),x,rho)=rho_z;
- addition, scaling, min and max have their ordinary real interpretations;
- E(res(a,b),x,rho)=max(E(b,x,rho)-E(a,x,rho),0);
- E(let z=a in b,x,rho)=E(b,x,rho[z:=E(a,x,rho)]);
- E(convert_c(a),x,rho)=k_c E(a,x,rho).

The right-hand side of a let is evaluated in the *old* environment. Source
names and local names occupy separate namespaces. All proof conclusions are
closed with respect to local variables. Write E_x(t) for an empty initial rho.

A context C has a nonempty finite set H of live cases. Its case h has affine
rows l_hi<=r_hi and a supplied rational feasible point. Let

    D_h = {x : E_x(l_hi)<=E_x(r_hi) for every row i},
    D_* = union_(h in H) D_h.

The hidden tag h is retained when case identity matters; union notation here
only abbreviates the numerical part. A case need not be bounded or full
dimensional. Its witness proves nonemptiness, not empirical correctness.
Define the domain of a local judgment to be D_h, and the domain of a global
judgment (case tag `None`) to be D_*.

The independently defined semantic assertion is

    C ; h |= t <=[b] s : u
    iff for every x in D_h, E_x(t)-E_x(s)<=b,

with D_* used for a global judgment. This definition mentions neither proof
steps nor algorithms. A semantic countermodel is an x in the specified domain
with E_x(t)-E_x(s)>b. Testing a point outside that domain does not refute it.

The comparison is about numerical denotations. Claiming that t and s denote
losses of two particular deployed programs additionally requires the declared
program/source interpretation and observation contract; the companion
[scope note](03a_soundness_scope_and_use.md) states that bridge explicitly. A successful mathematical term comparison does not inspect
arbitrary program code.

## 3. Evaluation and normalization lemmas

### Lemma S1 — totality, typing and finiteness

For a well-typed finite term t, a finite assignment x and a type-compatible
local environment, E(t,x,rho) is uniquely defined, finite and in t's declared
unit.

**Proof.** Induct on the syntax. Leaves have assigned finite values. Addition,
rational scaling, min, max and finite subtraction are total on finite reals.
A positive conversion supplies one finite result in its named target unit.
For a let, first apply induction to its right-hand side using the old rho;
then apply induction to its proper body subterm in the extended environment.
No recursive binding occurs. Each constructor fixes a unique result. The
explicit unit checks disallow combining unlike quantities. ∎

A zero multiplier does not excuse an ill-typed or unbound child: the type
checker traverses that child before normalization. Totality is important when
an expression later cancels; no undefined expression is made meaningful by
subtracting it from itself.

### Lemma S2 — exact collection with opaque nonlinear atoms

The normalizer used by K preserves E_x(t), for every admitted real assignment.
It may fail to recognize a true equality, but equality of its normalized forms
implies equality of denotations.

**Construction and proof.** A normal form is a pair (c,A), where c is rational
and A is a finite rational coefficient map on the following well-founded keys:
source names, or `(min,N1,N2)` / `(max,N1,N2)` with already constructed normal
forms N1,N2. Define its valuation by

    V_x(c,A)=c+sum_k A(k) V_x(k),
    V_x(source z)=x_z,
    V_x(min,N1,N2)=min(V_x(N1),V_x(N2)),
    V_x(max,N1,N2)=max(V_x(N1),V_x(N2)).

The recursive key structure is finite. Literal collection gives (q,empty),
source collection gives (0,{z:1}), addition adds coefficient maps, and scaling
multiplies every coefficient and c. Deleting a zero coefficient preserves the
finite sum. Unit conversions multiply by their declared rational factor.

For min/max, if both children are constant forms the ordinary rational
minimum/maximum is evaluated. Otherwise the pair of fully normalized children
is retained as a single key with coefficient one. Its valuation is exactly the
required operation by definition. Residuals normalize the form for b-a and
then apply max with zero. No hypothesis about an active region is used.

Maintain a *normal-form environment* for lexical variables. At a let, normalize
the right-hand side in the old environment and bind that complete form while
normalizing the body. Its meaning has already captured the old bindings;
subsequent shadowing does not change it. Induction on the constructors gives
V_x(N(t))=E_x(t). Equal normal forms have equal V_x, proving the claim. ∎

The proof applies to source rows too: the row normalizer is the affine
restriction of the same coefficient argument. Ordering serialized keys is an
implementation detail. A structural equality comparison cannot equate two
*different* coefficient maps merely because their display names resemble one
another. Distinct source coordinates are not collapsed by numerical samples.

### Corollary S3 — exact-difference replacement

If all four terms have unit u and N(t-s)=N(a-c), then

    E_x(t)-E_x(s)=E_x(a)-E_x(c)

for every assignment. Consequently any valid bound on a-c is a valid bound on
t-s. This is the soundness bridge for both `rewrite` and the checker's final
comparison with the result expected from a rule. It is not contextual equality
inferred from a sample or from an unproved source alias.

### Lemma S4 — normalized source row

Suppose the declared row is l<=r, with

    E_x(l-r)=a^T x+c.

K's normalized row has left expression l-r-c, zero right expression, and budget
eta=-c. Every feasible x satisfies a^T x<=-c; therefore the normalized judgment
is valid. The proof uses the actual row of the supplied context, not a cached
claim about its earlier revision. ∎

## 4. Local rules: complete case audit

All parents of a non-`all_cases` instruction have the same domain as their
conclusion. In this section fix an arbitrary assignment x in that domain and
write t for E_x(t). This pointwise proof is why arbitrary dependence between
source coordinates is harmless: all parent inequalities hold at the same x.

### S5.1 — `constant`, `row` and `rewrite`

For `constant`, N(t-s) contains only c. Lemma S2 gives t-s=c everywhere, so the
stated budget c is exact. For `row`, use Lemma S4. For `rewrite`, use Corollary
S3 and the parent's established inequality. These rules require no optimization
oracle and no assumption that a finite sample exhausts the source.

### S5.2 — `trans` and `add`

Transitivity has t-m<=p and m-s<=q, where normalizer equality certifies that the
two displayed middle terms really agree. Adding gives t-s<=p+q. Addition has
`t1-s1<=p` and `t2-s2<=q`; summing gives

    (t1+t2)-(s1+s2)<=p+q.

The same parent can be referenced twice: its numerical difference and bound
then occur twice. This is not a claim that its underlying evidence was sampled
independently or that its confidence doubles.

### S5.3 — `scale`, `negate`, `convert` and `slack`

If t-s<=b and k>=0, then kt-ks<=kb; this includes k=0 and negative b.
Negation reverses the pair: (-s)-(-t)=t-s<=b. It does not infer -t+s<=-b.
A conversion has k>0 and transports the same inequality and its budget into
the named target unit. A fixed slack d>=0 gives t-s<=b+d. A different context's
interpretation is not obtained just by changing a conversion's label.

### S5.4 — `meet_proofs`

The two parents must prove the same numerical difference, up to Lemma S2.
That difference is <=p and <=q, hence <=min(p,q). This chooses a *proof bound*,
not an action that can observe a hidden state. No new behavior is authorized.

### S5.5 — `lattice`

The four zero-budget instances are min(a,b)<=a, min(a,b)<=b, a<=max(a,b), and
b<=max(a,b). Each follows directly from the ordinary real order. They remain
true for negative values, equal arguments and all activation boundaries.

### S5.6 — `max_common` and `min_common`

For a-c<=p and b-c<=q, max(a,b)<=c+max(p,q). For c-a<=p and c-b<=q, let
m=max(p,q). Then c-m<=a and c-m<=b, so c<=min(a,b)+m. No sign restriction on
p,q is needed. The required common expressions may be matched through exact
normalization, but not merely through equal means or equal marginal ranges.

### S5.7 — `congruence`

For F=min or max, suppose a1-b1<=p and a2-b2<=q. Let m=max(p,q). Monotonicity
and the common-shift identity of F yield

    F(a1,a2)<=F(b1+m,b2+m)=F(b1,b2)+m.

Thus the returned budget is m. This proves the signed-budget rule at positive,
zero and negative m. The common-shift identity is essential: a generic monotone
nonexpansive map need not preserve strict improvement in a saturated region.

### S5.8 — `res_congruence`

Write the first parent a_old-a_new<=p and the second b_new-b_old<=q. Then

    (b_new-a_new)-(b_old-a_old)<=p+q.

Put d=p+q. Since res(a,b)=max(b-a,0), apply the max congruence argument with
budgets d and 0 to obtain

    res(a_new,b_new)-res(a_old,b_old)<=max(d,0).

The first argument is contravariant and the second covariant. The zero floor
cannot be discarded when d<0: both residuals can be zero despite a strictly
negative change in their preactivations. This proof makes neither independence
nor differentiability assumptions.

### S5.9 — `all_cases`

There is exactly one local parent for every live h, no duplicates, and all
parents have the same literal new/old expression pair. Take any point of the
union domain and its case h. Its local parent proves t-s<=b_h. Since the
returned global budget is max_h b_h, the global inequality follows. Overlapping
cases are harmless. Missing cases, a minimum over budgets, or averaging without
a probability model would not justify this universal assertion.

The common-expression restriction is a checkable sufficient condition on the
mathematical query. Whether those expressions denote a fixed executable policy
still requires the external operational interpretation. Literal syntax equality
is not a verifier for arbitrary action code.

## 5. Derivation-level soundness

### Theorem S6 — finite K soundness

Let C be an admitted context, P a finite acyclic K trace, and n its designated
root. Assume every instruction passes the stated type, reference, domain,
shape and rational-budget checks. If the root is `t <=[b] s : u` local to h,
then C;h |= t <=[b] s:u. If it is global, C |= t <=[b] s:u.

**Proof.** Induct on the position of each instruction in the trace. Every parent
index is strictly smaller than its child's, so its semantic statement is
available by induction. Constant/source/lattice nodes satisfy their pointwise
lemmas without parents. Every other local constructor preserves the common
parent domain by section 4. The case-union constructor has the coverage premise
needed for S5.9. Finally, the checker may permit a different pair with the same
normalized difference as the constructor's expected pair; Corollary S3 transfers
the just-proved inequality to the recorded pair. This establishes the invariant
for every instruction, including the selected root. ∎

The trace can share a parent across descendants. Induction is on the DAG's
ordered nodes, not an assumption that it is a tree. Shared numeric contributions
are still added wherever the rule calls for addition. Unreachable instructions
are also checked by the reviewed implementation; a valid unused prefix cannot
rescue an invalid root, and an invalid unused node is conservatively rejected.

### Corollary S7 — the supremum target

For an accepted global root, the independently defined target B_C(t,s) satisfies
B_C(t,s)<=b. If b<0 this entails uniform modeled improvement of at least -b. If
B_C(t,s)=+infinity, no trace meeting the hypotheses can certify a finite b.
No supremum is evaluated by the proof checker to obtain this conclusion. ∎

### Corollary S8 — nonvacuity and no inconsistent self-comparison

Every admitted case and the union contain a point. Therefore no accepted root
with t and s identical can have b<0. Such a root would imply 0<=b at a supplied
witness. Rejection of an empty source is an *admission policy*, not an inference
from consistency of real arithmetic to empirical truth. ∎

## 6. What this proves about the reviewed program

The reviewed `check` validates C, traverses each Step in order, checks backward
parent indices and common local/global scope, calls `_expected`, compares the
actual budget to its exact returned budget, and checks equality of numerical
differences using `_form`. The native tag-to-lemma correspondence is exhaustive:

| Program path | Mathematical obligation |
|---|---|
| `infer`, finite assignment, let evaluation | S1 |
| `_form`, `same_difference` | S2–S3 |
| `normalized_row` | S4 |
| `constant`, `row`, `rewrite` | S5.1 |
| `trans`, `add` | S5.2 |
| `scale`, `negate`, `convert`, `slack` | S5.3 |
| `meet_proofs` | S5.4 |
| `lattice` | S5.5 |
| `max_common`, `min_common` | S5.6 |
| `congruence` | S5.7 |
| `res_congruence` | S5.8 |
| `all_cases` | S5.9 |
| sequential loop and final return | S6 |

Under the supported immutable data representation, exact integer/Fraction
arithmetic and ordinary execution of those operations, successful termination
therefore entails the corresponding numerical semantic assertion. This is a
written algorithm-level correspondence argument, not a formal verification of
Python, hashing, memory safety or all possible foreign object subclasses.

A context fingerprint is a stale-input guard, not evidence that a source is
correct. Numerical soundness for the *context actually passed to check* does
not require a theorem that hashes are injective: the rules and row budgets are
revalidated against that context. Cryptographic identity and version records
matter separately when claiming that this is the intended physical model,
criterion or program. No equality of hashes establishes those external meanings.

## 7. Emitted traces and the trust boundary

A producer may use linear optimization, neural proposals, branch search, symbolic
relaxation or other heuristics. If its output is a K trace, the output is checked
in C, and its root is the intended requested pair/budget, S6 establishes that
root's numerical claim. Producer quality can affect whether a useful trace is
found, its size and its bound; it need not be trusted for this conditional claim.

There are two distinct checks here:

1. **trace validity:** every encoded inference follows from its actual parents;
2. **request binding:** its root concerns the requested expressions, unit,
   local/global case and current context, with a bound strong enough for that use.

`check` performs the former and returns the actual root. A caller that merely
sees a successful return, ignores the root, and announces some stronger or
unrelated request has no soundness theorem. For example, a proof of x<=1 is not
a proof of x<=0 just because both are legal terms. A fresh request-bound audit
adapter and hostile fixtures will make this distinction executable without
changing the original checker.

Residual-discharge outputs require an additional discipline: their root often
says `t <=[0] s+E`. S6 justifies that exact expression-valued allowance. It does
not say E<=0, that E is small in expectation, or that a withdrawn premise is
actually satisfied. Reintroducing any such conclusion needs its own proof or
explicit external probabilistic premise.

## 8. Remaining F07 work

This first reconstruction covers native fixed-context arithmetic soundness and
its interface to checked producer outputs. F07 remains partial while its D90
floor and further reconstruction are outstanding. Continue with an independent
reconstruction of source/observation transports and selected producer contracts,
plus the precise assumption-to-operational bridge. Do not advance F08 or Gate B.

See the companion [trust and operational reconstruction](03a_soundness_scope_and_use.md)
for worked semantic checks, failure witnesses and the probability/expectation
boundaries. Validation and actual timing are in the F07 work log. No claim of
new mathematical priority, completeness, trained neural realization or
metaphysical access follows from S6.

The [graded reconstruction](03b_graded_soundness_reconstruction.md) proves
assumption-loss and source-substitution corollaries. The [function-space audit](03c_function_space_reconstruction.md)
reconstructs the argument algebraically and records the failed expectation
extension and guard counterexamples. These are parts of the same partial F07
work item, not an independent reviewer or the later characterization task.
## 9. Environment dependence and safe memoization boundary

This lemma checks a dependency that both an evaluator and an optimized normalizer
must preserve. It does not change either implementation in this checkpoint.

Let FS(t) and FL(t) be the syntactically free source and local names. Constants
have neither, a source/local leaf has its corresponding singleton, and arithmetic
constructors take unions. For a nonrecursive binding,

    FS(let u=a in b) = FS(a) union FS(b),
    FL(let u=a in b) = FL(a) union (FL(b) minus {u}).

### Lemma S9 — evaluation respects the relevant environment

Fix the conversion meanings and suppose the terms are well typed in both
environments. If x and x' agree on FS(t), and rho and rho' agree on FL(t), then

    E(t,x,rho) = E(t,x',rho').

**Proof.** Induct on t. Leaves read only the named coordinate. For an arithmetic
constructor, agreement on the union supplies each child induction hypothesis,
then the same deterministic operation returns equal results. At let u=a in b,
the outer environments agree on FL(a), so the bound values agree. The extended
environments consequently agree on u and on every other name in FL(b), because
those other names lie in the outer free-name set. Apply the body hypothesis.
The source agreement holds for both subterms. ∎

There is an analogous *syntactic* statement for normalization: equality of the
captured normal-form environment on FL(t), with the same source names and
conversion table, yields the identical collected normal form. Its proof is the
same structural induction with normal-form operations in place of evaluation.
The dependency sets can overapproximate actual dependence: t=x-x has a free
source x but denotes zero. No minimal-dependency characterization is claimed.

A memoization scheme keyed only by node identity is not justified when a shared
node is interpreted under different local environments. Let h be one shared
`local('h')` object and use max(h,0) under two separate bindings h=0 and h=1.
The two results are 0 and 1. Reusing the first cached result for the second
changes denotation and can create a false normalization equality. A safe cache
must additionally distinguish the relevant environment (and current source
assignment/conversion meanings when caching evaluations), or first produce a
properly captured closed representation. S9 supplies a sufficient invariant,
not a new trusted normalization rule or an implementation optimization claim.

The current checker recursively unfolds term occurrences, so a compact Python
object DAG does not automatically imply linear work. With t_0=x and
`t_(n+1)=t_n+t_n`, there are only n+1 distinct shared term objects but an ordinary
recursive traversal visits 2^n leaves. The collected form is merely 2^n*x.
Thus successful finite checking and proof soundness establish neither a chosen
complexity bound nor a performance advantage. The regression runtime recorded
for this session is an observed fact, not a consequence of the mathematical
soundness theorem.

The requested relation here is inclusive: t-s<=b. A caller demanding strict
improvement t-s<epsilon needs a certified b<epsilon, or an additional strict
argument. Equality b=epsilon does not establish that strict request. The audit
receiver deliberately exposes only the declared inclusive-bound interface;
strict action thresholds are not silently substituted for it.

### Corollary S10 — a request-bound receiver is numerically sound

Let J=(C,h,t,s,b_req,u) be a well-typed inclusive-bound request. Suppose a
receiver invokes the native checker on a supplied trace P in C, obtains root
(t_root,s_root,b_root,h_root), and verifies

    h_root=h, t_root=t, s_root=s,
    root_unit=u, b_root<=b_req.

Then J's source-relative numerical assertion holds.

**Proof.** S6 gives the root inequality on the root's domain. The domain and
term equalities make this exactly the requested domain and difference. The
unit equality prevents comparing unrelated numerical coordinates. The final
rational comparison and order transitivity weaken the root inequality to
b_req. All hypotheses are needed for the stated request, even when some
alternative proof could establish it. If instead a strict threshold epsilon
is requested, the stronger check b_root<epsilon gives t-s<epsilon; replacing
it by equality or a non-strict check is insufficient. ∎

This is a wrapper around the existing calculus, not an additional inference
axiom. The implementation can conservatively demand literal term identity and
current context identity. Any more permissive equivalence adapter needs its
own checked argument before S10 applies.
