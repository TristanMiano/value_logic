# F04 — Hostile examples and candidate discrimination

First pass, 2026-09-25 (America/Los_Angeles; observed UTC 2026-09-26).
Base: `6a9cc9993261187aa14af5bc6149921697966ff0`.
Status: **partial**; task completion also requires the protected D60 block.
This is candidate-level mathematics, not a selected calculus, Gate A, or F07/F08.

## 1. Question and comparison discipline

Can a loss-oriented calculus make useful comparisons when the loss is a proxy,
its errors share structure, its evaluator helps determine its own behavior,
and an apparent neural interpretation depends on arbitrary hidden-unit units?

The four [F02 candidates](../foundations/02_candidate_semantics.md) retain their
original meanings: evaluated scalars (S), aligned value profiles (P),
continuation-value transformers (T), and achievable guarantee fronts (G).
This pass tests them rather than redefining all four to store the entire input.
The [source note](F04_sources.md) records the relevant literature and limits.
The [session](../work_logs/F04_2026-09-25_S1.md) records scope and actual time.

Use smaller-is-better *cost* J throughout; signed value is V=-J. Intended task
cost, proxy score, training objective, and evidence about their relationship
are different objects. The examples stipulate mathematical models; none claims
access to ultimate utility or a calibrated empirical bound merely by stipulation.
A guarantee is conditional on the declared model/evidence contract.

**Selected opportunity:** OPP-01, a joint-error, loss-grounded comparison bridge.
Affine arithmetic already exploits common error sources. The useful first
question is what survives a value comparison, not whether we invented correlation
tracking. OPP-03 supplies a small deployable reflective example. OPP-02 is an
unexecuted causal-test design, not the final neural challenge.

## 2. W1 — A calibrated proxy can improve while task performance worsens

There is one input and a Bernoulli label with probability eta=3/5 of label 1.
A predictor outputs p in [0,1], incurs Brier loss (p-Y)^2, and classifies as 1
when p>=1/2. Its intended criterion here is classification error, not Brier loss.
Write

    S(p) = eta(1-p)^2 + (1-eta)p^2
         = (p-eta)^2 + eta(1-eta).

For A with p_A=1, S(A)=2/5=4000/10000 and J(A)=2/5.
For B with p_B=49/100,

    S(B) = (49/100-3/5)^2 + (3/5)(2/5)
         = 121/10000 + 2400/10000 = 2521/10000,
    J(B) = 3/5.

The proxy improves by 1479/10000, while intended error increases by 1/5.
All data, decision thresholds and task units are unchanged. No distribution shift,
finite-sample estimation, optimizer failure, or deliberately absurd loss is needed.

### Positive result and the exact distinction

The Bayes Brier risk is S*=eta(1-eta), attained at p=eta. Classification Bayes
risk is J*=min(eta,1-eta). When the classifier chooses the wrong Bayes action,
eta and p lie on opposite sides of 1/2 (with the declared tie convention), so

    |eta-1/2| <= |eta-p|,
    J(p)-J* = |2eta-1| <= 2|eta-p|.

When it chooses the correct Bayes action, the left side is zero. Therefore

    (J(p)-J*)^2 <= 4(S(p)-S*).

The analogous population inequality follows by taking expectations and applying
Cauchy–Schwarz. This is a special elementary instance of the surrogate-excess-risk
program, not a new general calibration theorem. In W1, B has proxy regret
121/10000 and target regret 1/5, satisfying 1/25 <= 484/10000.

**What fails:** an excess-risk upper bound for each predictor does not order
arbitrary pairs of predictors. Nor does a lower training loss certify proxy
calibration or empirical generalization. Every candidate needs an alignment
premise; a richer carrier cannot manufacture one.

## 3. W2 — Useful comparisons without absolute-value bounds

### 3.1 A precise uncertain-proxy fragment

Let n target costs have the form

    J = ell + B z + A epsilon,
    z in R^k, epsilon in [-1,1]^m.

