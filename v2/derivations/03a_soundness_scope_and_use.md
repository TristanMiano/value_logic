# F07 S1 — soundness scopes, independent reconstructions and hostile boundaries

Status: **first-pass derivation record; F07 remains partial**.
Base: `12ba077cb55ef177b5f49ad667dd6750f4e98836`.
The companion [soundness theorem](03_soundness.md) audits all native F06 tags.
This note supplies the assumptions that connect that numerical theorem to use,
not a redefinition of usefulness as proof-checker acceptance. The examples below
are reconstructed directly from denotation, not from the rule engine's output.

## 1. Reconstruct the composite claim without using proof syntax

Let a context constrain five finite real quantities by

    N1-O1-theta <= -3/4,
    N2-O2+theta <=  1/4.

Take an arbitrary feasible tuple; do not give theta a guessed distribution.
Adding its two real inequalities yields

    N1+N2-O1-O2 <= -1/2.

The term theta cancels because it names the SAME coordinate in both rows. A
feasible point is theta=1/2, O1=O2=1, N1=N2=3/4. Thus the conclusion is not
vacuous, and the bound is attained. Adding any common z>=0 to both old and new
costs in a component preserves the premise and conclusion while allowing
absolute losses to grow without a finite global upper bound.

Now replace the first occurrence by theta1 and the second by theta2. The sum
has remaining term theta1-theta2. With theta1=1, theta2=0, O1=O2=0 and
N1=N2=1/4, the two split-source rows hold at equality while the composite
change is +1/2. Merely retaining identical names in explanatory prose, or
similar distributions for two coordinates, does not justify cancellation.
The copied source identity is a mathematical premise with operational meaning.

This is the independent semantic counterpart of F06's partial-contract proof.
It uses no normalizer, no generated root and no evaluation at a favored point
to establish the universal inequality. The single point separately proves
nonemptiness and tightness.

## 2. Negative budgets, order operations and opposite residual polarity

### 2.1 Exact signed translation versus one-argument saturation

If a1-b1<=p and a2-b2<=q, setting m=max(p,q) gives both a_i<=b_i+m.
For min/max, a simultaneous translation by m passes through the operation;
hence the difference of the results is <=m even if m<0.

A unilateral improvement does not give the same negative bound. Let a=-1,
b=0. Then a-b=-1 but max(a,0)-max(b,0)=0. Thus the nonnegative floor in the
one-argument ReLU/residual comparison is necessary. It is not gratuitous
pessimism added by a probabilistic assumption.

### 2.2 Residual direction countermodel

For res(a,b)=max(b-a,0), decreasing a can *increase* the result. Choose
old first argument a0=1, new first argument a1=0, and b0=b1=1. The forward
comparison a1-a0=-1 holds, but

    res(a1,b1)-res(a0,b0)=1.

The source rule therefore requires an upper bound on a0-a1, not a1-a0.
Even with that correct polarity, replacing max(p+q,0) by p+q is invalid when
both resulting residuals are zero. These two mutations test distinct premises.

### 2.3 Independent branch extrema are not joint proof extrema

For two live cases x=0 and x=2, the casewise bounds on x are 0 and 2. The
union bound is 2, not 0 or their arithmetic mean. If a source is restricted to
x=0, its local proof remains true, but relabeling it global while leaving the
x=2 case live is false. That is why the checker requires exhaustive names and
why a request receiver must distinguish a local from a global root.

## 3. Lexical scope is a soundness premise

Consider

    t = let h=x in max(h,0),
    s = let h=y in max(h,0).

Treating `max(h,0)` as an opaque key *before* substituting its captured binding
would falsely cancel t-s. At x=1,y=-1 the true difference is 1. In the reviewed
normalizer the nonlinear keys are built from the normalized children x and y,
so this false equality is not recognized.

A second case needs genuine lexical capture:

    let h=x in (let k=h in (let h=y in max(k,0))).

Its value is max(x,0), not max(y,0). The old value of h was captured when k was
bound. A third case, `let h=x in (let h=h+1 in max(h,0))`, uses the old h on
the inner binding's right-hand side and equals max(x+1,0).

The normalizer proof uses an environment of already interpreted/normalized
values, not a global dictionary of unresolved local names. Memoization by a
shared syntax node alone would be unsafe under different environments. No such
memoization is presumed in the soundness theorem.

## 4. The theorem is conditional, but not vacuous

There are three logically separate questions:

1. Does a supplied finite source have an interpretation? Its rational witness
   answers this for the mathematical rows.
2. Do the inference rules preserve comparisons under that interpretation?
   The native soundness theorem answers this for every feasible real point.
3. Does the source and cost interpretation correctly describe a current use?
   That requires empirical/formal/operational bridge assumptions of the named
   evidence mode and program version.

A witness answers (1), not (3). A finite test checks specific instances of (2),
not the unrestricted theorem. A version string is an identity guard, not a
proof of (3). Keeping these distinctions does not prevent warranted action;
it states which kind of warrant has actually been obtained.

A source saying x<=0 admits x=0 and can yield a perfectly sound conditional
proof. In an actual setting with x=1, using that conditional proof as an
unqualified assertion fails because the source premise fails. This is not a
counterexample *inside* the source and hence not a refutation of numerical
soundness. A zero-premise proof of x<=0 would instead be refuted by x=1.

## 5. Successful proof checking is not the requested theorem

The checker returns a checked root. It does not receive the user's separate
intended query. Consequently, a caller must bind its request to that root.
A certificate for x<=1 may be sound while being inadequate for a requested
x<=0. A local certificate can be sound while being inadequate for a request
over all cases. A stale criterion or different program version can be the
wrong operational claim even if the current numerical proof is valid.

