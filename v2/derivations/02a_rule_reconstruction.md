# F06 S1 — reconstruction of rules, composition and evidence replay

Status: **partial F06 research**, September 27, 2026 (UTC).
Companion: [rule register](02_inference_rules.md). Semantics: [F05](../foundations/03_provisional_core.md).
All displayed derivations use one versioned, feasible joint source until an
explicit transport is performed. These are mathematical source-model arguments,
not actual-world guarantees without the stated evidence and interpretation.

## 1. Signed budgets are not distances

Let t-s<=b and s-r<=c. Adding yields t-r<=b+c regardless of the signs of b,c.
For t=1,s=3,r=4, budgets -2 and -1 compose to -3. Clipping each difference at
zero would replace every budget by zero and lose the improvement. Conversely,
from t-s<=-1 one cannot infer the reverse s-t<=1: t=0,s=100 is a countermodel.
An upper bound in one direction is not an exact difference or a two-sided error.

Negative scaling is easiest audited by writing the difference explicitly:

    (-s)-(-t)=t-s.

Thus the sound transformed query reverses its arguments. At t=0,s=1,b=0 the
incorrect transformed query -t-(-s)<=0 is false. Adding a common finite baseline
z preserves the difference, while adding it to only the new expression does
not. Using a premise twice adds its arithmetic allowance twice: t=1,s=0,b=1
refutes the proposed rule `2t-2s<=b`.

No grant, confidence or truth degree participates in these calculations. A
negative cycle of same-context bounds, t<=b s and s<=c t with b+c<0, would imply
0<0. In a nonempty context both cannot be semantically valid. This observation
cannot compare different evaluator/criterion versions as though they were the
same t,s; the context checks are part of the rule's applicability.

## 2. Sharpness of lattice and residual propagation

### 2.1 Lattice congruence

Assume a_i-b_i<=d_i for i=1,2 and let d=max(d_1,d_2). Then a_i<=b_i+d, and
monotonicity plus common translation give F(a)<=F(b)+d for F=min,max.
This is also the best universal bound from only the two scalar premises.
Select an index j attaining d. For min choose b_j much smaller than the other
b_i; for max choose it much larger. Take a_i=b_i+d_i. Finite separation of the
b_i ensures j wins in both expressions, and the difference is exactly d.
There is no boundedness requirement on absolute b_i.

If only the first input is changed, d_2=0. An improvement d_1<0 does not imply
that a saturating computation improves. Example: min(2,0)=min(1,0)=0, despite
2 being replaced by 1. The max version uses max(0,-1)=max(0,-2)=0.

### 2.2 Correct residual variance

Let a_old-a_new<=p and b_new-b_old<=q. With y=b_old-a_old,

    b_new-a_new <= y+p+q.

The largest possible change of max(y,0) under an increase at most d=p+q is
max(d,0). For d>=0 choose y sufficiently positive, giving difference d. For
d<0 choose both y and y+d negative, giving zero. These are finite witnesses.
Adding a sufficiently large common offset to all four a/b values makes them
nonnegative without changing either residual, so the boundary is not caused
by allowing signed cost inputs.

Using the first argument's forward bound rather than its reverse fails:
res(1,1)=0 but res(0,1)=1. The first argument has improved by -1, yet the
residual increased. Polarity is mathematical data, not an optional annotation.

### 2.3 Recover strict improvement with a reserve

A stronger local premise can preserve improvement through ReLU saturation.
Suppose y_new-y_old<=-gamma, y_old>=ell, with gamma,ell>=0. The rule trace is:

1. y_new <=[-gamma] y_old, by premise;
2. 0 <=[-ell] y_old, by the lower-bound premise;
3. max(y_new,0) <=[max(-gamma,-ell)] y_old, by common-target maximum;
4. y_old <=[0] max(y_old,0), by lattice introduction;
5. res(0,y_new) <=[-min(gamma,ell)] res(0,y_old), by transitivity.

The result is sharp: choose y_old=ell and y_new=ell-gamma. If gamma<=ell,
both are nonnegative and the difference is -gamma. Otherwise the new ReLU
is zero and the difference is -ell. This is a derived rule, not a new axiom.

For ordinary hinge loss, y=-m where m is the signed prediction margin.
An old negative margin with -m_old>=ell, a margin improvement of at least gamma,
and added use cost at most kappa give

    hinge(m_new)+use_new - hinge(m_old)-use_old
       <= kappa-min(gamma,ell).

For ell=3/4,gamma=1/2,kappa=1/4, improvement is at least 1/4. The interpretation
is for the declared pointwise margins (or an explicitly weighted collection
of such cases), not ReLU applied to an unspecified *mean* margin. No interchange
of expectation and ReLU is licensed. Absolute margins and a shared baseline
may remain unbounded. A trained network exhibiting this rule remains untested.

## 3. Derivation I — compose before forgetting dependence

Source: theta in [0,1], z1,z2>=0. Same old/new plans and additive-stage meaning
as F05, not two independently chosen source parameters:

    old1=z1+3/4, old2=z2+theta,
    new1=z1+theta, new2=z2+1/4.

The direct proof is an exact difference rewrite:

    new1+new2 - (old1+old2)
    = z1+theta+z2+1/4-z1-3/4-z2-theta
    = -1/2.

R0 establishes (-1/2)<=[-1/2]0. R2 rewrites this as the complete comparison.
This result is not loaded as a source row; only component interpretations were
supplied. A feasible point is theta=1/2,z1=z2=0, giving new=3/4, old=5/4.

A deliberately coarser proof also illustrates the rules. theta<=1 gives
new1-old1<=1/4. -theta<=0 gives new2-old2<=1/4. Adding those two bounds yields
+1/2, not -1/2. The coarse proof is sound but loses information by summarizing
before cancellation. New rules must not silently replace a joint expression
with independent extrema and claim that replacement is exact.

Change the model to independent coordinates theta1,theta2 in [0,1]. The
complete difference is theta1-theta2-1/2, and the feasible point (1,0) gives
+1/2. Similar source names and equal marginal ranges do not repair the proof.

## 4. Derivation II — native absolute-error loss plus cost

Source: y>=3/4, 0<=c<=1/4, z>=0. Predictions are old=0 and new=1. Their modeled
absolute errors plus use costs are

    J_old=max(y,-y)+z,
    J_new=max(y-1,1-y)+c+z.

A complete proof without assuming which new-error branch is active:

1. -y<=-3/4 is the normalized source row.
2. Multiply by 2: -2y<=-3/2.
3. Add the exact constant 1: 1-2y<=-1/2.
4. Rewrite: (1-y)<=[-1/2]y.
5. Exact arithmetic gives (y-1)<=[-1]y.
6. Common-target maximum gives max(y-1,1-y)<=[-1/2]y.
7. Lattice introduction gives y<=[0]max(y,-y).
8. Transitivity bounds the new absolute error by the old with budget -1/2.
9. The c row gives c<=[1/4]0; add it, then add the unchanged z.
10. Conclude J_new<=[-1/4]J_old.

The result is attained at y=3/4,c=1/4,z=0. Both cost families are nonnegative
and unbounded as y or z grows. No estimate of an absolute maximum is needed.
The proof uses a named one-unit prediction shift; changing the physical or
loss units must also transform the row constants and budget.

Removing y>=3/4 gives a countermodel y=0,c=1/4,z=0: the new cost is 5/4 and
the old cost is zero. The proof depends on its source condition, not merely
on the fact that absolute error is an ordinary ML loss.

## 5. Derivation III — a reflective report and warranted policy revision

The controller SELF-MIX-v1(r) emits a fixed rational r, uses branch S with
probability r and branch P otherwise. The outcomes are modeled with the same
unknown failure probabilities p,s. Fix kappa=1/4 as S's extra use charge.
The probability model and program version are supplied component semantics.
For fixed rational r, `H_r=(1-r)p+r s` is a native affine term.
It is not an implicit variable-multiplication primitive for an unknown r.

