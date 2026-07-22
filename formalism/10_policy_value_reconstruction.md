# Policy/Value Behavioral Reconstruction

Status: Task 22B completed

Date: 2026-07-21

Layman's-explanation amendment: 2026-07-21

Depends on: the finite encoder-image result and semantic boundaries in
[`notes/policy_value_judgment.md`](../notes/policy_value_judgment.md), the
interpretability evidence axes in
[`notes/policy_value_interpretability.md`](../notes/policy_value_interpretability.md),
and the pre-draft decision in
[`notes/checkpoints/D_predraft.md`](../notes/checkpoints/D_predraft.md)

Executable witnesses:
[`verification/policy_value_reconstruction.py`](../verification/policy_value_reconstruction.py)
and
[`verification/test_policy_value_reconstruction.py`](../verification/test_policy_value_reconstruction.py)

## Durable result summary

1. **Approximate action scores give a constructive behavioral guarantee.** For
   finite nonempty legal-action sets, intended scores `W`, approximate scores
   `W_hat`, coordinate error `e`, intended-policy action gap `g`, and a named
   evaluation distribution `mu`,

   ```text
   D_mu(pi,pi_hat) <= mu{e>rho} + mu{g<=2 rho}.                 (10.1)
   ```

   The statement binds the policy, score target, decoder, legal actions, tie
   rule, distribution, and their versions. Forced singleton-action states have
   `g=+infinity`.
2. **Equation (10.1) is an oracle inequality.** Its event masses use true score
   error and true intended gaps. An operational certificate needs an accepted
   joint record that bounds those masses, a pointwise envelope that implies
   them, or a direct held-out bound on disagreement.
3. **The factor two is exact for coordinatewise error.** At true gap `2 rho`,
   opposite coordinate errors of size `rho` can create an estimated tie. At a
   gap arbitrarily below `2 rho`, they can reverse the winner. No smaller
   universal coefficient replaces `2` under the stated assumptions.
4. **Conservative certification is a second layer.** Coordinate radius `rho`
   induces the generic pairwise-gap error radius `r_gap=2 rho`. An estimated
   winner gap strictly above `r_gap` certifies the true winner. Guaranteeing in
   advance that this conservative decoder both recovers `pi` and does not
   abstain is ensured by `g>2 r_gap=4 rho`. This `4 rho` condition is sufficient,
   not necessary. A directly accepted gap-error certificate may give a smaller
   `r_gap`.
5. **The exact existence statement remains intact.** The canonical score
   encoder `E` and fixed decoder `D` satisfy `D o E=id` on every deterministic
   policy in the declared finite class. The other composite `E o D` is an
   identity only on the encoder image. Approximation adds a stability question;
   it does not withdraw this exact correspondence.
6. **Return semantics add conditions.** For declared `Q^pi`, reconstruction of
   the source policy requires self-greediness on the claimed states and
   compatible perspective and ties. Otherwise the greedy composite can be
   policy improvement. A scalar `V^pi` requires a transparent harness exposing
   legal actions, dynamics, reward, discount or horizon, perspective, and tie
   handling; value error must first be propagated to action-score error.
7. **Stochastic reconstruction has a different target.** An `argmax` decoder
   recovers only a modal action. Distributional fidelity requires probability
   outputs or a sampling harness and a metric such as total variation or KL.
8. **Training, IID, and trajectory statements are separate.** Agreement on a
   training set gives no off-support result. An independent IID holdout can
   certify `D_mu` for a fixed pair. Trajectory similarity additionally needs a
   horizon, coupled visitation process, and stepwise conditional error control.
9. **The value-logic result is one typed atom.** A valid reconstruction record
   may support `DecodeStable` inside an action-authorizing surrogate profile.
   It does not by itself establish return/ranking adequacy, support, improvement,
   trace, mechanism, human usefulness, or a complete reliance license.
10. **The result is neutral about true utility.** It gives conditions under
    which a declared semantic surrogate and harness reproduce behavior. It
    makes no assertion about whether an arbitrary policy has a true utility or
    whether any surrogate recovers one.

## Layman's explanation

### What problem is this result trying to solve?