ell, B and A are supplied finite real coefficients in compatible units. z
represents unrestricted nuisance directions, and epsilon bounded error sources.
A shared symbol is a declared equality of sources, not an inference from matching
variable names or similar marginal statistics. Every finite z gives finite J;
there is no use of infinity-minus-infinity.

A consumer asks for a linear comparison w^T J. For replacement of old by new,
w has -1 at old and +1 at new. Positive w^T J is deterioration. More general
w can describe declared weighted use counts or affine combinations; it is not
an unrestricted model-composition operator.

### Lemma F04-C02: exact finite-bound criterion

Over the full declared product uncertainty set,

    sup w^T J = w^T ell + ||A^T w||_1     if B^T w=0,
              +infinity                  otherwise.

When finite, the infimum is w^T ell-||A^T w||_1 and both endpoints are attained.

**Proof.** Expand w^T J = w^T ell + (B^T w)^T z + (A^T w)^T epsilon.
If B^T w is nonzero, choose z=t B^T w. Its contribution is
t||B^T w||_2^2 and tends to infinity as t increases; fix epsilon=0.
If B^T w=0, that term vanishes exactly. Every remaining summand
(A^T w)_j epsilon_j is at most its coefficient's absolute value. Choose
all epsilon_j to have the corresponding sign (zero when the coefficient is
zero) to attain their sum. Reverse those signs for the infimum. □

The product-set assumption supplies sharpness. For a correlated subset of that
set the displayed finite expression remains an upper bound, but need not be exact.
For non-product restrictions on z, the stated unboundedness direction need not hold.

Thus **unbounded target costs are compatible with sharp finite comparative
warrants**. The substantive question is whether the consumer annihilates the
uncontrolled directions, not whether every semantic number has a global cap.
This is an elementary support-function/affine-form calculation; novelty is not
claimed for the linear algebra.

### 3.2 Hand-worked shared-source witness

Let

    J_old = 3 + z + epsilon/4,
    J_new = 1 + z - epsilon/4,
    z in R, epsilon in [-1,1].

Every individual cost ranges over the entire real line. Nevertheless

    J_new-J_old = -2-epsilon/2 in [-5/2,-3/2].

The new use improves cost by at least 3/2. For a literal nonnegative loss
example, restrict z>=0: both losses are then at least 3/4, remain unbounded
above, and have exactly the same difference interval. The general necessity
criterion above is still stated only for z in the whole real vector space.
The common unknown baseline need not be estimated at all. In the lemma, B=(1,1)^T, A=(1/4,-1/4)^T,
w=(-1,1)^T, so B^T w=0 and the radius is 1/2.

**Countermodel if shared-source identity is dropped.** Replace z in the two
expressions with independent unrestricted z_old,z_new. Each cost still has the
same marginal range R, but J_new-J_old is now unbounded above. For example,
z_old=0,z_new=4,epsilon=0 gives J_new-J_old=2, the opposite comparison.

**Countermodel to reusing a comparison in an altered use context.** For two uses
of new versus one of old, w=(-1,2). Now B^T w=1, so no finite robust bound follows.
A per-use common error occurs twice; it is not a once-only global accounting
constant. Multiplicity is an operational premise, not an optional notation.

### 3.3 Bounded witness separating joint information from marginal intervals

Set z=0 and compare two uncertainty contracts:

    shared:       J_old=3+epsilon, J_new=1+epsilon;
    independent:  J_old=3+epsilon_old, J_new=1+epsilon_new.

Every epsilon lies in [-1,1]. Both contracts have identical scalar proxy scores
(3,1) and identical individual cost intervals [2,4], [0,2]. In the shared case,
replacement improves cost by exactly 2; in the independent case its worst-case
improvement is 0. Hence scalar scores plus individual intervals cannot establish
the shared contract's positive margin, though they can establish non-worsening.

This is a fixed-margin distinction, not a claim that scalar summaries are useless.
One extra relational fact suffices here; copying the whole model is unnecessary.

### 3.4 Signed comparison versus a nonnegative inference-loss quantity

For a finite upper comparison U, define the certified replacement-loss bound

    d = max(U,0).