A sufficient receiver contract is:

- validate the expected current context and the requested term units;
- check the entire trace;
- require the root to have the requested local/global domain and literal term
  pair (or a separately proved equality adapter);
- require root_budget<=requested_budget.

The last condition is ordinary sound weakening. Literal-pair matching is
conservative: it can reject semantically equivalent presentations, but cannot
silently substitute a different action or target. The new F07 audit adapter
will implement this contract; it adds no inference instruction to the original
checker. It also does not infer empirical truth or program legality from the
matching strings.

## 6. Pointwise soundness of a data-selected proof

Here is a useful positive consequence of making the source condition explicit.
A proof can be selected AFTER looking at the evidence without automatically
requiring an extra failure allowance for every attempted algebraic argument.
What is required is a validity event for the source actually used.

### Proposition U1 — selected-proof implication

Let omega range over a probability space. A record D(omega) determines a context
C_D, a finite proof P_D and a requested numerical pair t_D,s_D with budget b_D.
Assume these objects and the resulting event statements are measurable. Let
A be the event that the request-bound receiver accepts. Let Theta(omega)
be the actual hidden case/finite source assignment under the declared model.
Define E as the event that Theta lies in the REQUESTED domain: the admitted
union for a global request, or the specified case domain for a local request
(with its case interpretation retained). Assume Pr(E)>=1-alpha.

Then

    Pr[A and (E_Theta(t_D)-E_Theta(s_D)>b_D)] <= alpha.

**Proof.** For each omega in A intersect E, instantiate the deterministic
soundness theorem at the context and proof selected by that particular record.
The actual assignment is a member of its semantic domain, and the receiver
binds its root to the requested pair and budget. The displayed strict failure
is impossible on A intersect E. Therefore A intersect failure is contained in
E-complement; probability is monotone under inclusion. ∎

No stochastic independence between D, the proof, or the selected budget is
used. The difficult external premise is the coverage of the SELECTED REQUEST DOMAIN,
not the algebraic proof search. Fixed-query versus record-dependent-query
interpretations must remain explicit; the theorem is not a universal guarantee
for an arbitrary new criterion that lacks a source bridge.

### 6.1 Marginal row validity is a different premise

If events E_i jointly make all relevant rows valid and Pr(E_i^c)<=alpha_i, the
union bound gives Pr(intersection_i E_i)>=1-sum_i alpha_i. This may be much
weaker than a direct joint event. Independence would give a different bound
but cannot be inferred from using different proof nodes.

A minimal counterexample to substituting marginal for joint coverage has
actual x=1 and two equally likely records. In the first, upper bounds for x
are (0,1); in the second they are (1,0). Each bound individually covers x with
probability 1/2. Selecting their minimum outputs 0 and fails with probability
one. The combined context is nonempty at every record (it contains x=0), so
feasibility does not repair the missing empirical premise.

Conversely, reusing ONE valid source event in one hundred arithmetic steps
adds no new validity event. A duplicated numerical premise contributes twice
to an additive bound, but its empirical event occurs once. Numerical resource
accounting and statistical evidence accounting are not interchangeable.

### 6.2 Conditional-on-acceptance error is not alpha

U1 bounds Pr(A and failure). It does not assert Pr(failure|A)<=alpha.
With actual x=1, suppose a data procedure outputs the singleton {0} with
probability alpha and {1} otherwise. A receiver asked to certify x<=0 accepts
only in the first record. The source procedure has coverage 1-alpha, yet every
issued conclusion is wrong. Then Pr(A and failure)=alpha and
Pr(failure|A)=1.

For Pr(A)>0, U1 implies only Pr(failure|A)<=min(1,alpha/Pr(A)) without a stronger
conditional validity assumption. This distinction is material when a system
abstains on most records, as phase one's experimental discussion already made
operationally relevant. It is not a defect in the real-inequality proof rules.

### 6.3 Repeated inquiry

For rounds n with validity events E_n, a uniform event E contained in every
E_n supports arbitrarily many adaptively selected finite checked proofs on E.
Alternatively, Pr(E_n^c)<=alpha_n yields a finite-horizon bound sum_(n<=N) alpha_n,
and a countable-horizon bound sum_n alpha_n when that series is meaningful.
A per-round fixed alpha is not a perpetual guarantee: independent false-source
events of probability alpha>0 occur at least once with probability tending to
one as the number of rounds increases. No optional-stopping theorem is silently
imported by the calculus. The evidence mode must supply its own sequential scope.

## 7. Paired expectation without subtracting infinite expectations

The primitive numerical theorem is pointwise. Expected-value uses need their
own measurability and integrability conditions. The appropriate object is often
the PAIRED difference, not two independent absolute cost expectations.

### Proposition U2 — integrable paired consequence

Suppose D=t-s is a measurable real-valued random variable, E[|D|]<infinity,
and D<=b almost surely for a finite deterministic b. Then E[D]<=b.
If a measurable allowance B satisfies D<=B and both are integrable, then
E[D]<=E[B].

**Proof.** B-D is nonnegative and integrable. Its expectation is nonnegative;
linearity for integrable random variables gives the claim. Use B=b for the
first case. ∎

The difference may be integrable while neither absolute cost has a finite
expectation. Let N take values n>=1 with mass 1/(n(n+1)); these masses sum to
one by telescoping. Put old=N+1 and new=N. Both are nonnegative and finite on
every realization. Each mean is infinite because E[N]=sum_(n>=1)1/(n+1).
But new-old=-1 identically and E[new-old]=-1. Writing
E[new]-E[old]=infinity-infinity would be undefined. The calculus can justify
the paired -1 comparison without evaluating that nonexistent subtraction.