Imagine a black-box agent that sees a situation and chooses an action. The
agent might be a neural network, a hand-written program, or any other bounded
policy. We would like to build a second model that describes the agent in more
meaningful terms. A natural candidate is a value-like model: instead of merely
saying “choose action A,” it assigns numbers to the available actions or to
their possible consequences, and a visible decision rule chooses the action
with the highest score.

This would be useful even if the second model never revealed every detail of
the original agent. Its scores could expose stable comparisons, close calls,
failure regions, or counterfactual alternatives. That is the interpretability
motivation. The mathematical question here is narrower:

> When does an approximate score model, together with a completely stated
> decision rule, reproduce the black-box policy's choices?

The theorem gives a local answer and then adds up the unresolved cases over a
named population of situations.

### Can numbers encode categorical choices without losing information?

Two apparently conflicting intuitions are both useful.

First, a finite categorical policy can be encoded exactly by numbers. For each
situation, give the chosen action score `1` and every other action score `0`.
The rule “choose the largest score” recovers the action with no behavioral
loss. Once the score space is restricted to these canonical encodings, policy
and score representation are two exact descriptions of the same finite choice
function. This is the project's finite encoder-image existence or isomorphism
claim.

Second, converting an arbitrary score vector into its winning category usually
does discard information. Scores `(10,9)` and `(10,0)` produce the same action,
although the first decision is close and the second is decisive. Many different
score vectors collapse to one categorical choice. The action alone cannot tell
us the ranking margins or what would happen after a small perturbation.

The exact existence claim concerns the first direction: a policy can be placed
inside a carefully declared numerical representation without losing its
choices. It does not say that decoding arbitrary scores preserves every fact
about those scores. The practical value-surrogate question is interesting
precisely because a semantically meaningful score model may retain more useful
structure than the final categorical action while still reproducing that
action.

### Why does the action gap control reconstruction?

Suppose the intended model gives action A a score of `10` and action B a score
of `6`. The action gap is `4`. Now suppose every approximate score is wrong by
at most `1`. In the worst case, A is underestimated as `9` while B is
overestimated as `7`. A still wins.

The important point is that two coordinates can move against us at once. The
winner can move down by `rho`, and a rival can move up by `rho`. Their gap can
therefore shrink by as much as `2 rho`. This yields the simple guarantee:

```text
approximation error at most rho
and intended action gap greater than 2 rho
    => the decoded action is unchanged.
```

The factor two is genuine. If the original gap is exactly `2 rho`, the two
opposite errors can create a tie. If the gap is slightly smaller, they can
reverse the winner. This is why the theorem uses a strict boundary rather than
quietly treating equality as safe.

Over a whole evaluation population, every disagreement must therefore occur in
at least one of two regions:

1. the score approximation was worse than `rho`; or
2. the original decision was within `2 rho` of a competing action.

That is what equation (10.1) says. It does not say that every small-gap state is
misdecoded. It says those states are unresolved by this particular guarantee.
This is useful because it separates two improvement targets: reduce score error,
or understand and handle the policy's genuinely close decisions.

### Why is the theorem called an oracle bound?

The clean formula uses the *true* score error and the *true* action gap. In a
real learned system, those quantities may be only partly known. A network does
not certify its own accuracy merely by producing confident numbers.

The formula therefore begins as an oracle inequality: it tells us which facts
would be sufficient and how they combine. It becomes an operational guarantee
only after accepted evidence supplies those facts. That evidence might be a
valid pointwise error envelope, statistically justified upper bounds on the two
unresolved population masses, or an independent held-out estimate of action
disagreement for a fixed policy pair and distribution.

This distinction matters for the value-logic project. The theorem identifies a
possible `DecodeStable` requirement. A checked evidence record must support that
requirement before it participates in a reliance profile. The mathematical
shape of a guarantee and the evidence that its premises hold are different
objects.

### Why does `4 rho` appear in the conservative version?

A raw decoder always picks the largest estimated score. It can reproduce the
right action whenever the true gap exceeds `2 rho`, assuming the coordinate
error bound holds.

A conservative decoder asks for more. Before authorizing the action, it demands
that the *estimated* winning gap itself be larger than the possible error in a
pairwise gap. Because two coordinates can each be wrong by `rho`, that
pairwise-gap error radius is `2 rho`.