Then J_new<=J_old+d throughout the contract. If U<=-r, r>=0, the stronger
J_new+r<=J_old holds. The signed U preserves improvement margins that d alone
forgets: U=-2 and U=-1 both map to d=0. Therefore the nonnegative loss bound
and the signed comparison margin answer different questions.

An RLL-like numerical layer can check these finite inequalities; it does not
establish the proxy/evidence contract by arithmetic. For finite signed pair
encodings J_i=p_i-n_i with p_i,n_i>=0, the target inequality is

    p_new+n_old+r <= p_old+n_new,

which matches an additive RLL sequent with the right-hand sum on the antecedent
side. The finiteness and interpretation premises must remain explicit. This
pass does not claim to emit a full RLL derivation for every matrix identity.

### 3.5 Joint propagation versus adding already-reduced radii

For two consumers w1,w2 annihilating B, their combined exact radius is

    ||A^T(w1+w2)||_1 <= ||A^T w1||_1 + ||A^T w2||_1.

The inequality follows coordinate by coordinate from |a+b|<=|a|+|b|. It can be
strict: J1=epsilon,J2=-epsilon have individual radius 1, while J1+J2=0 has
radius 0. A record containing only their radii no longer supports this equality.
For an affine map F, propagate (ell,B,A) to (F ell,F B,F A) before reduction.
This is exact for that fragment. Nonlinear operations require new error enclosures
or explicit region conditions, as in affine arithmetic; a source tag alone does
not make their propagation exact.

### 3.6 Units, evidence updates, and statistical scope

A positive unit change a multiplies ell,B,A,U,r and the task tolerance together.
The comparison is unchanged after decoding the new units. Scaling only the proxy
but leaving its error and tolerance untouched asks a different question.
Adding a common offset has no effect exactly for w^T 1=0 in this affine fragment.
No invariance under arbitrary monotone recodings is assumed.

If evidence narrows an uncertainty set E to a nonempty E' subset E without
changing the functions or units, a prior universal guarantee over E survives.
If evidence instead splits one shared source into two independently varying
sources, E is enlarged and the W2 countermodel applies. If the intended loss,
proxy version, or source map changes, it is not mere conditioning of the old
contract. A coverage claim P(actual parameters in E)>=1-alpha yields at most
that coverage interpretation for a consequence, not unconditional factivity.
Empty E is an inconsistent evidence state, not a cost-free proof of every claim.

**Phase-one tie.** This develops phase one's shared provenance, tube-valid bound
propagation and revision conditions at a quantitative interface. It does not
relicense a composite from the component grants alone. A supplied certificate
that supports the joint relation is still needed before a license is lifted.

## 4. W3–W5 — Modest reflection with a genuine feedback loop

### 4.1 What counts as self-assessment here

The object is a named, versioned controller that uses its own reported failure
bound to choose its own behavior. Its self-model names that same controller,
not an unrelated predictor relabeled as 'self'. The scope is finite randomization
and explicitly supplied uncertainty intervals, not unrestricted logical reflection.
The source-oracle comparison is a precedent, not an oracle used by this program.

Let stress cause failure with unknown probability theta in a supplied nonempty
interval I=[a,b] subset [0,1]. A checked-safe branch has failure probability zero
in this toy model. A version `SELF-MIX-v1` uses report r in [0,1] to take the safe
branch with probability r and stress otherwise. Its expected failure is

    H_theta(r) = theta(1-r).

The report affects the very quantity assessed. The safe-branch condition and
validity of I are external/model assumptions, not proved by self-endorsement.
Changing either condition or the controller version changes this model.

### W3: exact prediction, consistency, and convergence are different

If theta is specified, exact self-calibration requires

    r=theta(1-r), so r*=theta/(1+theta).

For theta=1 the unique solution is 1/2. Yet naive updates r_(t+1)=1-r_t oscillate
between 0 and 1 from r_0=0. Existence and uniqueness therefore do not imply
convergence of a chosen update algorithm. With damping,

    r_(t+1) = (r_t+b(1-r_t))/2
            = b/2 + (1-b)r_t/2,