A high-probability improvement alone is not an expected improvement for
unbounded losses. If D=-1 with probability 1-epsilon and D=M with probability
epsilon, then E[D]=-1+epsilon+epsilon M. Increasing M defeats any expected
improvement conclusion from epsilon alone. An expected residual magnitude or
a stated tail bound supplies genuinely additional information.

## 8. Reflection: a quantified claim about report-dependent behavior

For a fixed report r in [0,1], let the declared controller select two branches
with weights 1-r and r, and let their failure probabilities be p and s. Its
modeled failure is

    H_r(p,s)=(1-r)p+r s.

A checked proof H_r-r<=0 warrants that numerical self-report for every retained
(p,s). It does not certify every output of an arbitrary self-evaluator, nor
assert that the checker proves its own soundness. r is fixed at the point of
deployment; its policy map may be report-dependent without creating a recursive
cycle in the finite expression evaluator.

A concrete nonempty source is

    0<=p, 0<=s, p+s<=1, s-p<=-1/4.

It contains (p,s)=(1/2,0). For r=3/4,

    H_r = (p+s)/2+(s-p)/4 <= 1/2-1/16=7/16,
    H_r-r <= -5/16.

For r=1/2, H_r-r<=(p+s)/2-1/2<=0. The paired failure-probability change is

    H_(3/4)-H_(1/2)=(s-p)/4<=-1/16.

If the intended-loss discrepancy change is bounded by e<=1/32, then the same
fixed policy change has intended-loss increase <=-1/32. The point (p,s,e)=
(5/8,3/8,1/32) attains both p+s=1 and s-p=-1/4 and the intended-loss bound.
Thus the proof is not a favorable-sample extrapolation or a vacuous source.

Remove the discrepancy premise. The sound numerical statement becomes

    intended_change <= -1/32 + max(e-1/32,0).

At e=0 it still implies improvement. At e=1 it does not. The remaining
self-report bound may hold in both cases. This is the direct link between
assumption uncertainty and modeled loss: an explicit residual keeps track of
what the missing premise costs, without treating its correctness as certain.

## 9. Common expression pairs do not mean common hidden-state actions

For finite observation set O, a deployment policy is fixed separately at each
observed o. Within C_o, the hidden case h must not choose a different action
unless h is observable under that contract. Suppose two policies pi_new(o),
pi_old(o) have a declared expected-loss interpretation t_h(x),s_h(x) under every
retained hidden case. A casewise numerical warrant implies the modeled
policy-comparison warrant only under that interpretation.

A small counterexample makes the condition indispensable. There are two hidden
states with one visible observation, and actions A,B with loss table

    state 0: A=0, B=2,
    state 1: A=2, B=0.

The pointwise numerical minimum is zero in both states. But no fixed action
attains it, and a fixed randomized action choosing A with probability p has
losses 2(1-p) and 2p. Its worst loss is at least 1, attained at p=1/2. A proof
that min(L_A,L_B)=0 is correct numerical reasoning and not a certificate for an
unavailable zero-loss policy. Root-expression matching cannot solve this
interpretation problem by itself.

### 9.1 A constructive encoding of finite case-indexed CPWA costs

K currently requires a common term pair at `all_cases`. This is stricter than
F05's general finite case-indexed interpretation table. There is a useful
semantic adapter that preserves the difference without inventing hidden-state
policy choice. It does NOT assert that the adapter or its coverage certificates
are already implemented.

Fix an old case h with rational polyhedral domain P_h. Let the cost terms
of the SAME two observation-legal programs have finite rational CPWA
interpretations t_h(x),s_h(x). Form a common finite refinement of their affine
cells. On each retained cell j, write

    t_h(x)=a_hj^T x+c_hj,
    s_h(x)=b_hj^T x+d_hj.

Introduce two fresh, correctly typed source coordinates n,o. The lifted case
consists of P_h, that cell's affine guards, and the two graph equalities

    n=a_hj^T x+c_hj,
    o=b_hj^T x+d_hj,

each equality represented by both affine inequality directions. Omit empty
cells only with the declared exclusion evidence; provide a feasible rational
witness for each live lifted cell. Now the same pair `src(n),src(o)` occurs in
every lifted case.

### Proposition U3 — semantic graph-lift equivalence

Assume the listed cells cover each original case and the displayed affine
pieces agree with its two cost terms there. Then

    for all h,x in P_h: t_h(x)-s_h(x)<=b

holds exactly when the common pair n-o<=b holds on every lifted case.

**Proof.** For any original h,x, choose a covering cell j and assign n=t_h(x),
o=s_h(x). The graph equalities hold, so the assignment lifts into that case.
Conversely, any lifted assignment projects to x in its P_h and satisfies the
two exact graph equalities. Hence its n-o is exactly t_h(x)-s_h(x), not a loose
bound or an independently chosen pair. The two universal statements follow
in opposite directions. Overlap of cells is harmless because both affine
representatives equal the original term on the overlap. ∎

This is an interpretation-preserving source adapter, not a completeness proof
for K or an efficient encoding theorem. It may expand the case set. The rows
are definitions of component cost terms and their guards; no desired final
comparison is assumed as a source score. Most importantly, the declared
program pair stays fixed throughout. Replacing each t_h by the cost of the
best action *chosen using h* changes that premise and is not authorized by U3.