Starting from the true scores, the observed gap can first shrink by `2 rho`.
The shrunken observed gap must then still clear the conservative certificate
threshold of `2 rho`. A true gap greater than `4 rho` guarantees both outcomes:
the action is recovered, and the conservative decoder does not abstain.

This does not mean ordinary behavioral reconstruction inherently requires
`4 rho`. The extra separation pays for a stronger operational result: a
generic certificate of the winner together with guaranteed non-abstention. It
is a sufficient condition, and a more direct accepted estimate of pairwise-gap
error can justify a smaller certificate radius.

### What kind of “value” is being reconstructed?

The theorem works with action scores, but different score constructions carry
different meanings.

- A canonical `1/0` encoding can represent any finite deterministic policy
  exactly. It is behaviorally strong and semantically thin: the numbers are
  labels chosen for reconstruction rather than expected returns.
- A declared `Q^pi` has return semantics relative to a stated environment,
  reward, horizon or discount, state description, and perspective. Greedy
  decoding reproduces the source policy only where that policy already chooses
  the action favored by its own `Q^pi`. Elsewhere, the decoder may be improving
  the policy according to the declared return rather than reconstructing it.
- A scalar `V^pi` does not itself say which action to take. The decision harness
  must expose the legal actions, successor dynamics, immediate rewards,
  discount or horizon, perspective, and tie rule. Errors in `V` must be carried
  through that harness before the action-gap theorem applies.
- For a stochastic policy, recovering only the most likely action loses the
  rest of the action distribution. Distributional reconstruction needs
  probabilities or a sampling rule and a metric such as total variation or KL.

These cases explain why exact representational existence and meaningful learned
reconstruction should remain separate claims. The first shows that a lossless
behavioral code is possible. The second asks whether a useful semantic surrogate
can be learned and supported by evidence.

### What does the result say about generalization and interpretability?

Exact agreement on training situations can coexist with complete disagreement
everywhere else. An independent IID test can support an action-disagreement
bound under its named sampling distribution. A trajectory claim is stronger:
one changed action can send the two policies into different future states, so
the analysis needs a horizon, a coupling, and error control under the sequence
of visited situations.

For the same reason, behavioral agreement does not by itself identify the
source policy's hidden computation. A value surrogate may still be an
interpretable model-of-a-model: it can expose declared rankings, margins,
counterfactuals, and failure regions. If researchers want to trace that meaning
backward into the original policy network, they must additionally connect the
surrogate to policy hidden states and test the proposed connection with
policy-side interventions.

The project leaves the “true utility” question open. The result concerns a
declared representation and its behavioral fidelity. It neither assumes that
every policy has a true utility nor concludes that such a utility is absent.

### Short public-facing version

> A policy chooses an action; a value-like surrogate gives scores to the
> alternatives and then chooses the largest. If every estimated score is within
> `rho` of its intended value, the winning action cannot change wherever its
> original lead is greater than `2 rho`: the winner can be underestimated by
> `rho` while a rival is overestimated by another `rho`. Across a population,
> disagreements can therefore occur only where the approximation error is too
> large or the original decision was too close to call. This is initially an
> oracle statement because the true errors and gaps still need evidence. A
> conservative system that must certify the winner and avoid abstaining needs
> more room; `4 rho` is a generic sufficient true gap. The result preserves the
> exact finite policy-to-score encoding claim while keeping return semantics,
> off-support generalization, internal mechanism, and true-utility questions as
> separately investigated matters.

## 1. Versioned finite reconstruction contract

Let `X` be a finite state or information-state domain. Each `x in X` has a
finite nonempty legal-action set `A_x`. Fix:

- a deterministic policy `pi_vpi(x) in A_x`;
- intended action scores `W_vW(x,a) in R`;
- approximate action scores `W_hat_vhat(x,a) in R`;
- a decoder `D_vD` that chooses a score maximizer using an explicit total tie
  priority `tau_x` on each `A_x`; and
- a named evaluation distribution `mu_vmu` on `X` or a declared subset of it.

The policy action is required to win under the intended score table on the
claimed support:

```text
D_vD(W_vW)(x) = pi_vpi(x).                                      (10.2)
```