Retain 0<=s<=1/4, p-s=1/2, 0<=p<=1, and a paired discrepancy e<=1/32.
All expectations share the source; z,w may be unbounded common baselines.
Write the directional source rows relevant to these derivations as

    p-s<=eta_plus=1/2,
    s-p<=eta_minus=-1/2,
    s<=eta_s=1/4,
    e<=eta_e=1/32.

The two directions of equality are distinct row uses. The old report r0=1/2
has shortfall

    H_r0-r0 = (p-s)/2+s-1/2.

Scale the plus row by 1/2, add the s row, and add the constant -1/2.
This gives the exact proof budget

    beta_report0 = eta_plus/2+eta_s-1/2 = 0.

For the new report r1=3/4 the same construction gives

    beta_report1 = eta_plus/4+eta_s-3/4 = -3/8.

Each report is therefore a valid upper bound on the behavior it induces, though
the true failure rates remain uncertain. Neither report is trusted because
it was emitted, nor because a prediction loss was minimized.

Proxy cost is L_r=H_r+kappa*r+z. Direct affine rewriting yields

    L_r1-L_r0 = (s-p)/4+1/16.

Read the minus row, multiply by 1/4, and add 1/16. Thus

    beta_proxy=eta_minus/4+1/16=-1/16.

The intended pair has J_r1=L_r1+w+e and J_r0=L_r0+w. The e row and the proxy
bridge establish

    beta_intended=eta_minus/4+1/16+eta_e=-1/32.

All final bounds were built from separate source rows, constants, and rules.
The unknown baselines cancel before evaluation. The reports/policies are the
same across all feasible p,s,e,z,w; there is no hidden-case action choice.

### 5.1 Evidence directions have different consequences

Increase eta_e to 3/64, retaining every source meaning. The same arithmetic
proof gives beta_intended=-1/64; both report proofs are unchanged. Increase
eta_minus to -7/16 instead, keeping eta_e=1/32, and the intended bound is again
-1/64. Doing both gives zero. These are explicit proof recalculations, not an
assumption that a stale fingerprint remains valid.

Increasing eta_plus to 9/16 changes the old report proof to +1/32 while leaving
the paired cost proof unchanged: the two rely on opposite equality directions.
The old exact-report warrant is no longer established; a positive allowance
would be a different declared reporting contract. With the other original rows,
p=9/16,s=0 makes H_(1/2)=9/32<1/2 and is not a witness of invalidity; the relevant
countermodel uses p=13/16,s=1/4, giving H_(1/2)=17/32>1/2. This point satisfies
p<=1 and the weakened plus row while the lower difference row still holds.
The new report's bound remains negative.

The distinction is operational: evidence may cease to warrant one report while
still warranting a particular improvement, or the reverse. Replacing the code
with SELF-MIX-reversed changes the policy interpretation and invalidates reuse
of the old term definitions, even if the report literals are identical.

## 6. Derivation IV — nonlinear component, affine proof

Use F05's proved chord enclosure for q=theta^2. The chosen syntax does not have
a variable-product operator; q is a source coordinate with explicit component
rows. There are four supplied cases, with theta in [a_j,b_j] and

    q <= k_j theta + d_j,
    k_j=a_j+b_j, d_j=-a_j*b_j.

The analytic inclusion of the exact kernel model was proved in F05 using
`(theta-a)(b-theta)>=0`. Here the task is to derive the final comparison from
these component rows. Every case has a rational witness and includes q>=0.
For J_new=q+z and J_old=theta+z, combine the chord row with one endpoint row:

* When k_j<=1, add (1-k_j) times -theta<=-a_j.
* When k_j>=1, add (k_j-1) times theta<=b_j.

The resulting left side is q-theta; all multipliers are nonnegative. The
explicit calculations are:

| interval | k | d | endpoint multiplier and row | final budget |
|---|---:|---:|---|---:|
| [1/4,3/8] | 5/8 | -3/32 | (3/8)(-theta<=-1/4) | -3/16 |
| [3/8,1/2] | 7/8 | -3/16 | (1/8)(-theta<=-3/8) | -15/64 |
| [1/2,5/8] | 9/8 | -5/16 | (1/8)(theta<=5/8) | -15/64 |
| [5/8,3/4] | 11/8 | -15/32 | (3/8)(theta<=3/4) | -3/16 |

R10 takes their maximum, -3/16. R2 adds/cancels the common baseline z. This
certifies the same fixed two-trial policy across all hidden cases. The proof
branches may differ without the executable program learning its hidden case.

If the new expression uses -q, an upper enclosure for q is the wrong premise;
the reverse directed inequality is needed. If a case is omitted, the proof no
longer covers the source. A finer mesh improves component precision, not this
already exact endpoint comparison. No superiority is claimed merely from using
more cases or more lines of proof.

## 7. Derived rule for changed randomized choices

Same-weight mixtures follow from nonnegative scaling and addition. Changing
the weights requires more information. Let p,q be two fixed rational probability
vectors; let old component costs be s_i and new costs t_i, all in one unit.
Choose a reference index 0. Then exact normalization gives

    sum_i q_i t_i - sum_i p_i s_i
    = sum_i q_i(t_i-s_i) + sum_i(q_i-p_i)(s_i-s_0).

The reference baseline cancels because both weights sum to one. If t_i-s_i<=b_i
and ell_i<=s_i-s_0<=u_i, scaling with the correct polarity gives

    B = sum_i q_i b_i
        + sum_{q_i>=p_i}(q_i-p_i)u_i
        + sum_{q_i<p_i}(q_i-p_i)ell_i.

The low-level rule trace uses R5's argument reversal for negative coefficients.
The action tables must be observation-legal and available; this is expected
cost under the declared lotteries, not a pathwise guarantee per random outcome.

A two-action positive case: old costs (z+1,z+1+d), both new costs are lower by
1/4, old weights (1,0), new weights (1/2,1/2), and 0<=d<=1/8. The budget is
-1/4+(1/2)(1/8)=-3/16, despite an unbounded common z. Remove the d upper bound
and take d=100: both components improved but the changed mixture is worse by
49.75. Applying the same-weight rule after changing the weights would be unsound.

## 8. Proof budgets as executable functions of source evidence

A useful derivation should expose more than its last scalar. Fix the source
row *directions* a_i(x), the typed query terms, program meanings, hidden modes,
and observation. Vary only numerical bounds eta_i in a_i(x)<=eta_i, with a
separate feasible witness for every live revised case. Normalize row constants
onto the right before doing this: a row reference must not accidentally freeze
an old right-hand-side literal inside its supposedly unchanged query.

For a fixed proof skeleton pi, calculate a budget expression beta_pi(eta):

| proof construction | budget construction |
|---|---|
| exact constant difference c | c |
| row i | eta_i |
| same-difference rewrite / argument-negation | unchanged |
| weakening by fixed slack k>=0 | budget+k |
| transitivity / addition | sum |
| nonnegative scalar k / declared conversion | k times budget |
| two proofs of the same query | minimum |
| max/min congruence or common-target rule | maximum |
| residual congruence | max(reverse-first + forward-second, 0) |
| exhaustive cases | maximum of case budgets |

This is a finite monotone CPWA expression in the premise bounds, even when its
value is negative. Proof sharing can keep it as a DAG. Bounds in different units
are converted by their declared bridge before addition. The source values x
are not inputs to this budget computation; eta is the visible evidence summary.

The replay justification is local: replace each row instance by the revised
valid row, recompute each arithmetic budget, and recheck the exact same rule
side conditions. Sum, nonnegative scaling, min and max preserve the required
inequalities. Reusing the proof *shape* does not mean reusing its old numerical
conclusion. No optimality or exactness of beta_pi is implied.

For the reflective example, the three derived functions are

    beta_report0 = eta_plus/2 + eta_s - 1/2,
    beta_report1 = eta_plus/4 + eta_s - 3/4,
    beta_intended = eta_minus/4 + 1/16 + eta_e.

These coefficients provide explicit quantitative dependency information. They
say why changing an e-bound affects the intended-loss result but not report
validity, and why the two directions of p-s=1/2 have different roles.