the error relative to b/(1+b) is multiplied by (1-b)/2, which lies in [0,1/2].
This recurrence stays in [0,1] and converges geometrically. For b=1 it reaches
the solution in one step. The result follows directly by subtracting the fixed
point; no unrestricted fixed-point theorem is imported.

**Finite iteration needs its own warrant.** Convergence alone does not make each
intermediate report safe. Starting from r_0=0 with b=2/5 gives r_1=1/5,
but worst-case failure is (2/5)(4/5)=8/25>1/5. Starting instead at r_0=1
preserves r_t>=r* at every step, since the error multiplier is nonnegative.
Moreover r_(t+1)-r_t = -((1+b)/2)(r_t-r*)<=0. Thus this upper-start iteration
provides a decreasing sequence of valid deployable upper reports. Its current
failure bound is evaluated for the current report-induced policy, not a fixed
policy silently substituted from a different iteration. The exact rational
formula r*=b/(1+b) remains available in this small example; the iteration result
is a control against confusing convergence with finite-step certification.

In a different version `SELF-HARD-v1`, stress certainly fails and the controller
stresses exactly when its scalar exact-failure forecast r is below 1/2. Then

    H(r)=1 if r<1/2, and H(r)=0 otherwise.

There is no r=H(r): in the first case equality would force r=1, in the second
r=0. This refutes unrestricted *exact* self-prediction for this interface, not
all reflection. For example, an upper-bound report has different semantics:
r=1/2 is a valid bound on H(r)=0. Randomizing or weakening equality to a bound
changes the contract and must be stated, not silently treated as the same proof.

In the separate version H(r)=r every r is self-calibrated. Choosing r=9/10
can therefore be perfectly calibrated and still fail a tolerance of 1/10.
Self-consistency alone does not express good performance or a unique policy.

### W4: a solution for each hidden model is not one deployable report

For a<b, the family of exact equilibria is

    {theta/(1+theta): theta in [a,b]} = [a/(1+a),b/(1+b)].

But no single report can be exactly self-calibrated for both a and b: subtracting
r=a(1-r)=b(1-r) implies r=1, which would require r=0. Selecting r*(theta) would
use an unknown parameter. An interval of pointwise equilibria is not already an
executable policy available before theta is learned.

### Positive result F04-C04: a deployable self-bound with uncertainty

Give the report its intended type: **an upper bound on the expected failure of
this same deployed controller**. Require it uniformly over the supplied I:

    for all theta in I, theta(1-r)<=r.

Since r<=1, the worst theta is b. The condition is exactly

    b(1-r)<=r  iff  r>=b/(1+b).

Choose the least such report r_I=b/(1+b). The implemented program can compute
this from the available interval; it does not need actual theta. Its own
expected failure interval is exactly

    [a/(1+b), b/(1+b)].

The upper endpoint equals its report, and each endpoint is attainable under
the stipulated interval model. This is a bounded, constructive, genuinely
feedback-dependent semantics with explicit unresolved uncertainty.

**Worked update.** At I_0=[0,1], the report is 1/2 and own failure lies in [0,1/2].
Adequacy at tolerance 1/3 is unresolved. After admissible evidence supplies
I_1=[1/5,2/5], the report becomes 2/7, and own failure lies in [1/7,2/7].
The same version now supports adequacy at 1/3. No empirical procedure that
produces I_1 is claimed here; this is its conditional consequence.

The pointwise-equilibrium interval [1/6,2/7] would be a *wrong* loss interval
for this deployed controller: at theta=1/5 its actual failure is 1/7<1/6.
The right interval uses the same deployed r_I for all theta. This is a concrete
common-policy-witness distinction, not merely an abstract quantifier warning.

### W5: a better bound need not mean the changed controller is better

Hold true theta=2/5 fixed across the worked update. Before it, failure is
(2/5)(1/2)=1/5. After it, failure is (2/5)(5/7)=2/7, which is larger. The upper
bound has decreased because the prior uncertainty shrank, but the controller
also takes more stress actions. There is no contradiction: it is not the same
fixed policy with two error bounds. It is a new deployed behavior.

If safe operation has cost k, a possible total task cost is

    J_theta(r)=theta(1-r)+k r.