This permits a tie only when the declared tie rule selects the policy action.
The robust pointwise region below has a strictly positive gap, so its conclusion
does not depend on how an estimated tie is resolved. Version binding matters:
changing legal actions, the state representation, reward perspective, decoder,
or tie priority creates a new contract rather than silently reusing an old
certificate.

Define the decoded approximation and disagreement risk by

```text
pi_hat(x) = D_vD(W_hat_vhat)(x),
D_mu(pi,pi_hat) = mu{x : pi_hat(x) != pi(x)}.
```

For `rho>=0`, define the true coordinate error

```text
e(x) = max_(a in A_x) |W_hat(x,a)-W(x,a)|.
```

When `A_x` contains at least two actions, define the true policy-relative gap

```text
g(x) = W(x,pi(x)) - max_(a in A_x, a!=pi(x)) W(x,a).
```

Set `g(x)=+infinity` when `A_x={pi(x)}`. This convention records that no score
perturbation can change a forced action while the legal-action contract remains
fixed. It does not call the singleton score accurate.

## 2. Raw oracle reconstruction theorem

### Lemma 1: pointwise stability

For any state `x`,

```text
e(x)<=rho and g(x)>2 rho  =>  pi_hat(x)=pi(x).                  (10.3)
```

**Proof.** The singleton case is immediate. Otherwise, for every
`a!=pi(x)`,

```text
W_hat(x,pi(x)) - W_hat(x,a)
  >= W(x,pi(x))-rho - (W(x,a)+rho)
  >= g(x)-2 rho
  > 0.
```

Thus `pi(x)` is the unique maximizer under `W_hat`, so the decoder returns it.
`square`

This proof constructs the certified region directly from two checkable kinds
of separation: bounded coordinate error and a sufficiently large intended
action gap. It leaves the remaining states visible rather than assigning them
a verdict.

### Theorem 2: distributional oracle bound

Under the contract in §1,

```text
D_mu(pi,pi_hat)
  <= mu{e>rho} + mu{g<=2 rho}.                                 (10.4)
```

**Proof.** Lemma 1 gives the event inclusion

```text
{pi_hat!=pi} subseteq {e>rho} union {g<=2 rho}.
```

Take `mu` and apply the union bound. `square`

The right side can exceed one; clipping it at one gives an equally valid risk
bound. The unclipped sum is retained because its two terms show separately how
much mass remains unresolved by error and by boundary geometry.

### Proposition 3: the coefficient two is tight

Fix `rho>0` and two actions `a,b`, with source action `pi(x)=a`.

At the boundary, let

```text
W(a)=2 rho,  W(b)=0,
W_hat(a)=rho, W_hat(b)=rho.
```

Then `e=rho` and `g=2 rho`. A tie rule prioritizing `b` decodes `b`, so the
strict condition in Lemma 1 cannot be weakened to `g>=2 rho` for arbitrary
compatible deterministic decoders.

For a strict flip, choose `0<zeta<2 rho` and let

```text
W(a)=2 rho-zeta,  W(b)=0,
W_hat(a)=rho-zeta, W_hat(b)=rho.
```

Again `e=rho`, while `W_hat(b)>W_hat(a)`. Given any proposed universal
coefficient `c<2`, choose `zeta<(2-c)rho`; then `g>c rho` and the approximation
still flips the action. Therefore no coefficient below two proves the same
coordinatewise statement. `square`

The fixture is executable in `OracleBoundTests`. It explains a boundary; it
does not suggest that learned errors generally take this adversarial form.

### Corollary 4: exact canonical-score robustness

For the canonical encoder

```text
E(pi)(x,a) = 1 if a=pi(x), and 0 otherwise,
```

every nonsingleton intended gap is one. If an accepted pointwise score envelope
gives `e(x)<=rho<1/2` throughout a declared domain, raw decoding is exact there.
Singleton states are exact for every finite score perturbation that preserves
their legal-action set.

The corollary concerns an arbitrary-policy behavioral code. The numbers `0`
and `1` receive no return, preference, or cardinal-utility meaning from this
construction.

## 3. From an oracle inequality to accepted evidence

Equation (10.4) contains true `e` and `g`. A network's own scores do not reveal
their error merely by being emitted, and a learned `Q` does not reveal the true
small-gap mass merely by naming its output `Q`. Three constructive evidence
routes are available.