### 8.1 Coherent proof choice and the order of quantifiers

`min` combines proofs valid for the same query in the same case. `max` combines
exhaustive hidden cases. Thus a natural budget has form

    max_h min_{pi valid in h} beta_(h,pi)(eta_h).

There is no rule swapping these operators for free. The scalar inequality
`max min <= min max` can hold under suitable common index sets, but equality
requires additional structure. Requiring one proof coefficient vector in every
case can be unnecessarily conservative; letting the *policy* vary by hidden
case can instead be unjustified. The proof tree fixes which object is allowed
to vary, rather than treating every minimum as an optimization over actions.

### 8.2 Local branch guards are a different kind of dependency

An exact rewrite `min(a,b)=a` based on an old certificate a<=b cannot be
replayed after that certificate's budget becomes positive. Numeric changes to
eta may cross the branch guard. Example: old context x<=0 permits max(x,0)=0;
new context x<=1 contains x=1, where that equation fails. Keeping the old branch
normalization is unsound even though the matrix row direction stayed unchanged.

The first-pass replay contract therefore covers unconditional rules and exact,
source-independent algebraic rewrites only. A guarded rewrite must either keep
a proof of its zero-budget side condition, or expand back into the unconditional
order rules and recalculate a conservative bound. This distinction avoids
mistaking an old active region for a proof valid on a new evidence domain.

A numerical cancellation using a truly shared finite source is unconditional.
A cancellation using an empirical equality is not: its two directional source
premises must remain available at the required budgets. That is a particularly
important difference for loss proxies and dependent neural features.

### 8.3 Smoothness is not needed, but it is not certified by a derivative

For a fixed skeleton, beta_pi is continuous CPWA in eta. Its active affine
coefficient vector can change across min/max boundaries. A gradient at one old
point need not describe a finite revision crossing such a boundary. Re-evaluating
the complete budget expression remains valid. Reusing one global affine
certificate remains valid when its row coefficients continue to certify the
same query, but may cease to be the best available proof.

This is a concrete computational interpretation worth testing in ordinary ReLU
networks: an output could select/combine quantitative arguments rather than
merely encode a truth degree. At present the budget expression is derived from
a mathematical proof; no trained network has been found to implement it.

## 9. Withdrawing evidence: availability is not a truth degree

A row can disappear rather than receive a larger finite eta. The old proof
then has an unavailable premise. There is a conservative constructive way to
reuse some proof structure without calling the missing fact false:

* an available row or unconditional constant proof survives;
* a strictly positive scaling, addition, or transitivity needs its used premises;
* scaling by zero can be replaced by the unconditional proof 0<=0;
* a minimum node for identical queries can keep either surviving proof;
* a case maximum requires every live case, even when one branch disappears.

One can implement this with an internal `unavailable` marker, or calculate
budgets in R union {+infinity} with 0*(+infinity)=0 and then extract a finite
surviving subtree. The marker is NOT a new loss term, finite sequent, or a
license to assert anything. The finite extracted proof must be rechecked under
the revised context. No negative infinity or infinity cancellation is involved.
The procedure is conservative: cancellation or a newly discovered proof might
succeed where this reuse attempt does not.

Example: row 1 says x<=1 and row 2 says x<=2. Two row proofs combined by R6
certify x<=1. Withdraw row 1: the row-2 proof still certifies x<=2. Withdraw
both: there is no remaining finite upper proof from that skeleton. By contrast,
a two-case result with bounds 1 and 2 cannot ignore the second live case when
its proof is withdrawn. Using `min` for cases would fabricate an unsupported
universal conclusion.

This is a proof-reconstruction contract, not automatic empirical validation.
A verifier version or source meaning change is not merely a missing row.
Mapping stable row identifiers to the revised context is itself checked data;
ordinal indices alone do not survive arbitrary insertion/reordering.

## 10. Statistical assumptions must not follow arithmetic multiplicity

The formal inference operates conditionally on source rows. A statistical
application needs a distinct coverage premise. Let E_j be named events under
which the source facts supplied by evidence object j are valid, and suppose
Pr(E_j^c)<=alpha_j. A proof depending on those objects is correct on their
intersection. The union bound gives

    Pr(any used source event fails) <= sum_{distinct j} alpha_j.

Reusing one row twice does not create two independent events and does not
square its failure probability. A single joint certificate for several rows
can supply one E_j; separately calibrated rows need not have joint validity.
Bayesian posterior statements and frequentist coverage claims cannot be mixed
just because both carry a number called confidence.

### 10.1 Selecting the strongest proof can expose selection error

Take N equiprobable data states d=1,...,N and a fixed actual modeled cost x=1.
Procedure i supplies the upper bound eta_i(d)=0 if d=i and eta_i(d)=1 otherwise.
Each individual row x<=eta_i is valid with probability 1-1/N. Their joint
polyhedron is nevertheless x<=0 at every data state, and is nonempty (witness
x=0) while never containing the actual x=1. Taking the smallest of the N
arithmetically valid *conditional* row proofs always returns an invalid
actual-cost bound zero.

There is no contradiction of R6. The missing hypothesis is simultaneous
source coverage. Reusing the individual 1-1/N confidence for the selected result
is the invalid step. The union allowance sum_i(1/N)=1 correctly supplies no
nontrivial bound. A stronger joint coverage theorem would permit adaptive
proof/policy selection without inventing independence.

### 10.2 An accepted-result conditional probability is different again

If a procedure accepts only on its bad event, then all accepted conclusions
can fail even when the unconditional bad-event probability is small. The
bound Pr(accept AND failure)<=alpha does not imply
Pr(failure | accept)<=alpha. A literal finite countermodel uses four equal
outcomes, acceptance only on outcome 1, and failure on that outcome only:
unconditional error is 1/4 and conditional error among accepted outputs is 1.

These examples matter for reflective learning. A source coverage event for the
common unknown p,s can justify many report values simultaneously. Estimating
and selecting separate report-specific bounds needs a selection-aware premise.
Low training loss, self-emission, or finite source feasibility does not provide
that premise. F06 does not introduce a new calibration algorithm.

## 11. A signed bound can be reified as zero shifted shortfall

It is important not to overstate the information lost by clipping. For every
finite rational b and finite terms t,s,

    t-s<=b  iff  res(s+b,t)=0.

This does NOT identify the unshifted shortfall res(s,t) with a signed comparison.
It places the proposed budget in the reference term before clipping. The proof
uses t-s-b<=0, then takes the maximum of that difference and zero; conversely,
t-s-b<=max(t-s-b,0)=0. Hence negative improvement thresholds can be represented
by a zero residual at a shifted reference. The scalar range alone is not the
project's contribution or the reason to prefer its sequent notation.

A rule trace from t<=[b]s adds the exact constant -b, rewrites to
`t-(s+b)<=[0]0`, and uses common-target maximum with `0<=[0]0`. For the reverse,
use `t-(s+b)<=[0]res(s+b,t)`, transitivity with its zero bound, and the constant
b shift. No Boolean truth-detachment or access to a true utility is introduced.