For k=1 the worked update improves total cost from 7/10 to 4/7; for k=0 the
failure cost worsens. The example does not prove this self-bound policy is optimal
for either objective. It shows exactly where proxy, bound, risk, information,
and policy value need distinct roles. No task-independent utility is inferred.

**Version countermodel.** If an unannounced new version always stresses, the old
report 2/7 is false at theta=2/5. Matching version identifiers are necessary for
using this self-model; retaining a formerly correct numeric report is not enough.

### 4.2 Fit to the candidates and to phase one

For fixed theta and controller parameter r, the terminal-value transformer is

    T_(theta,r)(v0,v1) = (1-theta(1-r))v0 + theta(1-r)v1.

It is a positive normalized linear transformer in terminal values, so it fits
T's elementary fragment. The feedback equation concerns a **control parameter**
r, not an ordinary monotone continuation argument. Flattening both roles into
one scalar without declaring their types would incorrectly treat the decreasing
map H_theta as a monotone value transformer. Solving for r is a new, specified
operation on a family of transformers, not a consequence of acyclic composition.

The bound b(1-r)<=r can be represented as guarded finite arithmetic in an RLL-like
layer; uncertainty is a separate range premise. P can retain the joint theta/r
semantics directly. G can retain achievable risk/cost tradeoffs and the implementing
policy witness. S can store a concluded bound, but not reconstruct the controller
or its version dependencies from that number alone.

The phase-one ranked assessor is a viable staged starting point. This example
extends beyond staging only in its explicitly solved feedback case. It does not
import factivity, a universal self-proof rule, or an AGI result.

## 5. W6–W7 — Neural 'values' must survive coordinate changes and interventions

Consider an ordinary one-hidden-layer ReLU network with affine output,

    h_i(x)=ReLU(w_i^T x+b_i),
    f(x)=beta+sum_i v_i h_i(x).

For c_i>0 and a permutation pi, define

    w'_j=c_j w_(pi(j)), b'_j=c_j b_(pi(j)), v'_j=v_(pi(j))/c_j.

Positive homogeneity gives h'_j=c_j h_(pi(j)), hence f'=f on every input.
This is an exact function-preserving reparameterization of this architecture.

### W6: raw activation is not an identifiable numerical value

A hidden activation can be multiplied by any positive factor without changing
network outputs. Its absolute magnitude and a ranking of magnitudes across
neurons therefore cannot, on their own, identify a task's fixed-unit utility.
The elementary identity ReLU(b-a)=max(b-a,0) is a mechanistic candidate, not
evidence that an arbitrary trained neuron is a loss comparison.

A better-defined observation in this restricted architecture is the contribution
v_i h_i. It is invariant under the rescaling (up to permutation). More importantly,
a one-coordinate donor intervention has output effect

    Delta f = v_i [h_i(x_donor)-h_i(x_base)].

Its transformed counterpart has exactly the same effect because c_i cancels.
This proves an intervention control, not that these contributions possess the
intended semantic meaning. For deeper networks the analogous transport must
include all adjacent weight changes and downstream nonlinearities; this simple
formula is not asserted unchanged there.

### W7: perfect decoding without causal use

Take h1(x)=ReLU(x), h2(x)=ReLU(x), f(x)=h1(x)+0 h2(x). On positive inputs,
either hidden coordinate perfectly predicts x. Replacing h2(1) by h2(2) changes
nothing in the output, while the same interchange at h1 changes f from 1 to 2.
A probe with perfect predictive accuracy therefore need not locate a variable
that the network uses. The source causal-abstraction method addresses exactly
this distinction; we do not claim to invent interchange interventions.

Replacing the entire hidden state simply yields the donor output. It cannot
by itself substantiate an intermediate computational hypothesis. Require a
proper subrepresentation, retained other variables, and matched controls.

### 5.1 Prospective ordinary-training test