### Corollary 5: accepted event-mass certificate

Suppose one accepted joint record, with its population, lineage, versions,
mode, and coverage declared, establishes on an event `C`

```text
mu{e>rho}     <= eta_e,
mu{g<=2 rho}  <= eta_g.
```

Then on `C`,

```text
D_mu(pi,pi_hat) <= min(1,eta_e+eta_g).                          (10.5)
```

If separate records have failure probabilities `alpha_e` and `alpha_g`, their
ordinary union accounting gives joint coverage at least
`1-alpha_e-alpha_g` unless a sharper accepted dependence argument is supplied.
Point estimates of the two masses do not constitute these premises.

### Corollary 6: pointwise certified region

If accepted envelopes establish `e(x)<=rho` and `g(x)>2 rho` on a measurable
region `U`, then

```text
D_mu(pi,pi_hat) <= 1-mu(U).                                    (10.6)
```

This is useful when support, error, and gap certificates are local. It also
makes abstention geometry explicit: states outside `U` remain unresolved. A
state-dependent radius can be used by replacing the two constant-radius tests
pointwise; the proof is unchanged.

### Proposition 7: independent IID disagreement certificate

Fix `pi`, `pi_hat`, their complete versioned decoder contract, and a target
distribution `mu` before inspecting an independent IID holdout
`X_1,...,X_n~mu`. Let

```text
D_hat_n = (1/n) sum_i 1{pi_hat(X_i)!=pi(X_i)}.
```

Hoeffding's bounded-sum inequality gives, for `0<alpha<1`,

```text
P(D_mu(pi,pi_hat)
    <= D_hat_n + sqrt(log(1/alpha)/(2n))) >= 1-alpha.           (10.7)
```

The upper endpoint may be clipped at one. Equation (10.7) directly certifies
behavioral disagreement; it does not estimate or identify the oracle bound's
two explanatory terms. Model, threshold, distribution, or report selection
using the same holdout requires valid adaptive/multiplicity accounting.

## 4. Conservative winner certification

The raw decoder always returns an action. A license interface may instead
withhold action authorization unless accepted uncertainty proves the winner.
Let `a_hat` be the estimated winner and define its estimated pairwise gap

```text
g_hat = W_hat(x,a_hat) - max_(b!=a_hat) W_hat(x,b),
```

with `g_hat=+infinity` at a singleton state.

### Lemma 8: coordinate radius induces a pairwise-gap radius

If every coordinate obeys `|W_hat(x,a)-W(x,a)|<=rho`, then for every pair
`a,b`,

```text
|(W_hat(x,a)-W_hat(x,b))-(W(x,a)-W(x,b))| <= 2 rho.            (10.8)
```

Thus `r_gap:=2 rho` is a valid generic pairwise-gap error radius. If
`g_hat>r_gap`, then `a_hat` is the unique true winner. `square`

The strict inequality is essential for a unique-winner certificate. A directly
accepted certificate for pairwise gaps may supply `r_gap<2 rho`; its own target,
scope, and coverage then replace the generic coordinate calculation.

### Proposition 9: sufficient true gap for recovery without abstention

Use the conservative rule

```text
D_cert(W_hat)(x) = a_hat if g_hat>r_gap, and Withheld otherwise.
```

Under coordinate error at most `rho`, take `r_gap=2 rho`. If

```text
g(x)>4 rho,                                                    (10.9)
```

then `D_cert(W_hat)(x)=pi(x)`.

**Proof.** Lemma 1 already gives raw recovery because `g>4 rho` implies
`g>2 rho`. The estimated gap of `pi(x)` is at least `g-2 rho>2 rho=r_gap`, so
the certificate does not withhold. `square`

At true gap `4 rho`, opposite coordinate errors can leave the estimated gap
exactly `2 rho`, causing the strict conservative rule to withhold even while
the raw winner remains correct. Condition (10.9) is a generic sufficient
condition for guaranteed recovery plus non-abstention. It is not a necessary
condition for either property.

More generally, if a directly accepted gap-error radius is `r_gap`, a true gap
above `2 r_gap` is sufficient for the same two-sided conservative argument.
Calling `rho` itself a gap radius without a direct gap certificate would omit
one coordinate's possible error.