When evidence changes, the reference threshold b of the *question* is fixed.
The recomputed proof budget beta_pi(eta') must still be at most that b to
re-establish the zero-shortfall claim. Moving b along with the answer changes
the question and cannot be called persistence of the old warranted threshold.

The usual residual triangle is also derivable, rather than a separate oracle:

1. z-y<=[0]res(y,z) and y-x<=[0]res(x,y), by max introduction;
2. addition and rewrite give z-x<=[0]res(y,z)+res(x,y);
3. each residual is nonnegative, so zero has the same upper target;
4. common-target maximum gives
   `res(x,z)<=[0]res(x,y)+res(y,z)`.

This is the familiar finite Lawvere-style arithmetic mechanism, now applied
to quantities with explicit loss meanings. It is not claimed as new.

## 12. Changing a criterion is not just changing numerical units

Let delta=(delta_1,...,delta_k) be the shared vector of component cost changes.
An old criterion w certifies w^T delta<=b. A new criterion v satisfies

    v^T delta = w^T delta + (v-w)^T delta.

Only a bound on the second, paired expression permits transfer. Small changes
of positive weights are not sufficient by themselves when component changes
are unbounded. For u>=0, take delta=(u,-u-1). Under w=(1,1), the change is always
-1. Under v=(1+epsilon,1), it is epsilon*u-1, unbounded above for every epsilon>0.
The component losses can all be nonnegative: new=(u,0), old=(0,u+1).

With an explicit bound |delta_i|<=R_i, polarity-aware scaling and addition give
`(v-w)^T delta<=sum_i |v_i-w_i| R_i`. A joint source certificate may improve that
loose bound. Alternatively directly prove the paired discrepancy without any
absolute R_i, as in the shared-baseline examples. None of these premises follows
from the words 'same loss unit'. A genuine positive unit conversion scales both
sides coherently; a changed utility tradeoff changes the criterion.

## 13. Transport must prove inclusion, not merely map a witness

Suppose an old proof holds on A x<=eta and a proposed new source substitution
is x=sigma(x'). A check of sigma at one feasible point is not enough. Each old
row after substitution must hold throughout every covered new case. For old
0<=x<=1, new 0<=x'<=1 and sigma(x')=2x', the new witness x'=0 maps correctly, but
x'=1 maps outside the old domain. Transferring the old x<=1 claim would be false.

A finite positive example maps x=x'/2 for new 0<=x'<=2. The two old rows follow
by nonnegative scaling of the corresponding new rows. Thus the old proof of
x<=1 transfers to x'/2<=1. The loss criterion/program meanings still need their
stated relationship; typed arithmetic inclusion is not empirical identity.

For a changed paired query, a reusable macro is:

    old proof: (t-s) <= b on the old source;
    source map: every new case maps into a covered old case;
    correction: (t'-s') - (t-s)[sigma] <= delta on the new source.

Then exact rewriting and addition derive `(t'-s')<=b+delta`. A common unbounded
drift can cancel inside the correction; separate bounds on t'-t[sigma] and
s[sigma]-s' are sufficient but not necessary. No final comparison may be asserted
merely because someone supplied a map name or a new source version string.

At each step of a finite chain of policy revisions, apply the correct source
map and correction. Signed budgets then add by transitivity for the same
transported criterion. This is a finite conditional statement, not a guarantee
of convergence, permanent current validity, or finality of an open-ended library.

## 14. A proof-local split must not authorize hidden contingency

Native CPWA expressions sometimes need guarded piece selection. An admissible
future rule can split on an affine comparison a<=b versus b<=a: real total order
makes the pair exhaustive, including the tie. At a tie the two values agree.
The children may use different proof coefficients, but must prove the same
fixed-policy comparison. The guard is not an observed fact available to the
policy unless the observation interface already says so.

A generated guard can define an empty subcase even when the original source is
nonempty. A proof of infeasibility is a legitimate way to discharge that *piece*;
it is not a deployment context or a way to prove arbitrary action warrants.
For affine rows A x<=eta, a supplied lambda>=0 with A^T lambda=0 and
lambda^T eta<0 directly certifies emptiness by summation. A surviving piece
requires its feasible witness. Dropping a branch because no witness was found
is not this certificate. The parent must remain nonempty and coverage must hold.

The first executable pass uses supplied live cases and unconditional order
rules; automatic splitting/emptiness discharge is not claimed implemented.
This boundary is deliberate: it gives the subsequent F06 continuation a concrete
proof-language question without quietly changing F05's nonvacuity convention.

## 15. Selecting an available policy is different from a numerical minimum

There is a constructive, observation-respecting selection macro. At a fixed
visible observation, suppose each available fixed program pi_i has a checked
comparison against the SAME baseline pi_0,

    Cost(pi_i)-Cost(pi_0)<=b_i.

The b_i are known rational outputs of supplied proofs, not hidden-state costs.
Choose any deterministic index i* minimizing these b_i. The selected program
has the proved bound b_i* on every retained case. This uses one fixed index at
the observation; it does not require observing which hidden case makes a program
best. Include pi_0 with its identity bound zero only if it remains available.

With per-hidden-case bounds, first take max_h b_(i,h) for each fixed program,
then select an i. The valid guarantee is `min_i max_h b_(i,h)`, not
`max_h min_i b_(i,h)`. Costs (0,2) and (2,0) across two hidden cases make the
latter zero while no fixed deterministic choice attains zero.

### 15.1 Do not omit the cost of performing the selection

If the new wrapper expends additional reasoning/evaluation cost R before running
pi_i*, its modeled cost is R+Cost(pi_i*). A separate upper bound R<=kappa gives
comparison budget kappa+b_i*. Merely including pi_0 in the candidate set does
not make the wrapper non-deteriorating if it still pays this overhead.
For Cost(pi_0)=1, Cost(pi_1)=9/10 and R=1/5, the underlying program improves by
1/10 while the wrapper worsens by 1/10. The arithmetic proof about pi_1 is not
wrong; applying it to a different wrapper without its cost is wrong.

A context may intentionally compare only costs after research has been paid.
Then R is sunk and omitted from BOTH compared future-cost criteria. That is an
explicit task scope, not an automatic property of proof search. This leaves a
useful future metareasoning problem without claiming a new general value-of-
computation theorem here.

### 15.2 Relative error can certify a learned ranking without absolute accuracy

For observable numerical proposals hat_J_i, choose i* minimizing hat_J_i.
Let E_i=J_i-hat_J_i be an unknown discrepancy under one joint source.
A proved paired bound E_i*-E_j<=delta_(i*,j) yields

    J_i*-J_j <= hat_J_i*-hat_J_j+delta_(i*,j).

Taking the maximum over j, including j=i* with zero, gives a regret bound
against the numerical benchmark min_j J_j. That benchmark need not be an
observable action: the selected i* is the executable witness. The rule uses
addition, exact constants and common-target minimum. No accuracy of each
absolute J_i is needed, and no trained proposal supplies its own delta proof.

Example: proposals for A,B are 0 and 1/4. True modeled costs are J_A=z+e and
J_B=z+1/4 with z>=0 and 0<=e<=1/2. A is selected. The paired comparison is
J_A-J_B=e-1/4<=1/4, and comparison to itself is zero, so its regret is at most
1/4, attained at e=1/2. Absolute proposal errors grow without bound with z.
Tightening e<=1/8 proves that A beats B by at least 1/8 and has zero regret.
The source-relative ranking statement is stronger than an assertion of small
absolute prediction error in this example, not a new calibration theorem.

## 16. Mixture arithmetic needs the right conditional-cost model

The equality `H_r=(1-r)p+r s` is an interpretation of the specified controller,
not a theorem from two marginal probabilities alone. Let U be uniform and
r=1/2. Suppose branch P fails exactly when U>=1/2, while branch S fails exactly
when U<1/2; each has marginal failure 1/2. Choosing S when U<1/2 and P otherwise
fails with probability one, not one half. The branch's failure is correlated
with the selector. F05 avoids this by specifying fresh independent outcome
randomness, or equivalently the appropriate conditional branch probabilities.

A precise correction makes the boundary explicit. Let I denote selecting S,
with E[I]=r, and let F_P,F_S be counterfactual branch-failure indicators with
means p,s. Then, by expanding expectations,

    E[I F_S+(1-I)F_P]
     = r s+(1-r)p + Cov(I,F_S)-Cov(I,F_P).

A supplied bound on the covariance difference can be treated as a discrepancy
premise, not guessed away. Sharing an unknown parameter across trials and
conditional independence of fresh random draws are different assumptions.
The native calculus can add a modeled correction term; it does not prove a
stochastic independence assumption merely by summing the costs.

Even for the intended independent-draw controller, an expected-cost improvement
is not a pathwise improvement. Couple old r0=1/2 and new r1=3/4 using the same
selector U and independent failure draw V, with p-s=1/2 and kappa=1/4. On the
selector interval [1/2,3/4), the new program pays the S charge. If V>=p, neither
branch fails and its realized cost is higher by 1/4. On other outcome draws
it can avoid a failure and save 3/4. The expected difference is -1/16, but
some individual trials are worse. The criterion/aggregation scope must travel
with the proof; the unit label alone does not distinguish an expectation from
a per-trial bound.

## 17. Cost severity is needed to lift confidence into expected value

A high-probability comparison and an expected-cost comparison are different
claims. Let Delta be an integrable realized cost difference. Suppose Delta<=b
on an event E, Delta<=M on its complement, and Pr(E^c)<=alpha. For p=Pr(E^c),

    E[Delta] <= (1-p)b+p M <= b+alpha*max(M-b,0).

For the usual M>=b this is (1-alpha)b+alpha M. The expression is sharp using
a two-outcome model and choosing the maximizing allowed p. Without a finite
severity or tail premise, a small alpha does not bound expected loss: b=-1,
alpha=1/100 and M=200 permit expected deterioration 101/100. With M=10 the
same calculation instead guarantees expected improvement 89/100.

A useful alternative premise is an excess-tail bound

    E[(Delta-b)_+ * 1_(E^c)] <= T.

Since Delta<=b+(Delta-b)_+1_(E^c) pointwise, E[Delta]<=b+T. This directly
quantifies the cost of exceptional failures rather than treating their
probability as a utility by itself. These are typed application interfaces:
expectation and coverage premises need their declared stochastic model, and
variable products outside the native CPWA fragment need an explicit adapter.
No new sampling guarantee or treatment of infinite expectations is claimed.

## 18. A proof of how its own budget changes

The replay budget beta_pi(eta) in section 8 is a CPWA function built with
constants, variables, nonnegative scaling, addition, min and max. The same
order rules derive a finite *shock expression* S_pi(delta) satisfying

    beta_pi(eta+delta)-beta_pi(eta) <= S_pi(delta)

for all finite eta,delta, while the proof skeleton's context/guard contract is
unchanged. Construct it recursively:

    S_constant = 0;              S_eta_i = delta_i;
    S_(f+g) = S_f+S_g;           S_(k f) = k S_f for k>=0;
    S_min(f,g) = max(S_f,S_g);    S_max(f,g) = max(S_f,S_g).

The local justification is exactly R4/R5/R7: the parent receives signed child
change bounds, so lattice congruence takes their maximum. No derivative,
activation mask, absolute-value replacement, or assumption delta>=0 is needed.
S can be negative if every permitted branch improves. It is a finite max/plus
expression and hence itself admits the selected arithmetic representation.
This is a scoped recursive lemma for budget expressions, not the outstanding
F07 soundness theorem for the eventual full proof language.

The distinction between beta and S is important. beta computes a new proof's
actual bound from fully given numerical premises. S bounds its change from
partially specified perturbations. Knowing that S<=d is another native
source-relative inference over the perturbation quantities, not a license to
assume d from one observed gradient.

### 18.1 Shared perturbations can cancel

For beta=eta_1+eta_2 and delta=(u,-u), S=u-u=0 even when u is unbounded.
The proof budget is exactly unchanged. Marginal upper bounds on each
perturbation separately would both be infinite and lose this conclusion.
This reuses source-aware cancellation at the level of the reasoner's own
numerical evidence sensitivity.

### 18.2 Structural shocks can still be very loose

For beta=min(eta_1,eta_2), old eta=(1,2) and delta=(u,-u), the structural shock
is |u| and has no finite uniform bound over u in R. Nevertheless

    beta(eta+delta) = min(1+u,2-u) <= 3/2,

with equality at u=1/2. The actual budget deterioration is at most 1/2.
There is a short alternative proof: min(a,b)<=a and min(a,b)<=b; add the
inequalities, scale by 1/2, and rewrite to

    min(a,b) <= (a+b)/2.

The correlated sum a+b=3 then supplies the uniform bound. Equivalently, for
the joint source x-u<=1 and x+u<=2, half of each row proves x<=3/2 directly.
A point (x,u)=(3/2,1/2) proves sharpness. Thus failure of one replay/shock
certificate is not failure of the query. A richer retained relation can permit
a short repair rather than a full re-evaluation of the underlying program.

### 18.3 Finite mixtures of proof bounds

More generally, for fixed nonnegative weights summing to one,

    min_i t_i <= sum_i w_i t_i <= max_i t_i.

Multiply the relevant lattice projection inequalities by w_i and add. This
mixes numerical arguments, not executable actions or empirical confidence.
All used inequalities must hold together. If only one of several evidence
objects is reliable in an unknown case, averaging them is not justified;
case-wise proofs followed by a maximum are required instead.

### 18.4 Typed approximation reserve for a threshold

If an old proof has budget b and the permitted new budget is T, the available
reserve is T-b. A separate proof S_pi(delta)<=T-b preserves that threshold.
For a strict-improvement threshold T<0, this can survive nonzero source changes.
But changing the policy, evaluator version, branch partition or a guarded
rewrite requires its own compatibility checks, not only a numerical reserve.
This gives an operationally useful, modest self-assessment: a finite derivation
can expose conditions under which its own numerical conclusion remains usable.
It does not prove that those conditions will hold in every future inquiry.

## 19. What replay does not follow from the old final number

Replaying a proof rebuilds its premises and steps under the new context. It is
not the unrestricted rule 'old bound b implies new bound b'. Consider source
rows x<=1, y<=1, x<=y. One old proof of x<=1 uses the first row; another uses
x<=y and y<=1. If the first row changes to x<=10, those proof shapes yield
10 and 1 respectively. Their old final scalars were identical, while their
numerical dependency information differed. The smaller old number alone does
not say which reconstruction or repair is valid.

The current proof language distinguishes three situations:

1. **restriction:** old source premises are still consequences of the new source;
2. **replay:** new numerical premises support the same unconditional proof shape,
   with its bound recalculated;
3. **repair:** some old step no longer applies, so a new proof obligation or
   alternative proof is required.

All require a live, feasible new context. Starting with 0<=x<=1, a revision to
x<=0 and -x<=-1 is inconsistent. Adding its two rows would give 0<=-1 as a
conditional consequence of an empty domain, but no feasible witness passes
F05's deployment-context guard. This is inconsistent evidence, not a miraculous
improvement or a finite value of truth.

## 20. Changing source coefficients needs a residual proof

Right-hand-side replay is intentionally restricted to fixed row directions.
Suppose a stored linear proof has lambda>=0, A^T lambda=v, and derives
v^T x+c<=lambda^T eta+c. With new rows A' x<=eta', exact arithmetic yields

    v^T x+c = lambda^T A' x+c + (v-A'^T lambda)^T x.