See [the unexecuted design](../experiments/F04_neural_probe_design.md). Train a
standard small ReLU MLP on ordinary outcome labels with a conventional weighted
classification loss, not additional logical labels or residual regularizers.
Use known synthetic conditional event probabilities only to define independent
high-level task losses for post-hoc tests. A successful explanation must predict
held-out interchange effects, beat equally flexible alternative descriptions,
and transport under the exact rescaling/permutation above. Constructed networks
in the present fixture test the methodology only; no trained-network discovery
or final F15 challenge is reported.

## 6. Candidate discrimination, not a popularity ranking

| Question | S: scalar summary | P: aligned profiles | T: continuation map | G: guarantee front |
|---|---|---|---|---|
| W1: proxy improves, target worsens | Cannot exclude reversal without an alignment premise | Joint target/proxy data makes reversal visible; cannot infer unobserved alignment | Same need for alignment; a surrogate map alone is insufficient | Can distinguish target and proxy budgets when both supplied |
| W2: shared unbounded nuisance | Proxy scores and separate intervals lose the cancellation premise | Joint source alignment supports the exact affine fragment | A transform family retaining source identity can propagate it; reducing to independent minima loses it | A front that discarded joint source identity cannot recover it merely from marginal budgets |
| Multiplicity, units, updates | A final scalar bound may be usable on the same query; not automatically reusable | Coefficients and source dependencies expose which query changed | Typed composition preserves valid bounds; parameter/continuation roles differ | Costs/use counts and a policy witness must be carried, not inferred |
| W3–W5: own-behavior feedback | A report is an output, not its own calibration proof | Can represent nonempty joint controller/world semantics | Fixed-parameter kernels fit; the explicit feedback solve is an extension | Can retain implemented risk/cost choices; pointwise optima are not a common policy |
| W6–W7: neural interpretation | A neuron magnitude does not identify a value unit | A coordinate-aware semantic map is possible but needs intervention evidence | Causal maps are promising test objects, not automatically learned | A decoded menu does not show that its alternatives causally organize the network |

Two viable but not identical starting routes survive:

**A. Finite loss comparisons with shared-source affine certificates.** Use RLL-like
arithmetic for comparison/slack operations, while a declared joint proxy/evidence
model supplies the meaning and dependence. Advantages: exact small certificates,
sharp cancellation, and direct links to ReLU affine pieces. Limitations: not all
nonlinear uses preserve affine forms; analytic and statistical assumptions are
not established by arithmetic.

**B. Desirable differences / lower-value transformers with a specified context.**
For a supplied nonempty uncertainty family, evaluate a gain g by inf g (or a
specified lower expectation). A positive lower bound witnesses desirability.
This is close to existing desirability and preexpectation traditions; it does
not require taking RLL's whole propositional syntax as primary. It has natural
sequential interfaces, but must retain joint models, feasible decisions and
feedback semantics. The weak test inf g>=0 should not be equated without care
with a source's strict-desirability convention, which can exclude the zero gamble.

These routes overlap on some numerical judgments; an overlap is useful, not
proof they are identical calculi. A final comparison must include representational
cost, composition, proof certificates and an operational task. No winner is fixed.

## 7. Dispositions and bounded next work

- **Ruled out as general inference:** lower proxy score implies better target;
  identical marginal bounds imply interchangeable composite guarantees; a
  pointwise self-consistent solution is one deployable policy under uncertainty;
  unique fixed point implies iterative convergence; neural decodability proves
  causal use; raw activation magnitude is an invariant utility measure.
- **Positive restricted results:** the affine nuisance annihilator criterion;
  exact shared-source propagation; a finite, versioned, uncertain self-bound
  that controls its own behavior; and a gauge-transported neural intervention.
- **Still required before F04 completion:** satisfy D60; freshly reconstruct and
  challenge these examples, including the non-affine and relation-elimination
  boundaries; check that the comparison has not favored a candidate through
  hidden extra data. No Gate A assessment occurs in this work item.

The leading opportunity remains OPP-01, now narrowed to *difference-sufficient
proxy certificates with explicit source and evaluator versions*. Affine arithmetic,
robust optimization, paired comparison and surrogate-risk theory are strong
baselines. A novel result would have to add a meaningful composition/revision or
representation characterization rather than rename their elementary bounds.