## 5. Exact and approximate arrows

Writing the domains prevents several different correspondences from sharing
the word “inverse.”

### 5.1 Arbitrary deterministic policies and canonical scores

Let `Pi_v` be the declared deterministic policy class and let `W_all` be all
finite action-score tables on the same legal-action contract. The canonical
encoder and decoder have types

```text
E_can : Pi_v -> W_all,
D_tau : W_all -> Pi_v.
```

They satisfy

```text
D_tau o E_can = id_(Pi_v).                                    (10.10)
```

Let `Im(E_can)` be the one-hot score tables. Restricted to that image,

```text
E_can o D_tau = id_(Im(E_can)).                               (10.11)
```

Outside the image, `E_can o D_tau` replaces an arbitrary score table by the
canonical table for its winner and therefore need not return its input. This is
the exact finite encoder-image isomorphism/existence claim. Theorems 2 and 9
describe what happens after an approximate score map is inserted before
decoding.

### 5.2 Return-semantic action values

Fix a fully declared decision process `M` and perspective. Write

```text
F_M^Q : Pi -> Q_M,       F_M^Q(pi)=Q^pi,
G_(M,tau) : Q_M -> Pi,   G_(M,tau)(Q)=tie-broken greedy policy.
```

The policy composite obeys

```text
G_(M,tau)(F_M^Q(pi))=pi
```

exactly on the compatible self-greedy subset

```text
Fix_Q = {pi : pi(x)=G_(M,tau)(Q^pi)(x) on every claimed x}.   (10.12)
```

On `F_M^Q(Fix_Q)`, the other composite `F_M^Q o G_(M,tau)` is also the
identity. There is no corresponding identity on all numerical `Q` tables.

Under the standard finite discounted, fully observed, single-agent,
all-maximizing assumptions, global self-greediness makes `V^pi` a fixed point
of the Bellman optimality operator; hence `pi` is optimal. With a fixed tie
rule, some other optimal policies can choose a different tied optimal action
and therefore need not be fixed points of this particular decoder.
Self-greediness only on `mu`-supported states is weaker: it gives local
behavioral agreement there and supplies no global optimality statement.

To apply Theorem 2 to an approximation `Q_hat`, set `W` to the perspective-
oriented `Q^pi` only on states where the source policy is the declared greedy
winner. If `pi` is not self-greedy, `G(Q^pi)` is an improvement candidate and
the theorem can describe approximation of that greedy policy. Disagreement
with the source policy then mixes reconstruction error with genuine policy
improvement and must not be labeled pure inversion failure.

### 5.3 Scalar state value plus decision harness

A scalar `V(x)` lacks an action coordinate. Fix a transparent one-step harness

```text
H = (A_x, P(.|x,a), r(x,a), gamma, sigma_x, tau_x, versions),
```

where `sigma_x in {+1,-1}` converts the declared perspective into a maximization
score. The harness constructs

```text
W_V(x,a)
  = sigma_x [r(x,a) + gamma sum_y P(y|x,a)V(y)].               (10.13)
```

This covers a maximizing MDP with `sigma=+1` and an explicitly declared
minimizing turn with `sigma=-1`. Finite-horizon variants bind the time index in
the state or harness. Terminal conventions are part of `P,r,V`.

If the harness is exact and an accepted pointwise envelope gives

```text
|V_hat(y)-V(y)| <= epsilon_V(y),
```

then

```text
|W_Vhat(x,a)-W_V(x,a)|
  <= gamma sum_y P(y|x,a) epsilon_V(y).                        (10.14)
```

Taking the maximum over actions gives the `rho(x)` needed by Lemma 1. Under a
uniform value radius `epsilon_V`, one may take `rho<=gamma epsilon_V`. Learned
rewards, transitions, discount, perspective, or state aggregation require
their own error terms and a new accepted propagation rule; equation (10.14)
does not hide them.

The composite `D_tau o H o F_M^V` returns the source policy only on the
corresponding self-greedy subset. A harness that secretly looks up `pi` can
force a round trip for every scalar input, but then the behavioral information
resides in the hidden lookup. The executable reference harness exposes no
policy field.