### 9.2 Concrete case-indexed example

Let one hidden case have 0<=x<=1 and modeled costs t_0=|x|+1, s_0=|x|+2.
Let a second have -1<=x<=0 and t_1=|x|+3, s_1=|x|+4. These can describe one
fixed pair of programs under two environments with different overheads.
The lifted first case has n=x+1,o=x+2; the second has n=-x+3,o=-x+4.
In either case n-o=-1, with witnesses at x=0 and corresponding output values.
A shared comparison is therefore representable without giving either program
an environment-dependent action choice. The numerical result alone does not
prove the proposed physical overhead model; that remains its source premise.

## 10. A completed proof versus a complete implementation

The native soundness proof needs only the finite operational meaning of each
tag, normalization correctness and acyclic proof references. It does not need
an automatic solver for nonlinear inequalities, a complete method for finding
all proofs, or a guarantee that a heuristic emits a proof at all.

Likewise, a producer's final call to the unchanged checker can establish the
validity of the trace it actually returns. It cannot establish that every
possible input makes the producer terminate, that its chosen claim matches
an external user request, or that its retained proof is the tightest possible
one. These are different program contracts. F07's first-pass result makes
the numerical safety boundary smaller without declaring the entire toolchain
verified.

## 11. Proof-local premises: a stronger deterministic statement

Requiring all rows in C to be actually correct can be stronger than necessary
for one numerical derivation. The relevant premise family can be reconstructed
from that derivation, without claiming that its empirical validity is thereby
known.

### Proposition U4 — local support soundness

Let P be an accepted *local* K trace in case h. Let U(P) be the set of source
rows appearing among the root's reachable ancestors. Ignore other instructions
and rows, while retaining the signature, term meanings and the actual row
expressions in U(P). At every finite real assignment satisfying those used rows,
the root inequality holds, even if that assignment fails an unused row of C.

**Proof.** Perform the same topological induction as S6 on just the root's
ancestor subgraph. The only domain-dependent base cases are `row` leaves;
the current assignment satisfies exactly the leaves needed for this induction.
All other rules are valid pointwise over finite reals. An unused row is not
invoked by any ancestor and is not a hidden side condition in a native tag.
Its failure cannot invalidate this restricted argument. ∎

For instance, a proof of x<=1 using that row alone remains numerically true at
(x,y)=(1,1) even when its original context also contained y<=0. This does not
make an old context fingerprint a current one. A checked use in a revised
context must explicitly transport/reconstruct the proof, or bind an explicit
premise-restricted context to the new request.

### 11.1 Global traces and case localization

A global trace may use several `all_cases` nodes. For one fixed live h, replace
each such node by its h-parent and recursively reconstruct its ancestors in h.
All remaining native budget operations are monotone in parent budgets:
addition, nonnegative scaling/conversion, fixed slack, minimum, maximum, and
`max(p+q,0)`. Constant and row budgets do not change. At a removed union node,
the selected local budget is <= the old maximum.

Induction therefore gives a local trace with the same comparison pair (up to
its checked exact rewrite) and budget b_h<=b_global. Its used-row set U_h(P)
suffices pointwise by U4. The output budget need not equal the former global
budget: it can become strictly tighter. A hidden case index selects which
argument applies in this mathematical proof; it does not choose the deployed
policy.

### 11.2 Do not attach marginal confidence to an adaptively chosen support

If U is a fixed set of source events known before the data, marginal error
bounds alpha_i yield a joint bound sum_(i in U) alpha_i by the union bound.
If the proof support U(D) is chosen after observing D, that same small sum over
the realized support is not automatically justified. The two-bound example in
section 6.1 chooses one bad row at every record: the chosen support has one
row, but its error probability is one rather than the row's marginal 1/2.

A joint validity event for all candidate rows, valid conditional bounds under
the actual selection mechanism, independent validation data, or another proved
selection-aware evidence procedure can supply the missing premise. The calculus
may then exploit a small support without claiming to manufacture its confidence.
There is no independence assumption in U4; its conclusion is deterministic.

### 11.3 Interpretation domains are not mere unit labels

A unit named 'probability' does not establish 0<=p<=1. If a report-dependent
controller uses p,s as branch failure probabilities, those restrictions belong
to the operational interpretation or its retained structural domain. Softening
such rows still gives a valid REAL ARITHMETIC statement, but points outside the
probability range no longer describe that controller under the same semantics.
A separate clipping/error adapter could be investigated, but is not silently
supplied by residual discharge or by a nominal unit name.

The same applies to a task loss's nonnegativity and to an executable action's
observation constraints. Numeric typing, inequality premises and program meaning
are three different obligations. This is compatible with signed values as an
organizing primitive: it avoids obtaining stronger real-world claims by changing
the meaning of the very quantities being compared.

## 12. Strengthening the expectation boundary without hiding undefined arithmetic

The integrability condition in U2 is convenient for an ordinary finite
expectation. A one-sided finite bound supports a somewhat stronger statement.
This is a clarification of the mathematical interpretation, not a new native
expectation rule.

### Proposition U5 — extended paired expectation

Let D be measurable and finite almost surely. If D<=b almost surely for a finite
constant b, then E[D^+]<=max(b,0)<infinity. Consequently its extended expectation

    E[D] := E[D^+] - E[D^-]

is well-defined in [-infinity,infinity) and is <=b. If a *finite* expectation
is required, additionally require E[D^-]<infinity.

More generally, if D<=B and E[B^+]<infinity, both extended expectations are
well-defined and E[D]<=E[B].