A new-context proof of the residual query

    (v-A'^T lambda)^T x <= delta

therefore gives the repaired bound lambda^T eta'+c+delta. All quantities are
expressed in the same declared units, with named conversions where required.
This is a nonnegative row combination plus another ordinary inference, not an
unqualified inverse-matrix or derivative claim.

An arbitrarily small coefficient change can matter for unbounded sources.
Old row x<=1 certifies x<=1. New row x+epsilon*y<=1, with epsilon>0 and y
unrestricted, permits x=1+epsilon*M,y=-M for arbitrary M. No finite upper bound
on x follows. Keeping the old right-hand side is unsound. Add |y|<=R and the
residual -epsilon*y<=epsilon*R repairs the result to 1+epsilon*R; equality is
attained at y=-R, x=1+epsilon*R.

The new result remains a modeled comparison, not proof that the changed
coefficient describes the world correctly. A change of row meaning or program
version additionally needs its scope/interpretation bridge. Reusing the scalar
budget or a hash of only eta is insufficient.

## 21. A typed transcript of the reflective example

To remove a possible unit ambiguity, use three units: P for failure probability,
L for proxy loss, and J for intended cost. Declare positive conversions
`failure_cost:P->L` and `proxy_value:L->J`, both with numerical factor one.
Sources p,s have P; z has L; e,w have J. The constants kappa=1/4 L and the
rational report parameter r are different types of object. Define

    H_r=(1-r)p+r s : P,
    L_r=failure_cost(H_r)+(r/4)_L+z : L,
    J_old=proxy_value(L_(1/2))+w : J,
    J_new=proxy_value(L_(3/4))+w+e : J.

The probability row s-p<=(-1/2)_P is scaled by 1/4, then converted to L,
then combined with the exact (1/16)_L charge difference. Only then is the
proxy comparison converted to J and combined with e<=(1/32)_J. The final
budget is (-1/32)_J. Report-validity proofs remain in P and cannot simply
be added to that cost budget.

Changing `proxy_value` to factor 1/4 changes the intended comparison: the
same worst-case proxy bound -1/16 contributes -1/64 J, while e can contribute
+1/32 J, giving +1/64 J. It is a new interpretation/criterion record and must
not inherit the old negative intended-cost bound. Merely calling both outputs
'numerical value' would hide a sign reversal that the typed rule trace exposes.

For the old report r=1/2, weakening only the upper p-s bound to 9/16 permits
the feasible point p=13/16,s=1/4. The resulting failure is 17/32, exceeding the
reported 1/2 by 1/32. The lower difference row s-p<=-1/2 still holds. This
rechecks why report and improvement proofs read different directions, rather
than treating equality as an unversioned rewrite.

## 22. Compositional inference need not know complete component costs

The exact functions in section 3 are not required. Source-indexed *allowances*
can remain symbolic until after composition. F05 already permits expressing
`t-s<=e(x)` as the ordinary zero-budget comparison `t<=[0]s+e`; no new budget
sort or hidden evaluator is needed.

Suppose separately supplied component relations establish

    N1-O1 <= theta-3/4,
    N2-O2 <= 1/4-theta.

The costs N1,O1,N2,O2 may be opaque source quantities rather than fully given
functions. These are local component contracts, not a source row containing
the final composite score. Addition derives

    N1+N2 <=[0] O1+O2 + (theta-3/4)+(1/4-theta).

Exact normalization cancels theta, giving a composite improvement of at least
1/2. Equivalently the normalized source rows are

    N1-O1-theta<=-3/4,
    N2-O2+theta<=1/4.

Add the two rows and rewrite. A nonnegative-cost feasible witness is
O1=O2=1,N1=N2=3/4,theta=1/2, attaining the -1/2 bound. Unknown common baselines
can be added to each old/new pair. Even the [0,1] bound on theta is unnecessary
for this joint deduction; it is only needed to compare with the loose separate
scalar bounds. Thus the calculus can compose partial relational evidence, not
only re-evaluate fully known model expressions.

Breaking the shared source gives a sharp countermodel. Replace theta by theta1
in the first row and theta2 in the second, each in [0,1]. At theta1=1,theta2=0,
O1=O2=1,N1=N2=5/4 both local rows hold, but the composite is worse by 1/2.
No source-name convention can supply the missing relation theta1=theta2.

This is the primary operational composition example for the first rule pass.
It follows from existing linear arithmetic, but is precisely the information
contract needed by the proposed source-aware loss calculus. Ordinary component
grants or separate scalar extrema would not supply the same deduction.

## 23. Quantitative failure of joint requirements

The rules can establish a positive obstruction, not merely fail to find a
warrant. Suppose normalized cost coordinates c1,c2 satisfy c1+c2>=3, while
both target tolerances are one. Put u=c1-1 and v=c2-1. Then u+v>=1.
Lattice introduction gives u<=max(u,v) and v<=max(u,v); adding and scaling by
1/2 yields `(u+v)/2<=max(u,v)`. Hence

    max(res(1,c1),res(1,c2)) >= 1/2.

At least half a unit of uniform tolerance relaxation is necessary in every
modeled possibility for this fixed candidate. Equality is realized by
c1=c2=3/2. This is a lower bound on unavoidable shortfall, not a proof that the
agent can choose that favorable possibility or that no future candidate exists.
The required source inequality is what distinguishes this conclusion from an
absence of evidence about the individual constraints.

For fixed nonnegative weights summing to one, the same argument gives

    max_i res(epsilon_i,c_i)
       >= max(sum_i w_i c_i - sum_i w_i epsilon_i, 0).

One may substitute a proved lower bound on the weighted cost. A probability
interpretation is unnecessary: these weights form a numerical convex combination.
Different physical units need a prior explicit normalization/valuation bridge.
This does not silently replace the selected scalar judgment with phase one's
status algebra; it is a quantitative conclusion that a later interface may use.

## 24. Same-pass correction: a weakening guard cannot be silently frozen

The broad phrase 'same proof shape' needs one further qualification. R3 permits
weakening b to a fixed target d only when b<=d. If a revised leaf raises b above
d, retaining the same literal d is not a valid replay. For example an old x<=1
proof weakened to x<=2 cannot survive a revised only row x<=3 by keeping its
old target 2. The feasible point x=3 refutes that step.

There are two correct representations:

* retain the fixed target d and recheck the side condition b_new<=d; or
* store an explicit nonnegative slack k=d-b_old, and replay as b_new+k.

The unconditional budget-expression construction uses the second convention.
Its extra budget rule is `beta_weaken = beta_parent+k`, k>=0 fixed. A comparison
against a hard threshold remains an external checked inequality. The same
caution applies to a residual equivalence that assumes a nonnegative budget:
unconditional clipping recomputes max(b,0), while an unchanged-b rewrite must
recheck its sign condition. Guarded min/max branch selection was already
excluded in section 8.2.

This is a clarification of the first-pass replay contract discovered during
fresh reconstruction, not a change to historical F05 semantics. The negative
examples are retained for the executable audit. New code must not implement
fixed-target weakening as an unconditional constant budget function.

A zero-scaled missing-premise branch can be replaced by an identity proof only
when its terms remain well typed under the unchanged signature. Deleting a
source key or changing a program interpretation is not mere withdrawal of a
row. Undefined terms do not become meaningful because multiplied by zero.

## 25. Proof selection does not inherit outcome stability

Continuity of a proof-budget function does not imply continuity of the chosen
program's actual cost. Take actual costs J_A=0,J_B=1/2 and valid upper proposals
b_A=1+eta,b_B=1-eta, for eta in [-1/4,1/4]. The minimum bound is 1-|eta|.
Negative eta selects A, positive eta selects B. Moving from -epsilon to
2 epsilon, with 0<epsilon<=1/8, improves the selected upper bound from
1-epsilon to 1-2 epsilon while increasing actual cost from zero to one half.
All upper bounds remain valid. Their improvement was not a bound on the
paired cost change of the selected policies.

A relative-policy selection against the current program avoids that invalid
inference when each candidate has a DIRECT paired certificate and the unchanged
baseline remains available with bound zero. Any selected nonpositive paired
bound then actually asserts non-deterioration throughout the stated source.
Reasoning overhead and changed context/source coverage remain explicit premises.

Relative comparison can also work when all absolute upper bounds are infinite.
For z>=0 unbounded and costs J_0=z+1,J_A=z+1/10,J_B=z+1/5, the paired bounds
are -9/10 and -4/5. The source-aware arithmetic chooses a certified improvement
without needing to estimate the common baseline. This is not a proof of an
absolute adequacy limit, a uniquely correct utility, or an unlimited library's
best possible policy.

## 26. Fresh reconstruction of coefficient evidence as an actual derivation

Let the fixed, nonempty source supply affine rows a_i(x)<=eta_i, with all row
expressions already in the query unit through explicit conversions. Suppose a
finite rational vector lambda is nonnegative and exact algebra establishes

    t-s = c + sum_i lambda_i a_i.

This gives a finite derivation, not just a semantic optimization claim:

1. R1 introduces each a_i <=[eta_i] 0.
2. R5 multiplies its comparison and budget by lambda_i. A zero weight may be
   omitted, provided the entire final query is still well typed.
3. Repeated R4 adds the surviving comparisons.
4. R0 introduces the constant comparison c <=[c] 0; add it.
5. R2 rewrites the difference to t-s.

The resulting budget is c+sum_i lambda_i eta_i. No optimization oracle is used;
choosing useful lambda is a separate search problem. A proof that lambda is
optimal, or that every valid query has such a representation, is not required
for this inference. Those are different theorem or algorithmic obligations.

The shared-component example in section 22 uses lambda=(1,1), c=0. Its proof
uses the two contracts even though theta disappears from the final bound. If
the first contract's theta changes meaning or is renamed independently, the
coefficient identity fails. The budget's apparent lack of sensitivity to theta
is therefore NOT authority to erase the contracts' source-alignment obligation.
An exact coefficient identity is also not replaceable by a floating-point
near-equality on unbounded source coordinates: residual r^T x can be unbounded
for arbitrarily small nonzero r. Section 20 gives the explicit correction rule.

Finite rational certificates can be verified with rational arithmetic. This
does not turn all modeled real values into rationals; it checks an algebraic
identity valid for every finite real assignment. Nor does certificate checking
establish that the empirical rows hold in the world. It is an explicit finite
instance of the conditional linear reasoning already identified in F03/F04.

## 27. A sharper local replay bound retains old proof gaps

The homogeneous structural shock in section 18 discards the old distances
between alternative proof values. A useful refinement keeps those distances.
Let old child values be a_i and suppose current certificates establish
new child_i <= a_i+d_i. For F equal to min or max, monotonicity gives

    F(new children)-F(a) <= F(a+d)-F(a).

Write m=F(a), so the right side is respectively

    min_i ((a_i-m)+d_i),   or   max_i ((a_i-m)+d_i).

These are again ordinary min/plus expressions. For a minimum, the gaps a_i-m
are nonnegative; a once-weaker proof can become the useful one after revision.
For a maximum, the gaps are nonpositive, but all required cases must still be
covered. If only componentwise upper shock bounds are known, both expressions
are sharp at a single such node: setting each new child to its allowed upper
value attains them. Shared constraints may improve the result further.

Example: the old bounds on the SAME x are 1 and 2. Their minimum is 1. Revised
leaf increases are at most 10 and -1/2. The gap-aware result is

    min(0+10,1-1/2)=1/2,

so the new proof bound is at most 3/2. The coarser maximum-shock rule would
allow an increase of 10. This is proof selection, not an assumption about which
hidden state occurs. Dropping the first proof can still leave the second bound;
dropping a hidden case cannot be handled in that fashion.

The old values are not assumed to remain valid as bounds for the new source.
They are constants used to express a proved change allowance d_i. Without those
new allowances, remembering that a proof used to be strong gives no warrant.
This refinement is a mathematical interface only in this first pass; the audit
checker replays exact rational leaf bounds and does not implement a source-event
monitor or learned uncertainty estimator.

## 28. Interpretation versus proof program: the remaining obligations

Three kinds of finite object remain deliberately distinct:

    modeled expression: a cost or signed cost difference;
    proof: a conditional argument about that expression;
    budget expression: how that particular argument uses row bounds.

The proof's budget is a finite CPWA function of numeric evidence bounds for a
fixed schema. It is monotone in those bounds: constants are unchanged; row
leaves increase with their own bound; nonnegative scaling, addition, minimum
and maximum preserve order. It need not be positively homogeneous because
constant offsets and nonnegative weakening slack are part of the language.
It need not be concave because the schema includes case and order maxima.
Thus F04's more specialized concave certificate-portfolio characterization is
not applied to every proof-budget computation.

Semantic judgments remain meaningful whether or not this small proof language
can derive them. A rejected proof can indicate a missing rule, an inefficient
search, an unsupported premise, a changed source, or a false conclusion. The
proof checker must report only its actual check outcome. A separate feasible
countermodel is needed to refute semantic validity.

The reflected policy is a finite versioned operational object outside the
proof DAG. It can affect the probabilities named by the modeled expression,
but cannot cite this proof's acceptance as a premise establishing its own
empirical soundness. The displayed fixed-report H_r is fully interpreted;
there is no new arbitrary self-reference evaluator or fixed-point oracle.

The first pass deliberately leaves general proof search, derived case splitting,
source-map proof checking and loss-estimator coverage algorithms unimplemented.
Their mathematical obligations have been stated so that later work cannot
silently treat them as already supplied. F06 remains a rule-development task;
F07 must independently review the final selected rules and their closure under
all actually implemented proof constructors.

## 29. Compositional replacement inside an arithmetic consumer

The primitive comparison rules yield a structural replacement procedure for a
finite arithmetic consumer K with a named hole. Suppose

    t <=[b] s,       s <=[a] t.

Carry TWO directed budgets (U,V) for the difference between K(t) and K(s),
not an unsigned error made by discarding b's sign. At the hole use (b,a), and
at a genuinely unchanged leaf use (0,0). Addition adds corresponding budgets.
A nonnegative scale multiplies both; a negative scale swaps them and multiplies
by its magnitude. Minimum and maximum take the maximum of the respective child
budgets. For res(first,second), use

    U=max(V_first+U_second,0),
    V=max(U_first+V_second,0).

Every stage is a named primitive inference. This is a construction of a finite
proof, not a claim that the propagated bound is optimal. Let bindings are
expanded with capture-free lexical scope; a repeated source stays shared.
When only one directed premise is available, consumers that require the missing
direction cannot use this procedure without obtaining additional evidence.

Exact algebraic rewriting can substantially sharpen the structural result.
For K(x)=x-x, naive interval propagation permits b+a, although the exact
expression is identically zero and R0 proves the zero bound. These two proofs
may coexist; R6 selects their smaller bound. The structural method is conservative
and does not convert dependency loss into a false impossibility statement.

A consumer can also AMPLIFY a strict improvement. For

    K(x)=2x+res(0,x),

one directed comparison t-s<=b suffices. Scaling gives the first contribution
2b. Residual congruence gives max(b,0) for the second. Addition therefore yields

    K(t)-K(s) <= 2b+max(b,0).

At b=-1/4 the derived guarantee is -1/2; at b=1/4 it is 3/4. Both are sharp:
choose t,s negative in the first case and positive in the second. Absolute
values need not be bounded. In contrast, for K(x)=res(0,x) alone, an improvement
of one can become zero when both inputs are negative. It would be unsound to
use the positive-side slope as a universal signed improvement multiplier.

The familiar geometric explanation is that K has slopes between two and three:
for a monotone scalar map whose slopes lie in [m,L] over every relevant segment,
the signed modulus is L*max(b,0)-m*max(-b,0). A nonnegative b uses the upper
slope; a negative b needs the LOWER slope. The displayed K example requires no
new slope axiom because the elementary rules emit its proof directly. Importing
such a modulus for a separately supplied neural consumer needs a certificate
covering its entire relevant domain, not a derivative at one sample.

This example explains what 'composition' means for the chosen syntax. It is
more than arithmetic on final evaluated scores: a proved input relation is
propagated through a specified consumer, with polarity and saturation handled
explicitly. The consumer's real-world cost interpretation is still a separate
model premise, not a consequence of its expression being well typed.

## 30. A common randomized action can exploit cases without observing them

Here is a second composition proof starting from partial contracts. In hidden
case h1, the source says A-B0<=-2 and B-B0<=0. In h2, it says A-B0<=0 and
B-B0<=-2. The same three source meanings and the same unit are used throughout.
Each case is feasible: choose B0=2 and (A,B)=(0,2) or (2,0), respectively.

Deploy the single policy that chooses A or B with probability 1/2, using fresh
randomness. Its declared expected cost is (A+B)/2. In EACH case separately,
scale both component contracts by 1/2, add them, and rewrite the repeated
baseline B0/2+B0/2 to B0. Both case proofs give

    (A+B)/2 <=[-1] B0.

R10 then gives that same -1 bound for the hidden union. No policy sees h.
By contrast, first maximizing the individual A and B budgets over hidden cases
gives zero for each. Their subsequent mixture certifies only zero. The stronger
proof composes before eliminating the shared case information.

The pointwise numerical minimum min(A,B) is zero in these feasible examples,
but no unobserving deterministic choice achieves it in both cases. Randomizing
with probability q yields expected costs 2(1-q) and 2q, so the worst case is
at least one and is exactly one at q=1/2. The -1 improvement from baseline two
is therefore sharp for all fixed randomized policies in this example.

Randomization weights sum to one and are nonnegative; the expected-cost
interpretation assumes the action selection does not condition unaccountably
on branch outcome noise. Arithmetic R4/R5 alone cannot establish that operational
premise. The example stays inside the existing finite-policy interpretation,
not a new probabilistic inference primitive or an oracle action rule.

## 31. Updating a report without demanding the old report remain valid

A useful report-transfer proof needs an upper comparison, not a Boolean
'valid' label. Suppose the current source justifies

    H(r0)-r0 <= a0,
    H(r1)-H(r0) <= d.

Adding those comparisons and the exact constant r0-r1 gives

    H(r1)-r1 <= a0+d+r0-r1.

A nonpositive result supports the new exact report; a result at most xi supports
the explicitly slackened contract. The number a0 may itself be positive. Thus
an old report that no longer qualifies as valid can still carry quantitatively
useful information for proving a new report. Discarding all its numerical
content upon loss of a 'valid' label would destroy that inference.

For SELF-MIX with r0=1/2,r1=3/4, retain the revised rows

    p-s <= 9/16,    s-p <= -1/2,    s <= 1/4.

The old report proof yields a0=1/32. The report-induced failure change has
bound d=(1/4)(-1/2)=-1/8. Therefore transfer yields

    H(3/4)-3/4 <= 1/32-1/8-1/4 = -11/32.

It succeeds even though the old report's uniform exact-validity claim fails.
Direct reconstruction is slightly better: H(3/4)=s+(p-s)/4 gives budget

    1/4+(1/4)(9/16)-3/4 = -23/64.

R6 can retain the stronger direct result without invalidating the weaker
transport proof. Both computations are nonvacuous; p=13/16,s=1/4 realizes
the direct bound and makes the old report fail by 1/32. This is useful revision
rather than blind preservation or wholesale discarding of an old assessment.

More generally, H(r)=(1-r)p+r s with p,s in [0,1] satisfies
H(r1)-H(r0)<=(r1-r0) when r1>=r0. The preceding transfer therefore proves that
increasing a valid report preserves validity on a fixed source. It need not
improve actual failure or intended cost. The weaker necessary operational
question remains separate: what loss does the policy chosen by that report incur?

## 32. Two elementary proof routes recover a sharp self-report bound

For a known rational report r in [0,1], let the source say

    0<=p<=1,  0<=s<=b,  p-s<=a,

with 0<=b<=1 and a+b>=0. The last condition ensures the simple maximizing
witness below is feasible; it is not inferred from arbitrary malformed inputs.
For the fixed report-dependent failure H_r=(1-r)p+r s, two proofs give

    H_r <= (1-r)a+b,
    H_r <= (1-r)+r b.

The first scales the gap row and adds the s row after rewriting
H_r=s+(1-r)(p-s). The second scales p<=1 and s<=b and adds. R6 combines them:

    H_r <= min((1-r)a+b, (1-r)+r b).

This bound is sharp on the stated source: s=b and p=min(1,a+b) satisfy all
constraints, and H_r at that point equals the displayed minimum. The proof
calculus did not receive this final minimum as a source row. It constructs
both arguments and then chooses the stronger one; the feasible witness is a
separate demonstration of tightness in this small example.

For a=b=9/10, the gap-only proof requires r>=18/19 to certify H_r<=r. The
second proof permits r>=10/11. At r=10/11 the exact bound equals r, so that
report is valid, while the gap-only budget remains positive. Both reports are
rational, both branches can fail, and neither calculation assumes access to
the unknown actual p,s. This is a concrete gain from retaining alternative
proofs rather than committing to one compressed statistic.

When a=-1,b=1, the source forces p=0,s=1 and H_r=r; every r is exact. An
implementation must not divide by 1+a without a nonzero-denominator check.
The inference rules themselves use no division or fixed-point primitive: the
candidate r is chosen outside the checker and its stated bound is checked.
Choosing a new r changes the query coefficients; it calls for a new instance
of this proof schema, not an unchanged-query right-hand-side replay.

Known rational parameters and hidden sources therefore have different roles.
Variable report multiplication in an unobserved general model is not silently
added to the CPWA language. This finite family illustrates useful parameterized
reflection while preserving the chosen operational and arithmetic boundaries.

## 33. A limited numerical reflection on the bound calculator itself

The proof-budget program can be an object of further loss-language reasoning,
without asserting unrestricted proof reflection. Fix a versioned calculator
that receives two applicable proof bounds eta1,eta2 for the SAME cost difference
x and emits B=min(eta1,eta2). Its numerical behavior has an explicit finite
interpretation. Suppose the allowed future numeric inputs are

    eta1=-3/4+u,    eta2=-1/4-u,

where u is not bounded. Reify the calculator's emitted quantity as the native
term B(u)=min(-3/4+u,-1/4-u). Lattice projection gives B<=eta1 and B<=eta2.
Adding, dividing by the fixed rational two, and cancelling the shared u proves

    B(u) <= -1/2.

The result is sharp at u=1/4. Thus the agent can reason that this specified
future calculator will keep emitting a half-unit improvement bound throughout
a declared family of input changes, even though either individual input can
become arbitrarily weak. It need not guess which proof will be selected.

There are TWO different conclusions here. The displayed algebra proves what
number the calculator emits. Connecting that number to x also needs the current
applicability and validity of both proof inputs and the fixed source meaning.
That connection does not follow because the calculator says its answer is good.
At u=0, dropping the first source premise but continuing to take the two-number
minimum still emits -3/4. The feasible x=-3/10 satisfies the surviving row
x<=-1/4 but violates the emitted bound. A correct withdrawal-aware calculator
must change its applicability state and its proof, not merely its numerical
confidence. The fixed algebraic description alone cannot certify this change.

This is a small, versioned self-model of a reasoning procedure that can inform
its future reuse decision. It is related to phase one's stratified assessment,
not a new universal reflection theorem or evidence of spontaneous neural
metareasoning. F07 still owes the final kernel's soundness review. The distinction
between numerical self-prediction and warranted emitted conclusions is part of
this example's interpretation, not a reason to exclude self-models entirely.

## 34. Closing reconstruction: what the composition rows must describe

In the partial-contract derivation, N1,N2 and O1,O2 denote the costs in the
ACTUAL compared composite uses. A bound for a component run in isolation is
not automatically a bound for the component under inputs or distributions
changed by its predecessor. That is an interpretation/scope obligation before
R4 is applied, not an independence premise that adding numbers could supply.
Similarly, K(t) in section 29 is a specified cost consumer, not an arbitrary
program whose output error is assumed to have the same units as the task loss.

The final rule audit therefore retains these checks: one finite interpretation
per shared key; a nonempty source; the named cost aggregator; exact units and
valuation bridges; policy information fixed across hidden cases; current row
applicability; and the direction of each approximation. No stronger theorem is
inferred merely because the numerical final budgets agree in a few examples.
The countermodels above identify which failed claims require another premise
rather than more confidence in the same proof.

### 34.1 Lexical scope is also a premise of exact normalization

Opaque min/max/res atoms must retain their fully instantiated lexical
arguments. The terms `let y=x in min(y,0)` and
`let y=x+1 in min(y,0)` are not the same atom merely because their bodies have
the same printed local name. At x=-1 their values are -1 and 0. Erasing the
binding environment would falsely prove a zero difference.

A sufficient normalization discipline first expands nonrecursive lets by
capture-free substitution (interpreting the right-hand side in the outer
environment), preserves source identities and conversion factors, and then
collects linear combinations of fully instantiated atoms. Nested shadowing and
unused ill-typed children need explicit checks. This is a finite syntactic
proof of the rewrites it accepts, not a general identity solver for CPWA terms.
It is the same lexical distinction needed by F05's point evaluator, reconstructed
here at the separate proof interface.