### 5.4 Stochastic policies

For a stochastic policy, its normalized probability vector is itself a
lossless action-score representation:

```text
E_prob(pi)(x,a)=pi(a|x),
D_prob(p)(a|x)=p(x,a) / sum_b p(x,b),
```

on nonnegative rows with positive total. The maps are inverse on the normalized
simplex. An `argmax` decoder instead produces only

```text
mode_pi(x)=tau_x argmax_a pi(a|x).
```

For example, `(0.51,0.49)` and `(0.99,0.01)` share the same modal action while
their total-variation distance is `0.48`. Modal-action agreement therefore does
not certify distributional reconstruction. A stochastic claim must bind a
metric such as

```text
D_mu^TV(pi,pi_hat)=E_(x~mu) TV(pi(.|x),pi_hat(.|x))
```

or a finite KL/log-loss target with its support conventions, and must specify
whether deployment samples are coupled.

## 6. Constructive boundary fixtures

The verification suite keeps the following assumptions inspectable.

### 6.1 Hidden policy lookup in the harness

Define `H(V,x)=pi(x)` while ignoring `V`. Then every scalar function appears to
reconstruct `pi`. The construction demonstrates why harness transparency and
complexity accounting are premises: it is a valid behavioral program, but it
does not show that the scalar value carries the behavior.

### 6.2 Training equality with off-support disagreement

Let `X={x_train,x_deploy}`. Choose `W_hat=W` at `x_train` and reverse the two
scores at `x_deploy`. Training disagreement is zero under a point mass at
`x_train`; deployment disagreement is one under a point mass at `x_deploy`.
No theorem converts the first distribution into the second without a transport
or learning assumption.

### 6.3 Small and zero gaps

At `g=0`, an arbitrarily small perturbation can change a tie-broken action. At
`g` just below `2 rho`, the tightness fixture flips under coordinate error
`rho`. The theorem handles these states by exposing their mass; it does not
classify all of them as actual errors.

### 6.4 A suboptimal source policy

In a one-step state, let the source choose an action of return zero while
another legal action returns one. Then `G(Q^pi)` chooses the second action.
This constructively separates greedy improvement from reconstruction of the
source behavior.

### 6.5 Modal collapse

The stochastic example in §5.4 has exact modal agreement and substantial
distributional distance. Modal and distributional targets therefore receive
different result fields.

### 6.6 State aliasing and omitted history

Let two histories have the same visible observation `x` while the source policy
chooses `a` after the first and `b` after the second. No deterministic function
of visible `x` alone can reproduce both choices. Enlarging the domain to a
sufficient history or belief state can restore a well-typed reconstruction
problem under its declared model. The visible-state failure does not establish
that every proposed history compression is sufficient.

## 7. Pointwise, IID, and trajectory scope

The project uses three distinct claims.

### 7.1 Pointwise or training-set recovery

Equations (10.3), (10.6), and the canonical exact construction can apply to a
finite listed domain. When that domain is a training set, the conclusion ends
there. The off-support fixture is compatible with perfect training equality.

### 7.2 Held-out IID disagreement

Equation (10.7) estimates behavioral disagreement under one named `mu` for a
fixed pair. It does not show value fidelity, shared representations, or stable
performance under a different distribution. If the holdout is collected from
teacher trajectories, its target is the teacher-induced state distribution,
not every reachable state.

### 7.3 Coupled trajectory behavior

For a horizon `H`, couple the source and reconstructed process from the same
initial state and, in a stochastic environment, with declared shared
randomness until their first action split. Suppose accepted bounds give

```text
P(A_hat_t!=A_t | histories agree before t) <= epsilon_t.
```

Then

```text
P(any action split by H) <= min(1,sum_(t=0)^(H-1) epsilon_t).  (10.15)
```

This is a first-divergence union bound. Its premises concern the time-indexed
matched-history visitation distributions. A single `D_mu` under a static or
teacher-only distribution does not supply them. After a split, later state and
action comparisons require a separately chosen coupling or task-level loss.

The author's phrase “generalizes the same way a trained model generalizes” is
therefore retained as a prospective question:

> For named source and surrogate learners, training distribution, architecture,
> seeds, shift panels, and trajectory protocol, which behavioral/value
> agreements persist off the fitting sample and under induced visitation?