**Proof.** D^+<=B^+ and D^->=B^- pointwise. Positive parts therefore have finite
integrals, whereas negative parts may have infinite integrals. Subtracting them
cannot create infinity-infinity because the positive integral is finite.
Monotonicity of the two nonnegative integrals gives the inequality, including
the case where the right-hand expectation is -infinity. Set B=b for the first
statement. ∎

No assertion about E[new]-E[old] has been made. That separate subtraction can
remain undefined even when E[new-old] is finite and exactly known. The repeated
common-cost example old=N+1,new=N in section 7 is therefore legitimate without
asserting that two infinite marginal means can be cancelled arithmetically.

### 12.1 Equal heavy-tailed marginals do not determine a paired expectation

Let N have mass 1/[n(n+1)] at positive integer n. If old and new use the SAME N,
their difference is zero, although both individual means are infinite.
Instead let old=M and new=N, where M,N are independent copies of that law.
Then the positive part of N-M has infinite expectation. Indeed on M=1,
which has probability 1/2, its positive-part expectation contains

    (1/2) sum_(n>=2) (n-1)/[n(n+1)]
    >= (1/4) sum_(n>=2) 1/(n+1) = infinity.

By symmetry its negative part also has infinite expectation. The signed
expectation of N-M is now undefined, NOT zero by symmetry. The two constructions
have identical marginal cost laws but different paired interpretations.

This reinforces the choice of shared-source comparison: pairing is meaningful
information, not an encoding detail. It does not justify subtraction of arbitrary
unbounded expectations, and it does not require imposing a universal value cap.

## 13. Exact coefficient checking is substantive for unbounded sources

An approximate equality test for linear forms is not covered by S2. For any
positive rational epsilon, the premise x<=0 does not entail

    x+epsilon z<=0

when z is unconstrained. At x=0,z=1/epsilon the claimed conclusion fails by 1.
A normalizer that discards coefficients merely because they are smaller than
a floating-point tolerance could therefore accept an invalid argument.
This is true for arbitrarily small nonzero epsilon, with all numbers finite.
The exact checker retains the coefficient and rejects the rewrite.

There is a constructive alternative when an appropriate domain bound is
available. If z<=R and epsilon>=0, then the valid conclusion is

    x+epsilon z<=epsilon R.

For a general affine residual e^T z, one needs a bound on that residual over
the admitted source, not a declaration that e is numerically small. For a
coordinate box l_i<=z_i<=u_i, a certified bound is

    sum_(e_i>=0) e_i u_i + sum_(e_i<0) e_i l_i.

This can be derived by signed scaling of the appropriate source inequalities
and addition. A learned coefficient proposal can use this route after providing
its exact rational residual and source bounds. Neural proximity to a valid
coefficient vector is not itself an exact proof, and the current work does not
claim that the network causally implements that argument.

## 14. Metatheory and self-assessment modesty

The mathematical metatheory used here is ordinary classical real arithmetic,
finite syntax/graph induction, and the explicitly stated probability/integration
assumptions for U1–U5. The result is conditional on those meanings and on the
implemented checker matching the audited operations. It is not a claim of
access to an ultimate metaphysical description, nor a proof that every future
revision must retain this metatheory.

A finite proof graph remains acyclic because the soundness induction needs an
order of premises before conclusions. That does not prohibit report-dependent
behavior in the modeled world: H_r may describe behavior chosen using r, while
a particular r is checked against the explicit equation and uncertainty set.
Proving H_r<=r is a bounded self-assessment. Inferring the correctness of the
entire checker from its own assertion would require a different, unsupported
reflection principle. Neither an unknown proof nor an unknown loss estimator
is made reliable just by giving it a source coordinate or a confidence label.

## 15. Why rational counterexamples are appropriate here, but a finite grid is not

The theorem S6 quantifies over finite REAL assignments. The executable audit
uses exact rational numbers. The following independently reconstructed bridge
explains that choice without treating a finite enumeration as a proof.

### Lemma U6 — rational points are dense in a rational polyhedron

Let P={x:Ax<=b}, with finite rational A,b, and take any real x0 in P. Let I be
the rows tight at x0. Gaussian elimination of A_I x=b_I provides a rational
particular solution p and rational nullspace basis B, so x0=p+B y0 for some
real y0. Choose rational y_n tending to y0 and set q_n=p+B y_n. Each q_n is
rational, satisfies all tight equations, and tends to x0.

For each remaining row the slack at x0 is strictly positive. Since there are
finitely many such rows and their left sides are continuous, all these strict
slacks remain positive at q_n for sufficiently large n. Thus q_n lies in P
eventually. If the tight system has a unique solution, x0 itself is rational.
The empty collection of tight equations simply leaves all coordinates free. ∎

### Corollary U7 — every strict real violation has a rational witness

Every finite term in the selected language is continuous: its constructors
are continuous, and a finite lexical composition preserves continuity. Let
D(x)=E_x(t)-E_x(s). If x0 in a rational case satisfies D(x0)>b, continuity gives
a neighborhood of x0 on which the inequality remains strict. U6 supplies a
rational point of the same case in that neighborhood. ∎

Consequently a false universal comparison in this precise fragment has an
exact rational countermodel. This does not bound its size or put it on a
particular finite test grid. A finite collection of satisfying points remains
finite development evidence. For example, epsilon*z<=1 can hold throughout a
large fixed test box yet fail at z=2/epsilon when z is unrestricted.