Output agreement alone supplies no theorem that the learners share an
inductive bias, hidden mechanism, or deployment behavior.

## 8. Value-logic integration

An accepted record can instantiate a typed behavioral atom such as

```text
DecodeStable(
  policy=vpi,
  target_scores=vW,
  surrogate=vhat,
  decoder=vD,
  harness=vH,
  population=vmu,
  risk_bound=eta,
  evidence_mode=m,
  coverage=1-alpha,
  validity=I
).
```

For an action-authorizing version of `P_surrogate-rely`, `DecodeStable` can be
required alongside the existing value/ranking, improvement, support,
counterfactual-validity, and trace requirements. A profile used only to inspect
value predictions can report behavioral fidelity without requiring decoded
action authorization. Profile refinement makes that choice explicit.

`DecodeStable` means only that the accepted record supports a bound on decoded
behavior for its named distribution and versions. It is not an alias for
`Adeq(value fidelity)`, `Improve`, `Constraint(support)`, `Trace`,
representational alignment, causal faithfulness, or human inspectability.
Consequently it cannot grant `P_surrogate-rely` alone. A raw action gap, an
estimated gap without accepted uncertainty, or a training agreement number
does not support this atom.

The semantics-backward research program also remains typed. Interpreting hidden
features of an independently trained value surrogate studies that surrogate.
A conclusion about source-policy hidden states needs an explicit alignment or
readout map to those states, followed by policy-side interventions for a causal
claim. The behavioral theorem supplies neither step.

## 9. Literature boundary

The targeted primary-source check completed on 2026-07-21 supports the
positioning below.

- Rusu et al. (`RusuEtAl2015`) train student networks from teacher action-value
  outputs and evaluate policy distillation in Atari. This is a direct
  behavioral-surrogate precedent and a necessary future baseline. It does not
  establish return semantics or internal-value recovery for every distilled
  student.
- Bellemare et al. (`BellemareEtAl2016`) explicitly motivate larger action gaps
  as reducing the effect of approximation and estimation error on greedy
  policies. Their paper studies optimality-preserving Bellman operators. The
  elementary factor-two bound here is proved independently and is not presented
  as their theorem.
- Ross, Gordon, and Bagnell (`RossGordonBagnell2011`) show why sequential
  imitation differs from IID prediction when learner actions change later
  observations, and analyze learning on induced state distributions. This
  supports the distinction between (10.7) and (10.15); it does not transfer a
  DAgger guarantee to this untrained finite theorem.
- D'Amour et al. (`DAmourEtAl2022`) document that predictors with equivalent
  in-domain validation performance can differ materially on deployment stress
  tests. This supports keeping “same generalization” as a tested property
  rather than an inference from training agreement.
- Hoeffding (`Hoeffding1963`) supplies the bounded IID concentration inequality
  used in Proposition 7. Sutton and Barto (`SuttonBarto2018`) remain the source
  for standard policy evaluation/improvement and the global self-greediness
  qualification.

These sources delimit the result and its future comparisons. Theorem 2 itself
uses only finite maximization, the triangle inequality, event inclusion, and a
union bound.

## 10. Claim disposition and handoff

Claim `C12` is now `S1` at its formal scope. The repository proves the raw
oracle inequality, its evidence-certified forms, the conservative certificate
distinction, exact arrow domains, semantic variants, and finite boundary
fixtures. No learned reconstruction experiment was run, and the result assigns
no empirical grade to the companion repository.

The optional paper section may state Theorem 2 and Corollary 5 compactly. Its
main text must keep the exact encoder-image existence proposition, the raw
`2 rho` boundary, the conservative `4 rho` sufficient condition, and the
standard-return/self-greediness qualification distinguishable. Full proofs,
the arrow diagram, IID/trajectory scope, and countermodels belong in Appendix
F if the section survives drafting pressure.

Future empirical bridge work remains gated on the companion repository's open
PyTorch migration tasks, a fresh exact commit pin, and a prospective protocol
with named distributions, baselines, thresholds, evidence roles, and
trajectory tests. This task did not run or modify the companion repository.

The next roadmap item is **Task 26 — Draft the formal paper's motivation and
related work**.