Both restrictions are real. If source assumptions allowed x^2=2 and x>0, a
false claim x<=1 would have no rational feasible countermodel. If the loss
could be an arbitrary discontinuous indicator of irrationality, agreement at
every rational point would likewise not establish its values at reals. Neither
example belongs to this source/term fragment. Extending to richer nonlinear
sources or arbitrary learned primitives must revisit the witness argument.

## 16. Finite termination is not a linear-time verification guarantee

The logical proof uses finite induction. It does not imply that the current
Python evaluator handles every compact DAG efficiently. Let t0=x and let
`t_(n+1)=t_n+t_n` share its two child pointers. A DAG representation has only
O(n) distinct nodes, while an evaluator that recursively revisits each child
occurrence may perform O(2^n) work. A semantically trivial comparison t_n=t_n
can still be expensive for a nonmemoizing normalizer.

The original checker is not changed in this pass. Its exact semantics are the
subject of the soundness argument; measured execution limits and performance
belong to the validation record. A timeout is neither a successful check nor a
countermodel. A later memoization repair must preserve the lexical-environment
condition in section 3; caching by syntax-node identity alone is not sound for
open subterms evaluated under different bindings.

## 17. Two probability levels in the reflective use case

A report about failure probability and an error rate for the EVIDENCE supporting
that report are different quantities. They can be related under an explicit
behavioral law, but they are not the same confidence scalar.

### Proposition U8 — evidence error plus a behavioral failure bound

Let D be the current record, let the selected policy have actual conditional
failure probability H_D in [0,1], and let a request-bound checked proof establish
H_D<=r(D) whenever the source-validity event E occurs. Assume 0<=r(D)<=1,
Pr(E^c)<=alpha, and that H_D is genuinely the conditional failure probability
of the policy induced by the report. Then

    Pr[future failure] = E[H_D]
        <= E[r(D)] + E[(1-r(D)) 1_(E^c)]
        <= E[r(D)] + alpha.

**Proof.** On E, use the checked numerical bound. On E^c, use the independent
fact that a probability is at most one. Pointwise,
H_D<=r(D)+(1-r(D))1_(E^c). Take expectations and use the stated conditional-law
interpretation. No independence between D, E and the selected policy is assumed. ∎

For a fixed reported bound r, this sharp worst-case accounting reduces to
r+(1-r)alpha. It is attainable by a model with H=r on E and H=1 outside it.
If the arithmetic proof supplies a tighter uniform probability bound B<r, the
same formula can use B rather than the public report, provided its interpretation
and evidence event are the same.

In the source example of section 8, H_(3/4)<=7/16. At evidence error at most
1/20, the resulting unconditional modeled failure probability is at most

    7/16 + (9/16)(1/20) = 149/320.

This is not a claim that the source error has actually been calibrated. It is
a conditional, constructive bridge showing exactly where that evidence would
enter. The reflected policy may depend on its report; the required conditional
law must describe THAT policy, not a frozen predeployment distribution.

For arbitrary unbounded cost the bound outside E is not automatically one.
A corresponding magnitude or tail assumption is needed, as in section 7.
U8 therefore exploits the natural boundedness of a failure indicator, not a
universal cap imposed on values throughout the calculus.

## 18. A fully finite selection countermodel and its loss-based repair

This example checks the distinction between arithmetic correctness and selected
evidence validity without any infinite values, neural training or external
asymptotics. It also ties the failure directly to the graded theorem.

Let the observed data D be uniform on {1,...,20}, and let the actual scalar cost
change be x=0. For each j define a data-dependent upper-bound procedure

    eta_j(D) = -1 if D=j, and +1 otherwise.

Each individual procedure satisfies Pr(x<=eta_j(D))=19/20. Define a declared
one-row context C_j(D) by x<=eta_j(D), with witness x=eta_j(D). It is nonempty
on every data outcome. The native row proof therefore correctly derives its
upper bound in every such context.

Now select j=D after seeing the data. The selected proof has root x<=-1 on
EVERY outcome. Its trace is a valid derivation, yet its empirical conclusion
fails on EVERY outcome because actual x=0. No contradiction with S6 occurs:
the actual x is outside the selected declared source on every outcome. Neither
finite source satisfiability nor per-procedure 95% coverage gives selected 95%
coverage. The aggregate failure probability is one, equal to the disjoint-event
union bound 20*(1/20), not 1/20.

The loss-based repair is exact here. Withdraw the selected inequality and
replace it by

    x <= -1 + ReLU(x+1).

At actual x=0 its violation loss is one, and the right-hand side is zero.
Thus the repaired proof no longer falsely claims improvement: it exposes
exactly the missing unit. The algebra does not learn that the penalty is one
from the selected data; that equality is part of this independently specified
countermodel. For a real application the penalty or the joint event needs its
own evidence.

This example also rejects a tempting support-count shortcut. The selected proof
uses only ONE row, but that row was selected from twenty data-dependent
procedures. Counting only rows in the final proof cannot recover the marginal
coverage claim. One valid alternative is a simultaneous event over the eligible
procedures; another is an appropriately conditioned or fresh-data procedure.
Neither is produced solely by the exact arithmetic checker.

## 19. What bounded reflection can inherit from this theorem

A proof-producing agent may inspect, revise or predict its own finite numeric
output. Let Q be a versioned procedure that returns either a trace or failure.
For an externally specified request J, define a receiver that accepts only
when K validates the returned trace and its root matches J's context, scope,
terms and required strength. Then every accepted root has the numerical
property S6 establishes, regardless of whether Q used self-prediction, search,
a learned proposal or a hard-coded argument to produce it.

This statement does not assume that Q always returns a proof, that Q knows its
own correctness, or that a proposition about Q's behavior is automatically
true. If Q returns the valid constant proof 0<=0 when J asks for x<=-1, root
binding rejects it. If Q outputs a numerical confidence of one without a
trace, that is not a K derivation. If a trace correctly assumes a favorable
model of Q, its conclusion remains conditional on that model.

The strongest currently justified reflective reading is therefore modular:

    specified report-dependent behavior
      + applicable source/behavior premises
      + a checked argument about that behavior
      -> the particular numerical warrant.

The formal theorem can be applied to an agent that calls the checker. It does
not turn the checker into an unqualified internal truth predicate, erase the
metatheory, or introduce a new rule from "I accept J" to J. Genuine cyclic
source validation remains a distinct semantic obligation, not an unsupported
consequence of finite-DAG proof soundness. These are scope limits of this first
F07 reconstruction, not a permanent prohibition on richer reflection.
## 20. Independent ML-loss interpretation of a multistep argument

To check that the theorem applies to a useful loss comparison rather than only
a reformulation of its own rules, start with an externally specified binary
prediction task. For signed margin m use logistic loss

    ell(m)=log(1+exp(-m)).

Use a fixed loss coordinate (nats, with any resource price explicitly converted
to that coordinate). Let the old margin m_o<=-1 and the new margin m_n>=0.
The old and new uses share an arbitrary finite nonnegative overhead z, with
additional new-use cost 0<=c<=1/8:

    J_old = ell(m_o)+z,
    J_new = ell(m_n)+z+c.

The relevant analytic component bounds follow without consulting a proof trace:

    ell(m_o) >= -m_o,
    ell(m_n) <= log 2 < 3/4.

The first follows from 1+exp(-m_o)>=exp(-m_o) and monotonicity of log. For the
second, exp(-m_n)<=1. A rational upper bound on log 2 is justified because
exp(3/4) >= 1+3/4+(3/4)^2/2 = 65/32 > 2. The exponential inequality uses its
nonnegative Taylor terms at a positive argument; logarithm is increasing.
These are external mathematical component enclosures, not new native K terms.

Subtracting the modeled costs therefore gives

    J_new-J_old
      <= 3/4 + m_o + c
      <= 3/4 - 1 + 1/8
      = -1/8.

The common z cancels exactly. Both costs can be unbounded as z grows; the
comparison does not need a finite bound on z. The intended-cost meaning here
is the explicitly chosen logistic loss plus priced use cost, not a claim that
logistic loss uniquely represents all practical utility.

### Numerical source and proof interface

Let numeric source coordinates L_o,L_n,m_o,c,z have the above meanings, with
unit conversions already fixed. The required source rows are

    -m_o-L_o <= 0,
    L_n <= 3/4,
    m_o <= -1,
    c <= 1/8.

Their sum is L_n-L_o+c<=-1/8. Exact rewriting gives the requested pair
(L_n+z+c) versus (L_o+z), without an input row containing that final comparison.
The source has a rational witness m_o=-1,L_o=1,L_n=0,c=0,z=0. A feasible witness
need not itself be the exact logistic graph: this affine source deliberately
retains only the component enclosures. The actual graph assignments satisfy
those enclosures by the analytic argument above. Thus source nonemptiness,
component interpretation and the combined conclusion have separate witnesses.

A native proof may derive this by four row leaves, three additions and one
rewrite. S6 covers the resulting trace, but the independent analytic argument
shows why the source rows describe this particular modeled task. Neither side
uses the other as a semantic oracle. A purported application with a negative
new margin has lost a premise for L_n<=3/4 and needs a different enclosure;
source hashing and arithmetic acceptance cannot conceal that scope change.

For example, keeping m_o=-1 and taking m_n=-10,c=0 gives new logistic loss
strictly greater than the old one. The old source-row proof remains an algebraic
proof about its old declared source, but does not apply to this changed task.
This is a counterexample to unqualified application, not to S6.
## 21. Conditional branch laws, rather than implicit independence

The reflective interpretation uses H(r)=(1-r)p+r s. Its stochastic justification
must be explicit. Given observed data D, if A is the chosen branch and

    Pr(A=1 | D)=r,
    Pr(failure | D,A=0)=p,
    Pr(failure | D,A=1)=s,

then the formula follows by partitioning the two branch events. No independence
is required when p and s already have these conditional meanings. At a
zero-probability branch, its unused conditional probability can be assigned an
arbitrary admissible representative; its contribution is zero.

However, unconditional potential-branch failure probabilities need not have
those conditional meanings after branch selection. A finite counterexample:
let U be a fair hidden bit, define potential failures Y0=U and Y1=1-U, and
choose branch A=0 when U=1 and A=1 when U=0. Each potential branch has failure
probability 1/2 and each branch is selected with probability 1/2, yet the executed
branch fails with probability one. Inserting the marginal pair (1/2,1/2) into
the mixture formula would incorrectly predict 1/2. Its actual selection-
conditional probabilities are p=s=1, which give the correct value.

An independent random branch coin supplies a positive case: with the same
potential failures, selecting each branch independently with probability 1/2
gives total failure 1/2. More generally, appropriate conditional independence
of the action coin and potential branch outcomes suffices to identify marginal
and selection-conditional branch rates. This is an operational model premise,
not a property of a typed scalar called 'probability'.

Consequently a sound K proof about H(r) applies to the stated report-dependent
program only when its p,s mean the branch laws for THAT deployed policy, or an
explicit causal/independence premise permits their reuse from a different
policy. This is another reason a purely numerical self-report cannot certify
its own evidence model. The counterexample changes the program interpretation,
not the arithmetic validity of the mixture expression.

## 22. Rejection is not semantic refutation

A returned-trace soundness theorem is one-way. A rejected input can be
malformed, use an inadequate rule instance, exceed resources or assert a false
claim. Rejection alone does not determine which case holds.

For a concrete example, min(x,y)-min(y,x)=0 for all real x,y, but the native
opaque-atom normalizer does not equate those two differently ordered min keys.
A purported `constant` instruction for their difference is therefore rejected.
There is nevertheless an ordinary K proof: use min(x,y)<=y and min(x,y)<=x,
then `min_common` to obtain min(x,y)<=min(y,x), with zero budget. The opposite
direction has the symmetric proof. Failure of one normalization shortcut is
not failure of the claim or of all possible derivations.

Similarly, a rational point violating a query inside an affine SOURCE domain
is a countermodel to the source-relative numerical statement. It need not lie
on an independently specified exact program graph contained in that source
abstraction. Refuting a claimed operational application requires respecting
that extra interpretation. Source-relative refutation is still useful: it
shows that the retained premises do not alone justify the requested bound.
A failed proof search, unlike such a point, supplies no semantic countermodel.
## 23. Typed positive maps are not automatically physical identities

F05 explicitly permits both coordinate conversions and valuation bridges in the
positive map table. Soundness uses the declared factor for each map; it does
not assume that two maps with reversed unit names are mutual inverses. For
example factors 2 from U to V and 3 from V to U give a round trip 6x. The
normalizer correctly retains that factor. Calling the round trip an identity
would add an unjustified physical/semantic premise; only reciprocal factors
support the corresponding arithmetic identity.

For a genuine coordinate change, reciprocal factors and consistently transported
source rows, queries and budgets justify reuse. A valuation bridge, such as a
price assigned to a failure or a resource, need not have such an inverse meaning.
Changing that price changes the criterion unless the intended interpretation
supplies a different equivalence. The numerical theorem is no substitute for
specifying which of these roles a conversion plays.

Likewise, "unbounded" in S6 means that no uniform finite cap is imposed on the
source assignments. It does not mean a term may have value +infinity at one
assignment and then be subtracted from itself. The expectation corollaries
permit infinite expectations of finite pointwise costs under their stated
one-sided conditions. A program that incurs literally infinite cost with
positive probability, for example through nontermination under an infinite-
cost convention, needs an additional tagged/extended interpretation. It is not
silently admitted into finite-real arithmetic by the same word 'unbounded'.
## 24. Contradictory hard premises versus a meaningful violation objective

The requirement of a feasible context does not forbid reasoning about the cost
of mutually inconsistent requirements. It forbids treating their empty joint
source as a deployable warrant. For example x<=0 and x>=1 have no common
assignment, but the source-free quantity

    P(x)=ReLU(x)+ReLU(1-x)

is a perfectly meaningful finite loss. For every real x,

    ReLU(x)>=x, ReLU(1-x)>=1-x,
    hence P(x)>=1.

Equality holds for every x in [0,1], including the explicit rational point 1/2.
The system can therefore represent an irreducible total violation without
accepting a contradictory source. Both inequalities used in the proof are
ordinary max/lattice identities and can be assembled under an empty ROW list
inside a nonempty ambient case.

The general finite certificate has the same interpretation. Suppose affine
requirements a_i(x)<=eta_i admit nonnegative rational coefficients lambda_i
such that the variable coefficients in sum_i lambda_i a_i cancel and the
resulting exact constant exceeds sum_i lambda_i eta_i by gamma>0. Then,
without assuming any of the requirements,

    sum_i lambda_i max(a_i(x)-eta_i,0) >= gamma

for every finite assignment. Subtract eta_i from each a_i, bound it by its
positive part, and sum the inequalities; exact cancellation gives gamma on
the left. This is the familiar finite infeasibility-certificate argument viewed
as a lower bound on a modeled violation loss, not a new novelty claim.

The API's graded-discharge transformer requires an originally admitted context;
it cannot be applied to the contradictory hard context above. A new unconditional
proof of the violation objective is a DIFFERENT construction in a satisfiable
ambient context. Distinguishing those routes prevents a source-admission failure
from being disguised as a successful old proof. No arbitrary conclusion or
unqualified truth statement follows from the inconsistent hard requirements.

## 25. Review correction: local source coverage is not union coverage

The first draft of U1 described E as membership in the entire source union
without restricting its accepted request to be global. The native theorem and
receiver also permit local requests, so that wording was too weak and is now
corrected above. The proof itself requires membership in the root's actual
semantic domain. This is a correction to the new draft, not a change to F05/F06.

A two-case witness makes the obligation exact: one case has x=0 and the other
x=1. A local proof in the first case establishes x<=0. The actual assignment
x=1 belongs to the union with probability one, but the local conclusion fails.
Thus union coverage alone cannot justify applying a local result everywhere.
Binding a request to a global root excludes this mistake syntactically; using
a genuine local request instead requires coverage conditional on, or membership
in, its specified domain. The new tests retain both boundaries.

### Final first-pass reconstruction boundary

The real-valued native theorem, the graded/local-substitution corollaries and
the request-domain probability implication are ordinary conditional mathematical
results with separate hypotheses. The correction in section 25 is incorporated
in U1 before validation. No empirical coverage theorem, general program
verification, complete proof-search procedure, independent reviewer or formal
proof-assistant check is asserted. F07's remaining sessions must reconstruct
producer-specific and operational contracts rather than treating the number
of passing finite fixtures as completion of that work.
